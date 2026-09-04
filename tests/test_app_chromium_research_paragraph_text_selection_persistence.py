from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
import hashlib
import json
from pathlib import Path

import pytest

from pyxis import app as pyxis_app
from pyxis.app.chromium_research_paragraph_text_selection import (
    ChromiumPageResearchParagraphTextSelectionEvidence,
    select_chromium_research_paragraph_text,
)
from pyxis.app.chromium_research_paragraph_text_selection_persistence import (
    ChromiumPageResearchParagraphTextSelectionPersistenceEvidence,
    ChromiumPageResearchParagraphTextSelectionVerificationEvidence,
    ChromiumResearchParagraphTextSelectionIntegrityError,
    persist_chromium_research_paragraph_text_selection,
    verify_chromium_research_paragraph_text_selection,
)
from pyxis.app.chromium_research_passage_selection import (
    select_chromium_research_capture_paragraph,
)
from test_app_chromium_research_paragraph_text_selection_note_persistence import (
    BUNDLE_SHA,
    ENDPOINT,
    TARGET_ID,
    URL,
    _loaded_capture,
)


def _selection(
    *,
    source_path: Path,
    paragraph_text: str = "A😀B café",
    start_offset: int = 1,
    end_offset: int = 4,
    text_character_count: int | None = None,
    text_limit: int = 1024,
    truncated: bool = False,
) -> ChromiumPageResearchParagraphTextSelectionEvidence:
    capture = _loaded_capture(
        path=source_path,
        paragraph_text=paragraph_text,
        text_character_count=text_character_count,
        text_limit=text_limit,
        truncated=truncated,
    )
    paragraph_selection = select_chromium_research_capture_paragraph(
        capture,
        paragraph_ordinal=1,
    )
    return select_chromium_research_paragraph_text(
        paragraph_selection,
        start_offset=start_offset,
        end_offset=end_offset,
    )


def _canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def test_persist_exact_range_selection_writes_minimal_canonical_sidecar_and_retains_selection(
    tmp_path: Path,
) -> None:
    missing_source = tmp_path / "source-capture-does-not-need-to-exist.json"
    selection = _selection(source_path=missing_source)
    destination = tmp_path / "exact-range-selection.json"

    persisted = persist_chromium_research_paragraph_text_selection(
        selection,
        destination,
    )

    assert isinstance(
        persisted,
        ChromiumPageResearchParagraphTextSelectionPersistenceEvidence,
    )
    assert persisted.selection is selection
    assert persisted.path == destination.resolve()
    assert (
        persisted.selection_format
        == "pyxis.chromium.research_paragraph_text_selection.v1"
    )

    raw = destination.read_bytes()
    document = json.loads(raw)
    record = document["selection_record"]
    assert record == {
        "selection": {
            "paragraph": {
                "mode": "caller_explicit_returned_paragraph_ordinal",
                "ordinal": 1,
            },
            "text_range": {
                "end_offset": 4,
                "mode": "caller_explicit_returned_paragraph_text_range",
                "offset_unit": "unicode_code_point",
                "start_offset": 1,
            },
        },
        "source_capture": {
            "bundle_sha256": BUNDLE_SHA,
            "format": "pyxis.chromium.research_capture.v1",
        },
    }
    expected_sha = hashlib.sha256(_canonical_bytes(record)).hexdigest()
    assert (
        document["selection_record_sha256"]
        == expected_sha
        == persisted.selection_record_sha256
    )
    assert raw == _canonical_bytes(document) + b"\n"
    assert persisted.byte_count == len(raw)

    text = raw.decode("utf-8")
    assert URL not in text
    assert ENDPOINT not in text
    assert TARGET_ID not in text
    assert "A😀B café" not in text
    assert "😀B " not in text
    assert '"passage"' not in text
    assert str(missing_source) not in text
    assert "note" not in record
    assert "tag" not in record
    assert "citation" not in record

    with pytest.raises(FrozenInstanceError):
        persisted.byte_count = 0  # type: ignore[misc]


