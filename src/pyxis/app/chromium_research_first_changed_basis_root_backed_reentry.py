from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from .chromium_research_first_changed_basis_session_adoption import (
    ChromiumResearchFirstChangedBasisSessionAdoptionResult,
)
from .chromium_research_root_backed_session_reentry import (
    ChromiumResearchRootBackedSessionReentryPlan,
    ChromiumResearchRootBackedSessionReentryResult,
    create_chromium_research_root_backed_session_reentry_plan,
    reenter_chromium_research_root_backed_session,
)
from .chromium_research_session_reentry import (
    ChromiumResearchSessionReentryResult,
    ChromiumResearchWorkingSetMemberReentryLocator,
)


class ChromiumResearchFirstChangedBasisRootBackedReentryError(ValueError):
    """Raised when exact 44E evidence cannot support one explicit 35B proof."""


@dataclass(frozen=True, slots=True)
class ChromiumResearchFirstChangedBasisRootBackedReentryResult:
    """One explicit fresh 35B reconstruction verified against exact 44E evidence.

    This result is proof evidence only. It does not persist a 35C overlay, replace a
    mounted controller, establish a current/latest/head branch, or grant chronology.
    """

    adoption_result: ChromiumResearchFirstChangedBasisSessionAdoptionResult
    initial_ordinary_reentry: ChromiumResearchSessionReentryResult
    plan: ChromiumResearchRootBackedSessionReentryPlan
    fresh_reentry: ChromiumResearchRootBackedSessionReentryResult


def verify_chromium_research_first_changed_basis_root_backed_reentry(
    adoption_result: ChromiumResearchFirstChangedBasisSessionAdoptionResult,
    initial_ordinary_reentry: ChromiumResearchSessionReentryResult,
    appended_working_set_members: Iterable[ChromiumResearchWorkingSetMemberReentryLocator],
    *,
    changed_working_set_source: Path,
    changed_note_source: Path,
    transition_source: Path,
    root_source: Path,
    first_edge_source: Path,
    declaration_source: Path,
) -> ChromiumResearchFirstChangedBasisRootBackedReentryResult:
    """Freshly reconstruct exact 44E root-backed state through public 35B.

    Every changed-basis durable locator remains caller supplied. The exact initial
    ordinary 31A typed plan is reused as retained launch-lineage application state;
    no receipt path is promoted into locator authority.
    """

    if type(adoption_result) is not ChromiumResearchFirstChangedBasisSessionAdoptionResult:
        raise TypeError(
            "adoption_result must be exactly ChromiumResearchFirstChangedBasisSessionAdoptionResult."
        )
    if type(initial_ordinary_reentry) is not ChromiumResearchSessionReentryResult:
        raise TypeError(
            "initial_ordinary_reentry must be exactly ChromiumResearchSessionReentryResult."
        )

    transition_result = adoption_result.edge_result.root_result.transition_result
    if (
        initial_ordinary_reentry.controller.presentation
        != transition_result.controller.presentation
    ):
        raise ChromiumResearchFirstChangedBasisRootBackedReentryError(
            "Initial ordinary re-entry does not describe the exact pre-change session."
        )
    if (
        initial_ordinary_reentry.controller.declared_endpoint.verification.edge_record_sha256
        != transition_result.controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchFirstChangedBasisRootBackedReentryError(
            "Initial ordinary re-entry identifies a different pre-change endpoint."
        )

    paths = {
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

    plan = create_chromium_research_root_backed_session_reentry_plan(
        initial_ordinary_reentry.plan,
        appended_working_set_members,
        changed_working_set_source=changed_working_set_source,
        changed_note_source=changed_note_source,
        transition_source=transition_source,
        root_source=root_source,
        declared_edge_sources=(first_edge_source,),
        declaration_source=declaration_source,
    )
    fresh = reenter_chromium_research_root_backed_session(plan)

    if fresh.plan.prior_session_plan != initial_ordinary_reentry.plan:
        raise ChromiumResearchFirstChangedBasisRootBackedReentryError(
            "Fresh 35B plan did not retain the exact initial ordinary 31A plan."
        )

    expected_root_sha = adoption_result.edge_result.root_result.persistence.root_record_sha256
    if fresh.loaded_root.verification.root_record_sha256 != expected_root_sha:
        raise ChromiumResearchFirstChangedBasisRootBackedReentryError(
            "Fresh 35B reconstruction identifies a different 34A root."
        )

    if (
        fresh.loaded_declaration.verification.sequence_record_sha256
        != adoption_result.declaration.sequence_record_sha256
    ):
        raise ChromiumResearchFirstChangedBasisRootBackedReentryError(
            "Fresh 35B reconstruction identifies a different 26B declaration."
        )

    expected_edge_sha = adoption_result.edge_result.persistence.edge_record_sha256
    if (
        fresh.controller.declared_endpoint.verification.edge_record_sha256
        != expected_edge_sha
    ):
        raise ChromiumResearchFirstChangedBasisRootBackedReentryError(
            "Fresh 35B reconstruction identifies a different declared endpoint."
        )
    if fresh.controller.presentation != adoption_result.controller.presentation:
        raise ChromiumResearchFirstChangedBasisRootBackedReentryError(
            "Fresh 35B reconstruction presents different adopted research state."
        )

    return ChromiumResearchFirstChangedBasisRootBackedReentryResult(
        adoption_result=adoption_result,
        initial_ordinary_reentry=initial_ordinary_reentry,
        plan=plan,
        fresh_reentry=fresh,
    )


__all__ = [
    "ChromiumResearchFirstChangedBasisRootBackedReentryError",
    "ChromiumResearchFirstChangedBasisRootBackedReentryResult",
    "verify_chromium_research_first_changed_basis_root_backed_reentry",
]
