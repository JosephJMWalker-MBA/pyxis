from __future__ import annotations

from pathlib import Path

from textual.widgets import Button, Input, Static

from pyxis.app.chromium_research_session_rollover import ChromiumResearchSessionRolloverResult
from pyxis.app.chromium_research_third_basis_epoch_continuation_reentry_plan_document import (
    ChromiumResearchThirdBasisEpochContinuationCheckpointResult,
    persist_chromium_research_third_basis_epoch_continuation_checkpoint,
)
from pyxis.app.chromium_research_third_basis_epoch_reentry import (
    ChromiumResearchThirdBasisEpochReentryResult,
)
from pyxis.app.chromium_research_third_basis_epoch_shell_lineage import (
    ChromiumResearchThirdBasisEpochContinuationShellLineage,
    ChromiumResearchThirdBasisEpochShellLineage,
)

from .chromium_research_endpoint_revision_textual import ResearchEndpointRevisionControls
from .chromium_research_session_rollover_textual import ResearchSessionRolloverControls
from .chromium_research_third_basis_epoch_continuation_checkpoint_textual import (
    ThirdBasisEpochResearchSessionContinuationCheckpointControls,
)
from .research_session_shell import ResearchSessionShell


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
    """Controller shell retaining one exact proven 40C/40D launch lineage.

    The supplied 41A continuation wrapper remains explicit launch context only. No
    ordinary 31A lineage, cumulative third-epoch checkpoint controls, path prefilling,
    automatic persistence, or inspection authority is inferred from the live
    controller. Repeatable 40D checkpointing remains outside 41C.
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


def create_third_basis_epoch_research_session_shell(
    lineage: ChromiumResearchThirdBasisEpochShellLineage,
) -> ThirdBasisEpochResearchSessionShell:
    """Create one shell retaining exact proven 40B launch lineage."""

    return ThirdBasisEpochResearchSessionShell(lineage)


def create_third_basis_epoch_continuation_research_session_shell(
    lineage: ChromiumResearchThirdBasisEpochContinuationShellLineage,
) -> ThirdBasisEpochContinuationResearchSessionShell:
    """Create one controller shell retaining exact proven 40C/40D launch lineage."""

    return ThirdBasisEpochContinuationResearchSessionShell(lineage)


__all__ = [
    "ThirdBasisEpochContinuationResearchSessionShell",
    "ThirdBasisEpochResearchSessionShell",
    "create_third_basis_epoch_continuation_research_session_shell",
    "create_third_basis_epoch_research_session_shell",
]
