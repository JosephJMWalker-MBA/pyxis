from __future__ import annotations

from dataclasses import dataclass
import hashlib

from pyxis.compiler.artifacts import GeneratedArtifact
from pyxis.compiler.manifest import (
    GenerationManifest,
    generation_manifest_sha256,
    repository_ir_sha256,
)
from pyxis.rir.model import RepositoryIR


_CANONICAL_WORKSPACE_PATH = "authoring/canonical/workspace.json"
_REPOSITORY_RIR_PATH = "generated/repository.rir.json"
_GENERATION_MANIFEST_PATH = "generated/generation.manifest.json"


@dataclass(frozen=True, slots=True)
class ExportCompilerProduct:
    """One exact compiler product eligible for portable packaging."""

    path: str
    node_sha256: str
    artifact_sha256: str


@dataclass(frozen=True, slots=True)
class ExportPlan:
    """Immutable description of the current Workspace export payload.

    The plan identifies existing compiler products and persisted evidence only.
    It does not read files, copy files, compile, materialize, execute, or claim
    that an export is READY.
    """

    repository_id: str
    workspace_id: str
    rir_sha256: str
    generation_manifest_sha256: str
    canonical_path: str
    rir_path: str
    generation_manifest_path: str
    compiler_products: tuple[ExportCompilerProduct, ...]


def _artifact_sha256(artifact: GeneratedArtifact) -> str:
    return hashlib.sha256(artifact.source.encode("utf-8")).hexdigest()


def build_export_plan(
    repository: RepositoryIR,
    artifacts: tuple[GeneratedArtifact, ...],
    manifest: GenerationManifest,
) -> ExportPlan:
    """Plan packaging of exact current compiler products without filesystem work."""

    expected_rir_sha256 = repository_ir_sha256(repository)
    if manifest.rir_sha256 != expected_rir_sha256:
        raise ValueError("Generation manifest does not match the current Repository RIR.")

    if len(artifacts) != len(manifest.artifacts):
        raise ValueError("Generation manifest does not cover the current compiler products.")

    product_paths = tuple(artifact.path for artifact in artifacts)
    if len(set(product_paths)) != len(product_paths):
        raise ValueError("Compiler artifact paths must be unique.")

    planned_products: list[ExportCompilerProduct] = []
    for artifact, recorded in zip(artifacts, manifest.artifacts, strict=True):
        if artifact.path != recorded.path:
            raise ValueError("Generation manifest compiler-product order/path mismatch.")
        if artifact.node_sha256 != recorded.node_sha256:
            raise ValueError(
                f"Generation manifest node fingerprint mismatch for {artifact.path!r}."
            )

        artifact_sha256 = _artifact_sha256(artifact)
        if artifact_sha256 != recorded.artifact_sha256:
            raise ValueError(
                f"Generation manifest artifact integrity mismatch for {artifact.path!r}."
            )

        planned_products.append(
            ExportCompilerProduct(
                path=recorded.path,
                node_sha256=recorded.node_sha256,
                artifact_sha256=recorded.artifact_sha256,
            )
        )

    evidence_paths = {
        _CANONICAL_WORKSPACE_PATH,
        _REPOSITORY_RIR_PATH,
        _GENERATION_MANIFEST_PATH,
    }
    collision = evidence_paths.intersection(product_paths)
    if collision:
        raise ValueError(
            f"Compiler products collide with export evidence paths: {sorted(collision)!r}."
        )

    return ExportPlan(
        repository_id=repository.repository_id,
        workspace_id=repository.workspace.workspace_id,
        rir_sha256=manifest.rir_sha256,
        generation_manifest_sha256=generation_manifest_sha256(manifest),
        canonical_path=_CANONICAL_WORKSPACE_PATH,
        rir_path=_REPOSITORY_RIR_PATH,
        generation_manifest_path=_GENERATION_MANIFEST_PATH,
        compiler_products=tuple(planned_products),
    )
