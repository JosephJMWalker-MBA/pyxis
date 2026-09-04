from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .chromium_research_session_controller import ChromiumResearchSessionController
from .chromium_research_third_changed_basis_root_edge import (
    ChromiumResearchThirdChangedBasisRootEdgeResult,
)
from .chromium_research_working_set_note_revision_edge_sequence_declaration_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceDeclarationRecord,
    load_chromium_research_working_set_note_revision_edge_sequence_declaration,
)
from .chromium_research_working_set_note_revision_edge_sequence_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceRecord,
    load_chromium_research_working_set_note_revision_edge_sequence,
)
from .chromium_research_working_set_note_revision_edge_sequence_persistence import (
    ChromiumPageResearchWorkingSetNoteRevisionEdgeSequencePersistenceEvidence,
    persist_chromium_research_working_set_note_revision_edge_sequence,
)


class ChromiumResearchThirdChangedBasisSessionAdoptionError(ValueError):
    """Raised when an exact 47C edge cannot support one explicit third-basis adoption."""


@dataclass(frozen=True, slots=True)
class ChromiumResearchThirdChangedBasisSessionAdoptionResult:
    """One explicit governed-session adoption from exact successful 47C evidence.

    The exact 47C edge result remains the relationship authority. The sequence and
    declaration are freshly relinked through existing root-started public boundaries,
    and the controller is the standard governed research-session controller.

    This result is in-process adoption only. It creates no 40A fresh-process re-entry,
    40B overlay, third-epoch launch provenance, or current/latest/head authority.
    """

    edge_result: ChromiumResearchThirdChangedBasisRootEdgeResult
    sequence: ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceRecord
    declaration: ChromiumPageResearchWorkingSetNoteRevisionEdgeSequencePersistenceEvidence
    loaded_declaration: ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceDeclarationRecord
    controller: ChromiumResearchSessionController


def adopt_chromium_research_third_changed_basis_governed_session(
    edge_result: ChromiumResearchThirdChangedBasisRootEdgeResult,
    *,
    edge_source: Path,
    declaration_destination: Path,
) -> ChromiumResearchThirdChangedBasisSessionAdoptionResult:
    """Declare and freshly relink one exact 47C lineage as a governed session.

    The exact already-loaded third public-34A root retained by the edge result is the
    sequence starting record. Only the caller-supplied current durable 47C edge path
    is reopened, and the declaration destination is explicit and no-overwrite.

    Successful return creates one in-process governed controller. It does not perform
    40A fresh-process reconstruction, persist a 40B overlay, or choose a branch
    globally.
    """

    if type(edge_result) is not ChromiumResearchThirdChangedBasisRootEdgeResult:
        raise TypeError(
            "edge_result must be exactly "
            "ChromiumResearchThirdChangedBasisRootEdgeResult."
        )
    edge_source = _require_path(edge_source, label="edge_source")
    declaration_destination = _require_path(
        declaration_destination,
        label="declaration_destination",
    )

    root_result = edge_result.root_result
    loaded_root = root_result.loaded_root
    if (
        loaded_root.verification.root_record_sha256
        != root_result.persistence.root_record_sha256
    ):
        raise ChromiumResearchThirdChangedBasisSessionAdoptionError(
            "47C retained root does not match its persisted third public-34A identity."
        )
    if (
        edge_result.loaded_edge.verification.edge_record_sha256
        != edge_result.persistence.edge_record_sha256
    ):
        raise ChromiumResearchThirdChangedBasisSessionAdoptionError(
            "47C loaded edge does not match its persisted public-34B identity."
        )
    if (
        edge_result.loaded_edge.verification.predecessor_record_sha256
        != root_result.persistence.root_record_sha256
    ):
        raise ChromiumResearchThirdChangedBasisSessionAdoptionError(
            "47C loaded edge does not retain the exact third public-34A predecessor identity."
        )

    sequence = load_chromium_research_working_set_note_revision_edge_sequence(
        loaded_root,
        (edge_source,),
    )
    if sequence.starting_predecessor is not loaded_root:
        raise ChromiumResearchThirdChangedBasisSessionAdoptionError(
            "47D sequence did not retain the exact loaded third public-34A root."
        )
    if len(sequence.edges) != 1:
        raise ChromiumResearchThirdChangedBasisSessionAdoptionError(
            "Third changed-basis adoption must contain exactly the explicit 47C edge."
        )
    loaded_edge = sequence.edges[0]
    if (
        loaded_edge.verification.edge_record_sha256
        != edge_result.persistence.edge_record_sha256
    ):
        raise ChromiumResearchThirdChangedBasisSessionAdoptionError(
            "Explicit edge source identifies a different first post-third-root edge."
        )
    if (
        loaded_edge.revision.revised_note.note_text
        != edge_result.extension.revision.revised_note.note_text
    ):
        raise ChromiumResearchThirdChangedBasisSessionAdoptionError(
            "Fresh third-root-backed edge reconstructs different human rationale wording."
        )

    declaration = persist_chromium_research_working_set_note_revision_edge_sequence(
        sequence,
        declaration_destination,
    )
    loaded_declaration = (
        load_chromium_research_working_set_note_revision_edge_sequence_declaration(
            loaded_root,
            (edge_source,),
            declaration.path,
        )
    )
    controller = ChromiumResearchSessionController(loaded_declaration)

    if (
        loaded_declaration.verification.sequence_record_sha256
        != declaration.sequence_record_sha256
    ):
        raise ChromiumResearchThirdChangedBasisSessionAdoptionError(
            "Fresh 47D declaration relink identifies a different declaration."
        )
    if loaded_declaration.sequence.starting_predecessor is not loaded_root:
        raise ChromiumResearchThirdChangedBasisSessionAdoptionError(
            "Fresh 47D declaration relink did not retain the exact third public-34A root."
        )
    if (
        controller.declared_endpoint.verification.edge_record_sha256
        != edge_result.persistence.edge_record_sha256
    ):
        raise ChromiumResearchThirdChangedBasisSessionAdoptionError(
            "Adopted third-basis controller identifies a different declared endpoint."
        )
    if (
        controller.declared_endpoint.revision.revised_note.note_text
        != edge_result.extension.revision.revised_note.note_text
    ):
        raise ChromiumResearchThirdChangedBasisSessionAdoptionError(
            "Adopted third-basis controller reconstructs different endpoint wording."
        )

    return ChromiumResearchThirdChangedBasisSessionAdoptionResult(
        edge_result=edge_result,
        sequence=sequence,
        declaration=declaration,
        loaded_declaration=loaded_declaration,
        controller=controller,
    )


def _require_path(value: Path, *, label: str) -> Path:
    if not isinstance(value, Path):
        raise TypeError(f"{label} must be pathlib.Path.")
    return value


__all__ = [
    "ChromiumResearchThirdChangedBasisSessionAdoptionError",
    "ChromiumResearchThirdChangedBasisSessionAdoptionResult",
    "adopt_chromium_research_third_changed_basis_governed_session",
]
