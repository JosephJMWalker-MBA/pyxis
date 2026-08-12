from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from pyxis.authoring.persistence import persist_workspace_spec
from pyxis.authoring.workspace import WorkspaceSpec
from pyxis.compiler.artifacts import GeneratedArtifact
from pyxis.compiler.manifest import (
    GenerationManifest,
    build_generation_manifest,
    load_generation_manifest,
    persist_generation_manifest,
)
from pyxis.compiler.materialize import (
    inspect_materialized_artifact_integrity,
    reconcile_materialized_artifacts,
)
from pyxis.compiler.repository import compile_repository
from pyxis.compiler.status import (
    ArtifactGenerationStatus,
    classify_generation_statuses,
)
from pyxis.rir.model import RepositoryIR, build_repository_ir
from pyxis.rir.persistence import persist_repository_ir
from pyxis.runtime.loader import run_materialized_workspace


_BuildAndRunStage = Literal["build", "runtime"]
_StageBoundary = Literal["start", "end"]
_StageObserver = Callable[[_BuildAndRunStage, _StageBoundary], None]


@dataclass(frozen=True, slots=True)
class BuildResult:
    """Observable result of one Workspace build."""

    canonical_path: Path
    repository: RepositoryIR
    rir_path: Path
    artifacts: tuple[GeneratedArtifact, ...]
    manifest: GenerationManifest
    generation_statuses: tuple[ArtifactGenerationStatus, ...]
    manifest_path: Path
    written_paths: tuple[Path, ...]
    reused_paths: tuple[Path, ...]
    removed_paths: tuple[Path, ...]


@dataclass(frozen=True, slots=True)
class BuildAndRunResult:
    """Observable result of the complete first-run build-and-run operation."""

    build: BuildResult
    runtime_result: dict[str, object]


def build_workspace(
    spec: WorkspaceSpec,
    destination_root: Path,
) -> BuildResult:
    """Persist, lower, compile, classify, reconcile, and record one Workspace.

    This is orchestration only. Each transformation remains owned by its
    existing layer: authoring persists canonical intent, RIR lowering supplies
    and persists the derived repository model, the compiler supplies immutable
    artifacts, manifest evidence, and generation statuses, and the materializer
    consumes those statuses while reconciling only compiler-owned paths proven
    by the prior manifest.
    """

    previous_manifest = load_generation_manifest(destination_root)
    existing_integrity = inspect_materialized_artifact_integrity(
        previous_manifest,
        destination_root,
    )
    canonical_path = persist_workspace_spec(spec, destination_root)
    repository = build_repository_ir(spec)
    rir_path = persist_repository_ir(repository, destination_root)
    artifacts = compile_repository(repository)
    manifest = build_generation_manifest(repository, artifacts)
    generation_statuses = classify_generation_statuses(
        artifacts,
        previous_manifest,
        existing_integrity,
    )
    materialization = reconcile_materialized_artifacts(
        artifacts,
        generation_statuses,
        previous_manifest,
        destination_root,
    )
    manifest_path = persist_generation_manifest(manifest, destination_root)

    return BuildResult(
        canonical_path=canonical_path,
        repository=repository,
        rir_path=rir_path,
        artifacts=artifacts,
        manifest=manifest,
        generation_statuses=generation_statuses,
        manifest_path=manifest_path,
        written_paths=materialization.written_paths,
        reused_paths=materialization.reused_paths,
        removed_paths=materialization.removed_paths,
    )


def _observe_stage(
    observer: _StageObserver | None,
    stage: _BuildAndRunStage,
    boundary: _StageBoundary,
) -> None:
    if observer is not None:
        observer(stage, boundary)


def build_and_run_workspace(
    spec: WorkspaceSpec,
    destination_root: Path,
    text: str,
    *,
    _stage_observer: _StageObserver | None = None,
) -> BuildAndRunResult:
    """Build one Workspace, then execute the materialized generated entrypoint.

    This function deliberately composes the existing first-run build and runtime
    APIs. It contains no compiler, materialization, or runtime implementation of
    its own. The private stage observer exists only so application-owned
    measurement can time these established boundaries without duplicating the
    orchestration path.
    """

    _observe_stage(_stage_observer, "build", "start")
    build = build_workspace(spec, destination_root)
    _observe_stage(_stage_observer, "build", "end")

    _observe_stage(_stage_observer, "runtime", "start")
    runtime_result = run_materialized_workspace(
        build.repository,
        destination_root,
        text,
    )
    _observe_stage(_stage_observer, "runtime", "end")

    return BuildAndRunResult(
        build=build,
        runtime_result=runtime_result,
    )
