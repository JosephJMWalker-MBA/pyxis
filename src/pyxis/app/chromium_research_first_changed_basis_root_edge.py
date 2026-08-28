from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .chromium_research_first_changed_basis_revision_root import (
    ChromiumResearchFirstChangedBasisRevisionRootResult,
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


class ChromiumResearchFirstChangedBasisRootEdgeError(ValueError):
    """Raised when an exact 44C root cannot support the first 34B ordinary edge."""


@dataclass(frozen=True, slots=True)
class ChromiumResearchFirstChangedBasisRootEdgeResult:
    """One explicit first ordinary edge proven from an exact successful 44C root.

    The result retains the exact 44C product result, one human-authored in-memory 34B
    root-edge extension, its no-overwrite persistence evidence in the existing 24B
    edge format, and one fresh 34B relink back into the standard loaded-edge type.

    It does not create a sequence declaration, a 35A root-backed governed session, an
    epoch, or any current/latest/head state.
    """

    root_result: ChromiumResearchFirstChangedBasisRevisionRootResult
    extension: ChromiumResearchSessionWorkingSetTransitionRevisionRootEdgeExtensionRecord
    persistence: ChromiumResearchSessionWorkingSetTransitionRevisionRootEdgePersistenceEvidence
    loaded_edge: ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord


def persist_chromium_research_first_changed_basis_root_edge(
    root_result: ChromiumResearchFirstChangedBasisRevisionRootResult,
    *,
    revised_note_text: str,
    root_source: Path,
    destination: Path,
) -> ChromiumResearchFirstChangedBasisRootEdgeResult:
    """Persist and freshly relink the first ordinary 34B edge after exact 44C success.

    Only the caller-supplied current root file is reopened as durable predecessor
    evidence. The earlier transition and changed-basis files are not traversed again.
    The 44C root receipt path is not used as locator authority.

    The mounted old-basis governed session is irrelevant here. A successful 44C root
    is a durable historical relationship and can receive this local continuation even
    if another mounted branch continues elsewhere. No branch is selected as current.
    """

    if type(root_result) is not ChromiumResearchFirstChangedBasisRevisionRootResult:
        raise TypeError(
            "root_result must be exactly ChromiumResearchFirstChangedBasisRevisionRootResult."
        )
    if not isinstance(revised_note_text, str):
        raise TypeError("revised_note_text must be str.")

    loaded_root = root_result.loaded_root
    if loaded_root.verification.root_record_sha256 != root_result.persistence.root_record_sha256:
        raise ChromiumResearchFirstChangedBasisRootEdgeError(
            "44C loaded root does not match its persisted root identity."
        )
    if loaded_root.root.revision.revised_note.note_text != root_result.root.revision.revised_note.note_text:
        raise ChromiumResearchFirstChangedBasisRootEdgeError(
            "44C loaded root reconstructs different human root wording."
        )

    extension = (
        create_chromium_research_session_working_set_transition_revision_root_edge_extension(
            loaded_root,
            revised_note_text=revised_note_text,
        )
    )
    persistence = (
        persist_chromium_research_session_working_set_transition_revision_root_edge_extension(
            extension,
            root_source=_require_path(root_source, label="root_source"),
            destination=_require_path(destination, label="destination"),
        )
    )
    loaded_edge = load_chromium_research_session_working_set_transition_revision_root_edge(
        loaded_root,
        persistence.path,
    )

    if persistence.extension is not extension:
        raise ChromiumResearchFirstChangedBasisRootEdgeError(
            "34B persistence did not retain the exact in-memory root-edge extension."
        )
    if loaded_edge.verification.edge_record_sha256 != persistence.edge_record_sha256:
        raise ChromiumResearchFirstChangedBasisRootEdgeError(
            "Fresh 34B relink identifies a different edge record."
        )
    if loaded_edge.verification.predecessor_record_sha256 != root_result.persistence.root_record_sha256:
        raise ChromiumResearchFirstChangedBasisRootEdgeError(
            "Fresh 34B relink identifies a different 34A predecessor root."
        )
    if loaded_edge.revision.revised_note.note_text != revised_note_text:
        raise ChromiumResearchFirstChangedBasisRootEdgeError(
            "Fresh 34B relink reconstructs different human edge wording."
        )

    return ChromiumResearchFirstChangedBasisRootEdgeResult(
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
    "ChromiumResearchFirstChangedBasisRootEdgeError",
    "ChromiumResearchFirstChangedBasisRootEdgeResult",
    "persist_chromium_research_first_changed_basis_root_edge",
]
