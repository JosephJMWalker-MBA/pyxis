from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path

from textual.widgets import Button, Input, Static

from pyxis.app.chromium_research_first_changed_basis_root_backed_reentry import (
    ChromiumResearchFirstChangedBasisRootBackedReentryResult,
    verify_chromium_research_first_changed_basis_root_backed_reentry,
)
from pyxis.app.chromium_research_paragraph_text_selection_comparison_note_load import (
    ChromiumPageResearchLoadedParagraphTextSelectionComparisonNoteRecord,
)
from pyxis.app.chromium_research_paragraph_text_selection_note_load import (
    ChromiumPageResearchLoadedParagraphTextSelectionNoteRecord,
)
from pyxis.app.chromium_research_selection_note_load import (
    ChromiumPageResearchLoadedParagraphNoteRecord,
)
from pyxis.app.chromium_research_session_reentry import (
    ChromiumResearchComparisonNoteReentryLocator,
    ChromiumResearchExactRangeNoteReentryLocator,
    ChromiumResearchParagraphNoteReentryLocator,
    ChromiumResearchSessionReentryResult,
    ChromiumResearchWorkingSetMemberReentryLocator,
)
from pyxis.app.chromium_research_working_set import ChromiumPageResearchWorkingSetItem

from .chromium_research_first_changed_basis_root_backed_reentry_textual import (
    ResearchFirstChangedBasisRootBackedReentryControls,
)
from .first_changed_basis_session_adoption_research_session_shell import (
    FirstChangedBasisSessionAdoptionResearchSessionShell,
)


