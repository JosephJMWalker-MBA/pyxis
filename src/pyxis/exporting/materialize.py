from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path
import shutil
import tempfile

from .plan import ExportPlan


@dataclass(frozen=True, slots=True)
class ExportMaterializationResult:
    """Observable result of copying one validated export plan."""

    destination_root: Path
    copied_paths: tuple[Path, ...]


def _resolve_export_path(path_value: str, root: Path) -> Path:
    if not path_value:
        raise ValueError("Export paths must be non-empty.")

    relative = Path(path_value)
    if relative == Path(".") or relative.is_absolute() or ".." in relative.parts:
        raise ValueError(
            f"Export path must remain relative to the export root: {path_value!r}."
        )

    target = (root / relative).resolve()
    if target != root and root not in target.parents:
        raise ValueError(f"Export path escapes the export root: {path_value!r}.")
    return target


def _planned_paths(plan: ExportPlan) -> tuple[str, ...]:
    return (
        plan.canonical_path,
        plan.rir_path,
        plan.generation_manifest_path,
        *(product.path for product in plan.compiler_products),
    )


def materialize_export_plan(
    plan: ExportPlan,
    source_root: Path,
    destination_root: Path,
) -> ExportMaterializationResult:
    """Copy exact planned Workspace bytes into a separate export destination.

    The entire planned source set is read before export mutation begins. Every
    compiler product must still match the artifact hash recorded in the plan.
    The function never compiles, rewrites source, executes the Workspace, adds
    package metadata, or claims that the export is READY.
    """

    source = source_root.resolve()
    destination = destination_root.resolve()
    if (
        source == destination
        or source in destination.parents
        or destination in source.parents
    ):
        raise ValueError("Export source and destination must be separate trees.")
    if destination.exists():
        raise FileExistsError(f"Export destination already exists: {destination}")

    planned_paths = _planned_paths(plan)
    if len(set(planned_paths)) != len(planned_paths):
        raise ValueError("Export plan paths must be unique.")

    source_targets = tuple(
        _resolve_export_path(path_value, source) for path_value in planned_paths
    )
    destination_targets = tuple(
        _resolve_export_path(path_value, destination) for path_value in planned_paths
    )
    if len(set(source_targets)) != len(source_targets):
        raise ValueError("Export plan paths resolve to duplicate source files.")
    if len(set(destination_targets)) != len(destination_targets):
        raise ValueError("Export plan paths resolve to duplicate destination files.")

    # Preflight and snapshot every source before creating the export destination.
    source_bytes: list[bytes] = []
    for path_value, source_path in zip(planned_paths, source_targets, strict=True):
        if not source_path.is_file():
            raise FileNotFoundError(
                f"Planned export source is not a file: {path_value!r}."
            )
        source_bytes.append(source_path.read_bytes())

    product_offset = 3
    for product, payload in zip(
        plan.compiler_products,
        source_bytes[product_offset:],
        strict=True,
    ):
        artifact_sha256 = hashlib.sha256(payload).hexdigest()
        if artifact_sha256 != product.artifact_sha256:
            raise ValueError(
                f"Planned compiler product no longer matches recorded integrity: "
                f"{product.path!r}."
            )

    destination.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(
        tempfile.mkdtemp(
            prefix=f".{destination.name}.pyxis-export-",
            dir=destination.parent,
        )
    ).resolve()

    try:
        for path_value, payload in zip(planned_paths, source_bytes, strict=True):
            target = _resolve_export_path(path_value, staging)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(payload)

        if destination.exists():
            raise FileExistsError(f"Export destination already exists: {destination}")
        staging.rename(destination)
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise

    return ExportMaterializationResult(
        destination_root=destination,
        copied_paths=destination_targets,
    )
