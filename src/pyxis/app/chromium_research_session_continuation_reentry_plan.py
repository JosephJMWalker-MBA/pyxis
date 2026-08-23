from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .chromium_research_session_reentry import (
    ChromiumResearchSessionReentryPlan,
    ChromiumResearchSessionReentryResult,
    create_chromium_research_session_reentry_plan,
    reenter_chromium_research_session,
)
from .chromium_research_session_reentry_plan_document import (
    ChromiumResearchSessionReentryPlanDocumentPersistenceResult,
    load_chromium_research_session_reentry_plan_document,
    persist_chromium_research_session_reentry_plan_document,
)
from .chromium_research_session_rollover import ChromiumResearchSessionRolloverResult


@dataclass(frozen=True, slots=True)
class ChromiumResearchSessionContinuationReentryPlanResult:
    """One explicit restart plan for one already-chosen continuation session.

    The result preserves the exact prior caller-owned locator lineage, adds the old
    declared segment to the explicit predecessor path sequence, and points the new
    declared segment only at the explicitly supplied successor and continuation
    declaration locations. `fresh_reentry` proves those locations can reconstruct a
    session presentation equal to the already-earned 30A continuation before the
    locator document is persisted.

    This is operational restart configuration only. It is not a history index,
    content-identity registry, branch selector, chronology record, or global head.
    """

    prior_reentry: ChromiumResearchSessionReentryResult
    rollover: ChromiumResearchSessionRolloverResult
    plan: ChromiumResearchSessionReentryPlan
    fresh_reentry: ChromiumResearchSessionReentryResult
    persistence: ChromiumResearchSessionReentryPlanDocumentPersistenceResult


class ChromiumResearchSessionContinuationReentryPlanError(ValueError):
    """Raised when an explicit continuation cannot become a verified restart plan."""


def persist_chromium_research_session_continuation_reentry_plan(
    prior_reentry: ChromiumResearchSessionReentryResult,
    rollover: ChromiumResearchSessionRolloverResult,
    *,
    successor_edge_source: Path,
    continuation_declaration_source: Path,
    destination: Path,
) -> ChromiumResearchSessionContinuationReentryPlanResult:
    """Persist one no-overwrite locator plan for an explicit 30A continuation.

    The caller supplies current locations for the exact successor edge and exact
    continuation declaration. Pyxis does not reuse those paths as identity, discover
    moved files, search for a newer declaration, or choose among siblings.

    Before writing the operational locator document, Pyxis constructs the next 31A
    plan and freshly re-enters it from durable bytes. The reconstructed presentation
    must equal the already-earned 30A continuation presentation. Only then is the
    strict 31B locator document persisted and round-trip decoded.
    """

    if not isinstance(prior_reentry, ChromiumResearchSessionReentryResult):
        raise TypeError("prior_reentry must be ChromiumResearchSessionReentryResult.")
    if not isinstance(rollover, ChromiumResearchSessionRolloverResult):
        raise TypeError("rollover must be ChromiumResearchSessionRolloverResult.")

    successor_source = _require_path(successor_edge_source, "successor_edge_source")
    declaration_source = _require_path(
        continuation_declaration_source,
        "continuation_declaration_source",
    )
    document_destination = _require_path(destination, "destination")

    _require_prior_session_coherence(prior_reentry, rollover)

    prior_plan = prior_reentry.plan
    next_plan = create_chromium_research_session_reentry_plan(
        prior_plan.working_set_members,
        working_set_source=prior_plan.working_set_source,
        prior_note_source=prior_plan.prior_note_source,
        prior_revision_source=prior_plan.prior_revision_source,
        continuation_source=prior_plan.continuation_source,
        starting_predecessor_edge_sources=(
            *prior_plan.starting_predecessor_edge_sources,
            *prior_plan.declared_edge_sources,
        ),
        declared_edge_sources=(successor_source,),
        declaration_source=declaration_source,
    )

    try:
        fresh_reentry = reenter_chromium_research_session(next_plan)
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchSessionContinuationReentryPlanError(
            "Explicit continuation locations could not freshly reconstruct a governed session."
        ) from exc

    expected_presentation = rollover.continuation_controller.presentation
    if fresh_reentry.controller.presentation != expected_presentation:
        raise ChromiumResearchSessionContinuationReentryPlanError(
            "Fresh continuation re-entry does not match the explicitly chosen rollover session."
        )
    if (
        fresh_reentry.controller.declared_endpoint.verification.edge_record_sha256
        != rollover.continuation_controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchSessionContinuationReentryPlanError(
            "Fresh continuation endpoint identity does not match the chosen rollover endpoint."
        )

    persistence = persist_chromium_research_session_reentry_plan_document(
        next_plan,
        document_destination,
    )
    try:
        decoded = load_chromium_research_session_reentry_plan_document(persistence.path)
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchSessionContinuationReentryPlanError(
            "Persisted continuation locator plan could not be round-trip decoded."
        ) from exc
    if decoded != next_plan:
        raise ChromiumResearchSessionContinuationReentryPlanError(
            "Persisted continuation locator plan did not round-trip to the exact next plan."
        )

    return ChromiumResearchSessionContinuationReentryPlanResult(
        prior_reentry=prior_reentry,
        rollover=rollover,
        plan=next_plan,
        fresh_reentry=fresh_reentry,
        persistence=persistence,
    )


def _require_prior_session_coherence(
    prior_reentry: ChromiumResearchSessionReentryResult,
    rollover: ChromiumResearchSessionRolloverResult,
) -> None:
    prior_controller = prior_reentry.controller
    rollover_prior = rollover.prior_controller

    if prior_controller.presentation != rollover_prior.presentation:
        raise ChromiumResearchSessionContinuationReentryPlanError(
            "Prior re-entry plan does not describe the session from which this rollover was chosen."
        )
    if (
        prior_controller.presentation.sequence.declaration_record_sha256
        != rollover_prior.presentation.sequence.declaration_record_sha256
    ):
        raise ChromiumResearchSessionContinuationReentryPlanError(
            "Prior re-entry declaration identity does not match the rollover's prior session."
        )
    if (
        prior_controller.declared_endpoint.verification.edge_record_sha256
        != rollover_prior.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchSessionContinuationReentryPlanError(
            "Prior re-entry endpoint identity does not match the rollover's prior session."
        )


def _require_path(value: Path, label: str) -> Path:
    if not isinstance(value, Path):
        raise TypeError(f"{label} must be pathlib.Path.")
    return value
