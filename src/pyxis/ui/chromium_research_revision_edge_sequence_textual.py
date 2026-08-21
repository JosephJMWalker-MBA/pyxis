from __future__ import annotations

from collections.abc import Iterable

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Static

from pyxis.app.chromium_research_revision_edge_working_set_presentation import (
    ChromiumPageResearchRationaleWorkingSetPresentation,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_sequence_presentation import (
    ChromiumPageResearchRevisionEdgeSequenceMemberPresentation,
    ChromiumPageResearchRevisionEdgeSequencePresentation,
)

from .chromium_research_rationale_working_set_textual import (
    ResearchRationaleWorkingSetDetail,
    _require_rationale_working_set_presentation,
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


def _snapshot_working_set_contexts(
    presentation: ChromiumPageResearchRevisionEdgeSequencePresentation,
    contexts: Iterable[ChromiumPageResearchRationaleWorkingSetPresentation],
) -> tuple[ChromiumPageResearchRationaleWorkingSetPresentation, ...]:
    try:
        frozen = tuple(contexts)
    except TypeError as exc:
        raise TypeError("working_set_contexts must be an iterable of 27C presentations.") from exc

    seen_positions: set[int] = set()
    for context in frozen:
        _require_rationale_working_set_presentation(context)
        position = context.declared_position
        if position in seen_positions:
            raise ValueError("Working-set context declared positions must be unique.")
        if position > len(presentation.members):
            raise ValueError("Working-set context position is outside the displayed segment.")

        member = presentation.members[position - 1]
        if context.declaration_record_sha256 != presentation.declaration_record_sha256:
            raise ValueError("Working-set context references a different declaration.")
        if context.edge_format != member.edge_format:
            raise ValueError("Working-set context edge format does not match the displayed rationale.")
        if context.edge_record_sha256 != member.edge_record_sha256:
            raise ValueError("Working-set context edge identity does not match the displayed rationale.")
        if context.rationale_text != member.note_text:
            raise ValueError("Working-set context rationale text does not match the displayed rationale.")
        seen_positions.add(position)

    return frozen


def _format_identity(label: str, record_format: str, record_sha256: str) -> str:
    return "\n".join(
        (
            f"{label} format: {record_format}",
            f"{label} SHA-256: {record_sha256}",
        )
    )


class ResearchRevisionEdgeSequenceDetail(Vertical):
    """Read-only Textual rendering of 27A with optional explicit 27C context views.

    Context controls only reveal or hide already-produced presentation records. They
    perform no file reads, browser acquisition, research relinking, persistence,
    evidence mutation, chronology inference, semantic support analysis, or Workspace
    provenance association.
    """

    def __init__(
        self,
        presentation: ChromiumPageResearchRevisionEdgeSequencePresentation,
        *,
        working_set_contexts: Iterable[
            ChromiumPageResearchRationaleWorkingSetPresentation
        ] = (),
    ) -> None:
        _require_research_sequence_presentation(presentation)
        frozen_contexts = _snapshot_working_set_contexts(
            presentation,
            working_set_contexts,
        )
        super().__init__(id="research-revision-edge-sequence")
        self.presentation = presentation
        self.working_set_contexts = frozen_contexts
        self._contexts_by_position = {
            context.declared_position: context for context in frozen_contexts
        }

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

                context = self._contexts_by_position.get(member.declared_position)
                if context is not None:
                    yield Button(
                        "Inspect attached working set",
                        id=f"research-context-toggle-{member.declared_position}",
                        classes="research-context-toggle",
                    )
                    yield ResearchRationaleWorkingSetDetail(
                        context,
                        collapsed=True,
                    )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Reveal or hide one already-supplied 27C context presentation."""

        button_id = event.button.id
        prefix = "research-context-toggle-"
        if button_id is None or not button_id.startswith(prefix):
            return

        try:
            position = int(button_id[len(prefix) :])
        except ValueError:
            return

        detail = self.query_one(
            f"#research-rationale-working-set-{position}",
            ResearchRationaleWorkingSetDetail,
        )
        if detail.has_class("research-context-collapsed"):
            detail.remove_class("research-context-collapsed")
        else:
            detail.add_class("research-context-collapsed")
