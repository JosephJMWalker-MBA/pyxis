from __future__ import annotations

from pathlib import Path

from textual.widgets import Button, Input, Static

from pyxis.app.chromium_research_root_backed_session_continuation_checkpoint_extension import (
    ChromiumResearchRootBackedSessionContinuationCheckpointExtensionResult,
    persist_chromium_research_root_backed_session_continuation_checkpoint_extension,
)
from pyxis.app.chromium_research_root_backed_session_continuation_reentry_plan_document import (
    ChromiumResearchRootBackedSessionContinuationReentryResult,
)
from pyxis.app.chromium_research_session_presentation import present_chromium_research_session
from pyxis.app.chromium_research_session_rollover import ChromiumResearchSessionRolloverResult

from .chromium_research_endpoint_revision_textual import ResearchEndpointRevisionControls
from .chromium_research_revision_edge_sequence_textual import (
    ResearchRevisionEdgeSequenceDetail,
    _require_research_sequence_presentation,
    _snapshot_working_set_contexts,
)
from .chromium_research_root_backed_session_continuation_checkpoint_extension_textual import (
    RootBackedResearchSessionCumulativeCheckpointControls,
    cumulative_checkpoint_success_receipt,
)
from .chromium_research_session_restart_plan_textual import ResearchSessionRestartPlanControls
from .chromium_research_session_rollover_textual import ResearchSessionRolloverControls
from .research_session_shell import ResearchSessionShell


