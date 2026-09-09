from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest
from textual.widgets import OptionList, TextArea
from textual.widgets.text_area import Selection

from pyxis.app import (
    load_chromium_page_research_capture,
    persist_chromium_page_research_capture,
    select_chromium_research_capture_paragraph,
)
from pyxis.app.chromium_paragraphs import (
    ChromiumPageParagraphEvidence,
    ChromiumPageParagraphsEvidence,
)
from pyxis.ui.chromium_research_capture_selection_textual import (
    ResearchCapturePassageSelectionApp,
    selection_from_read_only_text_area,
)
from test_app_chromium_research_capture import ENDPOINT, TARGET_ID, URL, _bundle


def _loaded_capture(
    tmp_path: Path,
    texts: tuple[str, ...],
    *,
    character_counts: tuple[int, ...] | None = None,
    paragraph_count: int | None = None,
):
    base = _bundle()
    counts = character_counts or tuple(len(text) for text in texts)
    paragraphs = tuple(
        ChromiumPageParagraphEvidence(
            ordinal=index,
            element_id=f"p-{index}",
            text_prefix=text,
            text_character_count=counts[index - 1],
            text_limit=max(64, len(text)),
            truncated=counts[index - 1] > len(text),
        )
        for index, text in enumerate(texts, start=1)
    )
    observed_count = paragraph_count if paragraph_count is not None else len(paragraphs)
    paragraph_evidence = ChromiumPageParagraphsEvidence(
        endpoint=ENDPOINT,
        target_id=TARGET_ID,
        url=URL,
        source="document.querySelectorAll('p')",
        paragraphs=paragraphs,
        paragraph_count=observed_count,
        paragraph_limit=128,
        truncated=observed_count > len(paragraphs),
    )
    bundle = replace(base, paragraphs=paragraph_evidence)
    path = tmp_path / "capture.json"
    persist_chromium_page_research_capture(bundle, path)
    return load_chromium_page_research_capture(path)


@pytest.mark.parametrize(
    "selection",
    [
        Selection(start=(0, 1), end=(0, 5)),
        Selection(start=(0, 5), end=(0, 1)),
    ],
)
def test_51b_textual_selection_maps_forward_and_reverse_unicode_locations_to_same_18a(
    tmp_path: Path,
    selection: Selection,
) -> None:
    text = "Aé😀e\u0301Z"
    source = _loaded_capture(tmp_path, (text,))
    paragraph = select_chromium_research_capture_paragraph(
        source,
        paragraph_ordinal=1,
    )
    text_area = TextArea(text, read_only=True)
    text_area.selection = selection

    result = selection_from_read_only_text_area(paragraph, text_area)

    assert result.source is paragraph
    assert result.start_offset == 1
    assert result.end_offset == 5
    assert result.offset_unit == "unicode_code_point"
    assert result.selected_text == "é😀e\u0301"


def test_51b_textual_selection_maps_line_locations_through_exact_document_index(
    tmp_path: Path,
) -> None:
    text = "A😀\nBé"
    source = _loaded_capture(tmp_path, (text,))
    paragraph = select_chromium_research_capture_paragraph(
        source,
        paragraph_ordinal=1,
    )
    text_area = TextArea(text, read_only=True)
    text_area.selection = Selection(start=(0, 1), end=(1, 1))

    result = selection_from_read_only_text_area(paragraph, text_area)

    assert result.start_offset == 1
    assert result.end_offset == 4
    assert result.selected_text == "😀\nB"


def test_51b_textual_selection_rejects_empty_range(tmp_path: Path) -> None:
    source = _loaded_capture(tmp_path, ("Alpha",))
    paragraph = select_chromium_research_capture_paragraph(source, paragraph_ordinal=1)
    text_area = TextArea("Alpha", read_only=True)
    text_area.selection = Selection.cursor((0, 2))

    with pytest.raises(ValueError, match="non-empty"):
        selection_from_read_only_text_area(paragraph, text_area)


def test_51b_textual_selection_requires_read_only_exact_source_text(
    tmp_path: Path,
) -> None:
    source = _loaded_capture(tmp_path, ("Alpha",))
    paragraph = select_chromium_research_capture_paragraph(source, paragraph_ordinal=1)

    editable = TextArea("Alpha", read_only=False)
    editable.selection = Selection(start=(0, 0), end=(0, 1))
    with pytest.raises(ValueError, match="read-only"):
        selection_from_read_only_text_area(paragraph, editable)

    mismatched = TextArea("ALPHA", read_only=True)
    mismatched.selection = Selection(start=(0, 0), end=(0, 1))
    with pytest.raises(ValueError, match="exactly matches"):
        selection_from_read_only_text_area(paragraph, mismatched)


def test_51b_textual_mixed_line_ending_normalization_fails_closed_if_text_changes(
    tmp_path: Path,
) -> None:
    text = "A\r\nB\nC"
    source = _loaded_capture(tmp_path, (text,))
    paragraph = select_chromium_research_capture_paragraph(source, paragraph_ordinal=1)
    text_area = TextArea(text, read_only=True)
    text_area.selection = Selection(start=(0, 0), end=(1, 1))

    if text_area.text != text:
        with pytest.raises(ValueError, match="exactly matches"):
            selection_from_read_only_text_area(paragraph, text_area)
    else:
        result = selection_from_read_only_text_area(paragraph, text_area)
        assert result.selected_text == text_area.selected_text


def test_51b_app_exposes_only_returned_bounded_paragraphs_and_read_only_text(
    tmp_path: Path,
) -> None:
    source = _loaded_capture(
        tmp_path,
        ("First returned paragraph", "Second returned prefix"),
        character_counts=(24, 40),
        paragraph_count=5,
    )
    app = ResearchCapturePassageSelectionApp(source)
    widgets = list(app.compose())

    option_list = next(widget for widget in widgets if isinstance(widget, OptionList))
    text_area = next(widget for widget in widgets if isinstance(widget, TextArea))

    assert option_list.option_count == 2
    assert text_area.read_only is True
    assert text_area.text == "First returned paragraph"
    assert app.paragraph_selection.paragraph is source.bundle.paragraphs.paragraphs[0]


def test_51b_app_rejects_capture_with_no_returned_paragraph_evidence(
    tmp_path: Path,
) -> None:
    source = _loaded_capture(tmp_path, (), paragraph_count=3)

    with pytest.raises(ValueError, match="no returned paragraph evidence"):
        ResearchCapturePassageSelectionApp(source)



@pytest.mark.asyncio
async def test_51b_headless_app_selects_second_returned_paragraph_and_exits_exact_18a(
    tmp_path: Path,
) -> None:
    source = _loaded_capture(
        tmp_path,
        ("First paragraph", "Second returned prefix"),
    )
    app = ResearchCapturePassageSelectionApp(source)

    async with app.run_test() as pilot:
        options = app.query_one("#research-capture-selection-options", OptionList)
        options.highlighted = 1
        options.action_select()
        await pilot.pause()

        assert app.paragraph_selection.paragraph is source.bundle.paragraphs.paragraphs[1]
        text_area = app.query_one("#research-capture-selection-text", TextArea)
        assert text_area.text == "Second returned prefix"
        assert text_area.read_only is True
        text_area.selection = Selection(start=(0, 7), end=(0, 15))
        await pilot.pause()
        await pilot.click("#research-capture-selection-confirm")

    result = app.return_value
    assert result is not None
    assert result.source is app.paragraph_selection
    assert result.source.source is source
    assert result.start_offset == 7
    assert result.end_offset == 15
    assert result.selected_text == "returned"
