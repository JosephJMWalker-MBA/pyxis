from __future__ import annotations

from dataclasses import dataclass
import hmac

from .chromium_research_session_working_set_transition_load import (
    ChromiumPageResearchLoadedWorkingSetTransitionRecord,
)
from .chromium_research_working_set_note import create_chromium_research_working_set_note
from .chromium_research_working_set_note_revision import (
    ChromiumPageResearchWorkingSetNoteRevisionRecord,
    create_chromium_research_working_set_note_revision,
)


_TRANSITION_FORMAT = "pyxis.chromium.research_session_working_set_transition.v1"
_TRANSITION_MODE = "caller_explicit_transition_to_changed_research_working_set"
_EDGE_FORMAT = "pyxis.chromium.research_working_set_note_revision_edge.v1"
_WORKING_SET_FORMAT = "pyxis.chromium.research_working_set.v1"
_NOTE_FORMAT = "pyxis.chromium.research_working_set_note.v1"
_NOTE_MODE = "caller_authored_note_on_research_working_set"
_REVISION_MODE = "caller_authored_revision_of_research_working_set_note"
_ROOT_MODE = (
    "caller_authored_revision_root_after_changed_research_working_set_transition"
)


class ChromiumResearchSessionWorkingSetTransitionRevisionRootError(ValueError):
    """Raised when one loaded cross-working-set transition cannot root a revision lineage."""


@dataclass(frozen=True, slots=True)
class ChromiumResearchSessionWorkingSetTransitionRevisionRootRecord:
    """First same-working-set revision explicitly rooted in one loaded 33B transition.

    `transition` retains the exact caller-supplied loaded 33B transition. `revision`
    is one ordinary 22A human revision whose prior note is exactly the successor note
    reconstructed by that transition.

    This object preserves the evidence-basis crossing as the explicit lineage root.
    It does not make the 33B transition a same-working-set revision edge, adopt a
    session, select a current/latest/head state, infer chronology, or claim that the
    changed evidence supports the human rationale.
    """

    root_mode: str
    transition: ChromiumPageResearchLoadedWorkingSetTransitionRecord
    revision: ChromiumPageResearchWorkingSetNoteRevisionRecord


def create_chromium_research_session_working_set_transition_revision_root(
    transition: ChromiumPageResearchLoadedWorkingSetTransitionRecord,
    *,
    revised_note_text: str,
) -> ChromiumResearchSessionWorkingSetTransitionRevisionRootRecord:
    """Create the first ordinary rationale revision after one verified basis change.

    The operation consumes only already-loaded 33B application evidence and performs
    no file reads. It re-establishes the retained local transition relationships from
    their reported identities and then delegates the actual human text revision to
    public 22A over exactly `transition.successor_note.note`.

    Exact textual no-ops therefore remain rejected by 22A. The returned root records
    no paths, timestamps, revision numbers, history traversal, branch selection,
    source authority, semantic support, or session/head adoption.
    """

    if not isinstance(
        transition,
        ChromiumPageResearchLoadedWorkingSetTransitionRecord,
    ):
        raise TypeError(
            "transition must be ChromiumPageResearchLoadedWorkingSetTransitionRecord."
        )

    _validate_loaded_transition(transition)
    revision = create_chromium_research_working_set_note_revision(
        transition.successor_note.note,
        revised_note_text=revised_note_text,
    )
    if revision.prior_note is not transition.successor_note.note:
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootError(
            "Root revision did not retain the exact transition successor note."
        )
    if revision.revised_note.working_set is not transition.successor_note.note.working_set:
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootError(
            "Root revision did not retain the exact changed working set."
        )

    return ChromiumResearchSessionWorkingSetTransitionRevisionRootRecord(
        root_mode=_ROOT_MODE,
        transition=transition,
        revision=revision,
    )


def _validate_loaded_transition(
    transition: ChromiumPageResearchLoadedWorkingSetTransitionRecord,
) -> None:
    verification = transition.verification
    prior = transition.prior_endpoint
    successor = transition.successor_note

    if verification.transition_format != _TRANSITION_FORMAT:
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootError(
            "Loaded transition uses an unsupported transition format."
        )
    if verification.transition_mode != _TRANSITION_MODE:
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootError(
            "Loaded transition uses an unsupported transition mode."
        )
    if prior.verification.edge_format != _EDGE_FORMAT:
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootError(
            "Loaded transition prior endpoint uses an unsupported edge format."
        )
    if verification.prior_endpoint_format != prior.verification.edge_format:
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootError(
            "Loaded transition retained an incoherent prior endpoint format."
        )
    if not hmac.compare_digest(
        verification.prior_endpoint_record_sha256,
        prior.verification.edge_record_sha256,
    ):
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootError(
            "Loaded transition retained an incoherent prior endpoint identity."
        )

    if successor.working_set.verification.working_set_format != _WORKING_SET_FORMAT:
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootError(
            "Loaded transition successor working set uses an unsupported format."
        )
    if successor.verification.note_format != _NOTE_FORMAT:
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootError(
            "Loaded transition successor note uses an unsupported format."
        )
    if successor.note.note_mode != _NOTE_MODE:
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootError(
            "Loaded transition successor note uses an unsupported note mode."
        )
    if successor.note.working_set is not successor.working_set.working_set:
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootError(
            "Loaded transition successor note does not retain its exact working set."
        )
    if (
        verification.successor_working_set_format
        != successor.working_set.verification.working_set_format
    ):
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootError(
            "Loaded transition retained an incoherent successor working-set format."
        )
    if not hmac.compare_digest(
        verification.successor_working_set_record_sha256,
        successor.working_set.verification.working_set_record_sha256,
    ):
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootError(
            "Loaded transition retained an incoherent successor working-set identity."
        )
    if verification.successor_note_format != successor.verification.note_format:
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootError(
            "Loaded transition retained an incoherent successor-note format."
        )
    if not hmac.compare_digest(
        verification.successor_note_record_sha256,
        successor.verification.note_record_sha256,
    ):
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootError(
            "Loaded transition retained an incoherent successor-note identity."
        )

    rebuilt_note = create_chromium_research_working_set_note(
        successor.working_set.working_set,
        note_text=successor.verification.note_text,
    )
    if rebuilt_note.note_mode != successor.note.note_mode:
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootError(
            "Loaded transition successor note mode cannot be re-established."
        )
    if rebuilt_note.note_text != successor.note.note_text:
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootError(
            "Loaded transition successor note text cannot be re-established."
        )


__all__ = [
    "ChromiumResearchSessionWorkingSetTransitionRevisionRootError",
    "ChromiumResearchSessionWorkingSetTransitionRevisionRootRecord",
    "create_chromium_research_session_working_set_transition_revision_root",
]
