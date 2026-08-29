from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from .chromium_research_second_basis_epoch_reentry import (
    ChromiumResearchSecondBasisEpochReentryPlan,
    ChromiumResearchSecondBasisEpochReentryResult,
    create_chromium_research_second_basis_epoch_reentry_plan,
    reenter_chromium_research_second_basis_epoch,
)
from .chromium_research_second_changed_basis_session_adoption import (
    ChromiumResearchSecondChangedBasisSessionAdoptionResult,
)
from .chromium_research_session_reentry import (
    ChromiumResearchWorkingSetMemberReentryLocator,
)


class ChromiumResearchSecondChangedBasisEpochReentryError(ValueError):
    """Raised when exact 46D evidence cannot support one explicit 37A proof."""


@dataclass(frozen=True, slots=True)
class ChromiumResearchSecondChangedBasisEpochReentryResult:
    """One explicit fresh 37A reconstruction verified against exact 46D evidence.

    `adoption_result` is the exact historical 46D adoption selected for proof. `plan`
    is caller-owned operational configuration assembled only from explicit current
    locators. `fresh_reentry` is the public 37A reconstruction that re-earns both the
    prior first-root continuation ancestry and the second-root-backed adopted session.

    This result writes no 37B overlay, replaces no mounted controller, backfills no
    launch path, and grants no current/latest/head, chronology, path-identity, or
    semantic-support authority.
    """

    adoption_result: ChromiumResearchSecondChangedBasisSessionAdoptionResult
    plan: ChromiumResearchSecondBasisEpochReentryPlan
    fresh_reentry: ChromiumResearchSecondBasisEpochReentryResult


def verify_chromium_research_second_changed_basis_epoch_reentry(
    adoption_result: ChromiumResearchSecondChangedBasisSessionAdoptionResult,
    prior_root_backed_continuation_overlay_source: Path,
    appended_working_set_members: Iterable[ChromiumResearchWorkingSetMemberReentryLocator],
    *,
    changed_working_set_source: Path,
    changed_note_source: Path,
    transition_source: Path,
    root_source: Path,
    first_edge_source: Path,
    declaration_source: Path,
) -> ChromiumResearchSecondChangedBasisEpochReentryResult:
    """Freshly reconstruct the exact historical 46D session through public 37A.

    Every durable locator is supplied by the caller for this operation. In particular,
    the prior 35D/35E continuation overlay is explicit even when the launching product
    has persisted path provenance. Raw 36D launch provenance therefore remains pathless
    unless the caller independently supplies a valid persisted continuation overlay;
    successful verification never backfills that path into launch provenance.
    """

    if type(adoption_result) is not ChromiumResearchSecondChangedBasisSessionAdoptionResult:
        raise TypeError(
            "adoption_result must be exactly "
            "ChromiumResearchSecondChangedBasisSessionAdoptionResult."
        )

    paths = {
        "prior_root_backed_continuation_overlay_source": (
            prior_root_backed_continuation_overlay_source
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

    plan = create_chromium_research_second_basis_epoch_reentry_plan(
        prior_root_backed_continuation_overlay_source,
        appended_working_set_members,
        changed_working_set_source=changed_working_set_source,
        changed_note_source=changed_note_source,
        transition_source=transition_source,
        root_source=root_source,
        declared_edge_sources=(first_edge_source,),
        declaration_source=declaration_source,
    )
    fresh = reenter_chromium_research_second_basis_epoch(plan)

    fresh_prior = fresh.prior_continuation_reentry
    if fresh_prior.controller.presentation != retained_prior.controller.presentation:
        raise ChromiumResearchSecondChangedBasisEpochReentryError(
            "Fresh 37A reconstruction identifies different prior first-root continuation state."
        )
    if (
        fresh_prior.controller.declared_endpoint.verification.edge_record_sha256
        != retained_prior.controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchSecondChangedBasisEpochReentryError(
            "Fresh 37A reconstruction identifies a different prior continuation endpoint."
        )
    if (
        fresh_prior.prior_root_backed_reentry.loaded_root.verification.root_record_sha256
        != retained_prior.prior_root_backed_reentry.loaded_root.verification.root_record_sha256
    ):
        raise ChromiumResearchSecondChangedBasisEpochReentryError(
            "Fresh 37A reconstruction identifies a different retained first 34A root."
        )

    expected_second_root_sha = (
        adoption_result.edge_result.root_result.persistence.root_record_sha256
    )
    if fresh.loaded_root.verification.root_record_sha256 != expected_second_root_sha:
        raise ChromiumResearchSecondChangedBasisEpochReentryError(
            "Fresh 37A reconstruction identifies a different second 34A root."
        )
    if (
        fresh.loaded_declaration.verification.sequence_record_sha256
        != adoption_result.declaration.sequence_record_sha256
    ):
        raise ChromiumResearchSecondChangedBasisEpochReentryError(
            "Fresh 37A reconstruction identifies a different second-root-backed declaration."
        )

    expected_edge_sha = adoption_result.edge_result.persistence.edge_record_sha256
    if fresh.controller.declared_endpoint.verification.edge_record_sha256 != expected_edge_sha:
        raise ChromiumResearchSecondChangedBasisEpochReentryError(
            "Fresh 37A reconstruction identifies a different first post-second-root endpoint."
        )
    if fresh.controller.presentation != adoption_result.controller.presentation:
        raise ChromiumResearchSecondChangedBasisEpochReentryError(
            "Fresh 37A reconstruction presents different adopted second-basis research state."
        )

    return ChromiumResearchSecondChangedBasisEpochReentryResult(
        adoption_result=adoption_result,
        plan=plan,
        fresh_reentry=fresh,
    )


__all__ = [
    "ChromiumResearchSecondChangedBasisEpochReentryError",
    "ChromiumResearchSecondChangedBasisEpochReentryResult",
    "verify_chromium_research_second_changed_basis_epoch_reentry",
]
