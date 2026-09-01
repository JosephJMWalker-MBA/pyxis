from __future__ import annotations

from pathlib import Path

from textual.widgets import Button, Input, Static

from pyxis.app.chromium_research_second_basis_epoch_continuation_reentry_plan_document import (
    ChromiumResearchSecondBasisEpochContinuationReentryResult,
)
from pyxis.app.chromium_research_second_basis_epoch_shell_lineage import (
    ChromiumResearchSecondBasisEpochContinuationShellLineage,
)
from pyxis.app.chromium_research_session_rollover import ChromiumResearchSessionRolloverResult
from pyxis.app.chromium_research_third_changed_basis_transition import (
    ChromiumResearchThirdChangedBasisTransitionResult,
    persist_chromium_research_third_changed_basis_transition,
)

from .chromium_research_third_changed_basis_transition_textual import (
    ResearchThirdChangedBasisTransitionControls,
)
from .second_basis_epoch_authority_inspection_shell import (
    InspectableSecondBasisEpochContinuationHandoffResearchSessionShell,
    InspectableSecondBasisEpochContinuationResearchSessionShell,
)
from .second_basis_epoch_cumulative_handoff_shell import (
    SecondBasisEpochContinuationHandoffResearchSessionShell,
)
from .second_basis_epoch_research_session_shell import (
    SecondBasisEpochContinuationResearchSessionShell,
)


_THIRD_CHANGED_BASIS_TRANSITION_CSS = """
#research-third-changed-basis-transition-controls {
    width: 94%;
    height: auto;
    padding: 1 2;
    margin-top: 1;
    border: round $warning;
}

#research-third-changed-basis-transition-authority-notice,
#research-third-changed-basis-transition-prepared-summary,
#research-third-changed-basis-transition-prior-edge-source-label,
#research-third-changed-basis-transition-working-set-source-label,
#research-third-changed-basis-transition-note-source-label,
#research-third-changed-basis-transition-destination-label,
#research-third-changed-basis-transition-status {
    margin-top: 1;
}

#research-third-changed-basis-transition-title,
#research-third-changed-basis-transition-prior-edge-source-label,
#research-third-changed-basis-transition-working-set-source-label,
#research-third-changed-basis-transition-note-source-label,
#research-third-changed-basis-transition-destination-label {
    text-style: bold;
}

#persist-research-third-changed-basis-transition {
    margin-top: 1;
}
"""


