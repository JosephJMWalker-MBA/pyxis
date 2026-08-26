from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path

from .chromium_research_second_basis_epoch_continuation_reentry_plan_document import (
    ChromiumResearchSecondBasisEpochContinuationReentryResult,
)
from .chromium_research_second_basis_epoch_reentry import (
    ChromiumResearchSecondBasisEpochReentryResult,
)
from .chromium_research_second_basis_epoch_shell_lineage import (
    ChromiumResearchSecondBasisEpochContinuationShellLineage,
    ChromiumResearchSecondBasisEpochShellLineage,
)
from .chromium_research_session_controller import ChromiumResearchSessionController


_INSPECTION_FORMAT = (
    "pyxis.chromium.research_second_basis_epoch_authority_inspection.v1"
)
_AUTHORITY_NOTICE = (
    "This is a read-only inspection report, not evidence or a control-plane object. "
    "A displayed path is launch location context only, not current/latest/head. "
    "SHA-256 values are integrity/record-identity anchors only; they do not establish "
    "authorship, authenticity, trusted time, chronology, semantic support, or citation "
    "authority. The report grants no mutation, restart, checkpoint, discovery, browser, "
    "or path authority."
)


@dataclass(frozen=True, slots=True)
class SecondBasisEpochLaunchProvenanceInspection:
    """Immutable read-only launch provenance for already-proven second-epoch state."""

    launch_family: str
    launch_location_context: Path | None
    first_root_sha256: str
    second_root_sha256: str
    launch_endpoint_sha256: str


@dataclass(frozen=True, slots=True)
class SecondBasisEpochCurrentGovernedStateInspection:
    """Read-only description of one currently governed second-epoch state."""

    state_kind: str
    state_source: str
    endpoint_sha256: str
    declared_continuation_edge_count: int | None


@dataclass(frozen=True, slots=True)
class SecondBasisEpochAuthorityInspection:
    """UI-independent separation of immutable launch provenance from current state."""

    launch_provenance: SecondBasisEpochLaunchProvenanceInspection
    current_state: SecondBasisEpochCurrentGovernedStateInspection


def inspect_chromium_research_second_basis_epoch_launch(
    lineage: ChromiumResearchSecondBasisEpochShellLineage,
) -> SecondBasisEpochAuthorityInspection:
    """Project one already-proven persisted 37B launch without performing any I/O."""

    if not isinstance(lineage, ChromiumResearchSecondBasisEpochShellLineage):
        raise TypeError(
            "lineage must be ChromiumResearchSecondBasisEpochShellLineage."
        )
    reentry = lineage.reentry
    first_root, second_root = _root_shas_from_second_epoch(reentry)
    endpoint = _controller_endpoint_sha(reentry.controller)
    return SecondBasisEpochAuthorityInspection(
        launch_provenance=SecondBasisEpochLaunchProvenanceInspection(
            launch_family="persisted 37B second-basis-epoch launch",
            launch_location_context=lineage.overlay_source,
            first_root_sha256=first_root,
            second_root_sha256=second_root,
            launch_endpoint_sha256=endpoint,
        ),
        current_state=SecondBasisEpochCurrentGovernedStateInspection(
            state_kind="second-basis-epoch session",
            state_source="persisted 37B launch",
            endpoint_sha256=endpoint,
            declared_continuation_edge_count=None,
        ),
    )


def inspect_chromium_research_second_basis_epoch_continuation_launch(
    lineage: ChromiumResearchSecondBasisEpochContinuationShellLineage,
) -> SecondBasisEpochAuthorityInspection:
    """Project one already-proven persisted 37C/37D continuation launch."""

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
    return SecondBasisEpochAuthorityInspection(
        launch_provenance=SecondBasisEpochLaunchProvenanceInspection(
            launch_family="persisted 37C/37D continuation launch",
            launch_location_context=lineage.overlay_source,
            first_root_sha256=first_root,
            second_root_sha256=second_root,
            launch_endpoint_sha256=endpoint,
        ),
        current_state=_current_from_continuation(
            reentry,
            state_source="persisted 37C/37D launch",
        ),
    )


def inspect_chromium_research_second_basis_epoch_in_process_handoff(
    reentry: ChromiumResearchSecondBasisEpochContinuationReentryResult,
) -> SecondBasisEpochAuthorityInspection:
    """Project one exact in-process 38F handoff without inventing path provenance."""

    if not isinstance(
        reentry,
        ChromiumResearchSecondBasisEpochContinuationReentryResult,
    ):
        raise TypeError(
            "reentry must be ChromiumResearchSecondBasisEpochContinuationReentryResult."
        )
    first_root, second_root = _root_shas_from_continuation(reentry)
    endpoint = _controller_endpoint_sha(reentry.controller)
    return SecondBasisEpochAuthorityInspection(
        launch_provenance=SecondBasisEpochLaunchProvenanceInspection(
            launch_family="in-process 38F typed continuation handoff",
            launch_location_context=None,
            first_root_sha256=first_root,
            second_root_sha256=second_root,
            launch_endpoint_sha256=endpoint,
        ),
        current_state=_current_from_continuation(
            reentry,
            state_source="in-process 38F handoff",
        ),
    )


