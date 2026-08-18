from __future__ import annotations

from dataclasses import dataclass
import hashlib
import hmac
import json
from pathlib import Path
from typing import Any

from .chromium_research_capture_load import ChromiumPageResearchLoadedCaptureEvidence
from .chromium_research_paragraph_text_selection_comparison_note import (
    ChromiumPageResearchParagraphTextSelectionComparisonNoteRecord,
    create_chromium_research_paragraph_text_selection_comparison_note,
)


_NOTE_FORMAT = "pyxis.chromium.research_paragraph_text_selection_comparison_note.v1"
_CAPTURE_FORMAT = "pyxis.chromium.research_capture.v1"
_PARAGRAPH_SELECTION_MODE = "caller_explicit_returned_paragraph_ordinal"
_TEXT_SELECTION_MODE = "caller_explicit_returned_paragraph_text_range"
_OFFSET_UNIT = "unicode_code_point"
_COMPARISON_MODE = "caller_explicit_exact_text_range_comparison"
_NOTE_MODE = "caller_authored_note_on_exact_text_range_comparison"


class ChromiumResearchParagraphTextSelectionComparisonNoteIntegrityError(ValueError):
    """Raised when persisted comparison-note bytes fail their integrity contract."""


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchParagraphTextSelectionComparisonNotePersistenceEvidence:
    """Durable-file evidence for one already-created 19B human comparison note.

    `note` retains the exact in-memory 19B record supplied to persistence. The
    sidecar does not serialize selected source text, loaded capture graphs, source
    paths, or browser transport facts. It stores only two durable source-content
    references plus the caller-owned comparison mode and verbatim note.
    """

    path: Path
    note_format: str
    note_record_sha256: str
    byte_count: int
    note: ChromiumPageResearchParagraphTextSelectionComparisonNoteRecord


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchParagraphTextSelectionComparisonNoteVerificationEvidence:
    """Verified file-local integrity facts for one 19C comparison-note sidecar.

    Verification proves canonical Pyxis JSON, the recorded SHA-256, and the narrow
    structural/domain shape of both durable range references plus the human note.
    It does not reopen either source capture, prove either range still addresses
    source evidence, authenticate the caller, or establish any semantic relation.
    """

    path: Path
    note_format: str
    note_record_sha256: str
    byte_count: int
    comparison_mode: str
    first_source_capture_format: str
    first_source_bundle_sha256: str
    first_paragraph_selection_mode: str
    first_paragraph_ordinal: int
    first_text_selection_mode: str
    first_offset_unit: str
    first_start_offset: int
    first_end_offset: int
    second_source_capture_format: str
    second_source_bundle_sha256: str
    second_paragraph_selection_mode: str
    second_paragraph_ordinal: int
    second_text_selection_mode: str
    second_offset_unit: str
    second_start_offset: int
    second_end_offset: int
    note_mode: str
    note_text: str
    document_json: str


def persist_chromium_research_paragraph_text_selection_comparison_note(
    note: ChromiumPageResearchParagraphTextSelectionComparisonNoteRecord,
    destination: Path,
) -> ChromiumPageResearchParagraphTextSelectionComparisonNotePersistenceEvidence:
    """Persist one 19B comparison note as deterministic no-overwrite JSON.

    Persistence re-establishes the live 19B→19A→18A contract and validates both
    retained durable capture-reference shapes. It does not reread either source
    capture, reacquire Chromium, copy selected source text, infer author/time
    metadata, or grant semantic/citation authority.

    `note_record_sha256` covers the complete two-source reference, comparison mode,
    and exact human note. It is self-integrity evidence only.
    """

    _validate_live_note_reference(note)

    path = Path(destination).expanduser().resolve()
    if not path.parent.is_dir():
        raise FileNotFoundError(
            f"Research comparison-note parent directory does not exist: {path.parent}"
        )

    note_record = _note_record_payload(note)
    note_record_bytes = _canonical_json_bytes(note_record)
    note_record_sha256 = hashlib.sha256(note_record_bytes).hexdigest()
    document = {
        "format": _NOTE_FORMAT,
        "note_record": note_record,
        "note_record_sha256": note_record_sha256,
    }
    document_bytes = _canonical_document_bytes(document)

    with path.open("xb") as handle:
        handle.write(document_bytes)

    return ChromiumPageResearchParagraphTextSelectionComparisonNotePersistenceEvidence(
        path=path,
        note_format=_NOTE_FORMAT,
        note_record_sha256=note_record_sha256,
        byte_count=len(document_bytes),
        note=note,
    )


