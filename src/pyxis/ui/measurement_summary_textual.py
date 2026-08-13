from __future__ import annotations

from textual.app import App, ComposeResult
from textual.containers import Vertical, VerticalScroll
from textual.widgets import Static

from pyxis.app.measurement_summary_presentation import (
    BuildAndRunMeasurementSummaryPresentation,
    MeasurementWorkContextSummaryPresentation,
)


def _format_paths(paths: tuple[object, ...]) -> str:
    return ", ".join(str(path) for path in paths) if paths else "—"


def _format_group(
    group: MeasurementWorkContextSummaryPresentation,
    index: int,
) -> str:
    work = group.build_work
    statuses = ", ".join(
        f"{entry.path}={entry.status}" for entry in work.generation_statuses
    ) or "—"
    return "\n".join(
        (
            f"Work context {index}",
            f"Sample count: {group.sample_count}",
            f"Minimum seconds: {group.minimum_seconds}",
            f"Maximum seconds: {group.maximum_seconds}",
            f"Median seconds: {group.median_seconds}",
            f"Mean seconds: {group.mean_seconds}",
            "Population standard deviation seconds: "
            f"{group.population_standard_deviation_seconds}",
            f"Generation statuses: {statuses}",
            f"Written paths: {_format_paths(work.written_paths)}",
            f"Reused paths: {_format_paths(work.reused_paths)}",
            f"Removed paths: {_format_paths(work.removed_paths)}",
        )
    )


class MeasurementSummaryDetail(VerticalScroll):
    """Read-only Textual renderer for one exact measurement presentation."""

    def __init__(self, presentation: BuildAndRunMeasurementSummaryPresentation) -> None:
        super().__init__(id="measurement-summary-detail")
        self.presentation = presentation

    def compose(self) -> ComposeResult:
        yield Static("Pyxis measurement summary", id="measurement-summary-title")
        for stage in self.presentation.stages:
            with Vertical(
                id=f"measurement-stage-{stage.stage}",
                classes="measurement-stage",
            ):
                yield Static(stage.stage, classes="measurement-stage-title", markup=False)
                for index, group in enumerate(stage.groups, start=1):
                    yield Static(
                        _format_group(group, index),
                        id=f"measurement-{stage.stage}-group-{index}",
                        classes="measurement-work-context",
                        markup=False,
                    )


class MeasurementSummaryShell(App[None]):
    """Textual shell with presentation authority only."""

    TITLE = "Pyxis"
    SUB_TITLE = "Measurement evidence"
    CSS = """
    #measurement-summary-detail { width: 94%; height: 1fr; padding: 1 2; }
    .measurement-stage { width: 100%; height: auto; margin-bottom: 1; border: round $primary; padding: 1 2; }
    .measurement-stage-title { text-style: bold; margin-bottom: 1; }
    .measurement-work-context { width: 100%; height: auto; margin-bottom: 1; }
    """

    def __init__(self, presentation: BuildAndRunMeasurementSummaryPresentation) -> None:
        super().__init__()
        self.presentation = presentation

    def compose(self) -> ComposeResult:
        yield MeasurementSummaryDetail(self.presentation)


def create_measurement_summary_shell(
    presentation: BuildAndRunMeasurementSummaryPresentation,
) -> MeasurementSummaryShell:
    """Create a read-only Textual shell from existing 11N evidence only."""

    return MeasurementSummaryShell(presentation)
