from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from pyxis.authoring import load_workspace_spec
from pyxis.revisions import (
    RevisionEvent,
    append_revision_event,
    create_revision_event,
    revision_head_id,
)

from .build import BuildResult, build_workspace
from .preview import ArchitecturePreview, preview_remove_normalize_text


_REMOVE_NORMALIZE_OPERATION = "remove_capability:normalize_text"


@dataclass(frozen=True, slots=True)
class ApplyResult:
    """Observable result of applying one previously previewed architecture edit."""

    revision: RevisionEvent
    revision_log_path: Path
    build: BuildResult


def apply_remove_normalize_text(
    preview: ArchitecturePreview,
    destination_root: Path,
    rationale: str,
) -> ApplyResult:
    """Apply the previewed normalize_text removal through permanent boundaries.

    Apply first confirms that persisted canonical state still matches the state
    that was previewed. It then appends intent-bearing revision provenance before
    delegating canonical mutation and compilation to the existing build path.
    """

    current_spec = load_workspace_spec(destination_root)
    if current_spec != preview.current_spec:
        raise ValueError("Preview no longer matches current canonical Workspace state.")

    expected_preview = preview_remove_normalize_text(current_spec)
    if preview != expected_preview:
        raise ValueError("Preview does not match the supported architecture edit.")

    revision = create_revision_event(
        current_spec,
        preview.proposed_spec,
        _REMOVE_NORMALIZE_OPERATION,
        rationale,
        parent_revision_id=revision_head_id(destination_root),
    )
    revision_log_path = append_revision_event(revision, destination_root)
    build = build_workspace(preview.proposed_spec, destination_root)

    return ApplyResult(
        revision=revision,
        revision_log_path=revision_log_path,
        build=build,
    )
