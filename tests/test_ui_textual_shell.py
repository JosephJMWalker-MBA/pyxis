import importlib
from pathlib import Path

import pytest
from textual.widgets import Static

from pyxis.app import (
    build_and_run_workspace,
    create_workspace_presentation,
    export_workspace,
)
from pyxis.authoring import create_workspace_spec
from pyxis.ui import create_workspace_shell


app_query_module = importlib.import_module("pyxis.app.query")
compiler_repository_module = importlib.import_module("pyxis.compiler.repository")
runtime_loader_module = importlib.import_module("pyxis.runtime.loader")


def _file_snapshot(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


@pytest.mark.asyncio
async def test_textual_shell_renders_existing_presentation_without_app_work(
    tmp_path: Path,
    monkeypatch,
) -> None:
    source = tmp_path / "workspace"
    portable = tmp_path / "portable"
    text = "  hello   world  "
    spec = create_workspace_spec(
        "Text Lab",
        "Textual boot shell consumes presentation evidence only.",
    )
    run = build_and_run_workspace(spec, source, text)
    export = export_workspace(run.build, source, portable, text)
    presentation = create_workspace_presentation(spec, run, export=export)
    source_before = _file_snapshot(source)
    portable_before = _file_snapshot(portable)

    def fail_if_application_work(*args, **kwargs):
        raise AssertionError("Textual shell must not acquire or produce application evidence.")

    monkeypatch.setattr(
        app_query_module,
        "query_workspace_presentation",
        fail_if_application_work,
    )
    monkeypatch.setattr(
        compiler_repository_module,
        "compile_repository",
        fail_if_application_work,
    )
    monkeypatch.setattr(
        runtime_loader_module,
        "run_materialized_workspace",
        fail_if_application_work,
    )

    shell = create_workspace_shell(presentation)
    assert shell.presentation is presentation

    async with shell.run_test(size=(100, 30)) as pilot:
        await pilot.pause()
        assert shell.query_one("#workspace-name", Static).content == spec.name
        assert (
            shell.query_one("#workspace-description", Static).content
            == spec.description
        )
        assert shell.query_one("#repository-identity", Static).content == (
            f"Repository: {presentation.rir.repository_id}"
        )
        assert shell.query_one("#compiler-evidence", Static).content == (
            f"Compiler evidence: {len(presentation.artifacts)} artifacts"
        )
        assert shell.query_one("#revision-evidence", Static).content == (
            f"Revision evidence: {len(presentation.revisions)} events"
        )
        assert shell.query_one("#export-evidence", Static).content == (
            "Export evidence: READY"
        )

    assert _file_snapshot(source) == source_before
    assert _file_snapshot(portable) == portable_before


@pytest.mark.asyncio
async def test_textual_shell_does_not_invent_export_readiness(tmp_path: Path) -> None:
    root = tmp_path / "workspace"
    spec = create_workspace_spec(
        "Text Lab",
        "Absent export evidence remains absent in the renderer.",
    )
    run = build_and_run_workspace(spec, root, "hello world")
    presentation = create_workspace_presentation(spec, run)
    shell = create_workspace_shell(presentation)

    async with shell.run_test(size=(100, 30)) as pilot:
        await pilot.pause()
        export_text = shell.query_one("#export-evidence", Static).content
        assert export_text == "Export evidence: No READY evidence"
        assert "NOT READY" not in str(export_text)
