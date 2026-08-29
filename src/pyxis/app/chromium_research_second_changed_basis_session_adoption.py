from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .chromium_research_second_changed_basis_root_edge import (
    ChromiumResearchSecondChangedBasisRootEdgeResult,
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


class ChromiumResearchSecondChangedBasisSessionAdoptionError(ValueError):
    """Raised when an exact 46C edge cannot support one explicit second-basis adoption."""


@dataclass(frozen=True, slots=True)
class ChromiumResearchSecondChangedBasisSessionAdoptionResult:
    """One explicit governed-session adoption from exact successful 46C evidence.

    `edge_result` retains the exact successful second-root 34B product result.
    `sequence` is a fresh root-started sequence opened through the caller-supplied
    current edge path. `declaration` persists the existing sequence format without
    locator authority. `loaded_declaration` freshly reconciles the declaration to the
    exact loaded second root and explicit edge path. `controller` is the standard
    governed research-session controller.

    This result creates no second-epoch fresh-process re-entry result or persisted
    second-epoch overlay and grants no global branch preference, latest/head authority,
    path identity, chronology authority, or semantic-support authority.
    """

    edge_result: ChromiumResearchSecondChangedBasisRootEdgeResult
    sequence: ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceRecord
    declaration: ChromiumPageResearchWorkingSetNoteRevisionEdgeSequencePersistenceEvidence
    loaded_declaration: ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceDeclarationRecord
    controller: ChromiumResearchSessionController


def adopt_chromium_research_second_changed_basis_governed_session(
    edge_result: ChromiumResearchSecondChangedBasisRootEdgeResult,
    *,
    edge_source: Path,
    declaration_destination: Path,
) -> ChromiumResearchSecondChangedBasisSessionAdoptionResult:
    """Declare and freshly relink one exact 46C lineage as a governed session.

    The exact already-loaded second 34A root retained by `edge_result` is the explicit
    sequence starting record. The caller supplies only the current durable 46C edge
    source and a no-overwrite declaration destination. The historical 46C output path
    is not locator authority.

    Successful return creates an in-process governed controller only. It does not
    create second-epoch fresh-process re-entry, a second-epoch overlay, or choose any
    branch globally.
    """

    if type(edge_result) is not ChromiumResearchSecondChangedBasisRootEdgeResult:
        raise TypeError(
            "edge_result must be exactly ChromiumResearchSecondChangedBasisRootEdgeResult."
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
        raise ChromiumResearchSecondChangedBasisSessionAdoptionError(
            "46C retained root does not match its persisted second 34A root identity."
        )
    if (
        edge_result.loaded_edge.verification.edge_record_sha256
        != edge_result.persistence.edge_record_sha256
    ):
        raise ChromiumResearchSecondChangedBasisSessionAdoptionError(
            "46C loaded edge does not match its persisted 34B edge identity."
        )
    if (
        edge_result.loaded_edge.verification.predecessor_record_sha256
        != root_result.persistence.root_record_sha256
    ):
        raise ChromiumResearchSecondChangedBasisSessionAdoptionError(
            "46C loaded edge does not retain the exact second 34A predecessor identity."
        )

    sequence = load_chromium_research_working_set_note_revision_edge_sequence(
        loaded_root,
        (edge_source,),
    )
    if sequence.starting_predecessor is not loaded_root:
        raise ChromiumResearchSecondChangedBasisSessionAdoptionError(
            "46D sequence did not retain the exact loaded second 34A root."
        )
    if len(sequence.edges) != 1:
        raise ChromiumResearchSecondChangedBasisSessionAdoptionError(
            "Second changed-basis adoption must contain exactly the explicit 46C edge."
        )
    loaded_edge = sequence.edges[0]
    if (
        loaded_edge.verification.edge_record_sha256
        != edge_result.persistence.edge_record_sha256
    ):
        raise ChromiumResearchSecondChangedBasisSessionAdoptionError(
            "Explicit edge source identifies a different first post-second-root edge."
        )
    if (
        loaded_edge.revision.revised_note.note_text
        != edge_result.extension.revision.revised_note.note_text
    ):
        raise ChromiumResearchSecondChangedBasisSessionAdoptionError(
            "Fresh second-root-backed edge reconstructs different human rationale wording."
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
        raise ChromiumResearchSecondChangedBasisSessionAdoptionError(
            "Fresh 46D declaration relink identifies a different declaration."
        )
    if loaded_declaration.sequence.starting_predecessor is not loaded_root:
        raise ChromiumResearchSecondChangedBasisSessionAdoptionError(
            "Fresh 46D declaration relink did not retain the exact second 34A root."
        )
    if (
        controller.declared_endpoint.verification.edge_record_sha256
        != edge_result.persistence.edge_record_sha256
    ):
        raise ChromiumResearchSecondChangedBasisSessionAdoptionError(
            "Adopted second-basis controller identifies a different declared endpoint."
        )
    if (
        controller.declared_endpoint.revision.revised_note.note_text
        != edge_result.extension.revision.revised_note.note_text
    ):
        raise ChromiumResearchSecondChangedBasisSessionAdoptionError(
            "Adopted second-basis controller reconstructs different endpoint wording."
        )

    return ChromiumResearchSecondChangedBasisSessionAdoptionResult(
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
    "ChromiumResearchSecondChangedBasisSessionAdoptionError",
    "ChromiumResearchSecondChangedBasisSessionAdoptionResult",
    "adopt_chromium_research_second_changed_basis_governed_session",
]
