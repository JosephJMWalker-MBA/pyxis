from __future__ import annotations

from textual.app import ComposeResult

from pyxis.app.chromium_research_root_backed_session_continuation_checkpoint_extension import (
    ChromiumResearchRootBackedSessionContinuationCheckpointExtensionResult,
)
from pyxis.app.chromium_research_root_backed_session_continuation_reentry_plan_document import (
    ChromiumResearchRootBackedSessionContinuationReentryResult,
)
from pyxis.app.chromium_research_root_backed_session_reentry import (
    ChromiumResearchRootBackedSessionReentryResult,
)
from pyxis.app.chromium_research_root_backed_session_shell_lineage import (
    ChromiumResearchRootBackedSessionContinuationShellLineage,
    ChromiumResearchRootBackedSessionShellLineage,
)
from pyxis.app.chromium_research_second_changed_basis_session_adoption import (
    ChromiumResearchSecondChangedBasisSessionAdoptionResult,
)
from pyxis.app.chromium_research_session_rollover import ChromiumResearchSessionRolloverResult

from .chromium_research_root_backed_session_authority_inspection_textual import (
    RootBackedAuthorityInspectionPanel,
)
from .root_backed_research_session_shell import RootBackedResearchSessionShell
from .second_changed_basis_session_adoption_research_session_shell import (
    SecondChangedBasisSessionAdoptionResearchSessionShell,
)


_INSPECTION_CSS = """
#research-root-backed-authority-inspection {
    width: 94%;
    height: auto;
    padding: 1 2;
    margin-top: 1;
    border: round $secondary;
}
"""


class InspectableRootBackedResearchSessionShell(RootBackedResearchSessionShell):
    """Path-proofed 35C first-checkpoint shell with immutable launch inspection."""

    CSS = RootBackedResearchSessionShell.CSS + _INSPECTION_CSS

    def __init__(self, lineage: ChromiumResearchRootBackedSessionShellLineage) -> None:
        if not isinstance(lineage, ChromiumResearchRootBackedSessionShellLineage):
            raise TypeError(
                "lineage must be ChromiumResearchRootBackedSessionShellLineage."
            )
        super().__init__(lineage.reentry)
        self.root_backed_launch_lineage = lineage
        self.root_backed_authority_inspection = (
            RootBackedAuthorityInspectionPanel.from_root_backed_launch(lineage)
        )

    def compose(self) -> ComposeResult:
        yield self.root_backed_authority_inspection
        yield from super().compose()

    async def _mount_research_rollover(
        self,
        result: ChromiumResearchSessionRolloverResult,
    ) -> None:
        launch = self.root_backed_authority_inspection.launch_provenance
        await super()._mount_research_rollover(result)
        if self.root_backed_authority_inspection.launch_provenance is not launch:
            raise ValueError(
                "Rollover must not replace immutable persisted root-backed launch provenance."
            )
        self.root_backed_authority_inspection.update_current_from_controller(
            self.research_controller,
            state_kind="visible one-hop continuation",
            state_source="explicit rollover from persisted 35C launch",
        )


class InspectableRootBackedHandoffResearchSessionShell(RootBackedResearchSessionShell):
    """Raw 44H root-backed handoff shell with no persistent launch path."""

    CSS = RootBackedResearchSessionShell.CSS + _INSPECTION_CSS

    def __init__(self, reentry: ChromiumResearchRootBackedSessionReentryResult) -> None:
        super().__init__(reentry)
        self.root_backed_authority_inspection = (
            RootBackedAuthorityInspectionPanel.from_root_backed_handoff(reentry)
        )

    def compose(self) -> ComposeResult:
        yield self.root_backed_authority_inspection
        yield from super().compose()

    async def _mount_research_rollover(
        self,
        result: ChromiumResearchSessionRolloverResult,
    ) -> None:
        launch = self.root_backed_authority_inspection.launch_provenance
        await super()._mount_research_rollover(result)
        if self.root_backed_authority_inspection.launch_provenance is not launch:
            raise ValueError(
                "Rollover must not replace immutable 44H handoff provenance."
            )
        self.root_backed_authority_inspection.update_current_from_controller(
            self.research_controller,
            state_kind="visible one-hop continuation",
            state_source="explicit rollover after in-process 44H handoff",
        )


