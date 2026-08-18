from __future__ import annotations

from dataclasses import dataclass
import hashlib
import hmac
import json
from pathlib import Path
from typing import Any

from .chromium_research_paragraph_text_selection_comparison_note_load import (
    ChromiumPageResearchLoadedParagraphTextSelectionComparisonNoteRecord,
)
from .chromium_research_paragraph_text_selection_note_load import (
    ChromiumPageResearchLoadedParagraphTextSelectionNoteRecord,
)
from .chromium_research_selection_note_load import (
    ChromiumPageResearchLoadedParagraphNoteRecord,
)
from .chromium_research_working_set import (
    ChromiumPageResearchWorkingSetRecord,
    create_chromium_research_working_set,
)


_WORKING_SET_FORMAT = "pyxis.chromium.research_working_set.v1"
_WORKING_SET_MODE = "caller_explicit_ordered_relinked_research_working_set"

_PARAGRAPH_NOTE_KIND = "paragraph_note"
_PARAGRAPH_NOTE_FORMAT = "pyxis.chromium.research_paragraph_note.v1"
_EXACT_RANGE_NOTE_KIND = "exact_range_note"
_EXACT_RANGE_NOTE_FORMAT = "pyxis.chromium.research_paragraph_text_selection_note.v1"
_COMPARISON_NOTE_KIND = "comparison_note"
_COMPARISON_NOTE_FORMAT = (
    "pyxis.chromium.research_paragraph_text_selection_comparison_note.v1"
)


class ChromiumResearchWorkingSetIntegrityError(ValueError):
    """Raised when persisted working-set bytes fail their integrity contract."""


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchWorkingSetMemberReference:
    """One durable member identity inside a persisted research working set.

    The reference identifies only the already-verified durable member record by
    its explicit member family, sidecar format, and sidecar record SHA-256. It
    does not copy source text, human-note text, source-capture references, or a
    filesystem path, and it does not prove the referenced member file still exists.
    """

    member_kind: str
    member_format: str
    member_record_sha256: str


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchWorkingSetPersistenceEvidence:
    """Durable-file evidence for one already-created 20A research working set.

    `working_set` retains the exact in-memory 20A record supplied to persistence.
    The durable file stores only ordered member identities and the established
    working-set mode. It does not serialize member notes, selected text, source
    capture graphs, or member sidecar paths.
    """

    path: Path
    working_set_format: str
    working_set_record_sha256: str
    byte_count: int
    working_set: ChromiumPageResearchWorkingSetRecord


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchWorkingSetVerificationEvidence:
    """Verified file-local integrity facts for one 20B working-set sidecar.

    Verification proves canonical Pyxis JSON, the recorded SHA-256, the explicit
    working-set mode, and the ordered structural shape of durable member identities.
    It does not locate, reread, authenticate, or relink any referenced member.
    """

    path: Path
    working_set_format: str
    working_set_record_sha256: str
    byte_count: int
    working_set_mode: str
    items: tuple[ChromiumPageResearchWorkingSetMemberReference, ...]
    document_json: str


def persist_chromium_research_working_set(
    working_set: ChromiumPageResearchWorkingSetRecord,
    destination: Path,
) -> ChromiumPageResearchWorkingSetPersistenceEvidence:
    """Persist one 20A working set as deterministic no-overwrite canonical JSON.

    Persistence re-establishes the existing 20A in-memory coherence boundary, then
    records only each member's retained durable sidecar identity. It deliberately
    does not reread any member sidecar. A member sidecar may therefore be absent
    after successful earlier relinking while its retained verification identity is
    still eligible for working-set persistence.

    The working-set SHA-256 is self-integrity evidence only. It does not prove that
    any member sidecar still exists, remains unchanged, can be freshly relinked, or
    is semantically related to any other member.
    """

    _validate_live_working_set(working_set)

    path = Path(destination).expanduser().resolve()
    if not path.parent.is_dir():
        raise FileNotFoundError(
            f"Research working-set parent directory does not exist: {path.parent}"
        )

    working_set_record = _working_set_record_payload(working_set)
    working_set_record_bytes = _canonical_json_bytes(working_set_record)
    working_set_record_sha256 = hashlib.sha256(working_set_record_bytes).hexdigest()
    document = {
        "format": _WORKING_SET_FORMAT,
        "working_set_record": working_set_record,
        "working_set_record_sha256": working_set_record_sha256,
    }
    document_bytes = _canonical_document_bytes(document)

    with path.open("xb") as handle:
        handle.write(document_bytes)

    return ChromiumPageResearchWorkingSetPersistenceEvidence(
        path=path,
        working_set_format=_WORKING_SET_FORMAT,
        working_set_record_sha256=working_set_record_sha256,
        byte_count=len(document_bytes),
        working_set=working_set,
    )


