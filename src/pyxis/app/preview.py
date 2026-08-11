from __future__ import annotations

from dataclasses import dataclass

from pyxis.authoring.workspace import WorkspaceSpec
from pyxis.rir.model import RepositoryIR, build_repository_ir


_NORMALIZE_TEXT_CAPABILITY = "normalize_text"
_NORMALIZE_TEXT_ARTIFACT_PATH = "generated/capabilities/normalize_text.py"


@dataclass(frozen=True, slots=True)
class ArchitectureDelta:
    """Predicted structural consequences of one proposed architecture edit."""

    added_capabilities: tuple[str, ...]
    removed_capabilities: tuple[str, ...]
    added_artifact_paths: tuple[str, ...]
    changed_artifact_paths: tuple[str, ...]
    removed_artifact_paths: tuple[str, ...]
    added_runtime_keys: tuple[str, ...]
    removed_runtime_keys: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ArchitecturePreview:
    """One non-mutating proposed canonical/RIR state and its predicted delta."""

    current_spec: WorkspaceSpec
    proposed_spec: WorkspaceSpec
    proposed_repository: RepositoryIR
    delta: ArchitectureDelta


def preview_remove_normalize_text(spec: WorkspaceSpec) -> ArchitecturePreview:
    """Preview removing normalize_text without persisting or compiling anything.

    The proposed WorkspaceSpec and RepositoryIR exist only in memory. Artifact
    impact is limited to structure directly implied by the edit, and runtime
    prediction is limited to capability result keys implied by canonical state.
    """

    proposed_spec = spec.without_capability(_NORMALIZE_TEXT_CAPABILITY)
    proposed_repository = build_repository_ir(proposed_spec)
    workspace_entrypoint_path = (
        "generated/workspaces/"
        f"{proposed_repository.workspace.workspace_id}/"
        f"{proposed_repository.workspace.entrypoint}"
    )

    return ArchitecturePreview(
        current_spec=spec,
        proposed_spec=proposed_spec,
        proposed_repository=proposed_repository,
        delta=ArchitectureDelta(
            added_capabilities=(),
            removed_capabilities=(_NORMALIZE_TEXT_CAPABILITY,),
            added_artifact_paths=(),
            changed_artifact_paths=(workspace_entrypoint_path,),
            removed_artifact_paths=(_NORMALIZE_TEXT_ARTIFACT_PATH,),
            added_runtime_keys=(),
            removed_runtime_keys=(_NORMALIZE_TEXT_CAPABILITY,),
        ),
    )
