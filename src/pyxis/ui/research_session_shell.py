from __future__ import annotations

from pathlib import Path

from textual.app import App, ComposeResult
from textual.widgets import Button, Input, Static, TextArea

from pyxis.app.chromium_research_session_continuation_reentry_plan import (
    ChromiumResearchSessionContinuationReentryPlanResult,
    persist_chromium_research_session_continuation_reentry_plan,
)
from pyxis.app.chromium_research_session_controller import ChromiumResearchSessionController
from pyxis.app.chromium_research_session_presentation import present_chromium_research_session
from pyxis.app.chromium_research_session_reentry import ChromiumResearchSessionReentryResult
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
from .chromium_research_session_restart_plan_textual import (
    ResearchSessionRestartPlanControls,
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

    An optional exact 31A re-entry result adds restart-lineage authority for the
    standalone product path. That lineage is never inferred from the controller.
    """

    TITLE = "Pyxis"
    SUB_TITLE = "Governed research session"
    CSS = """
    #research-revision-edge-sequence,
    #research-endpoint-revision-controls,
    #research-session-rollover-controls,
    #research-session-restart-plan-controls,
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
    #research-session-rollover-status,
    #research-session-restart-plan-authority-notice,
    #research-session-restart-plan-candidate,
    #research-session-restart-plan-successor-source-label,
    #research-session-restart-plan-declaration-source-label,
    #research-session-restart-plan-destination-label,
    #research-session-restart-plan-status {
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
    #research-session-rollover-declaration-destination-label,
    #research-session-restart-plan-title,
    #research-session-restart-plan-successor-source-label,
    #research-session-restart-plan-declaration-source-label,
    #research-session-restart-plan-destination-label {
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
    #rollover-research-session,
    #save-research-session-restart-plan {
        margin-top: 1;
    }

    #research-endpoint-revised-note {
        width: 100%;
        height: 8;
        margin-top: 1;
    }
    """

    def __init__(
        self,
        controller: ChromiumResearchSessionController,
        *,
        reentry: ChromiumResearchSessionReentryResult | None = None,
    ) -> None:
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
        if reentry is not None:
            _require_reentry_coherence(controller, reentry)

        super().__init__()
        self.research_controller = controller
        self.research_reentry = reentry
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
        self.last_research_restart_plan: (
            ChromiumResearchSessionContinuationReentryPlanResult | None
        ) = None

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
        """Route only the governed standalone research mutation/checkpoint actions."""

        if event.button.id == "persist-research-endpoint-revision":
            event.stop()
            self.call_after_refresh(self._persist_research_endpoint_revision)
            return
        if event.button.id == "rollover-research-session":
            event.stop()
            self.call_after_refresh(self._rollover_research_session)
            return
        if event.button.id == "save-research-session-restart-plan":
            event.stop()
            self.call_after_refresh(self._save_research_restart_plan)

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

    async def _save_research_restart_plan(self) -> None:
        controls = self.query_one(
            "#research-session-restart-plan-controls",
            ResearchSessionRestartPlanControls,
        )
        status = self.query_one("#research-session-restart-plan-status", Static)
        if self.research_reentry is None:
            status.update(
                "Restart-plan save failed: this shell was not supplied an explicit re-entry lineage."
            )
            return
        if self.last_research_rollover is None:
            status.update(
                "Restart-plan save failed: no explicit continuation rollover is awaiting a checkpoint."
            )
            return
        if controls.rollover is not self.last_research_rollover:
            status.update(
                "Restart-plan save failed: displayed checkpoint does not match the shell's exact rollover."
            )
            return

        successor_source = self.query_one(
            "#research-session-restart-plan-successor-source", Input
        )
        declaration_source = self.query_one(
            "#research-session-restart-plan-declaration-source", Input
        )
        destination = self.query_one(
            "#research-session-restart-plan-destination", Input
        )
        if not successor_source.value.strip():
            status.update(
                "Restart-plan save failed: explicit current successor edge path is required."
            )
            return
        if not declaration_source.value.strip():
            status.update(
                "Restart-plan save failed: explicit current continuation declaration path is required."
            )
            return
        if not destination.value.strip():
            status.update(
                "Restart-plan save failed: explicit no-overwrite restart plan destination is required."
            )
            return

        prior_reentry = self.research_reentry
        try:
            result = persist_chromium_research_session_continuation_reentry_plan(
                prior_reentry,
                self.last_research_rollover,
                successor_edge_source=Path(successor_source.value),
                continuation_declaration_source=Path(declaration_source.value),
                destination=Path(destination.value),
            )
        except Exception as exc:
            status.update(f"Restart-plan save failed: {exc}")
            return

        if result.prior_reentry is not prior_reentry:
            raise ValueError(
                "Restart-plan result did not retain the shell's exact prior re-entry lineage."
            )
        if result.rollover is not self.last_research_rollover:
            raise ValueError(
                "Restart-plan result did not retain the shell's exact continuation rollover."
            )
        if result.fresh_reentry.controller.presentation != self.research_controller.presentation:
            raise ValueError(
                "Restart-plan fresh re-entry does not describe the shell's mounted continuation."
            )

        self.research_reentry = result.fresh_reentry
        self.last_research_restart_plan = result
        controls.lock_after_success(result)
        self.query_one(
            "#research-endpoint-revision-controls",
            ResearchEndpointRevisionControls,
        ).unlock_after_restart_plan()

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
        if len(self.query("#research-session-restart-plan-controls")) != 0:
            await self.query_one(
                "#research-session-restart-plan-controls",
                ResearchSessionRestartPlanControls,
            ).remove()
        await old_detail.remove()
        await old_revision_controls.remove()
        await old_rollover_controls.remove()

        checkpoint_required = self.research_reentry is not None
        self.research_controller = continuation
        self.research_session = new_session
        self.research_presentation = new_session.sequence
        self.research_working_set_contexts = new_contexts
        self.last_research_rollover = result
        self.last_research_restart_plan = None

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
        await self.mount(
            ResearchEndpointRevisionControls(
                restart_checkpoint_required=checkpoint_required,
            )
        )
        await self.mount(ResearchSessionRolloverControls())
        if checkpoint_required:
            await self.mount(ResearchSessionRestartPlanControls(result))


def _require_reentry_coherence(
    controller: ChromiumResearchSessionController,
    reentry: ChromiumResearchSessionReentryResult,
) -> None:
    if not isinstance(reentry, ChromiumResearchSessionReentryResult):
        raise TypeError("reentry must be ChromiumResearchSessionReentryResult.")
    if reentry.controller.presentation != controller.presentation:
        raise ValueError(
            "Research re-entry lineage does not describe the supplied controller presentation."
        )
    if (
        reentry.controller.presentation.sequence.declaration_record_sha256
        != controller.presentation.sequence.declaration_record_sha256
    ):
        raise ValueError(
            "Research re-entry lineage declaration identity does not match the supplied controller."
        )
    if (
        reentry.controller.declared_endpoint.verification.edge_record_sha256
        != controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ValueError(
            "Research re-entry lineage endpoint identity does not match the supplied controller."
        )


def create_research_session_shell(
    controller: ChromiumResearchSessionController,
    *,
    reentry: ChromiumResearchSessionReentryResult | None = None,
) -> ResearchSessionShell:
    """Create the standalone governed research shell from one exact controller."""

    return ResearchSessionShell(controller, reentry=reentry)
