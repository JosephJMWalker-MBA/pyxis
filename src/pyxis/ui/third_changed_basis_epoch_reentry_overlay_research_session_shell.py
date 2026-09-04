from __future__ import annotations

from textual.widgets import Button, Static

from pyxis.app.chromium_research_second_basis_epoch_continuation_reentry_plan_document import (
    ChromiumResearchSecondBasisEpochContinuationReentryResult,
)
from pyxis.app.chromium_research_second_basis_epoch_shell_lineage import (
    ChromiumResearchSecondBasisEpochContinuationShellLineage,
)
from pyxis.app.chromium_research_third_changed_basis_epoch_reentry_overlay import (
    ChromiumResearchThirdChangedBasisEpochReentryOverlayResult,
    persist_chromium_research_third_changed_basis_epoch_reentry_overlay,
)

from .chromium_research_changed_basis_restart_persistence_textual import (
    _ChangedBasisRestartPersistenceMountSpec,
    _ChangedBasisRestartPersistencePathSpec,
    _collect_changed_basis_restart_persistence_path_submission,
    _mount_changed_basis_restart_persistence_after_new_verification,
)
from .chromium_research_third_changed_basis_epoch_reentry_overlay_textual import (
    ResearchThirdChangedBasisEpochReentryOverlayControls,
)
from .third_changed_basis_epoch_reentry_research_session_shell import (
    InspectableThirdChangedBasisEpochReentryHandoffResearchSessionShell,
    InspectableThirdChangedBasisEpochReentryResearchSessionShell,
    ThirdChangedBasisEpochReentryHandoffResearchSessionShell,
    ThirdChangedBasisEpochReentryResearchSessionShell,
)


_THIRD_CHANGED_BASIS_EPOCH_REENTRY_OVERLAY_CSS = """
#research-third-changed-basis-epoch-reentry-overlay-controls {
    width: 94%;
    height: auto;
    padding: 1 2;
    margin-top: 1;
    border: round $warning;
}

#research-third-changed-basis-epoch-reentry-overlay-authority-notice,
#research-third-changed-basis-epoch-reentry-overlay-summary,
#research-third-changed-basis-epoch-reentry-overlay-status {
    margin-top: 1;
}

#research-third-changed-basis-epoch-reentry-overlay-title {
    text-style: bold;
}

#persist-research-third-changed-basis-epoch-reentry-overlay {
    margin-top: 1;
}
"""


_THIRD_CHANGED_BASIS_EPOCH_RESTART_PERSISTENCE_MOUNT = (
    _ChangedBasisRestartPersistenceMountSpec(
        controls_selector="#research-third-changed-basis-epoch-reentry-overlay-controls",
        duplicate_controls_error=(
            "Third-basis re-entry overlay controls are already mounted."
        ),
    )
)


_THIRD_CHANGED_BASIS_EPOCH_RESTART_PERSISTENCE_PATHS = (
    _ChangedBasisRestartPersistencePathSpec(
        source_selector=(
            "#research-third-changed-basis-epoch-reentry-overlay-prior-continuation-overlay-source"
        ),
        destination_selector=(
            "#research-third-changed-basis-epoch-reentry-overlay-destination"
        ),
        missing_source_error=(
            "Overlay persistence failed: explicit current prior 37C/37D second-epoch continuation-overlay path is required."
        ),
        missing_destination_error=(
            "Overlay persistence failed: explicit no-overwrite 40B destination is required."
        ),
    )
)


