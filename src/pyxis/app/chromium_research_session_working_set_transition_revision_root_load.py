from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
import hmac
from pathlib import Path

from .chromium_research_session_working_set_transition_load import (
    ChromiumPageResearchLoadedWorkingSetTransitionRecord,
    load_chromium_research_session_working_set_transition,
)
from .chromium_research_session_working_set_transition_revision_root import (
    ChromiumResearchSessionWorkingSetTransitionRevisionRootRecord,
    create_chromium_research_session_working_set_transition_revision_root,
)
from .chromium_research_session_working_set_transition_revision_root_persistence import (
    ChromiumResearchSessionWorkingSetTransitionRevisionRootVerificationEvidence,
    verify_chromium_research_session_working_set_transition_revision_root,
)
from .chromium_research_working_set import ChromiumPageResearchWorkingSetItem
from .chromium_research_working_set_note_revision_edge_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord,
)


_ROOT_FORMAT = (
    "pyxis.chromium.research_session_working_set_transition_revision_root.v1"
)
_TRANSITION_FORMAT = "pyxis.chromium.research_session_working_set_transition.v1"
_ROOT_MODE = (
    "caller_authored_revision_root_after_changed_research_working_set_transition"
)
_REVISION_MODE = "caller_authored_revision_of_research_working_set_note"
_NOTE_MODE = "caller_authored_note_on_research_working_set"


class ChromiumResearchSessionWorkingSetTransitionRevisionRootRelinkError(ValueError):
    """Raised when one durable 34A root cannot relink to an explicit 33B transition."""


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchLoadedWorkingSetTransitionRevisionRootRecord:
    """One verified 34A root freshly relinked through its exact 33B transition.

    `transition` is a fresh public-33B relink from every explicit durable input.
    `root` is a fresh in-memory 34A reconstruction whose first ordinary revision is
    over exactly that transition's successor note.

    The record preserves the basis-crossing as explicit local ancestry. It is not yet
    a 24C revision-edge predecessor, sequence declaration, session adoption, global
    history root, chronology claim, or current/latest/head selection.
    """

    verification: ChromiumResearchSessionWorkingSetTransitionRevisionRootVerificationEvidence
    transition: ChromiumPageResearchLoadedWorkingSetTransitionRecord
    root: ChromiumResearchSessionWorkingSetTransitionRevisionRootRecord


def load_chromium_research_session_working_set_transition_revision_root(
    prior_endpoint: ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord,
    successor_items: Iterable[ChromiumPageResearchWorkingSetItem],
    *,
    prior_edge_source: Path,
    working_set_source: Path,
    note_source: Path,
    transition_source: Path,
    root_source: Path,
) -> ChromiumPageResearchLoadedWorkingSetTransitionRevisionRootRecord:
    """Freshly relink one durable cross-working-set revision root.

    The caller supplies the same explicit prior endpoint context, complete ordered
    successor member sequence, and durable locators required by 33B plus the root
    file itself. Pyxis performs no discovery, ancestry traversal, path inference,
    ordering inference, chronology, or head selection.
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

    verification = verify_chromium_research_session_working_set_transition_revision_root(
        _require_path(root_source, label="root_source")
    )
    if verification.root_format != _ROOT_FORMAT:
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootRelinkError(
            "Verified cross-working-set revision root uses an unsupported format."
        )
    if verification.root_mode != _ROOT_MODE:
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootRelinkError(
            "Verified cross-working-set revision root uses an unsupported mode."
        )
    if verification.revision_mode != _REVISION_MODE:
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootRelinkError(
            "Verified cross-working-set revision root uses an unsupported revision mode."
        )
    if verification.revised_note_mode != _NOTE_MODE:
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootRelinkError(
            "Verified cross-working-set revision root uses an unsupported note mode."
        )

    transition = load_chromium_research_session_working_set_transition(
        prior_endpoint,
        items,
        prior_edge_source=_require_path(prior_edge_source, label="prior_edge_source"),
        working_set_source=_require_path(working_set_source, label="working_set_source"),
        note_source=_require_path(note_source, label="note_source"),
        transition_source=_require_path(transition_source, label="transition_source"),
    )
    if transition.verification.transition_format != _TRANSITION_FORMAT:
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootRelinkError(
            "Fresh transition uses an unsupported format."
        )
    if verification.transition_format != transition.verification.transition_format:
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootRelinkError(
            "Root references a different transition format."
        )
    if not hmac.compare_digest(
        verification.transition_record_sha256,
        transition.verification.transition_record_sha256,
    ):
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootRelinkError(
            "Root references a different transition record."
        )

    try:
        root = create_chromium_research_session_working_set_transition_revision_root(
            transition,
            revised_note_text=verification.revised_note_text,
        )
    except ValueError as exc:
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootRelinkError(
            "Verified root cannot be re-established as an actual revision of the transition successor note."
        ) from exc
    if root.root_mode != verification.root_mode:
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootRelinkError(
            "Reconstructed root mode does not match verified root bytes."
        )
    if root.revision.revision_mode != verification.revision_mode:
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootRelinkError(
            "Reconstructed root revision mode does not match verified root bytes."
        )
    if root.revision.revised_note.note_mode != verification.revised_note_mode:
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootRelinkError(
            "Reconstructed root revised-note mode does not match verified root bytes."
        )
    if root.revision.revised_note.note_text != verification.revised_note_text:
        raise ChromiumResearchSessionWorkingSetTransitionRevisionRootRelinkError(
            "Reconstructed root revised text does not match verified root bytes."
        )

    return ChromiumPageResearchLoadedWorkingSetTransitionRevisionRootRecord(
        verification=verification,
        transition=transition,
        root=root,
    )


def _require_path(value: Path, *, label: str) -> Path:
    if not isinstance(value, Path):
        raise TypeError(f"{label} must be pathlib.Path.")
    return value


__all__ = [
    "ChromiumPageResearchLoadedWorkingSetTransitionRevisionRootRecord",
    "ChromiumResearchSessionWorkingSetTransitionRevisionRootRelinkError",
    "load_chromium_research_session_working_set_transition_revision_root",
]
