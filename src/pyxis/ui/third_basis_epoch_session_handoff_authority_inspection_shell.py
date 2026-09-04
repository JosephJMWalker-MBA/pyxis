from __future__ import annotations

from textual.app import ComposeResult

from pyxis.app.chromium_research_session_rollover import ChromiumResearchSessionRolloverResult
from pyxis.app.chromium_research_third_basis_epoch_reentry import (
    ChromiumResearchThirdBasisEpochReentryResult,
)
from pyxis.app.chromium_research_third_basis_epoch_session_handoff_inspection import (
    inspect_chromium_research_third_basis_epoch_session_in_process_handoff,
)

from .chromium_research_third_basis_epoch_authority_inspection_textual import (
    ThirdBasisEpochAuthorityInspectionPanel,
)
from .third_basis_epoch_cumulative_handoff_shell import (
    ThirdBasisEpochHandoffResearchSessionShell,
)


_INSPECTION_CSS = """
#research-third-basis-epoch-authority-inspection {
    width: 94%;
    height: auto;
    padding: 1 2;
    margin-top: 1;
    border: round $secondary;
}
"""


class InspectableThirdBasisEpochHandoffResearchSessionShell(
    ThirdBasisEpochHandoffResearchSessionShell
):
    """Exact 47G initial third-epoch handoff with pathless launch inspection."""

    CSS = ThirdBasisEpochHandoffResearchSessionShell.CSS + _INSPECTION_CSS

    def __init__(self, reentry: ChromiumResearchThirdBasisEpochReentryResult) -> None:
        super().__init__(reentry)
        inspection = (
            inspect_chromium_research_third_basis_epoch_session_in_process_handoff(
                reentry
            )
        )
        self.third_basis_epoch_authority_inspection = (
            ThirdBasisEpochAuthorityInspectionPanel(
                inspection.launch_provenance,
                inspection.current_state,
            )
        )

    def compose(self) -> ComposeResult:
        yield self.third_basis_epoch_authority_inspection
        yield from super().compose()

    async def _mount_research_rollover(
        self,
        result: ChromiumResearchSessionRolloverResult,
    ) -> None:
        launch = self.third_basis_epoch_authority_inspection.launch_provenance
        await super()._mount_research_rollover(result)
        if self.third_basis_epoch_authority_inspection.launch_provenance is not launch:
            raise ValueError(
                "Rollover must not replace immutable 47G third-epoch handoff provenance."
            )
        self.third_basis_epoch_authority_inspection.update_current_from_controller(
            self.research_controller,
            state_kind="visible one-hop continuation",
            state_source="explicit rollover after in-process 47G handoff",
        )
        if self.third_basis_epoch_authority_inspection.launch_provenance is not launch:
            raise ValueError(
                "Current-state projection must retain exact 47G handoff provenance."
            )


def create_inspectable_third_basis_epoch_handoff_research_session_shell(
    reentry: ChromiumResearchThirdBasisEpochReentryResult,
) -> InspectableThirdBasisEpochHandoffResearchSessionShell:
    if type(reentry) is not ChromiumResearchThirdBasisEpochReentryResult:
        raise TypeError(
            "reentry must be exactly ChromiumResearchThirdBasisEpochReentryResult."
        )
    return InspectableThirdBasisEpochHandoffResearchSessionShell(reentry)


__all__ = [
    "InspectableThirdBasisEpochHandoffResearchSessionShell",
    "create_inspectable_third_basis_epoch_handoff_research_session_shell",
]
