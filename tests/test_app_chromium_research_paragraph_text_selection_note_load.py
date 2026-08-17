from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
import hashlib
import json
from pathlib import Path

import pytest

from pyxis import app as pyxis_app
from pyxis.app.chromium_headings import ChromiumPageHeadingsEvidence
from pyxis.app.chromium_lists import ChromiumPageListsEvidence
from pyxis.app.chromium_metadata import ChromiumPageMetadataEvidence
from pyxis.app.chromium_observation import (
    ChromiumPageContentEvidence,
    ChromiumPageLinksEvidence,
    ChromiumPageObservationEvidence,
)
from pyxis.app.chromium_paragraphs import (
    ChromiumPageParagraphEvidence,
    ChromiumPageParagraphsEvidence,
)
from pyxis.app.chromium_research_bundle import ChromiumPageResearchEvidenceBundle
from pyxis.app.chromium_research_capture import ChromiumPageResearchCaptureVerificationEvidence
from pyxis.app.chromium_research_capture_load import ChromiumPageResearchLoadedCaptureEvidence
from pyxis.app.chromium_research_paragraph_text_selection import (
    select_chromium_research_paragraph_text,
)
from pyxis.app.chromium_research_paragraph_text_selection_note import (
    create_chromium_research_paragraph_text_selection_note,
)
from pyxis.app.chromium_research_paragraph_text_selection_note_load import (
    ChromiumPageResearchLoadedParagraphTextSelectionNoteRecord,
    ChromiumResearchParagraphTextSelectionNoteSourceMismatchError,
    load_chromium_research_paragraph_text_selection_note,
)
from pyxis.app.chromium_research_paragraph_text_selection_note_persistence import (
    ChromiumResearchParagraphTextSelectionNoteIntegrityError,
    persist_chromium_research_paragraph_text_selection_note,
    verify_chromium_research_paragraph_text_selection_note,
)
from pyxis.app.chromium_research_passage_selection import (
    select_chromium_research_capture_paragraph,
)
from pyxis.app.chromium_tables import ChromiumPageTablesEvidence


ENDPOINT = "http://127.0.0.1:9222"
TARGET_ID = "page-1"
URL = "https://example.test/research"
ORDER = (
    "page",
    "links",
    "headings",
    "metadata",
    "paragraphs",
    "tables",
    "lists",
)
BUNDLE_SHA = "a" * 64


def _loaded_capture(
    *,
    path: Path,
    bundle_sha256: str = BUNDLE_SHA,
) -> ChromiumPageResearchLoadedCaptureEvidence:
    page = ChromiumPageObservationEvidence(
        endpoint=ENDPOINT,
        target_id=TARGET_ID,
        url=URL,
        title="Research page",
        content=ChromiumPageContentEvidence(
            source="document.body.innerText",
            text_prefix="A😀B café\nSecond paragraph",
            text_character_count=25,
            text_limit=2048,
            truncated=False,
        ),
    )
    links = ChromiumPageLinksEvidence(
        endpoint=ENDPOINT,
        target_id=TARGET_ID,
        url=URL,
        source="document.querySelectorAll('a[href]')",
        links=(),
        link_count=0,
        link_limit=64,
        truncated=False,
    )
    headings = ChromiumPageHeadingsEvidence(
        endpoint=ENDPOINT,
        target_id=TARGET_ID,
        url=URL,
        source="document.querySelectorAll('h1,h2,h3,h4,h5,h6')",
        headings=(),
        heading_count=0,
        heading_limit=64,
        truncated=False,
    )
    metadata = ChromiumPageMetadataEvidence(
        endpoint=ENDPOINT,
        target_id=TARGET_ID,
        url=URL,
        document_language="en",
        language_source="document.documentElement.getAttribute('lang')",
        canonical_source='document.querySelectorAll("link[rel~=\'canonical\' i][href]")',
        canonical_links=(),
        canonical_link_count=0,
        canonical_link_limit=8,
        canonical_links_truncated=False,
        description_source='document.querySelectorAll("meta[name=\'description\' i]")',
        descriptions=(),
        description_count=0,
        description_limit=8,
        descriptions_truncated=False,
    )
    paragraphs = ChromiumPageParagraphsEvidence(
        endpoint=ENDPOINT,
        target_id=TARGET_ID,
        url=URL,
        source="document.querySelectorAll('p')",
        paragraphs=(
            ChromiumPageParagraphEvidence(
                ordinal=1,
                element_id="passage",
                text_prefix="A😀B café",
                text_character_count=8,
                text_limit=1024,
                truncated=False,
            ),
            ChromiumPageParagraphEvidence(
                ordinal=2,
                element_id="passage",
                text_prefix="Second paragraph",
                text_character_count=16,
                text_limit=1024,
                truncated=False,
            ),
        ),
        paragraph_count=2,
        paragraph_limit=128,
        truncated=False,
    )
    tables = ChromiumPageTablesEvidence(
        endpoint=ENDPOINT,
        target_id=TARGET_ID,
        url=URL,
        source="document.querySelectorAll('table')",
        tables=(),
        table_count=0,
        table_limit=32,
        truncated=False,
    )
    lists = ChromiumPageListsEvidence(
        endpoint=ENDPOINT,
        target_id=TARGET_ID,
        url=URL,
        source="document.querySelectorAll('ol,ul')",
        lists=(),
        list_count=0,
        list_limit=64,
        truncated=False,
    )
    bundle = ChromiumPageResearchEvidenceBundle(
        endpoint=ENDPOINT,
        target_id=TARGET_ID,
        url=URL,
        acquisition_mode="sequential_non_atomic_url_coherent",
        acquisition_order=ORDER,
        page=page,
        links=links,
        headings=headings,
        metadata=metadata,
        paragraphs=paragraphs,
        tables=tables,
        lists=lists,
    )
    verification = ChromiumPageResearchCaptureVerificationEvidence(
        path=path,
        capture_format="pyxis.chromium.research_capture.v1",
        bundle_sha256=bundle_sha256,
        byte_count=1,
        endpoint=ENDPOINT,
        target_id=TARGET_ID,
        url=URL,
        acquisition_mode="sequential_non_atomic_url_coherent",
        acquisition_order=ORDER,
        document_json="{}\n",
    )
    return ChromiumPageResearchLoadedCaptureEvidence(
        verification=verification,
        bundle=bundle,
    )


