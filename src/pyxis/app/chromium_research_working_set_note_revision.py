from __future__ import annotations

from dataclasses import dataclass

from .chromium_research_working_set_note import (
    ChromiumPageResearchWorkingSetNoteRecord,
    create_chromium_research_working_set_note,
)


_NOTE_MODE = "caller_authored_note_on_research_working_set"
_REVISION_MODE = "caller_authored_revision_of_research_working_set_note"


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchWorkingSetNoteRevisionRecord:
    """One append-only human revision of one existing working-set note.

    `prior_note` retains the exact caller-supplied 21A note object. `revised_note`
    is a newly created 21A note over the exact same working-set object with the
    caller's revised text preserved verbatim.

    The revision records only that the caller replaced one exact human wording
    with another exact human wording for the same in-memory working set. It does
    not infer why the text changed, whether the new wording is better or truer,
    what semantic relationship exists between versions, authorship identity,
    trusted time, or source/claim authority.
    """

    revision_mode: str
    prior_note: ChromiumPageResearchWorkingSetNoteRecord
    revised_note: ChromiumPageResearchWorkingSetNoteRecord


def create_chromium_research_working_set_note_revision(
    prior_note: ChromiumPageResearchWorkingSetNoteRecord,
    *,
    revised_note_text: str,
) -> ChromiumPageResearchWorkingSetNoteRevisionRecord:
    """Create one append-only human-authored revision of a 21A note.

    The prior note is re-established through the public 21A constructor, but the
    validation result is discarded so the returned revision retains the exact
    caller-supplied prior-note object. The revised note is then created through
    the same public 21A constructor over the exact same working-set object.

    Exact text equality is rejected because it is not a revision event. This is
    only a byte-for-text equality check; Pyxis performs no semantic diff,
    similarity analysis, normalization, explanation, ranking, or correction.

    A note reconstructed through 21C can participate through its `.note` value.
    22A performs no file reads, persistence, browser work, member discovery,
    semantic inference, claim modeling, timestamping, or mutation.
    """

    if not isinstance(prior_note, ChromiumPageResearchWorkingSetNoteRecord):
        raise TypeError("prior_note must be ChromiumPageResearchWorkingSetNoteRecord.")
    if type(revised_note_text) is not str:
        raise TypeError("revised_note_text must be a string.")
    if not revised_note_text.strip():
        raise ValueError(
            "revised_note_text must contain non-whitespace caller-authored text."
        )

    rebuilt_prior = create_chromium_research_working_set_note(
        prior_note.working_set,
        note_text=prior_note.note_text,
    )
    if rebuilt_prior.note_mode != prior_note.note_mode:
        raise ValueError("prior working-set note mode is unsupported for revision.")
    if prior_note.note_mode != _NOTE_MODE:
        raise ValueError("prior working-set note mode is unsupported for revision.")

    if revised_note_text == prior_note.note_text:
        raise ValueError("revised_note_text must differ exactly from the prior note text.")

    revised_note = create_chromium_research_working_set_note(
        prior_note.working_set,
        note_text=revised_note_text,
    )

    return ChromiumPageResearchWorkingSetNoteRevisionRecord(
        revision_mode=_REVISION_MODE,
        prior_note=prior_note,
        revised_note=revised_note,
    )
