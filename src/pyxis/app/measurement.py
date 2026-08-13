from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import hashlib
from pathlib import Path
import platform
import time
from typing import Literal

from pyxis.authoring.workspace import WorkspaceSpec
from pyxis.compiler.manifest import repository_ir_sha256
from pyxis.compiler.status import ArtifactGenerationStatus, GenerationStatus

from .build import BuildAndRunResult, BuildResult, build_and_run_workspace


MeasurementStage = Literal["build", "runtime"]
MeasurementClock = Callable[[], float]


@dataclass(frozen=True, slots=True)
class MeasurementSubjectEvidence:
    """Logical Workspace identity plus exact measured architectural-state identity."""

    repository_id: str
    workspace_id: str
    rir_sha256: str

    def __post_init__(self) -> None:
        if not self.repository_id:
            raise ValueError("Measurement subject repository_id is required.")
        if not self.workspace_id:
            raise ValueError("Measurement subject workspace_id is required.")
        if not self.rir_sha256:
            raise ValueError("Measurement subject rir_sha256 is required.")


@dataclass(frozen=True, slots=True)
class ExecutionEnvironmentEvidence:
    """Stable non-identifying execution-environment identity for one measured cycle."""

    python_implementation: str
    python_version: str
    platform_system: str
    platform_machine: str

    def __post_init__(self) -> None:
        if not self.python_implementation:
            raise ValueError("Execution environment python_implementation is required.")
        if not self.python_version:
            raise ValueError("Execution environment python_version is required.")
        if not self.platform_system:
            raise ValueError("Execution environment platform_system is required.")
        if not self.platform_machine:
            raise ValueError("Execution environment platform_machine is required.")


ExecutionEnvironmentProvider = Callable[[], ExecutionEnvironmentEvidence]


@dataclass(frozen=True, slots=True)
class RuntimeInputEvidence:
    """Privacy-preserving identity and size evidence for one runtime input."""

    sha256: str
    character_count: int
    utf8_byte_count: int

    def __post_init__(self) -> None:
        if len(self.sha256) != 64 or any(
            character not in "0123456789abcdef" for character in self.sha256
        ):
            raise ValueError("Runtime input sha256 must be a lowercase SHA-256 hex digest.")
        if self.character_count < 0:
            raise ValueError("Runtime input character_count cannot be negative.")
        if self.utf8_byte_count < 0:
            raise ValueError("Runtime input utf8_byte_count cannot be negative.")


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

    subject: MeasurementSubjectEvidence
    environment: ExecutionEnvironmentEvidence
    runtime_input: RuntimeInputEvidence
    stages: tuple[StageDurationEvidence, ...]
    build_work: BuildWorkEvidence


@dataclass(frozen=True, slots=True)
class MeasuredBuildAndRunResult:
    """Existing build/run evidence paired with measurement evidence."""

    result: BuildAndRunResult
    measurement: BuildAndRunMeasurementEvidence


@dataclass(frozen=True, slots=True)
class MeasurementSubjectComparisonEvidence:
    """Before/after subject identity for two coherent logical Workspace cycles."""

    before: MeasurementSubjectEvidence
    after: MeasurementSubjectEvidence


@dataclass(frozen=True, slots=True)
class ExecutionEnvironmentComparisonEvidence:
    """Before/after environment identity for descriptively comparable cycles."""

    before: ExecutionEnvironmentEvidence
    after: ExecutionEnvironmentEvidence
    matches: bool

    def __post_init__(self) -> None:
        if self.matches != (self.before == self.after):
            raise ValueError(
                "Execution environment matches must reflect exact environment evidence equality."
            )


@dataclass(frozen=True, slots=True)
class RuntimeInputComparisonEvidence:
    """Before/after workload evidence without retaining raw runtime text."""

    before: RuntimeInputEvidence
    after: RuntimeInputEvidence
    matches: bool

    def __post_init__(self) -> None:
        if self.matches != (self.before == self.after):
            raise ValueError("Runtime input matches must reflect exact input evidence equality.")


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

    subject: MeasurementSubjectComparisonEvidence
    environment: ExecutionEnvironmentComparisonEvidence
    runtime_input: RuntimeInputComparisonEvidence
    stages: tuple[StageDurationComparisonEvidence, ...]
    build_work: BuildWorkComparisonEvidence


