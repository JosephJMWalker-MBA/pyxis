from __future__ import annotations

from textual.widgets import Static

from pyxis.app.chromium_research_session_controller import ChromiumResearchSessionController
from pyxis.app.chromium_research_third_basis_epoch_authority_inspection import (
    ThirdBasisEpochAuthorityInspection,
    ThirdBasisEpochCurrentGovernedStateInspection,
    ThirdBasisEpochLaunchProvenanceInspection,
    advance_chromium_research_third_basis_epoch_authority_from_continuation,
    advance_chromium_research_third_basis_epoch_authority_from_controller,
    inspect_chromium_research_third_basis_epoch_continuation_launch,
    inspect_chromium_research_third_basis_epoch_in_process_handoff,
    inspect_chromium_research_third_basis_epoch_launch,
    third_basis_epoch_authority_notice,
)
from pyxis.app.chromium_research_third_basis_epoch_continuation_reentry_plan_document import (
    ChromiumResearchThirdBasisEpochContinuationReentryResult,
)
from pyxis.app.chromium_research_third_basis_epoch_shell_lineage import (
    ChromiumResearchThirdBasisEpochContinuationShellLineage,
    ChromiumResearchThirdBasisEpochShellLineage,
)


class ThirdBasisEpochAuthorityInspectionPanel(Static):
    """Textual renderer over one UI-independent, already-proven authority projection."""

    def __init__(
        self,
        launch_provenance: ThirdBasisEpochLaunchProvenanceInspection,
        current_state: ThirdBasisEpochCurrentGovernedStateInspection,
    ) -> None:
        if not isinstance(
            launch_provenance,
            ThirdBasisEpochLaunchProvenanceInspection,
        ):
            raise TypeError(
                "launch_provenance must be ThirdBasisEpochLaunchProvenanceInspection."
            )
        if not isinstance(
            current_state,
            ThirdBasisEpochCurrentGovernedStateInspection,
        ):
            raise TypeError(
                "current_state must be ThirdBasisEpochCurrentGovernedStateInspection."
            )
        self.authority_projection = ThirdBasisEpochAuthorityInspection(
            launch_provenance=launch_provenance,
            current_state=current_state,
        )
        self.launch_provenance = self.authority_projection.launch_provenance
        self.current_state = self.authority_projection.current_state
        super().__init__(
            _render_inspection(self.launch_provenance, self.current_state),
            id="research-third-basis-epoch-authority-inspection",
            markup=False,
        )

    @classmethod
    def from_third_basis_epoch_launch(
        cls,
        lineage: ChromiumResearchThirdBasisEpochShellLineage,
    ) -> ThirdBasisEpochAuthorityInspectionPanel:
        inspection = inspect_chromium_research_third_basis_epoch_launch(lineage)
        return cls(inspection.launch_provenance, inspection.current_state)

    @classmethod
    def from_continuation_launch(
        cls,
        lineage: ChromiumResearchThirdBasisEpochContinuationShellLineage,
    ) -> ThirdBasisEpochAuthorityInspectionPanel:
        inspection = inspect_chromium_research_third_basis_epoch_continuation_launch(
            lineage
        )
        return cls(inspection.launch_provenance, inspection.current_state)

    @classmethod
    def from_in_process_handoff(
        cls,
        reentry: ChromiumResearchThirdBasisEpochContinuationReentryResult,
    ) -> ThirdBasisEpochAuthorityInspectionPanel:
        inspection = inspect_chromium_research_third_basis_epoch_in_process_handoff(reentry)
        return cls(inspection.launch_provenance, inspection.current_state)

    def update_current_from_controller(
        self,
        controller: ChromiumResearchSessionController,
        *,
        state_kind: str,
        state_source: str,
    ) -> None:
        updated = advance_chromium_research_third_basis_epoch_authority_from_controller(
            self.authority_projection,
            controller,
            state_kind=state_kind,
            state_source=state_source,
        )
        self._apply_updated_projection(updated)

    def update_current_from_continuation(
        self,
        reentry: ChromiumResearchThirdBasisEpochContinuationReentryResult,
        *,
        state_source: str,
    ) -> None:
        updated = (
            advance_chromium_research_third_basis_epoch_authority_from_continuation(
                self.authority_projection,
                reentry,
                state_source=state_source,
            )
        )
        self._apply_updated_projection(updated)

    def _apply_updated_projection(
        self,
        updated: ThirdBasisEpochAuthorityInspection,
    ) -> None:
        if not isinstance(updated, ThirdBasisEpochAuthorityInspection):
            raise TypeError("updated must be ThirdBasisEpochAuthorityInspection.")
        if updated.launch_provenance is not self.launch_provenance:
            raise ValueError(
                "Authority projection update replaced immutable third-epoch launch provenance."
            )
        self.authority_projection = updated
        self.current_state = updated.current_state
        self.update(_render_inspection(self.launch_provenance, self.current_state))


def _render_inspection(
    launch: ThirdBasisEpochLaunchProvenanceInspection,
    current: ThirdBasisEpochCurrentGovernedStateInspection,
) -> str:
    if launch.launch_location_context is None:
        launch_location = "none — exact in-process typed handoff; no persistent launch path"
    else:
        launch_location = str(launch.launch_location_context)
    if current.declared_continuation_edge_count is None:
        edge_count = "not represented as a typed continuation"
    else:
        edge_count = str(current.declared_continuation_edge_count)

    return (
        "Third-epoch authority inspection\n"
        "\n"
        "Immutable launch provenance\n"
        f"Launch family: {launch.launch_family}\n"
        f"Launch location context only: {launch_location}\n"
        f"First-root SHA-256: {launch.first_root_sha256}\n"
        f"Second-root SHA-256: {launch.second_root_sha256}\n"
        f"Third-root SHA-256: {launch.third_root_sha256}\n"
        f"Launch endpoint SHA-256: {launch.launch_endpoint_sha256}\n"
        "\n"
        "Current governed state\n"
        f"State kind: {current.state_kind}\n"
        f"State source: {current.state_source}\n"
        f"Current endpoint SHA-256: {current.endpoint_sha256}\n"
        f"Declared continuation edges: {edge_count}\n"
        "\n"
        f"Authority notice: {third_basis_epoch_authority_notice()}"
    )


__all__ = [
    "ThirdBasisEpochAuthorityInspectionPanel",
    "ThirdBasisEpochCurrentGovernedStateInspection",
    "ThirdBasisEpochLaunchProvenanceInspection",
]
