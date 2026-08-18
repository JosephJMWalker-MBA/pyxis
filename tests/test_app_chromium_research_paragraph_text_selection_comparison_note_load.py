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
from pyxis.app.chromium_research_paragraph_text_selection_comparison import (
    create_chromium_research_paragraph_text_selection_comparison,
)
from pyxis.app.chromium_research_paragraph_text_selection_comparison_note import (
    create_chromium_research_paragraph_text_selection_comparison_note,
)
from pyxis.app.chromium_research_paragraph_text_selection_comparison_note_load import (
    ChromiumPageResearchLoadedParagraphTextSelectionComparisonNoteRecord,
    ChromiumResearchParagraphTextSelectionComparisonNoteSourceMismatchError,
    load_chromium_research_paragraph_text_selection_comparison_note,
)
from pyxis.app.chromium_research_paragraph_text_selection_comparison_note_persistence import (
    ChromiumResearchParagraphTextSelectionComparisonNoteIntegrityError,
    persist_chromium_research_paragraph_text_selection_comparison_note,
    verify_chromium_research_paragraph_text_selection_comparison_note,
)
from pyxis.app.chromium_research_passage_selection import (
    select_chromium_research_capture_paragraph,
)
from pyxis.app.chromium_tables import ChromiumPageTablesEvidence


ENDPOINT = "http://127.0.0.1:9222"
ORDER = ("page", "links", "headings", "metadata", "paragraphs", "tables", "lists")