def test_verify_exact_range_selection_reads_only_sidecar_and_preserves_coordinates(
    tmp_path: Path,
) -> None:
    missing_source = tmp_path / "missing-source-capture.json"
    assert not missing_source.exists()
    selection = _selection(source_path=missing_source)
    destination = tmp_path / "exact-range-selection.json"
    persisted = persist_chromium_research_paragraph_text_selection(
        selection,
        destination,
    )

    verified = verify_chromium_research_paragraph_text_selection(destination)

    assert isinstance(
        verified,
        ChromiumPageResearchParagraphTextSelectionVerificationEvidence,
    )
    assert verified.path == destination.resolve()
    assert verified.selection_format == persisted.selection_format
    assert verified.selection_record_sha256 == persisted.selection_record_sha256
    assert verified.byte_count == persisted.byte_count
    assert verified.source_capture_format == "pyxis.chromium.research_capture.v1"
    assert verified.source_bundle_sha256 == BUNDLE_SHA
    assert (
        verified.paragraph_selection_mode
        == "caller_explicit_returned_paragraph_ordinal"
    )
    assert verified.paragraph_ordinal == 1
    assert (
        verified.text_selection_mode
        == "caller_explicit_returned_paragraph_text_range"
    )
    assert verified.offset_unit == "unicode_code_point"
    assert verified.start_offset == 1
    assert verified.end_offset == 4
    assert verified.document_json == destination.read_text(encoding="utf-8")
    assert not missing_source.exists()


def test_persist_exact_range_selection_refuses_overwrite_and_missing_parent(
    tmp_path: Path,
) -> None:
    selection = _selection(source_path=tmp_path / "missing-source.json")
    destination = tmp_path / "exact-range-selection.json"

    persist_chromium_research_paragraph_text_selection(selection, destination)

    with pytest.raises(FileExistsError):
        persist_chromium_research_paragraph_text_selection(selection, destination)
    with pytest.raises(FileNotFoundError, match="parent directory does not exist"):
        persist_chromium_research_paragraph_text_selection(
            selection,
            tmp_path / "missing-parent" / "exact-range-selection.json",
        )


def test_persist_exact_range_selection_reuses_live_range_validation_and_checks_digest(
    tmp_path: Path,
) -> None:
    selection = _selection(
        source_path=tmp_path / "missing-source.json",
        paragraph_text="Alpha",
        start_offset=0,
        end_offset=5,
        text_character_count=10,
        text_limit=5,
        truncated=True,
    )
    forged_range = replace(selection, end_offset=6)

    with pytest.raises(
        ValueError,
        match="outside the bounded returned paragraph text prefix",
    ):
        persist_chromium_research_paragraph_text_selection(
            forged_range,
            tmp_path / "range-selection.json",
        )

    loaded_capture = selection.source.source
    forged_verification = replace(
        loaded_capture.verification,
        bundle_sha256="not-a-sha",
    )
    forged_capture = replace(loaded_capture, verification=forged_verification)
    forged_paragraph_selection = replace(selection.source, source=forged_capture)
    forged_digest_selection = replace(selection, source=forged_paragraph_selection)

    with pytest.raises(ValueError, match="bundle SHA-256 has an invalid shape"):
        persist_chromium_research_paragraph_text_selection(
            forged_digest_selection,
            tmp_path / "digest-selection.json",
        )


def test_persist_exact_range_selection_rejects_wrong_authority_family(
    tmp_path: Path,
) -> None:
    with pytest.raises(
        TypeError,
        match="exactly ChromiumPageResearchParagraphTextSelectionEvidence",
    ):
        persist_chromium_research_paragraph_text_selection(
            object(),  # type: ignore[arg-type]
            tmp_path / "wrong-selection.json",
        )


