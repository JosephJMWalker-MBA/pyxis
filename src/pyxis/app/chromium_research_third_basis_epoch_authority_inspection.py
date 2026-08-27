from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .chromium_research_session_controller import ChromiumResearchSessionController
from .chromium_research_third_basis_epoch_continuation_reentry_plan_document import (
    ChromiumResearchThirdBasisEpochContinuationReentryResult,
)
from .chromium_research_third_basis_epoch_reentry import (
    ChromiumResearchThirdBasisEpochReentryResult,
)
from .chromium_research_third_basis_epoch_shell_lineage import (
    ChromiumResearchThirdBasisEpochContinuationShellLineage,
    ChromiumResearchThirdBasisEpochShellLineage,
)


_AUTHORITY_NOTICE = (
    "This is a read-only inspection projection, not evidence or a control-plane object. "
    "A displayed path is launch location context only, not current/latest/head. "
    "SHA-256 values are integrity/record-identity anchors only; they do not establish "
    "authorship, authenticity, trusted time, chronology, semantic support, or citation "
    "authority. The projection grants no mutation, restart, checkpoint, discovery, browser, "
    "or path authority."
)


@dataclass(frozen=True, slots=True)
class ThirdBasisEpochLaunchProvenanceInspection:
    """Immutable read-only launch provenance for already-proven third-epoch state."""

    launch_family: str
    launch_location_context: Path | None
    first_root_sha256: str
    second_root_sha256: str
    third_root_sha256: str
    launch_endpoint_sha256: str


@dataclass(frozen=True, slots=True)
class ThirdBasisEpochCurrentGovernedStateInspection:
    """Read-only description of one currently governed third-epoch state."""

    state_kind: str
    state_source: str
    endpoint_sha256: str
    declared_continuation_edge_count: int | None


@dataclass(frozen=True, slots=True)
class ThirdBasisEpochAuthorityInspection:
    """UI-independent separation of immutable launch provenance from current state."""

    launch_provenance: ThirdBasisEpochLaunchProvenanceInspection
    current_state: ThirdBasisEpochCurrentGovernedStateInspection


def inspect_chromium_research_third_basis_epoch_launch(
    lineage: ChromiumResearchThirdBasisEpochShellLineage,
) -> ThirdBasisEpochAuthorityInspection:
    """Project one already-proven persisted 40B launch without performing I/O."""

    if not isinstance(lineage, ChromiumResearchThirdBasisEpochShellLineage):
        raise TypeError(
            "lineage must be ChromiumResearchThirdBasisEpochShellLineage."
        )
    reentry = lineage.reentry
    first_root, second_root, third_root = _root_shas_from_third_epoch(reentry)
    endpoint = _controller_endpoint_sha(reentry.controller)
    return ThirdBasisEpochAuthorityInspection(
        launch_provenance=ThirdBasisEpochLaunchProvenanceInspection(
            launch_family="persisted 40B third-basis-epoch launch",
            launch_location_context=lineage.overlay_source,
            first_root_sha256=first_root,
            second_root_sha256=second_root,
            third_root_sha256=third_root,
            launch_endpoint_sha256=endpoint,
        ),
        current_state=ThirdBasisEpochCurrentGovernedStateInspection(
            state_kind="third-basis-epoch session",
            state_source="persisted 40B launch",
            endpoint_sha256=endpoint,
            declared_continuation_edge_count=None,
        ),
    )


def inspect_chromium_research_third_basis_epoch_continuation_launch(
    lineage: ChromiumResearchThirdBasisEpochContinuationShellLineage,
) -> ThirdBasisEpochAuthorityInspection:
    """Project one already-proven persisted 40C/40D continuation launch."""

    if not isinstance(
        lineage,
        ChromiumResearchThirdBasisEpochContinuationShellLineage,
    ):
        raise TypeError(
            "lineage must be ChromiumResearchThirdBasisEpochContinuationShellLineage."
        )
    reentry = lineage.reentry
    first_root, second_root, third_root = _root_shas_from_continuation(reentry)
    endpoint = _controller_endpoint_sha(reentry.controller)
    return ThirdBasisEpochAuthorityInspection(
        launch_provenance=ThirdBasisEpochLaunchProvenanceInspection(
            launch_family="persisted 40C/40D continuation launch",
            launch_location_context=lineage.overlay_source,
            first_root_sha256=first_root,
            second_root_sha256=second_root,
            third_root_sha256=third_root,
            launch_endpoint_sha256=endpoint,
        ),
        current_state=_current_from_continuation(
            reentry,
            state_source="persisted 40C/40D launch",
        ),
    )


def inspect_chromium_research_third_basis_epoch_in_process_handoff(
    reentry: ChromiumResearchThirdBasisEpochContinuationReentryResult,
) -> ThirdBasisEpochAuthorityInspection:
    """Project one exact in-process 41E handoff without inventing path provenance."""

    if not isinstance(
        reentry,
        ChromiumResearchThirdBasisEpochContinuationReentryResult,
    ):
        raise TypeError(
            "reentry must be ChromiumResearchThirdBasisEpochContinuationReentryResult."
        )
    first_root, second_root, third_root = _root_shas_from_continuation(reentry)
    endpoint = _controller_endpoint_sha(reentry.controller)
    return ThirdBasisEpochAuthorityInspection(
        launch_provenance=ThirdBasisEpochLaunchProvenanceInspection(
            launch_family="in-process 41E typed continuation handoff",
            launch_location_context=None,
            first_root_sha256=first_root,
            second_root_sha256=second_root,
            third_root_sha256=third_root,
            launch_endpoint_sha256=endpoint,
        ),
        current_state=_current_from_continuation(
            reentry,
            state_source="in-process 41E handoff",
        ),
    )


