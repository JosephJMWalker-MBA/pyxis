from __future__ import annotations

from pathlib import Path

from textual.widgets import Button, Input, Static

from pyxis.app.chromium_research_second_basis_epoch_continuation_checkpoint_extension import (
    ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionResult,
    persist_chromium_research_second_basis_epoch_continuation_checkpoint_extension,
)
from pyxis.app.chromium_research_second_basis_epoch_continuation_reentry_plan_document import (
    ChromiumResearchSecondBasisEpochContinuationCheckpointResult,
    ChromiumResearchSecondBasisEpochContinuationReentryResult,
    persist_chromium_research_second_basis_epoch_continuation_checkpoint,
)
from pyxis.app.chromium_research_second_basis_epoch_shell_lineage import (
    ChromiumResearchSecondBasisEpochContinuationShellLineage,
    ChromiumResearchSecondBasisEpochShellLineage,
)
from pyxis.app.chromium_research_session_presentation import present_chromium_research_session
from pyxis.app.chromium_research_session_rollover import ChromiumResearchSessionRolloverResult

from .chromium_research_endpoint_revision_textual import ResearchEndpointRevisionControls
from .chromium_research_revision_edge_sequence_textual import (
    ResearchRevisionEdgeSequenceDetail,
    _require_research_sequence_presentation,
    _snapshot_working_set_contexts,
)
from .chromium_research_second_basis_epoch_continuation_checkpoint_extension_textual import (
    SecondBasisEpochResearchSessionCumulativeCheckpointControls,
    second_basis_epoch_cumulative_checkpoint_success_receipt,
)
from .chromium_research_second_basis_epoch_continuation_checkpoint_textual import (
    SecondBasisEpochResearchSessionContinuationCheckpointControls,
)
from .chromium_research_session_restart_plan_textual import ResearchSessionRestartPlanControls
from .chromium_research_session_rollover_textual import ResearchSessionRolloverControls
from .research_session_shell import ResearchSessionShell


