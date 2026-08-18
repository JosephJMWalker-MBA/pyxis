from __future__ import annotations

from dataclasses import FrozenInstanceError, fields, replace
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
from pyxis.app.chromium_paragraphs import ChromiumPageParagraphEvidence, ChromiumPageParagraphsEvidence
from pyxis.app.chromium_research_bundle import ChromiumPageResearchEvidenceBundle
from pyxis.app.chromium_research_capture import ChromiumPageResearchCaptureVerificationEvidence
from pyxis.app.chromium_research_capture_load import ChromiumPageResearchLoadedCaptureEvidence
from pyxis.app.chromium_research_paragraph_text_selection import select_chromium_research_paragraph_text
from pyxis.app.chromium_research_paragraph_text_selection_comparison import (
    ChromiumPageResearchParagraphTextSelectionComparisonRecord,
    create_chromium_research_paragraph_text_selection_comparison,
)
from pyxis.app.chromium_research_paragraph_text_selection_comparison_note import (
    ChromiumPageResearchParagraphTextSelectionComparisonNoteRecord,
    create_chromium_research_paragraph_text_selection_comparison_note,
)
from pyxis.app.chromium_research_passage_selection import select_chromium_research_capture_paragraph
from pyxis.app.chromium_tables import ChromiumPageTablesEvidence


ENDPOINT = "http://127.0.0.1:9222"
ORDER = ("page", "links", "headings", "metadata", "paragraphs", "tables", "lists")


def _loaded_capture(
    *, target_id: str, url: str, digest_character: str, paragraph_text: str
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
        path=Path(f"/tmp/{target_id}.json"),
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
    return ChromiumPageResearchLoadedCaptureEvidence(verification=verification, bundle=bundle)


def _comparison() -> ChromiumPageResearchParagraphTextSelectionComparisonRecord:
    first_capture = _loaded_capture(
        target_id="page-a",
        url="https://example.test/a",
        digest_character="a",
        paragraph_text="Alpha evidence",
    )
    second_capture = _loaded_capture(
        target_id="page-b",
        url="https://example.test/b",
        digest_character="b",
        paragraph_text="Beta evidence",
    )
    first_parent = select_chromium_research_capture_paragraph(first_capture, paragraph_ordinal=1)
    second_parent = select_chromium_research_capture_paragraph(second_capture, paragraph_ordinal=1)
    first = select_chromium_research_paragraph_text(first_parent, start_offset=0, end_offset=5)
    second = select_chromium_research_paragraph_text(second_parent, start_offset=0, end_offset=4)
    return create_chromium_research_paragraph_text_selection_comparison(first, second)


def test_comparison_note_retains_exact_comparison_and_verbatim_human_text() -> None:
    comparison = _comparison()
    note_text = "  These passages frame the issue differently.\nΔοκιμή 😀  "

    note = create_chromium_research_paragraph_text_selection_comparison_note(
        comparison,
        note_text=note_text,
    )

    assert isinstance(note, ChromiumPageResearchParagraphTextSelectionComparisonNoteRecord)
    assert note.note_mode == "caller_authored_note_on_exact_text_range_comparison"
    assert note.comparison is comparison
    assert note.note_text == note_text
    assert note.comparison.first_selection.selected_text == "Alpha"
    assert note.comparison.second_selection.selected_text == "Beta"
    assert [field.name for field in fields(note)] == ["note_mode", "comparison", "note_text"]

    with pytest.raises(FrozenInstanceError):
        note.note_text = "changed"  # type: ignore[misc]


def test_comparison_note_rejects_non_string_or_whitespace_only_text() -> None:
    comparison = _comparison()

    with pytest.raises(TypeError, match="note_text"):
        create_chromium_research_paragraph_text_selection_comparison_note(
            comparison,
            note_text=123,  # type: ignore[arg-type]
        )
    with pytest.raises(ValueError, match="non-whitespace"):
        create_chromium_research_paragraph_text_selection_comparison_note(
            comparison,
            note_text=" \n\t ",
        )


def test_comparison_note_rejects_non_comparison_input() -> None:
    comparison = _comparison()

    with pytest.raises(TypeError, match="comparison"):
        create_chromium_research_paragraph_text_selection_comparison_note(
            comparison.first_selection,  # type: ignore[arg-type]
            note_text="human note",
        )


def test_comparison_note_rejects_unsupported_comparison_mode() -> None:
    comparison = replace(_comparison(), comparison_mode="machine_inferred_similarity")

    with pytest.raises(ValueError, match="comparison mode"):
        create_chromium_research_paragraph_text_selection_comparison_note(
            comparison,
            note_text="human note",
        )


def test_comparison_note_reuses_19a_and_18a_validation() -> None:
    comparison = _comparison()

    copied_paragraph = replace(comparison.first_selection.source.paragraph)
    forged_parent = replace(comparison.first_selection.source, paragraph=copied_paragraph)
    forged_first = replace(comparison.first_selection, source=forged_parent)
    forged_comparison = replace(comparison, first_selection=forged_first)

    assert copied_paragraph == comparison.first_selection.source.paragraph
    assert copied_paragraph is not comparison.first_selection.source.paragraph

    with pytest.raises(ValueError, match="exact paragraph object"):
        create_chromium_research_paragraph_text_selection_comparison_note(
            forged_comparison,
            note_text="human note",
        )

    bad_range_comparison = replace(
        comparison,
        second_selection=replace(comparison.second_selection, end_offset=999),
    )
    with pytest.raises(ValueError, match="outside returned paragraph text evidence"):
        create_chromium_research_paragraph_text_selection_comparison_note(
            bad_range_comparison,
            note_text="human note",
        )


def test_comparison_note_revalidates_but_retains_supplied_comparison_object() -> None:
    original = _comparison()
    supplied = replace(original)

    assert supplied == original
    assert supplied is not original

    note = create_chromium_research_paragraph_text_selection_comparison_note(
        supplied,
        note_text="The human owns this interpretation.",
    )

    assert note.comparison is supplied
    assert note.comparison is not original
    assert note.comparison.first_selection is original.first_selection
    assert note.comparison.second_selection is original.second_selection


def test_comparison_note_is_available_through_public_app_surface() -> None:
    from pyxis.app import (
        ChromiumPageResearchParagraphTextSelectionComparisonNoteRecord as PublicRecord,
    )
    from pyxis.app import (
        create_chromium_research_paragraph_text_selection_comparison_note as public_create,
    )

    assert PublicRecord is ChromiumPageResearchParagraphTextSelectionComparisonNoteRecord
    assert public_create is create_chromium_research_paragraph_text_selection_comparison_note