def verify_chromium_research_paragraph_text_selection_comparison_note(
    source: Path,
) -> ChromiumPageResearchParagraphTextSelectionComparisonNoteVerificationEvidence:
    """Verify canonical bytes and digest for one 19C sidecar only.

    This operation reads only the comparison-note sidecar. It deliberately does
    not locate, read, verify, or rehydrate either referenced source capture. A
    structurally valid self-consistent file therefore does not prove its persisted
    coordinates still address caller-supplied source evidence.
    """

    path = Path(source).expanduser().resolve()
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ChromiumResearchParagraphTextSelectionComparisonNoteIntegrityError(
            "Research comparison note is not valid UTF-8."
        ) from exc

    try:
        document = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ChromiumResearchParagraphTextSelectionComparisonNoteIntegrityError(
            "Research comparison note is not valid JSON."
        ) from exc

    note_record, recorded_sha256 = _validate_persisted_document(document)
    observed_sha256 = hashlib.sha256(_canonical_json_bytes(note_record)).hexdigest()
    if not hmac.compare_digest(recorded_sha256, observed_sha256):
        raise ChromiumResearchParagraphTextSelectionComparisonNoteIntegrityError(
            "Research comparison-note SHA-256 does not match the persisted record."
        )

    canonical_document_bytes = _canonical_document_bytes(document)
    if raw != canonical_document_bytes:
        raise ChromiumResearchParagraphTextSelectionComparisonNoteIntegrityError(
            "Research comparison-note bytes are not in canonical Pyxis JSON encoding."
        )

    comparison = note_record["comparison"]
    first = comparison["first"]
    second = comparison["second"]
    first_source = first["source_capture"]
    first_paragraph = first["selection"]["paragraph"]
    first_range = first["selection"]["text_range"]
    second_source = second["source_capture"]
    second_paragraph = second["selection"]["paragraph"]
    second_range = second["selection"]["text_range"]
    human_note = note_record["note"]

    return ChromiumPageResearchParagraphTextSelectionComparisonNoteVerificationEvidence(
        path=path,
        note_format=_NOTE_FORMAT,
        note_record_sha256=recorded_sha256,
        byte_count=len(raw),
        comparison_mode=comparison["mode"],
        first_source_capture_format=first_source["format"],
        first_source_bundle_sha256=first_source["bundle_sha256"],
        first_paragraph_selection_mode=first_paragraph["mode"],
        first_paragraph_ordinal=first_paragraph["ordinal"],
        first_text_selection_mode=first_range["mode"],
        first_offset_unit=first_range["offset_unit"],
        first_start_offset=first_range["start_offset"],
        first_end_offset=first_range["end_offset"],
        second_source_capture_format=second_source["format"],
        second_source_bundle_sha256=second_source["bundle_sha256"],
        second_paragraph_selection_mode=second_paragraph["mode"],
        second_paragraph_ordinal=second_paragraph["ordinal"],
        second_text_selection_mode=second_range["mode"],
        second_offset_unit=second_range["offset_unit"],
        second_start_offset=second_range["start_offset"],
        second_end_offset=second_range["end_offset"],
        note_mode=human_note["mode"],
        note_text=human_note["text"],
        document_json=text,
    )


def _validate_live_note_reference(
    note: ChromiumPageResearchParagraphTextSelectionComparisonNoteRecord,
) -> None:
    if not isinstance(
        note, ChromiumPageResearchParagraphTextSelectionComparisonNoteRecord
    ):
        raise TypeError(
            "note must be "
            "ChromiumPageResearchParagraphTextSelectionComparisonNoteRecord."
        )
    if note.note_mode != _NOTE_MODE:
        raise ValueError("note mode is unsupported for durable comparison-note persistence.")
    if type(note.note_text) is not str or not note.note_text.strip():
        raise ValueError("note text must retain non-whitespace caller-authored text.")

    # Reuse 19B, which in turn re-establishes 19A and both 18A exact ranges. The
    # temporary result is validation only; persistence retains the caller's note.
    create_chromium_research_paragraph_text_selection_comparison_note(
        note.comparison,
        note_text=note.note_text,
    )

    _validate_live_selection_source(note.comparison.first_selection, role="first")
    _validate_live_selection_source(note.comparison.second_selection, role="second")


