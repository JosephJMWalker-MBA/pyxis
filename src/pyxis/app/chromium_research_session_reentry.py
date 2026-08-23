from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import TypeAlias

from .chromium_research_capture_load import load_chromium_page_research_capture
from .chromium_research_paragraph_text_selection_comparison_note_load import (
    load_chromium_research_paragraph_text_selection_comparison_note,
)
from .chromium_research_paragraph_text_selection_note_load import (
    load_chromium_research_paragraph_text_selection_note,
)
from .chromium_research_selection_note_load import load_chromium_research_paragraph_note
from .chromium_research_session_controller import ChromiumResearchSessionController
from .chromium_research_working_set import ChromiumPageResearchWorkingSetItem
from .chromium_research_working_set_note_revision_continuation_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord,
    load_chromium_research_working_set_note_revision_continuation,
)
from .chromium_research_working_set_note_revision_edge_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord,
    load_chromium_research_working_set_note_revision_edge,
)
from .chromium_research_working_set_note_revision_edge_sequence_declaration_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceDeclarationRecord,
    load_chromium_research_working_set_note_revision_edge_sequence_declaration,
)


@dataclass(frozen=True, slots=True)
class ChromiumResearchParagraphNoteReentryLocator:
    """Explicit locations needed to freshly relink one durable 17D paragraph note."""

    capture_source: Path
    note_source: Path


@dataclass(frozen=True, slots=True)
class ChromiumResearchExactRangeNoteReentryLocator:
    """Explicit locations needed to freshly relink one durable 18D exact-range note."""

    capture_source: Path
    note_source: Path


@dataclass(frozen=True, slots=True)
class ChromiumResearchComparisonNoteReentryLocator:
    """Explicit ordered locations needed to freshly relink one durable 19D comparison note."""

    first_capture_source: Path
    second_capture_source: Path
    note_source: Path


ChromiumResearchWorkingSetMemberReentryLocator: TypeAlias = (
    ChromiumResearchParagraphNoteReentryLocator
    | ChromiumResearchExactRangeNoteReentryLocator
    | ChromiumResearchComparisonNoteReentryLocator
)


@dataclass(frozen=True, slots=True)
class ChromiumResearchSessionReentryPlan:
    """Caller-owned locator plan for one explicit fresh research-session re-entry.

    This record contains locations and caller-declared order only. It is not a
    research-evidence artifact, content-identity authority, history index, head
    pointer, chronology record, or discovery mechanism. Every referenced durable
    artifact must earn authority again through the existing public relinking
    boundaries when `reenter_chromium_research_session()` runs.
    """

    working_set_members: tuple[ChromiumResearchWorkingSetMemberReentryLocator, ...]
    working_set_source: Path
    prior_note_source: Path
    prior_revision_source: Path
    continuation_source: Path
    starting_predecessor_edge_sources: tuple[Path, ...]
    declared_edge_sources: tuple[Path, ...]
    declaration_source: Path


@dataclass(frozen=True, slots=True)
class ChromiumResearchSessionReentryResult:
    """Freshly reconstructed governed research session from one explicit locator plan."""

    plan: ChromiumResearchSessionReentryPlan
    loaded_members: tuple[ChromiumPageResearchWorkingSetItem, ...]
    loaded_continuation: ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord
    starting_predecessor: (
        ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord
        | ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord
    )
    loaded_declaration: ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceDeclarationRecord
    controller: ChromiumResearchSessionController


class ChromiumResearchSessionReentryError(ValueError):
    """Raised when one explicit durable re-entry step cannot be re-established."""


