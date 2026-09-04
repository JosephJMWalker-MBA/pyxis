from __future__ import annotations

from .chromium_research_third_basis_epoch_authority_inspection import (
    ThirdBasisEpochAuthorityInspection,
    ThirdBasisEpochCurrentGovernedStateInspection,
    ThirdBasisEpochLaunchProvenanceInspection,
)
from .chromium_research_third_basis_epoch_reentry import (
    ChromiumResearchThirdBasisEpochReentryResult,
)


def inspect_chromium_research_third_basis_epoch_session_in_process_handoff(
    reentry: ChromiumResearchThirdBasisEpochReentryResult,
) -> ThirdBasisEpochAuthorityInspection:
    """Project one exact initial 47G handoff without inventing path provenance.

    The re-entry has already been freshly earned by public 40B during 47F. This helper
    performs no file I/O, reconstruction, persistence, discovery, checkpointing, or
    authority promotion. It only projects immutable launch provenance and the initial
    current governed state for read-only inspection.
    """

    if type(reentry) is not ChromiumResearchThirdBasisEpochReentryResult:
        raise TypeError(
            "reentry must be exactly ChromiumResearchThirdBasisEpochReentryResult."
        )

    second_epoch = (
        reentry.prior_second_basis_epoch_continuation_reentry
        .prior_second_basis_epoch_reentry
    )
    first_root = (
        second_epoch.prior_continuation_reentry.prior_root_backed_reentry
        .loaded_root.verification.root_record_sha256
    )
    second_root = second_epoch.loaded_root.verification.root_record_sha256
    third_root = reentry.loaded_root.verification.root_record_sha256
    endpoint = reentry.controller.declared_endpoint.verification.edge_record_sha256

    return ThirdBasisEpochAuthorityInspection(
        launch_provenance=ThirdBasisEpochLaunchProvenanceInspection(
            launch_family="in-process 47G typed third-basis-epoch handoff",
            launch_location_context=None,
            first_root_sha256=first_root,
            second_root_sha256=second_root,
            third_root_sha256=third_root,
            launch_endpoint_sha256=endpoint,
        ),
        current_state=ThirdBasisEpochCurrentGovernedStateInspection(
            state_kind="third-basis-epoch session",
            state_source="in-process 47G handoff",
            endpoint_sha256=endpoint,
            declared_continuation_edge_count=None,
        ),
    )


__all__ = [
    "inspect_chromium_research_third_basis_epoch_session_in_process_handoff",
]