def verify_chromium_research_working_set(
    source: Path,
) -> ChromiumPageResearchWorkingSetVerificationEvidence:
    """Verify canonical bytes and recorded digest for one working-set sidecar only.

    This operation reads only the working-set file. It does not search for, read,
    verify, or relink any referenced paragraph-note, exact-range-note, comparison-
    note, source capture, or browser state. Member re-establishment is a separate
    authority boundary.
    """

    path = Path(source).expanduser().resolve()
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ChromiumResearchWorkingSetIntegrityError(
            "Research working set is not valid UTF-8."
        ) from exc

    try:
        document = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ChromiumResearchWorkingSetIntegrityError(
            "Research working set is not valid JSON."
        ) from exc

    working_set_record, recorded_sha256 = _validate_persisted_document(document)
    observed_sha256 = hashlib.sha256(
        _canonical_json_bytes(working_set_record)
    ).hexdigest()
    if not hmac.compare_digest(recorded_sha256, observed_sha256):
        raise ChromiumResearchWorkingSetIntegrityError(
            "Research working-set SHA-256 does not match the persisted record."
        )

    canonical_document_bytes = _canonical_document_bytes(document)
    if raw != canonical_document_bytes:
        raise ChromiumResearchWorkingSetIntegrityError(
            "Research working-set bytes are not in the canonical Pyxis JSON encoding."
        )

    item_references = tuple(
        ChromiumPageResearchWorkingSetMemberReference(
            member_kind=item["member_kind"],
            member_format=item["member_format"],
            member_record_sha256=item["member_record_sha256"],
        )
        for item in working_set_record["items"]
    )
    return ChromiumPageResearchWorkingSetVerificationEvidence(
        path=path,
        working_set_format=_WORKING_SET_FORMAT,
        working_set_record_sha256=recorded_sha256,
        byte_count=len(raw),
        working_set_mode=working_set_record["working_set_mode"],
        items=item_references,
        document_json=text,
    )


def _validate_live_working_set(
    working_set: ChromiumPageResearchWorkingSetRecord,
) -> None:
    if not isinstance(working_set, ChromiumPageResearchWorkingSetRecord):
        raise TypeError("working_set must be ChromiumPageResearchWorkingSetRecord.")
    if working_set.working_set_mode != _WORKING_SET_MODE:
        raise ValueError("working-set mode is unsupported for durable persistence.")

    rebuilt = create_chromium_research_working_set(working_set.items)
    if rebuilt.working_set_mode != working_set.working_set_mode:
        raise ValueError("working-set mode is incoherent with the established 20A boundary.")

    for index, item in enumerate(working_set.items):
        _member_reference(item, index=index)


def _working_set_record_payload(
    working_set: ChromiumPageResearchWorkingSetRecord,
) -> dict[str, Any]:
    return {
        "items": [
            {
                "member_format": reference.member_format,
                "member_kind": reference.member_kind,
                "member_record_sha256": reference.member_record_sha256,
            }
            for index, item in enumerate(working_set.items)
            for reference in (_member_reference(item, index=index),)
        ],
        "working_set_mode": working_set.working_set_mode,
    }


def _member_reference(
    item: object,
    *,
    index: int,
) -> ChromiumPageResearchWorkingSetMemberReference:
    if isinstance(item, ChromiumPageResearchLoadedParagraphNoteRecord):
        return _verification_reference(
            member_kind=_PARAGRAPH_NOTE_KIND,
            expected_format=_PARAGRAPH_NOTE_FORMAT,
            member_format=item.verification.note_format,
            member_record_sha256=item.verification.note_record_sha256,
            index=index,
        )
    if isinstance(item, ChromiumPageResearchLoadedParagraphTextSelectionNoteRecord):
        return _verification_reference(
            member_kind=_EXACT_RANGE_NOTE_KIND,
            expected_format=_EXACT_RANGE_NOTE_FORMAT,
            member_format=item.verification.note_format,
            member_record_sha256=item.verification.note_record_sha256,
            index=index,
        )
    if isinstance(
        item,
        ChromiumPageResearchLoadedParagraphTextSelectionComparisonNoteRecord,
    ):
        return _verification_reference(
            member_kind=_COMPARISON_NOTE_KIND,
            expected_format=_COMPARISON_NOTE_FORMAT,
            member_format=item.verification.note_format,
            member_record_sha256=item.verification.note_record_sha256,
            index=index,
        )
    raise TypeError(f"working_set.items[{index}] has an unsupported member family.")


