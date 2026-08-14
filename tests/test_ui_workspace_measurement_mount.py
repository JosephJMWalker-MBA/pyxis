import importlib
from pathlib import Path

import pytest
from textual.widgets import Button, Input, Static

from pyxis.app import WorkspaceController, build_and_run_workspace, create_workspace_presentation
from pyxis.app.measurement_dispersion import create_build_and_run_measurement_population_standard_deviation
from pyxis.app.measurement_summary import create_build_and_run_measurement_descriptive_summary
from pyxis.app.measurement_summary_presentation import create_build_and_run_measurement_summary_presentation
from pyxis.authoring import create_workspace_spec
from pyxis.ui import MeasurementSummaryDetail, create_workspace_shell
from test_app_measurement_mean import _chain


measurement_module = importlib.import_module("pyxis.app.measurement")
presentation_module = importlib.import_module("pyxis.app.measurement_summary_presentation")


def _measurement_presentation(tmp_path: Path):
    median, mean = _chain(tmp_path)
    summary = create_build_and_run_measurement_descriptive_summary(
        median.envelope,
        median,
        mean,
        create_build_and_run_measurement_population_standard_deviation(mean),
    )
    return create_build_and_run_measurement_summary_presentation(summary)


@pytest.mark.asyncio
async def test_workspace_shell_mounts_supplied_measurement_without_refresh(
    tmp_path: Path,
    monkeypatch,
) -> None:
    measurement = _measurement_presentation(tmp_path)
    root = tmp_path / "workspace"
    spec = create_workspace_spec("Text Lab", "Mean stays attached to median evidence.")
    run = build_and_run_workspace(spec, root, "same workload")
    workspace = create_workspace_presentation(spec, run)
    controller = WorkspaceController(root, run)

    def fail_if_measurement_work(*args, **kwargs):
        raise AssertionError("Workspace shell must not acquire or re-project measurement evidence.")

    monkeypatch.setattr(measurement_module, "measure_build_and_run_workspace", fail_if_measurement_work)
    monkeypatch.setattr(
        presentation_module,
        "create_build_and_run_measurement_summary_presentation",
        fail_if_measurement_work,
    )

    shell = create_workspace_shell(
        workspace,
        controller=controller,
        measurement_presentation=measurement,
    )
    assert shell.measurement_presentation is measurement

    async with shell.run_test(size=(120, 50)) as pilot:
        await pilot.pause()
        detail = shell.query_one(MeasurementSummaryDetail)
        assert detail.presentation is measurement
        assert {button.id for button in shell.query(Button)} == {
            "preview-remove-normalize-text",
            "preview-add-split-lines",
            "refresh-export",
        }
        assert {widget.id for widget in shell.query(Input)} == {
            "runtime-input",
            "export-destination",
        }
        assert "Sample count: 4" in str(
            shell.query_one("#measurement-build-group-2", Static).content
        )

        runtime_input = shell.query_one("#runtime-input", Input)
        runtime_input.value = "a different runtime input"
        runtime_input.focus()
        await pilot.pause()
        await pilot.press("enter")
        await pilot.pause()

        assert shell.presentation is not workspace
        assert shell.measurement_presentation is measurement
        assert detail.presentation is measurement


@pytest.mark.asyncio
async def test_workspace_shell_omits_measurement_when_none_is_supplied(tmp_path: Path) -> None:
    spec = create_workspace_spec("Plain Workspace", "Existing shell path stays unchanged.")
    run = build_and_run_workspace(spec, tmp_path / "plain", "hello")
    shell = create_workspace_shell(create_workspace_presentation(spec, run))

    async with shell.run_test(size=(100, 30)) as pilot:
        await pilot.pause()
        assert len(shell.query(MeasurementSummaryDetail)) == 0
