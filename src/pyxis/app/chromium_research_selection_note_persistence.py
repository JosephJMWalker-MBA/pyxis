from __future__ import annotations

from dataclasses import dataclass
import hashlib
import hmac
import json
from pathlib import Path
from typing import Any

from .chromium_research_capture_load import ChromiumPageResearchLoadedCaptureEvidence
from .chromium_research_passage_selection import (
    ChromiumPageResearchParagraphSelectionEvidence,
)
from .chromium_research_selection_note import (
    ChromiumPageResearchParagraphNoteRecord,
)


_NOTE_FORMAT = "pyxis.chromium.research_paragraph_note.v1"
_CAPTURE_FORMAT = "pyxis.chromium.research_capture.v1"
_SELECTION_MODE = "caller_explicit_returned_paragraph_ordinal"
_NOTE_MODE = "caller_authored_exact_text_on_paragraph_selection"


class ChromiumResearchParagraphNoteIntegrityError(ValueError):
    """Raised when persisted paragraph-note bytes fail their narrow integrity contract."""


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchParagraphNotePersistenceEvidence:
    """Durable-file evidence for one already-created human note record.

    `note` retains the exact in-memory 17B record supplied to persistence. The
    persisted sidecar does not serialize the full selected paragraph or loaded
    capture. It stores only the durable source-capture content reference needed
    to identify the attachment context plus the caller-owned selection/note facts.
    """

    path: Path
    note_format: str
    note_record_sha256: str
    byte_count: int
    note: ChromiumPageResearchParagraphNoteRecord


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchParagraphNoteVerificationEvidence:
    """Verified file-level integrity facts for one persisted human note sidecar.

    Successful verification proves only that the sidecar is canonical Pyxis note
    JSON and that its complete note-reference payload matches the recorded SHA-256.
    It does not authenticate the caller, reopen the referenced capture, prove the
    referenced source is present, or establish any truth/support relationship
    between the human note and the selected paragraph.
    """

    path: Path
    note_format: str
    note_record_sha256: str
    byte_count: int
    source_capture_format: str
    source_bundle_sha256: str
    selection_mode: str
    paragraph_ordinal: int
    note_mode: str
    note_text: str
    document_json: str


