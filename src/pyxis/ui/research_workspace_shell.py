from __future__ import annotations

from collections.abc import Iterable

from textual.app import ComposeResult

from pyxis.app.chromium_research_revision_edge_working_set_presentation import (
    ChromiumPageResearchRationaleWorkingSetPresentation,
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


class WorkspaceShell(_WorkspaceShell):
    """Normal Pyxis shell with optional independently supplied research evidence.

    Research rationale and working-set context presentations mounted here remain
    deliberately independent of Repository Zero Workspace provenance. Context
    controls reveal or hide already-produced presentation evidence only; this
    wrapper performs no browser/file acquisition, research relinking, semantic
    analysis, or evidence mutation.
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

    Button[id^="research-context-toggle-"] {
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
        research_presentation: ChromiumPageResearchRevisionEdgeSequencePresentation | None = None,
        research_working_set_contexts: Iterable[
            ChromiumPageResearchRationaleWorkingSetPresentation
        ] = (),
    ) -> None:
        if research_presentation is None:
            frozen_contexts = tuple(research_working_set_contexts)
            if frozen_contexts:
                raise ValueError(
                    "research_working_set_contexts require a research_presentation."
                )
        else:
            _require_research_sequence_presentation(research_presentation)
            frozen_contexts = _snapshot_working_set_contexts(
                research_presentation,
                research_working_set_contexts,
            )

        super().__init__(
            presentation,
            controller=controller,
            measurement_presentation=measurement_presentation,
        )
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
        research_presentation=research_presentation,
        research_working_set_contexts=research_working_set_contexts,
    )