def _measurement_subject_from_build(build: BuildResult) -> MeasurementSubjectEvidence:
    repository = build.repository
    rir_sha256 = repository_ir_sha256(repository)
    if build.manifest.rir_sha256 != rir_sha256:
        raise ValueError(
            "Build measurement subject is incoherent: manifest RIR identity does not "
            "match RepositoryIR."
        )

    return MeasurementSubjectEvidence(
        repository_id=repository.repository_id,
        workspace_id=repository.workspace.workspace_id,
        rir_sha256=rir_sha256,
    )


def _current_execution_environment() -> ExecutionEnvironmentEvidence:
    return ExecutionEnvironmentEvidence(
        python_implementation=platform.python_implementation(),
        python_version=platform.python_version(),
        platform_system=platform.system() or "unknown",
        platform_machine=platform.machine() or "unknown",
    )


def _runtime_input_evidence(text: str) -> RuntimeInputEvidence:
    encoded = text.encode("utf-8")
    return RuntimeInputEvidence(
        sha256=hashlib.sha256(encoded).hexdigest(),
        character_count=len(text),
        utf8_byte_count=len(encoded),
    )


def _validated_measurement_subject(
    measured: MeasuredBuildAndRunResult,
) -> MeasurementSubjectEvidence:
    expected = _measurement_subject_from_build(measured.result.build)
    subject = measured.measurement.subject
    if subject != expected:
        raise ValueError(
            "Measurement subject evidence does not match its BuildResult identity."
        )
    return subject


def measure_build_and_run_workspace(
    spec: WorkspaceSpec,
    destination_root: Path,
    text: str,
    *,
    clock: MeasurementClock = time.monotonic,
    environment_provider: ExecutionEnvironmentProvider = _current_execution_environment,
) -> MeasuredBuildAndRunResult:
    """Measure the existing build-and-run operation without replacing it.

    Timing observes only the established build and runtime boundaries exposed by
    ``build_and_run_workspace``. Subject identity comes from the returned
    RepositoryIR plus generation manifest. Stable, non-identifying execution
    environment evidence is acquired once before timed stages begin. Runtime input
    evidence records only a deterministic SHA-256 and size facts; raw text is not
    retained by measurement. Compiler/materialization work evidence is copied
    directly from the returned ``BuildResult``; this layer performs no filesystem
    discovery and makes no independent work or waste classification.
    """

    environment = environment_provider()
    if not isinstance(environment, ExecutionEnvironmentEvidence):
        raise TypeError(
            "Execution environment provider must return ExecutionEnvironmentEvidence."
        )

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
        subject=_measurement_subject_from_build(build),
        environment=environment,
        runtime_input=_runtime_input_evidence(text),
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
    """Compare two coherent Workspace measurements without causal interpretation.

    Each measurement subject is first revalidated against its own BuildResult.
    Logical Repository/Workspace identity must match before any timing or work
    comparison is constructed. RIR identity may differ, making architectural-state
    changes explicit while still permitting comparison within one Workspace.

    Execution environment and runtime input evidence are retained exactly for both
    observations and report whether their respective identities match. Mismatches
    do not invalidate descriptive comparison; they remain explicit confounds for
    any later interpretation.

    This function performs no execution, filesystem access, reclassification, or
    scoring. Duration deltas mean only ``after - before``. Work comparison carries
    the exact immutable evidence already observed for each cycle and reports only
    literal compiler-status transitions by artifact path.
    """

    before_subject = _validated_measurement_subject(before)
    after_subject = _validated_measurement_subject(after)
    if (
        before_subject.repository_id != after_subject.repository_id
        or before_subject.workspace_id != after_subject.workspace_id
    ):
        raise ValueError("Measured cycles must describe the same Workspace subject.")

    subject = MeasurementSubjectComparisonEvidence(
        before=before_subject,
        after=after_subject,
    )
    environment = ExecutionEnvironmentComparisonEvidence(
        before=before.measurement.environment,
        after=after.measurement.environment,
        matches=before.measurement.environment == after.measurement.environment,
    )
    runtime_input = RuntimeInputComparisonEvidence(
        before=before.measurement.runtime_input,
        after=after.measurement.runtime_input,
        matches=before.measurement.runtime_input == after.measurement.runtime_input,
    )

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
        subject=subject,
        environment=environment,
        runtime_input=runtime_input,
        stages=stages,
        build_work=BuildWorkComparisonEvidence(
            before=before_work,
            after=after_work,
            artifact_statuses=artifact_statuses,
        ),
    )
