from __future__ import annotations

from dataclasses import dataclass
import hashlib
import hmac
import json
from pathlib import Path
from typing import TYPE_CHECKING, Any

from .chromium_research_working_set_note_revision_continuation_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord,
)
from .chromium_research_working_set_note_revision_continuation_persistence import (
    _validate_persisted_document as _validate_continuation_persisted_document,
)
from .chromium_research_working_set_note_revision_edge_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord,
    _validate_loaded_edge_predecessor,
    _validate_loaded_predecessor,
    _validate_loaded_root_predecessor,
)
from .chromium_research_working_set_note_revision_edge_persistence import (
    _validate_persisted_document as _validate_edge_persisted_document,
)
from .chromium_research_working_set_note_revision_edge_sequence_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceRecord,
)

if TYPE_CHECKING:
    from .chromium_research_session_working_set_transition_revision_root_load import (
        ChromiumPageResearchLoadedWorkingSetTransitionRevisionRootRecord,
    )


_SEQUENCE_FORMAT = (
    "pyxis.chromium.research_working_set_note_revision_edge_sequence.v1"
)
_SEQUENCE_MODE = (
    "caller_explicit_ordered_relinked_research_working_set_note_revision_edge_sequence"
)
_CONTINUATION_FORMAT = (
    "pyxis.chromium.research_working_set_note_revision_continuation.v1"
)
_EDGE_FORMAT = "pyxis.chromium.research_working_set_note_revision_edge.v1"
_ROOT_FORMAT = (
    "pyxis.chromium.research_session_working_set_transition_revision_root.v1"
)
_SUPPORTED_STARTING_FORMATS = frozenset(
    {_CONTINUATION_FORMAT, _EDGE_FORMAT, _ROOT_FORMAT}
)


class ChromiumResearchWorkingSetNoteRevisionEdgeSequenceIntegrityError(ValueError):
    """Raised when persisted 26B sequence-declaration bytes fail self-integrity."""


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchWorkingSetNoteRevisionEdgeSequenceReference:
    """One content-addressed record identity retained by a sequence declaration.

    A reference contains only a durable record format and its record SHA-256. It
    does not contain a filesystem path and does not prove that the referenced file
    currently exists, remains available, or can be relinked.
    """

    record_format: str
    record_sha256: str


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchWorkingSetNoteRevisionEdgeSequencePersistenceEvidence:
    """Durable evidence for one already-loaded caller-explicit 26A sequence.

    `sequence` retains the exact caller-supplied 26A application record. The file
    stores only the sequence mode, the starting predecessor content identity, and
    the ordered content identities of the loaded revision edges. It stores no edge
    paths, note text, source evidence, timestamps, revision numbers, or head marker.

    A 35A sequence may name one exact 34A root as its starting predecessor. That
    records only the explicit sequence start already proved in memory; it does not
    turn the root into a generic 24C predecessor or a global session head.
    """

    path: Path
    sequence_format: str
    sequence_record_sha256: str
    byte_count: int
    sequence: ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceRecord


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchWorkingSetNoteRevisionEdgeSequenceVerificationEvidence:
    """Verified file-local facts for one 26B sequence declaration.

    Verification proves canonical structure and self-integrity only. It does not
    open the starting predecessor or any edge file, does not re-establish adjacency,
    and does not prove that the declared order is complete, canonical, latest, or
    historically authoritative.
    """

    path: Path
    sequence_format: str
    sequence_record_sha256: str
    byte_count: int
    sequence_mode: str
    starting_predecessor: ChromiumPageResearchWorkingSetNoteRevisionEdgeSequenceReference
    edges: tuple[ChromiumPageResearchWorkingSetNoteRevisionEdgeSequenceReference, ...]
    document_json: str


