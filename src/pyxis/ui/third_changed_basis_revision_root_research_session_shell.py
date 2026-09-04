from __future__ import annotations

from pathlib import Path

from textual.widgets import Button, Input, Static, TextArea

from pyxis.app.chromium_research_second_basis_epoch_continuation_reentry_plan_document import (
    ChromiumResearchSecondBasisEpochContinuationReentryResult,
)
from pyxis.app.chromium_research_second_basis_epoch_shell_lineage import (
    ChromiumResearchSecondBasisEpochContinuationShellLineage,
)
from pyxis.app.chromium_research_third_changed_basis_revision_root import (
    ChromiumResearchThirdChangedBasisRevisionRootResult,
    persist_chromium_research_third_changed_basis_revision_root,
)

from .chromium_research_third_changed_basis_revision_root_textual import (
    ResearchThirdChangedBasisRevisionRootControls,
)
from .third_changed_basis_transition_research_session_shell import (
    InspectableThirdChangedBasisTransitionHandoffResearchSessionShell,
    InspectableThirdChangedBasisTransitionResearchSessionShell,
    ThirdChangedBasisTransitionHandoffResearchSessionShell,
    ThirdChangedBasisTransitionResearchSessionShell,
)


_THIRD_CHANGED_BASIS_REVISION_ROOT_CSS = """
#research-third-changed-basis-revision-root-controls {
    width: 94%;
    height: auto;
    padding: 1 2;
    margin-top: 1;
    border: round $warning;
}

#research-third-changed-basis-revision-root-authority-notice,
#research-third-changed-basis-revision-root-transition-summary,
#research-third-changed-basis-revision-root-rationale-label,
#research-third-changed-basis-revision-root-prior-edge-source-label,
#research-third-changed-basis-revision-root-working-set-source-label,
#research-third-changed-basis-revision-root-note-source-label,
#research-third-changed-basis-revision-root-transition-source-label,
#research-third-changed-basis-revision-root-destination-label,
#research-third-changed-basis-revision-root-status {
    margin-top: 1;
}

#research-third-changed-basis-revision-root-title,
#research-third-changed-basis-revision-root-rationale-label,
#research-third-changed-basis-revision-root-prior-edge-source-label,
#research-third-changed-basis-revision-root-working-set-source-label,
#research-third-changed-basis-revision-root-note-source-label,
#research-third-changed-basis-revision-root-transition-source-label,
#research-third-changed-basis-revision-root-destination-label {
    text-style: bold;
}

#research-third-changed-basis-revision-root-rationale {
    width: 100%;
    height: 8;
    margin-top: 1;
}

#persist-research-third-changed-basis-revision-root {
    margin-top: 1;
}
"""


