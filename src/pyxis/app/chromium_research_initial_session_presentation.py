from __future__ import annotations

from dataclasses import dataclass

from .chromium_research_revision_edge_working_set_presentation import (
    ChromiumPageResearchWorkingSetMemberPresentation,
    _present_working_set_member,
)
from .chromium_research_working_set import create_chromium_research_working_set
from .chromium_research_working_set_note import (
    create_chromium_research_working_set_note,
)
from .chromium_research_working_set_note_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRecord,
)


_PRESENTATION_MODE = "read_only_initial_research_session_root"
_WORKING_SET_MODE = "caller_explicit_ordered_relinked_research_working_set"
_NOTE_MODE = "caller_authored_note_on_research_working_set"
_NOTE_FORMAT_V1 = "pyxis.chromium.research_working_set_note.v1"
_NOTE_FORMAT_V2 = "pyxis.chromium.research_working_set_note.v2"
_WORKING_SET_FORMAT_V1 = "pyxis.chromium.research_working_set.v1"
_WORKING_SET_FORMAT_V2 = "pyxis.chromium.research_working_set.v2"
_NOTE_PARENT_FORMATS = {
    _NOTE_FORMAT_V1: _WORKING_SET_FORMAT_V1,
    _NOTE_FORMAT_V2: _WORKING_SET_FORMAT_V2,
}


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchInitialSessionPresentation:
    """Read-only presentation of one freshly loaded first-session rationale root.

    This is an application presentation over already-earned 20C/21C evidence. It
    records no revision, declaration, chronology, current/latest/head state, source
    truth, semantic support, or browser authority.
    """

    presentation_mode: str
    note_format: str
    note_record_sha256: str
    working_set_format: str
    working_set_record_sha256: str
    rationale_text: str
    working_set_mode: str
    members: tuple[ChromiumPageResearchWorkingSetMemberPresentation, ...]


def present_chromium_research_initial_session(
    loaded: ChromiumPageResearchLoadedWorkingSetNoteRecord,
) -> ChromiumPageResearchInitialSessionPresentation:
    """Present one explicit loaded working-set note as an initial governed root.

    The function performs no file or browser I/O. It re-establishes only retained
    in-memory coherence and reuses the same working-set member projection used by
    declared revision-edge working-set presentation.
    """

    if not isinstance(loaded, ChromiumPageResearchLoadedWorkingSetNoteRecord):
        raise TypeError(
            "loaded must be ChromiumPageResearchLoadedWorkingSetNoteRecord."
        )

    verification = loaded.verification
    loaded_working_set = loaded.working_set
    note = loaded.note
    working_set = loaded_working_set.working_set

    expected_working_set_format = _NOTE_PARENT_FORMATS.get(verification.note_format)
    if expected_working_set_format is None:
        raise ValueError("loaded initial-session note format is unsupported.")
    if verification.working_set_format != expected_working_set_format:
        raise ValueError(
            "loaded initial-session note references an unsupported working-set format."
        )
    if loaded_working_set.verification.working_set_format != expected_working_set_format:
        raise ValueError(
            "loaded initial-session working-set format is incoherent with its note."
        )
    if (
        loaded_working_set.verification.working_set_record_sha256
        != verification.working_set_record_sha256
    ):
        raise ValueError(
            "loaded initial-session working-set identity is incoherent with its note."
        )
    if verification.note_mode != _NOTE_MODE or note.note_mode != _NOTE_MODE:
        raise ValueError("loaded initial-session note mode is unsupported.")
    if note.note_text != verification.note_text:
        raise ValueError("loaded initial-session rationale text is incoherent.")
    if note.working_set is not working_set:
        raise ValueError(
            "loaded initial-session note does not retain its exact loaded working set."
        )
    if working_set.working_set_mode != _WORKING_SET_MODE:
        raise ValueError("loaded initial-session working-set mode is unsupported.")
    if loaded_working_set.verification.working_set_mode != working_set.working_set_mode:
        raise ValueError("loaded initial-session working-set mode is incoherent.")

    rebuilt_working_set = create_chromium_research_working_set(working_set.items)
    if len(rebuilt_working_set.items) != len(working_set.items) or any(
        observed is not retained
        for observed, retained in zip(rebuilt_working_set.items, working_set.items)
    ):
        raise ValueError("loaded initial-session working-set membership is incoherent.")
    rebuilt_note = create_chromium_research_working_set_note(
        working_set,
        note_text=note.note_text,
    )
    if rebuilt_note.note_mode != note.note_mode:
        raise ValueError("loaded initial-session rationale mode is incoherent.")

    members = tuple(
        _present_working_set_member(item, position=index)
        for index, item in enumerate(working_set.items, start=1)
    )
    if not members:
        raise ValueError("initial research session root must contain at least one member.")

    return ChromiumPageResearchInitialSessionPresentation(
        presentation_mode=_PRESENTATION_MODE,
        note_format=verification.note_format,
        note_record_sha256=verification.note_record_sha256,
        working_set_format=verification.working_set_format,
        working_set_record_sha256=verification.working_set_record_sha256,
        rationale_text=note.note_text,
        working_set_mode=working_set.working_set_mode,
        members=members,
    )
