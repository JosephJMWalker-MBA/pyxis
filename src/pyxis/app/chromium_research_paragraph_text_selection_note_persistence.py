from __future__ import annotations

from dataclasses import dataclass
import hashlib
import hmac
import json
from pathlib import Path
from typing import Any

from .chromium_research_capture_load import ChromiumPageResearchLoadedCaptureEvidence
from .chromium_research_paragraph_text_selection_note import (
    ChromiumPageResearchParagraphTextSelectionNoteRecord,
    create_chromium_research_paragraph_text_selection_note,
)


_NOTE_FORMAT = "pyxis.chromium.research_paragraph_text_selection_note.v1"
_CAPTURE_FORMAT = "pyxis.chromium.research_capture.v1"
_PARAGRAPH_SELECTION_MODE = "caller_explicit_returned_paragraph_ordinal"
_TEXT_SELECTION_MODE = "caller_explicit_returned_paragraph_text_range"
_OFFSET_UNIT = "unicode_code_point"
_NOTE_MODE = "caller_authored_exact_text_on_paragraph_text_selection"


class ChromiumResearchParagraphTextSelectionNoteIntegrityError(ValueError):
    """Raised when persisted exact-range-note bytes fail their integrity contract."""


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchParagraphTextSelectionNotePersistenceEvidence:
    """Durable-file evidence for one already-created exact-range human note.

    `note` retains the exact in-memory 18B record supplied to persistence. The
    sidecar does not serialize selected source text, the loaded capture, or the
    source path. It stores only durable source-content identity plus the layered
    caller-owned paragraph/range/note facts needed for later explicit relinking.
    """

    path: Path
    note_format: str
    note_record_sha256: str
    byte_count: int
    note: ChromiumPageResearchParagraphTextSelectionNoteRecord


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchParagraphTextSelectionNoteVerificationEvidence:
    """Verified file-level integrity facts for one exact-range-note sidecar.

    Verification is file-local. It proves canonical Pyxis JSON, the recorded
    SHA-256, and the narrow structural/domain shape of the durable reference. It
    does not reopen the source capture, prove the recorded range addresses that
    source, authenticate the caller, or promote the human note into source truth.
    """

    path: Path
    note_format: str
    note_record_sha256: str
    byte_count: int
    source_capture_format: str
    source_bundle_sha256: str
    paragraph_selection_mode: str
    paragraph_ordinal: int
    text_selection_mode: str
    offset_unit: str
    start_offset: int
    end_offset: int
    note_mode: str
    note_text: str
    document_json: str


