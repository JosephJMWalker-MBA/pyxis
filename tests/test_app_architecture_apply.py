import importlib
from pathlib import Path

import pytest

from pyxis.app import (
    WorkspaceArchitecturePreviewController,
    build_and_run_workspace,
    build_workspace,
    export_workspace,
    query_workspace_presentation,
)
from pyxis.authoring import create_workspace_spec, load_workspace_spec


architecture_apply_module = importlib.import_module("pyxis.app.architecture_apply")


def _file_snapshot(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


def test_architecture_controller_applies_exact_pending_preview_and_drops_ready(
    tmp_path: Path,
    monkeypatch,
) -> None:
    source = tmp_path / "workspace"
    portable = tmp_path / "portable"
    text = "  hello   world  "
    spec = create_workspace_spec(
        "Text Lab",
        "Rationale-bearing application apply seam proof.",
    )
    run = build_and_run_workspace(spec, source, text)
    export = export_workspace(run.build, source, portable, text)
    portable_before = _file_snapshot(portable)

    controller = WorkspaceArchitecturePreviewController(
        source,
        run,
        export=export,
    )
    controller.preview_remove_normalize_text()
    pending = controller.pending_preview
    assert pending is not None
    assert controller.current_run is run
    assert controller.current_export is export

    real_apply = architecture_apply_module.apply_remove_normalize_text
    apply_calls = 0

    def counted_apply(preview, destination_root, rationale):
        nonlocal apply_calls
        apply_calls += 1
        assert preview is pending
        assert destination_root == source.resolve()
        assert rationale == "Remove normalization after reviewing the preview."
        return real_apply(preview, destination_root, rationale)

    monkeypatch.setattr(
        architecture_apply_module,
        "apply_remove_normalize_text",
        counted_apply,
    )

    real_runtime = architecture_apply_module.run_materialized_workspace
    runtime_calls = 0

    def counted_runtime(repository, destination_root, runtime_text):
        nonlocal runtime_calls
        runtime_calls += 1
        assert repository == pending.proposed_repository
        assert destination_root == source.resolve()
        assert runtime_text == text
        return real_runtime(repository, destination_root, runtime_text)

    monkeypatch.setattr(
        architecture_apply_module,
        "run_materialized_workspace",
        counted_runtime,
    )

    presentation = controller.apply_pending_remove_normalize_text(
        "  Remove normalization after reviewing the preview.  ",
        text,
    )

    assert apply_calls == 1
    assert runtime_calls == 1
    assert controller.pending_preview is None
    assert controller.current_run is not run
    assert controller.current_export is None

    assert load_workspace_spec(source) == pending.proposed_spec
    assert controller.current_run.build.repository == pending.proposed_repository
    assert tuple(controller.current_run.runtime_result) == ("inspect_text",)
    assert presentation.canonical.capabilities == ("inspect_text",)
    assert presentation.rir.capabilities == ("inspect_text",)
    assert presentation.export is None
    assert any(
        artifact.path == "generated/capabilities/normalize_text.py"
        and artifact.status == "removed"
        for artifact in presentation.artifacts
    )
    assert len(presentation.revisions) == 1
    assert presentation.revisions[0].operation == "remove_capability:normalize_text"
    assert presentation.revisions[0].rationale == (
        "Remove normalization after reviewing the preview."
    )
    assert presentation.revisions[0].completed is True

    post_apply = query_workspace_presentation(
        source,
        run=controller.current_run,
        export=None,
    )
    assert post_apply == presentation

    # The old portable files still exist, but pre-change READY evidence is no
    # longer carried as current state after architecture/compiler identity changes.
    assert _file_snapshot(portable) == portable_before
    assert portable.is_dir()


def test_architecture_controller_requires_nonempty_rationale_without_consuming_preview(
    tmp_path: Path,
) -> None:
    source = tmp_path / "workspace"
    portable = tmp_path / "portable"
    text = "hello world"
    spec = create_workspace_spec(
        "Text Lab",
        "Empty rationale must not consume proposed architecture.",
    )
    run = build_and_run_workspace(spec, source, text)
    export = export_workspace(run.build, source, portable, text)
    controller = WorkspaceArchitecturePreviewController(source, run, export=export)
    controller.preview_remove_normalize_text()
    pending = controller.pending_preview
    source_before = _file_snapshot(source)
    portable_before = _file_snapshot(portable)

    with pytest.raises(ValueError, match="rationale"):
        controller.apply_pending_remove_normalize_text("   ", text)

    assert controller.pending_preview is pending
    assert controller.current_run is run
    assert controller.current_export is export
    assert _file_snapshot(source) == source_before
    assert _file_snapshot(portable) == portable_before


def test_architecture_controller_keeps_pending_state_when_governed_apply_fails(
    tmp_path: Path,
    monkeypatch,
) -> None:
    source = tmp_path / "workspace"
    text = "hello world"
    spec = create_workspace_spec(
        "Text Lab",
        "Failed governed apply must not advance controller state.",
    )
    run = build_and_run_workspace(spec, source, text)
    controller = WorkspaceArchitecturePreviewController(source, run)
    controller.preview_remove_normalize_text()
    pending = controller.pending_preview
    source_before = _file_snapshot(source)

    def fail_apply(preview, destination_root, rationale):
        assert preview is pending
        raise RuntimeError("simulated governed apply failure")

    monkeypatch.setattr(
        architecture_apply_module,
        "apply_remove_normalize_text",
        fail_apply,
    )

    def fail_if_runtime_runs(*args, **kwargs):
        raise AssertionError("Runtime must not execute after failed apply.")

    monkeypatch.setattr(
        architecture_apply_module,
        "run_materialized_workspace",
        fail_if_runtime_runs,
    )

    with pytest.raises(RuntimeError, match="simulated governed apply failure"):
        controller.apply_pending_remove_normalize_text(
            "Keep the pending proposal if apply fails.",
            text,
        )

    assert controller.pending_preview is pending
    assert controller.current_run is run
    assert controller.current_export is None
    assert _file_snapshot(source) == source_before


def test_architecture_controller_requires_a_pending_preview_before_apply(
    tmp_path: Path,
) -> None:
    source = tmp_path / "workspace"
    spec = create_workspace_spec(
        "Text Lab",
        "Apply requires an exact preview shown earlier.",
    )
    run = build_and_run_workspace(spec, source, "hello world")
    controller = WorkspaceArchitecturePreviewController(source, run)
    source_before = _file_snapshot(source)

    with pytest.raises(ValueError, match="No pending architecture preview"):
        controller.apply_pending_remove_normalize_text(
            "This rationale has no retained preview to govern.",
            "hello world",
        )

    assert controller.current_run is run
    assert controller.pending_preview is None
    assert _file_snapshot(source) == source_before


def test_architecture_apply_rejects_stale_live_run_before_governed_apply(
    tmp_path: Path,
    monkeypatch,
) -> None:
    source = tmp_path / "workspace"
    text = "hello world"
    spec = create_workspace_spec(
        "Text Lab",
        "Stale live evidence must fail before architectural mutation.",
    )
    run = build_and_run_workspace(spec, source, text)
    controller = WorkspaceArchitecturePreviewController(source, run)
    controller.preview_remove_normalize_text()
    pending = controller.pending_preview

    changed_spec = spec.without_capability("normalize_text")
    build_workspace(changed_spec, source)
    source_before = _file_snapshot(source)

    def fail_if_apply_runs(*args, **kwargs):
        raise AssertionError("Stale live evidence must fail before governed apply.")

    monkeypatch.setattr(
        architecture_apply_module,
        "apply_remove_normalize_text",
        fail_if_apply_runs,
    )

    with pytest.raises(ValueError, match="persisted Workspace RIR"):
        controller.apply_pending_remove_normalize_text(
            "Do not mutate from stale live evidence.",
            text,
        )

    assert controller.pending_preview is pending
    assert controller.current_run is run
    assert _file_snapshot(source) == source_before