def _verification_reference(
    *,
    member_kind: str,
    expected_format: str,
    member_format: object,
    member_record_sha256: object,
    index: int,
) -> ChromiumPageResearchWorkingSetMemberReference:
    if member_format != expected_format:
        raise ValueError(
            f"working_set.items[{index}] retained member sidecar format is unsupported."
        )
    if not _is_sha256(member_record_sha256):
        raise ValueError(
            f"working_set.items[{index}] retained member record SHA-256 has an invalid shape."
        )
    return ChromiumPageResearchWorkingSetMemberReference(
        member_kind=member_kind,
        member_format=expected_format,
        member_record_sha256=member_record_sha256,
    )


def _validate_persisted_document(document: Any) -> tuple[dict[str, Any], str]:
    if type(document) is not dict or set(document) != {
        "format",
        "working_set_record",
        "working_set_record_sha256",
    }:
        raise ChromiumResearchWorkingSetIntegrityError(
            "Research working-set document has an invalid top-level shape."
        )
    if document["format"] != _WORKING_SET_FORMAT:
        raise ChromiumResearchWorkingSetIntegrityError(
            "Research working-set format is unsupported."
        )

    recorded_sha256 = document["working_set_record_sha256"]
    if not _is_sha256(recorded_sha256):
        raise ChromiumResearchWorkingSetIntegrityError(
            "Research working-set SHA-256 has an invalid shape."
        )

    working_set_record = document["working_set_record"]
    if type(working_set_record) is not dict or set(working_set_record) != {
        "items",
        "working_set_mode",
    }:
        raise ChromiumResearchWorkingSetIntegrityError(
            "Research working-set record has an invalid shape."
        )
    if working_set_record["working_set_mode"] != _WORKING_SET_MODE:
        raise ChromiumResearchWorkingSetIntegrityError(
            "Research working-set mode is unsupported."
        )

    items = working_set_record["items"]
    if type(items) is not list or not items:
        raise ChromiumResearchWorkingSetIntegrityError(
            "Research working-set items must be a non-empty ordered list."
        )
    for index, item in enumerate(items):
        _validate_persisted_member_reference(item, index=index)

    return working_set_record, recorded_sha256


def _validate_persisted_member_reference(item: Any, *, index: int) -> None:
    if type(item) is not dict or set(item) != {
        "member_format",
        "member_kind",
        "member_record_sha256",
    }:
        raise ChromiumResearchWorkingSetIntegrityError(
            f"Research working-set item {index} has an invalid shape."
        )

    member_kind = item["member_kind"]
    expected_formats = {
        _PARAGRAPH_NOTE_KIND: _PARAGRAPH_NOTE_FORMAT,
        _EXACT_RANGE_NOTE_KIND: _EXACT_RANGE_NOTE_FORMAT,
        _COMPARISON_NOTE_KIND: _COMPARISON_NOTE_FORMAT,
    }
    if type(member_kind) is not str or member_kind not in expected_formats:
        raise ChromiumResearchWorkingSetIntegrityError(
            f"Research working-set item {index} has an unsupported member kind."
        )
    if item["member_format"] != expected_formats[member_kind]:
        raise ChromiumResearchWorkingSetIntegrityError(
            f"Research working-set item {index} has an unsupported member format."
        )
    if not _is_sha256(item["member_record_sha256"]):
        raise ChromiumResearchWorkingSetIntegrityError(
            f"Research working-set item {index} record SHA-256 has an invalid shape."
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
            "Research working-set record is not canonical-JSON serializable."
        ) from exc
    return encoded.encode("utf-8")


def _canonical_document_bytes(document: Any) -> bytes:
    return _canonical_json_bytes(document) + b"\n"
