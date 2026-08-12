import hashlib
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
)


compiler_repository_module = importlib.import_module("pyxis.compiler.repository")


def _file_snapshot(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


def _build_portable_export(tmp_path: Path):
    source = tmp_path / "workspace"
    portable = tmp_path / "portable"
    spec = create_workspace_spec(
        "Text Lab",
        "Conventional package materialization proof.",
    )
    build = build_workspace(spec, source)
    export_plan = build_export_plan(build.repository, build.artifacts, build.manifest)
    materialize_export_plan(export_plan, source, portable)
    package_plan = build_package_layout_plan(export_plan)
    return portable, package_plan


def test_materialize_package_layout_copies_exact_compiler_bytes_and_only_planned_support(
    tmp_path: Path,
    monkeypatch,
) -> None:
    portable, package_plan = _build_portable_export(tmp_path)
    before = _file_snapshot(portable)
    generated_before = {
        path: payload
        for path, payload in before.items()
        if path.startswith("generated/")
    }

    def fail_if_compiled(*args, **kwargs):
        raise AssertionError("Package materialization must not compile.")

    monkeypatch.setattr(
        compiler_repository_module,
        "compile_repository",
        fail_if_compiled,
    )

    result = materialize_package_layout(package_plan, portable)

    assert result.portable_root == portable.resolve()
    assert tuple(
        path.relative_to(portable).as_posix()
        for path in result.compiler_projection_paths
    ) == tuple(
        projection.package_path
        for projection in package_plan.compiler_projections
    )
    assert tuple(
        path.relative_to(portable).as_posix()
        for path in result.support_paths
    ) == tuple(support.path for support in package_plan.support_files)

    for projection in package_plan.compiler_projections:
        source_bytes = (portable / projection.source_path).read_bytes()
        package_bytes = (portable / projection.package_path).read_bytes()
        assert package_bytes == source_bytes
        assert hashlib.sha256(package_bytes).hexdigest() == projection.artifact_sha256

    for support in package_plan.support_files:
        assert (portable / support.path).read_bytes() == support.source.encode("utf-8")

    after = _file_snapshot(portable)
    assert {
        path: payload
        for path, payload in after.items()
        if path.startswith("generated/")
    } == generated_before
    assert set(after) == set(before).union(
        projection.package_path for projection in package_plan.compiler_projections
    ).union(support.path for support in package_plan.support_files)


def test_materialize_package_layout_rejects_tampered_compiler_source_before_writes(
    tmp_path: Path,
) -> None:
    portable, package_plan = _build_portable_export(tmp_path)
    projection = package_plan.compiler_projections[0]
    source_path = portable / projection.source_path
    source_path.write_bytes(b"# changed after export verification\n")
    before = _file_snapshot(portable)

    with pytest.raises(ValueError, match="no longer matches recorded integrity"):
        materialize_package_layout(package_plan, portable)

    assert _file_snapshot(portable) == before
    assert not (portable / "src").exists()
    assert not (portable / "pyproject.toml").exists()


def test_materialize_package_layout_rejects_existing_target_before_any_new_writes(
    tmp_path: Path,
) -> None:
    portable, package_plan = _build_portable_export(tmp_path)
    existing_target = portable / package_plan.support_files[0].path
    existing_target.write_text("existing owner\n", encoding="utf-8")
    before = _file_snapshot(portable)

    with pytest.raises(FileExistsError, match="already exists"):
        materialize_package_layout(package_plan, portable)

    assert _file_snapshot(portable) == before
    assert not (portable / "src").exists()
    assert existing_target.read_text(encoding="utf-8") == "existing owner\n"


def test_materialize_package_layout_cleans_new_package_files_after_write_failure(
    tmp_path: Path,
    monkeypatch,
) -> None:
    portable, package_plan = _build_portable_export(tmp_path)
    before = _file_snapshot(portable)
    real_write_bytes = Path.write_bytes
    writes = 0

    def fail_during_package_write(path: Path, payload: bytes) -> int:
        nonlocal writes
        if portable.resolve() in path.resolve().parents:
            writes += 1
            if writes == 2:
                raise OSError("synthetic package write failure")
        return real_write_bytes(path, payload)

    monkeypatch.setattr(Path, "write_bytes", fail_during_package_write)

    with pytest.raises(OSError, match="synthetic package write failure"):
        materialize_package_layout(package_plan, portable)

    assert _file_snapshot(portable) == before
    assert not (portable / "src").exists()
    assert not (portable / "pyproject.toml").exists()
