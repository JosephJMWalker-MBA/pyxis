from __future__ import annotations

from dataclasses import dataclass
import hmac

from .chromium_research_working_set_note import (
    create_chromium_research_working_set_note,
)
from .chromium_research_working_set_note_revision import (
    ChromiumPageResearchWorkingSetNoteRevisionRecord,
    create_chromium_research_working_set_note_revision,
)
from .chromium_research_working_set_note_revision_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionRecord,
)


_NOTE_FORMAT = "pyxis.chromium.research_working_set_note.v1"
_REVISION_FORMAT = "pyxis.chromium.research_working_set_note_revision.v1"
_NOTE_MODE = "caller_authored_note_on_research_working_set"
_REVISION_MODE = "caller_authored_revision_of_research_working_set_note"
_CONTINUATION_MODE = (
    "caller_authored_continuation_of_verified_research_working_set_note_revision"
)


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchWorkingSetNoteRevisionContinuationRecord:
    """One human revision explicitly continued from one loaded 22C revision.

    `prior_revision` retains the exact caller-supplied 22C loaded revision object.
    `revision` is one newly created 22A revision whose prior note is exactly the
    revised note reconstructed by that loaded predecessor.

    The record establishes only an explicit in-memory human continuation
    relationship. It does not persist a chain, infer chronology, assign revision
    numbers, discover predecessors, compare semantics, or upgrade source truth.
    """

    continuation_mode: str
    prior_revision: ChromiumPageResearchLoadedWorkingSetNoteRevisionRecord
    revision: ChromiumPageResearchWorkingSetNoteRevisionRecord


def create_chromium_research_working_set_note_revision_continuation(
    prior_revision: ChromiumPageResearchLoadedWorkingSetNoteRevisionRecord,
    *,
    revised_note_text: str,
) -> ChromiumPageResearchWorkingSetNoteRevisionContinuationRecord:
    """Continue one explicit verified durable revision with one new human revision.

    23A consumes an already-loaded 22C record and performs no file reads. Before
    creating the continuation it re-establishes the retained in-memory 22C
    relationships from existing public 21A/22A constructors plus retained durable
    identity facts. The exact caller-supplied loaded predecessor object is kept.

    The new revision is then created through public 22A over exactly
    `prior_revision.revision.revised_note`. Exact textual no-ops therefore remain
    rejected by 22A. No persistence, chain traversal, revision numbering,
    timestamps, semantic diff, source acquisition, or browser work occurs here.
    """

    if not isinstance(prior_revision, ChromiumPageResearchLoadedWorkingSetNoteRevisionRecord):
        raise TypeError(
            "prior_revision must be ChromiumPageResearchLoadedWorkingSetNoteRevisionRecord."
        )

    _validate_loaded_prior_revision(prior_revision)

    revision = create_chromium_research_working_set_note_revision(
        prior_revision.revision.revised_note,
        revised_note_text=revised_note_text,
    )

    return ChromiumPageResearchWorkingSetNoteRevisionContinuationRecord(
        continuation_mode=_CONTINUATION_MODE,
        prior_revision=prior_revision,
        revision=revision,
    )


def _validate_loaded_prior_revision(
    prior_revision: ChromiumPageResearchLoadedWorkingSetNoteRevisionRecord,
) -> None:
    verification = prior_revision.verification
    loaded_prior_note = prior_revision.prior_note
    loaded_revision = prior_revision.revision

    if verification.revision_format != _REVISION_FORMAT:
        raise ValueError("loaded predecessor uses an unsupported revision format.")
    if verification.prior_note_format != _NOTE_FORMAT:
        raise ValueError("loaded predecessor references an unsupported note format.")
    if verification.revision_mode != _REVISION_MODE:
        raise ValueError("loaded predecessor uses an unsupported revision mode.")
    if verification.revised_note_mode != _NOTE_MODE:
        raise ValueError("loaded predecessor uses an unsupported revised-note mode.")

    if loaded_prior_note.verification.note_format != verification.prior_note_format:
        raise ValueError("loaded predecessor retained an incoherent prior-note format.")
    if not hmac.compare_digest(
        loaded_prior_note.verification.note_record_sha256,
        verification.prior_note_record_sha256,
    ):
        raise ValueError("loaded predecessor retained an incoherent prior-note identity.")

    rebuilt_prior_note = create_chromium_research_working_set_note(
        loaded_prior_note.working_set.working_set,
        note_text=loaded_prior_note.verification.note_text,
    )
    if rebuilt_prior_note.note_mode != loaded_prior_note.note.note_mode:
        raise ValueError("loaded predecessor retained an incoherent prior-note mode.")
    if rebuilt_prior_note.note_text != loaded_prior_note.note.note_text:
        raise ValueError("loaded predecessor retained incoherent prior-note text.")
    if loaded_prior_note.note.working_set is not loaded_prior_note.working_set.working_set:
        raise ValueError("loaded predecessor prior note does not retain its exact working set.")

    try:
        rebuilt_revision = create_chromium_research_working_set_note_revision(
            loaded_prior_note.note,
            revised_note_text=verification.revised_note_text,
        )
    except ValueError as exc:
        raise ValueError(
            "loaded predecessor cannot be re-established as an actual revision."
        ) from exc

    if loaded_revision.revision_mode != rebuilt_revision.revision_mode:
        raise ValueError("loaded predecessor retained an incoherent revision mode.")
    if loaded_revision.prior_note is not loaded_prior_note.note:
        raise ValueError("loaded predecessor revision does not retain the exact prior note.")
    if loaded_revision.revised_note.working_set is not loaded_prior_note.note.working_set:
        raise ValueError(
            "loaded predecessor revised note does not retain the exact working set."
        )
    if loaded_revision.revised_note.note_mode != verification.revised_note_mode:
        raise ValueError("loaded predecessor retained an incoherent revised-note mode.")
    if loaded_revision.revised_note.note_text != verification.revised_note_text:
        raise ValueError("loaded predecessor retained incoherent revised-note text.")
