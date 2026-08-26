from __future__ import annotations

from textual.app import ComposeResult

from pyxis.app.chromium_research_second_basis_epoch_continuation_checkpoint_extension import (
    ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionResult,
)
from pyxis.app.chromium_research_second_basis_epoch_continuation_reentry_plan_document import (
    ChromiumResearchSecondBasisEpochContinuationReentryResult,
)
from pyxis.app.chromium_research_second_basis_epoch_shell_lineage import (
    ChromiumResearchSecondBasisEpochContinuationShellLineage,
    ChromiumResearchSecondBasisEpochShellLineage,
)
from pyxis.app.chromium_research_session_rollover import ChromiumResearchSessionRolloverResult

from .chromium_research_second_basis_epoch_authority_inspection_textual import (
    SecondBasisEpochAuthorityInspectionPanel,
)
from .second_basis_epoch_cumulative_handoff_shell import (
    SecondBasisEpochContinuationHandoffResearchSessionShell,
    SecondBasisEpochCumulativeHandoffResearchSessionShell,
)
from .second_basis_epoch_research_session_shell import (
    SecondBasisEpochContinuationResearchSessionShell,
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


class InspectableSecondBasisEpochCumulativeHandoffResearchSessionShell(
    SecondBasisEpochCumulativeHandoffResearchSessionShell
):
    """Current 37B/38F first-checkpoint product shell with read-only authority inspection."""

    CSS = SecondBasisEpochCumulativeHandoffResearchSessionShell.CSS + _INSPECTION_CSS

    def __init__(self, lineage: ChromiumResearchSecondBasisEpochShellLineage) -> None:
        super().__init__(lineage)
        self.second_basis_epoch_authority_inspection = (
            SecondBasisEpochAuthorityInspectionPanel.from_second_basis_epoch_launch(
                lineage
            )
        )

    def compose(self) -> ComposeResult:
        yield self.second_basis_epoch_authority_inspection
        yield from super().compose()

    async def _mount_research_rollover(
        self,
        result: ChromiumResearchSessionRolloverResult,
    ) -> None:
        await super()._mount_research_rollover(result)
        self.second_basis_epoch_authority_inspection.update_current_from_controller(
            self.research_controller,
            state_kind="visible one-hop continuation",
            state_source="explicit rollover from persisted 37B launch",
        )


class InspectableSecondBasisEpochContinuationResearchSessionShell(
    SecondBasisEpochContinuationResearchSessionShell
):
    """Current path-proofed 37C/37D shell with immutable launch/current inspection."""

    CSS = SecondBasisEpochContinuationResearchSessionShell.CSS + _INSPECTION_CSS

    def __init__(
        self,
        lineage: ChromiumResearchSecondBasisEpochContinuationShellLineage,
    ) -> None:
        super().__init__(lineage)
        self.second_basis_epoch_authority_inspection = (
            SecondBasisEpochAuthorityInspectionPanel.from_continuation_launch(lineage)
        )

    def compose(self) -> ComposeResult:
        yield self.second_basis_epoch_authority_inspection
        yield from super().compose()

    async def _promote_second_basis_epoch_cumulative_checkpoint(
        self,
        result: ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionResult,
    ) -> None:
        launch_provenance = (
            self.second_basis_epoch_authority_inspection.launch_provenance
        )
        await super()._promote_second_basis_epoch_cumulative_checkpoint(result)
        if self.second_basis_epoch_authority_inspection.launch_provenance is not launch_provenance:
            raise ValueError(
                "Cumulative promotion must not replace immutable second-epoch launch provenance."
            )
        self.second_basis_epoch_authority_inspection.update_current_from_continuation(
            self.second_basis_epoch_continuation_reentry,
            state_source="37D cumulative promotion",
        )


class InspectableSecondBasisEpochContinuationHandoffResearchSessionShell(
    SecondBasisEpochContinuationHandoffResearchSessionShell
):
    """Current raw 38F handoff shell with no persistent launch path in inspection."""

    CSS = SecondBasisEpochContinuationHandoffResearchSessionShell.CSS + _INSPECTION_CSS

    def __init__(
        self,
        reentry: ChromiumResearchSecondBasisEpochContinuationReentryResult,
    ) -> None:
        super().__init__(reentry)
        self.second_basis_epoch_authority_inspection = (
            SecondBasisEpochAuthorityInspectionPanel.from_in_process_handoff(reentry)
        )

    def compose(self) -> ComposeResult:
        yield self.second_basis_epoch_authority_inspection
        yield from super().compose()

    async def _promote_second_basis_epoch_cumulative_checkpoint(
        self,
        result: ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionResult,
    ) -> None:
        launch_provenance = (
            self.second_basis_epoch_authority_inspection.launch_provenance
        )
        await super()._promote_second_basis_epoch_cumulative_checkpoint(result)
        if self.second_basis_epoch_authority_inspection.launch_provenance is not launch_provenance:
            raise ValueError(
                "Cumulative promotion must not replace immutable second-epoch handoff provenance."
            )
        self.second_basis_epoch_authority_inspection.update_current_from_continuation(
            self.second_basis_epoch_continuation_reentry,
            state_source="37D cumulative promotion after in-process handoff",
        )


def create_inspectable_second_basis_epoch_cumulative_handoff_research_session_shell(
    lineage: ChromiumResearchSecondBasisEpochShellLineage,
) -> InspectableSecondBasisEpochCumulativeHandoffResearchSessionShell:
    if not isinstance(lineage, ChromiumResearchSecondBasisEpochShellLineage):
        raise TypeError(
            "lineage must be ChromiumResearchSecondBasisEpochShellLineage."
        )
    return InspectableSecondBasisEpochCumulativeHandoffResearchSessionShell(lineage)


def create_inspectable_second_basis_epoch_continuation_research_session_shell(
    lineage: ChromiumResearchSecondBasisEpochContinuationShellLineage,
) -> InspectableSecondBasisEpochContinuationResearchSessionShell:
    if not isinstance(
        lineage,
        ChromiumResearchSecondBasisEpochContinuationShellLineage,
    ):
        raise TypeError(
            "lineage must be ChromiumResearchSecondBasisEpochContinuationShellLineage."
        )
    return InspectableSecondBasisEpochContinuationResearchSessionShell(lineage)


def create_inspectable_second_basis_epoch_continuation_handoff_research_session_shell(
    reentry: ChromiumResearchSecondBasisEpochContinuationReentryResult,
) -> InspectableSecondBasisEpochContinuationHandoffResearchSessionShell:
    if not isinstance(
        reentry,
        ChromiumResearchSecondBasisEpochContinuationReentryResult,
    ):
        raise TypeError(
            "reentry must be ChromiumResearchSecondBasisEpochContinuationReentryResult."
        )
    return InspectableSecondBasisEpochContinuationHandoffResearchSessionShell(reentry)


__all__ = [
    "InspectableSecondBasisEpochContinuationHandoffResearchSessionShell",
    "InspectableSecondBasisEpochContinuationResearchSessionShell",
    "InspectableSecondBasisEpochCumulativeHandoffResearchSessionShell",
    "create_inspectable_second_basis_epoch_continuation_handoff_research_session_shell",
    "create_inspectable_second_basis_epoch_continuation_research_session_shell",
    "create_inspectable_second_basis_epoch_cumulative_handoff_research_session_shell",
]
