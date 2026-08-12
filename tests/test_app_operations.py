import importlib
from pathlib import Path

import pytest

from pyxis.app import (
    apply_remove_normalize_text,
    build_and_run_workspace,
    export_workspace,
    preview_remove_normalize_text,
    rerun_workspace,
)
from pyxis.authoring import create_workspace_spec


operations_module = importlib.import_module("pyxis.app.operations")
compiler_repository_module = importlib.import_module("pyxis.compiler.repository")


def _file_snapshot(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


def test_rerun_workspace_reuses_build_and_returns_fresh_presentation(
    tmp_path: Path,
    monkeypatch,
) -> None:
    root = tmp_path / "workspace"
    portable = tmp_path / "portable"
    spec = create_workspace_spec(
        "Text Lab",
        "Runtime-only application operation proof.",
    )
    first = build_and_run_workspace(spec, root, "one")
    export = export_workspace(first.build, root, portable, "one")
    source_before = _file_snapshot(root)
    portable_before = _file_snapshot(portable)

    def fail_if_compiled(*args, **kwargs):
        raise AssertionError("Runtime-only Workspace operation must not compile.")

    monkeypatch.setattr(
        compiler_repository_module,
        "compile_repository",
        fail_if_compiled,
    )

    real_runtime = operations_module.run_materialized_workspace
    runtime_calls = 0

    def counted_runtime(*args, **kwargs):
        nonlocal runtime_calls
        runtime_calls += 1
        return real_runtime(*args, **kwargs)

    monkeypatch.setattr(
        operations_module,
        "run_materialized_workspace",
        counted_runtime,
    )

    result = rerun_workspace(
        root,
        first,
        "two words with different runtime evidence",
        export=export,
    )

    assert runtime_calls == 1
    assert result.run.build is first.build
    assert result.run.runtime_result != first.runtime_result
    assert result.presentation.runtime_result == result.run.runtime_result
    assert result.presentation.canonical.workspace_id == spec.workspace_id
    assert result.presentation.rir.rir_sha256 == first.build.manifest.rir_sha256
    assert tuple(
        (artifact.path, artifact.status)
        for artifact in result.presentation.artifacts
    ) == tuple(
        (status.path, status.status)
        for status in first.build.generation_statuses
    )
    assert result.presentation.export is not None
    assert result.presentation.export.readiness == "READY"
    assert result.presentation.export.export_root == portable.resolve()
    assert (
        result.presentation.export.input_sha256
        == export.verification.runtime.input_sha256
    )
    assert _file_snapshot(root) == source_before
    assert _file_snapshot(portable) == portable_before


def test_rerun_workspace_rejects_stale_run_before_runtime(
    tmp_path: Path,
    monkeypatch,
) -> None:
    root = tmp_path / "workspace"
    spec = create_workspace_spec(
        "Text Lab",
        "Stale live evidence must fail before runtime execution.",
    )
    stale_run = build_and_run_workspace(spec, root, "first input")
    preview = preview_remove_normalize_text(spec)
    apply_remove_normalize_text(
        preview,
        root,
        "Change persisted architecture after the earlier run evidence.",
    )

    def fail_if_runtime_executes(*args, **kwargs):
        raise AssertionError("Stale evidence must be rejected before runtime.")

    monkeypatch.setattr(
        operations_module,
        "run_materialized_workspace",
        fail_if_runtime_executes,
    )

    with pytest.raises(ValueError, match="persisted Workspace RIR"):
        rerun_workspace(
            root,
            stale_run,
            "this must never execute",
        )
