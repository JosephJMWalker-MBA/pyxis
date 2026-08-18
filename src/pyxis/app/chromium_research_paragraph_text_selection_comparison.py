from __future__ import annotations

from dataclasses import dataclass

from .chromium_research_paragraph_text_selection import (
    ChromiumPageResearchParagraphTextSelectionEvidence,
    select_chromium_research_paragraph_text,
)


_TEXT_SELECTION_MODE = "caller_explicit_returned_paragraph_text_range"
_OFFSET_UNIT = "unicode_code_point"
_COMPARISON_MODE = "caller_explicit_exact_text_range_comparison"


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchParagraphTextSelectionComparisonRecord:
    """One caller-owned pairing of two exact 18A text selections.

    `first_selection` and `second_selection` retain the exact caller-supplied 18A
    objects. The record proves only that the caller chose to place those two
    already-valid ranges together for examination. It does not claim that the
    ranges are similar, different, contradictory, corroborating, relevant,
    supportive, authentic, true, or otherwise semantically related.
    """

    comparison_mode: str
    first_selection: ChromiumPageResearchParagraphTextSelectionEvidence
    second_selection: ChromiumPageResearchParagraphTextSelectionEvidence


def create_chromium_research_paragraph_text_selection_comparison(
    first_selection: ChromiumPageResearchParagraphTextSelectionEvidence,
    second_selection: ChromiumPageResearchParagraphTextSelectionEvidence,
) -> ChromiumPageResearchParagraphTextSelectionComparisonRecord:
    """Record one explicit human choice to examine two exact 18A ranges together.

    Each supplied range is re-established through the existing public 18A
    selector rather than through a second coordinate or source validator. After
    validation, this operation retains the exact caller-supplied selection
    objects rather than replacing them with newly-created validation results.

    The two selections may come from the same paragraph, different paragraphs,
    different durable captures, or even be the same exact selection object. Pyxis
    records the human act of juxtaposition without deciding whether that choice
    is meaningful.

    This operation performs no browser acquisition, capture-file read,
    persistence, source discovery, source ranking, similarity measurement,
    contradiction detection, claim modeling, quotation verification, citation
    resolution, source authentication, LLM interpretation, or mutation of either
    supplied selection.
    """

    _validate_text_selection(first_selection, role="first_selection")
    _validate_text_selection(second_selection, role="second_selection")

    return ChromiumPageResearchParagraphTextSelectionComparisonRecord(
        comparison_mode=_COMPARISON_MODE,
        first_selection=first_selection,
        second_selection=second_selection,
    )


def _validate_text_selection(
    selection: ChromiumPageResearchParagraphTextSelectionEvidence,
    *,
    role: str,
) -> None:
    if not isinstance(selection, ChromiumPageResearchParagraphTextSelectionEvidence):
        raise TypeError(
            f"{role} must be ChromiumPageResearchParagraphTextSelectionEvidence."
        )
    if selection.selection_mode != _TEXT_SELECTION_MODE:
        raise ValueError(f"{role} selection mode is unsupported for comparison.")
    if selection.offset_unit != _OFFSET_UNIT:
        raise ValueError(f"{role} offset unit is unsupported for comparison.")

    # Delegate parent identity, coordinate type, half-open range, Unicode-unit,
    # and bounded-prefix validation to the established 18A public operation.
    select_chromium_research_paragraph_text(
        selection.source,
        start_offset=selection.start_offset,
        end_offset=selection.end_offset,
    )
