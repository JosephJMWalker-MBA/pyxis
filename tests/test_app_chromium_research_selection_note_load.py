from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
import json
from pathlib import Path

import pytest

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
from pyxis.app.chromium_research_passage_selection import select_chromium_research_capture_paragraph
from pyxis.app.chromium_research_selection_note import create_chromium_research_paragraph_note
from pyxis.app.chromium_research_selection_note_load import (
    ChromiumPageResearchLoadedParagraphNoteRecord,
    ChromiumResearchParagraphNoteSourceMismatchError,
    load_chromium_research_paragraph_note,
)
from pyxis.app.chromium_research_selection_note_persistence import (
    ChromiumResearchParagraphNoteIntegrityError,
    persist_chromium_research_paragraph_note,
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
            text_prefix="Alpha Beta",
            text_character_count=10,
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
                text_prefix="Alpha",
                text_character_count=5,
                text_limit=1024,
                truncated=False,
            ),
            ChromiumPageParagraphEvidence(
                ordinal=2,
                element_id="passage",
                text_prefix="Beta",
                text_character_count=4,
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


def _persist_note(source: ChromiumPageResearchLoadedCaptureEvidence, destination: Path) -> str:
    selection = select_chromium_research_capture_paragraph(source, paragraph_ordinal=2)
    text = "  Human interpretation 😀\nKeep this exact.  "
    note = create_chromium_research_paragraph_note(selection, note_text=text)
    persist_chromium_research_paragraph_note(note, destination)
    return text


def test_load_relinks_verified_sidecar_to_exact_supplied_capture_and_paragraph(
    tmp_path: Path,
) -> None:
    missing_capture_path = tmp_path / "source-capture-does-not-need-to-exist.json"
    source = _loaded_capture(path=missing_capture_path)
    note_path = tmp_path / "research-note.json"
    text = _persist_note(source, note_path)

    loaded = load_chromium_research_paragraph_note(source, note_path)

    assert isinstance(loaded, ChromiumPageResearchLoadedParagraphNoteRecord)
    assert loaded.verification.path == note_path.resolve()
    assert loaded.verification.source_bundle_sha256 == BUNDLE_SHA
    assert loaded.verification.paragraph_ordinal == 2
    assert loaded.note.note_text == text
    assert loaded.note.selection.source is source
    assert loaded.note.selection.paragraph is source.bundle.paragraphs.paragraphs[1]
    assert not missing_capture_path.exists()

    with pytest.raises(FrozenInstanceError):
        loaded.note = loaded.note  # type: ignore[misc]


def test_load_uses_content_identity_not_capture_path_identity(tmp_path: Path) -> None:
    original_source = _loaded_capture(path=tmp_path / "original-capture.json")
    note_path = tmp_path / "research-note.json"
    _persist_note(original_source, note_path)

    same_content_elsewhere = replace(
        original_source,
        verification=replace(
            original_source.verification,
            path=tmp_path / "different-location.json",
        ),
    )

    loaded = load_chromium_research_paragraph_note(same_content_elsewhere, note_path)

    assert loaded.note.selection.source is same_content_elsewhere
    assert loaded.note.selection.paragraph is same_content_elsewhere.bundle.paragraphs.paragraphs[1]
    assert loaded.verification.source_bundle_sha256 == same_content_elsewhere.verification.bundle_sha256


def test_load_rejects_verified_note_that_references_different_capture_bundle(
    tmp_path: Path,
) -> None:
    original_source = _loaded_capture(path=tmp_path / "original-capture.json")
    note_path = tmp_path / "research-note.json"
    _persist_note(original_source, note_path)

    different_source = _loaded_capture(
        path=tmp_path / "different-capture.json",
        bundle_sha256="b" * 64,
    )

    with pytest.raises(
        ChromiumResearchParagraphNoteSourceMismatchError,
        match="different capture bundle",
    ):
        load_chromium_research_paragraph_note(different_source, note_path)


def test_load_reverifies_sidecar_instead_of_trusting_file_shape(tmp_path: Path) -> None:
    source = _loaded_capture(path=tmp_path / "source-capture.json")
    note_path = tmp_path / "research-note.json"
    _persist_note(source, note_path)

    document = json.loads(note_path.read_text(encoding="utf-8"))
    document["note_record"]["note"]["text"] = "Tampered without digest update"
    note_path.write_text(
        json.dumps(
            document,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
        + "\n",
        encoding="utf-8",
    )

    with pytest.raises(ChromiumResearchParagraphNoteIntegrityError, match="SHA-256"):
        load_chromium_research_paragraph_note(source, note_path)


def test_load_does_not_expand_bounded_paragraph_evidence_during_relink(tmp_path: Path) -> None:
    complete_source = _loaded_capture(path=tmp_path / "complete-capture.json")
    note_path = tmp_path / "research-note.json"
    _persist_note(complete_source, note_path)

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
        load_chromium_research_paragraph_note(bounded_source, note_path)


def test_load_rejects_unsupported_supplied_capture_format_before_reconstruction(
    tmp_path: Path,
) -> None:
    source = _loaded_capture(path=tmp_path / "source-capture.json")
    note_path = tmp_path / "research-note.json"
    _persist_note(source, note_path)
    unsupported_source = replace(
        source,
        verification=replace(source.verification, capture_format="other.capture.v1"),
    )

    with pytest.raises(
        ChromiumResearchParagraphNoteSourceMismatchError,
        match="source capture format is unsupported",
    ):
        load_chromium_research_paragraph_note(unsupported_source, note_path)
