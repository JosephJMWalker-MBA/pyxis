from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Input, Static

from pyxis.app.chromium_research_session_rollover import ChromiumResearchSessionRolloverResult
from pyxis.app.chromium_research_third_basis_epoch_continuation_reentry_plan_document import (
    ChromiumResearchThirdBasisEpochContinuationCheckpointResult,
)


THIRD_BASIS_EPOCH_CHECKPOINT_AUTHORITY_NOTICE = (
    "Checkpoint this explicitly chosen first continuation through the 40C third-epoch "
    "boundary. Re-enter all current durable locations explicitly; the proven launch "
    "overlay and rollover inputs are context, not reusable path authority. The saved "
    "overlay is operational restart configuration only, not evidence or a "
    "latest/current/head pointer."
)


def _candidate_receipt(result: ChromiumResearchSessionRolloverResult) -> str:
    return (
        "Mounted third-epoch continuation is not yet checkpointed through a 40C overlay.\n"
        f"Chosen successor SHA-256: {result.prior_revision.persistence.edge_record_sha256}\n"
        f"One-hop continuation declaration SHA-256: {result.declaration.sequence_record_sha256}\n"
        "Further endpoint revision remains locked. Supply explicit current locations below."
    )


def third_basis_epoch_checkpoint_success_receipt(
    result: ChromiumResearchThirdBasisEpochContinuationCheckpointResult,
) -> str:
    """Format one receipt for a freshly proven first post-third-root checkpoint."""

    prior = result.fresh_reentry.prior_third_basis_epoch_reentry
    second_epoch = (
        prior.prior_second_basis_epoch_continuation_reentry
        .prior_second_basis_epoch_reentry
    )
    first_root = (
        second_epoch.prior_continuation_reentry.prior_root_backed_reentry.loaded_root
    )
    second_root = second_epoch.loaded_root
    third_root = prior.loaded_root
    return (
        "Success — first continuation above the third evidence-basis epoch freshly "
        "proven and checkpointed.\n"
        f"40C continuation overlay: {result.persistence.path}\n"
        f"Declared endpoint SHA-256: "
        f"{result.fresh_reentry.controller.declared_endpoint.verification.edge_record_sha256}\n"
        f"Retained third-root SHA-256: {third_root.verification.root_record_sha256}\n"
        f"Retained second-root SHA-256: {second_root.verification.root_record_sha256}\n"
        f"Retained first-root SHA-256: {first_root.verification.root_record_sha256}\n"
        "Further revision remains locked in this first-checkpoint shell. Relaunch "
        "explicitly with `pyxis research-shell "
        "--third-basis-epoch-continuation-overlay <saved-overlay>` before continuing. "
        "This checkpoint is not a global latest/current/head claim."
    )


class ThirdBasisEpochResearchSessionContinuationCheckpointControls(Vertical):
    """Blank explicit inputs for one governed 40C first-continuation checkpoint."""

    def __init__(self, rollover: ChromiumResearchSessionRolloverResult) -> None:
        if not isinstance(rollover, ChromiumResearchSessionRolloverResult):
            raise TypeError("rollover must be ChromiumResearchSessionRolloverResult.")
        super().__init__(id="research-third-basis-epoch-continuation-checkpoint-controls")
        self.rollover = rollover
        self.persistence_result: (
            ChromiumResearchThirdBasisEpochContinuationCheckpointResult | None
        ) = None

    def compose(self) -> ComposeResult:
        yield Static(
            "Checkpoint first continuation from persisted third-epoch ancestry",
            id="research-third-basis-epoch-checkpoint-title",
        )
        yield Static(
            THIRD_BASIS_EPOCH_CHECKPOINT_AUTHORITY_NOTICE,
            id="research-third-basis-epoch-checkpoint-authority-notice",
            markup=False,
        )
        yield Static(
            _candidate_receipt(self.rollover),
            id="research-third-basis-epoch-checkpoint-candidate",
            markup=False,
        )
        yield Static(
            "Current durable file for the exact prior 40B third-epoch overlay",
            id="research-third-basis-epoch-checkpoint-prior-overlay-source-label",
        )
        yield Input(
            placeholder="Explicit current 40B overlay path",
            id="research-third-basis-epoch-checkpoint-prior-overlay-source",
        )
        yield Static(
            "Current durable file for the exact chosen successor",
            id="research-third-basis-epoch-checkpoint-successor-source-label",
        )
        yield Input(
            placeholder="Explicit current successor edge path",
            id="research-third-basis-epoch-checkpoint-successor-source",
        )
        yield Static(
            "Current durable file for the exact one-hop continuation declaration",
            id="research-third-basis-epoch-checkpoint-declaration-source-label",
        )
        yield Input(
            placeholder="Explicit current continuation declaration path",
            id="research-third-basis-epoch-checkpoint-declaration-source",
        )
        yield Static(
            "No-overwrite destination for the proven 40C continuation overlay",
            id="research-third-basis-epoch-checkpoint-destination-label",
        )
        yield Input(
            placeholder="Explicit 40C continuation overlay destination",
            id="research-third-basis-epoch-checkpoint-destination",
        )
        yield Button(
            "Save proven 40C continuation checkpoint",
            id="save-research-third-basis-epoch-continuation-checkpoint",
            variant="warning",
        )
        yield Static(
            "Further revision remains locked until this checkpoint succeeds; 41C also "
            "keeps revision locked after success until an explicit continuation-overlay relaunch.",
            id="research-third-basis-epoch-checkpoint-status",
            markup=False,
        )

    def lock_after_success(
        self,
        result: ChromiumResearchThirdBasisEpochContinuationCheckpointResult,
    ) -> None:
        """Lock this form after one successful no-overwrite 40C checkpoint."""

        if not isinstance(
            result,
            ChromiumResearchThirdBasisEpochContinuationCheckpointResult,
        ):
            raise TypeError(
                "result must be ChromiumResearchThirdBasisEpochContinuationCheckpointResult."
            )
        if result.rollover is not self.rollover:
            raise ValueError(
                "Third-epoch checkpoint result does not belong to this exact rollover."
            )

        self.persistence_result = result
        for selector in (
            "#research-third-basis-epoch-checkpoint-prior-overlay-source",
            "#research-third-basis-epoch-checkpoint-successor-source",
            "#research-third-basis-epoch-checkpoint-declaration-source",
            "#research-third-basis-epoch-checkpoint-destination",
        ):
            self.query_one(selector, Input).disabled = True
        self.query_one(
            "#save-research-third-basis-epoch-continuation-checkpoint",
            Button,
        ).disabled = True
        self.query_one("#research-third-basis-epoch-checkpoint-status", Static).update(
            third_basis_epoch_checkpoint_success_receipt(result)
        )


__all__ = [
    "THIRD_BASIS_EPOCH_CHECKPOINT_AUTHORITY_NOTICE",
    "ThirdBasisEpochResearchSessionContinuationCheckpointControls",
    "third_basis_epoch_checkpoint_success_receipt",
]
