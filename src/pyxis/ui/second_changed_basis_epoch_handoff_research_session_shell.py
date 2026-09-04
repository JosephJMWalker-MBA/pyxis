from __future__ import annotations

from collections.abc import Iterable

from textual.widgets import Button

from pyxis.app.chromium_research_root_backed_session_continuation_reentry_plan_document import (
    ChromiumResearchRootBackedSessionContinuationReentryResult,
)
from pyxis.app.chromium_research_second_basis_epoch_reentry import (
    ChromiumResearchSecondBasisEpochReentryResult,
)
from pyxis.app.chromium_research_working_set import ChromiumPageResearchWorkingSetItem

from .chromium_research_changed_basis_typed_handoff_runner import (
    _run_changed_basis_typed_handoff,
)
from .chromium_research_changed_basis_typed_handoff_textual import (
    _ChangedBasisTypedHandoffSurfaceSpec,
    _mount_changed_basis_typed_handoff_after_new_persistence,
    _require_changed_basis_checkpoint_fresh_handoff,
)
from .second_basis_epoch_session_handoff_authority_inspection_shell import (
    create_inspectable_second_basis_epoch_handoff_research_session_shell,
)
from .second_changed_basis_epoch_reentry_overlay_research_session_shell import (
    SecondChangedBasisEpochReentryOverlayResearchSessionShell,
)


_SECOND_CHANGED_BASIS_EPOCH_HANDOFF = _ChangedBasisTypedHandoffSurfaceSpec(
    button_id="continue-second-changed-basis-epoch-session",
    notice_id="research-second-changed-basis-epoch-handoff-notice",
    notice_text=(
        "46F persistence is complete and the currently mounted prior product "
        "remains unchanged. Choose the explicit handoff below to leave that state "
        "and continue with the exact freshly proven second-basis-epoch session in "
        "the established first-checkpoint product. This transfers typed in-memory "
        "proof; the saved 37B overlay path is not reloaded or promoted to "
        "current/latest/head authority."
    ),
    button_label="Continue with verified second-basis-epoch session",
    missing_result_error=(
        "46G handoff requires one exact successful retained 46F persistence result."
    ),
    invalid_handoff_error=(
        "46F checkpoint fresh re-entry must be exactly ChromiumResearchSecondBasisEpochReentryResult."
    ),
    duplicate_controls_error=(
        "46G handoff controls are already mounted after successful 46F persistence."
    ),
)


def _is_second_changed_basis_epoch_handoff(value: object) -> bool:
    return type(value) is ChromiumResearchSecondBasisEpochReentryResult


class SecondChangedBasisEpochHandoffResearchSessionShell(
    SecondChangedBasisEpochReentryOverlayResearchSessionShell
):
    """Concrete 46A→46G surface with one explicit post-46F typed handoff.

    Successful 46F persistence remains historical restart configuration only. It does
    not automatically promote this shell into second-epoch mode. Only the explicit
    handoff action exits with the exact public-37B `checkpoint.fresh_reentry` already
    earned in memory. The persisted 37B path is not reloaded, inferred, or promoted.
    """

    CSS = SecondChangedBasisEpochReentryOverlayResearchSessionShell.CSS + """
    #research-second-changed-basis-epoch-handoff-notice {
        width: 94%;
        height: auto;
        padding: 1 2;
        margin-top: 1;
        border: round $secondary;
    }

    #continue-second-changed-basis-epoch-session {
        margin-top: 1;
    }
    """

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == _SECOND_CHANGED_BASIS_EPOCH_HANDOFF.button_id:
            event.stop()
            handoff = _require_changed_basis_checkpoint_fresh_handoff(
                self.last_second_changed_basis_epoch_reentry_overlay,
                spec=_SECOND_CHANGED_BASIS_EPOCH_HANDOFF,
                validate_handoff=_is_second_changed_basis_epoch_handoff,
            )
            self.exit(handoff)
            return
        # Textual dispatches inherited message handlers through the MRO. Do not call
        # the parent handler manually or inherited 46A–46F actions will run twice.

    async def _persist_second_changed_basis_epoch_reentry_overlay(self) -> None:
        """Run inherited 46F, then expose 46G only after one new exact success."""

        prior = self.last_second_changed_basis_epoch_reentry_overlay
        await super()._persist_second_changed_basis_epoch_reentry_overlay()
        result = self.last_second_changed_basis_epoch_reentry_overlay
        await _mount_changed_basis_typed_handoff_after_new_persistence(
            self,
            previous_result=prior,
            current_result=result,
            spec=_SECOND_CHANGED_BASIS_EPOCH_HANDOFF,
            validate_handoff=_is_second_changed_basis_epoch_handoff,
        )


def create_second_changed_basis_epoch_handoff_research_session_shell(
    reentry: ChromiumResearchRootBackedSessionContinuationReentryResult,
    appended_items: Iterable[ChromiumPageResearchWorkingSetItem] = (),
) -> SecondChangedBasisEpochHandoffResearchSessionShell:
    """Create the concrete second changed-basis surface through explicit 46G handoff."""

    if type(reentry) is not ChromiumResearchRootBackedSessionContinuationReentryResult:
        raise TypeError(
            "reentry must be exactly ChromiumResearchRootBackedSessionContinuationReentryResult."
        )
    shell = SecondChangedBasisEpochHandoffResearchSessionShell(reentry)
    candidate = tuple(appended_items)
    if candidate:
        shell.configure_changed_basis_candidate(candidate)
    return shell


def run_second_changed_basis_epoch_handoff_research_session_shell(
    reentry: ChromiumResearchRootBackedSessionContinuationReentryResult,
    appended_items: Iterable[ChromiumPageResearchWorkingSetItem] = (),
) -> ChromiumResearchSecondBasisEpochReentryResult | None:
    """Run 46G and chain only an explicit typed handoff into the pathless receiver.

    Normal close returns ``None`` and launches nothing. An explicit 46G result is
    passed as the exact same object into the inspectable second-epoch receiver. No 37B
    overlay path is loaded, reconstructed, inferred, or carried as launch provenance.
    """

    source = create_second_changed_basis_epoch_handoff_research_session_shell(
        reentry,
        appended_items,
    )
    return _run_changed_basis_typed_handoff(
        run_source=source.run,
        validate_handoff=_is_second_changed_basis_epoch_handoff,
        invalid_handoff_error="46G shell returned an invalid second-basis-epoch handoff result.",
        create_receiver=create_inspectable_second_basis_epoch_handoff_research_session_shell,
    )


__all__ = [
    "SecondChangedBasisEpochHandoffResearchSessionShell",
    "create_second_changed_basis_epoch_handoff_research_session_shell",
    "run_second_changed_basis_epoch_handoff_research_session_shell",
]
