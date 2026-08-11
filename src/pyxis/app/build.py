from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from pyxis.authoring.workspace import WorkspaceSpec
from pyxis.compiler.artifacts import GeneratedArtifact
from pyxis.compiler.materialize import materialize_artifacts
from pyxis.compiler.repository import compile_repository
from pyxis.rir.model import RepositoryIR, build_repository_ir
from pyxis.runtime.loader import run_materialized_workspace


@dataclass(frozen=True, slots=True)
class BuildResult:
    """Observable result of one first-run Workspace build."""

    repository: RepositoryIR
    artifacts: tuple[GeneratedArtifact, ...]
    written_paths: tuple[Path, ...]


@dataclass(frozen=True, slots=True)
class BuildAndRunResult:
    """Observable result of the complete first-run build-and-run operation."""

    build: BuildResult
    runtime_result: dict[str, object]


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


def build_and_run_workspace(
    spec: WorkspaceSpec,
    destination_root: Path,
    text: str,
) -> BuildAndRunResult:
    """Build one Workspace, then execute the materialized generated entrypoint.

    This function deliberately composes the existing first-run build and runtime
    APIs. It contains no compiler, materialization, or runtime implementation of
    its own.
    """

    build = build_workspace(spec, destination_root)
    runtime_result = run_materialized_workspace(
        build.repository,
        destination_root,
        text,
    )

    return BuildAndRunResult(
        build=build,
        runtime_result=runtime_result,
    )
