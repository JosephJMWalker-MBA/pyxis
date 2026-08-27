from __future__ import annotations

from pathlib import Path

from textual.widgets import Button, Input, Static

from pyxis.app.chromium_research_session_rollover import ChromiumResearchSessionRolloverResult
from pyxis.app.chromium_research_third_basis_epoch_continuation_checkpoint_extension import (
    ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionResult,
    persist_chromium_research_third_basis_epoch_continuation_checkpoint_extension,
)
from pyxis.app.chromium_research_third_basis_epoch_continuation_reentry_plan_document import (
    ChromiumResearchThirdBasisEpochContinuationCheckpointResult,
    ChromiumResearchThirdBasisEpochContinuationReentryResult,
    persist_chromium_research_third_basis_epoch_continuation_checkpoint,
)
from pyxis.app.chromium_research_third_basis_epoch_reentry import (
    ChromiumResearchThirdBasisEpochReentryResult,
)
from pyxis.app.chromium_research_third_basis_epoch_shell_lineage import (
    ChromiumResearchThirdBasisEpochContinuationShellLineage,
    ChromiumResearchThirdBasisEpochShellLineage,
)

from .chromium_research_cumulative_checkpoint_promotion_textual import (
    _CumulativeCheckpointPromotionSpec,
    _promote_cumulative_checkpoint_surface,
)
from .chromium_research_endpoint_revision_textual import ResearchEndpointRevisionControls
from .chromium_research_session_restart_plan_textual import ResearchSessionRestartPlanControls
from .chromium_research_session_rollover_textual import ResearchSessionRolloverControls
from .chromium_research_third_basis_epoch_continuation_checkpoint_extension_textual import (
    ThirdBasisEpochResearchSessionCumulativeCheckpointControls,
    third_basis_epoch_cumulative_checkpoint_success_receipt,
)
from .chromium_research_third_basis_epoch_continuation_checkpoint_textual import (
    ThirdBasisEpochResearchSessionContinuationCheckpointControls,
)
from .research_session_shell import ResearchSessionShell


_THIRD_BASIS_EPOCH_CUMULATIVE_PROMOTION = _CumulativeCheckpointPromotionSpec(
    checkpoint_controls_selector=(
        "#research-third-basis-epoch-cumulative-checkpoint-controls"
    ),
    checkpoint_controls_type=ThirdBasisEpochResearchSessionCumulativeCheckpointControls,
    success_receipt_id="research-third-basis-epoch-cumulative-checkpoint-success-receipt",
    presentation_error=(
        "Fresh cumulative third-epoch controller presentation is incoherent with retained loaded evidence."
    ),
    context_cardinality_error=(
        "Fresh cumulative third-epoch session must contain one context per declared position."
    ),
)


