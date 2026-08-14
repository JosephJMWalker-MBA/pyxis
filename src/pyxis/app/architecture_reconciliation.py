from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from pyxis.compiler import GenerationStatus

from .apply import ApplyResult
from .presentation import WorkspacePresentation
from .preview_presentation import ArchitecturePreviewPresentation


ProposedArtifactAction = Literal["add", "change", "remove"]


@dataclass(frozen=True, slots=True)
class ObservedArtifactGenerationPresentation:
    """One compiler generation-status fact observed after Apply."""

    path: str
    status: GenerationStatus


@dataclass(frozen=True, slots=True)
class ArchitectureApplyObservationPresentation:
    """Observed post-Apply evidence kept separate from the earlier preview."""

    revision_id: str
    operation: str
    before_canonical_sha256: str
    after_canonical_sha256: str
    completion_rir_sha256: str
    completion_generation_manifest_sha256: str
    canonical_sha256: str
    rir_sha256: str
    rir_capabilities: tuple[str, ...]
    artifact_generation: tuple[ObservedArtifactGenerationPresentation, ...]
    runtime_keys: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ArchitectureArtifactConsequenceReconciliationPresentation:
    """Mechanical comparison of one predicted compiler-product consequence."""

    path: str
    proposed_action: ProposedArtifactAction
    expected_generation_status: GenerationStatus
    observed_generation_status: GenerationStatus | None
    matches: bool


@dataclass(frozen=True, slots=True)
class ArchitectureConsequenceReconciliationPresentation:
    """Preview evidence plus distinct observed evidence and exact comparisons."""

    proposed: ArchitecturePreviewPresentation
    observed: ArchitectureApplyObservationPresentation
    revision_transition_matches_preview: bool
    observed_canonical_matches_preview: bool
    observed_rir_capabilities_match_preview: bool
    artifact_consequences: tuple[
        ArchitectureArtifactConsequenceReconciliationPresentation, ...
    ]
    observed_runtime_keys_match_preview: bool
    revision_completion_rir_matches_observed_rir: bool


def _expected_generation_status(action: ProposedArtifactAction) -> GenerationStatus:
    if action == "add":
        return "new"
    if action == "change":
        return "regenerated"
    return "removed"


def create_architecture_consequence_reconciliation(
    proposed: ArchitecturePreviewPresentation,
    applied: ApplyResult,
    observed_presentation: WorkspacePresentation,
) -> ArchitectureConsequenceReconciliationPresentation:
    """Reconcile one retained preview with evidence already produced by Apply.

    This projection performs no filesystem reads, compilation, execution,
    persistence, or rediscovery. The original preview presentation is retained
    unchanged. Post-Apply evidence is copied into a separate observed record and
    only narrow structural equalities are computed between the two.
    """

    matching_revisions = tuple(
        revision
        for revision in observed_presentation.revisions
        if revision.revision_id == applied.revision.revision_id
    )
    if len(matching_revisions) != 1:
        raise ValueError(
            "Observed Workspace presentation must contain exactly the applied revision."
        )
    revision = matching_revisions[0]
    if not revision.completed:
        raise ValueError("Applied revision must have completion evidence.")
    if revision.completion_rir_sha256 is None:
        raise ValueError("Applied revision completion RIR identity is required.")
    if revision.completion_generation_manifest_sha256 is None:
        raise ValueError(
            "Applied revision completion generation-manifest identity is required."
        )

    artifact_generation = tuple(
        ObservedArtifactGenerationPresentation(
            path=artifact.path,
            status=artifact.status,
        )
        for artifact in observed_presentation.artifacts
    )
    status_by_path = {artifact.path: artifact.status for artifact in artifact_generation}
    if len(status_by_path) != len(artifact_generation):
        raise ValueError("Observed artifact generation evidence contains duplicate paths.")

    predicted_artifact_steps = tuple(
        step
        for step in proposed.consequence_trace
        if step.stage == "compiler_product"
    )
    predicted_paths = tuple(step.subject for step in predicted_artifact_steps)
    if len(set(predicted_paths)) != len(predicted_paths):
        raise ValueError("Preview consequence trace contains duplicate artifact paths.")

    artifact_consequences: list[
        ArchitectureArtifactConsequenceReconciliationPresentation
    ] = []
    for step in predicted_artifact_steps:
        if step.action not in {"add", "change", "remove"}:
            raise ValueError("Unsupported compiler-product consequence action.")
        action: ProposedArtifactAction = step.action  # type: ignore[assignment]
        expected_status = _expected_generation_status(action)
        observed_status = status_by_path.get(step.subject)
        artifact_consequences.append(
            ArchitectureArtifactConsequenceReconciliationPresentation(
                path=step.subject,
                proposed_action=action,
                expected_generation_status=expected_status,
                observed_generation_status=observed_status,
                matches=observed_status == expected_status,
            )
        )

    observed = ArchitectureApplyObservationPresentation(
        revision_id=revision.revision_id,
        operation=revision.operation,
        before_canonical_sha256=revision.before_canonical_sha256,
        after_canonical_sha256=revision.after_canonical_sha256,
        completion_rir_sha256=revision.completion_rir_sha256,
        completion_generation_manifest_sha256=(
            revision.completion_generation_manifest_sha256
        ),
        canonical_sha256=observed_presentation.canonical.canonical_sha256,
        rir_sha256=observed_presentation.rir.rir_sha256,
        rir_capabilities=observed_presentation.rir.capabilities,
        artifact_generation=artifact_generation,
        runtime_keys=tuple(observed_presentation.runtime_result),
    )

    return ArchitectureConsequenceReconciliationPresentation(
        proposed=proposed,
        observed=observed,
        revision_transition_matches_preview=(
            observed.before_canonical_sha256 == proposed.current.canonical_sha256
            and observed.after_canonical_sha256 == proposed.proposed.canonical_sha256
        ),
        observed_canonical_matches_preview=(
            observed.canonical_sha256 == proposed.proposed.canonical_sha256
        ),
        observed_rir_capabilities_match_preview=(
            observed.rir_capabilities == proposed.proposed.capabilities
        ),
        artifact_consequences=tuple(artifact_consequences),
        observed_runtime_keys_match_preview=(
            observed.runtime_keys == proposed.proposed_runtime_keys
        ),
        revision_completion_rir_matches_observed_rir=(
            observed.completion_rir_sha256 == observed.rir_sha256
        ),
    )
