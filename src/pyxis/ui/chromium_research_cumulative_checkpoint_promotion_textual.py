from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from textual.widget import Widget
from textual.widgets import Static

from pyxis.app.chromium_research_session_presentation import present_chromium_research_session

from .chromium_research_endpoint_revision_textual import ResearchEndpointRevisionControls
from .chromium_research_revision_edge_sequence_textual import (
    ResearchRevisionEdgeSequenceDetail,
    _require_research_sequence_presentation,
    _snapshot_working_set_contexts,
)
from .chromium_research_session_rollover_textual import ResearchSessionRolloverControls
from .research_session_shell import ResearchSessionShell


@dataclass(frozen=True, slots=True)
class _CumulativeCheckpointPromotionSpec:
    """Concrete surface details for one already-proven cumulative promotion."""

    checkpoint_controls_selector: str
    checkpoint_controls_type: type[Widget]
    success_receipt_id: str
    presentation_error: str
    context_cardinality_error: str


async def _promote_cumulative_checkpoint_surface(
    shell: ResearchSessionShell,
    *,
    fresh_reentry: Any,
    checkpoint_result: Any,
    spec: _CumulativeCheckpointPromotionSpec,
    success_receipt: Callable[[Any], str],
    advance_current_reentry: Callable[[Any], None],
    record_checkpoint: Callable[[Any], None],
) -> None:
    """Promote one already-proven cumulative controller onto the live Textual surface.

    This private procedure begins only after a concrete family has completed its own
    persistence, exact-current/rollover checks, fixed-anchor or ancestry proof, and
    old-form locking. It knows no root count, epoch, milestone, persistence format,
    anchor field, or checkpoint proof semantics.
    """

    fresh_controller = fresh_reentry.controller
    rebuilt_session = present_chromium_research_session(fresh_controller.loaded)
    if rebuilt_session != fresh_controller.presentation:
        raise ValueError(spec.presentation_error)

    new_session = fresh_controller.presentation
    _require_research_sequence_presentation(new_session.sequence)
    new_contexts = _snapshot_working_set_contexts(
        new_session.sequence,
        new_session.working_set_contexts,
    )
    if len(new_contexts) != len(new_session.sequence.members):
        raise ValueError(spec.context_cardinality_error)

    old_detail = shell.query_one(
        "#research-revision-edge-sequence",
        ResearchRevisionEdgeSequenceDetail,
    )
    old_revision = shell.query_one(
        "#research-endpoint-revision-controls",
        ResearchEndpointRevisionControls,
    )
    old_rollover = shell.query_one(
        "#research-session-rollover-controls",
        ResearchSessionRolloverControls,
    )
    old_checkpoint = shell.query_one(
        spec.checkpoint_controls_selector,
        spec.checkpoint_controls_type,
    )

    if len(shell.query("#research-rollover-success-receipt")):
        await shell.query_one("#research-rollover-success-receipt", Static).remove()
    await old_detail.remove()
    await old_revision.remove()
    await old_rollover.remove()
    await old_checkpoint.remove()

    advance_current_reentry(fresh_reentry)
    shell.research_controller = fresh_controller
    shell.research_session = new_session
    shell.research_presentation = new_session.sequence
    shell.research_working_set_contexts = new_contexts
    shell.last_research_rollover = None
    shell.last_research_restart_plan = None
    record_checkpoint(checkpoint_result)

    await shell.mount(
        Static(
            success_receipt(checkpoint_result),
            id=spec.success_receipt_id,
            markup=False,
        )
    )
    await shell.mount(
        ResearchRevisionEdgeSequenceDetail(
            new_session.sequence,
            working_set_contexts=new_contexts,
        )
    )
    await shell.mount(ResearchEndpointRevisionControls())
    await shell.mount(ResearchSessionRolloverControls())


__all__: list[str] = []
