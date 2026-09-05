from __future__ import annotations

from dataclasses import dataclass
import hashlib
import hmac
import json
from pathlib import Path
from typing import Any

from .chromium_research_paragraph_text_selection_load import (
    ChromiumPageResearchLoadedParagraphTextSelectionRecord,
)
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
_WORKING_SET_FORMAT_V2 = "pyxis.chromium.research_working_set.v2"
_WORKING_SET_MODE = "caller_explicit_ordered_relinked_research_working_set"

_PARAGRAPH_NOTE_KIND = "paragraph_note"
_PARAGRAPH_NOTE_FORMAT = "pyxis.chromium.research_paragraph_note.v1"
_EXACT_RANGE_SELECTION_KIND = "exact_range_selection"
_EXACT_RANGE_SELECTION_FORMAT = "pyxis.chromium.research_paragraph_text_selection.v1"
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
    """Persist one 20A working set using the frozen 20B v1 member vocabulary.

    This established writer remains deliberately v1-only. A 49C working set that
    contains a bare 49B exact-range selection still rejects here rather than being
    silently promoted to the v2 format.
    """

    _validate_live_working_set(working_set)
    return _persist_working_set(
        working_set,
        destination,
        working_set_format=_WORKING_SET_FORMAT,
        member_reference=_member_reference,
    )


def persist_chromium_research_working_set_v2(
    working_set: ChromiumPageResearchWorkingSetRecord,
    destination: Path,
) -> ChromiumPageResearchWorkingSetPersistenceEvidence:
    """Persist one 49C working set through the explicit expanded v2 contract.

    v2 adds only the durable exact-range-selection member family. All persistence
    mechanics remain the established 20B canonical/no-overwrite behavior, and no
    individual member sidecar is reread.
    """

    _validate_live_working_set_v2(working_set)
    return _persist_working_set(
        working_set,
        destination,
        working_set_format=_WORKING_SET_FORMAT_V2,
        member_reference=_member_reference_v2,
    )


def _persist_working_set(
    working_set: ChromiumPageResearchWorkingSetRecord,
    destination: Path,
    *,
    working_set_format: str,
    member_reference: Any,
) -> ChromiumPageResearchWorkingSetPersistenceEvidence:
    path = Path(destination).expanduser().resolve()
    if not path.parent.is_dir():
        raise FileNotFoundError(
            f"Research working-set parent directory does not exist: {path.parent}"
        )

    working_set_record = _working_set_record_payload(
        working_set,
        member_reference=member_reference,
    )
    working_set_record_bytes = _canonical_json_bytes(working_set_record)
    working_set_record_sha256 = hashlib.sha256(working_set_record_bytes).hexdigest()
    document = {
        "format": working_set_format,
        "working_set_record": working_set_record,
        "working_set_record_sha256": working_set_record_sha256,
    }
    document_bytes = _canonical_document_bytes(document)

    with path.open("xb") as handle:
        handle.write(document_bytes)

    return ChromiumPageResearchWorkingSetPersistenceEvidence(
        path=path,
        working_set_format=working_set_format,
        working_set_record_sha256=working_set_record_sha256,
        byte_count=len(document_bytes),
        working_set=working_set,
    )


def verify_chromium_research_working_set(
    source: Path,
) -> ChromiumPageResearchWorkingSetVerificationEvidence:
    """Verify canonical bytes for an explicit v1 or v2 working-set sidecar only.

    This operation reads only the working-set file. It does not search for, read,
    verify, or relink any referenced bare selection, note-bearing member, source
    capture, or browser state. Member re-establishment is a separate authority
    boundary.
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
        working_set_format=document["format"],
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


def _validate_live_working_set_v2(
    working_set: ChromiumPageResearchWorkingSetRecord,
) -> None:
    if not isinstance(working_set, ChromiumPageResearchWorkingSetRecord):
        raise TypeError("working_set must be ChromiumPageResearchWorkingSetRecord.")
    if working_set.working_set_mode != _WORKING_SET_MODE:
        raise ValueError("working-set mode is unsupported for durable v2 persistence.")

    rebuilt = create_chromium_research_working_set(working_set.items)
    if rebuilt.working_set_mode != working_set.working_set_mode:
        raise ValueError("working-set mode is incoherent with the established 20A boundary.")

    for index, item in enumerate(working_set.items):
        _member_reference_v2(item, index=index)


def _working_set_record_payload(
    working_set: ChromiumPageResearchWorkingSetRecord,
    *,
    member_reference: Any,
) -> dict[str, Any]:
    return {
        "items": [
            {
                "member_format": reference.member_format,
                "member_kind": reference.member_kind,
                "member_record_sha256": reference.member_record_sha256,
            }
            for index, item in enumerate(working_set.items)
            for reference in (member_reference(item, index=index),)
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


def _member_reference_v2(
    item: object,
    *,
    index: int,
) -> ChromiumPageResearchWorkingSetMemberReference:
    if isinstance(item, ChromiumPageResearchLoadedParagraphTextSelectionRecord):
        return _verification_reference(
            member_kind=_EXACT_RANGE_SELECTION_KIND,
            expected_format=_EXACT_RANGE_SELECTION_FORMAT,
            member_format=item.verification.selection_format,
            member_record_sha256=item.verification.selection_record_sha256,
            index=index,
        )
    return _member_reference(item, index=index)


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
    working_set_format = document["format"]
    if working_set_format not in {_WORKING_SET_FORMAT, _WORKING_SET_FORMAT_V2}:
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
        _validate_persisted_member_reference(
            item,
            index=index,
            working_set_format=working_set_format,
        )

    return working_set_record, recorded_sha256


def _validate_persisted_member_reference(
    item: Any,
    *,
    index: int,
    working_set_format: str,
) -> None:
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
    if working_set_format == _WORKING_SET_FORMAT_V2:
        expected_formats[_EXACT_RANGE_SELECTION_KIND] = _EXACT_RANGE_SELECTION_FORMAT
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
