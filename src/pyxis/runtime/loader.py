from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

from pyxis.rir.model import RepositoryIR


def run_materialized_workspace(
    repository: RepositoryIR,
    repository_root: Path,
    text: str,
) -> dict[str, object]:
    """Execute one materialized Workspace entrypoint without compiling or writing.

    The runtime consumes the RIR only to locate the generated Workspace artifact.
    It does not read canonical authoring state, invoke the compiler, or modify the
    materialized repository.
    """

    root = repository_root.resolve()
    generated_root = (root / "generated").resolve()
    entrypoint = (
        generated_root
        / "workspaces"
        / repository.workspace.workspace_id
        / repository.workspace.entrypoint
    ).resolve()

    if generated_root != root and root not in generated_root.parents:
        raise ValueError("Generated root escapes the repository root.")
    if entrypoint != root and root not in entrypoint.parents:
        raise ValueError("Workspace entrypoint escapes the repository root.")
    if not entrypoint.is_file():
        raise FileNotFoundError(
            f"Materialized Workspace entrypoint does not exist: {entrypoint}"
        )

    previous_path = list(sys.path)
    sys.path.insert(0, str(generated_root))

    try:
        spec = importlib.util.spec_from_file_location(
            f"pyxis_generated_{repository.workspace.workspace_id}",
            entrypoint,
        )
        if spec is None or spec.loader is None:
            raise RuntimeError(
                f"Unable to load materialized Workspace entrypoint: {entrypoint}"
            )

        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        run_text = getattr(module, "run_text", None)
        if not callable(run_text):
            raise RuntimeError(
                "Materialized Workspace entrypoint does not expose callable run_text."
            )

        result = run_text(text)
        if not isinstance(result, dict):
            raise RuntimeError("Materialized Workspace returned a non-dict result.")
        return result
    finally:
        sys.path[:] = previous_path
        for module_name in tuple(sys.modules):
            if module_name == "capabilities" or module_name.startswith("capabilities."):
                del sys.modules[module_name]