def _persist_note(
    source: ChromiumPageResearchLoadedCaptureEvidence,
    destination: Path,
    *,
    paragraph_ordinal: int = 1,
    start_offset: int = 1,
    end_offset: int = 4,
) -> str:
    paragraph_selection = select_chromium_research_capture_paragraph(
        source,
        paragraph_ordinal=paragraph_ordinal,
    )
    text_selection = select_chromium_research_paragraph_text(
        paragraph_selection,
        start_offset=start_offset,
        end_offset=end_offset,
    )
    note_text = "  Human interpretation 😀\nKeep this exact.  "
    note = create_chromium_research_paragraph_text_selection_note(
        text_selection,
        note_text=note_text,
    )
    persist_chromium_research_paragraph_text_selection_note(note, destination)
    return note_text


def _canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def test_load_exact_range_note_relinks_to_exact_supplied_source_and_range(
    tmp_path: Path,
) -> None:
    missing_capture_path = tmp_path / "source-capture-does-not-need-to-exist.json"
    source = _loaded_capture(path=missing_capture_path)
    note_path = tmp_path / "exact-range-note.json"
    note_text = _persist_note(source, note_path)

    loaded = load_chromium_research_paragraph_text_selection_note(source, note_path)

    assert isinstance(loaded, ChromiumPageResearchLoadedParagraphTextSelectionNoteRecord)
    assert loaded.verification.path == note_path.resolve()
    assert loaded.verification.source_bundle_sha256 == BUNDLE_SHA
    assert loaded.verification.paragraph_ordinal == 1
    assert loaded.verification.start_offset == 1
    assert loaded.verification.end_offset == 4
    assert loaded.note.note_text == note_text
    assert loaded.note.selection.selected_text == "😀B "
    assert loaded.note.selection.source.source is source
    assert loaded.note.selection.source.paragraph is source.bundle.paragraphs.paragraphs[0]
    assert not missing_capture_path.exists()

    with pytest.raises(FrozenInstanceError):
        loaded.note = loaded.note  # type: ignore[misc]


def test_load_exact_range_note_uses_content_identity_not_source_path(tmp_path: Path) -> None:
    original = _loaded_capture(path=tmp_path / "original-capture.json")
    note_path = tmp_path / "exact-range-note.json"
    _persist_note(original, note_path)

    same_content_elsewhere = replace(
        original,
        verification=replace(
            original.verification,
            path=tmp_path / "different-location.json",
        ),
    )

    loaded = load_chromium_research_paragraph_text_selection_note(
        same_content_elsewhere,
        note_path,
    )

    assert loaded.note.selection.source.source is same_content_elsewhere
    assert loaded.note.selection.source.paragraph is same_content_elsewhere.bundle.paragraphs.paragraphs[0]
    assert loaded.note.selection.selected_text == "😀B "


