from __future__ import annotations

from dataclasses import dataclass
import hashlib
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tempfile
import zipfile

from .package_plan import PackageLayoutPlan


_SITE_CUSTOMIZE = (
    "import sys\n\n"
    "class _BlockPyxisImport:\n"
    "    def find_spec(self, fullname, path=None, target=None):\n"
    "        if fullname == \"pyxis\" or fullname.startswith(\"pyxis.\"):\n"
    "            raise RuntimeError(\"Pyxis import attempted during portable wheel build.\")\n"
    "        return None\n\n"
    "sys.meta_path.insert(0, _BlockPyxisImport())\n"
)


@dataclass(frozen=True, slots=True)
class WheelCompilerProductVerification:
    """Identity evidence for one compiler product recovered from a built wheel."""

    package_path: str
    wheel_member: str
    node_sha256: str
    artifact_sha256: str


@dataclass(frozen=True, slots=True)
class PackageWheelBuildResult:
    """Evidence that a conventional wheel was built from the portable package."""

    portable_root: Path
    wheel_path: Path
    project_name: str
    version: str
    wheel_sha256: str
    compiler_products: tuple[WheelCompilerProductVerification, ...]


def _resolve_portable_path(path_value: str, root: Path) -> Path:
    if not path_value:
        raise ValueError("Wheel build paths must be non-empty.")

    relative = Path(path_value)
    if relative == Path(".") or relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"Wheel build path must remain relative: {path_value!r}.")

    target = (root / relative).resolve()
    if target != root and root not in target.parents:
        raise ValueError(f"Wheel build path escapes the portable root: {path_value!r}.")
    return target


def _wheel_member_for_src_path(path_value: str) -> str:
    path = PurePosixPath(path_value)
    if path.is_absolute() or ".." in path.parts or len(path.parts) < 2:
        raise ValueError(f"Wheel package path is not safely relative: {path_value!r}.")
    if path.parts[0] != "src":
        raise ValueError(f"Wheel package path must be under src/: {path_value!r}.")
    return PurePosixPath(*path.parts[1:]).as_posix()


