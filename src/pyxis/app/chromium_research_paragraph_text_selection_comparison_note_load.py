from __future__ import annotations

from dataclasses import dataclass
import hmac
from pathlib import Path
from typing import Any

from .chromium_research_capture_load import ChromiumPageResearchLoadedCaptureEvidence
from .chromium_research_paragraph_text_selection import (
    ChromiumPageResearchParagraphTextSelectionEvidence,
    select_chromium_research_paragraph_text,
)
from .chromium_research_paragraph_text_selection_comparison import (
    ChromiumPageResearchParagraphTextSelectionComparisonRecord,
    create_chromium_research_paragraph_text_selection_comparison,
)
from .chromium_research_paragraph_text_selection_comparison_note import (
    ChromiumPageResearchParagraphTextSelectionComparisonNoteRecord,
    create_chromium_research_paragraph_text_selection_comparison_note,
)
from .chromium_research_paragraph_text_selection_comparison_note_persistence import (
    ChromiumPageResearchParagraphTextSelectionComparisonNoteVerificationEvidence,
    verify_chromium_research_paragraph_text_selection_comparison_note,
)
from .chromium_research_passage_selection import (
    select_chromium_research_capture_paragraph,
)


_CAPTURE_FORMAT = "pyxis.chromium.research_capture.v1"
_PARAGRAPH_SELECTION_MODE = "caller_explicit_returned_paragraph_ordinal"
_TEXT_SELECTION_MODE = "caller_explicit_returned_paragraph_text_range"
_OFFSET_UNIT = "unicode_code_point"
_COMPARISON_MODE = "caller_explicit_exact_text_range_comparison"
_NOTE_MODE = "caller_authored_note_on_exact_text_range_comparison"


class ChromiumResearchParagraphTextSelectionComparisonNoteSourceMismatchError(ValueError):
    """Raised when a verified comparison note does not match supplied sources."""


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchLoadedParagraphTextSelectionComparisonNoteRecord:
    """One verified durable comparison note relinked to two supplied captures.

    `verification` is the fresh 19C sidecar-verification evidence produced during
    this load. `note` is a newly reconstructed 19B note whose 19A comparison
    contains newly reconstructed 18A selections over the exact caller-supplied
    loaded captures and their already-returned paragraph evidence.

    Relinking proves attachment coherence only. It does not authenticate either
    source or the note, identify the human author, establish trusted time or chain
    of custody, prove a semantic relationship, or grant quotation/citation or
    claim-support authority.
    """

    verification: ChromiumPageResearchParagraphTextSelectionComparisonNoteVerificationEvidence
    note: ChromiumPageResearchParagraphTextSelectionComparisonNoteRecord


def load_chromium_research_paragraph_text_selection_comparison_note(
    first_source: ChromiumPageResearchLoadedCaptureEvidence,
    second_source: ChromiumPageResearchLoadedCaptureEvidence,
    note_source: Path,
) -> ChromiumPageResearchLoadedParagraphTextSelectionComparisonNoteRecord:
    """Verify one 19C sidecar and relink its ordered pair to explicit sources.

    The sidecar is always freshly verified from the caller-supplied file path.
    Its first and second durable capture identities must respectively match the
    exact 16B verification identities retained by the two supplied 16C captures.
    Source order is not inferred or swapped.

    Reconstruction delegates to existing public boundaries in order: 17A
    paragraph selection, 18A exact-range selection, 19A human-owned comparison,
    and 19B human-authored comparison note. This is where structurally valid 19C
    coordinates are tested again against actual supplied source evidence.

    This operation performs no Chromium acquisition, source discovery by digest
    or path, source-capture file read, capture rehydration, persistence, text
    search, source ranking, semantic comparison, quotation/citation verification,
    claim modeling, authorship inference, or authenticity/provenance upgrade.
    """

    if not isinstance(first_source, ChromiumPageResearchLoadedCaptureEvidence):
        raise TypeError(
            "first_source must be ChromiumPageResearchLoadedCaptureEvidence."
        )
    if not isinstance(second_source, ChromiumPageResearchLoadedCaptureEvidence):
        raise TypeError(
            "second_source must be ChromiumPageResearchLoadedCaptureEvidence."
        )

    verification = verify_chromium_research_paragraph_text_selection_comparison_note(
        note_source
    )
    _validate_verified_modes(verification)
    _validate_source_reference(first_source, verification, role="first")
    _validate_source_reference(second_source, verification, role="second")

    first_selection = _reconstruct_selection(
        first_source,
        paragraph_ordinal=verification.first_paragraph_ordinal,
        paragraph_selection_mode=verification.first_paragraph_selection_mode,
        start_offset=verification.first_start_offset,
        end_offset=verification.first_end_offset,
        text_selection_mode=verification.first_text_selection_mode,
        offset_unit=verification.first_offset_unit,
        role="first",
    )
    second_selection = _reconstruct_selection(
        second_source,
        paragraph_ordinal=verification.second_paragraph_ordinal,
        paragraph_selection_mode=verification.second_paragraph_selection_mode,
        start_offset=verification.second_start_offset,
        end_offset=verification.second_end_offset,
        text_selection_mode=verification.second_text_selection_mode,
        offset_unit=verification.second_offset_unit,
        role="second",
    )

    comparison = create_chromium_research_paragraph_text_selection_comparison(
        first_selection,
        second_selection,
    )
    if comparison.comparison_mode != verification.comparison_mode:
        raise ChromiumResearchParagraphTextSelectionComparisonNoteSourceMismatchError(
            "Reconstructed comparison mode does not match the verified sidecar."
        )

    note = create_chromium_research_paragraph_text_selection_comparison_note(
        comparison,
        note_text=verification.note_text,
    )
    if note.note_mode != verification.note_mode or note.note_text != verification.note_text:
        raise ChromiumResearchParagraphTextSelectionComparisonNoteSourceMismatchError(
            "Reconstructed comparison note does not match the verified sidecar."
        )

    return ChromiumPageResearchLoadedParagraphTextSelectionComparisonNoteRecord(
        verification=verification,
        note=note,
    )


