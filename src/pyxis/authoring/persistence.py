from __future__ import annotations

import json
from pathlib import Path

from .workspace import WorkspaceSpec


_CANONICAL_WORKSPACE_PATH = Path("authoring/canonical/workspace.json")


def load_workspace_spec(workspace_root: Path) -> WorkspaceSpec:
    """Load authoritative Workspace intent from canonical persisted state.

    This is an authoring read boundary. It does not inspect generated output,
    lower RIR, compile artifacts, or execute runtime behavior.
    """

    canonical_path = workspace_root.resolve() / _CANONICAL_WORKSPACE_PATH
    if not canonical_path.exists():
        raise FileNotFoundError(
            f"Canonical Workspace state does not exist: {canonical_path}"
        )

    payload = json.loads(canonical_path.read_text(encoding="utf-8"))
    expected_keys = {"workspace_id", "name", "description", "capabilities"}
    if not isinstance(payload, dict) or set(payload) != expected_keys:
        raise ValueError("Canonical Workspace state has an invalid shape.")

    workspace_id = payload["workspace_id"]
    name = payload["name"]
    description = payload["description"]
    capabilities = payload["capabilities"]

    if not all(
        isinstance(value, str) and value
        for value in (workspace_id, name, description)
    ):
        raise ValueError("Canonical Workspace identity fields must be non-empty strings.")
    if not isinstance(capabilities, list) or not all(
        isinstance(capability, str) and capability
        for capability in capabilities
    ):
        raise ValueError("Canonical Workspace capabilities must be non-empty strings.")
    if len(set(capabilities)) != len(capabilities):
        raise ValueError("Canonical Workspace capabilities must be unique.")

    return WorkspaceSpec(
        workspace_id=workspace_id,
        name=name,
        description=description,
        capabilities=tuple(capabilities),
    )


def persist_workspace_spec(
    spec: WorkspaceSpec,
    workspace_root: Path,
) -> Path:
    """Persist authoritative Workspace intent as deterministic canonical JSON.

    This is an authoring filesystem boundary. It writes only canonical authoring
    state; it does not lower RIR, compile artifacts, or touch generated output.
    """

    root = workspace_root.resolve()
    canonical_path = root / _CANONICAL_WORKSPACE_PATH
    canonical_path.parent.mkdir(parents=True, exist_ok=True)

    payload = json.dumps(
        spec.to_canonical_dict(),
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    )
    canonical_path.write_text(f"{payload}\n", encoding="utf-8")
    return canonical_path
