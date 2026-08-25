from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from .chromium_research_session_controller import ChromiumResearchSessionController
from .chromium_research_session_reentry import (
    ChromiumResearchSessionReentryPlan,
    ChromiumResearchSessionReentryResult,
    ChromiumResearchWorkingSetMemberReentryLocator,
    _load_member,
    _require_path,
    _snapshot_path_iterable,
    _validate_member_locator,
    _validate_plan,
    reenter_chromium_research_session,
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
class ChromiumResearchRootBackedSessionReentryPlan:
    """Caller-owned locators for one explicit fresh root-backed session re-entry.

    `prior_session_plan` is one existing 31A locator plan that freshly reconstructs
    the exact ordinary governed session from which the evidence basis was changed.
    `appended_working_set_members` names only the explicit additional 17D/18D/19D
    members used by that changed basis; the prior members are recovered from the
    freshly reconstructed prior declared endpoint rather than duplicated in this
    plan.

    The remaining paths explicitly locate the changed 20B working set, changed 21B
    note, 33B transition, 34A root, 35A root-started ordinary edge sequence, and 26B
    declaration. This plan is operational configuration only. It is not research
    evidence, a history index, a head pointer, a chronology record, or a discovery
    mechanism.
    """

    prior_session_plan: ChromiumResearchSessionReentryPlan
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
class ChromiumResearchRootBackedSessionReentryResult:
    """One freshly reconstructed governed session whose declared segment starts at 34A.

    `prior_reentry` is a complete fresh 31A reconstruction of the ordinary session
    that owned the pre-change endpoint. `loaded_appended_members` contains only the
    additional explicitly located members. `successor_items` preserves the prior
    endpoint's exact working-set members first, followed by those additional members
    in exact caller order with duplicates retained.

    `loaded_root` freshly re-establishes the 33B transition and 34A root through
    explicit durable inputs. `loaded_declaration` then freshly reconciles the 35A
    root-started ordinary edge sequence and durable declaration. `controller` is the
    existing governed 29A controller built from that standard loaded declaration.
    """

    plan: ChromiumResearchRootBackedSessionReentryPlan
    prior_reentry: ChromiumResearchSessionReentryResult
    loaded_appended_members: tuple[ChromiumPageResearchWorkingSetItem, ...]
    successor_items: tuple[ChromiumPageResearchWorkingSetItem, ...]
    loaded_root: ChromiumPageResearchLoadedWorkingSetTransitionRevisionRootRecord
    loaded_declaration: ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceDeclarationRecord
    controller: ChromiumResearchSessionController


class ChromiumResearchRootBackedSessionReentryError(ValueError):
    """Raised when one explicit 35B root-backed fresh re-entry step cannot be proven."""


def create_chromium_research_root_backed_session_reentry_plan(
    prior_session_plan: ChromiumResearchSessionReentryPlan,
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
) -> ChromiumResearchRootBackedSessionReentryPlan:
    """Snapshot one explicit 35B locator plan without reading durable artifacts.

    The prior ordinary session remains represented by its established 31A typed plan
    rather than having all of its locators copied into a second schema. The caller
    supplies only the additional member locators and changed-basis/root/declaration
    paths needed beyond that prior plan.
    """

    if not isinstance(prior_session_plan, ChromiumResearchSessionReentryPlan):
        raise TypeError("prior_session_plan must be ChromiumResearchSessionReentryPlan.")
    _validate_plan(prior_session_plan)

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

    return ChromiumResearchRootBackedSessionReentryPlan(
        prior_session_plan=prior_session_plan,
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


def reenter_chromium_research_root_backed_session(
    plan: ChromiumResearchRootBackedSessionReentryPlan,
) -> ChromiumResearchRootBackedSessionReentryResult:
    """Freshly reconstruct one 35A root-backed governed session from explicit locators.

    The operation first delegates the complete pre-change session reconstruction to
    public 31A. It then freshly relinks only the explicitly appended members, derives
    the complete changed-basis member order from the freshly reconstructed prior
    endpoint plus those appended members, and delegates the 33B/34A relationship to
    the public 34A root loader.

    The prior endpoint's retained verification path is used as the 33B prior-edge
    locator because that path was itself reached through the explicit caller-owned
    31A plan and freshly verified during this same operation. Pyxis does not search
    for an edge by digest or infer another predecessor location.

    Finally, public 26C/35A freshly reconciles the explicitly supplied root-started
    edge paths with the durable declaration before the existing 29A controller is
    constructed.

    No directory scanning, digest discovery, browser reacquisition, path inference,
    automatic history traversal, chronology, branch selection, current/latest/head
    inference, evidence-support judgment, or semantic interpretation occurs.
    """

    if not isinstance(plan, ChromiumResearchRootBackedSessionReentryPlan):
        raise TypeError("plan must be ChromiumResearchRootBackedSessionReentryPlan.")
    _validate_root_backed_plan(plan)

    try:
        prior_reentry = reenter_chromium_research_session(plan.prior_session_plan)
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchRootBackedSessionReentryError(
            "The explicit prior ordinary research session could not be freshly re-entered."
        ) from exc

    loaded_appended: list[ChromiumPageResearchWorkingSetItem] = []
    for index, locator in enumerate(plan.appended_working_set_members):
        try:
            loaded_appended.append(_load_member(locator))
        except (OSError, TypeError, ValueError) as exc:
            raise ChromiumResearchRootBackedSessionReentryError(
                f"Appended working-set member {index} could not be freshly relinked from the explicit locator plan."
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
        raise ChromiumResearchRootBackedSessionReentryError(
            "The explicit changed working set, 33B transition, and 34A root could not be freshly relinked."
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
        raise ChromiumResearchRootBackedSessionReentryError(
            "The explicit root-backed declared segment could not be freshly reconciled with its declaration."
        ) from exc

    try:
        controller = ChromiumResearchSessionController(loaded_declaration)
    except (TypeError, ValueError) as exc:
        raise ChromiumResearchRootBackedSessionReentryError(
            "Freshly relinked root-backed declaration could not become a governed research-session controller."
        ) from exc

    return ChromiumResearchRootBackedSessionReentryResult(
        plan=plan,
        prior_reentry=prior_reentry,
        loaded_appended_members=appended,
        successor_items=successor_items,
        loaded_root=loaded_root,
        loaded_declaration=loaded_declaration,
        controller=controller,
    )


def _validate_root_backed_plan(plan: ChromiumResearchRootBackedSessionReentryPlan) -> None:
    if not isinstance(plan.prior_session_plan, ChromiumResearchSessionReentryPlan):
        raise TypeError("plan.prior_session_plan must be ChromiumResearchSessionReentryPlan.")
    _validate_plan(plan.prior_session_plan)

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
    "ChromiumResearchRootBackedSessionReentryError",
    "ChromiumResearchRootBackedSessionReentryPlan",
    "ChromiumResearchRootBackedSessionReentryResult",
    "create_chromium_research_root_backed_session_reentry_plan",
    "reenter_chromium_research_root_backed_session",
]
