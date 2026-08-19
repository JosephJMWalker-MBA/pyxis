from __future__ import annotations

from dataclasses import dataclass
import hmac

from .chromium_research_working_set_note_revision import (
    ChromiumPageResearchWorkingSetNoteRevisionRecord,
    create_chromium_research_working_set_note_revision,
)
from .chromium_research_working_set_note_revision_continuation import (
    create_chromium_research_working_set_note_revision_continuation,
)
from .chromium_research_working_set_note_revision_continuation_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord,
)


_CONTINUATION_FORMAT = (
    "pyxis.chromium.research_working_set_note_revision_continuation.v1"
)
_REVISION_FORMAT = "pyxis.chromium.research_working_set_note_revision.v1"
_NOTE_MODE = "caller_authored_note_on_research_working_set"
_REVISION_MODE = "caller_authored_revision_of_research_working_set_note"
_CONTINUATION_MODE = (
    "caller_authored_continuation_of_verified_research_working_set_note_revision"
)
_EXTENSION_MODE = (
    "caller_authored_extension_of_verified_research_working_set_note_revision_continuation"
)


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchWorkingSetNoteRevisionContinuationExtensionRecord:
    """One new human revision explicitly extended from one loaded 23C continuation.

    `prior_continuation` retains the exact caller-supplied 23C loaded continuation
    object. `revision` is one newly created 22A revision whose prior note is exactly
    the v3 note reconstructed by that loaded continuation.

    The record establishes only an explicit in-memory human extension relationship.
    It does not persist recursive history, traverse predecessors, infer chronology,
    assign revision numbers, compare semantics, or upgrade source truth.
    """

    extension_mode: str
    prior_continuation: ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord
    revision: ChromiumPageResearchWorkingSetNoteRevisionRecord


def create_chromium_research_working_set_note_revision_continuation_extension(
    prior_continuation: ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord,
    *,
    revised_note_text: str,
) -> ChromiumPageResearchWorkingSetNoteRevisionContinuationExtensionRecord:
    """Extend one explicit verified durable continuation with one new human revision.

    24A consumes one already-loaded 23C record and performs no file reads. Before
    creating the new revision it re-establishes the retained in-memory 23C
    relationships from existing public 23A/22A constructors plus retained durable
    identity facts.

    The new revision is then created through public 22A over exactly
    `prior_continuation.continuation.revision.revised_note`. Exact textual no-ops
    therefore remain rejected by 22A. No persistence, recursive history traversal,
    revision numbering, timestamps, semantic diff, source acquisition, or browser
    work occurs here.
    """

    if not isinstance(
        prior_continuation,
        ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord,
    ):
        raise TypeError(
            "prior_continuation must be "
            "ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord."
        )

    _validate_loaded_prior_continuation(prior_continuation)

    revision = create_chromium_research_working_set_note_revision(
        prior_continuation.continuation.revision.revised_note,
        revised_note_text=revised_note_text,
    )

    return ChromiumPageResearchWorkingSetNoteRevisionContinuationExtensionRecord(
        extension_mode=_EXTENSION_MODE,
        prior_continuation=prior_continuation,
        revision=revision,
    )


def _validate_loaded_prior_continuation(
    prior_continuation: ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord,
) -> None:
    verification = prior_continuation.verification
    loaded_prior_revision = prior_continuation.prior_revision
    loaded_continuation = prior_continuation.continuation

    if verification.continuation_format != _CONTINUATION_FORMAT:
        raise ValueError("loaded predecessor uses an unsupported continuation format.")
    if verification.prior_revision_format != _REVISION_FORMAT:
        raise ValueError("loaded predecessor references an unsupported revision format.")
    if verification.continuation_mode != _CONTINUATION_MODE:
        raise ValueError("loaded predecessor uses an unsupported continuation mode.")
    if verification.revision_mode != _REVISION_MODE:
        raise ValueError("loaded predecessor uses an unsupported revision mode.")
    if verification.revised_note_mode != _NOTE_MODE:
        raise ValueError("loaded predecessor uses an unsupported revised-note mode.")

    if (
        loaded_prior_revision.verification.revision_format
        != verification.prior_revision_format
    ):
        raise ValueError("loaded predecessor retained an incoherent prior-revision format.")
    if not hmac.compare_digest(
        loaded_prior_revision.verification.revision_record_sha256,
        verification.prior_revision_record_sha256,
    ):
        raise ValueError("loaded predecessor retained an incoherent prior-revision identity.")

    try:
        rebuilt_continuation = (
            create_chromium_research_working_set_note_revision_continuation(
                loaded_prior_revision,
                revised_note_text=verification.revised_note_text,
            )
        )
    except ValueError as exc:
        raise ValueError(
            "loaded predecessor cannot be re-established as an actual continuation."
        ) from exc

    if loaded_continuation.continuation_mode != rebuilt_continuation.continuation_mode:
        raise ValueError("loaded predecessor retained an incoherent continuation mode.")
    if loaded_continuation.continuation_mode != verification.continuation_mode:
        raise ValueError("loaded predecessor continuation mode disagrees with verification.")
    if loaded_continuation.prior_revision is not loaded_prior_revision:
        raise ValueError(
            "loaded predecessor continuation does not retain the exact prior revision."
        )
    if loaded_continuation.revision.revision_mode != verification.revision_mode:
        raise ValueError("loaded predecessor retained an incoherent revision mode.")
    if (
        loaded_continuation.revision.prior_note
        is not loaded_prior_revision.revision.revised_note
    ):
        raise ValueError(
            "loaded predecessor revision does not retain the exact v2 note object."
        )
    if (
        loaded_continuation.revision.revised_note.working_set
        is not loaded_prior_revision.revision.revised_note.working_set
    ):
        raise ValueError(
            "loaded predecessor revised note does not retain the exact working set."
        )
    if loaded_continuation.revision.revised_note.note_mode != verification.revised_note_mode:
        raise ValueError("loaded predecessor retained an incoherent revised-note mode.")
    if loaded_continuation.revision.revised_note.note_text != verification.revised_note_text:
        raise ValueError("loaded predecessor retained incoherent v3 note text.")
