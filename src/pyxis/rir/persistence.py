from __future__ import annotations

import json
from pathlib import Path

from .model import RepositoryIR


_REPOSITORY_RIR_PATH = Path("generated/repository.rir.json")


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
