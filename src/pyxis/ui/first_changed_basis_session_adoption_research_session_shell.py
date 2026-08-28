from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from textual.widgets import Button, Input, Static

from pyxis.app.chromium_research_first_changed_basis_session_adoption import (
    ChromiumResearchFirstChangedBasisSessionAdoptionResult,
    adopt_chromium_research_first_changed_basis_governed_session,
)
from pyxis.app.chromium_research_session_reentry import ChromiumResearchSessionReentryResult
from pyxis.app.chromium_research_working_set import ChromiumPageResearchWorkingSetItem

from .chromium_research_endpoint_revision_textual import ResearchEndpointRevisionControls
from .chromium_research_first_changed_basis_session_adoption_textual import (
    ResearchFirstChangedBasisSessionAdoptionControls,
)
from .chromium_research_revision_edge_sequence_textual import (
    ResearchRevisionEdgeSequenceDetail,
    _snapshot_working_set_contexts,
)
from .chromium_research_session_rollover_textual import ResearchSessionRolloverControls
from .first_changed_basis_root_edge_research_session_shell import (
    FirstChangedBasisRootEdgeResearchSessionShell,
)


class FirstChangedBasisSessionAdoptionResearchSessionShell(
    FirstChangedBasisRootEdgeResearchSessionShell
):
    """Concrete 44A→44B→44C→44D→44E surface through explicit 35A adoption.

    The upstream changed-basis artifacts remain historical evidence until the 44E
    action succeeds. Adoption then intentionally replaces this shell's active governed
    controller with the exact root-backed 35A controller while retaining the locked
    44A–44E receipts.

    This is shell-local branch adoption only. It does not create 35B root-backed
    fresh-process re-entry authority and does not modify later root-backed/epoch shells.
    """

    CSS = FirstChangedBasisRootEdgeResearchSessionShell.CSS + """
    #research-first-changed-basis-session-adoption-controls {
        width: 94%;
        height: auto;
        padding: 1 2;
        margin-top: 1;
        border: round $warning;
    }

    #research-first-changed-basis-session-adoption-authority-notice,
    #research-first-changed-basis-session-adoption-summary,
    #research-first-changed-basis-session-adoption-edge-source-label,
    #research-first-changed-basis-session-adoption-declaration-destination-label,
    #research-first-changed-basis-session-adoption-status {
        margin-top: 1;
    }

    #research-first-changed-basis-session-adoption-title,
    #research-first-changed-basis-session-adoption-edge-source-label,
    #research-first-changed-basis-session-adoption-declaration-destination-label {
        text-style: bold;
    }

    #adopt-research-first-changed-basis-session {
        margin-top: 1;
    }
    """

    def __init__(
        self,
        ordinary_reentry: ChromiumResearchSessionReentryResult,
        appended_items: Iterable[ChromiumPageResearchWorkingSetItem],
    ) -> None:
        super().__init__(ordinary_reentry, appended_items)
        self.last_first_changed_basis_session_adoption: (
            ChromiumResearchFirstChangedBasisSessionAdoptionResult | None
        ) = None

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "adopt-research-first-changed-basis-session":
            event.stop()
            self.call_after_refresh(self._adopt_research_first_changed_basis_session)
            return
        super().on_button_pressed(event)

    async def _persist_research_first_changed_basis_root_edge(self) -> None:
        """Run inherited 44D, then mount 44E only after one new exact success."""

        prior = self.last_first_changed_basis_root_edge
        await super()._persist_research_first_changed_basis_root_edge()
        edge_result = self.last_first_changed_basis_root_edge
        if edge_result is None or edge_result is prior:
            return
        if len(self.query("#research-first-changed-basis-session-adoption-controls")) != 0:
            raise ValueError("Changed-basis session-adoption controls are already mounted.")
        await self.mount(ResearchFirstChangedBasisSessionAdoptionControls(edge_result))

    async def _adopt_research_first_changed_basis_session(self) -> None:
        controls = self.query_one(
            "#research-first-changed-basis-session-adoption-controls",
            ResearchFirstChangedBasisSessionAdoptionControls,
        )
        status = self.query_one(
            "#research-first-changed-basis-session-adoption-status",
            Static,
        )
        edge_result = self.last_first_changed_basis_root_edge
        if edge_result is None or controls.edge_result is not edge_result:
            status.update(
                "Adoption failed: no exact successful first changed-basis edge owns this form."
            )
            return

        edge_source = self.query_one(
            "#research-first-changed-basis-session-adoption-edge-source",
            Input,
        )
        declaration_destination = self.query_one(
            "#research-first-changed-basis-session-adoption-declaration-destination",
            Input,
        )
        if not edge_source.value.strip():
            status.update(
                "Adoption failed: explicit current first-edge path is required."
            )
            return
        if not declaration_destination.value.strip():
            status.update(
                "Adoption failed: explicit no-overwrite root-backed declaration destination is required."
            )
            return

        prior_controller = self.research_controller
        try:
            result = adopt_chromium_research_first_changed_basis_governed_session(
                edge_result,
                edge_source=Path(edge_source.value),
                declaration_destination=Path(declaration_destination.value),
            )
        except Exception as exc:
            status.update(f"Adoption failed: {exc}")
            return

        if result.edge_result is not edge_result:
            raise ValueError(
                "Changed-basis session adoption did not retain the exact successful 44D edge."
            )
        if self.research_controller is not prior_controller:
            raise ValueError(
                "Mounted governed research controller changed during 35A declaration construction."
            )

        controls.lock_after_success(result)
        await self._promote_first_changed_basis_session_adoption(result)

    async def _promote_first_changed_basis_session_adoption(
        self,
        result: ChromiumResearchFirstChangedBasisSessionAdoptionResult,
    ) -> None:
        """Replace only the active governed surface after one explicit 44E success."""

        if result is not self.last_first_changed_basis_session_adoption and (
            self.last_first_changed_basis_session_adoption is not None
        ):
            raise ValueError("A different changed-basis adoption is already retained.")

        controller = result.controller
        session = controller.presentation
        presentation = session.sequence
        contexts = _snapshot_working_set_contexts(
            presentation,
            session.working_set_contexts,
        )
        if len(contexts) != len(presentation.members):
            raise ValueError(
                "Adopted changed-basis session must contain one context per declared position."
            )
        if (
            controller.declared_endpoint.verification.edge_record_sha256
            != result.edge_result.persistence.edge_record_sha256
        ):
            raise ValueError(
                "Adopted changed-basis controller endpoint does not match the exact 44D edge."
            )

        old_detail = self.query_one(
            "#research-revision-edge-sequence",
            ResearchRevisionEdgeSequenceDetail,
        )
        old_revision = self.query_one(
            "#research-endpoint-revision-controls",
            ResearchEndpointRevisionControls,
        )
        old_rollover = self.query_one(
            "#research-session-rollover-controls",
            ResearchSessionRolloverControls,
        )

        await old_detail.remove()
        await old_revision.remove()
        await old_rollover.remove()
        for selector in (
            "#research-session-restart-plan-controls",
            "#research-rollover-success-receipt",
        ):
            matches = list(self.query(selector))
            if len(matches) > 1:
                raise ValueError(
                    f"Changed-basis adoption found multiple active widgets for {selector}."
                )
            if matches:
                await matches[0].remove()

        self.research_controller = controller
        self.research_reentry = None
        self.research_session = session
        self.research_presentation = presentation
        self.research_working_set_contexts = contexts
        self.last_research_rollover = None
        self.last_research_restart_plan = None

        # The old candidate belonged to a different governed controller. Preserve the
        # completed 44A–44E result objects/receipts, but retain no live candidate authority.
        self.changed_basis_candidate_items = None
        self.changed_basis_candidate_presentation = None
        self.changed_basis_candidate_controller = None
        self.changed_basis_candidate_endpoint = None

        self.last_first_changed_basis_session_adoption = result

        await self.mount(
            ResearchRevisionEdgeSequenceDetail(
                presentation,
                working_set_contexts=contexts,
            )
        )
        await self.mount(ResearchEndpointRevisionControls())
        await self.mount(ResearchSessionRolloverControls())


def create_first_changed_basis_session_adoption_research_session_shell(
    ordinary_reentry: ChromiumResearchSessionReentryResult,
    appended_items: Iterable[ChromiumPageResearchWorkingSetItem],
) -> FirstChangedBasisSessionAdoptionResearchSessionShell:
    """Create the concrete first-changed-basis product surface through 35A adoption."""

    return FirstChangedBasisSessionAdoptionResearchSessionShell(
        ordinary_reentry,
        appended_items,
    )


__all__ = [
    "FirstChangedBasisSessionAdoptionResearchSessionShell",
    "create_first_changed_basis_session_adoption_research_session_shell",
]
