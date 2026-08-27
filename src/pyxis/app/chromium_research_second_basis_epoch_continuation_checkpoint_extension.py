from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .chromium_research_fixed_anchor_cumulative_extension import (
    _FixedAnchorCumulativeExtensionAdapter,
    _FixedAnchorCumulativeExtensionMessages,
    _extend_fixed_anchor_cumulative_continuation,
)
from .chromium_research_second_basis_epoch_continuation_reentry_plan_document import (
    ChromiumResearchSecondBasisEpochContinuationOverlayPersistenceResult,
    ChromiumResearchSecondBasisEpochContinuationReentryPlan,
    ChromiumResearchSecondBasisEpochContinuationReentryResult,
    _persist_overlay,
    load_chromium_research_second_basis_epoch_continuation_reentry_plan_document,
    reenter_chromium_research_second_basis_epoch_continuation,
)
from .chromium_research_session_rollover import ChromiumResearchSessionRolloverResult
from .chromium_research_working_set_note_revision_edge_sequence_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceRecord,
)
from .chromium_research_working_set_note_revision_edge_sequence_persistence import (
    ChromiumPageResearchWorkingSetNoteRevisionEdgeSequencePersistenceEvidence,
)


@dataclass(frozen=True, slots=True)
class ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionResult:
    """One cumulative post-second-root checkpoint using the existing 37C format."""

    current_reentry: ChromiumResearchSecondBasisEpochContinuationReentryResult
    rollover: ChromiumResearchSessionRolloverResult
    current_plan: ChromiumResearchSecondBasisEpochContinuationReentryPlan
    explicit_sequence: ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceRecord
    declaration: ChromiumPageResearchWorkingSetNoteRevisionEdgeSequencePersistenceEvidence
    next_plan: ChromiumResearchSecondBasisEpochContinuationReentryPlan
    fresh_reentry: ChromiumResearchSecondBasisEpochContinuationReentryResult
    overlay: ChromiumResearchSecondBasisEpochContinuationOverlayPersistenceResult


class ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionError(ValueError):
    """Raised when one 37D cumulative continuation checkpoint cannot be proven."""


def persist_chromium_research_second_basis_epoch_continuation_checkpoint_extension(
    current_reentry: ChromiumResearchSecondBasisEpochContinuationReentryResult,
    rollover: ChromiumResearchSessionRolloverResult,
    *,
    current_overlay_source: Path,
    successor_edge_source: Path,
    cumulative_declaration_destination: Path,
    next_overlay_destination: Path,
) -> ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionResult:
    """Extend one persisted 37C continuation without recursive overlay ancestry.

    Concrete 37D authority remains here: path-distinct durable current equivalence,
    retained first/second roots, rollover ownership, the direct 37B anchor, and public
    37C result/error types remain unchanged. Only triply-proven fixed-anchor mechanics
    delegate to the private cumulative-extension kernel.
    """

    if not isinstance(
        current_reentry,
        ChromiumResearchSecondBasisEpochContinuationReentryResult,
    ):
        raise TypeError(
            "current_reentry must be ChromiumResearchSecondBasisEpochContinuationReentryResult."
        )
    if not isinstance(rollover, ChromiumResearchSessionRolloverResult):
        raise TypeError("rollover must be ChromiumResearchSessionRolloverResult.")

    kernel = _extend_fixed_anchor_cumulative_continuation(
        current_reentry,
        rollover,
        current_overlay_source=current_overlay_source,
        successor_edge_source=successor_edge_source,
        cumulative_declaration_destination=cumulative_declaration_destination,
        next_overlay_destination=next_overlay_destination,
        adapter=_ADAPTER,
    )
    return ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionResult(
        current_reentry=current_reentry,
        rollover=rollover,
        current_plan=kernel.current_plan,
        explicit_sequence=kernel.explicit_sequence,
        declaration=kernel.declaration,
        next_plan=kernel.next_plan,
        fresh_reentry=kernel.fresh_reentry,
        overlay=kernel.overlay,
    )


