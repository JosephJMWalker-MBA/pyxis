from __future__ import annotations

from dataclasses import dataclass
import hashlib
import hmac
import json
from pathlib import Path
from typing import Any

from .chromium_research_session_working_set_transition import (
    ChromiumResearchSessionWorkingSetTransitionRecord,
)
from .chromium_research_working_set import create_chromium_research_working_set
from .chromium_research_working_set_note import create_chromium_research_working_set_note
from .chromium_research_working_set_note_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRecord,
    load_chromium_research_working_set_note,
)
from .chromium_research_working_set_note_revision_edge_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord,
    load_chromium_research_working_set_note_revision_edge,
)


_TRANSITION_FORMAT = "pyxis.chromium.research_session_working_set_transition.v1"
_TRANSITION_MODE = "caller_explicit_transition_to_changed_research_working_set"
_EDGE_FORMAT = "pyxis.chromium.research_working_set_note_revision_edge.v1"
_WORKING_SET_FORMAT = "pyxis.chromium.research_working_set.v1"
_NOTE_FORMAT = "pyxis.chromium.research_working_set_note.v1"


class ChromiumResearchSessionWorkingSetTransitionIntegrityError(ValueError):
    """Raised when durable transition bytes fail their file-local integrity contract."""


@dataclass(frozen=True, slots=True)
class ChromiumResearchSessionWorkingSetTransitionPersistenceEvidence:
    """Durable write evidence for one explicit cross-working-set transition."""

    path: Path
    transition_format: str
    transition_record_sha256: str
    byte_count: int
    transition: ChromiumResearchSessionWorkingSetTransitionRecord
    fresh_prior_endpoint: ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord
    fresh_successor_note: ChromiumPageResearchLoadedWorkingSetNoteRecord


@dataclass(frozen=True, slots=True)
class ChromiumResearchSessionWorkingSetTransitionVerificationEvidence:
    """File-local verification facts for one persisted cross-working-set transition."""

    path: Path
    transition_format: str
    transition_record_sha256: str
    byte_count: int
    transition_mode: str
    prior_endpoint_format: str
    prior_endpoint_record_sha256: str
    successor_working_set_format: str
    successor_working_set_record_sha256: str
    successor_note_format: str
    successor_note_record_sha256: str
    document_json: str


def persist_chromium_research_session_working_set_transition(
    transition: ChromiumResearchSessionWorkingSetTransitionRecord,
    *,
    prior_edge_source: Path,
    working_set_source: Path,
    note_source: Path,
    destination: Path,
) -> ChromiumResearchSessionWorkingSetTransitionPersistenceEvidence:
    """Freshly re-establish explicit durable inputs and persist one transition record.

    Every locator is caller supplied. Pyxis does not search for the prior edge, changed
    working set, changed note, or destination. The prior endpoint is freshly reopened
    through public 24C against its retained explicit predecessor. The successor basis
    is freshly reopened through public 21C, which in turn re-establishes public 20C.

    Only after those identities agree with the in-memory transition is a canonical,
    no-overwrite transition file written. The file records content identities only;
    it stores no paths, timestamps, chronology, semantic-support fields, or head state.
    """

    _validate_transition_shape(transition)
    path = _preflight_destination(destination)

    fresh_prior = load_chromium_research_working_set_note_revision_edge(
        transition.prior_endpoint.predecessor,
        _require_path(prior_edge_source, label="prior_edge_source"),
    )
    _require_same_prior_endpoint(transition.prior_endpoint, fresh_prior)

    fresh_successor = load_chromium_research_working_set_note(
        transition.successor_working_set.items,
        _require_path(working_set_source, label="working_set_source"),
        _require_path(note_source, label="note_source"),
    )
    _require_same_successor_basis(transition, fresh_successor)

    transition_record = {
        "prior_endpoint_reference": {
            "format": fresh_prior.verification.edge_format,
            "record_sha256": fresh_prior.verification.edge_record_sha256,
        },
        "successor_note_reference": {
            "format": fresh_successor.verification.note_format,
            "record_sha256": fresh_successor.verification.note_record_sha256,
        },
        "successor_working_set_reference": {
            "format": fresh_successor.working_set.verification.working_set_format,
            "record_sha256": (
                fresh_successor.working_set.verification.working_set_record_sha256
            ),
        },
        "transition_mode": transition.transition_mode,
    }
    record_bytes = _canonical_json_bytes(transition_record)
    record_sha256 = hashlib.sha256(record_bytes).hexdigest()
    document = {
        "format": _TRANSITION_FORMAT,
        "transition_record": transition_record,
        "transition_record_sha256": record_sha256,
    }
    document_bytes = _canonical_document_bytes(document)

    with path.open("xb") as handle:
        handle.write(document_bytes)

    return ChromiumResearchSessionWorkingSetTransitionPersistenceEvidence(
        path=path,
        transition_format=_TRANSITION_FORMAT,
        transition_record_sha256=record_sha256,
        byte_count=len(document_bytes),
        transition=transition,
        fresh_prior_endpoint=fresh_prior,
        fresh_successor_note=fresh_successor,
    )


