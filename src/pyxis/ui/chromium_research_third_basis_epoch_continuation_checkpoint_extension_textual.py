from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Input, Static

from pyxis.app.chromium_research_session_rollover import ChromiumResearchSessionRolloverResult
from pyxis.app.chromium_research_third_basis_epoch_continuation_checkpoint_extension import (
    ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionResult,
)
from pyxis.app.chromium_research_third_basis_epoch_continuation_reentry_plan_document import (
    ChromiumResearchThirdBasisEpochContinuationReentryResult,
)


THIRD_BASIS_EPOCH_CUMULATIVE_CHECKPOINT_AUTHORITY_NOTICE = (
    "Checkpoint this explicitly chosen next continuation through the cumulative 40D "
    "post-third-root boundary. Re-enter the current 40C/40D overlay and chosen "
    "successor locations explicitly, plus two distinct no-overwrite destinations. "
    "Launch-time and prior-checkpoint paths are not reused as current-location "
    "authority. The resulting declaration and overlay are operational restart "
    "configuration, not latest/current/head authority."
)


def _candidate_receipt(
    current: ChromiumResearchThirdBasisEpochContinuationReentryResult,
    rollover: ChromiumResearchSessionRolloverResult,
) -> str:
    return (
        "Mounted one-hop continuation is not yet checkpointed into the cumulative "
        "post-third-root lineage.\n"
        f"Current cumulative edge count: {len(current.plan.declared_edge_sources)}\n"
        f"Chosen successor SHA-256: {rollover.prior_revision.persistence.edge_record_sha256}\n"
        "Further endpoint revision remains locked. Supply explicit current locations "
        "and new destinations below."
    )


def third_basis_epoch_cumulative_checkpoint_success_receipt(
    result: ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionResult,
) -> str:
    """Format one receipt for a freshly proven cumulative 40D checkpoint."""

    endpoint = result.fresh_reentry.controller.declared_endpoint
    return (
        "Success — cumulative post-third-root continuation freshly proven and checkpointed.\n"
        f"Cumulative declaration: {result.declaration.path}\n"
        f"Next 40C/40D overlay: {result.overlay.path}\n"
        f"Declared post-third-root edge count: {len(result.next_plan.declared_edge_sources)}\n"
        f"Terminal edge SHA-256: {endpoint.verification.edge_record_sha256}\n"
        "The shell now displays the exact freshly proven cumulative continuation and "
        "may author one next explicit successor. This is not a global "
        "latest/current/head claim."
    )


class ThirdBasisEpochResearchSessionCumulativeCheckpointControls(Vertical):
    """Blank explicit inputs for one governed cumulative 40D checkpoint."""

    def __init__(
        self,
        current_reentry: ChromiumResearchThirdBasisEpochContinuationReentryResult,
        rollover: ChromiumResearchSessionRolloverResult,
    ) -> None:
        if not isinstance(
            current_reentry,
            ChromiumResearchThirdBasisEpochContinuationReentryResult,
        ):
            raise TypeError(
                "current_reentry must be ChromiumResearchThirdBasisEpochContinuationReentryResult."
            )
        if not isinstance(rollover, ChromiumResearchSessionRolloverResult):
            raise TypeError("rollover must be ChromiumResearchSessionRolloverResult.")
        super().__init__(id="research-third-basis-epoch-cumulative-checkpoint-controls")
        self.current_reentry = current_reentry
        self.rollover = rollover
        self.persistence_result: (
            ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionResult | None
        ) = None

    def compose(self) -> ComposeResult:
        yield Static(
            "Checkpoint cumulative post-third-root continuation",
            id="research-third-basis-epoch-cumulative-checkpoint-title",
        )
        yield Static(
            THIRD_BASIS_EPOCH_CUMULATIVE_CHECKPOINT_AUTHORITY_NOTICE,
            id="research-third-basis-epoch-cumulative-checkpoint-authority-notice",
            markup=False,
        )
        yield Static(
            _candidate_receipt(self.current_reentry, self.rollover),
            id="research-third-basis-epoch-cumulative-checkpoint-candidate",
            markup=False,
        )
        yield Static(
            "Current durable file for the exact current 40C/40D continuation overlay",
            id="research-third-basis-epoch-cumulative-checkpoint-current-overlay-source-label",
        )
        yield Input(
            placeholder="Explicit current 40C/40D overlay path",
            id="research-third-basis-epoch-cumulative-checkpoint-current-overlay-source",
        )
        yield Static(
            "Current durable file for the exact chosen successor",
            id="research-third-basis-epoch-cumulative-checkpoint-successor-source-label",
        )
        yield Input(
            placeholder="Explicit current chosen successor edge path",
            id="research-third-basis-epoch-cumulative-checkpoint-successor-source",
        )
        yield Static(
            "No-overwrite destination for the new cumulative post-third-root declaration",
            id="research-third-basis-epoch-cumulative-checkpoint-declaration-destination-label",
        )
        yield Input(
            placeholder="Explicit cumulative declaration destination",
            id="research-third-basis-epoch-cumulative-checkpoint-declaration-destination",
        )
        yield Static(
            "No-overwrite destination for the next 40C/40D continuation overlay",
            id="research-third-basis-epoch-cumulative-checkpoint-overlay-destination-label",
        )
        yield Input(
            placeholder="Explicit next continuation overlay destination",
            id="research-third-basis-epoch-cumulative-checkpoint-overlay-destination",
        )
        yield Button(
            "Save proven cumulative third-epoch continuation checkpoint",
            id="save-research-third-basis-epoch-cumulative-checkpoint",
            variant="warning",
        )
        yield Static(
            "Further revision remains locked until a fresh cumulative checkpoint succeeds.",
            id="research-third-basis-epoch-cumulative-checkpoint-status",
            markup=False,
        )

    def lock_after_success(
        self,
        result: ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionResult,
    ) -> None:
        """Lock the old one-hop checkpoint form before its surface is promoted away."""

        if not isinstance(
            result,
            ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionResult,
        ):
            raise TypeError(
                "result must be ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionResult."
            )
        if result.current_reentry is not self.current_reentry:
            raise ValueError(
                "Cumulative third-epoch checkpoint result does not retain this form's exact current re-entry."
            )
        if result.rollover is not self.rollover:
            raise ValueError(
                "Cumulative third-epoch checkpoint result does not retain this form's exact rollover."
            )

        self.persistence_result = result
        for selector in (
            "#research-third-basis-epoch-cumulative-checkpoint-current-overlay-source",
            "#research-third-basis-epoch-cumulative-checkpoint-successor-source",
            "#research-third-basis-epoch-cumulative-checkpoint-declaration-destination",
            "#research-third-basis-epoch-cumulative-checkpoint-overlay-destination",
        ):
            self.query_one(selector, Input).disabled = True
        self.query_one(
            "#save-research-third-basis-epoch-cumulative-checkpoint",
            Button,
        ).disabled = True
        self.query_one(
            "#research-third-basis-epoch-cumulative-checkpoint-status",
            Static,
        ).update(third_basis_epoch_cumulative_checkpoint_success_receipt(result))


__all__ = [
    "THIRD_BASIS_EPOCH_CUMULATIVE_CHECKPOINT_AUTHORITY_NOTICE",
    "ThirdBasisEpochResearchSessionCumulativeCheckpointControls",
    "third_basis_epoch_cumulative_checkpoint_success_receipt",
]
