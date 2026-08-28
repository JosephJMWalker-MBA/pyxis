from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from .chromium_research_revision_edge_working_set_presentation import (
    ChromiumPageResearchWorkingSetMemberPresentation,
    _present_working_set_member,
)
from .chromium_research_session_controller import ChromiumResearchSessionController
from .chromium_research_session_presentation import present_chromium_research_session
from .chromium_research_working_set import (
    ChromiumPageResearchWorkingSetItem,
    create_chromium_research_working_set,
)


_PRESENTATION_MODE = "read_only_candidate_appended_research_evidence"
_CANDIDATE_ROLE = "candidate_not_yet_working_set_or_adopted"


@dataclass(frozen=True, slots=True)
class ChromiumResearchChangedBasisCandidatePresentation:
    """Read-only projection of exact evidence proposed for a changed research basis.

    The projection is deliberately not a working-set, revision-position, transition,
    root, epoch, or adoption presentation. It describes only already-loaded evidence
    explicitly supplied by the caller as candidate appended membership against one
    exact currently declared endpoint.
    """

    presentation_mode: str
    candidate_role: str
    declaration_record_sha256: str
    declared_endpoint_sha256: str
    candidate_member_count: int
    members: tuple[ChromiumPageResearchWorkingSetMemberPresentation, ...]


def present_chromium_research_changed_basis_candidate(
    controller: ChromiumResearchSessionController,
    appended_items: Iterable[ChromiumPageResearchWorkingSetItem],
) -> ChromiumResearchChangedBasisCandidatePresentation:
    """Project exact already-loaded candidate members without persistence or adoption.

    No path, sidecar, browser, or discovery operation occurs here. The existing 20A
    constructor re-establishes only the in-memory member contracts. Member/excerpt
    formatting reuses the established read-only working-set member projection while
    intentionally omitting every declared-position and revision-edge field.
    """

    if not isinstance(controller, ChromiumResearchSessionController):
        raise TypeError("controller must be ChromiumResearchSessionController.")
    rebuilt_session = present_chromium_research_session(controller.loaded)
    if rebuilt_session != controller.presentation:
        raise ValueError(
            "Research controller presentation is incoherent with its retained loaded evidence."
        )

    items = tuple(appended_items)
    if not items:
        raise ValueError("candidate appended evidence must contain at least one item.")

    rebuilt = create_chromium_research_working_set(items)
    if len(rebuilt.items) != len(items) or any(
        observed is not supplied for observed, supplied in zip(rebuilt.items, items)
    ):
        raise ValueError("candidate appended evidence identity/order is incoherent.")

    members = tuple(
        _present_working_set_member(item, position=index)
        for index, item in enumerate(items, start=1)
    )
    if len(members) != len(items):
        raise ValueError("candidate member presentation cardinality is incoherent.")

    return ChromiumResearchChangedBasisCandidatePresentation(
        presentation_mode=_PRESENTATION_MODE,
        candidate_role=_CANDIDATE_ROLE,
        declaration_record_sha256=(
            controller.presentation.sequence.declaration_record_sha256
        ),
        declared_endpoint_sha256=(
            controller.declared_endpoint.verification.edge_record_sha256
        ),
        candidate_member_count=len(members),
        members=members,
    )


__all__ = [
    "ChromiumResearchChangedBasisCandidatePresentation",
    "present_chromium_research_changed_basis_candidate",
]
