from __future__ import annotations

from dataclasses import dataclass
import hashlib
import hmac
import json
from pathlib import Path
from typing import Any

from .chromium_research_working_set_note_revision_continuation_extension import (
    ChromiumPageResearchWorkingSetNoteRevisionContinuationExtensionRecord,
    create_chromium_research_working_set_note_revision_continuation_extension,
)
from .chromium_research_working_set_note_revision_continuation_load import (
    load_chromium_research_working_set_note_revision_continuation,
)


_EDGE_FORMAT = "pyxis.chromium.research_working_set_note_revision_edge.v1"
_CONTINUATION_FORMAT = (
    "pyxis.chromium.research_working_set_note_revision_continuation.v1"
)
_SUPPORTED_PREDECESSOR_FORMATS = frozenset({_CONTINUATION_FORMAT, _EDGE_FORMAT})
_NOTE_MODE = "caller_authored_note_on_research_working_set"
_REVISION_MODE = "caller_authored_revision_of_research_working_set_note"
_EXTENSION_MODE = (
    "caller_authored_extension_of_verified_research_working_set_note_revision_continuation"
)
_EDGE_MODE = "caller_authored_research_working_set_note_revision_edge"


class ChromiumResearchWorkingSetNoteRevisionEdgeIntegrityError(ValueError):
    """Raised when persisted 24B revision-edge bytes fail file integrity."""


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchWorkingSetNoteRevisionEdgePersistenceEvidence:
    """Durable evidence for one 24A extension written as a general revision edge.

    `extension` retains the exact caller-supplied 24A object. The file stores only
    the freshly re-established durable identity of its predecessor continuation,
    one generic edge mode, and the new verbatim human wording. Earlier note text,
    working-set membership, source evidence, and filesystem paths are not copied.
    """

    path: Path
    edge_format: str
    edge_record_sha256: str
    byte_count: int
    extension: ChromiumPageResearchWorkingSetNoteRevisionContinuationExtensionRecord


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchWorkingSetNoteRevisionEdgeVerificationEvidence:
    """Verified file-local facts for one 24B general revision-edge sidecar.

    Verification proves canonical structure and self-integrity only. It does not
    open or relink the referenced predecessor. The predecessor may be either one
    23B continuation record or another 24B edge record. Accepting the latter shape
    makes repeated revision edges representable without granting traversal,
    existence, ancestry, chronology, or semantic authority.
    """

    path: Path
    edge_format: str
    edge_record_sha256: str
    byte_count: int
    predecessor_format: str
    predecessor_record_sha256: str
    edge_mode: str
    revision_mode: str
    revised_note_mode: str
    revised_note_text: str
    document_json: str