class _ThirdChangedBasisEpochReentryOverlayProductMixin:
    """47F-only persistence behavior shared by the four dedicated 47E products."""

    last_third_changed_basis_epoch_reentry_overlay: (
        ChromiumResearchThirdChangedBasisEpochReentryOverlayResult | None
    )

    def __init__(self, authority) -> None:
        super().__init__(authority)
        self.last_third_changed_basis_epoch_reentry_overlay = None

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Own only the 47F action; inherited handlers remain MRO-dispatched."""

        if event.button.id == "persist-research-third-changed-basis-epoch-reentry-overlay":
            event.stop()
            self.call_after_refresh(
                self._persist_third_changed_basis_epoch_reentry_overlay
            )

    async def _verify_third_changed_basis_epoch_reentry(self) -> None:
        """Run inherited 47E, then mount 47F only after one new exact success."""

        prior = self.last_third_changed_basis_epoch_reentry_verification
        await super()._verify_third_changed_basis_epoch_reentry()
        verification = self.last_third_changed_basis_epoch_reentry_verification
        await _mount_changed_basis_restart_persistence_after_new_verification(
            self,
            previous_verification=prior,
            current_verification=verification,
            spec=_THIRD_CHANGED_BASIS_EPOCH_RESTART_PERSISTENCE_MOUNT,
            create_controls=ResearchThirdChangedBasisEpochReentryOverlayControls,
        )

    async def _persist_third_changed_basis_epoch_reentry_overlay(self) -> None:
        controls = self.query_one(
            "#research-third-changed-basis-epoch-reentry-overlay-controls",
            ResearchThirdChangedBasisEpochReentryOverlayControls,
        )
        status = self.query_one(
            "#research-third-changed-basis-epoch-reentry-overlay-status",
            Static,
        )
        verification = self.last_third_changed_basis_epoch_reentry_verification
        if verification is None or controls.verification_result is not verification:
            status.update(
                "Overlay persistence failed: no exact successful 47E verification owns this form."
            )
            return

        paths = _collect_changed_basis_restart_persistence_path_submission(
            self,
            status=status,
            spec=_THIRD_CHANGED_BASIS_EPOCH_RESTART_PERSISTENCE_PATHS,
        )
        if paths is None:
            return

        mounted_controller = self.research_controller
        mounted_session = self.research_session
        mounted_reentry = self.research_reentry
        historical_continuation = self.second_basis_epoch_continuation_reentry
        try:
            result = persist_chromium_research_third_changed_basis_epoch_reentry_overlay(
                verification,
                prior_second_basis_epoch_continuation_overlay_source=paths.source,
                destination=paths.destination,
            )
        except Exception as exc:
            status.update(f"Overlay persistence failed: {exc}")
            return

        if result.verification_result is not verification:
            raise ValueError("47F did not retain the exact successful 47E verification.")
        if (
            self.research_controller is not mounted_controller
            or self.research_session is not mounted_session
            or self.research_reentry is not mounted_reentry
            or self.second_basis_epoch_continuation_reentry is not historical_continuation
        ):
            raise ValueError(
                "Mounted governed state or retained second-epoch continuation changed during 47F persistence."
            )

        self.last_third_changed_basis_epoch_reentry_overlay = result
        controls.lock_after_success(result)


class ThirdChangedBasisEpochReentryOverlayResearchSessionShell(
    _ThirdChangedBasisEpochReentryOverlayProductMixin,
    ThirdChangedBasisEpochReentryResearchSessionShell,
):
    """47F persistence product from a persisted second-epoch continuation launch."""

    CSS = (
        ThirdChangedBasisEpochReentryResearchSessionShell.CSS
        + _THIRD_CHANGED_BASIS_EPOCH_REENTRY_OVERLAY_CSS
    )


class ThirdChangedBasisEpochReentryOverlayHandoffResearchSessionShell(
    _ThirdChangedBasisEpochReentryOverlayProductMixin,
    ThirdChangedBasisEpochReentryHandoffResearchSessionShell,
):
    """47F persistence product from an exact pathless 38F second-epoch handoff."""

    CSS = (
        ThirdChangedBasisEpochReentryHandoffResearchSessionShell.CSS
        + _THIRD_CHANGED_BASIS_EPOCH_REENTRY_OVERLAY_CSS
    )


class InspectableThirdChangedBasisEpochReentryOverlayResearchSessionShell(
    _ThirdChangedBasisEpochReentryOverlayProductMixin,
    InspectableThirdChangedBasisEpochReentryResearchSessionShell,
):
    """Inspectable persisted-launch 47F product preserving inspection authority."""

    CSS = (
        InspectableThirdChangedBasisEpochReentryResearchSessionShell.CSS
        + _THIRD_CHANGED_BASIS_EPOCH_REENTRY_OVERLAY_CSS
    )

    async def _persist_third_changed_basis_epoch_reentry_overlay(self) -> None:
        panel = self.second_basis_epoch_authority_inspection
        launch = panel.launch_provenance
        current = panel.current_state
        await super()._persist_third_changed_basis_epoch_reentry_overlay()
        if panel.launch_provenance is not launch or panel.current_state is not current:
            raise ValueError(
                "47F persistence must not mutate persisted second-epoch launch provenance or current inspection state."
            )


class InspectableThirdChangedBasisEpochReentryOverlayHandoffResearchSessionShell(
    _ThirdChangedBasisEpochReentryOverlayProductMixin,
    InspectableThirdChangedBasisEpochReentryHandoffResearchSessionShell,
):
    """Inspectable pathless 47F product preserving raw 38F inspection authority."""

    CSS = (
        InspectableThirdChangedBasisEpochReentryHandoffResearchSessionShell.CSS
        + _THIRD_CHANGED_BASIS_EPOCH_REENTRY_OVERLAY_CSS
    )

    async def _persist_third_changed_basis_epoch_reentry_overlay(self) -> None:
        panel = self.second_basis_epoch_authority_inspection
        launch = panel.launch_provenance
        current = panel.current_state
        if launch.launch_location_context is not None:
            raise ValueError("Raw 38F launch provenance must remain pathless before 47F persistence.")
        await super()._persist_third_changed_basis_epoch_reentry_overlay()
        if panel.launch_provenance is not launch or panel.current_state is not current:
            raise ValueError(
                "47F persistence must not mutate raw 38F launch provenance or current inspection state."
            )
        if panel.launch_provenance.launch_location_context is not None:
            raise ValueError("47F persistence must not backfill a path into raw 38F launch provenance.")


def create_third_changed_basis_epoch_reentry_overlay_research_session_shell(
    lineage: ChromiumResearchSecondBasisEpochContinuationShellLineage,
) -> ThirdChangedBasisEpochReentryOverlayResearchSessionShell:
    if not isinstance(lineage, ChromiumResearchSecondBasisEpochContinuationShellLineage):
        raise TypeError(
            "lineage must be ChromiumResearchSecondBasisEpochContinuationShellLineage."
        )
    return ThirdChangedBasisEpochReentryOverlayResearchSessionShell(lineage)


def create_third_changed_basis_epoch_reentry_overlay_handoff_research_session_shell(
    reentry: ChromiumResearchSecondBasisEpochContinuationReentryResult,
) -> ThirdChangedBasisEpochReentryOverlayHandoffResearchSessionShell:
    if type(reentry) is not ChromiumResearchSecondBasisEpochContinuationReentryResult:
        raise TypeError(
            "reentry must be exactly ChromiumResearchSecondBasisEpochContinuationReentryResult."
        )
    return ThirdChangedBasisEpochReentryOverlayHandoffResearchSessionShell(reentry)


def create_inspectable_third_changed_basis_epoch_reentry_overlay_research_session_shell(
    lineage: ChromiumResearchSecondBasisEpochContinuationShellLineage,
) -> InspectableThirdChangedBasisEpochReentryOverlayResearchSessionShell:
    if not isinstance(lineage, ChromiumResearchSecondBasisEpochContinuationShellLineage):
        raise TypeError(
            "lineage must be ChromiumResearchSecondBasisEpochContinuationShellLineage."
        )
    return InspectableThirdChangedBasisEpochReentryOverlayResearchSessionShell(lineage)


def create_inspectable_third_changed_basis_epoch_reentry_overlay_handoff_research_session_shell(
    reentry: ChromiumResearchSecondBasisEpochContinuationReentryResult,
) -> InspectableThirdChangedBasisEpochReentryOverlayHandoffResearchSessionShell:
    if type(reentry) is not ChromiumResearchSecondBasisEpochContinuationReentryResult:
        raise TypeError(
            "reentry must be exactly ChromiumResearchSecondBasisEpochContinuationReentryResult."
        )
    return InspectableThirdChangedBasisEpochReentryOverlayHandoffResearchSessionShell(reentry)


__all__ = [
    "InspectableThirdChangedBasisEpochReentryOverlayHandoffResearchSessionShell",
    "InspectableThirdChangedBasisEpochReentryOverlayResearchSessionShell",
    "ThirdChangedBasisEpochReentryOverlayHandoffResearchSessionShell",
    "ThirdChangedBasisEpochReentryOverlayResearchSessionShell",
    "create_inspectable_third_changed_basis_epoch_reentry_overlay_handoff_research_session_shell",
    "create_inspectable_third_changed_basis_epoch_reentry_overlay_research_session_shell",
    "create_third_changed_basis_epoch_reentry_overlay_handoff_research_session_shell",
    "create_third_changed_basis_epoch_reentry_overlay_research_session_shell",
]
