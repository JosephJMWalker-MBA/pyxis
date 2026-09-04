from __future__ import annotations

from textual.widgets import Button, Static

from pyxis.app.chromium_research_third_basis_epoch_continuation_reentry_plan_document import (
    ChromiumResearchThirdBasisEpochContinuationReentryResult,
)
from pyxis.app.chromium_research_third_basis_epoch_reentry import (
    ChromiumResearchThirdBasisEpochReentryResult,
)
from pyxis.app.chromium_research_third_basis_epoch_shell_lineage import (
    ChromiumResearchThirdBasisEpochShellLineage,
)

from .research_session_shell import ResearchSessionShell
from .third_basis_epoch_research_session_shell import (
    ThirdBasisEpochContinuationResearchSessionShell,
    ThirdBasisEpochResearchSessionShell,
)


class ThirdBasisEpochCumulativeHandoffResearchSessionShell(
    ThirdBasisEpochResearchSessionShell
):
    """41C first-checkpoint shell with one explicit 41E cumulative-mode handoff.

    A successful 40C checkpoint still leaves revision locked. Checkpoint success alone
    does not change modes. Only the explicit handoff button exits this Textual app with
    the exact fresh typed continuation earned by that checkpoint.

    The saved overlay path is never returned, promoted, or reused as current authority.
    Closing the shell normally remains a valid alternative to the in-process handoff.
    """

    CSS = ThirdBasisEpochResearchSessionShell.CSS + """
    #research-third-basis-epoch-cumulative-handoff-notice {
        width: 94%;
        height: auto;
        padding: 1 2;
        margin-top: 1;
        border: round $secondary;
    }

    #continue-third-basis-epoch-cumulative-mode {
        margin-top: 1;
    }
    """

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "continue-third-basis-epoch-cumulative-mode":
            event.stop()
            checkpoint = self.last_third_basis_epoch_continuation_checkpoint
            if checkpoint is None:
                raise ValueError(
                    "Cumulative handoff requires one successful retained 40C checkpoint."
                )
            self.exit(checkpoint.fresh_reentry)
            return
        super().on_button_pressed(event)

    async def _save_third_basis_epoch_continuation_checkpoint(self) -> None:
        """Run the established 41C save, then expose only an earned explicit handoff."""

        prior_checkpoint = self.last_third_basis_epoch_continuation_checkpoint
        await super()._save_third_basis_epoch_continuation_checkpoint()
        checkpoint = self.last_third_basis_epoch_continuation_checkpoint
        if checkpoint is None or checkpoint is prior_checkpoint:
            return
        if len(self.query("#continue-third-basis-epoch-cumulative-mode")):
            return

        await self.mount(
            Static(
                "Checkpoint complete. Further revision remains locked. Choose the explicit "
                "handoff below to continue immediately in cumulative mode with the exact "
                "freshly proven in-memory continuation, or close this shell and relaunch "
                "the saved continuation overlay later. No saved path is promoted to "
                "continuing authority.",
                id="research-third-basis-epoch-cumulative-handoff-notice",
                markup=False,
            )
        )
        await self.mount(
            Button(
                "Continue in cumulative mode",
                id="continue-third-basis-epoch-cumulative-mode",
                variant="primary",
            )
        )
        # Deliberately do not unlock revision or auto-exit after checkpoint success.


class ThirdBasisEpochHandoffResearchSessionShell(
    ThirdBasisEpochCumulativeHandoffResearchSessionShell
):
    """Established first-checkpoint behavior from one exact pathless 47G handoff.

    The supplied third-epoch re-entry was freshly earned by public 40B during 47F in
    the same process. This receiver deliberately bypasses persisted 41A launch-lineage
    construction: no 40B path is loaded, stored, inferred, or promoted as launch
    provenance. Existing 40C and 41E behavior is inherited unchanged.
    """

    def __init__(self, reentry: ChromiumResearchThirdBasisEpochReentryResult) -> None:
        if type(reentry) is not ChromiumResearchThirdBasisEpochReentryResult:
            raise TypeError(
                "reentry must be exactly ChromiumResearchThirdBasisEpochReentryResult."
            )

        ResearchSessionShell.__init__(self, reentry.controller)
        self.third_basis_epoch_launch_lineage = None
        self.third_basis_epoch_handoff_reentry = reentry
        self.third_basis_epoch_reentry = reentry
        self.last_third_basis_epoch_continuation_checkpoint = None


class ThirdBasisEpochContinuationHandoffResearchSessionShell(
    ThirdBasisEpochContinuationResearchSessionShell
):
    """41D cumulative behavior initialized from one exact in-process typed handoff.

    This constructor intentionally does not fabricate a 41A launch-lineage wrapper.
    The supplied re-entry was already freshly earned by the successful 40C checkpoint
    in the same process. No overlay path is loaded, stored, inferred, or promoted.
    """

    def __init__(
        self,
        reentry: ChromiumResearchThirdBasisEpochContinuationReentryResult,
    ) -> None:
        if not isinstance(
            reentry,
            ChromiumResearchThirdBasisEpochContinuationReentryResult,
        ):
            raise TypeError(
                "reentry must be ChromiumResearchThirdBasisEpochContinuationReentryResult."
            )

        # Bypass the persisted-launch constructor deliberately: that constructor
        # requires a 41A path/re-entry proof wrapper, which is the wrong authority
        # family for an exact in-process typed handoff.
        ResearchSessionShell.__init__(self, reentry.controller)
        self.third_basis_epoch_continuation_launch_lineage = None
        self.third_basis_epoch_continuation_handoff_reentry = reentry
        self.third_basis_epoch_continuation_reentry = reentry
        self.last_third_basis_epoch_cumulative_checkpoint = None


def create_third_basis_epoch_cumulative_handoff_research_session_shell(
    lineage: ChromiumResearchThirdBasisEpochShellLineage,
) -> ThirdBasisEpochCumulativeHandoffResearchSessionShell:
    """Create the explicit-handoff extension of the proven 40B first-checkpoint shell."""

    if not isinstance(lineage, ChromiumResearchThirdBasisEpochShellLineage):
        raise TypeError(
            "lineage must be ChromiumResearchThirdBasisEpochShellLineage."
        )
    return ThirdBasisEpochCumulativeHandoffResearchSessionShell(lineage)


def create_third_basis_epoch_handoff_research_session_shell(
    reentry: ChromiumResearchThirdBasisEpochReentryResult,
) -> ThirdBasisEpochHandoffResearchSessionShell:
    """Create first-checkpoint mode directly from one exact 47G typed handoff."""

    return ThirdBasisEpochHandoffResearchSessionShell(reentry)


def create_third_basis_epoch_continuation_handoff_research_session_shell(
    reentry: ChromiumResearchThirdBasisEpochContinuationReentryResult,
) -> ThirdBasisEpochContinuationHandoffResearchSessionShell:
    """Create cumulative mode directly from an exact freshly proven in-process re-entry."""

    return ThirdBasisEpochContinuationHandoffResearchSessionShell(reentry)


__all__ = [
    "ThirdBasisEpochContinuationHandoffResearchSessionShell",
    "ThirdBasisEpochCumulativeHandoffResearchSessionShell",
    "ThirdBasisEpochHandoffResearchSessionShell",
    "create_third_basis_epoch_continuation_handoff_research_session_shell",
    "create_third_basis_epoch_cumulative_handoff_research_session_shell",
    "create_third_basis_epoch_handoff_research_session_shell",
]
