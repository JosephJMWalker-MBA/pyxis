from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
import hashlib
import json
from pathlib import Path

import pytest

from pyxis import app as pyxis_app
from pyxis.app.chromium_research_paragraph_text_selection import (
    select_chromium_research_paragraph_text,
)
from pyxis.app.chromium_research_paragraph_text_selection_load import (
    ChromiumPageResearchLoadedParagraphTextSelectionRecord,
    ChromiumResearchParagraphTextSelectionSourceMismatchError,
    load_chromium_research_paragraph_text_selection,
)
from pyxis.app.chromium_research_paragraph_text_selection_persistence import (
    ChromiumResearchParagraphTextSelectionIntegrityError,
    persist_chromium_research_paragraph_text_selection,
    verify_chromium_research_paragraph_text_selection,
)
from pyxis.app.chromium_research_passage_selection import (
    select_chromium_research_capture_paragraph,
)
from test_app_chromium_research_paragraph_text_selection_note_load import (
    BUNDLE_SHA,
    _loaded_capture,
)


def _canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def _persist_selection(
    source,
    destination: Path,
    *,
    paragraph_ordinal: int = 1,
    start_offset: int = 1,
    end_offset: int = 4,
):
    paragraph = select_chromium_research_capture_paragraph(
        source,
        paragraph_ordinal=paragraph_ordinal,
    )
    selection = select_chromium_research_paragraph_text(
        paragraph,
        start_offset=start_offset,
        end_offset=end_offset,
    )
    return persist_chromium_research_paragraph_text_selection(
        selection,
        destination,
    )


def test_49b_relinks_verified_selection_to_exact_supplied_capture(
    tmp_path: Path,
) -> None:
    source = _loaded_capture(path=tmp_path / "missing-source-capture.json")
    assert not source.verification.path.exists()
    selection_path = tmp_path / "selection.json"
    persisted = _persist_selection(source, selection_path)

    loaded = load_chromium_research_paragraph_text_selection(
        source,
        selection_path,
    )

    assert isinstance(
        loaded,
        ChromiumPageResearchLoadedParagraphTextSelectionRecord,
    )
    assert loaded.verification.path == selection_path.resolve()
    assert (
        loaded.verification.selection_record_sha256
        == persisted.selection_record_sha256
    )
    assert loaded.selection.source.source is source
    assert (
        loaded.selection.source.paragraph
        is source.bundle.paragraphs.paragraphs[0]
    )
    assert loaded.selection.start_offset == 1
    assert loaded.selection.end_offset == 4
    assert loaded.selection.selected_text == "😀B "
    assert not source.verification.path.exists()

    with pytest.raises(FrozenInstanceError):
        loaded.selection = persisted.selection  # type: ignore[misc]


def test_49b_source_path_is_not_identity_and_same_content_elsewhere_can_relink(
    tmp_path: Path,
) -> None:
    original = _loaded_capture(path=tmp_path / "original-missing.json")
    selection_path = tmp_path / "selection.json"
    _persist_selection(original, selection_path)

    same_content_elsewhere = _loaded_capture(
        path=tmp_path / "elsewhere-missing.json",
        bundle_sha256=BUNDLE_SHA,
    )
    assert same_content_elsewhere.verification.path != original.verification.path
    assert not same_content_elsewhere.verification.path.exists()

    loaded = load_chromium_research_paragraph_text_selection(
        same_content_elsewhere,
        selection_path,
    )

    assert loaded.selection.source.source is same_content_elsewhere
    assert loaded.selection.source.source is not original
    assert loaded.selection.selected_text == "😀B "


def test_49b_rejects_wrong_source_authority_family(tmp_path: Path) -> None:
    source = _loaded_capture(path=tmp_path / "source.json")
    selection_path = tmp_path / "selection.json"
    _persist_selection(source, selection_path)

    with pytest.raises(
        TypeError,
        match="source must be ChromiumPageResearchLoadedCaptureEvidence",
    ):
        load_chromium_research_paragraph_text_selection(
            object(),  # type: ignore[arg-type]
            selection_path,
        )


def test_49b_rejects_malformed_or_different_supplied_capture_identity(
    tmp_path: Path,
) -> None:
    source = _loaded_capture(path=tmp_path / "source.json")
    selection_path = tmp_path / "selection.json"
    _persist_selection(source, selection_path)

    malformed = replace(
        source,
        verification=replace(source.verification, bundle_sha256="not-a-sha"),
    )
    with pytest.raises(
        ChromiumResearchParagraphTextSelectionSourceMismatchError,
        match="bundle SHA-256 has an invalid shape",
    ):
        load_chromium_research_paragraph_text_selection(
            malformed,
            selection_path,
        )

    different = _loaded_capture(
        path=tmp_path / "different.json",
        bundle_sha256="b" * 64,
    )
    with pytest.raises(
        ChromiumResearchParagraphTextSelectionSourceMismatchError,
        match="different capture bundle",
    ):
        load_chromium_research_paragraph_text_selection(
            different,
            selection_path,
        )

    unsupported = replace(
        source,
        verification=replace(
            source.verification,
            capture_format="other.capture.v1",
        ),
    )
    with pytest.raises(
        ChromiumResearchParagraphTextSelectionSourceMismatchError,
        match="source capture format is unsupported",
    ):
        load_chromium_research_paragraph_text_selection(
            unsupported,
            selection_path,
        )


