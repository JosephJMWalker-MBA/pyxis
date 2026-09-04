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
from .chromium_research_paragraph_text_selection_persistence import (
    ChromiumPageResearchParagraphTextSelectionVerificationEvidence,
    verify_chromium_research_paragraph_text_selection,
)
from .chromium_research_passage_selection import (
    select_chromium_research_capture_paragraph,
)


_CAPTURE_FORMAT = "pyxis.chromium.research_capture.v1"
_PARAGRAPH_SELECTION_MODE = "caller_explicit_returned_paragraph_ordinal"
_TEXT_SELECTION_MODE = "caller_explicit_returned_paragraph_text_range"
_OFFSET_UNIT = "unicode_code_point"


class ChromiumResearchParagraphTextSelectionSourceMismatchError(ValueError):
    """Raised when a verified durable exact-range selection does not match a source."""


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchLoadedParagraphTextSelectionRecord:
    """One verified durable exact range relinked to explicit supplied source evidence.

    verification is the exact fresh 49A sidecar-verification evidence produced during
    this load. selection is a newly reconstructed public 18A selection over a newly
    reconstructed public 17A paragraph selection that retains the exact caller-supplied
    16C loaded capture.

    Relinking proves attachment coherence only. It does not authenticate the source,
    identify authorship, establish trusted time or chain of custody, prove quotation
    or citation status, infer semantic support, compare against a live page, or grant
    fuzzy re-anchoring authority.
    """

    verification: ChromiumPageResearchParagraphTextSelectionVerificationEvidence
    selection: ChromiumPageResearchParagraphTextSelectionEvidence


def load_chromium_research_paragraph_text_selection(
    source: ChromiumPageResearchLoadedCaptureEvidence,
    selection_source: Path,
) -> ChromiumPageResearchLoadedParagraphTextSelectionRecord:
    """Freshly verify one 49A sidecar and relink it to one explicit loaded capture.

    The caller supplies both the exact loaded source evidence and the durable 49A
    sidecar path. The sidecar is freshly verified from bytes, then its durable capture
    identity is compared with the supplied capture before any paragraph/range
    reconstruction occurs.

    Reconstruction delegates in order to the existing public 17A paragraph selector
    and public 18A exact-range selector. A file-locally valid coordinate that does not
    address the supplied bounded source evidence therefore fails here rather than
    being searched for, expanded, or silently re-anchored elsewhere.
    """

    if not isinstance(source, ChromiumPageResearchLoadedCaptureEvidence):
        raise TypeError("source must be ChromiumPageResearchLoadedCaptureEvidence.")

    verification = verify_chromium_research_paragraph_text_selection(selection_source)
    _validate_source_reference(source, verification)

    paragraph_selection = select_chromium_research_capture_paragraph(
        source,
        paragraph_ordinal=verification.paragraph_ordinal,
    )
    if paragraph_selection.selection_mode != verification.paragraph_selection_mode:
        raise ChromiumResearchParagraphTextSelectionSourceMismatchError(
            "Reconstructed paragraph selection mode does not match the verified sidecar."
        )

    selection = select_chromium_research_paragraph_text(
        paragraph_selection,
        start_offset=verification.start_offset,
        end_offset=verification.end_offset,
    )
    if (
        selection.selection_mode != verification.text_selection_mode
        or selection.offset_unit != verification.offset_unit
        or selection.start_offset != verification.start_offset
        or selection.end_offset != verification.end_offset
    ):
        raise ChromiumResearchParagraphTextSelectionSourceMismatchError(
            "Reconstructed text selection does not match the verified sidecar."
        )

    return ChromiumPageResearchLoadedParagraphTextSelectionRecord(
        verification=verification,
        selection=selection,
    )


def _validate_source_reference(
    source: ChromiumPageResearchLoadedCaptureEvidence,
    verification: ChromiumPageResearchParagraphTextSelectionVerificationEvidence,
) -> None:
    source_verification = source.verification

    if source_verification.capture_format != _CAPTURE_FORMAT:
        raise ChromiumResearchParagraphTextSelectionSourceMismatchError(
            "Supplied source capture format is unsupported for exact-range-selection relinking."
        )
    if not _is_sha256(source_verification.bundle_sha256):
        raise ChromiumResearchParagraphTextSelectionSourceMismatchError(
            "Supplied source capture bundle SHA-256 has an invalid shape."
        )

    if verification.source_capture_format != source_verification.capture_format:
        raise ChromiumResearchParagraphTextSelectionSourceMismatchError(
            "Verified exact-range-selection sidecar references a different capture format."
        )
    if not hmac.compare_digest(
        verification.source_bundle_sha256,
        source_verification.bundle_sha256,
    ):
        raise ChromiumResearchParagraphTextSelectionSourceMismatchError(
            "Verified exact-range-selection sidecar references a different capture bundle."
        )

    if verification.paragraph_selection_mode != _PARAGRAPH_SELECTION_MODE:
        raise ChromiumResearchParagraphTextSelectionSourceMismatchError(
            "Verified exact-range-selection sidecar uses an unsupported paragraph selection mode."
        )
    if verification.text_selection_mode != _TEXT_SELECTION_MODE:
        raise ChromiumResearchParagraphTextSelectionSourceMismatchError(
            "Verified exact-range-selection sidecar uses an unsupported text selection mode."
        )
    if verification.offset_unit != _OFFSET_UNIT:
        raise ChromiumResearchParagraphTextSelectionSourceMismatchError(
            "Verified exact-range-selection sidecar uses an unsupported offset unit."
        )


def _is_sha256(value: Any) -> bool:
    return (
        type(value) is str
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


__all__ = [
    "ChromiumPageResearchLoadedParagraphTextSelectionRecord",
    "ChromiumResearchParagraphTextSelectionSourceMismatchError",
    "load_chromium_research_paragraph_text_selection",
]
