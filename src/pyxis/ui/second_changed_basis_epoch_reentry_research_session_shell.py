from __future__ import annotations

from pathlib import Path

from textual.widgets import Button, Input, Static

from pyxis.app.chromium_research_paragraph_text_selection_comparison_note_load import (
    ChromiumPageResearchLoadedParagraphTextSelectionComparisonNoteRecord,
)
from pyxis.app.chromium_research_paragraph_text_selection_note_load import (
    ChromiumPageResearchLoadedParagraphTextSelectionNoteRecord,
)
from pyxis.app.chromium_research_second_changed_basis_epoch_reentry import (
    ChromiumResearchSecondChangedBasisEpochReentryResult,
    verify_chromium_research_second_changed_basis_epoch_reentry,
)
from pyxis.app.chromium_research_second_changed_basis_session_adoption import (
    ChromiumResearchSecondChangedBasisSessionAdoptionResult,
)
from pyxis.app.chromium_research_selection_note_load import (
    ChromiumPageResearchLoadedParagraphNoteRecord,
)
from pyxis.app.chromium_research_session_reentry import (
    ChromiumResearchComparisonNoteReentryLocator,
    ChromiumResearchExactRangeNoteReentryLocator,
    ChromiumResearchParagraphNoteReentryLocator,
    ChromiumResearchWorkingSetMemberReentryLocator,
)

from .chromium_research_second_changed_basis_epoch_reentry_textual import (
    ResearchSecondChangedBasisEpochReentryControls,
)
from .second_changed_basis_session_adoption_research_session_shell import (
    SecondChangedBasisSessionAdoptionResearchSessionShell,
)


