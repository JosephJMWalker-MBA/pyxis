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
from pyxis.ui import WorkspaceDetail, create_workspace_shell


controller_module = importlib.import_module("pyxis.app.controller")
compiler_repository_module = importlib.import_module("pyxis.compiler.repository")


def _file_snapshot(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


@pytest.mark.asyncio
async def test_visible_export_refresh_restores_ready_for_exact_post_apply_run(
    tmp_path: Path,
    monkeypatch,
) -> None:
    source = tmp_path / "workspace"
    old_portable = tmp_path / "portable-before-apply"
    fresh_portable = tmp_path / "portable-after-apply"
    initial_text = "  hello   world  "
    apply_text = "explicit visible runtime input for apply and export verification"
    rationale = "Remove normalization before verifying the new portable state."
    spec = create_workspace_spec(
        "Text Lab",
        "Visible export refresh should restore READY only for post-Apply evidence.",
    )
    initial_run = build_and_run_workspace(spec, source, initial_text)
    initial_export = export_workspace(
        initial_run.build,
        source,
        old_portable,
        initial_text,
    )
    presentation = query_workspace_presentation(
        source,
        run=initial_run,
        export=initial_export,
    )
    controller = WorkspaceController(
        source,
        initial_run,
        export=initial_export,
    )
    old_portable_before = _file_snapshot(old_portable)
    shell = create_workspace_shell(presentation, controller=controller)

    async with shell.run_test(size=(120, 60)) as pilot:
        await pilot.pause()

        assert len(shell.query("#export-refresh-controls")) == 0
        assert shell.query_one("#export-evidence", Static).content == (
            "Export evidence: READY"
        )

        runtime_input = shell.query_one("#runtime-input", Input)
        runtime_input.value = apply_text

        preview_button = shell.query_one("#preview-remove-normalize-text", Button)
        preview_button.focus()
        await pilot.press("enter")
        await pilot.pause()

        rationale_input = shell.query_one("#architecture-rationale", Input)
        rationale_input.value = rationale
        apply_button = shell.query_one("#apply-remove-normalize-text", Button)
        apply_button.focus()
        await pilot.press("enter")
        await pilot.pause()

        post_apply_run = controller.current_run
        post_apply_presentation = shell.presentation
        source_after_apply = _file_snapshot(source)

        assert post_apply_run is not initial_run
        assert controller.current_export is None
        assert controller.pending_preview is None
        assert post_apply_presentation.export is None
        assert post_apply_presentation.canonical.capabilities == ("inspect_text",)
        assert shell.query_one("#export-evidence", Static).content == (
            "Export evidence: No READY evidence"
        )
        assert len(shell.query("#export-refresh-controls")) == 1
        assert shell.query_one("#export-destination", Input)
        assert shell.query_one("#refresh-export", Button)

        def fail_if_compiled(*args, **kwargs):
            raise AssertionError("Visible verified export refresh must not compile.")

        monkeypatch.setattr(
            compiler_repository_module,
            "compile_repository",
            fail_if_compiled,
        )

        real_refresh = controller_module.refresh_workspace_export
        refresh_inputs = []

        def tracked_refresh(workspace_root, run, destination_root, text):
            refresh_inputs.append((workspace_root, run, destination_root, text))
            return real_refresh(workspace_root, run, destination_root, text)

        monkeypatch.setattr(
            controller_module,
            "refresh_workspace_export",
            tracked_refresh,
        )

        shell.query_one("#export-destination", Input).value = str(fresh_portable)
        export_button = shell.query_one("#refresh-export", Button)
        export_button.focus()
        await pilot.press("enter")
        await pilot.pause()

        assert refresh_inputs == [
            (source.resolve(), post_apply_run, fresh_portable, apply_text)
        ]
        assert controller.current_run is post_apply_run
        assert controller.current_export is not None
        assert controller.current_export.verification.readiness == "READY"
        assert controller.pending_preview is None
        assert shell.presentation is shell.query_one(WorkspaceDetail).presentation
        assert shell.presentation.export is not None
        assert shell.presentation.export.readiness == "READY"
        assert shell.presentation.canonical.capabilities == ("inspect_text",)
        assert shell.query_one("#export-evidence", Static).content == (
            "Export evidence: READY"
        )
        assert "Readiness: READY" in str(
            shell.query_one("#export-verification", Static).content
        )
        assert str(fresh_portable.resolve()) in str(
            shell.query_one("#export-verification", Static).content
        )
        assert len(shell.query("#export-refresh-controls")) == 0
        assert _file_snapshot(source) == source_after_apply

    assert _file_snapshot(old_portable) == old_portable_before
    assert fresh_portable.is_dir()
    assert query_workspace_presentation(
        source,
        run=controller.current_run,
        export=controller.current_export,
    ) == shell.presentation


@pytest.mark.asyncio
async def test_visible_export_failure_leaves_current_evidence_and_controller_state_unchanged(
    tmp_path: Path,
    monkeypatch,
) -> None:
    source = tmp_path / "workspace"
    occupied = tmp_path / "occupied-export"
    occupied.mkdir()
    text = "verification text remains explicit"
    spec = create_workspace_spec(
        "Text Lab",
        "Failed visible export must not manufacture READY evidence.",
    )
    run = build_and_run_workspace(spec, source, text)
    presentation = query_workspace_presentation(source, run=run, export=None)
    controller = WorkspaceController(source, run)
    source_before = _file_snapshot(source)
    shell = create_workspace_shell(presentation, controller=controller)

    def fail_if_compiled(*args, **kwargs):
        raise AssertionError("Failed export refresh must not compile.")

    monkeypatch.setattr(
        compiler_repository_module,
        "compile_repository",
        fail_if_compiled,
    )

    async with shell.run_test(size=(120, 48)) as pilot:
        await pilot.pause()

        detail = shell.query_one(WorkspaceDetail)
        current_before = shell.presentation
        export_text_before = shell.query_one("#export-verification", Static).content

        assert controller.current_run is run
        assert controller.current_export is None
        assert len(shell.query("#export-refresh-controls")) == 1

        shell.query_one("#runtime-input", Input).value = text
        shell.query_one("#export-destination", Input).value = str(occupied)
        export_button = shell.query_one("#refresh-export", Button)
        export_button.focus()
        await pilot.press("enter")
        await pilot.pause()

        assert controller.current_run is run
        assert controller.current_export is None
        assert controller.pending_preview is None
        assert shell.presentation is current_before
        assert detail.presentation is current_before
        assert shell.query_one("#export-verification", Static).content == export_text_before
        assert shell.query_one("#export-evidence", Static).content == (
            "Export evidence: No READY evidence"
        )
        assert "Export destination already exists" in str(
            shell.query_one("#export-refresh-status", Static).content
        )
        assert len(shell.query("#export-refresh-controls")) == 1
        assert _file_snapshot(source) == source_before
        assert list(occupied.iterdir()) == []
