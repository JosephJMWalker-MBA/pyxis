import importlib
from pathlib import Path

import pytest
from textual.widgets import Button, Input, Static

from pyxis.app import (
    WorkspaceController,
    build_and_run_workspace,
    export_workspace,
    query_workspace_presentation,
)
from pyxis.authoring import create_workspace_spec
from pyxis.ui import ArchitecturePreviewDetail, WorkspaceDetail, create_workspace_shell


controller_module = importlib.import_module("pyxis.app.controller")
compiler_repository_module = importlib.import_module("pyxis.compiler.repository")


def _file_snapshot(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


@pytest.mark.asyncio
async def test_textual_runtime_then_preview_share_one_live_workspace_controller(
    tmp_path: Path,
    monkeypatch,
) -> None:
    source = tmp_path / "workspace"
    portable = tmp_path / "portable"
    initial_text = "  hello   world  "
    submitted_text = "fresh runtime text before preview"
    spec = create_workspace_spec(
        "Text Lab",
        "Textual runtime and Preview must share one live Workspace authority.",
    )
    initial_run = build_and_run_workspace(spec, source, initial_text)
    export = export_workspace(initial_run.build, source, portable, initial_text)
    presentation = query_workspace_presentation(
        source,
        run=initial_run,
        export=export,
    )
    controller = WorkspaceController(source, initial_run, export=export)
    source_before = _file_snapshot(source)
    portable_before = _file_snapshot(portable)

    def fail_if_compiled(*args, **kwargs):
        raise AssertionError("10K runtime/Preview UI sequence must not compile.")

    monkeypatch.setattr(
        compiler_repository_module,
        "compile_repository",
        fail_if_compiled,
    )

    real_rerun = controller_module.rerun_workspace
    real_preview = controller_module.preview_workspace_remove_normalize_text
    rerun_inputs = []
    preview_inputs = []

    def tracked_rerun(workspace_root, run, text, *, export=None):
        rerun_inputs.append((workspace_root, run, text, export))
        return real_rerun(workspace_root, run, text, export=export)

    def tracked_preview(workspace_root, run, *, export=None):
        preview_inputs.append((workspace_root, run, export))
        return real_preview(workspace_root, run, export=export)

    monkeypatch.setattr(controller_module, "rerun_workspace", tracked_rerun)
    monkeypatch.setattr(
        controller_module,
        "preview_workspace_remove_normalize_text",
        tracked_preview,
    )

    shell = create_workspace_shell(presentation, controller=controller)

    async with shell.run_test(size=(120, 48)) as pilot:
        await pilot.pause()

        assert len(shell.query(Input)) == 1
        assert len(shell.query(Button)) == 1
        assert len(shell.query("#architecture-rationale")) == 0
        assert len(shell.query("#apply-remove-normalize-text")) == 0

        runtime_input = shell.query_one("#runtime-input", Input)
        preview_button = shell.query_one("#preview-remove-normalize-text", Button)
        detail = shell.query_one(WorkspaceDetail)
        preview_detail = shell.query_one(ArchitecturePreviewDetail)

        assert detail.presentation is presentation
        assert preview_detail.presentation is None
        assert controller.current_run is initial_run
        assert controller.current_export is export
        assert controller.pending_preview is None

        runtime_input.value = submitted_text
        runtime_input.focus()
        await pilot.pause()
        await pilot.press("enter")
        await pilot.pause()

        run_after_rerun = controller.current_run
        presentation_after_rerun = shell.presentation
        runtime_after_rerun = shell.query_one("#runtime-result", Static).content
        export_after_rerun = shell.query_one("#export-verification", Static).content

        assert rerun_inputs == [
            (source.resolve(), initial_run, submitted_text, export)
        ]
        assert run_after_rerun is not initial_run
        assert run_after_rerun.build is initial_run.build
        assert controller.current_export is export
        assert controller.pending_preview is None
        assert detail.presentation is presentation_after_rerun
        assert presentation_after_rerun.export is not None
        assert "Readiness: READY" in str(export_after_rerun)

        preview_button.focus()
        await pilot.pause()
        await pilot.press("enter")
        await pilot.pause()

        assert preview_inputs == [
            (source.resolve(), run_after_rerun, export)
        ]
        assert controller.current_run is run_after_rerun
        assert controller.current_export is export
        assert controller.pending_preview is not None
        assert shell.presentation is presentation_after_rerun
        assert detail.presentation is presentation_after_rerun
        assert shell.query_one("#runtime-result", Static).content == runtime_after_rerun
        assert shell.query_one("#export-verification", Static).content == export_after_rerun
        assert shell.query_one("#export-evidence", Static).content == (
            "Export evidence: READY"
        )

        preview_text = shell.query_one(
            "#architecture-preview-evidence",
            Static,
        ).content
        assert "PROPOSED — NOT APPLIED" in str(preview_text)
        assert "Removed capabilities:\n- normalize_text" in str(preview_text)
        assert preview_detail.presentation is not None

        assert len(shell.query(Input)) == 1
        assert len(shell.query(Button)) == 1
        assert len(shell.query("#architecture-rationale")) == 0
        assert len(shell.query("#apply-remove-normalize-text")) == 0

    assert _file_snapshot(source) == source_before
    assert _file_snapshot(portable) == portable_before