class SecondBasisEpochResearchSessionShell(ResearchSessionShell):
    """Standalone shell retaining proven 37B launch lineage for one 37C checkpoint.

    The exact 38B wrapper remains launch authority: it binds one explicit 37B
    location to the fresh second-epoch re-entry proven from that location. The base
    shell receives no ordinary 31A re-entry lineage.

    After one explicit 30A rollover, this shell locks further revision and exposes
    only the existing proof-gated 37C checkpoint boundary. All durable checkpoint
    locations must be entered again explicitly; the launch overlay path is not
    prefilled or silently reused as current-path authority. A successful checkpoint
    remains locked and requires explicit continuation-overlay relaunch.
    """

    CSS = ResearchSessionShell.CSS + """
    #research-second-basis-epoch-continuation-checkpoint-controls {
        width: 94%;
        height: auto;
        padding: 1 2;
        margin-top: 1;
        border: round $secondary;
    }

    #research-second-basis-epoch-checkpoint-authority-notice,
    #research-second-basis-epoch-checkpoint-candidate,
    #research-second-basis-epoch-checkpoint-prior-overlay-source-label,
    #research-second-basis-epoch-checkpoint-successor-source-label,
    #research-second-basis-epoch-checkpoint-declaration-source-label,
    #research-second-basis-epoch-checkpoint-destination-label,
    #research-second-basis-epoch-checkpoint-status {
        margin-top: 1;
    }

    #research-second-basis-epoch-checkpoint-title,
    #research-second-basis-epoch-checkpoint-prior-overlay-source-label,
    #research-second-basis-epoch-checkpoint-successor-source-label,
    #research-second-basis-epoch-checkpoint-declaration-source-label,
    #research-second-basis-epoch-checkpoint-destination-label {
        text-style: bold;
    }

    #save-research-second-basis-epoch-continuation-checkpoint {
        margin-top: 1;
    }
    """

    def __init__(self, lineage: ChromiumResearchSecondBasisEpochShellLineage) -> None:
        if not isinstance(lineage, ChromiumResearchSecondBasisEpochShellLineage):
            raise TypeError(
                "lineage must be ChromiumResearchSecondBasisEpochShellLineage."
            )
        super().__init__(lineage.reentry.controller)
        self.second_basis_epoch_launch_lineage = lineage
        self.last_second_basis_epoch_continuation_checkpoint: (
            ChromiumResearchSecondBasisEpochContinuationCheckpointResult | None
        ) = None

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save-research-second-basis-epoch-continuation-checkpoint":
            event.stop()
            self.call_after_refresh(self._save_second_basis_epoch_continuation_checkpoint)
            return
        super().on_button_pressed(event)

    async def _mount_research_rollover(
        self,
        result: ChromiumResearchSessionRolloverResult,
    ) -> None:
        await super()._mount_research_rollover(result)
        if self.last_research_rollover is not result:
            raise ValueError(
                "Base research shell did not retain the exact second-epoch continuation rollover."
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
            SecondBasisEpochResearchSessionContinuationCheckpointControls(result)
        )

    async def _save_second_basis_epoch_continuation_checkpoint(self) -> None:
        controls = self.query_one(
            "#research-second-basis-epoch-continuation-checkpoint-controls",
            SecondBasisEpochResearchSessionContinuationCheckpointControls,
        )
        status = self.query_one(
            "#research-second-basis-epoch-checkpoint-status",
            Static,
        )
        rollover = self.last_research_rollover
        if rollover is None:
            status.update(
                "Second-epoch checkpoint failed: no explicit continuation rollover is awaiting a checkpoint."
            )
            return
        if controls.rollover is not rollover:
            status.update(
                "Second-epoch checkpoint failed: displayed checkpoint does not match the shell's exact rollover."
            )
            return
        prior_overlay_source = self.query_one(
            "#research-second-basis-epoch-checkpoint-prior-overlay-source",
            Input,
        )
        successor_source = self.query_one(
            "#research-second-basis-epoch-checkpoint-successor-source",
            Input,
        )
        declaration_source = self.query_one(
            "#research-second-basis-epoch-checkpoint-declaration-source",
            Input,
        )
        destination = self.query_one(
            "#research-second-basis-epoch-checkpoint-destination",
            Input,
        )
        if not prior_overlay_source.value.strip():
            status.update(
                "Second-epoch checkpoint failed: explicit current 37B overlay path is required."
            )
            return
        if not successor_source.value.strip():
            status.update(
                "Second-epoch checkpoint failed: explicit current successor edge path is required."
            )
            return
        if not declaration_source.value.strip():
            status.update(
                "Second-epoch checkpoint failed: explicit current continuation declaration path is required."
            )
            return
        if not destination.value.strip():
            status.update(
                "Second-epoch checkpoint failed: explicit no-overwrite 37C overlay destination is required."
            )
            return
        prior = self.second_basis_epoch_launch_lineage.reentry
        try:
            checkpoint = (
                persist_chromium_research_second_basis_epoch_continuation_checkpoint(
                    prior,
                    rollover,
                    prior_second_basis_epoch_overlay_source=Path(
                        prior_overlay_source.value
                    ),
                    successor_edge_source=Path(successor_source.value),
                    continuation_declaration_source=Path(declaration_source.value),
                    destination=Path(destination.value),
                )
            )
        except Exception as exc:
            status.update(f"Second-epoch checkpoint failed: {exc}")
            return
        _require_second_basis_epoch_checkpoint_matches_shell(
            checkpoint,
            prior=prior,
            rollover=rollover,
            one_hop_controller=self.research_controller,
        )
        self.last_second_basis_epoch_continuation_checkpoint = checkpoint
        controls.lock_after_success(checkpoint)


