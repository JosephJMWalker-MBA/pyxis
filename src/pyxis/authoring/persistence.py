from __future__ import annotations

import json
from pathlib import Path

from .workspace import WorkspaceSpec


_CANONICAL_WORKSPACE_PATH = Path("authoring/canonical/workspace.json")


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
