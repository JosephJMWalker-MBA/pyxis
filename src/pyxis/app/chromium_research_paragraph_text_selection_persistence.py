from __future__ import annotations

from dataclasses import dataclass
import hashlib
import hmac
import json
from pathlib import Path
from typing import Any

from .chromium_research_capture_load import ChromiumPageResearchLoadedCaptureEvidence
from .chromium_research_paragraph_text_selection import (
    ChromiumPageResearchParagraphTextSelectionEvidence,
    select_chromium_research_paragraph_text,
)


_SELECTION_FORMAT = "pyxis.chromium.research_paragraph_text_selection.v1"
_CAPTURE_FORMAT = "pyxis.chromium.research_capture.v1"
_PARAGRAPH_SELECTION_MODE = "caller_explicit_returned_paragraph_ordinal"
_TEXT_SELECTION_MODE = "caller_explicit_returned_paragraph_text_range"
_OFFSET_UNIT = "unicode_code_point"


class ChromiumResearchParagraphTextSelectionIntegrityError(ValueError):
    """Raised when persisted exact-range-selection bytes fail their integrity contract."""


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchParagraphTextSelectionPersistenceEvidence:
    """Durable-file evidence for one exact already-created 18A text range.

    The selection field retains the exact caller-supplied in-memory selection. The
    durable sidecar stores only source capture content identity plus paragraph/range
    coordinates. It does not duplicate selected source text or add note, citation,
    authorship, authenticity, trusted-time, or semantic-support authority.
    """

    path: Path
    selection_format: str
    selection_record_sha256: str
    byte_count: int
    selection: ChromiumPageResearchParagraphTextSelectionEvidence


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchParagraphTextSelectionVerificationEvidence:
    """File-local verification facts for one persisted exact text-range selection.

    Verification proves canonical Pyxis JSON, the recorded SHA-256, and the narrow
    structural/domain shape of the durable reference. It does not reopen a source
    capture, prove the coordinates address source evidence, reconstruct selected text,
    or establish quotation/citation authority.
    """

    path: Path
    selection_format: str
    selection_record_sha256: str
    byte_count: int
    source_capture_format: str
    source_bundle_sha256: str
    paragraph_selection_mode: str
    paragraph_ordinal: int
    text_selection_mode: str
    offset_unit: str
    start_offset: int
    end_offset: int
    document_json: str


def persist_chromium_research_paragraph_text_selection(
    selection: ChromiumPageResearchParagraphTextSelectionEvidence,
    destination: Path,
) -> ChromiumPageResearchParagraphTextSelectionPersistenceEvidence:
    """Persist one exact 18A selection as deterministic no-overwrite JSON.

    The live selection contract is re-established through the existing public 18A
    selector before writing. The temporary validation result is not substituted for
    the caller's object; returned persistence evidence retains the exact supplied
    selection by object identity.

    The sidecar stores no selected text and no source path. Its SHA-256 is self-integrity
    evidence only.
    """

    _validate_live_selection_reference(selection)

    path = Path(destination).expanduser().resolve()
    if not path.parent.is_dir():
        raise FileNotFoundError(
            f"Research exact-range-selection parent directory does not exist: {path.parent}"
        )

    selection_record = _selection_record_payload(selection)
    selection_record_bytes = _canonical_json_bytes(selection_record)
    selection_record_sha256 = hashlib.sha256(selection_record_bytes).hexdigest()
    document = {
        "format": _SELECTION_FORMAT,
        "selection_record": selection_record,
        "selection_record_sha256": selection_record_sha256,
    }
    document_bytes = _canonical_document_bytes(document)

    with path.open("xb") as handle:
        handle.write(document_bytes)

    return ChromiumPageResearchParagraphTextSelectionPersistenceEvidence(
        path=path,
        selection_format=_SELECTION_FORMAT,
        selection_record_sha256=selection_record_sha256,
        byte_count=len(document_bytes),
        selection=selection,
    )


