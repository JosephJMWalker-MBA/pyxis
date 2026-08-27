from __future__ import annotations

from pyxis.app.chromium_research_third_basis_epoch_shell_lineage import (
    ChromiumResearchThirdBasisEpochContinuationShellLineage,
    ChromiumResearchThirdBasisEpochShellLineage,
)

from .research_session_shell import ResearchSessionShell


class ThirdBasisEpochResearchSessionShell(ResearchSessionShell):
    """Controller shell retaining one exact proven 40B launch lineage.

    The 41A wrapper is launch authority only: it binds the explicit 40B location to
    the fresh three-root re-entry proven from that location. The base shell receives
    only that fresh governed controller and deliberately receives no ordinary 31A
    re-entry lineage, so ordinary restart-plan controls are never authorized here.

    41B adds no third-epoch checkpoint behavior. If the live controller later moves
    through ordinary in-memory revision/rollover behavior, the retained launch lineage
    is not rewritten or promoted into a claim that the moved state is durably
    restartable.
    """

    def __init__(self, lineage: ChromiumResearchThirdBasisEpochShellLineage) -> None:
        if not isinstance(lineage, ChromiumResearchThirdBasisEpochShellLineage):
            raise TypeError(
                "lineage must be ChromiumResearchThirdBasisEpochShellLineage."
            )
        super().__init__(lineage.reentry.controller)
        self.third_basis_epoch_launch_lineage = lineage


class ThirdBasisEpochContinuationResearchSessionShell(ResearchSessionShell):
    """Controller shell retaining one exact proven 40C/40D launch lineage.

    The supplied 41A continuation wrapper remains explicit launch context only. No
    ordinary 31A lineage, third-epoch checkpoint controls, path prefilling, automatic
    persistence, or inspection authority is inferred from the live controller.
    """

    def __init__(
        self,
        lineage: ChromiumResearchThirdBasisEpochContinuationShellLineage,
    ) -> None:
        if not isinstance(
            lineage,
            ChromiumResearchThirdBasisEpochContinuationShellLineage,
        ):
            raise TypeError(
                "lineage must be ChromiumResearchThirdBasisEpochContinuationShellLineage."
            )
        super().__init__(lineage.reentry.controller)
        self.third_basis_epoch_continuation_launch_lineage = lineage


def create_third_basis_epoch_research_session_shell(
    lineage: ChromiumResearchThirdBasisEpochShellLineage,
) -> ThirdBasisEpochResearchSessionShell:
    """Create one controller shell retaining exact proven 40B launch lineage."""

    return ThirdBasisEpochResearchSessionShell(lineage)


def create_third_basis_epoch_continuation_research_session_shell(
    lineage: ChromiumResearchThirdBasisEpochContinuationShellLineage,
) -> ThirdBasisEpochContinuationResearchSessionShell:
    """Create one controller shell retaining exact proven 40C/40D launch lineage."""

    return ThirdBasisEpochContinuationResearchSessionShell(lineage)


__all__ = [
    "ThirdBasisEpochContinuationResearchSessionShell",
    "ThirdBasisEpochResearchSessionShell",
    "create_third_basis_epoch_continuation_research_session_shell",
    "create_third_basis_epoch_research_session_shell",
]
