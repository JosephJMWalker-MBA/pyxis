from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from .chromium_research_root_backed_session_continuation_reentry_plan_document import (
    ChromiumResearchRootBackedSessionContinuationReentryResult,
    load_chromium_research_root_backed_session_continuation_reentry_plan_document,
    reenter_chromium_research_root_backed_session_continuation,
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
class ChromiumResearchSecondBasisEpochReentryPlan:
    """Explicit locators for one second changed-evidence-basis session re-entry.

    The prior-session anchor is one persisted 35D/35E continuation overlay location.
    That overlay is decoded and freshly re-entered before the second basis-change
    region is reconstructed. The first root-backed ancestry is therefore retained by
    the fresh prior continuation rather than flattened into an ordinary 31A plan or
    copied into this plan.

    The remaining locators describe only the second epoch: explicitly appended
    research members, changed working-set/note evidence, the second 33B transition,
    the second 34A root, and the root-started ordinary declaration above that root.

    This plan is operational configuration only. It is not evidence, a history index,
    a recursive ancestry schema, a head pointer, or a chronology record.
    """

    prior_root_backed_continuation_overlay_source: Path
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
class ChromiumResearchSecondBasisEpochReentryResult:
    """One freshly reconstructed second basis-change epoch above prior root ancestry.

    `prior_continuation_reentry` preserves the complete fresh first-epoch root-backed
    continuation reconstructed from the explicit 35D/35E overlay. `loaded_root` is a
    distinct second 34A root freshly relinked from that prior continuation's declared
    endpoint and the explicit second changed evidence basis.

    No Python object identity is treated as durable authority across those independent
    loads. Durable relationships are re-established through the existing public
    loaders and explicit record identities.
    """

    plan: ChromiumResearchSecondBasisEpochReentryPlan
    prior_continuation_reentry: ChromiumResearchRootBackedSessionContinuationReentryResult
    loaded_appended_members: tuple[ChromiumPageResearchWorkingSetItem, ...]
    successor_items: tuple[ChromiumPageResearchWorkingSetItem, ...]
    loaded_root: ChromiumPageResearchLoadedWorkingSetTransitionRevisionRootRecord
    loaded_declaration: ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceDeclarationRecord
    controller: ChromiumResearchSessionController


class ChromiumResearchSecondBasisEpochReentryError(ValueError):
    """Raised when one explicit second basis-change epoch cannot be freshly re-entered."""


def create_chromium_research_second_basis_epoch_reentry_plan(
    prior_root_backed_continuation_overlay_source: Path,
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
) -> ChromiumResearchSecondBasisEpochReentryPlan:
    """Snapshot one explicit second-epoch locator plan without reading artifacts.

    The prior 35D/35E overlay is retained only as an explicit location. Construction
    does not decode that overlay, read research evidence, scan directories, discover
    predecessors, infer a format, or select a latest/current/head state.
    """

    prior_overlay = _require_path(
        prior_root_backed_continuation_overlay_source,
        "prior_root_backed_continuation_overlay_source",
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

    return ChromiumResearchSecondBasisEpochReentryPlan(
        prior_root_backed_continuation_overlay_source=prior_overlay,
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


def reenter_chromium_research_second_basis_epoch(
    plan: ChromiumResearchSecondBasisEpochReentryPlan,
) -> ChromiumResearchSecondBasisEpochReentryResult:
    """Freshly reconstruct one second changed-basis epoch from explicit locators.

    First, the exact prior 35D/35E overlay is strictly decoded and its complete first
    root-backed continuation is freshly re-entered through the existing public
    boundary. Only that fresh controller supplies the pre-change declared endpoint.

    Next, only the explicitly appended second-epoch research members are freshly
    relinked. Their complete successor order is derived from the fresh prior endpoint's
    current working-set members followed by those appended members in caller order.

    The existing public 34A root loader then freshly re-establishes the second 33B
    transition/root from every explicit second-epoch durable locator. Finally, the
    existing root-started 35A/26C declaration loader reconstructs the declared ordinary
    segment above the second root and the standard governed controller is created.

    No first-epoch ancestry is flattened into an ordinary plan. No directory scan,
    digest discovery, predecessor search, path inference, automatic ancestry walk,
    chronology, branch selection, current/latest/head selection, semantic-support
    judgment, authorship claim, or citation authority is introduced.
    """

    if not isinstance(plan, ChromiumResearchSecondBasisEpochReentryPlan):
        raise TypeError("plan must be ChromiumResearchSecondBasisEpochReentryPlan.")
    _validate_plan(plan)

    try:
        prior_plan = (
            load_chromium_research_root_backed_session_continuation_reentry_plan_document(
                plan.prior_root_backed_continuation_overlay_source
            )
        )
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchSecondBasisEpochReentryError(
            "Explicit prior 35D/35E continuation overlay could not be decoded."
        ) from exc

    try:
        prior_reentry = reenter_chromium_research_root_backed_session_continuation(
            prior_plan
        )
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchSecondBasisEpochReentryError(
            "Prior root-backed continuation could not be freshly re-entered."
        ) from exc

    loaded_appended: list[ChromiumPageResearchWorkingSetItem] = []
    for index, locator in enumerate(plan.appended_working_set_members):
        try:
            loaded_appended.append(_load_member(locator))
        except (OSError, TypeError, ValueError) as exc:
            raise ChromiumResearchSecondBasisEpochReentryError(
                f"Second-epoch appended working-set member {index} could not be freshly relinked from its explicit locator."
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
        raise ChromiumResearchSecondBasisEpochReentryError(
            "The explicit second changed working set, 33B transition, and 34A root could not be freshly relinked."
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
        raise ChromiumResearchSecondBasisEpochReentryError(
            "The explicit second root-backed declared segment could not be freshly reconciled with its declaration."
        ) from exc

    try:
        controller = ChromiumResearchSessionController(loaded_declaration)
    except (TypeError, ValueError) as exc:
        raise ChromiumResearchSecondBasisEpochReentryError(
            "Freshly relinked second-epoch declaration could not become a governed research-session controller."
        ) from exc

    return ChromiumResearchSecondBasisEpochReentryResult(
        plan=plan,
        prior_continuation_reentry=prior_reentry,
        loaded_appended_members=appended,
        successor_items=successor_items,
        loaded_root=loaded_root,
        loaded_declaration=loaded_declaration,
        controller=controller,
    )


def _validate_plan(plan: ChromiumResearchSecondBasisEpochReentryPlan) -> None:
    _require_path(
        plan.prior_root_backed_continuation_overlay_source,
        "plan.prior_root_backed_continuation_overlay_source",
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
    "ChromiumResearchSecondBasisEpochReentryError",
    "ChromiumResearchSecondBasisEpochReentryPlan",
    "ChromiumResearchSecondBasisEpochReentryResult",
    "create_chromium_research_second_basis_epoch_reentry_plan",
    "reenter_chromium_research_second_basis_epoch",
]
