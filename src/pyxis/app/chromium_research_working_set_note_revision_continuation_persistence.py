from __future__ import annotations

from dataclasses import dataclass
import hashlib
import hmac
import json
from pathlib import Path
from typing import Any

from .chromium_research_working_set_note_revision_continuation import (
    ChromiumPageResearchWorkingSetNoteRevisionContinuationRecord,
    create_chromium_research_working_set_note_revision_continuation,
)
from .chromium_research_working_set_note_revision_load import (
    load_chromium_research_working_set_note_revision,
)


_CONTINUATION_FORMAT = (
    "pyxis.chromium.research_working_set_note_revision_continuation.v1"
)
_REVISION_FORMAT = "pyxis.chromium.research_working_set_note_revision.v1"
_NOTE_MODE = "caller_authored_note_on_research_working_set"
_REVISION_MODE = "caller_authored_revision_of_research_working_set_note"
_CONTINUATION_MODE = (
    "caller_authored_continuation_of_verified_research_working_set_note_revision"
)


class ChromiumResearchWorkingSetNoteRevisionContinuationIntegrityError(ValueError):
    """Raised when persisted 23B revision-continuation bytes fail integrity."""


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchWorkingSetNoteRevisionContinuationPersistenceEvidence:
    """Durable-file evidence for one already-created 23A continuation.

    `continuation` retains the exact caller-supplied 23A object. The durable file
    stores only the freshly re-established durable identity of the predecessor
    22B revision plus the continuation mode and new human revision wording.
    Earlier note text, working-set membership, source evidence, and filesystem
    paths are not copied into this file.
    """

    path: Path
    continuation_format: str
    continuation_record_sha256: str
    byte_count: int
    continuation: ChromiumPageResearchWorkingSetNoteRevisionContinuationRecord


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchWorkingSetNoteRevisionContinuationVerificationEvidence:
    """Verified file-local facts for one 23B continuation sidecar.

    Verification proves canonical structure and self-integrity only. It does not
    open, verify, or relink the referenced predecessor revision. It therefore
    cannot establish that the predecessor identity is correct or that the new
    wording is actually different from the real predecessor's v2 wording.
    """

    path: Path
    continuation_format: str
    continuation_record_sha256: str
    byte_count: int
    prior_revision_format: str
    prior_revision_record_sha256: str
    continuation_mode: str
    revision_mode: str
    revised_note_mode: str
    revised_note_text: str
    document_json: str


