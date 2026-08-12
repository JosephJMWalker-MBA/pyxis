from __future__ import annotations

from dataclasses import dataclass
import hashlib
from typing import Literal

from .artifacts import GeneratedArtifact
from .manifest import GenerationManifest


GenerationStatus = Literal["new", "reused", "regenerated", "removed"]


@dataclass(frozen=True, slots=True)
class ExistingArtifactIntegrity:
    """Filesystem integrity evidence for one previously compiler-owned artifact."""

    path: str
    artifact_sha256: str | None


@dataclass(frozen=True, slots=True)
class ArtifactGenerationStatus:
    """Compiler-owned classification of one artifact path for this generation."""

    path: str
    status: GenerationStatus


def _artifact_sha256(artifact: GeneratedArtifact) -> str:
    return hashlib.sha256(artifact.source.encode("utf-8")).hexdigest()


def classify_generation_statuses(
    artifacts: tuple[GeneratedArtifact, ...],
    previous_manifest: GenerationManifest | None,
    existing_integrity: tuple[ExistingArtifactIntegrity, ...],
) -> tuple[ArtifactGenerationStatus, ...]:
    """Classify current and removed compiler products without filesystem access.

    Reuse requires three facts to agree: the semantic node fingerprint is
    unchanged, the current compiler output matches the previously recorded
    artifact hash, and the existing materialized artifact still has that exact
    hash. This function only classifies; it does not decide whether writes may be
    skipped.
    """

    current_paths = tuple(artifact.path for artifact in artifacts)
    if len(set(current_paths)) != len(current_paths):
        raise ValueError("Compiler artifact paths must be unique.")

    previous_entries = previous_manifest.artifacts if previous_manifest is not None else ()
    previous_paths = tuple(entry.path for entry in previous_entries)
    if len(set(previous_paths)) != len(previous_paths):
        raise ValueError("Previous manifest artifact paths must be unique.")

    integrity_paths = tuple(entry.path for entry in existing_integrity)
    if len(set(integrity_paths)) != len(integrity_paths):
        raise ValueError("Existing artifact integrity paths must be unique.")
    if set(integrity_paths) != set(previous_paths):
        raise ValueError(
            "Existing artifact integrity must cover exactly the previous manifest paths."
        )

    previous_by_path = {entry.path: entry for entry in previous_entries}
    integrity_by_path = {entry.path: entry for entry in existing_integrity}
    current_path_set = set(current_paths)
    statuses: list[ArtifactGenerationStatus] = []

    for artifact in artifacts:
        previous = previous_by_path.get(artifact.path)
        if previous is None:
            status: GenerationStatus = "new"
        else:
            existing = integrity_by_path[artifact.path]
            current_artifact_sha256 = _artifact_sha256(artifact)
            reusable = (
                artifact.node_sha256 == previous.node_sha256
                and current_artifact_sha256 == previous.artifact_sha256
                and existing.artifact_sha256 == previous.artifact_sha256
            )
            status = "reused" if reusable else "regenerated"

        statuses.append(
            ArtifactGenerationStatus(
                path=artifact.path,
                status=status,
            )
        )

    statuses.extend(
        ArtifactGenerationStatus(path=path, status="removed")
        for path in previous_paths
        if path not in current_path_set
    )
    return tuple(statuses)
