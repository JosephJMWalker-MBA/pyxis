import ast
from dataclasses import replace
from pathlib import Path
import tomllib

import pytest

from pyxis.authoring import create_workspace_spec
from pyxis.compiler import build_generation_manifest, compile_repository
from pyxis.exporting import (
    ExportCompilerProduct,
    build_export_plan,
    build_package_layout_plan,
)
from pyxis.rir import build_repository_ir


def _export_plan():
    spec = create_workspace_spec(
        "Text Lab",
        "Conventional portable package layout proof.",
    )
    repository = build_repository_ir(spec)
    artifacts = compile_repository(repository)
    manifest = build_generation_manifest(repository, artifacts)
    return build_export_plan(repository, artifacts, manifest)


def _support_by_path(package_plan):
    return {support.path: support for support in package_plan.support_files}


def test_package_layout_plan_is_pure_deterministic_and_conventional(
    tmp_path: Path,
    monkeypatch,
) -> None:
    export_plan = _export_plan()
    monkeypatch.chdir(tmp_path)

    first = build_package_layout_plan(export_plan)
    second = build_package_layout_plan(export_plan)

    assert first == second
    assert first.project_name == "text-lab"
    assert first.version == "0.0.0"
    assert first.console_script == "text-lab"
    assert first.workspace_module == "workspaces.text_lab.main"
    assert tuple(
        (projection.source_path, projection.package_path)
        for projection in first.compiler_projections
    ) == (
        (
            "generated/capabilities/inspect_text.py",
            "src/capabilities/inspect_text.py",
        ),
        (
            "generated/capabilities/normalize_text.py",
            "src/capabilities/normalize_text.py",
        ),
        (
            "generated/workspaces/text_lab/main.py",
            "src/workspaces/text_lab/main.py",
        ),
    )
    assert tuple(support.path for support in first.support_files) == (
        "pyproject.toml",
        "src/pyxis_workspace.py",
        "src/capabilities/__init__.py",
        "src/workspaces/__init__.py",
        "src/workspaces/text_lab/__init__.py",
    )
    assert not tuple(tmp_path.rglob("*"))


def test_package_layout_plan_preserves_compiler_identity_without_source_regeneration() -> None:
    export_plan = _export_plan()

    package_plan = build_package_layout_plan(export_plan)

    assert tuple(
        (
            projection.source_path,
            projection.node_sha256,
            projection.artifact_sha256,
        )
        for projection in package_plan.compiler_projections
    ) == tuple(
        (product.path, product.node_sha256, product.artifact_sha256)
        for product in export_plan.compiler_products
    )
    assert all(
        not hasattr(projection, "source")
        for projection in package_plan.compiler_projections
    )
    assert not set(
        projection.package_path for projection in package_plan.compiler_projections
    ).intersection(support.path for support in package_plan.support_files)


def test_package_layout_plan_support_files_form_standalone_setuptools_src_layout() -> None:
    package_plan = build_package_layout_plan(_export_plan())
    support = _support_by_path(package_plan)

    pyproject = tomllib.loads(support["pyproject.toml"].source)
    assert pyproject["build-system"] == {
        "requires": ["setuptools>=77.0.3"],
        "build-backend": "setuptools.build_meta",
    }
    assert pyproject["project"]["name"] == "text-lab"
    assert pyproject["project"]["version"] == "0.0.0"
    assert pyproject["project"]["requires-python"] == ">=3.11"
    assert pyproject["project"]["dependencies"] == []
    assert pyproject["project"]["scripts"] == {
        "text-lab": "pyxis_workspace:main"
    }
    assert pyproject["tool"]["setuptools"]["package-dir"] == {"": "src"}
    assert pyproject["tool"]["setuptools"]["py-modules"] == ["pyxis_workspace"]
    assert pyproject["tool"]["setuptools"]["packages"]["find"] == {
        "where": ["src"],
        "namespaces": False,
    }

    runner_source = support["src/pyxis_workspace.py"].source
    ast.parse(runner_source)
    assert '_WORKSPACE_MODULE = "workspaces.text_lab.main"' in runner_source
    assert "import pyxis" not in runner_source
    assert "from pyxis" not in runner_source
    assert all(
        support[path].source == ""
        for path in (
            "src/capabilities/__init__.py",
            "src/workspaces/__init__.py",
            "src/workspaces/text_lab/__init__.py",
        )
    )


def test_package_layout_plan_rejects_non_generated_compiler_product() -> None:
    export_plan = _export_plan()
    original = export_plan.compiler_products[0]
    unsupported = ExportCompilerProduct(
        path="outside/inspect_text.py",
        node_sha256=original.node_sha256,
        artifact_sha256=original.artifact_sha256,
    )
    changed = replace(
        export_plan,
        compiler_products=(unsupported, *export_plan.compiler_products[1:]),
    )

    with pytest.raises(ValueError, match="requires compiler products under generated"):
        build_package_layout_plan(changed)


def test_package_layout_plan_rejects_non_python_compiler_product() -> None:
    export_plan = _export_plan()
    original = export_plan.compiler_products[0]
    unsupported = ExportCompilerProduct(
        path="generated/capabilities/inspect_text.bin",
        node_sha256=original.node_sha256,
        artifact_sha256=original.artifact_sha256,
    )
    changed = replace(
        export_plan,
        compiler_products=(unsupported, *export_plan.compiler_products[1:]),
    )

    with pytest.raises(ValueError, match="Python compiler products only"):
        build_package_layout_plan(changed)
