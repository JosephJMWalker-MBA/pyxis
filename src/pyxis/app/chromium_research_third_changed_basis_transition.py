from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .chromium_research_second_basis_epoch_continuation_reentry_plan_document import (
    ChromiumResearchSecondBasisEpochContinuationReentryResult,
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


class ChromiumResearchThirdChangedBasisTransitionError(ValueError):
    """Raised when exact second-epoch continuation authority cannot support a third crossing."""


@dataclass(frozen=True, slots=True)
class ChromiumResearchThirdChangedBasisTransitionResult:
    """One explicit third changed-basis transition from exact second-epoch continuation.

    The result retains the exact mounted controller, the exact second-basis-epoch
    continuation re-entry supplied as two-root ancestry authority, the exact successful
    generic 44A preparation, the public 33B in-memory transition, its durable persistence
    evidence, and one fresh 33B relink from caller-explicit locators.

    It does not create the third 34A revision root, a third-epoch declared session,
    a 40A re-entry plan, a 40B overlay, or any current/latest/head state.
    """

    controller: ChromiumResearchSessionController
    continuation_reentry: ChromiumResearchSecondBasisEpochContinuationReentryResult
    prepared: ChromiumResearchSessionWorkingSetExtensionPersistenceResult
    transition: ChromiumResearchSessionWorkingSetTransitionRecord
    persistence: ChromiumResearchSessionWorkingSetTransitionPersistenceEvidence
    loaded_transition: ChromiumPageResearchLoadedWorkingSetTransitionRecord


def persist_chromium_research_third_changed_basis_transition(
    controller: ChromiumResearchSessionController,
    continuation_reentry: ChromiumResearchSecondBasisEpochContinuationReentryResult,
    prepared: ChromiumResearchSessionWorkingSetExtensionPersistenceResult,
    *,
    prior_edge_source: Path,
    working_set_source: Path,
    note_source: Path,
    destination: Path,
) -> ChromiumResearchThirdChangedBasisTransitionResult:
    """Persist and freshly relink one explicit third changed-basis transition.

    Eligibility is deliberately concrete. The caller must provide an exact
    second-basis-epoch continuation re-entry result whose retained controller is the
    supplied controller by object identity. This does not generalize 46A into an Nth
    transition abstraction.

    Every durable locator remains explicit. No path is taken from preparation receipts,
    persisted 37C/37D launch provenance, 38F handoff context, checkpoint paths, or any
    directory/current/latest/head inference.
    """

    if not isinstance(controller, ChromiumResearchSessionController):
        raise TypeError("controller must be ChromiumResearchSessionController.")
    if type(continuation_reentry) is not ChromiumResearchSecondBasisEpochContinuationReentryResult:
        raise TypeError(
            "continuation_reentry must be exactly "
            "ChromiumResearchSecondBasisEpochContinuationReentryResult."
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
        raise ChromiumResearchThirdChangedBasisTransitionError(
            "Prepared changed basis does not belong to the exact second-epoch continuation session."
        )
    if prepared.prior_endpoint is not controller.declared_endpoint:
        raise ChromiumResearchThirdChangedBasisTransitionError(
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
        raise ChromiumResearchThirdChangedBasisTransitionError(
            "Transition persistence did not retain the exact in-memory third-basis transition."
        )
    if loaded.verification.transition_record_sha256 != persistence.transition_record_sha256:
        raise ChromiumResearchThirdChangedBasisTransitionError(
            "Fresh transition relink identifies a different third-basis transition record."
        )
    if (
        loaded.prior_endpoint.verification.edge_record_sha256
        != controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchThirdChangedBasisTransitionError(
            "Fresh transition relink identifies a different second-epoch continuation endpoint."
        )
    if (
        loaded.successor_note.working_set.verification.working_set_record_sha256
        != prepared.working_set_persistence.working_set_record_sha256
    ):
        raise ChromiumResearchThirdChangedBasisTransitionError(
            "Fresh transition relink identifies a different prepared working set."
        )
    if (
        loaded.successor_note.verification.note_record_sha256
        != prepared.note_persistence.note_record_sha256
    ):
        raise ChromiumResearchThirdChangedBasisTransitionError(
            "Fresh transition relink identifies a different prepared working-set note."
        )

    return ChromiumResearchThirdChangedBasisTransitionResult(
        controller=controller,
        continuation_reentry=continuation_reentry,
        prepared=prepared,
        transition=transition,
        persistence=persistence,
        loaded_transition=loaded,
    )


def _require_continuation_reentry_matches_controller(
    controller: ChromiumResearchSessionController,
    continuation_reentry: ChromiumResearchSecondBasisEpochContinuationReentryResult,
) -> None:
    reentered = continuation_reentry.controller
    if reentered is not controller:
        raise ChromiumResearchThirdChangedBasisTransitionError(
            "Second-basis-epoch continuation re-entry controller does not match the supplied exact controller object."
        )
    if reentered.presentation != controller.presentation:
        raise ChromiumResearchThirdChangedBasisTransitionError(
            "Second-basis-epoch continuation re-entry does not describe the supplied controller presentation."
        )
    if (
        reentered.presentation.sequence.declaration_record_sha256
        != controller.presentation.sequence.declaration_record_sha256
    ):
        raise ChromiumResearchThirdChangedBasisTransitionError(
            "Second-basis-epoch continuation declaration identity does not match the supplied controller."
        )
    if (
        reentered.declared_endpoint.verification.edge_record_sha256
        != controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchThirdChangedBasisTransitionError(
            "Second-basis-epoch continuation endpoint identity does not match the supplied controller."
        )


def _require_path(value: Path, *, label: str) -> Path:
    if not isinstance(value, Path):
        raise TypeError(f"{label} must be pathlib.Path.")
    return value


__all__ = [
    "ChromiumResearchThirdChangedBasisTransitionError",
    "ChromiumResearchThirdChangedBasisTransitionResult",
    "persist_chromium_research_third_changed_basis_transition",
]