def persist_chromium_research_working_set_note_revision_edge_sequence(
    sequence: ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceRecord,
    destination: Path,
) -> ChromiumPageResearchWorkingSetNoteRevisionEdgeSequencePersistenceEvidence:
    """Persist one explicit loaded 26A edge sequence without rereading its files.

    Pyxis first re-establishes the retained in-memory sequence structure. It checks
    the starting predecessor and every loaded edge through the existing bounded
    local coherence boundaries, and it re-checks each retained verification object's
    canonical document JSON and recorded content digest in memory. No referenced
    durable file is reread or required to still exist.

    The resulting file is a durable declaration of one human-supplied ordered
    segment. It is not a discovered history, current head, chronology statement,
    uniqueness claim, or whole-ancestry validation.
    """

    starting_reference, edge_references = _validate_live_sequence(sequence)

    path = Path(destination).expanduser().resolve()
    if not path.parent.is_dir():
        raise FileNotFoundError(
            "Research revision-edge-sequence parent directory does not exist: "
            f"{path.parent}"
        )

    sequence_record = {
        "edge_references": [
            {
                "format": reference.record_format,
                "record_sha256": reference.record_sha256,
            }
            for reference in edge_references
        ],
        "sequence_mode": sequence.sequence_mode,
        "starting_predecessor_reference": {
            "format": starting_reference.record_format,
            "record_sha256": starting_reference.record_sha256,
        },
    }
    sequence_record_sha256 = hashlib.sha256(
        _canonical_json_bytes(sequence_record)
    ).hexdigest()
    document = {
        "format": _SEQUENCE_FORMAT,
        "sequence_record": sequence_record,
        "sequence_record_sha256": sequence_record_sha256,
    }
    document_bytes = _canonical_document_bytes(document)

    with path.open("xb") as handle:
        handle.write(document_bytes)

    return ChromiumPageResearchWorkingSetNoteRevisionEdgeSequencePersistenceEvidence(
        path=path,
        sequence_format=_SEQUENCE_FORMAT,
        sequence_record_sha256=sequence_record_sha256,
        byte_count=len(document_bytes),
        sequence=sequence,
    )


def verify_chromium_research_working_set_note_revision_edge_sequence(
    source: Path,
) -> ChromiumPageResearchWorkingSetNoteRevisionEdgeSequenceVerificationEvidence:
    """Verify one sequence-declaration file without opening any referenced record.

    A self-consistent file may therefore contain a structurally valid but incorrect
    starting-predecessor digest, incorrect edge digest, or ordered list that does not
    describe a relinkable adjacency sequence and still pass this file-only boundary.
    Those relationships require a separate explicit relinking step.
    """

    path = Path(source).expanduser().resolve()
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeSequenceIntegrityError(
            "Research revision-edge sequence is not valid UTF-8."
        ) from exc

    try:
        document = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeSequenceIntegrityError(
            "Research revision-edge sequence is not valid JSON."
        ) from exc

    sequence_record, recorded_sha256 = _validate_persisted_document(document)
    observed_sha256 = hashlib.sha256(
        _canonical_json_bytes(sequence_record)
    ).hexdigest()
    if not hmac.compare_digest(recorded_sha256, observed_sha256):
        raise ChromiumResearchWorkingSetNoteRevisionEdgeSequenceIntegrityError(
            "Research revision-edge-sequence SHA-256 does not match the persisted record."
        )

    canonical_document_bytes = _canonical_document_bytes(document)
    if raw != canonical_document_bytes:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeSequenceIntegrityError(
            "Research revision-edge-sequence bytes are not canonical Pyxis JSON."
        )

    starting_payload = sequence_record["starting_predecessor_reference"]
    edge_payloads = sequence_record["edge_references"]
    return ChromiumPageResearchWorkingSetNoteRevisionEdgeSequenceVerificationEvidence(
        path=path,
        sequence_format=_SEQUENCE_FORMAT,
        sequence_record_sha256=recorded_sha256,
        byte_count=len(raw),
        sequence_mode=sequence_record["sequence_mode"],
        starting_predecessor=ChromiumPageResearchWorkingSetNoteRevisionEdgeSequenceReference(
            record_format=starting_payload["format"],
            record_sha256=starting_payload["record_sha256"],
        ),
        edges=tuple(
            ChromiumPageResearchWorkingSetNoteRevisionEdgeSequenceReference(
                record_format=item["format"],
                record_sha256=item["record_sha256"],
            )
            for item in edge_payloads
        ),
        document_json=text,
    )


