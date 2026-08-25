from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Input, Static

from pyxis.app.chromium_research_second_basis_epoch_continuation_reentry_plan_document import (
    ChromiumResearchSecondBasisEpochContinuationCheckpointResult,
)
from pyxis.app.chromium_research_session_rollover import ChromiumResearchSessionRolloverResult


SECOND_BASIS_EPOCH_CHECKPOINT_AUTHORITY_NOTICE = (
    "Checkpoint this explicitly chosen first continuation through the 37C second-epoch "
    "boundary. Re-enter all current durable locations explicitly; the proven launch "
    "overlay and rollover inputs are context, not reusable path authority. The saved "
    "overlay is operational restart configuration only, not evidence or a "
    "latest/current/head pointer."
)


def _candidate_receipt(result: ChromiumResearchSessionRolloverResult) -> str:
    return (
        "Mounted second-epoch continuation is not yet checkpointed through a 37C overlay.\n"
        f"Chosen successor SHA-256: {result.prior_revision.persistence.edge_record_sha256}\n"
        f"One-hop continuation declaration SHA-256: {result.declaration.sequence_record_sha256}\n"
        "Further endpoint revision remains locked. Supply explicit current locations below."
    )


def second_basis_epoch_checkpoint_success_receipt(
    result: ChromiumResearchSecondBasisEpochContinuationCheckpointResult,
) -> str:
    """Format one receipt for a freshly proven first post-second-root checkpoint."""

    first_root = (
        result.fresh_reentry.prior_second_basis_epoch_reentry
        .prior_continuation_reentry.prior_root_backed_reentry.loaded_root
    )
    second_root = result.fresh_reentry.prior_second_basis_epoch_reentry.loaded_root
    return (
        "Success — first continuation above the second evidence-basis epoch freshly "
        "proven and checkpointed.\n"
        f"37C continuation overlay: {result.persistence.path}\n"
        f"Declared endpoint SHA-256: "
        f"{result.fresh_reentry.controller.declared_endpoint.verification.edge_record_sha256}\n"
        f"Retained second-root SHA-256: {second_root.verification.root_record_sha256}\n"
        f"Retained first-root SHA-256: {first_root.verification.root_record_sha256}\n"
        "Further revision remains locked in this first-checkpoint shell. Relaunch "
        "explicitly with `pyxis research-shell "
        "--second-basis-epoch-continuation-overlay <saved-overlay>` before continuing. "
        "This checkpoint is not a global latest/current/head claim."
    )


class SecondBasisEpochResearchSessionContinuationCheckpointControls(Vertical):
    """Blank explicit inputs for one governed 37C first-continuation checkpoint."""

    def __init__(self, rollover: ChromiumResearchSessionRolloverResult) -> None:
        if not isinstance(rollover, ChromiumResearchSessionRolloverResult):
            raise TypeError("rollover must be ChromiumResearchSessionRolloverResult.")
        super().__init__(id="research-second-basis-epoch-continuation-checkpoint-controls")
        self.rollover = rollover
        self.persistence_result: (
            ChromiumResearchSecondBasisEpochContinuationCheckpointResult | None
        ) = None

    def compose(self) -> ComposeResult:
        yield Static(
            "Checkpoint first continuation from persisted second-epoch ancestry",
            id="research-second-basis-epoch-checkpoint-title",
        )
        yield Static(
            SECOND_BASIS_EPOCH_CHECKPOINT_AUTHORITY_NOTICE,
            id="research-second-basis-epoch-checkpoint-authority-notice",
            markup=False,
        )
        yield Static(
            _candidate_receipt(self.rollover),
            id="research-second-basis-epoch-checkpoint-candidate",
            markup=False,
        )
        yield Static(
            "Current durable file for the exact prior 37B second-epoch overlay",
            id="research-second-basis-epoch-checkpoint-prior-overlay-source-label",
        )
        yield Input(
            placeholder="Explicit current 37B overlay path",
            id="research-second-basis-epoch-checkpoint-prior-overlay-source",
        )
        yield Static(
            "Current durable file for the exact chosen successor",
            id="research-second-basis-epoch-checkpoint-successor-source-label",
        )
        yield Input(
            placeholder="Explicit current successor edge path",
            id="research-second-basis-epoch-checkpoint-successor-source",
        )
        yield Static(
            "Current durable file for the exact one-hop continuation declaration",
            id="research-second-basis-epoch-checkpoint-declaration-source-label",
        )
        yield Input(
            placeholder="Explicit current continuation declaration path",
            id="research-second-basis-epoch-checkpoint-declaration-source",
        )
        yield Static(
            "No-overwrite destination for the proven 37C continuation overlay",
            id="research-second-basis-epoch-checkpoint-destination-label",
        )
        yield Input(
            placeholder="Explicit 37C continuation overlay destination",
            id="research-second-basis-epoch-checkpoint-destination",
        )
        yield Button(
            "Save proven 37C continuation checkpoint",
            id="save-research-second-basis-epoch-continuation-checkpoint",
            variant="warning",
        )
        yield Static(
            "Further revision remains locked until this checkpoint succeeds; 38D also "
            "keeps revision locked after success until an explicit continuation-overlay relaunch.",
            id="research-second-basis-epoch-checkpoint-status",
            markup=False,
        )

    def lock_after_success(
        self,
        result: ChromiumResearchSecondBasisEpochContinuationCheckpointResult,
    ) -> None:
        """Lock this form after one successful no-overwrite 37C checkpoint."""

        if not isinstance(
            result,
            ChromiumResearchSecondBasisEpochContinuationCheckpointResult,
        ):
            raise TypeError(
                "result must be ChromiumResearchSecondBasisEpochContinuationCheckpointResult."
            )
        if result.rollover is not self.rollover:
            raise ValueError(
                "Second-epoch checkpoint result does not belong to this exact rollover."
            )

        self.persistence_result = result
        for selector in (
            "#research-second-basis-epoch-checkpoint-prior-overlay-source",
            "#research-second-basis-epoch-checkpoint-successor-source",
            "#research-second-basis-epoch-checkpoint-declaration-source",
            "#research-second-basis-epoch-checkpoint-destination",
        ):
            self.query_one(selector, Input).disabled = True
        self.query_one(
            "#save-research-second-basis-epoch-continuation-checkpoint",
            Button,
        ).disabled = True
        self.query_one("#research-second-basis-epoch-checkpoint-status", Static).update(
            second_basis_epoch_checkpoint_success_receipt(result)
        )


__all__ = [
    "SECOND_BASIS_EPOCH_CHECKPOINT_AUTHORITY_NOTICE",
    "SecondBasisEpochResearchSessionContinuationCheckpointControls",
    "second_basis_epoch_checkpoint_success_receipt",
]
