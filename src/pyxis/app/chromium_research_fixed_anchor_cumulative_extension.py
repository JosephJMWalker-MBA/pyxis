from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Generic, TypeVar

from .chromium_research_session_rollover import ChromiumResearchSessionRolloverResult
from .chromium_research_working_set_note_revision_edge_sequence_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceRecord,
    load_chromium_research_working_set_note_revision_edge_sequence,
)
from .chromium_research_working_set_note_revision_edge_sequence_persistence import (
    ChromiumPageResearchWorkingSetNoteRevisionEdgeSequencePersistenceEvidence,
    persist_chromium_research_working_set_note_revision_edge_sequence,
)


PlanT = TypeVar("PlanT")
ReentryT = TypeVar("ReentryT")
OverlayT = TypeVar("OverlayT")


@dataclass(frozen=True, slots=True)
class _FixedAnchorCumulativeExtensionMessages:
    """Concrete-family wording for one shared cumulative-extension procedure."""

    current_decode: str
    current_reentry: str
    sequence_relink: str
    terminal_identity: str
    terminal_text: str
    next_reentry: str
    overlay_decode: str
    overlay_round_trip: str


@dataclass(frozen=True, slots=True)
class _FixedAnchorCumulativeExtensionAdapter(Generic[PlanT, ReentryT, OverlayT]):
    """Concrete operations required by the fixed-anchor mechanical kernel.

    This adapter deliberately says nothing about evidence-basis epochs or root count.
    Concrete callers remain responsible for ancestry semantics and durable formats.
    """

    error_type: type[ValueError]
    messages: _FixedAnchorCumulativeExtensionMessages
    load_plan: Callable[[Path], PlanT]
    reenter: Callable[[PlanT], ReentryT]
    require_loaded_plan_match: Callable[[PlanT, ReentryT], None] | None
    require_current_match: Callable[[ReentryT, ReentryT], None]
    require_rollover_prior_match: Callable[
        [ReentryT, ChromiumResearchSessionRolloverResult], None
    ]
    declared_edge_sources: Callable[[PlanT], tuple[Path, ...]]
    anchor_endpoint: Callable[[ReentryT], Any]
    build_next_plan: Callable[
        [PlanT, tuple[Path, ...], Path],
        PlanT,
    ]
    require_next_match: Callable[
        [ChromiumResearchSessionRolloverResult, ReentryT], None
    ]
    persist_overlay: Callable[[PlanT, Path], OverlayT]
    overlay_path: Callable[[OverlayT], Path]


@dataclass(frozen=True, slots=True)
class _FixedAnchorCumulativeExtensionKernelResult(Generic[PlanT, ReentryT, OverlayT]):
    """Mechanical outputs before a concrete public result wrapper is constructed."""

    current_plan: PlanT
    explicit_sequence: ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceRecord
    declaration: ChromiumPageResearchWorkingSetNoteRevisionEdgeSequencePersistenceEvidence
    next_plan: PlanT
    fresh_reentry: ReentryT
    overlay: OverlayT


def _extend_fixed_anchor_cumulative_continuation(
    current_reentry: ReentryT,
    rollover: ChromiumResearchSessionRolloverResult,
    *,
    current_overlay_source: Path,
    successor_edge_source: Path,
    cumulative_declaration_destination: Path,
    next_overlay_destination: Path,
    adapter: _FixedAnchorCumulativeExtensionAdapter[PlanT, ReentryT, OverlayT],
) -> _FixedAnchorCumulativeExtensionKernelResult[PlanT, ReentryT, OverlayT]:
    """Execute the procedure shared by 35E, 37D, and 40D.

    Authority remains concrete. The kernel validates only shared operational mechanics:
    explicit paths, no-overwrite destinations, cumulative edge relinking, terminal
    SHA/text equivalence, cumulative declaration persistence, next-plan fresh re-entry,
    and exact overlay round-trip. Concrete callbacks retain all ancestry semantics.
    """

    for value, label in (
        (current_overlay_source, "current_overlay_source"),
        (successor_edge_source, "successor_edge_source"),
        (cumulative_declaration_destination, "cumulative_declaration_destination"),
        (next_overlay_destination, "next_overlay_destination"),
    ):
        if not isinstance(value, Path):
            raise TypeError(f"{label} must be pathlib.Path.")

    overlay_source = current_overlay_source.resolve()
    successor_source = successor_edge_source.resolve()
    declaration_destination = cumulative_declaration_destination.resolve()
    overlay_destination = next_overlay_destination.resolve()

    if declaration_destination == overlay_destination:
        raise ValueError(
            "cumulative declaration and next overlay destinations must be distinct."
        )
    if declaration_destination.exists():
        raise FileExistsError("cumulative_declaration_destination already exists.")
    if overlay_destination.exists():
        raise FileExistsError("next_overlay_destination already exists.")

    try:
        current_plan = adapter.load_plan(overlay_source)
    except (OSError, TypeError, ValueError) as exc:
        raise adapter.error_type(adapter.messages.current_decode) from exc

    if adapter.require_loaded_plan_match is not None:
        adapter.require_loaded_plan_match(current_plan, current_reentry)

    try:
        fresh_current = adapter.reenter(current_plan)
    except (OSError, TypeError, ValueError) as exc:
        raise adapter.error_type(adapter.messages.current_reentry) from exc

    adapter.require_current_match(current_reentry, fresh_current)
    adapter.require_rollover_prior_match(current_reentry, rollover)

    cumulative_sources = (
        *adapter.declared_edge_sources(current_plan),
        successor_source,
    )
    try:
        explicit_sequence = load_chromium_research_working_set_note_revision_edge_sequence(
            adapter.anchor_endpoint(fresh_current),
            cumulative_sources,
        )
    except (OSError, TypeError, ValueError) as exc:
        raise adapter.error_type(adapter.messages.sequence_relink) from exc

    successor = explicit_sequence.edges[-1]
    chosen = rollover.prior_revision
    if successor.verification.edge_record_sha256 != chosen.persistence.edge_record_sha256:
        raise adapter.error_type(adapter.messages.terminal_identity)
    if (
        successor.revision.revised_note.note_text
        != chosen.extension.revision.revised_note.note_text
    ):
        raise adapter.error_type(adapter.messages.terminal_text)

    declaration = persist_chromium_research_working_set_note_revision_edge_sequence(
        explicit_sequence,
        declaration_destination,
    )
    next_plan = adapter.build_next_plan(
        current_plan,
        tuple(cumulative_sources),
        declaration.path,
    )

    try:
        fresh_next = adapter.reenter(next_plan)
    except (OSError, TypeError, ValueError) as exc:
        raise adapter.error_type(adapter.messages.next_reentry) from exc
    adapter.require_next_match(rollover, fresh_next)

    overlay = adapter.persist_overlay(next_plan, overlay_destination)
    try:
        decoded = adapter.load_plan(adapter.overlay_path(overlay))
    except (OSError, TypeError, ValueError) as exc:
        raise adapter.error_type(adapter.messages.overlay_decode) from exc
    if decoded != next_plan:
        raise adapter.error_type(adapter.messages.overlay_round_trip)

    return _FixedAnchorCumulativeExtensionKernelResult(
        current_plan=current_plan,
        explicit_sequence=explicit_sequence,
        declaration=declaration,
        next_plan=next_plan,
        fresh_reentry=fresh_next,
        overlay=overlay,
    )


__all__: list[str] = []
