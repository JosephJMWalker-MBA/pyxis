from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from .chromium_research_session_reentry import (
    ChromiumResearchWorkingSetMemberReentryLocator,
)
from .chromium_research_third_basis_epoch_reentry import (
    ChromiumResearchThirdBasisEpochReentryPlan,
    ChromiumResearchThirdBasisEpochReentryResult,
    create_chromium_research_third_basis_epoch_reentry_plan,
    reenter_chromium_research_third_basis_epoch,
)
from .chromium_research_third_changed_basis_session_adoption import (
    ChromiumResearchThirdChangedBasisSessionAdoptionResult,
)


class ChromiumResearchThirdChangedBasisEpochReentryError(ValueError):
    """Raised when exact 47D evidence cannot support one explicit 40A proof."""


@dataclass(frozen=True, slots=True)
class ChromiumResearchThirdChangedBasisEpochReentryResult:
    """One explicit fresh 40A reconstruction verified against exact 47D evidence.

    `adoption_result` is the exact historical 47D adoption selected for proof. `plan`
    is caller-owned operational configuration assembled only from explicit current
    locators. `fresh_reentry` is the public 40A reconstruction that re-earns the
    complete retained first-/second-root continuation ancestry and the third-root-backed
    adopted session.

    This result writes no 40B overlay, replaces no mounted controller, backfills no
    launch path, and grants no current/latest/head, chronology, path-identity, or
    semantic-support authority.
    """

    adoption_result: ChromiumResearchThirdChangedBasisSessionAdoptionResult
    plan: ChromiumResearchThirdBasisEpochReentryPlan
    fresh_reentry: ChromiumResearchThirdBasisEpochReentryResult


def verify_chromium_research_third_changed_basis_epoch_reentry(
    adoption_result: ChromiumResearchThirdChangedBasisSessionAdoptionResult,
    prior_second_basis_epoch_continuation_overlay_source: Path,
    appended_working_set_members: Iterable[ChromiumResearchWorkingSetMemberReentryLocator],
    *,
    changed_working_set_source: Path,
    changed_note_source: Path,
    transition_source: Path,
    root_source: Path,
    first_edge_source: Path,
    declaration_source: Path,
) -> ChromiumResearchThirdChangedBasisEpochReentryResult:
    """Freshly reconstruct the exact historical 47D session through public 40A.

    Every durable locator is supplied by the caller for this operation. In particular,
    the prior 37C/37D continuation overlay is explicit even when the launching product
    has persisted path provenance. Raw 38F launch provenance therefore remains pathless
    unless the caller independently supplies a valid persisted continuation overlay;
    successful verification never backfills that path into launch provenance.
    """

    if type(adoption_result) is not ChromiumResearchThirdChangedBasisSessionAdoptionResult:
        raise TypeError(
            "adoption_result must be exactly "
            "ChromiumResearchThirdChangedBasisSessionAdoptionResult."
        )

    paths = {
        "prior_second_basis_epoch_continuation_overlay_source": (
            prior_second_basis_epoch_continuation_overlay_source
        ),
        "changed_working_set_source": changed_working_set_source,
        "changed_note_source": changed_note_source,
        "transition_source": transition_source,
        "root_source": root_source,
        "first_edge_source": first_edge_source,
        "declaration_source": declaration_source,
    }
    for label, value in paths.items():
        if not isinstance(value, Path):
            raise TypeError(f"{label} must be pathlib.Path.")

    transition_result = adoption_result.edge_result.root_result.transition_result
    retained_prior = transition_result.continuation_reentry

    plan = create_chromium_research_third_basis_epoch_reentry_plan(
        prior_second_basis_epoch_continuation_overlay_source,
        appended_working_set_members,
        changed_working_set_source=changed_working_set_source,
        changed_note_source=changed_note_source,
        transition_source=transition_source,
        root_source=root_source,
        declared_edge_sources=(first_edge_source,),
        declaration_source=declaration_source,
    )
    fresh = reenter_chromium_research_third_basis_epoch(plan)

    fresh_prior = fresh.prior_second_basis_epoch_continuation_reentry
    if fresh_prior.controller.presentation != retained_prior.controller.presentation:
        raise ChromiumResearchThirdChangedBasisEpochReentryError(
            "Fresh 40A reconstruction identifies different prior second-epoch continuation state."
        )
    if (
        fresh_prior.controller.declared_endpoint.verification.edge_record_sha256
        != retained_prior.controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchThirdChangedBasisEpochReentryError(
            "Fresh 40A reconstruction identifies a different prior second-epoch continuation endpoint."
        )

    fresh_second_epoch = fresh_prior.prior_second_basis_epoch_reentry
    retained_second_epoch = retained_prior.prior_second_basis_epoch_reentry
    if (
        fresh_second_epoch.prior_continuation_reentry.prior_root_backed_reentry.loaded_root.verification.root_record_sha256
        != retained_second_epoch.prior_continuation_reentry.prior_root_backed_reentry.loaded_root.verification.root_record_sha256
    ):
        raise ChromiumResearchThirdChangedBasisEpochReentryError(
            "Fresh 40A reconstruction identifies a different retained first 34A root."
        )
    if (
        fresh_second_epoch.loaded_root.verification.root_record_sha256
        != retained_second_epoch.loaded_root.verification.root_record_sha256
    ):
        raise ChromiumResearchThirdChangedBasisEpochReentryError(
            "Fresh 40A reconstruction identifies a different retained second 34A root."
        )

    expected_third_root_sha = (
        adoption_result.edge_result.root_result.persistence.root_record_sha256
    )
    if fresh.loaded_root.verification.root_record_sha256 != expected_third_root_sha:
        raise ChromiumResearchThirdChangedBasisEpochReentryError(
            "Fresh 40A reconstruction identifies a different third 34A root."
        )
    if (
        fresh.loaded_declaration.verification.sequence_record_sha256
        != adoption_result.declaration.sequence_record_sha256
    ):
        raise ChromiumResearchThirdChangedBasisEpochReentryError(
            "Fresh 40A reconstruction identifies a different third-root-backed declaration."
        )

    expected_edge_sha = adoption_result.edge_result.persistence.edge_record_sha256
    if fresh.controller.declared_endpoint.verification.edge_record_sha256 != expected_edge_sha:
        raise ChromiumResearchThirdChangedBasisEpochReentryError(
            "Fresh 40A reconstruction identifies a different first post-third-root endpoint."
        )
    if fresh.controller.presentation != adoption_result.controller.presentation:
        raise ChromiumResearchThirdChangedBasisEpochReentryError(
            "Fresh 40A reconstruction presents different adopted third-basis research state."
        )

    return ChromiumResearchThirdChangedBasisEpochReentryResult(
        adoption_result=adoption_result,
        plan=plan,
        fresh_reentry=fresh,
    )


__all__ = [
    "ChromiumResearchThirdChangedBasisEpochReentryError",
    "ChromiumResearchThirdChangedBasisEpochReentryResult",
    "verify_chromium_research_third_changed_basis_epoch_reentry",
]
