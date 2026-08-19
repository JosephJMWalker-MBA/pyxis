from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
import hmac
from pathlib import Path

from .chromium_research_working_set import ChromiumPageResearchWorkingSetItem
from .chromium_research_working_set_note_revision_continuation import (
    ChromiumPageResearchWorkingSetNoteRevisionContinuationRecord,
    create_chromium_research_working_set_note_revision_continuation,
)
from .chromium_research_working_set_note_revision_continuation_persistence import (
    ChromiumPageResearchWorkingSetNoteRevisionContinuationVerificationEvidence,
    verify_chromium_research_working_set_note_revision_continuation,
)
from .chromium_research_working_set_note_revision_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionRecord,
    load_chromium_research_working_set_note_revision,
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


class ChromiumResearchWorkingSetNoteRevisionContinuationRelinkError(ValueError):
    """Raised when one verified 23B continuation cannot relink to its predecessor."""


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord:
    """One verified 23B continuation relinked to one explicit durable 22B revision.

    `verification` is fresh 23B file-local verification evidence. `prior_revision`
    is the fresh 22C loaded predecessor produced from the caller-supplied 20B/21B/
    22B sidecars and complete ordered loaded-member sequence. `continuation` is a
    newly reconstructed 23A human continuation whose prior revision is exactly
    `prior_revision` and whose new human wording is the verbatim text retained by
    the verified 23B sidecar.

    Successful relinking proves only durable predecessor identity coherence and
    re-establishment of an actual exact-text continuation relative to that explicit
    predecessor. It does not prove chronology, authorship, semantic improvement,
    source truth, claim support, or machine agreement.
    """

    verification: ChromiumPageResearchWorkingSetNoteRevisionContinuationVerificationEvidence
    prior_revision: ChromiumPageResearchLoadedWorkingSetNoteRevisionRecord
    continuation: ChromiumPageResearchWorkingSetNoteRevisionContinuationRecord


def load_chromium_research_working_set_note_revision_continuation(
    items: Iterable[ChromiumPageResearchWorkingSetItem],
    working_set_source: Path,
    prior_note_source: Path,
    prior_revision_source: Path,
    continuation_source: Path,
) -> ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord:
    """Relink one durable 23B continuation to one explicit durable 22B predecessor.

    The caller supplies the complete ordered already-loaded member sequence plus
    explicit 20B, 21B, 22B, and 23B sidecar paths. Pyxis performs no predecessor
    discovery, digest search, directory scan, path-history lookup, recursive chain
    traversal, revision numbering, timestamp inference, or semantic comparison.

    The 23B sidecar is freshly verified. The predecessor 22B revision is then
    freshly relinked through public 22C. The predecessor revision identity persisted
    by 23B must match the fresh 22B verification retained by 22C. Only then is the
    23A continuation reconstructed over that exact loaded predecessor. Public 23A,
    via public 22A, therefore re-establishes that the persisted v3 wording is an
    actual exact-text revision rather than an exact no-op relative to v2.
    """

    try:
        supplied_items = tuple(items)
    except TypeError as exc:
        raise TypeError("items must be an iterable of relinked research records.") from exc

    verification = verify_chromium_research_working_set_note_revision_continuation(
        continuation_source
    )
    if verification.continuation_format != _CONTINUATION_FORMAT:
        raise ChromiumResearchWorkingSetNoteRevisionContinuationRelinkError(
            "Verified revision continuation uses an unsupported continuation format."
        )
    if verification.prior_revision_format != _REVISION_FORMAT:
        raise ChromiumResearchWorkingSetNoteRevisionContinuationRelinkError(
            "Verified revision continuation references an unsupported predecessor format."
        )
    if verification.continuation_mode != _CONTINUATION_MODE:
        raise ChromiumResearchWorkingSetNoteRevisionContinuationRelinkError(
            "Verified revision continuation uses an unsupported continuation mode."
        )
    if verification.revision_mode != _REVISION_MODE:
        raise ChromiumResearchWorkingSetNoteRevisionContinuationRelinkError(
            "Verified revision continuation uses an unsupported revision mode."
        )
    if verification.revised_note_mode != _NOTE_MODE:
        raise ChromiumResearchWorkingSetNoteRevisionContinuationRelinkError(
            "Verified revision continuation uses an unsupported revised-note mode."
        )

    loaded_prior = load_chromium_research_working_set_note_revision(
        supplied_items,
        working_set_source,
        prior_note_source,
        prior_revision_source,
    )

    if loaded_prior.verification.revision_format != verification.prior_revision_format:
        raise ChromiumResearchWorkingSetNoteRevisionContinuationRelinkError(
            "Verified continuation references a different predecessor revision format."
        )
    if not hmac.compare_digest(
        loaded_prior.verification.revision_record_sha256,
        verification.prior_revision_record_sha256,
    ):
        raise ChromiumResearchWorkingSetNoteRevisionContinuationRelinkError(
            "Verified continuation references a different predecessor revision record."
        )

    try:
        continuation = create_chromium_research_working_set_note_revision_continuation(
            loaded_prior,
            revised_note_text=verification.revised_note_text,
        )
    except ValueError as exc:
        raise ChromiumResearchWorkingSetNoteRevisionContinuationRelinkError(
            "Verified continuation cannot be re-established as an actual continuation of the supplied predecessor."
        ) from exc

    if continuation.continuation_mode != verification.continuation_mode:
        raise ChromiumResearchWorkingSetNoteRevisionContinuationRelinkError(
            "Reconstructed continuation mode does not match the verified sidecar."
        )
    if continuation.revision.revision_mode != verification.revision_mode:
        raise ChromiumResearchWorkingSetNoteRevisionContinuationRelinkError(
            "Reconstructed revision mode does not match the verified sidecar."
        )
    if continuation.revision.revised_note.note_mode != verification.revised_note_mode:
        raise ChromiumResearchWorkingSetNoteRevisionContinuationRelinkError(
            "Reconstructed revised-note mode does not match the verified sidecar."
        )

    return ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord(
        verification=verification,
        prior_revision=loaded_prior,
        continuation=continuation,
    )
