from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
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
    load_chromium_research_paragraph_text_selection_comparison_note,
)
from pyxis.app.chromium_research_paragraph_text_selection_comparison_note_persistence import (
    persist_chromium_research_paragraph_text_selection_comparison_note,
)
from pyxis.app.chromium_research_paragraph_text_selection_note import (
    create_chromium_research_paragraph_text_selection_note,
)
from pyxis.app.chromium_research_paragraph_text_selection_note_load import (
    load_chromium_research_paragraph_text_selection_note,
)
from pyxis.app.chromium_research_paragraph_text_selection_note_persistence import (
    persist_chromium_research_paragraph_text_selection_note,
)
from pyxis.app.chromium_research_passage_selection import (
    select_chromium_research_capture_paragraph,
)
from pyxis.app.chromium_research_selection_note import create_chromium_research_paragraph_note
from pyxis.app.chromium_research_selection_note_load import (
    load_chromium_research_paragraph_note,
)
from pyxis.app.chromium_research_selection_note_persistence import (
    persist_chromium_research_paragraph_note,
)
from pyxis.app.chromium_research_working_set import (
    ChromiumPageResearchWorkingSetRecord,
    create_chromium_research_working_set,
)
from pyxis.app.chromium_tables import ChromiumPageTablesEvidence


ENDPOINT = "http://127.0.0.1:9222"
ORDER = ("page", "links", "headings", "metadata", "paragraphs", "tables", "lists")


