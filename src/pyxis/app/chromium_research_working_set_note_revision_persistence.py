from __future__ import annotations

from dataclasses import dataclass
import hashlib
import hmac
import json
from pathlib import Path
from typing import Any

from .chromium_research_working_set_note_load import (
    load_chromium_research_working_set_note,
)
from .chromium_research_working_set_note_revision import (
    ChromiumPageResearchWorkingSetNoteRevisionRecord,
    create_chromium_research_working_set_note_revision,
)


_REVISION_FORMAT = "pyxis.chromium.research_working_set_note_revision.v1"
_REVISION_FORMAT_V2 = "pyxis.chromium.research_working_set_note_revision.v2"
_NOTE_FORMAT = "pyxis.chromium.research_working_set_note.v1"
_NOTE_FORMAT_V2 = "pyxis.chromium.research_working_set_note.v2"
_NOTE_MODE = "caller_authored_note_on_research_working_set"
_REVISION_MODE = "caller_authored_revision_of_research_working_set_note"


class ChromiumResearchWorkingSetNoteRevisionIntegrityError(ValueError):
    """Raised when persisted working-set-note-revision bytes fail integrity."""


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchWorkingSetNoteRevisionPersistenceEvidence:
    """Durable-file evidence for one already-created 22A revision.

    `revision` retains the exact live 22A object supplied to persistence. The
    durable file stores only the verified durable identity of the predecessor
    21B note plus the caller's exact revision mode and revised human wording.
    It does not copy the predecessor text, working-set graph, source evidence,
    or filesystem paths.
    """

    path: Path
    revision_format: str
    revision_record_sha256: str
    byte_count: int
    revision: ChromiumPageResearchWorkingSetNoteRevisionRecord


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchWorkingSetNoteRevisionVerificationEvidence:
    """Verified file-local facts for one 22B revision sidecar.

    Verification proves canonical structure and self-integrity only. It does not
    open, verify, or relink the referenced predecessor note and therefore cannot
    establish that the predecessor identity is correct or that the revised text
    actually differs from that predecessor's human wording.
    """

    path: Path
    revision_format: str
    revision_record_sha256: str
    byte_count: int
    prior_note_format: str
    prior_note_record_sha256: str
    revision_mode: str
    revised_note_mode: str
    revised_note_text: str
    document_json: str


def persist_chromium_research_working_set_note_revision(
    revision: ChromiumPageResearchWorkingSetNoteRevisionRecord,
    working_set_source: Path,
    prior_note_source: Path,
    destination: Path,
) -> ChromiumPageResearchWorkingSetNoteRevisionPersistenceEvidence:
    """Persist one 22A revision through the frozen revision-v1/note-v1 contract."""

    return _persist_chromium_research_working_set_note_revision(
        revision,
        working_set_source,
        prior_note_source,
        destination,
        revision_format=document["format"],
        expected_note_format=_NOTE_FORMAT,
    )


def persist_chromium_research_working_set_note_revision_v2(
    revision: ChromiumPageResearchWorkingSetNoteRevisionRecord,
    working_set_source: Path,
    prior_note_source: Path,
    destination: Path,
) -> ChromiumPageResearchWorkingSetNoteRevisionPersistenceEvidence:
    """Persist one 22A revision through the explicit revision-v2/note-v2 contract."""

    return _persist_chromium_research_working_set_note_revision(
        revision,
        working_set_source,
        prior_note_source,
        destination,
        revision_format=_REVISION_FORMAT_V2,
        expected_note_format=_NOTE_FORMAT_V2,
    )


