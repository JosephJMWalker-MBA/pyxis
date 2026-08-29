from __future__ import annotations

from pathlib import Path

from textual.widgets import Button, Input, Static

from pyxis.app.chromium_research_second_changed_basis_epoch_reentry_overlay import (
    ChromiumResearchSecondChangedBasisEpochReentryOverlayResult,
    persist_chromium_research_second_changed_basis_epoch_reentry_overlay,
)

from .chromium_research_second_changed_basis_epoch_reentry_overlay_textual import (
    ResearchSecondChangedBasisEpochReentryOverlayControls,
)
from .second_changed_basis_epoch_reentry_research_session_shell import (
    SecondChangedBasisEpochReentryResearchSessionShell,
)


class SecondChangedBasisEpochReentryOverlayResearchSessionShell(
    SecondChangedBasisEpochReentryResearchSessionShell
):
    """Concrete 46A→46F surface through explicit public-37B persistence.

    The 46F overlay belongs to the exact historical 46E verification that mounted its
    form. It does not become active restart authority and does not replace whatever
    governed controller the shell has mounted when persistence occurs.
    """

    CSS = SecondChangedBasisEpochReentryResearchSessionShell.CSS + """
    #research-second-changed-basis-epoch-reentry-overlay-controls {
        width: 94%;
        height: auto;
        padding: 1 2;
        margin-top: 1;
        border: round $warning;
    }

    #research-second-changed-basis-epoch-reentry-overlay-authority-notice,
    #research-second-changed-basis-epoch-reentry-overlay-summary,
    #research-second-changed-basis-epoch-reentry-overlay-status {
        margin-top: 1;
    }

    #research-second-changed-basis-epoch-reentry-overlay-title {
        text-style: bold;
    }

    #persist-research-second-changed-basis-epoch-reentry-overlay {
        margin-top: 1;
    }
    """

    def __init__(self, reentry) -> None:
        super().__init__(reentry)
        self.last_second_changed_basis_epoch_reentry_overlay: (
            ChromiumResearchSecondChangedBasisEpochReentryOverlayResult | None
        ) = None

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "persist-research-second-changed-basis-epoch-reentry-overlay":
            event.stop()
            self.call_after_refresh(self._persist_second_changed_basis_epoch_reentry_overlay)
            return
        # Textual dispatches inherited handlers through the MRO. Do not manually call
        # the parent handler or inherited actions will be scheduled twice.

    async def _verify_second_changed_basis_epoch_reentry(self) -> None:
        """Run inherited 46E, then mount 46F only after one new exact success."""

        prior = self.last_second_changed_basis_epoch_reentry_verification
        await super()._verify_second_changed_basis_epoch_reentry()
        verification = self.last_second_changed_basis_epoch_reentry_verification
        if verification is None or verification is prior:
            return
        if len(self.query("#research-second-changed-basis-epoch-reentry-overlay-controls")) != 0:
            raise ValueError("Second-basis re-entry overlay controls are already mounted.")
        await self.mount(
            ResearchSecondChangedBasisEpochReentryOverlayControls(verification)
        )

    async def _persist_second_changed_basis_epoch_reentry_overlay(self) -> None:
        controls = self.query_one(
            "#research-second-changed-basis-epoch-reentry-overlay-controls",
            ResearchSecondChangedBasisEpochReentryOverlayControls,
        )
        status = self.query_one(
            "#research-second-changed-basis-epoch-reentry-overlay-status",
            Static,
        )
        verification = self.last_second_changed_basis_epoch_reentry_verification
        if verification is None or controls.verification_result is not verification:
            status.update(
                "Overlay persistence failed: no exact successful 46E verification owns this form."
            )
            return

        prior_overlay = self.query_one(
            "#research-second-changed-basis-epoch-reentry-overlay-prior-continuation-overlay-source",
            Input,
        )
        destination = self.query_one(
            "#research-second-changed-basis-epoch-reentry-overlay-destination",
            Input,
        )
        if not prior_overlay.value.strip():
            status.update(
                "Overlay persistence failed: explicit current prior 35D/35E continuation-overlay path is required."
            )
            return
        if not destination.value.strip():
            status.update(
                "Overlay persistence failed: explicit no-overwrite 37B destination is required."
            )
            return

        mounted_controller = self.research_controller
        mounted_session = self.research_session
        mounted_reentry = self.research_reentry
        historical_continuation = self.root_backed_continuation_reentry
        try:
            result = persist_chromium_research_second_changed_basis_epoch_reentry_overlay(
                verification,
                prior_root_backed_continuation_overlay_source=Path(prior_overlay.value),
                destination=Path(destination.value),
            )
        except Exception as exc:
            status.update(f"Overlay persistence failed: {exc}")
            return

        if result.verification_result is not verification:
            raise ValueError("46F did not retain the exact successful 46E verification.")
        if (
            self.research_controller is not mounted_controller
            or self.research_session is not mounted_session
            or self.research_reentry is not mounted_reentry
            or self.root_backed_continuation_reentry is not historical_continuation
        ):
            raise ValueError(
                "Mounted governed state or retained first-root continuation changed during 46F persistence."
            )

        self.last_second_changed_basis_epoch_reentry_overlay = result
        controls.lock_after_success(result)


def create_second_changed_basis_epoch_reentry_overlay_research_session_shell(
    reentry,
) -> SecondChangedBasisEpochReentryOverlayResearchSessionShell:
    """Create the concrete second changed-basis product surface through 37B persistence."""

    return SecondChangedBasisEpochReentryOverlayResearchSessionShell(reentry)


__all__ = [
    "SecondChangedBasisEpochReentryOverlayResearchSessionShell",
    "create_second_changed_basis_epoch_reentry_overlay_research_session_shell",
]
