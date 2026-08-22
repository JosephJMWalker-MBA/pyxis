from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from textual.app import ComposeResult
from textual.widgets import Button, Input, Static, TextArea

from pyxis.app.chromium_research_revision_edge_working_set_presentation import (
    ChromiumPageResearchRationaleWorkingSetPresentation,
)
from pyxis.app.chromium_research_session_controller import (
    ChromiumResearchSessionController,
)
from pyxis.app.chromium_research_session_presentation import (
    ChromiumPageResearchSessionPresentation,
    present_chromium_research_session,
)
from pyxis.app.chromium_research_session_rollover import (
    ChromiumResearchSessionRolloverResult,
    rollover_chromium_research_session_to_persisted_successor,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_sequence_presentation import (
    ChromiumPageResearchRevisionEdgeSequencePresentation,
)
from pyxis.app.controller import WorkspaceController
from pyxis.app.measurement_summary_presentation import (
    BuildAndRunMeasurementSummaryPresentation,
)
from pyxis.app.presentation import WorkspacePresentation

from .chromium_research_endpoint_revision_textual import (
    ResearchEndpointRevisionControls,
)
from .chromium_research_revision_edge_sequence_textual import (
    ResearchRevisionEdgeSequenceDetail,
    _require_research_sequence_presentation,
    _snapshot_working_set_contexts,
)
from .chromium_research_session_rollover_textual import (
    ResearchSessionRolloverControls,
    rollover_success_receipt,
)
from .workspace_shell import WorkspaceShell as _WorkspaceShell


_RESEARCH_SESSION_PRESENTATION_MODE = "read_only_complete_declared_research_session"


class WorkspaceShell(_WorkspaceShell):
    """Normal Pyxis shell with optional independently supplied research evidence.

    Research rationale and working-set context presentations mounted here remain
    deliberately independent of Repository Zero Workspace provenance. Callers may
    supply one governed research controller, one complete read-only research-session
    presentation, or the older split 27A/27C presentation form. The three forms are
    mutually exclusive.

    A controller may first write one explicit successor through 29A/29B and then,
    only after a separate explicit 30A/30B rollover choice, replace this shell's
    research surface with a new declared continuation session. That local adoption
    does not create global latest/current/head semantics or Workspace provenance.
    """

    CSS = (
        _WorkspaceShell.CSS
        + """
    #research-revision-edge-sequence,
    #research-endpoint-revision-controls,
    #research-session-rollover-controls,
    #research-rollover-success-receipt {
        width: 94%;
        height: auto;
        padding: 1 2;
        margin-top: 1;
        border: round $secondary;
    }

    #research-sequence-independence-notice,
    #research-sequence-declaration-identity,
    #research-sequence-starting-identity,
    .research-sequence-member,
    #research-endpoint-revision-authority-notice,
    #research-endpoint-revised-note-label,
    #research-endpoint-prior-edge-source-label,
    #research-endpoint-destination-label,
    #research-endpoint-revision-status,
    #research-session-rollover-authority-notice,
    #research-session-rollover-candidate,
    #research-session-rollover-successor-source-label,
    #research-session-rollover-declaration-destination-label,
    #research-session-rollover-status {
        margin-top: 1;
    }

    .research-sequence-member {
        width: 100%;
        height: auto;
        padding: 1 2;
        border: round $secondary;
    }

    .research-sequence-member-title,
    .research-sequence-note-label,
    #research-endpoint-revision-title,
    #research-endpoint-revised-note-label,
    #research-endpoint-prior-edge-source-label,
    #research-endpoint-destination-label,
    #research-session-rollover-title,
    #research-session-rollover-successor-source-label,
    #research-session-rollover-declaration-destination-label {
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

    .research-context-toggle,
    #persist-research-endpoint-revision,
    #rollover-research-session {
        margin-top: 1;
    }

    #research-endpoint-revised-note {
        width: 100%;
        height: 8;
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
        research_controller: ChromiumResearchSessionController | None = None,
        research_session: ChromiumPageResearchSessionPresentation | None = None,
        research_presentation: ChromiumPageResearchRevisionEdgeSequencePresentation | None = None,
        research_working_set_contexts: Iterable[
            ChromiumPageResearchRationaleWorkingSetPresentation
        ] = (),
    ) -> None:
        explicit_contexts = tuple(research_working_set_contexts)

        if research_controller is not None:
            if research_session is not None or research_presentation is not None or explicit_contexts:
                raise ValueError(
                    "research_controller cannot be combined with read-only research presentation inputs."
                )
            if not isinstance(research_controller, ChromiumResearchSessionController):
                raise TypeError(
                    "research_controller must be ChromiumResearchSessionController."
                )
            rebuilt_session = present_chromium_research_session(research_controller.loaded)
            if rebuilt_session != research_controller.presentation:
                raise ValueError(
                    "Research controller presentation is incoherent with its retained loaded evidence."
                )
            if (
                research_controller.last_endpoint_revision is not None
                and research_controller.last_endpoint_revision.prior_session
                is not research_controller.presentation
            ):
                raise ValueError(
                    "Research controller prior successful revision is incoherent with its retained session."
                )
            research_session = research_controller.presentation

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
        self.research_controller = research_controller
        self.research_session = research_session
        self.research_presentation = research_presentation
        self.research_working_set_contexts = frozen_contexts
        self.last_research_rollover: ChromiumResearchSessionRolloverResult | None = None

    def compose(self) -> ComposeResult:
        yield from super().compose()
        if self.research_presentation is not None:
            yield ResearchRevisionEdgeSequenceDetail(
                self.research_presentation,
                working_set_contexts=self.research_working_set_contexts,
            )
        if self.research_controller is not None:
            yield ResearchEndpointRevisionControls(
                self.research_controller.last_endpoint_revision
            )
            yield ResearchSessionRolloverControls(
                self.research_controller.last_endpoint_revision
            )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Route only governed research buttons; inherited handlers remain Textual-owned."""

        if event.button.id == "persist-research-endpoint-revision":
            event.stop()
            self.call_after_refresh(self._persist_research_endpoint_revision)
            return
        if event.button.id == "rollover-research-session":
            event.stop()
            self.call_after_refresh(self._rollover_research_session)

    async def _persist_research_endpoint_revision(self) -> None:
        if self.research_controller is None:
            return

        revised_note = self.query_one("#research-endpoint-revised-note", TextArea)
        prior_edge_source = self.query_one("#research-endpoint-prior-edge-source", Input)
        destination = self.query_one("#research-endpoint-destination", Input)
        status = self.query_one("#research-endpoint-revision-status", Static)

        if not prior_edge_source.value.strip():
            status.update("Write failed: explicit durable endpoint path is required.")
            return
        if not destination.value.strip():
            status.update("Write failed: explicit successor destination path is required.")
            return

        try:
            result = self.research_controller.persist_declared_endpoint_revision(
                revised_note.text,
                prior_edge_source=Path(prior_edge_source.value),
                destination=Path(destination.value),
            )
        except Exception as exc:
            status.update(f"Write failed: {exc}")
            return

        controls = self.query_one(
            "#research-endpoint-revision-controls",
            ResearchEndpointRevisionControls,
        )
        controls.lock_after_success(result)
        self.query_one(
            "#research-session-rollover-controls",
            ResearchSessionRolloverControls,
        ).enable_for_revision(result)

    async def _rollover_research_session(self) -> None:
        controller = self.research_controller
        if controller is None:
            return

        controls = self.query_one(
            "#research-session-rollover-controls",
            ResearchSessionRolloverControls,
        )
        status = self.query_one("#research-session-rollover-status", Static)
        chosen_revision = controls.candidate_revision
        if chosen_revision is None:
            status.update("Continuation failed: no displayed successor has been selected.")
            return

        successor_source = self.query_one(
            "#research-session-rollover-successor-source", Input
        )
        declaration_destination = self.query_one(
            "#research-session-rollover-declaration-destination", Input
        )
        if not successor_source.value.strip():
            status.update("Continuation failed: explicit successor edge path is required.")
            return
        if not declaration_destination.value.strip():
            status.update(
                "Continuation failed: explicit continuation declaration destination is required."
            )
            return

        try:
            result = rollover_chromium_research_session_to_persisted_successor(
                controller,
                chosen_revision,
                successor_edge_source=Path(successor_source.value),
                declaration_destination=Path(declaration_destination.value),
            )
        except Exception as exc:
            status.update(f"Continuation failed: {exc}")
            return

        await self._mount_research_rollover(result)

    async def _mount_research_rollover(
        self,
        result: ChromiumResearchSessionRolloverResult,
    ) -> None:
        """Replace only the research surface with one successful explicit continuation."""

        prior_controller = self.research_controller
        if prior_controller is None or result.prior_controller is not prior_controller:
            raise ValueError(
                "Research rollover result does not belong to the shell's exact prior controller."
            )

        continuation = result.continuation_controller
        rebuilt_session = present_chromium_research_session(continuation.loaded)
        if rebuilt_session != continuation.presentation:
            raise ValueError(
                "Continuation controller presentation is incoherent with retained loaded evidence."
            )

        new_session = continuation.presentation
        _require_research_sequence_presentation(new_session.sequence)
        new_contexts = _snapshot_working_set_contexts(
            new_session.sequence,
            new_session.working_set_contexts,
        )
        if len(new_contexts) != len(new_session.sequence.members):
            raise ValueError(
                "Continuation session must contain one context per declared position."
            )

        old_detail = self.query_one(
            "#research-revision-edge-sequence",
            ResearchRevisionEdgeSequenceDetail,
        )
        old_revision_controls = self.query_one(
            "#research-endpoint-revision-controls",
            ResearchEndpointRevisionControls,
        )
        old_rollover_controls = self.query_one(
            "#research-session-rollover-controls",
            ResearchSessionRolloverControls,
        )

        if len(self.query("#research-rollover-success-receipt")) != 0:
            await self.query_one("#research-rollover-success-receipt", Static).remove()
        await old_detail.remove()
        await old_revision_controls.remove()
        await old_rollover_controls.remove()

        self.research_controller = continuation
        self.research_session = new_session
        self.research_presentation = new_session.sequence
        self.research_working_set_contexts = new_contexts
        self.last_research_rollover = result

        await self.mount(
            Static(
                rollover_success_receipt(result),
                id="research-rollover-success-receipt",
                markup=False,
            )
        )
        await self.mount(
            ResearchRevisionEdgeSequenceDetail(
                new_session.sequence,
                working_set_contexts=new_contexts,
            )
        )
        await self.mount(ResearchEndpointRevisionControls())
        await self.mount(ResearchSessionRolloverControls())


def create_workspace_shell(
    presentation: WorkspacePresentation,
    *,
    controller: WorkspaceController | None = None,
    measurement_presentation: BuildAndRunMeasurementSummaryPresentation | None = None,
    research_controller: ChromiumResearchSessionController | None = None,
    research_session: ChromiumPageResearchSessionPresentation | None = None,
    research_presentation: ChromiumPageResearchRevisionEdgeSequencePresentation | None = None,
    research_working_set_contexts: Iterable[
        ChromiumPageResearchRationaleWorkingSetPresentation
    ] = (),
) -> WorkspaceShell:
    """Create the Pyxis shell with optional governed or read-only research evidence."""

    return WorkspaceShell(
        presentation,
        controller=controller,
        measurement_presentation=measurement_presentation,
        research_controller=research_controller,
        research_session=research_session,
        research_presentation=research_presentation,
        research_working_set_contexts=research_working_set_contexts,
    )
