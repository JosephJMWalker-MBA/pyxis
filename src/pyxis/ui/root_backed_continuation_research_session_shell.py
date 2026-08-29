from __future__ import annotations

from pathlib import Path

from textual.widgets import Button, Input, Static, TextArea

from pyxis.app.chromium_research_root_backed_session_continuation_checkpoint_extension import (
    ChromiumResearchRootBackedSessionContinuationCheckpointExtensionResult,
    persist_chromium_research_root_backed_session_continuation_checkpoint_extension,
)
from pyxis.app.chromium_research_root_backed_session_continuation_reentry_plan_document import (
    ChromiumResearchRootBackedSessionContinuationReentryResult,
)
from pyxis.app.chromium_research_second_changed_basis_revision_root import (
    ChromiumResearchSecondChangedBasisRevisionRootResult,
    persist_chromium_research_second_changed_basis_revision_root,
)
from pyxis.app.chromium_research_second_changed_basis_transition import (
    ChromiumResearchSecondChangedBasisTransitionResult,
    persist_chromium_research_second_changed_basis_transition,
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
from .chromium_research_second_changed_basis_revision_root_textual import (
    ResearchSecondChangedBasisRevisionRootControls,
)
from .chromium_research_second_changed_basis_transition_textual import (
    ResearchSecondChangedBasisTransitionControls,
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

    The base shell owns governed inspection, endpoint revision, explicit 30A rollover,
    and optional 44A changed-basis preparation. This subclass adds the 35E cumulative
    checkpoint transition and, only after exact predecessor successes, one explicit
    46A second changed-basis 33B transition and one 46B second changed-basis 34A root.

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

    #research-second-changed-basis-transition-controls {
        width: 94%;
        height: auto;
        padding: 1 2;
        margin-top: 1;
        border: round $warning;
    }

    #research-second-changed-basis-transition-authority-notice,
    #research-second-changed-basis-transition-prepared-summary,
    #research-second-changed-basis-transition-prior-edge-source-label,
    #research-second-changed-basis-transition-working-set-source-label,
    #research-second-changed-basis-transition-note-source-label,
    #research-second-changed-basis-transition-destination-label,
    #research-second-changed-basis-transition-status {
        margin-top: 1;
    }

    #research-second-changed-basis-transition-title,
    #research-second-changed-basis-transition-prior-edge-source-label,
    #research-second-changed-basis-transition-working-set-source-label,
    #research-second-changed-basis-transition-note-source-label,
    #research-second-changed-basis-transition-destination-label {
        text-style: bold;
    }

    #persist-research-second-changed-basis-transition {
        margin-top: 1;
    }

    #research-second-changed-basis-revision-root-controls {
        width: 94%;
        height: auto;
        padding: 1 2;
        margin-top: 1;
        border: round $warning;
    }

    #research-second-changed-basis-revision-root-authority-notice,
    #research-second-changed-basis-revision-root-transition-summary,
    #research-second-changed-basis-revision-root-rationale-label,
    #research-second-changed-basis-revision-root-prior-edge-source-label,
    #research-second-changed-basis-revision-root-working-set-source-label,
    #research-second-changed-basis-revision-root-note-source-label,
    #research-second-changed-basis-revision-root-transition-source-label,
    #research-second-changed-basis-revision-root-destination-label,
    #research-second-changed-basis-revision-root-status {
        margin-top: 1;
    }

    #research-second-changed-basis-revision-root-title,
    #research-second-changed-basis-revision-root-rationale-label,
    #research-second-changed-basis-revision-root-prior-edge-source-label,
    #research-second-changed-basis-revision-root-working-set-source-label,
    #research-second-changed-basis-revision-root-note-source-label,
    #research-second-changed-basis-revision-root-transition-source-label,
    #research-second-changed-basis-revision-root-destination-label {
        text-style: bold;
    }

    #research-second-changed-basis-revision-root-rationale {
        width: 100%;
        height: 8;
        margin-top: 1;
    }

    #persist-research-second-changed-basis-revision-root {
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
        self.last_second_changed_basis_transition: (
            ChromiumResearchSecondChangedBasisTransitionResult | None
        ) = None
        self.last_second_changed_basis_revision_root: (
            ChromiumResearchSecondChangedBasisRevisionRootResult | None
        ) = None

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "persist-research-second-changed-basis-revision-root":
            event.stop()
            self.call_after_refresh(self._persist_second_changed_basis_revision_root)
            return
        if event.button.id == "persist-research-second-changed-basis-transition":
            event.stop()
            self.call_after_refresh(self._persist_second_changed_basis_transition)
            return
        if event.button.id == "save-research-root-backed-cumulative-checkpoint":
            event.stop()
            self.call_after_refresh(self._save_root_backed_cumulative_checkpoint)
            return
        super().on_button_pressed(event)

    async def _persist_research_changed_basis_preparation(self) -> None:
        """Run inherited 44A, then expose 46A only for a new exact continuation success."""

        prior = self.last_changed_basis_preparation
        await super()._persist_research_changed_basis_preparation()
        prepared = self.last_changed_basis_preparation
        if prepared is None or prepared is prior:
            return
        current_reentry = self.root_backed_continuation_reentry
        if self.research_controller is not current_reentry.controller:
            raise ValueError(
                "Second changed-basis preparation no longer belongs to the exact retained continuation controller."
            )
        if self.research_controller.declared_endpoint is not prepared.prior_endpoint:
            raise ValueError(
                "Second changed-basis preparation does not retain the mounted continuation endpoint."
            )
        if len(self.query("#research-second-changed-basis-transition-controls")) != 0:
            raise ValueError("Second changed-basis transition controls are already mounted.")
        await self.mount(ResearchSecondChangedBasisTransitionControls(prepared))

    async def _persist_second_changed_basis_transition(self) -> None:
        controls = self.query_one(
            "#research-second-changed-basis-transition-controls",
            ResearchSecondChangedBasisTransitionControls,
        )
        status = self.query_one(
            "#research-second-changed-basis-transition-status", Static
        )
        if controls.stale:
            status.update(
                "Second transition failed: this prepared basis is stale and will not be silently retargeted."
            )
            return

        prepared = self.last_changed_basis_preparation
        current_reentry = self.root_backed_continuation_reentry
        if prepared is None or controls.prepared is not prepared:
            status.update(
                "Second transition failed: no exact successful 44A preparation owns this transition form."
            )
            return
        if (
            self.research_controller is not current_reentry.controller
            or self.research_controller.declared_endpoint is not prepared.prior_endpoint
        ):
            controls.mark_stale()
            return

        prior_edge_source = self.query_one(
            "#research-second-changed-basis-transition-prior-edge-source", Input
        )
        working_set_source = self.query_one(
            "#research-second-changed-basis-transition-working-set-source", Input
        )
        note_source = self.query_one(
            "#research-second-changed-basis-transition-note-source", Input
        )
        destination = self.query_one(
            "#research-second-changed-basis-transition-destination", Input
        )
        required = (
            (prior_edge_source, "explicit current prior endpoint edge path"),
            (working_set_source, "explicit prepared working-set path"),
            (note_source, "explicit prepared working-set-note path"),
            (destination, "explicit second transition destination path"),
        )
        for widget, label in required:
            if not widget.value.strip():
                status.update(f"Second transition failed: {label} is required.")
                return

        controller = self.research_controller
        session = self.research_session
        try:
            result = persist_chromium_research_second_changed_basis_transition(
                controller,
                current_reentry,
                prepared,
                prior_edge_source=Path(prior_edge_source.value),
                working_set_source=Path(working_set_source.value),
                note_source=Path(note_source.value),
                destination=Path(destination.value),
            )
        except Exception as exc:
            status.update(f"Second transition failed: {exc}")
            return

        if result.controller is not controller:
            raise ValueError(
                "Second changed-basis transition did not retain the exact mounted controller."
            )
        if result.continuation_reentry is not current_reentry:
            raise ValueError(
                "Second changed-basis transition did not retain the exact continuation re-entry."
            )
        if result.prepared is not prepared:
            raise ValueError(
                "Second changed-basis transition did not retain the exact prepared basis."
            )
        if (
            self.research_controller is not controller
            or self.research_session is not session
            or self.root_backed_continuation_reentry is not current_reentry
        ):
            raise ValueError(
                "Mounted one-root continuation changed during second changed-basis transition persistence."
            )

        self.last_second_changed_basis_transition = result
        controls.lock_after_success(result)
        if len(self.query("#research-second-changed-basis-revision-root-controls")) != 0:
            raise ValueError("Second changed-basis revision-root controls are already mounted.")
        await self.mount(ResearchSecondChangedBasisRevisionRootControls(result))

    async def _persist_second_changed_basis_revision_root(self) -> None:
        controls = self.query_one(
            "#research-second-changed-basis-revision-root-controls",
            ResearchSecondChangedBasisRevisionRootControls,
        )
        status = self.query_one(
            "#research-second-changed-basis-revision-root-status", Static
        )
        transition_result = self.last_second_changed_basis_transition
        if transition_result is None or controls.transition_result is not transition_result:
            status.update(
                "Second root failed: no exact successful 46A transition owns this root form."
            )
            return

        rationale = self.query_one(
            "#research-second-changed-basis-revision-root-rationale", TextArea
        )
        if not rationale.text.strip():
            status.update("Second root failed: a new human rationale is required.")
            return

        prior_edge_source = self.query_one(
            "#research-second-changed-basis-revision-root-prior-edge-source", Input
        )
        working_set_source = self.query_one(
            "#research-second-changed-basis-revision-root-working-set-source", Input
        )
        note_source = self.query_one(
            "#research-second-changed-basis-revision-root-note-source", Input
        )
        transition_source = self.query_one(
            "#research-second-changed-basis-revision-root-transition-source", Input
        )
        destination = self.query_one(
            "#research-second-changed-basis-revision-root-destination", Input
        )
        required = (
            (prior_edge_source, "explicit prior endpoint edge path"),
            (working_set_source, "explicit changed working-set path"),
            (note_source, "explicit changed working-set-note path"),
            (transition_source, "explicit second changed-basis transition path"),
            (destination, "explicit second revision-root destination path"),
        )
        for widget, label in required:
            if not widget.value.strip():
                status.update(f"Second root failed: {label} is required.")
                return

        mounted_controller = self.research_controller
        mounted_session = self.research_session
        mounted_reentry = self.root_backed_continuation_reentry
        try:
            result = persist_chromium_research_second_changed_basis_revision_root(
                transition_result,
                revised_note_text=rationale.text,
                prior_edge_source=Path(prior_edge_source.value),
                working_set_source=Path(working_set_source.value),
                note_source=Path(note_source.value),
                transition_source=Path(transition_source.value),
                destination=Path(destination.value),
            )
        except Exception as exc:
            status.update(f"Second root failed: {exc}")
            return

        if result.transition_result is not transition_result:
            raise ValueError(
                "Second changed-basis root did not retain the exact successful 46A transition."
            )
        if (
            self.research_controller is not mounted_controller
            or self.research_session is not mounted_session
            or self.root_backed_continuation_reentry is not mounted_reentry
        ):
            raise ValueError(
                "Mounted one-root continuation changed during second root persistence."
            )

        self.last_second_changed_basis_revision_root = result
        controls.lock_after_success(result)

    async def _mount_research_rollover(
        self,
        result: ChromiumResearchSessionRolloverResult,
    ) -> None:
        """Mount one-hop continuation, staling unsaved 46A, then require 35E proof."""

        if len(self.query("#research-second-changed-basis-transition-controls")) != 0:
            self.query_one(
                "#research-second-changed-basis-transition-controls",
                ResearchSecondChangedBasisTransitionControls,
            ).mark_stale()
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

        submission = controls._collect_cumulative_checkpoint_path_submission(
            current_overlay_required=(
                "Cumulative checkpoint failed: explicit current 35D/35E overlay path is required."
            ),
            successor_required=(
                "Cumulative checkpoint failed: explicit current successor edge path is required."
            ),
            declaration_required=(
                "Cumulative checkpoint failed: explicit no-overwrite cumulative declaration destination is required."
            ),
            next_overlay_required=(
                "Cumulative checkpoint failed: explicit no-overwrite next overlay destination is required."
            ),
        )
        if submission is None:
            return

        try:
            checkpoint = (
                persist_chromium_research_root_backed_session_continuation_checkpoint_extension(
                    current_reentry,
                    rollover,
                    current_overlay_source=submission.current_overlay_source,
                    successor_edge_source=submission.successor_edge_source,
                    cumulative_declaration_destination=(
                        submission.cumulative_declaration_destination
                    ),
                    next_overlay_destination=submission.next_overlay_destination,
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