def create_chromium_research_session_reentry_plan(
    working_set_members: Iterable[ChromiumResearchWorkingSetMemberReentryLocator],
    *,
    working_set_source: Path,
    prior_note_source: Path,
    prior_revision_source: Path,
    continuation_source: Path,
    starting_predecessor_edge_sources: Iterable[Path] = (),
    declared_edge_sources: Iterable[Path],
    declaration_source: Path,
) -> ChromiumResearchSessionReentryPlan:
    """Snapshot caller-selected durable locations without reading or verifying them."""

    if isinstance(working_set_members, (str, bytes, Path)):
        raise TypeError("working_set_members must be an ordered iterable of member locators.")
    try:
        members = tuple(working_set_members)
    except TypeError as exc:
        raise TypeError(
            "working_set_members must be an ordered iterable of member locators."
        ) from exc
    if not members:
        raise ValueError("working_set_members must contain at least one explicit member locator.")
    for index, member in enumerate(members):
        _validate_member_locator(member, index=index)

    predecessor_sources = _snapshot_path_iterable(
        starting_predecessor_edge_sources,
        label="starting_predecessor_edge_sources",
        allow_empty=True,
    )
    declared_sources = _snapshot_path_iterable(
        declared_edge_sources,
        label="declared_edge_sources",
        allow_empty=False,
    )

    return ChromiumResearchSessionReentryPlan(
        working_set_members=members,
        working_set_source=_require_path(working_set_source, "working_set_source"),
        prior_note_source=_require_path(prior_note_source, "prior_note_source"),
        prior_revision_source=_require_path(prior_revision_source, "prior_revision_source"),
        continuation_source=_require_path(continuation_source, "continuation_source"),
        starting_predecessor_edge_sources=predecessor_sources,
        declared_edge_sources=declared_sources,
        declaration_source=_require_path(declaration_source, "declaration_source"),
    )


def reenter_chromium_research_session(
    plan: ChromiumResearchSessionReentryPlan,
) -> ChromiumResearchSessionReentryResult:
    """Freshly reconstruct one declared research session from explicit durable locations.

    The operation performs no directory scan, digest search, path inference,
    predecessor discovery, branch enumeration, automatic traversal, browser
    reacquisition, current/latest/head selection, or semantic interpretation.

    Each working-set member is reconstructed from explicitly supplied capture and
    note-sidecar paths through the existing 16C/17D/18D/19D loaders. The 23C base is
    then freshly reconstructed from the exact caller-ordered members plus explicit
    20B/21B/22B/23B locations. Any predecessor edges between that base and the
    declaration start are folded in the exact supplied order through public 24C.
    Finally, public 26C freshly reconciles the explicit declared-edge paths with the
    explicit durable declaration before a new 29A controller is constructed.
    """

    if not isinstance(plan, ChromiumResearchSessionReentryPlan):
        raise TypeError("plan must be ChromiumResearchSessionReentryPlan.")
    _validate_plan(plan)

    loaded_members: list[ChromiumPageResearchWorkingSetItem] = []
    for index, locator in enumerate(plan.working_set_members):
        try:
            loaded_members.append(_load_member(locator))
        except (OSError, TypeError, ValueError) as exc:
            raise ChromiumResearchSessionReentryError(
                f"Working-set member {index} could not be freshly relinked from the explicit locator plan."
            ) from exc

    members = tuple(loaded_members)
    try:
        loaded_continuation = load_chromium_research_working_set_note_revision_continuation(
            members,
            plan.working_set_source,
            plan.prior_note_source,
            plan.prior_revision_source,
            plan.continuation_source,
        )
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchSessionReentryError(
            "The explicit 20B/21B/22B/23B base could not be freshly relinked."
        ) from exc

    starting_predecessor: (
        ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord
        | ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord
    ) = loaded_continuation
    for index, edge_source in enumerate(plan.starting_predecessor_edge_sources):
        try:
            starting_predecessor = load_chromium_research_working_set_note_revision_edge(
                starting_predecessor,
                edge_source,
            )
        except (OSError, TypeError, ValueError) as exc:
            raise ChromiumResearchSessionReentryError(
                f"Starting-predecessor edge {index} could not be freshly relinked in the explicit supplied order."
            ) from exc

    try:
        loaded_declaration = (
            load_chromium_research_working_set_note_revision_edge_sequence_declaration(
                starting_predecessor,
                plan.declared_edge_sources,
                plan.declaration_source,
            )
        )
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchSessionReentryError(
            "The explicit declared segment could not be freshly reconciled with its declaration."
        ) from exc

    try:
        controller = ChromiumResearchSessionController(loaded_declaration)
    except (TypeError, ValueError) as exc:
        raise ChromiumResearchSessionReentryError(
            "Freshly relinked declaration could not become a governed research-session controller."
        ) from exc

    return ChromiumResearchSessionReentryResult(
        plan=plan,
        loaded_members=members,
        loaded_continuation=loaded_continuation,
        starting_predecessor=starting_predecessor,
        loaded_declaration=loaded_declaration,
        controller=controller,
    )