def persist_chromium_research_paragraph_note(
    note: ChromiumPageResearchParagraphNoteRecord,
    destination: Path,
) -> ChromiumPageResearchParagraphNotePersistenceEvidence:
    """Persist one exact 17B note as deterministic no-overwrite sidecar JSON.

    Persistence consumes an already-created note record. It does not reopen the
    source capture, reacquire Chromium, copy page/paragraph text into the sidecar,
    infer author/time metadata, or promote the note into source evidence.

    The sidecar references the already-durable source only by its established
    capture format and bundle SHA-256 together with the explicit paragraph ordinal.
    The embedded SHA-256 protects self-integrity of that complete reference + note
    payload; it is not authentication or authorship evidence.
    """

    _validate_live_note_reference(note)

    path = Path(destination).expanduser().resolve()
    if not path.parent.is_dir():
        raise FileNotFoundError(
            f"Research paragraph-note parent directory does not exist: {path.parent}"
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

    return ChromiumPageResearchParagraphNotePersistenceEvidence(
        path=path,
        note_format=_NOTE_FORMAT,
        note_record_sha256=note_record_sha256,
        byte_count=len(document_bytes),
        note=note,
    )


def verify_chromium_research_paragraph_note(
    source: Path,
) -> ChromiumPageResearchParagraphNoteVerificationEvidence:
    """Verify canonical bytes and recorded digest for one note sidecar only.

    This operation reads only the sidecar file. It deliberately does not locate,
    read, verify, or rehydrate the referenced 16B/16C source capture. Relinking a
    durable note to durable source evidence is a separate authority boundary.
    """

    path = Path(source).expanduser().resolve()
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ChromiumResearchParagraphNoteIntegrityError(
            "Research paragraph note is not valid UTF-8."
        ) from exc

    try:
        document = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ChromiumResearchParagraphNoteIntegrityError(
            "Research paragraph note is not valid JSON."
        ) from exc

    note_record, recorded_sha256 = _validate_persisted_document(document)
    observed_sha256 = hashlib.sha256(_canonical_json_bytes(note_record)).hexdigest()
    if not hmac.compare_digest(recorded_sha256, observed_sha256):
        raise ChromiumResearchParagraphNoteIntegrityError(
            "Research paragraph-note SHA-256 does not match the persisted record."
        )

    canonical_document_bytes = _canonical_document_bytes(document)
    if raw != canonical_document_bytes:
        raise ChromiumResearchParagraphNoteIntegrityError(
            "Research paragraph-note bytes are not in the canonical Pyxis JSON encoding."
        )

    source_capture = note_record["source_capture"]
    selection = note_record["selection"]
    note = note_record["note"]
    return ChromiumPageResearchParagraphNoteVerificationEvidence(
        path=path,
        note_format=_NOTE_FORMAT,
        note_record_sha256=recorded_sha256,
        byte_count=len(raw),
        source_capture_format=source_capture["format"],
        source_bundle_sha256=source_capture["bundle_sha256"],
        selection_mode=selection["mode"],
        paragraph_ordinal=selection["paragraph_ordinal"],
        note_mode=note["mode"],
        note_text=note["text"],
        document_json=text,
    )


def _validate_live_note_reference(
    note: ChromiumPageResearchParagraphNoteRecord,
) -> None:
    if not isinstance(note, ChromiumPageResearchParagraphNoteRecord):
        raise TypeError("note must be ChromiumPageResearchParagraphNoteRecord.")
    if note.note_mode != _NOTE_MODE:
        raise ValueError("note mode is unsupported for durable paragraph-note persistence.")
    if type(note.note_text) is not str or not note.note_text.strip():
        raise ValueError("note text must retain non-whitespace caller-authored text.")

    selection = note.selection
    if not isinstance(selection, ChromiumPageResearchParagraphSelectionEvidence):
        raise ValueError("note selection is not paragraph-selection evidence.")
    if selection.selection_mode != _SELECTION_MODE:
        raise ValueError("selection mode is unsupported for durable paragraph-note persistence.")

    source = selection.source
    if not isinstance(source, ChromiumPageResearchLoadedCaptureEvidence):
        raise ValueError("selection source is not verified rehydrated capture evidence.")
    verification = source.verification
    if verification.capture_format != _CAPTURE_FORMAT:
        raise ValueError("source capture format is unsupported for durable paragraph-note persistence.")
    if not _is_sha256(verification.bundle_sha256):
        raise ValueError("source capture bundle SHA-256 has an invalid shape.")

    paragraph = selection.paragraph
    ordinal = paragraph.ordinal
    paragraphs = source.bundle.paragraphs.paragraphs
    if type(ordinal) is not int or ordinal < 1 or ordinal > len(paragraphs):
        raise ValueError("selection paragraph ordinal is outside returned source evidence.")
    if paragraphs[ordinal - 1] is not paragraph:
        raise ValueError(
            "selection paragraph is not the exact paragraph object retained by its source."
        )


def _note_record_payload(note: ChromiumPageResearchParagraphNoteRecord) -> dict[str, Any]:
    selection = note.selection
    return {
        "note": {
            "mode": note.note_mode,
            "text": note.note_text,
        },
        "selection": {
            "mode": selection.selection_mode,
            "paragraph_ordinal": selection.paragraph.ordinal,
        },
        "source_capture": {
            "bundle_sha256": selection.source.verification.bundle_sha256,
            "format": selection.source.verification.capture_format,
        },
    }


def _validate_persisted_document(document: Any) -> tuple[dict[str, Any], str]:
    if type(document) is not dict or set(document) != {
        "format",
        "note_record",
        "note_record_sha256",
    }:
        raise ChromiumResearchParagraphNoteIntegrityError(
            "Research paragraph-note document has an invalid top-level shape."
        )
    if document["format"] != _NOTE_FORMAT:
        raise ChromiumResearchParagraphNoteIntegrityError(
            "Research paragraph-note format is unsupported."
        )

    recorded_sha256 = document["note_record_sha256"]
    if not _is_sha256(recorded_sha256):
        raise ChromiumResearchParagraphNoteIntegrityError(
            "Research paragraph-note SHA-256 has an invalid shape."
        )

    note_record = document["note_record"]
    if type(note_record) is not dict or set(note_record) != {
        "note",
        "selection",
        "source_capture",
    }:
        raise ChromiumResearchParagraphNoteIntegrityError(
            "Research paragraph-note record has an invalid shape."
        )

    source_capture = note_record["source_capture"]
    if type(source_capture) is not dict or set(source_capture) != {
        "bundle_sha256",
        "format",
    }:
        raise ChromiumResearchParagraphNoteIntegrityError(
            "Research paragraph-note source-capture reference has an invalid shape."
        )
    if source_capture["format"] != _CAPTURE_FORMAT:
        raise ChromiumResearchParagraphNoteIntegrityError(
            "Research paragraph-note source capture format is unsupported."
        )
    if not _is_sha256(source_capture["bundle_sha256"]):
        raise ChromiumResearchParagraphNoteIntegrityError(
            "Research paragraph-note source bundle SHA-256 has an invalid shape."
        )

    selection = note_record["selection"]
    if type(selection) is not dict or set(selection) != {"mode", "paragraph_ordinal"}:
        raise ChromiumResearchParagraphNoteIntegrityError(
            "Research paragraph-note selection reference has an invalid shape."
        )
    if selection["mode"] != _SELECTION_MODE:
        raise ChromiumResearchParagraphNoteIntegrityError(
            "Research paragraph-note selection mode is unsupported."
        )
    paragraph_ordinal = selection["paragraph_ordinal"]
    if type(paragraph_ordinal) is not int or paragraph_ordinal < 1:
        raise ChromiumResearchParagraphNoteIntegrityError(
            "Research paragraph-note paragraph ordinal must be a positive integer."
        )

    note = note_record["note"]
    if type(note) is not dict or set(note) != {"mode", "text"}:
        raise ChromiumResearchParagraphNoteIntegrityError(
            "Research paragraph-note human-note record has an invalid shape."
        )
    if note["mode"] != _NOTE_MODE:
        raise ChromiumResearchParagraphNoteIntegrityError(
            "Research paragraph-note note mode is unsupported."
        )
    note_text = note["text"]
    if type(note_text) is not str or not note_text.strip():
        raise ChromiumResearchParagraphNoteIntegrityError(
            "Research paragraph-note text must contain non-whitespace caller-authored text."
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
            "Research paragraph-note record is not canonical-JSON serializable."
        ) from exc
    return encoded.encode("utf-8")


def _canonical_document_bytes(document: Any) -> bytes:
    return _canonical_json_bytes(document) + b"\n"
