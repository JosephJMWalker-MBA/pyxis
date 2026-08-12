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


def _file_snapshot(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


@pytest.mark.asyncio
async def test_visible_apply_consumes_retained_preview_and_refreshes_current_evidence(
    tmp_path: Path,
    monkeypatch,
) -> None:
    source = tmp_path / "workspace"
    portable = tmp_path / "portable"
    initial_text = "  hello   world  "
    apply_text = "runtime text supplied explicitly at apply"
    rationale = "  Remove normalization because callers need original spacing.  "
    clean_rationale = rationale.strip()
    spec = create_workspace_spec(
        "Text Lab",
        "Visible Apply must consume retained intent and refresh current evidence.",
    )
    initial_run = build_and_run_workspace(spec, source, initial_text)
    export = export_workspace(initial_run.build, source, portable, initial_text)
    presentation = query_workspace_presentation(
        source,
        run=initial_run,
        export=export,
    )
    controller = WorkspaceController(source, initial_run, export=export)
    portable_before = _file_snapshot(portable)

    real_apply = controller_module.apply_workspace_remove_normalize_text
    apply_inputs = []

    def tracked_apply(
        workspace_root,
        preview,
        current_run,
        rationale_value,
        text,
        *,
        export=None,
    ):
        apply_inputs.append(
            (workspace_root, preview, current_run, rationale_value, text, export)
        )
        return real_apply(
            workspace_root,
            preview,
            current_run,
            rationale_value,
            text,
            export=export,
        )

    monkeypatch.setattr(
        controller_module,
        "apply_workspace_remove_normalize_text",
        tracked_apply,
    )

    shell = create_workspace_shell(presentation, controller=controller)

    async with shell.run_test(size=(120, 56)) as pilot:
        await pilot.pause()

        runtime_input = shell.query_one("#runtime-input", Input)
        preview_button = shell.query_one("#preview-remove-normalize-text", Button)
        detail = shell.query_one(WorkspaceDetail)
        preview_detail = shell.query_one(ArchitecturePreviewDetail)

        runtime_input.value = apply_text
        preview_button.focus()
        await pilot.pause()
        await pilot.press("enter")
        await pilot.pause()

        pending = controller.pending_preview
        assert pending is not None
        assert len(shell.query("#architecture-rationale")) == 1
        assert len(shell.query("#apply-remove-normalize-text")) == 1
        assert preview_detail.presentation is not None
        assert shell.presentation is presentation
        assert detail.presentation is presentation
        assert controller.current_export is export

        rationale_input = shell.query_one("#architecture-rationale", Input)
        apply_button = shell.query_one("#apply-remove-normalize-text", Button)
        rationale_input.value = rationale

        apply_button.focus()
        await pilot.pause()
        await pilot.press("enter")
        await pilot.pause()

        assert apply_inputs == [
            (
                source.resolve(),
                pending,
                initial_run,
                rationale,
                apply_text,
                export,
            )
        ]
        assert controller.current_run is not initial_run
        assert controller.current_run.build is not initial_run.build
        assert controller.current_export is None
        assert controller.pending_preview is None
        assert tuple(controller.current_run.runtime_result) == ("inspect_text",)

        assert shell.presentation is detail.presentation
        assert shell.presentation.canonical.capabilities == ("inspect_text",)
        assert shell.presentation.export is None
        assert shell.presentation.revisions[-1].rationale == clean_rationale
        assert shell.presentation.revisions[-1].completed is True

        removed = next(
            artifact
            for artifact in shell.presentation.artifacts
            if artifact.path == "generated/capabilities/normalize_text.py"
        )
        assert removed.status == "removed"
        assert removed.node_sha256 is None
        assert removed.artifact_sha256 is None

        assert preview_detail.presentation is None
        assert shell.query_one(
            "#architecture-preview-evidence",
            Static,
        ).content == "No pending architecture preview."
        assert len(shell.query("#architecture-rationale")) == 0
        assert len(shell.query("#apply-remove-normalize-text")) == 0
        assert shell.query_one("#export-evidence", Static).content == (
            "Export evidence: No READY evidence"
        )
        assert shell.query_one("#export-verification", Static).content == (
            "No READY evidence."
        )
        assert "Status: removed" in str(
            shell.query_one("#compiler-artifacts", Static).content
        )
        revision_text = str(shell.query_one("#revision-timeline", Static).content)
        assert f"Rationale: {clean_rationale}" in revision_text
        assert "Completed: yes" in revision_text

    assert _file_snapshot(portable) == portable_before
    assert not (source / "generated/capabilities/normalize_text.py").exists()
    assert query_workspace_presentation(
        source,
        run=controller.current_run,
        export=controller.current_export,
    ) == shell.presentation


@pytest.mark.asyncio
async def test_empty_visible_rationale_leaves_current_and_proposed_evidence_unchanged(
    tmp_path: Path,
) -> None:
    source = tmp_path / "workspace"
    portable = tmp_path / "portable"
    text = "hello world"
    spec = create_workspace_spec(
        "Text Lab",
        "Empty rationale must not advance visible or application state.",
    )
    run = build_and_run_workspace(spec, source, text)
    export = export_workspace(run.build, source, portable, text)
    presentation = query_workspace_presentation(source, run=run, export=export)
    controller = WorkspaceController(source, run, export=export)
    shell = create_workspace_shell(presentation, controller=controller)

    async with shell.run_test(size=(120, 54)) as pilot:
        await pilot.pause()
        preview_button = shell.query_one("#preview-remove-normalize-text", Button)
        preview_button.focus()
        await pilot.press("enter")
        await pilot.pause()

        detail = shell.query_one(WorkspaceDetail)
        preview_detail = shell.query_one(ArchitecturePreviewDetail)
        pending = controller.pending_preview
        proposed_presentation = preview_detail.presentation
        current_before = shell.presentation
        current_text_before = shell.query_one("#canonical-evidence", Static).content
        preview_text_before = shell.query_one(
            "#architecture-preview-evidence",
            Static,
        ).content
        source_before = _file_snapshot(source)
        portable_before = _file_snapshot(portable)

        assert pending is not None
        assert proposed_presentation is not None

        shell.query_one("#runtime-input", Input).value = "explicit apply runtime input"
        shell.query_one("#architecture-rationale", Input).value = "   "
        apply_button = shell.query_one("#apply-remove-normalize-text", Button)
        apply_button.focus()
        await pilot.press("enter")
        await pilot.pause()

        assert controller.current_run is run
        assert controller.current_export is export
        assert controller.pending_preview is pending
        assert shell.presentation is current_before
        assert detail.presentation is current_before
        assert preview_detail.presentation is proposed_presentation
        assert shell.query_one("#canonical-evidence", Static).content == current_text_before
        assert shell.query_one(
            "#architecture-preview-evidence",
            Static,
        ).content == preview_text_before
        assert "Architecture rationale is required before apply." in str(
            shell.query_one("#architecture-apply-status", Static).content
        )
        assert len(shell.query("#architecture-rationale")) == 1
        assert len(shell.query("#apply-remove-normalize-text")) == 1
        assert _file_snapshot(source) == source_before
        assert _file_snapshot(portable) == portable_before


@pytest.mark.asyncio
async def test_failed_visible_apply_leaves_current_and_proposed_evidence_unchanged(
    tmp_path: Path,
    monkeypatch,
) -> None:
    source = tmp_path / "workspace"
    portable = tmp_path / "portable"
    text = "hello world"
    spec = create_workspace_spec(
        "Text Lab",
        "Failed Apply must not partially advance Textual or controller state.",
    )
    run = build_and_run_workspace(spec, source, text)
    export = export_workspace(run.build, source, portable, text)
    presentation = query_workspace_presentation(source, run=run, export=export)
    controller = WorkspaceController(source, run, export=export)
    shell = create_workspace_shell(presentation, controller=controller)

    async with shell.run_test(size=(120, 54)) as pilot:
        await pilot.pause()
        preview_button = shell.query_one("#preview-remove-normalize-text", Button)
        preview_button.focus()
        await pilot.press("enter")
        await pilot.pause()

        detail = shell.query_one(WorkspaceDetail)
        preview_detail = shell.query_one(ArchitecturePreviewDetail)
        pending = controller.pending_preview
        proposed_presentation = preview_detail.presentation
        current_before = shell.presentation
        current_text_before = shell.query_one("#canonical-evidence", Static).content
        preview_text_before = shell.query_one(
            "#architecture-preview-evidence",
            Static,
        ).content
        source_before = _file_snapshot(source)
        portable_before = _file_snapshot(portable)

        def fail_apply(*args, **kwargs):
            raise RuntimeError("simulated visible governed apply failure")

        monkeypatch.setattr(
            controller_module,
            "apply_workspace_remove_normalize_text",
            fail_apply,
        )

        shell.query_one("#runtime-input", Input).value = "explicit apply runtime input"
        shell.query_one("#architecture-rationale", Input).value = (
            "A valid rationale whose governed operation will fail."
        )
        apply_button = shell.query_one("#apply-remove-normalize-text", Button)
        apply_button.focus()
        await pilot.press("enter")
        await pilot.pause()

        assert controller.current_run is run
        assert controller.current_export is export
        assert controller.pending_preview is pending
        assert shell.presentation is current_before
        assert detail.presentation is current_before
        assert preview_detail.presentation is proposed_presentation
        assert shell.query_one("#canonical-evidence", Static).content == current_text_before
        assert shell.query_one(
            "#architecture-preview-evidence",
            Static,
        ).content == preview_text_before
        assert "simulated visible governed apply failure" in str(
            shell.query_one("#architecture-apply-status", Static).content
        )
        assert len(shell.query("#architecture-rationale")) == 1
        assert len(shell.query("#apply-remove-normalize-text")) == 1
        assert _file_snapshot(source) == source_before
        assert _file_snapshot(portable) == portable_before
