import hashlib
import importlib
from pathlib import Path

import pytest

from pyxis.app import build_workspace
from pyxis.authoring import create_workspace_spec
from pyxis.exporting import (
    build_export_plan,
    build_package_layout_plan,
    build_package_wheel,
    materialize_export_plan,
    materialize_package_layout,
    verify_export,
    verify_package_installation,
    verify_package_runtime,
)


compiler_repository_module = importlib.import_module("pyxis.compiler.repository")
package_install_module = importlib.import_module("pyxis.exporting.package_install")


def _file_snapshot(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


def _build_verified_wheel(tmp_path: Path, text: str):
    source = tmp_path / "workspace"
    portable = tmp_path / "portable"
    wheel_directory = tmp_path / "wheelhouse"
    spec = create_workspace_spec(
        "Text Lab",
        "Offline fresh-environment installation proof.",
    )
    build = build_workspace(spec, source)
    export_plan = build_export_plan(build.repository, build.artifacts, build.manifest)
    materialize_export_plan(export_plan, source, portable)
    export_verification = verify_export(export_plan, source, portable, text)
    package_plan = build_package_layout_plan(export_plan)
    materialize_package_layout(package_plan, portable)
    package_runtime = verify_package_runtime(
        package_plan,
        export_verification,
        portable,
        text,
    )
    wheel_build = build_package_wheel(
        package_plan,
        portable,
        wheel_directory,
    )
    return portable, package_plan, package_runtime, wheel_build


def test_verify_package_installation_installs_verified_wheel_offline_and_runs_console(
    tmp_path: Path,
    monkeypatch,
) -> None:
    text = "  hello   world  "
    portable, package_plan, package_runtime, wheel_build = _build_verified_wheel(
        tmp_path,
        text,
    )
    portable_before = _file_snapshot(portable)
    wheel_before = wheel_build.wheel_path.read_bytes()

    def fail_if_compiled(*args, **kwargs):
        raise AssertionError("Offline wheel installation must not compile Workspace source.")

    monkeypatch.setattr(
        compiler_repository_module,
        "compile_repository",
        fail_if_compiled,
    )

    result = verify_package_installation(
        package_plan,
        wheel_build,
        package_runtime,
        text,
    )

    assert result.project_name == package_plan.project_name == "text-lab"
    assert result.version == package_plan.version == "0.0.0"
    assert result.installation_mode == "offline-wheel"
    assert result.wheel_sha256 == wheel_build.wheel_sha256
    assert result.wheel_sha256 == hashlib.sha256(wheel_before).hexdigest()
    assert result.input_sha256 == package_runtime.input_sha256
    assert result.expected_result == package_runtime.package_result
    assert result.installed_result == result.expected_result
    assert result.installed_result["inspect_text"]["words"] == 2
    assert result.installed_result["normalize_text"] == {
        "normalized_text": "hello world",
        "changed": True,
    }
    assert _file_snapshot(portable) == portable_before
    assert wheel_build.wheel_path.read_bytes() == wheel_before


def test_verify_package_installation_rejects_changed_wheel_before_creating_venv(
    tmp_path: Path,
    monkeypatch,
) -> None:
    text = "hello world"
    _, package_plan, package_runtime, wheel_build = _build_verified_wheel(
        tmp_path,
        text,
    )
    wheel_build.wheel_path.write_bytes(b"changed wheel bytes")

    class FailEnvBuilder:
        def __init__(self, *args, **kwargs):
            raise AssertionError("Changed wheel must fail before virtualenv creation.")

    monkeypatch.setattr(package_install_module.venv, "EnvBuilder", FailEnvBuilder)

    with pytest.raises(ValueError, match="wheel bytes no longer match"):
        verify_package_installation(
            package_plan,
            wheel_build,
            package_runtime,
            text,
        )


def test_verify_package_installation_rejects_different_input_before_creating_venv(
    tmp_path: Path,
    monkeypatch,
) -> None:
    _, package_plan, package_runtime, wheel_build = _build_verified_wheel(
        tmp_path,
        "verified input",
    )

    class FailEnvBuilder:
        def __init__(self, *args, **kwargs):
            raise AssertionError("Mismatched input must fail before virtualenv creation.")

    monkeypatch.setattr(package_install_module.venv, "EnvBuilder", FailEnvBuilder)

    with pytest.raises(ValueError, match="input does not match package-runtime evidence"):
        verify_package_installation(
            package_plan,
            wheel_build,
            package_runtime,
            "different input",
        )


def test_verify_package_installation_requires_matching_wheel_compiler_evidence(
    tmp_path: Path,
    monkeypatch,
) -> None:
    text = "hello world"
    _, package_plan, package_runtime, wheel_build = _build_verified_wheel(
        tmp_path,
        text,
    )
    from dataclasses import replace

    first = wheel_build.compiler_products[0]
    changed_first = replace(first, artifact_sha256="changed-artifact-hash")
    changed_wheel_build = replace(
        wheel_build,
        compiler_products=(changed_first, *wheel_build.compiler_products[1:]),
    )

    class FailEnvBuilder:
        def __init__(self, *args, **kwargs):
            raise AssertionError("Mismatched wheel evidence must fail before virtualenv creation.")

    monkeypatch.setattr(package_install_module.venv, "EnvBuilder", FailEnvBuilder)

    with pytest.raises(ValueError, match="compiler-product evidence"):
        verify_package_installation(
            package_plan,
            changed_wheel_build,
            package_runtime,
            text,
        )