def persist_chromium_research_working_set_note_revision_edge(
    extension: ChromiumPageResearchWorkingSetNoteRevisionContinuationExtensionRecord,
    working_set_source: Path,
    prior_note_source: Path,
    prior_revision_source: Path,
    prior_continuation_source: Path,
    destination: Path,
) -> ChromiumPageResearchWorkingSetNoteRevisionEdgePersistenceEvidence:
    """Persist one 24A extension as the first general durable revision edge.

    The public creator currently anchors one edge to one explicit durable 23B
    continuation. Before writing, Pyxis re-establishes the live 24A contract and
    freshly relinks the predecessor through public 23C using the exact already-
    loaded member sequence retained by the extension.

    The persisted schema is deliberately more general than this creator: a
    predecessor reference may name either the 23B continuation format or another
    24B edge format. This reserves repeated edge representation without adding
    predecessor discovery, recursive loading, chain traversal, a current head,
    revision numbers, timestamps, or global ordering.
    """

    if not isinstance(
        extension,
        ChromiumPageResearchWorkingSetNoteRevisionContinuationExtensionRecord,
    ):
        raise TypeError(
            "extension must be "
            "ChromiumPageResearchWorkingSetNoteRevisionContinuationExtensionRecord."
        )

    rebuilt = create_chromium_research_working_set_note_revision_continuation_extension(
        extension.prior_continuation,
        revised_note_text=extension.revision.revised_note.note_text,
    )
    if rebuilt.extension_mode != extension.extension_mode:
        raise ValueError("revision-edge extension mode is unsupported for persistence.")
    if extension.extension_mode != _EXTENSION_MODE:
        raise ValueError("revision-edge extension mode is unsupported for persistence.")
    if rebuilt.revision.revision_mode != extension.revision.revision_mode:
        raise ValueError("revision-edge revision mode is unsupported for persistence.")
    if extension.revision.revision_mode != _REVISION_MODE:
        raise ValueError("revision-edge revision mode is unsupported for persistence.")
    if rebuilt.revision.revised_note.note_mode != extension.revision.revised_note.note_mode:
        raise ValueError("revision-edge revised-note mode is unsupported for persistence.")
    if extension.revision.revised_note.note_mode != _NOTE_MODE:
        raise ValueError("revision-edge revised-note mode is unsupported for persistence.")
    if (
        extension.revision.prior_note
        is not extension.prior_continuation.continuation.revision.revised_note
    ):
        raise ValueError(
            "revision edge must retain the exact predecessor continuation note object."
        )
    if (
        extension.revision.revised_note.working_set
        is not extension.prior_continuation.continuation.revision.revised_note.working_set
    ):
        raise ValueError(
            "revision-edge revised note must retain the exact predecessor working set."
        )

    supplied_items = (
        extension.prior_continuation.continuation.revision.revised_note.working_set.items
    )
    loaded_prior = load_chromium_research_working_set_note_revision_continuation(
        supplied_items,
        working_set_source,
        prior_note_source,
        prior_revision_source,
        prior_continuation_source,
    )
    if loaded_prior.verification.continuation_format != _CONTINUATION_FORMAT:
        raise ValueError("durable revision-edge predecessor format is unsupported.")
    if extension.prior_continuation.verification.continuation_format != (
        _CONTINUATION_FORMAT
    ):
        raise ValueError("retained revision-edge predecessor format is unsupported.")
    if loaded_prior.verification.continuation_format != (
        extension.prior_continuation.verification.continuation_format
    ):
        raise ValueError("durable revision-edge predecessor format does not match extension.")
    if not hmac.compare_digest(
        loaded_prior.verification.continuation_record_sha256,
        extension.prior_continuation.verification.continuation_record_sha256,
    ):
        raise ValueError("durable revision-edge predecessor does not match extension.")

    loaded_items = loaded_prior.continuation.revision.revised_note.working_set.items
    if len(loaded_items) != len(supplied_items):
        raise ValueError("durable revision-edge predecessor member count is incoherent.")
    for index, (observed, supplied) in enumerate(zip(loaded_items, supplied_items)):
        if observed is not supplied:
            raise ValueError(
                f"durable revision-edge predecessor item {index} does not retain "
                "the supplied member object."
            )

    path = Path(destination).expanduser().resolve()
    if not path.parent.is_dir():
        raise FileNotFoundError(
            "Research working-set-note revision-edge parent directory does not exist: "
            f"{path.parent}"
        )

    edge_record = {
        "predecessor_reference": {
            "format": loaded_prior.verification.continuation_format,
            "record_sha256": loaded_prior.verification.continuation_record_sha256,
        },
        "edge": {
            "mode": _EDGE_MODE,
            "revision": {
                "mode": extension.revision.revision_mode,
                "revised_note": {
                    "mode": extension.revision.revised_note.note_mode,
                    "text": extension.revision.revised_note.note_text,
                },
            },
        },
    }
    edge_record_bytes = _canonical_json_bytes(edge_record)
    edge_record_sha256 = hashlib.sha256(edge_record_bytes).hexdigest()
    document = {
        "format": _EDGE_FORMAT,
        "edge_record": edge_record,
        "edge_record_sha256": edge_record_sha256,
    }
    document_bytes = _canonical_document_bytes(document)

    with path.open("xb") as handle:
        handle.write(document_bytes)

    return ChromiumPageResearchWorkingSetNoteRevisionEdgePersistenceEvidence(
        path=path,
        edge_format=_EDGE_FORMAT,
        edge_record_sha256=edge_record_sha256,
        byte_count=len(document_bytes),
        extension=extension,
    )


