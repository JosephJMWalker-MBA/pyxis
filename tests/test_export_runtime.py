import hashlib
import importlib
import json
from pathlib import Path

import pytest

from pyxis.app import build_workspace
from pyxis.authoring import create_workspace_spec
from pyxis.exporting import (
    build_export_plan,
    materialize_export_plan,
    verify_export_identity,
    verify_export_runtime,
)


compiler_repository_module = importlib.import_module("pyxis.compiler.repository")
export_runtime_module = importlib.import_module("pyxis.exporting.runtime")


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
        "Independent exported runtime proof.",
    )
    build = build_workspace(spec, source)
    plan = build_export_plan(build.repository, build.artifacts, build.manifest)
    materialize_export_plan(plan, source, destination)
    return plan, source, destination


def test_verify_export_runtime_executes_exported_tree_without_compile_or_write(
    tmp_path: Path,
    monkeypatch,
) -> None:
    plan, source, destination = _build_export(tmp_path)
    source_before = _file_snapshot(source)
    export_before = _file_snapshot(destination)
    text = "  hello   world  "

    def fail_if_compiled(*args, **kwargs):
        raise AssertionError("Export runtime verification must not compile.")

    monkeypatch.setattr(
        compiler_repository_module,
        "compile_repository",
        fail_if_compiled,
    )

    result = verify_export_runtime(plan, source, destination, text)

    assert result.source_root == source.resolve()
    assert result.export_root == destination.resolve()
    assert result.repository_id == plan.repository_id
    assert result.workspace_id == plan.workspace_id
    assert result.input_sha256 == hashlib.sha256(text.encode("utf-8")).hexdigest()
    assert result.source_result == result.export_result
    assert result.export_result == {
        "inspect_text": {
            "characters": 17,
            "words": 2,
            "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        },
        "normalize_text": {
            "normalized_text": "hello world",
            "changed": True,
        },
    }
    assert not hasattr(result, "ready")
    assert _file_snapshot(source) == source_before
    assert _file_snapshot(destination) == export_before


def test_verify_export_runtime_rejects_behavior_changing_export_edit(
    tmp_path: Path,
) -> None:
    plan, source, destination = _build_export(tmp_path)
    normalize_path = destination / "generated/capabilities/normalize_text.py"
    normalize_path.write_text(
        "def execute(text: str) -> dict[str, object]:\n"
        "    return {\"normalized_text\": \"changed export\", \"changed\": True}\n",
        encoding="utf-8",
    )
    source_before = _file_snapshot(source)
    export_before = _file_snapshot(destination)

    with pytest.raises(ValueError, match="runtime behavior does not match"):
        verify_export_runtime(plan, source, destination, "  hello   world  ")

    assert _file_snapshot(source) == source_before
    assert _file_snapshot(destination) == export_before


def test_verify_export_runtime_requires_exported_rir_identity_before_execution(
    tmp_path: Path,
    monkeypatch,
) -> None:
    plan, source, destination = _build_export(tmp_path)
    rir_path = destination / plan.rir_path
    payload = json.loads(rir_path.read_text(encoding="utf-8"))
    payload["workspace"]["description"] = "Changed after export materialization."
    rir_path.write_text(
        f"{json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True)}\n",
        encoding="utf-8",
    )

    def fail_if_executed(*args, **kwargs):
        raise AssertionError("RIR identity must be checked before runtime execution.")

    monkeypatch.setattr(
        export_runtime_module,
        "run_materialized_workspace",
        fail_if_executed,
    )

    with pytest.raises(ValueError, match="Exported RIR identity"):
        verify_export_runtime(plan, source, destination, "hello world")


def test_runtime_equivalence_does_not_replace_export_identity_verification(
    tmp_path: Path,
) -> None:
    plan, source, destination = _build_export(tmp_path)
    inspect_path = destination / "generated/capabilities/inspect_text.py"
    inspect_path.write_bytes(inspect_path.read_bytes() + b"\n# behavior-neutral edit\n")
    before = _file_snapshot(destination)

    runtime_result = verify_export_runtime(
        plan,
        source,
        destination,
        "hello world",
    )

    assert runtime_result.source_result == runtime_result.export_result
    assert not hasattr(runtime_result, "ready")
    with pytest.raises(ValueError, match="compiler product identity"):
        verify_export_identity(plan, destination)
    assert _file_snapshot(destination) == before
