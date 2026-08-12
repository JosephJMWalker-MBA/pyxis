from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
import time
from typing import Literal

from pyxis.authoring.workspace import WorkspaceSpec
from pyxis.compiler.status import ArtifactGenerationStatus

from .build import BuildAndRunResult, build_and_run_workspace


MeasurementStage = Literal["build", "runtime"]
MeasurementClock = Callable[[], float]


@dataclass(frozen=True, slots=True)
class StageDurationEvidence:
    """Elapsed time observed for one established application stage."""

    stage: MeasurementStage
    duration_seconds: float

    def __post_init__(self) -> None:
        if self.duration_seconds < 0:
            raise ValueError("Stage duration cannot be negative.")


@dataclass(frozen=True, slots=True)
class BuildWorkEvidence:
    """Compiler/materialization work facts already owned by one BuildResult."""

    generation_statuses: tuple[ArtifactGenerationStatus, ...]
    written_paths: tuple[Path, ...]
    reused_paths: tuple[Path, ...]
    removed_paths: tuple[Path, ...]


@dataclass(frozen=True, slots=True)
class BuildAndRunMeasurementEvidence:
    """Immutable measurement evidence for one build-and-run cycle."""

    stages: tuple[StageDurationEvidence, ...]
    build_work: BuildWorkEvidence


@dataclass(frozen=True, slots=True)
class MeasuredBuildAndRunResult:
    """Existing build/run evidence paired with measurement evidence."""

    result: BuildAndRunResult
    measurement: BuildAndRunMeasurementEvidence


def measure_build_and_run_workspace(
    spec: WorkspaceSpec,
    destination_root: Path,
    text: str,
    *,
    clock: MeasurementClock = time.monotonic,
) -> MeasuredBuildAndRunResult:
    """Measure the existing build-and-run operation without replacing it.

    Timing observes only the established build and runtime boundaries exposed by
    ``build_and_run_workspace``. Compiler/materialization work evidence is copied
    directly from the returned ``BuildResult``; this layer performs no filesystem
    discovery and makes no independent work or waste classification.
    """

    started_at: dict[MeasurementStage, float] = {}
    stages: list[StageDurationEvidence] = []

    def observe(stage: MeasurementStage, boundary: Literal["start", "end"]) -> None:
        if boundary == "start":
            if stage in started_at:
                raise RuntimeError(f"Measurement stage already started: {stage}")
            started_at[stage] = clock()
            return

        start = started_at.pop(stage, None)
        if start is None:
            raise RuntimeError(f"Measurement stage ended before start: {stage}")
        stages.append(
            StageDurationEvidence(
                stage=stage,
                duration_seconds=clock() - start,
            )
        )

    result = build_and_run_workspace(
        spec,
        destination_root,
        text,
        _stage_observer=observe,
    )

    if started_at:
        raise RuntimeError("Measurement stage did not complete.")
    if tuple(stage.stage for stage in stages) != ("build", "runtime"):
        raise RuntimeError("Build-and-run measurement stage ordering changed.")

    build = result.build
    measurement = BuildAndRunMeasurementEvidence(
        stages=tuple(stages),
        build_work=BuildWorkEvidence(
            generation_statuses=build.generation_statuses,
            written_paths=build.written_paths,
            reused_paths=build.reused_paths,
            removed_paths=build.removed_paths,
        ),
    )
    return MeasuredBuildAndRunResult(
        result=result,
        measurement=measurement,
    )
