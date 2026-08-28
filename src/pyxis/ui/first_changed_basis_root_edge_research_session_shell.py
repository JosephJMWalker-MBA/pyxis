from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from textual.widgets import Button, Input, Static, TextArea

from pyxis.app.chromium_research_first_changed_basis_root_edge import (
    ChromiumResearchFirstChangedBasisRootEdgeResult,
    persist_chromium_research_first_changed_basis_root_edge,
)
from pyxis.app.chromium_research_session_reentry import ChromiumResearchSessionReentryResult
from pyxis.app.chromium_research_working_set import ChromiumPageResearchWorkingSetItem

from .chromium_research_first_changed_basis_root_edge_textual import (
    ResearchFirstChangedBasisRootEdgeControls,
)
from .first_changed_basis_root_research_session_shell import (
    FirstChangedBasisRootResearchSessionShell,
)


class FirstChangedBasisRootEdgeResearchSessionShell(
    FirstChangedBasisRootResearchSessionShell
):
    """Concrete 44A→44B→44C→44D surface through the first post-root edge.

    This shell inherits only the dedicated first-basis product chain. It mounts one
    34B bridge form after the exact first 44C root succeeds. Existing root-backed and
    later epoch shells do not subclass it, so they cannot inherit a generic root-edge
    action by implementation symmetry.

    A successful 44C root remains historical evidence even if the mounted old-basis
    session later continues. This shell therefore does not stale the 44D form on an
    old-basis rollover.
    """

    CSS = FirstChangedBasisRootResearchSessionShell.CSS + """
    #research-first-changed-basis-root-edge-controls {
        width: 94%;
        height: auto;
        padding: 1 2;
        margin-top: 1;
        border: round $warning;
    }

    #research-first-changed-basis-root-edge-authority-notice,
    #research-first-changed-basis-root-edge-root-summary,
    #research-first-changed-basis-root-edge-rationale-label,
    #research-first-changed-basis-root-edge-root-source-label,
    #research-first-changed-basis-root-edge-destination-label,
    #research-first-changed-basis-root-edge-status {
        margin-top: 1;
    }

    #research-first-changed-basis-root-edge-title,
    #research-first-changed-basis-root-edge-rationale-label,
    #research-first-changed-basis-root-edge-root-source-label,
    #research-first-changed-basis-root-edge-destination-label {
        text-style: bold;
    }

    #research-first-changed-basis-root-edge-rationale {
        width: 100%;
        height: 8;
        margin-top: 1;
    }

    #persist-research-first-changed-basis-root-edge {
        margin-top: 1;
    }
    """

    def __init__(
        self,
        ordinary_reentry: ChromiumResearchSessionReentryResult,
        appended_items: Iterable[ChromiumPageResearchWorkingSetItem],
    ) -> None:
        super().__init__(ordinary_reentry, appended_items)
        self.last_first_changed_basis_root_edge: (
            ChromiumResearchFirstChangedBasisRootEdgeResult | None
        ) = None

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "persist-research-first-changed-basis-root-edge":
            event.stop()
            self.call_after_refresh(self._persist_research_first_changed_basis_root_edge)
            return
        super().on_button_pressed(event)

    async def _persist_research_first_changed_basis_revision_root(self) -> None:
        """Run inherited 44C, then mount 44D only after one new exact success."""

        prior = self.last_first_changed_basis_revision_root
        await super()._persist_research_first_changed_basis_revision_root()
        root_result = self.last_first_changed_basis_revision_root
        if root_result is None or root_result is prior:
            return
        if len(self.query("#research-first-changed-basis-root-edge-controls")) != 0:
            raise ValueError("First post-root edge controls are already mounted.")
        await self.mount(ResearchFirstChangedBasisRootEdgeControls(root_result))

    async def _persist_research_first_changed_basis_root_edge(self) -> None:
        controls = self.query_one(
            "#research-first-changed-basis-root-edge-controls",
            ResearchFirstChangedBasisRootEdgeControls,
        )
        status = self.query_one(
            "#research-first-changed-basis-root-edge-status", Static
        )
        root_result = self.last_first_changed_basis_revision_root
        if root_result is None or controls.root_result is not root_result:
            status.update(
                "Edge failed: no exact successful first changed-basis root owns this form."
            )
            return

        rationale = self.query_one(
            "#research-first-changed-basis-root-edge-rationale", TextArea
        )
        if not rationale.text.strip():
            status.update("Edge failed: a new human rationale is required.")
            return

        root_source = self.query_one(
            "#research-first-changed-basis-root-edge-root-source", Input
        )
        destination = self.query_one(
            "#research-first-changed-basis-root-edge-destination", Input
        )
        if not root_source.value.strip():
            status.update("Edge failed: explicit current root path is required.")
            return
        if not destination.value.strip():
            status.update(
                "Edge failed: explicit first post-root edge destination path is required."
            )
            return

        mounted_controller = self.research_controller
        mounted_session = self.research_session
        try:
            result = persist_chromium_research_first_changed_basis_root_edge(
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
                "First post-root edge did not retain the exact successful 44C root."
            )
        if (
            self.research_controller is not mounted_controller
            or self.research_session is not mounted_session
        ):
            raise ValueError(
                "Mounted governed research session changed during first post-root edge persistence."
            )

        self.last_first_changed_basis_root_edge = result
        controls.lock_after_success(result)


def create_first_changed_basis_root_edge_research_session_shell(
    ordinary_reentry: ChromiumResearchSessionReentryResult,
    appended_items: Iterable[ChromiumPageResearchWorkingSetItem],
) -> FirstChangedBasisRootEdgeResearchSessionShell:
    """Create the concrete 44A→44B→44C→44D first-root-edge product surface."""

    return FirstChangedBasisRootEdgeResearchSessionShell(
        ordinary_reentry,
        appended_items,
    )


__all__ = [
    "FirstChangedBasisRootEdgeResearchSessionShell",
    "create_first_changed_basis_root_edge_research_session_shell",
]
