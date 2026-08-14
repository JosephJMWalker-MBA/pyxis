from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from pyxis.authoring import WorkspaceSpec, load_workspace_spec
from pyxis.compiler import generation_manifest_sha256
from pyxis.revisions import (
    RevisionCompletion,
    RevisionEvent,
    append_revision_completion,
    append_revision_event,
    create_revision_completion,
    create_revision_event,
    revision_head_id,
)

from .build import BuildResult, build_workspace
from .preview import (
    ArchitecturePreview,
    preview_add_split_lines,
    preview_remove_normalize_text,
    preview_restore_normalize_text,
)


_REMOVE_NORMALIZE_OPERATION = "remove_capability:normalize_text"
_RESTORE_NORMALIZE_OPERATION = "restore_capability:normalize_text"
_ADD_SPLIT_LINES_OPERATION = "add_capability:split_lines"


@dataclass(frozen=True, slots=True)
class ApplyResult:
    """Observable result of applying one previously previewed architecture edit."""

    revision: RevisionEvent
    revision_log_path: Path
    build: BuildResult
    completion: RevisionCompletion
    completion_log_path: Path


def _apply_previewed_edit(
    preview: ArchitecturePreview,
    destination_root: Path,
    rationale: str,
    *,
    operation: str,
    preview_builder: Callable[[WorkspaceSpec], ArchitecturePreview],
) -> ApplyResult:
    """Apply one validated preview through shared permanent governance boundaries."""

    current_spec = load_workspace_spec(destination_root)
    if current_spec != preview.current_spec:
        raise ValueError("Preview no longer matches current canonical Workspace state.")

    expected_preview = preview_builder(current_spec)
    if preview != expected_preview:
        raise ValueError("Preview does not match the supported architecture edit.")

    revision = create_revision_event(
        current_spec,
        preview.proposed_spec,
        operation,
        rationale,
        parent_revision_id=revision_head_id(destination_root),
    )
    revision_log_path = append_revision_event(revision, destination_root)
    build = build_workspace(preview.proposed_spec, destination_root)
    completion = create_revision_completion(
        revision,
        after_canonical_sha256=revision.after_canonical_sha256,
        rir_sha256=build.manifest.rir_sha256,
        generation_manifest_sha256=generation_manifest_sha256(build.manifest),
    )
    completion_log_path = append_revision_completion(completion, destination_root)

    return ApplyResult(
        revision=revision,
        revision_log_path=revision_log_path,
        build=build,
        completion=completion,
        completion_log_path=completion_log_path,
    )


def apply_remove_normalize_text(
    preview: ArchitecturePreview,
    destination_root: Path,
    rationale: str,
) -> ApplyResult:
    """Apply the previewed normalize_text removal through permanent boundaries."""

    return _apply_previewed_edit(
        preview,
        destination_root,
        rationale,
        operation=_REMOVE_NORMALIZE_OPERATION,
        preview_builder=preview_remove_normalize_text,
    )


def apply_restore_normalize_text(
    preview: ArchitecturePreview,
    destination_root: Path,
    rationale: str,
) -> ApplyResult:
    """Apply the previewed normalize_text restoration as a new forward revision."""

    return _apply_previewed_edit(
        preview,
        destination_root,
        rationale,
        operation=_RESTORE_NORMALIZE_OPERATION,
        preview_builder=preview_restore_normalize_text,
    )


def apply_add_split_lines(
    preview: ArchitecturePreview,
    destination_root: Path,
    rationale: str,
) -> ApplyResult:
    """Apply the previewed split_lines addition through permanent boundaries."""

    return _apply_previewed_edit(
        preview,
        destination_root,
        rationale,
        operation=_ADD_SPLIT_LINES_OPERATION,
        preview_builder=preview_add_split_lines,
    )