def verify_chromium_research_paragraph_text_selection(
    source: Path,
) -> ChromiumPageResearchParagraphTextSelectionVerificationEvidence:
    """Verify one exact-range-selection sidecar without reading its source capture."""

    path = Path(source).expanduser().resolve()
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ChromiumResearchParagraphTextSelectionIntegrityError(
            "Research exact-range selection is not valid UTF-8."
        ) from exc

    try:
        document = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ChromiumResearchParagraphTextSelectionIntegrityError(
            "Research exact-range selection is not valid JSON."
        ) from exc

    selection_record, recorded_sha256 = _validate_persisted_document(document)
    observed_sha256 = hashlib.sha256(_canonical_json_bytes(selection_record)).hexdigest()
    if not hmac.compare_digest(recorded_sha256, observed_sha256):
        raise ChromiumResearchParagraphTextSelectionIntegrityError(
            "Research exact-range-selection SHA-256 does not match the persisted record."
        )

    canonical_document_bytes = _canonical_document_bytes(document)
    if raw != canonical_document_bytes:
        raise ChromiumResearchParagraphTextSelectionIntegrityError(
            "Research exact-range-selection bytes are not in the canonical Pyxis JSON encoding."
        )

    source_capture = selection_record["source_capture"]
    selection = selection_record["selection"]
    paragraph = selection["paragraph"]
    text_range = selection["text_range"]
    return ChromiumPageResearchParagraphTextSelectionVerificationEvidence(
        path=path,
        selection_format=_SELECTION_FORMAT,
        selection_record_sha256=recorded_sha256,
        byte_count=len(raw),
        source_capture_format=source_capture["format"],
        source_bundle_sha256=source_capture["bundle_sha256"],
        paragraph_selection_mode=paragraph["mode"],
        paragraph_ordinal=paragraph["ordinal"],
        text_selection_mode=text_range["mode"],
        offset_unit=text_range["offset_unit"],
        start_offset=text_range["start_offset"],
        end_offset=text_range["end_offset"],
        document_json=text,
    )


def _validate_live_selection_reference(
    selection: ChromiumPageResearchParagraphTextSelectionEvidence,
) -> None:
    if type(selection) is not ChromiumPageResearchParagraphTextSelectionEvidence:
        raise TypeError(
            "selection must be exactly ChromiumPageResearchParagraphTextSelectionEvidence."
        )

    validated = select_chromium_research_paragraph_text(
        selection.source,
        start_offset=selection.start_offset,
        end_offset=selection.end_offset,
    )
    if (
        validated.selection_mode != selection.selection_mode
        or validated.offset_unit != selection.offset_unit
        or validated.source is not selection.source
        or validated.start_offset != selection.start_offset
        or validated.end_offset != selection.end_offset
    ):
        raise ValueError("Exact-range selection does not match the public 18A selection contract.")

    loaded_capture = selection.source.source
    if not isinstance(loaded_capture, ChromiumPageResearchLoadedCaptureEvidence):
        raise ValueError("Exact-range selection source is not verified loaded-capture evidence.")
    verification = loaded_capture.verification
    if verification.capture_format != _CAPTURE_FORMAT:
        raise ValueError(
            "Source capture format is unsupported for durable exact-range selection."
        )
    if not _is_sha256(verification.bundle_sha256):
        raise ValueError("Source capture bundle SHA-256 has an invalid shape.")


def _selection_record_payload(
    selection: ChromiumPageResearchParagraphTextSelectionEvidence,
) -> dict[str, Any]:
    paragraph_selection = selection.source
    loaded_capture = paragraph_selection.source
    return {
        "selection": {
            "paragraph": {
                "mode": paragraph_selection.selection_mode,
                "ordinal": paragraph_selection.paragraph.ordinal,
            },
            "text_range": {
                "end_offset": selection.end_offset,
                "mode": selection.selection_mode,
                "offset_unit": selection.offset_unit,
                "start_offset": selection.start_offset,
            },
        },
        "source_capture": {
            "bundle_sha256": loaded_capture.verification.bundle_sha256,
            "format": loaded_capture.verification.capture_format,
        },
    }


