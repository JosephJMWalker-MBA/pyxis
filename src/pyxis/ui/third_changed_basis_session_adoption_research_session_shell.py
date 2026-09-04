from __future__ import annotations

from pathlib import Path

from textual.widgets import Button, Input, Static

from pyxis.app.chromium_research_second_basis_epoch_continuation_reentry_plan_document import (
    ChromiumResearchSecondBasisEpochContinuationReentryResult,
)
from pyxis.app.chromium_research_second_basis_epoch_shell_lineage import (
    ChromiumResearchSecondBasisEpochContinuationShellLineage,
)
from pyxis.app.chromium_research_session_rollover import ChromiumResearchSessionRolloverResult
from pyxis.app.chromium_research_third_changed_basis_session_adoption import (
    ChromiumResearchThirdChangedBasisSessionAdoptionResult,
    adopt_chromium_research_third_changed_basis_governed_session,
)

from .chromium_research_endpoint_revision_textual import ResearchEndpointRevisionControls
from .chromium_research_revision_edge_sequence_textual import (
    ResearchRevisionEdgeSequenceDetail,
    _snapshot_working_set_contexts,
)
from .chromium_research_session_rollover_textual import ResearchSessionRolloverControls
from .chromium_research_third_changed_basis_session_adoption_textual import (
    ResearchThirdChangedBasisSessionAdoptionControls,
)
from .research_session_shell import ResearchSessionShell
from .third_changed_basis_root_edge_research_session_shell import (
    InspectableThirdChangedBasisRootEdgeHandoffResearchSessionShell,
    InspectableThirdChangedBasisRootEdgeResearchSessionShell,
    ThirdChangedBasisRootEdgeHandoffResearchSessionShell,
    ThirdChangedBasisRootEdgeResearchSessionShell,
)


_THIRD_CHANGED_BASIS_SESSION_ADOPTION_CSS = """
#research-third-changed-basis-session-adoption-controls {
    width: 94%;
    height: auto;
    padding: 1 2;
    margin-top: 1;
    border: round $warning;
}

#research-third-changed-basis-session-adoption-authority-notice,
#research-third-changed-basis-session-adoption-summary,
#research-third-changed-basis-session-adoption-edge-source-label,
#research-third-changed-basis-session-adoption-declaration-destination-label,
#research-third-changed-basis-session-adoption-status {
    margin-top: 1;
}

#research-third-changed-basis-session-adoption-title,
#research-third-changed-basis-session-adoption-edge-source-label,
#research-third-changed-basis-session-adoption-declaration-destination-label {
    text-style: bold;
}

#adopt-research-third-changed-basis-session {
    margin-top: 1;
}
"""


