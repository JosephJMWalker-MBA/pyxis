from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .chromium_research_fixed_anchor_cumulative_extension import (
    _FixedAnchorCumulativeExtensionAdapter,
    _FixedAnchorCumulativeExtensionMessages,
    _extend_fixed_anchor_cumulative_continuation,
)
from .chromium_research_session_rollover import ChromiumResearchSessionRolloverResult
from .chromium_research_third_basis_epoch_continuation_reentry_plan_document import (
    ChromiumResearchThirdBasisEpochContinuationOverlayPersistenceResult,
    ChromiumResearchThirdBasisEpochContinuationReentryPlan,
    ChromiumResearchThirdBasisEpochContinuationReentryResult,
    _persist_overlay,
    load_chromium_research_third_basis_epoch_continuation_reentry_plan_document,
    reenter_chromium_research_third_basis_epoch_continuation,
)
from .chromium_research_working_set_note_revision_edge_sequence_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceRecord,
)
from .chromium_research_working_set_note_revision_edge_sequence_persistence import (
    ChromiumPageResearchWorkingSetNoteRevisionEdgeSequencePersistenceEvidence,
)


@dataclass(frozen=True, slots=True)
class ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionResult:
    """One cumulative post-third-root checkpoint using the existing 40C format."""

    current_reentry: ChromiumResearchThirdBasisEpochContinuationReentryResult
    rollover: ChromiumResearchSessionRolloverResult
    current_plan: ChromiumResearchThirdBasisEpochContinuationReentryPlan
    explicit_sequence: ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceRecord
    declaration: ChromiumPageResearchWorkingSetNoteRevisionEdgeSequencePersistenceEvidence
    next_plan: ChromiumResearchThirdBasisEpochContinuationReentryPlan
    fresh_reentry: ChromiumResearchThirdBasisEpochContinuationReentryResult
    overlay: ChromiumResearchThirdBasisEpochContinuationOverlayPersistenceResult


class ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionError(ValueError):
    """Raised when one 40D cumulative continuation checkpoint cannot be proven."""


