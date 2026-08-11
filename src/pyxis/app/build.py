from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from pyxis.authoring.workspace import WorkspaceSpec
from pyxis.compiler.artifacts import GeneratedArtifact
from pyxis.compiler.materialize import materialize_artifacts
from pyxis.compiler.repository import compile_repository
from pyxis.rir.model import RepositoryIR, build_repository_ir


@dataclass(frozen=True, slots=True)
class BuildResult:
    """Observable result of one first-run Workspace build."""

    repository: RepositoryIR
    artifacts: tuple[GeneratedArtifact, ...]
    written_paths: tuple[Path, ...]


def build_workspace(
    spec: WorkspaceSpec,
    destination_root: Path,
) -> BuildResult:
    """Lower, compile, and materialize one authored Workspace.

    This is orchestration only. Each transformation remains owned by its
    existing layer: authoring supplies the spec, RIR lowering supplies the
    repository model, the compiler supplies immutable artifacts, and the
    materializer owns filesystem writes.
    """

    repository = build_repository_ir(spec)
    artifacts = compile_repository(repository)
    written_paths = materialize_artifacts(artifacts, destination_root)

    return BuildResult(
        repository=repository,
        artifacts=artifacts,
        written_paths=written_paths,
    )
