import importlib
from pathlib import Path

import pytest

from pyxis.app import build_workspace
from pyxis.authoring import create_workspace_spec
from pyxis.exporting import (
    build_export_plan,
    materialize_export_plan,
    verify_export,
    verify_export_identity,
)


compiler_repository_module = importlib.import_module("pyxis.compiler.repository")
export_readiness_module = importlib.import_module("pyxis.exporting.readiness")


def _file_snapshot(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


def _build_export(tmp_path: Path):
    source = tmp_path / "workspace"
    destination = tmp_path / "portable"
    spec = create_workspace_spec(
        "Text Lab",
        "Evidence-backed export readiness proof.",
    )
    build = build_workspace(spec, source)
    plan = build_export_plan(build.repository, build.artifacts, build.manifest)
    materialize_export_plan(plan, source, destination)
    return plan, source, destination


def test_verify_export_derives_ready_only_after_both_evidence_streams_succeed(
    tmp_path: Path,
    monkeypatch,
) -> None:
    plan, source, destination = _build_export(tmp_path)
    source_before = _file_snapshot(source)
    export_before = _file_snapshot(destination)

    def fail_if_compiled(*args, **kwargs):
        raise AssertionError("Final export verification must not compile.")

    monkeypatch.setattr(
        compiler_repository_module,
        "compile_repository",
        fail_if_compiled,
    )

    result = verify_export(
        plan,
        source,
        destination,
        "  hello   world  ",
    )

    assert result.readiness == "READY"
    assert result.identity.export_root == destination.resolve()
    assert result.runtime.export_root == destination.resolve()
    assert result.identity.repository_id == result.runtime.repository_id == plan.repository_id
    assert result.identity.workspace_id == result.runtime.workspace_id == plan.workspace_id
    assert result.identity.rir_sha256 == plan.rir_sha256
    assert result.runtime.source_result == result.runtime.export_result
    assert _file_snapshot(source) == source_before
    assert _file_snapshot(destination) == export_before


def test_verify_export_identity_failure_blocks_runtime_and_ready(
    tmp_path: Path,
    monkeypatch,
) -> None:
    plan, source, destination = _build_export(tmp_path)
    inspect_path = destination / "generated/capabilities/inspect_text.py"
    inspect_path.write_bytes(inspect_path.read_bytes() + b"\n# behavior-neutral edit\n")
    source_before = _file_snapshot(source)
    export_before = _file_snapshot(destination)

    def fail_if_runtime_attempted(*args, **kwargs):
        raise AssertionError("Runtime must not run after identity verification fails.")

    monkeypatch.setattr(
        export_readiness_module,
        "verify_export_runtime",
        fail_if_runtime_attempted,
    )

    with pytest.raises(ValueError, match="compiler product identity"):
        verify_export(plan, source, destination, "hello world")

    assert _file_snapshot(source) == source_before
    assert _file_snapshot(destination) == export_before


def test_verify_export_runtime_failure_blocks_ready_even_when_export_identity_passes(
    tmp_path: Path,
) -> None:
    plan, source, destination = _build_export(tmp_path)

    identity = verify_export_identity(plan, destination)
    assert identity.rir_sha256 == plan.rir_sha256

    source_normalize_path = source / "generated/capabilities/normalize_text.py"
    source_normalize_path.write_text(
        "def execute(text: str) -> dict[str, object]:\n"
        "    return {\"normalized_text\": \"changed source\", \"changed\": True}\n",
        encoding="utf-8",
    )
    source_before = _file_snapshot(source)
    export_before = _file_snapshot(destination)

    with pytest.raises(ValueError, match="runtime behavior does not match"):
        verify_export(plan, source, destination, "  hello   world  ")

    assert _file_snapshot(source) == source_before
    assert _file_snapshot(destination) == export_before


def test_verify_export_rejects_mismatched_successful_evidence_before_ready(
    tmp_path: Path,
    monkeypatch,
) -> None:
    plan, source, destination = _build_export(tmp_path)
    identity = verify_export_identity(plan, destination)

    real_runtime = export_readiness_module.verify_export_runtime(
        plan,
        source,
        destination,
        "hello world",
    )

    from dataclasses import replace

    mismatched_runtime = replace(
        real_runtime,
        export_root=(tmp_path / "different-export").resolve(),
    )

    monkeypatch.setattr(
        export_readiness_module,
        "verify_export_identity",
        lambda *args, **kwargs: identity,
    )
    monkeypatch.setattr(
        export_readiness_module,
        "verify_export_runtime",
        lambda *args, **kwargs: mismatched_runtime,
    )

    with pytest.raises(RuntimeError, match="different export roots"):
        verify_export(plan, source, destination, "hello world")
