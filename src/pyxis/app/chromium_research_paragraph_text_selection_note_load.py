from __future__ import annotations

from dataclasses import dataclass
import hmac
from pathlib import Path
from typing import Any

from .chromium_research_capture_load import ChromiumPageResearchLoadedCaptureEvidence
from .chromium_research_paragraph_text_selection import (
    select_chromium_research_paragraph_text,
)
from .chromium_research_paragraph_text_selection_note import (
    ChromiumPageResearchParagraphTextSelectionNoteRecord,
    create_chromium_research_paragraph_text_selection_note,
)
from .chromium_research_paragraph_text_selection_note_persistence import (
    ChromiumPageResearchParagraphTextSelectionNoteVerificationEvidence,
    verify_chromium_research_paragraph_text_selection_note,
)
from .chromium_research_passage_selection import (
    select_chromium_research_capture_paragraph,
)


_CAPTURE_FORMAT = "pyxis.chromium.research_capture.v1"
_PARAGRAPH_SELECTION_MODE = "caller_explicit_returned_paragraph_ordinal"
_TEXT_SELECTION_MODE = "caller_explicit_returned_paragraph_text_range"
_OFFSET_UNIT = "unicode_code_point"
_NOTE_MODE = "caller_authored_exact_text_on_paragraph_text_selection"


class ChromiumResearchParagraphTextSelectionNoteSourceMismatchError(ValueError):
    """Raised when a verified exact-range note references a different capture."""


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchLoadedParagraphTextSelectionNoteRecord:
    """One verified durable exact-range note relinked to supplied source evidence.

    `verification` is the exact fresh 18C sidecar-verification evidence produced
    during this load. `note` is a newly reconstructed 18B note whose text-range
    selection retains a newly reconstructed 17A paragraph selection over the exact
    caller-supplied 16C loaded capture and its exact already-returned paragraph.

    Relinking proves attachment coherence only. It does not authenticate either
    artifact, identify the human author, verify source provenance, turn the range
    into quotation/citation evidence, prove the human note, or establish chain of
    custody.
    """

    verification: ChromiumPageResearchParagraphTextSelectionNoteVerificationEvidence
    note: ChromiumPageResearchParagraphTextSelectionNoteRecord


def load_chromium_research_paragraph_text_selection_note(
    source: ChromiumPageResearchLoadedCaptureEvidence,
    note_source: Path,
) -> ChromiumPageResearchLoadedParagraphTextSelectionNoteRecord:
    """Verify one 18C sidecar and relink it to one explicit loaded capture.

    The sidecar is always freshly verified from the caller-supplied file path.
    Its durable capture reference must match the exact 16B verification identity
    retained by the supplied 16C capture before any human-selection reconstruction
    occurs.

    Reconstruction then delegates in order to the existing public 17A paragraph
    selector, 18A exact-text selector, and 18B note constructor. This is where a
    structurally valid 18C coordinate is re-tested against actual supplied source
    evidence. File integrity alone is therefore insufficient to reopen a range.

    This operation performs no Chromium acquisition, source-capture discovery or
    file read, capture rehydration, persistence, source-path inference, text search,
    ranking, semantic interpretation, quotation/citation verification, authorship
    inference, or authenticity/provenance upgrade.
    """

    if not isinstance(source, ChromiumPageResearchLoadedCaptureEvidence):
        raise TypeError("source must be ChromiumPageResearchLoadedCaptureEvidence.")

    verification = verify_chromium_research_paragraph_text_selection_note(note_source)
    _validate_source_reference(source, verification)

    paragraph_selection = select_chromium_research_capture_paragraph(
        source,
        paragraph_ordinal=verification.paragraph_ordinal,
    )
    if paragraph_selection.selection_mode != verification.paragraph_selection_mode:
        raise ChromiumResearchParagraphTextSelectionNoteSourceMismatchError(
            "Reconstructed paragraph selection mode does not match the verified sidecar."
        )

    text_selection = select_chromium_research_paragraph_text(
        paragraph_selection,
        start_offset=verification.start_offset,
        end_offset=verification.end_offset,
    )
    if (
        text_selection.selection_mode != verification.text_selection_mode
        or text_selection.offset_unit != verification.offset_unit
        or text_selection.start_offset != verification.start_offset
        or text_selection.end_offset != verification.end_offset
    ):
        raise ChromiumResearchParagraphTextSelectionNoteSourceMismatchError(
            "Reconstructed text selection does not match the verified sidecar."
        )

    note = create_chromium_research_paragraph_text_selection_note(
        text_selection,
        note_text=verification.note_text,
    )
    if note.note_mode != verification.note_mode or note.note_text != verification.note_text:
        raise ChromiumResearchParagraphTextSelectionNoteSourceMismatchError(
            "Reconstructed exact-range note does not match the verified sidecar."
        )

    return ChromiumPageResearchLoadedParagraphTextSelectionNoteRecord(
        verification=verification,
        note=note,
    )


def _validate_source_reference(
    source: ChromiumPageResearchLoadedCaptureEvidence,
    verification: ChromiumPageResearchParagraphTextSelectionNoteVerificationEvidence,
) -> None:
    source_verification = source.verification

    if source_verification.capture_format != _CAPTURE_FORMAT:
        raise ChromiumResearchParagraphTextSelectionNoteSourceMismatchError(
            "Supplied source capture format is unsupported for exact-range-note relinking."
        )
    if not _is_sha256(source_verification.bundle_sha256):
        raise ChromiumResearchParagraphTextSelectionNoteSourceMismatchError(
            "Supplied source capture bundle SHA-256 has an invalid shape."
        )

    if verification.source_capture_format != source_verification.capture_format:
        raise ChromiumResearchParagraphTextSelectionNoteSourceMismatchError(
            "Verified exact-range-note sidecar references a different capture format."
        )
    if not hmac.compare_digest(
        verification.source_bundle_sha256,
        source_verification.bundle_sha256,
    ):
        raise ChromiumResearchParagraphTextSelectionNoteSourceMismatchError(
            "Verified exact-range-note sidecar references a different capture bundle."
        )

    if verification.paragraph_selection_mode != _PARAGRAPH_SELECTION_MODE:
        raise ChromiumResearchParagraphTextSelectionNoteSourceMismatchError(
            "Verified exact-range-note sidecar uses an unsupported paragraph selection mode."
        )
    if verification.text_selection_mode != _TEXT_SELECTION_MODE:
        raise ChromiumResearchParagraphTextSelectionNoteSourceMismatchError(
            "Verified exact-range-note sidecar uses an unsupported text selection mode."
        )
    if verification.offset_unit != _OFFSET_UNIT:
        raise ChromiumResearchParagraphTextSelectionNoteSourceMismatchError(
            "Verified exact-range-note sidecar uses an unsupported offset unit."
        )
    if verification.note_mode != _NOTE_MODE:
        raise ChromiumResearchParagraphTextSelectionNoteSourceMismatchError(
            "Verified exact-range-note sidecar uses an unsupported note mode."
        )


def _is_sha256(value: Any) -> bool:
    return (
        type(value) is str
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )
