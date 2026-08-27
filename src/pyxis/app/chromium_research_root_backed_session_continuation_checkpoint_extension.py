from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .chromium_research_fixed_anchor_cumulative_extension import (
    _FixedAnchorCumulativeExtensionAdapter,
    _FixedAnchorCumulativeExtensionMessages,
    _extend_fixed_anchor_cumulative_continuation,
)
from .chromium_research_root_backed_session_continuation_reentry_plan_document import (
    ChromiumResearchRootBackedSessionContinuationOverlayPersistenceResult,
    ChromiumResearchRootBackedSessionContinuationReentryPlan,
    ChromiumResearchRootBackedSessionContinuationReentryResult,
    _persist_overlay,
    load_chromium_research_root_backed_session_continuation_reentry_plan_document,
    reenter_chromium_research_root_backed_session_continuation,
)
from .chromium_research_session_rollover import ChromiumResearchSessionRolloverResult
from .chromium_research_working_set_note_revision_edge_sequence_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceRecord,
)
from .chromium_research_working_set_note_revision_edge_sequence_persistence import (
    ChromiumPageResearchWorkingSetNoteRevisionEdgeSequencePersistenceEvidence,
)


@dataclass(frozen=True, slots=True)
class ChromiumResearchRootBackedSessionContinuationCheckpointExtensionResult:
    """One cumulative post-root continuation checkpoint using the existing 35D format."""

    current_reentry: ChromiumResearchRootBackedSessionContinuationReentryResult
    rollover: ChromiumResearchSessionRolloverResult
    current_plan: ChromiumResearchRootBackedSessionContinuationReentryPlan
    explicit_sequence: ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceRecord
    declaration: ChromiumPageResearchWorkingSetNoteRevisionEdgeSequencePersistenceEvidence
    next_plan: ChromiumResearchRootBackedSessionContinuationReentryPlan
    fresh_reentry: ChromiumResearchRootBackedSessionContinuationReentryResult
    overlay: ChromiumResearchRootBackedSessionContinuationOverlayPersistenceResult


class ChromiumResearchRootBackedSessionContinuationCheckpointExtensionError(ValueError):
    """Raised when one 35E cumulative continuation checkpoint cannot be proven."""


