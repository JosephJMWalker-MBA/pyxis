from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static

from pyxis.app.chromium_research_revision_edge_working_set_presentation import (
    ChromiumPageResearchRationaleWorkingSetPresentation,
    ChromiumPageResearchSourceExcerptPresentation,
    ChromiumPageResearchWorkingSetMemberPresentation,
)


_PRESENTATION_MODE = "read_only_declared_rationale_working_set_context"
_WORKING_SET_MODE = "caller_explicit_ordered_relinked_research_working_set"
_EDGE_FORMAT = "pyxis.chromium.research_working_set_note_revision_edge.v1"
_CAPTURE_FORMAT = "pyxis.chromium.research_capture.v1"
_OFFSET_UNIT = "unicode_code_point"

ATTACHMENT_NOTICE = (
    "Attached human working set. Attachment records what the rationale was authored "
    "about; it does not mean the source evidence proves or supports the rationale."
)


def _is_sha256(value: object) -> bool:
    return (
        type(value) is str
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _require_rationale_working_set_presentation(
    presentation: ChromiumPageResearchRationaleWorkingSetPresentation,
) -> None:
    if not isinstance(presentation, ChromiumPageResearchRationaleWorkingSetPresentation):
        raise TypeError(
            "presentation must be ChromiumPageResearchRationaleWorkingSetPresentation."
        )
    if presentation.presentation_mode != _PRESENTATION_MODE:
        raise ValueError("Rationale working-set presentation mode is unsupported.")
    if not _is_sha256(presentation.declaration_record_sha256):
        raise ValueError("Rationale working-set declaration SHA-256 is invalid.")
    if type(presentation.declared_position) is not int or presentation.declared_position < 1:
        raise ValueError("Rationale working-set declared position is invalid.")
    if presentation.edge_format != _EDGE_FORMAT:
        raise ValueError("Rationale working-set edge format is unsupported.")
    if not _is_sha256(presentation.edge_record_sha256):
        raise ValueError("Rationale working-set edge SHA-256 is invalid.")
    if type(presentation.rationale_text) is not str:
        raise TypeError("Rationale working-set rationale text must be a string.")
    if presentation.working_set_mode != _WORKING_SET_MODE:
        raise ValueError("Rationale working-set mode is unsupported.")
    if not presentation.members:
        raise ValueError("Rationale working-set presentation must contain members.")

    for expected_position, member in enumerate(presentation.members, start=1):
        _require_member(member, expected_position=expected_position)


def _require_member(
    member: ChromiumPageResearchWorkingSetMemberPresentation,
    *,
    expected_position: int,
) -> None:
    if not isinstance(member, ChromiumPageResearchWorkingSetMemberPresentation):
        raise TypeError("Working-set members must use the 27C presentation type.")
    if member.member_position != expected_position:
        raise ValueError("Working-set member positions must remain contiguous.")
    if type(member.human_note_text) is not str:
        raise TypeError("Working-set human note text must be a string.")

    expected: tuple[str, tuple[str, ...], tuple[str, ...]]
    if member.member_kind == "paragraph_note":
        expected = ("paragraph_note", ("paragraph",), ("returned_paragraph_prefix",))
    elif member.member_kind == "exact_range_note":
        expected = ("exact_range_note", ("selection",), ("exact_returned_text_range",))
    elif member.member_kind == "comparison_note":
        expected = (
            "comparison_note",
            ("first_selection", "second_selection"),
            ("exact_returned_text_range", "exact_returned_text_range"),
        )
    else:
        raise ValueError("Working-set member kind is unsupported.")

    roles = expected[1]
    kinds = expected[2]
    if len(member.excerpts) != len(roles):
        raise ValueError("Working-set member excerpt count is incoherent with its kind.")
    for excerpt, role, kind in zip(member.excerpts, roles, kinds):
        _require_excerpt(excerpt, expected_role=role, expected_kind=kind)


def _require_excerpt(
    excerpt: ChromiumPageResearchSourceExcerptPresentation,
    *,
    expected_role: str,
    expected_kind: str,
) -> None:
    if not isinstance(excerpt, ChromiumPageResearchSourceExcerptPresentation):
        raise TypeError("Source excerpts must use the 27C presentation type.")
    if excerpt.excerpt_role != expected_role:
        raise ValueError("Source excerpt role is incoherent with its working-set member.")
    if excerpt.source_capture_format != _CAPTURE_FORMAT:
        raise ValueError("Source excerpt capture format is unsupported.")
    if not _is_sha256(excerpt.source_bundle_sha256):
        raise ValueError("Source excerpt bundle SHA-256 is invalid.")
    if type(excerpt.url) is not str:
        raise TypeError("Source excerpt observed URL must be a string.")
    if type(excerpt.paragraph_ordinal) is not int or excerpt.paragraph_ordinal < 1:
        raise ValueError("Source excerpt paragraph ordinal is invalid.")
    if excerpt.excerpt_kind != expected_kind:
        raise ValueError("Source excerpt kind is incoherent with its working-set member.")
    if type(excerpt.text) is not str:
        raise TypeError("Source excerpt text must be a string.")
    if type(excerpt.paragraph_text_truncated) is not bool:
        raise TypeError("Source excerpt paragraph truncation flag must be boolean.")

    if expected_kind == "returned_paragraph_prefix":
        if (
            excerpt.offset_unit is not None
            or excerpt.start_offset is not None
            or excerpt.end_offset is not None
        ):
            raise ValueError("Paragraph-prefix source excerpt must not contain range offsets.")
        return

    if excerpt.offset_unit != _OFFSET_UNIT:
        raise ValueError("Exact-range source excerpt offset unit is unsupported.")
    if type(excerpt.start_offset) is not int or type(excerpt.end_offset) is not int:
        raise TypeError("Exact-range source excerpt offsets must be integers.")
    if excerpt.start_offset < 0 or excerpt.end_offset <= excerpt.start_offset:
        raise ValueError("Exact-range source excerpt offsets are invalid.")


def _excerpt_metadata(excerpt: ChromiumPageResearchSourceExcerptPresentation) -> str:
    lines = [
        f"Capture format: {excerpt.source_capture_format}",
        f"Capture bundle SHA-256: {excerpt.source_bundle_sha256}",
        f"Observed URL: {excerpt.url}",
        f"Paragraph ordinal: {excerpt.paragraph_ordinal}",
        "Parent paragraph text truncated: "
        + ("yes" if excerpt.paragraph_text_truncated else "no"),
    ]
    if excerpt.offset_unit is not None:
        lines.extend(
            (
                f"Offset unit: {excerpt.offset_unit}",
                f"Range: [{excerpt.start_offset}, {excerpt.end_offset})",
            )
        )
    return "\n".join(lines)


class ResearchRationaleWorkingSetDetail(Vertical):
    """Read-only Textual rendering of one already-produced 27C presentation."""

    DEFAULT_CSS = """
    ResearchRationaleWorkingSetDetail.research-context-collapsed {
        display: none;
    }

    ResearchRationaleWorkingSetDetail {
        width: 100%;
        height: auto;
        margin-top: 1;
        padding: 1 2;
        border: round $secondary;
    }

    .research-working-set-member,
    .research-source-excerpt {
        width: 100%;
        height: auto;
        margin-top: 1;
        padding: 1 2;
        border: round $secondary;
    }

    .research-working-set-context-title,
    .research-working-set-member-title,
    .research-working-set-note-label,
    .research-source-excerpt-title,
    .research-rationale-context-label {
        text-style: bold;
    }
    """

    def __init__(
        self,
        presentation: ChromiumPageResearchRationaleWorkingSetPresentation,
        *,
        collapsed: bool = False,
    ) -> None:
        _require_rationale_working_set_presentation(presentation)
        classes = "research-context-collapsed" if collapsed else None
        super().__init__(
            id=f"research-rationale-working-set-{presentation.declared_position}",
            classes=classes,
        )
        self.presentation = presentation

    def compose(self) -> ComposeResult:
        presentation = self.presentation
        yield Static(
            f"Attached working set for declared position {presentation.declared_position}",
            classes="research-working-set-context-title",
            markup=False,
        )
        yield Static(ATTACHMENT_NOTICE, markup=False)
        yield Static(
            "\n".join(
                (
                    f"Declaration SHA-256: {presentation.declaration_record_sha256}",
                    f"Edge format: {presentation.edge_format}",
                    f"Edge SHA-256: {presentation.edge_record_sha256}",
                )
            ),
            classes="evidence-body",
            markup=False,
        )
        yield Static(
            "Human-authored rationale — not source evidence",
            classes="research-rationale-context-label",
            markup=False,
        )
        yield Static(
            presentation.rationale_text,
            classes="research-rationale-context-text",
            markup=False,
        )

        for member in presentation.members:
            with Vertical(classes="research-working-set-member"):
                yield Static(
                    f"Working-set member {member.member_position}: {member.member_kind}",
                    classes="research-working-set-member-title",
                    markup=False,
                )
                yield Static(
                    "Human note on selected source evidence — not source evidence",
                    classes="research-working-set-note-label",
                    markup=False,
                )
                yield Static(
                    member.human_note_text,
                    classes="research-working-set-note-text",
                    markup=False,
                )
                for excerpt in member.excerpts:
                    with Vertical(classes="research-source-excerpt"):
                        if excerpt.excerpt_kind == "returned_paragraph_prefix":
                            label = (
                                "Bounded returned paragraph prefix — not a verified quotation"
                            )
                        else:
                            label = (
                                "Exact returned text range — not a verified quotation"
                            )
                        yield Static(
                            f"{excerpt.excerpt_role}: {label}",
                            classes="research-source-excerpt-title",
                            markup=False,
                        )
                        yield Static(
                            _excerpt_metadata(excerpt),
                            classes="research-source-excerpt-metadata",
                            markup=False,
                        )
                        yield Static(
                            excerpt.text,
                            classes="research-source-excerpt-text",
                            markup=False,
                        )
