import importlib
from pathlib import Path

import pytest
from textual.widgets import Button, Input

from pyxis.app import WorkspaceController, build_and_run_workspace, create_workspace_presentation
from pyxis.authoring import create_workspace_spec
from pyxis.ui import MeasurementSummaryDetail, create_workspace_shell
from test_ui_workspace_measurement_mount import _measurement_presentation


measurement_module = importlib.import_module("pyxis.app.measurement")
presentation_module = importlib.import_module("pyxis.app.measurement_summary_presentation")


@pytest.mark.asyncio
async def test_live_workspace_actions_keep_measurement_until_successful_rir_change(
    tmp_path: Path,
    monkeypatch,
) -> None:
    measurement = _measurement_presentation(tmp_path)
    subject = measurement.source.envelope.partition.condition.subject
    root = tmp_path / "workspace"
    spec = create_workspace_spec("Text Lab", "Mean stays attached to median evidence.")
    run = build_and_run_workspace(spec, root, "same workload")
    workspace = create_workspace_presentation(spec, run)
    controller = WorkspaceController(root, run)

    def fail_if_measurement_work(*args, **kwargs):
        raise AssertionError("Live Workspace actions must not acquire or re-project measurement evidence.")

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

    async with shell.run_test(size=(120, 60)) as pilot:
        await pilot.pause()
        detail = shell.query_one(MeasurementSummaryDetail)
        assert detail.presentation is measurement
        assert shell.presentation.rir.rir_sha256 == subject.rir_sha256

        runtime_input = shell.query_one("#runtime-input", Input)
        runtime_input.value = "different runtime input"
        runtime_input.focus()
        await pilot.press("enter")
        await pilot.pause()

        assert shell.measurement_presentation is measurement
        assert detail.presentation is measurement
        assert shell.presentation.rir.rir_sha256 == subject.rir_sha256

        shell.query_one("#export-destination", Input).value = str(tmp_path / "portable")
        export_button = shell.query_one("#refresh-export", Button)
        export_button.focus()
        await pilot.press("enter")
        await pilot.pause()

        assert controller.current_export is not None
        assert shell.measurement_presentation is measurement
        assert detail.presentation is measurement
        assert shell.presentation.rir.rir_sha256 == subject.rir_sha256

        preview_button = shell.query_one("#preview-remove-normalize-text", Button)
        preview_button.focus()
        await pilot.press("enter")
        await pilot.pause()

        assert shell.measurement_presentation is measurement
        assert len(shell.query(MeasurementSummaryDetail)) == 1

        apply_button = shell.query_one("#apply-remove-normalize-text", Button)
        apply_button.focus()
        await pilot.press("enter")
        await pilot.pause()

        assert controller.pending_preview is not None
        assert shell.measurement_presentation is measurement
        assert len(shell.query(MeasurementSummaryDetail)) == 1
        assert shell.presentation.rir.rir_sha256 == subject.rir_sha256

        shell.query_one("#architecture-rationale", Input).value = (
            "Remove normalization and advance to a new architecture state."
        )
        apply_button.focus()
        await pilot.press("enter")
        await pilot.pause()

        assert controller.pending_preview is None
        assert shell.presentation.rir.rir_sha256 != subject.rir_sha256
        assert shell.measurement_presentation is None
        assert len(shell.query(MeasurementSummaryDetail)) == 0
