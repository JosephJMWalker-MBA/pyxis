from __future__ import annotations

from collections.abc import Iterable

from textual.widgets import Button

from pyxis.app.chromium_research_root_backed_session_reentry import (
    ChromiumResearchRootBackedSessionReentryResult,
)
from pyxis.app.chromium_research_session_reentry import ChromiumResearchSessionReentryResult
from pyxis.app.chromium_research_working_set import ChromiumPageResearchWorkingSetItem

from .chromium_research_changed_basis_typed_handoff_runner import (
    _run_changed_basis_typed_handoff,
)
from .chromium_research_changed_basis_typed_handoff_textual import (
    _ChangedBasisTypedHandoffSurfaceSpec,
    _mount_changed_basis_typed_handoff_after_new_persistence,
    _require_changed_basis_checkpoint_fresh_handoff,
)
from .first_changed_basis_root_backed_reentry_overlay_research_session_shell import (
    FirstChangedBasisRootBackedReentryOverlayResearchSessionShell,
)
from .root_backed_authority_inspection_shell import (
    create_inspectable_root_backed_handoff_research_session_shell,
)


_FIRST_CHANGED_BASIS_ROOT_BACKED_HANDOFF = _ChangedBasisTypedHandoffSurfaceSpec(
    button_id="continue-first-changed-basis-root-backed-session",
    notice_id="research-first-changed-basis-root-backed-handoff-notice",
    notice_text=(
        "44G persistence is complete and the currently mounted governed session "
        "remains unchanged. Choose the explicit handoff below to leave that mounted "
        "state and continue with the exact freshly proven 35C root-backed session in "
        "the established root-backed product. This transfers typed in-memory proof; "
        "the saved overlay path is not reloaded or promoted to current/latest/head "
        "authority."
    ),
    button_label="Continue with verified changed-basis session",
    missing_result_error=(
        "44H handoff requires one exact successful retained 44G persistence result."
    ),
    invalid_handoff_error=(
        "44G checkpoint fresh re-entry must be a root-backed session re-entry result."
    ),
    duplicate_controls_error=(
        "44H handoff controls are already mounted after successful 44G persistence."
    ),
)


def _is_first_changed_basis_root_backed_handoff(value: object) -> bool:
    return isinstance(value, ChromiumResearchRootBackedSessionReentryResult)


class FirstChangedBasisRootBackedHandoffResearchSessionShell(
    FirstChangedBasisRootBackedReentryOverlayResearchSessionShell
):
    """Concrete 44A→44H surface with one explicit post-44G typed handoff.

    44H never treats successful 44G persistence as automatic mode promotion. Only an
    explicit button press exits this shell with the exact 35C `checkpoint.fresh_reentry`
    already earned by 44G. The persisted overlay path is not reloaded or promoted to
    current/latest/head authority during that in-process handoff.
    """

    CSS = FirstChangedBasisRootBackedReentryOverlayResearchSessionShell.CSS + """
    #research-first-changed-basis-root-backed-handoff-notice {
        width: 94%;
        height: auto;
        padding: 1 2;
        margin-top: 1;
        border: round $secondary;
    }

    #continue-first-changed-basis-root-backed-session {
        margin-top: 1;
    }
    """

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == _FIRST_CHANGED_BASIS_ROOT_BACKED_HANDOFF.button_id:
            event.stop()
            handoff = _require_changed_basis_checkpoint_fresh_handoff(
                self.last_first_changed_basis_root_backed_reentry_overlay,
                spec=_FIRST_CHANGED_BASIS_ROOT_BACKED_HANDOFF,
                validate_handoff=_is_first_changed_basis_root_backed_handoff,
            )
            self.exit(handoff)
            return
        # Textual dispatches inherited message handlers through the MRO. Calling a
        # parent handler manually would duplicate the inherited 44A–44G actions.

    async def _persist_research_first_changed_basis_root_backed_reentry_overlay(
        self,
    ) -> None:
        """Run inherited 44G, then expose 44H only after one new exact success."""

        prior = self.last_first_changed_basis_root_backed_reentry_overlay
        await super()._persist_research_first_changed_basis_root_backed_reentry_overlay()
        result = self.last_first_changed_basis_root_backed_reentry_overlay
        await _mount_changed_basis_typed_handoff_after_new_persistence(
            self,
            previous_result=prior,
            current_result=result,
            spec=_FIRST_CHANGED_BASIS_ROOT_BACKED_HANDOFF,
            validate_handoff=_is_first_changed_basis_root_backed_handoff,
        )


def create_first_changed_basis_root_backed_handoff_research_session_shell(
    ordinary_reentry: ChromiumResearchSessionReentryResult,
    appended_items: Iterable[ChromiumPageResearchWorkingSetItem],
) -> FirstChangedBasisRootBackedHandoffResearchSessionShell:
    """Create the first changed-basis product surface through explicit 44H handoff."""

    return FirstChangedBasisRootBackedHandoffResearchSessionShell(
        ordinary_reentry,
        appended_items,
    )


def run_first_changed_basis_root_backed_handoff_research_session_shell(
    ordinary_reentry: ChromiumResearchSessionReentryResult,
    appended_items: Iterable[ChromiumPageResearchWorkingSetItem],
) -> ChromiumResearchRootBackedSessionReentryResult | None:
    """Run 44H and chain only an explicit typed handoff into the inspectable receiver.

    Normal close returns ``None`` and launches nothing. When the 44H shell returns one
    exact root-backed re-entry result, this runner passes that same object directly to
    the 45A raw-handoff inspection adapter. No overlay path is read, reconstructed,
    inferred, or carried forward by this orchestration seam, so the receiver visibly
    records that this launch has no persistent path provenance.
    """

    source = create_first_changed_basis_root_backed_handoff_research_session_shell(
        ordinary_reentry,
        appended_items,
    )
    return _run_changed_basis_typed_handoff(
        run_source=source.run,
        validate_handoff=_is_first_changed_basis_root_backed_handoff,
        invalid_handoff_error="44H shell returned an invalid root-backed handoff result.",
        create_receiver=create_inspectable_root_backed_handoff_research_session_shell,
    )


__all__ = [
    "FirstChangedBasisRootBackedHandoffResearchSessionShell",
    "create_first_changed_basis_root_backed_handoff_research_session_shell",
    "run_first_changed_basis_root_backed_handoff_research_session_shell",
]
