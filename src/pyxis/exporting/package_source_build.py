from __future__ import annotations

from dataclasses import dataclass
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Literal

from .package_plan import PackageLayoutPlan


_NETWORK_AND_IMPORT_GUARD = (
    "import socket\n"
    "import sys\n\n"
    "class _BlockPyxisImport:\n"
    "    def find_spec(self, fullname, path=None, target=None):\n"
    "        if fullname == \"pyxis\" or fullname.startswith(\"pyxis.\"):\n"
    "            raise RuntimeError(\"Pyxis import attempted during offline source-build observation.\")\n"
    "        return None\n\n"
    "def _pyxis_block_network(*args, **kwargs):\n"
    "    raise RuntimeError(\"Network access attempted during offline source-build observation.\")\n\n"
    "class _PyxisBlockedSocket(socket.socket):\n"
    "    def connect(self, *args, **kwargs):\n"
    "        return _pyxis_block_network(*args, **kwargs)\n"
    "    def connect_ex(self, *args, **kwargs):\n"
    "        return _pyxis_block_network(*args, **kwargs)\n\n"
    "socket.socket = _PyxisBlockedSocket\n"
    "socket.create_connection = _pyxis_block_network\n"
    "socket.getaddrinfo = _pyxis_block_network\n"
    "sys.meta_path.insert(0, _BlockPyxisImport())\n"
)


OfflineSourceBuildOutcome = Literal["built", "failed"]


@dataclass(frozen=True, slots=True)
class OfflineSourceWheelBuildObservation:
    """Observed result of a conventional source-to-wheel attempt with network blocked."""

    portable_root: Path
    project_name: str
    version: str
    outcome: OfflineSourceBuildOutcome
    returncode: int
    wheel_filenames: tuple[str, ...]
    stdout: str
    stderr: str


def _resolve_portable_path(path_value: str, root: Path) -> Path:
    if not path_value:
        raise ValueError("Offline source-build paths must be non-empty.")

    relative = Path(path_value)
    if relative == Path(".") or relative.is_absolute() or ".." in relative.parts:
        raise ValueError(
            f"Offline source-build path must remain relative: {path_value!r}."
        )

    target = (root / relative).resolve()
    if target != root and root not in target.parents:
        raise ValueError(
            f"Offline source-build path escapes the portable root: {path_value!r}."
        )
    return target


def observe_offline_source_wheel_build(
    plan: PackageLayoutPlan,
    portable_root: Path,
) -> OfflineSourceWheelBuildObservation:
    """Attempt the current conventional source build with network access blocked.

    This is a characterization boundary, not a workaround. It preserves PEP 517
    build isolation, does not vendor or inject build dependencies, and does not
    fall back to another backend. Exact planned package bytes are copied into a
    disposable build context so the verified portable tree remains unchanged.
    The subprocess outcome is returned as evidence whether the build succeeds or
    fails under the stated offline condition.
    """

    root = portable_root.resolve()
    if not root.is_dir():
        raise FileNotFoundError(f"Portable package root does not exist: {root}")

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
        raise ValueError("Offline source-build package paths must be unique.")

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
        raise ValueError(
            "Offline source build requires exactly one planned pyproject.toml build metadata file."
        )

    with tempfile.TemporaryDirectory(prefix="pyxis-offline-source-build-") as temporary:
        temporary_root = Path(temporary).resolve()
        build_root = temporary_root / "project"
        wheel_root = temporary_root / "wheelhouse"
        guard_root = temporary_root / "guard"
        build_root.mkdir()
        wheel_root.mkdir()
        guard_root.mkdir()

        for path_value, payload in planned_bytes.items():
            target = _resolve_portable_path(path_value, build_root)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(payload)

        (guard_root / "sitecustomize.py").write_text(
            _NETWORK_AND_IMPORT_GUARD,
            encoding="utf-8",
        )

        environment = os.environ.copy()
        environment.pop("PYTHONHOME", None)
        environment["PYTHONPATH"] = str(guard_root)
        environment["PYTHONNOUSERSITE"] = "1"
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        environment["PIP_NO_INDEX"] = "1"
        environment["PIP_NO_CACHE_DIR"] = "1"
        environment["PIP_DISABLE_PIP_VERSION_CHECK"] = "1"
        environment["PIP_CONFIG_FILE"] = os.devnull

        completed = subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "wheel",
                "--no-index",
                "--no-deps",
                "--disable-pip-version-check",
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
        wheel_filenames = tuple(
            path.name for path in sorted(wheel_root.glob("*.whl"))
        )

    return OfflineSourceWheelBuildObservation(
        portable_root=root,
        project_name=plan.project_name,
        version=plan.version,
        outcome="built" if completed.returncode == 0 else "failed",
        returncode=completed.returncode,
        wheel_filenames=wheel_filenames,
        stdout=completed.stdout,
        stderr=completed.stderr,
    )
