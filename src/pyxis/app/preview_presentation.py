from __future__ import annotations

from dataclasses import dataclass

from pyxis.authoring import WorkspaceSpec
from pyxis.revisions import canonical_sha256

from .preview import ArchitecturePreview


@dataclass(frozen=True, slots=True)
class CanonicalPreviewPresentation:
    """One canonical state identity shown in an architectural preview."""

    workspace_id: str
    name: str
    description: str
    capabilities: tuple[str, ...]
    canonical_sha256: str


@dataclass(frozen=True, slots=True)
class ArchitecturePreviewPresentation:
    """Immutable presentation-safe evidence for one proposed architecture edit."""

    current: CanonicalPreviewPresentation
    proposed: CanonicalPreviewPresentation
    added_capabilities: tuple[str, ...]
    removed_capabilities: tuple[str, ...]
    added_artifact_paths: tuple[str, ...]
    changed_artifact_paths: tuple[str, ...]
    removed_artifact_paths: tuple[str, ...]
    current_runtime_keys: tuple[str, ...]
    proposed_runtime_keys: tuple[str, ...]
    added_runtime_keys: tuple[str, ...]
    removed_runtime_keys: tuple[str, ...]


def _present_canonical(spec: WorkspaceSpec) -> CanonicalPreviewPresentation:
    return CanonicalPreviewPresentation(
        workspace_id=spec.workspace_id,
        name=spec.name,
        description=spec.description,
        capabilities=spec.capabilities,
        canonical_sha256=canonical_sha256(spec),
    )


def create_architecture_preview_presentation(
    preview: ArchitecturePreview,
) -> ArchitecturePreviewPresentation:
    """Adapt an existing in-memory ArchitecturePreview for presentation only.

    The adapter derives no compiler or runtime implementation facts. It copies
    structural consequences already owned by ArchitecturePreview and exposes the
    observable runtime-key contract directly implied by current/proposed
    canonical capability declarations.
    """

    current = preview.current_spec
    proposed = preview.proposed_spec
    proposed_workspace = preview.proposed_repository.workspace

    if (
        current.workspace_id != proposed.workspace_id
        or current.name != proposed.name
        or current.description != proposed.description
    ):
        raise ValueError(
            "Architecture preview may change capabilities but not Workspace identity."
        )

    if (
        proposed_workspace.workspace_id != proposed.workspace_id
        or proposed_workspace.name != proposed.name
        or proposed_workspace.description != proposed.description
        or proposed_workspace.capabilities != proposed.capabilities
    ):
        raise ValueError(
            "Architecture preview proposed RIR does not match proposed canonical intent."
        )

    actual_added_capabilities = tuple(
        capability
        for capability in proposed.capabilities
        if capability not in current.capabilities
    )
    actual_removed_capabilities = tuple(
        capability
        for capability in current.capabilities
        if capability not in proposed.capabilities
    )
    if preview.delta.added_capabilities != actual_added_capabilities:
        raise ValueError(
            "Architecture preview added-capability evidence does not match canonical delta."
        )
    if preview.delta.removed_capabilities != actual_removed_capabilities:
        raise ValueError(
            "Architecture preview removed-capability evidence does not match canonical delta."
        )
    if preview.delta.added_runtime_keys != actual_added_capabilities:
        raise ValueError(
            "Architecture preview added runtime-key evidence does not match canonical capabilities."
        )
    if preview.delta.removed_runtime_keys != actual_removed_capabilities:
        raise ValueError(
            "Architecture preview removed runtime-key evidence does not match canonical capabilities."
        )

    return ArchitecturePreviewPresentation(
        current=_present_canonical(current),
        proposed=_present_canonical(proposed),
        added_capabilities=preview.delta.added_capabilities,
        removed_capabilities=preview.delta.removed_capabilities,
        added_artifact_paths=preview.delta.added_artifact_paths,
        changed_artifact_paths=preview.delta.changed_artifact_paths,
        removed_artifact_paths=preview.delta.removed_artifact_paths,
        current_runtime_keys=current.capabilities,
        proposed_runtime_keys=proposed.capabilities,
        added_runtime_keys=preview.delta.added_runtime_keys,
        removed_runtime_keys=preview.delta.removed_runtime_keys,
    )
