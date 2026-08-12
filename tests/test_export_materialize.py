import importlib
from pathlib import Path

import pytest

from pyxis.app import build_workspace
from pyxis.authoring import create_workspace_spec
from pyxis.exporting import build_export_plan, materialize_export_plan


compiler_repository_module = importlib.import_module("pyxis.compiler.repository")


def _file_snapshot(root: Path) -> dict[str, bytes]:
    if not root.exists():
        return {}
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


def _planned_paths(plan) -> tuple[str, ...]:
    return (
        plan.canonical_path,
        plan.rir_path,
        plan.generation_manifest_path,
        *(product.path for product in plan.compiler_products),
    )


def _staging_paths(destination: Path) -> tuple[Path, ...]:
    if not destination.parent.exists():
        return ()
    return tuple(destination.parent.glob(f".{destination.name}.pyxis-export-*"))


def test_materialize_export_copies_only_exact_planned_bytes_without_recompiling(
    tmp_path: Path,
    monkeypatch,
) -> None:
    source = tmp_path / "workspace"
    destination = tmp_path / "portable"
    spec = create_workspace_spec(
        "Text Lab",
        "Exact-byte export materialization proof.",
    )
    build = build_workspace(spec, source)
    plan = build_export_plan(build.repository, build.artifacts, build.manifest)
    source_before = _file_snapshot(source)

    def fail_if_compiled(*args, **kwargs):
        raise AssertionError("Export materialization must not compile.")

    monkeypatch.setattr(
        compiler_repository_module,
        "compile_repository",
        fail_if_compiled,
    )

    result = materialize_export_plan(plan, source, destination)

    planned_paths = _planned_paths(plan)
    assert result.destination_root == destination.resolve()
    assert tuple(
        path.relative_to(destination).as_posix() for path in result.copied_paths
    ) == planned_paths
    assert _file_snapshot(destination) == {
        path: source_before[path]
        for path in planned_paths
    }
    assert set(_file_snapshot(destination)) == set(planned_paths)
    assert _file_snapshot(source) == source_before
    assert _staging_paths(destination) == ()


def test_materialize_export_rejects_tampered_compiler_product_before_destination(
    tmp_path: Path,
) -> None:
    source = tmp_path / "workspace"
    destination = tmp_path / "portable"
    spec = create_workspace_spec(
        "Text Lab",
        "Tampered export source proof.",
    )
    build = build_workspace(spec, source)
    plan = build_export_plan(build.repository, build.artifacts, build.manifest)

    tampered_path = source / "generated/capabilities/inspect_text.py"
    tampered_path.write_bytes(b"# changed after export planning\n")

    with pytest.raises(ValueError, match="no longer matches recorded integrity"):
        materialize_export_plan(plan, source, destination)

    assert not destination.exists()
    assert _staging_paths(destination) == ()
    assert tampered_path.read_bytes() == b"# changed after export planning\n"


def test_materialize_export_rejects_missing_planned_evidence_before_destination(
    tmp_path: Path,
) -> None:
    source = tmp_path / "workspace"
    destination = tmp_path / "portable"
    spec = create_workspace_spec(
        "Text Lab",
        "Missing export evidence proof.",
    )
    build = build_workspace(spec, source)
    plan = build_export_plan(build.repository, build.artifacts, build.manifest)

    (source / plan.rir_path).unlink()

    with pytest.raises(FileNotFoundError, match="Planned export source is not a file"):
        materialize_export_plan(plan, source, destination)

    assert not destination.exists()
    assert _staging_paths(destination) == ()


def test_materialize_export_requires_separate_source_and_destination_trees(
    tmp_path: Path,
) -> None:
    source = tmp_path / "workspace"
    spec = create_workspace_spec(
        "Text Lab",
        "Separate export tree proof.",
    )
    build = build_workspace(spec, source)
    plan = build_export_plan(build.repository, build.artifacts, build.manifest)
    source_before = _file_snapshot(source)

    with pytest.raises(ValueError, match="separate trees"):
        materialize_export_plan(plan, source, source / "exports/portable")

    assert _file_snapshot(source) == source_before
    assert not (source / "exports").exists()
