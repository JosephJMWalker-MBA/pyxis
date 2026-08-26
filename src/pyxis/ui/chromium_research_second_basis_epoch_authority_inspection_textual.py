from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from textual.widgets import Static

from pyxis.app.chromium_research_second_basis_epoch_continuation_reentry_plan_document import (
    ChromiumResearchSecondBasisEpochContinuationReentryResult,
)
from pyxis.app.chromium_research_second_basis_epoch_reentry import (
    ChromiumResearchSecondBasisEpochReentryResult,
)
from pyxis.app.chromium_research_second_basis_epoch_shell_lineage import (
    ChromiumResearchSecondBasisEpochContinuationShellLineage,
    ChromiumResearchSecondBasisEpochShellLineage,
)
from pyxis.app.chromium_research_session_controller import ChromiumResearchSessionController


@dataclass(frozen=True, slots=True)
class SecondBasisEpochLaunchProvenanceInspection:
    """Immutable read-only launch provenance for one already-proven second-epoch shell."""

    launch_family: str
    launch_location_context: Path | None
    first_root_sha256: str
    second_root_sha256: str
    launch_endpoint_sha256: str


@dataclass(frozen=True, slots=True)
class SecondBasisEpochCurrentGovernedStateInspection:
    """Read-only description of the shell's currently governed visible/typed state."""

    state_kind: str
    state_source: str
    endpoint_sha256: str
    declared_continuation_edge_count: int | None


class SecondBasisEpochAuthorityInspectionPanel(Static):
    """Visible read-only separation between immutable launch provenance and current state.

    The panel performs no file reads, path proof, discovery, mutation, checkpointing,
    or authority promotion. A displayed persisted path is launch location context only.
    """

    def __init__(
        self,
        launch_provenance: SecondBasisEpochLaunchProvenanceInspection,
        current_state: SecondBasisEpochCurrentGovernedStateInspection,
    ) -> None:
        if not isinstance(
            launch_provenance,
            SecondBasisEpochLaunchProvenanceInspection,
        ):
            raise TypeError(
                "launch_provenance must be SecondBasisEpochLaunchProvenanceInspection."
            )
        if not isinstance(
            current_state,
            SecondBasisEpochCurrentGovernedStateInspection,
        ):
            raise TypeError(
                "current_state must be SecondBasisEpochCurrentGovernedStateInspection."
            )
        self.launch_provenance = launch_provenance
        self.current_state = current_state
        super().__init__(
            _render_inspection(launch_provenance, current_state),
            id="research-second-basis-epoch-authority-inspection",
            markup=False,
        )

    @classmethod
    def from_second_basis_epoch_launch(
        cls,
        lineage: ChromiumResearchSecondBasisEpochShellLineage,
    ) -> SecondBasisEpochAuthorityInspectionPanel:
        if not isinstance(lineage, ChromiumResearchSecondBasisEpochShellLineage):
            raise TypeError(
                "lineage must be ChromiumResearchSecondBasisEpochShellLineage."
            )
        reentry = lineage.reentry
        first_root, second_root = _root_shas_from_second_epoch(reentry)
        endpoint = _controller_endpoint_sha(reentry.controller)
        return cls(
            SecondBasisEpochLaunchProvenanceInspection(
                launch_family="persisted 37B second-basis-epoch launch",
                launch_location_context=lineage.overlay_source,
                first_root_sha256=first_root,
                second_root_sha256=second_root,
                launch_endpoint_sha256=endpoint,
            ),
            SecondBasisEpochCurrentGovernedStateInspection(
                state_kind="second-basis-epoch session",
                state_source="persisted 37B launch",
                endpoint_sha256=endpoint,
                declared_continuation_edge_count=None,
            ),
        )

    @classmethod
    def from_continuation_launch(
        cls,
        lineage: ChromiumResearchSecondBasisEpochContinuationShellLineage,
    ) -> SecondBasisEpochAuthorityInspectionPanel:
        if not isinstance(
            lineage,
            ChromiumResearchSecondBasisEpochContinuationShellLineage,
        ):
            raise TypeError(
                "lineage must be ChromiumResearchSecondBasisEpochContinuationShellLineage."
            )
        reentry = lineage.reentry
        first_root, second_root = _root_shas_from_continuation(reentry)
        endpoint = _controller_endpoint_sha(reentry.controller)
        return cls(
            SecondBasisEpochLaunchProvenanceInspection(
                launch_family="persisted 37C/37D continuation launch",
                launch_location_context=lineage.overlay_source,
                first_root_sha256=first_root,
                second_root_sha256=second_root,
                launch_endpoint_sha256=endpoint,
            ),
            _current_from_continuation(
                reentry,
                state_source="persisted 37C/37D launch",
            ),
        )

    @classmethod
    def from_in_process_handoff(
        cls,
        reentry: ChromiumResearchSecondBasisEpochContinuationReentryResult,
    ) -> SecondBasisEpochAuthorityInspectionPanel:
        if not isinstance(
            reentry,
            ChromiumResearchSecondBasisEpochContinuationReentryResult,
        ):
            raise TypeError(
                "reentry must be ChromiumResearchSecondBasisEpochContinuationReentryResult."
            )
        first_root, second_root = _root_shas_from_continuation(reentry)
        endpoint = _controller_endpoint_sha(reentry.controller)
        return cls(
            SecondBasisEpochLaunchProvenanceInspection(
                launch_family="in-process 38F typed continuation handoff",
                launch_location_context=None,
                first_root_sha256=first_root,
                second_root_sha256=second_root,
                launch_endpoint_sha256=endpoint,
            ),
            _current_from_continuation(
                reentry,
                state_source="in-process 38F handoff",
            ),
        )

    def update_current_from_controller(
        self,
        controller: ChromiumResearchSessionController,
        *,
        state_kind: str,
        state_source: str,
    ) -> None:
        """Advance only the visible current-state section from one governed controller."""

        if not isinstance(controller, ChromiumResearchSessionController):
            raise TypeError("controller must be ChromiumResearchSessionController.")
        if not isinstance(state_kind, str) or not state_kind.strip():
            raise TypeError("state_kind must be a non-empty string.")
        if not isinstance(state_source, str) or not state_source.strip():
            raise TypeError("state_source must be a non-empty string.")
        self.current_state = SecondBasisEpochCurrentGovernedStateInspection(
            state_kind=state_kind.strip(),
            state_source=state_source.strip(),
            endpoint_sha256=_controller_endpoint_sha(controller),
            declared_continuation_edge_count=None,
        )
        self.update(_render_inspection(self.launch_provenance, self.current_state))

    def update_current_from_continuation(
        self,
        reentry: ChromiumResearchSecondBasisEpochContinuationReentryResult,
        *,
        state_source: str,
    ) -> None:
        """Advance current typed continuation while requiring launch ancestry to remain fixed."""

        if not isinstance(
            reentry,
            ChromiumResearchSecondBasisEpochContinuationReentryResult,
        ):
            raise TypeError(
                "reentry must be ChromiumResearchSecondBasisEpochContinuationReentryResult."
            )
        if not isinstance(state_source, str) or not state_source.strip():
            raise TypeError("state_source must be a non-empty string.")
        first_root, second_root = _root_shas_from_continuation(reentry)
        if first_root != self.launch_provenance.first_root_sha256:
            raise ValueError(
                "Current continuation first-root identity does not match immutable launch provenance."
            )
        if second_root != self.launch_provenance.second_root_sha256:
            raise ValueError(
                "Current continuation second-root identity does not match immutable launch provenance."
            )
        self.current_state = _current_from_continuation(
            reentry,
            state_source=state_source.strip(),
        )
        self.update(_render_inspection(self.launch_provenance, self.current_state))


