from __future__ import annotations

import hmac
from pathlib import Path

from .chromium_research_session_working_set_transition_revision_root_load import (
    ChromiumPageResearchLoadedWorkingSetTransitionRevisionRootRecord,
)
from .chromium_research_working_set_note_revision import (
    create_chromium_research_working_set_note_revision,
)
from .chromium_research_working_set_note_revision_edge_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord,
    _validate_loaded_root_predecessor,
)
from .chromium_research_working_set_note_revision_edge_persistence import (
    verify_chromium_research_working_set_note_revision_edge,
)


_EDGE_FORMAT = "pyxis.chromium.research_working_set_note_revision_edge.v1"
_ROOT_FORMAT = (
    "pyxis.chromium.research_session_working_set_transition_revision_root.v1"
)
_EDGE_MODE = "caller_authored_research_working_set_note_revision_edge"
_REVISION_MODE = "caller_authored_revision_of_research_working_set_note"
_NOTE_MODE = "caller_authored_note_on_research_working_set"


class ChromiumResearchSessionWorkingSetTransitionRevisionRootEdgeRelinkError(ValueError):
    """Raised when one root-backed 24B edge cannot relink to the supplied 34A root."""


def load_chromium_research_session_working_set_transition_revision_root_edge(
    prior_root: ChromiumPageResearchLoadedWorkingSetTransitionRevisionRootRecord,
    edge_source: Path,
) -> ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord:
    """Relink the first ordinary 24B edge after one explicit loaded 34A root.

    This is the one-time bridge from cross-working-set ancestry back into the normal
    revision-edge record type. It freshly verifies only the caller-supplied edge file,
    re-establishes the retained loaded root in memory, requires exact root format +
    content identity, and reconstructs the edge revision over the exact root endpoint.

    The generic 24C loader remains unchanged and still rejects roots directly.
    """

    if not isinstance(
        prior_root,
        ChromiumPageResearchLoadedWorkingSetTransitionRevisionRootRecord,
    ):
        raise TypeError(
            "prior_root must be "
            "ChromiumPageResearchLoadedWorkingSetTransitionRevisionRootRecord."
        )
    if not isinstance(edge_source, Path):
        raise TypeError("edge_source must be pathlib.Path.")

    verification = verify_chromium_research_working_set_note_revision_edge(edge_source)
    if verification.edge_format != _EDGE_FORMAT:
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootEdgeRelinkError(
            "Verified root-backed edge uses an unsupported edge format."
        )
    if verification.edge_mode != _EDGE_MODE:
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootEdgeRelinkError(
            "Verified root-backed edge uses an unsupported edge mode."
        )
    if verification.revision_mode != _REVISION_MODE:
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootEdgeRelinkError(
            "Verified root-backed edge uses an unsupported revision mode."
        )
    if verification.revised_note_mode != _NOTE_MODE:
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootEdgeRelinkError(
            "Verified root-backed edge uses an unsupported revised-note mode."
        )

    root_format, root_sha256, endpoint_note = _validate_loaded_root_predecessor(prior_root)
    if root_format != _ROOT_FORMAT:
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootEdgeRelinkError(
            "Loaded predecessor root uses an unsupported format."
        )
    if verification.predecessor_format != root_format:
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootEdgeRelinkError(
            "Root-backed edge references a different predecessor format."
        )
    if not hmac.compare_digest(verification.predecessor_record_sha256, root_sha256):
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootEdgeRelinkError(
            "Root-backed edge references a different predecessor root."
        )

    try:
        revision = create_chromium_research_working_set_note_revision(
            endpoint_note,
            revised_note_text=verification.revised_note_text,
        )
    except ValueError as exc:
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootEdgeRelinkError(
            "Verified root-backed edge cannot be re-established as an actual revision of the root endpoint."
        ) from exc
    if revision.revision_mode != verification.revision_mode:
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootEdgeRelinkError(
            "Reconstructed root-backed edge revision mode is incoherent."
        )
    if revision.revised_note.note_mode != verification.revised_note_mode:
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootEdgeRelinkError(
            "Reconstructed root-backed edge note mode is incoherent."
        )

    return ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord(
        verification=verification,
        predecessor=prior_root,
        revision=revision,
    )


__all__ = [
    "ChromiumResearchSessionWorkingSetTransitionRevisionRootEdgeRelinkError",
    "load_chromium_research_session_working_set_transition_revision_root_edge",
]
