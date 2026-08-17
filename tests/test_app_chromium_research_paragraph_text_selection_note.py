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
from pyxis.app.chromium_research_paragraph_text_selection_note import (
    ChromiumPageResearchParagraphTextSelectionNoteRecord,
    create_chromium_research_paragraph_text_selection_note,
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


def _text_selection(
    *,
    paragraph_text: str = "A😀B café",
    start_offset: int = 1,
    end_offset: int = 4,
    **kwargs: object,
) -> ChromiumPageResearchParagraphTextSelectionEvidence:
    paragraph_selection = _paragraph_selection(paragraph_text=paragraph_text, **kwargs)
    return select_chromium_research_paragraph_text(
        paragraph_selection,
        start_offset=start_offset,
        end_offset=end_offset,
    )


def test_text_selection_note_retains_exact_range_and_verbatim_note() -> None:
    selection = _text_selection()
    note_text = "  This exact phrase changed the interpretation. 😀\n"

    note = create_chromium_research_paragraph_text_selection_note(
        selection,
        note_text=note_text,
    )

    assert isinstance(note, ChromiumPageResearchParagraphTextSelectionNoteRecord)
    assert note.note_mode == "caller_authored_exact_text_on_paragraph_text_selection"
    assert note.selection is selection
    assert note.selection.selected_text == "😀B "
    assert note.note_text == note_text
    assert [field.name for field in fields(note)] == [
        "note_mode",
        "selection",
        "note_text",
    ]

    with pytest.raises(FrozenInstanceError):
        note.note_text = "changed"  # type: ignore[misc]


def test_text_selection_note_does_not_reinterpret_selected_whitespace() -> None:
    selection = _text_selection(
        paragraph_text="A B",
        start_offset=1,
        end_offset=2,
    )

    assert selection.selected_text == " "

    note = create_chromium_research_paragraph_text_selection_note(
        selection,
        note_text="The spacing itself is what I am recording.",
    )

    assert note.selection is selection
    assert note.selection.selected_text == " "


def test_text_selection_note_rejects_non_string_or_blank_note() -> None:
    selection = _text_selection()

    with pytest.raises(TypeError, match="note_text"):
        create_chromium_research_paragraph_text_selection_note(
            selection,
            note_text=123,  # type: ignore[arg-type]
        )
    with pytest.raises(ValueError, match="non-whitespace"):
        create_chromium_research_paragraph_text_selection_note(
            selection,
            note_text=" \n\t ",
        )


def test_text_selection_note_rejects_unsupported_range_mode_or_offset_unit() -> None:
    selection = _text_selection()

    with pytest.raises(ValueError, match="selection mode"):
        create_chromium_research_paragraph_text_selection_note(
            replace(selection, selection_mode="other-selection"),
            note_text="Human note",
        )
    with pytest.raises(ValueError, match="offset unit"):
        create_chromium_research_paragraph_text_selection_note(
            replace(selection, offset_unit="utf16_code_unit"),
            note_text="Human note",
        )


def test_text_selection_note_reuses_18a_bounded_range_validation() -> None:
    selection = _text_selection(
        paragraph_text="Alpha",
        start_offset=0,
        end_offset=5,
        text_character_count=10,
        text_limit=5,
        truncated=True,
    )
    forged_selection = replace(selection, end_offset=6)

    with pytest.raises(ValueError, match="outside the bounded returned paragraph text prefix"):
        create_chromium_research_paragraph_text_selection_note(
            forged_selection,
            note_text="Human note",
        )


def test_text_selection_note_rejects_equal_by_value_parent_paragraph_copy() -> None:
    selection = _text_selection()
    paragraph_selection = selection.source
    copied_paragraph = replace(paragraph_selection.paragraph)
    forged_paragraph_selection = replace(
        paragraph_selection,
        paragraph=copied_paragraph,
    )
    forged_text_selection = replace(selection, source=forged_paragraph_selection)

    assert copied_paragraph == paragraph_selection.paragraph
    assert copied_paragraph is not paragraph_selection.paragraph

    with pytest.raises(ValueError, match="exact paragraph object"):
        create_chromium_research_paragraph_text_selection_note(
            forged_text_selection,
            note_text="Human note",
        )
