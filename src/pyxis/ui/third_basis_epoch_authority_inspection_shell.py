from __future__ import annotations

from textual.app import ComposeResult

from pyxis.app.chromium_research_session_rollover import ChromiumResearchSessionRolloverResult
from pyxis.app.chromium_research_third_basis_epoch_continuation_checkpoint_extension import (
    ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionResult,
)
from pyxis.app.chromium_research_third_basis_epoch_continuation_reentry_plan_document import (
    ChromiumResearchThirdBasisEpochContinuationReentryResult,
)
from pyxis.app.chromium_research_third_basis_epoch_shell_lineage import (
    ChromiumResearchThirdBasisEpochContinuationShellLineage,
    ChromiumResearchThirdBasisEpochShellLineage,
)

from .chromium_research_third_basis_epoch_authority_inspection_textual import (
    ThirdBasisEpochAuthorityInspectionPanel,
)
from .third_basis_epoch_cumulative_handoff_shell import (
    ThirdBasisEpochContinuationHandoffResearchSessionShell,
    ThirdBasisEpochCumulativeHandoffResearchSessionShell,
)
from .third_basis_epoch_research_session_shell import (
    ThirdBasisEpochContinuationResearchSessionShell,
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


class InspectableThirdBasisEpochCumulativeHandoffResearchSessionShell(
    ThirdBasisEpochCumulativeHandoffResearchSessionShell
):
    """Current 40B/41E first-checkpoint shell with read-only three-root inspection."""

    CSS = ThirdBasisEpochCumulativeHandoffResearchSessionShell.CSS + _INSPECTION_CSS

    def __init__(self, lineage: ChromiumResearchThirdBasisEpochShellLineage) -> None:
        super().__init__(lineage)
        self.third_basis_epoch_authority_inspection = (
            ThirdBasisEpochAuthorityInspectionPanel.from_third_basis_epoch_launch(lineage)
        )

    def compose(self) -> ComposeResult:
        yield self.third_basis_epoch_authority_inspection
        yield from super().compose()

    async def _mount_research_rollover(
        self,
        result: ChromiumResearchSessionRolloverResult,
    ) -> None:
        await super()._mount_research_rollover(result)
        self.third_basis_epoch_authority_inspection.update_current_from_controller(
            self.research_controller,
            state_kind="visible one-hop continuation",
            state_source="explicit rollover from persisted 40B launch",
        )


class InspectableThirdBasisEpochContinuationResearchSessionShell(
    ThirdBasisEpochContinuationResearchSessionShell
):
    """Current path-proofed 40C/40D shell with immutable launch/current inspection."""

    CSS = ThirdBasisEpochContinuationResearchSessionShell.CSS + _INSPECTION_CSS

    def __init__(
        self,
        lineage: ChromiumResearchThirdBasisEpochContinuationShellLineage,
    ) -> None:
        super().__init__(lineage)
        self.third_basis_epoch_authority_inspection = (
            ThirdBasisEpochAuthorityInspectionPanel.from_continuation_launch(lineage)
        )

    def compose(self) -> ComposeResult:
        yield self.third_basis_epoch_authority_inspection
        yield from super().compose()

    async def _promote_third_basis_epoch_cumulative_checkpoint(
        self,
        result: ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionResult,
    ) -> None:
        launch_provenance = self.third_basis_epoch_authority_inspection.launch_provenance
        await super()._promote_third_basis_epoch_cumulative_checkpoint(result)
        if self.third_basis_epoch_authority_inspection.launch_provenance is not launch_provenance:
            raise ValueError(
                "Cumulative promotion must not replace immutable third-epoch launch provenance."
            )
        self.third_basis_epoch_authority_inspection.update_current_from_continuation(
            self.third_basis_epoch_continuation_reentry,
            state_source="40D cumulative promotion",
        )


class InspectableThirdBasisEpochContinuationHandoffResearchSessionShell(
    ThirdBasisEpochContinuationHandoffResearchSessionShell
):
    """Current raw 41E handoff shell with no persistent launch path in inspection."""

    CSS = ThirdBasisEpochContinuationHandoffResearchSessionShell.CSS + _INSPECTION_CSS

    def __init__(
        self,
        reentry: ChromiumResearchThirdBasisEpochContinuationReentryResult,
    ) -> None:
        super().__init__(reentry)
        self.third_basis_epoch_authority_inspection = (
            ThirdBasisEpochAuthorityInspectionPanel.from_in_process_handoff(reentry)
        )

    def compose(self) -> ComposeResult:
        yield self.third_basis_epoch_authority_inspection
        yield from super().compose()

    async def _promote_third_basis_epoch_cumulative_checkpoint(
        self,
        result: ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionResult,
    ) -> None:
        launch_provenance = self.third_basis_epoch_authority_inspection.launch_provenance
        await super()._promote_third_basis_epoch_cumulative_checkpoint(result)
        if self.third_basis_epoch_authority_inspection.launch_provenance is not launch_provenance:
            raise ValueError(
                "Cumulative promotion must not replace immutable third-epoch handoff provenance."
            )
        self.third_basis_epoch_authority_inspection.update_current_from_continuation(
            self.third_basis_epoch_continuation_reentry,
            state_source="40D cumulative promotion after in-process 41E handoff",
        )


def create_inspectable_third_basis_epoch_cumulative_handoff_research_session_shell(
    lineage: ChromiumResearchThirdBasisEpochShellLineage,
) -> InspectableThirdBasisEpochCumulativeHandoffResearchSessionShell:
    if not isinstance(lineage, ChromiumResearchThirdBasisEpochShellLineage):
        raise TypeError(
            "lineage must be ChromiumResearchThirdBasisEpochShellLineage."
        )
    return InspectableThirdBasisEpochCumulativeHandoffResearchSessionShell(lineage)


def create_inspectable_third_basis_epoch_continuation_research_session_shell(
    lineage: ChromiumResearchThirdBasisEpochContinuationShellLineage,
) -> InspectableThirdBasisEpochContinuationResearchSessionShell:
    if not isinstance(
        lineage,
        ChromiumResearchThirdBasisEpochContinuationShellLineage,
    ):
        raise TypeError(
            "lineage must be ChromiumResearchThirdBasisEpochContinuationShellLineage."
        )
    return InspectableThirdBasisEpochContinuationResearchSessionShell(lineage)


def create_inspectable_third_basis_epoch_continuation_handoff_research_session_shell(
    reentry: ChromiumResearchThirdBasisEpochContinuationReentryResult,
) -> InspectableThirdBasisEpochContinuationHandoffResearchSessionShell:
    if not isinstance(
        reentry,
        ChromiumResearchThirdBasisEpochContinuationReentryResult,
    ):
        raise TypeError(
            "reentry must be ChromiumResearchThirdBasisEpochContinuationReentryResult."
        )
    return InspectableThirdBasisEpochContinuationHandoffResearchSessionShell(reentry)


__all__ = [
    "InspectableThirdBasisEpochContinuationHandoffResearchSessionShell",
    "InspectableThirdBasisEpochContinuationResearchSessionShell",
    "InspectableThirdBasisEpochCumulativeHandoffResearchSessionShell",
    "create_inspectable_third_basis_epoch_continuation_handoff_research_session_shell",
    "create_inspectable_third_basis_epoch_continuation_research_session_shell",
    "create_inspectable_third_basis_epoch_cumulative_handoff_research_session_shell",
]
