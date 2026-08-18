from __future__ import annotations

from dataclasses import dataclass

from .chromium_research_paragraph_text_selection_comparison import (
    ChromiumPageResearchParagraphTextSelectionComparisonRecord,
    create_chromium_research_paragraph_text_selection_comparison,
)


_COMPARISON_MODE = "caller_explicit_exact_text_range_comparison"
_NOTE_MODE = "caller_authored_note_on_exact_text_range_comparison"


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchParagraphTextSelectionComparisonNoteRecord:
    """One caller-authored note attached to one exact 19A comparison.

    `comparison` retains the exact caller-supplied 19A comparison object and
    `note_text` is retained verbatim. The note records human interpretation of
    the caller-owned juxtaposition. It does not become source evidence, evidence
    that the compared ranges have any semantic relationship, claim support,
    relevance evidence, quotation/citation evidence, or machine interpretation.
    """

    note_mode: str
    comparison: ChromiumPageResearchParagraphTextSelectionComparisonRecord
    note_text: str


def create_chromium_research_paragraph_text_selection_comparison_note(
    comparison: ChromiumPageResearchParagraphTextSelectionComparisonRecord,
    *,
    note_text: str,
) -> ChromiumPageResearchParagraphTextSelectionComparisonNoteRecord:
    """Create one immutable caller-authored note over one exact 19A comparison.

    The caller supplies the note text. Leading/trailing whitespace, line breaks,
    Unicode, punctuation, and wording are preserved exactly. Whitespace-only text
    is refused because it does not constitute a note, but validation does not
    normalize the stored value.

    Comparison validity remains owned by 19A. This operation reuses the public
    19A comparison constructor with the exact retained two selections, then keeps
    the caller-supplied comparison object rather than replacing it with the
    validation result.

    This operation performs no browser acquisition, capture-file read,
    persistence, source discovery, source ranking, similarity measurement,
    contradiction detection, corroboration judgment, claim modeling, quotation
    verification, citation resolution, source authentication, timestamp or author
    inference, LLM interpretation, or mutation of the supplied comparison.
    """

    if not isinstance(
        comparison, ChromiumPageResearchParagraphTextSelectionComparisonRecord
    ):
        raise TypeError(
            "comparison must be "
            "ChromiumPageResearchParagraphTextSelectionComparisonRecord."
        )
    if type(note_text) is not str:
        raise TypeError("note_text must be a string.")
    if not note_text.strip():
        raise ValueError("note_text must contain non-whitespace caller-authored text.")

    _validate_comparison(comparison)

    return ChromiumPageResearchParagraphTextSelectionComparisonNoteRecord(
        note_mode=_NOTE_MODE,
        comparison=comparison,
        note_text=note_text,
    )


def _validate_comparison(
    comparison: ChromiumPageResearchParagraphTextSelectionComparisonRecord,
) -> None:
    if comparison.comparison_mode != _COMPARISON_MODE:
        raise ValueError("comparison mode is unsupported for a comparison note.")

    # Delegate both exact-range relationships and the caller-owned pairing shape
    # to the established 19A public operation. The validation result is discarded
    # so this layer retains the exact caller-supplied comparison object.
    create_chromium_research_paragraph_text_selection_comparison(
        comparison.first_selection,
        comparison.second_selection,
    )