def _validate_live_selection_source(selection: Any, *, role: str) -> None:
    loaded_capture = selection.source.source
    if not isinstance(loaded_capture, ChromiumPageResearchLoadedCaptureEvidence):
        raise ValueError(
            f"{role} comparison range source is not verified rehydrated capture evidence."
        )
    verification = loaded_capture.verification
    if verification.capture_format != _CAPTURE_FORMAT:
        raise ValueError(
            f"{role} source capture format is unsupported for durable comparison-note persistence."
        )
    if not _is_sha256(verification.bundle_sha256):
        raise ValueError(f"{role} source capture bundle SHA-256 has an invalid shape.")


def _note_record_payload(
    note: ChromiumPageResearchParagraphTextSelectionComparisonNoteRecord,
) -> dict[str, Any]:
    return {
        "comparison": {
            "first": _selection_reference_payload(note.comparison.first_selection),
            "mode": note.comparison.comparison_mode,
            "second": _selection_reference_payload(note.comparison.second_selection),
        },
        "note": {
            "mode": note.note_mode,
            "text": note.note_text,
        },
    }


def _selection_reference_payload(selection: Any) -> dict[str, Any]:
    paragraph_selection = selection.source
    loaded_capture = paragraph_selection.source
    return {
        "selection": {
            "paragraph": {
                "mode": paragraph_selection.selection_mode,
                "ordinal": paragraph_selection.paragraph.ordinal,
            },
            "text_range": {
                "end_offset": selection.end_offset,
                "mode": selection.selection_mode,
                "offset_unit": selection.offset_unit,
                "start_offset": selection.start_offset,
            },
        },
        "source_capture": {
            "bundle_sha256": loaded_capture.verification.bundle_sha256,
            "format": loaded_capture.verification.capture_format,
        },
    }


def _validate_persisted_document(document: Any) -> tuple[dict[str, Any], str]:
    if type(document) is not dict or set(document) != {
        "format",
        "note_record",
        "note_record_sha256",
    }:
        raise ChromiumResearchParagraphTextSelectionComparisonNoteIntegrityError(
            "Research comparison-note document has an invalid top-level shape."
        )
    if document["format"] != _NOTE_FORMAT:
        raise ChromiumResearchParagraphTextSelectionComparisonNoteIntegrityError(
            "Research comparison-note format is unsupported."
        )

    recorded_sha256 = document["note_record_sha256"]
    if not _is_sha256(recorded_sha256):
        raise ChromiumResearchParagraphTextSelectionComparisonNoteIntegrityError(
            "Research comparison-note SHA-256 has an invalid shape."
        )

    note_record = document["note_record"]
    if type(note_record) is not dict or set(note_record) != {"comparison", "note"}:
        raise ChromiumResearchParagraphTextSelectionComparisonNoteIntegrityError(
            "Research comparison-note record has an invalid shape."
        )

    comparison = note_record["comparison"]
    if type(comparison) is not dict or set(comparison) != {"first", "mode", "second"}:
        raise ChromiumResearchParagraphTextSelectionComparisonNoteIntegrityError(
            "Research comparison record has an invalid shape."
        )
    if comparison["mode"] != _COMPARISON_MODE:
        raise ChromiumResearchParagraphTextSelectionComparisonNoteIntegrityError(
            "Research comparison mode is unsupported."
        )

    _validate_persisted_selection_reference(comparison["first"], role="first")
    _validate_persisted_selection_reference(comparison["second"], role="second")

    human_note = note_record["note"]
    if type(human_note) is not dict or set(human_note) != {"mode", "text"}:
        raise ChromiumResearchParagraphTextSelectionComparisonNoteIntegrityError(
            "Research comparison human-note record has an invalid shape."
        )
    if human_note["mode"] != _NOTE_MODE:
        raise ChromiumResearchParagraphTextSelectionComparisonNoteIntegrityError(
            "Research comparison note mode is unsupported."
        )
    note_text = human_note["text"]
    if type(note_text) is not str or not note_text.strip():
        raise ChromiumResearchParagraphTextSelectionComparisonNoteIntegrityError(
            "Research comparison-note text must contain non-whitespace caller-authored text."
        )

    return note_record, recorded_sha256


