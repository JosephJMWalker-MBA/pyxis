from __future__ import annotations

from collections.abc import Iterable

from textual.widgets import Button

from pyxis.app.chromium_research_second_basis_epoch_continuation_reentry_plan_document import (
    ChromiumResearchSecondBasisEpochContinuationReentryResult,
)
from pyxis.app.chromium_research_second_basis_epoch_shell_lineage import (
    ChromiumResearchSecondBasisEpochContinuationShellLineage,
)
from pyxis.app.chromium_research_third_basis_epoch_reentry import (
    ChromiumResearchThirdBasisEpochReentryResult,
)
from pyxis.app.chromium_research_working_set import ChromiumPageResearchWorkingSetItem

from .chromium_research_changed_basis_typed_handoff_textual import (
    _ChangedBasisTypedHandoffSurfaceSpec,
    _mount_changed_basis_typed_handoff_after_new_persistence,
    _require_changed_basis_checkpoint_fresh_handoff,
)
from .third_basis_epoch_session_handoff_authority_inspection_shell import (
    create_inspectable_third_basis_epoch_handoff_research_session_shell,
)
from .third_changed_basis_epoch_reentry_overlay_research_session_shell import (
    InspectableThirdChangedBasisEpochReentryOverlayHandoffResearchSessionShell,
    InspectableThirdChangedBasisEpochReentryOverlayResearchSessionShell,
    ThirdChangedBasisEpochReentryOverlayHandoffResearchSessionShell,
    ThirdChangedBasisEpochReentryOverlayResearchSessionShell,
)


_HANDOFF_CSS = """
#research-third-changed-basis-epoch-handoff-notice {
    width: 94%;
    height: auto;
    padding: 1 2;
    margin-top: 1;
    border: round $secondary;
}

#continue-third-changed-basis-epoch-session {
    margin-top: 1;
}
"""


_THIRD_CHANGED_BASIS_EPOCH_HANDOFF = _ChangedBasisTypedHandoffSurfaceSpec(
    button_id="continue-third-changed-basis-epoch-session",
    notice_id="research-third-changed-basis-epoch-handoff-notice",
    notice_text=(
        "47F persistence is complete and the currently mounted changed-basis "
        "product remains unchanged. Choose the explicit handoff below to leave "
        "that state and continue with the exact freshly proven third-basis-epoch "
        "session in the established first-checkpoint product. This transfers "
        "typed in-memory proof; the saved 40B overlay path is not reloaded or "
        "promoted to current/latest/head authority."
    ),
    button_label="Continue with verified third-basis-epoch session",
    missing_result_error=(
        "47G handoff requires one exact successful retained 47F persistence result."
    ),
    invalid_handoff_error=(
        "47F checkpoint fresh re-entry must be exactly ChromiumResearchThirdBasisEpochReentryResult."
    ),
    duplicate_controls_error=(
        "47G handoff controls are already mounted after successful 47F persistence."
    ),
)


def _is_third_changed_basis_epoch_handoff(value: object) -> bool:
    return type(value) is ChromiumResearchThirdBasisEpochReentryResult


class _ThirdChangedBasisEpochHandoffProductMixin:
    """47G-only explicit typed handoff after one exact successful 47F persistence."""

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == _THIRD_CHANGED_BASIS_EPOCH_HANDOFF.button_id:
            event.stop()
            handoff = _require_changed_basis_checkpoint_fresh_handoff(
                self.last_third_changed_basis_epoch_reentry_overlay,
                spec=_THIRD_CHANGED_BASIS_EPOCH_HANDOFF,
                validate_handoff=_is_third_changed_basis_epoch_handoff,
            )
            self.exit(handoff)
        # Textual dispatches inherited message handlers through the MRO. Do not call
        # a parent handler manually or inherited 47A–47F actions will run twice.

    async def _persist_third_changed_basis_epoch_reentry_overlay(self) -> None:
        """Run inherited 47F, then expose 47G only after one new exact success."""

        prior = self.last_third_changed_basis_epoch_reentry_overlay
        await super()._persist_third_changed_basis_epoch_reentry_overlay()
        result = self.last_third_changed_basis_epoch_reentry_overlay
        await _mount_changed_basis_typed_handoff_after_new_persistence(
            self,
            previous_result=prior,
            current_result=result,
            spec=_THIRD_CHANGED_BASIS_EPOCH_HANDOFF,
            validate_handoff=_is_third_changed_basis_epoch_handoff,
        )


class ThirdChangedBasisEpochPersistedSourceHandoffResearchSessionShell(
    _ThirdChangedBasisEpochHandoffProductMixin,
    ThirdChangedBasisEpochReentryOverlayResearchSessionShell,
):
    """47G source product from a persisted second-epoch continuation launch."""

    CSS = ThirdChangedBasisEpochReentryOverlayResearchSessionShell.CSS + _HANDOFF_CSS


class ThirdChangedBasisEpochRawSourceHandoffResearchSessionShell(
    _ThirdChangedBasisEpochHandoffProductMixin,
    ThirdChangedBasisEpochReentryOverlayHandoffResearchSessionShell,
):
    """47G source product from an exact pathless 38F second-epoch handoff."""

    CSS = ThirdChangedBasisEpochReentryOverlayHandoffResearchSessionShell.CSS + _HANDOFF_CSS


class InspectableThirdChangedBasisEpochPersistedSourceHandoffResearchSessionShell(
    _ThirdChangedBasisEpochHandoffProductMixin,
    InspectableThirdChangedBasisEpochReentryOverlayResearchSessionShell,
):
    """Inspectable persisted-source 47G product."""

    CSS = (
        InspectableThirdChangedBasisEpochReentryOverlayResearchSessionShell.CSS
        + _HANDOFF_CSS
    )