def _loaded_capture(
    *,
    path: Path,
    target_id: str,
    url: str,
    digest_character: str,
    paragraph_text: str,
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


def _loaded_records(tmp_path: Path):
    first_source = _loaded_capture(
        path=tmp_path / "source-a.json",
        target_id="page-a",
        url="https://example.test/a",
        digest_character="a",
        paragraph_text="Alpha evidence paragraph",
    )
    second_source = _loaded_capture(
        path=tmp_path / "source-b.json",
        target_id="page-b",
        url="https://example.test/b",
        digest_character="b",
        paragraph_text="Beta evidence paragraph",
    )

    paragraph_selection = select_chromium_research_capture_paragraph(
        first_source,
        paragraph_ordinal=1,
    )
    paragraph_note = create_chromium_research_paragraph_note(
        paragraph_selection,
        note_text="  Whole paragraph matters.  ",
    )
    paragraph_note_path = tmp_path / "paragraph-note.json"
    persist_chromium_research_paragraph_note(paragraph_note, paragraph_note_path)
    loaded_paragraph_note = load_chromium_research_paragraph_note(
        first_source,
        paragraph_note_path,
    )

    first_range = select_chromium_research_paragraph_text(
        paragraph_selection,
        start_offset=0,
        end_offset=5,
    )
    exact_note = create_chromium_research_paragraph_text_selection_note(
        first_range,
        note_text="Exact range note 😀",
    )
    exact_note_path = tmp_path / "exact-note.json"
    persist_chromium_research_paragraph_text_selection_note(exact_note, exact_note_path)
    loaded_exact_note = load_chromium_research_paragraph_text_selection_note(
        first_source,
        exact_note_path,
    )

    second_paragraph = select_chromium_research_capture_paragraph(
        second_source,
        paragraph_ordinal=1,
    )
    second_range = select_chromium_research_paragraph_text(
        second_paragraph,
        start_offset=0,
        end_offset=4,
    )
    comparison = create_chromium_research_paragraph_text_selection_comparison(
        first_range,
        second_range,
    )
    comparison_note = create_chromium_research_paragraph_text_selection_comparison_note(
        comparison,
        note_text="  Human comparison; no machine relation claim.\nKeep exact.  ",
    )
    comparison_note_path = tmp_path / "comparison-note.json"
    persist_chromium_research_paragraph_text_selection_comparison_note(
        comparison_note,
        comparison_note_path,
    )
    loaded_comparison_note = (
        load_chromium_research_paragraph_text_selection_comparison_note(
            first_source,
            second_source,
            comparison_note_path,
        )
    )

    return (
        loaded_paragraph_note,
        loaded_exact_note,
        loaded_comparison_note,
    )


def test_working_set_preserves_mixed_order_and_exact_item_identity(tmp_path: Path) -> None:
    paragraph_note, exact_note, comparison_note = _loaded_records(tmp_path)

    working_set = create_chromium_research_working_set(
        [exact_note, paragraph_note, comparison_note]
    )

    assert isinstance(working_set, ChromiumPageResearchWorkingSetRecord)
    assert working_set.working_set_mode == (
        "caller_explicit_ordered_relinked_research_working_set"
    )
    assert working_set.items[0] is exact_note
    assert working_set.items[1] is paragraph_note
    assert working_set.items[2] is comparison_note

    with pytest.raises(FrozenInstanceError):
        working_set.items = ()  # type: ignore[misc]


def test_working_set_snapshots_sequence_and_preserves_duplicate_members(tmp_path: Path) -> None:
    _, _, comparison_note = _loaded_records(tmp_path)
    requested = [comparison_note, comparison_note]

    working_set = create_chromium_research_working_set(requested)
    requested.clear()

    assert len(working_set.items) == 2
    assert working_set.items[0] is comparison_note
    assert working_set.items[1] is comparison_note


def test_working_set_uses_loaded_evidence_without_rereading_sidecars(tmp_path: Path) -> None:
    paragraph_note, exact_note, comparison_note = _loaded_records(tmp_path)

    paragraph_note.verification.path.unlink()
    exact_note.verification.path.unlink()
    comparison_note.verification.path.unlink()

    working_set = create_chromium_research_working_set(
        (paragraph_note, exact_note, comparison_note)
    )

    assert working_set.items == (paragraph_note, exact_note, comparison_note)
    assert not paragraph_note.verification.path.exists()
    assert not exact_note.verification.path.exists()
    assert not comparison_note.verification.path.exists()


def test_working_set_rejects_in_memory_verification_note_mismatch(tmp_path: Path) -> None:
    _, exact_note, _ = _loaded_records(tmp_path)
    forged = replace(
        exact_note,
        verification=replace(
            exact_note.verification,
            note_text="Different retained verification text",
        ),
    )

    with pytest.raises(
        ValueError,
        match=r"items\[0\] exact-range-note verification is incoherent",
    ):
        create_chromium_research_working_set((forged,))


def test_working_set_rejects_comparison_source_reference_mismatch(tmp_path: Path) -> None:
    _, _, comparison_note = _loaded_records(tmp_path)
    forged = replace(
        comparison_note,
        verification=replace(
            comparison_note.verification,
            first_source_bundle_sha256="f" * 64,
        ),
    )

    with pytest.raises(
        ValueError,
        match=r"items\[0\] comparison-note verification is incoherent",
    ):
        create_chromium_research_working_set((forged,))


def test_working_set_rejects_empty_and_non_relinked_records(tmp_path: Path) -> None:
    paragraph_note, _, _ = _loaded_records(tmp_path)

    with pytest.raises(ValueError, match="must contain at least one item"):
        create_chromium_research_working_set(())

    with pytest.raises(TypeError, match=r"items\[0\] must be a supported relinked"):
        create_chromium_research_working_set(
            (paragraph_note.note,)  # type: ignore[arg-type]
        )


def test_public_app_exports_research_working_set(tmp_path: Path) -> None:
    paragraph_note, exact_note, comparison_note = _loaded_records(tmp_path)

    working_set = pyxis_app.create_chromium_research_working_set(
        (paragraph_note, exact_note, comparison_note)
    )

    assert isinstance(working_set, pyxis_app.ChromiumPageResearchWorkingSetRecord)
    assert working_set.items[0] is paragraph_note
    assert working_set.items[1] is exact_note
    assert working_set.items[2] is comparison_note
