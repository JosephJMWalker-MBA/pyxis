from __future__ import annotations

from textual.widgets import Static

from pyxis.app.chromium_research_root_backed_session_authority_inspection import (
    RootBackedAuthorityInspection,
    RootBackedCurrentGovernedStateInspection,
    RootBackedLaunchProvenanceInspection,
    advance_chromium_research_root_backed_authority_from_continuation,
    advance_chromium_research_root_backed_authority_from_controller,
    inspect_chromium_research_root_backed_session_continuation_in_process_handoff,
    inspect_chromium_research_root_backed_session_continuation_launch,
    inspect_chromium_research_root_backed_session_in_process_handoff,
    inspect_chromium_research_root_backed_session_launch,
    root_backed_authority_notice,
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
from pyxis.app.chromium_research_session_controller import ChromiumResearchSessionController


class RootBackedAuthorityInspectionPanel(Static):
    """Textual renderer over one UI-independent, already-proven one-root projection.

    The panel performs no file reads, path proof, discovery, mutation, checkpointing,
    restart, browser access, or authority promotion. A displayed persisted path is
    launch location context only.
    """

    def __init__(
        self,
        launch_provenance: RootBackedLaunchProvenanceInspection,
        current_state: RootBackedCurrentGovernedStateInspection,
    ) -> None:
        if not isinstance(launch_provenance, RootBackedLaunchProvenanceInspection):
            raise TypeError(
                "launch_provenance must be RootBackedLaunchProvenanceInspection."
            )
        if not isinstance(current_state, RootBackedCurrentGovernedStateInspection):
            raise TypeError(
                "current_state must be RootBackedCurrentGovernedStateInspection."
            )
        self.authority_projection = RootBackedAuthorityInspection(
            launch_provenance=launch_provenance,
            current_state=current_state,
        )
        self.launch_provenance = self.authority_projection.launch_provenance
        self.current_state = self.authority_projection.current_state
        super().__init__(
            _render_inspection(self.launch_provenance, self.current_state),
            id="research-root-backed-authority-inspection",
            markup=False,
        )

    @classmethod
    def from_root_backed_launch(
        cls,
        lineage: ChromiumResearchRootBackedSessionShellLineage,
    ) -> RootBackedAuthorityInspectionPanel:
        inspection = inspect_chromium_research_root_backed_session_launch(lineage)
        return cls(inspection.launch_provenance, inspection.current_state)

    @classmethod
    def from_root_backed_handoff(
        cls,
        reentry: ChromiumResearchRootBackedSessionReentryResult,
    ) -> RootBackedAuthorityInspectionPanel:
        inspection = inspect_chromium_research_root_backed_session_in_process_handoff(
            reentry
        )
        return cls(inspection.launch_provenance, inspection.current_state)

    @classmethod
    def from_continuation_launch(
        cls,
        lineage: ChromiumResearchRootBackedSessionContinuationShellLineage,
    ) -> RootBackedAuthorityInspectionPanel:
        inspection = inspect_chromium_research_root_backed_session_continuation_launch(
            lineage
        )
        return cls(inspection.launch_provenance, inspection.current_state)

    @classmethod
    def from_continuation_handoff(
        cls,
        reentry: ChromiumResearchRootBackedSessionContinuationReentryResult,
    ) -> RootBackedAuthorityInspectionPanel:
        inspection = (
            inspect_chromium_research_root_backed_session_continuation_in_process_handoff(
                reentry
            )
        )
        return cls(inspection.launch_provenance, inspection.current_state)

    def update_current_from_controller(
        self,
        controller: ChromiumResearchSessionController,
        *,
        state_kind: str,
        state_source: str,
    ) -> None:
        updated = advance_chromium_research_root_backed_authority_from_controller(
            self.authority_projection,
            controller,
            state_kind=state_kind,
            state_source=state_source,
        )
        self._apply_updated_projection(updated)

    def update_current_from_continuation(
        self,
        reentry: ChromiumResearchRootBackedSessionContinuationReentryResult,
        *,
        state_source: str,
    ) -> None:
        updated = advance_chromium_research_root_backed_authority_from_continuation(
            self.authority_projection,
            reentry,
            state_source=state_source,
        )
        self._apply_updated_projection(updated)

    def _apply_updated_projection(
        self,
        updated: RootBackedAuthorityInspection,
    ) -> None:
        if not isinstance(updated, RootBackedAuthorityInspection):
            raise TypeError("updated must be RootBackedAuthorityInspection.")
        if updated.launch_provenance is not self.launch_provenance:
            raise ValueError(
                "Authority projection update replaced immutable root-backed launch provenance."
            )
        self.authority_projection = updated
        self.current_state = updated.current_state
        self.update(_render_inspection(self.launch_provenance, self.current_state))


def _render_inspection(
    launch: RootBackedLaunchProvenanceInspection,
    current: RootBackedCurrentGovernedStateInspection,
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
        "Root-backed authority inspection\n"
        "\n"
        "Immutable launch provenance\n"
        f"Launch family: {launch.launch_family}\n"
        f"Launch location context only: {launch_location}\n"
        f"Root SHA-256: {launch.root_sha256}\n"
        f"Launch endpoint SHA-256: {launch.launch_endpoint_sha256}\n"
        "\n"
        "Current governed state\n"
        f"State kind: {current.state_kind}\n"
        f"State source: {current.state_source}\n"
        f"Current endpoint SHA-256: {current.endpoint_sha256}\n"
        f"Declared continuation edges: {edge_count}\n"
        "\n"
        f"Authority notice: {root_backed_authority_notice()}"
    )


__all__ = [
    "RootBackedAuthorityInspectionPanel",
    "RootBackedCurrentGovernedStateInspection",
    "RootBackedLaunchProvenanceInspection",
]
