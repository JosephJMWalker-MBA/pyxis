from __future__ import annotations

from dataclasses import dataclass

from .chromium_research_working_set_note_revision import (
    ChromiumPageResearchWorkingSetNoteRevisionRecord,
    create_chromium_research_working_set_note_revision,
)
from .chromium_research_working_set_note_revision_edge_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord,
    _validate_loaded_edge_predecessor,
)


_EXTENSION_MODE = "caller_authored_extension_of_verified_research_working_set_note_revision_edge"


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchWorkingSetNoteRevisionEdgeExtensionRecord:
    """One new human revision explicitly extended from one loaded 24C edge.

    `prior_edge` retains the exact caller-supplied loaded edge object. `revision` is
    one newly created public-22A revision whose prior note is exactly that loaded
    edge's reconstructed endpoint note.

    The record establishes only one explicit in-memory human extension from one
    coherent loaded edge. It does not persist the extension, traverse ancestry,
    establish chronology, select a history head, assign a revision number, or make
    semantic/source-truth claims.
    """

    extension_mode: str
    prior_edge: ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord
    revision: ChromiumPageResearchWorkingSetNoteRevisionRecord


def create_chromium_research_working_set_note_revision_edge_extension(
    prior_edge: ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord,
    *,
    revised_note_text: str,
) -> ChromiumPageResearchWorkingSetNoteRevisionEdgeExtensionRecord:
    """Create one human revision explicitly extending one already-loaded 24C edge.

    25A performs no file reads. Before creating the new revision it reuses 24C's
    established in-memory loaded-edge validator to re-establish the predecessor
    edge's immediate local relationship. That validator deliberately does not
    recursively re-prove the entire ancestry carried beneath the loaded edge.

    Public 22A then creates the new revision over exactly
    `prior_edge.revision.revised_note`, preserving exact-text no-op rejection and
    the exact working-set object. No persistence, predecessor discovery, digest
    search, recursive loading, history traversal, timestamps, semantic diff, or
    browser work occurs here.
    """

    if not isinstance(prior_edge, ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord):
        raise TypeError(
            "prior_edge must be ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord."
        )

    # Re-establish exactly the immediate local 24C relationship. The returned
    # tuple describes the predecessor beneath `prior_edge`; 25A does not need to
    # traverse it. Success here is the in-memory coherence gate for using the
    # loaded edge's endpoint as the next human revision input.
    _validate_loaded_edge_predecessor(prior_edge)

    revision = create_chromium_research_working_set_note_revision(
        prior_edge.revision.revised_note,
        revised_note_text=revised_note_text,
    )

    return ChromiumPageResearchWorkingSetNoteRevisionEdgeExtensionRecord(
        extension_mode=_EXTENSION_MODE,
        prior_edge=prior_edge,
        revision=revision,
    )
