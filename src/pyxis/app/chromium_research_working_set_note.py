from __future__ import annotations

from dataclasses import dataclass

from .chromium_research_working_set import (
    ChromiumPageResearchWorkingSetRecord,
    create_chromium_research_working_set,
)


_WORKING_SET_MODE = "caller_explicit_ordered_relinked_research_working_set"
_NOTE_MODE = "caller_authored_note_on_research_working_set"


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchWorkingSetNoteRecord:
    """One caller-authored note attached to one exact 20A research working set.

    `working_set` retains the exact caller-supplied 20A working-set object and
    `note_text` is retained verbatim. The note records the researcher's own
    rationale, question, reminder, interpretation, or other text about carrying
    that ordered set of already-loaded research records forward together.

    The note is human interpretation. It does not become source evidence,
    evidence that the working-set members are semantically related, evidence that
    the set is complete or representative, claim support, citation authority,
    ranking, or machine interpretation.
    """

    note_mode: str
    working_set: ChromiumPageResearchWorkingSetRecord
    note_text: str


def create_chromium_research_working_set_note(
    working_set: ChromiumPageResearchWorkingSetRecord,
    *,
    note_text: str,
) -> ChromiumPageResearchWorkingSetNoteRecord:
    """Attach one verbatim caller-authored note to one exact 20A working set.

    Leading/trailing whitespace, line breaks, Unicode, punctuation, and wording
    are preserved exactly. Whitespace-only text is refused because it does not
    constitute a note, but the stored value is never normalized.

    Working-set validity remains owned by 20A. This operation calls the existing
    public 20A constructor over the exact retained member sequence, discards that
    validation result, and keeps the exact caller-supplied working-set object.

    A working set reconstructed by 20C can participate through its `.working_set`
    value, but 21A does not require or consume 20C verification evidence. It does
    no file verification, persistence, member discovery, member relinking, source
    acquisition, semantic clustering, ranking, claim modeling, citation checking,
    authorship/timestamp inference, LLM interpretation, or mutation.
    """

    if not isinstance(working_set, ChromiumPageResearchWorkingSetRecord):
        raise TypeError("working_set must be ChromiumPageResearchWorkingSetRecord.")
    if type(note_text) is not str:
        raise TypeError("note_text must be a string.")
    if not note_text.strip():
        raise ValueError("note_text must contain non-whitespace caller-authored text.")

    _validate_working_set(working_set)

    return ChromiumPageResearchWorkingSetNoteRecord(
        note_mode=_NOTE_MODE,
        working_set=working_set,
        note_text=note_text,
    )


def _validate_working_set(working_set: ChromiumPageResearchWorkingSetRecord) -> None:
    if working_set.working_set_mode != _WORKING_SET_MODE:
        raise ValueError("working-set mode is unsupported for a working-set note.")

    rebuilt = create_chromium_research_working_set(working_set.items)
    if rebuilt.working_set_mode != working_set.working_set_mode:
        raise ValueError("working-set mode is incoherent with the established 20A boundary.")
