from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

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
    load_chromium_research_working_set_note_revision_edge_sequence,
)
from .chromium_research_working_set_note_revision_edge_sequence_persistence import (
    ChromiumPageResearchWorkingSetNoteRevisionEdgeSequencePersistenceEvidence,
    persist_chromium_research_working_set_note_revision_edge_sequence,
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

    The current 35D overlay is freshly decoded and re-entered. Its fixed 35C ancestry
    anchor is retained exactly. The current ordered post-root edge tuple is extended
    by the explicitly supplied chosen successor, freshly relinked from the root-backed
    endpoint through public 26A/24C behavior, and persisted as a new cumulative 26B
    declaration. A new 35D overlay then points to the same 35C overlay, the cumulative
    edge tuple, and that new declaration.

    No existing overlay or declaration is modified or deleted. No directory scan,
    digest search, predecessor discovery, head selection, chronology inference, or
    semantic interpretation occurs.
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
            load_chromium_research_root_backed_session_continuation_reentry_plan_document(
                overlay_source
            )
        )
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchRootBackedSessionContinuationCheckpointExtensionError(
            "Explicit current 35D overlay could not be decoded."
        ) from exc
    if current_plan != current_reentry.plan:
        raise ChromiumResearchRootBackedSessionContinuationCheckpointExtensionError(
            "Explicit current 35D overlay does not describe the supplied continuation plan."
        )

    try:
        fresh_current = reenter_chromium_research_root_backed_session_continuation(
            current_plan
        )
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchRootBackedSessionContinuationCheckpointExtensionError(
            "Explicit current 35D overlay could not freshly reconstruct its continuation."
        ) from exc
    _require_current_match(current_reentry, fresh_current)
    _require_rollover_prior_match(current_reentry, rollover)

    cumulative_sources = (*current_plan.declared_edge_sources, successor_source)
    anchor = fresh_current.prior_root_backed_reentry.controller.declared_endpoint
    try:
        explicit_sequence = load_chromium_research_working_set_note_revision_edge_sequence(
            anchor,
            cumulative_sources,
        )
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchRootBackedSessionContinuationCheckpointExtensionError(
            "Cumulative post-root edge sequence could not be freshly relinked from the 35C anchor."
        ) from exc

    successor = explicit_sequence.edges[-1]
    chosen = rollover.prior_revision
    if successor.verification.edge_record_sha256 != chosen.persistence.edge_record_sha256:
        raise ChromiumResearchRootBackedSessionContinuationCheckpointExtensionError(
            "Cumulative sequence endpoint identity does not match the chosen rollover successor."
        )
    if (
        successor.revision.revised_note.note_text
        != chosen.extension.revision.revised_note.note_text
    ):
        raise ChromiumResearchRootBackedSessionContinuationCheckpointExtensionError(
            "Cumulative sequence endpoint text does not match the chosen rollover successor."
        )

    declaration = persist_chromium_research_working_set_note_revision_edge_sequence(
        explicit_sequence,
        declaration_destination,
    )
    next_plan = ChromiumResearchRootBackedSessionContinuationReentryPlan(
        prior_root_backed_overlay_source=current_plan.prior_root_backed_overlay_source,
        declared_edge_sources=tuple(cumulative_sources),
        declaration_source=declaration.path,
    )

    try:
        fresh_next = reenter_chromium_research_root_backed_session_continuation(next_plan)
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchRootBackedSessionContinuationCheckpointExtensionError(
            "New cumulative declaration could not freshly reconstruct the chosen continuation."
        ) from exc
    _require_next_match(rollover, fresh_next)

    overlay = _persist_overlay(next_plan, overlay_destination)
    try:
        decoded = load_chromium_research_root_backed_session_continuation_reentry_plan_document(
            overlay.path
        )
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchRootBackedSessionContinuationCheckpointExtensionError(
            "Persisted next 35D overlay could not be round-trip decoded."
        ) from exc
    if decoded != next_plan:
        raise ChromiumResearchRootBackedSessionContinuationCheckpointExtensionError(
            "Persisted next 35D overlay did not round-trip to the exact cumulative plan."
        )

    return ChromiumResearchRootBackedSessionContinuationCheckpointExtensionResult(
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


def _require_next_match(
    rollover: ChromiumResearchSessionRolloverResult,
    fresh: ChromiumResearchRootBackedSessionContinuationReentryResult,
) -> None:
    if fresh.controller.presentation != rollover.continuation_controller.presentation:
        raise ChromiumResearchRootBackedSessionContinuationCheckpointExtensionError(
            "Fresh cumulative continuation presentation does not match the chosen rollover."
        )
    if (
        fresh.controller.declared_endpoint.verification.edge_record_sha256
        != rollover.continuation_controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchRootBackedSessionContinuationCheckpointExtensionError(
            "Fresh cumulative continuation endpoint identity does not match the chosen rollover."
        )


__all__ = [
    "ChromiumResearchRootBackedSessionContinuationCheckpointExtensionError",
    "ChromiumResearchRootBackedSessionContinuationCheckpointExtensionResult",
    "persist_chromium_research_root_backed_session_continuation_checkpoint_extension",
]
