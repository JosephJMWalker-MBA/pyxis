from __future__ import annotations

from textual.app import App, ComposeResult
from textual.widgets import Button, OptionList, Static, TextArea

from pyxis.app import (
    ChromiumPageResearchLoadedCaptureEvidence,
    ChromiumPageResearchParagraphSelectionEvidence,
    ChromiumPageResearchParagraphTextSelectionEvidence,
    select_chromium_research_capture_paragraph,
    select_chromium_research_paragraph_text,
)


AUTHORITY_NOTICE = (
    "Interactive selection operates only on bounded evidence already present in the "
    "explicit durable capture. It does not reacquire Chromium, expand truncated text, "
    "authenticate a source, verify a quotation, or attach interpretation."
)


def _paragraph_option_label(
    paragraph_ordinal: int,
    text_prefix: str,
    *,
    truncated: bool,
) -> str:
    preview = text_prefix.replace("\r", " ").replace("\n", " ")
    if len(preview) > 80:
        preview = preview[:77] + "..."
    suffix = " [returned prefix truncated]" if truncated else ""
    return f"{paragraph_ordinal}: {preview}{suffix}"


def _capture_notice(source: ChromiumPageResearchLoadedCaptureEvidence) -> str:
    paragraphs = source.bundle.paragraphs
    returned = len(paragraphs.paragraphs)
    if paragraphs.truncated:
        return (
            f"Returned bounded paragraph evidence: {returned} of "
            f"{paragraphs.paragraph_count} observed paragraphs. "
            "Paragraphs outside this returned prefix are unavailable here."
        )
    return f"Returned bounded paragraph evidence: {returned} paragraphs."


def _paragraph_metadata(
    selection: ChromiumPageResearchParagraphSelectionEvidence,
) -> str:
    paragraph = selection.paragraph
    returned_count = len(paragraph.text_prefix)
    return "\n".join(
        (
            f"Paragraph ordinal: {paragraph.ordinal}",
            f"Returned code points: {returned_count}",
            f"Observed code points: {paragraph.text_character_count}",
            "Returned text truncated: " + ("yes" if paragraph.truncated else "no"),
        )
    )


def selection_from_read_only_text_area(
    source: ChromiumPageResearchParagraphSelectionEvidence,
    text_area: TextArea,
) -> ChromiumPageResearchParagraphTextSelectionEvidence:
    """Convert one exact Textual selection into the established public 18A type."""

    if not isinstance(source, ChromiumPageResearchParagraphSelectionEvidence):
        raise TypeError(
            "source must be ChromiumPageResearchParagraphSelectionEvidence."
        )
    if not isinstance(text_area, TextArea):
        raise TypeError("text_area must be TextArea.")
    if not text_area.read_only:
        raise ValueError("Interactive source text must remain read-only.")

    source_text = source.paragraph.text_prefix
    if text_area.text != source_text:
        raise ValueError(
            "Interactive source text no longer exactly matches the loaded paragraph prefix."
        )

    selected = text_area.selection
    if selected.is_empty:
        raise ValueError("Select a non-empty exact text range before saving.")

    first = text_area.document.get_index_from_location(selected.start)
    second = text_area.document.get_index_from_location(selected.end)
    start_offset, end_offset = sorted((first, second))
    if start_offset == end_offset:
        raise ValueError("Select a non-empty exact text range before saving.")

    expected_text = source_text[start_offset:end_offset]
    if text_area.selected_text != expected_text:
        raise ValueError(
            "Interactive selected text is incoherent with the derived source coordinates."
        )

    return select_chromium_research_paragraph_text(
        source,
        start_offset=start_offset,
        end_offset=end_offset,
    )


