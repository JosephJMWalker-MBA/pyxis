from __future__ import annotations

from pyxis.app.chromium_research_second_basis_epoch_continuation_checkpoint_extension import (
    ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionResult,
)
from pyxis.app.chromium_research_second_basis_epoch_continuation_reentry_plan_document import (
    ChromiumResearchSecondBasisEpochContinuationReentryResult,
)
from pyxis.app.chromium_research_session_rollover import ChromiumResearchSessionRolloverResult

from .chromium_research_cumulative_checkpoint_textual import (
    _CumulativeCheckpointTextualControls,
    _CumulativeCheckpointTextualSpec,
)


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


_SPEC = _CumulativeCheckpointTextualSpec(
    controls_id="research-second-basis-epoch-cumulative-checkpoint-controls",
    title="Checkpoint cumulative post-second-root continuation",
    title_id="research-second-basis-epoch-cumulative-checkpoint-title",
    authority_notice=SECOND_BASIS_EPOCH_CUMULATIVE_CHECKPOINT_AUTHORITY_NOTICE,
    authority_notice_id=(
        "research-second-basis-epoch-cumulative-checkpoint-authority-notice"
    ),
    candidate_id="research-second-basis-epoch-cumulative-checkpoint-candidate",
    current_overlay_label=(
        "Current durable file for the exact current 37C/37D continuation overlay"
    ),
    current_overlay_label_id=(
        "research-second-basis-epoch-cumulative-checkpoint-current-overlay-source-label"
    ),
    current_overlay_placeholder="Explicit current 37C/37D overlay path",
    current_overlay_input_id=(
        "research-second-basis-epoch-cumulative-checkpoint-current-overlay-source"
    ),
    successor_label="Current durable file for the exact chosen successor",
    successor_label_id=(
        "research-second-basis-epoch-cumulative-checkpoint-successor-source-label"
    ),
    successor_placeholder="Explicit current chosen successor edge path",
    successor_input_id=(
        "research-second-basis-epoch-cumulative-checkpoint-successor-source"
    ),
    declaration_label=(
        "No-overwrite destination for the new cumulative post-second-root declaration"
    ),
    declaration_label_id=(
        "research-second-basis-epoch-cumulative-checkpoint-declaration-destination-label"
    ),
    declaration_placeholder="Explicit cumulative declaration destination",
    declaration_input_id=(
        "research-second-basis-epoch-cumulative-checkpoint-declaration-destination"
    ),
    overlay_label=(
        "No-overwrite destination for the next 37C/37D continuation overlay"
    ),
    overlay_label_id=(
        "research-second-basis-epoch-cumulative-checkpoint-overlay-destination-label"
    ),
    overlay_placeholder="Explicit next continuation overlay destination",
    overlay_input_id=(
        "research-second-basis-epoch-cumulative-checkpoint-overlay-destination"
    ),
    save_label="Save proven cumulative second-epoch continuation checkpoint",
    save_button_id="save-research-second-basis-epoch-cumulative-checkpoint",
    pending_status=(
        "Further revision remains locked until a fresh cumulative checkpoint succeeds."
    ),
    status_id="research-second-basis-epoch-cumulative-checkpoint-status",
)


class SecondBasisEpochResearchSessionCumulativeCheckpointControls(
    _CumulativeCheckpointTextualControls[
        ChromiumResearchSecondBasisEpochContinuationReentryResult,
        ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionResult,
    ]
):
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
        super().__init__(
            current_reentry,
            rollover,
            spec=_SPEC,
            candidate_receipt=_candidate_receipt(current_reentry, rollover),
            success_receipt=second_basis_epoch_cumulative_checkpoint_success_receipt,
        )

    def lock_after_success(
        self,
        result: ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionResult,
    ) -> None:
        """Lock the old one-hop checkpoint form before its surface is promoted away."""

        self._lock_cumulative_checkpoint_after_success(
            result,
            result_type=ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionResult,
            result_type_error=(
                "result must be ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionResult."
            ),
            current_identity_error=(
                "Cumulative second-epoch checkpoint result does not retain this form's exact current re-entry."
            ),
            rollover_identity_error=(
                "Cumulative second-epoch checkpoint result does not retain this form's exact rollover."
            ),
        )


__all__ = [
    "SECOND_BASIS_EPOCH_CUMULATIVE_CHECKPOINT_AUTHORITY_NOTICE",
    "SecondBasisEpochResearchSessionCumulativeCheckpointControls",
    "second_basis_epoch_cumulative_checkpoint_success_receipt",
]
