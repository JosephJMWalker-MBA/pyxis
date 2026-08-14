import importlib
from pathlib import Path

import pytest
from textual.widgets import Button, Input, Static

from pyxis.app import WorkspaceController, build_and_run_workspace, create_workspace_presentation
from pyxis.authoring import create_workspace_spec
from pyxis.ui import MeasurementSummaryDetail, create_workspace_shell
from pyxis.ui.workspace_shell import MEASUREMENT_SNAPSHOT_REMOVED_NOTICE
from test_ui_workspace_measurement_mount import _measurement_presentation


measurement_module = importlib.import_module("pyxis.app.measurement")
presentation_module = importlib.import_module("pyxis.app.measurement_summary_presentation")


def _block_measurement_work(monkeypatch) -> None:
    def fail_if_measurement_work(*args, **kwargs):
        raise AssertionError("Measurement re-entry must not acquire or re-project evidence.")

    monkeypatch.setattr(
        measurement_module,
        "measure_build_and_run_workspace",
        fail_if_measurement_work,
    )
    monkeypatch.setattr(
        presentation_module,
        "create_build_and_run_measurement_summary_presentation",
        fail_if_measurement_work,
    )


@pytest.mark.asyncio
async def test_current_rir_measurement_can_reenter_without_measurement_work(
    tmp_path: Path,
    monkeypatch,
) -> None:
    measurement = _measurement_presentation(tmp_path / "measurement")
    root = tmp_path / "workspace"
    spec = create_workspace_spec("Text Lab", "Mean stays attached to median evidence.")
    run = build_and_run_workspace(spec, root, "same workload")
    workspace = create_workspace_presentation(spec, run)
    controller = WorkspaceController(root, run)
    _block_measurement_work(monkeypatch)

    shell = create_workspace_shell(workspace, controller=controller)

    async with shell.run_test(size=(120, 60)) as pilot:
        await pilot.pause()
        assert shell.measurement_presentation is None
        assert len(shell.query(MeasurementSummaryDetail)) == 0

        await shell.mount(
            Static(
                MEASUREMENT_SNAPSHOT_REMOVED_NOTICE,
                id="measurement-snapshot-notice",
                markup=False,
            )
        )
        assert len(shell.query("#measurement-snapshot-notice")) == 1

        await shell.supply_measurement_presentation(measurement)
        await pilot.pause()

        assert shell.measurement_presentation is measurement
        detail = shell.query_one(MeasurementSummaryDetail)
        assert detail.presentation is measurement
        assert len(shell.query("#measurement-snapshot-notice")) == 0
        assert {button.id for button in shell.query(Button)} == {
            "preview-remove-normalize-text",
            "refresh-export",
        }
        assert {widget.id for widget in shell.query(Input)} == {
            "runtime-input",
            "export-destination",
        }

        with pytest.raises(ValueError, match="already mounted"):
            await shell.supply_measurement_presentation(measurement)

        assert shell.measurement_presentation is measurement
        assert len(shell.query(MeasurementSummaryDetail)) == 1


@pytest.mark.asyncio
async def test_mismatched_measurement_reentry_fails_before_ui_mutation(
    tmp_path: Path,
    monkeypatch,
) -> None:
    measurement = _measurement_presentation(tmp_path / "measurement")
    root = tmp_path / "different-workspace"
    spec = create_workspace_spec("Different Workspace", "Different provenance.")
    run = build_and_run_workspace(spec, root, "same workload")
    workspace = create_workspace_presentation(spec, run)
    controller = WorkspaceController(root, run)
    _block_measurement_work(monkeypatch)

    shell = create_workspace_shell(workspace, controller=controller)

    async with shell.run_test(size=(120, 60)) as pilot:
        await pilot.pause()
        await shell.mount(
            Static(
                MEASUREMENT_SNAPSHOT_REMOVED_NOTICE,
                id="measurement-snapshot-notice",
                markup=False,
            )
        )

        with pytest.raises(ValueError, match="does not match"):
            await shell.supply_measurement_presentation(measurement)

        assert shell.measurement_presentation is None
        assert len(shell.query(MeasurementSummaryDetail)) == 0
        assert len(shell.query("#measurement-snapshot-notice")) == 1
