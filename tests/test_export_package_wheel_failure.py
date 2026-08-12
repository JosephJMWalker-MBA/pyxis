import importlib
from pathlib import Path
import subprocess

import pytest

from pyxis.app import build_workspace
from pyxis.authoring import create_workspace_spec
from pyxis.exporting import (
    build_export_plan,
    build_package_layout_plan,
    build_package_wheel,
    materialize_export_plan,
    materialize_package_layout,
)


package_wheel_module = importlib.import_module("pyxis.exporting.package_wheel")


def _snapshot(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


def test_build_package_wheel_removes_output_after_backend_failure(
    tmp_path: Path,
    monkeypatch,
) -> None:
    source = tmp_path / "workspace"
    portable = tmp_path / "portable"
    wheel_directory = tmp_path / "wheelhouse"
    spec = create_workspace_spec("Text Lab", "Wheel failure cleanup proof.")
    build = build_workspace(spec, source)
    export_plan = build_export_plan(build.repository, build.artifacts, build.manifest)
    materialize_export_plan(export_plan, source, portable)
    package_plan = build_package_layout_plan(export_plan)
    materialize_package_layout(package_plan, portable)
    before = _snapshot(portable)

    def fail_build(command, **kwargs):
        return subprocess.CompletedProcess(
            args=command,
            returncode=1,
            stdout="",
            stderr="synthetic backend failure",
        )

    monkeypatch.setattr(package_wheel_module.subprocess, "run", fail_build)

    with pytest.raises(RuntimeError, match="synthetic backend failure"):
        build_package_wheel(package_plan, portable, wheel_directory)

    assert _snapshot(portable) == before
    assert not wheel_directory.exists()
