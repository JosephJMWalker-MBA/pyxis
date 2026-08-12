from __future__ import annotations

import json
from pathlib import Path

from .model import RIR_SCHEMA_VERSION, RepositoryIR, WorkspaceIR


_REPOSITORY_RIR_PATH = Path("generated/repository.rir.json")


def load_repository_ir(workspace_root: Path) -> RepositoryIR:
    """Load persisted Repository IR without deriving or compiling anything."""

    rir_path = workspace_root.resolve() / _REPOSITORY_RIR_PATH
    if not rir_path.exists():
        raise FileNotFoundError(f"Repository RIR does not exist: {rir_path}")

    payload = json.loads(rir_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or set(payload) != {
        "schema_version",
        "repository_id",
        "workspace",
    }:
        raise ValueError("Repository RIR has an invalid top-level shape.")

    schema_version = payload["schema_version"]
    repository_id = payload["repository_id"]
    raw_workspace = payload["workspace"]
    if schema_version != RIR_SCHEMA_VERSION:
        raise ValueError("Repository RIR has an unsupported schema version.")
    if not isinstance(repository_id, str) or not repository_id:
        raise ValueError("Repository RIR has no valid repository_id.")
    if not isinstance(raw_workspace, dict) or set(raw_workspace) != {
        "workspace_id",
        "name",
        "description",
        "entrypoint",
        "capabilities",
    }:
        raise ValueError("Repository RIR Workspace has an invalid shape.")

    workspace_id = raw_workspace["workspace_id"]
    name = raw_workspace["name"]
    description = raw_workspace["description"]
    entrypoint = raw_workspace["entrypoint"]
    capabilities = raw_workspace["capabilities"]
    if not all(
        isinstance(value, str) and value
        for value in (workspace_id, name, description, entrypoint)
    ):
        raise ValueError("Repository RIR Workspace identity fields are invalid.")
    if not isinstance(capabilities, list) or not all(
        isinstance(capability, str) and capability
        for capability in capabilities
    ):
        raise ValueError("Repository RIR Workspace capabilities are invalid.")
    if len(set(capabilities)) != len(capabilities):
        raise ValueError("Repository RIR Workspace capabilities must be unique.")

    return RepositoryIR(
        schema_version=schema_version,
        repository_id=repository_id,
        workspace=WorkspaceIR(
            workspace_id=workspace_id,
            name=name,
            description=description,
            entrypoint=entrypoint,
            capabilities=tuple(capabilities),
        ),
    )


def persist_repository_ir(
    repository: RepositoryIR,
    workspace_root: Path,
) -> Path:
    """Persist derived Repository IR as deterministic inspectable JSON.

    This is an RIR filesystem boundary. It writes only the already-derived
    compiler input for inspection; it does not read canonical authoring state,
    compile artifacts, or execute generated code.
    """

    root = workspace_root.resolve()
    rir_path = root / _REPOSITORY_RIR_PATH
    rir_path.parent.mkdir(parents=True, exist_ok=True)

    payload = json.dumps(
        repository.to_dict(),
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    )
    rir_path.write_text(f"{payload}\n", encoding="utf-8")
    return rir_path