def _reconstruct_selection(
    source: ChromiumPageResearchLoadedCaptureEvidence,
    *,
    paragraph_ordinal: int,
    paragraph_selection_mode: str,
    start_offset: int,
    end_offset: int,
    text_selection_mode: str,
    offset_unit: str,
    role: str,
) -> ChromiumPageResearchParagraphTextSelectionEvidence:
    paragraph_selection = select_chromium_research_capture_paragraph(
        source,
        paragraph_ordinal=paragraph_ordinal,
    )
    if paragraph_selection.selection_mode != paragraph_selection_mode:
        raise ChromiumResearchParagraphTextSelectionComparisonNoteSourceMismatchError(
            f"Reconstructed {role} paragraph selection mode does not match the verified sidecar."
        )

    text_selection = select_chromium_research_paragraph_text(
        paragraph_selection,
        start_offset=start_offset,
        end_offset=end_offset,
    )
    if (
        text_selection.selection_mode != text_selection_mode
        or text_selection.offset_unit != offset_unit
        or text_selection.start_offset != start_offset
        or text_selection.end_offset != end_offset
    ):
        raise ChromiumResearchParagraphTextSelectionComparisonNoteSourceMismatchError(
            f"Reconstructed {role} text selection does not match the verified sidecar."
        )
    return text_selection


def _validate_source_reference(
    source: ChromiumPageResearchLoadedCaptureEvidence,
    verification: ChromiumPageResearchParagraphTextSelectionComparisonNoteVerificationEvidence,
    *,
    role: str,
) -> None:
    source_verification = source.verification
    if source_verification.capture_format != _CAPTURE_FORMAT:
        raise ChromiumResearchParagraphTextSelectionComparisonNoteSourceMismatchError(
            f"Supplied {role} source capture format is unsupported for comparison-note relinking."
        )
    if not _is_sha256(source_verification.bundle_sha256):
        raise ChromiumResearchParagraphTextSelectionComparisonNoteSourceMismatchError(
            f"Supplied {role} source capture bundle SHA-256 has an invalid shape."
        )

    expected_format = getattr(verification, f"{role}_source_capture_format")
    expected_digest = getattr(verification, f"{role}_source_bundle_sha256")
    if expected_format != source_verification.capture_format:
        raise ChromiumResearchParagraphTextSelectionComparisonNoteSourceMismatchError(
            f"Verified comparison-note sidecar references a different {role} capture format."
        )
    if not hmac.compare_digest(expected_digest, source_verification.bundle_sha256):
        raise ChromiumResearchParagraphTextSelectionComparisonNoteSourceMismatchError(
            f"Verified comparison-note sidecar references a different {role} capture bundle."
        )


def _validate_verified_modes(
    verification: ChromiumPageResearchParagraphTextSelectionComparisonNoteVerificationEvidence,
) -> None:
    if verification.comparison_mode != _COMPARISON_MODE:
        raise ChromiumResearchParagraphTextSelectionComparisonNoteSourceMismatchError(
            "Verified comparison-note sidecar uses an unsupported comparison mode."
        )
    for role in ("first", "second"):
        if getattr(verification, f"{role}_paragraph_selection_mode") != _PARAGRAPH_SELECTION_MODE:
            raise ChromiumResearchParagraphTextSelectionComparisonNoteSourceMismatchError(
                f"Verified comparison-note sidecar uses an unsupported {role} paragraph selection mode."
            )
        if getattr(verification, f"{role}_text_selection_mode") != _TEXT_SELECTION_MODE:
            raise ChromiumResearchParagraphTextSelectionComparisonNoteSourceMismatchError(
                f"Verified comparison-note sidecar uses an unsupported {role} text selection mode."
            )
        if getattr(verification, f"{role}_offset_unit") != _OFFSET_UNIT:
            raise ChromiumResearchParagraphTextSelectionComparisonNoteSourceMismatchError(
                f"Verified comparison-note sidecar uses an unsupported {role} offset unit."
            )
    if verification.note_mode != _NOTE_MODE:
        raise ChromiumResearchParagraphTextSelectionComparisonNoteSourceMismatchError(
            "Verified comparison-note sidecar uses an unsupported note mode."
        )


def _is_sha256(value: Any) -> bool:
    return (
        type(value) is str
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )
