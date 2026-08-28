from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from textual.widgets import Button, Input, Static

from pyxis.app.chromium_research_first_changed_basis_root_backed_reentry_overlay import (
    ChromiumResearchFirstChangedBasisRootBackedReentryOverlayResult,
    persist_chromium_research_first_changed_basis_root_backed_reentry_overlay,
)
from pyxis.app.chromium_research_session_reentry import ChromiumResearchSessionReentryResult
from pyxis.app.chromium_research_working_set import ChromiumPageResearchWorkingSetItem

from .chromium_research_first_changed_basis_root_backed_reentry_overlay_textual import (
    ResearchFirstChangedBasisRootBackedReentryOverlayControls,
)
from .first_changed_basis_root_backed_reentry_research_session_shell import (
    FirstChangedBasisRootBackedReentryResearchSessionShell,
)


class FirstChangedBasisRootBackedReentryOverlayResearchSessionShell(
    FirstChangedBasisRootBackedReentryResearchSessionShell
):
    """Concrete 44A→44G surface through proof-gated 35C overlay persistence.

    44G persists the exact historical session proven by 44F. It intentionally does
    not promote the overlay into active restart authority or reinterpret it as the
    currently mounted governed session when that shell has already continued.
    """

    CSS = FirstChangedBasisRootBackedReentryResearchSessionShell.CSS + """
    #research-first-changed-basis-root-backed-reentry-overlay-controls {
        width: 94%;
        height: auto;
        padding: 1 2;
        margin-top: 1;
        border: round $warning;
    }

    #research-first-changed-basis-root-backed-reentry-overlay-authority-notice,
    #research-first-changed-basis-root-backed-reentry-overlay-summary,
    #research-first-changed-basis-root-backed-reentry-overlay-prior-plan-source,
    #research-first-changed-basis-root-backed-reentry-overlay-destination,
    #research-first-changed-basis-root-backed-reentry-overlay-status {
        margin-top: 1;
    }

    #research-first-changed-basis-root-backed-reentry-overlay-title {
        text-style: bold;
    }

    #persist-research-first-changed-basis-root-backed-reentry-overlay {
        margin-top: 1;
    }
    """

    def __init__(
        self,
        ordinary_reentry: ChromiumResearchSessionReentryResult,
        appended_items: Iterable[ChromiumPageResearchWorkingSetItem],
    ) -> None:
        super().__init__(ordinary_reentry, appended_items)
        self.last_first_changed_basis_root_backed_reentry_overlay: (
            ChromiumResearchFirstChangedBasisRootBackedReentryOverlayResult | None
        ) = None

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "persist-research-first-changed-basis-root-backed-reentry-overlay":
            event.stop()
            self.call_after_refresh(
                self._persist_research_first_changed_basis_root_backed_reentry_overlay
            )
            return
        # Textual dispatches inherited message handlers through the MRO. Calling the
        # parent handler manually here would schedule parent-owned actions twice.

    async def _verify_research_first_changed_basis_root_backed_reentry(self) -> None:
        """Run inherited 44F, then mount 44G only after one new exact proof."""

        prior = self.last_first_changed_basis_root_backed_reentry_verification
        await super()._verify_research_first_changed_basis_root_backed_reentry()
        verification = self.last_first_changed_basis_root_backed_reentry_verification
        if verification is None or verification is prior:
            return
        if len(
            self.query(
                "#research-first-changed-basis-root-backed-reentry-overlay-controls"
            )
        ) != 0:
            raise ValueError("44G overlay persistence controls are already mounted.")
        await self.mount(
            ResearchFirstChangedBasisRootBackedReentryOverlayControls(verification)
        )

    async def _persist_research_first_changed_basis_root_backed_reentry_overlay(
        self,
    ) -> None:
        controls = self.query_one(
            "#research-first-changed-basis-root-backed-reentry-overlay-controls",
            ResearchFirstChangedBasisRootBackedReentryOverlayControls,
        )
        status = self.query_one(
            "#research-first-changed-basis-root-backed-reentry-overlay-status",
            Static,
        )
        verification = self.last_first_changed_basis_root_backed_reentry_verification
        if verification is None or controls.verification_result is not verification:
            status.update(
                "Overlay persistence failed: no exact successful 44F verification owns this form."
            )
            return

        prior_plan_source = self.query_one(
            "#research-first-changed-basis-root-backed-reentry-overlay-prior-plan-source",
            Input,
        )
        destination = self.query_one(
            "#research-first-changed-basis-root-backed-reentry-overlay-destination",
            Input,
        )
        if not prior_plan_source.value.strip():
            status.update(
                "Overlay persistence failed: explicit ordinary 31B plan-document path is required."
            )
            return
        if not destination.value.strip():
            status.update(
                "Overlay persistence failed: explicit no-overwrite 35C overlay destination is required."
            )
            return

        mounted_controller = self.research_controller
        mounted_session = self.research_session
        mounted_reentry = self.research_reentry
        try:
            result = persist_chromium_research_first_changed_basis_root_backed_reentry_overlay(
                verification,
                prior_session_plan_source=Path(prior_plan_source.value),
                destination=Path(destination.value),
            )
        except Exception as exc:
            status.update(f"Overlay persistence failed: {exc}")
            return

        if result.verification_result is not verification:
            raise ValueError("44G persistence did not retain the exact 44F proof.")
        if (
            self.research_controller is not mounted_controller
            or self.research_session is not mounted_session
            or self.research_reentry is not mounted_reentry
        ):
            raise ValueError(
                "Mounted governed research state changed during 44G overlay persistence."
            )

        self.last_first_changed_basis_root_backed_reentry_overlay = result
        controls.lock_after_success(result)


def create_first_changed_basis_root_backed_reentry_overlay_research_session_shell(
    ordinary_reentry: ChromiumResearchSessionReentryResult,
    appended_items: Iterable[ChromiumPageResearchWorkingSetItem],
) -> FirstChangedBasisRootBackedReentryOverlayResearchSessionShell:
    """Create the concrete first-changed-basis product surface through 35C persistence."""

    return FirstChangedBasisRootBackedReentryOverlayResearchSessionShell(
        ordinary_reentry,
        appended_items,
    )


__all__ = [
    "FirstChangedBasisRootBackedReentryOverlayResearchSessionShell",
    "create_first_changed_basis_root_backed_reentry_overlay_research_session_shell",
]
