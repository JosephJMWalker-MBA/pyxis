from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
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


def _loaded_capture() -> ChromiumPageResearchLoadedCaptureEvidence:
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
    paragraph_one = ChromiumPageParagraphEvidence(
        ordinal=1,
        element_id="passage",
        text_prefix="Alpha",
        text_character_count=5,
        text_limit=1024,
        truncated=False,
    )
    paragraph_two = ChromiumPageParagraphEvidence(
        ordinal=2,
        element_id="passage",
        text_prefix="Beta",
        text_character_count=4,
        text_limit=1024,
        truncated=False,
    )
    paragraphs = ChromiumPageParagraphsEvidence(
        endpoint=ENDPOINT,
        target_id=TARGET_ID,
        url=URL,
        source="document.querySelectorAll('p')",
        paragraphs=(paragraph_one, paragraph_two),
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
        path=Path("/tmp/pyxis-research-capture.json"),
        capture_format="pyxis.chromium.research_capture.v1",
        bundle_sha256="0" * 64,
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


def test_select_rehydrated_paragraph_preserves_exact_source_and_paragraph_identity() -> None:
    source = _loaded_capture()

    selection = select_chromium_research_capture_paragraph(
        source,
        paragraph_ordinal=2,
    )

    assert selection.selection_mode == "caller_explicit_returned_paragraph_ordinal"
    assert selection.source is source
    assert selection.paragraph is source.bundle.paragraphs.paragraphs[1]
    assert selection.paragraph.ordinal == 2
    assert selection.paragraph.element_id == "passage"
    assert selection.paragraph.text_prefix == "Beta"

    with pytest.raises(FrozenInstanceError):
        selection.selection_mode = "changed"  # type: ignore[misc]


def test_select_rehydrated_paragraph_uses_ordinal_not_authored_id() -> None:
    source = _loaded_capture()
    assert source.bundle.paragraphs.paragraphs[0].element_id == "passage"
    assert source.bundle.paragraphs.paragraphs[1].element_id == "passage"

    first = select_chromium_research_capture_paragraph(source, paragraph_ordinal=1)
    second = select_chromium_research_capture_paragraph(source, paragraph_ordinal=2)

    assert first.paragraph is source.bundle.paragraphs.paragraphs[0]
    assert second.paragraph is source.bundle.paragraphs.paragraphs[1]
    assert first.paragraph is not second.paragraph


def test_select_rehydrated_paragraph_refuses_unreturned_truncated_evidence() -> None:
    source = _loaded_capture()
    truncated_paragraphs = replace(
        source.bundle.paragraphs,
        paragraph_count=3,
        truncated=True,
    )
    source = replace(
        source,
        bundle=replace(source.bundle, paragraphs=truncated_paragraphs),
    )

    with pytest.raises(ValueError, match="outside the bounded returned paragraph prefix"):
        select_chromium_research_capture_paragraph(source, paragraph_ordinal=3)


def test_select_rehydrated_paragraph_rejects_invalid_ordinals() -> None:
    source = _loaded_capture()

    with pytest.raises(TypeError, match="must be an integer"):
        select_chromium_research_capture_paragraph(source, paragraph_ordinal=True)
    with pytest.raises(ValueError, match=">= 1"):
        select_chromium_research_capture_paragraph(source, paragraph_ordinal=0)
    with pytest.raises(ValueError, match="does not identify an observed paragraph"):
        select_chromium_research_capture_paragraph(source, paragraph_ordinal=3)


def test_select_rehydrated_paragraph_rejects_source_origin_incoherence() -> None:
    source = _loaded_capture()
    source = replace(
        source,
        verification=replace(source.verification, url="https://example.test/other"),
    )

    with pytest.raises(ValueError, match="verification url is incoherent"):
        select_chromium_research_capture_paragraph(source, paragraph_ordinal=1)
