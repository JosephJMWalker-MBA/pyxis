from __future__ import annotations

import json
from pathlib import Path

from .model import REVISION_SCHEMA_VERSION, RevisionCompletion, RevisionEvent


_REVISION_LOG_PATH = Path("revisions/events.jsonl")
_REVISION_COMPLETION_LOG_PATH = Path("revisions/completions.jsonl")
_REVISION_EVENT_KEYS = {
    "schema_version",
    "revision_id",
    "parent_revision_id",
    "operation",
    "rationale",
    "before_canonical_sha256",
    "after_canonical_sha256",
}
_REVISION_COMPLETION_KEYS = {
    "schema_version",
    "revision_id",
    "after_canonical_sha256",
    "rir_sha256",
    "generation_manifest_sha256",
}


def _read_revision_events(log_path: Path) -> tuple[RevisionEvent, ...]:
    if not log_path.exists():
        return ()

    events: list[RevisionEvent] = []
    revision_ids: set[str] = set()
    expected_parent: str | None = None

    for line_number, line in enumerate(
        log_path.read_text(encoding="utf-8").splitlines(),
        start=1,
    ):
        if not line:
            raise ValueError(f"Revision log contains an empty line at {line_number}.")

        payload = json.loads(line)
        if not isinstance(payload, dict) or set(payload) != _REVISION_EVENT_KEYS:
            raise ValueError(f"Revision log entry {line_number} has an invalid shape.")

        schema_version = payload["schema_version"]
        revision_id = payload["revision_id"]
        parent_revision_id = payload["parent_revision_id"]
        operation = payload["operation"]
        rationale = payload["rationale"]
        before_canonical_sha256 = payload["before_canonical_sha256"]
        after_canonical_sha256 = payload["after_canonical_sha256"]

        if schema_version != REVISION_SCHEMA_VERSION:
            raise ValueError(
                f"Revision log entry {line_number} has an unsupported schema version."
            )
        if not all(
            isinstance(value, str) and value
            for value in (
                revision_id,
                operation,
                rationale,
                before_canonical_sha256,
                after_canonical_sha256,
            )
        ):
            raise ValueError(
                f"Revision log entry {line_number} contains invalid values."
            )
        if parent_revision_id is not None and (
            not isinstance(parent_revision_id, str) or not parent_revision_id
        ):
            raise ValueError(
                f"Revision log entry {line_number} has an invalid parent_revision_id."
            )
        if parent_revision_id != expected_parent:
            raise ValueError(
                f"Revision log chain is invalid at entry {line_number}."
            )
        if revision_id in revision_ids:
            raise ValueError(
                f"Revision log contains duplicate revision_id {revision_id!r}."
            )

        event = RevisionEvent(
            schema_version=schema_version,
            revision_id=revision_id,
            parent_revision_id=parent_revision_id,
            operation=operation,
            rationale=rationale,
            before_canonical_sha256=before_canonical_sha256,
            after_canonical_sha256=after_canonical_sha256,
        )
        events.append(event)
        revision_ids.add(revision_id)
        expected_parent = revision_id

    return tuple(events)


def _read_revision_completions(
    log_path: Path,
) -> tuple[RevisionCompletion, ...]:
    if not log_path.exists():
        return ()

    completions: list[RevisionCompletion] = []
    revision_ids: set[str] = set()

    for line_number, line in enumerate(
        log_path.read_text(encoding="utf-8").splitlines(),
        start=1,
    ):
        if not line:
            raise ValueError(
                f"Revision completion log contains an empty line at {line_number}."
            )

        payload = json.loads(line)
        if not isinstance(payload, dict) or set(payload) != _REVISION_COMPLETION_KEYS:
            raise ValueError(
                f"Revision completion entry {line_number} has an invalid shape."
            )

        schema_version = payload["schema_version"]
        revision_id = payload["revision_id"]
        after_canonical_sha256 = payload["after_canonical_sha256"]
        rir_sha256 = payload["rir_sha256"]
        generation_manifest_sha256 = payload["generation_manifest_sha256"]
        if schema_version != REVISION_SCHEMA_VERSION:
            raise ValueError(
                f"Revision completion entry {line_number} has an unsupported schema version."
            )
        if not all(
            isinstance(value, str) and value
            for value in (
                revision_id,
                after_canonical_sha256,
                rir_sha256,
                generation_manifest_sha256,
            )
        ):
            raise ValueError(
                f"Revision completion entry {line_number} contains invalid values."
            )
        if revision_id in revision_ids:
            raise ValueError(
                f"Revision completion log repeats revision_id {revision_id!r}."
            )

        completions.append(
            RevisionCompletion(
                schema_version=schema_version,
                revision_id=revision_id,
                after_canonical_sha256=after_canonical_sha256,
                rir_sha256=rir_sha256,
                generation_manifest_sha256=generation_manifest_sha256,
            )
        )
        revision_ids.add(revision_id)

    return tuple(completions)


def load_revision_events(workspace_root: Path) -> tuple[RevisionEvent, ...]:
    """Load the append-only revision chain without mutating Workspace state."""

    return _read_revision_events(
        workspace_root.resolve() / _REVISION_LOG_PATH
    )


def load_revision_completions(
    workspace_root: Path,
) -> tuple[RevisionCompletion, ...]:
    """Load revision completion evidence and require matching persisted events."""

    root = workspace_root.resolve()
    events = _read_revision_events(root / _REVISION_LOG_PATH)
    completions = _read_revision_completions(root / _REVISION_COMPLETION_LOG_PATH)
    events_by_id = {event.revision_id: event for event in events}

    for completion in completions:
        event = events_by_id.get(completion.revision_id)
        if event is None:
            raise ValueError("Revision completion references an unknown revision.")
        if completion.schema_version != event.schema_version:
            raise ValueError("Revision completion schema does not match its event.")
        if completion.after_canonical_sha256 != event.after_canonical_sha256:
            raise ValueError("Revision completion canonical hash does not match its event.")

    return completions


def revision_head_id(workspace_root: Path) -> str | None:
    """Return the current append-only revision chain head without mutation."""

    events = load_revision_events(workspace_root)
    return events[-1].revision_id if events else None


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
    events = _read_revision_events(log_path)
    expected_parent = events[-1].revision_id if events else None
    revision_ids = {existing.revision_id for existing in events}

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


def append_revision_completion(
    completion: RevisionCompletion,
    workspace_root: Path,
) -> Path:
    """Append compiler completion evidence for one previously recorded revision."""

    root = workspace_root.resolve()
    completion_log_path = root / _REVISION_COMPLETION_LOG_PATH
    events = load_revision_events(root)
    revision = next(
        (
            event
            for event in events
            if event.revision_id == completion.revision_id
        ),
        None,
    )
    if revision is None:
        raise ValueError("Completion references an unknown revision.")
    if revision.schema_version != completion.schema_version:
        raise ValueError("Completion schema does not match the revision event.")
    if revision.after_canonical_sha256 != completion.after_canonical_sha256:
        raise ValueError("Completion canonical hash does not match the revision event.")

    existing_completions = load_revision_completions(root)
    if any(
        existing.revision_id == completion.revision_id
        for existing in existing_completions
    ):
        raise ValueError(
            f"Revision {completion.revision_id!r} already has completion evidence."
        )

    completion_log_path.parent.mkdir(parents=True, exist_ok=True)
    serialized = json.dumps(
        completion.to_dict(),
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    with completion_log_path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(f"{serialized}\n")

    return completion_log_path