def test_load_exact_range_note_rejects_different_capture_or_unsupported_source(
    tmp_path: Path,
) -> None:
    source = _loaded_capture(path=tmp_path / "source-capture.json")
    note_path = tmp_path / "exact-range-note.json"
    _persist_note(source, note_path)

    different_source = _loaded_capture(
        path=tmp_path / "different-capture.json",
        bundle_sha256="b" * 64,
    )
    with pytest.raises(
        ChromiumResearchParagraphTextSelectionNoteSourceMismatchError,
        match="different capture bundle",
    ):
        load_chromium_research_paragraph_text_selection_note(different_source, note_path)

    unsupported_source = replace(
        source,
        verification=replace(source.verification, capture_format="other.capture.v1"),
    )
    with pytest.raises(
        ChromiumResearchParagraphTextSelectionNoteSourceMismatchError,
        match="source capture format is unsupported",
    ):
        load_chromium_research_paragraph_text_selection_note(unsupported_source, note_path)


def test_load_exact_range_note_reverifies_sidecar_before_relink(tmp_path: Path) -> None:
    source = _loaded_capture(path=tmp_path / "source-capture.json")
    note_path = tmp_path / "exact-range-note.json"
    _persist_note(source, note_path)

    document = json.loads(note_path.read_text(encoding="utf-8"))
    document["note_record"]["note"]["text"] = "Tampered without digest update"
    note_path.write_bytes(_canonical_bytes(document) + b"\n")

    with pytest.raises(
        ChromiumResearchParagraphTextSelectionNoteIntegrityError,
        match="SHA-256",
    ):
        load_chromium_research_paragraph_text_selection_note(source, note_path)


def test_load_rejects_file_valid_coordinate_that_does_not_address_source(
    tmp_path: Path,
) -> None:
    source = _loaded_capture(path=tmp_path / "source-capture.json")
    note_path = tmp_path / "exact-range-note.json"
    _persist_note(source, note_path)

    document = json.loads(note_path.read_text(encoding="utf-8"))
    record = document["note_record"]
    record["selection"]["text_range"]["end_offset"] = 999
    document["note_record_sha256"] = hashlib.sha256(_canonical_bytes(record)).hexdigest()
    note_path.write_bytes(_canonical_bytes(document) + b"\n")

    verification = verify_chromium_research_paragraph_text_selection_note(note_path)
    assert verification.end_offset == 999

    with pytest.raises(ValueError, match="outside returned paragraph text evidence"):
        load_chromium_research_paragraph_text_selection_note(source, note_path)


def test_load_exact_range_note_does_not_expand_bounded_paragraph_prefix(
    tmp_path: Path,
) -> None:
    complete_source = _loaded_capture(path=tmp_path / "complete-capture.json")
    note_path = tmp_path / "exact-range-note.json"
    _persist_note(
        complete_source,
        note_path,
        paragraph_ordinal=2,
        start_offset=0,
        end_offset=6,
    )

    paragraphs = complete_source.bundle.paragraphs
    bounded_paragraphs = replace(
        paragraphs,
        paragraphs=(paragraphs.paragraphs[0],),
        paragraph_count=2,
        truncated=True,
    )
    bounded_source = replace(
        complete_source,
        verification=replace(
            complete_source.verification,
            path=tmp_path / "bounded-capture.json",
        ),
        bundle=replace(complete_source.bundle, paragraphs=bounded_paragraphs),
    )

    with pytest.raises(ValueError, match="bounded returned paragraph prefix"):
        load_chromium_research_paragraph_text_selection_note(bounded_source, note_path)


def test_public_app_exports_exact_range_note_loader(tmp_path: Path) -> None:
    source = _loaded_capture(path=tmp_path / "source-capture.json")
    note_path = tmp_path / "exact-range-note.json"
    _persist_note(source, note_path)

    loaded = pyxis_app.load_chromium_research_paragraph_text_selection_note(
        source,
        note_path,
    )

    assert isinstance(
        loaded,
        pyxis_app.ChromiumPageResearchLoadedParagraphTextSelectionNoteRecord,
    )
    assert loaded.note.selection.selected_text == "😀B "
