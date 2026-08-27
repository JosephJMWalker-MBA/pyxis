from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

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
    load_chromium_research_working_set_note_revision_edge_sequence,
)
from .chromium_research_working_set_note_revision_edge_sequence_persistence import (
    ChromiumPageResearchWorkingSetNoteRevisionEdgeSequencePersistenceEvidence,
    persist_chromium_research_working_set_note_revision_edge_sequence,
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

    The exact current 40C overlay is freshly decoded and re-entered. Its direct 40B
    ancestry anchor is retained, which in turn freshly reconstructs first-, second-,
    and third-root ancestry. The current ordered post-third-root edge tuple is then
    extended by one explicitly supplied chosen successor, freshly relinked from the
    third-epoch endpoint, and persisted as a new cumulative declaration. The next
    overlay reuses the existing 40C format and still points directly to the same 40B
    overlay rather than to the current 40C overlay.

    Whole-presentation equality to the one-hop rollover is intentionally not required
    after cumulative extension because the cumulative controller presents a longer
    declared segment. Terminal authority is instead checked by durable terminal edge
    identity and exact final human note text.

    Paths remain location context only. A path-distinct current 40C overlay may be
    accepted only when explicit fresh reconstruction proves the same continuation and
    retained three-root ancestry. No path or successor is discovered automatically.
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
    for value, label in (
        (current_overlay_source, "current_overlay_source"),
        (successor_edge_source, "successor_edge_source"),
        (cumulative_declaration_destination, "cumulative_declaration_destination"),
        (next_overlay_destination, "next_overlay_destination"),
    ):
        if not isinstance(value, Path):
            raise TypeError(f"{label} must be pathlib.Path.")

    overlay_source = current_overlay_source.resolve()
    successor_source = successor_edge_source.resolve()
    declaration_destination = cumulative_declaration_destination.resolve()
    overlay_destination = next_overlay_destination.resolve()

    if declaration_destination == overlay_destination:
        raise ValueError(
            "cumulative declaration and next overlay destinations must be distinct."
        )
    if declaration_destination.exists():
        raise FileExistsError("cumulative_declaration_destination already exists.")
    if overlay_destination.exists():
        raise FileExistsError("next_overlay_destination already exists.")

    try:
        current_plan = (
            load_chromium_research_third_basis_epoch_continuation_reentry_plan_document(
                overlay_source
            )
        )
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionError(
            "Explicit current 40C overlay could not be decoded."
        ) from exc

    try:
        fresh_current = reenter_chromium_research_third_basis_epoch_continuation(
            current_plan
        )
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionError(
            "Explicit current 40C overlay could not freshly reconstruct its continuation."
        ) from exc

    _require_current_match(current_reentry, fresh_current)
    _require_rollover_prior_match(current_reentry, rollover)

    cumulative_sources = (*current_plan.declared_edge_sources, successor_source)
    anchor = fresh_current.prior_third_basis_epoch_reentry.controller.declared_endpoint
    try:
        explicit_sequence = load_chromium_research_working_set_note_revision_edge_sequence(
            anchor,
            cumulative_sources,
        )
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionError(
            "Cumulative post-third-root edge sequence could not be freshly relinked from the direct 40B ancestry anchor."
        ) from exc

    successor = explicit_sequence.edges[-1]
    chosen = rollover.prior_revision
    if successor.verification.edge_record_sha256 != chosen.persistence.edge_record_sha256:
        raise ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionError(
            "Cumulative sequence endpoint identity does not match the chosen rollover successor."
        )
    if (
        successor.revision.revised_note.note_text
        != chosen.extension.revision.revised_note.note_text
    ):
        raise ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionError(
            "Cumulative sequence endpoint text does not match the chosen rollover successor."
        )

    declaration = persist_chromium_research_working_set_note_revision_edge_sequence(
        explicit_sequence,
        declaration_destination,
    )
    next_plan = ChromiumResearchThirdBasisEpochContinuationReentryPlan(
        prior_third_basis_epoch_overlay_source=(
            current_plan.prior_third_basis_epoch_overlay_source
        ),
        declared_edge_sources=tuple(cumulative_sources),
        declaration_source=declaration.path,
    )

    try:
        fresh_next = reenter_chromium_research_third_basis_epoch_continuation(next_plan)
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionError(
            "New cumulative declaration could not freshly reconstruct the chosen continuation."
        ) from exc
    _require_next_match(rollover, fresh_next)

    overlay = _persist_overlay(next_plan, overlay_destination)
    try:
        decoded = load_chromium_research_third_basis_epoch_continuation_reentry_plan_document(
            overlay.path
        )
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionError(
            "Persisted next 40C overlay could not be round-trip decoded."
        ) from exc
    if decoded != next_plan:
        raise ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionError(
            "Persisted next 40C overlay did not round-trip to the exact cumulative plan."
        )

    return ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionResult(
        current_reentry=current_reentry,
        rollover=rollover,
        current_plan=current_plan,
        explicit_sequence=explicit_sequence,
        declaration=declaration,
        next_plan=next_plan,
        fresh_reentry=fresh_next,
        overlay=overlay,
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


__all__ = [
    "ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionError",
    "ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionResult",
    "persist_chromium_research_third_basis_epoch_continuation_checkpoint_extension",
]