class FirstChangedBasisRootBackedReentryResearchSessionShell(
    FirstChangedBasisSessionAdoptionResearchSessionShell
):
    """Concrete 44A→44F surface through explicit 35B fresh re-entry verification.

    44F proves restartability for the exact historical 44E adopted session. The fresh
    reconstructed controller is retained only as proof evidence; it never replaces
    the shell's currently mounted controller and no 35C overlay is written.
    """

    CSS = FirstChangedBasisSessionAdoptionResearchSessionShell.CSS + """
    #research-first-changed-basis-root-backed-reentry-controls {
        width: 94%;
        height: auto;
        padding: 1 2;
        margin-top: 1;
        border: round $warning;
    }

    #research-first-changed-basis-root-backed-reentry-authority-notice,
    #research-first-changed-basis-root-backed-reentry-summary,
    #research-first-changed-basis-root-backed-reentry-status,
    .research-first-changed-basis-reentry-member-summary,
    .research-first-changed-basis-reentry-input {
        margin-top: 1;
    }

    #research-first-changed-basis-root-backed-reentry-title {
        text-style: bold;
    }

    #verify-research-first-changed-basis-root-backed-reentry {
        margin-top: 1;
    }
    """

    def __init__(
        self,
        ordinary_reentry: ChromiumResearchSessionReentryResult,
        appended_items: Iterable[ChromiumPageResearchWorkingSetItem],
    ) -> None:
        super().__init__(ordinary_reentry, appended_items)
        self.last_first_changed_basis_root_backed_reentry_verification: (
            ChromiumResearchFirstChangedBasisRootBackedReentryResult | None
        ) = None

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "verify-research-first-changed-basis-root-backed-reentry":
            event.stop()
            self.call_after_refresh(
                self._verify_research_first_changed_basis_root_backed_reentry
            )
            return
        super().on_button_pressed(event)

    async def _adopt_research_first_changed_basis_session(self) -> None:
        """Run inherited 44E, then mount 44F only after one new exact adoption."""

        prior = self.last_first_changed_basis_session_adoption
        await super()._adopt_research_first_changed_basis_session()
        adoption = self.last_first_changed_basis_session_adoption
        if adoption is None or adoption is prior:
            return
        prepared = self.last_changed_basis_preparation
        if prepared is None:
            raise ValueError("44F requires the exact retained successful 44A preparation.")
        if len(self.query("#research-first-changed-basis-root-backed-reentry-controls")) != 0:
            raise ValueError("Fresh root-backed re-entry verification controls are already mounted.")
        await self.mount(
            ResearchFirstChangedBasisRootBackedReentryControls(
                adoption,
                prepared.appended_items,
            )
        )

    async def _verify_research_first_changed_basis_root_backed_reentry(self) -> None:
        controls = self.query_one(
            "#research-first-changed-basis-root-backed-reentry-controls",
            ResearchFirstChangedBasisRootBackedReentryControls,
        )
        status = self.query_one(
            "#research-first-changed-basis-root-backed-reentry-status",
            Static,
        )
        adoption = self.last_first_changed_basis_session_adoption
        if adoption is None or controls.adoption_result is not adoption:
            status.update(
                "Re-entry verification failed: no exact successful 44E adoption owns this form."
            )
            return

        appended_locators = self._collect_44f_appended_locators(controls, status)
        if appended_locators is None:
            return

        general_ids = (
            ("changed-working-set-source", "explicit changed working-set path"),
            ("changed-note-source", "explicit changed working-set-note path"),
            ("transition-source", "explicit 33B transition path"),
            ("root-source", "explicit 34A root path"),
            ("first-edge-source", "explicit first post-root edge path"),
            ("declaration-source", "explicit root-backed declaration path"),
        )
        general: dict[str, Path] = {}
        for suffix, label in general_ids:
            widget = self.query_one(
                f"#research-first-changed-basis-reentry-{suffix}", Input
            )
            if not widget.value.strip():
                status.update(f"Re-entry verification failed: {label} is required.")
                return
            general[suffix] = Path(widget.value)

        mounted_controller = self.research_controller
        mounted_session = self.research_session
        try:
            result = verify_chromium_research_first_changed_basis_root_backed_reentry(
                adoption,
                self.initial_ordinary_reentry,
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
            raise ValueError("44F proof did not retain the exact 44E adoption.")
        if result.initial_ordinary_reentry is not self.initial_ordinary_reentry:
            raise ValueError("44F proof did not retain the exact initial ordinary re-entry.")
        if (
            self.research_controller is not mounted_controller
            or self.research_session is not mounted_session
        ):
            raise ValueError(
                "Mounted governed research session changed during 44F fresh reconstruction proof."
            )

        self.last_first_changed_basis_root_backed_reentry_verification = result
        controls.lock_after_success(result)

    def _collect_44f_appended_locators(
        self,
        controls: ResearchFirstChangedBasisRootBackedReentryControls,
        status: Static,
    ) -> tuple[ChromiumResearchWorkingSetMemberReentryLocator, ...] | None:
        locators: list[ChromiumResearchWorkingSetMemberReentryLocator] = []
        for index, item in enumerate(controls.appended_items):
            note = self.query_one(
                f"#research-first-changed-basis-reentry-member-{index}-note-source",
                Input,
            )
            if isinstance(item, ChromiumPageResearchLoadedParagraphTextSelectionComparisonNoteRecord):
                first = self.query_one(
                    f"#research-first-changed-basis-reentry-member-{index}-first-capture-source",
                    Input,
                )
                second = self.query_one(
                    f"#research-first-changed-basis-reentry-member-{index}-second-capture-source",
                    Input,
                )
                if not first.value.strip():
                    status.update(
                        f"Re-entry verification failed: appended member {index} first capture path is required."
                    )
                    return None
                if not second.value.strip():
                    status.update(
                        f"Re-entry verification failed: appended member {index} second capture path is required."
                    )
                    return None
                if not note.value.strip():
                    status.update(
                        f"Re-entry verification failed: appended member {index} note path is required."
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
                f"#research-first-changed-basis-reentry-member-{index}-capture-source",
                Input,
            )
            if not capture.value.strip():
                status.update(
                    f"Re-entry verification failed: appended member {index} capture path is required."
                )
                return None
            if not note.value.strip():
                status.update(
                    f"Re-entry verification failed: appended member {index} note path is required."
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
                raise TypeError("44F encountered an unsupported appended working-set item.")

        return tuple(locators)


def create_first_changed_basis_root_backed_reentry_research_session_shell(
    ordinary_reentry: ChromiumResearchSessionReentryResult,
    appended_items: Iterable[ChromiumPageResearchWorkingSetItem],
) -> FirstChangedBasisRootBackedReentryResearchSessionShell:
    """Create the concrete first-changed-basis product surface through 35B proof."""

    return FirstChangedBasisRootBackedReentryResearchSessionShell(
        ordinary_reentry,
        appended_items,
    )


__all__ = [
    "FirstChangedBasisRootBackedReentryResearchSessionShell",
    "create_first_changed_basis_root_backed_reentry_research_session_shell",
]