def test_verify_exact_range_selection_rejects_digest_mismatch_and_noncanonical_bytes(
    tmp_path: Path,
) -> None:
    selection = _selection(source_path=tmp_path / "missing-source.json")
    destination = tmp_path / "exact-range-selection.json"
    persist_chromium_research_paragraph_text_selection(selection, destination)

    document = json.loads(destination.read_text(encoding="utf-8"))
    document["selection_record"]["selection"]["text_range"]["end_offset"] = 5
    destination.write_bytes(_canonical_bytes(document) + b"\n")

    with pytest.raises(
        ChromiumResearchParagraphTextSelectionIntegrityError,
        match="SHA-256",
    ):
        verify_chromium_research_paragraph_text_selection(destination)

    canonical_destination = tmp_path / "canonical-range-selection.json"
    persist_chromium_research_paragraph_text_selection(
        selection,
        canonical_destination,
    )
    canonical_document = json.loads(
        canonical_destination.read_text(encoding="utf-8")
    )
    canonical_destination.write_text(
        json.dumps(canonical_document, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ChromiumResearchParagraphTextSelectionIntegrityError,
        match="canonical",
    ):
        verify_chromium_research_paragraph_text_selection(canonical_destination)


@pytest.mark.parametrize(
    ("mutator", "match"),
    [
        (
            lambda document: document.__setitem__("format", "other-format"),
            "format",
        ),
        (
            lambda document: document["selection_record"]["source_capture"].__setitem__(
                "bundle_sha256",
                "bad",
            ),
            "bundle SHA-256",
        ),
        (
            lambda document: document["selection_record"]["selection"][
                "paragraph"
            ].__setitem__("mode", "other-mode"),
            "paragraph selection mode",
        ),
        (
            lambda document: document["selection_record"]["selection"][
                "text_range"
            ].__setitem__("mode", "other-mode"),
            "text selection mode",
        ),
        (
            lambda document: document["selection_record"]["selection"][
                "text_range"
            ].__setitem__("offset_unit", "utf16-code-unit"),
            "offset unit",
        ),
        (
            lambda document: document["selection_record"]["selection"][
                "text_range"
            ].__setitem__("start_offset", -1),
            "start offset",
        ),
        (
            lambda document: document["selection_record"]["selection"][
                "paragraph"
            ].__setitem__("ordinal", 0),
            "paragraph ordinal",
        ),
        (
            lambda document: document["selection_record"]["selection"][
                "text_range"
            ].__setitem__("end_offset", 1),
            "end offset",
        ),
        (
            lambda document: document["selection_record"][
                "source_capture"
            ].__setitem__("format", "other-capture-format"),
            "source capture format",
        ),
    ],
)
def test_verify_exact_range_selection_rejects_malformed_domain_fields(
    tmp_path: Path,
    mutator,
    match: str,
) -> None:
    selection = _selection(source_path=tmp_path / "missing-source.json")
    destination = tmp_path / f"malformed-{match.replace(' ', '-')}.json"
    persist_chromium_research_paragraph_text_selection(selection, destination)

    document = json.loads(destination.read_text(encoding="utf-8"))
    mutator(document)
    record = document["selection_record"]
    document["selection_record_sha256"] = hashlib.sha256(
        _canonical_bytes(record)
    ).hexdigest()
    destination.write_bytes(_canonical_bytes(document) + b"\n")

    with pytest.raises(
        ChromiumResearchParagraphTextSelectionIntegrityError,
        match=match,
    ):
        verify_chromium_research_paragraph_text_selection(destination)


def test_recomputed_digest_is_self_integrity_not_source_range_authentication(
    tmp_path: Path,
) -> None:
    selection = _selection(source_path=tmp_path / "missing-source.json")
    destination = tmp_path / "exact-range-selection.json"
    persist_chromium_research_paragraph_text_selection(selection, destination)

    document = json.loads(destination.read_text(encoding="utf-8"))
    record = document["selection_record"]
    record["selection"]["text_range"]["end_offset"] = 999
    document["selection_record_sha256"] = hashlib.sha256(
        _canonical_bytes(record)
    ).hexdigest()
    destination.write_bytes(_canonical_bytes(document) + b"\n")

    verified = verify_chromium_research_paragraph_text_selection(destination)

    assert verified.end_offset == 999
    assert verified.selection_record_sha256 == document["selection_record_sha256"]


def test_public_app_exports_persist_and_verify_exact_range_selection(
    tmp_path: Path,
) -> None:
    selection = _selection(source_path=tmp_path / "missing-source.json")
    destination = tmp_path / "exact-range-selection.json"

    persisted = pyxis_app.persist_chromium_research_paragraph_text_selection(
        selection,
        destination,
    )
    verified = pyxis_app.verify_chromium_research_paragraph_text_selection(
        destination,
    )

    assert isinstance(
        persisted,
        pyxis_app.ChromiumPageResearchParagraphTextSelectionPersistenceEvidence,
    )
    assert isinstance(
        verified,
        pyxis_app.ChromiumPageResearchParagraphTextSelectionVerificationEvidence,
    )
    assert persisted.selection is selection
    assert verified.start_offset == selection.start_offset
    assert verified.end_offset == selection.end_offset
