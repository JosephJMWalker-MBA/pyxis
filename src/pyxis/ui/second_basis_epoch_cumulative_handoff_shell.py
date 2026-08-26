from __future__ import annotations

from textual.widgets import Button, Static

from pyxis.app.chromium_research_second_basis_epoch_continuation_reentry_plan_document import (
    ChromiumResearchSecondBasisEpochContinuationReentryResult,
)
from pyxis.app.chromium_research_second_basis_epoch_shell_lineage import (
    ChromiumResearchSecondBasisEpochShellLineage,
)

from .research_session_shell import ResearchSessionShell
from .second_basis_epoch_research_session_shell import (
    SecondBasisEpochContinuationResearchSessionShell,
    SecondBasisEpochResearchSessionShell,
)


class SecondBasisEpochCumulativeHandoffResearchSessionShell(
    SecondBasisEpochResearchSessionShell
):
    """38D first-checkpoint shell with one explicit 38F cumulative-mode handoff.

    A successful 37C checkpoint still leaves revision locked. Checkpoint success alone
    does not change modes. Only the explicit handoff button exits this Textual app with
    the exact fresh typed continuation earned by that checkpoint.

    The saved overlay path is never returned, promoted, or reused as current authority.
    Closing the shell normally remains a valid alternative to the in-process handoff.
    """

    CSS = SecondBasisEpochResearchSessionShell.CSS + """
    #research-second-basis-epoch-cumulative-handoff-notice {
        width: 94%;
        height: auto;
        padding: 1 2;
        margin-top: 1;
        border: round $secondary;
    }

    #continue-second-basis-epoch-cumulative-mode {
        margin-top: 1;
    }
    """

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "continue-second-basis-epoch-cumulative-mode":
            event.stop()
            checkpoint = self.last_second_basis_epoch_continuation_checkpoint
            if checkpoint is None:
                raise ValueError(
                    "Cumulative handoff requires one successful retained 37C checkpoint."
                )
            self.exit(checkpoint.fresh_reentry)
            return
        super().on_button_pressed(event)

    async def _save_second_basis_epoch_continuation_checkpoint(self) -> None:
        """Run the established 38D save, then expose only an earned explicit handoff."""

        prior_checkpoint = self.last_second_basis_epoch_continuation_checkpoint
        await super()._save_second_basis_epoch_continuation_checkpoint()
        checkpoint = self.last_second_basis_epoch_continuation_checkpoint
        if checkpoint is None or checkpoint is prior_checkpoint:
            return
        if len(self.query("#continue-second-basis-epoch-cumulative-mode")):
            return

        await self.mount(
            Static(
                "Checkpoint complete. Further revision remains locked. Choose the explicit "
                "handoff below to continue immediately in cumulative mode with the exact "
                "freshly proven in-memory continuation, or close this shell and relaunch "
                "the saved continuation overlay later. No saved path is promoted to "
                "continuing authority.",
                id="research-second-basis-epoch-cumulative-handoff-notice",
                markup=False,
            )
        )
        await self.mount(
            Button(
                "Continue in cumulative mode",
                id="continue-second-basis-epoch-cumulative-mode",
                variant="primary",
            )
        )
        # Deliberately do not unlock revision or auto-exit after checkpoint success.


class SecondBasisEpochContinuationHandoffResearchSessionShell(
    SecondBasisEpochContinuationResearchSessionShell
):
    """38E cumulative behavior initialized from one exact in-process typed handoff.

    This constructor intentionally does not fabricate a 38B launch-lineage wrapper.
    The supplied re-entry was already freshly earned by the successful 37C checkpoint
    in the same process. No overlay path is loaded, stored, inferred, or promoted.
    """

    def __init__(
        self,
        reentry: ChromiumResearchSecondBasisEpochContinuationReentryResult,
    ) -> None:
        if not isinstance(
            reentry,
            ChromiumResearchSecondBasisEpochContinuationReentryResult,
        ):
            raise TypeError(
                "reentry must be ChromiumResearchSecondBasisEpochContinuationReentryResult."
            )

        # Bypass the persisted-launch constructor deliberately: that constructor
        # requires a 38B path/re-entry proof wrapper, which is the wrong authority
        # family for an exact in-process typed handoff.
        ResearchSessionShell.__init__(self, reentry.controller)
        self.second_basis_epoch_continuation_launch_lineage = None
        self.second_basis_epoch_continuation_handoff_reentry = reentry
        self.second_basis_epoch_continuation_reentry = reentry
        self.last_second_basis_epoch_cumulative_checkpoint = None


def create_second_basis_epoch_cumulative_handoff_research_session_shell(
    lineage: ChromiumResearchSecondBasisEpochShellLineage,
) -> SecondBasisEpochCumulativeHandoffResearchSessionShell:
    """Create the explicit-handoff extension of the proven 37B first-checkpoint shell."""

    if not isinstance(lineage, ChromiumResearchSecondBasisEpochShellLineage):
        raise TypeError(
            "lineage must be ChromiumResearchSecondBasisEpochShellLineage."
        )
    return SecondBasisEpochCumulativeHandoffResearchSessionShell(lineage)


def create_second_basis_epoch_continuation_handoff_research_session_shell(
    reentry: ChromiumResearchSecondBasisEpochContinuationReentryResult,
) -> SecondBasisEpochContinuationHandoffResearchSessionShell:
    """Create cumulative mode directly from an exact freshly proven in-process re-entry."""

    return SecondBasisEpochContinuationHandoffResearchSessionShell(reentry)


__all__ = [
    "SecondBasisEpochContinuationHandoffResearchSessionShell",
    "SecondBasisEpochCumulativeHandoffResearchSessionShell",
    "create_second_basis_epoch_continuation_handoff_research_session_shell",
    "create_second_basis_epoch_cumulative_handoff_research_session_shell",
]