def advance_chromium_research_second_basis_epoch_authority_from_controller(
    inspection: SecondBasisEpochAuthorityInspection,
    controller: ChromiumResearchSessionController,
    *,
    state_kind: str,
    state_source: str,
) -> SecondBasisEpochAuthorityInspection:
    """Return a new current-state projection while retaining exact launch provenance."""

    _require_inspection(inspection)
    if not isinstance(controller, ChromiumResearchSessionController):
        raise TypeError("controller must be ChromiumResearchSessionController.")
    state_kind = _require_non_empty_string(state_kind, label="state_kind")
    state_source = _require_non_empty_string(state_source, label="state_source")
    return SecondBasisEpochAuthorityInspection(
        launch_provenance=inspection.launch_provenance,
        current_state=SecondBasisEpochCurrentGovernedStateInspection(
            state_kind=state_kind,
            state_source=state_source,
            endpoint_sha256=_controller_endpoint_sha(controller),
            declared_continuation_edge_count=None,
        ),
    )


def advance_chromium_research_second_basis_epoch_authority_from_continuation(
    inspection: SecondBasisEpochAuthorityInspection,
    reentry: ChromiumResearchSecondBasisEpochContinuationReentryResult,
    *,
    state_source: str,
) -> SecondBasisEpochAuthorityInspection:
    """Advance typed continuation state while requiring launch ancestry to stay fixed."""

    _require_inspection(inspection)
    if not isinstance(
        reentry,
        ChromiumResearchSecondBasisEpochContinuationReentryResult,
    ):
        raise TypeError(
            "reentry must be ChromiumResearchSecondBasisEpochContinuationReentryResult."
        )
    state_source = _require_non_empty_string(state_source, label="state_source")
    first_root, second_root = _root_shas_from_continuation(reentry)
    launch = inspection.launch_provenance
    if first_root != launch.first_root_sha256:
        raise ValueError(
            "Current continuation first-root identity does not match immutable launch provenance."
        )
    if second_root != launch.second_root_sha256:
        raise ValueError(
            "Current continuation second-root identity does not match immutable launch provenance."
        )
    return SecondBasisEpochAuthorityInspection(
        launch_provenance=launch,
        current_state=_current_from_continuation(
            reentry,
            state_source=state_source,
        ),
    )


def serialize_chromium_research_second_basis_epoch_authority_inspection(
    inspection: SecondBasisEpochAuthorityInspection,
) -> str:
    """Serialize one read-only inspection deterministically as JSON plus newline."""

    _require_inspection(inspection)
    launch = inspection.launch_provenance
    current = inspection.current_state
    document = {
        "authority_notice": _AUTHORITY_NOTICE,
        "current_governed_state": {
            "declared_continuation_edge_count": current.declared_continuation_edge_count,
            "endpoint_sha256": current.endpoint_sha256,
            "state_kind": current.state_kind,
            "state_source": current.state_source,
        },
        "format": _INSPECTION_FORMAT,
        "launch_provenance": {
            "first_root_sha256": launch.first_root_sha256,
            "launch_endpoint_sha256": launch.launch_endpoint_sha256,
            "launch_family": launch.launch_family,
            "launch_location_context_only": (
                None
                if launch.launch_location_context is None
                else str(launch.launch_location_context)
            ),
            "second_root_sha256": launch.second_root_sha256,
        },
        "report_role": "read_only_inspection_not_authority",
    }
    return json.dumps(
        document,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    ) + "\n"


def second_basis_epoch_authority_notice() -> str:
    """Return the shared negative-authority notice for UI and serialized inspection."""

    return _AUTHORITY_NOTICE


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


def _require_inspection(
    inspection: SecondBasisEpochAuthorityInspection,
) -> SecondBasisEpochAuthorityInspection:
    if not isinstance(inspection, SecondBasisEpochAuthorityInspection):
        raise TypeError("inspection must be SecondBasisEpochAuthorityInspection.")
    return inspection


def _require_non_empty_string(value: str, *, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise TypeError(f"{label} must be a non-empty string.")
    return value.strip()


__all__ = [
    "SecondBasisEpochAuthorityInspection",
    "SecondBasisEpochCurrentGovernedStateInspection",
    "SecondBasisEpochLaunchProvenanceInspection",
    "advance_chromium_research_second_basis_epoch_authority_from_continuation",
    "advance_chromium_research_second_basis_epoch_authority_from_controller",
    "inspect_chromium_research_second_basis_epoch_continuation_launch",
    "inspect_chromium_research_second_basis_epoch_in_process_handoff",
    "inspect_chromium_research_second_basis_epoch_launch",
    "second_basis_epoch_authority_notice",
    "serialize_chromium_research_second_basis_epoch_authority_inspection",
]
