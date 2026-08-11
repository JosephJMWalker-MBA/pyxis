from __future__ import annotations

import json
from pathlib import Path

from .model import RevisionEvent


_REVISION_LOG_PATH = Path("revisions/events.jsonl")


def _existing_revision_ids(log_path: Path) -> tuple[str, ...]:
    if not log_path.exists():
        return ()

    revision_ids: list[str] = []
    expected_parent: str | None = None

    for line_number, line in enumerate(
        log_path.read_text(encoding="utf-8").splitlines(),
        start=1,
    ):
        if not line:
            raise ValueError(f"Revision log contains an empty line at {line_number}.")

        payload = json.loads(line)
        revision_id = payload.get("revision_id")
        parent_revision_id = payload.get("parent_revision_id")

        if not isinstance(revision_id, str) or not revision_id:
            raise ValueError(
                f"Revision log entry {line_number} has no valid revision_id."
            )
        if parent_revision_id != expected_parent:
            raise ValueError(
                f"Revision log chain is invalid at entry {line_number}."
            )
        if revision_id in revision_ids:
            raise ValueError(
                f"Revision log contains duplicate revision_id {revision_id!r}."
            )

        revision_ids.append(revision_id)
        expected_parent = revision_id

    return tuple(revision_ids)


def revision_head_id(workspace_root: Path) -> str | None:
    """Return the current append-only revision chain head without mutation."""

    log_path = workspace_root.resolve() / _REVISION_LOG_PATH
    revision_ids = _existing_revision_ids(log_path)
    return revision_ids[-1] if revision_ids else None


def append_revision_event(
    event: RevisionEvent,
    workspace_root: Path,
) -> Path:
    """Append one immutable event while preserving the existing revision chain.

    Existing bytes are never rewritten. The event must name the current chain
    head as its parent (or no parent for the first event).
    """

    root = workspace_root.resolve()
    log_path = root / _REVISION_LOG_PATH
    revision_ids = _existing_revision_ids(log_path)
    expected_parent = revision_ids[-1] if revision_ids else None

    if event.parent_revision_id != expected_parent:
        raise ValueError(
            "Revision parent does not match the current append-only chain head."
        )
    if event.revision_id in revision_ids:
        raise ValueError(f"Revision {event.revision_id!r} is already recorded.")

    log_path.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(
        event.to_dict(),
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    with log_path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(f"{serialized}\n")

    return log_path
