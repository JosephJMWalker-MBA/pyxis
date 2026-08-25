from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Input, Static

from pyxis.app.chromium_research_root_backed_session_continuation_checkpoint_extension import (
    ChromiumResearchRootBackedSessionContinuationCheckpointExtensionResult,
)
from pyxis.app.chromium_research_root_backed_session_continuation_reentry_plan_document import (
    ChromiumResearchRootBackedSessionContinuationReentryResult,
)
from pyxis.app.chromium_research_session_rollover import ChromiumResearchSessionRolloverResult


CUMULATIVE_CHECKPOINT_AUTHORITY_NOTICE = (
    "Checkpoint this explicitly chosen next continuation through the 35E cumulative "
    "post-root boundary. Re-enter the current 35D/35E overlay and chosen successor "
    "locations explicitly, plus two distinct no-overwrite destinations. Prior paths "
    "are not reused as current-location authority. The resulting declaration and "
    "overlay are operational lineage configuration, not latest/current/head authority."
)


def _candidate_receipt(
    current: ChromiumResearchRootBackedSessionContinuationReentryResult,
    rollover: ChromiumResearchSessionRolloverResult,
) -> str:
    return (
        "Mounted one-hop continuation is not yet checkpointed into the cumulative post-root lineage.\n"
        f"Current cumulative edge count: {len(current.plan.declared_edge_sources)}\n"
        f"Chosen successor SHA-256: {rollover.prior_revision.persistence.edge_record_sha256}\n"
        "Further endpoint revision remains locked. Supply explicit current locations and new destinations below."
    )


def cumulative_checkpoint_success_receipt(
    result: ChromiumResearchRootBackedSessionContinuationCheckpointExtensionResult,
) -> str:
    """Format one receipt for a freshly proven 35E cumulative checkpoint."""

    endpoint = result.fresh_reentry.controller.declared_endpoint
    return (
        "Success — cumulative post-root continuation freshly proven and checkpointed.\n"
        f"Cumulative declaration: {result.declaration.path}\n"
        f"Next 35D/35E overlay: {result.overlay.path}\n"
        f"Declared post-root edge count: {len(result.next_plan.declared_edge_sources)}\n"
        f"Terminal edge SHA-256: {endpoint.verification.edge_record_sha256}\n"
        "The shell now displays the exact freshly proven cumulative continuation and "
        "may author one next explicit successor. This is not a global latest/current/head claim."
    )


class RootBackedResearchSessionCumulativeCheckpointControls(Vertical):
    """Blank explicit inputs for one governed 35E cumulative continuation checkpoint."""

    def __init__(
        self,
        current_reentry: ChromiumResearchRootBackedSessionContinuationReentryResult,
        rollover: ChromiumResearchSessionRolloverResult,
    ) -> None:
        if not isinstance(
            current_reentry,
            ChromiumResearchRootBackedSessionContinuationReentryResult,
        ):
            raise TypeError(
                "current_reentry must be ChromiumResearchRootBackedSessionContinuationReentryResult."
            )
        if not isinstance(rollover, ChromiumResearchSessionRolloverResult):
            raise TypeError("rollover must be ChromiumResearchSessionRolloverResult.")
        super().__init__(id="research-root-backed-cumulative-checkpoint-controls")
        self.current_reentry = current_reentry
        self.rollover = rollover
        self.persistence_result: (
            ChromiumResearchRootBackedSessionContinuationCheckpointExtensionResult | None
        ) = None

    def compose(self) -> ComposeResult:
        yield Static(
            "Checkpoint cumulative post-root continuation",
            id="research-root-backed-cumulative-checkpoint-title",
        )
        yield Static(
            CUMULATIVE_CHECKPOINT_AUTHORITY_NOTICE,
            id="research-root-backed-cumulative-checkpoint-authority-notice",
            markup=False,
        )
        yield Static(
            _candidate_receipt(self.current_reentry, self.rollover),
            id="research-root-backed-cumulative-checkpoint-candidate",
            markup=False,
        )
        yield Static(
            "Current durable file for the exact current 35D/35E continuation overlay",
            id="research-root-backed-cumulative-checkpoint-current-overlay-source-label",
        )
        yield Input(
            placeholder="Explicit current 35D/35E overlay path",
            id="research-root-backed-cumulative-checkpoint-current-overlay-source",
        )
        yield Static(
            "Current durable file for the exact chosen successor",
            id="research-root-backed-cumulative-checkpoint-successor-source-label",
        )
        yield Input(
            placeholder="Explicit current chosen successor edge path",
            id="research-root-backed-cumulative-checkpoint-successor-source",
        )
        yield Static(
            "No-overwrite destination for the new cumulative post-root declaration",
            id="research-root-backed-cumulative-checkpoint-declaration-destination-label",
        )
        yield Input(
            placeholder="Explicit cumulative declaration destination",
            id="research-root-backed-cumulative-checkpoint-declaration-destination",
        )
        yield Static(
            "No-overwrite destination for the next 35D/35E continuation overlay",
            id="research-root-backed-cumulative-checkpoint-overlay-destination-label",
        )
        yield Input(
            placeholder="Explicit next continuation overlay destination",
            id="research-root-backed-cumulative-checkpoint-overlay-destination",
        )
        yield Button(
            "Save proven cumulative continuation checkpoint",
            id="save-research-root-backed-cumulative-checkpoint",
            variant="warning",
        )
        yield Static(
            "Further revision remains locked until a fresh cumulative checkpoint succeeds.",
            id="research-root-backed-cumulative-checkpoint-status",
            markup=False,
        )

    def lock_after_success(
        self,
        result: ChromiumResearchRootBackedSessionContinuationCheckpointExtensionResult,
    ) -> None:
        """Lock the old one-hop checkpoint form before its surface is promoted away."""

        if not isinstance(
            result,
            ChromiumResearchRootBackedSessionContinuationCheckpointExtensionResult,
        ):
            raise TypeError(
                "result must be ChromiumResearchRootBackedSessionContinuationCheckpointExtensionResult."
            )
        if result.current_reentry is not self.current_reentry:
            raise ValueError(
                "Cumulative checkpoint result does not retain this form's exact current re-entry lineage."
            )
        if result.rollover is not self.rollover:
            raise ValueError(
                "Cumulative checkpoint result does not retain this form's exact rollover."
            )

        self.persistence_result = result
        for selector in (
            "#research-root-backed-cumulative-checkpoint-current-overlay-source",
            "#research-root-backed-cumulative-checkpoint-successor-source",
            "#research-root-backed-cumulative-checkpoint-declaration-destination",
            "#research-root-backed-cumulative-checkpoint-overlay-destination",
        ):
            self.query_one(selector, Input).disabled = True
        self.query_one(
            "#save-research-root-backed-cumulative-checkpoint",
            Button,
        ).disabled = True
        self.query_one(
            "#research-root-backed-cumulative-checkpoint-status",
            Static,
        ).update(cumulative_checkpoint_success_receipt(result))


__all__ = [
    "CUMULATIVE_CHECKPOINT_AUTHORITY_NOTICE",
    "RootBackedResearchSessionCumulativeCheckpointControls",
    "cumulative_checkpoint_success_receipt",
]
