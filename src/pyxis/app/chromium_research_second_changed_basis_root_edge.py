from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .chromium_research_second_changed_basis_revision_root import (
    ChromiumResearchSecondChangedBasisRevisionRootResult,
)
from .chromium_research_session_working_set_transition_revision_root_edge_extension import (
    ChromiumResearchSessionWorkingSetTransitionRevisionRootEdgeExtensionRecord,
    create_chromium_research_session_working_set_transition_revision_root_edge_extension,
)
from .chromium_research_session_working_set_transition_revision_root_edge_extension_persistence import (
    ChromiumResearchSessionWorkingSetTransitionRevisionRootEdgePersistenceEvidence,
    persist_chromium_research_session_working_set_transition_revision_root_edge_extension,
)
from .chromium_research_session_working_set_transition_revision_root_edge_load import (
    load_chromium_research_session_working_set_transition_revision_root_edge,
)
from .chromium_research_working_set_note_revision_edge_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord,
)


class ChromiumResearchSecondChangedBasisRootEdgeError(ValueError):
    """Raised when an exact 46B root cannot support the first second-basis 34B edge."""


@dataclass(frozen=True, slots=True)
class ChromiumResearchSecondChangedBasisRootEdgeResult:
    """One explicit first ordinary edge proven from an exact successful 46B root.

    The result retains the exact 46B product result, one human-authored in-memory 34B
    root-edge extension, its no-overwrite persistence evidence in the existing
    ordinary edge format, and one fresh 34B relink into the standard loaded-edge type.

    It does not create a sequence declaration, second-epoch session/re-entry/adoption,
    or any current/latest/head state.
    """

    root_result: ChromiumResearchSecondChangedBasisRevisionRootResult
    extension: ChromiumResearchSessionWorkingSetTransitionRevisionRootEdgeExtensionRecord
    persistence: ChromiumResearchSessionWorkingSetTransitionRevisionRootEdgePersistenceEvidence
    loaded_edge: ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord


def persist_chromium_research_second_changed_basis_root_edge(
    root_result: ChromiumResearchSecondChangedBasisRevisionRootResult,
    *,
    revised_note_text: str,
    root_source: Path,
    destination: Path,
) -> ChromiumResearchSecondChangedBasisRootEdgeResult:
    """Persist and freshly relink the first ordinary 34B edge after exact 46B success.

    Only the caller-supplied current root file is reopened as durable predecessor
    evidence. Earlier second-transition and changed-basis files are not traversed
    again. The 46B root receipt path is not used as locator authority.

    The currently mounted one-root continuation is irrelevant here. A successful 46B
    root is durable historical relationship authority and can receive this local
    continuation even if the older one-root branch later continues elsewhere. No
    branch is selected as current/latest/head.
    """

    if type(root_result) is not ChromiumResearchSecondChangedBasisRevisionRootResult:
        raise TypeError(
            "root_result must be exactly "
            "ChromiumResearchSecondChangedBasisRevisionRootResult."
        )
    if not isinstance(revised_note_text, str):
        raise TypeError("revised_note_text must be str.")

    loaded_root = root_result.loaded_root
    if (
        loaded_root.verification.root_record_sha256
        != root_result.persistence.root_record_sha256
    ):
        raise ChromiumResearchSecondChangedBasisRootEdgeError(
            "46B loaded root does not match its persisted root identity."
        )
    if (
        loaded_root.root.revision.revised_note.note_text
        != root_result.root.revision.revised_note.note_text
    ):
        raise ChromiumResearchSecondChangedBasisRootEdgeError(
            "46B loaded root reconstructs different human root wording."
        )

    root_source = _require_path(root_source, label="root_source")
    destination = _require_path(destination, label="destination")

    extension = (
        create_chromium_research_session_working_set_transition_revision_root_edge_extension(
            loaded_root,
            revised_note_text=revised_note_text,
        )
    )
    persistence = (
        persist_chromium_research_session_working_set_transition_revision_root_edge_extension(
            extension,
            root_source=root_source,
            destination=destination,
        )
    )
    loaded_edge = load_chromium_research_session_working_set_transition_revision_root_edge(
        loaded_root,
        persistence.path,
    )

    if persistence.extension is not extension:
        raise ChromiumResearchSecondChangedBasisRootEdgeError(
            "Second-root 34B persistence did not retain the exact in-memory edge extension."
        )
    if loaded_edge.verification.edge_record_sha256 != persistence.edge_record_sha256:
        raise ChromiumResearchSecondChangedBasisRootEdgeError(
            "Fresh second-root 34B relink identifies a different edge record."
        )
    if (
        loaded_edge.verification.predecessor_record_sha256
        != root_result.persistence.root_record_sha256
    ):
        raise ChromiumResearchSecondChangedBasisRootEdgeError(
            "Fresh second-root 34B relink identifies a different 46B predecessor root."
        )
    if loaded_edge.revision.revised_note.note_text != revised_note_text:
        raise ChromiumResearchSecondChangedBasisRootEdgeError(
            "Fresh second-root 34B relink reconstructs different human edge wording."
        )

    return ChromiumResearchSecondChangedBasisRootEdgeResult(
        root_result=root_result,
        extension=extension,
        persistence=persistence,
        loaded_edge=loaded_edge,
    )


def _require_path(value: Path, *, label: str) -> Path:
    if not isinstance(value, Path):
        raise TypeError(f"{label} must be pathlib.Path.")
    return value


__all__ = [
    "ChromiumResearchSecondChangedBasisRootEdgeError",
    "ChromiumResearchSecondChangedBasisRootEdgeResult",
    "persist_chromium_research_second_changed_basis_root_edge",
]
