from __future__ import annotations

from dataclasses import dataclass

from .chromium_research_paragraph_text_selection import (
    ChromiumPageResearchParagraphTextSelectionEvidence,
    select_chromium_research_paragraph_text,
)


_TEXT_SELECTION_MODE = "caller_explicit_returned_paragraph_text_range"
_OFFSET_UNIT = "unicode_code_point"
_NOTE_MODE = "caller_authored_exact_text_on_paragraph_text_selection"


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchParagraphTextSelectionNoteRecord:
    """One caller-authored note attached to one exact 18A text selection.

    `selection` is retained by exact object identity and `note_text` is retained
    verbatim. The note records human interpretation of the caller-owned range; it
    does not become page/source evidence, quotation evidence, citation evidence,
    claim support, relevance evidence, or machine interpretation.
    """

    note_mode: str
    selection: ChromiumPageResearchParagraphTextSelectionEvidence
    note_text: str


def create_chromium_research_paragraph_text_selection_note(
    selection: ChromiumPageResearchParagraphTextSelectionEvidence,
    *,
    note_text: str,
) -> ChromiumPageResearchParagraphTextSelectionNoteRecord:
    """Create one immutable caller-authored note over one exact 18A range.

    The caller supplies the note text. Leading/trailing whitespace, line breaks,
    Unicode, punctuation, and wording are preserved exactly. Whitespace-only text
    is refused because it does not constitute a note, but validation does not
    normalize the stored value.

    Range validity remains owned by 18A. This operation reuses the public 18A
    selector with the exact retained paragraph selection and recorded offsets,
    then keeps the caller-supplied 18A object rather than replacing it with the
    validation result.

    This operation performs no browser acquisition, capture-file read,
    persistence, ranking, summarization, claim modeling, quotation verification,
    citation resolution, source verification, timestamp inference, author
    inference, LLM interpretation, or mutation of the supplied selection.
    """

    if not isinstance(selection, ChromiumPageResearchParagraphTextSelectionEvidence):
        raise TypeError(
            "selection must be ChromiumPageResearchParagraphTextSelectionEvidence."
        )
    if type(note_text) is not str:
        raise TypeError("note_text must be a string.")
    if not note_text.strip():
        raise ValueError("note_text must contain non-whitespace caller-authored text.")

    _validate_text_selection(selection)

    return ChromiumPageResearchParagraphTextSelectionNoteRecord(
        note_mode=_NOTE_MODE,
        selection=selection,
        note_text=note_text,
    )


def _validate_text_selection(
    selection: ChromiumPageResearchParagraphTextSelectionEvidence,
) -> None:
    if selection.selection_mode != _TEXT_SELECTION_MODE:
        raise ValueError("selection mode is unsupported for a text-selection note.")
    if selection.offset_unit != _OFFSET_UNIT:
        raise ValueError("selection offset unit is unsupported for a text-selection note.")

    # Delegate parent identity, coordinate type, half-open range, Unicode-unit,
    # and bounded-prefix validation to the established 18A public operation.
    select_chromium_research_paragraph_text(
        selection.source,
        start_offset=selection.start_offset,
        end_offset=selection.end_offset,
    )
