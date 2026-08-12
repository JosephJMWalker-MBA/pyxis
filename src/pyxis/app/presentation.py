from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Literal

from pyxis.authoring import WorkspaceSpec
from pyxis.compiler import (
    GenerationStatus,
    generation_manifest_sha256,
    repository_ir_sha256,
)
from pyxis.revisions import RevisionCompletion, RevisionEvent, canonical_sha256

from .build import BuildAndRunResult
from .export import WorkspaceExportResult


@dataclass(frozen=True, slots=True)
class CanonicalPresentation:
    """Authoritative authored Workspace identity for presentation."""

    workspace_id: str
    name: str
    description: str
    capabilities: tuple[str, ...]
    canonical_sha256: str


@dataclass(frozen=True, slots=True)
class RIRPresentation:
    """Derived compiler-input evidence for presentation."""

    schema_version: str
    repository_id: str
    workspace_id: str
    entrypoint: str
    capabilities: tuple[str, ...]
    rir_sha256: str


@dataclass(frozen=True, slots=True)
class CompilerArtifactPresentation:
    """One compiler-owned generation-status fact and current integrity identity."""

    path: str
    status: GenerationStatus
    node_sha256: str | None
    artifact_sha256: str | None


@dataclass(frozen=True, slots=True)
class RevisionPresentation:
    """One append-only revision event with optional compiler completion evidence."""

    revision_id: str
    parent_revision_id: str | None
    operation: str
    rationale: str
    before_canonical_sha256: str
    after_canonical_sha256: str
    completed: bool
    completion_rir_sha256: str | None
    completion_generation_manifest_sha256: str | None


@dataclass(frozen=True, slots=True)
class ExportPresentation:
    """Evidence-backed READY facts for one verified portable export."""

    readiness: Literal["READY"]
    export_root: Path
    rir_sha256: str
    generation_manifest_sha256: str
    input_sha256: str
    compiler_product_count: int


@dataclass(frozen=True, slots=True)
class WorkspacePresentation:
    """Small read-only application contract for a future Workspace UI.

    This object contains only facts already owned by canonical authoring,
    compiler/runtime application results, append-only revision evidence, and
    export verification. Constructing it performs no filesystem reads, writes,
    compilation, execution, export, or discovery.
    """

    canonical: CanonicalPresentation
    rir: RIRPresentation
    artifacts: tuple[CompilerArtifactPresentation, ...]
    runtime_result: Mapping[str, object]
    revisions: tuple[RevisionPresentation, ...]
    export: ExportPresentation | None


def _freeze_runtime_value(value: object) -> object:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        if not all(isinstance(key, str) for key in value):
            raise TypeError("Runtime presentation mappings require string keys.")
        return MappingProxyType(
            {
                key: _freeze_runtime_value(item)
                for key, item in value.items()
            }
        )
    if isinstance(value, (list, tuple)):
        return tuple(_freeze_runtime_value(item) for item in value)
    raise TypeError(
        "Runtime presentation supports only JSON-like scalar, mapping, and sequence values."
    )


def _freeze_runtime_result(result: dict[str, object]) -> Mapping[str, object]:
    frozen = _freeze_runtime_value(result)
    if not isinstance(frozen, Mapping):
        raise TypeError("Workspace runtime result must remain a mapping for presentation.")
    return frozen


def _present_artifacts(run: BuildAndRunResult) -> tuple[CompilerArtifactPresentation, ...]:
    manifest_by_path = {
        artifact.path: artifact
        for artifact in run.build.manifest.artifacts
    }
    if len(manifest_by_path) != len(run.build.manifest.artifacts):
        raise ValueError("Generation manifest contains duplicate artifact paths.")

    status_paths = tuple(status.path for status in run.build.generation_statuses)
    if len(set(status_paths)) != len(status_paths):
        raise ValueError("Generation status evidence contains duplicate artifact paths.")

    current_status_paths = {
        status.path
        for status in run.build.generation_statuses
        if status.status != "removed"
    }
    if current_status_paths != set(manifest_by_path):
        raise ValueError(
            "Generation status evidence does not cover exactly the current manifest artifacts."
        )

    presentations: list[CompilerArtifactPresentation] = []
    for status in run.build.generation_statuses:
        manifest_artifact = manifest_by_path.get(status.path)
        if status.status == "removed":
            if manifest_artifact is not None:
                raise ValueError("Removed artifact status conflicts with the current manifest.")
            node_sha256 = None
            artifact_sha256 = None
        else:
            if manifest_artifact is None:
                raise ValueError("Current artifact status has no matching manifest evidence.")
            node_sha256 = manifest_artifact.node_sha256
            artifact_sha256 = manifest_artifact.artifact_sha256

        presentations.append(
            CompilerArtifactPresentation(
                path=status.path,
                status=status.status,
                node_sha256=node_sha256,
                artifact_sha256=artifact_sha256,
            )
        )

    return tuple(presentations)