def verify_chromium_research_working_set_note_revision_edge(
    source: Path,
) -> ChromiumPageResearchWorkingSetNoteRevisionEdgeVerificationEvidence:
    """Verify one 24B edge sidecar without opening its predecessor.

    A self-consistent file may therefore contain a structurally valid but wrong
    predecessor digest and still pass verification. It may also contain new wording
    equal to the real predecessor wording. A same-format predecessor reference is
    accepted structurally without proving that such an edge exists or can be
    relinked. Those relationships belong to later explicit boundaries.
    """

    path = Path(source).expanduser().resolve()
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeIntegrityError(
            "Research revision edge is not valid UTF-8."
        ) from exc

    try:
        document = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeIntegrityError(
            "Research revision edge is not valid JSON."
        ) from exc

    edge_record, recorded_sha256 = _validate_persisted_document(document)
    observed_sha256 = hashlib.sha256(_canonical_json_bytes(edge_record)).hexdigest()
    if not hmac.compare_digest(recorded_sha256, observed_sha256):
        raise ChromiumResearchWorkingSetNoteRevisionEdgeIntegrityError(
            "Research revision-edge SHA-256 does not match the persisted record."
        )

    canonical_document_bytes = _canonical_document_bytes(document)
    if raw != canonical_document_bytes:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeIntegrityError(
            "Research revision-edge bytes are not canonical Pyxis JSON."
        )

    predecessor = edge_record["predecessor_reference"]
    edge_payload = edge_record["edge"]
    revision_payload = edge_payload["revision"]
    revised_note = revision_payload["revised_note"]
    return ChromiumPageResearchWorkingSetNoteRevisionEdgeVerificationEvidence(
        path=path,
        edge_format=_EDGE_FORMAT,
        edge_record_sha256=recorded_sha256,
        byte_count=len(raw),
        predecessor_format=predecessor["format"],
        predecessor_record_sha256=predecessor["record_sha256"],
        edge_mode=edge_payload["mode"],
        revision_mode=revision_payload["mode"],
        revised_note_mode=revised_note["mode"],
        revised_note_text=revised_note["text"],
        document_json=text,
    )


def _validate_persisted_document(document: Any) -> tuple[dict[str, Any], str]:
    if type(document) is not dict or set(document) != {
        "format",
        "edge_record",
        "edge_record_sha256",
    }:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeIntegrityError(
            "Research revision-edge document has an invalid top-level shape."
        )
    if document["format"] != _EDGE_FORMAT:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeIntegrityError(
            "Research revision-edge format is unsupported."
        )

    recorded_sha256 = document["edge_record_sha256"]
    if not _is_sha256(recorded_sha256):
        raise ChromiumResearchWorkingSetNoteRevisionEdgeIntegrityError(
            "Research revision-edge SHA-256 has an invalid shape."
        )

    edge_record = document["edge_record"]
    if type(edge_record) is not dict or set(edge_record) != {
        "predecessor_reference",
        "edge",
    }:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeIntegrityError(
            "Research revision-edge record has an invalid shape."
        )

    predecessor = edge_record["predecessor_reference"]
    if type(predecessor) is not dict or set(predecessor) != {
        "format",
        "record_sha256",
    }:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeIntegrityError(
            "Research revision-edge predecessor reference has an invalid shape."
        )
    if predecessor["format"] not in _SUPPORTED_PREDECESSOR_FORMATS:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeIntegrityError(
            "Research revision-edge predecessor format is unsupported."
        )
    if not _is_sha256(predecessor["record_sha256"]):
        raise ChromiumResearchWorkingSetNoteRevisionEdgeIntegrityError(
            "Research revision-edge predecessor SHA-256 has an invalid shape."
        )

    edge_payload = edge_record["edge"]
    if type(edge_payload) is not dict or set(edge_payload) != {"mode", "revision"}:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeIntegrityError(
            "Research revision-edge payload has an invalid shape."
        )
    if edge_payload["mode"] != _EDGE_MODE:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeIntegrityError(
            "Research revision-edge mode is unsupported."
        )

    revision_payload = edge_payload["revision"]
    if type(revision_payload) is not dict or set(revision_payload) != {
        "mode",
        "revised_note",
    }:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeIntegrityError(
            "Research revision-edge revision has an invalid shape."
        )
    if revision_payload["mode"] != _REVISION_MODE:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeIntegrityError(
            "Research revision-edge revision mode is unsupported."
        )

    revised_note = revision_payload["revised_note"]
    if type(revised_note) is not dict or set(revised_note) != {"mode", "text"}:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeIntegrityError(
            "Research revision-edge revised note has an invalid shape."
        )
    if revised_note["mode"] != _NOTE_MODE:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeIntegrityError(
            "Research revision-edge revised-note mode is unsupported."
        )
    revised_text = revised_note["text"]
    if type(revised_text) is not str or not revised_text.strip():
        raise ChromiumResearchWorkingSetNoteRevisionEdgeIntegrityError(
            "Research revision-edge revised text must contain human text."
        )

    return edge_record, recorded_sha256


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
            "Research revision-edge record is not canonical-JSON serializable."
        ) from exc
    return encoded.encode("utf-8")


def _canonical_document_bytes(document: Any) -> bytes:
    return _canonical_json_bytes(document) + b"\n"
