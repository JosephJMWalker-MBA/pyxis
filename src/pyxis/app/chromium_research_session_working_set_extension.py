from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from .chromium_research_session_controller import ChromiumResearchSessionController
from .chromium_research_session_presentation import (
    ChromiumPageResearchSessionPresentation,
    present_chromium_research_session,
)
from .chromium_research_working_set import (
    ChromiumPageResearchWorkingSetItem,
    ChromiumPageResearchWorkingSetRecord,
    create_chromium_research_working_set,
)
from .chromium_research_working_set_note import (
    ChromiumPageResearchWorkingSetNoteRecord,
    create_chromium_research_working_set_note,
)
from .chromium_research_working_set_note_persistence import (
    ChromiumPageResearchWorkingSetNotePersistenceEvidence,
    persist_chromium_research_working_set_note,
)
from .chromium_research_working_set_note_revision_edge_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord,
)
from .chromium_research_working_set_persistence import (
    ChromiumPageResearchWorkingSetPersistenceEvidence,
    persist_chromium_research_working_set,
)


@dataclass(frozen=True, slots=True)
class ChromiumResearchSessionWorkingSetExtensionPersistenceResult:
    """One explicit durable evidence-basis extension prepared from a declared session.

    `prior_session` and `prior_endpoint` identify the exact declared research state
    from which the researcher chose to prepare a different working set.
    `appended_items` is the exact explicit ordered member tuple supplied by the
    caller. `working_set` preserves every prior member first, followed by those
    explicit appended members without deduplication or semantic interpretation.

    `note` is a newly authored human note over that changed working set. Its text is
    never inherited from the prior endpoint by Pyxis. The durable 20B/21B outputs
    form a prepared evidence basis only; they are not an adopted continuation of the
    prior revision chain and do not make the new evidence supportive of the note.
    """

    prior_session: ChromiumPageResearchSessionPresentation
    prior_endpoint: ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord
    prior_working_set: ChromiumPageResearchWorkingSetRecord
    appended_items: tuple[ChromiumPageResearchWorkingSetItem, ...]
    working_set: ChromiumPageResearchWorkingSetRecord
    working_set_persistence: ChromiumPageResearchWorkingSetPersistenceEvidence
    note: ChromiumPageResearchWorkingSetNoteRecord
    note_persistence: ChromiumPageResearchWorkingSetNotePersistenceEvidence


class ChromiumResearchSessionWorkingSetExtensionError(ValueError):
    """Raised when a declared session cannot prepare one explicit changed evidence basis."""


def persist_chromium_research_session_working_set_extension(
    controller: ChromiumResearchSessionController,
    appended_items: Iterable[ChromiumPageResearchWorkingSetItem],
    *,
    rationale_text: str,
    working_set_destination: Path,
    note_destination: Path,
) -> ChromiumResearchSessionWorkingSetExtensionPersistenceResult:
    """Persist one explicit changed working set plus one explicit new human rationale.

    The operation starts from the exact *declared* session endpoint retained by the
    supplied 29A controller. It never uses `last_endpoint_revision` as adoption or
    selection authority. Any unadopted successor write therefore remains unrelated
    bookkeeping for this operation.

    The caller supplies a non-empty ordered iterable of already-relinked 17D/18D/19D
    research members. Pyxis appends them after the exact current working-set member
    sequence and delegates membership coherence to public 20A. Duplicates are
    preserved because repetition is not treated as accidental.

    The caller must also supply human rationale text for the changed working set.
    Pyxis never copies the prior endpoint rationale automatically. The caller may
    deliberately provide identical text; explicit same wording is still a human
    choice over a different working set, not machine-inferred inheritance.

    Both durable destinations are explicit, distinct, no-overwrite paths and are
    preflighted before the first write. Persistence delegates to public 20B and 21B.
    The operation does not read member sidecars, acquire browser evidence, infer
    relevance/support, create a cross-working-set revision edge, rewrite a session
    declaration, adopt the prepared basis, select a head, or claim chronology.
    """

    if not isinstance(controller, ChromiumResearchSessionController):
        raise TypeError("controller must be ChromiumResearchSessionController.")

    rebuilt_session = present_chromium_research_session(controller.loaded)
    if rebuilt_session != controller.presentation:
        raise ChromiumResearchSessionWorkingSetExtensionError(
            "Research controller presentation is incoherent with its retained loaded evidence."
        )

    if isinstance(appended_items, (str, bytes, Path)):
        raise TypeError("appended_items must be an ordered iterable of loaded research members.")
    try:
        appended = tuple(appended_items)
    except TypeError as exc:
        raise TypeError(
            "appended_items must be an ordered iterable of loaded research members."
        ) from exc
    if not appended:
        raise ValueError("appended_items must contain at least one explicit loaded member.")

    endpoint = controller.declared_endpoint
    prior_note = endpoint.revision.revised_note
    prior_working_set = prior_note.working_set

    combined_items = (*prior_working_set.items, *appended)
    working_set = create_chromium_research_working_set(combined_items)
    if len(working_set.items) != len(prior_working_set.items) + len(appended):
        raise ChromiumResearchSessionWorkingSetExtensionError(
            "Extended working-set member count is incoherent with the explicit append operation."
        )
    for index, prior_item in enumerate(prior_working_set.items):
        if working_set.items[index] is not prior_item:
            raise ChromiumResearchSessionWorkingSetExtensionError(
                f"Extended working set did not preserve prior member {index} by exact object identity."
            )
    for offset, appended_item in enumerate(appended):
        observed = working_set.items[len(prior_working_set.items) + offset]
        if observed is not appended_item:
            raise ChromiumResearchSessionWorkingSetExtensionError(
                f"Extended working set did not preserve appended member {offset} by exact object identity."
            )

    note = create_chromium_research_working_set_note(
        working_set,
        note_text=rationale_text,
    )

    working_set_path = _preflight_destination(
        working_set_destination,
        label="working_set_destination",
    )
    note_path = _preflight_destination(
        note_destination,
        label="note_destination",
    )
    if working_set_path == note_path:
        raise ValueError("working_set_destination and note_destination must be distinct paths.")

    working_set_persistence = persist_chromium_research_working_set(
        working_set,
        working_set_path,
    )
    note_persistence = persist_chromium_research_working_set_note(
        note,
        working_set_persistence.path,
        note_path,
    )

    return ChromiumResearchSessionWorkingSetExtensionPersistenceResult(
        prior_session=controller.presentation,
        prior_endpoint=endpoint,
        prior_working_set=prior_working_set,
        appended_items=appended,
        working_set=working_set,
        working_set_persistence=working_set_persistence,
        note=note,
        note_persistence=note_persistence,
    )


def _preflight_destination(value: Path, *, label: str) -> Path:
    if not isinstance(value, Path):
        raise TypeError(f"{label} must be pathlib.Path.")
    path = value.expanduser().resolve()
    if not path.parent.is_dir():
        raise FileNotFoundError(f"{label} parent directory does not exist: {path.parent}")
    if path.exists():
        raise FileExistsError(f"{label} already exists: {path}")
    return path