class SecondChangedBasisEpochReentryResearchSessionShell(
    SecondChangedBasisSessionAdoptionResearchSessionShell
):
    """Concrete 46A→46E surface through explicit public-37A reconstruction proof.

    46E proves restartability for the exact historical 46D adopted second-basis
    session. The freshly reconstructed second-epoch controller remains proof evidence
    only; it never replaces the currently mounted controller and no 37B overlay is
    written.
    """

    CSS = SecondChangedBasisSessionAdoptionResearchSessionShell.CSS + """
    #research-second-changed-basis-epoch-reentry-controls {
        width: 94%;
        height: auto;
        padding: 1 2;
        margin-top: 1;
        border: round $warning;
    }

    #research-second-changed-basis-epoch-reentry-authority-notice,
    #research-second-changed-basis-epoch-reentry-summary,
    #research-second-changed-basis-epoch-reentry-status,
    .research-second-changed-basis-epoch-reentry-member-summary,
    .research-second-changed-basis-epoch-reentry-input {
        margin-top: 1;
    }

    #research-second-changed-basis-epoch-reentry-title {
        text-style: bold;
    }

    #verify-research-second-changed-basis-epoch-reentry {
        margin-top: 1;
    }
    """

    def __init__(self, reentry) -> None:
        super().__init__(reentry)
        self.last_second_changed_basis_epoch_reentry_verification: (
            ChromiumResearchSecondChangedBasisEpochReentryResult | None
        ) = None

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "verify-research-second-changed-basis-epoch-reentry":
            event.stop()
            self.call_after_refresh(self._verify_second_changed_basis_epoch_reentry)
            return
        # Textual dispatches inherited handlers through the MRO. Do not manually call
        # super().on_button_pressed(event), which would schedule inherited actions twice.

    async def _promote_second_changed_basis_session_adoption(
        self,
        result: ChromiumResearchSecondChangedBasisSessionAdoptionResult,
    ) -> None:
        """Run inherited 46D promotion, then mount 46E for that exact history target."""

        prior = self.last_second_changed_basis_session_adoption
        await super()._promote_second_changed_basis_session_adoption(result)
        adoption = self.last_second_changed_basis_session_adoption
        if adoption is None or adoption is prior:
            return
        if adoption is not result:
            raise ValueError("46E promotion did not retain the exact successful 46D adoption.")
        appended_items = (
            adoption.edge_result.root_result.transition_result.prepared.appended_items
        )
        if len(self.query("#research-second-changed-basis-epoch-reentry-controls")) != 0:
            raise ValueError("Second-basis fresh re-entry verification controls are already mounted.")
        await self.mount(
            ResearchSecondChangedBasisEpochReentryControls(adoption, appended_items)
        )

    async def _verify_second_changed_basis_epoch_reentry(self) -> None:
        controls = self.query_one(
            "#research-second-changed-basis-epoch-reentry-controls",
            ResearchSecondChangedBasisEpochReentryControls,
        )
        status = self.query_one(
            "#research-second-changed-basis-epoch-reentry-status",
            Static,
        )
        adoption = self.last_second_changed_basis_session_adoption
        if adoption is None or controls.adoption_result is not adoption:
            status.update(
                "Re-entry verification failed: no exact successful 46D adoption owns this form."
            )
            return

        appended_locators = self._collect_46e_appended_locators(controls, status)
        if appended_locators is None:
            return

        prior_overlay = self.query_one(
            "#research-second-changed-basis-epoch-reentry-prior-continuation-overlay-source",
            Input,
        )
        if not prior_overlay.value.strip():
            status.update(
                "Re-entry verification failed: explicit prior 35D/35E continuation overlay path is required."
            )
            return

        general_ids = (
            ("changed-working-set-source", "explicit changed working-set path"),
            ("changed-note-source", "explicit changed working-set-note path"),
            ("transition-source", "explicit second 33B transition path"),
            ("root-source", "explicit second 34A root path"),
            ("first-edge-source", "explicit first post-second-root edge path"),
            ("declaration-source", "explicit second-root-backed declaration path"),
        )
        general: dict[str, Path] = {}
        for suffix, label in general_ids:
            widget = self.query_one(
                f"#research-second-changed-basis-epoch-reentry-{suffix}", Input
            )
            if not widget.value.strip():
                status.update(f"Re-entry verification failed: {label} is required.")
                return
            general[suffix] = Path(widget.value)

        mounted_controller = self.research_controller
        mounted_session = self.research_session
        mounted_reentry = self.research_reentry
        historical_continuation = self.root_backed_continuation_reentry
        try:
            result = verify_chromium_research_second_changed_basis_epoch_reentry(
                adoption,
                Path(prior_overlay.value),
                appended_locators,
                changed_working_set_source=general["changed-working-set-source"],
                changed_note_source=general["changed-note-source"],
                transition_source=general["transition-source"],
                root_source=general["root-source"],
                first_edge_source=general["first-edge-source"],
                declaration_source=general["declaration-source"],
            )
        except Exception as exc:
            status.update(f"Re-entry verification failed: {exc}")
            return

        if result.adoption_result is not adoption:
            raise ValueError("46E proof did not retain the exact 46D adoption.")
        if (
            self.research_controller is not mounted_controller
            or self.research_session is not mounted_session
            or self.research_reentry is not mounted_reentry
            or self.root_backed_continuation_reentry is not historical_continuation
        ):
            raise ValueError(
                "Mounted governed state or retained prior continuation changed during 46E fresh reconstruction proof."
            )

        self.last_second_changed_basis_epoch_reentry_verification = result
        controls.lock_after_success(result)

    def _collect_46e_appended_locators(
        self,
        controls: ResearchSecondChangedBasisEpochReentryControls,
        status: Static,
    ) -> tuple[ChromiumResearchWorkingSetMemberReentryLocator, ...] | None:
        locators: list[ChromiumResearchWorkingSetMemberReentryLocator] = []
        for index, item in enumerate(controls.appended_items):
            note = self.query_one(
                f"#research-second-changed-basis-epoch-reentry-member-{index}-note-source",
                Input,
            )
            if isinstance(item, ChromiumPageResearchLoadedParagraphTextSelectionComparisonNoteRecord):
                first = self.query_one(
                    f"#research-second-changed-basis-epoch-reentry-member-{index}-first-capture-source",
                    Input,
                )
                second = self.query_one(
                    f"#research-second-changed-basis-epoch-reentry-member-{index}-second-capture-source",
                    Input,
                )
                if not first.value.strip() or not second.value.strip() or not note.value.strip():
                    status.update(
                        f"Re-entry verification failed: appended comparison member {index} requires both capture paths and note path."
                    )
                    return None
                locators.append(
                    ChromiumResearchComparisonNoteReentryLocator(
                        first_capture_source=Path(first.value),
                        second_capture_source=Path(second.value),
                        note_source=Path(note.value),
                    )
                )
                continue

            capture = self.query_one(
                f"#research-second-changed-basis-epoch-reentry-member-{index}-capture-source",
                Input,
            )
            if not capture.value.strip() or not note.value.strip():
                status.update(
                    f"Re-entry verification failed: appended member {index} requires capture and note paths."
                )
                return None
            if isinstance(item, ChromiumPageResearchLoadedParagraphNoteRecord):
                locators.append(
                    ChromiumResearchParagraphNoteReentryLocator(
                        capture_source=Path(capture.value),
                        note_source=Path(note.value),
                    )
                )
            elif isinstance(item, ChromiumPageResearchLoadedParagraphTextSelectionNoteRecord):
                locators.append(
                    ChromiumResearchExactRangeNoteReentryLocator(
                        capture_source=Path(capture.value),
                        note_source=Path(note.value),
                    )
                )
            else:
                raise TypeError("46E encountered an unsupported appended working-set item.")
        return tuple(locators)


def create_second_changed_basis_epoch_reentry_research_session_shell(
    reentry,
) -> SecondChangedBasisEpochReentryResearchSessionShell:
    """Create the concrete second changed-basis product surface through 37A proof."""

    return SecondChangedBasisEpochReentryResearchSessionShell(reentry)


__all__ = [
    "SecondChangedBasisEpochReentryResearchSessionShell",
    "create_second_changed_basis_epoch_reentry_research_session_shell",
]