def verify_chromium_research_session_working_set_transition(
    source: Path,
) -> ChromiumResearchSessionWorkingSetTransitionVerificationEvidence:
    """Verify one transition file without opening any referenced durable record."""

    path = _require_path(source, label="source").expanduser().resolve()
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ChromiumResearchSessionWorkingSetTransitionIntegrityError(
            "Research working-set transition is not valid UTF-8."
        ) from exc

    try:
        document = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ChromiumResearchSessionWorkingSetTransitionIntegrityError(
            "Research working-set transition is not valid JSON."
        ) from exc

    record, recorded_sha256 = _validate_document(document)
    observed_sha256 = hashlib.sha256(_canonical_json_bytes(record)).hexdigest()
    if not hmac.compare_digest(recorded_sha256, observed_sha256):
        raise ChromiumResearchSessionWorkingSetTransitionIntegrityError(
            "Research working-set-transition SHA-256 does not match the persisted record."
        )
    if raw != _canonical_document_bytes(document):
        raise ChromiumResearchSessionWorkingSetTransitionIntegrityError(
            "Research working-set-transition bytes are not canonical Pyxis JSON."
        )

    prior = record["prior_endpoint_reference"]
    working_set = record["successor_working_set_reference"]
    note = record["successor_note_reference"]
    return ChromiumResearchSessionWorkingSetTransitionVerificationEvidence(
        path=path,
        transition_format=_TRANSITION_FORMAT,
        transition_record_sha256=recorded_sha256,
        byte_count=len(raw),
        transition_mode=record["transition_mode"],
        prior_endpoint_format=prior["format"],
        prior_endpoint_record_sha256=prior["record_sha256"],
        successor_working_set_format=working_set["format"],
        successor_working_set_record_sha256=working_set["record_sha256"],
        successor_note_format=note["format"],
        successor_note_record_sha256=note["record_sha256"],
        document_json=text,
    )


def _validate_transition_shape(
    transition: ChromiumResearchSessionWorkingSetTransitionRecord,
) -> None:
    if not isinstance(transition, ChromiumResearchSessionWorkingSetTransitionRecord):
        raise TypeError(
            "transition must be ChromiumResearchSessionWorkingSetTransitionRecord."
        )
    if transition.transition_mode != _TRANSITION_MODE:
        raise ValueError("transition mode is unsupported for durable persistence.")
    if not isinstance(
        transition.prior_endpoint,
        ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord,
    ):
        raise TypeError("transition prior endpoint has an unsupported loaded-record type.")
    if transition.successor_note.working_set is not transition.successor_working_set:
        raise ValueError("transition successor note is not attached to its exact working set.")
    if (
        transition.successor_working_set
        is transition.prior_endpoint.revision.revised_note.working_set
    ):
        raise ValueError("cross-working-set transition must use a different working-set object.")

    rebuilt_working_set = create_chromium_research_working_set(
        transition.successor_working_set.items
    )
    if rebuilt_working_set.working_set_mode != transition.successor_working_set.working_set_mode:
        raise ValueError("transition successor working set is incoherent with 20A.")
    rebuilt_note = create_chromium_research_working_set_note(
        transition.successor_working_set,
        note_text=transition.successor_note.note_text,
    )
    if rebuilt_note.note_mode != transition.successor_note.note_mode:
        raise ValueError("transition successor note is incoherent with 21A.")


def _require_same_prior_endpoint(
    expected: ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord,
    observed: ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord,
) -> None:
    if observed.verification.edge_format != _EDGE_FORMAT:
        raise ValueError("fresh prior endpoint uses an unsupported edge format.")
    if expected.verification.edge_format != observed.verification.edge_format:
        raise ValueError("fresh prior endpoint has a different edge format.")
    if not hmac.compare_digest(
        expected.verification.edge_record_sha256,
        observed.verification.edge_record_sha256,
    ):
        raise ValueError("fresh prior endpoint identifies a different edge record.")