def _validate_persisted_selection_reference(reference: Any, *, role: str) -> None:
    prefix = f"Research comparison-note {role}"
    if type(reference) is not dict or set(reference) != {"selection", "source_capture"}:
        raise ChromiumResearchParagraphTextSelectionComparisonNoteIntegrityError(
            f"{prefix} range reference has an invalid shape."
        )

    source_capture = reference["source_capture"]
    if type(source_capture) is not dict or set(source_capture) != {
        "bundle_sha256",
        "format",
    }:
        raise ChromiumResearchParagraphTextSelectionComparisonNoteIntegrityError(
            f"{prefix} source-capture reference has an invalid shape."
        )
    if source_capture["format"] != _CAPTURE_FORMAT:
        raise ChromiumResearchParagraphTextSelectionComparisonNoteIntegrityError(
            f"{prefix} source capture format is unsupported."
        )
    if not _is_sha256(source_capture["bundle_sha256"]):
        raise ChromiumResearchParagraphTextSelectionComparisonNoteIntegrityError(
            f"{prefix} source bundle SHA-256 has an invalid shape."
        )

    selection = reference["selection"]
    if type(selection) is not dict or set(selection) != {"paragraph", "text_range"}:
        raise ChromiumResearchParagraphTextSelectionComparisonNoteIntegrityError(
            f"{prefix} selection reference has an invalid shape."
        )

    paragraph = selection["paragraph"]
    if type(paragraph) is not dict or set(paragraph) != {"mode", "ordinal"}:
        raise ChromiumResearchParagraphTextSelectionComparisonNoteIntegrityError(
            f"{prefix} paragraph reference has an invalid shape."
        )
    if paragraph["mode"] != _PARAGRAPH_SELECTION_MODE:
        raise ChromiumResearchParagraphTextSelectionComparisonNoteIntegrityError(
            f"{prefix} paragraph selection mode is unsupported."
        )
    paragraph_ordinal = paragraph["ordinal"]
    if type(paragraph_ordinal) is not int or paragraph_ordinal < 1:
        raise ChromiumResearchParagraphTextSelectionComparisonNoteIntegrityError(
            f"{prefix} paragraph ordinal must be a positive integer."
        )

    text_range = selection["text_range"]
    if type(text_range) is not dict or set(text_range) != {
        "end_offset",
        "mode",
        "offset_unit",
        "start_offset",
    }:
        raise ChromiumResearchParagraphTextSelectionComparisonNoteIntegrityError(
            f"{prefix} text-range reference has an invalid shape."
        )
    if text_range["mode"] != _TEXT_SELECTION_MODE:
        raise ChromiumResearchParagraphTextSelectionComparisonNoteIntegrityError(
            f"{prefix} text selection mode is unsupported."
        )
    if text_range["offset_unit"] != _OFFSET_UNIT:
        raise ChromiumResearchParagraphTextSelectionComparisonNoteIntegrityError(
            f"{prefix} offset unit is unsupported."
        )
    start_offset = text_range["start_offset"]
    end_offset = text_range["end_offset"]
    if type(start_offset) is not int or start_offset < 0:
        raise ChromiumResearchParagraphTextSelectionComparisonNoteIntegrityError(
            f"{prefix} start offset must be a non-negative integer."
        )
    if type(end_offset) is not int or end_offset <= start_offset:
        raise ChromiumResearchParagraphTextSelectionComparisonNoteIntegrityError(
            f"{prefix} end offset must be an integer greater than start offset."
        )


def _is_sha256(value: Any) -> bool:
    return (
        type(value) is str
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _canonical_json_bytes(payload: Any) -> bytes:
    try:
        encoded = json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise ValueError(
            "Research comparison-note record is not canonical-JSON serializable."
        ) from exc
    return encoded.encode("utf-8")


def _canonical_document_bytes(document: Any) -> bytes:
    return _canonical_json_bytes(document) + b"\n"
