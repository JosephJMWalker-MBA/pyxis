from __future__ import annotations

from pathlib import Path

from textual.app import App, ComposeResult
from textual.widgets import Button, Input, Static, TextArea

from pyxis.app.chromium_research_session_controller import ChromiumResearchSessionController
from pyxis.app.chromium_research_session_presentation import present_chromium_research_session
from pyxis.app.chromium_research_session_rollover import (
    ChromiumResearchSessionRolloverResult,
    rollover_chromium_research_session_to_persisted_successor,
)

from .chromium_research_endpoint_revision_textual import ResearchEndpointRevisionControls
from .chromium_research_revision_edge_sequence_textual import (
    ResearchRevisionEdgeSequenceDetail,
    _require_research_sequence_presentation,
    _snapshot_working_set_contexts,
)
from .chromium_research_session_rollover_textual import (
    ResearchSessionRolloverControls,
    rollover_success_receipt,
)


class ResearchSessionShell(App[None]):
    """Standalone governed Textual shell for one explicit research-session controller.

    This shell intentionally contains no Repository Zero Workspace presentation or
    Workspace controller. Research evidence and mutation authority come only from
    the supplied, freshly validated `ChromiumResearchSessionController`.
    """

    TITLE = "Pyxis"
    SUB_TITLE = "Governed research session"
    CSS = """
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

    def __init__(self, controller: ChromiumResearchSessionController) -> None:
        if not isinstance(controller, ChromiumResearchSessionController):
            raise TypeError("controller must be ChromiumResearchSessionController.")

        rebuilt_session = present_chromium_research_session(controller.loaded)
        if rebuilt_session != controller.presentation:
            raise ValueError(
                "Research controller presentation is incoherent with its retained loaded evidence."
            )
        if (
            controller.last_endpoint_revision is not None
            and controller.last_endpoint_revision.prior_session is not controller.presentation
        ):
            raise ValueError(
                "Research controller prior successful revision is incoherent with its retained session."
            )

        super().__init__()
        self.research_controller = controller
        self.research_session = controller.presentation
        self.research_presentation = controller.presentation.sequence
        self.research_working_set_contexts = _snapshot_working_set_contexts(
            controller.presentation.sequence,
            controller.presentation.working_set_contexts,
        )
        if len(self.research_working_set_contexts) != len(
            self.research_presentation.members
        ):
            raise ValueError(
                "Complete research session must contain one context per declared position."
            )
        self.last_research_rollover: ChromiumResearchSessionRolloverResult | None = None

    def compose(self) -> ComposeResult:
        yield ResearchRevisionEdgeSequenceDetail(
            self.research_presentation,
            working_set_contexts=self.research_working_set_contexts,
        )
        yield ResearchEndpointRevisionControls(
            self.research_controller.last_endpoint_revision
        )
        yield ResearchSessionRolloverControls(
            self.research_controller.last_endpoint_revision
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Route only the two governed research mutation actions."""

        if event.button.id == "persist-research-endpoint-revision":
            event.stop()
            self.call_after_refresh(self._persist_research_endpoint_revision)
            return
        if event.button.id == "rollover-research-session":
            event.stop()
            self.call_after_refresh(self._rollover_research_session)

    async def _persist_research_endpoint_revision(self) -> None:
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

        self.query_one(
            "#research-endpoint-revision-controls",
            ResearchEndpointRevisionControls,
        ).lock_after_success(result)
        self.query_one(
            "#research-session-rollover-controls",
            ResearchSessionRolloverControls,
        ).enable_for_revision(result)

    async def _rollover_research_session(self) -> None:
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
                self.research_controller,
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
        """Replace this standalone research surface after one explicit 30A success."""

        prior_controller = self.research_controller
        if result.prior_controller is not prior_controller:
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


def create_research_session_shell(
    controller: ChromiumResearchSessionController,
) -> ResearchSessionShell:
    """Create the standalone governed research shell from one exact controller."""

    return ResearchSessionShell(controller)
