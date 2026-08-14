from __future__ import annotations

from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Input, Static

from pyxis.app.controller import WorkspaceController
from pyxis.app.measurement_summary_presentation import (
    BuildAndRunMeasurementSummaryPresentation,
)
from pyxis.app.presentation import WorkspacePresentation

from .architecture_consequence_trace_textual import ArchitectureConsequenceTraceDetail
from .measurement_summary_textual import MeasurementSummaryDetail, MeasurementSummaryShell
from .textual_shell import (
    ArchitectureApplyControls,
    ArchitecturePreviewDetail,
    ExportRefreshControls,
    WorkspaceDetail,
)
from .textual_shell import WorkspaceShell as _WorkspaceShell


MEASUREMENT_SNAPSHOT_REMOVED_NOTICE = (
    "Notice — not evidence: the prior measurement snapshot was removed because "
    "it described the previous RIR and does not describe the current Workspace."
)


def _measurement_provenance_matches(
    presentation: WorkspacePresentation,
    measurement_presentation: BuildAndRunMeasurementSummaryPresentation | None,
) -> bool:
    if measurement_presentation is None:
        return True

    subject = measurement_presentation.source.envelope.partition.condition.subject
    rir = presentation.rir
    return (
        subject.repository_id == rir.repository_id
        and subject.workspace_id == rir.workspace_id
        and subject.rir_sha256 == rir.rir_sha256
    )


def _require_measurement_provenance_coherence(
    presentation: WorkspacePresentation,
    measurement_presentation: BuildAndRunMeasurementSummaryPresentation | None,
) -> None:
    if measurement_presentation is None:
        return

    subject = measurement_presentation.source.envelope.partition.condition.subject
    rir = presentation.rir

    if subject.repository_id != rir.repository_id:
        raise ValueError(
            "Measurement presentation Repository ID does not match the Workspace presentation."
        )
    if subject.workspace_id != rir.workspace_id:
        raise ValueError(
            "Measurement presentation Workspace ID does not match the Workspace presentation."
        )
    if subject.rir_sha256 != rir.rir_sha256:
        raise ValueError(
            "Measurement presentation RIR SHA-256 does not match the Workspace presentation."
        )


class SplitLinesApplyControls(Vertical):
    """Concrete rationale/apply controls for the second architecture operation."""

    def __init__(self) -> None:
        super().__init__(id="split-lines-apply-controls")

    def compose(self) -> ComposeResult:
        yield Static(
            "Rationale required before Apply",
            id="split-lines-rationale-label",
        )
        yield Input(
            placeholder="Explain why split_lines should be added",
            id="split-lines-rationale",
        )
        yield Button(
            "Apply addition of split_lines",
            id="apply-add-split-lines",
            variant="warning",
        )
        yield Static(
            "",
            id="split-lines-apply-status",
            markup=False,
        )


