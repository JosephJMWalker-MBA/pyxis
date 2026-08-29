from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .chromium_research_root_backed_session_continuation_reentry_plan_document import (
    ChromiumResearchRootBackedSessionContinuationReentryResult,
)
from .chromium_research_session_controller import ChromiumResearchSessionController
from .chromium_research_session_working_set_extension import (
    ChromiumResearchSessionWorkingSetExtensionPersistenceResult,
)
from .chromium_research_session_working_set_transition import (
    ChromiumResearchSessionWorkingSetTransitionRecord,
    create_chromium_research_session_working_set_transition,
)
from .chromium_research_session_working_set_transition_load import (
    ChromiumPageResearchLoadedWorkingSetTransitionRecord,
    load_chromium_research_session_working_set_transition,
)
from .chromium_research_session_working_set_transition_persistence import (
    ChromiumResearchSessionWorkingSetTransitionPersistenceEvidence,
    persist_chromium_research_session_working_set_transition,
)


class ChromiumResearchSecondChangedBasisTransitionError(ValueError):
    """Raised when exact one-root continuation authority cannot support a second crossing."""


@dataclass(frozen=True, slots=True)
class ChromiumResearchSecondChangedBasisTransitionResult:
    """One explicit second changed-basis transition from exact one-root continuation.

    The result retains the exact mounted controller, the exact root-backed
    continuation re-entry supplied as one-root ancestry authority, the exact
    successful 33A/44A preparation, the public 33B in-memory transition, its durable
    persistence evidence, and one fresh 33B relink from caller-explicit locators.

    It does not create the second 34A revision root, a second-epoch declared session,
    a 37A re-entry plan, or any current/latest/head state.
    """

    controller: ChromiumResearchSessionController
    continuation_reentry: ChromiumResearchRootBackedSessionContinuationReentryResult
    prepared: ChromiumResearchSessionWorkingSetExtensionPersistenceResult
    transition: ChromiumResearchSessionWorkingSetTransitionRecord
    persistence: ChromiumResearchSessionWorkingSetTransitionPersistenceEvidence
    loaded_transition: ChromiumPageResearchLoadedWorkingSetTransitionRecord