def _require_current_match(
    supplied: ChromiumResearchSecondBasisEpochContinuationReentryResult,
    fresh: ChromiumResearchSecondBasisEpochContinuationReentryResult,
) -> None:
    if fresh.controller.presentation != supplied.controller.presentation:
        raise ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionError(
            "Fresh current continuation presentation does not match the supplied continuation."
        )
    if (
        fresh.controller.declared_endpoint.verification.edge_record_sha256
        != supplied.controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionError(
            "Fresh current continuation endpoint identity does not match the supplied continuation."
        )

    fresh_second = fresh.prior_second_basis_epoch_reentry
    supplied_second = supplied.prior_second_basis_epoch_reentry
    if fresh_second.controller.presentation != supplied_second.controller.presentation:
        raise ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionError(
            "Fresh second-epoch anchor presentation does not match the supplied ancestry."
        )
    if (
        fresh_second.controller.declared_endpoint.verification.edge_record_sha256
        != supplied_second.controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionError(
            "Fresh second-epoch anchor endpoint identity does not match the supplied ancestry."
        )
    if (
        fresh_second.loaded_root.verification.root_record_sha256
        != supplied_second.loaded_root.verification.root_record_sha256
    ):
        raise ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionError(
            "Fresh second-root identity does not match the supplied continuation ancestry."
        )
    if (
        fresh_second.prior_continuation_reentry.prior_root_backed_reentry.loaded_root.verification.root_record_sha256
        != supplied_second.prior_continuation_reentry.prior_root_backed_reentry.loaded_root.verification.root_record_sha256
    ):
        raise ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionError(
            "Fresh retained first-root identity does not match the supplied continuation ancestry."
        )


def _require_rollover_prior_match(
    current: ChromiumResearchSecondBasisEpochContinuationReentryResult,
    rollover: ChromiumResearchSessionRolloverResult,
) -> None:
    if rollover.prior_controller.presentation != current.controller.presentation:
        raise ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionError(
            "Chosen rollover does not belong to the supplied current continuation presentation."
        )
    if (
        rollover.prior_controller.declared_endpoint.verification.edge_record_sha256
        != current.controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionError(
            "Chosen rollover prior endpoint identity does not match the current continuation."
        )


def _build_next_plan(
    current_plan: ChromiumResearchSecondBasisEpochContinuationReentryPlan,
    cumulative_sources: tuple[Path, ...],
    declaration_source: Path,
) -> ChromiumResearchSecondBasisEpochContinuationReentryPlan:
    return ChromiumResearchSecondBasisEpochContinuationReentryPlan(
        prior_second_basis_epoch_overlay_source=(
            current_plan.prior_second_basis_epoch_overlay_source
        ),
        declared_edge_sources=cumulative_sources,
        declaration_source=declaration_source,
    )


def _require_next_match(
    rollover: ChromiumResearchSessionRolloverResult,
    fresh: ChromiumResearchSecondBasisEpochContinuationReentryResult,
) -> None:
    fresh_endpoint = fresh.controller.declared_endpoint
    chosen_endpoint = rollover.continuation_controller.declared_endpoint
    if (
        fresh_endpoint.verification.edge_record_sha256
        != chosen_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionError(
            "Fresh cumulative continuation endpoint identity does not match the chosen rollover."
        )
    if (
        fresh_endpoint.revision.revised_note.note_text
        != chosen_endpoint.revision.revised_note.note_text
    ):
        raise ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionError(
            "Fresh cumulative continuation endpoint text does not match the chosen rollover."
        )


_ADAPTER = _FixedAnchorCumulativeExtensionAdapter[
    ChromiumResearchSecondBasisEpochContinuationReentryPlan,
    ChromiumResearchSecondBasisEpochContinuationReentryResult,
    ChromiumResearchSecondBasisEpochContinuationOverlayPersistenceResult,
](
    error_type=ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionError,
    messages=_FixedAnchorCumulativeExtensionMessages(
        current_decode="Explicit current 37C overlay could not be decoded.",
        current_reentry=(
            "Explicit current 37C overlay could not freshly reconstruct its continuation."
        ),
        sequence_relink=(
            "Cumulative post-second-root edge sequence could not be freshly relinked from the 37B anchor."
        ),
        terminal_identity=(
            "Cumulative sequence endpoint identity does not match the chosen rollover successor."
        ),
        terminal_text=(
            "Cumulative sequence endpoint text does not match the chosen rollover successor."
        ),
        next_reentry=(
            "New cumulative declaration could not freshly reconstruct the chosen continuation."
        ),
        overlay_decode="Persisted next 37C overlay could not be round-trip decoded.",
        overlay_round_trip=(
            "Persisted next 37C overlay did not round-trip to the exact cumulative plan."
        ),
    ),
    load_plan=load_chromium_research_second_basis_epoch_continuation_reentry_plan_document,
    reenter=reenter_chromium_research_second_basis_epoch_continuation,
    require_loaded_plan_match=None,
    require_current_match=_require_current_match,
    require_rollover_prior_match=_require_rollover_prior_match,
    declared_edge_sources=lambda plan: plan.declared_edge_sources,
    anchor_endpoint=(
        lambda reentry: reentry.prior_second_basis_epoch_reentry.controller.declared_endpoint
    ),
    build_next_plan=_build_next_plan,
    require_next_match=_require_next_match,
    persist_overlay=_persist_overlay,
    overlay_path=lambda overlay: overlay.path,
)


__all__ = [
    "ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionError",
    "ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionResult",
    "persist_chromium_research_second_basis_epoch_continuation_checkpoint_extension",
]
