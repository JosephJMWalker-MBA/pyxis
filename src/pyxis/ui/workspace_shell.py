from __future__ import annotations

from textual.app import ComposeResult

from pyxis.app.controller import WorkspaceController
from pyxis.app.measurement_summary_presentation import (
    BuildAndRunMeasurementSummaryPresentation,
)
from pyxis.app.presentation import WorkspacePresentation

from .measurement_summary_textual import MeasurementSummaryDetail, MeasurementSummaryShell
from .textual_shell import WorkspaceShell as _WorkspaceShell


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
        super().__init__(presentation, controller=controller)
        self.measurement_presentation = measurement_presentation

    def compose(self) -> ComposeResult:
        yield from super().compose()
        if self.measurement_presentation is not None:
            yield MeasurementSummaryDetail(self.measurement_presentation)


def create_workspace_shell(
    presentation: WorkspacePresentation,
    *,
    controller: WorkspaceController | None = None,
    measurement_presentation: BuildAndRunMeasurementSummaryPresentation | None = None,
) -> WorkspaceShell:
    """Create the normal shell and optionally mount existing measurement evidence."""

    return WorkspaceShell(
        presentation,
        controller=controller,
        measurement_presentation=measurement_presentation,
    )
