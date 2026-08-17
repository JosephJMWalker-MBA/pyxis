from __future__ import annotations

from dataclasses import dataclass

from .chromium_paragraphs import ChromiumPageParagraphEvidence
from .chromium_research_capture_load import ChromiumPageResearchLoadedCaptureEvidence
from .chromium_research_passage_selection import (
    ChromiumPageResearchParagraphSelectionEvidence,
)


_PARAGRAPH_SELECTION_MODE = "caller_explicit_returned_paragraph_ordinal"
_TEXT_SELECTION_MODE = "caller_explicit_returned_paragraph_text_range"
_OFFSET_UNIT = "unicode_code_point"


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchParagraphTextSelectionEvidence:
    """One exact caller-owned text range inside one already-selected paragraph.

    `source` retains the exact 17A paragraph-selection object. The selected text is
    derived from that source's already-returned paragraph `text_prefix` using the
    recorded zero-based half-open Unicode code-point offsets; it is not stored as
    a second source-text representation.
    """

    selection_mode: str
    offset_unit: str
    source: ChromiumPageResearchParagraphSelectionEvidence
    start_offset: int
    end_offset: int

    @property
    def selected_text(self) -> str:
        return self.source.paragraph.text_prefix[self.start_offset : self.end_offset]


def select_chromium_research_paragraph_text(
    source: ChromiumPageResearchParagraphSelectionEvidence,
    *,
    start_offset: int,
    end_offset: int,
) -> ChromiumPageResearchParagraphTextSelectionEvidence:
    """Refine one exact 17A paragraph selection to a returned text range.

    Offsets are zero-based, half-open Unicode code-point coordinates into the
    paragraph's already-returned `text_prefix`. The caller owns both coordinates.
    This operation never searches by text, expands a truncated prefix, rereads a
    capture, reacquires Chromium state, verifies a quotation, resolves a citation,
    ranks relevance, or interprets the selected text.
    """

    if not isinstance(source, ChromiumPageResearchParagraphSelectionEvidence):
        raise TypeError(
            "source must be ChromiumPageResearchParagraphSelectionEvidence."
        )
    if type(start_offset) is not int:
        raise TypeError("start_offset must be an integer Unicode code-point offset.")
    if type(end_offset) is not int:
        raise TypeError("end_offset must be an integer Unicode code-point offset.")
    if start_offset < 0:
        raise ValueError("start_offset must be >= 0.")
    if end_offset <= start_offset:
        raise ValueError("end_offset must be greater than start_offset.")

    _validate_exact_paragraph_selection_identity(source)

    paragraph = source.paragraph
    returned_count = len(paragraph.text_prefix)
    if start_offset >= returned_count or end_offset > returned_count:
        if paragraph.truncated and (
            start_offset < paragraph.text_character_count
            or end_offset <= paragraph.text_character_count
        ):
            raise ValueError(
                "text range addresses evidence outside the bounded returned paragraph "
                "text prefix; selection does not reacquire or expand source text."
            )
        raise ValueError("text range is outside returned paragraph text evidence.")

    return ChromiumPageResearchParagraphTextSelectionEvidence(
        selection_mode=_TEXT_SELECTION_MODE,
        offset_unit=_OFFSET_UNIT,
        source=source,
        start_offset=start_offset,
        end_offset=end_offset,
    )


def _validate_exact_paragraph_selection_identity(
    selection: ChromiumPageResearchParagraphSelectionEvidence,
) -> None:
    if selection.selection_mode != _PARAGRAPH_SELECTION_MODE:
        raise ValueError("source selection mode is unsupported for text refinement.")

    loaded_capture = selection.source
    paragraph = selection.paragraph
    if not isinstance(loaded_capture, ChromiumPageResearchLoadedCaptureEvidence):
        raise ValueError("source selection does not retain verified loaded-capture evidence.")
    if not isinstance(paragraph, ChromiumPageParagraphEvidence):
        raise ValueError("source selection does not retain paragraph evidence.")

    paragraphs = loaded_capture.bundle.paragraphs.paragraphs
    ordinal = paragraph.ordinal
    if type(ordinal) is not int or ordinal < 1 or ordinal > len(paragraphs):
        raise ValueError("source paragraph ordinal is outside returned capture evidence.")
    if paragraphs[ordinal - 1] is not paragraph:
        raise ValueError(
            "source paragraph is not the exact paragraph object retained by its capture."
        )

    if paragraph.text_character_count < 0:
        raise ValueError("source paragraph character count is negative.")
    if paragraph.text_limit < 0:
        raise ValueError("source paragraph text limit is negative.")
    returned_count = len(paragraph.text_prefix)
    if returned_count > paragraph.text_limit:
        raise ValueError("source paragraph text exceeds its recorded text limit.")
    if paragraph.text_character_count < returned_count:
        raise ValueError("source paragraph character count is smaller than returned text.")
    if paragraph.truncated != (paragraph.text_character_count > returned_count):
        raise ValueError("source paragraph text truncation is incoherent.")
