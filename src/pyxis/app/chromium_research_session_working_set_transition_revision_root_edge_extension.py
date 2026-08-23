from __future__ import annotations

from dataclasses import dataclass

from .chromium_research_session_working_set_transition_revision_root_load import (
    ChromiumPageResearchLoadedWorkingSetTransitionRevisionRootRecord,
)
from .chromium_research_working_set_note_revision import (
    ChromiumPageResearchWorkingSetNoteRevisionRecord,
    create_chromium_research_working_set_note_revision,
)
from .chromium_research_working_set_note_revision_edge_load import (
    _validate_loaded_root_predecessor,
)


_EXTENSION_MODE = (
    "caller_authored_extension_of_verified_cross_working_set_revision_root"
)


@dataclass(frozen=True, slots=True)
class ChromiumResearchSessionWorkingSetTransitionRevisionRootEdgeExtensionRecord:
    """One ordinary human revision explicitly extended from one loaded 34A root.

    `prior_root` retains the exact caller-supplied loaded cross-working-set root.
    `revision` is one public-22A same-working-set revision whose prior note is exactly
    that root's revised endpoint note.

    The extension establishes only one explicit in-memory local continuation after
    the basis change. It does not persist anything, traverse the transition ancestry,
    adopt a session, select a head, infer chronology, or make semantic claims.
    """

    extension_mode: str
    prior_root: ChromiumPageResearchLoadedWorkingSetTransitionRevisionRootRecord
    revision: ChromiumPageResearchWorkingSetNoteRevisionRecord


def create_chromium_research_session_working_set_transition_revision_root_edge_extension(
    prior_root: ChromiumPageResearchLoadedWorkingSetTransitionRevisionRootRecord,
    *,
    revised_note_text: str,
) -> ChromiumResearchSessionWorkingSetTransitionRevisionRootEdgeExtensionRecord:
    """Create the first ordinary revision after one verified 34A root.

    No file reads occur. The retained root is re-established through the same bounded
    predecessor validator used by 24C, then public 22A creates the next exact-text
    revision over the root endpoint note. Exact textual no-ops remain rejected.
    """

    if not isinstance(
        prior_root,
        ChromiumPageResearchLoadedWorkingSetTransitionRevisionRootRecord,
    ):
        raise TypeError(
            "prior_root must be "
            "ChromiumPageResearchLoadedWorkingSetTransitionRevisionRootRecord."
        )

    _, _, endpoint_note = _validate_loaded_root_predecessor(prior_root)
    revision = create_chromium_research_working_set_note_revision(
        endpoint_note,
        revised_note_text=revised_note_text,
    )
    return ChromiumResearchSessionWorkingSetTransitionRevisionRootEdgeExtensionRecord(
        extension_mode=_EXTENSION_MODE,
        prior_root=prior_root,
        revision=revision,
    )


__all__ = [
    "ChromiumResearchSessionWorkingSetTransitionRevisionRootEdgeExtensionRecord",
    "create_chromium_research_session_working_set_transition_revision_root_edge_extension",
]
