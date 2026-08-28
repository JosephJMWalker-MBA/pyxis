from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from textual.widgets import Button, Input, Static

from pyxis.app.chromium_research_first_changed_basis_transition import (
    ChromiumResearchFirstChangedBasisTransitionResult,
    persist_chromium_research_first_changed_basis_transition,
)
from pyxis.app.chromium_research_session_reentry import ChromiumResearchSessionReentryResult
from pyxis.app.chromium_research_session_rollover import ChromiumResearchSessionRolloverResult
from pyxis.app.chromium_research_working_set import ChromiumPageResearchWorkingSetItem

from .chromium_research_first_changed_basis_transition_textual import (
    ResearchFirstChangedBasisTransitionControls,
)
from .research_session_shell import ResearchSessionShell


class FirstChangedBasisResearchSessionShell(ResearchSessionShell):
    """Concrete ordinary-pre-root shell for 44A preparation then one 44B transition.

    The constructor requires the exact ordinary 31A re-entry family and mounts the
    inherited 44A preparation surface for exact caller-supplied candidate evidence.
    Only after that preparation succeeds does this shell mount one first changed-basis
    33B transition form.

    Root-backed and later epoch shells do not subclass this product surface, so they
    cannot inherit a generic transition-again action by implementation symmetry.
    """

    CSS = ResearchSessionShell.CSS + """
    #research-first-changed-basis-transition-controls {
        width: 94%;
        height: auto;
        padding: 1 2;
        margin-top: 1;
        border: round $warning;
    }

    #research-first-changed-basis-transition-authority-notice,
    #research-first-changed-basis-transition-prepared-summary,
    #research-first-changed-basis-transition-prior-edge-source-label,
    #research-first-changed-basis-transition-working-set-source-label,
    #research-first-changed-basis-transition-note-source-label,
    #research-first-changed-basis-transition-destination-label,
    #research-first-changed-basis-transition-status {
        margin-top: 1;
    }

    #research-first-changed-basis-transition-title,
    #research-first-changed-basis-transition-prior-edge-source-label,
    #research-first-changed-basis-transition-working-set-source-label,
    #research-first-changed-basis-transition-note-source-label,
    #research-first-changed-basis-transition-destination-label {
        text-style: bold;
    }

    #persist-research-first-changed-basis-transition {
        margin-top: 1;
    }
    """

    def __init__(
        self,
        ordinary_reentry: ChromiumResearchSessionReentryResult,
        appended_items: Iterable[ChromiumPageResearchWorkingSetItem],
    ) -> None:
        if type(ordinary_reentry) is not ChromiumResearchSessionReentryResult:
            raise TypeError(
                "ordinary_reentry must be exactly ChromiumResearchSessionReentryResult."
            )
        super().__init__(ordinary_reentry.controller, reentry=ordinary_reentry)
        self.initial_ordinary_reentry = ordinary_reentry
        self.last_first_changed_basis_transition: (
            ChromiumResearchFirstChangedBasisTransitionResult | None
        ) = None
        self.configure_changed_basis_candidate(appended_items)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "persist-research-first-changed-basis-transition":
            event.stop()
            self.call_after_refresh(
                self._persist_research_first_changed_basis_transition
            )
            return
        super().on_button_pressed(event)

    async def _persist_research_changed_basis_preparation(self) -> None:
        """Run inherited 44A, then mount 44B only after a new exact success."""

        prior = self.last_changed_basis_preparation
        await super()._persist_research_changed_basis_preparation()
        prepared = self.last_changed_basis_preparation
        if prepared is None or prepared is prior:
            return
        if self.research_controller is not self.initial_ordinary_reentry.controller:
            raise ValueError(
                "First changed-basis preparation no longer belongs to the initial ordinary controller."
            )
        if len(self.query("#research-first-changed-basis-transition-controls")) != 0:
            raise ValueError(
                "First changed-basis transition controls are already mounted."
            )
        await self.mount(ResearchFirstChangedBasisTransitionControls(prepared))

    async def _persist_research_first_changed_basis_transition(self) -> None:
        controls = self.query_one(
            "#research-first-changed-basis-transition-controls",
            ResearchFirstChangedBasisTransitionControls,
        )
        status = self.query_one(
            "#research-first-changed-basis-transition-status", Static
        )
        if controls.stale:
            status.update(
                "Transition failed: this prepared basis is stale and will not be silently retargeted."
            )
            return

        prepared = self.last_changed_basis_preparation
        if prepared is None or controls.prepared is not prepared:
            status.update(
                "Transition failed: no exact successful 44A preparation owns this transition form."
            )
            return
        if (
            self.research_controller is not self.initial_ordinary_reentry.controller
            or self.research_controller.declared_endpoint is not prepared.prior_endpoint
        ):
            controls.mark_stale()
            return

        prior_edge_source = self.query_one(
            "#research-first-changed-basis-transition-prior-edge-source", Input
        )
        working_set_source = self.query_one(
            "#research-first-changed-basis-transition-working-set-source", Input
        )
        note_source = self.query_one(
            "#research-first-changed-basis-transition-note-source", Input
        )
        destination = self.query_one(
            "#research-first-changed-basis-transition-destination", Input
        )

        required = (
            (prior_edge_source, "explicit prior endpoint edge path"),
            (working_set_source, "explicit prepared working-set path"),
            (note_source, "explicit prepared working-set-note path"),
            (destination, "explicit transition destination path"),
        )
        for widget, label in required:
            if not widget.value.strip():
                status.update(f"Transition failed: {label} is required.")
                return

        controller = self.research_controller
        session = self.research_session
        try:
            result = persist_chromium_research_first_changed_basis_transition(
                controller,
                self.initial_ordinary_reentry,
                prepared,
                prior_edge_source=Path(prior_edge_source.value),
                working_set_source=Path(working_set_source.value),
                note_source=Path(note_source.value),
                destination=Path(destination.value),
            )
        except Exception as exc:
            status.update(f"Transition failed: {exc}")
            return

        if result.controller is not controller:
            raise ValueError(
                "First changed-basis transition did not retain the exact mounted controller."
            )
        if result.prepared is not prepared:
            raise ValueError(
                "First changed-basis transition did not retain the exact prepared basis."
            )
        if self.research_controller is not controller or self.research_session is not session:
            raise ValueError(
                "Mounted governed research session changed during first changed-basis transition persistence."
            )

        self.last_first_changed_basis_transition = result
        controls.lock_after_success(result)

    async def _mount_research_rollover(
        self,
        result: ChromiumResearchSessionRolloverResult,
    ) -> None:
        """Stale any unsaved 44B transition before inherited 30A session replacement."""

        if len(self.query("#research-first-changed-basis-transition-controls")) != 0:
            self.query_one(
                "#research-first-changed-basis-transition-controls",
                ResearchFirstChangedBasisTransitionControls,
            ).mark_stale()
        await super()._mount_research_rollover(result)


def create_first_changed_basis_research_session_shell(
    ordinary_reentry: ChromiumResearchSessionReentryResult,
    appended_items: Iterable[ChromiumPageResearchWorkingSetItem],
) -> FirstChangedBasisResearchSessionShell:
    """Create the concrete pre-root 44A→44B product surface."""

    return FirstChangedBasisResearchSessionShell(ordinary_reentry, appended_items)


__all__ = [
    "FirstChangedBasisResearchSessionShell",
    "create_first_changed_basis_research_session_shell",
]
