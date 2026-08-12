from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path

from .artifacts import GeneratedArtifact
from .manifest import GenerationManifest
from .status import ArtifactGenerationStatus, ExistingArtifactIntegrity


@dataclass(frozen=True, slots=True)
class MaterializationResult:
    """Observable filesystem consequence of one artifact materialization pass."""

    written_paths: tuple[Path, ...]
    reused_paths: tuple[Path, ...]
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


def inspect_materialized_artifact_integrity(
    previous_manifest: GenerationManifest | None,
    destination_root: Path,
) -> tuple[ExistingArtifactIntegrity, ...]:
    """Read hashes only for paths previously declared as compiler products.

    Missing or non-file paths are recorded with no hash. This function does not
    scan the generated tree, infer ownership, compile, or mutate the filesystem.
    """

    if previous_manifest is None:
        return ()

    root = destination_root.resolve()
    evidence: list[ExistingArtifactIntegrity] = []

    for entry in previous_manifest.artifacts:
        target = _resolve_artifact_target(entry.path, root)
        artifact_sha256 = (
            hashlib.sha256(target.read_bytes()).hexdigest()
            if target.is_file()
            else None
        )
        evidence.append(
            ExistingArtifactIntegrity(
                path=entry.path,
                artifact_sha256=artifact_sha256,
            )
        )

    return tuple(evidence)


def materialize_artifacts(
    artifacts: tuple[GeneratedArtifact, ...],
    destination_root: Path,
) -> tuple[Path, ...]:
    """Write an already-compiled artifact set beneath one destination root.

    This function does not compile, interpret, or execute generated code. It
    materializes the artifact paths and exact UTF-8 source bytes provided by the
    compiler result.
    """

    root = destination_root.resolve()
    written: list[Path] = []

    for artifact in artifacts:
        target = _resolve_artifact_target(artifact.path, root)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(artifact.source.encode("utf-8"))
        written.append(target)

    return tuple(written)


def reconcile_materialized_artifacts(
    artifacts: tuple[GeneratedArtifact, ...],
    generation_statuses: tuple[ArtifactGenerationStatus, ...],
    previous_manifest: GenerationManifest | None,
    destination_root: Path,
) -> MaterializationResult:
    """Materialize current compiler products from proven generation statuses.

    Only artifacts classified as ``new`` or ``regenerated`` are written.
    ``reused`` artifacts are preserved in place, and ``removed`` paths are
    deleted only when prior ownership is proven by the previous manifest. This
    function consumes compiler status evidence; it does not classify artifacts.
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
    expected_status_paths = (*current_paths, *stale_paths)
    status_paths = tuple(entry.path for entry in generation_statuses)
    if len(set(status_paths)) != len(status_paths):
        raise ValueError("Generation status paths must be unique.")
    if set(status_paths) != set(expected_status_paths):
        raise ValueError(
            "Generation statuses must cover exactly current and removed artifact paths."
        )

    status_by_path = {entry.path: entry.status for entry in generation_statuses}
    for path in current_paths:
        if status_by_path[path] not in {"new", "reused", "regenerated"}:
            raise ValueError(
                f"Current compiler artifact has invalid status: {path!r}."
            )
    for path in stale_paths:
        if status_by_path[path] != "removed":
            raise ValueError(
                f"Stale compiler artifact must have removed status: {path!r}."
            )

    # Validate every path before mutating the filesystem.
    for path in expected_status_paths:
        _resolve_artifact_target(path, root)

    reused: list[Path] = []
    artifacts_to_write: list[GeneratedArtifact] = []
    for artifact in artifacts:
        status = status_by_path[artifact.path]
        if status == "reused":
            target = _resolve_artifact_target(artifact.path, root)
            if not target.is_file():
                raise ValueError(
                    f"Reused compiler artifact is not a file: {artifact.path!r}."
                )
            reused.append(target)
        else:
            artifacts_to_write.append(artifact)

    written_paths = materialize_artifacts(tuple(artifacts_to_write), root)
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
        reused_paths=tuple(reused),
        removed_paths=tuple(removed),
    )
