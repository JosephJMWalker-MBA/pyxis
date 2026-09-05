from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
import hmac
from pathlib import Path

from .chromium_research_working_set import ChromiumPageResearchWorkingSetItem
from .chromium_research_working_set_note_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRecord,
    load_chromium_research_working_set_note,
)
from .chromium_research_working_set_note_revision import (
    ChromiumPageResearchWorkingSetNoteRevisionRecord,
    create_chromium_research_working_set_note_revision,
)
from .chromium_research_working_set_note_revision_persistence import (
    ChromiumPageResearchWorkingSetNoteRevisionVerificationEvidence,
    verify_chromium_research_working_set_note_revision,
)


_REVISION_FORMAT = "pyxis.chromium.research_working_set_note_revision.v1"
_REVISION_FORMAT_V2 = "pyxis.chromium.research_working_set_note_revision.v2"
_NOTE_FORMAT = "pyxis.chromium.research_working_set_note.v1"
_NOTE_FORMAT_V2 = "pyxis.chromium.research_working_set_note.v2"
_NOTE_MODE = "caller_authored_note_on_research_working_set"

_REVISION_PREDECESSOR_FORMATS = {
    _REVISION_FORMAT: _NOTE_FORMAT,
    _REVISION_FORMAT_V2: _NOTE_FORMAT_V2,
}
_REVISION_MODE = "caller_authored_revision_of_research_working_set_note"


class ChromiumResearchWorkingSetNoteRevisionRelinkError(ValueError):
    """Raised when one verified 22B revision cannot relink to the supplied predecessor."""


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchLoadedWorkingSetNoteRevisionRecord:
    """One verified 22B revision relinked to one explicit durable predecessor.

    `verification` is fresh 22B file-local verification evidence. `prior_note` is
    the fresh 21C loaded predecessor produced from the caller-supplied 20B/21B
    sidecars and complete ordered loaded-member sequence. `revision` is a newly
    reconstructed 22A human revision whose prior note is exactly
    `prior_note.note` and whose revised wording is the verbatim human text retained
    by the verified 22B sidecar.

    Successful relinking proves only durable predecessor identity coherence and
    re-establishment of an actual exact-text revision relative to that explicit
    predecessor. It does not prove chronology, authorship, semantic improvement,
    source truth, claim support, or machine agreement.
    """

    verification: ChromiumPageResearchWorkingSetNoteRevisionVerificationEvidence
    prior_note: ChromiumPageResearchLoadedWorkingSetNoteRecord
    revision: ChromiumPageResearchWorkingSetNoteRevisionRecord


def load_chromium_research_working_set_note_revision(
    items: Iterable[ChromiumPageResearchWorkingSetItem],
    working_set_source: Path,
    prior_note_source: Path,
    revision_source: Path,
) -> ChromiumPageResearchLoadedWorkingSetNoteRevisionRecord:
    """Relink one durable v1/v2 revision to one explicit durable note predecessor.

    The caller supplies the complete ordered already-loaded member sequence, one
    20B working-set sidecar path, one 21B predecessor-note sidecar path, and one
    22B revision sidecar path. Pyxis performs no predecessor discovery, digest
    search, path-history lookup, chain traversal, or semantic inference.

    The 22B sidecar is freshly verified. The predecessor is then freshly relinked
    through public 21C. The predecessor note identity persisted by 22B must match
    the fresh 21B verification retained by 21C. Only then is the 22A revision
    reconstructed over the exact 21C predecessor note. Public 22A therefore
    re-establishes that the persisted revised wording is an actual exact-text
    revision rather than an exact no-op relative to that predecessor.
    """

    try:
        supplied_items = tuple(items)
    except TypeError as exc:
        raise TypeError("items must be an iterable of relinked research records.") from exc

    verification = verify_chromium_research_working_set_note_revision(revision_source)
    expected_note_format = _REVISION_PREDECESSOR_FORMATS.get(
        verification.revision_format
    )
    if expected_note_format is None:
        raise ChromiumResearchWorkingSetNoteRevisionRelinkError(
            "Verified working-set-note revision uses an unsupported revision format."
        )
    if verification.prior_note_format != expected_note_format:
        raise ChromiumResearchWorkingSetNoteRevisionRelinkError(
            "Verified working-set-note revision references an unsupported predecessor format."
        )
    if verification.revision_mode != _REVISION_MODE:
        raise ChromiumResearchWorkingSetNoteRevisionRelinkError(
            "Verified working-set-note revision uses an unsupported revision mode."
        )
    if verification.revised_note_mode != _NOTE_MODE:
        raise ChromiumResearchWorkingSetNoteRevisionRelinkError(
            "Verified working-set-note revision uses an unsupported revised-note mode."
        )

    loaded_prior = load_chromium_research_working_set_note(
        supplied_items,
        working_set_source,
        prior_note_source,
    )

    if loaded_prior.verification.note_format != verification.prior_note_format:
        raise ChromiumResearchWorkingSetNoteRevisionRelinkError(
            "Verified revision references a different predecessor note format."
        )
    if not hmac.compare_digest(
        loaded_prior.verification.note_record_sha256,
        verification.prior_note_record_sha256,
    ):
        raise ChromiumResearchWorkingSetNoteRevisionRelinkError(
            "Verified revision references a different predecessor note record."
        )

    try:
        revision = create_chromium_research_working_set_note_revision(
            loaded_prior.note,
            revised_note_text=verification.revised_note_text,
        )
    except ValueError as exc:
        raise ChromiumResearchWorkingSetNoteRevisionRelinkError(
            "Verified revision cannot be re-established as an actual revision of the supplied predecessor."
        ) from exc

    if revision.revision_mode != verification.revision_mode:
        raise ChromiumResearchWorkingSetNoteRevisionRelinkError(
            "Reconstructed revision mode does not match the verified sidecar."
        )
    if revision.revised_note.note_mode != verification.revised_note_mode:
        raise ChromiumResearchWorkingSetNoteRevisionRelinkError(
            "Reconstructed revised-note mode does not match the verified sidecar."
        )

    return ChromiumPageResearchLoadedWorkingSetNoteRevisionRecord(
        verification=verification,
        prior_note=loaded_prior,
        revision=revision,
    )
