from __future__ import annotations

from dataclasses import dataclass

from .chromium_paragraphs import ChromiumPageParagraphEvidence
from .chromium_research_capture_load import ChromiumPageResearchLoadedCaptureEvidence
from .chromium_research_passage_selection import (
    ChromiumPageResearchParagraphSelectionEvidence,
)


_SELECTION_MODE = "caller_explicit_returned_paragraph_ordinal"
_NOTE_MODE = "caller_authored_exact_text_on_paragraph_selection"


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchParagraphNoteRecord:
    """One caller-authored note attached to one exact 17A paragraph selection.

    `selection` is retained by exact object identity. `note_text` is retained
    verbatim. This record distinguishes human interpretation from the selected
    page evidence; the note does not become source evidence, quotation evidence,
    citation evidence, claim support, or machine interpretation.
    """

    note_mode: str
    selection: ChromiumPageResearchParagraphSelectionEvidence
    note_text: str


def create_chromium_research_paragraph_note(
    selection: ChromiumPageResearchParagraphSelectionEvidence,
    *,
    note_text: str,
) -> ChromiumPageResearchParagraphNoteRecord:
    """Create one immutable caller-authored note over one exact selection.

    The caller supplies the note text. Leading/trailing whitespace, line breaks,
    Unicode, punctuation, and wording are preserved exactly. Whitespace-only text
    is refused because it does not constitute a note, but validation does not
    normalize the stored value.

    This operation performs no browser acquisition, capture-file read,
    persistence, ranking, summarization, claim modeling, quotation verification,
    citation resolution, source verification, timestamp inference, author
    inference, LLM interpretation, or mutation of the supplied selection.
    """

    if not isinstance(selection, ChromiumPageResearchParagraphSelectionEvidence):
        raise TypeError(
            "selection must be ChromiumPageResearchParagraphSelectionEvidence."
        )
    if type(note_text) is not str:
        raise TypeError("note_text must be a string.")
    if not note_text.strip():
        raise ValueError("note_text must contain non-whitespace caller-authored text.")

    _validate_exact_selection_identity(selection)

    return ChromiumPageResearchParagraphNoteRecord(
        note_mode=_NOTE_MODE,
        selection=selection,
        note_text=note_text,
    )


def _validate_exact_selection_identity(
    selection: ChromiumPageResearchParagraphSelectionEvidence,
) -> None:
    if selection.selection_mode != _SELECTION_MODE:
        raise ValueError("selection mode is unsupported for a paragraph note.")

    source = selection.source
    paragraph = selection.paragraph
    if not isinstance(source, ChromiumPageResearchLoadedCaptureEvidence):
        raise ValueError("selection source is not verified rehydrated capture evidence.")
    if not isinstance(paragraph, ChromiumPageParagraphEvidence):
        raise ValueError("selection paragraph is not paragraph evidence.")

    paragraphs = source.bundle.paragraphs.paragraphs
    ordinal = paragraph.ordinal
    if type(ordinal) is not int or ordinal < 1 or ordinal > len(paragraphs):
        raise ValueError("selection paragraph ordinal is outside returned source evidence.")

    exact_source_paragraph = paragraphs[ordinal - 1]
    if exact_source_paragraph is not paragraph:
        raise ValueError(
            "selection paragraph is not the exact paragraph object retained by its source."
        )
