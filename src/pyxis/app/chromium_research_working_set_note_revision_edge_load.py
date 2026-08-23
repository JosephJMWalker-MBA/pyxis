from __future__ import annotations

from dataclasses import dataclass
import hmac
from pathlib import Path
from typing import TYPE_CHECKING

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

if TYPE_CHECKING:
    from .chromium_research_session_working_set_transition_revision_root_load import (
        ChromiumPageResearchLoadedWorkingSetTransitionRevisionRootRecord,
    )


_EDGE_FORMAT = "pyxis.chromium.research_working_set_note_revision_edge.v1"
_CONTINUATION_FORMAT = (
    "pyxis.chromium.research_working_set_note_revision_continuation.v1"
)
_ROOT_FORMAT = (
    "pyxis.chromium.research_session_working_set_transition_revision_root.v1"
)
_ROOT_MODE = (
    "caller_authored_revision_root_after_changed_research_working_set_transition"
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

    `predecessor` is retained by exact object identity and may be one loaded 23C
    continuation, one loaded 34A cross-working-set revision root, or another loaded
    24C edge. `revision` is freshly reconstructed through public 22A over exactly
    that predecessor's endpoint note.

    This record establishes only one explicit local predecessor relationship. It
    does not discover predecessors, recursively load files, establish a global
    history head, infer chronology, detect durable cycles, or make semantic claims.
    """

    verification: ChromiumPageResearchWorkingSetNoteRevisionEdgeVerificationEvidence
    predecessor: (
        ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord
        | ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord
        | ChromiumPageResearchLoadedWorkingSetTransitionRevisionRootRecord
    )
    revision: ChromiumPageResearchWorkingSetNoteRevisionRecord


def load_chromium_research_working_set_note_revision_edge(
    predecessor: (
        ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord
        | ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord
        | ChromiumPageResearchLoadedWorkingSetTransitionRevisionRootRecord
    ),
    edge_source: Path,
) -> ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord:
    """Relink one 24B edge to one explicit already-loaded predecessor.

    The caller chooses and supplies the predecessor object. Pyxis freshly verifies
    only `edge_source`; it performs no digest search, directory scan, predecessor
    discovery, recursive file loading, chain traversal, current-head selection,
    revision numbering, timestamp inference, or semantic comparison.

    Since 34B, the predecessor may also be one already-loaded 34A cross-working-set
    revision root. That widens only this local edge relationship; it does not make
    the root a 26A sequence start or a declared/current session head.
    """

    from .chromium_research_session_working_set_transition_revision_root_load import (
        ChromiumPageResearchLoadedWorkingSetTransitionRevisionRootRecord,
    )

    if not isinstance(
        predecessor,
        (
            ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord,
            ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord,
            ChromiumPageResearchLoadedWorkingSetTransitionRevisionRootRecord,
        ),
    ):
        raise TypeError(
            "predecessor must be an already-loaded 23C continuation, 24C revision "
            "edge, or 34A cross-working-set revision root."
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


def _validate_loaded_predecessor(predecessor):
    from .chromium_research_session_working_set_transition_revision_root_load import (
        ChromiumPageResearchLoadedWorkingSetTransitionRevisionRootRecord,
    )

    if isinstance(
        predecessor,
        ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord,
    ):
        return _validate_loaded_continuation_predecessor(predecessor)
    if isinstance(predecessor, ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord):
        return _validate_loaded_edge_predecessor(predecessor)
    if isinstance(
        predecessor,
        ChromiumPageResearchLoadedWorkingSetTransitionRevisionRootRecord,
    ):
        return _validate_loaded_root_predecessor(predecessor)
    raise TypeError(
        "loaded predecessor must be an already-loaded 23C continuation, 24C edge, "
        "or 34A cross-working-set revision root."
    )


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


def _validate_loaded_root_predecessor(predecessor):
    from .chromium_research_session_working_set_transition_revision_root import (
        create_chromium_research_session_working_set_transition_revision_root,
    )
    from .chromium_research_session_working_set_transition_revision_root_load import (
        ChromiumPageResearchLoadedWorkingSetTransitionRevisionRootRecord,
    )

    if not isinstance(
        predecessor,
        ChromiumPageResearchLoadedWorkingSetTransitionRevisionRootRecord,
    ):
        raise TypeError(
            "root predecessor must be "
            "ChromiumPageResearchLoadedWorkingSetTransitionRevisionRootRecord."
        )

    verification = predecessor.verification
    transition = predecessor.transition
    root = predecessor.root
    if verification.root_format != _ROOT_FORMAT:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError(
            "Loaded root predecessor uses an unsupported format."
        )
    if verification.root_mode != _ROOT_MODE:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError(
            "Loaded root predecessor uses an unsupported mode."
        )
    if verification.revision_mode != _REVISION_MODE:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError(
            "Loaded root predecessor retains an unsupported revision mode."
        )
    if verification.revised_note_mode != _NOTE_MODE:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError(
            "Loaded root predecessor retains an unsupported note mode."
        )
    if verification.transition_format != transition.verification.transition_format:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError(
            "Loaded root predecessor retained an incoherent transition format."
        )
    if not hmac.compare_digest(
        verification.transition_record_sha256,
        transition.verification.transition_record_sha256,
    ):
        raise ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError(
            "Loaded root predecessor retained an incoherent transition identity."
        )
    if root.transition is not transition:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError(
            "Loaded root predecessor does not retain its exact transition object."
        )

    try:
        rebuilt = create_chromium_research_session_working_set_transition_revision_root(
            transition,
            revised_note_text=verification.revised_note_text,
        )
    except ValueError as exc:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError(
            "Loaded root predecessor cannot be re-established as an actual root revision."
        ) from exc

    if root.root_mode != rebuilt.root_mode:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError(
            "Loaded root predecessor retained an incoherent root mode."
        )
    if root.revision.prior_note is not transition.successor_note.note:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError(
            "Loaded root predecessor does not retain the exact transition successor note."
        )
    if root.revision.revised_note.working_set is not transition.successor_note.note.working_set:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError(
            "Loaded root predecessor does not retain the exact changed working set."
        )
    if root.revision.revised_note.note_mode != verification.revised_note_mode:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError(
            "Loaded root predecessor retained an incoherent revised-note mode."
        )
    if root.revision.revised_note.note_text != verification.revised_note_text:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError(
            "Loaded root predecessor retained incoherent endpoint text."
        )

    return (
        verification.root_format,
        verification.root_record_sha256,
        root.revision.revised_note,
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
            "Loaded edge predecessor uses an unsupported mode."
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
    if predecessor.revision.revised_note.working_set is not nested_note.working_set:
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


def _reported_predecessor_facts(predecessor):
    """Return already-loaded predecessor facts without recursive ancestry validation."""

    from .chromium_research_session_working_set_transition_revision_root_load import (
        ChromiumPageResearchLoadedWorkingSetTransitionRevisionRootRecord,
    )

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
    if isinstance(
        predecessor,
        ChromiumPageResearchLoadedWorkingSetTransitionRevisionRootRecord,
    ):
        return (
            predecessor.verification.root_format,
            predecessor.verification.root_record_sha256,
            predecessor.root.revision.revised_note,
        )
    raise TypeError(
        "loaded edge predecessor must itself retain a supported already-loaded predecessor."
    )
