import importlib
import json
from pathlib import Path
import subprocess
import sys

import pytest

from pyxis.app import build_workspace
from pyxis.authoring import create_workspace_spec
from pyxis.exporting import (
    build_export_plan,
    build_package_layout_plan,
    materialize_export_plan,
    materialize_package_layout,
    verify_export,
    verify_package_runtime,
)


compiler_repository_module = importlib.import_module("pyxis.compiler.repository")
package_runtime_module = importlib.import_module("pyxis.exporting.package_runtime")


def _file_snapshot(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


def _build_verified_package(tmp_path: Path, text: str):
    source = tmp_path / "workspace"
    portable = tmp_path / "portable"
    spec = create_workspace_spec(
        "Text Lab",
        "Isolated conventional package runtime proof.",
    )
    build = build_workspace(spec, source)
    export_plan = build_export_plan(build.repository, build.artifacts, build.manifest)
    materialize_export_plan(export_plan, source, portable)
    export_verification = verify_export(export_plan, source, portable, text)
    package_plan = build_package_layout_plan(export_plan)
    materialize_package_layout(package_plan, portable)
    return portable, package_plan, export_verification


def test_verify_package_runtime_executes_src_layout_without_pyxis_or_writes(
    tmp_path: Path,
    monkeypatch,
) -> None:
    text = "  hello   world  "
    portable, package_plan, export_verification = _build_verified_package(
        tmp_path,
        text,
    )
    before = _file_snapshot(portable)

    def fail_if_compiled(*args, **kwargs):
        raise AssertionError("Package runtime verification must not compile.")

    monkeypatch.setattr(
        compiler_repository_module,
        "compile_repository",
        fail_if_compiled,
    )

    result = verify_package_runtime(
        package_plan,
        export_verification,
        portable,
        text,
    )

    assert result.portable_root == portable.resolve()
    assert result.project_name == package_plan.project_name == "text-lab"
    assert result.workspace_module == "workspaces.text_lab.main"
    assert result.expected_result == export_verification.runtime.export_result
    assert result.package_result == result.expected_result
    assert result.package_result["inspect_text"]["words"] == 2
    assert result.package_result["normalize_text"] == {
        "normalized_text": "hello world",
        "changed": True,
    }
    assert _file_snapshot(portable) == before
    assert not tuple(portable.rglob("__pycache__"))
    assert not tuple(portable.rglob("*.pyc"))


def test_verify_package_runtime_uses_only_portable_src_pythonpath_and_no_site(
    tmp_path: Path,
    monkeypatch,
) -> None:
    text = "hello world"
    portable, package_plan, export_verification = _build_verified_package(
        tmp_path,
        text,
    )
    expected = export_verification.runtime.export_result
    observed: dict[str, object] = {}

    def fake_run(command, **kwargs):
        observed["command"] = command
        observed.update(kwargs)
        return subprocess.CompletedProcess(
            args=command,
            returncode=0,
            stdout=json.dumps(expected),
            stderr="",
        )

    monkeypatch.setattr(package_runtime_module.subprocess, "run", fake_run)

    result = verify_package_runtime(
        package_plan,
        export_verification,
        portable,
        text,
    )

    command = observed["command"]
    assert command[0] == sys.executable
    assert command[1:3] == ["-S", "-c"]
    assert 'find_spec("pyxis")' in command[3]
    assert 'run_module("pyxis_workspace"' in command[3]
    assert command[4] == text
    assert observed["cwd"] == portable.resolve()
    environment = observed["env"]
    assert environment["PYTHONPATH"] == str((portable / "src").resolve())
    assert environment["PYTHONDONTWRITEBYTECODE"] == "1"
    assert environment["PYTHONNOUSERSITE"] == "1"
    assert "PYTHONHOME" not in environment
    assert observed["capture_output"] is True
    assert observed["text"] is True
    assert observed["check"] is False
    assert result.package_result == expected


def test_verify_package_runtime_rejects_different_input_before_subprocess(
    tmp_path: Path,
    monkeypatch,
) -> None:
    portable, package_plan, export_verification = _build_verified_package(
        tmp_path,
        "verified input",
    )

    def fail_if_spawned(*args, **kwargs):
        raise AssertionError("Mismatched verification input must fail before subprocess.")

    monkeypatch.setattr(package_runtime_module.subprocess, "run", fail_if_spawned)

    with pytest.raises(ValueError, match="input does not match verified export input"):
        verify_package_runtime(
            package_plan,
            export_verification,
            portable,
            "different input",
        )


def test_verify_package_runtime_rejects_behavior_changing_src_projection(
    tmp_path: Path,
) -> None:
    text = "  hello   world  "
    portable, package_plan, export_verification = _build_verified_package(
        tmp_path,
        text,
    )
    normalize_path = portable / "src/capabilities/normalize_text.py"
    normalize_path.write_text(
        "def execute(text: str) -> dict[str, object]:\n"
        "    return {\"normalized_text\": \"changed package\", \"changed\": True}\n",
        encoding="utf-8",
    )
    before = _file_snapshot(portable)

    with pytest.raises(ValueError, match="package runtime behavior does not match"):
        verify_package_runtime(
            package_plan,
            export_verification,
            portable,
            text,
        )

    assert _file_snapshot(portable) == before
    assert not tuple(portable.rglob("__pycache__"))
    assert not tuple(portable.rglob("*.pyc"))
