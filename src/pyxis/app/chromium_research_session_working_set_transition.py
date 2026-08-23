from __future__ import annotations

from dataclasses import dataclass

from .chromium_research_session_controller import ChromiumResearchSessionController
from .chromium_research_session_presentation import present_chromium_research_session
from .chromium_research_session_working_set_extension import (
    ChromiumResearchSessionWorkingSetExtensionPersistenceResult,
)
from .chromium_research_working_set import (
    ChromiumPageResearchWorkingSetRecord,
    create_chromium_research_working_set,
)
from .chromium_research_working_set_note import (
    ChromiumPageResearchWorkingSetNoteRecord,
    create_chromium_research_working_set_note,
)
from .chromium_research_working_set_note_revision_edge_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord,
)


_TRANSITION_MODE = "caller_explicit_transition_to_changed_research_working_set"


class ChromiumResearchSessionWorkingSetTransitionError(ValueError):
    """Raised when a prepared changed evidence basis cannot become an explicit transition."""


@dataclass(frozen=True, slots=True)
class ChromiumResearchSessionWorkingSetTransitionRecord:
    """One explicit human choice to continue from one declared endpoint onto a changed basis.

    The transition retains the exact declared 24C endpoint, the exact changed 20A
    working set prepared by 33A, and the exact 21A human note authored over that set.

    It records only the caller's explicit choice to relate those already-established
    application objects. It is not a same-working-set revision edge, session
    declaration, chronology claim, current/head pointer, semantic-support assertion,
    or proof that the changed evidence basis is complete or correct.
    """

    transition_mode: str
    prior_endpoint: ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord
    successor_working_set: ChromiumPageResearchWorkingSetRecord
    successor_note: ChromiumPageResearchWorkingSetNoteRecord


def create_chromium_research_session_working_set_transition(
    controller: ChromiumResearchSessionController,
    prepared: ChromiumResearchSessionWorkingSetExtensionPersistenceResult,
) -> ChromiumResearchSessionWorkingSetTransitionRecord:
    """Create one explicit in-memory cross-working-set transition from exact 33A output.

    The controller's declared endpoint remains the only prior-session authority. An
    unadopted 29A successor is irrelevant. The prepared 33A result must have been
    produced from that exact declared endpoint and must still retain a coherent
    changed working set, human note, and persistence receipts.

    No files are read and nothing is persisted here. Durable re-establishment is a
    separate 33B persistence/load boundary.
    """

    if not isinstance(controller, ChromiumResearchSessionController):
        raise TypeError("controller must be ChromiumResearchSessionController.")
    if not isinstance(
        prepared,
        ChromiumResearchSessionWorkingSetExtensionPersistenceResult,
    ):
        raise TypeError(
            "prepared must be ChromiumResearchSessionWorkingSetExtensionPersistenceResult."
        )

    rebuilt_session = present_chromium_research_session(controller.loaded)
    if rebuilt_session != controller.presentation:
        raise ChromiumResearchSessionWorkingSetTransitionError(
            "Research controller presentation is incoherent with retained loaded evidence."
        )

    endpoint = controller.declared_endpoint
    prior_working_set = endpoint.revision.revised_note.working_set

    if prepared.prior_session != controller.presentation:
        raise ChromiumResearchSessionWorkingSetTransitionError(
            "Prepared evidence basis belongs to a different prior session presentation."
        )
    if prepared.prior_endpoint is not endpoint:
        raise ChromiumResearchSessionWorkingSetTransitionError(
            "Prepared evidence basis belongs to a different declared endpoint."
        )
    if prepared.prior_working_set is not prior_working_set:
        raise ChromiumResearchSessionWorkingSetTransitionError(
            "Prepared evidence basis does not retain the declared endpoint's exact working set."
        )
    if not prepared.appended_items:
        raise ChromiumResearchSessionWorkingSetTransitionError(
            "Prepared evidence basis must retain at least one explicit appended member."
        )

    rebuilt_working_set = create_chromium_research_working_set(prepared.working_set.items)
    if rebuilt_working_set.working_set_mode != prepared.working_set.working_set_mode:
        raise ChromiumResearchSessionWorkingSetTransitionError(
            "Prepared successor working set is incoherent with the 20A boundary."
        )

    expected_items = (*prior_working_set.items, *prepared.appended_items)
    if len(expected_items) != len(prepared.working_set.items):
        raise ChromiumResearchSessionWorkingSetTransitionError(
            "Prepared successor working-set member count is incoherent."
        )
    for index, (observed, expected) in enumerate(
        zip(prepared.working_set.items, expected_items)
    ):
        if observed is not expected:
            raise ChromiumResearchSessionWorkingSetTransitionError(
                f"Prepared successor working-set member {index} lost exact object identity."
            )

    if prepared.note.working_set is not prepared.working_set:
        raise ChromiumResearchSessionWorkingSetTransitionError(
            "Prepared human note is not attached to the exact successor working set."
        )
    rebuilt_note = create_chromium_research_working_set_note(
        prepared.working_set,
        note_text=prepared.note.note_text,
    )
    if rebuilt_note.note_mode != prepared.note.note_mode:
        raise ChromiumResearchSessionWorkingSetTransitionError(
            "Prepared human note is incoherent with the 21A boundary."
        )
    if prepared.working_set_persistence.working_set is not prepared.working_set:
        raise ChromiumResearchSessionWorkingSetTransitionError(
            "Prepared working-set persistence does not retain the exact successor set."
        )
    if prepared.note_persistence.note is not prepared.note:
        raise ChromiumResearchSessionWorkingSetTransitionError(
            "Prepared note persistence does not retain the exact successor note."
        )

    return ChromiumResearchSessionWorkingSetTransitionRecord(
        transition_mode=_TRANSITION_MODE,
        prior_endpoint=endpoint,
        successor_working_set=prepared.working_set,
        successor_note=prepared.note,
    )