def _validate_live_sequence(
    sequence: ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceRecord,
) -> tuple[
    ChromiumPageResearchWorkingSetNoteRevisionEdgeSequenceReference,
    tuple[ChromiumPageResearchWorkingSetNoteRevisionEdgeSequenceReference, ...],
]:
    if not isinstance(
        sequence,
        ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceRecord,
    ):
        raise TypeError(
            "sequence must be "
            "ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceRecord."
        )
    if sequence.sequence_mode != _SEQUENCE_MODE:
        raise ValueError("revision-edge-sequence mode is unsupported for persistence.")
    if not sequence.edges:
        raise ValueError("revision-edge sequence must retain at least one loaded edge.")

    starting_reference = _loaded_record_reference(sequence.starting_predecessor)
    current: (
        ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord
        | ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord
        | ChromiumPageResearchLoadedWorkingSetTransitionRevisionRootRecord
    ) = sequence.starting_predecessor
    current_reference = starting_reference
    edge_references: list[
        ChromiumPageResearchWorkingSetNoteRevisionEdgeSequenceReference
    ] = []

    for index, edge in enumerate(sequence.edges):
        if not isinstance(edge, ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord):
            raise TypeError(
                f"sequence.edges[{index}] must be "
                "ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord."
            )
        if edge.predecessor is not current:
            raise ValueError(
                f"sequence.edges[{index}] does not retain the exact preceding application record."
            )

        # Re-establish the bounded local relationship retained by each loaded edge.
        # A root-backed first edge is valid only because 34B already earned that
        # exact local predecessor relationship; this does not widen generic 24C.
        _validate_loaded_edge_predecessor(edge)
        edge_reference = _retained_edge_reference(edge)

        if edge.verification.predecessor_format != current_reference.record_format:
            raise ValueError(
                f"sequence.edges[{index}] retained predecessor format is incoherent."
            )
        if not hmac.compare_digest(
            edge.verification.predecessor_record_sha256,
            current_reference.record_sha256,
        ):
            raise ValueError(
                f"sequence.edges[{index}] retained predecessor identity is incoherent."
            )

        edge_references.append(edge_reference)
        current = edge
        current_reference = edge_reference

    return starting_reference, tuple(edge_references)


def _loaded_record_reference(
    record: (
        ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord
        | ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord
        | ChromiumPageResearchLoadedWorkingSetTransitionRevisionRootRecord
    ),
) -> ChromiumPageResearchWorkingSetNoteRevisionEdgeSequenceReference:
    from .chromium_research_session_working_set_transition_revision_root_load import (
        ChromiumPageResearchLoadedWorkingSetTransitionRevisionRootRecord,
    )

    if not isinstance(
        record,
        (
            ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord,
            ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord,
            ChromiumPageResearchLoadedWorkingSetTransitionRevisionRootRecord,
        ),
    ):
        raise TypeError(
            "sequence starting predecessor must be an already-loaded 23C continuation, "
            "24C revision edge, or 34A cross-working-set revision root."
        )

    if isinstance(
        record,
        ChromiumPageResearchLoadedWorkingSetTransitionRevisionRootRecord,
    ):
        _validate_loaded_root_predecessor(record)
        return _retained_root_reference(record)

    # Re-establish the existing bounded ordinary application relationship first.
    _validate_loaded_predecessor(record)
    if isinstance(record, ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord):
        return _retained_continuation_reference(record)
    return _retained_edge_reference(record)


def _retained_root_reference(
    record: ChromiumPageResearchLoadedWorkingSetTransitionRevisionRootRecord,
) -> ChromiumPageResearchWorkingSetNoteRevisionEdgeSequenceReference:
    from .chromium_research_session_working_set_transition_revision_root_persistence import (
        _validate_document as _validate_root_persisted_document,
    )

    verification = record.verification
    try:
        document = json.loads(verification.document_json)
        root_record, recorded_sha256 = _validate_root_persisted_document(document)
    except (TypeError, ValueError, json.JSONDecodeError) as exc:
        raise ValueError(
            "loaded sequence starting root retains incoherent verification JSON."
        ) from exc

    _require_retained_document_self_integrity(
        document=document,
        record_payload=root_record,
        recorded_sha256=recorded_sha256,
        verification_sha256=verification.root_record_sha256,
        verification_document_json=verification.document_json,
        verification_byte_count=verification.byte_count,
        label="loaded sequence starting root",
    )

    transition_reference = root_record["transition_reference"]
    root_payload = root_record["root"]
    revision = root_payload["revision"]
    revised_note = revision["revised_note"]
    if verification.root_format != _ROOT_FORMAT:
        raise ValueError("loaded sequence starting root format is unsupported.")
    if verification.transition_format != transition_reference["format"]:
        raise ValueError("loaded sequence starting root transition format is incoherent.")
    if not hmac.compare_digest(
        verification.transition_record_sha256,
        transition_reference["record_sha256"],
    ):
        raise ValueError("loaded sequence starting root transition identity is incoherent.")
    if verification.root_mode != root_payload["mode"]:
        raise ValueError("loaded sequence starting root mode is incoherent.")
    if verification.revision_mode != revision["mode"]:
        raise ValueError("loaded sequence starting root revision mode is incoherent.")
    if verification.revised_note_mode != revised_note["mode"]:
        raise ValueError("loaded sequence starting root note mode is incoherent.")
    if verification.revised_note_text != revised_note["text"]:
        raise ValueError("loaded sequence starting root text is incoherent.")

    return ChromiumPageResearchWorkingSetNoteRevisionEdgeSequenceReference(
        record_format=_ROOT_FORMAT,
        record_sha256=recorded_sha256,
    )


