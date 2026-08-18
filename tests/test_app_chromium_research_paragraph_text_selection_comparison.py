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
from pyxis.app.chromium_paragraphs import (
    ChromiumPageParagraphEvidence,
    ChromiumPageParagraphsEvidence,
)
from pyxis.app.chromium_research_bundle import ChromiumPageResearchEvidenceBundle
from pyxis.app.chromium_research_capture import ChromiumPageResearchCaptureVerificationEvidence
from pyxis.app.chromium_research_capture_load import ChromiumPageResearchLoadedCaptureEvidence
from pyxis.app.chromium_research_paragraph_text_selection import (
    ChromiumPageResearchParagraphTextSelectionEvidence,
    select_chromium_research_paragraph_text,
)
from pyxis.app.chromium_research_paragraph_text_selection_comparison import (
    ChromiumPageResearchParagraphTextSelectionComparisonRecord,
    create_chromium_research_paragraph_text_selection_comparison,
)
from pyxis.app.chromium_research_passage_selection import (
    ChromiumPageResearchParagraphSelectionEvidence,
    select_chromium_research_capture_paragraph,
)
from pyxis.app.chromium_tables import ChromiumPageTablesEvidence


ENDPOINT = "http://127.0.0.1:9222"
ORDER = (
    "page",
    "links",
    "headings",
    "metadata",
    "paragraphs",
    "tables",
    "lists",
)


def _loaded_capture(
    *,
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
    return ChromiumPageResearchLoadedCaptureEvidence(
        verification=verification,
        bundle=bundle,
    )


def _paragraph_selection(
    *,
    target_id: str = "page-1",
    url: str = "https://example.test/first",
    digest_character: str = "a",
    paragraph_text: str = "Alpha evidence",
) -> ChromiumPageResearchParagraphSelectionEvidence:
    capture = _loaded_capture(
        target_id=target_id,
        url=url,
        digest_character=digest_character,
        paragraph_text=paragraph_text,
    )
    return select_chromium_research_capture_paragraph(capture, paragraph_ordinal=1)


def _text_selection(
    paragraph_selection: ChromiumPageResearchParagraphSelectionEvidence,
    *,
    start_offset: int,
    end_offset: int,
) -> ChromiumPageResearchParagraphTextSelectionEvidence:
    return select_chromium_research_paragraph_text(
        paragraph_selection,
        start_offset=start_offset,
        end_offset=end_offset,
    )


def test_comparison_retains_exact_selections_from_two_distinct_captures() -> None:
    first_parent = _paragraph_selection(
        target_id="page-a",
        url="https://example.test/a",
        digest_character="a",
        paragraph_text="Alpha evidence",
    )
    second_parent = _paragraph_selection(
        target_id="page-b",
        url="https://example.test/b",
        digest_character="b",
        paragraph_text="Beta evidence",
    )
    first = _text_selection(first_parent, start_offset=0, end_offset=5)
    second = _text_selection(second_parent, start_offset=0, end_offset=4)

    comparison = create_chromium_research_paragraph_text_selection_comparison(
        first,
        second,
    )

    assert isinstance(
        comparison,
        ChromiumPageResearchParagraphTextSelectionComparisonRecord,
    )
    assert comparison.comparison_mode == "caller_explicit_exact_text_range_comparison"
    assert comparison.first_selection is first
    assert comparison.second_selection is second
    assert comparison.first_selection.selected_text == "Alpha"
    assert comparison.second_selection.selected_text == "Beta"
    assert first.source.source is not second.source.source
    assert first.source.source.verification.bundle_sha256 == "a" * 64
    assert second.source.source.verification.bundle_sha256 == "b" * 64
    assert [field.name for field in fields(comparison)] == [
        "comparison_mode",
        "first_selection",
        "second_selection",
    ]

    with pytest.raises(FrozenInstanceError):
        comparison.comparison_mode = "other"  # type: ignore[misc]


def test_comparison_allows_two_ranges_from_the_same_paragraph() -> None:
    parent = _paragraph_selection(paragraph_text="Alpha Beta")
    first = _text_selection(parent, start_offset=0, end_offset=5)
    second = _text_selection(parent, start_offset=6, end_offset=10)

    comparison = create_chromium_research_paragraph_text_selection_comparison(
        first,
        second,
    )

    assert comparison.first_selection is first
    assert comparison.second_selection is second
    assert comparison.first_selection.source is comparison.second_selection.source
    assert comparison.first_selection.selected_text == "Alpha"
    assert comparison.second_selection.selected_text == "Beta"


def test_comparison_allows_same_exact_selection_without_judging_significance() -> None:
    parent = _paragraph_selection()
    selection = _text_selection(parent, start_offset=0, end_offset=5)

    comparison = create_chromium_research_paragraph_text_selection_comparison(
        selection,
        selection,
    )

    assert comparison.first_selection is selection
    assert comparison.second_selection is selection


def test_comparison_rejects_wrong_selection_types() -> None:
    parent = _paragraph_selection()
    selection = _text_selection(parent, start_offset=0, end_offset=5)

    with pytest.raises(TypeError, match="first_selection"):
        create_chromium_research_paragraph_text_selection_comparison(
            parent,  # type: ignore[arg-type]
            selection,
        )
    with pytest.raises(TypeError, match="second_selection"):
        create_chromium_research_paragraph_text_selection_comparison(
            selection,
            parent,  # type: ignore[arg-type]
        )


def test_comparison_rejects_unsupported_range_mode_or_offset_unit() -> None:
    parent = _paragraph_selection()
    first = _text_selection(parent, start_offset=0, end_offset=5)
    second = _text_selection(parent, start_offset=6, end_offset=8)

    with pytest.raises(ValueError, match="first_selection selection mode"):
        create_chromium_research_paragraph_text_selection_comparison(
            replace(first, selection_mode="other-selection"),
            second,
        )
    with pytest.raises(ValueError, match="second_selection offset unit"):
        create_chromium_research_paragraph_text_selection_comparison(
            first,
            replace(second, offset_unit="utf16_code_unit"),
        )


def test_comparison_reuses_18a_parent_identity_and_coordinate_validation() -> None:
    first_parent = _paragraph_selection(paragraph_text="Alpha evidence")
    second_parent = _paragraph_selection(
        target_id="page-2",
        url="https://example.test/second",
        digest_character="b",
        paragraph_text="Beta evidence",
    )
    first = _text_selection(first_parent, start_offset=0, end_offset=5)
    second = _text_selection(second_parent, start_offset=0, end_offset=4)

    copied_paragraph = replace(first.source.paragraph)
    forged_parent = replace(first.source, paragraph=copied_paragraph)
    forged_first = replace(first, source=forged_parent)

    assert copied_paragraph == first.source.paragraph
    assert copied_paragraph is not first.source.paragraph

    with pytest.raises(ValueError, match="exact paragraph object"):
        create_chromium_research_paragraph_text_selection_comparison(
            forged_first,
            second,
        )

    with pytest.raises(ValueError, match="outside returned paragraph text evidence"):
        create_chromium_research_paragraph_text_selection_comparison(
            first,
            replace(second, end_offset=999),
        )


def test_comparison_is_available_through_public_app_surface() -> None:
    from pyxis.app import (
        ChromiumPageResearchParagraphTextSelectionComparisonRecord as PublicRecord,
    )
    from pyxis.app import (
        create_chromium_research_paragraph_text_selection_comparison as public_create,
    )

    assert PublicRecord is ChromiumPageResearchParagraphTextSelectionComparisonRecord
    assert public_create is create_chromium_research_paragraph_text_selection_comparison
