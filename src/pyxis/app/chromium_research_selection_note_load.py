from __future__ import annotations

from dataclasses import dataclass
import hmac
from pathlib import Path
from typing import Any

from .chromium_research_capture_load import ChromiumPageResearchLoadedCaptureEvidence
from .chromium_research_passage_selection import (
    select_chromium_research_capture_paragraph,
)
from .chromium_research_selection_note import (
    ChromiumPageResearchParagraphNoteRecord,
    create_chromium_research_paragraph_note,
)
from .chromium_research_selection_note_persistence import (
    ChromiumPageResearchParagraphNoteVerificationEvidence,
    verify_chromium_research_paragraph_note,
)


_CAPTURE_FORMAT = "pyxis.chromium.research_capture.v1"
_SELECTION_MODE = "caller_explicit_returned_paragraph_ordinal"
_NOTE_MODE = "caller_authored_exact_text_on_paragraph_selection"


class ChromiumResearchParagraphNoteSourceMismatchError(ValueError):
    """Raised when a verified note sidecar references a different capture."""


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchLoadedParagraphNoteRecord:
    """One verified durable human note relinked to supplied loaded source evidence.

    `verification` is the exact fresh 17C sidecar-verification evidence produced
    during this load. `note` is a newly reconstructed 17B note whose selection
    retains the exact caller-supplied 16C loaded-capture object and exact existing
    paragraph object.

    Relinking proves only that the sidecar's durable source-content reference
    matches the supplied capture's retained 16B verification identity. It does
    not authenticate either artifact, identify the human author, prove source
    truth, verify a quotation/citation, or establish chain of custody.
    """

    verification: ChromiumPageResearchParagraphNoteVerificationEvidence
    note: ChromiumPageResearchParagraphNoteRecord


def load_chromium_research_paragraph_note(
    source: ChromiumPageResearchLoadedCaptureEvidence,
    note_source: Path,
) -> ChromiumPageResearchLoadedParagraphNoteRecord:
    """Verify one note sidecar and relink it to one explicit loaded capture.

    The sidecar is always re-verified from its caller-supplied path. This
    operation does not accept a caller-constructed verification dataclass as a
    substitute for file verification.

    The verified sidecar's capture format and bundle SHA-256 must match the exact
    16B verification evidence retained by the supplied 16C loaded capture before
    any selection/note reconstruction occurs. Reconstruction then delegates to
    the existing public 17A selector and 17B note constructor.

    This operation performs no Chromium acquisition, source-capture file search,
    capture rehydration, persistence, source-path inference, ranking, semantic
    interpretation, authorship inference, or authenticity/provenance upgrade.
    """

    if not isinstance(source, ChromiumPageResearchLoadedCaptureEvidence):
        raise TypeError("source must be ChromiumPageResearchLoadedCaptureEvidence.")

    verification = verify_chromium_research_paragraph_note(note_source)
    _validate_source_reference(source, verification)

    selection = select_chromium_research_capture_paragraph(
        source,
        paragraph_ordinal=verification.paragraph_ordinal,
    )
    if selection.selection_mode != verification.selection_mode:
        raise ChromiumResearchParagraphNoteSourceMismatchError(
            "Reconstructed paragraph selection mode does not match the verified sidecar."
        )

    note = create_chromium_research_paragraph_note(
        selection,
        note_text=verification.note_text,
    )
    if note.note_mode != verification.note_mode or note.note_text != verification.note_text:
        raise ChromiumResearchParagraphNoteSourceMismatchError(
            "Reconstructed paragraph note does not match the verified sidecar."
        )

    return ChromiumPageResearchLoadedParagraphNoteRecord(
        verification=verification,
        note=note,
    )


def _validate_source_reference(
    source: ChromiumPageResearchLoadedCaptureEvidence,
    verification: ChromiumPageResearchParagraphNoteVerificationEvidence,
) -> None:
    source_verification = source.verification

    if source_verification.capture_format != _CAPTURE_FORMAT:
        raise ChromiumResearchParagraphNoteSourceMismatchError(
            "Supplied source capture format is unsupported for paragraph-note relinking."
        )
    if not _is_sha256(source_verification.bundle_sha256):
        raise ChromiumResearchParagraphNoteSourceMismatchError(
            "Supplied source capture bundle SHA-256 has an invalid shape."
        )

    if verification.source_capture_format != source_verification.capture_format:
        raise ChromiumResearchParagraphNoteSourceMismatchError(
            "Verified paragraph-note sidecar references a different capture format."
        )
    if not hmac.compare_digest(
        verification.source_bundle_sha256,
        source_verification.bundle_sha256,
    ):
        raise ChromiumResearchParagraphNoteSourceMismatchError(
            "Verified paragraph-note sidecar references a different capture bundle."
        )

    if verification.selection_mode != _SELECTION_MODE:
        raise ChromiumResearchParagraphNoteSourceMismatchError(
            "Verified paragraph-note sidecar uses an unsupported selection mode."
        )
    if verification.note_mode != _NOTE_MODE:
        raise ChromiumResearchParagraphNoteSourceMismatchError(
            "Verified paragraph-note sidecar uses an unsupported note mode."
        )


def _is_sha256(value: Any) -> bool:
    return (
        type(value) is str
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )
