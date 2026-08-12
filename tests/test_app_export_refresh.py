import importlib
from pathlib import Path

import pytest

from pyxis.app import (
    WorkspaceController,
    build_and_run_workspace,
    export_workspace,
    query_workspace_presentation,
    refresh_workspace_export,
)
from pyxis.authoring import create_workspace_spec


controller_module = importlib.import_module("pyxis.app.controller")
export_refresh_module = importlib.import_module("pyxis.app.export_refresh")
compiler_repository_module = importlib.import_module("pyxis.compiler.repository")


def _file_snapshot(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


def _post_apply_controller(
    tmp_path: Path,
) -> tuple[Path, Path, WorkspaceController]:
    source = tmp_path / "workspace"
    old_portable = tmp_path / "portable-before-apply"
    text = "  hello   world  "
    spec = create_workspace_spec(
        "Text Lab",
        "Export refresh should recover READY only for the current architecture.",
    )
    initial_run = build_and_run_workspace(spec, source, text)
    initial_export = export_workspace(
        initial_run.build,
        source,
        old_portable,
        text,
    )
    controller = WorkspaceController(
        source,
        initial_run,
        export=initial_export,
    )
    controller.preview_remove_normalize_text()
    controller.apply_pending_remove_normalize_text(
        "Remove normalization before proving READY recovery.",
        text,
    )

    assert controller.current_export is None
    assert controller.pending_preview is None
    assert tuple(controller.current_run.runtime_result) == ("inspect_text",)
    return source, old_portable, controller


def test_refresh_workspace_export_recovers_ready_from_exact_post_apply_build(
    tmp_path: Path,
    monkeypatch,
) -> None:
    source, old_portable, controller = _post_apply_controller(tmp_path)
    destination = tmp_path / "portable-after-apply"
    text = "verification input for the current post-apply build"
    current_run = controller.current_run
    source_before = _file_snapshot(source)
    old_portable_before = _file_snapshot(old_portable)

    def fail_if_compiled(*args, **kwargs):
        raise AssertionError("Verified export refresh must not compile.")

    monkeypatch.setattr(
        compiler_repository_module,
        "compile_repository",
        fail_if_compiled,
    )

    real_export = export_refresh_module.export_workspace
    export_inputs = []

    def tracked_export(build, source_root, destination_root, actual_text):
        export_inputs.append((build, source_root, destination_root, actual_text))
        return real_export(build, source_root, destination_root, actual_text)

    monkeypatch.setattr(export_refresh_module, "export_workspace", tracked_export)

    result = refresh_workspace_export(
        source,
        current_run,
        destination,
        text,
    )

    assert export_inputs == [
        (current_run.build, source.resolve(), destination, text)
    ]
    assert result.export.verification.readiness == "READY"
    assert result.export.materialization.destination_root == destination.resolve()
    assert result.presentation.export is not None
    assert result.presentation.export.readiness == "READY"
    assert result.presentation.canonical.capabilities == ("inspect_text",)
    assert tuple(result.presentation.runtime_result) == ("inspect_text",)
    assert query_workspace_presentation(
        source,
        run=current_run,
        export=result.export,
    ) == result.presentation
    assert _file_snapshot(source) == source_before
    assert _file_snapshot(old_portable) == old_portable_before


def test_refresh_workspace_export_rejects_stale_run_before_export(
    tmp_path: Path,
    monkeypatch,
) -> None:
    source = tmp_path / "workspace"
    destination = tmp_path / "portable-after-stale-run"
    text = "hello world"
    spec = create_workspace_spec(
        "Text Lab",
        "Stale live evidence must fail before export starts.",
    )
    stale_run = build_and_run_workspace(spec, source, text)
    controller = WorkspaceController(source, stale_run)
    controller.preview_remove_normalize_text()
    controller.apply_pending_remove_normalize_text(
        "Change architecture so the original run becomes stale.",
        text,
    )
    source_before = _file_snapshot(source)

    def fail_if_exported(*args, **kwargs):
        raise AssertionError("Stale run evidence must be rejected before export.")

    monkeypatch.setattr(
        export_refresh_module,
        "export_workspace",
        fail_if_exported,
    )

    with pytest.raises(ValueError, match="does not match the persisted Workspace RIR"):
        refresh_workspace_export(
            source,
            stale_run,
            destination,
            text,
        )

    assert not destination.exists()
    assert _file_snapshot(source) == source_before


def test_workspace_controller_retains_export_only_after_verified_refresh_success(
    tmp_path: Path,
    monkeypatch,
) -> None:
    source, old_portable, controller = _post_apply_controller(tmp_path)
    occupied = tmp_path / "occupied-portable"
    occupied.mkdir()
    fresh_destination = tmp_path / "fresh-portable"
    text = "explicit verification input"
    current_run = controller.current_run
    source_before = _file_snapshot(source)
    old_portable_before = _file_snapshot(old_portable)

    def fail_if_compiled(*args, **kwargs):
        raise AssertionError("Controller export refresh must not compile.")

    monkeypatch.setattr(
        compiler_repository_module,
        "compile_repository",
        fail_if_compiled,
    )

    real_refresh = controller_module.refresh_workspace_export
    refresh_inputs = []

    def tracked_refresh(workspace_root, run, destination_root, actual_text):
        refresh_inputs.append((workspace_root, run, destination_root, actual_text))
        return real_refresh(workspace_root, run, destination_root, actual_text)

    monkeypatch.setattr(
        controller_module,
        "refresh_workspace_export",
        tracked_refresh,
    )

    with pytest.raises(FileExistsError, match="Export destination already exists"):
        controller.refresh_export(occupied, text)

    assert controller.current_run is current_run
    assert controller.current_export is None
    assert controller.pending_preview is None
    assert _file_snapshot(source) == source_before
    assert _file_snapshot(old_portable) == old_portable_before

    presentation = controller.refresh_export(fresh_destination, text)

    assert refresh_inputs == [
        (source.resolve(), current_run, occupied, text),
        (source.resolve(), current_run, fresh_destination, text),
    ]
    assert controller.current_run is current_run
    assert controller.current_export is not None
    assert controller.current_export.verification.readiness == "READY"
    assert controller.current_export.materialization.destination_root == (
        fresh_destination.resolve()
    )
    assert controller.pending_preview is None
    assert presentation.export is not None
    assert presentation.export.readiness == "READY"
    assert presentation.canonical.capabilities == ("inspect_text",)
    assert query_workspace_presentation(
        source,
        run=controller.current_run,
        export=controller.current_export,
    ) == presentation
    assert _file_snapshot(source) == source_before
    assert _file_snapshot(old_portable) == old_portable_before
