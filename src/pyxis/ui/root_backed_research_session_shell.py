from __future__ import annotations

from pathlib import Path

from textual.widgets import Button, Input, Static

from pyxis.app.chromium_research_root_backed_session_reentry import (
    ChromiumResearchRootBackedSessionReentryResult,
)
from pyxis.app.chromium_research_root_backed_session_continuation_reentry_plan_document import (
    ChromiumResearchRootBackedSessionContinuationCheckpointResult,
    persist_chromium_research_root_backed_session_continuation_checkpoint,
)
from pyxis.app.chromium_research_session_rollover import ChromiumResearchSessionRolloverResult

from .chromium_research_endpoint_revision_textual import ResearchEndpointRevisionControls
from .chromium_research_root_backed_session_continuation_checkpoint_textual import (
    RootBackedResearchSessionContinuationCheckpointControls,
)
from .chromium_research_session_rollover_textual import ResearchSessionRolloverControls
from .research_session_shell import ResearchSessionShell


class RootBackedResearchSessionShell(ResearchSessionShell):
    """Standalone shell retaining one exact 35B lineage for the first 35D checkpoint.

    The base shell still owns inspection, endpoint revision, and explicit 30A rollover.
    This subclass adds only the first root-backed continuation checkpoint boundary.
    It never constructs or stores an ordinary 31A re-entry result.

    After a successful 35D checkpoint this 36B shell remains revision-locked. Moving
    into repeated post-root continuation checkpointing is intentionally deferred to a
    separate authority milestone rather than silently changing lineage families in
    place.
    """

    CSS = ResearchSessionShell.CSS + """
    #research-root-backed-continuation-checkpoint-controls {
        width: 94%;
        height: auto;
        padding: 1 2;
        margin-top: 1;
        border: round $secondary;
    }

    #research-root-backed-checkpoint-authority-notice,
    #research-root-backed-checkpoint-candidate,
    #research-root-backed-checkpoint-prior-overlay-source-label,
    #research-root-backed-checkpoint-successor-source-label,
    #research-root-backed-checkpoint-declaration-source-label,
    #research-root-backed-checkpoint-destination-label,
    #research-root-backed-checkpoint-status {
        margin-top: 1;
    }

    #research-root-backed-checkpoint-title,
    #research-root-backed-checkpoint-prior-overlay-source-label,
    #research-root-backed-checkpoint-successor-source-label,
    #research-root-backed-checkpoint-declaration-source-label,
    #research-root-backed-checkpoint-destination-label {
        text-style: bold;
    }

    #save-research-root-backed-continuation-checkpoint {
        margin-top: 1;
    }
    """

    def __init__(
        self,
        reentry: ChromiumResearchRootBackedSessionReentryResult,
    ) -> None:
        if not isinstance(reentry, ChromiumResearchRootBackedSessionReentryResult):
            raise TypeError(
                "reentry must be ChromiumResearchRootBackedSessionReentryResult."
            )
        super().__init__(reentry.controller)
        self.root_backed_reentry = reentry
        self.last_root_backed_continuation_checkpoint: (
            ChromiumResearchRootBackedSessionContinuationCheckpointResult | None
        ) = None

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save-research-root-backed-continuation-checkpoint":
            event.stop()
            self.call_after_refresh(self._save_root_backed_continuation_checkpoint)
            return
        super().on_button_pressed(event)

    async def _mount_research_rollover(
        self,
        result: ChromiumResearchSessionRolloverResult,
    ) -> None:
        """Mount the base continuation, then require a dedicated 35D checkpoint."""

        await super()._mount_research_rollover(result)
        if self.last_research_rollover is not result:
            raise ValueError(
                "Base research shell did not retain the exact root-backed continuation rollover."
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
            RootBackedResearchSessionContinuationCheckpointControls(result)
        )

    async def _save_root_backed_continuation_checkpoint(self) -> None:
        controls = self.query_one(
            "#research-root-backed-continuation-checkpoint-controls",
            RootBackedResearchSessionContinuationCheckpointControls,
        )
        status = self.query_one("#research-root-backed-checkpoint-status", Static)
        rollover = self.last_research_rollover
        if rollover is None:
            status.update(
                "Root-backed checkpoint failed: no explicit continuation rollover is awaiting a checkpoint."
            )
            return
        if controls.rollover is not rollover:
            status.update(
                "Root-backed checkpoint failed: displayed checkpoint does not match the shell's exact rollover."
            )
            return

        prior_overlay_source = self.query_one(
            "#research-root-backed-checkpoint-prior-overlay-source",
            Input,
        )
        successor_source = self.query_one(
            "#research-root-backed-checkpoint-successor-source",
            Input,
        )
        declaration_source = self.query_one(
            "#research-root-backed-checkpoint-declaration-source",
            Input,
        )
        destination = self.query_one(
            "#research-root-backed-checkpoint-destination",
            Input,
        )
        if not prior_overlay_source.value.strip():
            status.update(
                "Root-backed checkpoint failed: explicit current 35C overlay path is required."
            )
            return
        if not successor_source.value.strip():
            status.update(
                "Root-backed checkpoint failed: explicit current successor edge path is required."
            )
            return
        if not declaration_source.value.strip():
            status.update(
                "Root-backed checkpoint failed: explicit current continuation declaration path is required."
            )
            return
        if not destination.value.strip():
            status.update(
                "Root-backed checkpoint failed: explicit no-overwrite 35D overlay destination is required."
            )
            return

        prior = self.root_backed_reentry
        try:
            checkpoint = persist_chromium_research_root_backed_session_continuation_checkpoint(
                prior,
                rollover,
                prior_root_backed_overlay_source=Path(prior_overlay_source.value),
                successor_edge_source=Path(successor_source.value),
                continuation_declaration_source=Path(declaration_source.value),
                destination=Path(destination.value),
            )
        except Exception as exc:
            status.update(f"Root-backed checkpoint failed: {exc}")
            return

        if checkpoint.prior_reentry is not prior:
            raise ValueError(
                "35D checkpoint did not retain the shell's exact root-backed prior lineage."
            )
        if checkpoint.rollover is not rollover:
            raise ValueError(
                "35D checkpoint did not retain the shell's exact continuation rollover."
            )
        if checkpoint.fresh_reentry.controller.presentation != self.research_controller.presentation:
            raise ValueError(
                "35D checkpoint fresh re-entry does not describe the shell's mounted continuation presentation."
            )
        if (
            checkpoint.fresh_reentry.controller.declared_endpoint.verification.edge_record_sha256
            != self.research_controller.declared_endpoint.verification.edge_record_sha256
        ):
            raise ValueError(
                "35D checkpoint fresh endpoint identity does not match the shell's mounted continuation."
            )
        if (
            checkpoint.fresh_reentry.prior_root_backed_reentry.loaded_root.verification.root_record_sha256
            != prior.loaded_root.verification.root_record_sha256
        ):
            raise ValueError(
                "35D checkpoint fresh root identity does not match the shell's retained root-backed lineage."
            )

        self.last_root_backed_continuation_checkpoint = checkpoint
        controls.lock_after_success(checkpoint)
        # Deliberately do not unlock ResearchEndpointRevisionControls in 36B.


def create_root_backed_research_session_shell(
    reentry: ChromiumResearchRootBackedSessionReentryResult,
) -> RootBackedResearchSessionShell:
    """Create one first-checkpoint-aware shell from an exact fresh 35B result."""

    return RootBackedResearchSessionShell(reentry)


__all__ = [
    "RootBackedResearchSessionShell",
    "create_root_backed_research_session_shell",
]