def _retained_continuation_reference(
    record: ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord,
) -> ChromiumPageResearchWorkingSetNoteRevisionEdgeSequenceReference:
    verification = record.verification
    try:
        document = json.loads(verification.document_json)
        continuation_record, recorded_sha256 = _validate_continuation_persisted_document(
            document
        )
    except (TypeError, ValueError, json.JSONDecodeError) as exc:
        raise ValueError(
            "loaded sequence starting continuation retains incoherent verification JSON."
        ) from exc

    _require_retained_document_self_integrity(
        document=document,
        record_payload=continuation_record,
        recorded_sha256=recorded_sha256,
        verification_sha256=verification.continuation_record_sha256,
        verification_document_json=verification.document_json,
        verification_byte_count=verification.byte_count,
        label="loaded sequence starting continuation",
    )

    prior = continuation_record["prior_revision_reference"]
    continuation = continuation_record["continuation"]
    revision = continuation["revision"]
    revised_note = revision["revised_note"]
    if verification.continuation_format != _CONTINUATION_FORMAT:
        raise ValueError("loaded sequence starting continuation format is unsupported.")
    if verification.prior_revision_format != prior["format"]:
        raise ValueError("loaded sequence starting continuation predecessor format is incoherent.")
    if not hmac.compare_digest(
        verification.prior_revision_record_sha256,
        prior["revision_record_sha256"],
    ):
        raise ValueError("loaded sequence starting continuation predecessor identity is incoherent.")
    if verification.continuation_mode != continuation["mode"]:
        raise ValueError("loaded sequence starting continuation mode is incoherent.")
    if verification.revision_mode != revision["mode"]:
        raise ValueError("loaded sequence starting continuation revision mode is incoherent.")
    if verification.revised_note_mode != revised_note["mode"]:
        raise ValueError("loaded sequence starting continuation note mode is incoherent.")
    if verification.revised_note_text != revised_note["text"]:
        raise ValueError("loaded sequence starting continuation text is incoherent.")

    return ChromiumPageResearchWorkingSetNoteRevisionEdgeSequenceReference(
        record_format=_CONTINUATION_FORMAT,
        record_sha256=recorded_sha256,
    )


def _retained_edge_reference(
    record: ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord,
) -> ChromiumPageResearchWorkingSetNoteRevisionEdgeSequenceReference:
    verification = record.verification
    try:
        document = json.loads(verification.document_json)
        edge_record, recorded_sha256 = _validate_edge_persisted_document(document)
    except (TypeError, ValueError, json.JSONDecodeError) as exc:
        raise ValueError("loaded sequence edge retains incoherent verification JSON.") from exc

    _require_retained_document_self_integrity(
        document=document,
        record_payload=edge_record,
        recorded_sha256=recorded_sha256,
        verification_sha256=verification.edge_record_sha256,
        verification_document_json=verification.document_json,
        verification_byte_count=verification.byte_count,
        label="loaded sequence edge",
    )

    predecessor = edge_record["predecessor_reference"]
    edge = edge_record["edge"]
    revision = edge["revision"]
    revised_note = revision["revised_note"]
    if verification.edge_format != _EDGE_FORMAT:
        raise ValueError("loaded sequence edge format is unsupported.")
    if verification.predecessor_format != predecessor["format"]:
        raise ValueError("loaded sequence edge predecessor format is incoherent.")
    if not hmac.compare_digest(
        verification.predecessor_record_sha256,
        predecessor["record_sha256"],
    ):
        raise ValueError("loaded sequence edge predecessor identity is incoherent.")
    if verification.edge_mode != edge["mode"]:
        raise ValueError("loaded sequence edge mode is incoherent.")
    if verification.revision_mode != revision["mode"]:
        raise ValueError("loaded sequence edge revision mode is incoherent.")
    if verification.revised_note_mode != revised_note["mode"]:
        raise ValueError("loaded sequence edge note mode is incoherent.")
    if verification.revised_note_text != revised_note["text"]:
        raise ValueError("loaded sequence edge text is incoherent.")

    return ChromiumPageResearchWorkingSetNoteRevisionEdgeSequenceReference(
        record_format=_EDGE_FORMAT,
        record_sha256=recorded_sha256,
    )


