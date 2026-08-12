import importlib
from pathlib import Path

import pytest

from pyxis.app import (
    WorkspaceController,
    build_and_run_workspace,
    export_workspace,
    query_workspace_presentation,
)
from pyxis.authoring import create_workspace_spec


controller_module = importlib.import_module("pyxis.app.controller")


def test_workspace_controller_keeps_one_live_state_across_rerun_preview_apply_rerun(
    tmp_path: Path,
    monkeypatch,
) -> None:
    source = tmp_path / "workspace"
    portable = tmp_path / "portable"
    initial_text = "  initial   text  "
    spec = create_workspace_spec(
        "Text Lab",
        "One live controller state must cross runtime and architecture operations.",
    )
    initial_run = build_and_run_workspace(spec, source, initial_text)
    export = export_workspace(initial_run.build, source, portable, initial_text)
    controller = WorkspaceController(source, initial_run, export=export)

    real_rerun = controller_module.rerun_workspace
    real_preview = controller_module.preview_workspace_remove_normalize_text
    real_apply = controller_module.apply_workspace_remove_normalize_text
    rerun_inputs = []
    preview_inputs = []
    apply_inputs = []

    def tracked_rerun(workspace_root, run, text, *, export=None):
        rerun_inputs.append((workspace_root, run, text, export))
        return real_rerun(workspace_root, run, text, export=export)

    def tracked_preview(workspace_root, run, *, export=None):
        preview_inputs.append((workspace_root, run, export))
        return real_preview(workspace_root, run, export=export)

    def tracked_apply(
        workspace_root,
        preview,
        current_run,
        rationale,
        text,
        *,
        export=None,
    ):
        apply_inputs.append(
            (workspace_root, preview, current_run, rationale, text, export)
        )
        return real_apply(
            workspace_root,
            preview,
            current_run,
            rationale,
            text,
            export=export,
        )

    monkeypatch.setattr(controller_module, "rerun_workspace", tracked_rerun)
    monkeypatch.setattr(
        controller_module,
        "preview_workspace_remove_normalize_text",
        tracked_preview,
    )
    monkeypatch.setattr(
        controller_module,
        "apply_workspace_remove_normalize_text",
        tracked_apply,
    )

    first_presentation = controller.rerun("runtime before preview")
    run_after_first_rerun = controller.current_run

    assert run_after_first_rerun is not initial_run
    assert run_after_first_rerun.build is initial_run.build
    assert controller.current_export is export
    assert controller.pending_preview is None
    assert rerun_inputs == [
        (source.resolve(), initial_run, "runtime before preview", export)
    ]
    assert first_presentation.export is not None

    preview_presentation = controller.preview_remove_normalize_text()
    pending = controller.pending_preview

    assert pending is not None
    assert preview_inputs == [
        (source.resolve(), run_after_first_rerun, export)
    ]
    assert preview_presentation.proposed.capabilities == ("inspect_text",)
    assert controller.current_run is run_after_first_rerun
    assert controller.current_export is export

    applied_presentation = controller.apply_pending_remove_normalize_text(
        "Remove normalization through the one live Workspace authority.",
        "runtime immediately after apply",
    )
    run_after_apply = controller.current_run

    assert apply_inputs == [
        (
            source.resolve(),
            pending,
            run_after_first_rerun,
            "Remove normalization through the one live Workspace authority.",
            "runtime immediately after apply",
            export,
        )
    ]
    assert run_after_apply is not run_after_first_rerun
    assert run_after_apply.build is not run_after_first_rerun.build
    assert tuple(run_after_apply.runtime_result) == ("inspect_text",)
    assert controller.current_export is None
    assert controller.pending_preview is None
    assert applied_presentation.export is None
    assert applied_presentation.canonical.capabilities == ("inspect_text",)
    assert applied_presentation.revisions[-1].completed is True

    final_presentation = controller.rerun("runtime after architecture apply")
    run_after_final_rerun = controller.current_run

    assert len(rerun_inputs) == 2
    assert rerun_inputs[1] == (
        source.resolve(),
        run_after_apply,
        "runtime after architecture apply",
        None,
    )
    assert run_after_final_rerun is not run_after_apply
    assert run_after_final_rerun.build is run_after_apply.build
    assert tuple(run_after_final_rerun.runtime_result) == ("inspect_text",)
    assert controller.current_export is None
    assert controller.pending_preview is None
    assert final_presentation.export is None
    assert final_presentation.canonical.capabilities == ("inspect_text",)

    current = query_workspace_presentation(
        source,
        run=controller.current_run,
        export=controller.current_export,
    )
    assert current == final_presentation
    assert portable.is_dir()


def test_workspace_controller_failed_apply_does_not_advance_shared_state(
    tmp_path: Path,
    monkeypatch,
) -> None:
    source = tmp_path / "workspace"
    portable = tmp_path / "portable"
    text = "hello world"
    spec = create_workspace_spec(
        "Text Lab",
        "Shared live state advances only after successful application operations.",
    )
    run = build_and_run_workspace(spec, source, text)
    export = export_workspace(run.build, source, portable, text)
    controller = WorkspaceController(source, run, export=export)
    controller.preview_remove_normalize_text()
    pending = controller.pending_preview

    def fail_apply(*args, **kwargs):
        raise RuntimeError("simulated unified-controller apply failure")

    monkeypatch.setattr(
        controller_module,
        "apply_workspace_remove_normalize_text",
        fail_apply,
    )

    with pytest.raises(RuntimeError, match="simulated unified-controller apply failure"):
        controller.apply_pending_remove_normalize_text(
            "Keep all shared live state if governed apply fails.",
            text,
        )

    assert controller.current_run is run
    assert controller.current_export is export
    assert controller.pending_preview is pending