class _ThirdChangedBasisTransitionProductMixin:
    """47A-only product behavior shared by persisted and raw second-epoch launches."""

    last_third_changed_basis_transition: ChromiumResearchThirdChangedBasisTransitionResult | None

    def __init__(self, authority) -> None:
        super().__init__(authority)
        self.last_third_changed_basis_transition = None

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "persist-research-third-changed-basis-transition":
            event.stop()
            self.call_after_refresh(self._persist_third_changed_basis_transition)
            return
        super().on_button_pressed(event)

    async def _persist_research_changed_basis_preparation(self) -> None:
        """Run inherited 44A, then expose 47A only for a new exact continuation success."""

        prior = self.last_changed_basis_preparation
        await super()._persist_research_changed_basis_preparation()
        prepared = self.last_changed_basis_preparation
        if prepared is None or prepared is prior:
            return

        current_reentry = self.second_basis_epoch_continuation_reentry
        if type(current_reentry) is not ChromiumResearchSecondBasisEpochContinuationReentryResult:
            raise TypeError(
                "47A requires exactly ChromiumResearchSecondBasisEpochContinuationReentryResult."
            )
        if self.research_controller is not current_reentry.controller:
            raise ValueError(
                "Third changed-basis preparation no longer belongs to the exact retained second-epoch continuation controller."
            )
        if self.research_controller.declared_endpoint is not prepared.prior_endpoint:
            raise ValueError(
                "Third changed-basis preparation does not retain the mounted second-epoch continuation endpoint."
            )
        if len(self.query("#research-third-changed-basis-transition-controls")) != 0:
            raise ValueError("Third changed-basis transition controls are already mounted.")
        await self.mount(ResearchThirdChangedBasisTransitionControls(prepared))

    async def _persist_third_changed_basis_transition(self) -> None:
        controls = self.query_one(
            "#research-third-changed-basis-transition-controls",
            ResearchThirdChangedBasisTransitionControls,
        )
        status = self.query_one(
            "#research-third-changed-basis-transition-status",
            Static,
        )
        if controls.stale:
            status.update(
                "Third transition failed: this prepared basis is stale and will not be silently retargeted."
            )
            return

        prepared = self.last_changed_basis_preparation
        current_reentry = self.second_basis_epoch_continuation_reentry
        if prepared is None or controls.prepared is not prepared:
            status.update(
                "Third transition failed: no exact successful 44A preparation owns this transition form."
            )
            return
        if type(current_reentry) is not ChromiumResearchSecondBasisEpochContinuationReentryResult:
            status.update(
                "Third transition failed: exact second-basis-epoch continuation authority is absent."
            )
            return
        if (
            self.research_controller is not current_reentry.controller
            or self.research_controller.declared_endpoint is not prepared.prior_endpoint
        ):
            controls.mark_stale()
            return

        prior_edge_source = self.query_one(
            "#research-third-changed-basis-transition-prior-edge-source", Input
        )
        working_set_source = self.query_one(
            "#research-third-changed-basis-transition-working-set-source", Input
        )
        note_source = self.query_one(
            "#research-third-changed-basis-transition-note-source", Input
        )
        destination = self.query_one(
            "#research-third-changed-basis-transition-destination", Input
        )
        required = (
            (prior_edge_source, "explicit current prior endpoint edge path"),
            (working_set_source, "explicit prepared working-set path"),
            (note_source, "explicit prepared working-set-note path"),
            (destination, "explicit third transition destination path"),
        )
        for widget, label in required:
            if not widget.value.strip():
                status.update(f"Third transition failed: {label} is required.")
                return

        controller = self.research_controller
        session = self.research_session
        try:
            result = persist_chromium_research_third_changed_basis_transition(
                controller,
                current_reentry,
                prepared,
                prior_edge_source=Path(prior_edge_source.value),
                working_set_source=Path(working_set_source.value),
                note_source=Path(note_source.value),
                destination=Path(destination.value),
            )
        except Exception as exc:
            status.update(f"Third transition failed: {exc}")
            return

        if result.controller is not controller:
            raise ValueError(
                "Third changed-basis transition did not retain the exact mounted controller."
            )
        if result.continuation_reentry is not current_reentry:
            raise ValueError(
                "Third changed-basis transition did not retain the exact second-epoch continuation re-entry."
            )
        if result.prepared is not prepared:
            raise ValueError(
                "Third changed-basis transition did not retain the exact prepared basis."
            )
        if (
            self.research_controller is not controller
            or self.research_session is not session
            or self.second_basis_epoch_continuation_reentry is not current_reentry
        ):
            raise ValueError(
                "Mounted second-epoch continuation changed during third changed-basis transition persistence."
            )

        self.last_third_changed_basis_transition = result
        controls.lock_after_success(result)

    async def _mount_research_rollover(
        self,
        result: ChromiumResearchSessionRolloverResult,
    ) -> None:
        if len(self.query("#research-third-changed-basis-transition-controls")) != 0:
            controls = self.query_one(
                "#research-third-changed-basis-transition-controls",
                ResearchThirdChangedBasisTransitionControls,
            )
            controls.mark_stale()
        await super()._mount_research_rollover(result)


class ThirdChangedBasisTransitionResearchSessionShell(
    _ThirdChangedBasisTransitionProductMixin,
    SecondBasisEpochContinuationResearchSessionShell,
):
    """47A product from one path-proofed persisted 37C/37D continuation launch."""

    CSS = SecondBasisEpochContinuationResearchSessionShell.CSS + _THIRD_CHANGED_BASIS_TRANSITION_CSS


