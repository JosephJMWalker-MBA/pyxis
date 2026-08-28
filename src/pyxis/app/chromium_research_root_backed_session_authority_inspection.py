from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .chromium_research_root_backed_session_continuation_reentry_plan_document import (
    ChromiumResearchRootBackedSessionContinuationReentryResult,
)
from .chromium_research_root_backed_session_reentry import (
    ChromiumResearchRootBackedSessionReentryResult,
)
from .chromium_research_root_backed_session_shell_lineage import (
    ChromiumResearchRootBackedSessionContinuationShellLineage,
    ChromiumResearchRootBackedSessionShellLineage,
)
from .chromium_research_session_controller import ChromiumResearchSessionController


_AUTHORITY_NOTICE = (
    "This is read-only authority inspection, not evidence or a control-plane object. "
    "A displayed path is launch location context only, not current/latest/head. "
    "SHA-256 values are integrity/record-identity anchors only; they do not establish "
    "authorship, authenticity, trusted time, chronology, semantic support, or citation "
    "authority. The inspection grants no mutation, restart, checkpoint, discovery, "
    "browser, or path authority."
)


@dataclass(frozen=True, slots=True)
class RootBackedLaunchProvenanceInspection:
    """Immutable read-only launch provenance for already-proven one-root state."""

    launch_family: str
    launch_location_context: Path | None
    root_sha256: str
    launch_endpoint_sha256: str


@dataclass(frozen=True, slots=True)
class RootBackedCurrentGovernedStateInspection:
    """Read-only description of one currently governed one-root state."""

    state_kind: str
    state_source: str
    endpoint_sha256: str
    declared_continuation_edge_count: int | None


@dataclass(frozen=True, slots=True)
class RootBackedAuthorityInspection:
    """UI-independent separation of immutable one-root launch provenance and current state."""

    launch_provenance: RootBackedLaunchProvenanceInspection
    current_state: RootBackedCurrentGovernedStateInspection


def inspect_chromium_research_root_backed_session_launch(
    lineage: ChromiumResearchRootBackedSessionShellLineage,
) -> RootBackedAuthorityInspection:
    """Project one already-proven persisted 35C launch without performing I/O."""

    if not isinstance(lineage, ChromiumResearchRootBackedSessionShellLineage):
        raise TypeError(
            "lineage must be ChromiumResearchRootBackedSessionShellLineage."
        )
    reentry = lineage.reentry
    root = _root_sha_from_root_backed(reentry)
    endpoint = _controller_endpoint_sha(reentry.controller)
    return RootBackedAuthorityInspection(
        launch_provenance=RootBackedLaunchProvenanceInspection(
            launch_family="persisted 35C root-backed launch",
            launch_location_context=lineage.overlay_source,
            root_sha256=root,
            launch_endpoint_sha256=endpoint,
        ),
        current_state=RootBackedCurrentGovernedStateInspection(
            state_kind="root-backed session",
            state_source="persisted 35C launch",
            endpoint_sha256=endpoint,
            declared_continuation_edge_count=None,
        ),
    )


def inspect_chromium_research_root_backed_session_in_process_handoff(
    reentry: ChromiumResearchRootBackedSessionReentryResult,
) -> RootBackedAuthorityInspection:
    """Project one exact in-process 44H handoff without inventing path provenance."""

    if not isinstance(reentry, ChromiumResearchRootBackedSessionReentryResult):
        raise TypeError(
            "reentry must be ChromiumResearchRootBackedSessionReentryResult."
        )
    root = _root_sha_from_root_backed(reentry)
    endpoint = _controller_endpoint_sha(reentry.controller)
    return RootBackedAuthorityInspection(
        launch_provenance=RootBackedLaunchProvenanceInspection(
            launch_family="in-process 44H typed root-backed handoff",
            launch_location_context=None,
            root_sha256=root,
            launch_endpoint_sha256=endpoint,
        ),
        current_state=RootBackedCurrentGovernedStateInspection(
            state_kind="root-backed session",
            state_source="in-process 44H handoff",
            endpoint_sha256=endpoint,
            declared_continuation_edge_count=None,
        ),
    )


def inspect_chromium_research_root_backed_session_continuation_launch(
    lineage: ChromiumResearchRootBackedSessionContinuationShellLineage,
) -> RootBackedAuthorityInspection:
    """Project one already-proven persisted 35D/35E continuation launch."""

    if not isinstance(
        lineage,
        ChromiumResearchRootBackedSessionContinuationShellLineage,
    ):
        raise TypeError(
            "lineage must be ChromiumResearchRootBackedSessionContinuationShellLineage."
        )
    reentry = lineage.reentry
    root = _root_sha_from_continuation(reentry)
    endpoint = _controller_endpoint_sha(reentry.controller)
    return RootBackedAuthorityInspection(
        launch_provenance=RootBackedLaunchProvenanceInspection(
            launch_family="persisted 35D/35E root-backed continuation launch",
            launch_location_context=lineage.overlay_source,
            root_sha256=root,
            launch_endpoint_sha256=endpoint,
        ),
        current_state=_current_from_continuation(
            reentry,
            state_source="persisted 35D/35E launch",
        ),
    )