class ThirdBasisEpochResearchSessionShell(ResearchSessionShell):
    """Standalone shell retaining proven 40B launch lineage for one 40C checkpoint.

    The exact 41A wrapper remains launch authority: it binds one explicit 40B
    location to the fresh three-root re-entry proven from that location. The base
    shell receives no ordinary 31A re-entry lineage.

    After one explicit 30A rollover, this shell locks further revision and exposes
    only the existing proof-gated 40C checkpoint boundary. All durable checkpoint
    locations must be entered again explicitly; the launch overlay path is not
    prefilled or silently reused as current-path authority. A successful checkpoint
    remains locked and requires explicit continuation-overlay relaunch.
    """

    CSS = ResearchSessionShell.CSS + """
    #research-third-basis-epoch-continuation-checkpoint-controls {
        width: 94%;
        height: auto;
        padding: 1 2;
        margin-top: 1;
        border: round $secondary;
    }

    #research-third-basis-epoch-checkpoint-authority-notice,
    #research-third-basis-epoch-checkpoint-candidate,
    #research-third-basis-epoch-checkpoint-prior-overlay-source-label,
    #research-third-basis-epoch-checkpoint-successor-source-label,
    #research-third-basis-epoch-checkpoint-declaration-source-label,
    #research-third-basis-epoch-checkpoint-destination-label,
    #research-third-basis-epoch-checkpoint-status {
        margin-top: 1;
    }

    #research-third-basis-epoch-checkpoint-title,
    #research-third-basis-epoch-checkpoint-prior-overlay-source-label,
    #research-third-basis-epoch-checkpoint-successor-source-label,
    #research-third-basis-epoch-checkpoint-declaration-source-label,
    #research-third-basis-epoch-checkpoint-destination-label {
        text-style: bold;
    }

    #save-research-third-basis-epoch-continuation-checkpoint {
        margin-top: 1;
    }
    """

    def __init__(self, lineage: ChromiumResearchThirdBasisEpochShellLineage) -> None:
        if not isinstance(lineage, ChromiumResearchThirdBasisEpochShellLineage):
            raise TypeError(
                "lineage must be ChromiumResearchThirdBasisEpochShellLineage."
            )
        super().__init__(lineage.reentry.controller)
        self.third_basis_epoch_launch_lineage = lineage
        self.last_third_basis_epoch_continuation_checkpoint: (
            ChromiumResearchThirdBasisEpochContinuationCheckpointResult | None
        ) = None

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save-research-third-basis-epoch-continuation-checkpoint":
            event.stop()
            self.call_after_refresh(self._save_third_basis_epoch_continuation_checkpoint)
            return
        super().on_button_pressed(event)

    async def _mount_research_rollover(
        self,
        result: ChromiumResearchSessionRolloverResult,
    ) -> None:
        await super()._mount_research_rollover(result)
        if self.last_research_rollover is not result:
            raise ValueError(
                "Base research shell did not retain the exact third-epoch continuation rollover."
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
            ThirdBasisEpochResearchSessionContinuationCheckpointControls(result)
        )

    async def _save_third_basis_epoch_continuation_checkpoint(self) -> None:
        controls = self.query_one(
            "#research-third-basis-epoch-continuation-checkpoint-controls",
            ThirdBasisEpochResearchSessionContinuationCheckpointControls,
        )
        status = self.query_one(
            "#research-third-basis-epoch-checkpoint-status",
            Static,
        )
        rollover = self.last_research_rollover
        if rollover is None:
            status.update(
                "Third-epoch checkpoint failed: no explicit continuation rollover is awaiting a checkpoint."
            )
            return
        if controls.rollover is not rollover:
            status.update(
                "Third-epoch checkpoint failed: displayed checkpoint does not match the shell's exact rollover."
            )
            return
        prior_overlay_source = self.query_one(
            "#research-third-basis-epoch-checkpoint-prior-overlay-source",
            Input,
        )
        successor_source = self.query_one(
            "#research-third-basis-epoch-checkpoint-successor-source",
            Input,
        )
        declaration_source = self.query_one(
            "#research-third-basis-epoch-checkpoint-declaration-source",
            Input,
        )
        destination = self.query_one(
            "#research-third-basis-epoch-checkpoint-destination",
            Input,
        )
        if not prior_overlay_source.value.strip():
            status.update(
                "Third-epoch checkpoint failed: explicit current 40B overlay path is required."
            )
            return
        if not successor_source.value.strip():
            status.update(
                "Third-epoch checkpoint failed: explicit current successor edge path is required."
            )
            return
        if not declaration_source.value.strip():
            status.update(
                "Third-epoch checkpoint failed: explicit current continuation declaration path is required."
            )
            return
        if not destination.value.strip():
            status.update(
                "Third-epoch checkpoint failed: explicit no-overwrite 40C overlay destination is required."
            )
            return
        prior = self.third_basis_epoch_launch_lineage.reentry
        try:
            checkpoint = (
                persist_chromium_research_third_basis_epoch_continuation_checkpoint(
                    prior,
                    rollover,
                    prior_third_basis_epoch_overlay_source=Path(
                        prior_overlay_source.value
                    ),
                    successor_edge_source=Path(successor_source.value),
                    continuation_declaration_source=Path(declaration_source.value),
                    destination=Path(destination.value),
                )
            )
        except Exception as exc:
            status.update(f"Third-epoch checkpoint failed: {exc}")
            return
        _require_third_basis_epoch_checkpoint_matches_shell(
            checkpoint,
            prior=prior,
            rollover=rollover,
            one_hop_controller=self.research_controller,
        )
        self.last_third_basis_epoch_continuation_checkpoint = checkpoint
        controls.lock_after_success(checkpoint)


