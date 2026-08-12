from __future__ import annotations

from collections.abc import Mapping
import json

from textual.app import App, ComposeResult
from textual.containers import Vertical, VerticalScroll
from textual.widgets import Static

from pyxis.app.presentation import (
    CompilerArtifactPresentation,
    ExportPresentation,
    RevisionPresentation,
    WorkspacePresentation,
)


def _format_capabilities(capabilities: tuple[str, ...]) -> str:
    if not capabilities:
        return "—"
    return "\n".join(f"- {capability}" for capability in capabilities)


def _format_optional(value: str | None) -> str:
    return value if value is not None else "—"


def _runtime_to_builtin(value: object) -> object:
    if isinstance(value, Mapping):
        return {
            str(key): _runtime_to_builtin(item)
            for key, item in value.items()
        }
    if isinstance(value, tuple):
        return [_runtime_to_builtin(item) for item in value]
    return value


def _format_runtime(presentation: WorkspacePresentation) -> str:
    return json.dumps(
        _runtime_to_builtin(presentation.runtime_result),
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    )


def _format_artifact(artifact: CompilerArtifactPresentation) -> str:
    return "\n".join(
        (
            f"Path: {artifact.path}",
            f"Status: {artifact.status}",
            f"Node SHA-256: {_format_optional(artifact.node_sha256)}",
            f"Artifact SHA-256: {_format_optional(artifact.artifact_sha256)}",
        )
    )


def _format_artifacts(presentation: WorkspacePresentation) -> str:
    if not presentation.artifacts:
        return "No compiler artifact evidence."
    return "\n\n".join(
        _format_artifact(artifact)
        for artifact in presentation.artifacts
    )


def _format_revision(revision: RevisionPresentation, index: int) -> str:
    return "\n".join(
        (
            f"Revision {index}",
            f"Revision ID: {revision.revision_id}",
            f"Parent revision ID: {_format_optional(revision.parent_revision_id)}",
            f"Operation: {revision.operation}",
            f"Rationale: {revision.rationale}",
            f"Before canonical SHA-256: {revision.before_canonical_sha256}",
            f"After canonical SHA-256: {revision.after_canonical_sha256}",
            f"Completed: {'yes' if revision.completed else 'no'}",
            "Completion RIR SHA-256: "
            f"{_format_optional(revision.completion_rir_sha256)}",
            "Completion generation manifest SHA-256: "
            f"{_format_optional(revision.completion_generation_manifest_sha256)}",
        )
    )


def _format_revisions(presentation: WorkspacePresentation) -> str:
    if not presentation.revisions:
        return "No revision evidence."
    return "\n\n".join(
        _format_revision(revision, index)
        for index, revision in enumerate(presentation.revisions, start=1)
    )


def _format_export(export: ExportPresentation | None) -> str:
    if export is None:
        return "No READY evidence."
    return "\n".join(
        (
            f"Readiness: {export.readiness}",
            f"Export root: {export.export_root}",
            f"RIR SHA-256: {export.rir_sha256}",
            "Generation manifest SHA-256: "
            f"{export.generation_manifest_sha256}",
            f"Verification input SHA-256: {export.input_sha256}",
            f"Compiler product count: {export.compiler_product_count}",
        )
    )


