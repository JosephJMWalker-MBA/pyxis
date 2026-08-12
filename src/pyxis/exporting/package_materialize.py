from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path

from .package_plan import PackageLayoutPlan


@dataclass(frozen=True, slots=True)
class PackageMaterializationResult:
    """Observable filesystem consequence of one package-layout materialization."""

    portable_root: Path
    compiler_projection_paths: tuple[Path, ...]
    support_paths: tuple[Path, ...]


def _resolve_package_path(path_value: str, root: Path) -> Path:
    if not path_value:
        raise ValueError("Package materialization paths must be non-empty.")

    relative = Path(path_value)
    if relative == Path(".") or relative.is_absolute() or ".." in relative.parts:
        raise ValueError(
            f"Package materialization path must remain relative: {path_value!r}."
        )

    target = (root / relative).resolve()
    if target != root and root not in target.parents:
        raise ValueError(
            f"Package materialization path escapes the portable root: {path_value!r}."
        )
    return target


def materialize_package_layout(
    plan: PackageLayoutPlan,
    portable_root: Path,
) -> PackageMaterializationResult:
    """Add exact compiler projections and packaging support to a portable export.

    Compiler products are read from their existing exported ``generated/`` paths,
    verified against the hashes recorded in the package plan, and copied byte for
    byte into their planned package paths. Packaging support files are the only
    newly-authored bytes. Existing generated compiler products are never modified.
    This function does not compile, build a distribution, install, or execute.
    """

    root = portable_root.resolve()
    if not root.is_dir():
        raise FileNotFoundError(f"Portable export root does not exist: {root}")

    source_paths = tuple(
        _resolve_package_path(projection.source_path, root)
        for projection in plan.compiler_projections
    )
    projection_targets = tuple(
        _resolve_package_path(projection.package_path, root)
        for projection in plan.compiler_projections
    )
    support_targets = tuple(
        _resolve_package_path(support.path, root)
        for support in plan.support_files
    )
    target_paths = (*projection_targets, *support_targets)

    if len(set(source_paths)) != len(source_paths):
        raise ValueError("Package compiler projection sources must be unique.")
    if len(set(target_paths)) != len(target_paths):
        raise ValueError("Package materialization targets must be unique.")
    if set(source_paths).intersection(target_paths):
        raise ValueError("Package materialization targets must not overwrite compiler sources.")

    # Preflight every source and target before any package mutation occurs.
    compiler_bytes: list[bytes] = []
    for projection, source_path in zip(
        plan.compiler_projections,
        source_paths,
        strict=True,
    ):
        if not source_path.is_file():
            raise FileNotFoundError(
                f"Projected compiler source is not a file: {projection.source_path!r}."
            )
        payload = source_path.read_bytes()
        artifact_sha256 = hashlib.sha256(payload).hexdigest()
        if artifact_sha256 != projection.artifact_sha256:
            raise ValueError(
                f"Projected compiler source no longer matches recorded integrity: "
                f"{projection.source_path!r}."
            )
        compiler_bytes.append(payload)

    for target in target_paths:
        if target.exists():
            raise FileExistsError(f"Planned package target already exists: {target}")

    created_files: list[Path] = []
    try:
        for target, payload in zip(
            projection_targets,
            compiler_bytes,
            strict=True,
        ):
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(payload)
            created_files.append(target)

        for support, target in zip(plan.support_files, support_targets, strict=True):
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(support.source.encode("utf-8"))
            created_files.append(target)
    except Exception:
        for created in reversed(created_files):
            created.unlink(missing_ok=True)
        for directory in sorted(
            {path.parent for path in target_paths},
            key=lambda path: len(path.parts),
            reverse=True,
        ):
            current = directory
            while current != root and root in current.parents:
                try:
                    current.rmdir()
                except OSError:
                    break
                current = current.parent
        raise

    return PackageMaterializationResult(
        portable_root=root,
        compiler_projection_paths=projection_targets,
        support_paths=support_targets,
    )
