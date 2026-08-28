from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .chromium_research_session_controller import ChromiumResearchSessionController
from .chromium_research_session_reentry import ChromiumResearchSessionReentryResult
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


class ChromiumResearchFirstChangedBasisTransitionError(ValueError):
    """Raised when ordinary pre-root authority cannot support the first basis crossing."""


@dataclass(frozen=True, slots=True)
class ChromiumResearchFirstChangedBasisTransitionResult:
    """One explicit first changed-basis transition proven from ordinary 31A lineage.

    The result retains the exact mounted controller, the exact ordinary 31A re-entry
    evidence supplied for pre-root lineage authority, the exact successful 33A/44A
    preparation, the in-memory 33B transition, its durable persistence evidence, and
    one fresh 33B relink from the caller's explicit locators.

    It does not create a 34A revision root, a 35A declared root-backed session, an
    epoch, or any current/latest/head state.
    """

    controller: ChromiumResearchSessionController
    ordinary_reentry: ChromiumResearchSessionReentryResult
    prepared: ChromiumResearchSessionWorkingSetExtensionPersistenceResult
    transition: ChromiumResearchSessionWorkingSetTransitionRecord
    persistence: ChromiumResearchSessionWorkingSetTransitionPersistenceEvidence
    loaded_transition: ChromiumPageResearchLoadedWorkingSetTransitionRecord


def persist_chromium_research_first_changed_basis_transition(
    controller: ChromiumResearchSessionController,
    ordinary_reentry: ChromiumResearchSessionReentryResult,
    prepared: ChromiumResearchSessionWorkingSetExtensionPersistenceResult,
    *,
    prior_edge_source: Path,
    working_set_source: Path,
    note_source: Path,
    destination: Path,
) -> ChromiumResearchFirstChangedBasisTransitionResult:
    """Persist and freshly relink the first explicit changed-basis transition.

    Eligibility is deliberately narrower than public 33B. The caller must provide an
    exact ordinary 31A re-entry result coherent with the mounted controller. That
    re-entry family cannot encode root-backed ancestry, so it is the product-level
    authority that this is still the pre-root lineage rather than an arbitrary later
    evidence-basis epoch.

    Every durable locator remains explicit. No path is taken from the preparation
    receipts automatically, no file is discovered, and no root/session adoption is
    performed.
    """

    if not isinstance(controller, ChromiumResearchSessionController):
        raise TypeError("controller must be ChromiumResearchSessionController.")
    if type(ordinary_reentry) is not ChromiumResearchSessionReentryResult:
        raise TypeError(
            "ordinary_reentry must be exactly ChromiumResearchSessionReentryResult."
        )
    if not isinstance(
        prepared,
        ChromiumResearchSessionWorkingSetExtensionPersistenceResult,
    ):
        raise TypeError(
            "prepared must be ChromiumResearchSessionWorkingSetExtensionPersistenceResult."
        )

    _require_ordinary_reentry_matches_controller(controller, ordinary_reentry)
    if prepared.prior_session != controller.presentation:
        raise ChromiumResearchFirstChangedBasisTransitionError(
            "Prepared changed basis does not belong to the mounted ordinary session."
        )
    if prepared.prior_endpoint is not controller.declared_endpoint:
        raise ChromiumResearchFirstChangedBasisTransitionError(
            "Prepared changed basis does not retain the mounted controller's exact declared endpoint."
        )

    transition = create_chromium_research_session_working_set_transition(
        controller,
        prepared,
    )
    persistence = persist_chromium_research_session_working_set_transition(
        transition,
        prior_edge_source=_require_path(prior_edge_source, label="prior_edge_source"),
        working_set_source=_require_path(working_set_source, label="working_set_source"),
        note_source=_require_path(note_source, label="note_source"),
        destination=_require_path(destination, label="destination"),
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
        raise ChromiumResearchFirstChangedBasisTransitionError(
            "Transition persistence did not retain the exact in-memory transition."
        )
    if (
        loaded.verification.transition_record_sha256
        != persistence.transition_record_sha256
    ):
        raise ChromiumResearchFirstChangedBasisTransitionError(
            "Fresh transition relink identifies a different transition record."
        )
    if (
        loaded.prior_endpoint.verification.edge_record_sha256
        != controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchFirstChangedBasisTransitionError(
            "Fresh transition relink identifies a different prior endpoint."
        )
    if (
        loaded.successor_note.working_set.verification.working_set_record_sha256
        != prepared.working_set_persistence.working_set_record_sha256
    ):
        raise ChromiumResearchFirstChangedBasisTransitionError(
            "Fresh transition relink identifies a different prepared working set."
        )
    if (
        loaded.successor_note.verification.note_record_sha256
        != prepared.note_persistence.note_record_sha256
    ):
        raise ChromiumResearchFirstChangedBasisTransitionError(
            "Fresh transition relink identifies a different prepared working-set note."
        )

    return ChromiumResearchFirstChangedBasisTransitionResult(
        controller=controller,
        ordinary_reentry=ordinary_reentry,
        prepared=prepared,
        transition=transition,
        persistence=persistence,
        loaded_transition=loaded,
    )


def _require_ordinary_reentry_matches_controller(
    controller: ChromiumResearchSessionController,
    ordinary_reentry: ChromiumResearchSessionReentryResult,
) -> None:
    if ordinary_reentry.controller.presentation != controller.presentation:
        raise ChromiumResearchFirstChangedBasisTransitionError(
            "Ordinary re-entry does not describe the mounted controller presentation."
        )
    if (
        ordinary_reentry.controller.presentation.sequence.declaration_record_sha256
        != controller.presentation.sequence.declaration_record_sha256
    ):
        raise ChromiumResearchFirstChangedBasisTransitionError(
            "Ordinary re-entry declaration identity does not match the mounted controller."
        )
    if (
        ordinary_reentry.controller.declared_endpoint.verification.edge_record_sha256
        != controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchFirstChangedBasisTransitionError(
            "Ordinary re-entry endpoint identity does not match the mounted controller."
        )


def _require_path(value: Path, *, label: str) -> Path:
    if not isinstance(value, Path):
        raise TypeError(f"{label} must be pathlib.Path.")
    return value


__all__ = [
    "ChromiumResearchFirstChangedBasisTransitionError",
    "ChromiumResearchFirstChangedBasisTransitionResult",
    "persist_chromium_research_first_changed_basis_transition",
]
