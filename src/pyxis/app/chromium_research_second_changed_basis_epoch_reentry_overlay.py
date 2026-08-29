from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .chromium_research_second_basis_epoch_reentry_plan_document import (
    ChromiumResearchSecondBasisEpochReentryPlanCheckpointResult,
    load_chromium_research_second_basis_epoch_reentry_plan_document,
    persist_chromium_research_second_basis_epoch_reentry_plan_document,
)
from .chromium_research_second_changed_basis_epoch_reentry import (
    ChromiumResearchSecondChangedBasisEpochReentryResult,
)


class ChromiumResearchSecondChangedBasisEpochReentryOverlayError(ValueError):
    """Raised when exact 46E proof cannot support one explicit 37B overlay write."""


@dataclass(frozen=True, slots=True)
class ChromiumResearchSecondChangedBasisEpochReentryOverlayResult:
    """One exact 46E proof persisted as strict 37B restart configuration.

    `verification_result` is the exact successful historical 46E proof selected for
    persistence. `checkpoint` is public 37B proof-gated persistence evidence. The
    overlay is operational locator configuration for that historical second-basis
    session only; it does not select whichever governed controller may currently be
    mounted and does not mutate launch provenance.
    """

    verification_result: ChromiumResearchSecondChangedBasisEpochReentryResult
    checkpoint: ChromiumResearchSecondBasisEpochReentryPlanCheckpointResult


def persist_chromium_research_second_changed_basis_epoch_reentry_overlay(
    verification_result: ChromiumResearchSecondChangedBasisEpochReentryResult,
    *,
    prior_root_backed_continuation_overlay_source: Path,
    destination: Path,
) -> ChromiumResearchSecondChangedBasisEpochReentryOverlayResult:
    """Persist exact 46E proof through the established public 37B boundary.

    Both durable locations remain caller supplied. Public 37B rebuilds the candidate
    plan from the explicitly re-supplied current prior-continuation overlay plus the
    earned second-epoch locator layer, freshly reconstructs both ancestry layers,
    writes without overwrite, and strictly round-trip decodes the new overlay.

    This helper adds only bounded product-level coherence checks. It does not relaunch
    from the overlay, replace mounted state, discover files, backfill launch provenance,
    checkpoint a later continuation, or infer current/latest/head state.
    """

    if type(verification_result) is not ChromiumResearchSecondChangedBasisEpochReentryResult:
        raise TypeError(
            "verification_result must be exactly "
            "ChromiumResearchSecondChangedBasisEpochReentryResult."
        )
    if not isinstance(prior_root_backed_continuation_overlay_source, Path):
        raise TypeError(
            "prior_root_backed_continuation_overlay_source must be pathlib.Path."
        )
    if not isinstance(destination, Path):
        raise TypeError("destination must be pathlib.Path.")

    earned = verification_result.fresh_reentry
    checkpoint = persist_chromium_research_second_basis_epoch_reentry_plan_document(
        earned,
        prior_root_backed_continuation_overlay_source=(
            prior_root_backed_continuation_overlay_source
        ),
        destination=destination,
    )

    if checkpoint.reentry is not earned:
        raise ChromiumResearchSecondChangedBasisEpochReentryOverlayError(
            "37B checkpoint did not retain the exact 46E fresh 37A proof."
        )

    original_plan = earned.plan
    candidate_plan = checkpoint.plan
    if (
        candidate_plan.prior_root_backed_continuation_overlay_source
        != prior_root_backed_continuation_overlay_source.resolve()
    ):
        raise ChromiumResearchSecondChangedBasisEpochReentryOverlayError(
            "37B candidate plan did not retain the explicit current prior continuation-overlay source."
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
            raise ChromiumResearchSecondChangedBasisEpochReentryOverlayError(
                f"37B candidate plan changed earned second-epoch locator field {field_name!r}."
            )

    fresh = checkpoint.fresh_reentry
    if (
        fresh.prior_continuation_reentry.controller.presentation
        != earned.prior_continuation_reentry.controller.presentation
    ):
        raise ChromiumResearchSecondChangedBasisEpochReentryOverlayError(
            "37B mandatory fresh proof presents different prior first-root continuation state."
        )
    if (
        fresh.prior_continuation_reentry.controller.declared_endpoint.verification.edge_record_sha256
        != earned.prior_continuation_reentry.controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchSecondChangedBasisEpochReentryOverlayError(
            "37B mandatory fresh proof identifies a different prior continuation endpoint."
        )
    if (
        fresh.prior_continuation_reentry.prior_root_backed_reentry.loaded_root.verification.root_record_sha256
        != earned.prior_continuation_reentry.prior_root_backed_reentry.loaded_root.verification.root_record_sha256
    ):
        raise ChromiumResearchSecondChangedBasisEpochReentryOverlayError(
            "37B mandatory fresh proof identifies a different retained first 34A root."
        )
    if (
        fresh.loaded_root.verification.root_record_sha256
        != earned.loaded_root.verification.root_record_sha256
    ):
        raise ChromiumResearchSecondChangedBasisEpochReentryOverlayError(
            "37B mandatory fresh proof identifies a different second 34A root."
        )
    if fresh.controller.presentation != earned.controller.presentation:
        raise ChromiumResearchSecondChangedBasisEpochReentryOverlayError(
            "37B mandatory fresh proof presents different second-basis governed state."
        )
    if (
        fresh.controller.declared_endpoint.verification.edge_record_sha256
        != earned.controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchSecondChangedBasisEpochReentryOverlayError(
            "37B mandatory fresh proof identifies a different second-basis endpoint."
        )

    expected_destination = destination.resolve()
    if checkpoint.persistence.path != expected_destination:
        raise ChromiumResearchSecondChangedBasisEpochReentryOverlayError(
            "37B persisted overlay path does not equal the explicit requested destination."
        )
    if load_chromium_research_second_basis_epoch_reentry_plan_document(
        checkpoint.persistence.path
    ) != candidate_plan:
        raise ChromiumResearchSecondChangedBasisEpochReentryOverlayError(
            "37B persisted overlay does not strictly decode to the public candidate plan."
        )

    return ChromiumResearchSecondChangedBasisEpochReentryOverlayResult(
        verification_result=verification_result,
        checkpoint=checkpoint,
    )


__all__ = [
    "ChromiumResearchSecondChangedBasisEpochReentryOverlayError",
    "ChromiumResearchSecondChangedBasisEpochReentryOverlayResult",
    "persist_chromium_research_second_changed_basis_epoch_reentry_overlay",
]
