from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Input, Static

from pyxis.app.chromium_research_second_basis_epoch_continuation_checkpoint_extension import (
    ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionResult,
)
from pyxis.app.chromium_research_second_basis_epoch_continuation_reentry_plan_document import (
    ChromiumResearchSecondBasisEpochContinuationReentryResult,
)
from pyxis.app.chromium_research_session_rollover import ChromiumResearchSessionRolloverResult


SECOND_BASIS_EPOCH_CUMULATIVE_CHECKPOINT_AUTHORITY_NOTICE = (
    "Checkpoint this explicitly chosen next continuation through the cumulative 37D "
    "post-second-root boundary. Re-enter the current 37C/37D overlay and chosen "
    "successor locations explicitly, plus two distinct no-overwrite destinations. "
    "Launch-time and prior-checkpoint paths are not reused as current-location "
    "authority. The resulting declaration and overlay are operational restart "
    "configuration, not latest/current/head authority."
)


def _candidate_receipt(
    current: ChromiumResearchSecondBasisEpochContinuationReentryResult,
    rollover: ChromiumResearchSessionRolloverResult,
) -> str:
    return (
        "Mounted one-hop continuation is not yet checkpointed into the cumulative "
        "post-second-root lineage.\n"
        f"Current cumulative edge count: {len(current.plan.declared_edge_sources)}\n"
        f"Chosen successor SHA-256: {rollover.prior_revision.persistence.edge_record_sha256}\n"
        "Further endpoint revision remains locked. Supply explicit current locations "
        "and new destinations below."
    )


def second_basis_epoch_cumulative_checkpoint_success_receipt(
    result: ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionResult,
) -> str:
    """Format one receipt for a freshly proven cumulative 37D checkpoint."""

    endpoint = result.fresh_reentry.controller.declared_endpoint
    return (
        "Success — cumulative post-second-root continuation freshly proven and checkpointed.\n"
        f"Cumulative declaration: {result.declaration.path}\n"
        f"Next 37C/37D overlay: {result.overlay.path}\n"
        f"Declared post-second-root edge count: {len(result.next_plan.declared_edge_sources)}\n"
        f"Terminal edge SHA-256: {endpoint.verification.edge_record_sha256}\n"
        "The shell now displays the exact freshly proven cumulative continuation and "
        "may author one next explicit successor. This is not a global "
        "latest/current/head claim."
    )


class SecondBasisEpochResearchSessionCumulativeCheckpointControls(Vertical):
    """Blank explicit inputs for one governed cumulative 37D checkpoint."""

    def __init__(
        self,
        current_reentry: ChromiumResearchSecondBasisEpochContinuationReentryResult,
        rollover: ChromiumResearchSessionRolloverResult,
    ) -> None:
        if not isinstance(
            current_reentry,
            ChromiumResearchSecondBasisEpochContinuationReentryResult,
        ):
            raise TypeError(
                "current_reentry must be ChromiumResearchSecondBasisEpochContinuationReentryResult."
            )
        if not isinstance(rollover, ChromiumResearchSessionRolloverResult):
            raise TypeError("rollover must be ChromiumResearchSessionRolloverResult.")
        super().__init__(id="research-second-basis-epoch-cumulative-checkpoint-controls")
        self.current_reentry = current_reentry
        self.rollover = rollover
        self.persistence_result: (
            ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionResult | None
        ) = None

    def compose(self) -> ComposeResult:
        yield Static(
            "Checkpoint cumulative post-second-root continuation",
            id="research-second-basis-epoch-cumulative-checkpoint-title",
        )
        yield Static(
            SECOND_BASIS_EPOCH_CUMULATIVE_CHECKPOINT_AUTHORITY_NOTICE,
            id="research-second-basis-epoch-cumulative-checkpoint-authority-notice",
            markup=False,
        )
        yield Static(
            _candidate_receipt(self.current_reentry, self.rollover),
            id="research-second-basis-epoch-cumulative-checkpoint-candidate",
            markup=False,
        )
        yield Static(
            "Current durable file for the exact current 37C/37D continuation overlay",
            id="research-second-basis-epoch-cumulative-checkpoint-current-overlay-source-label",
        )
        yield Input(
            placeholder="Explicit current 37C/37D overlay path",
            id="research-second-basis-epoch-cumulative-checkpoint-current-overlay-source",
        )
        yield Static(
            "Current durable file for the exact chosen successor",
            id="research-second-basis-epoch-cumulative-checkpoint-successor-source-label",
        )
        yield Input(
            placeholder="Explicit current chosen successor edge path",
            id="research-second-basis-epoch-cumulative-checkpoint-successor-source",
        )
        yield Static(
            "No-overwrite destination for the new cumulative post-second-root declaration",
            id="research-second-basis-epoch-cumulative-checkpoint-declaration-destination-label",
        )
        yield Input(
            placeholder="Explicit cumulative declaration destination",
            id="research-second-basis-epoch-cumulative-checkpoint-declaration-destination",
        )
        yield Static(
            "No-overwrite destination for the next 37C/37D continuation overlay",
            id="research-second-basis-epoch-cumulative-checkpoint-overlay-destination-label",
        )
        yield Input(
            placeholder="Explicit next continuation overlay destination",
            id="research-second-basis-epoch-cumulative-checkpoint-overlay-destination",
        )
        yield Button(
            "Save proven cumulative second-epoch continuation checkpoint",
            id="save-research-second-basis-epoch-cumulative-checkpoint",
            variant="warning",
        )
        yield Static(
            "Further revision remains locked until a fresh cumulative checkpoint succeeds.",
            id="research-second-basis-epoch-cumulative-checkpoint-status",
            markup=False,
        )

    def lock_after_success(
        self,
        result: ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionResult,
    ) -> None:
        """Lock the old one-hop checkpoint form before its surface is promoted away."""

        if not isinstance(
            result,
            ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionResult,
        ):
            raise TypeError(
                "result must be ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionResult."
            )
        if result.current_reentry is not self.current_reentry:
            raise ValueError(
                "Cumulative second-epoch checkpoint result does not retain this form's exact current re-entry."
            )
        if result.rollover is not self.rollover:
            raise ValueError(
                "Cumulative second-epoch checkpoint result does not retain this form's exact rollover."
            )

        self.persistence_result = result
        for selector in (
            "#research-second-basis-epoch-cumulative-checkpoint-current-overlay-source",
            "#research-second-basis-epoch-cumulative-checkpoint-successor-source",
            "#research-second-basis-epoch-cumulative-checkpoint-declaration-destination",
            "#research-second-basis-epoch-cumulative-checkpoint-overlay-destination",
        ):
            self.query_one(selector, Input).disabled = True
        self.query_one(
            "#save-research-second-basis-epoch-cumulative-checkpoint",
            Button,
        ).disabled = True
        self.query_one(
            "#research-second-basis-epoch-cumulative-checkpoint-status",
            Static,
        ).update(second_basis_epoch_cumulative_checkpoint_success_receipt(result))


__all__ = [
    "SECOND_BASIS_EPOCH_CUMULATIVE_CHECKPOINT_AUTHORITY_NOTICE",
    "SecondBasisEpochResearchSessionCumulativeCheckpointControls",
    "second_basis_epoch_cumulative_checkpoint_success_receipt",
]
