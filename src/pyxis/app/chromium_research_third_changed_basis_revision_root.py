from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .chromium_research_session_working_set_transition_revision_root import (
    ChromiumResearchSessionWorkingSetTransitionRevisionRootRecord,
    create_chromium_research_session_working_set_transition_revision_root,
)
from .chromium_research_session_working_set_transition_revision_root_load import (
    ChromiumPageResearchLoadedWorkingSetTransitionRevisionRootRecord,
    load_chromium_research_session_working_set_transition_revision_root,
)
from .chromium_research_session_working_set_transition_revision_root_persistence import (
    ChromiumResearchSessionWorkingSetTransitionRevisionRootPersistenceEvidence,
    persist_chromium_research_session_working_set_transition_revision_root,
)
from .chromium_research_third_changed_basis_transition import (
    ChromiumResearchThirdChangedBasisTransitionResult,
)


class ChromiumResearchThirdChangedBasisRevisionRootError(ValueError):
    """Raised when an exact 47A result cannot support the third changed-basis root."""


@dataclass(frozen=True, slots=True)
class ChromiumResearchThirdChangedBasisRevisionRootResult:
    """One explicit public-34A third revision root proven from an exact 47A transition.

    The result retains the exact 47A product result, one human-authored in-memory 34A
    root, its no-overwrite persistence evidence, and one fresh public-34A relink
    through caller-supplied durable transition/basis locators.

    It does not create the first ordinary edge after the third root, a third-epoch
    declaration/session, 40A re-entry, 40B restart overlay, or current/latest/head
    state.
    """

    transition_result: ChromiumResearchThirdChangedBasisTransitionResult
    root: ChromiumResearchSessionWorkingSetTransitionRevisionRootRecord
    persistence: ChromiumResearchSessionWorkingSetTransitionRevisionRootPersistenceEvidence
    loaded_root: ChromiumPageResearchLoadedWorkingSetTransitionRevisionRootRecord


def persist_chromium_research_third_changed_basis_revision_root(
    transition_result: ChromiumResearchThirdChangedBasisTransitionResult,
    *,
    revised_note_text: str,
    prior_edge_source: Path,
    working_set_source: Path,
    note_source: Path,
    transition_source: Path,
    destination: Path,
) -> ChromiumResearchThirdChangedBasisRevisionRootResult:
    """Persist and freshly relink one third public-34A root after exact 47A success.

    Every durable locator remains caller supplied. 47A receipt paths are evidence of
    prior successful operations, not perpetual current-location authority. Public 34A
    persistence/load boundaries freshly re-establish the durable relationship from
    the explicit paths supplied to this call.

    The mounted second-epoch continuation is irrelevant after 47A succeeds. The
    transition remains durable historical relationship authority and may receive its
    root even if the older second-epoch branch later continues elsewhere. No branch is
    selected as current/latest/head by doing so.
    """

    if type(transition_result) is not ChromiumResearchThirdChangedBasisTransitionResult:
        raise TypeError(
            "transition_result must be exactly ChromiumResearchThirdChangedBasisTransitionResult."
        )
    if not isinstance(revised_note_text, str):
        raise TypeError("revised_note_text must be str.")

    loaded_transition = transition_result.loaded_transition
    if (
        loaded_transition.verification.transition_record_sha256
        != transition_result.persistence.transition_record_sha256
    ):
        raise ChromiumResearchThirdChangedBasisRevisionRootError(
            "47A loaded transition does not match its persisted transition identity."
        )
    if (
        loaded_transition.prior_endpoint.verification.edge_record_sha256
        != transition_result.controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchThirdChangedBasisRevisionRootError(
            "47A loaded transition does not retain the third crossing's exact prior endpoint identity."
        )
    if (
        loaded_transition.successor_note.working_set.verification.working_set_record_sha256
        != transition_result.prepared.working_set_persistence.working_set_record_sha256
    ):
        raise ChromiumResearchThirdChangedBasisRevisionRootError(
            "47A loaded transition does not retain the exact prepared third working set."
        )
    if (
        loaded_transition.successor_note.verification.note_record_sha256
        != transition_result.prepared.note_persistence.note_record_sha256
    ):
        raise ChromiumResearchThirdChangedBasisRevisionRootError(
            "47A loaded transition does not retain the exact prepared third working-set note."
        )

    prior_edge_source = _require_path(prior_edge_source, label="prior_edge_source")
    working_set_source = _require_path(working_set_source, label="working_set_source")
    note_source = _require_path(note_source, label="note_source")
    transition_source = _require_path(transition_source, label="transition_source")
    destination = _require_path(destination, label="destination")

    root = create_chromium_research_session_working_set_transition_revision_root(
        loaded_transition,
        revised_note_text=revised_note_text,
    )
    persistence = persist_chromium_research_session_working_set_transition_revision_root(
        root,
        prior_edge_source=prior_edge_source,
        working_set_source=working_set_source,
        note_source=note_source,
        transition_source=transition_source,
        destination=destination,
    )
    loaded_root = load_chromium_research_session_working_set_transition_revision_root(
        loaded_transition.prior_endpoint,
        transition_result.prepared.working_set.items,
        prior_edge_source=prior_edge_source,
        working_set_source=working_set_source,
        note_source=note_source,
        transition_source=transition_source,
        root_source=persistence.path,
    )

    if persistence.root is not root:
        raise ChromiumResearchThirdChangedBasisRevisionRootError(
            "Third public-34A persistence did not retain the exact in-memory root."
        )
    if loaded_root.verification.root_record_sha256 != persistence.root_record_sha256:
        raise ChromiumResearchThirdChangedBasisRevisionRootError(
            "Fresh third public-34A relink identifies a different root record."
        )
    if (
        loaded_root.transition.verification.transition_record_sha256
        != transition_result.persistence.transition_record_sha256
    ):
        raise ChromiumResearchThirdChangedBasisRevisionRootError(
            "Fresh third public-34A relink identifies a different 47A transition."
        )
    if loaded_root.root.revision.revised_note.note_text != revised_note_text:
        raise ChromiumResearchThirdChangedBasisRevisionRootError(
            "Fresh third public-34A relink reconstructs different human root wording."
        )

    return ChromiumResearchThirdChangedBasisRevisionRootResult(
        transition_result=transition_result,
        root=root,
        persistence=persistence,
        loaded_root=loaded_root,
    )


def _require_path(value: Path, *, label: str) -> Path:
    if not isinstance(value, Path):
        raise TypeError(f"{label} must be pathlib.Path.")
    return value


__all__ = [
    "ChromiumResearchThirdChangedBasisRevisionRootError",
    "ChromiumResearchThirdChangedBasisRevisionRootResult",
    "persist_chromium_research_third_changed_basis_revision_root",
]