def build_package_wheel(
    plan: PackageLayoutPlan,
    portable_root: Path,
    wheel_directory: Path,
) -> PackageWheelBuildResult:
    """Build and inspect one standard wheel without allowing Pyxis participation.

    The materialized package surface is fully preflighted before output mutation.
    Exact planned bytes are copied into a temporary build context so backend
    scratch files cannot modify the portable repository. ``pip wheel`` performs
    the conventional PEP 517 build with isolation enabled. A ``sitecustomize``
    guard rejects any attempted ``pyxis`` import in the pip/build subprocesses.
    The resulting wheel is accepted only when its Python payload contains exactly
    the planned package Python files and every compiler product matches its
    recorded artifact hash. This function does not install the wheel or claim
    installability/READY state.
    """

    root = portable_root.resolve()
    wheel_root = wheel_directory.resolve()
    if not root.is_dir():
        raise FileNotFoundError(f"Portable package root does not exist: {root}")
    if (
        root == wheel_root
        or root in wheel_root.parents
        or wheel_root in root.parents
    ):
        raise ValueError("Wheel output and portable package must be separate trees.")
    if wheel_root.exists():
        raise FileExistsError(f"Wheel output directory already exists: {wheel_root}")

    compiler_paths = tuple(
        _resolve_portable_path(projection.package_path, root)
        for projection in plan.compiler_projections
    )
    support_paths = tuple(
        _resolve_portable_path(support.path, root)
        for support in plan.support_files
    )
    planned_paths = (*compiler_paths, *support_paths)
    if len(set(planned_paths)) != len(planned_paths):
        raise ValueError("Wheel build package paths must be unique.")

    planned_bytes: dict[str, bytes] = {}
    for projection, path in zip(plan.compiler_projections, compiler_paths, strict=True):
        if not path.is_file():
            raise FileNotFoundError(
                f"Materialized compiler projection is not a file: {projection.package_path!r}."
            )
        payload = path.read_bytes()
        if hashlib.sha256(payload).hexdigest() != projection.artifact_sha256:
            raise ValueError(
                f"Materialized compiler projection no longer matches recorded integrity: "
                f"{projection.package_path!r}."
            )
        planned_bytes[projection.package_path] = payload

    for support, path in zip(plan.support_files, support_paths, strict=True):
        if not path.is_file():
            raise FileNotFoundError(
                f"Materialized package support is not a file: {support.path!r}."
            )
        payload = path.read_bytes()
        expected = support.source.encode("utf-8")
        if payload != expected:
            raise ValueError(
                f"Materialized package support no longer matches its plan: {support.path!r}."
            )
        planned_bytes[support.path] = payload

    pyproject_files = tuple(
        support
        for support in plan.support_files
        if support.role == "build_metadata" and support.path == "pyproject.toml"
    )
    if len(pyproject_files) != 1:
        raise ValueError("Wheel build requires exactly one planned pyproject.toml build metadata file.")

    wheel_root.mkdir(parents=True, exist_ok=False)
    try:
        with tempfile.TemporaryDirectory(prefix="pyxis-wheel-build-") as temporary:
            temporary_root = Path(temporary).resolve()
            build_root = temporary_root / "project"
            guard_root = temporary_root / "guard"
            build_root.mkdir()
            guard_root.mkdir()

            for path_value, payload in planned_bytes.items():
                target = _resolve_portable_path(path_value, build_root)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(payload)

            (guard_root / "sitecustomize.py").write_text(
                _SITE_CUSTOMIZE,
                encoding="utf-8",
            )

            environment = os.environ.copy()
            environment.pop("PYTHONHOME", None)
            environment["PYTHONPATH"] = str(guard_root)
            environment["PYTHONNOUSERSITE"] = "1"
            environment["PYTHONDONTWRITEBYTECODE"] = "1"
            environment["PIP_DISABLE_PIP_VERSION_CHECK"] = "1"

            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "wheel",
                    "--no-deps",
                    "--wheel-dir",
                    str(wheel_root),
                    ".",
                ],
                cwd=build_root,
                env=environment,
                capture_output=True,
                text=True,
                check=False,
            )
            if completed.returncode != 0:
                detail = completed.stderr.strip() or completed.stdout.strip()
                raise RuntimeError(
                    "Portable wheel build subprocess failed"
                    + (f": {detail}" if detail else ".")
                )

        wheel_paths = tuple(sorted(wheel_root.glob("*.whl")))
        if len(wheel_paths) != 1:
            raise RuntimeError(
                f"Portable wheel build produced {len(wheel_paths)} wheel files; expected exactly one."
            )
        wheel_path = wheel_paths[0]

        verified_products: list[WheelCompilerProductVerification] = []
        expected_python_members = {
            _wheel_member_for_src_path(projection.package_path)
            for projection in plan.compiler_projections
        }
        expected_python_members.update(
            _wheel_member_for_src_path(support.path)
            for support in plan.support_files
            if support.path.startswith("src/") and support.path.endswith(".py")
        )

        with zipfile.ZipFile(wheel_path, "r") as archive:
            members = set(archive.namelist())
            actual_python_members = {member for member in members if member.endswith(".py")}
            if actual_python_members != expected_python_members:
                raise ValueError(
                    "Built wheel Python payload does not exactly match the planned package files."
                )

            for projection in plan.compiler_projections:
                wheel_member = _wheel_member_for_src_path(projection.package_path)
                try:
                    payload = archive.read(wheel_member)
                except KeyError as exc:
                    raise ValueError(
                        f"Built wheel is missing compiler product: {wheel_member!r}."
                    ) from exc
                artifact_sha256 = hashlib.sha256(payload).hexdigest()
                if artifact_sha256 != projection.artifact_sha256:
                    raise ValueError(
                        f"Built wheel compiler product identity mismatch: {wheel_member!r}."
                    )
                verified_products.append(
                    WheelCompilerProductVerification(
                        package_path=projection.package_path,
                        wheel_member=wheel_member,
                        node_sha256=projection.node_sha256,
                        artifact_sha256=artifact_sha256,
                    )
                )

            for support in plan.support_files:
                if not (support.path.startswith("src/") and support.path.endswith(".py")):
                    continue
                wheel_member = _wheel_member_for_src_path(support.path)
                if archive.read(wheel_member) != support.source.encode("utf-8"):
                    raise ValueError(
                        f"Built wheel package support differs from its plan: {wheel_member!r}."
                    )

            entry_point_members = tuple(
                member for member in members if member.endswith(".dist-info/entry_points.txt")
            )
            if len(entry_point_members) != 1:
                raise ValueError("Built wheel does not contain exactly one console-entrypoint record.")
            entry_points = archive.read(entry_point_members[0]).decode("utf-8")
            expected_entrypoint = f"{plan.console_script} = pyxis_workspace:main"
            if expected_entrypoint not in entry_points:
                raise ValueError("Built wheel console entrypoint does not match the package plan.")

        return PackageWheelBuildResult(
            portable_root=root,
            wheel_path=wheel_path.resolve(),
            project_name=plan.project_name,
            version=plan.version,
            wheel_sha256=hashlib.sha256(wheel_path.read_bytes()).hexdigest(),
            compiler_products=tuple(verified_products),
        )
    except Exception:
        shutil.rmtree(wheel_root, ignore_errors=True)
        raise
