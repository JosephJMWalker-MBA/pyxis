from __future__ import annotations

from pathlib import Path

from textual.widgets import Button, Input, Static

from pyxis.app.chromium_research_second_changed_basis_session_adoption import (
    ChromiumResearchSecondChangedBasisSessionAdoptionResult,
    adopt_chromium_research_second_changed_basis_governed_session,
)
from pyxis.app.chromium_research_session_rollover import ChromiumResearchSessionRolloverResult

from .chromium_research_endpoint_revision_textual import ResearchEndpointRevisionControls
from .chromium_research_revision_edge_sequence_textual import (
    ResearchRevisionEdgeSequenceDetail,
    _snapshot_working_set_contexts,
)
from .chromium_research_second_changed_basis_session_adoption_textual import (
    ResearchSecondChangedBasisSessionAdoptionControls,
)
from .chromium_research_session_rollover_textual import ResearchSessionRolloverControls
from .research_session_shell import ResearchSessionShell
from .root_backed_continuation_research_session_shell import (
    RootBackedContinuationResearchSessionShell,
)


class SecondChangedBasisSessionAdoptionResearchSessionShell(
    RootBackedContinuationResearchSessionShell
):
    """Concrete 46A→46B→46C→46D surface through explicit second-basis adoption.

    The inherited one-root continuation remains active until 46D succeeds. Adoption
    then intentionally replaces this shell's active governed controller with the exact
    second-root-backed declared controller while retaining the completed 46-series
    artifacts as historical evidence.

    The retained first-root continuation re-entry remains ancestry/provenance context
    only after adoption. It is no longer current checkpoint authority, so subsequent
    rollovers use the ordinary governed-session path rather than first-root 35E.
    """

    CSS = RootBackedContinuationResearchSessionShell.CSS + """
    #research-second-changed-basis-session-adoption-controls {
        width: 94%;
        height: auto;
        padding: 1 2;
        margin-top: 1;
        border: round $warning;
    }

    #research-second-changed-basis-session-adoption-authority-notice,
    #research-second-changed-basis-session-adoption-summary,
    #research-second-changed-basis-session-adoption-edge-source-label,
    #research-second-changed-basis-session-adoption-declaration-destination-label,
    #research-second-changed-basis-session-adoption-status {
        margin-top: 1;
    }

    #research-second-changed-basis-session-adoption-title,
    #research-second-changed-basis-session-adoption-edge-source-label,
    #research-second-changed-basis-session-adoption-declaration-destination-label {
        text-style: bold;
    }

    #adopt-research-second-changed-basis-session {
        margin-top: 1;
    }
    """

    def __init__(self, reentry) -> None:
        super().__init__(reentry)
        self.last_second_changed_basis_session_adoption: (
            ChromiumResearchSecondChangedBasisSessionAdoptionResult | None
        ) = None

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "adopt-research-second-changed-basis-session":
            event.stop()
            self.call_after_refresh(self._adopt_second_changed_basis_session)
            return
        super().on_button_pressed(event)

    async def _persist_second_changed_basis_root_edge(self) -> None:
        """Run inherited 46C, then mount 46D only after one new exact success."""

        prior = self.last_second_changed_basis_root_edge
        await super()._persist_second_changed_basis_root_edge()
        edge_result = self.last_second_changed_basis_root_edge
        if edge_result is None or edge_result is prior:
            return
        if len(self.query("#research-second-changed-basis-session-adoption-controls")) != 0:
            raise ValueError("Second changed-basis session-adoption controls are already mounted.")
        await self.mount(ResearchSecondChangedBasisSessionAdoptionControls(edge_result))

    async def _adopt_second_changed_basis_session(self) -> None:
        controls = self.query_one(
            "#research-second-changed-basis-session-adoption-controls",
            ResearchSecondChangedBasisSessionAdoptionControls,
        )
        status = self.query_one(
            "#research-second-changed-basis-session-adoption-status",
            Static,
        )
        edge_result = self.last_second_changed_basis_root_edge
        if edge_result is None or controls.edge_result is not edge_result:
            status.update(
                "Adoption failed: no exact successful 46C edge owns this form."
            )
            return

        edge_source = self.query_one(
            "#research-second-changed-basis-session-adoption-edge-source",
            Input,
        )
        declaration_destination = self.query_one(
            "#research-second-changed-basis-session-adoption-declaration-destination",
            Input,
        )
        if not edge_source.value.strip():
            status.update(
                "Adoption failed: explicit current post-second-root edge path is required."
            )
            return
        if not declaration_destination.value.strip():
            status.update(
                "Adoption failed: explicit no-overwrite second-root-backed declaration destination is required."
            )
            return

        prior_controller = self.research_controller
        prior_session = self.research_session
        prior_reentry = self.root_backed_continuation_reentry
        try:
            result = adopt_chromium_research_second_changed_basis_governed_session(
                edge_result,
                edge_source=Path(edge_source.value),
                declaration_destination=Path(declaration_destination.value),
            )
        except Exception as exc:
            status.update(f"Adoption failed: {exc}")
            return

        if result.edge_result is not edge_result:
            raise ValueError(
                "Second changed-basis adoption did not retain the exact successful 46C edge."
            )
        if (
            self.research_controller is not prior_controller
            or self.research_session is not prior_session
            or self.root_backed_continuation_reentry is not prior_reentry
        ):
            raise ValueError(
                "Mounted one-root continuation changed during 46D declaration construction."
            )

        controls.lock_after_success(result)
        await self._promote_second_changed_basis_session_adoption(result)

    async def _promote_second_changed_basis_session_adoption(
        self,
        result: ChromiumResearchSecondChangedBasisSessionAdoptionResult,
    ) -> None:
        """Replace active governed state after one explicit 46D success."""

        if (
            self.last_second_changed_basis_session_adoption is not None
            and result is not self.last_second_changed_basis_session_adoption
        ):
            raise ValueError("A different second changed-basis adoption is already retained.")

        controller = result.controller
        session = controller.presentation
        presentation = session.sequence
        contexts = _snapshot_working_set_contexts(
            presentation,
            session.working_set_contexts,
        )
        if len(contexts) != len(presentation.members):
            raise ValueError(
                "Adopted second changed-basis session must contain one context per declared position."
            )
        if (
            controller.declared_endpoint.verification.edge_record_sha256
            != result.edge_result.persistence.edge_record_sha256
        ):
            raise ValueError(
                "Adopted second changed-basis controller endpoint does not match the exact 46C edge."
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
            "#research-root-backed-cumulative-checkpoint-controls",
            "#research-root-backed-cumulative-checkpoint-success-receipt",
        ):
            matches = list(self.query(selector))
            if len(matches) > 1:
                raise ValueError(
                    f"Second changed-basis adoption found multiple active widgets for {selector}."
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

        self.changed_basis_candidate_items = None
        self.changed_basis_candidate_presentation = None
        self.changed_basis_candidate_controller = None
        self.changed_basis_candidate_endpoint = None

        self.last_second_changed_basis_session_adoption = result

        await self.mount(
            ResearchRevisionEdgeSequenceDetail(
                presentation,
                working_set_contexts=contexts,
            )
        )
        await self.mount(ResearchEndpointRevisionControls())
        await self.mount(ResearchSessionRolloverControls())

    async def _mount_research_rollover(
        self,
        result: ChromiumResearchSessionRolloverResult,
    ) -> None:
        """Use first-root 35E only before 46D; ordinary rollover after adoption."""

        if self.last_second_changed_basis_session_adoption is None:
            await super()._mount_research_rollover(result)
            return
        await ResearchSessionShell._mount_research_rollover(self, result)


def create_second_changed_basis_session_adoption_research_session_shell(
    reentry,
) -> SecondChangedBasisSessionAdoptionResearchSessionShell:
    """Create the concrete second changed-basis product surface through 46D adoption."""

    return SecondChangedBasisSessionAdoptionResearchSessionShell(reentry)


__all__ = [
    "SecondChangedBasisSessionAdoptionResearchSessionShell",
    "create_second_changed_basis_session_adoption_research_session_shell",
]