def _persist_chromium_research_working_set_note_revision(
    revision: ChromiumPageResearchWorkingSetNoteRevisionRecord,
    working_set_source: Path,
    prior_note_source: Path,
    destination: Path,
    *,
    revision_format: str,
    expected_note_format: str,
) -> ChromiumPageResearchWorkingSetNoteRevisionPersistenceEvidence:
    if not isinstance(revision, ChromiumPageResearchWorkingSetNoteRevisionRecord):
        raise TypeError(
            "revision must be ChromiumPageResearchWorkingSetNoteRevisionRecord."
        )

    rebuilt_revision = create_chromium_research_working_set_note_revision(
        revision.prior_note,
        revised_note_text=revision.revised_note.note_text,
    )
    if rebuilt_revision.revision_mode != revision.revision_mode:
        raise ValueError("working-set note revision mode is unsupported for persistence.")
    if revision.revision_mode != _REVISION_MODE:
        raise ValueError("working-set note revision mode is unsupported for persistence.")
    if rebuilt_revision.revised_note.note_mode != revision.revised_note.note_mode:
        raise ValueError("revised working-set note mode is unsupported for persistence.")
    if revision.revised_note.note_mode != _NOTE_MODE:
        raise ValueError("revised working-set note mode is unsupported for persistence.")
    if revision.revised_note.working_set is not revision.prior_note.working_set:
        raise ValueError("revised note must retain the exact prior working-set object.")

    loaded_prior = load_chromium_research_working_set_note(
        revision.prior_note.working_set.items,
        working_set_source,
        prior_note_source,
    )
    if loaded_prior.verification.note_format != expected_note_format:
        raise ValueError("durable predecessor note format is unsupported.")
    if loaded_prior.note.note_mode != revision.prior_note.note_mode:
        raise ValueError("durable predecessor note mode does not match revision.prior_note.")
    if loaded_prior.note.note_text != revision.prior_note.note_text:
        raise ValueError("durable predecessor note text does not match revision.prior_note.")

    loaded_items = loaded_prior.note.working_set.items
    supplied_items = revision.prior_note.working_set.items
    if len(loaded_items) != len(supplied_items):
        raise ValueError("durable predecessor working-set member count is incoherent.")
    for index, (observed, supplied) in enumerate(zip(loaded_items, supplied_items)):
        if observed is not supplied:
            raise ValueError(
                f"durable predecessor item {index} does not retain the supplied member object."
            )

    path = Path(destination).expanduser().resolve()
    if not path.parent.is_dir():
        raise FileNotFoundError(
            f"Research working-set-note-revision parent directory does not exist: {path.parent}"
        )

    revision_record = {
        "prior_note_reference": {
            "format": loaded_prior.verification.note_format,
            "note_record_sha256": loaded_prior.verification.note_record_sha256,
        },
        "revision": {
            "mode": revision.revision_mode,
            "revised_note": {
                "mode": revision.revised_note.note_mode,
                "text": revision.revised_note.note_text,
            },
        },
    }
    revision_record_bytes = _canonical_json_bytes(revision_record)
    revision_record_sha256 = hashlib.sha256(revision_record_bytes).hexdigest()
    document = {
        "format": revision_format,
        "revision_record": revision_record,
        "revision_record_sha256": revision_record_sha256,
    }
    document_bytes = _canonical_document_bytes(document)

    with path.open("xb") as handle:
        handle.write(document_bytes)

    return ChromiumPageResearchWorkingSetNoteRevisionPersistenceEvidence(
        path=path,
        revision_format=revision_format,
        revision_record_sha256=revision_record_sha256,
        byte_count=len(document_bytes),
        revision=revision,
    )

def verify_chromium_research_working_set_note_revision(
    source: Path,
) -> ChromiumPageResearchWorkingSetNoteRevisionVerificationEvidence:
    """Verify one 22B sidecar without opening its referenced predecessor note.

    A self-consistent file may therefore contain a structurally valid but wrong
    predecessor digest and still pass verification. It may also contain revised
    text that happens to equal the real predecessor's text, because predecessor
    content is not opened by file-only verification. Those relationships require
    a later explicit relinking boundary.
    """

    path = Path(source).expanduser().resolve()
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ChromiumResearchWorkingSetNoteRevisionIntegrityError(
            "Research working-set-note revision is not valid UTF-8."
        ) from exc

    try:
        document = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ChromiumResearchWorkingSetNoteRevisionIntegrityError(
            "Research working-set-note revision is not valid JSON."
        ) from exc

    revision_record, recorded_sha256 = _validate_persisted_document(document)
    observed_sha256 = hashlib.sha256(_canonical_json_bytes(revision_record)).hexdigest()
    if not hmac.compare_digest(recorded_sha256, observed_sha256):
        raise ChromiumResearchWorkingSetNoteRevisionIntegrityError(
            "Research working-set-note-revision SHA-256 does not match the persisted record."
        )

    canonical_document_bytes = _canonical_document_bytes(document)
    if raw != canonical_document_bytes:
        raise ChromiumResearchWorkingSetNoteRevisionIntegrityError(
            "Research working-set-note-revision bytes are not canonical Pyxis JSON."
        )

    prior_reference = revision_record["prior_note_reference"]
    revision_payload = revision_record["revision"]
    revised_note = revision_payload["revised_note"]
    return ChromiumPageResearchWorkingSetNoteRevisionVerificationEvidence(
        path=path,
        revision_format=_REVISION_FORMAT,
        revision_record_sha256=recorded_sha256,
        byte_count=len(raw),
        prior_note_format=prior_reference["format"],
        prior_note_record_sha256=prior_reference["note_record_sha256"],
        revision_mode=revision_payload["mode"],
        revised_note_mode=revised_note["mode"],
        revised_note_text=revised_note["text"],
        document_json=text,
    )


