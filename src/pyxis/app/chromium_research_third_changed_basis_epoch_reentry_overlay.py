from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .chromium_research_third_basis_epoch_reentry_plan_document import (
    ChromiumResearchThirdBasisEpochReentryPlanCheckpointResult,
    load_chromium_research_third_basis_epoch_reentry_plan_document,
    persist_chromium_research_third_basis_epoch_reentry_plan_document,
)
from .chromium_research_third_changed_basis_epoch_reentry import (
    ChromiumResearchThirdChangedBasisEpochReentryResult,
)


class ChromiumResearchThirdChangedBasisEpochReentryOverlayError(ValueError):
    """Raised when exact 47E proof cannot support one explicit 40B overlay write."""


@dataclass(frozen=True, slots=True)
class ChromiumResearchThirdChangedBasisEpochReentryOverlayResult:
    """One exact 47E proof persisted as strict 40B restart configuration.

    `verification_result` is the exact successful historical 47E proof selected for
    persistence. `checkpoint` is public 40B proof-gated persistence evidence. The
    overlay is operational locator configuration for that historical third-basis
    session only; it does not select whichever governed controller may currently be
    mounted and does not mutate launch provenance.
    """

    verification_result: ChromiumResearchThirdChangedBasisEpochReentryResult
    checkpoint: ChromiumResearchThirdBasisEpochReentryPlanCheckpointResult


def persist_chromium_research_third_changed_basis_epoch_reentry_overlay(
    verification_result: ChromiumResearchThirdChangedBasisEpochReentryResult,
    *,
    prior_second_basis_epoch_continuation_overlay_source: Path,
    destination: Path,
) -> ChromiumResearchThirdChangedBasisEpochReentryOverlayResult:
    """Persist exact 47E proof through the established public 40B boundary.

    Both durable locations remain caller supplied. Public 40B rebuilds the candidate
    plan from the explicitly re-supplied current prior-continuation overlay plus the
    earned third-epoch locator layer, freshly reconstructs all three ancestry layers,
    writes without overwrite, and strictly round-trip decodes the new overlay.

    This helper adds only bounded product-level coherence checks. It does not relaunch
    from the overlay, replace mounted state, discover files, backfill launch provenance,
    checkpoint a later continuation, or infer current/latest/head state.
    """

    if type(verification_result) is not ChromiumResearchThirdChangedBasisEpochReentryResult:
        raise TypeError(
            "verification_result must be exactly "
            "ChromiumResearchThirdChangedBasisEpochReentryResult."
        )
    if not isinstance(prior_second_basis_epoch_continuation_overlay_source, Path):
        raise TypeError(
            "prior_second_basis_epoch_continuation_overlay_source must be pathlib.Path."
        )
    if not isinstance(destination, Path):
        raise TypeError("destination must be pathlib.Path.")

    earned = verification_result.fresh_reentry
    checkpoint = persist_chromium_research_third_basis_epoch_reentry_plan_document(
        earned,
        prior_second_basis_epoch_continuation_overlay_source=(
            prior_second_basis_epoch_continuation_overlay_source
        ),
        destination=destination,
    )

    if checkpoint.reentry is not earned:
        raise ChromiumResearchThirdChangedBasisEpochReentryOverlayError(
            "40B checkpoint did not retain the exact 47E fresh 40A proof."
        )

    original_plan = earned.plan
    candidate_plan = checkpoint.plan
    if (
        candidate_plan.prior_second_basis_epoch_continuation_overlay_source
        != prior_second_basis_epoch_continuation_overlay_source.resolve()
    ):
        raise ChromiumResearchThirdChangedBasisEpochReentryOverlayError(
            "40B candidate plan did not retain the explicit current prior second-epoch continuation-overlay source."
        )
    for field_name in (
        "appended_working_set_members",
        "changed_working_set_source",
        "changed_note_source",
        "transition_source",
        "root_source",
        "declared_edge_sources",
        "declaration_source",
    ):
        if getattr(candidate_plan, field_name) != getattr(original_plan, field_name):
            raise ChromiumResearchThirdChangedBasisEpochReentryOverlayError(
                f"40B candidate plan changed earned third-epoch locator field {field_name!r}."
            )

    fresh = checkpoint.fresh_reentry
    earned_prior = earned.prior_second_basis_epoch_continuation_reentry
    fresh_prior = fresh.prior_second_basis_epoch_continuation_reentry
    if fresh_prior.controller.presentation != earned_prior.controller.presentation:
        raise ChromiumResearchThirdChangedBasisEpochReentryOverlayError(
            "40B mandatory fresh proof presents different prior second-epoch continuation state."
        )
    if (
        fresh_prior.controller.declared_endpoint.verification.edge_record_sha256
        != earned_prior.controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchThirdChangedBasisEpochReentryOverlayError(
            "40B mandatory fresh proof identifies a different prior second-epoch continuation endpoint."
        )

    earned_second = earned_prior.prior_second_basis_epoch_reentry
    fresh_second = fresh_prior.prior_second_basis_epoch_reentry
    if (
        fresh_second.prior_continuation_reentry.prior_root_backed_reentry.loaded_root.verification.root_record_sha256
        != earned_second.prior_continuation_reentry.prior_root_backed_reentry.loaded_root.verification.root_record_sha256
    ):
        raise ChromiumResearchThirdChangedBasisEpochReentryOverlayError(
            "40B mandatory fresh proof identifies a different retained first 34A root."
        )
    if (
        fresh_second.loaded_root.verification.root_record_sha256
        != earned_second.loaded_root.verification.root_record_sha256
    ):
        raise ChromiumResearchThirdChangedBasisEpochReentryOverlayError(
            "40B mandatory fresh proof identifies a different retained second 34A root."
        )
    if (
        fresh.loaded_root.verification.root_record_sha256
        != earned.loaded_root.verification.root_record_sha256
    ):
        raise ChromiumResearchThirdChangedBasisEpochReentryOverlayError(
            "40B mandatory fresh proof identifies a different third 34A root."
        )
    if fresh.controller.presentation != earned.controller.presentation:
        raise ChromiumResearchThirdChangedBasisEpochReentryOverlayError(
            "40B mandatory fresh proof presents different third-basis governed state."
        )
    if (
        fresh.controller.declared_endpoint.verification.edge_record_sha256
        != earned.controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchThirdChangedBasisEpochReentryOverlayError(
            "40B mandatory fresh proof identifies a different third-basis endpoint."
        )

    expected_destination = destination.resolve()
    if checkpoint.persistence.path != expected_destination:
        raise ChromiumResearchThirdChangedBasisEpochReentryOverlayError(
            "40B persisted overlay path does not equal the explicit requested destination."
        )
    if load_chromium_research_third_basis_epoch_reentry_plan_document(
        checkpoint.persistence.path
    ) != candidate_plan:
        raise ChromiumResearchThirdChangedBasisEpochReentryOverlayError(
            "40B persisted overlay does not strictly decode to the public candidate plan."
        )

    return ChromiumResearchThirdChangedBasisEpochReentryOverlayResult(
        verification_result=verification_result,
        checkpoint=checkpoint,
    )


__all__ = [
    "ChromiumResearchThirdChangedBasisEpochReentryOverlayError",
    "ChromiumResearchThirdChangedBasisEpochReentryOverlayResult",
    "persist_chromium_research_third_changed_basis_epoch_reentry_overlay",
]
