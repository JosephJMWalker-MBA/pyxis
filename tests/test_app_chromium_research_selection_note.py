from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
from pathlib import Path

import pytest

from pyxis.app import (
    ChromiumPageResearchParagraphNoteRecord,
    create_chromium_research_paragraph_note,
    select_chromium_research_capture_paragraph,
)
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


def _selection():
    return select_chromium_research_capture_paragraph(
        _loaded_capture(),
        paragraph_ordinal=2,
    )


def test_note_retains_exact_selection_verbatim_text_and_is_frozen() -> None:
    selection = _selection()
    text = "  Compare this with the earlier definition. 😀\nKeep the wording exact.  "

    note = create_chromium_research_paragraph_note(selection, note_text=text)

    assert isinstance(note, ChromiumPageResearchParagraphNoteRecord)
    assert note.note_mode == "caller_authored_exact_text_on_paragraph_selection"
    assert note.selection is selection
    assert note.note_text == text

    with pytest.raises(FrozenInstanceError):
        note.note_text = "changed"  # type: ignore[misc]


def test_note_validation_does_not_trim_or_normalize_caller_text() -> None:
    selection = _selection()
    text = "\n  Human interpretation — not source evidence.  \n"

    note = create_chromium_research_paragraph_note(selection, note_text=text)

    assert note.note_text == text
    assert note.note_text.startswith("\n  ")
    assert note.note_text.endswith("  \n")


def test_note_rejects_non_string_and_whitespace_only_text() -> None:
    selection = _selection()

    with pytest.raises(TypeError, match="must be a string"):
        create_chromium_research_paragraph_note(selection, note_text=123)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="non-whitespace"):
        create_chromium_research_paragraph_note(selection, note_text=" \n\t ")


def test_note_rejects_unsupported_or_forged_selection_mode() -> None:
    selection = replace(_selection(), selection_mode="machine_ranked")

    with pytest.raises(ValueError, match="selection mode is unsupported"):
        create_chromium_research_paragraph_note(selection, note_text="Caller note")


def test_note_requires_exact_selected_paragraph_object_identity() -> None:
    selection = _selection()
    equal_but_distinct_paragraph = replace(selection.paragraph)
    assert equal_but_distinct_paragraph == selection.paragraph
    assert equal_but_distinct_paragraph is not selection.paragraph

    forged_selection = replace(selection, paragraph=equal_but_distinct_paragraph)

    with pytest.raises(ValueError, match="not the exact paragraph object"):
        create_chromium_research_paragraph_note(
            forged_selection,
            note_text="Caller note",
        )


def test_public_selection_then_note_composition_preserves_both_human_actions() -> None:
    source = _loaded_capture()
    selection = select_chromium_research_capture_paragraph(
        source,
        paragraph_ordinal=1,
    )

    note = create_chromium_research_paragraph_note(
        selection,
        note_text="This wording may matter later.",
    )

    assert note.selection is selection
    assert note.selection.source is source
    assert note.selection.paragraph is source.bundle.paragraphs.paragraphs[0]
    assert note.note_text == "This wording may matter later."