class RootBackedContinuationResearchSessionShell(ResearchSessionShell):
    """Repeatable Textual shell for one exact persisted 35D/35E continuation lineage.

    The base shell owns governed inspection, endpoint revision, and explicit 30A
    rollover. This subclass adds only the 35E cumulative checkpoint transition.

    A successful 35E checkpoint changes more than restart configuration: the freshly
    proven controller presents the cumulative post-root declaration. Therefore this
    shell replaces the visible one-hop continuation with that exact fresh cumulative
    controller before unlocking another endpoint revision.
    """

    CSS = ResearchSessionShell.CSS + """
    #research-root-backed-cumulative-checkpoint-controls,
    #research-root-backed-cumulative-checkpoint-success-receipt {
        width: 94%;
        height: auto;
        padding: 1 2;
        margin-top: 1;
        border: round $secondary;
    }

    #research-root-backed-cumulative-checkpoint-authority-notice,
    #research-root-backed-cumulative-checkpoint-candidate,
    #research-root-backed-cumulative-checkpoint-current-overlay-source-label,
    #research-root-backed-cumulative-checkpoint-successor-source-label,
    #research-root-backed-cumulative-checkpoint-declaration-destination-label,
    #research-root-backed-cumulative-checkpoint-overlay-destination-label,
    #research-root-backed-cumulative-checkpoint-status {
        margin-top: 1;
    }

    #research-root-backed-cumulative-checkpoint-title,
    #research-root-backed-cumulative-checkpoint-current-overlay-source-label,
    #research-root-backed-cumulative-checkpoint-successor-source-label,
    #research-root-backed-cumulative-checkpoint-declaration-destination-label,
    #research-root-backed-cumulative-checkpoint-overlay-destination-label {
        text-style: bold;
    }

    #save-research-root-backed-cumulative-checkpoint {
        margin-top: 1;
    }
    """

    def __init__(
        self,
        reentry: ChromiumResearchRootBackedSessionContinuationReentryResult,
    ) -> None:
        if not isinstance(
            reentry,
            ChromiumResearchRootBackedSessionContinuationReentryResult,
        ):
            raise TypeError(
                "reentry must be ChromiumResearchRootBackedSessionContinuationReentryResult."
            )
        super().__init__(reentry.controller)
        self.root_backed_continuation_reentry = reentry
        self.last_root_backed_cumulative_checkpoint: (
            ChromiumResearchRootBackedSessionContinuationCheckpointExtensionResult | None
        ) = None

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save-research-root-backed-cumulative-checkpoint":
            event.stop()
            self.call_after_refresh(self._save_root_backed_cumulative_checkpoint)
            return
        super().on_button_pressed(event)

    async def _mount_research_rollover(
        self,
        result: ChromiumResearchSessionRolloverResult,
    ) -> None:
        """Mount one-hop continuation, then lock it pending explicit 35E proof."""

        current_reentry = self.root_backed_continuation_reentry
        await super()._mount_research_rollover(result)
        if self.last_research_rollover is not result:
            raise ValueError(
                "Base research shell did not retain the exact cumulative-lineage rollover."
            )

        if len(self.query("#research-root-backed-cumulative-checkpoint-success-receipt")):
            await self.query_one(
                "#research-root-backed-cumulative-checkpoint-success-receipt",
                Static,
            ).remove()
        if len(self.query(ResearchSessionRestartPlanControls)):
            raise ValueError(
                "Cumulative root-backed shell must not mount ordinary restart-plan controls."
            )

        unlocked_revision = self.query_one(
            "#research-endpoint-revision-controls",
            ResearchEndpointRevisionControls,
        )
        empty_rollover = self.query_one(
            "#research-session-rollover-controls",
            ResearchSessionRolloverControls,
        )
        await unlocked_revision.remove()
        await empty_rollover.remove()

        await self.mount(
            ResearchEndpointRevisionControls(restart_checkpoint_required=True)
        )
        await self.mount(ResearchSessionRolloverControls())
        await self.mount(
            RootBackedResearchSessionCumulativeCheckpointControls(
                current_reentry,
                result,
            )
        )

    async def _save_root_backed_cumulative_checkpoint(self) -> None:
        controls = self.query_one(
            "#research-root-backed-cumulative-checkpoint-controls",
            RootBackedResearchSessionCumulativeCheckpointControls,
        )
        status = self.query_one(
            "#research-root-backed-cumulative-checkpoint-status",
            Static,
        )
        rollover = self.last_research_rollover
        current_reentry = self.root_backed_continuation_reentry
        if rollover is None:
            status.update(
                "Cumulative checkpoint failed: no explicit continuation rollover is awaiting a checkpoint."
            )
            return
        if controls.rollover is not rollover:
            status.update(
                "Cumulative checkpoint failed: displayed checkpoint does not match the shell's exact rollover."
            )
            return
        if controls.current_reentry is not current_reentry:
            status.update(
                "Cumulative checkpoint failed: displayed checkpoint does not match the shell's exact current continuation lineage."
            )
            return

        current_overlay = self.query_one(
            "#research-root-backed-cumulative-checkpoint-current-overlay-source",
            Input,
        )
        successor_source = self.query_one(
            "#research-root-backed-cumulative-checkpoint-successor-source",
            Input,
        )
        declaration_destination = self.query_one(
            "#research-root-backed-cumulative-checkpoint-declaration-destination",
            Input,
        )
        overlay_destination = self.query_one(
            "#research-root-backed-cumulative-checkpoint-overlay-destination",
            Input,
        )
        if not current_overlay.value.strip():
            status.update(
                "Cumulative checkpoint failed: explicit current 35D/35E overlay path is required."
            )
            return
        if not successor_source.value.strip():
            status.update(
                "Cumulative checkpoint failed: explicit current successor edge path is required."
            )
            return
        if not declaration_destination.value.strip():
            status.update(
                "Cumulative checkpoint failed: explicit no-overwrite cumulative declaration destination is required."
            )
            return
        if not overlay_destination.value.strip():
            status.update(
                "Cumulative checkpoint failed: explicit no-overwrite next overlay destination is required."
            )
            return

        try:
            checkpoint = (
                persist_chromium_research_root_backed_session_continuation_checkpoint_extension(
                    current_reentry,
                    rollover,
                    current_overlay_source=Path(current_overlay.value),
                    successor_edge_source=Path(successor_source.value),
                    cumulative_declaration_destination=Path(
                        declaration_destination.value
                    ),
                    next_overlay_destination=Path(overlay_destination.value),
                )
            )
        except Exception as exc:
            status.update(f"Cumulative checkpoint failed: {exc}")
            return

        _require_checkpoint_result_matches_shell(
            checkpoint,
            current_reentry=current_reentry,
            rollover=rollover,
            one_hop_controller=self.research_controller,
        )
        controls.lock_after_success(checkpoint)
        await self._promote_cumulative_checkpoint(checkpoint)

    async def _promote_cumulative_checkpoint(
        self,
        result: ChromiumResearchRootBackedSessionContinuationCheckpointExtensionResult,
    ) -> None:
        """Replace the one-hop surface with the exact fresh cumulative 35E controller."""

        fresh_reentry = result.fresh_reentry
        fresh_controller = fresh_reentry.controller
        rebuilt_session = present_chromium_research_session(fresh_controller.loaded)
        if rebuilt_session != fresh_controller.presentation:
            raise ValueError(
                "Fresh cumulative controller presentation is incoherent with retained loaded evidence."
            )

        new_session = fresh_controller.presentation
        _require_research_sequence_presentation(new_session.sequence)
        new_contexts = _snapshot_working_set_contexts(
            new_session.sequence,
            new_session.working_set_contexts,
        )
        if len(new_contexts) != len(new_session.sequence.members):
            raise ValueError(
                "Fresh cumulative session must contain one context per declared position."
            )

        old_detail = self.query_one(
            "#research-revision-edge-sequence",
            ResearchRevisionEdgeSequenceDetail,
        )
        old_revision = self.query_one(
            "#research-endpoint-revision-controls",
            ResearchEndpointRevisionControls,
        )
        old_rollover = self.query_one(
            "#research-session-rollover-controls",
            ResearchSessionRolloverControls,
        )
        old_checkpoint = self.query_one(
            "#research-root-backed-cumulative-checkpoint-controls",
            RootBackedResearchSessionCumulativeCheckpointControls,
        )

        if len(self.query("#research-rollover-success-receipt")):
            await self.query_one("#research-rollover-success-receipt", Static).remove()
        await old_detail.remove()
        await old_revision.remove()
        await old_rollover.remove()
        await old_checkpoint.remove()

        self.root_backed_continuation_reentry = fresh_reentry
        self.research_controller = fresh_controller
        self.research_session = new_session
        self.research_presentation = new_session.sequence
        self.research_working_set_contexts = new_contexts
        self.last_research_rollover = None
        self.last_research_restart_plan = None
        self.last_root_backed_cumulative_checkpoint = result

        await self.mount(
            Static(
                cumulative_checkpoint_success_receipt(result),
                id="research-root-backed-cumulative-checkpoint-success-receipt",
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


def _require_checkpoint_result_matches_shell(
    result: ChromiumResearchRootBackedSessionContinuationCheckpointExtensionResult,
    *,
    current_reentry: ChromiumResearchRootBackedSessionContinuationReentryResult,
    rollover: ChromiumResearchSessionRolloverResult,
    one_hop_controller,
) -> None:
    if result.current_reentry is not current_reentry:
        raise ValueError(
            "35E checkpoint did not retain the shell's exact current continuation lineage."
        )
    if result.rollover is not rollover:
        raise ValueError(
            "35E checkpoint did not retain the shell's exact continuation rollover."
        )
    if (
        result.next_plan.prior_root_backed_overlay_source
        != current_reentry.plan.prior_root_backed_overlay_source
    ):
        raise ValueError(
            "35E checkpoint changed the fixed 35C ancestry anchor."
        )
    if (
        result.fresh_reentry.controller.declared_endpoint.verification.edge_record_sha256
        != one_hop_controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ValueError(
            "35E fresh cumulative endpoint identity does not match the mounted one-hop continuation."
        )
    if (
        result.fresh_reentry.controller.declared_endpoint.revision.revised_note.note_text
        != one_hop_controller.declared_endpoint.revision.revised_note.note_text
    ):
        raise ValueError(
            "35E fresh cumulative endpoint text does not match the mounted one-hop continuation."
        )
    if (
        result.fresh_reentry.prior_root_backed_reentry.loaded_root.verification.root_record_sha256
        != current_reentry.prior_root_backed_reentry.loaded_root.verification.root_record_sha256
    ):
        raise ValueError(
            "35E fresh cumulative root identity does not match the current continuation ancestry."
        )


def create_root_backed_continuation_research_session_shell(
    reentry: ChromiumResearchRootBackedSessionContinuationReentryResult,
) -> RootBackedContinuationResearchSessionShell:
    """Create one repeatable cumulative-checkpoint shell from an exact 35D/35E result."""

    return RootBackedContinuationResearchSessionShell(reentry)


__all__ = [
    "RootBackedContinuationResearchSessionShell",
    "create_root_backed_continuation_research_session_shell",
]
