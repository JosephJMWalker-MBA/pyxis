from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .chromium_research_third_changed_basis_revision_root import (
    ChromiumResearchThirdChangedBasisRevisionRootResult,
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


class ChromiumResearchThirdChangedBasisRootEdgeError(ValueError):
    """Raised when an exact 47B root cannot support the first third-basis 34B edge."""


@dataclass(frozen=True, slots=True)
class ChromiumResearchThirdChangedBasisRootEdgeResult:
    """One explicit first ordinary edge proven from an exact successful 47B root.

    The result retains the exact 47B product result, one human-authored in-memory
    public-34B root-edge extension, its no-overwrite persistence evidence in the
    existing ordinary edge format, and one fresh public-34B relink.

    It does not create a root-started sequence declaration, third-epoch session,
    re-entry/restart authority, adoption, or any current/latest/head state.
    """

    root_result: ChromiumResearchThirdChangedBasisRevisionRootResult
    extension: ChromiumResearchSessionWorkingSetTransitionRevisionRootEdgeExtensionRecord
    persistence: ChromiumResearchSessionWorkingSetTransitionRevisionRootEdgePersistenceEvidence
    loaded_edge: ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord


def persist_chromium_research_third_changed_basis_root_edge(
    root_result: ChromiumResearchThirdChangedBasisRevisionRootResult,
    *,
    revised_note_text: str,
    root_source: Path,
    destination: Path,
) -> ChromiumResearchThirdChangedBasisRootEdgeResult:
    """Persist and freshly relink the first ordinary 34B edge after exact 47B success.

    Only the caller-supplied current third-root file is reopened as durable
    predecessor evidence. Earlier third-transition, changed-basis, second-epoch
    overlay, and launch-provenance paths are not traversed or inferred.

    The currently mounted second-epoch continuation is irrelevant to the historical
    relationship proved here. A successful exact 47B root may receive its own local
    first edge even if that older mounted branch later continues elsewhere. No branch
    is selected as current/latest/head.
    """

    if type(root_result) is not ChromiumResearchThirdChangedBasisRevisionRootResult:
        raise TypeError(
            "root_result must be exactly "
            "ChromiumResearchThirdChangedBasisRevisionRootResult."
        )
    if not isinstance(revised_note_text, str):
        raise TypeError("revised_note_text must be str.")

    loaded_root = root_result.loaded_root
    if (
        loaded_root.verification.root_record_sha256
        != root_result.persistence.root_record_sha256
    ):
        raise ChromiumResearchThirdChangedBasisRootEdgeError(
            "47B loaded root does not match its persisted root identity."
        )
    if (
        loaded_root.root.revision.revised_note.note_text
        != root_result.root.revision.revised_note.note_text
    ):
        raise ChromiumResearchThirdChangedBasisRootEdgeError(
            "47B loaded root reconstructs different human root wording."
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
        raise ChromiumResearchThirdChangedBasisRootEdgeError(
            "Third-root 34B persistence did not retain the exact in-memory edge extension."
        )
    if loaded_edge.verification.edge_record_sha256 != persistence.edge_record_sha256:
        raise ChromiumResearchThirdChangedBasisRootEdgeError(
            "Fresh third-root 34B relink identifies a different edge record."
        )
    if (
        loaded_edge.verification.predecessor_record_sha256
        != root_result.persistence.root_record_sha256
    ):
        raise ChromiumResearchThirdChangedBasisRootEdgeError(
            "Fresh third-root 34B relink identifies a different 47B predecessor root."
        )
    if loaded_edge.revision.revised_note.note_text != revised_note_text:
        raise ChromiumResearchThirdChangedBasisRootEdgeError(
            "Fresh third-root 34B relink reconstructs different human edge wording."
        )

    return ChromiumResearchThirdChangedBasisRootEdgeResult(
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
    "ChromiumResearchThirdChangedBasisRootEdgeError",
    "ChromiumResearchThirdChangedBasisRootEdgeResult",
    "persist_chromium_research_third_changed_basis_root_edge",
]
