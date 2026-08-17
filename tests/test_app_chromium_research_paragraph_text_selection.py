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
from pyxis.app.chromium_research_passage_selection import (
    ChromiumPageResearchParagraphSelectionEvidence,
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


def _loaded_capture(
    *,
    paragraph_text: str = "A😀B café",
    text_character_count: int | None = None,
    text_limit: int = 1024,
    truncated: bool = False,
) -> ChromiumPageResearchLoadedCaptureEvidence:
    if text_character_count is None:
        text_character_count = len(paragraph_text)

    page = ChromiumPageObservationEvidence(
        endpoint=ENDPOINT,
        target_id=TARGET_ID,
        url=URL,
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
    paragraph = ChromiumPageParagraphEvidence(
        ordinal=1,
        element_id="passage",
        text_prefix=paragraph_text,
        text_character_count=text_character_count,
        text_limit=text_limit,
        truncated=truncated,
    )
    paragraphs = ChromiumPageParagraphsEvidence(
        endpoint=ENDPOINT,
        target_id=TARGET_ID,
        url=URL,
        source="document.querySelectorAll('p')",
        paragraphs=(paragraph,),
        paragraph_count=1,
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
        path=Path("/tmp/research-capture.json"),
        capture_format="pyxis.chromium.research_capture.v1",
        bundle_sha256="a" * 64,
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


def _paragraph_selection(**kwargs: object) -> ChromiumPageResearchParagraphSelectionEvidence:
    capture = _loaded_capture(**kwargs)
    return select_chromium_research_capture_paragraph(capture, paragraph_ordinal=1)


def test_text_selection_retains_exact_source_and_derives_unicode_slice() -> None:
    paragraph_selection = _paragraph_selection()

    selected = select_chromium_research_paragraph_text(
        paragraph_selection,
        start_offset=1,
        end_offset=4,
    )

    assert isinstance(selected, ChromiumPageResearchParagraphTextSelectionEvidence)
    assert selected.selection_mode == "caller_explicit_returned_paragraph_text_range"
    assert selected.offset_unit == "unicode_code_point"
    assert selected.source is paragraph_selection
    assert selected.start_offset == 1
    assert selected.end_offset == 4
    assert selected.selected_text == "😀B "
    assert [field.name for field in fields(selected)] == [
        "selection_mode",
        "offset_unit",
        "source",
        "start_offset",
        "end_offset",
    ]

    with pytest.raises(FrozenInstanceError):
        selected.start_offset = 0  # type: ignore[misc]


def test_text_selection_uses_exact_integer_half_open_coordinates() -> None:
    paragraph_selection = _paragraph_selection()

    with pytest.raises(TypeError, match="start_offset"):
        select_chromium_research_paragraph_text(
            paragraph_selection,
            start_offset=True,
            end_offset=2,
        )
    with pytest.raises(TypeError, match="end_offset"):
        select_chromium_research_paragraph_text(
            paragraph_selection,
            start_offset=0,
            end_offset=False,
        )
    with pytest.raises(ValueError, match="start_offset"):
        select_chromium_research_paragraph_text(
            paragraph_selection,
            start_offset=-1,
            end_offset=1,
        )
    with pytest.raises(ValueError, match="greater than start_offset"):
        select_chromium_research_paragraph_text(
            paragraph_selection,
            start_offset=2,
            end_offset=2,
        )


def test_text_selection_rejects_equal_by_value_paragraph_copy() -> None:
    paragraph_selection = _paragraph_selection()
    copied_paragraph = replace(paragraph_selection.paragraph)
    forged_selection = replace(paragraph_selection, paragraph=copied_paragraph)

    assert copied_paragraph == paragraph_selection.paragraph
    assert copied_paragraph is not paragraph_selection.paragraph

    with pytest.raises(ValueError, match="exact paragraph object"):
        select_chromium_research_paragraph_text(
            forged_selection,
            start_offset=0,
            end_offset=1,
        )


def test_text_selection_rejects_unsupported_parent_selection_mode() -> None:
    paragraph_selection = _paragraph_selection()
    forged_selection = replace(paragraph_selection, selection_mode="other-selection")

    with pytest.raises(ValueError, match="selection mode"):
        select_chromium_research_paragraph_text(
            forged_selection,
            start_offset=0,
            end_offset=1,
        )


def test_text_selection_can_use_returned_prefix_but_not_truncated_suffix() -> None:
    paragraph_selection = _paragraph_selection(
        paragraph_text="Alpha",
        text_character_count=10,
        text_limit=5,
        truncated=True,
    )

    returned_prefix = select_chromium_research_paragraph_text(
        paragraph_selection,
        start_offset=0,
        end_offset=5,
    )
    assert returned_prefix.selected_text == "Alpha"

    with pytest.raises(ValueError, match="outside the bounded returned paragraph text prefix"):
        select_chromium_research_paragraph_text(
            paragraph_selection,
            start_offset=0,
            end_offset=6,
        )


def test_text_selection_rejects_coordinates_outside_complete_returned_text() -> None:
    paragraph_selection = _paragraph_selection(paragraph_text="Alpha")

    with pytest.raises(ValueError, match="outside returned paragraph text evidence"):
        select_chromium_research_paragraph_text(
            paragraph_selection,
            start_offset=5,
            end_offset=6,
        )
    with pytest.raises(ValueError, match="outside returned paragraph text evidence"):
        select_chromium_research_paragraph_text(
            paragraph_selection,
            start_offset=4,
            end_offset=6,
        )
