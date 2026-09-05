from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
import hmac
from pathlib import Path

from .chromium_research_working_set import ChromiumPageResearchWorkingSetItem
from .chromium_research_working_set_load import (
    ChromiumPageResearchLoadedWorkingSetRecord,
    load_chromium_research_working_set,
)
from .chromium_research_working_set_note import (
    ChromiumPageResearchWorkingSetNoteRecord,
    create_chromium_research_working_set_note,
)
from .chromium_research_working_set_note_persistence import (
    ChromiumPageResearchWorkingSetNoteVerificationEvidence,
    verify_chromium_research_working_set_note,
)


_WORKING_SET_NOTE_FORMAT = "pyxis.chromium.research_working_set_note.v1"
_WORKING_SET_NOTE_FORMAT_V2 = "pyxis.chromium.research_working_set_note.v2"
_WORKING_SET_FORMAT = "pyxis.chromium.research_working_set.v1"
_WORKING_SET_FORMAT_V2 = "pyxis.chromium.research_working_set.v2"
_NOTE_MODE = "caller_authored_note_on_research_working_set"

_NOTE_PARENT_FORMATS = {
    _WORKING_SET_NOTE_FORMAT: _WORKING_SET_FORMAT,
    _WORKING_SET_NOTE_FORMAT_V2: _WORKING_SET_FORMAT_V2,
}


class ChromiumResearchWorkingSetNoteParentMismatchError(ValueError):
    """Raised when a verified 21B note does not match the supplied durable parent."""


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchLoadedWorkingSetNoteRecord:
    """One verified 21B note relinked to one explicit durable working set.

    `verification` is fresh 21B file-local verification evidence. `working_set`
    is the fresh 20C loaded-parent record produced from the caller-supplied member
    sequence and 20B sidecar. `note` is a newly reconstructed 21A note whose
    parent is exactly `working_set.working_set` and whose text is the verbatim
    human text retained by the verified 21B sidecar.

    Successful relinking proves only durable parent-attachment coherence relative
    to the caller-supplied 20B parent and already-loaded members. It does not prove
    note correctness, semantic relationship, source truth, authorship, trusted
    time, citation authority, or machine agreement.
    """

    verification: ChromiumPageResearchWorkingSetNoteVerificationEvidence
    working_set: ChromiumPageResearchLoadedWorkingSetRecord
    note: ChromiumPageResearchWorkingSetNoteRecord


def load_chromium_research_working_set_note(
    items: Iterable[ChromiumPageResearchWorkingSetItem],
    working_set_source: Path,
    note_source: Path,
) -> ChromiumPageResearchLoadedWorkingSetNoteRecord:
    """Relink one durable v1/v2 human note to one explicit durable working-set parent.

    The caller supplies the complete ordered already-loaded member sequence, one
    20B working-set path, and one 21B working-set-note path. Pyxis performs no
    parent discovery or digest search.

    The 21B sidecar is freshly verified first. The parent is then freshly loaded
    through public 20C, which verifies the supplied 20B sidecar and re-establishes
    its complete ordered membership against the supplied loaded records. The
    21B parent reference must exactly match that fresh 20B verification evidence.

    After that match succeeds, the persisted human text is reconstructed through
    public 21A over the exact 20A working-set object returned by 20C.
    """

    try:
        supplied_items = tuple(items)
    except TypeError as exc:
        raise TypeError("items must be an iterable of relinked research records.") from exc

    verification = verify_chromium_research_working_set_note(note_source)
    expected_parent_format = _NOTE_PARENT_FORMATS.get(verification.note_format)
    if expected_parent_format is None:
        raise ChromiumResearchWorkingSetNoteParentMismatchError(
            "Verified working-set-note sidecar uses an unsupported note format."
        )
    if verification.working_set_format != expected_parent_format:
        raise ChromiumResearchWorkingSetNoteParentMismatchError(
            "Verified working-set-note sidecar references an unsupported parent format."
        )
    if verification.note_mode != _NOTE_MODE:
        raise ChromiumResearchWorkingSetNoteParentMismatchError(
            "Verified working-set-note sidecar uses an unsupported note mode."
        )

    loaded_parent = load_chromium_research_working_set(
        supplied_items,
        working_set_source,
    )

    if loaded_parent.verification.working_set_format != verification.working_set_format:
        raise ChromiumResearchWorkingSetNoteParentMismatchError(
            "Verified working-set-note sidecar references a different parent format."
        )
    if not hmac.compare_digest(
        loaded_parent.verification.working_set_record_sha256,
        verification.working_set_record_sha256,
    ):
        raise ChromiumResearchWorkingSetNoteParentMismatchError(
            "Verified working-set-note sidecar references a different working-set record."
        )

    note = create_chromium_research_working_set_note(
        loaded_parent.working_set,
        note_text=verification.note_text,
    )
    if note.note_mode != verification.note_mode:
        raise ChromiumResearchWorkingSetNoteParentMismatchError(
            "Reconstructed working-set-note mode does not match the verified sidecar."
        )

    return ChromiumPageResearchLoadedWorkingSetNoteRecord(
        verification=verification,
        working_set=loaded_parent,
        note=note,
    )
