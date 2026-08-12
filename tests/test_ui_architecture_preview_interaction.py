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


compiler_repository_module = importlib.import_module("pyxis.compiler.repository")


def _file_snapshot(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


@pytest.mark.asyncio
async def test_single_visible_architecture_preview_changes_only_proposed_display(
    tmp_path: Path,
    monkeypatch,
) -> None:
    source = tmp_path / "workspace"
    portable = tmp_path / "portable"
    text = "  hello   world  "
    spec = create_workspace_spec(
        "Text Lab",
        "Visible preview must remain distinct from current Workspace evidence.",
    )
    run = build_and_run_workspace(spec, source, text)
    export = export_workspace(run.build, source, portable, text)
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
        raise AssertionError("Visible architecture preview must not compile.")

    monkeypatch.setattr(
        compiler_repository_module,
        "compile_repository",
        fail_if_compiled,
    )

    real_preview = controller.preview_remove_normalize_text
    preview_calls = 0

    def counted_preview():
        nonlocal preview_calls
        preview_calls += 1
        return real_preview()

    monkeypatch.setattr(
        controller,
        "preview_remove_normalize_text",
        counted_preview,
    )

    shell = create_workspace_shell(
        presentation,
        controller=controller,
    )

    async with shell.run_test(size=(120, 46)) as pilot:
        await pilot.pause()

        assert len(shell.query(Button)) == 1
        assert len(shell.query(Input)) == 1
        assert len(shell.query("#architecture-rationale")) == 0
        assert len(shell.query("#apply-remove-normalize-text")) == 0
        assert shell.query_one("#runtime-input", Input)
        button = shell.query_one("#preview-remove-normalize-text", Button)
        detail = shell.query_one(WorkspaceDetail)
        preview_detail = shell.query_one(ArchitecturePreviewDetail)
        assert detail.presentation is presentation
        assert preview_detail.presentation is None
        assert shell.query_one(
            "#architecture-preview-evidence",
            Static,
        ).content == "No pending architecture preview."

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

        button.focus()
        await pilot.pause()
        await pilot.press("enter")
        await pilot.pause()

        assert preview_calls == 1
        assert controller.pending_preview is not None
        assert controller.current_run is run
        assert controller.current_export is export
        assert shell.presentation is presentation
        assert detail.presentation is presentation
        assert preview_detail.presentation is not None

        preview_text = shell.query_one(
            "#architecture-preview-evidence",
            Static,
        ).content
        assert "PROPOSED — NOT APPLIED" in str(preview_text)
        assert "Removed capabilities:\n- normalize_text" in str(preview_text)
        assert (
            "Removed compiler-product paths:\n"
            "- generated/capabilities/normalize_text.py"
        ) in str(preview_text)
        assert "Proposed runtime keys:\n- inspect_text" in str(preview_text)
        assert presentation.canonical.canonical_sha256 in str(preview_text)
        assert (
            preview_detail.presentation.proposed.canonical_sha256
            in str(preview_text)
        )

        current_after = {
            selector: shell.query_one(selector, Static).content
            for selector in current_selectors
        }
        assert current_after == current_before
        assert len(shell.query(Button)) == 2
        assert len(shell.query(Input)) == 2
        assert shell.query_one("#architecture-rationale", Input)
        assert shell.query_one("#apply-remove-normalize-text", Button)

    assert _file_snapshot(source) == source_before
    assert _file_snapshot(portable) == portable_before
