from __future__ import annotations

from pyxis.app.chromium_research_root_backed_session_continuation_checkpoint_extension import (
    ChromiumResearchRootBackedSessionContinuationCheckpointExtensionResult,
)
from pyxis.app.chromium_research_root_backed_session_continuation_reentry_plan_document import (
    ChromiumResearchRootBackedSessionContinuationReentryResult,
)
from pyxis.app.chromium_research_session_rollover import ChromiumResearchSessionRolloverResult

from .chromium_research_cumulative_checkpoint_textual import (
    _CumulativeCheckpointTextualControls,
    _CumulativeCheckpointTextualSpec,
)


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


_SPEC = _CumulativeCheckpointTextualSpec(
    controls_id="research-root-backed-cumulative-checkpoint-controls",
    title="Checkpoint cumulative post-root continuation",
    title_id="research-root-backed-cumulative-checkpoint-title",
    authority_notice=CUMULATIVE_CHECKPOINT_AUTHORITY_NOTICE,
    authority_notice_id="research-root-backed-cumulative-checkpoint-authority-notice",
    candidate_id="research-root-backed-cumulative-checkpoint-candidate",
    current_overlay_label=(
        "Current durable file for the exact current 35D/35E continuation overlay"
    ),
    current_overlay_label_id=(
        "research-root-backed-cumulative-checkpoint-current-overlay-source-label"
    ),
    current_overlay_placeholder="Explicit current 35D/35E overlay path",
    current_overlay_input_id=(
        "research-root-backed-cumulative-checkpoint-current-overlay-source"
    ),
    successor_label="Current durable file for the exact chosen successor",
    successor_label_id="research-root-backed-cumulative-checkpoint-successor-source-label",
    successor_placeholder="Explicit current chosen successor edge path",
    successor_input_id="research-root-backed-cumulative-checkpoint-successor-source",
    declaration_label=(
        "No-overwrite destination for the new cumulative post-root declaration"
    ),
    declaration_label_id=(
        "research-root-backed-cumulative-checkpoint-declaration-destination-label"
    ),
    declaration_placeholder="Explicit cumulative declaration destination",
    declaration_input_id=(
        "research-root-backed-cumulative-checkpoint-declaration-destination"
    ),
    overlay_label="No-overwrite destination for the next 35D/35E continuation overlay",
    overlay_label_id=(
        "research-root-backed-cumulative-checkpoint-overlay-destination-label"
    ),
    overlay_placeholder="Explicit next continuation overlay destination",
    overlay_input_id="research-root-backed-cumulative-checkpoint-overlay-destination",
    save_label="Save proven cumulative continuation checkpoint",
    save_button_id="save-research-root-backed-cumulative-checkpoint",
    pending_status=(
        "Further revision remains locked until a fresh cumulative checkpoint succeeds."
    ),
    status_id="research-root-backed-cumulative-checkpoint-status",
)


class RootBackedResearchSessionCumulativeCheckpointControls(
    _CumulativeCheckpointTextualControls[
        ChromiumResearchRootBackedSessionContinuationReentryResult,
        ChromiumResearchRootBackedSessionContinuationCheckpointExtensionResult,
    ]
):
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
        super().__init__(
            current_reentry,
            rollover,
            spec=_SPEC,
            candidate_receipt=_candidate_receipt(current_reentry, rollover),
            success_receipt=cumulative_checkpoint_success_receipt,
        )

    def lock_after_success(
        self,
        result: ChromiumResearchRootBackedSessionContinuationCheckpointExtensionResult,
    ) -> None:
        """Lock the old one-hop checkpoint form before its surface is promoted away."""

        self._lock_cumulative_checkpoint_after_success(
            result,
            result_type=ChromiumResearchRootBackedSessionContinuationCheckpointExtensionResult,
            result_type_error=(
                "result must be ChromiumResearchRootBackedSessionContinuationCheckpointExtensionResult."
            ),
            current_identity_error=(
                "Cumulative checkpoint result does not retain this form's exact current re-entry lineage."
            ),
            rollover_identity_error=(
                "Cumulative checkpoint result does not retain this form's exact rollover."
            ),
        )


__all__ = [
    "CUMULATIVE_CHECKPOINT_AUTHORITY_NOTICE",
    "RootBackedResearchSessionCumulativeCheckpointControls",
    "cumulative_checkpoint_success_receipt",
]