def _require_retained_document_self_integrity(
    *,
    document: Any,
    record_payload: Any,
    recorded_sha256: str,
    verification_sha256: object,
    verification_document_json: object,
    verification_byte_count: object,
    label: str,
) -> None:
    observed_sha256 = hashlib.sha256(_canonical_json_bytes(record_payload)).hexdigest()
    if not hmac.compare_digest(recorded_sha256, observed_sha256):
        raise ValueError(f"{label} retained record SHA-256 is internally incoherent.")
    if not _is_sha256(verification_sha256) or not hmac.compare_digest(
        recorded_sha256,
        verification_sha256,
    ):
        raise ValueError(f"{label} retained verification identity is incoherent.")

    canonical_document = _canonical_document_bytes(document)
    if type(verification_document_json) is not str:
        raise ValueError(f"{label} retained verification JSON is not text.")
    retained_bytes = verification_document_json.encode("utf-8")
    if retained_bytes != canonical_document:
        raise ValueError(f"{label} retained verification JSON is not canonical.")
    if type(verification_byte_count) is not int or verification_byte_count != len(
        retained_bytes
    ):
        raise ValueError(f"{label} retained verification byte count is incoherent.")


def _validate_persisted_document(document: Any) -> tuple[dict[str, Any], str]:
    if type(document) is not dict or set(document) != {
        "format",
        "sequence_record",
        "sequence_record_sha256",
    }:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeSequenceIntegrityError(
            "Research revision-edge-sequence document has an invalid top-level shape."
        )
    if document["format"] != _SEQUENCE_FORMAT:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeSequenceIntegrityError(
            "Research revision-edge-sequence format is unsupported."
        )

    recorded_sha256 = document["sequence_record_sha256"]
    if not _is_sha256(recorded_sha256):
        raise ChromiumResearchWorkingSetNoteRevisionEdgeSequenceIntegrityError(
            "Research revision-edge-sequence SHA-256 has an invalid shape."
        )

    sequence_record = document["sequence_record"]
    if type(sequence_record) is not dict or set(sequence_record) != {
        "edge_references",
        "sequence_mode",
        "starting_predecessor_reference",
    }:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeSequenceIntegrityError(
            "Research revision-edge-sequence record has an invalid shape."
        )
    if sequence_record["sequence_mode"] != _SEQUENCE_MODE:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeSequenceIntegrityError(
            "Research revision-edge-sequence mode is unsupported."
        )

    starting = sequence_record["starting_predecessor_reference"]
    _validate_reference(
        starting,
        allowed_formats=_SUPPORTED_STARTING_FORMATS,
        label="starting predecessor",
    )

    edges = sequence_record["edge_references"]
    if type(edges) is not list or not edges:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeSequenceIntegrityError(
            "Research revision-edge-sequence edge references must be a non-empty ordered list."
        )
    for index, edge in enumerate(edges):
        _validate_reference(
            edge,
            allowed_formats=frozenset({_EDGE_FORMAT}),
            label=f"edge reference {index}",
        )

    return sequence_record, recorded_sha256


def _validate_reference(
    reference: Any,
    *,
    allowed_formats: frozenset[str],
    label: str,
) -> None:
    if type(reference) is not dict or set(reference) != {"format", "record_sha256"}:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeSequenceIntegrityError(
            f"Research revision-edge-sequence {label} has an invalid shape."
        )
    if reference["format"] not in allowed_formats:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeSequenceIntegrityError(
            f"Research revision-edge-sequence {label} format is unsupported."
        )
    if not _is_sha256(reference["record_sha256"]):
        raise ChromiumResearchWorkingSetNoteRevisionEdgeSequenceIntegrityError(
            f"Research revision-edge-sequence {label} SHA-256 has an invalid shape."
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
            "Research revision-edge-sequence record is not canonical-JSON serializable."
        ) from exc
    return encoded.encode("utf-8")


def _canonical_document_bytes(document: Any) -> bytes:
    return _canonical_json_bytes(document) + b"\n"
