from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from textual.widgets import Button, Input, Static, TextArea

from pyxis.app.chromium_research_first_changed_basis_revision_root import (
    ChromiumResearchFirstChangedBasisRevisionRootResult,
    persist_chromium_research_first_changed_basis_revision_root,
)
from pyxis.app.chromium_research_session_reentry import ChromiumResearchSessionReentryResult
from pyxis.app.chromium_research_working_set import ChromiumPageResearchWorkingSetItem

from .chromium_research_first_changed_basis_revision_root_textual import (
    ResearchFirstChangedBasisRevisionRootControls,
)
from .first_changed_basis_research_session_shell import (
    FirstChangedBasisResearchSessionShell,
)


class FirstChangedBasisRootResearchSessionShell(FirstChangedBasisResearchSessionShell):
    """Concrete 44A→44B→44C product surface for the first changed-basis root.

    This shell inherits the dedicated first-transition product rather than widening
    the base research shell. It mounts one 34A revision-root form only after the exact
    first 44B transition has succeeded.

    The root remains bound to that persisted transition even if the mounted old-basis
    session later continues. Such coexistence is not a current/latest/head claim.
    """

    CSS = FirstChangedBasisResearchSessionShell.CSS + """
    #research-first-changed-basis-revision-root-controls {
        width: 94%;
        height: auto;
        padding: 1 2;
        margin-top: 1;
        border: round $warning;
    }

    #research-first-changed-basis-revision-root-authority-notice,
    #research-first-changed-basis-revision-root-transition-summary,
    #research-first-changed-basis-revision-root-rationale-label,
    #research-first-changed-basis-revision-root-prior-edge-source-label,
    #research-first-changed-basis-revision-root-working-set-source-label,
    #research-first-changed-basis-revision-root-note-source-label,
    #research-first-changed-basis-revision-root-transition-source-label,
    #research-first-changed-basis-revision-root-destination-label,
    #research-first-changed-basis-revision-root-status {
        margin-top: 1;
    }

    #research-first-changed-basis-revision-root-title,
    #research-first-changed-basis-revision-root-rationale-label,
    #research-first-changed-basis-revision-root-prior-edge-source-label,
    #research-first-changed-basis-revision-root-working-set-source-label,
    #research-first-changed-basis-revision-root-note-source-label,
    #research-first-changed-basis-revision-root-transition-source-label,
    #research-first-changed-basis-revision-root-destination-label {
        text-style: bold;
    }

    #research-first-changed-basis-revision-root-rationale {
        width: 100%;
        height: 8;
        margin-top: 1;
    }

    #persist-research-first-changed-basis-revision-root {
        margin-top: 1;
    }
    """

    def __init__(
        self,
        ordinary_reentry: ChromiumResearchSessionReentryResult,
        appended_items: Iterable[ChromiumPageResearchWorkingSetItem],
    ) -> None:
        super().__init__(ordinary_reentry, appended_items)
        self.last_first_changed_basis_revision_root: (
            ChromiumResearchFirstChangedBasisRevisionRootResult | None
        ) = None

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "persist-research-first-changed-basis-revision-root":
            event.stop()
            self.call_after_refresh(
                self._persist_research_first_changed_basis_revision_root
            )
            return
        super().on_button_pressed(event)

    async def _persist_research_first_changed_basis_transition(self) -> None:
        """Run inherited 44B, then mount 44C only after one new exact success."""

        prior = self.last_first_changed_basis_transition
        await super()._persist_research_first_changed_basis_transition()
        transition_result = self.last_first_changed_basis_transition
        if transition_result is None or transition_result is prior:
            return
        if len(self.query("#research-first-changed-basis-revision-root-controls")) != 0:
            raise ValueError(
                "First changed-basis revision-root controls are already mounted."
            )
        await self.mount(
            ResearchFirstChangedBasisRevisionRootControls(transition_result)
        )

    async def _persist_research_first_changed_basis_revision_root(self) -> None:
        controls = self.query_one(
            "#research-first-changed-basis-revision-root-controls",
            ResearchFirstChangedBasisRevisionRootControls,
        )
        status = self.query_one(
            "#research-first-changed-basis-revision-root-status", Static
        )
        transition_result = self.last_first_changed_basis_transition
        if (
            transition_result is None
            or controls.transition_result is not transition_result
        ):
            status.update(
                "Root failed: no exact successful first changed-basis transition owns this form."
            )
            return

        rationale = self.query_one(
            "#research-first-changed-basis-revision-root-rationale", TextArea
        )
        if not rationale.text.strip():
            status.update("Root failed: a new human rationale is required.")
            return

        prior_edge_source = self.query_one(
            "#research-first-changed-basis-revision-root-prior-edge-source", Input
        )
        working_set_source = self.query_one(
            "#research-first-changed-basis-revision-root-working-set-source", Input
        )
        note_source = self.query_one(
            "#research-first-changed-basis-revision-root-note-source", Input
        )
        transition_source = self.query_one(
            "#research-first-changed-basis-revision-root-transition-source", Input
        )
        destination = self.query_one(
            "#research-first-changed-basis-revision-root-destination", Input
        )

        required = (
            (prior_edge_source, "explicit prior endpoint edge path"),
            (working_set_source, "explicit changed working-set path"),
            (note_source, "explicit changed working-set-note path"),
            (transition_source, "explicit first changed-basis transition path"),
            (destination, "explicit revision-root destination path"),
        )
        for widget, label in required:
            if not widget.value.strip():
                status.update(f"Root failed: {label} is required.")
                return

        mounted_controller = self.research_controller
        mounted_session = self.research_session
        try:
            result = persist_chromium_research_first_changed_basis_revision_root(
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
                "First changed-basis root did not retain the exact successful 44B transition."
            )
        if (
            self.research_controller is not mounted_controller
            or self.research_session is not mounted_session
        ):
            raise ValueError(
                "Mounted governed research session changed during first root persistence."
            )

        self.last_first_changed_basis_revision_root = result
        controls.lock_after_success(result)


def create_first_changed_basis_root_research_session_shell(
    ordinary_reentry: ChromiumResearchSessionReentryResult,
    appended_items: Iterable[ChromiumPageResearchWorkingSetItem],
) -> FirstChangedBasisRootResearchSessionShell:
    """Create the concrete 44A→44B→44C first-root product surface."""

    return FirstChangedBasisRootResearchSessionShell(ordinary_reentry, appended_items)


__all__ = [
    "FirstChangedBasisRootResearchSessionShell",
    "create_first_changed_basis_root_research_session_shell",
]
