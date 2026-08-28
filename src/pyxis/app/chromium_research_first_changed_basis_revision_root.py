from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .chromium_research_first_changed_basis_transition import (
    ChromiumResearchFirstChangedBasisTransitionResult,
)
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


class ChromiumResearchFirstChangedBasisRevisionRootError(ValueError):
    """Raised when an exact 44B result cannot support the first changed-basis root."""


@dataclass(frozen=True, slots=True)
class ChromiumResearchFirstChangedBasisRevisionRootResult:
    """One explicit 34A revision root proven from an exact successful 44B transition.

    The result retains the exact 44B product result, one human-authored in-memory 34A
    root, its no-overwrite persistence evidence, and one fresh 34A relink through the
    caller-supplied durable transition/basis locators.

    It does not create the 34B first ordinary edge after the root, a 35A declared
    root-backed session, an epoch, or any current/latest/head state.
    """

    transition_result: ChromiumResearchFirstChangedBasisTransitionResult
    root: ChromiumResearchSessionWorkingSetTransitionRevisionRootRecord
    persistence: ChromiumResearchSessionWorkingSetTransitionRevisionRootPersistenceEvidence
    loaded_root: ChromiumPageResearchLoadedWorkingSetTransitionRevisionRootRecord


def persist_chromium_research_first_changed_basis_revision_root(
    transition_result: ChromiumResearchFirstChangedBasisTransitionResult,
    *,
    revised_note_text: str,
    prior_edge_source: Path,
    working_set_source: Path,
    note_source: Path,
    transition_source: Path,
    destination: Path,
) -> ChromiumResearchFirstChangedBasisRevisionRootResult:
    """Persist and freshly relink the first 34A revision root after exact 44B success.

    Every durable locator remains caller supplied. The 44B receipt paths are not used
    as locator authority. The exact loaded 33B transition retained by the 44B result
    supplies only application identity/relationship context; public 34A persistence
    and load boundaries freshly re-establish durable evidence from the explicit paths.

    The mounted old-basis governed session is irrelevant here. A 44B transition is a
    durable historical relationship and may root a changed-basis lineage even if the
    old-basis product later continues elsewhere. No branch is selected as current.
    """

    if type(transition_result) is not ChromiumResearchFirstChangedBasisTransitionResult:
        raise TypeError(
            "transition_result must be exactly ChromiumResearchFirstChangedBasisTransitionResult."
        )
    if not isinstance(revised_note_text, str):
        raise TypeError("revised_note_text must be str.")

    loaded_transition = transition_result.loaded_transition
    if (
        loaded_transition.verification.transition_record_sha256
        != transition_result.persistence.transition_record_sha256
    ):
        raise ChromiumResearchFirstChangedBasisRevisionRootError(
            "44B loaded transition does not match its persisted transition identity."
        )
    if (
        loaded_transition.prior_endpoint.verification.edge_record_sha256
        != transition_result.controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchFirstChangedBasisRevisionRootError(
            "44B loaded transition does not retain the first crossing's exact prior endpoint."
        )
    if (
        loaded_transition.successor_note.working_set.verification.working_set_record_sha256
        != transition_result.prepared.working_set_persistence.working_set_record_sha256
    ):
        raise ChromiumResearchFirstChangedBasisRevisionRootError(
            "44B loaded transition does not retain the exact prepared working set."
        )
    if (
        loaded_transition.successor_note.verification.note_record_sha256
        != transition_result.prepared.note_persistence.note_record_sha256
    ):
        raise ChromiumResearchFirstChangedBasisRevisionRootError(
            "44B loaded transition does not retain the exact prepared working-set note."
        )

    root = create_chromium_research_session_working_set_transition_revision_root(
        loaded_transition,
        revised_note_text=revised_note_text,
    )
    persistence = persist_chromium_research_session_working_set_transition_revision_root(
        root,
        prior_edge_source=_require_path(prior_edge_source, label="prior_edge_source"),
        working_set_source=_require_path(working_set_source, label="working_set_source"),
        note_source=_require_path(note_source, label="note_source"),
        transition_source=_require_path(transition_source, label="transition_source"),
        destination=_require_path(destination, label="destination"),
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
        raise ChromiumResearchFirstChangedBasisRevisionRootError(
            "34A persistence did not retain the exact in-memory root."
        )
    if loaded_root.verification.root_record_sha256 != persistence.root_record_sha256:
        raise ChromiumResearchFirstChangedBasisRevisionRootError(
            "Fresh 34A relink identifies a different root record."
        )
    if (
        loaded_root.transition.verification.transition_record_sha256
        != transition_result.persistence.transition_record_sha256
    ):
        raise ChromiumResearchFirstChangedBasisRevisionRootError(
            "Fresh 34A relink identifies a different 33B transition."
        )
    if loaded_root.root.revision.revised_note.note_text != revised_note_text:
        raise ChromiumResearchFirstChangedBasisRevisionRootError(
            "Fresh 34A relink reconstructs different human root wording."
        )

    return ChromiumResearchFirstChangedBasisRevisionRootResult(
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
    "ChromiumResearchFirstChangedBasisRevisionRootError",
    "ChromiumResearchFirstChangedBasisRevisionRootResult",
    "persist_chromium_research_first_changed_basis_revision_root",
]