def persist_chromium_research_paragraph_text_selection_note(
    note: ChromiumPageResearchParagraphTextSelectionNoteRecord,
    destination: Path,
) -> ChromiumPageResearchParagraphTextSelectionNotePersistenceEvidence:
    """Persist one exact 18B range note as deterministic no-overwrite JSON.

    Persistence re-establishes the live 18B/18A note-and-range contract from the
    supplied in-memory record and validates the retained durable capture-reference
    shape. It does not reread the source capture, reacquire Chromium, copy selected
    source text, infer author/time metadata, or grant quotation/citation authority.

    The sidecar SHA-256 covers the complete source-reference + human-action record.
    It is self-integrity evidence only, not authentication or authorship evidence.
    """

    _validate_live_note_reference(note)

    path = Path(destination).expanduser().resolve()
    if not path.parent.is_dir():
        raise FileNotFoundError(
            f"Research exact-range-note parent directory does not exist: {path.parent}"
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

    return ChromiumPageResearchParagraphTextSelectionNotePersistenceEvidence(
        path=path,
        note_format=_NOTE_FORMAT,
        note_record_sha256=note_record_sha256,
        byte_count=len(document_bytes),
        note=note,
    )


def verify_chromium_research_paragraph_text_selection_note(
    source: Path,
) -> ChromiumPageResearchParagraphTextSelectionNoteVerificationEvidence:
    """Verify canonical bytes and digest for one exact-range-note sidecar only.

    This operation reads only the sidecar. It deliberately does not locate, read,
    verify, or rehydrate the referenced source capture. A structurally valid,
    self-consistent sidecar therefore does not by itself prove that its coordinates
    address a supplied capture; explicit relinking remains a separate authority.
    """

    path = Path(source).expanduser().resolve()
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ChromiumResearchParagraphTextSelectionNoteIntegrityError(
            "Research exact-range note is not valid UTF-8."
        ) from exc

    try:
        document = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ChromiumResearchParagraphTextSelectionNoteIntegrityError(
            "Research exact-range note is not valid JSON."
        ) from exc

    note_record, recorded_sha256 = _validate_persisted_document(document)
    observed_sha256 = hashlib.sha256(_canonical_json_bytes(note_record)).hexdigest()
    if not hmac.compare_digest(recorded_sha256, observed_sha256):
        raise ChromiumResearchParagraphTextSelectionNoteIntegrityError(
            "Research exact-range-note SHA-256 does not match the persisted record."
        )

    canonical_document_bytes = _canonical_document_bytes(document)
    if raw != canonical_document_bytes:
        raise ChromiumResearchParagraphTextSelectionNoteIntegrityError(
            "Research exact-range-note bytes are not in the canonical Pyxis JSON encoding."
        )

    source_capture = note_record["source_capture"]
    selection = note_record["selection"]
    paragraph = selection["paragraph"]
    text_range = selection["text_range"]
    human_note = note_record["note"]
    return ChromiumPageResearchParagraphTextSelectionNoteVerificationEvidence(
        path=path,
        note_format=_NOTE_FORMAT,
        note_record_sha256=recorded_sha256,
        byte_count=len(raw),
        source_capture_format=source_capture["format"],
        source_bundle_sha256=source_capture["bundle_sha256"],
        paragraph_selection_mode=paragraph["mode"],
        paragraph_ordinal=paragraph["ordinal"],
        text_selection_mode=text_range["mode"],
        offset_unit=text_range["offset_unit"],
        start_offset=text_range["start_offset"],
        end_offset=text_range["end_offset"],
        note_mode=human_note["mode"],
        note_text=human_note["text"],
        document_json=text,
    )


def _validate_live_note_reference(
    note: ChromiumPageResearchParagraphTextSelectionNoteRecord,
) -> None:
    if not isinstance(note, ChromiumPageResearchParagraphTextSelectionNoteRecord):
        raise TypeError(
            "note must be ChromiumPageResearchParagraphTextSelectionNoteRecord."
        )
    if note.note_mode != _NOTE_MODE:
        raise ValueError("note mode is unsupported for durable exact-range-note persistence.")
    if type(note.note_text) is not str or not note.note_text.strip():
        raise ValueError("note text must retain non-whitespace caller-authored text.")

    # Reuse 18B, which in turn delegates exact range validity to 18A. The returned
    # temporary record is validation only; persistence retains the caller's note.
    create_chromium_research_paragraph_text_selection_note(
        note.selection,
        note_text=note.note_text,
    )

    loaded_capture = note.selection.source.source
    if not isinstance(loaded_capture, ChromiumPageResearchLoadedCaptureEvidence):
        raise ValueError("range-note source is not verified rehydrated capture evidence.")
    verification = loaded_capture.verification
    if verification.capture_format != _CAPTURE_FORMAT:
        raise ValueError(
            "source capture format is unsupported for durable exact-range-note persistence."
        )
    if not _is_sha256(verification.bundle_sha256):
        raise ValueError("source capture bundle SHA-256 has an invalid shape.")


def _note_record_payload(
    note: ChromiumPageResearchParagraphTextSelectionNoteRecord,
) -> dict[str, Any]:
    text_selection = note.selection
    paragraph_selection = text_selection.source
    loaded_capture = paragraph_selection.source
    return {
        "note": {
            "mode": note.note_mode,
            "text": note.note_text,
        },
        "selection": {
            "paragraph": {
                "mode": paragraph_selection.selection_mode,
                "ordinal": paragraph_selection.paragraph.ordinal,
            },
            "text_range": {
                "end_offset": text_selection.end_offset,
                "mode": text_selection.selection_mode,
                "offset_unit": text_selection.offset_unit,
                "start_offset": text_selection.start_offset,
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
        raise ChromiumResearchParagraphTextSelectionNoteIntegrityError(
            "Research exact-range-note document has an invalid top-level shape."
        )
    if document["format"] != _NOTE_FORMAT:
        raise ChromiumResearchParagraphTextSelectionNoteIntegrityError(
            "Research exact-range-note format is unsupported."
        )

    recorded_sha256 = document["note_record_sha256"]
    if not _is_sha256(recorded_sha256):
        raise ChromiumResearchParagraphTextSelectionNoteIntegrityError(
            "Research exact-range-note SHA-256 has an invalid shape."
        )

    note_record = document["note_record"]
    if type(note_record) is not dict or set(note_record) != {
        "note",
        "selection",
        "source_capture",
    }:
        raise ChromiumResearchParagraphTextSelectionNoteIntegrityError(
            "Research exact-range-note record has an invalid shape."
        )

    source_capture = note_record["source_capture"]
    if type(source_capture) is not dict or set(source_capture) != {
        "bundle_sha256",
        "format",
    }:
        raise ChromiumResearchParagraphTextSelectionNoteIntegrityError(
            "Research exact-range-note source-capture reference has an invalid shape."
        )
    if source_capture["format"] != _CAPTURE_FORMAT:
        raise ChromiumResearchParagraphTextSelectionNoteIntegrityError(
            "Research exact-range-note source capture format is unsupported."
        )
    if not _is_sha256(source_capture["bundle_sha256"]):
        raise ChromiumResearchParagraphTextSelectionNoteIntegrityError(
            "Research exact-range-note source bundle SHA-256 has an invalid shape."
        )

    selection = note_record["selection"]
    if type(selection) is not dict or set(selection) != {"paragraph", "text_range"}:
        raise ChromiumResearchParagraphTextSelectionNoteIntegrityError(
            "Research exact-range-note selection reference has an invalid shape."
        )

    paragraph = selection["paragraph"]
    if type(paragraph) is not dict or set(paragraph) != {"mode", "ordinal"}:
        raise ChromiumResearchParagraphTextSelectionNoteIntegrityError(
            "Research exact-range-note paragraph reference has an invalid shape."
        )
    if paragraph["mode"] != _PARAGRAPH_SELECTION_MODE:
        raise ChromiumResearchParagraphTextSelectionNoteIntegrityError(
            "Research exact-range-note paragraph selection mode is unsupported."
        )
    paragraph_ordinal = paragraph["ordinal"]
    if type(paragraph_ordinal) is not int or paragraph_ordinal < 1:
        raise ChromiumResearchParagraphTextSelectionNoteIntegrityError(
            "Research exact-range-note paragraph ordinal must be a positive integer."
        )

    text_range = selection["text_range"]
    if type(text_range) is not dict or set(text_range) != {
        "end_offset",
        "mode",
        "offset_unit",
        "start_offset",
    }:
        raise ChromiumResearchParagraphTextSelectionNoteIntegrityError(
            "Research exact-range-note text-range reference has an invalid shape."
        )
    if text_range["mode"] != _TEXT_SELECTION_MODE:
        raise ChromiumResearchParagraphTextSelectionNoteIntegrityError(
            "Research exact-range-note text selection mode is unsupported."
        )
    if text_range["offset_unit"] != _OFFSET_UNIT:
        raise ChromiumResearchParagraphTextSelectionNoteIntegrityError(
            "Research exact-range-note offset unit is unsupported."
        )
    start_offset = text_range["start_offset"]
    end_offset = text_range["end_offset"]
    if type(start_offset) is not int or start_offset < 0:
        raise ChromiumResearchParagraphTextSelectionNoteIntegrityError(
            "Research exact-range-note start offset must be a non-negative integer."
        )
    if type(end_offset) is not int or end_offset <= start_offset:
        raise ChromiumResearchParagraphTextSelectionNoteIntegrityError(
            "Research exact-range-note end offset must be an integer greater than start offset."
        )

    human_note = note_record["note"]
    if type(human_note) is not dict or set(human_note) != {"mode", "text"}:
        raise ChromiumResearchParagraphTextSelectionNoteIntegrityError(
            "Research exact-range-note human-note record has an invalid shape."
        )
    if human_note["mode"] != _NOTE_MODE:
        raise ChromiumResearchParagraphTextSelectionNoteIntegrityError(
            "Research exact-range-note note mode is unsupported."
        )
    note_text = human_note["text"]
    if type(note_text) is not str or not note_text.strip():
        raise ChromiumResearchParagraphTextSelectionNoteIntegrityError(
            "Research exact-range-note text must contain non-whitespace caller-authored text."
        )

    return note_record, recorded_sha256


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
            "Research exact-range-note record is not canonical-JSON serializable."
        ) from exc
    return encoded.encode("utf-8")


def _canonical_document_bytes(document: Any) -> bytes:
    return _canonical_json_bytes(document) + b"\n"
