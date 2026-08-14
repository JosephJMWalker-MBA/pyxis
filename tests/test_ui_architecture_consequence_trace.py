import importlib
from pathlib import Path

import pytest
from textual.widgets import Button, Static

from pyxis.app import (
    WorkspaceController,
    build_and_run_workspace,
    export_workspace,
    query_workspace_presentation,
)
from pyxis.authoring import create_workspace_spec
from pyxis.ui import create_workspace_shell


compiler_repository_module = importlib.import_module("pyxis.compiler.repository")


def _file_snapshot(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


@pytest.mark.asyncio
async def test_split_lines_preview_shows_read_only_consequence_trace(
    tmp_path: Path,
    monkeypatch,
) -> None:
    source = tmp_path / "workspace"
    portable = tmp_path / "portable"
    text = "first line\nsecond line"
    spec = create_workspace_spec(
        "Text Lab",
        "Visible architecture consequence trace proof.",
    )
    run = build_and_run_workspace(spec, source, text)
    export = export_workspace(run.build, source, portable, text)
    presentation = query_workspace_presentation(
        source,
        run=run,
        export=export,
    )
    controller = WorkspaceController(source, run, export=export)
    source_before = _file_snapshot(source)
    portable_before = _file_snapshot(portable)

    def fail_if_compiled(*args, **kwargs):
        raise AssertionError("Visible consequence trace must not compile.")

    monkeypatch.setattr(
        compiler_repository_module,
        "compile_repository",
        fail_if_compiled,
    )

    shell = create_workspace_shell(
        presentation,
        controller=controller,
    )

    async with shell.run_test(size=(120, 52)) as pilot:
        await pilot.pause()

        trace = shell.query_one("#architecture-consequence-trace-evidence", Static)
        assert trace.content == "No pending architecture consequence trace."

        current_selectors = (
            "#canonical-evidence",
            "#rir-evidence",
            "#compiler-artifacts",
            "#runtime-result",
            "#revision-timeline",
            "#export-verification",
        )
        current_before = {
            selector: shell.query_one(selector, Static).content
            for selector in current_selectors
        }

        button = shell.query_one("#preview-add-split-lines", Button)
        button.focus()
        await pilot.press("enter")
        await pilot.pause()

        trace_text = str(trace.content)
        expected_fragments = (
            "PROPOSED CONSEQUENCE TRACE — NOT APPLIED",
            "Requested architecture change\n→ add capability: split_lines",
            "Proposed canonical state\n→ add capability: split_lines",
            "Proposed RIR\n→ add capability: split_lines",
            "Compiler products\n→ add artifact: generated/capabilities/split_lines.py",
            "→ change artifact: generated/workspaces/text_lab/main.py",
            "Runtime contract\n→ add runtime key: split_lines",
        )
        for fragment in expected_fragments:
            assert fragment in trace_text

        assert controller.current_run is run
        assert controller.current_export is export
        assert {
            selector: shell.query_one(selector, Static).content
            for selector in current_selectors
        } == current_before

    assert _file_snapshot(source) == source_before
    assert _file_snapshot(portable) == portable_before
