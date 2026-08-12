from __future__ import annotations

from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Literal

from .plan import ExportPlan


_PACKAGE_VERSION = "0.0.0"
_RUNNER_MODULE = "pyxis_workspace"


PackageSupportRole = Literal["build_metadata", "runtime_entrypoint", "package_marker"]


@dataclass(frozen=True, slots=True)
class PackageCompilerProjection:
    """One exact compiler product projected into the installable src layout."""

    source_path: str
    package_path: str
    node_sha256: str
    artifact_sha256: str


@dataclass(frozen=True, slots=True)
class PackageSupportFile:
    """One deterministic packaging-only file, never a compiler product."""

    path: str
    role: PackageSupportRole
    source: str


@dataclass(frozen=True, slots=True)
class PackageLayoutPlan:
    """Pure description of a conventional portable Python repository layout.

    Compiler products are represented only as exact-byte copy projections from
    their already-exported paths into ``src/``. Support files are packaging
    consequences and are kept distinct from compiler products. This plan does
    not read or write files, compile, build a distribution, install, or execute.
    """

    project_name: str
    version: str
    console_script: str
    workspace_module: str
    compiler_projections: tuple[PackageCompilerProjection, ...]
    support_files: tuple[PackageSupportFile, ...]


def _validated_generated_relative(path_value: str) -> PurePosixPath:
    path = PurePosixPath(path_value)
    if path.is_absolute() or ".." in path.parts or len(path.parts) < 2:
        raise ValueError(f"Compiler product path is not safely relative: {path_value!r}.")
    if path.parts[0] != "generated":
        raise ValueError(
            f"Portable packaging currently requires compiler products under generated/: "
            f"{path_value!r}."
        )

    relative = PurePosixPath(*path.parts[1:])
    if relative.suffix != ".py":
        raise ValueError(
            f"Portable Python packaging currently supports Python compiler products only: "
            f"{path_value!r}."
        )
    return relative


def _package_markers(
    projections: tuple[PackageCompilerProjection, ...],
) -> tuple[PackageSupportFile, ...]:
    marker_paths: set[str] = set()

    for projection in projections:
        relative = PurePosixPath(projection.package_path).relative_to("src")
        parents = relative.parent.parts
        for depth in range(1, len(parents) + 1):
            package_parts = parents[:depth]
            if not all(part.isidentifier() for part in package_parts):
                raise ValueError(
                    f"Portable package path contains an invalid Python package name: "
                    f"{projection.package_path!r}."
                )
            marker_paths.add(
                (PurePosixPath("src", *package_parts) / "__init__.py").as_posix()
            )

    return tuple(
        PackageSupportFile(
            path=path,
            role="package_marker",
            source="",
        )
        for path in sorted(marker_paths)
    )


def _runner_source(workspace_module: str, console_script: str) -> str:
    return (
        "from __future__ import annotations\n\n"
        "import argparse\n"
        "import importlib\n"
        "import json\n\n"
        f'_WORKSPACE_MODULE = "{workspace_module}"\n\n\n'
        "def main() -> None:\n"
        f'    parser = argparse.ArgumentParser(prog="{console_script}")\n'
        '    parser.add_argument("text")\n'
        "    args = parser.parse_args()\n\n"
        "    module = importlib.import_module(_WORKSPACE_MODULE)\n"
        '    run_text = getattr(module, "run_text", None)\n'
        "    if not callable(run_text):\n"
        '        raise RuntimeError("Packaged Workspace does not expose callable run_text.")\n\n'
        "    result = run_text(args.text)\n"
        "    if not isinstance(result, dict):\n"
        '        raise RuntimeError("Packaged Workspace returned a non-dict result.")\n'
        "    print(json.dumps(result, indent=2, sort_keys=True))\n\n\n"
        'if __name__ == "__main__":\n'
        "    main()\n"
    )


def _pyproject_source(project_name: str, console_script: str) -> str:
    return (
        "[build-system]\n"
        'requires = ["setuptools>=77.0.3"]\n'
        'build-backend = "setuptools.build_meta"\n\n'
        "[project]\n"
        f'name = "{project_name}"\n'
        f'version = "{_PACKAGE_VERSION}"\n'
        'requires-python = ">=3.11"\n'
        "dependencies = []\n\n"
        "[project.scripts]\n"
        f'{console_script} = "{_RUNNER_MODULE}:main"\n\n'
        "[tool.setuptools]\n"
        'package-dir = {"" = "src"}\n'
        f'py-modules = ["{_RUNNER_MODULE}"]\n\n'
        "[tool.setuptools.packages.find]\n"
        'where = ["src"]\n'
        "namespaces = false\n"
    )


def build_package_layout_plan(export_plan: ExportPlan) -> PackageLayoutPlan:
    """Plan conventional package layout without touching exported bytes."""

    if not export_plan.repository_id:
        raise ValueError("Export plan has no Repository identity for package naming.")
    if not export_plan.workspace_id:
        raise ValueError("Export plan has no Workspace identity for package layout.")

    projections = tuple(
        PackageCompilerProjection(
            source_path=product.path,
            package_path=(
                PurePosixPath("src") / _validated_generated_relative(product.path)
            ).as_posix(),
            node_sha256=product.node_sha256,
            artifact_sha256=product.artifact_sha256,
        )
        for product in export_plan.compiler_products
    )

    projection_paths = tuple(projection.package_path for projection in projections)
    if len(set(projection_paths)) != len(projection_paths):
        raise ValueError("Compiler products map to duplicate portable package paths.")

    workspace_prefix = f"src/workspaces/{export_plan.workspace_id}/"
    workspace_candidates = tuple(
        projection
        for projection in projections
        if projection.package_path.startswith(workspace_prefix)
    )
    if len(workspace_candidates) != 1:
        raise ValueError(
            "Portable packaging requires exactly one Workspace entrypoint compiler product."
        )

    workspace_path = PurePosixPath(workspace_candidates[0].package_path).relative_to("src")
    workspace_module = ".".join(workspace_path.with_suffix("").parts)
    if not all(part.isidentifier() for part in workspace_path.with_suffix("").parts):
        raise ValueError("Workspace entrypoint does not map to a valid Python module name.")

    markers = _package_markers(projections)
    support_files = (
        PackageSupportFile(
            path="pyproject.toml",
            role="build_metadata",
            source=_pyproject_source(
                export_plan.repository_id,
                export_plan.repository_id,
            ),
        ),
        PackageSupportFile(
            path=f"src/{_RUNNER_MODULE}.py",
            role="runtime_entrypoint",
            source=_runner_source(
                workspace_module,
                export_plan.repository_id,
            ),
        ),
        *markers,
    )

    support_paths = tuple(file.path for file in support_files)
    if len(set(support_paths)) != len(support_paths):
        raise ValueError("Portable package support paths must be unique.")
    collision = set(support_paths).intersection(projection_paths)
    if collision:
        raise ValueError(
            f"Packaging support collides with compiler-product projections: "
            f"{sorted(collision)!r}."
        )

    return PackageLayoutPlan(
        project_name=export_plan.repository_id,
        version=_PACKAGE_VERSION,
        console_script=export_plan.repository_id,
        workspace_module=workspace_module,
        compiler_projections=projections,
        support_files=support_files,
    )