def _validate_persisted_document(document: Any) -> tuple[dict[str, Any], str]:
    if type(document) is not dict or set(document) != {
        "format",
        "selection_record",
        "selection_record_sha256",
    }:
        raise ChromiumResearchParagraphTextSelectionIntegrityError(
            "Research exact-range-selection document has an invalid top-level shape."
        )
    if document["format"] != _SELECTION_FORMAT:
        raise ChromiumResearchParagraphTextSelectionIntegrityError(
            "Research exact-range-selection format is unsupported."
        )

    recorded_sha256 = document["selection_record_sha256"]
    if not _is_sha256(recorded_sha256):
        raise ChromiumResearchParagraphTextSelectionIntegrityError(
            "Research exact-range-selection SHA-256 has an invalid shape."
        )

    selection_record = document["selection_record"]
    if type(selection_record) is not dict or set(selection_record) != {
        "selection",
        "source_capture",
    }:
        raise ChromiumResearchParagraphTextSelectionIntegrityError(
            "Research exact-range-selection record has an invalid shape."
        )

    source_capture = selection_record["source_capture"]
    if type(source_capture) is not dict or set(source_capture) != {
        "bundle_sha256",
        "format",
    }:
        raise ChromiumResearchParagraphTextSelectionIntegrityError(
            "Research exact-range-selection source-capture reference has an invalid shape."
        )
    if source_capture["format"] != _CAPTURE_FORMAT:
        raise ChromiumResearchParagraphTextSelectionIntegrityError(
            "Research exact-range-selection source capture format is unsupported."
        )
    if not _is_sha256(source_capture["bundle_sha256"]):
        raise ChromiumResearchParagraphTextSelectionIntegrityError(
            "Research exact-range-selection source bundle SHA-256 has an invalid shape."
        )

    selection = selection_record["selection"]
    if type(selection) is not dict or set(selection) != {"paragraph", "text_range"}:
        raise ChromiumResearchParagraphTextSelectionIntegrityError(
            "Research exact-range-selection selection reference has an invalid shape."
        )

    paragraph = selection["paragraph"]
    if type(paragraph) is not dict or set(paragraph) != {"mode", "ordinal"}:
        raise ChromiumResearchParagraphTextSelectionIntegrityError(
            "Research exact-range-selection paragraph reference has an invalid shape."
        )
    if paragraph["mode"] != _PARAGRAPH_SELECTION_MODE:
        raise ChromiumResearchParagraphTextSelectionIntegrityError(
            "Research exact-range-selection paragraph selection mode is unsupported."
        )
    paragraph_ordinal = paragraph["ordinal"]
    if type(paragraph_ordinal) is not int or paragraph_ordinal < 1:
        raise ChromiumResearchParagraphTextSelectionIntegrityError(
            "Research exact-range-selection paragraph ordinal must be a positive integer."
        )

    text_range = selection["text_range"]
    if type(text_range) is not dict or set(text_range) != {
        "end_offset",
        "mode",
        "offset_unit",
        "start_offset",
    }:
        raise ChromiumResearchParagraphTextSelectionIntegrityError(
            "Research exact-range-selection text-range reference has an invalid shape."
        )
    if text_range["mode"] != _TEXT_SELECTION_MODE:
        raise ChromiumResearchParagraphTextSelectionIntegrityError(
            "Research exact-range-selection text selection mode is unsupported."
        )
    if text_range["offset_unit"] != _OFFSET_UNIT:
        raise ChromiumResearchParagraphTextSelectionIntegrityError(
            "Research exact-range-selection offset unit is unsupported."
        )
    start_offset = text_range["start_offset"]
    end_offset = text_range["end_offset"]
    if type(start_offset) is not int or start_offset < 0:
        raise ChromiumResearchParagraphTextSelectionIntegrityError(
            "Research exact-range-selection start offset must be a non-negative integer."
        )
    if type(end_offset) is not int or end_offset <= start_offset:
        raise ChromiumResearchParagraphTextSelectionIntegrityError(
            "Research exact-range-selection end offset must be an integer greater than start offset."
        )

    return selection_record, recorded_sha256


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
            "Research exact-range-selection record is not canonical-JSON serializable."
        ) from exc
    return encoded.encode("utf-8")


def _canonical_document_bytes(document: Any) -> bytes:
    return _canonical_json_bytes(document) + b"\n"


__all__ = [
    "ChromiumPageResearchParagraphTextSelectionPersistenceEvidence",
    "ChromiumPageResearchParagraphTextSelectionVerificationEvidence",
    "ChromiumResearchParagraphTextSelectionIntegrityError",
    "persist_chromium_research_paragraph_text_selection",
    "verify_chromium_research_paragraph_text_selection",
]
