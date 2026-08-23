from __future__ import annotations

from dataclasses import dataclass
import hashlib
import hmac
import json
from pathlib import Path
from typing import Any

from .chromium_research_session_working_set_transition_load import (
    ChromiumPageResearchLoadedWorkingSetTransitionRecord,
    load_chromium_research_session_working_set_transition,
)
from .chromium_research_session_working_set_transition_revision_root import (
    ChromiumResearchSessionWorkingSetTransitionRevisionRootRecord,
    create_chromium_research_session_working_set_transition_revision_root,
)


_ROOT_FORMAT = (
    "pyxis.chromium.research_session_working_set_transition_revision_root.v1"
)
_TRANSITION_FORMAT = "pyxis.chromium.research_session_working_set_transition.v1"
_ROOT_MODE = (
    "caller_authored_revision_root_after_changed_research_working_set_transition"
)
_REVISION_MODE = "caller_authored_revision_of_research_working_set_note"
_NOTE_MODE = "caller_authored_note_on_research_working_set"


class ChromiumResearchSessionWorkingSetTransitionRevisionRootIntegrityError(ValueError):
    """Raised when persisted cross-working-set revision-root bytes fail integrity."""


@dataclass(frozen=True, slots=True)
class ChromiumResearchSessionWorkingSetTransitionRevisionRootPersistenceEvidence:
    """Durable evidence for one 34A cross-working-set revision root.

    `root` retains the exact caller-supplied in-memory root. `fresh_transition` is a
    fresh 33B relink performed immediately before persistence. The durable file stores
    only that verified transition identity plus the first ordinary same-working-set
    human revision wording.
    """

    path: Path
    root_format: str
    root_record_sha256: str
    byte_count: int
    root: ChromiumResearchSessionWorkingSetTransitionRevisionRootRecord
    fresh_transition: ChromiumPageResearchLoadedWorkingSetTransitionRecord


@dataclass(frozen=True, slots=True)
class ChromiumResearchSessionWorkingSetTransitionRevisionRootVerificationEvidence:
    """File-local verification facts for one 34A root document."""

    path: Path
    root_format: str
    root_record_sha256: str
    byte_count: int
    transition_format: str
    transition_record_sha256: str
    root_mode: str
    revision_mode: str
    revised_note_mode: str
    revised_note_text: str
    document_json: str


