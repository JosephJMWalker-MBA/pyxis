from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from pyxis.authoring.persistence import persist_workspace_spec
from pyxis.authoring.workspace import WorkspaceSpec
from pyxis.compiler.artifacts import GeneratedArtifact
from pyxis.compiler.manifest import (
    GenerationManifest,
    build_generation_manifest,
    persist_generation_manifest,
)
from pyxis.compiler.materialize import materialize_artifacts
from pyxis.compiler.repository import compile_repository
from pyxis.rir.model import RepositoryIR, build_repository_ir
from pyxis.rir.persistence import persist_repository_ir
from pyxis.runtime.loader import run_materialized_workspace


@dataclass(frozen=True, slots=True)
class BuildResult:
    """Observable result of one first-run Workspace build."""

    canonical_path: Path
    repository: RepositoryIR
    rir_path: Path
    artifacts: tuple[GeneratedArtifact, ...]
    manifest: GenerationManifest
    manifest_path: Path
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
    """Persist, lower, compile, record evidence, and materialize one Workspace.

    This is orchestration only. Each transformation remains owned by its
    existing layer: authoring persists canonical intent, RIR lowering supplies
    and persists the derived repository model, the compiler supplies immutable
    artifacts and their manifest evidence, and the materializer owns generated
    implementation writes.
    """

    canonical_path = persist_workspace_spec(spec, destination_root)
    repository = build_repository_ir(spec)
    rir_path = persist_repository_ir(repository, destination_root)
    artifacts = compile_repository(repository)
    manifest = build_generation_manifest(repository, artifacts)
    manifest_path = persist_generation_manifest(manifest, destination_root)
    written_paths = materialize_artifacts(artifacts, destination_root)

    return BuildResult(
        canonical_path=canonical_path,
        repository=repository,
        rir_path=rir_path,
        artifacts=artifacts,
        manifest=manifest,
        manifest_path=manifest_path,
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