class WorkspaceDetail(VerticalScroll):
    """Complete read-only renderer for one immutable Workspace presentation."""

    def __init__(self, presentation: WorkspacePresentation) -> None:
        super().__init__(id="workspace-detail")
        self.presentation = presentation

    def compose(self) -> ComposeResult:
        presentation = self.presentation
        canonical = presentation.canonical
        rir = presentation.rir
        export_evidence = (
            "READY"
            if presentation.export is not None
            else "No READY evidence"
        )

        with Vertical(id="workspace-summary"):
            yield Static("Pyxis Workspace", id="shell-title")
            yield Static(canonical.name, id="workspace-name", markup=False)
            yield Static(
                canonical.description,
                id="workspace-description",
                markup=False,
            )
            yield Static(
                f"Repository: {rir.repository_id}",
                id="repository-identity",
                markup=False,
            )
            yield Static(
                f"Compiler evidence: {len(presentation.artifacts)} artifacts",
                id="compiler-evidence",
                markup=False,
            )
            yield Static(
                f"Revision evidence: {len(presentation.revisions)} events",
                id="revision-evidence",
                markup=False,
            )
            yield Static(
                f"Export evidence: {export_evidence}",
                id="export-evidence",
                markup=False,
            )

        with Vertical(classes="evidence-section", id="canonical-section"):
            yield Static("Canonical intent", classes="section-title")
            yield Static(
                "\n".join(
                    (
                        f"Workspace ID: {canonical.workspace_id}",
                        f"Name: {canonical.name}",
                        f"Description: {canonical.description}",
                        "Capabilities:",
                        _format_capabilities(canonical.capabilities),
                        f"Canonical SHA-256: {canonical.canonical_sha256}",
                    )
                ),
                id="canonical-evidence",
                classes="evidence-body",
                markup=False,
            )

        with Vertical(classes="evidence-section", id="rir-section"):
            yield Static("Repository Intermediate Representation", classes="section-title")
            yield Static(
                "\n".join(
                    (
                        f"Schema version: {rir.schema_version}",
                        f"Repository ID: {rir.repository_id}",
                        f"Workspace ID: {rir.workspace_id}",
                        f"Entrypoint: {rir.entrypoint}",
                        "Capabilities:",
                        _format_capabilities(rir.capabilities),
                        f"RIR SHA-256: {rir.rir_sha256}",
                    )
                ),
                id="rir-evidence",
                classes="evidence-body",
                markup=False,
            )

        with Vertical(classes="evidence-section", id="compiler-section"):
            yield Static("Compiler artifacts", classes="section-title")
            yield Static(
                _format_artifacts(presentation),
                id="compiler-artifacts",
                classes="evidence-body",
                markup=False,
            )

        with Vertical(classes="evidence-section", id="runtime-section"):
            yield Static("Runtime result", classes="section-title")
            yield Static(
                _format_runtime(presentation),
                id="runtime-result",
                classes="evidence-body",
                markup=False,
            )

        with Vertical(classes="evidence-section", id="revisions-section"):
            yield Static("Revision timeline", classes="section-title")
            yield Static(
                _format_revisions(presentation),
                id="revision-timeline",
                classes="evidence-body",
                markup=False,
            )

        with Vertical(classes="evidence-section", id="export-section"):
            yield Static("Export verification", classes="section-title")
            yield Static(
                _format_export(presentation.export),
                id="export-verification",
                classes="evidence-body",
                markup=False,
            )


class WorkspaceShell(App[None]):
    """Textual application shell over one immutable Workspace presentation.

    The shell renders application-owned evidence only. It does not load a
    Workspace, compile, execute runtime code, query revision files, export, or
    infer READY state.
    """

    TITLE = "Pyxis"
    SUB_TITLE = "Workspace evidence"
    CSS = """
    Screen {
        align: center top;
    }

    #workspace-detail {
        width: 94%;
        height: 100%;
        padding: 1 2 2 2;
    }

    #workspace-summary,
    .evidence-section {
        width: 100%;
        height: auto;
        padding: 1 2;
        margin-bottom: 1;
        border: round $primary;
    }

    #workspace-name,
    .section-title {
        text-style: bold;
    }

    .section-title {
        margin-bottom: 1;
    }

    .evidence-body {
        width: 100%;
        height: auto;
    }
    """

    def __init__(self, presentation: WorkspacePresentation) -> None:
        super().__init__()
        self.presentation = presentation

    def compose(self) -> ComposeResult:
        yield WorkspaceDetail(self.presentation)


def create_workspace_shell(presentation: WorkspacePresentation) -> WorkspaceShell:
    """Create the local read-only UI shell without acquiring or changing evidence."""

    return WorkspaceShell(presentation)
