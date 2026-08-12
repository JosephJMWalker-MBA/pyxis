from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

from .package_plan import PackageLayoutPlan
from .readiness import ExportVerificationResult


_SUBPROCESS_PROBE = (
    "import importlib.util\n"
    "import runpy\n\n"
    'if importlib.util.find_spec("pyxis") is not None:\n'
    '    raise RuntimeError("Pyxis unexpectedly importable in portable package runtime.")\n\n'
    'runpy.run_module("pyxis_workspace", run_name="__main__")\n'
)


@dataclass(frozen=True, slots=True)
class PackageRuntimeVerificationResult:
    """Evidence that the portable src-layout runtime matches verified export behavior."""

    portable_root: Path
    project_name: str
    workspace_module: str
    input_sha256: str
    expected_result: dict[str, object]
    package_result: dict[str, object]


def verify_package_runtime(
    plan: PackageLayoutPlan,
    export_verification: ExportVerificationResult,
    portable_root: Path,
    text: str,
) -> PackageRuntimeVerificationResult:
    """Run the standalone src-layout package without making Pyxis importable.

    Expected behavior comes only from already-successful export verification for
    the same portable tree and input. The child interpreter disables site-package
    loading, receives only the portable ``src/`` tree through ``PYTHONPATH``, and
    refuses to run if ``pyxis`` is importable. This function does not compile,
    build a distribution, install, or write verification state.
    """

    root = portable_root.resolve()
    if not root.is_dir():
        raise FileNotFoundError(f"Portable package root does not exist: {root}")

    if export_verification.readiness != "READY":
        raise ValueError("Package runtime verification requires READY export evidence.")
    if export_verification.identity.export_root != root:
        raise ValueError("Package runtime verification export root does not match identity evidence.")
    if export_verification.runtime.export_root != root:
        raise ValueError("Package runtime verification export root does not match runtime evidence.")
    if plan.project_name != export_verification.identity.repository_id:
        raise ValueError("Package project identity does not match verified export Repository.")

    input_sha256 = hashlib.sha256(text.encode("utf-8")).hexdigest()
    if input_sha256 != export_verification.runtime.input_sha256:
        raise ValueError("Package runtime verification input does not match verified export input.")

    src_root = (root / "src").resolve()
    runner_path = src_root / "pyxis_workspace.py"
    if not src_root.is_dir() or not runner_path.is_file():
        raise FileNotFoundError("Portable package runtime entrypoint is not materialized.")

    environment = os.environ.copy()
    environment.pop("PYTHONHOME", None)
    environment["PYTHONPATH"] = str(src_root)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    environment["PYTHONNOUSERSITE"] = "1"

    completed = subprocess.run(
        [sys.executable, "-S", "-c", _SUBPROCESS_PROBE, text],
        cwd=root,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise RuntimeError(
            "Portable package runtime subprocess failed"
            + (f": {detail}" if detail else ".")
        )

    try:
        package_result = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError("Portable package runtime returned invalid JSON.") from exc
    if not isinstance(package_result, dict):
        raise RuntimeError("Portable package runtime returned a non-dict JSON result.")

    expected_result = export_verification.runtime.export_result
    if package_result != expected_result:
        raise ValueError("Portable package runtime behavior does not match verified export behavior.")

    return PackageRuntimeVerificationResult(
        portable_root=root,
        project_name=plan.project_name,
        workspace_module=plan.workspace_module,
        input_sha256=input_sha256,
        expected_result=expected_result,
        package_result=package_result,
    )