def persist_chromium_research_working_set_note_revision_continuation(
    continuation: ChromiumPageResearchWorkingSetNoteRevisionContinuationRecord,
    working_set_source: Path,
    prior_note_source: Path,
    prior_revision_source: Path,
    destination: Path,
) -> ChromiumPageResearchWorkingSetNoteRevisionContinuationPersistenceEvidence:
    """Persist one 23A continuation against one explicit durable 22B predecessor.

    The caller supplies the live 23A continuation plus the current locations of
    its durable 20B working set, 21B predecessor note, and 22B predecessor
    revision. Pyxis first re-establishes the 23A in-memory contract through the
    public 23A constructor. It then freshly loads the supplied durable predecessor
    through public 22C using the exact already-loaded member sequence retained by
    the continuation's predecessor.

    The freshly loaded 22B predecessor content identity must match the durable
    identity already retained by the caller-supplied 22C predecessor object before
    any destination file is created. The new sidecar then records only that
    predecessor revision identity plus the continuation mode and v3 human text.
    """

    if not isinstance(
        continuation,
        ChromiumPageResearchWorkingSetNoteRevisionContinuationRecord,
    ):
        raise TypeError(
            "continuation must be "
            "ChromiumPageResearchWorkingSetNoteRevisionContinuationRecord."
        )

    rebuilt = create_chromium_research_working_set_note_revision_continuation(
        continuation.prior_revision,
        revised_note_text=continuation.revision.revised_note.note_text,
    )
    if rebuilt.continuation_mode != continuation.continuation_mode:
        raise ValueError("revision-continuation mode is unsupported for persistence.")
    if continuation.continuation_mode != _CONTINUATION_MODE:
        raise ValueError("revision-continuation mode is unsupported for persistence.")
    if rebuilt.revision.revision_mode != continuation.revision.revision_mode:
        raise ValueError("continued revision mode is unsupported for persistence.")
    if continuation.revision.revision_mode != _REVISION_MODE:
        raise ValueError("continued revision mode is unsupported for persistence.")
    if rebuilt.revision.revised_note.note_mode != continuation.revision.revised_note.note_mode:
        raise ValueError("continued revised-note mode is unsupported for persistence.")
    if continuation.revision.revised_note.note_mode != _NOTE_MODE:
        raise ValueError("continued revised-note mode is unsupported for persistence.")
    if continuation.revision.prior_note is not continuation.prior_revision.revision.revised_note:
        raise ValueError(
            "continued revision must retain the exact predecessor revised-note object."
        )
    if (
        continuation.revision.revised_note.working_set
        is not continuation.prior_revision.revision.revised_note.working_set
    ):
        raise ValueError(
            "continued revised note must retain the exact predecessor working set."
        )

    supplied_items = continuation.prior_revision.revision.revised_note.working_set.items
    loaded_prior = load_chromium_research_working_set_note_revision(
        supplied_items,
        working_set_source,
        prior_note_source,
        prior_revision_source,
    )
    if loaded_prior.verification.revision_format != _REVISION_FORMAT:
        raise ValueError("durable predecessor revision format is unsupported.")
    if continuation.prior_revision.verification.revision_format != _REVISION_FORMAT:
        raise ValueError("retained predecessor revision format is unsupported.")
    if loaded_prior.verification.revision_format != (
        continuation.prior_revision.verification.revision_format
    ):
        raise ValueError("durable predecessor revision format does not match continuation.")
    if not hmac.compare_digest(
        loaded_prior.verification.revision_record_sha256,
        continuation.prior_revision.verification.revision_record_sha256,
    ):
        raise ValueError("durable predecessor revision does not match continuation.")

    loaded_items = loaded_prior.revision.revised_note.working_set.items
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
            "Research working-set-note-revision-continuation parent directory "
            f"does not exist: {path.parent}"
        )

    continuation_record = {
        "prior_revision_reference": {
            "format": loaded_prior.verification.revision_format,
            "revision_record_sha256": (
                loaded_prior.verification.revision_record_sha256
            ),
        },
        "continuation": {
            "mode": continuation.continuation_mode,
            "revision": {
                "mode": continuation.revision.revision_mode,
                "revised_note": {
                    "mode": continuation.revision.revised_note.note_mode,
                    "text": continuation.revision.revised_note.note_text,
                },
            },
        },
    }
    continuation_record_bytes = _canonical_json_bytes(continuation_record)
    continuation_record_sha256 = hashlib.sha256(continuation_record_bytes).hexdigest()
    document = {
        "format": _CONTINUATION_FORMAT,
        "continuation_record": continuation_record,
        "continuation_record_sha256": continuation_record_sha256,
    }
    document_bytes = _canonical_document_bytes(document)

    with path.open("xb") as handle:
        handle.write(document_bytes)

    return ChromiumPageResearchWorkingSetNoteRevisionContinuationPersistenceEvidence(
        path=path,
        continuation_format=_CONTINUATION_FORMAT,
        continuation_record_sha256=continuation_record_sha256,
        byte_count=len(document_bytes),
        continuation=continuation,
    )


def verify_chromium_research_working_set_note_revision_continuation(
    source: Path,
) -> ChromiumPageResearchWorkingSetNoteRevisionContinuationVerificationEvidence:
    """Verify one 23B sidecar without opening its predecessor revision.

    A self-consistent file may therefore contain a structurally valid but wrong
    predecessor revision digest and still pass verification. It may likewise
    contain v3 wording equal to the real predecessor's v2 wording, because the
    predecessor is not opened by file-only verification. Those relationships are
    intentionally left for a later explicit relinking boundary.
    """

    path = Path(source).expanduser().resolve()
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ChromiumResearchWorkingSetNoteRevisionContinuationIntegrityError(
            "Research revision continuation is not valid UTF-8."
        ) from exc

    try:
        document = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ChromiumResearchWorkingSetNoteRevisionContinuationIntegrityError(
            "Research revision continuation is not valid JSON."
        ) from exc

    continuation_record, recorded_sha256 = _validate_persisted_document(document)
    observed_sha256 = hashlib.sha256(
        _canonical_json_bytes(continuation_record)
    ).hexdigest()
    if not hmac.compare_digest(recorded_sha256, observed_sha256):
        raise ChromiumResearchWorkingSetNoteRevisionContinuationIntegrityError(
            "Research revision-continuation SHA-256 does not match the persisted record."
        )

    canonical_document_bytes = _canonical_document_bytes(document)
    if raw != canonical_document_bytes:
        raise ChromiumResearchWorkingSetNoteRevisionContinuationIntegrityError(
            "Research revision-continuation bytes are not canonical Pyxis JSON."
        )

    prior_reference = continuation_record["prior_revision_reference"]
    continuation_payload = continuation_record["continuation"]
    revision_payload = continuation_payload["revision"]
    revised_note = revision_payload["revised_note"]
    return ChromiumPageResearchWorkingSetNoteRevisionContinuationVerificationEvidence(
        path=path,
        continuation_format=_CONTINUATION_FORMAT,
        continuation_record_sha256=recorded_sha256,
        byte_count=len(raw),
        prior_revision_format=prior_reference["format"],
        prior_revision_record_sha256=prior_reference["revision_record_sha256"],
        continuation_mode=continuation_payload["mode"],
        revision_mode=revision_payload["mode"],
        revised_note_mode=revised_note["mode"],
        revised_note_text=revised_note["text"],
        document_json=text,
    )