class _ThirdChangedBasisSessionAdoptionProductMixin:
    """47D-only behavior shared by the four dedicated 47C launch products."""

    last_third_changed_basis_session_adoption: (
        ChromiumResearchThirdChangedBasisSessionAdoptionResult | None
    )

    def __init__(self, authority) -> None:
        super().__init__(authority)
        self.last_third_changed_basis_session_adoption = None

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Own only the 47D action; inherited Textual handlers remain MRO-dispatched."""

        if event.button.id == "adopt-research-third-changed-basis-session":
            event.stop()
            self.call_after_refresh(self._adopt_third_changed_basis_session)

    async def _persist_third_changed_basis_root_edge(self) -> None:
        """Run inherited 47C, then mount 47D only after one new exact success."""

        prior = self.last_third_changed_basis_root_edge
        await super()._persist_third_changed_basis_root_edge()
        edge_result = self.last_third_changed_basis_root_edge
        if edge_result is None or edge_result is prior:
            return
        if len(self.query("#research-third-changed-basis-session-adoption-controls")) != 0:
            raise ValueError(
                "Third changed-basis session-adoption controls are already mounted."
            )
        await self.mount(ResearchThirdChangedBasisSessionAdoptionControls(edge_result))

    async def _adopt_third_changed_basis_session(self) -> None:
        controls = self.query_one(
            "#research-third-changed-basis-session-adoption-controls",
            ResearchThirdChangedBasisSessionAdoptionControls,
        )
        status = self.query_one(
            "#research-third-changed-basis-session-adoption-status",
            Static,
        )
        edge_result = self.last_third_changed_basis_root_edge
        if edge_result is None or controls.edge_result is not edge_result:
            status.update(
                "Adoption failed: no exact successful 47C edge owns this form."
            )
            return

        edge_source = self.query_one(
            "#research-third-changed-basis-session-adoption-edge-source",
            Input,
        )
        declaration_destination = self.query_one(
            "#research-third-changed-basis-session-adoption-declaration-destination",
            Input,
        )
        if not edge_source.value.strip():
            status.update(
                "Adoption failed: explicit current post-third-root edge path is required."
            )
            return
        if not declaration_destination.value.strip():
            status.update(
                "Adoption failed: explicit no-overwrite third-root-backed declaration destination is required."
            )
            return

        prior_controller = self.research_controller
        prior_session = self.research_session
        prior_reentry = self.second_basis_epoch_continuation_reentry
        try:
            result = adopt_chromium_research_third_changed_basis_governed_session(
                edge_result,
                edge_source=Path(edge_source.value),
                declaration_destination=Path(declaration_destination.value),
            )
        except Exception as exc:
            status.update(f"Adoption failed: {exc}")
            return

        if result.edge_result is not edge_result:
            raise ValueError(
                "Third changed-basis adoption did not retain the exact successful 47C edge."
            )
        if (
            self.research_controller is not prior_controller
            or self.research_session is not prior_session
            or self.second_basis_epoch_continuation_reentry is not prior_reentry
        ):
            raise ValueError(
                "Mounted second-epoch continuation changed during 47D declaration construction."
            )

        controls.lock_after_success(result)
        await self._promote_third_changed_basis_session_adoption(result)

    async def _promote_third_changed_basis_session_adoption(
        self,
        result: ChromiumResearchThirdChangedBasisSessionAdoptionResult,
    ) -> None:
        """Replace active governed state after one explicit 47D success."""

        if (
            self.last_third_changed_basis_session_adoption is not None
            and result is not self.last_third_changed_basis_session_adoption
        ):
            raise ValueError(
                "A different third changed-basis adoption is already retained."
            )

        controller = result.controller
        session = controller.presentation
        presentation = session.sequence
        contexts = _snapshot_working_set_contexts(
            presentation,
            session.working_set_contexts,
        )
        if len(contexts) != len(presentation.members):
            raise ValueError(
                "Adopted third changed-basis session must contain one context per declared position."
            )
        if (
            controller.declared_endpoint.verification.edge_record_sha256
            != result.edge_result.persistence.edge_record_sha256
        ):
            raise ValueError(
                "Adopted third changed-basis controller endpoint does not match the exact 47C edge."
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
            "#research-second-basis-epoch-continuation-checkpoint-controls",
            "#research-second-basis-epoch-cumulative-checkpoint-controls",
            "#research-second-basis-epoch-cumulative-checkpoint-success-receipt",
        ):
            matches = list(self.query(selector))
            if len(matches) > 1:
                raise ValueError(
                    f"Third changed-basis adoption found multiple active widgets for {selector}."
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

        self.last_third_changed_basis_session_adoption = result

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
        """Use second-epoch checkpoint behavior only before 47D adoption."""

        if self.last_third_changed_basis_session_adoption is None:
            await super()._mount_research_rollover(result)
            return
        await ResearchSessionShell._mount_research_rollover(self, result)


class ThirdChangedBasisSessionAdoptionResearchSessionShell(
    _ThirdChangedBasisSessionAdoptionProductMixin,
    ThirdChangedBasisRootEdgeResearchSessionShell,
):
    """47D adoption product from a persisted second-epoch continuation launch."""

    CSS = (
        ThirdChangedBasisRootEdgeResearchSessionShell.CSS
        + _THIRD_CHANGED_BASIS_SESSION_ADOPTION_CSS
    )


class ThirdChangedBasisSessionAdoptionHandoffResearchSessionShell(
    _ThirdChangedBasisSessionAdoptionProductMixin,
    ThirdChangedBasisRootEdgeHandoffResearchSessionShell,
):
    """47D adoption product from an exact pathless 38F second-epoch handoff."""

    CSS = (
        ThirdChangedBasisRootEdgeHandoffResearchSessionShell.CSS
        + _THIRD_CHANGED_BASIS_SESSION_ADOPTION_CSS
    )


class InspectableThirdChangedBasisSessionAdoptionResearchSessionShell(
    _ThirdChangedBasisSessionAdoptionProductMixin,
    InspectableThirdChangedBasisRootEdgeResearchSessionShell,
):
    """Inspectable persisted-launch 47D product preserving immutable launch provenance."""

    CSS = (
        InspectableThirdChangedBasisRootEdgeResearchSessionShell.CSS
        + _THIRD_CHANGED_BASIS_SESSION_ADOPTION_CSS
    )

    async def _promote_third_changed_basis_session_adoption(
        self,
        result: ChromiumResearchThirdChangedBasisSessionAdoptionResult,
    ) -> None:
        launch = self.second_basis_epoch_authority_inspection.launch_provenance
        await super()._promote_third_changed_basis_session_adoption(result)
        if self.second_basis_epoch_authority_inspection.launch_provenance is not launch:
            raise ValueError(
                "47D adoption must not replace immutable persisted second-epoch launch provenance."
            )
        self.second_basis_epoch_authority_inspection.update_current_from_controller(
            self.research_controller,
            state_kind="adopted third changed-basis governed session",
            state_source="explicit 47D third changed-basis adoption",
        )

    async def _mount_research_rollover(
        self,
        result: ChromiumResearchSessionRolloverResult,
    ) -> None:
        launch = self.second_basis_epoch_authority_inspection.launch_provenance
        adoption = self.last_third_changed_basis_session_adoption
        await super()._mount_research_rollover(result)
        if self.second_basis_epoch_authority_inspection.launch_provenance is not launch:
            raise ValueError(
                "Post-47D rollover must not replace immutable persisted second-epoch launch provenance."
            )
        if adoption is not None:
            self.second_basis_epoch_authority_inspection.update_current_from_controller(
                self.research_controller,
                state_kind="visible continuation after third changed-basis adoption",
                state_source="explicit rollover after 47D third changed-basis adoption",
            )


class InspectableThirdChangedBasisSessionAdoptionHandoffResearchSessionShell(
    _ThirdChangedBasisSessionAdoptionProductMixin,
    InspectableThirdChangedBasisRootEdgeHandoffResearchSessionShell,
):
    """Inspectable pathless 47D product preserving immutable 38F launch provenance."""

    CSS = (
        InspectableThirdChangedBasisRootEdgeHandoffResearchSessionShell.CSS
        + _THIRD_CHANGED_BASIS_SESSION_ADOPTION_CSS
    )

    async def _promote_third_changed_basis_session_adoption(
        self,
        result: ChromiumResearchThirdChangedBasisSessionAdoptionResult,
    ) -> None:
        launch = self.second_basis_epoch_authority_inspection.launch_provenance
        await super()._promote_third_changed_basis_session_adoption(result)
        if self.second_basis_epoch_authority_inspection.launch_provenance is not launch:
            raise ValueError(
                "47D adoption must not replace immutable raw 38F launch provenance."
            )
        self.second_basis_epoch_authority_inspection.update_current_from_controller(
            self.research_controller,
            state_kind="adopted third changed-basis governed session",
            state_source=(
                "explicit 47D third changed-basis adoption after in-process 38F handoff"
            ),
        )

    async def _mount_research_rollover(
        self,
        result: ChromiumResearchSessionRolloverResult,
    ) -> None:
        launch = self.second_basis_epoch_authority_inspection.launch_provenance
        adoption = self.last_third_changed_basis_session_adoption
        await super()._mount_research_rollover(result)
        if self.second_basis_epoch_authority_inspection.launch_provenance is not launch:
            raise ValueError(
                "Post-47D rollover must not replace immutable raw 38F launch provenance."
            )
        if adoption is not None:
            self.second_basis_epoch_authority_inspection.update_current_from_controller(
                self.research_controller,
                state_kind="visible continuation after third changed-basis adoption",
                state_source=(
                    "explicit rollover after 47D adoption from in-process 38F handoff"
                ),
            )


def create_third_changed_basis_session_adoption_research_session_shell(
    lineage: ChromiumResearchSecondBasisEpochContinuationShellLineage,
) -> ThirdChangedBasisSessionAdoptionResearchSessionShell:
    if not isinstance(lineage, ChromiumResearchSecondBasisEpochContinuationShellLineage):
        raise TypeError(
            "lineage must be ChromiumResearchSecondBasisEpochContinuationShellLineage."
        )
    return ThirdChangedBasisSessionAdoptionResearchSessionShell(lineage)


def create_third_changed_basis_session_adoption_handoff_research_session_shell(
    reentry: ChromiumResearchSecondBasisEpochContinuationReentryResult,
) -> ThirdChangedBasisSessionAdoptionHandoffResearchSessionShell:
    if type(reentry) is not ChromiumResearchSecondBasisEpochContinuationReentryResult:
        raise TypeError(
            "reentry must be exactly ChromiumResearchSecondBasisEpochContinuationReentryResult."
        )
    return ThirdChangedBasisSessionAdoptionHandoffResearchSessionShell(reentry)


def create_inspectable_third_changed_basis_session_adoption_research_session_shell(
    lineage: ChromiumResearchSecondBasisEpochContinuationShellLineage,
) -> InspectableThirdChangedBasisSessionAdoptionResearchSessionShell:
    if not isinstance(lineage, ChromiumResearchSecondBasisEpochContinuationShellLineage):
        raise TypeError(
            "lineage must be ChromiumResearchSecondBasisEpochContinuationShellLineage."
        )
    return InspectableThirdChangedBasisSessionAdoptionResearchSessionShell(lineage)


def create_inspectable_third_changed_basis_session_adoption_handoff_research_session_shell(
    reentry: ChromiumResearchSecondBasisEpochContinuationReentryResult,
) -> InspectableThirdChangedBasisSessionAdoptionHandoffResearchSessionShell:
    if type(reentry) is not ChromiumResearchSecondBasisEpochContinuationReentryResult:
        raise TypeError(
            "reentry must be exactly ChromiumResearchSecondBasisEpochContinuationReentryResult."
        )
    return InspectableThirdChangedBasisSessionAdoptionHandoffResearchSessionShell(reentry)


__all__ = [
    "InspectableThirdChangedBasisSessionAdoptionHandoffResearchSessionShell",
    "InspectableThirdChangedBasisSessionAdoptionResearchSessionShell",
    "ThirdChangedBasisSessionAdoptionHandoffResearchSessionShell",
    "ThirdChangedBasisSessionAdoptionResearchSessionShell",
    "create_inspectable_third_changed_basis_session_adoption_handoff_research_session_shell",
    "create_inspectable_third_changed_basis_session_adoption_research_session_shell",
    "create_third_changed_basis_session_adoption_handoff_research_session_shell",
    "create_third_changed_basis_session_adoption_research_session_shell",
]