def test_49b_freshly_reverifies_sidecar_before_source_attachment(
    tmp_path: Path,
) -> None:
    source = _loaded_capture(path=tmp_path / "source.json")
    selection_path = tmp_path / "selection.json"
    _persist_selection(source, selection_path)

    document = json.loads(selection_path.read_text(encoding="utf-8"))
    document["selection_record"]["selection"]["text_range"]["end_offset"] = 5
    selection_path.write_bytes(_canonical_bytes(document) + b"\n")

    with pytest.raises(
        ChromiumResearchParagraphTextSelectionIntegrityError,
        match="SHA-256",
    ):
        load_chromium_research_paragraph_text_selection(
            source,
            selection_path,
        )


def test_49b_file_valid_out_of_source_coordinate_fails_during_18a_reconstruction(
    tmp_path: Path,
) -> None:
    source = _loaded_capture(path=tmp_path / "source.json")
    selection_path = tmp_path / "selection.json"
    _persist_selection(source, selection_path)

    document = json.loads(selection_path.read_text(encoding="utf-8"))
    record = document["selection_record"]
    record["selection"]["text_range"]["end_offset"] = 999
    document["selection_record_sha256"] = hashlib.sha256(
        _canonical_bytes(record)
    ).hexdigest()
    selection_path.write_bytes(_canonical_bytes(document) + b"\n")

    verified = verify_chromium_research_paragraph_text_selection(selection_path)
    assert verified.end_offset == 999

    with pytest.raises(
        ValueError,
        match="outside returned paragraph text evidence",
    ):
        load_chromium_research_paragraph_text_selection(
            source,
            selection_path,
        )


def test_49b_file_valid_unknown_paragraph_ordinal_fails_against_supplied_capture(
    tmp_path: Path,
) -> None:
    source = _loaded_capture(path=tmp_path / "source.json")
    selection_path = tmp_path / "selection.json"
    _persist_selection(source, selection_path)

    document = json.loads(selection_path.read_text(encoding="utf-8"))
    record = document["selection_record"]
    record["selection"]["paragraph"]["ordinal"] = 3
    document["selection_record_sha256"] = hashlib.sha256(
        _canonical_bytes(record)
    ).hexdigest()
    selection_path.write_bytes(_canonical_bytes(document) + b"\n")

    verified = verify_chromium_research_paragraph_text_selection(selection_path)
    assert verified.paragraph_ordinal == 3

    with pytest.raises(
        ValueError,
        match="does not identify an observed paragraph",
    ):
        load_chromium_research_paragraph_text_selection(
            source,
            selection_path,
        )


def test_49b_does_not_expand_bounded_returned_paragraph_prefix(
    tmp_path: Path,
) -> None:
    complete = _loaded_capture(path=tmp_path / "complete.json")
    selection_path = tmp_path / "selection.json"
    _persist_selection(
        complete,
        selection_path,
        paragraph_ordinal=2,
        start_offset=0,
        end_offset=6,
    )

    paragraphs = complete.bundle.paragraphs
    bounded_paragraphs = replace(
        paragraphs,
        paragraphs=(paragraphs.paragraphs[0],),
        paragraph_count=2,
        truncated=True,
    )
    bounded = replace(
        complete,
        verification=replace(
            complete.verification,
            path=tmp_path / "bounded-missing.json",
        ),
        bundle=replace(
            complete.bundle,
            paragraphs=bounded_paragraphs,
        ),
    )

    with pytest.raises(
        ValueError,
        match="bounded returned paragraph prefix",
    ):
        load_chromium_research_paragraph_text_selection(
            bounded,
            selection_path,
        )


def test_49b_unsupported_persisted_selector_mode_fails_in_fresh_49a_verification(
    tmp_path: Path,
) -> None:
    source = _loaded_capture(path=tmp_path / "source.json")
    selection_path = tmp_path / "selection.json"
    _persist_selection(source, selection_path)

    document = json.loads(selection_path.read_text(encoding="utf-8"))
    record = document["selection_record"]
    record["selection"]["text_range"]["mode"] = "other-mode"
    document["selection_record_sha256"] = hashlib.sha256(
        _canonical_bytes(record)
    ).hexdigest()
    selection_path.write_bytes(_canonical_bytes(document) + b"\n")

    with pytest.raises(
        ChromiumResearchParagraphTextSelectionIntegrityError,
        match="text selection mode",
    ):
        load_chromium_research_paragraph_text_selection(
            source,
            selection_path,
        )


def test_public_app_exports_49b_exact_range_selection_loader(
    tmp_path: Path,
) -> None:
    source = _loaded_capture(path=tmp_path / "source.json")
    selection_path = tmp_path / "selection.json"
    _persist_selection(source, selection_path)

    loaded = pyxis_app.load_chromium_research_paragraph_text_selection(
        source,
        selection_path,
    )

    assert isinstance(
        loaded,
        pyxis_app.ChromiumPageResearchLoadedParagraphTextSelectionRecord,
    )
    assert isinstance(
        loaded.verification,
        pyxis_app.ChromiumPageResearchParagraphTextSelectionVerificationEvidence,
    )
    assert loaded.selection.source.source is source
    assert loaded.selection.selected_text == "😀B "
