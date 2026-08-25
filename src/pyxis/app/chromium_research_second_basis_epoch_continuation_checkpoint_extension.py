from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

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
    load_chromium_research_working_set_note_revision_edge_sequence,
)
from .chromium_research_working_set_note_revision_edge_sequence_persistence import (
    ChromiumPageResearchWorkingSetNoteRevisionEdgeSequencePersistenceEvidence,
    persist_chromium_research_working_set_note_revision_edge_sequence,
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

    The explicit current 37C overlay is freshly decoded and re-entered. Its fixed 37B
    ancestry anchor is retained. The current ordered post-second-root edge tuple is
    extended by the explicitly supplied chosen successor, freshly relinked from the
    second-epoch endpoint, and persisted as a new cumulative 26B declaration. A new
    37C overlay then points to the same 37B overlay, the cumulative edge tuple, and
    that new declaration.

    Whole-presentation equality to the one-hop rollover is intentionally not required
    after cumulative extension. The cumulative controller presents a longer declared
    segment, so chosen terminal equivalence is established by durable terminal edge
    identity plus exact final human wording.

    The current overlay path is location rather than content identity. A path-distinct
    current 37C overlay may therefore be accepted only when fresh reconstruction proves
    the same current continuation and both retained basis-change roots.
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
        raise ValueError("cumulative declaration and next overlay destinations must be distinct.")
    if declaration_destination.exists():
        raise FileExistsError("cumulative_declaration_destination already exists.")
    if overlay_destination.exists():
        raise FileExistsError("next_overlay_destination already exists.")

    try:
        current_plan = (
            load_chromium_research_second_basis_epoch_continuation_reentry_plan_document(
                overlay_source
            )
        )
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionError(
            "Explicit current 37C overlay could not be decoded."
        ) from exc

    try:
        fresh_current = reenter_chromium_research_second_basis_epoch_continuation(
            current_plan
        )
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionError(
            "Explicit current 37C overlay could not freshly reconstruct its continuation."
        ) from exc
    _require_current_match(current_reentry, fresh_current)
    _require_rollover_prior_match(current_reentry, rollover)

    cumulative_sources = (*current_plan.declared_edge_sources, successor_source)
    anchor = fresh_current.prior_second_basis_epoch_reentry.controller.declared_endpoint
    try:
        explicit_sequence = load_chromium_research_working_set_note_revision_edge_sequence(
            anchor,
            cumulative_sources,
        )
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionError(
            "Cumulative post-second-root edge sequence could not be freshly relinked from the 37B anchor."
        ) from exc

    successor = explicit_sequence.edges[-1]
    chosen = rollover.prior_revision
    if successor.verification.edge_record_sha256 != chosen.persistence.edge_record_sha256:
        raise ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionError(
            "Cumulative sequence endpoint identity does not match the chosen rollover successor."
        )
    if (
        successor.revision.revised_note.note_text
        != chosen.extension.revision.revised_note.note_text
    ):
        raise ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionError(
            "Cumulative sequence endpoint text does not match the chosen rollover successor."
        )

    declaration = persist_chromium_research_working_set_note_revision_edge_sequence(
        explicit_sequence,
        declaration_destination,
    )
    next_plan = ChromiumResearchSecondBasisEpochContinuationReentryPlan(
        prior_second_basis_epoch_overlay_source=(
            current_plan.prior_second_basis_epoch_overlay_source
        ),
        declared_edge_sources=tuple(cumulative_sources),
        declaration_source=declaration.path,
    )

    try:
        fresh_next = reenter_chromium_research_second_basis_epoch_continuation(next_plan)
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionError(
            "New cumulative declaration could not freshly reconstruct the chosen continuation."
        ) from exc
    _require_next_match(rollover, fresh_next)

    overlay = _persist_overlay(next_plan, overlay_destination)
    try:
        decoded = load_chromium_research_second_basis_epoch_continuation_reentry_plan_document(
            overlay.path
        )
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionError(
            "Persisted next 37C overlay could not be round-trip decoded."
        ) from exc
    if decoded != next_plan:
        raise ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionError(
            "Persisted next 37C overlay did not round-trip to the exact cumulative plan."
        )

    return ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionResult(
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


__all__ = [
    "ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionError",
    "ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionResult",
    "persist_chromium_research_second_basis_epoch_continuation_checkpoint_extension",
]
