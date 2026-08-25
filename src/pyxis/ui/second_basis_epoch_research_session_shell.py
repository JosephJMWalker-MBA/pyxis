from __future__ import annotations

from pathlib import Path

from textual.widgets import Button, Input, Static

from pyxis.app.chromium_research_second_basis_epoch_continuation_reentry_plan_document import (
    ChromiumResearchSecondBasisEpochContinuationCheckpointResult,
    persist_chromium_research_second_basis_epoch_continuation_checkpoint,
)
from pyxis.app.chromium_research_second_basis_epoch_shell_lineage import (
    ChromiumResearchSecondBasisEpochContinuationShellLineage,
    ChromiumResearchSecondBasisEpochShellLineage,
)
from pyxis.app.chromium_research_session_rollover import ChromiumResearchSessionRolloverResult

from .chromium_research_endpoint_revision_textual import ResearchEndpointRevisionControls
from .chromium_research_second_basis_epoch_continuation_checkpoint_textual import (
    SecondBasisEpochResearchSessionContinuationCheckpointControls,
)
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
        """Mount one-hop continuation, then lock it pending explicit 37C proof."""

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
        # Deliberately keep ResearchEndpointRevisionControls locked. 38D does not
        # automatically switch into cumulative 37D mode or rewrite launch lineage.


class SecondBasisEpochContinuationResearchSessionShell(ResearchSessionShell):
    """Controller shell retaining one exact proven 37C/37D launch lineage.

    The supplied 38B continuation wrapper remains explicit launch context only. No
    ordinary 31A lineage, cumulative second-epoch checkpoint controls, path prefilling,
    or automatic persistence authority is inferred from the live controller.
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


def create_second_basis_epoch_research_session_shell(
    lineage: ChromiumResearchSecondBasisEpochShellLineage,
) -> SecondBasisEpochResearchSessionShell:
    """Create one first-checkpoint-aware shell from exact proven 37B launch lineage."""

    return SecondBasisEpochResearchSessionShell(lineage)


def create_second_basis_epoch_continuation_research_session_shell(
    lineage: ChromiumResearchSecondBasisEpochContinuationShellLineage,
) -> SecondBasisEpochContinuationResearchSessionShell:
    """Create one controller shell retaining exact proven 37C/37D launch lineage."""

    return SecondBasisEpochContinuationResearchSessionShell(lineage)


__all__ = [
    "SecondBasisEpochContinuationResearchSessionShell",
    "SecondBasisEpochResearchSessionShell",
    "create_second_basis_epoch_continuation_research_session_shell",
    "create_second_basis_epoch_research_session_shell",
]
