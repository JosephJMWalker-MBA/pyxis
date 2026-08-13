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


def _live_evidence(tmp_path: Path):
    measurement = _measurement_presentation(tmp_path)
    subject = measurement.source.envelope.partition.condition.subject
    root = tmp_path / "workspace"
    spec = create_workspace_spec("Text Lab", "Mean stays attached to median evidence.")
    run = build_and_run_workspace(spec, root, "same workload")
    workspace = create_workspace_presentation(spec, run)
    controller = WorkspaceController(root, run)
    return measurement, subject, workspace, controller


def _block_measurement_work(monkeypatch) -> None:
    def fail_if_measurement_work(*args, **kwargs):
        raise AssertionError("Live Workspace actions must not acquire or re-project measurement evidence.")

    monkeypatch.setattr(measurement_module, "measure_build_and_run_workspace", fail_if_measurement_work)
    monkeypatch.setattr(
        presentation_module,
        "create_build_and_run_measurement_summary_presentation",
        fail_if_measurement_work,
    )


@pytest.mark.asyncio
async def test_same_rir_and_failed_actions_keep_measurement_snapshot(
    tmp_path: Path,
    monkeypatch,
) -> None:
    measurement, subject, workspace, controller = _live_evidence(tmp_path)
    _block_measurement_work(monkeypatch)
    shell = create_workspace_shell(
        workspace,
        controller=controller,
        measurement_presentation=measurement,
    )

    async with shell.run_test(size=(120, 60)) as pilot:
        await pilot.pause()
        detail = shell.query_one(MeasurementSummaryDetail)
        assert detail.presentation is measurement

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
        assert len(shell.query("#measurement-snapshot-notice")) == 0


@pytest.mark.asyncio
async def test_successful_apply_replaces_measurement_with_transient_non_evidence_notice(
    tmp_path: Path,
    monkeypatch,
) -> None:
    measurement, subject, workspace, controller = _live_evidence(tmp_path)
    _block_measurement_work(monkeypatch)
    shell = create_workspace_shell(
        workspace,
        controller=controller,
        measurement_presentation=measurement,
    )

    async with shell.run_test(size=(120, 60)) as pilot:
        await pilot.pause()
        preview_button = shell.query_one("#preview-remove-normalize-text", Button)
        preview_button.focus()
        await pilot.press("enter")
        await pilot.pause()

        shell.query_one("#architecture-rationale", Input).value = (
            "Remove normalization and advance to a new architecture state."
        )
        apply_button = shell.query_one("#apply-remove-normalize-text", Button)
        apply_button.focus()
        await pilot.pause()
        await pilot.press("enter")
        await pilot.pause()

        assert controller.pending_preview is None
        assert shell.presentation.rir.rir_sha256 != subject.rir_sha256
        assert shell.measurement_presentation is None
        assert len(shell.query(MeasurementSummaryDetail)) == 0

        notice = shell.query_one("#measurement-snapshot-notice", Static)
        assert MEASUREMENT_SNAPSHOT_REMOVED_NOTICE.startswith("Notice — not evidence:")
        for forbidden in (
            "sample count",
            "minimum seconds",
            "maximum seconds",
            "median seconds",
            "mean seconds",
            "standard deviation",
        ):
            assert forbidden not in MEASUREMENT_SNAPSHOT_REMOVED_NOTICE.lower()
        assert not hasattr(notice, "presentation")
        assert len(notice.query(Button)) == 0
        assert len(notice.query(Input)) == 0

        runtime_input = shell.query_one("#runtime-input", Input)
        runtime_input.value = "next operation clears the notice"
        runtime_input.focus()
        await pilot.press("enter")
        await pilot.pause()

        assert len(shell.query("#measurement-snapshot-notice")) == 0
        assert shell.measurement_presentation is None
        assert len(shell.query(MeasurementSummaryDetail)) == 0