def persist_chromium_research_root_backed_session_continuation_checkpoint_extension(
    current_reentry: ChromiumResearchRootBackedSessionContinuationReentryResult,
    rollover: ChromiumResearchSessionRolloverResult,
    *,
    current_overlay_source: Path,
    successor_edge_source: Path,
    cumulative_declaration_destination: Path,
    next_overlay_destination: Path,
) -> ChromiumResearchRootBackedSessionContinuationCheckpointExtensionResult:
    """Extend one persisted 35D continuation without recursive overlay ancestry.

    Concrete 35E authority remains here: the exact current plan relationship, retained
    root identity, rollover ownership, direct 35C anchor, and public 35D result/error
    types are unchanged. Shared path/relink/declaration/round-trip mechanics delegate
    to the private fixed-anchor cumulative-extension kernel proven again at 37D/40D.
    """

    if not isinstance(
        current_reentry,
        ChromiumResearchRootBackedSessionContinuationReentryResult,
    ):
        raise TypeError(
            "current_reentry must be ChromiumResearchRootBackedSessionContinuationReentryResult."
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
    return ChromiumResearchRootBackedSessionContinuationCheckpointExtensionResult(
        current_reentry=current_reentry,
        rollover=rollover,
        current_plan=kernel.current_plan,
        explicit_sequence=kernel.explicit_sequence,
        declaration=kernel.declaration,
        next_plan=kernel.next_plan,
        fresh_reentry=kernel.fresh_reentry,
        overlay=kernel.overlay,
    )


def _require_loaded_plan_match(
    current_plan: ChromiumResearchRootBackedSessionContinuationReentryPlan,
    current_reentry: ChromiumResearchRootBackedSessionContinuationReentryResult,
) -> None:
    if current_plan != current_reentry.plan:
        raise ChromiumResearchRootBackedSessionContinuationCheckpointExtensionError(
            "Explicit current 35D overlay does not describe the supplied continuation plan."
        )


def _require_current_match(
    supplied: ChromiumResearchRootBackedSessionContinuationReentryResult,
    fresh: ChromiumResearchRootBackedSessionContinuationReentryResult,
) -> None:
    if fresh.controller.presentation != supplied.controller.presentation:
        raise ChromiumResearchRootBackedSessionContinuationCheckpointExtensionError(
            "Fresh current continuation presentation does not match the supplied continuation."
        )
    if (
        fresh.controller.declared_endpoint.verification.edge_record_sha256
        != supplied.controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchRootBackedSessionContinuationCheckpointExtensionError(
            "Fresh current continuation endpoint identity does not match the supplied continuation."
        )
    if (
        fresh.prior_root_backed_reentry.loaded_root.verification.root_record_sha256
        != supplied.prior_root_backed_reentry.loaded_root.verification.root_record_sha256
    ):
        raise ChromiumResearchRootBackedSessionContinuationCheckpointExtensionError(
            "Fresh current root identity does not match the supplied continuation ancestry."
        )


def _require_rollover_prior_match(
    current: ChromiumResearchRootBackedSessionContinuationReentryResult,
    rollover: ChromiumResearchSessionRolloverResult,
) -> None:
    if rollover.prior_controller.presentation != current.controller.presentation:
        raise ChromiumResearchRootBackedSessionContinuationCheckpointExtensionError(
            "Chosen rollover does not belong to the supplied current continuation presentation."
        )
    if (
        rollover.prior_controller.declared_endpoint.verification.edge_record_sha256
        != current.controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchRootBackedSessionContinuationCheckpointExtensionError(
            "Chosen rollover prior endpoint identity does not match the current continuation."
        )


def _build_next_plan(
    current_plan: ChromiumResearchRootBackedSessionContinuationReentryPlan,
    cumulative_sources: tuple[Path, ...],
    declaration_source: Path,
) -> ChromiumResearchRootBackedSessionContinuationReentryPlan:
    return ChromiumResearchRootBackedSessionContinuationReentryPlan(
        prior_root_backed_overlay_source=current_plan.prior_root_backed_overlay_source,
        declared_edge_sources=cumulative_sources,
        declaration_source=declaration_source,
    )


def _require_next_match(
    rollover: ChromiumResearchSessionRolloverResult,
    fresh: ChromiumResearchRootBackedSessionContinuationReentryResult,
) -> None:
    fresh_endpoint = fresh.controller.declared_endpoint
    chosen_endpoint = rollover.continuation_controller.declared_endpoint
    if (
        fresh_endpoint.verification.edge_record_sha256
        != chosen_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchRootBackedSessionContinuationCheckpointExtensionError(
            "Fresh cumulative continuation endpoint identity does not match the chosen rollover."
        )
    if (
        fresh_endpoint.revision.revised_note.note_text
        != chosen_endpoint.revision.revised_note.note_text
    ):
        raise ChromiumResearchRootBackedSessionContinuationCheckpointExtensionError(
            "Fresh cumulative continuation endpoint text does not match the chosen rollover."
        )


_ADAPTER = _FixedAnchorCumulativeExtensionAdapter[
    ChromiumResearchRootBackedSessionContinuationReentryPlan,
    ChromiumResearchRootBackedSessionContinuationReentryResult,
    ChromiumResearchRootBackedSessionContinuationOverlayPersistenceResult,
](
    error_type=ChromiumResearchRootBackedSessionContinuationCheckpointExtensionError,
    messages=_FixedAnchorCumulativeExtensionMessages(
        current_decode="Explicit current 35D overlay could not be decoded.",
        current_reentry=(
            "Explicit current 35D overlay could not freshly reconstruct its continuation."
        ),
        sequence_relink=(
            "Cumulative post-root edge sequence could not be freshly relinked from the 35C anchor."
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
        overlay_decode="Persisted next 35D overlay could not be round-trip decoded.",
        overlay_round_trip=(
            "Persisted next 35D overlay did not round-trip to the exact cumulative plan."
        ),
    ),
    load_plan=load_chromium_research_root_backed_session_continuation_reentry_plan_document,
    reenter=reenter_chromium_research_root_backed_session_continuation,
    require_loaded_plan_match=_require_loaded_plan_match,
    require_current_match=_require_current_match,
    require_rollover_prior_match=_require_rollover_prior_match,
    declared_edge_sources=lambda plan: plan.declared_edge_sources,
    anchor_endpoint=(
        lambda reentry: reentry.prior_root_backed_reentry.controller.declared_endpoint
    ),
    build_next_plan=_build_next_plan,
    require_next_match=_require_next_match,
    persist_overlay=_persist_overlay,
    overlay_path=lambda overlay: overlay.path,
)


__all__ = [
    "ChromiumResearchRootBackedSessionContinuationCheckpointExtensionError",
    "ChromiumResearchRootBackedSessionContinuationCheckpointExtensionResult",
    "persist_chromium_research_root_backed_session_continuation_checkpoint_extension",
]
