from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from .chromium_research_second_basis_epoch_continuation_reentry_plan_document import (
    ChromiumResearchSecondBasisEpochContinuationReentryResult,
    load_chromium_research_second_basis_epoch_continuation_reentry_plan_document,
    reenter_chromium_research_second_basis_epoch_continuation,
)
from .chromium_research_session_controller import ChromiumResearchSessionController
from .chromium_research_session_reentry import (
    ChromiumResearchWorkingSetMemberReentryLocator,
    _load_member,
    _require_path,
    _snapshot_path_iterable,
    _validate_member_locator,
)
from .chromium_research_session_working_set_transition_revision_root_load import (
    ChromiumPageResearchLoadedWorkingSetTransitionRevisionRootRecord,
    load_chromium_research_session_working_set_transition_revision_root,
)
from .chromium_research_working_set import ChromiumPageResearchWorkingSetItem
from .chromium_research_working_set_note_revision_edge_sequence_declaration_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceDeclarationRecord,
    load_chromium_research_working_set_note_revision_edge_sequence_declaration,
)


@dataclass(frozen=True, slots=True)
class ChromiumResearchThirdBasisEpochReentryPlan:
    """Explicit locators for one third changed-evidence-basis session re-entry.

    The prior-session anchor is one explicitly supplied persisted 37C/37D second-epoch
    continuation overlay location. That overlay is decoded and freshly re-entered
    before the third basis-change region is reconstructed. First- and second-root
    ancestry therefore remain retained by the fresh prior continuation rather than
    copied or flattened into this plan.

    The remaining locators describe only the third epoch: explicitly appended
    research members, changed working-set/note evidence, one further 33B transition,
    one further 34A root, and the root-started ordinary declaration above that root.

    This plan is operational configuration only. It is not evidence, a recursive
    ancestry schema, a history index, a head pointer, or a chronology record.
    """

    prior_second_basis_epoch_continuation_overlay_source: Path
    appended_working_set_members: tuple[
        ChromiumResearchWorkingSetMemberReentryLocator, ...
    ]
    changed_working_set_source: Path
    changed_note_source: Path
    transition_source: Path
    root_source: Path
    declared_edge_sources: tuple[Path, ...]
    declaration_source: Path


@dataclass(frozen=True, slots=True)
class ChromiumResearchThirdBasisEpochReentryResult:
    """One freshly reconstructed third basis-change epoch above two-root ancestry."""

    plan: ChromiumResearchThirdBasisEpochReentryPlan
    prior_second_basis_epoch_continuation_reentry: ChromiumResearchSecondBasisEpochContinuationReentryResult
    loaded_appended_members: tuple[ChromiumPageResearchWorkingSetItem, ...]
    successor_items: tuple[ChromiumPageResearchWorkingSetItem, ...]
    loaded_root: ChromiumPageResearchLoadedWorkingSetTransitionRevisionRootRecord
    loaded_declaration: ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceDeclarationRecord
    controller: ChromiumResearchSessionController


class ChromiumResearchThirdBasisEpochReentryError(ValueError):
    """Raised when one explicit third basis-change epoch cannot be freshly re-entered."""


def create_chromium_research_third_basis_epoch_reentry_plan(
    prior_second_basis_epoch_continuation_overlay_source: Path,
    appended_working_set_members: Iterable[
        ChromiumResearchWorkingSetMemberReentryLocator
    ],
    *,
    changed_working_set_source: Path,
    changed_note_source: Path,
    transition_source: Path,
    root_source: Path,
    declared_edge_sources: Iterable[Path],
    declaration_source: Path,
) -> ChromiumResearchThirdBasisEpochReentryPlan:
    """Snapshot one explicit third-epoch locator plan without reading artifacts."""

    prior_overlay = _require_path(
        prior_second_basis_epoch_continuation_overlay_source,
        "prior_second_basis_epoch_continuation_overlay_source",
    )

    if isinstance(appended_working_set_members, (str, bytes, Path)):
        raise TypeError(
            "appended_working_set_members must be an ordered iterable of member locators."
        )
    try:
        appended = tuple(appended_working_set_members)
    except TypeError as exc:
        raise TypeError(
            "appended_working_set_members must be an ordered iterable of member locators."
        ) from exc
    if not appended:
        raise ValueError(
            "appended_working_set_members must contain at least one explicit member locator."
        )
    for index, member in enumerate(appended):
        _validate_member_locator(member, index=index)

    declared_sources = _snapshot_path_iterable(
        declared_edge_sources,
        label="declared_edge_sources",
        allow_empty=False,
    )

    return ChromiumResearchThirdBasisEpochReentryPlan(
        prior_second_basis_epoch_continuation_overlay_source=prior_overlay,
        appended_working_set_members=appended,
        changed_working_set_source=_require_path(
            changed_working_set_source,
            "changed_working_set_source",
        ),
        changed_note_source=_require_path(changed_note_source, "changed_note_source"),
        transition_source=_require_path(transition_source, "transition_source"),
        root_source=_require_path(root_source, "root_source"),
        declared_edge_sources=declared_sources,
        declaration_source=_require_path(declaration_source, "declaration_source"),
    )


