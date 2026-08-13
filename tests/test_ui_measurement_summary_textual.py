import importlib
from math import sqrt
from pathlib import Path

import pytest
from textual.widgets import Button, Input, Static

from pyxis.app.measurement_dispersion import (
    create_build_and_run_measurement_population_standard_deviation,
)
from pyxis.app.measurement_summary import create_build_and_run_measurement_descriptive_summary
from pyxis.app.measurement_summary_presentation import (
    create_build_and_run_measurement_summary_presentation,
)
from pyxis.ui import MeasurementSummaryDetail, create_measurement_summary_shell
from test_app_measurement_mean import _chain


measurement_module = importlib.import_module("pyxis.app.measurement")
compiler_module = importlib.import_module("pyxis.compiler.repository")
runtime_module = importlib.import_module("pyxis.runtime.loader")
presentation_module = importlib.import_module("pyxis.app.measurement_summary_presentation")


def _snapshot(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


@pytest.mark.asyncio
async def test_measurement_summary_textual_renders_existing_evidence_only(
    tmp_path: Path,
    monkeypatch,
) -> None:
    median, mean = _chain(tmp_path)
    envelope = median.envelope
    summary = create_build_and_run_measurement_descriptive_summary(
        envelope,
        median,
        mean,
        create_build_and_run_measurement_population_standard_deviation(mean),
    )
    presentation = create_build_and_run_measurement_summary_presentation(summary)
    workspace = tmp_path / "workspace"
    before = _snapshot(workspace)

    def fail_if_application_work(*args, **kwargs):
        raise AssertionError("Measurement Textual renderer must consume presentation only.")

    monkeypatch.setattr(measurement_module, "measure_build_and_run_workspace", fail_if_application_work)
    monkeypatch.setattr(compiler_module, "compile_repository", fail_if_application_work)
    monkeypatch.setattr(runtime_module, "run_materialized_workspace", fail_if_application_work)
    monkeypatch.setattr(
        presentation_module,
        "create_build_and_run_measurement_summary_presentation",
        fail_if_application_work,
    )

    shell = create_measurement_summary_shell(presentation)
    assert shell.presentation is presentation

    async with shell.run_test(size=(120, 40)) as pilot:
        await pilot.pause()
        detail = shell.query_one(MeasurementSummaryDetail)
        assert detail.presentation is presentation
        assert len(shell.query(Button)) == 0
        assert len(shell.query(Input)) == 0
        assert shell.query_one("#measurement-stage-build")
        assert shell.query_one("#measurement-stage-runtime")

        reused = str(shell.query_one("#measurement-build-group-2", Static).content)
        assert "Sample count: 4" in reused
        assert "Minimum seconds: 0.5" in reused
        assert "Maximum seconds: 1.5" in reused
        assert "Median seconds: 0.875" in reused
        assert "Mean seconds: 0.9375" in reused
        assert f"Population standard deviation seconds: {sqrt(0.13671875)}" in reused
        assert "=reused" in reused

    assert _snapshot(workspace) == before
