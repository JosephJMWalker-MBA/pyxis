from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from textual.widget import Widget
from textual.widgets import Static

from pyxis.app.chromium_research_session_rollover import ChromiumResearchSessionRolloverResult

from .chromium_research_endpoint_revision_textual import ResearchEndpointRevisionControls
from .chromium_research_session_restart_plan_textual import ResearchSessionRestartPlanControls
from .chromium_research_session_rollover_textual import ResearchSessionRolloverControls
from .research_session_shell import ResearchSessionShell


@dataclass(frozen=True, slots=True)
class _CumulativeCheckpointRolloverMountSpec:
    """Concrete surface details for one already-mounted cumulative rollover."""

    stale_success_receipt_selector: str
    retained_rollover_error: str
    restart_plan_error: str


async def _mount_cumulative_checkpoint_after_rollover(
    shell: ResearchSessionShell,
    *,
    current_reentry: Any,
    rollover: ChromiumResearchSessionRolloverResult,
    spec: _CumulativeCheckpointRolloverMountSpec,
    create_checkpoint_controls: Callable[[Any, ChromiumResearchSessionRolloverResult], Widget],
) -> None:
    """Replace the base one-hop controls with one concrete cumulative checkpoint form.

    The concrete subclass must call `ResearchSessionShell._mount_research_rollover`
    before entering this private procedure. The helper therefore owns only the
    now-triply-proven post-rollover Textual mechanics. It knows no root count,
    evidence-basis epoch, milestone, durable path, persistence format, fixed anchor,
    ancestry relation, or checkpoint proof semantics.
    """

    if shell.last_research_rollover is not rollover:
        raise ValueError(spec.retained_rollover_error)

    if len(shell.query(spec.stale_success_receipt_selector)):
        await shell.query_one(spec.stale_success_receipt_selector, Static).remove()

    if len(shell.query(ResearchSessionRestartPlanControls)):
        raise ValueError(spec.restart_plan_error)

    unlocked_revision = shell.query_one(
        "#research-endpoint-revision-controls",
        ResearchEndpointRevisionControls,
    )
    empty_rollover = shell.query_one(
        "#research-session-rollover-controls",
        ResearchSessionRolloverControls,
    )
    await unlocked_revision.remove()
    await empty_rollover.remove()

    await shell.mount(
        ResearchEndpointRevisionControls(restart_checkpoint_required=True)
    )
    await shell.mount(ResearchSessionRolloverControls())
    await shell.mount(create_checkpoint_controls(current_reentry, rollover))


__all__: list[str] = []
