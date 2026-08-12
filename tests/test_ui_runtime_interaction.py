import importlib
import json
from pathlib import Path

import pytest
from textual.widgets import Button, Input, Static

from pyxis.app import (
    BuildAndRunResult,
    WorkspaceController,
    apply_remove_normalize_text,
    build_and_run_workspace,
    export_workspace,
    preview_remove_normalize_text,
    query_workspace_presentation,
)
from pyxis.authoring import create_workspace_spec
from pyxis.runtime import run_materialized_workspace
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
async def test_single_runtime_input_reruns_through_unified_workspace_controller(
    tmp_path: Path,
    monkeypatch,
) -> None:
    source = tmp_path / "workspace"
    portable = tmp_path / "portable"
    initial_text = "  hello   world  "
    submitted_text = "three new words"
    spec = create_workspace_spec(
        "Text Lab",
        "Single Textual runtime interaction proof.",
    )
    build_and_run_workspace(spec, source, initial_text)
    preview = preview_remove_normalize_text(spec)
    applied = apply_remove_normalize_text(
        preview,
        source,
        "Keep revision evidence visible while proving runtime-only UI interaction.",
    )
    runtime_result = run_materialized_workspace(
        applied.build.repository,
        source,
        initial_text,
    )
    run = BuildAndRunResult(
        build=applied.build,
        runtime_result=runtime_result,
    )
    export = export_workspace(applied.build, source, portable, initial_text)
    presentation = query_workspace_presentation(
        source,
        run=run,
        export=export,
    )
    controller = WorkspaceController(
        source,
        run,
        export=export,
    )
    source_before = _file_snapshot(source)
    portable_before = _file_snapshot(portable)

    def fail_if_compiled(*args, **kwargs):
        raise AssertionError("Runtime UI interaction must not compile.")

    monkeypatch.setattr(
        compiler_repository_module,
        "compile_repository",
        fail_if_compiled,
    )

    real_rerun = controller_module.rerun_workspace
    rerun_calls = 0

    def counted_rerun(*args, **kwargs):
        nonlocal rerun_calls
        rerun_calls += 1
        return real_rerun(*args, **kwargs)

    monkeypatch.setattr(controller_module, "rerun_workspace", counted_rerun)

    shell = create_workspace_shell(
        presentation,
        controller=controller,
    )

    async with shell.run_test(size=(120, 40)) as pilot:
        await pilot.pause()

        assert len(shell.query(Input)) == 1
        assert len(shell.query(Button)) == 1
        assert shell.query_one("#preview-remove-normalize-text", Button)
        runtime_input = shell.query_one("#runtime-input", Input)
        detail = shell.query_one(WorkspaceDetail)
        assert detail.presentation is presentation

        stable_selectors = (
            "#canonical-evidence",
            "#rir-evidence",
            "#compiler-artifacts",
            "#revision-timeline",
            "#export-verification",
        )
        stable_before = {
            selector: shell.query_one(selector, Static).content
            for selector in stable_selectors
        }
        runtime_before = shell.query_one("#runtime-result", Static).content

        runtime_input.value = submitted_text
        runtime_input.focus()
        await pilot.pause()
        await pilot.press("enter")
        await pilot.pause()

        assert rerun_calls == 1
        assert controller.current_run.build is run.build
        assert controller.current_run.runtime_result != runtime_result
        assert controller.current_export is export
        assert controller.pending_preview is None
        assert shell.presentation.runtime_result == controller.current_run.runtime_result
        assert detail.presentation is shell.presentation
        assert shell.query_one("#runtime-result", Static).content == json.dumps(
            controller.current_run.runtime_result,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        assert shell.query_one("#runtime-result", Static).content != runtime_before

        stable_after = {
            selector: shell.query_one(selector, Static).content
            for selector in stable_selectors
        }
        assert stable_after == stable_before
        assert len(shell.query(Input)) == 1
        assert len(shell.query(Button)) == 1

    assert _file_snapshot(source) == source_before
    assert _file_snapshot(portable) == portable_before
