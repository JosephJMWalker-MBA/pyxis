from __future__ import annotations

from textual.app import ComposeResult
from textual.widgets import Button, Input, Static

from pyxis.app.controller import WorkspaceController
from pyxis.app.measurement_summary_presentation import (
    BuildAndRunMeasurementSummaryPresentation,
)
from pyxis.app.presentation import WorkspacePresentation

from .measurement_summary_textual import MeasurementSummaryDetail, MeasurementSummaryShell
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

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Expire the transient removal notice on the next runtime operation."""

        if (
            event.input.id == "runtime-input"
            and len(self.query("#measurement-snapshot-notice")) != 0
        ):
            self.call_after_refresh(self._clear_measurement_notice)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Observe Apply provenance and expire any prior transient notice."""

        if len(self.query("#measurement-snapshot-notice")) != 0:
            self.call_after_refresh(self._clear_measurement_notice)

        if event.button.id == "apply-remove-normalize-text":
            self.call_after_refresh(self._remove_incoherent_measurement)

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