def _present_revisions(
    events: tuple[RevisionEvent, ...],
    completions: tuple[RevisionCompletion, ...],
) -> tuple[RevisionPresentation, ...]:
    event_ids = tuple(event.revision_id for event in events)
    if len(set(event_ids)) != len(event_ids):
        raise ValueError("Revision presentation evidence contains duplicate revision events.")

    expected_parent: str | None = None
    for event in events:
        if event.parent_revision_id != expected_parent:
            raise ValueError("Revision presentation evidence does not form one append-only chain.")
        expected_parent = event.revision_id

    completion_by_revision: dict[str, RevisionCompletion] = {}
    for completion in completions:
        if completion.revision_id in completion_by_revision:
            raise ValueError("Revision presentation evidence contains duplicate completions.")
        if completion.revision_id not in event_ids:
            raise ValueError("Revision completion references an unknown revision event.")
        completion_by_revision[completion.revision_id] = completion

    presentations: list[RevisionPresentation] = []
    for event in events:
        completion = completion_by_revision.get(event.revision_id)
        if completion is not None:
            if completion.schema_version != event.schema_version:
                raise ValueError("Revision completion schema does not match its event.")
            if completion.after_canonical_sha256 != event.after_canonical_sha256:
                raise ValueError("Revision completion canonical identity does not match its event.")

        presentations.append(
            RevisionPresentation(
                revision_id=event.revision_id,
                parent_revision_id=event.parent_revision_id,
                operation=event.operation,
                rationale=event.rationale,
                before_canonical_sha256=event.before_canonical_sha256,
                after_canonical_sha256=event.after_canonical_sha256,
                completed=completion is not None,
                completion_rir_sha256=(
                    completion.rir_sha256 if completion is not None else None
                ),
                completion_generation_manifest_sha256=(
                    completion.generation_manifest_sha256
                    if completion is not None
                    else None
                ),
            )
        )

    return tuple(presentations)


def _present_export(
    run: BuildAndRunResult,
    export: WorkspaceExportResult | None,
    *,
    rir_sha256: str,
) -> ExportPresentation | None:
    if export is None:
        return None

    verification = export.verification
    identity = verification.identity
    runtime = verification.runtime
    repository = run.build.repository
    manifest_sha256 = generation_manifest_sha256(run.build.manifest)

    if verification.readiness != "READY":
        raise ValueError("Workspace export presentation requires READY verification evidence.")
    if identity.repository_id != repository.repository_id:
        raise ValueError("Export evidence refers to a different Repository.")
    if identity.workspace_id != repository.workspace.workspace_id:
        raise ValueError("Export evidence refers to a different Workspace.")
    if identity.rir_sha256 != rir_sha256:
        raise ValueError("Export evidence does not match the presented RIR identity.")
    if identity.generation_manifest_sha256 != manifest_sha256:
        raise ValueError("Export evidence does not match the current generation manifest.")
    if runtime.export_root != identity.export_root:
        raise ValueError("Export identity and runtime evidence refer to different roots.")
    if runtime.repository_id != identity.repository_id:
        raise ValueError("Export identity and runtime evidence refer to different Repositories.")
    if runtime.workspace_id != identity.workspace_id:
        raise ValueError("Export identity and runtime evidence refer to different Workspaces.")

    return ExportPresentation(
        readiness=verification.readiness,
        export_root=identity.export_root,
        rir_sha256=identity.rir_sha256,
        generation_manifest_sha256=identity.generation_manifest_sha256,
        input_sha256=runtime.input_sha256,
        compiler_product_count=len(identity.compiler_products),
    )


def create_workspace_presentation(
    spec: WorkspaceSpec,
    run: BuildAndRunResult,
    *,
    revision_events: tuple[RevisionEvent, ...] = (),
    revision_completions: tuple[RevisionCompletion, ...] = (),
    export: WorkspaceExportResult | None = None,
) -> WorkspacePresentation:
    """Compose one read-only Workspace presentation from existing evidence only."""

    repository = run.build.repository
    workspace = repository.workspace
    if (
        workspace.workspace_id != spec.workspace_id
        or workspace.name != spec.name
        or workspace.description != spec.description
        or workspace.capabilities != spec.capabilities
    ):
        raise ValueError("Canonical Workspace evidence does not match the build RIR.")

    rir_sha256 = repository_ir_sha256(repository)
    if run.build.manifest.rir_sha256 != rir_sha256:
        raise ValueError("Generation manifest does not match the build RIR identity.")

    canonical = CanonicalPresentation(
        workspace_id=spec.workspace_id,
        name=spec.name,
        description=spec.description,
        capabilities=spec.capabilities,
        canonical_sha256=canonical_sha256(spec),
    )
    rir = RIRPresentation(
        schema_version=repository.schema_version,
        repository_id=repository.repository_id,
        workspace_id=workspace.workspace_id,
        entrypoint=workspace.entrypoint,
        capabilities=workspace.capabilities,
        rir_sha256=rir_sha256,
    )

    return WorkspacePresentation(
        canonical=canonical,
        rir=rir,
        artifacts=_present_artifacts(run),
        runtime_result=_freeze_runtime_result(run.runtime_result),
        revisions=_present_revisions(revision_events, revision_completions),
        export=_present_export(run, export, rir_sha256=rir_sha256),
    )