def _load_member(
    locator: ChromiumResearchWorkingSetMemberReentryLocator,
) -> ChromiumPageResearchWorkingSetItem:
    if isinstance(locator, ChromiumResearchParagraphNoteReentryLocator):
        source = load_chromium_page_research_capture(locator.capture_source)
        return load_chromium_research_paragraph_note(source, locator.note_source)

    if isinstance(locator, ChromiumResearchExactRangeNoteReentryLocator):
        source = load_chromium_page_research_capture(locator.capture_source)
        return load_chromium_research_paragraph_text_selection_note(
            source,
            locator.note_source,
        )

    if isinstance(locator, ChromiumResearchComparisonNoteReentryLocator):
        first_source = load_chromium_page_research_capture(locator.first_capture_source)
        second_source = load_chromium_page_research_capture(locator.second_capture_source)
        return load_chromium_research_paragraph_text_selection_comparison_note(
            first_source,
            second_source,
            locator.note_source,
        )

    raise TypeError("working-set re-entry locator uses an unsupported member type.")


def _validate_plan(plan: ChromiumResearchSessionReentryPlan) -> None:
    if not isinstance(plan.working_set_members, tuple) or not plan.working_set_members:
        raise TypeError("plan.working_set_members must be a non-empty tuple.")
    for index, member in enumerate(plan.working_set_members):
        _validate_member_locator(member, index=index)

    for name in (
        "working_set_source",
        "prior_note_source",
        "prior_revision_source",
        "continuation_source",
        "declaration_source",
    ):
        _require_path(getattr(plan, name), f"plan.{name}")

    if not isinstance(plan.starting_predecessor_edge_sources, tuple):
        raise TypeError("plan.starting_predecessor_edge_sources must be a tuple of Paths.")
    for index, source in enumerate(plan.starting_predecessor_edge_sources):
        _require_path(source, f"plan.starting_predecessor_edge_sources[{index}]")

    if not isinstance(plan.declared_edge_sources, tuple) or not plan.declared_edge_sources:
        raise TypeError("plan.declared_edge_sources must be a non-empty tuple of Paths.")
    for index, source in enumerate(plan.declared_edge_sources):
        _require_path(source, f"plan.declared_edge_sources[{index}]")


def _validate_member_locator(
    locator: ChromiumResearchWorkingSetMemberReentryLocator,
    *,
    index: int,
) -> None:
    if isinstance(locator, ChromiumResearchParagraphNoteReentryLocator):
        _require_path(locator.capture_source, f"working_set_members[{index}].capture_source")
        _require_path(locator.note_source, f"working_set_members[{index}].note_source")
        return
    if isinstance(locator, ChromiumResearchExactRangeNoteReentryLocator):
        _require_path(locator.capture_source, f"working_set_members[{index}].capture_source")
        _require_path(locator.note_source, f"working_set_members[{index}].note_source")
        return
    if isinstance(locator, ChromiumResearchComparisonNoteReentryLocator):
        _require_path(
            locator.first_capture_source,
            f"working_set_members[{index}].first_capture_source",
        )
        _require_path(
            locator.second_capture_source,
            f"working_set_members[{index}].second_capture_source",
        )
        _require_path(locator.note_source, f"working_set_members[{index}].note_source")
        return
    raise TypeError(
        f"working_set_members[{index}] must be a supported explicit re-entry locator."
    )


def _snapshot_path_iterable(
    values: Iterable[Path],
    *,
    label: str,
    allow_empty: bool,
) -> tuple[Path, ...]:
    if isinstance(values, (str, bytes, Path)):
        raise TypeError(f"{label} must be an ordered iterable of Paths, not one path.")
    try:
        frozen = tuple(values)
    except TypeError as exc:
        raise TypeError(f"{label} must be an ordered iterable of Paths.") from exc
    if not allow_empty and not frozen:
        raise ValueError(f"{label} must contain at least one explicit edge path.")
    return tuple(_require_path(value, f"{label}[{index}]") for index, value in enumerate(frozen))


def _require_path(value: Path, label: str) -> Path:
    if not isinstance(value, Path):
        raise TypeError(f"{label} must be pathlib.Path.")
    return value
