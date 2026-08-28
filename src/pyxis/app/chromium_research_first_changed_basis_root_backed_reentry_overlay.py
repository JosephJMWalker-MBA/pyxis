from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .chromium_research_first_changed_basis_root_backed_reentry import (
    ChromiumResearchFirstChangedBasisRootBackedReentryResult,
)
from .chromium_research_root_backed_session_reentry_plan_document import (
    ChromiumResearchRootBackedSessionReentryPlanCheckpointResult,
    persist_chromium_research_root_backed_session_reentry_plan_document,
)


class ChromiumResearchFirstChangedBasisRootBackedReentryOverlayError(ValueError):
    """Raised when exact 44F proof cannot support one explicit 35C overlay write."""


@dataclass(frozen=True, slots=True)
class ChromiumResearchFirstChangedBasisRootBackedReentryOverlayResult:
    """One exact 44F proof persisted as strict 35C restart configuration.

    `verification_result` is the exact successful 44F proof selected for persistence.
    `checkpoint` is public 35C proof-gated persistence evidence. The overlay describes
    that historical verified root-backed session only; it does not claim to represent
    whichever governed controller a UI may currently have mounted.
    """

    verification_result: ChromiumResearchFirstChangedBasisRootBackedReentryResult
    checkpoint: ChromiumResearchRootBackedSessionReentryPlanCheckpointResult


def persist_chromium_research_first_changed_basis_root_backed_reentry_overlay(
    verification_result: ChromiumResearchFirstChangedBasisRootBackedReentryResult,
    *,
    prior_session_plan_source: Path,
    destination: Path,
) -> ChromiumResearchFirstChangedBasisRootBackedReentryOverlayResult:
    """Persist exact 44F fresh proof through the established public 35C boundary.

    Both durable locations remain caller supplied. Public 35C independently decodes
    the ordinary 31B plan document, requires exact prior-plan equality, freshly
    reconstructs the root-backed session, writes the overlay without overwrite, and
    round-trip decodes the persisted document.

    This helper adds only product-level identity checks against the exact 44F proof.
    It does not promote the overlay to active restart authority, replace a controller,
    checkpoint a later continuation, discover files, or infer head/latest state.
    """

    if type(verification_result) is not ChromiumResearchFirstChangedBasisRootBackedReentryResult:
        raise TypeError(
            "verification_result must be exactly "
            "ChromiumResearchFirstChangedBasisRootBackedReentryResult."
        )
    if not isinstance(prior_session_plan_source, Path):
        raise TypeError("prior_session_plan_source must be pathlib.Path.")
    if not isinstance(destination, Path):
        raise TypeError("destination must be pathlib.Path.")

    checkpoint = persist_chromium_research_root_backed_session_reentry_plan_document(
        verification_result.fresh_reentry,
        prior_session_plan_source=prior_session_plan_source,
        destination=destination,
    )

    if checkpoint.reentry is not verification_result.fresh_reentry:
        raise ChromiumResearchFirstChangedBasisRootBackedReentryOverlayError(
            "35C checkpoint did not retain the exact 44F fresh re-entry proof."
        )
    if checkpoint.plan != verification_result.plan:
        raise ChromiumResearchFirstChangedBasisRootBackedReentryOverlayError(
            "35C checkpoint plan does not equal the exact 44F 35B locator plan."
        )
    if (
        checkpoint.fresh_reentry.controller.presentation
        != verification_result.fresh_reentry.controller.presentation
    ):
        raise ChromiumResearchFirstChangedBasisRootBackedReentryOverlayError(
            "35C mandatory fresh proof presents different root-backed research state."
        )
    if (
        checkpoint.fresh_reentry.loaded_root.verification.root_record_sha256
        != verification_result.fresh_reentry.loaded_root.verification.root_record_sha256
    ):
        raise ChromiumResearchFirstChangedBasisRootBackedReentryOverlayError(
            "35C mandatory fresh proof identifies a different 34A root."
        )
    if (
        checkpoint.fresh_reentry.controller.declared_endpoint.verification.edge_record_sha256
        != verification_result.fresh_reentry.controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchFirstChangedBasisRootBackedReentryOverlayError(
            "35C mandatory fresh proof identifies a different declared endpoint."
        )
    if checkpoint.persistence.path != destination.resolve():
        raise ChromiumResearchFirstChangedBasisRootBackedReentryOverlayError(
            "35C persisted overlay path does not equal the explicit requested destination."
        )

    return ChromiumResearchFirstChangedBasisRootBackedReentryOverlayResult(
        verification_result=verification_result,
        checkpoint=checkpoint,
    )


__all__ = [
    "ChromiumResearchFirstChangedBasisRootBackedReentryOverlayError",
    "ChromiumResearchFirstChangedBasisRootBackedReentryOverlayResult",
    "persist_chromium_research_first_changed_basis_root_backed_reentry_overlay",
]