def _validate_persisted_document(document: Any) -> tuple[dict[str, Any], str]:
    if type(document) is not dict or set(document) != {
        "format",
        "continuation_record",
        "continuation_record_sha256",
    }:
        raise ChromiumResearchWorkingSetNoteRevisionContinuationIntegrityError(
            "Research revision-continuation document has an invalid top-level shape."
        )
    if document["format"] != _CONTINUATION_FORMAT:
        raise ChromiumResearchWorkingSetNoteRevisionContinuationIntegrityError(
            "Research revision-continuation format is unsupported."
        )

    recorded_sha256 = document["continuation_record_sha256"]
    if not _is_sha256(recorded_sha256):
        raise ChromiumResearchWorkingSetNoteRevisionContinuationIntegrityError(
            "Research revision-continuation SHA-256 has an invalid shape."
        )

    continuation_record = document["continuation_record"]
    if type(continuation_record) is not dict or set(continuation_record) != {
        "prior_revision_reference",
        "continuation",
    }:
        raise ChromiumResearchWorkingSetNoteRevisionContinuationIntegrityError(
            "Research revision-continuation record has an invalid shape."
        )

    prior_reference = continuation_record["prior_revision_reference"]
    if type(prior_reference) is not dict or set(prior_reference) != {
        "format",
        "revision_record_sha256",
    }:
        raise ChromiumResearchWorkingSetNoteRevisionContinuationIntegrityError(
            "Research revision-continuation predecessor reference has an invalid shape."
        )
    if prior_reference["format"] != _REVISION_FORMAT:
        raise ChromiumResearchWorkingSetNoteRevisionContinuationIntegrityError(
            "Research revision-continuation predecessor format is unsupported."
        )
    if not _is_sha256(prior_reference["revision_record_sha256"]):
        raise ChromiumResearchWorkingSetNoteRevisionContinuationIntegrityError(
            "Research revision-continuation predecessor SHA-256 has an invalid shape."
        )

    continuation_payload = continuation_record["continuation"]
    if type(continuation_payload) is not dict or set(continuation_payload) != {
        "mode",
        "revision",
    }:
        raise ChromiumResearchWorkingSetNoteRevisionContinuationIntegrityError(
            "Research revision-continuation payload has an invalid shape."
        )
    if continuation_payload["mode"] != _CONTINUATION_MODE:
        raise ChromiumResearchWorkingSetNoteRevisionContinuationIntegrityError(
            "Research revision-continuation mode is unsupported."
        )

    revision_payload = continuation_payload["revision"]
    if type(revision_payload) is not dict or set(revision_payload) != {
        "mode",
        "revised_note",
    }:
        raise ChromiumResearchWorkingSetNoteRevisionContinuationIntegrityError(
            "Research continued revision has an invalid shape."
        )
    if revision_payload["mode"] != _REVISION_MODE:
        raise ChromiumResearchWorkingSetNoteRevisionContinuationIntegrityError(
            "Research continued revision mode is unsupported."
        )

    revised_note = revision_payload["revised_note"]
    if type(revised_note) is not dict or set(revised_note) != {"mode", "text"}:
        raise ChromiumResearchWorkingSetNoteRevisionContinuationIntegrityError(
            "Research continued revised note has an invalid shape."
        )
    if revised_note["mode"] != _NOTE_MODE:
        raise ChromiumResearchWorkingSetNoteRevisionContinuationIntegrityError(
            "Research continued revised-note mode is unsupported."
        )
    revised_text = revised_note["text"]
    if type(revised_text) is not str or not revised_text.strip():
        raise ChromiumResearchWorkingSetNoteRevisionContinuationIntegrityError(
            "Research continued revised text must contain human text."
        )

    return continuation_record, recorded_sha256


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
            "Research revision-continuation record is not canonical-JSON serializable."
        ) from exc
    return encoded.encode("utf-8")


def _canonical_document_bytes(document: Any) -> bytes:
    return _canonical_json_bytes(document) + b"\n"
