from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
import hmac
from pathlib import Path

from .chromium_research_session_working_set_transition_persistence import (
    ChromiumResearchSessionWorkingSetTransitionVerificationEvidence,
    verify_chromium_research_session_working_set_transition,
)
from .chromium_research_working_set import ChromiumPageResearchWorkingSetItem
from .chromium_research_working_set_note_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRecord,
    load_chromium_research_working_set_note,
)
from .chromium_research_working_set_note_revision_edge_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord,
    load_chromium_research_working_set_note_revision_edge,
)


_TRANSITION_FORMAT = "pyxis.chromium.research_session_working_set_transition.v1"
_TRANSITION_MODE = "caller_explicit_transition_to_changed_research_working_set"
_EDGE_FORMAT = "pyxis.chromium.research_working_set_note_revision_edge.v1"
_WORKING_SET_FORMAT = "pyxis.chromium.research_working_set.v1"
_NOTE_FORMAT = "pyxis.chromium.research_working_set_note.v1"


class ChromiumResearchSessionWorkingSetTransitionRelinkError(ValueError):
    """Raised when one durable transition cannot relink to explicit durable inputs."""


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchLoadedWorkingSetTransitionRecord:
    """One verified transition freshly relinked to explicit prior and successor records.

    `prior_endpoint` is a fresh public-24C reopen of the explicit old endpoint file.
    `successor_note` is a fresh public-21C reopen of the explicit changed 20B/21B
    evidence basis. The transition verification must identify exactly those durable
    records.

    This establishes one local cross-working-set relationship only. It is not a
    normal revision edge, recursive history traversal, session declaration, chronology
    claim, branch/head selection, or semantic-support assertion.
    """

    verification: ChromiumResearchSessionWorkingSetTransitionVerificationEvidence
    prior_endpoint: ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord
    successor_note: ChromiumPageResearchLoadedWorkingSetNoteRecord


def load_chromium_research_session_working_set_transition(
    prior_endpoint: ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord,
    successor_items: Iterable[ChromiumPageResearchWorkingSetItem],
    *,
    prior_edge_source: Path,
    working_set_source: Path,
    note_source: Path,
    transition_source: Path,
) -> ChromiumPageResearchLoadedWorkingSetTransitionRecord:
    """Freshly relink one durable transition against caller-supplied locators.

    The caller supplies the already-loaded predecessor context for the old edge, the
    complete ordered successor member sequence, and every durable path. Pyxis performs
    no path discovery, digest search, directory scan, member discovery, chronology
    inference, or current/head selection.
    """

    if not isinstance(
        prior_endpoint,
        ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord,
    ):
        raise TypeError(
            "prior_endpoint must be ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord."
        )
    if isinstance(successor_items, (str, bytes, Path)):
        raise TypeError("successor_items must be an ordered iterable of loaded research members.")
    try:
        items = tuple(successor_items)
    except TypeError as exc:
        raise TypeError(
            "successor_items must be an ordered iterable of loaded research members."
        ) from exc

    verification = verify_chromium_research_session_working_set_transition(
        _require_path(transition_source, label="transition_source")
    )
    if verification.transition_format != _TRANSITION_FORMAT:
        raise ChromiumResearchSessionWorkingSetTransitionRelinkError(
            "Verified transition uses an unsupported format."
        )
    if verification.transition_mode != _TRANSITION_MODE:
        raise ChromiumResearchSessionWorkingSetTransitionRelinkError(
            "Verified transition uses an unsupported mode."
        )

    fresh_prior = load_chromium_research_working_set_note_revision_edge(
        prior_endpoint.predecessor,
        _require_path(prior_edge_source, label="prior_edge_source"),
    )
    if fresh_prior.verification.edge_format != _EDGE_FORMAT:
        raise ChromiumResearchSessionWorkingSetTransitionRelinkError(
            "Fresh prior endpoint uses an unsupported edge format."
        )
    if prior_endpoint.verification.edge_format != fresh_prior.verification.edge_format:
        raise ChromiumResearchSessionWorkingSetTransitionRelinkError(
            "Supplied prior endpoint and fresh prior endpoint use different formats."
        )
    if not hmac.compare_digest(
        prior_endpoint.verification.edge_record_sha256,
        fresh_prior.verification.edge_record_sha256,
    ):
        raise ChromiumResearchSessionWorkingSetTransitionRelinkError(
            "Explicit prior edge source identifies a different endpoint record."
        )
    if verification.prior_endpoint_format != fresh_prior.verification.edge_format:
        raise ChromiumResearchSessionWorkingSetTransitionRelinkError(
            "Transition references a different prior endpoint format."
        )
    if not hmac.compare_digest(
        verification.prior_endpoint_record_sha256,
        fresh_prior.verification.edge_record_sha256,
    ):
        raise ChromiumResearchSessionWorkingSetTransitionRelinkError(
            "Transition references a different prior endpoint record."
        )

    fresh_successor = load_chromium_research_working_set_note(
        items,
        _require_path(working_set_source, label="working_set_source"),
        _require_path(note_source, label="note_source"),
    )
    if fresh_successor.working_set.verification.working_set_format != _WORKING_SET_FORMAT:
        raise ChromiumResearchSessionWorkingSetTransitionRelinkError(
            "Fresh successor working set uses an unsupported format."
        )
    if fresh_successor.verification.note_format != _NOTE_FORMAT:
        raise ChromiumResearchSessionWorkingSetTransitionRelinkError(
            "Fresh successor note uses an unsupported format."
        )
    if (
        verification.successor_working_set_format
        != fresh_successor.working_set.verification.working_set_format
    ):
        raise ChromiumResearchSessionWorkingSetTransitionRelinkError(
            "Transition references a different successor working-set format."
        )
    if not hmac.compare_digest(
        verification.successor_working_set_record_sha256,
        fresh_successor.working_set.verification.working_set_record_sha256,
    ):
        raise ChromiumResearchSessionWorkingSetTransitionRelinkError(
            "Transition references a different successor working-set record."
        )
    if verification.successor_note_format != fresh_successor.verification.note_format:
        raise ChromiumResearchSessionWorkingSetTransitionRelinkError(
            "Transition references a different successor-note format."
        )
    if not hmac.compare_digest(
        verification.successor_note_record_sha256,
        fresh_successor.verification.note_record_sha256,
    ):
        raise ChromiumResearchSessionWorkingSetTransitionRelinkError(
            "Transition references a different successor-note record."
        )

    return ChromiumPageResearchLoadedWorkingSetTransitionRecord(
        verification=verification,
        prior_endpoint=fresh_prior,
        successor_note=fresh_successor,
    )


def _require_path(value: Path, *, label: str) -> Path:
    if not isinstance(value, Path):
        raise TypeError(f"{label} must be pathlib.Path.")
    return value
