from __future__ import annotations

from pathlib import Path

from textual.widgets import Button, Input, Static, TextArea

from pyxis.app.chromium_research_second_basis_epoch_continuation_reentry_plan_document import (
    ChromiumResearchSecondBasisEpochContinuationReentryResult,
)
from pyxis.app.chromium_research_second_basis_epoch_shell_lineage import (
    ChromiumResearchSecondBasisEpochContinuationShellLineage,
)
from pyxis.app.chromium_research_third_changed_basis_root_edge import (
    ChromiumResearchThirdChangedBasisRootEdgeResult,
    persist_chromium_research_third_changed_basis_root_edge,
)

from .chromium_research_third_changed_basis_root_edge_textual import (
    ResearchThirdChangedBasisRootEdgeControls,
)
from .third_changed_basis_revision_root_research_session_shell import (
    InspectableThirdChangedBasisRevisionRootHandoffResearchSessionShell,
    InspectableThirdChangedBasisRevisionRootResearchSessionShell,
    ThirdChangedBasisRevisionRootHandoffResearchSessionShell,
    ThirdChangedBasisRevisionRootResearchSessionShell,
)


_THIRD_CHANGED_BASIS_ROOT_EDGE_CSS = """
#research-third-changed-basis-root-edge-controls {
    width: 94%;
    height: auto;
    padding: 1 2;
    margin-top: 1;
    border: round $warning;
}

#research-third-changed-basis-root-edge-authority-notice,
#research-third-changed-basis-root-edge-root-summary,
#research-third-changed-basis-root-edge-rationale-label,
#research-third-changed-basis-root-edge-root-source-label,
#research-third-changed-basis-root-edge-destination-label,
#research-third-changed-basis-root-edge-status {
    margin-top: 1;
}

#research-third-changed-basis-root-edge-title,
#research-third-changed-basis-root-edge-rationale-label,
#research-third-changed-basis-root-edge-root-source-label,
#research-third-changed-basis-root-edge-destination-label {
    text-style: bold;
}

#research-third-changed-basis-root-edge-rationale {
    width: 100%;
    height: 8;
    margin-top: 1;
}

#persist-research-third-changed-basis-root-edge {
    margin-top: 1;
}
"""