class ThirdBasisEpochContinuationResearchSessionShell(ResearchSessionShell):
    """Repeatable cumulative-checkpoint shell for proven persisted 40C/40D lineage.

    The exact 41A wrapper remains immutable launch provenance. A separate current
    typed continuation starts at `lineage.reentry` and advances only after an explicit
    40D checkpoint is freshly proven and visibly promoted. No ordinary restart-plan
    authority, current-path prefilling, or automatic handoff is inferred.
    """

    CSS = ResearchSessionShell.CSS + """
    #research-third-basis-epoch-cumulative-checkpoint-controls,
    #research-third-basis-epoch-cumulative-checkpoint-success-receipt {
        width: 94%;
        height: auto;
        padding: 1 2;
        margin-top: 1;
        border: round $secondary;
    }

    #research-third-basis-epoch-cumulative-checkpoint-authority-notice,
    #research-third-basis-epoch-cumulative-checkpoint-candidate,
    #research-third-basis-epoch-cumulative-checkpoint-current-overlay-source-label,
    #research-third-basis-epoch-cumulative-checkpoint-successor-source-label,
    #research-third-basis-epoch-cumulative-checkpoint-declaration-destination-label,
    #research-third-basis-epoch-cumulative-checkpoint-overlay-destination-label,
    #research-third-basis-epoch-cumulative-checkpoint-status {
        margin-top: 1;
    }

    #research-third-basis-epoch-cumulative-checkpoint-title,
    #research-third-basis-epoch-cumulative-checkpoint-current-overlay-source-label,
    #research-third-basis-epoch-cumulative-checkpoint-successor-source-label,
    #research-third-basis-epoch-cumulative-checkpoint-declaration-destination-label,
    #research-third-basis-epoch-cumulative-checkpoint-overlay-destination-label {
        text-style: bold;
    }

    #save-research-third-basis-epoch-cumulative-checkpoint {
        margin-top: 1;
    }
    """

    def __init__(
        self,
        lineage: ChromiumResearchThirdBasisEpochContinuationShellLineage,
    ) -> None:
        if not isinstance(
            lineage,
            ChromiumResearchThirdBasisEpochContinuationShellLineage,
        ):
            raise TypeError(
                "lineage must be ChromiumResearchThirdBasisEpochContinuationShellLineage."
            )
        super().__init__(lineage.reentry.controller)
        self.third_basis_epoch_continuation_launch_lineage = lineage
        self.third_basis_epoch_continuation_reentry = lineage.reentry
        self.last_third_basis_epoch_cumulative_checkpoint: (
            ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionResult | None
        ) = None

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save-research-third-basis-epoch-cumulative-checkpoint":
            event.stop()
            self.call_after_refresh(self._save_third_basis_epoch_cumulative_checkpoint)
            return
        super().on_button_pressed(event)

    async def _mount_research_rollover(
        self,
        result: ChromiumResearchSessionRolloverResult,
    ) -> None:
        current_reentry = self.third_basis_epoch_continuation_reentry
        await super()._mount_research_rollover(result)
        if self.last_research_rollover is not result:
            raise ValueError(
                "Base research shell did not retain the exact cumulative third-epoch rollover."
            )
        if len(self.query("#research-third-basis-epoch-cumulative-checkpoint-success-receipt")):
            await self.query_one(
                "#research-third-basis-epoch-cumulative-checkpoint-success-receipt",
                Static,
            ).remove()
        if len(self.query(ResearchSessionRestartPlanControls)):
            raise ValueError(
                "Cumulative third-epoch shell must not mount ordinary restart-plan controls."
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
            ThirdBasisEpochResearchSessionCumulativeCheckpointControls(
                current_reentry,
                result,
            )
        )

    async def _save_third_basis_epoch_cumulative_checkpoint(self) -> None:
        controls = self.query_one(
            "#research-third-basis-epoch-cumulative-checkpoint-controls",
            ThirdBasisEpochResearchSessionCumulativeCheckpointControls,
        )
        status = self.query_one(
            "#research-third-basis-epoch-cumulative-checkpoint-status",
            Static,
        )
        rollover = self.last_research_rollover
        current_reentry = self.third_basis_epoch_continuation_reentry
        if rollover is None:
            status.update(
                "Cumulative third-epoch checkpoint failed: no explicit rollover is awaiting a checkpoint."
            )
            return
        if controls.rollover is not rollover:
            status.update(
                "Cumulative third-epoch checkpoint failed: displayed checkpoint does not match the shell's exact rollover."
            )
            return
        if controls.current_reentry is not current_reentry:
            status.update(
                "Cumulative third-epoch checkpoint failed: displayed checkpoint does not match the shell's exact current typed continuation."
            )
            return
        current_overlay = self.query_one(
            "#research-third-basis-epoch-cumulative-checkpoint-current-overlay-source",
            Input,
        )
        successor_source = self.query_one(
            "#research-third-basis-epoch-cumulative-checkpoint-successor-source",
            Input,
        )
        declaration_destination = self.query_one(
            "#research-third-basis-epoch-cumulative-checkpoint-declaration-destination",
            Input,
        )
        overlay_destination = self.query_one(
            "#research-third-basis-epoch-cumulative-checkpoint-overlay-destination",
            Input,
        )
        if not current_overlay.value.strip():
            status.update(
                "Cumulative third-epoch checkpoint failed: explicit current 40C/40D overlay path is required."
            )
            return
        if not successor_source.value.strip():
            status.update(
                "Cumulative third-epoch checkpoint failed: explicit current successor edge path is required."
            )
            return
        if not declaration_destination.value.strip():
            status.update(
                "Cumulative third-epoch checkpoint failed: explicit no-overwrite cumulative declaration destination is required."
            )
            return
        if not overlay_destination.value.strip():
            status.update(
                "Cumulative third-epoch checkpoint failed: explicit no-overwrite next overlay destination is required."
            )
            return
        try:
            checkpoint = persist_chromium_research_third_basis_epoch_continuation_checkpoint_extension(
                current_reentry,
                rollover,
                current_overlay_source=Path(current_overlay.value),
                successor_edge_source=Path(successor_source.value),
                cumulative_declaration_destination=Path(declaration_destination.value),
                next_overlay_destination=Path(overlay_destination.value),
            )
        except Exception as exc:
            status.update(f"Cumulative third-epoch checkpoint failed: {exc}")
            return
        _require_third_basis_epoch_cumulative_checkpoint_matches_shell(
            checkpoint,
            current_reentry=current_reentry,
            rollover=rollover,
            one_hop_controller=self.research_controller,
        )
        controls.lock_after_success(checkpoint)
        await self._promote_third_basis_epoch_cumulative_checkpoint(checkpoint)

    async def _promote_third_basis_epoch_cumulative_checkpoint(
        self,
        result: ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionResult,
    ) -> None:
        def advance_current_reentry(fresh_reentry) -> None:
            self.third_basis_epoch_continuation_reentry = fresh_reentry

        def record_checkpoint(checkpoint) -> None:
            self.last_third_basis_epoch_cumulative_checkpoint = checkpoint

        await _promote_cumulative_checkpoint_surface(
            self,
            fresh_reentry=result.fresh_reentry,
            checkpoint_result=result,
            spec=_THIRD_BASIS_EPOCH_CUMULATIVE_PROMOTION,
            success_receipt_text=third_basis_epoch_cumulative_checkpoint_success_receipt(
                result
            ),
            advance_current_reentry=advance_current_reentry,
            record_checkpoint=record_checkpoint,
        )


