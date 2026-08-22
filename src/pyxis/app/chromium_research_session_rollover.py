from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .chromium_research_session_controller import (
    ChromiumResearchSessionController,
    ChromiumResearchSessionEndpointRevisionPersistenceResult,
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


_EDGE_FORMAT = "pyxis.chromium.research_working_set_note_revision_edge.v1"


@dataclass(frozen=True, slots=True)
class ChromiumResearchSessionRolloverResult:
    """One explicit continuation-session rollover from a persisted successor.

    `prior_controller` remains the exact pre-rollover 29A controller. `prior_revision`
    is the exact successful endpoint-revision write explicitly selected by the caller.
    `explicit_sequence` is one fresh 26A sequence whose starting predecessor is the
    old declared endpoint and whose sole member is the explicitly supplied successor
    file. `declaration` is a new durable 26B declaration for only that continuation
    segment. `loaded_declaration` is the freshly re-established 26C declaration, and
    `continuation_controller` is a new 29A controller over that new declared session.

    The result does not assert that the continuation is latest, current globally,
    canonical, unique, complete history, or semantically better than another edge.
    """

    prior_controller: ChromiumResearchSessionController
    prior_revision: ChromiumResearchSessionEndpointRevisionPersistenceResult
    explicit_sequence: ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceRecord
    declaration: ChromiumPageResearchWorkingSetNoteRevisionEdgeSequencePersistenceEvidence
    loaded_declaration: ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceDeclarationRecord
    continuation_controller: ChromiumResearchSessionController


def rollover_chromium_research_session_to_persisted_successor(
    controller: ChromiumResearchSessionController,
    revision: ChromiumResearchSessionEndpointRevisionPersistenceResult,
    *,
    successor_edge_source: Path,
    declaration_destination: Path,
) -> ChromiumResearchSessionRolloverResult:
    """Explicitly adopt one chosen 29A successor into a new declared session.

    The caller explicitly supplies the exact successful 29A result to continue from,
    the durable successor edge location, and a no-overwrite destination for a new
    declaration. Pyxis does not choose among successful sibling writes and does not
    discover either path.

    Pyxis first re-establishes that the chosen revision belongs to the supplied
    controller's exact declared endpoint. It then freshly relinks the explicitly
    supplied successor against that endpoint through public 26A, requires the fresh
    content identity and exact human text to match the chosen 29A write, persists a
    new one-edge 26B declaration, freshly relinks that declaration through public
    26C, and constructs a new 29A controller over the continuation session.

    The old controller, old declaration, and old presentation remain untouched. The
    new controller is an explicit caller-chosen continuation session only; it is not
    promoted to a global current/latest/canonical head.
    """

    if not isinstance(controller, ChromiumResearchSessionController):
        raise TypeError("controller must be ChromiumResearchSessionController.")
    _require_revision_coherence(controller, revision)

    successor_source = Path(successor_edge_source)
    declaration_path = Path(declaration_destination)

    explicit_sequence = load_chromium_research_working_set_note_revision_edge_sequence(
        controller.declared_endpoint,
        (successor_source,),
    )
    successor = explicit_sequence.edges[0]

    if successor.verification.edge_format != _EDGE_FORMAT:
        raise ValueError("Explicit successor edge format is unsupported for session rollover.")
    if revision.persistence.edge_format != _EDGE_FORMAT:
        raise ValueError("Selected endpoint-revision edge format is unsupported for rollover.")
    if successor.verification.edge_record_sha256 != revision.persistence.edge_record_sha256:
        raise ValueError(
            "Explicit successor edge identity does not match the selected endpoint revision."
        )
    if (
        successor.revision.revised_note.note_text
        != revision.extension.revision.revised_note.note_text
    ):
        raise ValueError(
            "Explicit successor human wording does not match the selected endpoint revision."
        )
    if successor.predecessor is not controller.declared_endpoint:
        raise ValueError(
            "Explicit successor does not retain the exact prior declared endpoint."
        )

    declaration = persist_chromium_research_working_set_note_revision_edge_sequence(
        explicit_sequence,
        declaration_path,
    )

    loaded_declaration = (
        load_chromium_research_working_set_note_revision_edge_sequence_declaration(
            controller.declared_endpoint,
            (successor_source,),
            declaration.path,
        )
    )
    if len(loaded_declaration.sequence.edges) != 1:
        raise ValueError("Continuation declaration must retain exactly one successor edge.")
    loaded_successor = loaded_declaration.sequence.edges[0]
    if loaded_successor.verification.edge_record_sha256 != revision.persistence.edge_record_sha256:
        raise ValueError(
            "Freshly relinked continuation declaration does not identify the selected successor."
        )

    continuation_controller = ChromiumResearchSessionController(loaded_declaration)
    if continuation_controller.declared_endpoint is not loaded_successor:
        raise ValueError(
            "Continuation controller did not retain the exact freshly relinked successor endpoint."
        )

    return ChromiumResearchSessionRolloverResult(
        prior_controller=controller,
        prior_revision=revision,
        explicit_sequence=explicit_sequence,
        declaration=declaration,
        loaded_declaration=loaded_declaration,
        continuation_controller=continuation_controller,
    )


def _require_revision_coherence(
    controller: ChromiumResearchSessionController,
    revision: ChromiumResearchSessionEndpointRevisionPersistenceResult,
) -> None:
    if not isinstance(revision, ChromiumResearchSessionEndpointRevisionPersistenceResult):
        raise TypeError(
            "revision must be ChromiumResearchSessionEndpointRevisionPersistenceResult."
        )
    if revision.prior_session is not controller.presentation:
        raise ValueError(
            "Selected endpoint revision does not belong to the controller's exact session."
        )
    if revision.extension.prior_edge is not controller.declared_endpoint:
        raise ValueError(
            "Selected endpoint revision does not extend the controller's exact declared endpoint."
        )
    if revision.persistence.extension is not revision.extension:
        raise ValueError(
            "Selected endpoint revision persistence does not retain the exact extension object."
        )
    if revision.persistence.edge_format != _EDGE_FORMAT:
        raise ValueError("Selected endpoint revision edge format is unsupported for rollover.")
