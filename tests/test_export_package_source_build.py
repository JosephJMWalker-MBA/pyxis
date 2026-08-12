import importlib
from pathlib import Path

import pytest

from pyxis.app import build_workspace
from pyxis.authoring import create_workspace_spec
from pyxis.exporting import (
    build_export_plan,
    build_package_layout_plan,
    materialize_export_plan,
    materialize_package_layout,
    observe_offline_source_wheel_build,
)


compiler_repository_module = importlib.import_module("pyxis.compiler.repository")


def _file_snapshot(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


def _build_materialized_package(tmp_path: Path):
    source = tmp_path / "workspace"
    portable = tmp_path / "portable"
    spec = create_workspace_spec(
        "Text Lab",
        "Offline conventional source-build characterization.",
    )
    build = build_workspace(spec, source)
    export_plan = build_export_plan(build.repository, build.artifacts, build.manifest)
    materialize_export_plan(export_plan, source, portable)
    package_plan = build_package_layout_plan(export_plan)
    materialize_package_layout(package_plan, portable)
    return portable, package_plan


def test_observe_offline_source_wheel_build_reproduces_build_dependency_constraint(
    tmp_path: Path,
    monkeypatch,
) -> None:
    portable, package_plan = _build_materialized_package(tmp_path)
    before = _file_snapshot(portable)

    def fail_if_compiled(*args, **kwargs):
        raise AssertionError("Offline source-build observation must not compile Workspace source.")

    monkeypatch.setattr(
        compiler_repository_module,
        "compile_repository",
        fail_if_compiled,
    )

    observation = observe_offline_source_wheel_build(package_plan, portable)

    diagnostic = f"{observation.stdout}\n{observation.stderr}".lower()
    assert observation.portable_root == portable.resolve()
    assert observation.project_name == "text-lab"
    assert observation.version == "0.0.0"
    assert observation.outcome == "failed"
    assert observation.returncode != 0
    assert observation.wheel_filenames == ()
    assert "setuptools" in diagnostic
    assert "77.0.3" in diagnostic
    assert (
        "no matching distribution" in diagnostic
        or "could not find a version" in diagnostic
    )
    assert _file_snapshot(portable) == before


def test_observe_offline_source_wheel_build_rejects_tampered_projection_before_subprocess(
    tmp_path: Path,
    monkeypatch,
) -> None:
    portable, package_plan = _build_materialized_package(tmp_path)
    projection = package_plan.compiler_projections[0]
    (portable / projection.package_path).write_bytes(b"# changed package projection\n")
    before = _file_snapshot(portable)

    package_source_build_module = importlib.import_module(
        "pyxis.exporting.package_source_build"
    )

    def fail_if_spawned(*args, **kwargs):
        raise AssertionError("Tampered package must fail before source-build subprocess.")

    monkeypatch.setattr(package_source_build_module.subprocess, "run", fail_if_spawned)

    with pytest.raises(ValueError, match="no longer matches recorded integrity"):
        observe_offline_source_wheel_build(package_plan, portable)

    assert _file_snapshot(portable) == before
