from __future__ import annotations

from pyxis.app.chromium_research_session_rollover import ChromiumResearchSessionRolloverResult
from pyxis.app.chromium_research_third_basis_epoch_continuation_checkpoint_extension import (
    ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionResult,
)
from pyxis.app.chromium_research_third_basis_epoch_continuation_reentry_plan_document import (
    ChromiumResearchThirdBasisEpochContinuationReentryResult,
)

from .chromium_research_cumulative_checkpoint_textual import (
    _CumulativeCheckpointTextualControls,
    _CumulativeCheckpointTextualSpec,
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


_SPEC = _CumulativeCheckpointTextualSpec(
    controls_id="research-third-basis-epoch-cumulative-checkpoint-controls",
    title="Checkpoint cumulative post-third-root continuation",
    title_id="research-third-basis-epoch-cumulative-checkpoint-title",
    authority_notice=THIRD_BASIS_EPOCH_CUMULATIVE_CHECKPOINT_AUTHORITY_NOTICE,
    authority_notice_id=(
        "research-third-basis-epoch-cumulative-checkpoint-authority-notice"
    ),
    candidate_id="research-third-basis-epoch-cumulative-checkpoint-candidate",
    current_overlay_label=(
        "Current durable file for the exact current 40C/40D continuation overlay"
    ),
    current_overlay_label_id=(
        "research-third-basis-epoch-cumulative-checkpoint-current-overlay-source-label"
    ),
    current_overlay_placeholder="Explicit current 40C/40D overlay path",
    current_overlay_input_id=(
        "research-third-basis-epoch-cumulative-checkpoint-current-overlay-source"
    ),
    successor_label="Current durable file for the exact chosen successor",
    successor_label_id=(
        "research-third-basis-epoch-cumulative-checkpoint-successor-source-label"
    ),
    successor_placeholder="Explicit current chosen successor edge path",
    successor_input_id=(
        "research-third-basis-epoch-cumulative-checkpoint-successor-source"
    ),
    declaration_label=(
        "No-overwrite destination for the new cumulative post-third-root declaration"
    ),
    declaration_label_id=(
        "research-third-basis-epoch-cumulative-checkpoint-declaration-destination-label"
    ),
    declaration_placeholder="Explicit cumulative declaration destination",
    declaration_input_id=(
        "research-third-basis-epoch-cumulative-checkpoint-declaration-destination"
    ),
    overlay_label=(
        "No-overwrite destination for the next 40C/40D continuation overlay"
    ),
    overlay_label_id=(
        "research-third-basis-epoch-cumulative-checkpoint-overlay-destination-label"
    ),
    overlay_placeholder="Explicit next continuation overlay destination",
    overlay_input_id=(
        "research-third-basis-epoch-cumulative-checkpoint-overlay-destination"
    ),
    save_label="Save proven cumulative third-epoch continuation checkpoint",
    save_button_id="save-research-third-basis-epoch-cumulative-checkpoint",
    pending_status=(
        "Further revision remains locked until a fresh cumulative checkpoint succeeds."
    ),
    status_id="research-third-basis-epoch-cumulative-checkpoint-status",
)


class ThirdBasisEpochResearchSessionCumulativeCheckpointControls(
    _CumulativeCheckpointTextualControls[
        ChromiumResearchThirdBasisEpochContinuationReentryResult,
        ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionResult,
    ]
):
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
        super().__init__(
            current_reentry,
            rollover,
            spec=_SPEC,
            candidate_receipt=_candidate_receipt(current_reentry, rollover),
            success_receipt=third_basis_epoch_cumulative_checkpoint_success_receipt,
        )

    def lock_after_success(
        self,
        result: ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionResult,
    ) -> None:
        """Lock the old one-hop checkpoint form before its surface is promoted away."""

        self._lock_cumulative_checkpoint_after_success(
            result,
            result_type=ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionResult,
            result_type_error=(
                "result must be ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionResult."
            ),
            current_identity_error=(
                "Cumulative third-epoch checkpoint result does not retain this form's exact current re-entry."
            ),
            rollover_identity_error=(
                "Cumulative third-epoch checkpoint result does not retain this form's exact rollover."
            ),
        )


__all__ = [
    "THIRD_BASIS_EPOCH_CUMULATIVE_CHECKPOINT_AUTHORITY_NOTICE",
    "ThirdBasisEpochResearchSessionCumulativeCheckpointControls",
    "third_basis_epoch_cumulative_checkpoint_success_receipt",
]
