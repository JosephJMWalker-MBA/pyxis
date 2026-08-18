from __future__ import annotations

from dataclasses import dataclass
import hashlib
import hmac
import json
from pathlib import Path
from typing import Any

from .chromium_research_working_set_load import load_chromium_research_working_set
from .chromium_research_working_set_note import (
    ChromiumPageResearchWorkingSetNoteRecord,
    create_chromium_research_working_set_note,
)


_WORKING_SET_NOTE_FORMAT = "pyxis.chromium.research_working_set_note.v1"
_WORKING_SET_FORMAT = "pyxis.chromium.research_working_set.v1"
_NOTE_MODE = "caller_authored_note_on_research_working_set"


class ChromiumResearchWorkingSetNoteIntegrityError(ValueError):
    """Raised when persisted working-set-note bytes fail their integrity contract."""


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchWorkingSetNotePersistenceEvidence:
    """Durable-file evidence for one already-created 21A working-set note.

    `note` retains the exact live 21A object supplied to persistence. The durable
    file stores only the durable 20B parent working-set identity plus the caller's
    exact note mode/text. It does not copy the parent member graph or any source
    evidence.
    """

    path: Path
    note_format: str
    note_record_sha256: str
    byte_count: int
    note: ChromiumPageResearchWorkingSetNoteRecord


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchWorkingSetNoteVerificationEvidence:
    """Verified file-local integrity facts for one 21B working-set-note sidecar.

    Verification proves canonical structure and self-integrity only. It does not
    locate, read, verify, or relink the referenced 20B working-set sidecar and does
    not establish that the human rationale is correct.
    """

    path: Path
    note_format: str
    note_record_sha256: str
    byte_count: int
    working_set_format: str
    working_set_record_sha256: str
    note_mode: str
    note_text: str
    document_json: str


def persist_chromium_research_working_set_note(
    note: ChromiumPageResearchWorkingSetNoteRecord,
    working_set_source: Path,
    destination: Path,
) -> ChromiumPageResearchWorkingSetNotePersistenceEvidence:
    """Persist one 21A note against one explicitly supplied durable 20B parent.

    The live note is first re-established through 21A. The caller-supplied 20B
    working-set path is then freshly verified and relinked through public 20C using
    the exact member sequence retained by the note's working set. This earns only
    the durable parent identity needed by the 21B sidecar.

    Persistence does not reread individual member sidecars, discover a working set,
    search by digest, copy member/source evidence, or infer note semantics. The
    recorded SHA-256 is self-integrity evidence only.
    """

    if not isinstance(note, ChromiumPageResearchWorkingSetNoteRecord):
        raise TypeError("note must be ChromiumPageResearchWorkingSetNoteRecord.")

    rebuilt_note = create_chromium_research_working_set_note(
        note.working_set,
        note_text=note.note_text,
    )
    if rebuilt_note.note_mode != note.note_mode:
        raise ValueError("working-set note mode is unsupported for durable persistence.")

    loaded_parent = load_chromium_research_working_set(
        note.working_set.items,
        working_set_source,
    )
    if loaded_parent.verification.working_set_format != _WORKING_SET_FORMAT:
        raise ValueError("working-set format is unsupported for note persistence.")

    if len(loaded_parent.working_set.items) != len(note.working_set.items):
        raise ValueError("relinked working-set member count is incoherent with the note parent.")
    for index, (observed, supplied) in enumerate(
        zip(loaded_parent.working_set.items, note.working_set.items)
    ):
        if observed is not supplied:
            raise ValueError(
                f"relinked working-set item {index} does not retain the note parent's exact member object."
            )

    path = Path(destination).expanduser().resolve()
    if not path.parent.is_dir():
        raise FileNotFoundError(
            f"Research working-set-note parent directory does not exist: {path.parent}"
        )

    note_record = {
        "note": {
            "mode": note.note_mode,
            "text": note.note_text,
        },
        "working_set_reference": {
            "format": loaded_parent.verification.working_set_format,
            "working_set_record_sha256": (
                loaded_parent.verification.working_set_record_sha256
            ),
        },
    }
    note_record_bytes = _canonical_json_bytes(note_record)
    note_record_sha256 = hashlib.sha256(note_record_bytes).hexdigest()
    document = {
        "format": _WORKING_SET_NOTE_FORMAT,
        "note_record": note_record,
        "note_record_sha256": note_record_sha256,
    }
    document_bytes = _canonical_document_bytes(document)

    with path.open("xb") as handle:
        handle.write(document_bytes)

    return ChromiumPageResearchWorkingSetNotePersistenceEvidence(
        path=path,
        note_format=_WORKING_SET_NOTE_FORMAT,
        note_record_sha256=note_record_sha256,
        byte_count=len(document_bytes),
        note=note,
    )


