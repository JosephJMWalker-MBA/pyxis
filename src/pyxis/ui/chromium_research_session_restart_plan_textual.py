from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Input, Static

from pyxis.app.chromium_research_session_continuation_reentry_plan import (
    ChromiumResearchSessionContinuationReentryPlanResult,
)
from pyxis.app.chromium_research_session_rollover import (
    ChromiumResearchSessionRolloverResult,
)


RESTART_PLAN_AUTHORITY_NOTICE = (
    "Save a restart locator plan for this explicitly chosen continuation before "
    "authoring another successor. The plan records current caller-supplied locations "
    "and order only; it is not research evidence, a history index, or a latest/current/head pointer."
)


def _candidate_receipt(result: ChromiumResearchSessionRolloverResult) -> str:
    return (
        "Mounted continuation is not yet proven restartable through a saved locator plan.\n"
        f"Chosen successor SHA-256: {result.prior_revision.persistence.edge_record_sha256}\n"
        f"Continuation declaration SHA-256: {result.declaration.sequence_record_sha256}\n"
        "Re-enter the successor and declaration locations explicitly; prior UI paths are not reused as authority."
    )


def restart_plan_success_receipt(
    result: ChromiumResearchSessionContinuationReentryPlanResult,
) -> str:
    """Format one UI receipt for a freshly proven continuation restart plan."""

    return (
        "Success — continuation restart plan freshly proven and written.\n"
        f"Restart plan: {result.persistence.path}\n"
        f"Declared endpoint SHA-256: "
        f"{result.fresh_reentry.controller.declared_endpoint.verification.edge_record_sha256}\n"
        "Further revision is unlocked for this mounted continuation. The saved plan is "
        "operational restart configuration only; it is not a global latest/current/head claim."
    )


class ResearchSessionRestartPlanControls(Vertical):
    """Explicit UI inputs for one governed 32A continuation restart-plan save."""

    def __init__(self, rollover: ChromiumResearchSessionRolloverResult) -> None:
        if not isinstance(rollover, ChromiumResearchSessionRolloverResult):
            raise TypeError("rollover must be ChromiumResearchSessionRolloverResult.")
        super().__init__(id="research-session-restart-plan-controls")
        self.rollover = rollover
        self.persistence_result: ChromiumResearchSessionContinuationReentryPlanResult | None = None

    def compose(self) -> ComposeResult:
        yield Static(
            "Save restart plan for mounted continuation",
            id="research-session-restart-plan-title",
        )
        yield Static(
            RESTART_PLAN_AUTHORITY_NOTICE,
            id="research-session-restart-plan-authority-notice",
            markup=False,
        )
        yield Static(
            _candidate_receipt(self.rollover),
            id="research-session-restart-plan-candidate",
            markup=False,
        )
        yield Static(
            "Current durable file for the exact chosen successor",
            id="research-session-restart-plan-successor-source-label",
        )
        yield Input(
            placeholder="Explicit current successor edge path",
            id="research-session-restart-plan-successor-source",
        )
        yield Static(
            "Current durable file for the exact continuation declaration",
            id="research-session-restart-plan-declaration-source-label",
        )
        yield Input(
            placeholder="Explicit current continuation declaration path",
            id="research-session-restart-plan-declaration-source",
        )
        yield Static(
            "No-overwrite destination for the proven restart locator plan",
            id="research-session-restart-plan-destination-label",
        )
        yield Input(
            placeholder="Explicit restart plan destination path",
            id="research-session-restart-plan-destination",
        )
        yield Button(
            "Save proven restart plan — then allow further revision",
            id="save-research-session-restart-plan",
            variant="warning",
        )
        yield Static(
            "Further revision remains locked until this continuation has a proven restart plan.",
            id="research-session-restart-plan-status",
            markup=False,
        )

    def lock_after_success(
        self,
        result: ChromiumResearchSessionContinuationReentryPlanResult,
    ) -> None:
        """Lock this checkpoint after one successful no-overwrite restart-plan save."""

        if not isinstance(result, ChromiumResearchSessionContinuationReentryPlanResult):
            raise TypeError(
                "result must be ChromiumResearchSessionContinuationReentryPlanResult."
            )
        if result.rollover is not self.rollover:
            raise ValueError("Restart-plan result does not belong to this exact rollover checkpoint.")

        self.persistence_result = result
        self.query_one("#research-session-restart-plan-successor-source", Input).disabled = True
        self.query_one("#research-session-restart-plan-declaration-source", Input).disabled = True
        self.query_one("#research-session-restart-plan-destination", Input).disabled = True
        self.query_one("#save-research-session-restart-plan", Button).disabled = True
        self.query_one("#research-session-restart-plan-status", Static).update(
            restart_plan_success_receipt(result)
        )