class SecondBasisEpochContinuationResearchSessionShell(ResearchSessionShell):
    """Repeatable cumulative-checkpoint shell for proven persisted 37C/37D lineage."""

    CSS = ResearchSessionShell.CSS + """
    #research-second-basis-epoch-cumulative-checkpoint-controls,
    #research-second-basis-epoch-cumulative-checkpoint-success-receipt {
        width: 94%;
        height: auto;
        padding: 1 2;
        margin-top: 1;
        border: round $secondary;
    }

    #research-second-basis-epoch-cumulative-checkpoint-authority-notice,
    #research-second-basis-epoch-cumulative-checkpoint-candidate,
    #research-second-basis-epoch-cumulative-checkpoint-current-overlay-source-label,
    #research-second-basis-epoch-cumulative-checkpoint-successor-source-label,
    #research-second-basis-epoch-cumulative-checkpoint-declaration-destination-label,
    #research-second-basis-epoch-cumulative-checkpoint-overlay-destination-label,
    #research-second-basis-epoch-cumulative-checkpoint-status {
        margin-top: 1;
    }

    #research-second-basis-epoch-cumulative-checkpoint-title,
    #research-second-basis-epoch-cumulative-checkpoint-current-overlay-source-label,
    #research-second-basis-epoch-cumulative-checkpoint-successor-source-label,
    #research-second-basis-epoch-cumulative-checkpoint-declaration-destination-label,
    #research-second-basis-epoch-cumulative-checkpoint-overlay-destination-label {
        text-style: bold;
    }

    #save-research-second-basis-epoch-cumulative-checkpoint {
        margin-top: 1;
    }
    """

    def __init__(
        self,
        lineage: ChromiumResearchSecondBasisEpochContinuationShellLineage,
    ) -> None:
        if not isinstance(
            lineage,
            ChromiumResearchSecondBasisEpochContinuationShellLineage,
        ):
            raise TypeError(
                "lineage must be ChromiumResearchSecondBasisEpochContinuationShellLineage."
            )
        super().__init__(lineage.reentry.controller)
        self.second_basis_epoch_continuation_launch_lineage = lineage
        self.second_basis_epoch_continuation_reentry = lineage.reentry
        self.last_second_basis_epoch_cumulative_checkpoint: (
            ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionResult | None
        ) = None

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save-research-second-basis-epoch-cumulative-checkpoint":
            event.stop()
            self.call_after_refresh(self._save_second_basis_epoch_cumulative_checkpoint)
            return
        super().on_button_pressed(event)

    async def _mount_research_rollover(
        self,
        result: ChromiumResearchSessionRolloverResult,
    ) -> None:
        current_reentry = self.second_basis_epoch_continuation_reentry
        await super()._mount_research_rollover(result)
        if self.last_research_rollover is not result:
            raise ValueError(
                "Base research shell did not retain the exact cumulative second-epoch rollover."
            )
        if len(self.query("#research-second-basis-epoch-cumulative-checkpoint-success-receipt")):
            await self.query_one(
                "#research-second-basis-epoch-cumulative-checkpoint-success-receipt",
                Static,
            ).remove()
        if len(self.query(ResearchSessionRestartPlanControls)):
            raise ValueError(
                "Cumulative second-epoch shell must not mount ordinary restart-plan controls."
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
            SecondBasisEpochResearchSessionCumulativeCheckpointControls(
                current_reentry,
                result,
            )
        )

    async def _save_second_basis_epoch_cumulative_checkpoint(self) -> None:
        controls = self.query_one(
            "#research-second-basis-epoch-cumulative-checkpoint-controls",
            SecondBasisEpochResearchSessionCumulativeCheckpointControls,
        )
        status = self.query_one(
            "#research-second-basis-epoch-cumulative-checkpoint-status",
            Static,
        )
        rollover = self.last_research_rollover
        current_reentry = self.second_basis_epoch_continuation_reentry
        if rollover is None:
            status.update(
                "Cumulative second-epoch checkpoint failed: no explicit rollover is awaiting a checkpoint."
            )
            return
        if controls.rollover is not rollover:
            status.update(
                "Cumulative second-epoch checkpoint failed: displayed checkpoint does not match the shell's exact rollover."
            )
            return
        if controls.current_reentry is not current_reentry:
            status.update(
                "Cumulative second-epoch checkpoint failed: displayed checkpoint does not match the shell's exact current typed continuation."
            )
            return
        current_overlay = self.query_one(
            "#research-second-basis-epoch-cumulative-checkpoint-current-overlay-source",
            Input,
        )
        successor_source = self.query_one(
            "#research-second-basis-epoch-cumulative-checkpoint-successor-source",
            Input,
        )
        declaration_destination = self.query_one(
            "#research-second-basis-epoch-cumulative-checkpoint-declaration-destination",
            Input,
        )
        overlay_destination = self.query_one(
            "#research-second-basis-epoch-cumulative-checkpoint-overlay-destination",
            Input,
        )
        if not current_overlay.value.strip():
            status.update(
                "Cumulative second-epoch checkpoint failed: explicit current 37C/37D overlay path is required."
            )
            return
        if not successor_source.value.strip():
            status.update(
                "Cumulative second-epoch checkpoint failed: explicit current successor edge path is required."
            )
            return
        if not declaration_destination.value.strip():
            status.update(
                "Cumulative second-epoch checkpoint failed: explicit no-overwrite cumulative declaration destination is required."
            )
            return
        if not overlay_destination.value.strip():
            status.update(
                "Cumulative second-epoch checkpoint failed: explicit no-overwrite next overlay destination is required."
            )
            return
        try:
            checkpoint = persist_chromium_research_second_basis_epoch_continuation_checkpoint_extension(
                current_reentry,
                rollover,
                current_overlay_source=Path(current_overlay.value),
                successor_edge_source=Path(successor_source.value),
                cumulative_declaration_destination=Path(declaration_destination.value),
                next_overlay_destination=Path(overlay_destination.value),
            )
        except Exception as exc:
            status.update(f"Cumulative second-epoch checkpoint failed: {exc}")
            return
        _require_second_basis_epoch_cumulative_checkpoint_matches_shell(
            checkpoint,
            current_reentry=current_reentry,
            rollover=rollover,
            one_hop_controller=self.research_controller,
        )
        controls.lock_after_success(checkpoint)
        await self._promote_second_basis_epoch_cumulative_checkpoint(checkpoint)

    async def _promote_second_basis_epoch_cumulative_checkpoint(
        self,
        result: ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionResult,
    ) -> None:
        fresh_reentry = result.fresh_reentry
        fresh_controller = fresh_reentry.controller
        rebuilt_session = present_chromium_research_session(fresh_controller.loaded)
        if rebuilt_session != fresh_controller.presentation:
            raise ValueError(
                "Fresh cumulative second-epoch controller presentation is incoherent with retained loaded evidence."
            )
        new_session = fresh_controller.presentation
        _require_research_sequence_presentation(new_session.sequence)
        new_contexts = _snapshot_working_set_contexts(
            new_session.sequence,
            new_session.working_set_contexts,
        )
        if len(new_contexts) != len(new_session.sequence.members):
            raise ValueError(
                "Fresh cumulative second-epoch session must contain one context per declared position."
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
            "#research-second-basis-epoch-cumulative-checkpoint-controls",
            SecondBasisEpochResearchSessionCumulativeCheckpointControls,
        )
        if len(self.query("#research-rollover-success-receipt")):
            await self.query_one("#research-rollover-success-receipt", Static).remove()
        await old_detail.remove()
        await old_revision.remove()
        await old_rollover.remove()
        await old_checkpoint.remove()
        self.second_basis_epoch_continuation_reentry = fresh_reentry
        self.research_controller = fresh_controller
        self.research_session = new_session
        self.research_presentation = new_session.sequence
        self.research_working_set_contexts = new_contexts
        self.last_research_rollover = None
        self.last_research_restart_plan = None
        self.last_second_basis_epoch_cumulative_checkpoint = result
        await self.mount(
            Static(
                second_basis_epoch_cumulative_checkpoint_success_receipt(result),
                id="research-second-basis-epoch-cumulative-checkpoint-success-receipt",
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


def _require_second_basis_epoch_checkpoint_matches_shell(
    result: ChromiumResearchSecondBasisEpochContinuationCheckpointResult,
    *,
    prior,
    rollover: ChromiumResearchSessionRolloverResult,
    one_hop_controller,
) -> None:
    if result.prior_reentry is not prior:
        raise ValueError(
            "37C checkpoint did not retain the shell's exact proven second-epoch prior lineage."
        )
    if result.rollover is not rollover:
        raise ValueError(
            "37C checkpoint did not retain the shell's exact continuation rollover."
        )
    if result.fresh_reentry.controller.presentation != one_hop_controller.presentation:
        raise ValueError(
            "37C fresh continuation presentation does not match the shell's mounted one-hop continuation."
        )
    if (
        result.fresh_reentry.controller.declared_endpoint.verification.edge_record_sha256
        != one_hop_controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ValueError(
            "37C fresh continuation endpoint identity does not match the shell's mounted one-hop continuation."
        )
    fresh_prior = result.fresh_reentry.prior_second_basis_epoch_reentry
    if (
        fresh_prior.loaded_root.verification.root_record_sha256
        != prior.loaded_root.verification.root_record_sha256
    ):
        raise ValueError(
            "37C fresh second-root identity does not match the shell's proven launch ancestry."
        )
    if (
        fresh_prior.prior_continuation_reentry.prior_root_backed_reentry.loaded_root.verification.root_record_sha256
        != prior.prior_continuation_reentry.prior_root_backed_reentry.loaded_root.verification.root_record_sha256
    ):
        raise ValueError(
            "37C fresh retained first-root identity does not match the shell's proven launch ancestry."
        )


def _require_second_basis_epoch_cumulative_checkpoint_matches_shell(
    result: ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionResult,
    *,
    current_reentry: ChromiumResearchSecondBasisEpochContinuationReentryResult,
    rollover: ChromiumResearchSessionRolloverResult,
    one_hop_controller,
) -> None:
    if result.current_reentry is not current_reentry:
        raise ValueError(
            "37D checkpoint did not retain the shell's exact current second-epoch continuation."
        )
    if result.rollover is not rollover:
        raise ValueError(
            "37D checkpoint did not retain the shell's exact continuation rollover."
        )
    if (
        result.next_plan.prior_second_basis_epoch_overlay_source
        != result.current_plan.prior_second_basis_epoch_overlay_source
    ):
        raise ValueError(
            "37D checkpoint did not preserve the explicit current plan's direct 37B ancestry anchor."
        )
    fresh_endpoint = result.fresh_reentry.controller.declared_endpoint
    one_hop_endpoint = one_hop_controller.declared_endpoint
    if (
        fresh_endpoint.verification.edge_record_sha256
        != one_hop_endpoint.verification.edge_record_sha256
    ):
        raise ValueError(
            "37D fresh cumulative endpoint identity does not match the mounted one-hop continuation."
        )
    if (
        fresh_endpoint.revision.revised_note.note_text
        != one_hop_endpoint.revision.revised_note.note_text
    ):
        raise ValueError(
            "37D fresh cumulative endpoint text does not match the mounted one-hop continuation."
        )
    fresh_second = result.fresh_reentry.prior_second_basis_epoch_reentry
    current_second = current_reentry.prior_second_basis_epoch_reentry
    if fresh_second.controller.presentation != current_second.controller.presentation:
        raise ValueError(
            "37D fresh second-epoch anchor presentation changed cumulative ancestry."
        )
    if (
        fresh_second.controller.declared_endpoint.verification.edge_record_sha256
        != current_second.controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ValueError(
            "37D fresh second-epoch anchor endpoint identity changed cumulative ancestry."
        )
    if (
        fresh_second.loaded_root.verification.root_record_sha256
        != current_second.loaded_root.verification.root_record_sha256
    ):
        raise ValueError("37D fresh second-root identity changed cumulative ancestry.")
    if (
        fresh_second.prior_continuation_reentry.prior_root_backed_reentry.loaded_root.verification.root_record_sha256
        != current_second.prior_continuation_reentry.prior_root_backed_reentry.loaded_root.verification.root_record_sha256
    ):
        raise ValueError(
            "37D fresh retained first-root identity changed cumulative ancestry."
        )


def create_second_basis_epoch_research_session_shell(
    lineage: ChromiumResearchSecondBasisEpochShellLineage,
) -> SecondBasisEpochResearchSessionShell:
    return SecondBasisEpochResearchSessionShell(lineage)


def create_second_basis_epoch_continuation_research_session_shell(
    lineage: ChromiumResearchSecondBasisEpochContinuationShellLineage,
) -> SecondBasisEpochContinuationResearchSessionShell:
    return SecondBasisEpochContinuationResearchSessionShell(lineage)


__all__ = [
    "SecondBasisEpochContinuationResearchSessionShell",
    "SecondBasisEpochResearchSessionShell",
    "create_second_basis_epoch_continuation_research_session_shell",
    "create_second_basis_epoch_research_session_shell",
]