def _loaded_capture(
    *,
    target_id: str,
    url: str,
    digest_character: str,
    paragraph_text: str,
    path: Path,
) -> ChromiumPageResearchLoadedCaptureEvidence:
    page = ChromiumPageObservationEvidence(
        endpoint=ENDPOINT,
        target_id=target_id,
        url=url,
        title="Research page",
        content=ChromiumPageContentEvidence(
            source="document.body.innerText",
            text_prefix=paragraph_text,
            text_character_count=len(paragraph_text),
            text_limit=2048,
            truncated=False,
        ),
    )
    links = ChromiumPageLinksEvidence(
        endpoint=ENDPOINT,
        target_id=target_id,
        url=url,
        source="document.querySelectorAll('a[href]')",
        links=(),
        link_count=0,
        link_limit=64,
        truncated=False,
    )
    headings = ChromiumPageHeadingsEvidence(
        endpoint=ENDPOINT,
        target_id=target_id,
        url=url,
        source="document.querySelectorAll('h1,h2,h3,h4,h5,h6')",
        headings=(),
        heading_count=0,
        heading_limit=64,
        truncated=False,
    )
    metadata = ChromiumPageMetadataEvidence(
        endpoint=ENDPOINT,
        target_id=target_id,
        url=url,
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
    paragraph = ChromiumPageParagraphEvidence(
        ordinal=1,
        element_id="passage",
        text_prefix=paragraph_text,
        text_character_count=len(paragraph_text),
        text_limit=1024,
        truncated=False,
    )
    paragraphs = ChromiumPageParagraphsEvidence(
        endpoint=ENDPOINT,
        target_id=target_id,
        url=url,
        source="document.querySelectorAll('p')",
        paragraphs=(paragraph,),
        paragraph_count=1,
        paragraph_limit=128,
        truncated=False,
    )
    tables = ChromiumPageTablesEvidence(
        endpoint=ENDPOINT,
        target_id=target_id,
        url=url,
        source="document.querySelectorAll('table')",
        tables=(),
        table_count=0,
        table_limit=32,
        truncated=False,
    )
    lists = ChromiumPageListsEvidence(
        endpoint=ENDPOINT,
        target_id=target_id,
        url=url,
        source="document.querySelectorAll('ol,ul')",
        lists=(),
        list_count=0,
        list_limit=64,
        truncated=False,
    )
    bundle = ChromiumPageResearchEvidenceBundle(
        endpoint=ENDPOINT,
        target_id=target_id,
        url=url,
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
        bundle_sha256=digest_character * 64,
        byte_count=1,
        endpoint=ENDPOINT,
        target_id=target_id,
        url=url,
        acquisition_mode="sequential_non_atomic_url_coherent",
        acquisition_order=ORDER,
        document_json="{}\n",
    )
    return ChromiumPageResearchLoadedCaptureEvidence(
        verification=verification,
        bundle=bundle,
    )


def _selection(
    source: ChromiumPageResearchLoadedCaptureEvidence,
    *,
    start: int,
    end: int,
):
    paragraph = select_chromium_research_capture_paragraph(source, paragraph_ordinal=1)
    return select_chromium_research_paragraph_text(
        paragraph,
        start_offset=start,
        end_offset=end,
    )


def _persist_note(
    first_source: ChromiumPageResearchLoadedCaptureEvidence,
    second_source: ChromiumPageResearchLoadedCaptureEvidence,
    destination: Path,
    *,
    first_start: int = 0,
    first_end: int = 5,
    second_start: int = 0,
    second_end: int = 4,
) -> str:
    first = _selection(first_source, start=first_start, end=first_end)
    second = _selection(second_source, start=second_start, end=second_end)
    comparison = create_chromium_research_paragraph_text_selection_comparison(
        first,
        second,
    )
    note_text = "  Human comparison: Δ differs?\nKeep verbatim.  "
    note = create_chromium_research_paragraph_text_selection_comparison_note(
        comparison,
        note_text=note_text,
    )
    persist_chromium_research_paragraph_text_selection_comparison_note(
        note,
        destination,
    )
    return note_text


def _sources(tmp_path: Path):
    first_path = tmp_path / "first-capture-does-not-need-to-exist.json"
    second_path = tmp_path / "second-capture-does-not-need-to-exist.json"
    first = _loaded_capture(
        target_id="page-a",
        url="https://example.test/a",
        digest_character="a",
        paragraph_text="Alpha evidence",
        path=first_path,
    )
    second = _loaded_capture(
        target_id="page-b",
        url="https://example.test/b",
        digest_character="b",
        paragraph_text="Beta evidence",
        path=second_path,
    )
    return first, second, first_path, second_path


def _canonical_record_bytes(record: object) -> bytes:
    return json.dumps(
        record,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def _canonical_document_bytes(document: object) -> bytes:
    return _canonical_record_bytes(document) + b"\n"


def test_load_comparison_note_relinks_ordered_pair_to_exact_supplied_sources(
    tmp_path: Path,
) -> None:
    first, second, first_path, second_path = _sources(tmp_path)
    note_path = tmp_path / "comparison-note.json"
    note_text = _persist_note(first, second, note_path)

    loaded = load_chromium_research_paragraph_text_selection_comparison_note(
        first,
        second,
        note_path,
    )

    assert isinstance(
        loaded,
        ChromiumPageResearchLoadedParagraphTextSelectionComparisonNoteRecord,
    )
    assert loaded.verification.path == note_path.resolve()
    assert loaded.verification.first_source_bundle_sha256 == "a" * 64
    assert loaded.verification.second_source_bundle_sha256 == "b" * 64
    assert loaded.note.note_text == note_text
    assert loaded.note.comparison.first_selection.selected_text == "Alpha"
    assert loaded.note.comparison.second_selection.selected_text == "Beta"
    assert loaded.note.comparison.first_selection.source.source is first
    assert loaded.note.comparison.second_selection.source.source is second
    assert (
        loaded.note.comparison.first_selection.source.paragraph
        is first.bundle.paragraphs.paragraphs[0]
    )
    assert (
        loaded.note.comparison.second_selection.source.paragraph
        is second.bundle.paragraphs.paragraphs[0]
    )
    assert not first_path.exists()
    assert not second_path.exists()

    with pytest.raises(FrozenInstanceError):
        loaded.note = loaded.note  # type: ignore[misc]


def test_load_comparison_note_uses_content_identity_not_source_paths(tmp_path: Path) -> None:
    first, second, _, _ = _sources(tmp_path)
    note_path = tmp_path / "comparison-note.json"
    _persist_note(first, second, note_path)

    first_elsewhere = replace(
        first,
        verification=replace(first.verification, path=tmp_path / "moved-a.json"),
    )
    second_elsewhere = replace(
        second,
        verification=replace(second.verification, path=tmp_path / "moved-b.json"),
    )

    loaded = load_chromium_research_paragraph_text_selection_comparison_note(
        first_elsewhere,
        second_elsewhere,
        note_path,
    )

    assert loaded.note.comparison.first_selection.source.source is first_elsewhere
    assert loaded.note.comparison.second_selection.source.source is second_elsewhere
    assert loaded.note.comparison.first_selection.selected_text == "Alpha"
    assert loaded.note.comparison.second_selection.selected_text == "Beta"


def test_load_comparison_note_rejects_swapped_or_unsupported_sources(tmp_path: Path) -> None:
    first, second, _, _ = _sources(tmp_path)
    note_path = tmp_path / "comparison-note.json"
    _persist_note(first, second, note_path)

    with pytest.raises(
        ChromiumResearchParagraphTextSelectionComparisonNoteSourceMismatchError,
        match="different first capture bundle",
    ):
        load_chromium_research_paragraph_text_selection_comparison_note(
            second,
            first,
            note_path,
        )

    unsupported_first = replace(
        first,
        verification=replace(first.verification, capture_format="other.capture.v1"),
    )
    with pytest.raises(
        ChromiumResearchParagraphTextSelectionComparisonNoteSourceMismatchError,
        match="first source capture format is unsupported",
    ):
        load_chromium_research_paragraph_text_selection_comparison_note(
            unsupported_first,
            second,
            note_path,
        )

    with pytest.raises(TypeError, match="first_source"):
        load_chromium_research_paragraph_text_selection_comparison_note(
            None,  # type: ignore[arg-type]
            second,
            note_path,
        )


def test_load_comparison_note_reverifies_sidecar_before_relink(tmp_path: Path) -> None:
    first, second, _, _ = _sources(tmp_path)
    note_path = tmp_path / "comparison-note.json"
    _persist_note(first, second, note_path)

    document = json.loads(note_path.read_text(encoding="utf-8"))
    document["note_record"]["note"]["text"] = "Tampered without digest update"
    note_path.write_bytes(_canonical_document_bytes(document))

    with pytest.raises(
        ChromiumResearchParagraphTextSelectionComparisonNoteIntegrityError,
        match="SHA-256",
    ):
        load_chromium_research_paragraph_text_selection_comparison_note(
            first,
            second,
            note_path,
        )


def test_load_rejects_file_valid_second_range_that_does_not_address_source(
    tmp_path: Path,
) -> None:
    first, second, _, _ = _sources(tmp_path)
    note_path = tmp_path / "comparison-note.json"
    _persist_note(first, second, note_path)

    document = json.loads(note_path.read_text(encoding="utf-8"))
    record = document["note_record"]
    record["comparison"]["second"]["selection"]["text_range"]["end_offset"] = 999
    document["note_record_sha256"] = hashlib.sha256(
        _canonical_record_bytes(record)
    ).hexdigest()
    note_path.write_bytes(_canonical_document_bytes(document))

    verification = verify_chromium_research_paragraph_text_selection_comparison_note(
        note_path
    )
    assert verification.second_end_offset == 999

    with pytest.raises(ValueError, match="outside returned paragraph text evidence"):
        load_chromium_research_paragraph_text_selection_comparison_note(
            first,
            second,
            note_path,
        )


def test_load_same_selection_comparison_allows_same_supplied_source_twice(
    tmp_path: Path,
) -> None:
    source = _loaded_capture(
        target_id="same",
        url="https://example.test/same",
        digest_character="c",
        paragraph_text="Same source",
        path=tmp_path / "same-capture-does-not-need-to-exist.json",
    )
    note_path = tmp_path / "same-comparison-note.json"
    _persist_note(
        source,
        source,
        note_path,
        first_start=0,
        first_end=4,
        second_start=0,
        second_end=4,
    )

    loaded = load_chromium_research_paragraph_text_selection_comparison_note(
        source,
        source,
        note_path,
    )

    assert loaded.note.comparison.first_selection.source.source is source
    assert loaded.note.comparison.second_selection.source.source is source
    assert loaded.note.comparison.first_selection.selected_text == "Same"
    assert loaded.note.comparison.second_selection.selected_text == "Same"


def test_public_app_exports_comparison_note_loader(tmp_path: Path) -> None:
    first, second, _, _ = _sources(tmp_path)
    note_path = tmp_path / "comparison-note.json"
    _persist_note(first, second, note_path)

    loaded = pyxis_app.load_chromium_research_paragraph_text_selection_comparison_note(
        first,
        second,
        note_path,
    )

    assert isinstance(
        loaded,
        pyxis_app.ChromiumPageResearchLoadedParagraphTextSelectionComparisonNoteRecord,
    )
    assert loaded.note.comparison.first_selection.selected_text == "Alpha"
    assert loaded.note.comparison.second_selection.selected_text == "Beta"