def _require_same_successor_basis(
    transition: ChromiumResearchSessionWorkingSetTransitionRecord,
    observed: ChromiumPageResearchLoadedWorkingSetNoteRecord,
) -> None:
    if observed.working_set.verification.working_set_format != _WORKING_SET_FORMAT:
        raise ValueError("fresh successor working set uses an unsupported format.")
    if observed.verification.note_format != _NOTE_FORMAT:
        raise ValueError("fresh successor note uses an unsupported format.")
    if observed.note.note_text != transition.successor_note.note_text:
        raise ValueError("fresh successor note has different human text.")
    if observed.note.note_mode != transition.successor_note.note_mode:
        raise ValueError("fresh successor note has a different note mode.")
    if len(observed.working_set.working_set.items) != len(
        transition.successor_working_set.items
    ):
        raise ValueError("fresh successor working set has a different member count.")
    for index, (fresh_item, expected_item) in enumerate(
        zip(
            observed.working_set.working_set.items,
            transition.successor_working_set.items,
        )
    ):
        if fresh_item is not expected_item:
            raise ValueError(
                f"fresh successor working-set member {index} lost exact object identity."
            )


def _preflight_destination(value: Path) -> Path:
    path = _require_path(value, label="destination").expanduser().resolve()
    if not path.parent.is_dir():
        raise FileNotFoundError(
            f"Research working-set-transition parent directory does not exist: {path.parent}"
        )
    if path.exists():
        raise FileExistsError(f"Research working-set-transition destination exists: {path}")
    return path


def _require_path(value: Path, *, label: str) -> Path:
    if not isinstance(value, Path):
        raise TypeError(f"{label} must be pathlib.Path.")
    return value


def _validate_document(document: Any) -> tuple[dict[str, Any], str]:
    if type(document) is not dict or set(document) != {
        "format",
        "transition_record",
        "transition_record_sha256",
    }:
        raise ChromiumResearchSessionWorkingSetTransitionIntegrityError(
            "Research working-set-transition document has an invalid top-level shape."
        )
    if document["format"] != _TRANSITION_FORMAT:
        raise ChromiumResearchSessionWorkingSetTransitionIntegrityError(
            "Research working-set-transition format is unsupported."
        )
    recorded_sha256 = document["transition_record_sha256"]
    if not _is_sha256(recorded_sha256):
        raise ChromiumResearchSessionWorkingSetTransitionIntegrityError(
            "Research working-set-transition SHA-256 has an invalid shape."
        )

    record = document["transition_record"]
    if type(record) is not dict or set(record) != {
        "prior_endpoint_reference",
        "successor_note_reference",
        "successor_working_set_reference",
        "transition_mode",
    }:
        raise ChromiumResearchSessionWorkingSetTransitionIntegrityError(
            "Research working-set-transition record has an invalid shape."
        )
    if record["transition_mode"] != _TRANSITION_MODE:
        raise ChromiumResearchSessionWorkingSetTransitionIntegrityError(
            "Research working-set-transition mode is unsupported."
        )

    _validate_reference(
        record["prior_endpoint_reference"],
        expected_format=_EDGE_FORMAT,
        label="prior endpoint",
    )
    _validate_reference(
        record["successor_working_set_reference"],
        expected_format=_WORKING_SET_FORMAT,
        label="successor working set",
    )
    _validate_reference(
        record["successor_note_reference"],
        expected_format=_NOTE_FORMAT,
        label="successor note",
    )
    return record, recorded_sha256


def _validate_reference(value: Any, *, expected_format: str, label: str) -> None:
    if type(value) is not dict or set(value) != {"format", "record_sha256"}:
        raise ChromiumResearchSessionWorkingSetTransitionIntegrityError(
            f"Research working-set-transition {label} reference has an invalid shape."
        )
    if value["format"] != expected_format:
        raise ChromiumResearchSessionWorkingSetTransitionIntegrityError(
            f"Research working-set-transition {label} format is unsupported."
        )
    if not _is_sha256(value["record_sha256"]):
        raise ChromiumResearchSessionWorkingSetTransitionIntegrityError(
            f"Research working-set-transition {label} SHA-256 has an invalid shape."
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
            "Research working-set-transition record is not canonical-JSON serializable."
        ) from exc
    return encoded.encode("utf-8")


def _canonical_document_bytes(document: Any) -> bytes:
    return _canonical_json_bytes(document) + b"\n"