def _root_shas(reentry: ChromiumResearchThirdBasisEpochReentryResult) -> tuple[str, str, str]:
    second_epoch = (
        reentry.prior_second_basis_epoch_continuation_reentry
        .prior_second_basis_epoch_reentry
    )
    first_root = (
        second_epoch.prior_continuation_reentry.prior_root_backed_reentry.loaded_root
    )
    return (
        first_root.verification.root_record_sha256,
        second_epoch.loaded_root.verification.root_record_sha256,
        reentry.loaded_root.verification.root_record_sha256,
    )


def _require_third_basis_epoch_checkpoint_matches_shell(
    result: ChromiumResearchThirdBasisEpochContinuationCheckpointResult,
    *,
    prior: ChromiumResearchThirdBasisEpochReentryResult,
    rollover: ChromiumResearchSessionRolloverResult,
    one_hop_controller,
) -> None:
    if not isinstance(
        result,
        ChromiumResearchThirdBasisEpochContinuationCheckpointResult,
    ):
        raise TypeError(
            "result must be ChromiumResearchThirdBasisEpochContinuationCheckpointResult."
        )
    if result.prior_reentry is not prior:
        raise ValueError(
            "Third-epoch checkpoint did not retain the shell's exact proven launch re-entry."
        )
    if result.rollover is not rollover:
        raise ValueError(
            "Third-epoch checkpoint did not retain the shell's exact chosen rollover."
        )
    if result.fresh_reentry.controller.presentation != one_hop_controller.presentation:
        raise ValueError(
            "Fresh third-epoch continuation checkpoint presentation does not match the mounted one-hop continuation."
        )
    if (
        result.fresh_reentry.controller.declared_endpoint.verification.edge_record_sha256
        != one_hop_controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ValueError(
            "Fresh third-epoch continuation checkpoint endpoint does not match the mounted one-hop continuation."
        )
    if _root_shas(result.fresh_reentry.prior_third_basis_epoch_reentry) != _root_shas(prior):
        raise ValueError(
            "Fresh third-epoch continuation checkpoint does not retain the shell's exact three-root durable ancestry."
        )


def _require_third_basis_epoch_cumulative_checkpoint_matches_shell(
    result: ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionResult,
    *,
    current_reentry: ChromiumResearchThirdBasisEpochContinuationReentryResult,
    rollover: ChromiumResearchSessionRolloverResult,
    one_hop_controller,
) -> None:
    if not isinstance(
        result,
        ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionResult,
    ):
        raise TypeError(
            "result must be ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionResult."
        )
    if result.current_reentry is not current_reentry:
        raise ValueError(
            "40D checkpoint did not retain the shell's exact current third-epoch continuation."
        )
    if result.rollover is not rollover:
        raise ValueError(
            "40D checkpoint did not retain the shell's exact continuation rollover."
        )
    if (
        result.next_plan.prior_third_basis_epoch_overlay_source
        != result.current_plan.prior_third_basis_epoch_overlay_source
    ):
        raise ValueError(
            "40D checkpoint did not preserve the explicit current plan's direct 40B ancestry anchor."
        )
    fresh_endpoint = result.fresh_reentry.controller.declared_endpoint
    one_hop_endpoint = one_hop_controller.declared_endpoint
    if (
        fresh_endpoint.verification.edge_record_sha256
        != one_hop_endpoint.verification.edge_record_sha256
    ):
        raise ValueError(
            "40D fresh cumulative endpoint identity does not match the mounted one-hop continuation."
        )
    if (
        fresh_endpoint.revision.revised_note.note_text
        != one_hop_endpoint.revision.revised_note.note_text
    ):
        raise ValueError(
            "40D fresh cumulative endpoint text does not match the mounted one-hop continuation."
        )
    fresh_third = result.fresh_reentry.prior_third_basis_epoch_reentry
    current_third = current_reentry.prior_third_basis_epoch_reentry
    if fresh_third.controller.presentation != current_third.controller.presentation:
        raise ValueError(
            "40D fresh third-epoch anchor presentation changed cumulative ancestry."
        )
    if (
        fresh_third.controller.declared_endpoint.verification.edge_record_sha256
        != current_third.controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ValueError(
            "40D fresh third-epoch anchor endpoint identity changed cumulative ancestry."
        )
    if _root_shas(fresh_third) != _root_shas(current_third):
        raise ValueError(
            "40D fresh cumulative checkpoint changed retained three-root ancestry."
        )


def create_third_basis_epoch_research_session_shell(
    lineage: ChromiumResearchThirdBasisEpochShellLineage,
) -> ThirdBasisEpochResearchSessionShell:
    """Create one shell retaining exact proven 40B launch lineage."""

    return ThirdBasisEpochResearchSessionShell(lineage)


def create_third_basis_epoch_continuation_research_session_shell(
    lineage: ChromiumResearchThirdBasisEpochContinuationShellLineage,
) -> ThirdBasisEpochContinuationResearchSessionShell:
    """Create one cumulative shell retaining exact proven 40C/40D launch lineage."""

    return ThirdBasisEpochContinuationResearchSessionShell(lineage)


__all__ = [
    "ThirdBasisEpochContinuationResearchSessionShell",
    "ThirdBasisEpochResearchSessionShell",
    "create_third_basis_epoch_continuation_research_session_shell",
    "create_third_basis_epoch_research_session_shell",
]