class _ThirdChangedBasisRevisionRootProductMixin:
    """47B-only behavior shared by the four dedicated 47A launch products."""

    last_third_changed_basis_revision_root: ChromiumResearchThirdChangedBasisRevisionRootResult | None

    def __init__(self, authority) -> None:
        super().__init__(authority)
        self.last_third_changed_basis_revision_root = None

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Own only the 47B action; inherited Textual handlers remain MRO-dispatched."""

        if event.button.id == "persist-research-third-changed-basis-revision-root":
            event.stop()
            self.call_after_refresh(self._persist_third_changed_basis_revision_root)

    async def _persist_third_changed_basis_transition(self) -> None:
        """Run inherited 47A, then mount 47B only after one new exact success."""

        prior = self.last_third_changed_basis_transition
        await super()._persist_third_changed_basis_transition()
        transition_result = self.last_third_changed_basis_transition
        if transition_result is None or transition_result is prior:
            return
        if len(self.query("#research-third-changed-basis-revision-root-controls")) != 0:
            raise ValueError(
                "Third changed-basis revision-root controls are already mounted."
            )
        await self.mount(ResearchThirdChangedBasisRevisionRootControls(transition_result))

    async def _persist_third_changed_basis_revision_root(self) -> None:
        controls = self.query_one(
            "#research-third-changed-basis-revision-root-controls",
            ResearchThirdChangedBasisRevisionRootControls,
        )
        status = self.query_one(
            "#research-third-changed-basis-revision-root-status", Static
        )
        transition_result = self.last_third_changed_basis_transition
        if transition_result is None or controls.transition_result is not transition_result:
            status.update(
                "Root failed: no exact successful third changed-basis transition owns this form."
            )
            return

        rationale = self.query_one(
            "#research-third-changed-basis-revision-root-rationale", TextArea
        )
        if not rationale.text.strip():
            status.update("Root failed: a new human rationale is required.")
            return

        prior_edge_source = self.query_one(
            "#research-third-changed-basis-revision-root-prior-edge-source", Input
        )
        working_set_source = self.query_one(
            "#research-third-changed-basis-revision-root-working-set-source", Input
        )
        note_source = self.query_one(
            "#research-third-changed-basis-revision-root-note-source", Input
        )
        transition_source = self.query_one(
            "#research-third-changed-basis-revision-root-transition-source", Input
        )
        destination = self.query_one(
            "#research-third-changed-basis-revision-root-destination", Input
        )
        required = (
            (prior_edge_source, "explicit prior endpoint edge path"),
            (working_set_source, "explicit changed working-set path"),
            (note_source, "explicit changed working-set-note path"),
            (transition_source, "explicit third changed-basis transition path"),
            (destination, "explicit third revision-root destination path"),
        )
        for widget, label in required:
            if not widget.value.strip():
                status.update(f"Root failed: {label} is required.")
                return

        mounted_controller = self.research_controller
        mounted_session = self.research_session
        mounted_reentry = self.second_basis_epoch_continuation_reentry
        try:
            result = persist_chromium_research_third_changed_basis_revision_root(
                transition_result,
                revised_note_text=rationale.text,
                prior_edge_source=Path(prior_edge_source.value),
                working_set_source=Path(working_set_source.value),
                note_source=Path(note_source.value),
                transition_source=Path(transition_source.value),
                destination=Path(destination.value),
            )
        except Exception as exc:
            status.update(f"Root failed: {exc}")
            return

        if result.transition_result is not transition_result:
            raise ValueError(
                "Third changed-basis root did not retain the exact successful 47A transition."
            )
        if (
            self.research_controller is not mounted_controller
            or self.research_session is not mounted_session
            or self.second_basis_epoch_continuation_reentry is not mounted_reentry
        ):
            raise ValueError(
                "Mounted second-epoch continuation changed during third root persistence."
            )

        self.last_third_changed_basis_revision_root = result
        controls.lock_after_success(result)


class ThirdChangedBasisRevisionRootResearchSessionShell(
    _ThirdChangedBasisRevisionRootProductMixin,
    ThirdChangedBasisTransitionResearchSessionShell,
):
    """47B product from one path-proofed persisted second-epoch continuation launch."""

    CSS = ThirdChangedBasisTransitionResearchSessionShell.CSS + _THIRD_CHANGED_BASIS_REVISION_ROOT_CSS


class ThirdChangedBasisRevisionRootHandoffResearchSessionShell(
    _ThirdChangedBasisRevisionRootProductMixin,
    ThirdChangedBasisTransitionHandoffResearchSessionShell,
):
    """47B product from one exact pathless second-epoch continuation handoff."""

    CSS = ThirdChangedBasisTransitionHandoffResearchSessionShell.CSS + _THIRD_CHANGED_BASIS_REVISION_ROOT_CSS


class InspectableThirdChangedBasisRevisionRootResearchSessionShell(
    _ThirdChangedBasisRevisionRootProductMixin,
    InspectableThirdChangedBasisTransitionResearchSessionShell,
):
    """Inspectable persisted-launch 47B product retaining immutable launch provenance."""

    CSS = (
        InspectableThirdChangedBasisTransitionResearchSessionShell.CSS
        + _THIRD_CHANGED_BASIS_REVISION_ROOT_CSS
    )


class InspectableThirdChangedBasisRevisionRootHandoffResearchSessionShell(
    _ThirdChangedBasisRevisionRootProductMixin,
    InspectableThirdChangedBasisTransitionHandoffResearchSessionShell,
):
    """Inspectable pathless 47B product retaining immutable raw launch provenance."""

    CSS = (
        InspectableThirdChangedBasisTransitionHandoffResearchSessionShell.CSS
        + _THIRD_CHANGED_BASIS_REVISION_ROOT_CSS
    )


def create_third_changed_basis_revision_root_research_session_shell(
    lineage: ChromiumResearchSecondBasisEpochContinuationShellLineage,
) -> ThirdChangedBasisRevisionRootResearchSessionShell:
    if not isinstance(lineage, ChromiumResearchSecondBasisEpochContinuationShellLineage):
        raise TypeError(
            "lineage must be ChromiumResearchSecondBasisEpochContinuationShellLineage."
        )
    return ThirdChangedBasisRevisionRootResearchSessionShell(lineage)


def create_third_changed_basis_revision_root_handoff_research_session_shell(
    reentry: ChromiumResearchSecondBasisEpochContinuationReentryResult,
) -> ThirdChangedBasisRevisionRootHandoffResearchSessionShell:
    if type(reentry) is not ChromiumResearchSecondBasisEpochContinuationReentryResult:
        raise TypeError(
            "reentry must be exactly ChromiumResearchSecondBasisEpochContinuationReentryResult."
        )
    return ThirdChangedBasisRevisionRootHandoffResearchSessionShell(reentry)


def create_inspectable_third_changed_basis_revision_root_research_session_shell(
    lineage: ChromiumResearchSecondBasisEpochContinuationShellLineage,
) -> InspectableThirdChangedBasisRevisionRootResearchSessionShell:
    if not isinstance(lineage, ChromiumResearchSecondBasisEpochContinuationShellLineage):
        raise TypeError(
            "lineage must be ChromiumResearchSecondBasisEpochContinuationShellLineage."
        )
    return InspectableThirdChangedBasisRevisionRootResearchSessionShell(lineage)


def create_inspectable_third_changed_basis_revision_root_handoff_research_session_shell(
    reentry: ChromiumResearchSecondBasisEpochContinuationReentryResult,
) -> InspectableThirdChangedBasisRevisionRootHandoffResearchSessionShell:
    if type(reentry) is not ChromiumResearchSecondBasisEpochContinuationReentryResult:
        raise TypeError(
            "reentry must be exactly ChromiumResearchSecondBasisEpochContinuationReentryResult."
        )
    return InspectableThirdChangedBasisRevisionRootHandoffResearchSessionShell(reentry)


__all__ = [
    "InspectableThirdChangedBasisRevisionRootHandoffResearchSessionShell",
    "InspectableThirdChangedBasisRevisionRootResearchSessionShell",
    "ThirdChangedBasisRevisionRootHandoffResearchSessionShell",
    "ThirdChangedBasisRevisionRootResearchSessionShell",
    "create_inspectable_third_changed_basis_revision_root_handoff_research_session_shell",
    "create_inspectable_third_changed_basis_revision_root_research_session_shell",
    "create_third_changed_basis_revision_root_handoff_research_session_shell",
    "create_third_changed_basis_revision_root_research_session_shell",
]
