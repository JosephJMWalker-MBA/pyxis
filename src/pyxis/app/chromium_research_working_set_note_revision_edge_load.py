from __future__ import annotations

from dataclasses import dataclass
import hmac
from pathlib import Path

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
from .chromium_research_working_set_note_revision_edge_persistence import (
    ChromiumPageResearchWorkingSetNoteRevisionEdgeVerificationEvidence,
    verify_chromium_research_working_set_note_revision_edge,
)


_EDGE_FORMAT = "pyxis.chromium.research_working_set_note_revision_edge.v1"
_CONTINUATION_FORMAT = (
    "pyxis.chromium.research_working_set_note_revision_continuation.v1"
)
_NOTE_MODE = "caller_authored_note_on_research_working_set"
_REVISION_MODE = "caller_authored_revision_of_research_working_set_note"
_CONTINUATION_MODE = (
    "caller_authored_continuation_of_verified_research_working_set_note_revision"
)
_EDGE_MODE = "caller_authored_research_working_set_note_revision_edge"


class ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError(ValueError):
    """Raised when one verified 24B edge cannot relink to an explicit predecessor."""


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord:
    """One verified 24B edge relinked to one explicit already-loaded predecessor.

    `predecessor` is retained by exact object identity and may be either one loaded
    23C continuation or another already-loaded 24C edge. `revision` is freshly
    reconstructed through public 22A over exactly that predecessor's endpoint note.

    This record establishes only one explicit local predecessor relationship. It
    does not discover predecessors, recursively load files, establish a global
    history head, infer chronology, detect durable cycles, or make semantic claims.
    """

    verification: ChromiumPageResearchWorkingSetNoteRevisionEdgeVerificationEvidence
    predecessor: (
        ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord
        | ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord
    )
    revision: ChromiumPageResearchWorkingSetNoteRevisionRecord


def load_chromium_research_working_set_note_revision_edge(
    predecessor: (
        ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord
        | ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord
    ),
    edge_source: Path,
) -> ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord:
    """Relink one 24B edge to one explicit already-loaded predecessor.

    The caller chooses and supplies the predecessor object. Pyxis freshly verifies
    only `edge_source`; it performs no digest search, directory scan, predecessor
    discovery, recursive file loading, chain traversal, current-head selection,
    revision numbering, timestamp inference, or semantic comparison.

    The edge's persisted predecessor format + content identity must match the
    supplied predecessor. Only then is public 22A used to reconstruct the new human
    revision over that predecessor's exact endpoint note, re-establishing exact-text
    non-no-op behavior for the edge being loaded.
    """

    if not isinstance(
        predecessor,
        (
            ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord,
            ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord,
        ),
    ):
        raise TypeError(
            "predecessor must be an already-loaded 23C continuation or 24C revision edge."
        )

    verification = verify_chromium_research_working_set_note_revision_edge(edge_source)
    if verification.edge_format != _EDGE_FORMAT:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError(
            "Verified revision edge uses an unsupported edge format."
        )
    if verification.edge_mode != _EDGE_MODE:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError(
            "Verified revision edge uses an unsupported edge mode."
        )
    if verification.revision_mode != _REVISION_MODE:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError(
            "Verified revision edge uses an unsupported revision mode."
        )
    if verification.revised_note_mode != _NOTE_MODE:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError(
            "Verified revision edge uses an unsupported revised-note mode."
        )

    predecessor_format, predecessor_sha256, prior_note = _validate_loaded_predecessor(
        predecessor
    )

    if verification.predecessor_format != predecessor_format:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError(
            "Verified revision edge references a different predecessor format."
        )
    if not hmac.compare_digest(
        verification.predecessor_record_sha256,
        predecessor_sha256,
    ):
        raise ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError(
            "Verified revision edge references a different predecessor record."
        )

    try:
        revision = create_chromium_research_working_set_note_revision(
            prior_note,
            revised_note_text=verification.revised_note_text,
        )
    except ValueError as exc:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError(
            "Verified revision edge cannot be re-established as an actual revision of the supplied predecessor endpoint."
        ) from exc

    if revision.revision_mode != verification.revision_mode:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError(
            "Reconstructed revision mode does not match the verified edge."
        )
    if revision.revised_note.note_mode != verification.revised_note_mode:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError(
            "Reconstructed revised-note mode does not match the verified edge."
        )

    return ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord(
        verification=verification,
        predecessor=predecessor,
        revision=revision,
    )


def _validate_loaded_predecessor(
    predecessor: (
        ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord
        | ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord
    ),
):
    if isinstance(
        predecessor,
        ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord,
    ):
        return _validate_loaded_continuation_predecessor(predecessor)
    return _validate_loaded_edge_predecessor(predecessor)


