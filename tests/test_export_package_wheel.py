import hashlib
import importlib
from pathlib import Path
import zipfile

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
        "Standard wheel construction identity proof.",
    )
    build = build_workspace(spec, source)
    export_plan = build_export_plan(build.repository, build.artifacts, build.manifest)
    materialize_export_plan(export_plan, source, portable)
    package_plan = build_package_layout_plan(export_plan)
    materialize_package_layout(package_plan, portable)
    return portable, package_plan


def _wheel_member(package_path: str) -> str:
    path = Path(package_path)
    assert path.parts[0] == "src"
    return Path(*path.parts[1:]).as_posix()


def test_build_package_wheel_builds_standard_wheel_and_preserves_compiler_identity(
    tmp_path: Path,
    monkeypatch,
) -> None:
    portable, package_plan = _build_materialized_package(tmp_path)
    wheel_directory = tmp_path / "wheelhouse"
    before = _file_snapshot(portable)

    def fail_if_compiled(*args, **kwargs):
        raise AssertionError("Portable wheel construction must not compile Workspace source.")

    monkeypatch.setattr(
        compiler_repository_module,
        "compile_repository",
        fail_if_compiled,
    )

    result = build_package_wheel(package_plan, portable, wheel_directory)

    assert result.portable_root == portable.resolve()
    assert result.project_name == "text-lab"
    assert result.version == "0.0.0"
    assert result.wheel_path.parent == wheel_directory.resolve()
    assert result.wheel_path.suffix == ".whl"
    assert result.wheel_sha256 == hashlib.sha256(result.wheel_path.read_bytes()).hexdigest()

    with zipfile.ZipFile(result.wheel_path, "r") as archive:
        members = set(archive.namelist())
        expected_python_members = {
            _wheel_member(projection.package_path)
            for projection in package_plan.compiler_projections
        }.union(
            _wheel_member(support.path)
            for support in package_plan.support_files
            if support.path.startswith("src/") and support.path.endswith(".py")
        )
        assert {member for member in members if member.endswith(".py")} == expected_python_members
        assert not any(member.startswith("pyxis/") for member in members)

        for projection in package_plan.compiler_projections:
            member = _wheel_member(projection.package_path)
            payload = archive.read(member)
            assert payload == (portable / projection.package_path).read_bytes()
            assert hashlib.sha256(payload).hexdigest() == projection.artifact_sha256

        entry_points = tuple(
            member for member in members if member.endswith(".dist-info/entry_points.txt")
        )
        assert len(entry_points) == 1
        assert "text-lab = pyxis_workspace:main" in archive.read(entry_points[0]).decode("utf-8")

    assert tuple(product.artifact_sha256 for product in result.compiler_products) == tuple(
        projection.artifact_sha256 for projection in package_plan.compiler_projections
    )
    assert _file_snapshot(portable) == before
    assert not (portable / "build").exists()
    assert not tuple((portable / "src").glob("*.egg-info"))


def test_build_package_wheel_rejects_tampered_compiler_projection_before_output(
    tmp_path: Path,
) -> None:
    portable, package_plan = _build_materialized_package(tmp_path)
    wheel_directory = tmp_path / "wheelhouse"
    projection = package_plan.compiler_projections[0]
    (portable / projection.package_path).write_bytes(b"# changed package projection\n")
    before = _file_snapshot(portable)

    with pytest.raises(ValueError, match="no longer matches recorded integrity"):
        build_package_wheel(package_plan, portable, wheel_directory)

    assert _file_snapshot(portable) == before
    assert not wheel_directory.exists()


def test_build_package_wheel_rejects_tampered_support_before_output(
    tmp_path: Path,
) -> None:
    portable, package_plan = _build_materialized_package(tmp_path)
    wheel_directory = tmp_path / "wheelhouse"
    (portable / "pyproject.toml").write_text("# changed build metadata\n", encoding="utf-8")
    before = _file_snapshot(portable)

    with pytest.raises(ValueError, match="support no longer matches its plan"):
        build_package_wheel(package_plan, portable, wheel_directory)

    assert _file_snapshot(portable) == before
    assert not wheel_directory.exists()
