from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
import time
from typing import Literal

from pyxis.authoring.workspace import WorkspaceSpec
from pyxis.compiler.status import ArtifactGenerationStatus, GenerationStatus

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


@dataclass(frozen=True, slots=True)
class StageDurationComparisonEvidence:
    """Literal before/after duration evidence for one matching stage."""

    stage: MeasurementStage
    before_seconds: float
    after_seconds: float
    delta_seconds: float

    def __post_init__(self) -> None:
        if self.before_seconds < 0 or self.after_seconds < 0:
            raise ValueError("Compared stage durations cannot be negative.")
        if self.delta_seconds != self.after_seconds - self.before_seconds:
            raise ValueError("Stage duration delta must equal after minus before.")


@dataclass(frozen=True, slots=True)
class ArtifactGenerationStatusComparisonEvidence:
    """Literal compiler-owned status transition for one artifact path."""

    path: str
    before_status: GenerationStatus | None
    after_status: GenerationStatus | None


@dataclass(frozen=True, slots=True)
class BuildWorkComparisonEvidence:
    """Before/after work facts plus path-level compiler status transitions."""

    before: BuildWorkEvidence
    after: BuildWorkEvidence
    artifact_statuses: tuple[ArtifactGenerationStatusComparisonEvidence, ...]


@dataclass(frozen=True, slots=True)
class BuildAndRunMeasurementComparisonEvidence:
    """Pure factual comparison of two already-measured build-and-run cycles."""

    stages: tuple[StageDurationComparisonEvidence, ...]
    build_work: BuildWorkComparisonEvidence


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


def compare_build_and_run_measurements(
    before: MeasuredBuildAndRunResult,
    after: MeasuredBuildAndRunResult,
) -> BuildAndRunMeasurementComparisonEvidence:
    """Compare two measured cycles without inferring cause, quality, or waste.

    This function performs no execution, filesystem access, reclassification, or
    scoring. Duration deltas mean only ``after - before``. Work comparison carries
    the exact immutable evidence already observed for each cycle and reports only
    literal compiler-status transitions by artifact path.
    """

    before_stages = before.measurement.stages
    after_stages = after.measurement.stages
    before_stage_names = tuple(stage.stage for stage in before_stages)
    after_stage_names = tuple(stage.stage for stage in after_stages)
    if before_stage_names != after_stage_names:
        raise ValueError("Measured cycles must contain the same ordered stages.")

    stages = tuple(
        StageDurationComparisonEvidence(
            stage=before_stage.stage,
            before_seconds=before_stage.duration_seconds,
            after_seconds=after_stage.duration_seconds,
            delta_seconds=after_stage.duration_seconds - before_stage.duration_seconds,
        )
        for before_stage, after_stage in zip(before_stages, after_stages, strict=True)
    )

    before_work = before.measurement.build_work
    after_work = after.measurement.build_work
    before_statuses = {entry.path: entry.status for entry in before_work.generation_statuses}
    after_statuses = {entry.path: entry.status for entry in after_work.generation_statuses}
    if len(before_statuses) != len(before_work.generation_statuses):
        raise ValueError("Before measurement contains duplicate artifact status paths.")
    if len(after_statuses) != len(after_work.generation_statuses):
        raise ValueError("After measurement contains duplicate artifact status paths.")

    ordered_paths = tuple(before_statuses) + tuple(
        path for path in after_statuses if path not in before_statuses
    )
    artifact_statuses = tuple(
        ArtifactGenerationStatusComparisonEvidence(
            path=path,
            before_status=before_statuses.get(path),
            after_status=after_statuses.get(path),
        )
        for path in ordered_paths
    )

    return BuildAndRunMeasurementComparisonEvidence(
        stages=stages,
        build_work=BuildWorkComparisonEvidence(
            before=before_work,
            after=after_work,
            artifact_statuses=artifact_statuses,
        ),
    )
