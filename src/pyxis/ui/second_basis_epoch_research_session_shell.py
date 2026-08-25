from __future__ import annotations

from pyxis.app.chromium_research_second_basis_epoch_shell_lineage import (
    ChromiumResearchSecondBasisEpochContinuationShellLineage,
    ChromiumResearchSecondBasisEpochShellLineage,
)

from .research_session_shell import ResearchSessionShell


class SecondBasisEpochResearchSessionShell(ResearchSessionShell):
    """Controller shell retaining one exact proven 37B launch lineage.

    The 38B wrapper is launch authority only: it binds the explicit 37B location to
    the fresh second-epoch re-entry proven from that location. The base shell receives
    only that fresh governed controller and deliberately receives no ordinary 31A
    re-entry lineage, so ordinary restart-plan controls are never authorized here.

    This milestone adds no second-epoch checkpoint behavior. If the live controller
    later moves through ordinary in-memory revision/rollover behavior, the retained
    launch lineage is not rewritten or promoted into a claim that the moved state is
    durably restartable.
    """

    def __init__(self, lineage: ChromiumResearchSecondBasisEpochShellLineage) -> None:
        if not isinstance(lineage, ChromiumResearchSecondBasisEpochShellLineage):
            raise TypeError(
                "lineage must be ChromiumResearchSecondBasisEpochShellLineage."
            )
        super().__init__(lineage.reentry.controller)
        self.second_basis_epoch_launch_lineage = lineage


class SecondBasisEpochContinuationResearchSessionShell(ResearchSessionShell):
    """Controller shell retaining one exact proven 37C/37D launch lineage.

    The supplied 38B continuation wrapper remains explicit launch context only. No
    ordinary 31A lineage, second-epoch checkpoint controls, path prefilling, or
    automatic persistence authority is inferred from the live controller.
    """

    def __init__(
        self,
        lineage: ChromiumResearchSecondBasisEpochContinuationShellLineage,
    ) -> None:
        if not isinstance(
            lineage,
            ChromiumResearchSecondBasisEpochContinuationShellLineage,
        ):
            raise TypeError(
                "lineage must be ChromiumResearchSecondBasisEpochContinuationShellLineage."
            )
        super().__init__(lineage.reentry.controller)
        self.second_basis_epoch_continuation_launch_lineage = lineage


def create_second_basis_epoch_research_session_shell(
    lineage: ChromiumResearchSecondBasisEpochShellLineage,
) -> SecondBasisEpochResearchSessionShell:
    """Create one controller-only shell retaining exact proven 37B launch lineage."""

    return SecondBasisEpochResearchSessionShell(lineage)


def create_second_basis_epoch_continuation_research_session_shell(
    lineage: ChromiumResearchSecondBasisEpochContinuationShellLineage,
) -> SecondBasisEpochContinuationResearchSessionShell:
    """Create one controller-only shell retaining exact proven 37C/37D launch lineage."""

    return SecondBasisEpochContinuationResearchSessionShell(lineage)


__all__ = [
    "SecondBasisEpochContinuationResearchSessionShell",
    "SecondBasisEpochResearchSessionShell",
    "create_second_basis_epoch_continuation_research_session_shell",
    "create_second_basis_epoch_research_session_shell",
]