class InspectableThirdChangedBasisEpochRawSourceHandoffResearchSessionShell(
    _ThirdChangedBasisEpochHandoffProductMixin,
    InspectableThirdChangedBasisEpochReentryOverlayHandoffResearchSessionShell,
):
    """Inspectable raw-source 47G product."""

    CSS = (
        InspectableThirdChangedBasisEpochReentryOverlayHandoffResearchSessionShell.CSS
        + _HANDOFF_CSS
    )


def _configure_candidate(shell, appended_items: Iterable[ChromiumPageResearchWorkingSetItem]):
    candidate = tuple(appended_items)
    if candidate:
        shell.configure_changed_basis_candidate(candidate)
    return shell


def create_third_changed_basis_epoch_persisted_source_handoff_research_session_shell(
    lineage: ChromiumResearchSecondBasisEpochContinuationShellLineage,
    appended_items: Iterable[ChromiumPageResearchWorkingSetItem] = (),
) -> ThirdChangedBasisEpochPersistedSourceHandoffResearchSessionShell:
    if not isinstance(lineage, ChromiumResearchSecondBasisEpochContinuationShellLineage):
        raise TypeError(
            "lineage must be ChromiumResearchSecondBasisEpochContinuationShellLineage."
        )
    return _configure_candidate(
        ThirdChangedBasisEpochPersistedSourceHandoffResearchSessionShell(lineage),
        appended_items,
    )


def create_third_changed_basis_epoch_raw_source_handoff_research_session_shell(
    reentry: ChromiumResearchSecondBasisEpochContinuationReentryResult,
    appended_items: Iterable[ChromiumPageResearchWorkingSetItem] = (),
) -> ThirdChangedBasisEpochRawSourceHandoffResearchSessionShell:
    if type(reentry) is not ChromiumResearchSecondBasisEpochContinuationReentryResult:
        raise TypeError(
            "reentry must be exactly ChromiumResearchSecondBasisEpochContinuationReentryResult."
        )
    return _configure_candidate(
        ThirdChangedBasisEpochRawSourceHandoffResearchSessionShell(reentry),
        appended_items,
    )


def create_inspectable_third_changed_basis_epoch_persisted_source_handoff_research_session_shell(
    lineage: ChromiumResearchSecondBasisEpochContinuationShellLineage,
    appended_items: Iterable[ChromiumPageResearchWorkingSetItem] = (),
) -> InspectableThirdChangedBasisEpochPersistedSourceHandoffResearchSessionShell:
    if not isinstance(lineage, ChromiumResearchSecondBasisEpochContinuationShellLineage):
        raise TypeError(
            "lineage must be ChromiumResearchSecondBasisEpochContinuationShellLineage."
        )
    return _configure_candidate(
        InspectableThirdChangedBasisEpochPersistedSourceHandoffResearchSessionShell(
            lineage
        ),
        appended_items,
    )


def create_inspectable_third_changed_basis_epoch_raw_source_handoff_research_session_shell(
    reentry: ChromiumResearchSecondBasisEpochContinuationReentryResult,
    appended_items: Iterable[ChromiumPageResearchWorkingSetItem] = (),
) -> InspectableThirdChangedBasisEpochRawSourceHandoffResearchSessionShell:
    if type(reentry) is not ChromiumResearchSecondBasisEpochContinuationReentryResult:
        raise TypeError(
            "reentry must be exactly ChromiumResearchSecondBasisEpochContinuationReentryResult."
        )
    return _configure_candidate(
        InspectableThirdChangedBasisEpochRawSourceHandoffResearchSessionShell(reentry),
        appended_items,
    )


def run_third_changed_basis_epoch_handoff_research_session_shell(
    lineage: ChromiumResearchSecondBasisEpochContinuationShellLineage,
    appended_items: Iterable[ChromiumPageResearchWorkingSetItem] = (),
) -> ChromiumResearchThirdBasisEpochReentryResult | None:
    """Chain only an explicit 47G result into the pathless inspectable receiver.

    Normal close returns None and launches nothing. An explicit 47G result is passed
    object-identically into the inspectable third-epoch receiver. No 40B overlay path
    is loaded, reconstructed, inferred, or carried as launch provenance.
    """

    handoff = create_third_changed_basis_epoch_persisted_source_handoff_research_session_shell(
        lineage,
        appended_items,
    ).run()
    if handoff is None:
        return None
    if type(handoff) is not ChromiumResearchThirdBasisEpochReentryResult:
        raise TypeError("47G shell returned an invalid third-basis-epoch handoff result.")

    create_inspectable_third_basis_epoch_handoff_research_session_shell(handoff).run()
    return handoff


__all__ = [
    "InspectableThirdChangedBasisEpochPersistedSourceHandoffResearchSessionShell",
    "InspectableThirdChangedBasisEpochRawSourceHandoffResearchSessionShell",
    "ThirdChangedBasisEpochPersistedSourceHandoffResearchSessionShell",
    "ThirdChangedBasisEpochRawSourceHandoffResearchSessionShell",
    "create_inspectable_third_changed_basis_epoch_persisted_source_handoff_research_session_shell",
    "create_inspectable_third_changed_basis_epoch_raw_source_handoff_research_session_shell",
    "create_third_changed_basis_epoch_persisted_source_handoff_research_session_shell",
    "create_third_changed_basis_epoch_raw_source_handoff_research_session_shell",
    "run_third_changed_basis_epoch_handoff_research_session_shell",
]
