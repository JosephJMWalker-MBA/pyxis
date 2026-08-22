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
    is its exact retained successful endpoint-revision write. `explicit_sequence` is
    one fresh 26A sequence whose starting predecessor is the old declared endpoint
    and whose sole member is the explicitly supplied successor file. `declaration`
    is a new durable 26B declaration for only that continuation segment.
    `loaded_declaration` is the freshly re-established 26C declaration, and
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
    *,
    successor_edge_source: Path,
    declaration_destination: Path,
) -> ChromiumResearchSessionRolloverResult:
    """Explicitly adopt one retained 29A successor into a new declared session.

    The caller supplies the durable successor edge location and a no-overwrite
    destination for a new declaration. Pyxis does not discover either path.

    This function requires one successful 29A endpoint write retained by `controller`,
    freshly relinks the explicitly supplied successor against the controller's exact
    declared endpoint through public 26A, requires that freshly observed successor
    identity and exact human text to match the retained 29A write, persists a new
    one-edge 26B declaration, freshly relinks that declaration through public 26C,
    and constructs a new 29A controller over the resulting continuation session.

    The old controller, old declaration, and old presentation remain untouched. The
    new controller is an explicit caller-chosen continuation session only; it is not
    promoted to a global current/latest/canonical head.
    """

    if not isinstance(controller, ChromiumResearchSessionController):
        raise TypeError("controller must be ChromiumResearchSessionController.")

    prior_revision = controller.last_endpoint_revision
    if prior_revision is None:
        raise ValueError(
            "Research session rollover requires one retained successful endpoint revision."
        )
    _require_retained_revision_coherence(controller, prior_revision)

    successor_source = Path(successor_edge_source)
    declaration_path = Path(declaration_destination)

    explicit_sequence = load_chromium_research_working_set_note_revision_edge_sequence(
        controller.declared_endpoint,
        (successor_source,),
    )
    successor = explicit_sequence.edges[0]

    if successor.verification.edge_format != _EDGE_FORMAT:
        raise ValueError("Explicit successor edge format is unsupported for session rollover.")
    if prior_revision.persistence.edge_format != _EDGE_FORMAT:
        raise ValueError("Retained endpoint-revision edge format is unsupported for rollover.")
    if (
        successor.verification.edge_record_sha256
        != prior_revision.persistence.edge_record_sha256
    ):
        raise ValueError(
            "Explicit successor edge identity does not match the retained endpoint revision."
        )
    if (
        successor.revision.revised_note.note_text
        != prior_revision.extension.revision.revised_note.note_text
    ):
        raise ValueError(
            "Explicit successor human wording does not match the retained endpoint revision."
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
    if (
        loaded_successor.verification.edge_record_sha256
        != prior_revision.persistence.edge_record_sha256
    ):
        raise ValueError(
            "Freshly relinked continuation declaration does not identify the retained successor."
        )

    continuation_controller = ChromiumResearchSessionController(loaded_declaration)
    if continuation_controller.declared_endpoint is not loaded_successor:
        raise ValueError(
            "Continuation controller did not retain the exact freshly relinked successor endpoint."
        )

    return ChromiumResearchSessionRolloverResult(
        prior_controller=controller,
        prior_revision=prior_revision,
        explicit_sequence=explicit_sequence,
        declaration=declaration,
        loaded_declaration=loaded_declaration,
        continuation_controller=continuation_controller,
    )


def _require_retained_revision_coherence(
    controller: ChromiumResearchSessionController,
    revision: ChromiumResearchSessionEndpointRevisionPersistenceResult,
) -> None:
    if not isinstance(revision, ChromiumResearchSessionEndpointRevisionPersistenceResult):
        raise TypeError(
            "controller.last_endpoint_revision must be "
            "ChromiumResearchSessionEndpointRevisionPersistenceResult."
        )
    if revision.prior_session is not controller.presentation:
        raise ValueError(
            "Retained endpoint revision does not belong to the controller's exact session."
        )
    if revision.extension.prior_edge is not controller.declared_endpoint:
        raise ValueError(
            "Retained endpoint revision does not extend the controller's exact declared endpoint."
        )
    if revision.persistence.extension is not revision.extension:
        raise ValueError(
            "Retained endpoint revision persistence does not retain the exact extension object."
        )
    if revision.persistence.edge_format != _EDGE_FORMAT:
        raise ValueError("Retained endpoint revision edge format is unsupported for rollover.")