def inspect_chromium_research_root_backed_session_continuation_in_process_handoff(
    reentry: ChromiumResearchRootBackedSessionContinuationReentryResult,
) -> RootBackedAuthorityInspection:
    """Project one exact in-process 36D handoff without inventing path provenance."""

    if not isinstance(
        reentry,
        ChromiumResearchRootBackedSessionContinuationReentryResult,
    ):
        raise TypeError(
            "reentry must be ChromiumResearchRootBackedSessionContinuationReentryResult."
        )
    root = _root_sha_from_continuation(reentry)
    endpoint = _controller_endpoint_sha(reentry.controller)
    return RootBackedAuthorityInspection(
        launch_provenance=RootBackedLaunchProvenanceInspection(
            launch_family="in-process 36D typed root-backed continuation handoff",
            launch_location_context=None,
            root_sha256=root,
            launch_endpoint_sha256=endpoint,
        ),
        current_state=_current_from_continuation(
            reentry,
            state_source="in-process 36D handoff",
        ),
    )


def advance_chromium_research_root_backed_authority_from_controller(
    inspection: RootBackedAuthorityInspection,
    controller: ChromiumResearchSessionController,
    *,
    state_kind: str,
    state_source: str,
) -> RootBackedAuthorityInspection:
    """Return a new current-state projection while retaining exact launch provenance."""

    _require_inspection(inspection)
    if not isinstance(controller, ChromiumResearchSessionController):
        raise TypeError("controller must be ChromiumResearchSessionController.")
    state_kind = _require_non_empty_string(state_kind, label="state_kind")
    state_source = _require_non_empty_string(state_source, label="state_source")
    return RootBackedAuthorityInspection(
        launch_provenance=inspection.launch_provenance,
        current_state=RootBackedCurrentGovernedStateInspection(
            state_kind=state_kind,
            state_source=state_source,
            endpoint_sha256=_controller_endpoint_sha(controller),
            declared_continuation_edge_count=None,
        ),
    )


def advance_chromium_research_root_backed_authority_from_continuation(
    inspection: RootBackedAuthorityInspection,
    reentry: ChromiumResearchRootBackedSessionContinuationReentryResult,
    *,
    state_source: str,
) -> RootBackedAuthorityInspection:
    """Advance typed continuation state while requiring launch root to stay fixed."""

    _require_inspection(inspection)
    if not isinstance(
        reentry,
        ChromiumResearchRootBackedSessionContinuationReentryResult,
    ):
        raise TypeError(
            "reentry must be ChromiumResearchRootBackedSessionContinuationReentryResult."
        )
    state_source = _require_non_empty_string(state_source, label="state_source")
    root = _root_sha_from_continuation(reentry)
    launch = inspection.launch_provenance
    if root != launch.root_sha256:
        raise ValueError(
            "Current continuation root identity does not match immutable launch provenance."
        )
    return RootBackedAuthorityInspection(
        launch_provenance=launch,
        current_state=_current_from_continuation(
            reentry,
            state_source=state_source,
        ),
    )


def root_backed_authority_notice() -> str:
    """Return the shared negative-authority notice for the Textual inspection panel."""

    return _AUTHORITY_NOTICE


def _root_sha_from_root_backed(
    reentry: ChromiumResearchRootBackedSessionReentryResult,
) -> str:
    if not isinstance(reentry, ChromiumResearchRootBackedSessionReentryResult):
        raise TypeError(
            "reentry must be ChromiumResearchRootBackedSessionReentryResult."
        )
    return reentry.loaded_root.verification.root_record_sha256


def _root_sha_from_continuation(
    reentry: ChromiumResearchRootBackedSessionContinuationReentryResult,
) -> str:
    if not isinstance(
        reentry,
        ChromiumResearchRootBackedSessionContinuationReentryResult,
    ):
        raise TypeError(
            "reentry must be ChromiumResearchRootBackedSessionContinuationReentryResult."
        )
    return _root_sha_from_root_backed(reentry.prior_root_backed_reentry)


def _controller_endpoint_sha(controller: ChromiumResearchSessionController) -> str:
    if not isinstance(controller, ChromiumResearchSessionController):
        raise TypeError("controller must be ChromiumResearchSessionController.")
    return controller.declared_endpoint.verification.edge_record_sha256


def _current_from_continuation(
    reentry: ChromiumResearchRootBackedSessionContinuationReentryResult,
    *,
    state_source: str,
) -> RootBackedCurrentGovernedStateInspection:
    return RootBackedCurrentGovernedStateInspection(
        state_kind="typed root-backed continuation",
        state_source=state_source,
        endpoint_sha256=_controller_endpoint_sha(reentry.controller),
        declared_continuation_edge_count=len(reentry.plan.declared_edge_sources),
    )


def _require_inspection(
    inspection: RootBackedAuthorityInspection,
) -> RootBackedAuthorityInspection:
    if not isinstance(inspection, RootBackedAuthorityInspection):
        raise TypeError("inspection must be RootBackedAuthorityInspection.")
    return inspection


def _require_non_empty_string(value: str, *, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise TypeError(f"{label} must be a non-empty string.")
    return value.strip()


__all__ = [
    "RootBackedAuthorityInspection",
    "RootBackedCurrentGovernedStateInspection",
    "RootBackedLaunchProvenanceInspection",
    "advance_chromium_research_root_backed_authority_from_continuation",
    "advance_chromium_research_root_backed_authority_from_controller",
    "inspect_chromium_research_root_backed_session_continuation_in_process_handoff",
    "inspect_chromium_research_root_backed_session_continuation_launch",
    "inspect_chromium_research_root_backed_session_in_process_handoff",
    "inspect_chromium_research_root_backed_session_launch",
    "root_backed_authority_notice",
]