def advance_chromium_research_third_basis_epoch_authority_from_controller(
    inspection: ThirdBasisEpochAuthorityInspection,
    controller: ChromiumResearchSessionController,
    *,
    state_kind: str,
    state_source: str,
) -> ThirdBasisEpochAuthorityInspection:
    """Return a new current-state projection while retaining exact launch provenance."""

    _require_inspection(inspection)
    if not isinstance(controller, ChromiumResearchSessionController):
        raise TypeError("controller must be ChromiumResearchSessionController.")
    state_kind = _require_non_empty_string(state_kind, label="state_kind")
    state_source = _require_non_empty_string(state_source, label="state_source")
    return ThirdBasisEpochAuthorityInspection(
        launch_provenance=inspection.launch_provenance,
        current_state=ThirdBasisEpochCurrentGovernedStateInspection(
            state_kind=state_kind,
            state_source=state_source,
            endpoint_sha256=_controller_endpoint_sha(controller),
            declared_continuation_edge_count=None,
        ),
    )


def advance_chromium_research_third_basis_epoch_authority_from_continuation(
    inspection: ThirdBasisEpochAuthorityInspection,
    reentry: ChromiumResearchThirdBasisEpochContinuationReentryResult,
    *,
    state_source: str,
) -> ThirdBasisEpochAuthorityInspection:
    """Advance typed continuation while requiring all three launch roots to stay fixed."""

    _require_inspection(inspection)
    if not isinstance(
        reentry,
        ChromiumResearchThirdBasisEpochContinuationReentryResult,
    ):
        raise TypeError(
            "reentry must be ChromiumResearchThirdBasisEpochContinuationReentryResult."
        )
    state_source = _require_non_empty_string(state_source, label="state_source")
    first_root, second_root, third_root = _root_shas_from_continuation(reentry)
    launch = inspection.launch_provenance
    if first_root != launch.first_root_sha256:
        raise ValueError(
            "Current continuation first-root identity does not match immutable launch provenance."
        )
    if second_root != launch.second_root_sha256:
        raise ValueError(
            "Current continuation second-root identity does not match immutable launch provenance."
        )
    if third_root != launch.third_root_sha256:
        raise ValueError(
            "Current continuation third-root identity does not match immutable launch provenance."
        )
    return ThirdBasisEpochAuthorityInspection(
        launch_provenance=launch,
        current_state=_current_from_continuation(
            reentry,
            state_source=state_source,
        ),
    )


def third_basis_epoch_authority_notice() -> str:
    """Return the shared negative-authority notice for visible third-epoch inspection."""

    return _AUTHORITY_NOTICE


def _root_shas_from_third_epoch(
    reentry: ChromiumResearchThirdBasisEpochReentryResult,
) -> tuple[str, str, str]:
    if not isinstance(reentry, ChromiumResearchThirdBasisEpochReentryResult):
        raise TypeError(
            "reentry must be ChromiumResearchThirdBasisEpochReentryResult."
        )
    second_epoch = (
        reentry.prior_second_basis_epoch_continuation_reentry
        .prior_second_basis_epoch_reentry
    )
    first_root = (
        second_epoch.prior_continuation_reentry.prior_root_backed_reentry.loaded_root
        .verification.root_record_sha256
    )
    second_root = second_epoch.loaded_root.verification.root_record_sha256
    third_root = reentry.loaded_root.verification.root_record_sha256
    return first_root, second_root, third_root


def _root_shas_from_continuation(
    reentry: ChromiumResearchThirdBasisEpochContinuationReentryResult,
) -> tuple[str, str, str]:
    if not isinstance(
        reentry,
        ChromiumResearchThirdBasisEpochContinuationReentryResult,
    ):
        raise TypeError(
            "reentry must be ChromiumResearchThirdBasisEpochContinuationReentryResult."
        )
    return _root_shas_from_third_epoch(reentry.prior_third_basis_epoch_reentry)


def _controller_endpoint_sha(controller: ChromiumResearchSessionController) -> str:
    if not isinstance(controller, ChromiumResearchSessionController):
        raise TypeError("controller must be ChromiumResearchSessionController.")
    return controller.declared_endpoint.verification.edge_record_sha256


def _current_from_continuation(
    reentry: ChromiumResearchThirdBasisEpochContinuationReentryResult,
    *,
    state_source: str,
) -> ThirdBasisEpochCurrentGovernedStateInspection:
    return ThirdBasisEpochCurrentGovernedStateInspection(
        state_kind="typed third-basis-epoch continuation",
        state_source=state_source,
        endpoint_sha256=_controller_endpoint_sha(reentry.controller),
        declared_continuation_edge_count=len(reentry.plan.declared_edge_sources),
    )


def _require_inspection(
    inspection: ThirdBasisEpochAuthorityInspection,
) -> ThirdBasisEpochAuthorityInspection:
    if not isinstance(inspection, ThirdBasisEpochAuthorityInspection):
        raise TypeError("inspection must be ThirdBasisEpochAuthorityInspection.")
    return inspection


def _require_non_empty_string(value: str, *, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise TypeError(f"{label} must be a non-empty string.")
    return value.strip()


__all__ = [
    "ThirdBasisEpochAuthorityInspection",
    "ThirdBasisEpochCurrentGovernedStateInspection",
    "ThirdBasisEpochLaunchProvenanceInspection",
    "advance_chromium_research_third_basis_epoch_authority_from_continuation",
    "advance_chromium_research_third_basis_epoch_authority_from_controller",
    "inspect_chromium_research_third_basis_epoch_continuation_launch",
    "inspect_chromium_research_third_basis_epoch_in_process_handoff",
    "inspect_chromium_research_third_basis_epoch_launch",
    "third_basis_epoch_authority_notice",
]
