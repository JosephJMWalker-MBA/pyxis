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
from pyxis.app.chromium_research_session_rollover import ChromiumResearchSessionRolloverResult

from .chromium_research_cumulative_checkpoint_promotion_textual import (
    _CumulativeCheckpointPromotionSpec,
    _promote_cumulative_checkpoint_surface,
)
from .chromium_research_cumulative_checkpoint_rollover_textual import (
    _CumulativeCheckpointRolloverMountSpec,
    _mount_cumulative_checkpoint_after_rollover,
)
from .chromium_research_root_backed_session_continuation_checkpoint_extension_textual import (
    RootBackedResearchSessionCumulativeCheckpointControls,
    cumulative_checkpoint_success_receipt,
)
from .research_session_shell import ResearchSessionShell


_ROOT_BACKED_CUMULATIVE_PROMOTION = _CumulativeCheckpointPromotionSpec(
    checkpoint_controls_selector="#research-root-backed-cumulative-checkpoint-controls",
    checkpoint_controls_type=RootBackedResearchSessionCumulativeCheckpointControls,
    success_receipt_id="research-root-backed-cumulative-checkpoint-success-receipt",
    presentation_error=(
        "Fresh cumulative controller presentation is incoherent with retained loaded evidence."
    ),
    context_cardinality_error=(
        "Fresh cumulative session must contain one context per declared position."
    ),
)

_ROOT_BACKED_CUMULATIVE_ROLLOVER = _CumulativeCheckpointRolloverMountSpec(
    stale_success_receipt_selector=(
        "#research-root-backed-cumulative-checkpoint-success-receipt"
    ),
    retained_rollover_error=(
        "Base research shell did not retain the exact cumulative-lineage rollover."
    ),
    restart_plan_error=(
        "Cumulative root-backed shell must not mount ordinary restart-plan controls."
    ),
)


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

        def create_checkpoint_controls(current, rollover):
            return RootBackedResearchSessionCumulativeCheckpointControls(
                current,
                rollover,
            )

        await _mount_cumulative_checkpoint_after_rollover(
            self,
            current_reentry=current_reentry,
            rollover=result,
            spec=_ROOT_BACKED_CUMULATIVE_ROLLOVER,
            create_checkpoint_controls=create_checkpoint_controls,
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

        def advance_current_reentry(fresh_reentry) -> None:
            self.root_backed_continuation_reentry = fresh_reentry

        def record_checkpoint(checkpoint) -> None:
            self.last_root_backed_cumulative_checkpoint = checkpoint

        await _promote_cumulative_checkpoint_surface(
            self,
            fresh_reentry=result.fresh_reentry,
            checkpoint_result=result,
            spec=_ROOT_BACKED_CUMULATIVE_PROMOTION,
            success_receipt_text=cumulative_checkpoint_success_receipt(result),
            advance_current_reentry=advance_current_reentry,
            record_checkpoint=record_checkpoint,
        )


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