class WorkspaceShell(_WorkspaceShell):
    """Normal Workspace shell with one optional supplied measurement snapshot."""

    CSS = (
        _WorkspaceShell.CSS
        + "\n"
        + MeasurementSummaryShell.CSS
        + """
    #measurement-snapshot-notice {
        width: 94%;
        height: auto;
        padding: 1 2;
        margin-top: 1;
        border: round $secondary;
    }

    #split-lines-apply-controls,
    #architecture-consequence-trace {
        width: 100%;
        height: auto;
        margin-top: 1;
    }

    #split-lines-rationale-label,
    #architecture-consequence-trace-title {
        text-style: bold;
        margin-bottom: 1;
    }

    #split-lines-apply-status {
        margin-top: 1;
    }
    """
    )

    def __init__(
        self,
        presentation: WorkspacePresentation,
        *,
        controller: WorkspaceController | None = None,
        measurement_presentation: BuildAndRunMeasurementSummaryPresentation | None = None,
    ) -> None:
        _require_measurement_provenance_coherence(
            presentation,
            measurement_presentation,
        )
        super().__init__(presentation, controller=controller)
        self.measurement_presentation = measurement_presentation

    def compose(self) -> ComposeResult:
        yield from super().compose()
        if self.measurement_presentation is not None:
            yield MeasurementSummaryDetail(self.measurement_presentation)

    async def on_mount(self) -> None:
        """Expose the second concrete architecture preview and read-only trace."""

        if self.controller is None:
            return
        container = self.query_one("#architecture-preview-interaction", Vertical)
        await container.mount(
            Button(
                "Preview addition of split_lines",
                id="preview-add-split-lines",
            )
        )
        preview_detail = self.query_one(ArchitecturePreviewDetail)
        await preview_detail.mount(ArchitectureConsequenceTraceDetail())

    async def supply_measurement_presentation(
        self,
        measurement_presentation: BuildAndRunMeasurementSummaryPresentation,
    ) -> None:
        """Mount one already-produced coherent measurement snapshot.

        The caller remains responsible for producing the measurement presentation.
        This boundary only checks provenance against current Workspace evidence and
        mounts the supplied read-only presentation when no snapshot is currently
        present. It performs no measurement acquisition, re-projection, or refresh.
        """

        _require_measurement_provenance_coherence(
            self.presentation,
            measurement_presentation,
        )
        if self.measurement_presentation is not None:
            raise ValueError("A measurement presentation is already mounted.")

        detail = MeasurementSummaryDetail(measurement_presentation)
        await self.mount(detail)
        self.measurement_presentation = measurement_presentation
        await self._clear_measurement_notice()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Expire the transient removal notice on the next runtime operation."""

        if (
            event.input.id == "runtime-input"
            and len(self.query("#measurement-snapshot-notice")) != 0
        ):
            self.call_after_refresh(self._clear_measurement_notice)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Observe architecture actions and transient measurement status."""

        if len(self.query("#measurement-snapshot-notice")) != 0:
            self.call_after_refresh(self._clear_measurement_notice)

        if event.button.id == "preview-add-split-lines":
            self.call_after_refresh(self._preview_add_split_lines)
            return

        if event.button.id == "preview-remove-normalize-text":
            self.call_after_refresh(self._clear_split_lines_apply_controls)
            self.call_after_refresh(self._sync_consequence_trace)
            return

        if event.button.id == "apply-add-split-lines":
            self.call_after_refresh(self._apply_add_split_lines)
            return

        if event.button.id == "apply-remove-normalize-text":
            self.call_after_refresh(self._clear_consequence_trace)
            self.call_after_refresh(self._remove_incoherent_measurement)

    async def _preview_add_split_lines(self) -> None:
        if self.controller is None:
            return

        presentation = self.controller.preview_add_split_lines()
        self.query_one(ArchitecturePreviewDetail).replace_presentation(presentation)
        self.query_one(ArchitectureConsequenceTraceDetail).replace_presentation(
            presentation
        )

        if len(self.query("#architecture-apply-controls")) != 0:
            await self.query_one(
                "#architecture-apply-controls",
                ArchitectureApplyControls,
            ).remove()
        if len(self.query("#split-lines-apply-controls")) != 0:
            await self.query_one(
                "#split-lines-apply-controls",
                SplitLinesApplyControls,
            ).remove()

        container = self.query_one("#architecture-preview-interaction", Vertical)
        await container.mount(SplitLinesApplyControls())

    async def _sync_consequence_trace(self) -> None:
        preview_detail = self.query_one(ArchitecturePreviewDetail)
        trace_detail = self.query_one(ArchitectureConsequenceTraceDetail)
        if preview_detail.presentation is None:
            trace_detail.clear_presentation()
            return
        trace_detail.replace_presentation(preview_detail.presentation)

    async def _clear_consequence_trace(self) -> None:
        self.query_one(ArchitectureConsequenceTraceDetail).clear_presentation()

    async def _clear_split_lines_apply_controls(self) -> None:
        if len(self.query("#split-lines-apply-controls")) == 0:
            return
        await self.query_one(
            "#split-lines-apply-controls",
            SplitLinesApplyControls,
        ).remove()

    async def _apply_add_split_lines(self) -> None:
        if self.controller is None:
            return

        rationale_input = self.query_one("#split-lines-rationale", Input)
        runtime_input = self.query_one("#runtime-input", Input)
        status = self.query_one("#split-lines-apply-status", Static)

        try:
            presentation = self.controller.apply_pending_add_split_lines(
                rationale_input.value,
                runtime_input.value,
            )
        except Exception as exc:
            status.update(f"Apply failed: {exc}")
            return

        self.presentation = presentation
        self.query_one(WorkspaceDetail).replace_presentation(presentation)
        self.query_one(ArchitecturePreviewDetail).clear_presentation()
        await self._clear_consequence_trace()
        await self.query_one(
            "#split-lines-apply-controls",
            SplitLinesApplyControls,
        ).remove()

        if len(self.query("#export-refresh-controls")) == 0:
            slot = self.query_one("#export-refresh-slot", Vertical)
            await slot.mount(ExportRefreshControls())

        await self._remove_incoherent_measurement()

    async def _remove_incoherent_measurement(self) -> None:
        if _measurement_provenance_matches(
            self.presentation,
            self.measurement_presentation,
        ):
            return

        self.measurement_presentation = None
        await self.query_one(MeasurementSummaryDetail).remove()
        await self.mount(
            Static(
                MEASUREMENT_SNAPSHOT_REMOVED_NOTICE,
                id="measurement-snapshot-notice",
                markup=False,
            )
        )

    async def _clear_measurement_notice(self) -> None:
        if len(self.query("#measurement-snapshot-notice")) == 0:
            return
        await self.query_one("#measurement-snapshot-notice", Static).remove()


def create_workspace_shell(
    presentation: WorkspacePresentation,
    *,
    controller: WorkspaceController | None = None,
    measurement_presentation: BuildAndRunMeasurementSummaryPresentation | None = None,
) -> WorkspaceShell:
    """Create the normal shell and optionally mount coherent measurement evidence."""

    return WorkspaceShell(
        presentation,
        controller=controller,
        measurement_presentation=measurement_presentation,
    )