class InspectableRootBackedContinuationResearchSessionShell(
    SecondChangedBasisSessionAdoptionResearchSessionShell
):
    """Path-proofed 35D/35E/46D shell with immutable launch inspection."""

    CSS = SecondChangedBasisSessionAdoptionResearchSessionShell.CSS + _INSPECTION_CSS

    def __init__(
        self,
        lineage: ChromiumResearchRootBackedSessionContinuationShellLineage,
    ) -> None:
        if not isinstance(
            lineage,
            ChromiumResearchRootBackedSessionContinuationShellLineage,
        ):
            raise TypeError(
                "lineage must be ChromiumResearchRootBackedSessionContinuationShellLineage."
            )
        super().__init__(lineage.reentry)
        self.root_backed_continuation_launch_lineage = lineage
        self.root_backed_authority_inspection = (
            RootBackedAuthorityInspectionPanel.from_continuation_launch(lineage)
        )

    def compose(self) -> ComposeResult:
        yield self.root_backed_authority_inspection
        yield from super().compose()

    async def _promote_cumulative_checkpoint(
        self,
        result: ChromiumResearchRootBackedSessionContinuationCheckpointExtensionResult,
    ) -> None:
        launch = self.root_backed_authority_inspection.launch_provenance
        await super()._promote_cumulative_checkpoint(result)
        if self.root_backed_authority_inspection.launch_provenance is not launch:
            raise ValueError(
                "Cumulative promotion must not replace immutable persisted root-backed continuation launch provenance."
            )
        self.root_backed_authority_inspection.update_current_from_continuation(
            self.root_backed_continuation_reentry,
            state_source="35E cumulative promotion",
        )

    async def _promote_second_changed_basis_session_adoption(
        self,
        result: ChromiumResearchSecondChangedBasisSessionAdoptionResult,
    ) -> None:
        launch = self.root_backed_authority_inspection.launch_provenance
        await super()._promote_second_changed_basis_session_adoption(result)
        if self.root_backed_authority_inspection.launch_provenance is not launch:
            raise ValueError(
                "46D adoption must not replace immutable persisted root-backed continuation launch provenance."
            )
        self.root_backed_authority_inspection.update_current_from_controller(
            self.research_controller,
            state_kind="adopted second changed-basis governed session",
            state_source="explicit 46D second changed-basis adoption",
        )


class InspectableRootBackedContinuationHandoffResearchSessionShell(
    SecondChangedBasisSessionAdoptionResearchSessionShell
):
    """Raw 36D/46D shell with no persistent launch path."""

    CSS = SecondChangedBasisSessionAdoptionResearchSessionShell.CSS + _INSPECTION_CSS

    def __init__(
        self,
        reentry: ChromiumResearchRootBackedSessionContinuationReentryResult,
    ) -> None:
        super().__init__(reentry)
        self.root_backed_authority_inspection = (
            RootBackedAuthorityInspectionPanel.from_continuation_handoff(reentry)
        )

    def compose(self) -> ComposeResult:
        yield self.root_backed_authority_inspection
        yield from super().compose()

    async def _promote_cumulative_checkpoint(
        self,
        result: ChromiumResearchRootBackedSessionContinuationCheckpointExtensionResult,
    ) -> None:
        launch = self.root_backed_authority_inspection.launch_provenance
        await super()._promote_cumulative_checkpoint(result)
        if self.root_backed_authority_inspection.launch_provenance is not launch:
            raise ValueError(
                "Cumulative promotion must not replace immutable 36D handoff provenance."
            )
        self.root_backed_authority_inspection.update_current_from_continuation(
            self.root_backed_continuation_reentry,
            state_source="35E cumulative promotion after in-process 36D handoff",
        )

    async def _promote_second_changed_basis_session_adoption(
        self,
        result: ChromiumResearchSecondChangedBasisSessionAdoptionResult,
    ) -> None:
        launch = self.root_backed_authority_inspection.launch_provenance
        await super()._promote_second_changed_basis_session_adoption(result)
        if self.root_backed_authority_inspection.launch_provenance is not launch:
            raise ValueError(
                "46D adoption must not replace immutable 36D handoff provenance."
            )
        self.root_backed_authority_inspection.update_current_from_controller(
            self.research_controller,
            state_kind="adopted second changed-basis governed session",
            state_source="explicit 46D second changed-basis adoption after in-process 36D handoff",
        )


def create_inspectable_root_backed_research_session_shell(
    lineage: ChromiumResearchRootBackedSessionShellLineage,
) -> InspectableRootBackedResearchSessionShell:
    return InspectableRootBackedResearchSessionShell(lineage)


def create_inspectable_root_backed_handoff_research_session_shell(
    reentry: ChromiumResearchRootBackedSessionReentryResult,
) -> InspectableRootBackedHandoffResearchSessionShell:
    return InspectableRootBackedHandoffResearchSessionShell(reentry)


def create_inspectable_root_backed_continuation_research_session_shell(
    lineage: ChromiumResearchRootBackedSessionContinuationShellLineage,
) -> InspectableRootBackedContinuationResearchSessionShell:
    return InspectableRootBackedContinuationResearchSessionShell(lineage)


def create_inspectable_root_backed_continuation_handoff_research_session_shell(
    reentry: ChromiumResearchRootBackedSessionContinuationReentryResult,
) -> InspectableRootBackedContinuationHandoffResearchSessionShell:
    return InspectableRootBackedContinuationHandoffResearchSessionShell(reentry)


__all__ = [
    "InspectableRootBackedContinuationHandoffResearchSessionShell",
    "InspectableRootBackedContinuationResearchSessionShell",
    "InspectableRootBackedHandoffResearchSessionShell",
    "InspectableRootBackedResearchSessionShell",
    "create_inspectable_root_backed_continuation_handoff_research_session_shell",
    "create_inspectable_root_backed_continuation_research_session_shell",
    "create_inspectable_root_backed_handoff_research_session_shell",
    "create_inspectable_root_backed_research_session_shell",
]