def persist_chromium_research_second_changed_basis_transition(
    controller: ChromiumResearchSessionController,
    continuation_reentry: ChromiumResearchRootBackedSessionContinuationReentryResult,
    prepared: ChromiumResearchSessionWorkingSetExtensionPersistenceResult,
    *,
    prior_edge_source: Path,
    working_set_source: Path,
    note_source: Path,
    destination: Path,
) -> ChromiumResearchSecondChangedBasisTransitionResult:
    """Persist and freshly relink one explicit second changed-basis transition.

    Eligibility is deliberately concrete. The caller must provide an exact one-root
    continuation re-entry result whose retained controller is the supplied controller.
    This does not generalize 44B's first-crossing authority and does not create an
    Nth-transition abstraction.

    Every durable locator remains explicit. No path is taken from preparation
    receipts, continuation plans, persisted launch provenance, checkpoint paths, or
    raw in-process handoff context.
    """

    if not isinstance(controller, ChromiumResearchSessionController):
        raise TypeError("controller must be ChromiumResearchSessionController.")
    if type(continuation_reentry) is not ChromiumResearchRootBackedSessionContinuationReentryResult:
        raise TypeError(
            "continuation_reentry must be exactly "
            "ChromiumResearchRootBackedSessionContinuationReentryResult."
        )
    if not isinstance(
        prepared,
        ChromiumResearchSessionWorkingSetExtensionPersistenceResult,
    ):
        raise TypeError(
            "prepared must be ChromiumResearchSessionWorkingSetExtensionPersistenceResult."
        )

    _require_continuation_reentry_matches_controller(controller, continuation_reentry)
    if prepared.prior_session != controller.presentation:
        raise ChromiumResearchSecondChangedBasisTransitionError(
            "Prepared changed basis does not belong to the exact one-root continuation session."
        )
    if prepared.prior_endpoint is not controller.declared_endpoint:
        raise ChromiumResearchSecondChangedBasisTransitionError(
            "Prepared changed basis does not retain the supplied controller's exact declared endpoint."
        )

    prior_edge_source = _require_path(prior_edge_source, label="prior_edge_source")
    working_set_source = _require_path(working_set_source, label="working_set_source")
    note_source = _require_path(note_source, label="note_source")
    destination = _require_path(destination, label="destination")

    transition = create_chromium_research_session_working_set_transition(
        controller,
        prepared,
    )
    persistence = persist_chromium_research_session_working_set_transition(
        transition,
        prior_edge_source=prior_edge_source,
        working_set_source=working_set_source,
        note_source=note_source,
        destination=destination,
    )
    loaded = load_chromium_research_session_working_set_transition(
        controller.declared_endpoint,
        prepared.working_set.items,
        prior_edge_source=prior_edge_source,
        working_set_source=working_set_source,
        note_source=note_source,
        transition_source=persistence.path,
    )

    if persistence.transition is not transition:
        raise ChromiumResearchSecondChangedBasisTransitionError(
            "Transition persistence did not retain the exact in-memory second-basis transition."
        )
    if loaded.verification.transition_record_sha256 != persistence.transition_record_sha256:
        raise ChromiumResearchSecondChangedBasisTransitionError(
            "Fresh transition relink identifies a different second-basis transition record."
        )
    if (
        loaded.prior_endpoint.verification.edge_record_sha256
        != controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchSecondChangedBasisTransitionError(
            "Fresh transition relink identifies a different one-root continuation endpoint."
        )
    if (
        loaded.successor_note.working_set.verification.working_set_record_sha256
        != prepared.working_set_persistence.working_set_record_sha256
    ):
        raise ChromiumResearchSecondChangedBasisTransitionError(
            "Fresh transition relink identifies a different prepared working set."
        )
    if (
        loaded.successor_note.verification.note_record_sha256
        != prepared.note_persistence.note_record_sha256
    ):
        raise ChromiumResearchSecondChangedBasisTransitionError(
            "Fresh transition relink identifies a different prepared working-set note."
        )

    return ChromiumResearchSecondChangedBasisTransitionResult(
        controller=controller,
        continuation_reentry=continuation_reentry,
        prepared=prepared,
        transition=transition,
        persistence=persistence,
        loaded_transition=loaded,
    )


def _require_continuation_reentry_matches_controller(
    controller: ChromiumResearchSessionController,
    continuation_reentry: ChromiumResearchRootBackedSessionContinuationReentryResult,
) -> None:
    reentered = continuation_reentry.controller
    if reentered is not controller:
        raise ChromiumResearchSecondChangedBasisTransitionError(
            "Root-backed continuation re-entry controller does not match the supplied exact controller object."
        )
    if reentered.presentation != controller.presentation:
        raise ChromiumResearchSecondChangedBasisTransitionError(
            "Root-backed continuation re-entry does not describe the supplied controller presentation."
        )
    if (
        reentered.presentation.sequence.declaration_record_sha256
        != controller.presentation.sequence.declaration_record_sha256
    ):
        raise ChromiumResearchSecondChangedBasisTransitionError(
            "Root-backed continuation declaration identity does not match the supplied controller."
        )
    if (
        reentered.declared_endpoint.verification.edge_record_sha256
        != controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchSecondChangedBasisTransitionError(
            "Root-backed continuation endpoint identity does not match the supplied controller."
        )


def _require_path(value: Path, *, label: str) -> Path:
    if not isinstance(value, Path):
        raise TypeError(f"{label} must be pathlib.Path.")
    return value


__all__ = [
    "ChromiumResearchSecondChangedBasisTransitionError",
    "ChromiumResearchSecondChangedBasisTransitionResult",
    "persist_chromium_research_second_changed_basis_transition",
]
