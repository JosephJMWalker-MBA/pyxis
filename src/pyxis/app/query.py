from __future__ import annotations

from pathlib import Path

from pyxis.authoring import load_workspace_spec
from pyxis.compiler import load_generation_manifest
from pyxis.revisions import load_revision_completions, load_revision_events
from pyxis.rir import load_repository_ir

from .build import BuildAndRunResult
from .export import WorkspaceExportResult
from .presentation import WorkspacePresentation, create_workspace_presentation


def query_workspace_presentation(
    workspace_root: Path,
    *,
    run: BuildAndRunResult | None = None,
    export: WorkspaceExportResult | None = None,
) -> WorkspacePresentation:
    """Assemble one existing Workspace presentation from durable and live evidence.

    Canonical state, persisted RIR, generation manifest, and revision history are
    loaded through their owning read boundaries. Runtime output and generation
    statuses are intentionally not reconstructed because they are transient
    facts; callers must supply the current BuildAndRunResult. Export READY
    evidence is likewise included only when the actual WorkspaceExportResult is
    supplied.

    This function does not compile, execute generated code, classify generation
    status, verify an export, or discover evidence from arbitrary files.
    """

    if run is None:
        raise ValueError(
            "Workspace presentation requires a supplied BuildAndRunResult; "
            "runtime output and generation statuses are transient and are not "
            "reconstructed from persisted files."
        )

    root = workspace_root.resolve()
    spec = load_workspace_spec(root)
    persisted_repository = load_repository_ir(root)
    persisted_manifest = load_generation_manifest(root)
    if persisted_manifest is None:
        raise FileNotFoundError(
            "Generation manifest does not exist for the existing Workspace."
        )

    if run.build.repository != persisted_repository:
        raise ValueError("Supplied run RIR does not match the persisted Workspace RIR.")
    if run.build.manifest != persisted_manifest:
        raise ValueError(
            "Supplied run generation manifest does not match persisted compiler evidence."
        )

    revision_events = load_revision_events(root)
    revision_completions = load_revision_completions(root)

    if export is not None:
        if export.verification.runtime.source_root != root:
            raise ValueError("Supplied export evidence belongs to a different source Workspace.")
        if (
            export.materialization.destination_root
            != export.verification.identity.export_root
        ):
            raise ValueError(
                "Supplied export materialization and verification refer to different roots."
            )

    return create_workspace_presentation(
        spec,
        run,
        revision_events=revision_events,
        revision_completions=revision_completions,
        export=export,
    )
