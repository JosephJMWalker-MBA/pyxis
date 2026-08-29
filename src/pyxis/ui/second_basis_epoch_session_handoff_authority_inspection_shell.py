from __future__ import annotations

from textual.app import ComposeResult

from pyxis.app.chromium_research_second_basis_epoch_reentry import (
    ChromiumResearchSecondBasisEpochReentryResult,
)
from pyxis.app.chromium_research_second_basis_epoch_session_handoff_inspection import (
    inspect_chromium_research_second_basis_epoch_session_in_process_handoff,
)
from pyxis.app.chromium_research_session_rollover import ChromiumResearchSessionRolloverResult

from .chromium_research_second_basis_epoch_authority_inspection_textual import (
    SecondBasisEpochAuthorityInspectionPanel,
)
from .second_basis_epoch_cumulative_handoff_shell import (
    SecondBasisEpochHandoffResearchSessionShell,
)


_INSPECTION_CSS = """
#research-second-basis-epoch-authority-inspection {
    width: 94%;
    height: auto;
    padding: 1 2;
    margin-top: 1;
    border: round $secondary;
}
"""


class InspectableSecondBasisEpochHandoffResearchSessionShell(
    SecondBasisEpochHandoffResearchSessionShell
):
    """Exact 46G initial second-epoch handoff with pathless launch inspection."""

    CSS = SecondBasisEpochHandoffResearchSessionShell.CSS + _INSPECTION_CSS

    def __init__(self, reentry: ChromiumResearchSecondBasisEpochReentryResult) -> None:
        super().__init__(reentry)
        inspection = (
            inspect_chromium_research_second_basis_epoch_session_in_process_handoff(
                reentry
            )
        )
        self.second_basis_epoch_authority_inspection = (
            SecondBasisEpochAuthorityInspectionPanel(
                inspection.launch_provenance,
                inspection.current_state,
            )
        )

    def compose(self) -> ComposeResult:
        yield self.second_basis_epoch_authority_inspection
        yield from super().compose()

    async def _mount_research_rollover(
        self,
        result: ChromiumResearchSessionRolloverResult,
    ) -> None:
        launch = self.second_basis_epoch_authority_inspection.launch_provenance
        await super()._mount_research_rollover(result)
        if self.second_basis_epoch_authority_inspection.launch_provenance is not launch:
            raise ValueError(
                "Rollover must not replace immutable 46G second-epoch handoff provenance."
            )
        self.second_basis_epoch_authority_inspection.update_current_from_controller(
            self.research_controller,
            state_kind="visible one-hop continuation",
            state_source="explicit rollover after in-process 46G handoff",
        )
        if self.second_basis_epoch_authority_inspection.launch_provenance is not launch:
            raise ValueError(
                "Current-state projection must retain exact 46G handoff provenance."
            )


def create_inspectable_second_basis_epoch_handoff_research_session_shell(
    reentry: ChromiumResearchSecondBasisEpochReentryResult,
) -> InspectableSecondBasisEpochHandoffResearchSessionShell:
    if type(reentry) is not ChromiumResearchSecondBasisEpochReentryResult:
        raise TypeError(
            "reentry must be exactly ChromiumResearchSecondBasisEpochReentryResult."
        )
    return InspectableSecondBasisEpochHandoffResearchSessionShell(reentry)


__all__ = [
    "InspectableSecondBasisEpochHandoffResearchSessionShell",
    "create_inspectable_second_basis_epoch_handoff_research_session_shell",
]