def reenter_chromium_research_third_basis_epoch(
    plan: ChromiumResearchThirdBasisEpochReentryPlan,
) -> ChromiumResearchThirdBasisEpochReentryResult:
    """Freshly reconstruct one third changed-basis epoch from explicit locators.

    The exact prior 37C/37D continuation overlay is strictly decoded and its complete
    two-root ancestry is freshly re-entered first. Only that fresh governed endpoint
    becomes the pre-third-epoch endpoint.

    The explicitly appended third-epoch research members are then freshly relinked.
    Their successor order is the fresh prior endpoint's working-set order followed by
    the appended members in caller order. Existing 33B/34A loaders then re-establish
    the third transition/root, and the existing root-started declaration loader
    reconstructs the explicit ordinary segment above that third root.

    This proves one additional composition step only. It does not discover or walk a
    generic epoch chain and introduces no directory scan, format guessing, predecessor
    search, chronology, branch authority, current/latest/head selection, semantic-
    support judgment, authorship claim, or citation authority.
    """

    if not isinstance(plan, ChromiumResearchThirdBasisEpochReentryPlan):
        raise TypeError("plan must be ChromiumResearchThirdBasisEpochReentryPlan.")
    _validate_plan(plan)

    try:
        prior_plan = (
            load_chromium_research_second_basis_epoch_continuation_reentry_plan_document(
                plan.prior_second_basis_epoch_continuation_overlay_source
            )
        )
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchThirdBasisEpochReentryError(
            "Explicit prior 37C/37D second-basis-epoch continuation overlay could not be decoded."
        ) from exc

    try:
        prior_reentry = reenter_chromium_research_second_basis_epoch_continuation(
            prior_plan
        )
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchThirdBasisEpochReentryError(
            "Prior second-basis-epoch continuation could not be freshly re-entered."
        ) from exc

    loaded_appended: list[ChromiumPageResearchWorkingSetItem] = []
    for index, locator in enumerate(plan.appended_working_set_members):
        try:
            loaded_appended.append(_load_member(locator))
        except (OSError, TypeError, ValueError) as exc:
            raise ChromiumResearchThirdBasisEpochReentryError(
                f"Third-epoch appended working-set member {index} could not be freshly relinked from its explicit locator."
            ) from exc

    appended = tuple(loaded_appended)
    prior_endpoint = prior_reentry.controller.declared_endpoint
    prior_items = prior_endpoint.revision.revised_note.working_set.items
    successor_items = (*prior_items, *appended)

    try:
        loaded_root = load_chromium_research_session_working_set_transition_revision_root(
            prior_endpoint,
            successor_items,
            prior_edge_source=prior_endpoint.verification.path,
            working_set_source=plan.changed_working_set_source,
            note_source=plan.changed_note_source,
            transition_source=plan.transition_source,
            root_source=plan.root_source,
        )
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchThirdBasisEpochReentryError(
            "The explicit third changed working set, 33B transition, and 34A root could not be freshly relinked."
        ) from exc

    try:
        loaded_declaration = (
            load_chromium_research_working_set_note_revision_edge_sequence_declaration(
                loaded_root,
                plan.declared_edge_sources,
                plan.declaration_source,
            )
        )
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchThirdBasisEpochReentryError(
            "The explicit third root-backed declared segment could not be freshly reconciled with its declaration."
        ) from exc

    try:
        controller = ChromiumResearchSessionController(loaded_declaration)
    except (TypeError, ValueError) as exc:
        raise ChromiumResearchThirdBasisEpochReentryError(
            "Freshly relinked third-epoch declaration could not become a governed research-session controller."
        ) from exc

    return ChromiumResearchThirdBasisEpochReentryResult(
        plan=plan,
        prior_second_basis_epoch_continuation_reentry=prior_reentry,
        loaded_appended_members=appended,
        successor_items=successor_items,
        loaded_root=loaded_root,
        loaded_declaration=loaded_declaration,
        controller=controller,
    )


def _validate_plan(plan: ChromiumResearchThirdBasisEpochReentryPlan) -> None:
    _require_path(
        plan.prior_second_basis_epoch_continuation_overlay_source,
        "plan.prior_second_basis_epoch_continuation_overlay_source",
    )

    if (
        not isinstance(plan.appended_working_set_members, tuple)
        or not plan.appended_working_set_members
    ):
        raise TypeError(
            "plan.appended_working_set_members must be a non-empty tuple of member locators."
        )
    for index, member in enumerate(plan.appended_working_set_members):
        _validate_member_locator(member, index=index)

    for name in (
        "changed_working_set_source",
        "changed_note_source",
        "transition_source",
        "root_source",
        "declaration_source",
    ):
        _require_path(getattr(plan, name), f"plan.{name}")

    if not isinstance(plan.declared_edge_sources, tuple) or not plan.declared_edge_sources:
        raise TypeError("plan.declared_edge_sources must be a non-empty tuple of Paths.")
    for index, source in enumerate(plan.declared_edge_sources):
        _require_path(source, f"plan.declared_edge_sources[{index}]")


__all__ = [
    "ChromiumResearchThirdBasisEpochReentryError",
    "ChromiumResearchThirdBasisEpochReentryPlan",
    "ChromiumResearchThirdBasisEpochReentryResult",
    "create_chromium_research_third_basis_epoch_reentry_plan",
    "reenter_chromium_research_third_basis_epoch",
]
