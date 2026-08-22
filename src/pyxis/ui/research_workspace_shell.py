from __future__ import annotations

from collections.abc import Iterable

from textual.app import ComposeResult

from pyxis.app.chromium_research_revision_edge_working_set_presentation import (
    ChromiumPageResearchRationaleWorkingSetPresentation,
)
from pyxis.app.chromium_research_session_presentation import (
    ChromiumPageResearchSessionPresentation,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_sequence_presentation import (
    ChromiumPageResearchRevisionEdgeSequencePresentation,
)
from pyxis.app.controller import WorkspaceController
from pyxis.app.measurement_summary_presentation import (
    BuildAndRunMeasurementSummaryPresentation,
)
from pyxis.app.presentation import WorkspacePresentation

from .chromium_research_revision_edge_sequence_textual import (
    ResearchRevisionEdgeSequenceDetail,
    _require_research_sequence_presentation,
    _snapshot_working_set_contexts,
)
from .workspace_shell import WorkspaceShell as _WorkspaceShell


_RESEARCH_SESSION_PRESENTATION_MODE = "read_only_complete_declared_research_session"


class WorkspaceShell(_WorkspaceShell):
    """Normal Pyxis shell with optional independently supplied research evidence.

    Research rationale and working-set context presentations mounted here remain
    deliberately independent of Repository Zero Workspace provenance. Callers may
    supply either one complete 28A research-session presentation or the older split
    27A/27C presentation form. Context controls reveal or hide already-produced
    presentation evidence only; this wrapper performs no browser/file acquisition,
    research relinking, semantic analysis, or evidence mutation.
    """

    CSS = (
        _WorkspaceShell.CSS
        + """
    #research-revision-edge-sequence {
        width: 94%;
        height: auto;
        padding: 1 2;
        margin-top: 1;
        border: round $secondary;
    }

    #research-sequence-independence-notice,
    #research-sequence-declaration-identity,
    #research-sequence-starting-identity,
    .research-sequence-member {
        margin-top: 1;
    }

    .research-sequence-member {
        width: 100%;
        height: auto;
        padding: 1 2;
        border: round $secondary;
    }

    .research-sequence-member-title,
    .research-sequence-note-label {
        text-style: bold;
    }

    .research-sequence-note-text,
    .research-working-set-note-text,
    .research-source-excerpt-text,
    .research-rationale-context-text {
        width: 100%;
        height: auto;
        margin-top: 1;
    }

    .research-context-toggle {
        margin-top: 1;
    }
    """
    )

    def __init__(
        self,
        presentation: WorkspacePresentation,
        *,
        controller: WorkspaceController | None = None,
        measurement_presentation: BuildAndRunMeasurementSummaryPresentation | None = None,
        research_session: ChromiumPageResearchSessionPresentation | None = None,
        research_presentation: ChromiumPageResearchRevisionEdgeSequencePresentation | None = None,
        research_working_set_contexts: Iterable[
            ChromiumPageResearchRationaleWorkingSetPresentation
        ] = (),
    ) -> None:
        explicit_contexts = tuple(research_working_set_contexts)

        if research_session is not None:
            if research_presentation is not None or explicit_contexts:
                raise ValueError(
                    "research_session cannot be combined with split research presentation inputs."
                )
            if not isinstance(research_session, ChromiumPageResearchSessionPresentation):
                raise TypeError(
                    "research_session must be ChromiumPageResearchSessionPresentation."
                )
            if research_session.presentation_mode != _RESEARCH_SESSION_PRESENTATION_MODE:
                raise ValueError("Research session presentation mode is unsupported.")

            session_sequence = research_session.sequence
            _require_research_sequence_presentation(session_sequence)
            session_contexts = _snapshot_working_set_contexts(
                session_sequence,
                research_session.working_set_contexts,
            )
            if len(session_contexts) != len(session_sequence.members):
                raise ValueError(
                    "Complete research session must contain one context per declared position."
                )

            research_presentation = session_sequence
            frozen_contexts = session_contexts
        elif research_presentation is None:
            if explicit_contexts:
                raise ValueError(
                    "research_working_set_contexts require a research_presentation."
                )
            frozen_contexts = ()
        else:
            _require_research_sequence_presentation(research_presentation)
            frozen_contexts = _snapshot_working_set_contexts(
                research_presentation,
                explicit_contexts,
            )

        super().__init__(
            presentation,
            controller=controller,
            measurement_presentation=measurement_presentation,
        )
        self.research_session = research_session
        self.research_presentation = research_presentation
        self.research_working_set_contexts = frozen_contexts

    def compose(self) -> ComposeResult:
        yield from super().compose()
        if self.research_presentation is not None:
            yield ResearchRevisionEdgeSequenceDetail(
                self.research_presentation,
                working_set_contexts=self.research_working_set_contexts,
            )


def create_workspace_shell(
    presentation: WorkspacePresentation,
    *,
    controller: WorkspaceController | None = None,
    measurement_presentation: BuildAndRunMeasurementSummaryPresentation | None = None,
    research_session: ChromiumPageResearchSessionPresentation | None = None,
    research_presentation: ChromiumPageResearchRevisionEdgeSequencePresentation | None = None,
    research_working_set_contexts: Iterable[
        ChromiumPageResearchRationaleWorkingSetPresentation
    ] = (),
) -> WorkspaceShell:
    """Create the Pyxis shell with optional independent read-only research evidence."""

    return WorkspaceShell(
        presentation,
        controller=controller,
        measurement_presentation=measurement_presentation,
        research_session=research_session,
        research_presentation=research_presentation,
        research_working_set_contexts=research_working_set_contexts,
    )