def _validate_persisted_document(document: Any) -> tuple[dict[str, Any], str]:
    if type(document) is not dict or set(document) != {
        "format",
        "revision_record",
        "revision_record_sha256",
    }:
        raise ChromiumResearchWorkingSetNoteRevisionIntegrityError(
            "Research working-set-note-revision document has an invalid top-level shape."
        )
    revision_format = document["format"]
    if revision_format not in {_REVISION_FORMAT, _REVISION_FORMAT_V2}:
        raise ChromiumResearchWorkingSetNoteRevisionIntegrityError(
            "Research working-set-note-revision format is unsupported."
        )

    recorded_sha256 = document["revision_record_sha256"]
    if not _is_sha256(recorded_sha256):
        raise ChromiumResearchWorkingSetNoteRevisionIntegrityError(
            "Research working-set-note-revision SHA-256 has an invalid shape."
        )

    revision_record = document["revision_record"]
    if type(revision_record) is not dict or set(revision_record) != {
        "prior_note_reference",
        "revision",
    }:
        raise ChromiumResearchWorkingSetNoteRevisionIntegrityError(
            "Research working-set-note-revision record has an invalid shape."
        )

    prior_reference = revision_record["prior_note_reference"]
    if type(prior_reference) is not dict or set(prior_reference) != {
        "format",
        "note_record_sha256",
    }:
        raise ChromiumResearchWorkingSetNoteRevisionIntegrityError(
            "Research working-set-note-revision predecessor reference has an invalid shape."
        )
    expected_note_format = (
        _NOTE_FORMAT
        if revision_format == _REVISION_FORMAT
        else _NOTE_FORMAT_V2
    )
    if prior_reference["format"] != expected_note_format:
        raise ChromiumResearchWorkingSetNoteRevisionIntegrityError(
            "Research working-set-note-revision predecessor format is unsupported."
        )
    if not _is_sha256(prior_reference["note_record_sha256"]):
        raise ChromiumResearchWorkingSetNoteRevisionIntegrityError(
            "Research working-set-note-revision predecessor SHA-256 has an invalid shape."
        )

    revision_payload = revision_record["revision"]
    if type(revision_payload) is not dict or set(revision_payload) != {
        "mode",
        "revised_note",
    }:
        raise ChromiumResearchWorkingSetNoteRevisionIntegrityError(
            "Research working-set-note-revision payload has an invalid shape."
        )
    if revision_payload["mode"] != _REVISION_MODE:
        raise ChromiumResearchWorkingSetNoteRevisionIntegrityError(
            "Research working-set-note-revision mode is unsupported."
        )

    revised_note = revision_payload["revised_note"]
    if type(revised_note) is not dict or set(revised_note) != {"mode", "text"}:
        raise ChromiumResearchWorkingSetNoteRevisionIntegrityError(
            "Research working-set-note-revision revised note has an invalid shape."
        )
    if revised_note["mode"] != _NOTE_MODE:
        raise ChromiumResearchWorkingSetNoteRevisionIntegrityError(
            "Research working-set-note-revision revised note mode is unsupported."
        )
    revised_text = revised_note["text"]
    if type(revised_text) is not str or not revised_text.strip():
        raise ChromiumResearchWorkingSetNoteRevisionIntegrityError(
            "Research working-set-note-revision revised text must contain human text."
        )

    return revision_record, recorded_sha256


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
            "Research working-set-note-revision record is not canonical-JSON serializable."
        ) from exc
    return encoded.encode("utf-8")


def _canonical_document_bytes(document: Any) -> bytes:
    return _canonical_json_bytes(document) + b"\n"