def persist_chromium_research_session_working_set_transition_revision_root(
    root: ChromiumResearchSessionWorkingSetTransitionRevisionRootRecord,
    *,
    prior_edge_source: Path,
    working_set_source: Path,
    note_source: Path,
    transition_source: Path,
    destination: Path,
) -> ChromiumResearchSessionWorkingSetTransitionRevisionRootPersistenceEvidence:
    """Persist one first rationale revision rooted in an exact durable 33B transition.

    The transition is freshly relinked from every caller-supplied locator before any
    root bytes are written. The fresh transition identity must match the exact loaded
    transition retained by `root`, and public 34A creation must reconstruct the same
    first revised human wording over that fresh transition successor note.

    No path discovery, chronology, branch/head selection, session adoption, semantic
    support inference, or history traversal occurs.
    """

    if not isinstance(
        root,
        ChromiumResearchSessionWorkingSetTransitionRevisionRootRecord,
    ):
        raise TypeError(
            "root must be ChromiumResearchSessionWorkingSetTransitionRevisionRootRecord."
        )

    rebuilt = create_chromium_research_session_working_set_transition_revision_root(
        root.transition,
        revised_note_text=root.revision.revised_note.note_text,
    )
    if rebuilt.root_mode != root.root_mode or root.root_mode != _ROOT_MODE:
        raise ValueError("Cross-working-set revision root mode is unsupported.")
    if rebuilt.revision.revision_mode != root.revision.revision_mode:
        raise ValueError("Cross-working-set root revision mode is incoherent.")
    if root.revision.revision_mode != _REVISION_MODE:
        raise ValueError("Cross-working-set root revision mode is unsupported.")
    if root.revision.revised_note.note_mode != _NOTE_MODE:
        raise ValueError("Cross-working-set root revised-note mode is unsupported.")
    if root.revision.prior_note is not root.transition.successor_note.note:
        raise ValueError("Cross-working-set root must retain the exact transition successor note.")

    fresh_transition = load_chromium_research_session_working_set_transition(
        root.transition.prior_endpoint,
        root.transition.successor_note.note.working_set.items,
        prior_edge_source=_require_path(prior_edge_source, label="prior_edge_source"),
        working_set_source=_require_path(working_set_source, label="working_set_source"),
        note_source=_require_path(note_source, label="note_source"),
        transition_source=_require_path(transition_source, label="transition_source"),
    )
    if fresh_transition.verification.transition_format != _TRANSITION_FORMAT:
        raise ValueError("Fresh root transition uses an unsupported format.")
    if root.transition.verification.transition_format != _TRANSITION_FORMAT:
        raise ValueError("Retained root transition uses an unsupported format.")
    if not hmac.compare_digest(
        fresh_transition.verification.transition_record_sha256,
        root.transition.verification.transition_record_sha256,
    ):
        raise ValueError("Fresh durable transition does not match the retained root transition.")

    fresh_root = create_chromium_research_session_working_set_transition_revision_root(
        fresh_transition,
        revised_note_text=root.revision.revised_note.note_text,
    )
    if fresh_root.root_mode != root.root_mode:
        raise ValueError("Fresh durable transition reconstructs a different root mode.")
    if fresh_root.revision.revised_note.note_text != root.revision.revised_note.note_text:
        raise ValueError("Fresh durable transition reconstructs different root wording.")

    path = _preflight_destination(destination)
    root_record = {
        "root": {
            "mode": root.root_mode,
            "revision": {
                "mode": root.revision.revision_mode,
                "revised_note": {
                    "mode": root.revision.revised_note.note_mode,
                    "text": root.revision.revised_note.note_text,
                },
            },
        },
        "transition_reference": {
            "format": fresh_transition.verification.transition_format,
            "record_sha256": fresh_transition.verification.transition_record_sha256,
        },
    }
    root_record_bytes = _canonical_json_bytes(root_record)
    root_record_sha256 = hashlib.sha256(root_record_bytes).hexdigest()
    document = {
        "format": _ROOT_FORMAT,
        "root_record": root_record,
        "root_record_sha256": root_record_sha256,
    }
    document_bytes = _canonical_document_bytes(document)
    with path.open("xb") as handle:
        handle.write(document_bytes)

    return ChromiumResearchSessionWorkingSetTransitionRevisionRootPersistenceEvidence(
        path=path,
        root_format=_ROOT_FORMAT,
        root_record_sha256=root_record_sha256,
        byte_count=len(document_bytes),
        root=root,
        fresh_transition=fresh_transition,
    )


def verify_chromium_research_session_working_set_transition_revision_root(
    source: Path,
) -> ChromiumResearchSessionWorkingSetTransitionRevisionRootVerificationEvidence:
    """Verify one root file locally without opening its referenced transition."""

    path = _require_path(source, label="source").expanduser().resolve()
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootIntegrityError(
            "Cross-working-set revision root is not valid UTF-8."
        ) from exc
    try:
        document = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootIntegrityError(
            "Cross-working-set revision root is not valid JSON."
        ) from exc

    root_record, recorded_sha256 = _validate_document(document)
    observed_sha256 = hashlib.sha256(_canonical_json_bytes(root_record)).hexdigest()
    if not hmac.compare_digest(recorded_sha256, observed_sha256):
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootIntegrityError(
            "Cross-working-set revision-root SHA-256 does not match the persisted record."
        )
    if raw != _canonical_document_bytes(document):
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootIntegrityError(
            "Cross-working-set revision-root bytes are not canonical Pyxis JSON."
        )

    transition_reference = root_record["transition_reference"]
    root_payload = root_record["root"]
    revision = root_payload["revision"]
    revised_note = revision["revised_note"]
    return ChromiumResearchSessionWorkingSetTransitionRevisionRootVerificationEvidence(
        path=path,
        root_format=_ROOT_FORMAT,
        root_record_sha256=recorded_sha256,
        byte_count=len(raw),
        transition_format=transition_reference["format"],
        transition_record_sha256=transition_reference["record_sha256"],
        root_mode=root_payload["mode"],
        revision_mode=revision["mode"],
        revised_note_mode=revised_note["mode"],
        revised_note_text=revised_note["text"],
        document_json=text,
    )


