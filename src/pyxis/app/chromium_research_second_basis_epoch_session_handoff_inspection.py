from __future__ import annotations

from .chromium_research_second_basis_epoch_authority_inspection import (
    SecondBasisEpochAuthorityInspection,
    SecondBasisEpochCurrentGovernedStateInspection,
    SecondBasisEpochLaunchProvenanceInspection,
)
from .chromium_research_second_basis_epoch_reentry import (
    ChromiumResearchSecondBasisEpochReentryResult,
)


def inspect_chromium_research_second_basis_epoch_session_in_process_handoff(
    reentry: ChromiumResearchSecondBasisEpochReentryResult,
) -> SecondBasisEpochAuthorityInspection:
    """Project one exact initial 46G handoff without inventing path provenance.

    The re-entry has already been freshly earned by public 37B during 46F. This helper
    performs no file I/O, reconstruction, persistence, discovery, checkpointing, or
    authority promotion. It only projects immutable launch provenance and the initial
    current governed state for read-only inspection.
    """

    if type(reentry) is not ChromiumResearchSecondBasisEpochReentryResult:
        raise TypeError(
            "reentry must be exactly ChromiumResearchSecondBasisEpochReentryResult."
        )

    first_root = (
        reentry.prior_continuation_reentry.prior_root_backed_reentry
        .loaded_root.verification.root_record_sha256
    )
    second_root = reentry.loaded_root.verification.root_record_sha256
    endpoint = reentry.controller.declared_endpoint.verification.edge_record_sha256

    return SecondBasisEpochAuthorityInspection(
        launch_provenance=SecondBasisEpochLaunchProvenanceInspection(
            launch_family="in-process 46G typed second-basis-epoch handoff",
            launch_location_context=None,
            first_root_sha256=first_root,
            second_root_sha256=second_root,
            launch_endpoint_sha256=endpoint,
        ),
        current_state=SecondBasisEpochCurrentGovernedStateInspection(
            state_kind="second-basis-epoch session",
            state_source="in-process 46G handoff",
            endpoint_sha256=endpoint,
            declared_continuation_edge_count=None,
        ),
    )


__all__ = [
    "inspect_chromium_research_second_basis_epoch_session_in_process_handoff",
]