def _validate_loaded_continuation_predecessor(
    predecessor: ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord,
):
    verification = predecessor.verification
    loaded_prior = predecessor.prior_revision
    continuation = predecessor.continuation

    if verification.continuation_format != _CONTINUATION_FORMAT:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError(
            "Loaded continuation predecessor uses an unsupported format."
        )
    if verification.continuation_mode != _CONTINUATION_MODE:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError(
            "Loaded continuation predecessor uses an unsupported mode."
        )
    if verification.revision_mode != _REVISION_MODE:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError(
            "Loaded continuation predecessor retains an unsupported revision mode."
        )
    if verification.revised_note_mode != _NOTE_MODE:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError(
            "Loaded continuation predecessor retains an unsupported note mode."
        )
    if loaded_prior.verification.revision_format != verification.prior_revision_format:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError(
            "Loaded continuation predecessor retained an incoherent prior-revision format."
        )
    if not hmac.compare_digest(
        loaded_prior.verification.revision_record_sha256,
        verification.prior_revision_record_sha256,
    ):
        raise ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError(
            "Loaded continuation predecessor retained an incoherent prior-revision identity."
        )

    try:
        rebuilt = create_chromium_research_working_set_note_revision_continuation(
            loaded_prior,
            revised_note_text=verification.revised_note_text,
        )
    except ValueError as exc:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError(
            "Loaded continuation predecessor cannot be re-established as an actual continuation."
        ) from exc

    if continuation.continuation_mode != rebuilt.continuation_mode:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError(
            "Loaded continuation predecessor retained an incoherent continuation mode."
        )
    if continuation.prior_revision is not loaded_prior:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError(
            "Loaded continuation predecessor does not retain its exact prior revision."
        )
    if continuation.revision.prior_note is not loaded_prior.revision.revised_note:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError(
            "Loaded continuation predecessor does not retain its exact prior note."
        )
    if continuation.revision.revised_note.note_text != verification.revised_note_text:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError(
            "Loaded continuation predecessor retained incoherent endpoint text."
        )

    return (
        verification.continuation_format,
        verification.continuation_record_sha256,
        continuation.revision.revised_note,
    )


def _validate_loaded_edge_predecessor(
    predecessor: ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord,
):
    verification = predecessor.verification

    if verification.edge_format != _EDGE_FORMAT:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError(
            "Loaded edge predecessor uses an unsupported edge format."
        )
    if verification.edge_mode != _EDGE_MODE:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError(
            "Loaded edge predecessor uses an unsupported edge mode."
        )
    if verification.revision_mode != _REVISION_MODE:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError(
            "Loaded edge predecessor retains an unsupported revision mode."
        )
    if verification.revised_note_mode != _NOTE_MODE:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError(
            "Loaded edge predecessor retains an unsupported note mode."
        )

    nested_format, nested_sha256, nested_note = _reported_predecessor_facts(
        predecessor.predecessor
    )
    if verification.predecessor_format != nested_format:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError(
            "Loaded edge predecessor retained an incoherent predecessor format."
        )
    if not hmac.compare_digest(
        verification.predecessor_record_sha256,
        nested_sha256,
    ):
        raise ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError(
            "Loaded edge predecessor retained an incoherent predecessor identity."
        )

    try:
        rebuilt = create_chromium_research_working_set_note_revision(
            nested_note,
            revised_note_text=verification.revised_note_text,
        )
    except ValueError as exc:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError(
            "Loaded edge predecessor cannot be re-established as an actual local revision."
        ) from exc

    if predecessor.revision.revision_mode != rebuilt.revision_mode:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError(
            "Loaded edge predecessor retained an incoherent revision mode."
        )
    if predecessor.revision.prior_note is not nested_note:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError(
            "Loaded edge predecessor does not retain its exact local predecessor note."
        )
    if (
        predecessor.revision.revised_note.working_set
        is not nested_note.working_set
    ):
        raise ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError(
            "Loaded edge predecessor does not retain the exact working set."
        )
    if predecessor.revision.revised_note.note_mode != verification.revised_note_mode:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError(
            "Loaded edge predecessor retained an incoherent revised-note mode."
        )
    if predecessor.revision.revised_note.note_text != verification.revised_note_text:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError(
            "Loaded edge predecessor retained incoherent endpoint text."
        )

    return (
        verification.edge_format,
        verification.edge_record_sha256,
        predecessor.revision.revised_note,
    )


def _reported_predecessor_facts(
    predecessor: (
        ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord
        | ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord
    ),
):
    """Return already-loaded predecessor facts without recursive ancestry validation."""

    if isinstance(
        predecessor,
        ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord,
    ):
        return (
            predecessor.verification.continuation_format,
            predecessor.verification.continuation_record_sha256,
            predecessor.continuation.revision.revised_note,
        )
    if isinstance(predecessor, ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord):
        return (
            predecessor.verification.edge_format,
            predecessor.verification.edge_record_sha256,
            predecessor.revision.revised_note,
        )
    raise TypeError(
        "loaded edge predecessor must itself retain a supported already-loaded predecessor."
    )
