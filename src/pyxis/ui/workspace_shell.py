from __future__ import annotations

from textual.app import ComposeResult
from textual.widgets import Button

from pyxis.app.controller import WorkspaceController
from pyxis.app.measurement_summary_presentation import (
    BuildAndRunMeasurementSummaryPresentation,
)
from pyxis.app.presentation import WorkspacePresentation

from .measurement_summary_textual import MeasurementSummaryDetail, MeasurementSummaryShell
from .textual_shell import WorkspaceShell as _WorkspaceShell


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

    CSS = _WorkspaceShell.CSS + "\n" + MeasurementSummaryShell.CSS

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

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Preserve co-display only while the supplied measurement still matches."""

        await super().on_button_pressed(event)

        if _measurement_provenance_matches(
            self.presentation,
            self.measurement_presentation,
        ):
            return

        self.measurement_presentation = None
        await self.query_one(MeasurementSummaryDetail).remove()


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