def verify_chromium_research_working_set_note(
    source: Path,
) -> ChromiumPageResearchWorkingSetNoteVerificationEvidence:
    """Verify one 21B sidecar without opening its referenced working-set parent.

    A self-consistent file may therefore contain a structurally valid but wrong
    parent working-set digest and still pass 21B verification. Parent identity
    correctness requires a later explicit relinking boundary.
    """

    path = Path(source).expanduser().resolve()
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ChromiumResearchWorkingSetNoteIntegrityError(
            "Research working-set note is not valid UTF-8."
        ) from exc

    try:
        document = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ChromiumResearchWorkingSetNoteIntegrityError(
            "Research working-set note is not valid JSON."
        ) from exc

    note_record, recorded_sha256 = _validate_persisted_document(document)
    observed_sha256 = hashlib.sha256(_canonical_json_bytes(note_record)).hexdigest()
    if not hmac.compare_digest(recorded_sha256, observed_sha256):
        raise ChromiumResearchWorkingSetNoteIntegrityError(
            "Research working-set-note SHA-256 does not match the persisted record."
        )

    canonical_document_bytes = _canonical_document_bytes(document)
    if raw != canonical_document_bytes:
        raise ChromiumResearchWorkingSetNoteIntegrityError(
            "Research working-set-note bytes are not in the canonical Pyxis JSON encoding."
        )

    working_set_reference = note_record["working_set_reference"]
    note_payload = note_record["note"]
    return ChromiumPageResearchWorkingSetNoteVerificationEvidence(
        path=path,
        note_format=_WORKING_SET_NOTE_FORMAT,
        note_record_sha256=recorded_sha256,
        byte_count=len(raw),
        working_set_format=working_set_reference["format"],
        working_set_record_sha256=(
            working_set_reference["working_set_record_sha256"]
        ),
        note_mode=note_payload["mode"],
        note_text=note_payload["text"],
        document_json=text,
    )


def _validate_persisted_document(document: Any) -> tuple[dict[str, Any], str]:
    if type(document) is not dict or set(document) != {
        "format",
        "note_record",
        "note_record_sha256",
    }:
        raise ChromiumResearchWorkingSetNoteIntegrityError(
            "Research working-set-note document has an invalid top-level shape."
        )
    if document["format"] != _WORKING_SET_NOTE_FORMAT:
        raise ChromiumResearchWorkingSetNoteIntegrityError(
            "Research working-set-note format is unsupported."
        )

    recorded_sha256 = document["note_record_sha256"]
    if not _is_sha256(recorded_sha256):
        raise ChromiumResearchWorkingSetNoteIntegrityError(
            "Research working-set-note SHA-256 has an invalid shape."
        )

    note_record = document["note_record"]
    if type(note_record) is not dict or set(note_record) != {
        "note",
        "working_set_reference",
    }:
        raise ChromiumResearchWorkingSetNoteIntegrityError(
            "Research working-set-note record has an invalid shape."
        )

    working_set_reference = note_record["working_set_reference"]
    if type(working_set_reference) is not dict or set(working_set_reference) != {
        "format",
        "working_set_record_sha256",
    }:
        raise ChromiumResearchWorkingSetNoteIntegrityError(
            "Research working-set-note parent reference has an invalid shape."
        )
    if working_set_reference["format"] != _WORKING_SET_FORMAT:
        raise ChromiumResearchWorkingSetNoteIntegrityError(
            "Research working-set-note parent format is unsupported."
        )
    if not _is_sha256(working_set_reference["working_set_record_sha256"]):
        raise ChromiumResearchWorkingSetNoteIntegrityError(
            "Research working-set-note parent SHA-256 has an invalid shape."
        )

    note_payload = note_record["note"]
    if type(note_payload) is not dict or set(note_payload) != {"mode", "text"}:
        raise ChromiumResearchWorkingSetNoteIntegrityError(
            "Research working-set-note human note has an invalid shape."
        )
    if note_payload["mode"] != _NOTE_MODE:
        raise ChromiumResearchWorkingSetNoteIntegrityError(
            "Research working-set-note mode is unsupported."
        )
    note_text = note_payload["text"]
    if type(note_text) is not str or not note_text.strip():
        raise ChromiumResearchWorkingSetNoteIntegrityError(
            "Research working-set-note text must contain non-whitespace human text."
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
            "Research working-set-note record is not canonical-JSON serializable."
        ) from exc
    return encoded.encode("utf-8")


def _canonical_document_bytes(document: Any) -> bytes:
    return _canonical_json_bytes(document) + b"\n"