def _validate_document(document: Any) -> tuple[dict[str, Any], str]:
    if type(document) is not dict or set(document) != {
        "format",
        "root_record",
        "root_record_sha256",
    }:
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootIntegrityError(
            "Cross-working-set revision-root document has an invalid top-level shape."
        )
    if document["format"] != _ROOT_FORMAT:
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootIntegrityError(
            "Cross-working-set revision-root format is unsupported."
        )
    recorded_sha256 = document["root_record_sha256"]
    if not _is_sha256(recorded_sha256):
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootIntegrityError(
            "Cross-working-set revision-root SHA-256 has an invalid shape."
        )

    root_record = document["root_record"]
    if type(root_record) is not dict or set(root_record) != {"root", "transition_reference"}:
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootIntegrityError(
            "Cross-working-set revision-root record has an invalid shape."
        )
    transition_reference = root_record["transition_reference"]
    if type(transition_reference) is not dict or set(transition_reference) != {
        "format",
        "record_sha256",
    }:
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootIntegrityError(
            "Cross-working-set revision-root transition reference has an invalid shape."
        )
    if transition_reference["format"] != _TRANSITION_FORMAT:
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootIntegrityError(
            "Cross-working-set revision-root transition format is unsupported."
        )
    if not _is_sha256(transition_reference["record_sha256"]):
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootIntegrityError(
            "Cross-working-set revision-root transition SHA-256 has an invalid shape."
        )

    root_payload = root_record["root"]
    if type(root_payload) is not dict or set(root_payload) != {"mode", "revision"}:
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootIntegrityError(
            "Cross-working-set revision-root payload has an invalid shape."
        )
    if root_payload["mode"] != _ROOT_MODE:
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootIntegrityError(
            "Cross-working-set revision-root mode is unsupported."
        )
    revision = root_payload["revision"]
    if type(revision) is not dict or set(revision) != {"mode", "revised_note"}:
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootIntegrityError(
            "Cross-working-set revision-root revision payload has an invalid shape."
        )
    if revision["mode"] != _REVISION_MODE:
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootIntegrityError(
            "Cross-working-set revision-root revision mode is unsupported."
        )
    revised_note = revision["revised_note"]
    if type(revised_note) is not dict or set(revised_note) != {"mode", "text"}:
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootIntegrityError(
            "Cross-working-set revision-root revised note has an invalid shape."
        )
    if revised_note["mode"] != _NOTE_MODE:
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootIntegrityError(
            "Cross-working-set revision-root revised-note mode is unsupported."
        )
    text = revised_note["text"]
    if type(text) is not str or not text.strip():
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootIntegrityError(
            "Cross-working-set revision-root revised text must contain human text."
        )
    return root_record, recorded_sha256


def _require_path(value: Path, *, label: str) -> Path:
    if not isinstance(value, Path):
        raise TypeError(f"{label} must be pathlib.Path.")
    return value


def _preflight_destination(value: Path) -> Path:
    path = _require_path(value, label="destination").expanduser().resolve()
    if not path.parent.is_dir():
        raise FileNotFoundError(
            f"Cross-working-set revision-root parent directory does not exist: {path.parent}"
        )
    if path.exists():
        raise FileExistsError(f"Cross-working-set revision-root destination already exists: {path}")
    return path


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
            "Cross-working-set revision-root record is not canonical-JSON serializable."
        ) from exc
    return encoded.encode("utf-8")


def _canonical_document_bytes(document: Any) -> bytes:
    return _canonical_json_bytes(document) + b"\n"


__all__ = [
    "ChromiumResearchSessionWorkingSetTransitionRevisionRootIntegrityError",
    "ChromiumResearchSessionWorkingSetTransitionRevisionRootPersistenceEvidence",
    "ChromiumResearchSessionWorkingSetTransitionRevisionRootVerificationEvidence",
    "persist_chromium_research_session_working_set_transition_revision_root",
    "verify_chromium_research_session_working_set_transition_revision_root",
]
