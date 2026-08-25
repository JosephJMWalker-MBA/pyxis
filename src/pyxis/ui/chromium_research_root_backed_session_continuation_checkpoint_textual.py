from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Input, Static

from pyxis.app.chromium_research_root_backed_session_continuation_reentry_plan_document import (
    ChromiumResearchRootBackedSessionContinuationCheckpointResult,
)
from pyxis.app.chromium_research_session_rollover import ChromiumResearchSessionRolloverResult


ROOT_BACKED_CHECKPOINT_AUTHORITY_NOTICE = (
    "Checkpoint this explicitly chosen first continuation through the root-backed 35D "
    "boundary. Re-enter all current durable locations explicitly; launch-time and "
    "rollover paths are not reused as authority. The resulting overlay is operational "
    "restart configuration only, not evidence or a latest/current/head pointer."
)


def _candidate_receipt(result: ChromiumResearchSessionRolloverResult) -> str:
    return (
        "Mounted root-backed continuation is not yet checkpointed through a 35D overlay.\n"
        f"Chosen successor SHA-256: {result.prior_revision.persistence.edge_record_sha256}\n"
        f"One-hop continuation declaration SHA-256: {result.declaration.sequence_record_sha256}\n"
        "Further endpoint revision remains locked. Supply explicit current locations below."
    )


def root_backed_checkpoint_success_receipt(
    result: ChromiumResearchRootBackedSessionContinuationCheckpointResult,
) -> str:
    """Format one receipt for a freshly proven first root-backed continuation checkpoint."""

    return (
        "Success — first root-backed continuation freshly proven and checkpointed.\n"
        f"35D continuation overlay: {result.persistence.path}\n"
        f"Declared endpoint SHA-256: "
        f"{result.fresh_reentry.controller.declared_endpoint.verification.edge_record_sha256}\n"
        f"Retained root SHA-256: "
        f"{result.fresh_reentry.prior_root_backed_reentry.loaded_root.verification.root_record_sha256}\n"
        "Further revision remains locked in this 36B shell. Relaunch explicitly with "
        "`pyxis research-shell --root-backed-continuation-overlay <saved-overlay>` "
        "before continuing. This checkpoint is not a global latest/current/head claim."
    )


class RootBackedResearchSessionContinuationCheckpointControls(Vertical):
    """Blank explicit inputs for one governed 35D first-continuation checkpoint."""

    def __init__(self, rollover: ChromiumResearchSessionRolloverResult) -> None:
        if not isinstance(rollover, ChromiumResearchSessionRolloverResult):
            raise TypeError("rollover must be ChromiumResearchSessionRolloverResult.")
        super().__init__(id="research-root-backed-continuation-checkpoint-controls")
        self.rollover = rollover
        self.persistence_result: (
            ChromiumResearchRootBackedSessionContinuationCheckpointResult | None
        ) = None

    def compose(self) -> ComposeResult:
        yield Static(
            "Checkpoint first continuation from persisted root-backed ancestry",
            id="research-root-backed-checkpoint-title",
        )
        yield Static(
            ROOT_BACKED_CHECKPOINT_AUTHORITY_NOTICE,
            id="research-root-backed-checkpoint-authority-notice",
            markup=False,
        )
        yield Static(
            _candidate_receipt(self.rollover),
            id="research-root-backed-checkpoint-candidate",
            markup=False,
        )
        yield Static(
            "Current durable file for the exact prior 35C root-backed overlay",
            id="research-root-backed-checkpoint-prior-overlay-source-label",
        )
        yield Input(
            placeholder="Explicit current 35C overlay path",
            id="research-root-backed-checkpoint-prior-overlay-source",
        )
        yield Static(
            "Current durable file for the exact chosen successor",
            id="research-root-backed-checkpoint-successor-source-label",
        )
        yield Input(
            placeholder="Explicit current successor edge path",
            id="research-root-backed-checkpoint-successor-source",
        )
        yield Static(
            "Current durable file for the exact one-hop continuation declaration",
            id="research-root-backed-checkpoint-declaration-source-label",
        )
        yield Input(
            placeholder="Explicit current continuation declaration path",
            id="research-root-backed-checkpoint-declaration-source",
        )
        yield Static(
            "No-overwrite destination for the proven 35D continuation overlay",
            id="research-root-backed-checkpoint-destination-label",
        )
        yield Input(
            placeholder="Explicit 35D continuation overlay destination",
            id="research-root-backed-checkpoint-destination",
        )
        yield Button(
            "Save proven 35D continuation checkpoint",
            id="save-research-root-backed-continuation-checkpoint",
            variant="warning",
        )
        yield Static(
            "Further revision remains locked until this checkpoint succeeds; 36B also "
            "keeps revision locked after success until an explicit continuation-overlay relaunch.",
            id="research-root-backed-checkpoint-status",
            markup=False,
        )

    def lock_after_success(
        self,
        result: ChromiumResearchRootBackedSessionContinuationCheckpointResult,
    ) -> None:
        """Lock this form after one successful no-overwrite 35D checkpoint."""

        if not isinstance(
            result,
            ChromiumResearchRootBackedSessionContinuationCheckpointResult,
        ):
            raise TypeError(
                "result must be ChromiumResearchRootBackedSessionContinuationCheckpointResult."
            )
        if result.rollover is not self.rollover:
            raise ValueError(
                "Root-backed checkpoint result does not belong to this exact rollover."
            )

        self.persistence_result = result
        for selector in (
            "#research-root-backed-checkpoint-prior-overlay-source",
            "#research-root-backed-checkpoint-successor-source",
            "#research-root-backed-checkpoint-declaration-source",
            "#research-root-backed-checkpoint-destination",
        ):
            self.query_one(selector, Input).disabled = True
        self.query_one(
            "#save-research-root-backed-continuation-checkpoint",
            Button,
        ).disabled = True
        self.query_one("#research-root-backed-checkpoint-status", Static).update(
            root_backed_checkpoint_success_receipt(result)
        )


__all__ = [
    "ROOT_BACKED_CHECKPOINT_AUTHORITY_NOTICE",
    "RootBackedResearchSessionContinuationCheckpointControls",
    "root_backed_checkpoint_success_receipt",
]