def persist_chromium_research_third_basis_epoch_continuation_checkpoint_extension(
    current_reentry: ChromiumResearchThirdBasisEpochContinuationReentryResult,
    rollover: ChromiumResearchSessionRolloverResult,
    *,
    current_overlay_source: Path,
    successor_edge_source: Path,
    cumulative_declaration_destination: Path,
    next_overlay_destination: Path,
) -> ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionResult:
    """Extend one persisted 40C continuation without recursive overlay ancestry.

    Concrete 40D authority remains here: path-distinct durable current equivalence,
    retained first/second/third roots, the retained second-epoch continuation, rollover
    ownership, direct 40B anchoring, and public 40C result/error types are unchanged.
    Only the triply-proven fixed-anchor mechanics delegate to the private kernel.
    """

    if not isinstance(
        current_reentry,
        ChromiumResearchThirdBasisEpochContinuationReentryResult,
    ):
        raise TypeError(
            "current_reentry must be ChromiumResearchThirdBasisEpochContinuationReentryResult."
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
    return ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionResult(
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
    supplied: ChromiumResearchThirdBasisEpochContinuationReentryResult,
    fresh: ChromiumResearchThirdBasisEpochContinuationReentryResult,
) -> None:
    if fresh.controller.presentation != supplied.controller.presentation:
        raise ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionError(
            "Fresh current continuation presentation does not match the supplied continuation."
        )
    if (
        fresh.controller.declared_endpoint.verification.edge_record_sha256
        != supplied.controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionError(
            "Fresh current continuation endpoint identity does not match the supplied continuation."
        )

    fresh_third = fresh.prior_third_basis_epoch_reentry
    supplied_third = supplied.prior_third_basis_epoch_reentry
    if fresh_third.controller.presentation != supplied_third.controller.presentation:
        raise ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionError(
            "Fresh third-epoch anchor presentation does not match the supplied ancestry."
        )
    if (
        fresh_third.controller.declared_endpoint.verification.edge_record_sha256
        != supplied_third.controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionError(
            "Fresh third-epoch anchor endpoint identity does not match the supplied ancestry."
        )
    if (
        fresh_third.loaded_root.verification.root_record_sha256
        != supplied_third.loaded_root.verification.root_record_sha256
    ):
        raise ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionError(
            "Fresh third-root identity does not match the supplied continuation ancestry."
        )

    fresh_prior = fresh_third.prior_second_basis_epoch_continuation_reentry
    supplied_prior = supplied_third.prior_second_basis_epoch_continuation_reentry
    if fresh_prior.controller.presentation != supplied_prior.controller.presentation:
        raise ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionError(
            "Fresh retained second-epoch continuation presentation does not match the supplied ancestry."
        )
    if (
        fresh_prior.controller.declared_endpoint.verification.edge_record_sha256
        != supplied_prior.controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionError(
            "Fresh retained second-epoch continuation endpoint identity does not match the supplied ancestry."
        )

    fresh_second = fresh_prior.prior_second_basis_epoch_reentry
    supplied_second = supplied_prior.prior_second_basis_epoch_reentry
    if (
        fresh_second.loaded_root.verification.root_record_sha256
        != supplied_second.loaded_root.verification.root_record_sha256
    ):
        raise ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionError(
            "Fresh second-root identity does not match the supplied continuation ancestry."
        )
    if (
        fresh_second.prior_continuation_reentry.prior_root_backed_reentry.loaded_root.verification.root_record_sha256
        != supplied_second.prior_continuation_reentry.prior_root_backed_reentry.loaded_root.verification.root_record_sha256
    ):
        raise ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionError(
            "Fresh retained first-root identity does not match the supplied continuation ancestry."
        )


def _require_rollover_prior_match(
    current: ChromiumResearchThirdBasisEpochContinuationReentryResult,
    rollover: ChromiumResearchSessionRolloverResult,
) -> None:
    if rollover.prior_controller.presentation != current.controller.presentation:
        raise ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionError(
            "Chosen rollover does not belong to the supplied current continuation presentation."
        )
    if (
        rollover.prior_controller.declared_endpoint.verification.edge_record_sha256
        != current.controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionError(
            "Chosen rollover prior endpoint identity does not match the current continuation."
        )


def _build_next_plan(
    current_plan: ChromiumResearchThirdBasisEpochContinuationReentryPlan,
    cumulative_sources: tuple[Path, ...],
    declaration_source: Path,
) -> ChromiumResearchThirdBasisEpochContinuationReentryPlan:
    return ChromiumResearchThirdBasisEpochContinuationReentryPlan(
        prior_third_basis_epoch_overlay_source=(
            current_plan.prior_third_basis_epoch_overlay_source
        ),
        declared_edge_sources=cumulative_sources,
        declaration_source=declaration_source,
    )


def _require_next_match(
    rollover: ChromiumResearchSessionRolloverResult,
    fresh: ChromiumResearchThirdBasisEpochContinuationReentryResult,
) -> None:
    fresh_endpoint = fresh.controller.declared_endpoint
    chosen_endpoint = rollover.continuation_controller.declared_endpoint
    if (
        fresh_endpoint.verification.edge_record_sha256
        != chosen_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionError(
            "Fresh cumulative continuation endpoint identity does not match the chosen rollover."
        )
    if (
        fresh_endpoint.revision.revised_note.note_text
        != chosen_endpoint.revision.revised_note.note_text
    ):
        raise ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionError(
            "Fresh cumulative continuation endpoint text does not match the chosen rollover."
        )


_ADAPTER = _FixedAnchorCumulativeExtensionAdapter[
    ChromiumResearchThirdBasisEpochContinuationReentryPlan,
    ChromiumResearchThirdBasisEpochContinuationReentryResult,
    ChromiumResearchThirdBasisEpochContinuationOverlayPersistenceResult,
](
    error_type=ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionError,
    messages=_FixedAnchorCumulativeExtensionMessages(
        current_decode="Explicit current 40C overlay could not be decoded.",
        current_reentry=(
            "Explicit current 40C overlay could not freshly reconstruct its continuation."
        ),
        sequence_relink=(
            "Cumulative post-third-root edge sequence could not be freshly relinked from the direct 40B ancestry anchor."
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
        overlay_decode="Persisted next 40C overlay could not be round-trip decoded.",
        overlay_round_trip=(
            "Persisted next 40C overlay did not round-trip to the exact cumulative plan."
        ),
    ),
    load_plan=load_chromium_research_third_basis_epoch_continuation_reentry_plan_document,
    reenter=reenter_chromium_research_third_basis_epoch_continuation,
    require_loaded_plan_match=None,
    require_current_match=_require_current_match,
    require_rollover_prior_match=_require_rollover_prior_match,
    declared_edge_sources=lambda plan: plan.declared_edge_sources,
    anchor_endpoint=(
        lambda reentry: reentry.prior_third_basis_epoch_reentry.controller.declared_endpoint
    ),
    build_next_plan=_build_next_plan,
    require_next_match=_require_next_match,
    persist_overlay=_persist_overlay,
    overlay_path=lambda overlay: overlay.path,
)


__all__ = [
    "ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionError",
    "ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionResult",
    "persist_chromium_research_third_basis_epoch_continuation_checkpoint_extension",
]
