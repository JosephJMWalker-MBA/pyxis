import importlib
from pathlib import Path

import pytest
from textual.widgets import Button, Input, Static

from pyxis.app import WorkspaceController, build_and_run_workspace, create_workspace_presentation
from pyxis.authoring import create_workspace_spec
from pyxis.ui import ArchitecturePreviewDetail, MeasurementSummaryDetail, create_workspace_shell
from pyxis.ui.workspace_shell import MEASUREMENT_SNAPSHOT_REMOVED_NOTICE
from test_ui_workspace_measurement_mount import _measurement_presentation


measurement_module = importlib.import_module("pyxis.app.measurement")
presentation_module = importlib.import_module("pyxis.app.measurement_summary_presentation")


def _block_measurement_work(monkeypatch) -> None:
    def fail_if_measurement_work(*args, **kwargs):
        raise AssertionError(
            "The split_lines UI path must not acquire or re-project measurement evidence."
        )

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
async def test_visible_split_lines_preview_apply_and_measurement_invalidation(
    tmp_path: Path,
    monkeypatch,
) -> None:
    measurement = _measurement_presentation(tmp_path / "measurement")
    root = tmp_path / "workspace"
    text = "one visible line"
    spec = create_workspace_spec(
        "Text Lab",
        "Mean stays attached to median evidence.",
    )
    run = build_and_run_workspace(spec, root, text)
    workspace = create_workspace_presentation(spec, run)
    controller = WorkspaceController(root, run)
    _block_measurement_work(monkeypatch)

    shell = create_workspace_shell(
        workspace,
        controller=controller,
        measurement_presentation=measurement,
    )
    old_rir_sha256 = workspace.rir.rir_sha256

    async with shell.run_test(size=(120, 64)) as pilot:
        await pilot.pause()
        assert shell.measurement_presentation is measurement
        assert len(shell.query(MeasurementSummaryDetail)) == 1

        preview_button = shell.query_one("#preview-add-split-lines", Button)
        preview_button.focus()
        await pilot.press("enter")
        await pilot.pause()

        preview_detail = shell.query_one(ArchitecturePreviewDetail)
        assert preview_detail.presentation is not None
        preview = preview_detail.presentation
        assert preview.added_capabilities == ("split_lines",)
        assert preview.removed_capabilities == ()
        assert preview.added_artifact_paths == (
            "generated/capabilities/split_lines.py",
        )
        assert preview.added_runtime_keys == ("split_lines",)
        assert preview.removed_runtime_keys == ()
        assert shell.presentation is workspace
        assert shell.measurement_presentation is measurement
        assert len(shell.query(MeasurementSummaryDetail)) == 1
        assert shell.query_one("#split-lines-rationale", Input)
        assert shell.query_one("#apply-add-split-lines", Button)

        shell.query_one("#runtime-input", Input).value = text
        shell.query_one("#split-lines-rationale", Input).value = (
            "Add a second concrete architecture operation before generalizing edits."
        )
        apply_button = shell.query_one("#apply-add-split-lines", Button)
        apply_button.focus()
        await pilot.press("enter")
        await pilot.pause()

        assert controller.pending_preview is None
        assert controller.current_export is None
        assert shell.presentation.rir.rir_sha256 != old_rir_sha256
        assert shell.presentation.canonical.capabilities == (
            "inspect_text",
            "normalize_text",
            "split_lines",
        )
        split_result = shell.presentation.runtime_result["split_lines"]
        assert split_result["line_count"] == 1
        assert tuple(split_result["lines"]) == (text,)
        assert len(shell.presentation.revisions) == 1
        assert shell.presentation.revisions[0].operation == "add_capability:split_lines"
        assert shell.presentation.revisions[0].completed is True
        assert preview_detail.presentation is None

        assert shell.measurement_presentation is None
        assert len(shell.query(MeasurementSummaryDetail)) == 0
        notice = shell.query_one("#measurement-snapshot-notice", Static)
        assert str(notice.content) == MEASUREMENT_SNAPSHOT_REMOVED_NOTICE
        assert len(notice.query(Button)) == 0
        assert len(notice.query(Input)) == 0

        assert shell.query_one("#export-destination", Input)
        assert shell.query_one("#refresh-export", Button)
