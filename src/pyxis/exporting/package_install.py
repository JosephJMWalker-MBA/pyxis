from __future__ import annotations

from dataclasses import dataclass
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
from typing import Literal
import venv

from .package_plan import PackageLayoutPlan
from .package_runtime import PackageRuntimeVerificationResult
from .package_wheel import PackageWheelBuildResult


_INSTALLATION_MODE = "offline-wheel"

_NETWORK_AND_IMPORT_GUARD = (
    "import socket\n"
    "import sys\n\n"
    "class _BlockPyxisImport:\n"
    "    def find_spec(self, fullname, path=None, target=None):\n"
    "        if fullname == \"pyxis\" or fullname.startswith(\"pyxis.\"):\n"
    "            raise RuntimeError(\"Pyxis import attempted during offline installation proof.\")\n"
    "        return None\n\n"
    "def _pyxis_block_network(*args, **kwargs):\n"
    "    raise RuntimeError(\"Network access attempted during offline installation proof.\")\n\n"
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

_ISOLATION_PROBE = (
    "import importlib.util\n"
    "import socket\n\n"
    "if importlib.util.find_spec(\"pyxis\") is not None:\n"
    "    raise RuntimeError(\"Pyxis unexpectedly importable in fresh installation environment.\")\n"
    "if socket.create_connection.__name__ != \"_pyxis_block_network\":\n"
    "    raise RuntimeError(\"Offline network guard is not active.\")\n"
)

_INSTALLED_PROBE = (
    "import importlib.util\n"
    "import socket\n\n"
    "if importlib.util.find_spec(\"pyxis\") is not None:\n"
    "    raise RuntimeError(\"Installed wheel unexpectedly exposes Pyxis.\")\n"
    "if importlib.util.find_spec(\"pyxis_workspace\") is None:\n"
    "    raise RuntimeError(\"Installed wheel does not expose its standalone runner.\")\n"
    "if socket.create_connection.__name__ != \"_pyxis_block_network\":\n"
    "    raise RuntimeError(\"Offline network guard is not active after installation.\")\n"
)


PackageInstallationMode = Literal["offline-wheel"]


@dataclass(frozen=True, slots=True)
class PackageInstallationVerificationResult:
    """Evidence that one verified wheel installs and runs in a fresh offline venv."""

    project_name: str
    version: str
    wheel_sha256: str
    input_sha256: str
    installation_mode: PackageInstallationMode
    expected_result: dict[str, object]
    installed_result: dict[str, object]


def _venv_python(environment_root: Path) -> Path:
    if os.name == "nt":
        return environment_root / "Scripts" / "python.exe"
    return environment_root / "bin" / "python"


def _venv_scripts(environment_root: Path) -> Path:
    if os.name == "nt":
        return environment_root / "Scripts"
    return environment_root / "bin"


def _run_checked(
    command: list[str],
    *,
    cwd: Path,
    environment: dict[str, str],
    failure_message: str,
) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(
        command,
        cwd=cwd,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise RuntimeError(
            failure_message + (f": {detail}" if detail else ".")
        )
    return completed


def verify_package_installation(
    plan: PackageLayoutPlan,
    wheel_build: PackageWheelBuildResult,
    package_runtime: PackageRuntimeVerificationResult,
    text: str,
) -> PackageInstallationVerificationResult:
    """Install a verified wheel offline in a fresh venv and execute its console script.

    This function consumes only already-proven package/wheel evidence plus the
    wheel file itself. It never rebuilds the package. The local wheel is installed
    with pip index access disabled and dependencies forbidden. A startup guard
    blocks network resolution/connections and any import of ``pyxis`` in the
    installation and execution subprocesses. The temporary environment is removed
    after verification and no READY state is broadened by this proof.
    """

    wheel_path = wheel_build.wheel_path.resolve()
    if not wheel_path.is_file():
        raise FileNotFoundError(f"Verified wheel does not exist: {wheel_path}")

    actual_wheel_sha256 = hashlib.sha256(wheel_path.read_bytes()).hexdigest()
    if actual_wheel_sha256 != wheel_build.wheel_sha256:
        raise ValueError("Verified wheel bytes no longer match wheel-build evidence.")

    if plan.project_name != wheel_build.project_name:
        raise ValueError("Package project name does not match wheel-build evidence.")
    if plan.version != wheel_build.version:
        raise ValueError("Package version does not match wheel-build evidence.")
    if plan.project_name != package_runtime.project_name:
        raise ValueError("Package project name does not match package-runtime evidence.")
    if wheel_build.portable_root != package_runtime.portable_root:
        raise ValueError("Wheel-build and package-runtime evidence refer to different portable roots.")

    expected_products = tuple(
        (
            projection.package_path,
            projection.node_sha256,
            projection.artifact_sha256,
        )
        for projection in plan.compiler_projections
    )
    wheel_products = tuple(
        (
            product.package_path,
            product.node_sha256,
            product.artifact_sha256,
        )
        for product in wheel_build.compiler_products
    )
    if wheel_products != expected_products:
        raise ValueError("Wheel compiler-product evidence does not match the package plan.")

    input_sha256 = hashlib.sha256(text.encode("utf-8")).hexdigest()
    if input_sha256 != package_runtime.input_sha256:
        raise ValueError("Installation verification input does not match package-runtime evidence.")
    if package_runtime.package_result != package_runtime.expected_result:
        raise ValueError("Package-runtime evidence is internally inconsistent.")

    with tempfile.TemporaryDirectory(prefix="pyxis-offline-install-") as temporary:
        temporary_root = Path(temporary).resolve()
        environment_root = temporary_root / "venv"
        guard_root = temporary_root / "guard"
        execution_root = temporary_root / "run"
        guard_root.mkdir()
        execution_root.mkdir()

        venv.EnvBuilder(
            with_pip=True,
            system_site_packages=False,
            clear=True,
        ).create(environment_root)

        python_path = _venv_python(environment_root)
        scripts_root = _venv_scripts(environment_root)
        if not python_path.is_file():
            raise RuntimeError("Fresh installation environment has no Python interpreter.")

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
        environment["PIP_DISABLE_PIP_VERSION_CHECK"] = "1"
        environment["PIP_NO_CACHE_DIR"] = "1"
        environment["PIP_CONFIG_FILE"] = os.devnull

        _run_checked(
            [str(python_path), "-c", _ISOLATION_PROBE],
            cwd=execution_root,
            environment=environment,
            failure_message="Fresh installation isolation probe failed",
        )

        _run_checked(
            [
                str(python_path),
                "-m",
                "pip",
                "install",
                "--no-index",
                "--no-deps",
                "--no-compile",
                "--disable-pip-version-check",
                str(wheel_path),
            ],
            cwd=execution_root,
            environment=environment,
            failure_message="Offline wheel installation failed",
        )

        _run_checked(
            [str(python_path), "-c", _INSTALLED_PROBE],
            cwd=execution_root,
            environment=environment,
            failure_message="Installed-package isolation probe failed",
        )

        console_path_value = shutil.which(
            plan.console_script,
            path=str(scripts_root),
        )
        if console_path_value is None:
            raise RuntimeError("Installed wheel did not create the planned console command.")

        completed = _run_checked(
            [console_path_value, text],
            cwd=execution_root,
            environment=environment,
            failure_message="Installed console command failed",
        )

        try:
            installed_result = json.loads(completed.stdout)
        except json.JSONDecodeError as exc:
            raise RuntimeError("Installed console command returned invalid JSON.") from exc
        if not isinstance(installed_result, dict):
            raise RuntimeError("Installed console command returned a non-dict JSON result.")

    expected_result = package_runtime.package_result
    if installed_result != expected_result:
        raise ValueError("Installed wheel behavior does not match verified package behavior.")

    return PackageInstallationVerificationResult(
        project_name=plan.project_name,
        version=plan.version,
        wheel_sha256=actual_wheel_sha256,
        input_sha256=input_sha256,
        installation_mode=_INSTALLATION_MODE,
        expected_result=expected_result,
        installed_result=installed_result,
    )
