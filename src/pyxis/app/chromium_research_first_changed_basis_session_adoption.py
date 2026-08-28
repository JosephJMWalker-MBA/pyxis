from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .chromium_research_first_changed_basis_root_edge import (
    ChromiumResearchFirstChangedBasisRootEdgeResult,
)
from .chromium_research_session_controller import ChromiumResearchSessionController
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


class ChromiumResearchFirstChangedBasisSessionAdoptionError(ValueError):
    """Raised when an exact 44D result cannot support one explicit 35A adoption."""


@dataclass(frozen=True, slots=True)
class ChromiumResearchFirstChangedBasisSessionAdoptionResult:
    """One explicit shell-ready 35A governed-session adoption from exact 44D evidence.

    `edge_result` retains the exact successful first changed-basis 34B product result.
    `sequence` is a fresh root-started 26A sequence opened through the caller-supplied
    current edge path. `declaration` persists the existing 26B format without paths.
    `loaded_declaration` freshly reconciles that declaration to the exact loaded root
    and explicit edge path. `controller` is the existing 29A governed controller.

    The result grants no fresh-process root-backed re-entry authority, global branch
    preference, latest/head/chronology authority, path identity, or semantic support.
    """

    edge_result: ChromiumResearchFirstChangedBasisRootEdgeResult
    sequence: ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceRecord
    declaration: ChromiumPageResearchWorkingSetNoteRevisionEdgeSequencePersistenceEvidence
    loaded_declaration: ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceDeclarationRecord
    controller: ChromiumResearchSessionController


def adopt_chromium_research_first_changed_basis_governed_session(
    edge_result: ChromiumResearchFirstChangedBasisRootEdgeResult,
    *,
    edge_source: Path,
    declaration_destination: Path,
) -> ChromiumResearchFirstChangedBasisSessionAdoptionResult:
    """Declare and freshly relink one exact 44D lineage as a 35A governed session.

    The exact already-loaded 34A root retained by `edge_result` is the explicit
    sequence starting record. The caller supplies only the current durable first-edge
    source and a no-overwrite declaration destination. The historical 44D output path
    is not locator authority.

    Successful return creates only an in-process governed controller. It does not
    create a 35B root-backed re-entry result or choose any branch globally.
    """

    if type(edge_result) is not ChromiumResearchFirstChangedBasisRootEdgeResult:
        raise TypeError(
            "edge_result must be exactly ChromiumResearchFirstChangedBasisRootEdgeResult."
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
        raise ChromiumResearchFirstChangedBasisSessionAdoptionError(
            "44D retained root does not match its persisted 34A root identity."
        )
    if (
        edge_result.loaded_edge.verification.edge_record_sha256
        != edge_result.persistence.edge_record_sha256
    ):
        raise ChromiumResearchFirstChangedBasisSessionAdoptionError(
            "44D loaded edge does not match its persisted 34B edge identity."
        )
    if (
        edge_result.loaded_edge.verification.predecessor_record_sha256
        != root_result.persistence.root_record_sha256
    ):
        raise ChromiumResearchFirstChangedBasisSessionAdoptionError(
            "44D loaded edge does not retain the exact 34A predecessor identity."
        )

    sequence = load_chromium_research_working_set_note_revision_edge_sequence(
        loaded_root,
        (edge_source,),
    )
    if sequence.starting_predecessor is not loaded_root:
        raise ChromiumResearchFirstChangedBasisSessionAdoptionError(
            "35A sequence did not retain the exact loaded 34A root."
        )
    if len(sequence.edges) != 1:
        raise ChromiumResearchFirstChangedBasisSessionAdoptionError(
            "First changed-basis adoption must contain exactly the explicit 44D edge."
        )
    loaded_edge = sequence.edges[0]
    if (
        loaded_edge.verification.edge_record_sha256
        != edge_result.persistence.edge_record_sha256
    ):
        raise ChromiumResearchFirstChangedBasisSessionAdoptionError(
            "Explicit edge source identifies a different first post-root edge."
        )
    if (
        loaded_edge.revision.revised_note.note_text
        != edge_result.extension.revision.revised_note.note_text
    ):
        raise ChromiumResearchFirstChangedBasisSessionAdoptionError(
            "Fresh root-backed edge reconstructs different human rationale wording."
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
        raise ChromiumResearchFirstChangedBasisSessionAdoptionError(
            "Fresh declaration relink identifies a different 26B declaration."
        )
    if loaded_declaration.sequence.starting_predecessor is not loaded_root:
        raise ChromiumResearchFirstChangedBasisSessionAdoptionError(
            "Fresh declaration relink did not retain the exact 34A root."
        )
    if (
        controller.declared_endpoint.verification.edge_record_sha256
        != edge_result.persistence.edge_record_sha256
    ):
        raise ChromiumResearchFirstChangedBasisSessionAdoptionError(
            "Adopted governed controller identifies a different declared endpoint."
        )
    if (
        controller.declared_endpoint.revision.revised_note.note_text
        != edge_result.extension.revision.revised_note.note_text
    ):
        raise ChromiumResearchFirstChangedBasisSessionAdoptionError(
            "Adopted governed controller reconstructs different endpoint wording."
        )

    return ChromiumResearchFirstChangedBasisSessionAdoptionResult(
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
    "ChromiumResearchFirstChangedBasisSessionAdoptionError",
    "ChromiumResearchFirstChangedBasisSessionAdoptionResult",
    "adopt_chromium_research_first_changed_basis_governed_session",
]