class _ThirdChangedBasisRootEdgeProductMixin:
    """47C-only behavior shared by the four dedicated 47B launch products."""

    last_third_changed_basis_root_edge: ChromiumResearchThirdChangedBasisRootEdgeResult | None

    def __init__(self, authority) -> None:
        super().__init__(authority)
        self.last_third_changed_basis_root_edge = None

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Own only the 47C action; inherited Textual handlers remain MRO-dispatched."""

        if event.button.id == "persist-research-third-changed-basis-root-edge":
            event.stop()
            self.call_after_refresh(self._persist_third_changed_basis_root_edge)

    async def _persist_third_changed_basis_revision_root(self) -> None:
        """Run inherited 47B, then mount 47C only after one new exact success."""

        prior = self.last_third_changed_basis_revision_root
        await super()._persist_third_changed_basis_revision_root()
        root_result = self.last_third_changed_basis_revision_root
        if root_result is None or root_result is prior:
            return
        if len(self.query("#research-third-changed-basis-root-edge-controls")) != 0:
            raise ValueError("Third changed-basis root-edge controls are already mounted.")
        await self.mount(ResearchThirdChangedBasisRootEdgeControls(root_result))

    async def _persist_third_changed_basis_root_edge(self) -> None:
        controls = self.query_one(
            "#research-third-changed-basis-root-edge-controls",
            ResearchThirdChangedBasisRootEdgeControls,
        )
        status = self.query_one(
            "#research-third-changed-basis-root-edge-status",
            Static,
        )
        root_result = self.last_third_changed_basis_revision_root
        if root_result is None or controls.root_result is not root_result:
            status.update(
                "Edge failed: no exact successful third changed-basis root owns this form."
            )
            return

        rationale = self.query_one(
            "#research-third-changed-basis-root-edge-rationale", TextArea
        )
        if not rationale.text.strip():
            status.update("Edge failed: a new human post-root rationale is required.")
            return

        root_source = self.query_one(
            "#research-third-changed-basis-root-edge-root-source", Input
        )
        destination = self.query_one(
            "#research-third-changed-basis-root-edge-destination", Input
        )
        required = (
            (root_source, "explicit current third-root path"),
            (destination, "explicit first post-third-root edge destination path"),
        )
        for widget, label in required:
            if not widget.value.strip():
                status.update(f"Edge failed: {label} is required.")
                return

        mounted_controller = self.research_controller
        mounted_session = self.research_session
        mounted_reentry = self.second_basis_epoch_continuation_reentry
        try:
            result = persist_chromium_research_third_changed_basis_root_edge(
                root_result,
                revised_note_text=rationale.text,
                root_source=Path(root_source.value),
                destination=Path(destination.value),
            )
        except Exception as exc:
            status.update(f"Edge failed: {exc}")
            return

        if result.root_result is not root_result:
            raise ValueError(
                "Third changed-basis root edge did not retain the exact successful 47B root."
            )
        if (
            self.research_controller is not mounted_controller
            or self.research_session is not mounted_session
            or self.second_basis_epoch_continuation_reentry is not mounted_reentry
        ):
            raise ValueError(
                "Mounted second-epoch continuation changed during third-root edge persistence."
            )

        self.last_third_changed_basis_root_edge = result
        controls.lock_after_success(result)


class ThirdChangedBasisRootEdgeResearchSessionShell(
    _ThirdChangedBasisRootEdgeProductMixin,
    ThirdChangedBasisRevisionRootResearchSessionShell,
):
    """47C product from one path-proofed persisted second-epoch continuation launch."""

    CSS = (
        ThirdChangedBasisRevisionRootResearchSessionShell.CSS
        + _THIRD_CHANGED_BASIS_ROOT_EDGE_CSS
    )


class ThirdChangedBasisRootEdgeHandoffResearchSessionShell(
    _ThirdChangedBasisRootEdgeProductMixin,
    ThirdChangedBasisRevisionRootHandoffResearchSessionShell,
):
    """47C product from one exact pathless second-epoch continuation handoff."""

    CSS = (
        ThirdChangedBasisRevisionRootHandoffResearchSessionShell.CSS
        + _THIRD_CHANGED_BASIS_ROOT_EDGE_CSS
    )


class InspectableThirdChangedBasisRootEdgeResearchSessionShell(
    _ThirdChangedBasisRootEdgeProductMixin,
    InspectableThirdChangedBasisRevisionRootResearchSessionShell,
):
    """Inspectable persisted-launch 47C product retaining immutable launch provenance."""

    CSS = (
        InspectableThirdChangedBasisRevisionRootResearchSessionShell.CSS
        + _THIRD_CHANGED_BASIS_ROOT_EDGE_CSS
    )


class InspectableThirdChangedBasisRootEdgeHandoffResearchSessionShell(
    _ThirdChangedBasisRootEdgeProductMixin,
    InspectableThirdChangedBasisRevisionRootHandoffResearchSessionShell,
):
    """Inspectable pathless 47C product retaining immutable raw launch provenance."""

    CSS = (
        InspectableThirdChangedBasisRevisionRootHandoffResearchSessionShell.CSS
        + _THIRD_CHANGED_BASIS_ROOT_EDGE_CSS
    )


def create_third_changed_basis_root_edge_research_session_shell(
    lineage: ChromiumResearchSecondBasisEpochContinuationShellLineage,
) -> ThirdChangedBasisRootEdgeResearchSessionShell:
    if not isinstance(lineage, ChromiumResearchSecondBasisEpochContinuationShellLineage):
        raise TypeError(
            "lineage must be ChromiumResearchSecondBasisEpochContinuationShellLineage."
        )
    return ThirdChangedBasisRootEdgeResearchSessionShell(lineage)


def create_third_changed_basis_root_edge_handoff_research_session_shell(
    reentry: ChromiumResearchSecondBasisEpochContinuationReentryResult,
) -> ThirdChangedBasisRootEdgeHandoffResearchSessionShell:
    if type(reentry) is not ChromiumResearchSecondBasisEpochContinuationReentryResult:
        raise TypeError(
            "reentry must be exactly ChromiumResearchSecondBasisEpochContinuationReentryResult."
        )
    return ThirdChangedBasisRootEdgeHandoffResearchSessionShell(reentry)


def create_inspectable_third_changed_basis_root_edge_research_session_shell(
    lineage: ChromiumResearchSecondBasisEpochContinuationShellLineage,
) -> InspectableThirdChangedBasisRootEdgeResearchSessionShell:
    if not isinstance(lineage, ChromiumResearchSecondBasisEpochContinuationShellLineage):
        raise TypeError(
            "lineage must be ChromiumResearchSecondBasisEpochContinuationShellLineage."
        )
    return InspectableThirdChangedBasisRootEdgeResearchSessionShell(lineage)


def create_inspectable_third_changed_basis_root_edge_handoff_research_session_shell(
    reentry: ChromiumResearchSecondBasisEpochContinuationReentryResult,
) -> InspectableThirdChangedBasisRootEdgeHandoffResearchSessionShell:
    if type(reentry) is not ChromiumResearchSecondBasisEpochContinuationReentryResult:
        raise TypeError(
            "reentry must be exactly ChromiumResearchSecondBasisEpochContinuationReentryResult."
        )
    return InspectableThirdChangedBasisRootEdgeHandoffResearchSessionShell(reentry)


__all__ = [
    "InspectableThirdChangedBasisRootEdgeHandoffResearchSessionShell",
    "InspectableThirdChangedBasisRootEdgeResearchSessionShell",
    "ThirdChangedBasisRootEdgeHandoffResearchSessionShell",
    "ThirdChangedBasisRootEdgeResearchSessionShell",
    "create_inspectable_third_changed_basis_root_edge_handoff_research_session_shell",
    "create_inspectable_third_changed_basis_root_edge_research_session_shell",
    "create_third_changed_basis_root_edge_handoff_research_session_shell",
    "create_third_changed_basis_root_edge_research_session_shell",
]