def _root_shas_from_second_epoch(
    reentry: ChromiumResearchSecondBasisEpochReentryResult,
) -> tuple[str, str]:
    if not isinstance(reentry, ChromiumResearchSecondBasisEpochReentryResult):
        raise TypeError(
            "reentry must be ChromiumResearchSecondBasisEpochReentryResult."
        )
    first_root = (
        reentry.prior_continuation_reentry.prior_root_backed_reentry
        .loaded_root.verification.root_record_sha256
    )
    second_root = reentry.loaded_root.verification.root_record_sha256
    return first_root, second_root


def _root_shas_from_continuation(
    reentry: ChromiumResearchSecondBasisEpochContinuationReentryResult,
) -> tuple[str, str]:
    if not isinstance(
        reentry,
        ChromiumResearchSecondBasisEpochContinuationReentryResult,
    ):
        raise TypeError(
            "reentry must be ChromiumResearchSecondBasisEpochContinuationReentryResult."
        )
    return _root_shas_from_second_epoch(reentry.prior_second_basis_epoch_reentry)


def _controller_endpoint_sha(controller: ChromiumResearchSessionController) -> str:
    if not isinstance(controller, ChromiumResearchSessionController):
        raise TypeError("controller must be ChromiumResearchSessionController.")
    return controller.declared_endpoint.verification.edge_record_sha256


def _current_from_continuation(
    reentry: ChromiumResearchSecondBasisEpochContinuationReentryResult,
    *,
    state_source: str,
) -> SecondBasisEpochCurrentGovernedStateInspection:
    return SecondBasisEpochCurrentGovernedStateInspection(
        state_kind="typed second-basis-epoch continuation",
        state_source=state_source,
        endpoint_sha256=_controller_endpoint_sha(reentry.controller),
        declared_continuation_edge_count=len(reentry.plan.declared_edge_sources),
    )


def _render_inspection(
    launch: SecondBasisEpochLaunchProvenanceInspection,
    current: SecondBasisEpochCurrentGovernedStateInspection,
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
        "Second-epoch authority inspection\n"
        "\n"
        "Immutable launch provenance\n"
        f"Launch family: {launch.launch_family}\n"
        f"Launch location context only: {launch_location}\n"
        f"First-root SHA-256: {launch.first_root_sha256}\n"
        f"Second-root SHA-256: {launch.second_root_sha256}\n"
        f"Launch endpoint SHA-256: {launch.launch_endpoint_sha256}\n"
        "\n"
        "Current governed state\n"
        f"State kind: {current.state_kind}\n"
        f"State source: {current.state_source}\n"
        f"Current endpoint SHA-256: {current.endpoint_sha256}\n"
        f"Declared continuation edges: {edge_count}\n"
        "\n"
        "Authority notice: a displayed path is launch location context only — not "
        "current/latest/head. SHA-256 values are integrity/record-identity anchors only; "
        "they do not establish authorship, authenticity, trusted time, chronology, "
        "semantic support, or citation authority. This panel is read-only and grants no "
        "mutation, restart, checkpoint, discovery, or path authority."
    )


__all__ = [
    "SecondBasisEpochAuthorityInspectionPanel",
    "SecondBasisEpochCurrentGovernedStateInspection",
    "SecondBasisEpochLaunchProvenanceInspection",
]
