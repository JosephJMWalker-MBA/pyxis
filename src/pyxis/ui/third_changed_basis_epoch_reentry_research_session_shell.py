from __future__ import annotations

from pathlib import Path

from textual.widgets import Button, Input, Static

from pyxis.app.chromium_research_paragraph_text_selection_comparison_note_load import (
    ChromiumPageResearchLoadedParagraphTextSelectionComparisonNoteRecord,
)
from pyxis.app.chromium_research_paragraph_text_selection_note_load import (
    ChromiumPageResearchLoadedParagraphTextSelectionNoteRecord,
)
from pyxis.app.chromium_research_second_basis_epoch_continuation_reentry_plan_document import (
    ChromiumResearchSecondBasisEpochContinuationReentryResult,
)
from pyxis.app.chromium_research_second_basis_epoch_shell_lineage import (
    ChromiumResearchSecondBasisEpochContinuationShellLineage,
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
from pyxis.app.chromium_research_third_changed_basis_epoch_reentry import (
    ChromiumResearchThirdChangedBasisEpochReentryResult,
    verify_chromium_research_third_changed_basis_epoch_reentry,
)
from pyxis.app.chromium_research_third_changed_basis_session_adoption import (
    ChromiumResearchThirdChangedBasisSessionAdoptionResult,
)

from .chromium_research_third_changed_basis_epoch_reentry_textual import (
    ResearchThirdChangedBasisEpochReentryControls,
)
from .third_changed_basis_session_adoption_research_session_shell import (
    InspectableThirdChangedBasisSessionAdoptionHandoffResearchSessionShell,
    InspectableThirdChangedBasisSessionAdoptionResearchSessionShell,
    ThirdChangedBasisSessionAdoptionHandoffResearchSessionShell,
    ThirdChangedBasisSessionAdoptionResearchSessionShell,
)


_THIRD_CHANGED_BASIS_EPOCH_REENTRY_CSS = """
#research-third-changed-basis-epoch-reentry-controls {
    width: 94%;
    height: auto;
    padding: 1 2;
    margin-top: 1;
    border: round $warning;
}

#research-third-changed-basis-epoch-reentry-authority-notice,
#research-third-changed-basis-epoch-reentry-summary,
#research-third-changed-basis-epoch-reentry-status,
.research-third-changed-basis-epoch-reentry-member-summary,
.research-third-changed-basis-epoch-reentry-input {
    margin-top: 1;
}

#research-third-changed-basis-epoch-reentry-title {
    text-style: bold;
}

#verify-research-third-changed-basis-epoch-reentry {
    margin-top: 1;
}
"""


class _ThirdChangedBasisEpochReentryProductMixin:
    """47E-only behavior shared by the four dedicated 47D launch products."""

    last_third_changed_basis_epoch_reentry_verification: (
        ChromiumResearchThirdChangedBasisEpochReentryResult | None
    )

    def __init__(self, authority) -> None:
        super().__init__(authority)
        self.last_third_changed_basis_epoch_reentry_verification = None

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Own only the 47E action; inherited handlers remain MRO-dispatched."""

        if event.button.id == "verify-research-third-changed-basis-epoch-reentry":
            event.stop()
            self.call_after_refresh(self._verify_third_changed_basis_epoch_reentry)

    async def _promote_third_changed_basis_session_adoption(
        self,
        result: ChromiumResearchThirdChangedBasisSessionAdoptionResult,
    ) -> None:
        """Run inherited 47D promotion, then mount 47E for that exact history target."""

        prior = self.last_third_changed_basis_session_adoption
        await super()._promote_third_changed_basis_session_adoption(result)
        adoption = self.last_third_changed_basis_session_adoption
        if adoption is None or adoption is prior:
            return
        if adoption is not result:
            raise ValueError("47E promotion did not retain the exact successful 47D adoption.")
        appended_items = (
            adoption.edge_result.root_result.transition_result.prepared.appended_items
        )
        if len(self.query("#research-third-changed-basis-epoch-reentry-controls")) != 0:
            raise ValueError(
                "Third-basis fresh re-entry verification controls are already mounted."
            )
        await self.mount(
            ResearchThirdChangedBasisEpochReentryControls(adoption, appended_items)
        )

    async def _verify_third_changed_basis_epoch_reentry(self) -> None:
        controls = self.query_one(
            "#research-third-changed-basis-epoch-reentry-controls",
            ResearchThirdChangedBasisEpochReentryControls,
        )
        status = self.query_one(
            "#research-third-changed-basis-epoch-reentry-status",
            Static,
        )
        adoption = self.last_third_changed_basis_session_adoption
        if adoption is None or controls.adoption_result is not adoption:
            status.update(
                "Re-entry verification failed: no exact successful 47D adoption owns this form."
            )
            return

        appended_locators = self._collect_47e_appended_locators(controls, status)
        if appended_locators is None:
            return

        prior_overlay = self.query_one(
            "#research-third-changed-basis-epoch-reentry-prior-continuation-overlay-source",
            Input,
        )
        if not prior_overlay.value.strip():
            status.update(
                "Re-entry verification failed: explicit prior 37C/37D second-epoch continuation overlay path is required."
            )
            return

        general_ids = (
            ("changed-working-set-source", "explicit changed working-set path"),
            ("changed-note-source", "explicit changed working-set-note path"),
            ("transition-source", "explicit third 33B transition path"),
            ("root-source", "explicit third 34A root path"),
            ("first-edge-source", "explicit first post-third-root edge path"),
            ("declaration-source", "explicit third-root-backed declaration path"),
        )
        general: dict[str, Path] = {}
        for suffix, label in general_ids:
            widget = self.query_one(
                f"#research-third-changed-basis-epoch-reentry-{suffix}", Input
            )
            if not widget.value.strip():
                status.update(f"Re-entry verification failed: {label} is required.")
                return
            general[suffix] = Path(widget.value)

        mounted_controller = self.research_controller
        mounted_session = self.research_session
        mounted_reentry = self.research_reentry
        historical_continuation = self.second_basis_epoch_continuation_reentry
        try:
            result = verify_chromium_research_third_changed_basis_epoch_reentry(
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
            raise ValueError("47E proof did not retain the exact 47D adoption.")
        if (
            self.research_controller is not mounted_controller
            or self.research_session is not mounted_session
            or self.research_reentry is not mounted_reentry
            or self.second_basis_epoch_continuation_reentry is not historical_continuation
        ):
            raise ValueError(
                "Mounted governed state or retained prior second-epoch continuation changed during 47E fresh reconstruction proof."
            )

        self.last_third_changed_basis_epoch_reentry_verification = result
        controls.lock_after_success(result)

    def _collect_47e_appended_locators(
        self,
        controls: ResearchThirdChangedBasisEpochReentryControls,
        status: Static,
    ) -> tuple[ChromiumResearchWorkingSetMemberReentryLocator, ...] | None:
        locators: list[ChromiumResearchWorkingSetMemberReentryLocator] = []
        for index, item in enumerate(controls.appended_items):
            note = self.query_one(
                f"#research-third-changed-basis-epoch-reentry-member-{index}-note-source",
                Input,
            )
            if isinstance(
                item,
                ChromiumPageResearchLoadedParagraphTextSelectionComparisonNoteRecord,
            ):
                first = self.query_one(
                    f"#research-third-changed-basis-epoch-reentry-member-{index}-first-capture-source",
                    Input,
                )
                second = self.query_one(
                    f"#research-third-changed-basis-epoch-reentry-member-{index}-second-capture-source",
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
                f"#research-third-changed-basis-epoch-reentry-member-{index}-capture-source",
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
            elif isinstance(
                item,
                ChromiumPageResearchLoadedParagraphTextSelectionNoteRecord,
            ):
                locators.append(
                    ChromiumResearchExactRangeNoteReentryLocator(
                        capture_source=Path(capture.value),
                        note_source=Path(note.value),
                    )
                )
            else:
                raise TypeError("47E encountered an unsupported appended working-set item.")
        return tuple(locators)


class ThirdChangedBasisEpochReentryResearchSessionShell(
    _ThirdChangedBasisEpochReentryProductMixin,
    ThirdChangedBasisSessionAdoptionResearchSessionShell,
):
    """47E proof product from a persisted second-epoch continuation launch."""

    CSS = (
        ThirdChangedBasisSessionAdoptionResearchSessionShell.CSS
        + _THIRD_CHANGED_BASIS_EPOCH_REENTRY_CSS
    )


class ThirdChangedBasisEpochReentryHandoffResearchSessionShell(
    _ThirdChangedBasisEpochReentryProductMixin,
    ThirdChangedBasisSessionAdoptionHandoffResearchSessionShell,
):
    """47E proof product from an exact pathless 38F second-epoch handoff."""

    CSS = (
        ThirdChangedBasisSessionAdoptionHandoffResearchSessionShell.CSS
        + _THIRD_CHANGED_BASIS_EPOCH_REENTRY_CSS
    )


class InspectableThirdChangedBasisEpochReentryResearchSessionShell(
    _ThirdChangedBasisEpochReentryProductMixin,
    InspectableThirdChangedBasisSessionAdoptionResearchSessionShell,
):
    """Inspectable persisted-launch 47E product preserving inspection authority."""

    CSS = (
        InspectableThirdChangedBasisSessionAdoptionResearchSessionShell.CSS
        + _THIRD_CHANGED_BASIS_EPOCH_REENTRY_CSS
    )

    async def _verify_third_changed_basis_epoch_reentry(self) -> None:
        panel = self.second_basis_epoch_authority_inspection
        launch = panel.launch_provenance
        current = panel.current_state
        await super()._verify_third_changed_basis_epoch_reentry()
        if panel.launch_provenance is not launch or panel.current_state is not current:
            raise ValueError(
                "47E verification must not mutate persisted second-epoch launch provenance or current inspection state."
            )


class InspectableThirdChangedBasisEpochReentryHandoffResearchSessionShell(
    _ThirdChangedBasisEpochReentryProductMixin,
    InspectableThirdChangedBasisSessionAdoptionHandoffResearchSessionShell,
):
    """Inspectable pathless 47E product preserving raw 38F inspection authority."""

    CSS = (
        InspectableThirdChangedBasisSessionAdoptionHandoffResearchSessionShell.CSS
        + _THIRD_CHANGED_BASIS_EPOCH_REENTRY_CSS
    )

    async def _verify_third_changed_basis_epoch_reentry(self) -> None:
        panel = self.second_basis_epoch_authority_inspection
        launch = panel.launch_provenance
        current = panel.current_state
        if launch.launch_location_context is not None:
            raise ValueError("Raw 38F launch provenance must remain pathless before 47E proof.")
        await super()._verify_third_changed_basis_epoch_reentry()
        if panel.launch_provenance is not launch or panel.current_state is not current:
            raise ValueError(
                "47E verification must not mutate raw 38F launch provenance or current inspection state."
            )
        if panel.launch_provenance.launch_location_context is not None:
            raise ValueError("47E proof must not backfill a path into raw 38F launch provenance.")


def create_third_changed_basis_epoch_reentry_research_session_shell(
    lineage: ChromiumResearchSecondBasisEpochContinuationShellLineage,
) -> ThirdChangedBasisEpochReentryResearchSessionShell:
    if not isinstance(lineage, ChromiumResearchSecondBasisEpochContinuationShellLineage):
        raise TypeError(
            "lineage must be ChromiumResearchSecondBasisEpochContinuationShellLineage."
        )
    return ThirdChangedBasisEpochReentryResearchSessionShell(lineage)


def create_third_changed_basis_epoch_reentry_handoff_research_session_shell(
    reentry: ChromiumResearchSecondBasisEpochContinuationReentryResult,
) -> ThirdChangedBasisEpochReentryHandoffResearchSessionShell:
    if type(reentry) is not ChromiumResearchSecondBasisEpochContinuationReentryResult:
        raise TypeError(
            "reentry must be exactly ChromiumResearchSecondBasisEpochContinuationReentryResult."
        )
    return ThirdChangedBasisEpochReentryHandoffResearchSessionShell(reentry)


def create_inspectable_third_changed_basis_epoch_reentry_research_session_shell(
    lineage: ChromiumResearchSecondBasisEpochContinuationShellLineage,
) -> InspectableThirdChangedBasisEpochReentryResearchSessionShell:
    if not isinstance(lineage, ChromiumResearchSecondBasisEpochContinuationShellLineage):
        raise TypeError(
            "lineage must be ChromiumResearchSecondBasisEpochContinuationShellLineage."
        )
    return InspectableThirdChangedBasisEpochReentryResearchSessionShell(lineage)


def create_inspectable_third_changed_basis_epoch_reentry_handoff_research_session_shell(
    reentry: ChromiumResearchSecondBasisEpochContinuationReentryResult,
) -> InspectableThirdChangedBasisEpochReentryHandoffResearchSessionShell:
    if type(reentry) is not ChromiumResearchSecondBasisEpochContinuationReentryResult:
        raise TypeError(
            "reentry must be exactly ChromiumResearchSecondBasisEpochContinuationReentryResult."
        )
    return InspectableThirdChangedBasisEpochReentryHandoffResearchSessionShell(reentry)


__all__ = [
    "InspectableThirdChangedBasisEpochReentryHandoffResearchSessionShell",
    "InspectableThirdChangedBasisEpochReentryResearchSessionShell",
    "ThirdChangedBasisEpochReentryHandoffResearchSessionShell",
    "ThirdChangedBasisEpochReentryResearchSessionShell",
    "create_inspectable_third_changed_basis_epoch_reentry_handoff_research_session_shell",
    "create_inspectable_third_changed_basis_epoch_reentry_research_session_shell",
    "create_third_changed_basis_epoch_reentry_handoff_research_session_shell",
    "create_third_changed_basis_epoch_reentry_research_session_shell",
]
