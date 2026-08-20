from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static

from pyxis.app.chromium_research_working_set_note_revision_edge_sequence_presentation import (
    ChromiumPageResearchRevisionEdgeSequenceMemberPresentation,
    ChromiumPageResearchRevisionEdgeSequencePresentation,
)


_PRESENTATION_MODE = (
    "read_only_verified_declared_research_working_set_note_revision_edge_sequence"
)
_SEQUENCE_MODE = (
    "caller_explicit_ordered_relinked_research_working_set_note_revision_edge_sequence"
)
_EDGE_FORMAT = "pyxis.chromium.research_working_set_note_revision_edge.v1"


INDEPENDENT_RESEARCH_NOTICE = (
    "Independently supplied research evidence. Displayed alongside Workspace evidence; "
    "no association with this Workspace is asserted."
)


def _require_research_sequence_presentation(
    presentation: ChromiumPageResearchRevisionEdgeSequencePresentation,
) -> None:
    if not isinstance(presentation, ChromiumPageResearchRevisionEdgeSequencePresentation):
        raise TypeError(
            "presentation must be ChromiumPageResearchRevisionEdgeSequencePresentation."
        )
    if presentation.presentation_mode != _PRESENTATION_MODE:
        raise ValueError("Research sequence presentation mode is unsupported.")
    if presentation.sequence_mode != _SEQUENCE_MODE:
        raise ValueError("Research sequence presentation sequence mode is unsupported.")
    if not presentation.members:
        raise ValueError("Research sequence presentation must contain at least one member.")

    expected_position = 1
    for member in presentation.members:
        _require_member(member, expected_position=expected_position)
        expected_position += 1


def _require_member(
    member: ChromiumPageResearchRevisionEdgeSequenceMemberPresentation,
    *,
    expected_position: int,
) -> None:
    if not isinstance(member, ChromiumPageResearchRevisionEdgeSequenceMemberPresentation):
        raise TypeError("Research sequence members must use the 27A presentation type.")
    if member.declared_position != expected_position:
        raise ValueError(
            "Research sequence member positions must remain contiguous declaration positions."
        )
    if member.edge_format != _EDGE_FORMAT:
        raise ValueError("Research sequence member edge format is unsupported.")


def _format_identity(label: str, record_format: str, record_sha256: str) -> str:
    return "\n".join(
        (
            f"{label} format: {record_format}",
            f"{label} SHA-256: {record_sha256}",
        )
    )


class ResearchRevisionEdgeSequenceDetail(Vertical):
    """Read-only Textual rendering of one already-produced 27A presentation.

    This widget consumes presentation evidence only. It performs no file reads,
    browser acquisition, persistence, mutation, chronology inference, head
    selection, source validation, or semantic analysis. The surrounding Workspace
    shell does not imply that this independently supplied research segment belongs
    to the rendered Workspace.
    """

    def __init__(
        self,
        presentation: ChromiumPageResearchRevisionEdgeSequencePresentation,
    ) -> None:
        _require_research_sequence_presentation(presentation)
        super().__init__(id="research-revision-edge-sequence")
        self.presentation = presentation

    def compose(self) -> ComposeResult:
        presentation = self.presentation

        yield Static(
            "Verified research rationale segment",
            id="research-sequence-title",
            classes="section-title",
        )
        yield Static(
            INDEPENDENT_RESEARCH_NOTICE,
            id="research-sequence-independence-notice",
            markup=False,
        )
        yield Static(
            _format_identity(
                "Declaration",
                presentation.declaration_format,
                presentation.declaration_record_sha256,
            ),
            id="research-sequence-declaration-identity",
            classes="evidence-body",
            markup=False,
        )
        yield Static(
            _format_identity(
                "Starting record",
                presentation.starting_record_format,
                presentation.starting_record_sha256,
            ),
            id="research-sequence-starting-identity",
            classes="evidence-body",
            markup=False,
        )

        for member in presentation.members:
            with Vertical(
                id=f"research-sequence-member-{member.declared_position}",
                classes="research-sequence-member",
            ):
                yield Static(
                    f"Declared position {member.declared_position} — not a global revision number",
                    classes="research-sequence-member-title",
                    markup=False,
                )
                yield Static(
                    _format_identity(
                        "Edge",
                        member.edge_format,
                        member.edge_record_sha256,
                    ),
                    classes="research-sequence-member-identity",
                    markup=False,
                )
                yield Static(
                    "Human-authored rationale — not source evidence",
                    classes="research-sequence-note-label",
                    markup=False,
                )
                yield Static(
                    member.note_text,
                    id=f"research-sequence-note-{member.declared_position}",
                    classes="research-sequence-note-text",
                    markup=False,
                )
