from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .artifacts import GeneratedArtifact
from .manifest import GenerationManifest


@dataclass(frozen=True, slots=True)
class MaterializationResult:
    """Observable filesystem consequence of one artifact materialization pass."""

    written_paths: tuple[Path, ...]
    removed_paths: tuple[Path, ...]


def _resolve_artifact_target(path_value: str, root: Path) -> Path:
    relative = Path(path_value)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(
            f"Artifact path must remain relative to the destination: {path_value!r}."
        )

    target = (root / relative).resolve()
    if target != root and root not in target.parents:
        raise ValueError(
            f"Artifact path escapes the destination: {path_value!r}."
        )
    return target


def materialize_artifacts(
    artifacts: tuple[GeneratedArtifact, ...],
    destination_root: Path,
) -> tuple[Path, ...]:
    """Write an already-compiled artifact set beneath one destination root.

    This function does not compile, interpret, or execute generated code. It
    materializes the artifact paths and source exactly as provided by the
    compiler result.
    """

    root = destination_root.resolve()
    written: list[Path] = []

    for artifact in artifacts:
        target = _resolve_artifact_target(artifact.path, root)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(artifact.source, encoding="utf-8")
        written.append(target)

    return tuple(written)


def reconcile_materialized_artifacts(
    artifacts: tuple[GeneratedArtifact, ...],
    previous_manifest: GenerationManifest | None,
    destination_root: Path,
) -> MaterializationResult:
    """Write current compiler products and remove only previously owned stale ones.

    Prior ownership comes exclusively from the previous generation manifest.
    This function does not scan the filesystem to infer generated artifacts and
    does not make incremental reuse or status decisions.
    """

    root = destination_root.resolve()
    current_paths = tuple(artifact.path for artifact in artifacts)
    if len(set(current_paths)) != len(current_paths):
        raise ValueError("Compiler artifact paths must be unique.")

    previous_paths = (
        tuple(entry.path for entry in previous_manifest.artifacts)
        if previous_manifest is not None
        else ()
    )
    if len(set(previous_paths)) != len(previous_paths):
        raise ValueError("Previous manifest artifact paths must be unique.")

    current_path_set = set(current_paths)
    stale_paths = tuple(
        path for path in previous_paths if path not in current_path_set
    )

    # Validate every path before mutating the filesystem.
    for path in (*current_paths, *stale_paths):
        _resolve_artifact_target(path, root)

    written_paths = materialize_artifacts(artifacts, root)
    removed: list[Path] = []

    for path in stale_paths:
        target = _resolve_artifact_target(path, root)
        if not target.exists():
            continue
        if target.is_dir():
            raise ValueError(
                f"Stale compiler artifact path is a directory: {path!r}."
            )
        target.unlink()
        removed.append(target)

    return MaterializationResult(
        written_paths=written_paths,
        removed_paths=tuple(removed),
    )