class ResearchCapturePassageSelectionApp(
    App[ChromiumPageResearchParagraphTextSelectionEvidence | None]
):
    """Human coordinate-entry surface over one already-loaded durable capture."""

    TITLE = "Pyxis"
    SUB_TITLE = "Select exact saved passage"
    BINDINGS = [("escape", "cancel", "Cancel")]
    CSS = """
    Screen {
        align: center top;
    }

    #research-capture-selection-title,
    #research-capture-selection-notice,
    #research-capture-selection-options,
    #research-capture-selection-metadata,
    #research-capture-selection-text,
    #research-capture-selection-actions,
    #research-capture-selection-status {
        width: 94%;
        margin-top: 1;
    }

    #research-capture-selection-title {
        text-style: bold;
    }

    #research-capture-selection-options {
        height: 10;
    }

    #research-capture-selection-text {
        height: 16;
        border: round $secondary;
    }

    #research-capture-selection-actions {
        height: auto;
    }
    """

    def __init__(self, source: ChromiumPageResearchLoadedCaptureEvidence) -> None:
        if not isinstance(source, ChromiumPageResearchLoadedCaptureEvidence):
            raise TypeError(
                "source must be ChromiumPageResearchLoadedCaptureEvidence."
            )
        if not source.bundle.paragraphs.paragraphs:
            raise ValueError(
                "Capture contains no returned paragraph evidence available for selection."
            )
        super().__init__()
        self.source = source
        self.paragraph_selection = select_chromium_research_capture_paragraph(
            source,
            paragraph_ordinal=1,
        )

    def compose(self) -> ComposeResult:
        paragraphs = self.source.bundle.paragraphs.paragraphs
        yield Static(
            "Select one exact returned passage",
            id="research-capture-selection-title",
        )
        yield Static(
            AUTHORITY_NOTICE + "\n" + _capture_notice(self.source),
            id="research-capture-selection-notice",
            markup=False,
        )
        yield OptionList(
            *(
                _paragraph_option_label(
                    paragraph.ordinal,
                    paragraph.text_prefix,
                    truncated=paragraph.truncated,
                )
                for paragraph in paragraphs
            ),
            id="research-capture-selection-options",
        )
        yield Static(
            _paragraph_metadata(self.paragraph_selection),
            id="research-capture-selection-metadata",
            markup=False,
        )
        yield TextArea(
            self.paragraph_selection.paragraph.text_prefix,
            id="research-capture-selection-text",
            read_only=True,
            show_line_numbers=False,
            soft_wrap=True,
        )
        yield Static(
            "Select text in the read-only passage, then confirm the exact range.",
            id="research-capture-selection-actions",
            markup=False,
        )
        yield Button(
            "Use exact selected range",
            id="research-capture-selection-confirm",
            variant="success",
        )
        yield Button(
            "Cancel",
            id="research-capture-selection-cancel",
        )
        yield Static(
            "",
            id="research-capture-selection-status",
            markup=False,
        )

    def on_mount(self) -> None:
        options = self.query_one("#research-capture-selection-options", OptionList)
        options.highlighted = 0

    def on_option_list_option_selected(
        self,
        event: OptionList.OptionSelected,
    ) -> None:
        ordinal = event.option_index + 1
        self.paragraph_selection = select_chromium_research_capture_paragraph(
            self.source,
            paragraph_ordinal=ordinal,
        )
        text_area = self.query_one("#research-capture-selection-text", TextArea)
        text_area.load_text(self.paragraph_selection.paragraph.text_prefix)
        self.query_one("#research-capture-selection-metadata", Static).update(
            _paragraph_metadata(self.paragraph_selection)
        )
        self.query_one("#research-capture-selection-status", Static).update("")
        text_area.focus()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "research-capture-selection-cancel":
            self.exit(None)
            return
        if event.button.id != "research-capture-selection-confirm":
            return

        status = self.query_one("#research-capture-selection-status", Static)
        text_area = self.query_one("#research-capture-selection-text", TextArea)
        try:
            selection = selection_from_read_only_text_area(
                self.paragraph_selection,
                text_area,
            )
        except (TypeError, ValueError) as exc:
            status.update(f"Selection not saved: {exc}")
            return
        self.exit(selection)

    def action_cancel(self) -> None:
        self.exit(None)


def create_chromium_research_capture_selection_app(
    source: ChromiumPageResearchLoadedCaptureEvidence,
) -> ResearchCapturePassageSelectionApp:
    return ResearchCapturePassageSelectionApp(source)


def run_chromium_research_capture_selection(
    source: ChromiumPageResearchLoadedCaptureEvidence,
) -> ChromiumPageResearchParagraphTextSelectionEvidence | None:
    return create_chromium_research_capture_selection_app(source).run()


__all__ = [
    "AUTHORITY_NOTICE",
    "ResearchCapturePassageSelectionApp",
    "create_chromium_research_capture_selection_app",
    "run_chromium_research_capture_selection",
    "selection_from_read_only_text_area",
]