class ThirdChangedBasisTransitionHandoffResearchSessionShell(
    _ThirdChangedBasisTransitionProductMixin,
    SecondBasisEpochContinuationHandoffResearchSessionShell,
):
    """47A product from one exact pathless 38F continuation handoff."""

    CSS = SecondBasisEpochContinuationHandoffResearchSessionShell.CSS + _THIRD_CHANGED_BASIS_TRANSITION_CSS


class InspectableThirdChangedBasisTransitionResearchSessionShell(
    _ThirdChangedBasisTransitionProductMixin,
    InspectableSecondBasisEpochContinuationResearchSessionShell,
):
    """Path-proofed 47A product retaining immutable second-epoch launch provenance."""

    CSS = (
        InspectableSecondBasisEpochContinuationResearchSessionShell.CSS
        + _THIRD_CHANGED_BASIS_TRANSITION_CSS
    )


class InspectableThirdChangedBasisTransitionHandoffResearchSessionShell(
    _ThirdChangedBasisTransitionProductMixin,
    InspectableSecondBasisEpochContinuationHandoffResearchSessionShell,
):
    """Pathless 47A product retaining immutable raw 38F launch provenance."""

    CSS = (
        InspectableSecondBasisEpochContinuationHandoffResearchSessionShell.CSS
        + _THIRD_CHANGED_BASIS_TRANSITION_CSS
    )


def create_third_changed_basis_transition_research_session_shell(
    lineage: ChromiumResearchSecondBasisEpochContinuationShellLineage,
) -> ThirdChangedBasisTransitionResearchSessionShell:
    if not isinstance(
        lineage,
        ChromiumResearchSecondBasisEpochContinuationShellLineage,
    ):
        raise TypeError(
            "lineage must be ChromiumResearchSecondBasisEpochContinuationShellLineage."
        )
    return ThirdChangedBasisTransitionResearchSessionShell(lineage)


def create_third_changed_basis_transition_handoff_research_session_shell(
    reentry: ChromiumResearchSecondBasisEpochContinuationReentryResult,
) -> ThirdChangedBasisTransitionHandoffResearchSessionShell:
    if type(reentry) is not ChromiumResearchSecondBasisEpochContinuationReentryResult:
        raise TypeError(
            "reentry must be exactly ChromiumResearchSecondBasisEpochContinuationReentryResult."
        )
    return ThirdChangedBasisTransitionHandoffResearchSessionShell(reentry)


def create_inspectable_third_changed_basis_transition_research_session_shell(
    lineage: ChromiumResearchSecondBasisEpochContinuationShellLineage,
) -> InspectableThirdChangedBasisTransitionResearchSessionShell:
    if not isinstance(
        lineage,
        ChromiumResearchSecondBasisEpochContinuationShellLineage,
    ):
        raise TypeError(
            "lineage must be ChromiumResearchSecondBasisEpochContinuationShellLineage."
        )
    return InspectableThirdChangedBasisTransitionResearchSessionShell(lineage)


def create_inspectable_third_changed_basis_transition_handoff_research_session_shell(
    reentry: ChromiumResearchSecondBasisEpochContinuationReentryResult,
) -> InspectableThirdChangedBasisTransitionHandoffResearchSessionShell:
    if type(reentry) is not ChromiumResearchSecondBasisEpochContinuationReentryResult:
        raise TypeError(
            "reentry must be exactly ChromiumResearchSecondBasisEpochContinuationReentryResult."
        )
    return InspectableThirdChangedBasisTransitionHandoffResearchSessionShell(reentry)


__all__ = [
    "InspectableThirdChangedBasisTransitionHandoffResearchSessionShell",
    "InspectableThirdChangedBasisTransitionResearchSessionShell",
    "ThirdChangedBasisTransitionHandoffResearchSessionShell",
    "ThirdChangedBasisTransitionResearchSessionShell",
    "create_inspectable_third_changed_basis_transition_handoff_research_session_shell",
    "create_inspectable_third_changed_basis_transition_research_session_shell",
    "create_third_changed_basis_transition_handoff_research_session_shell",
    "create_third_changed_basis_transition_research_session_shell",
]
