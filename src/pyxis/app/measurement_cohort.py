from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from .measurement import (
    ExecutionEnvironmentEvidence,
    MeasuredBuildAndRunResult,
    MeasurementStage,
    MeasurementSubjectEvidence,
    RuntimeInputEvidence,
    _validated_measurement_subject,
)


@dataclass(frozen=True, slots=True)
class MeasurementCohortConditionEvidence:
    """Exact condition shared by every observation in one repeated-measurement cohort."""

    subject: MeasurementSubjectEvidence
    runtime_input: RuntimeInputEvidence
    environment: ExecutionEnvironmentEvidence
    stages: tuple[MeasurementStage, ...]

    def __post_init__(self) -> None:
        if self.stages != ("build", "runtime"):
            raise ValueError(
                "Measurement cohort stage contract must be exactly build followed by runtime."
            )


@dataclass(frozen=True, slots=True)
class BuildAndRunMeasurementCohortEvidence:
    """Ordered repeated observations collected under one exact measurement condition."""

    condition: MeasurementCohortConditionEvidence
    observations: tuple[MeasuredBuildAndRunResult, ...]

    def __post_init__(self) -> None:
        if len(self.observations) < 2:
            raise ValueError("Measurement cohort requires at least two observations.")

        for observation in self.observations:
            _require_matching_cohort_condition(observation, self.condition)


def _cohort_condition_from_observation(
    observation: MeasuredBuildAndRunResult,
) -> MeasurementCohortConditionEvidence:
    measurement = observation.measurement
    return MeasurementCohortConditionEvidence(
        subject=_validated_measurement_subject(observation),
        runtime_input=measurement.runtime_input,
        environment=measurement.environment,
        stages=tuple(stage.stage for stage in measurement.stages),
    )


def _require_matching_cohort_condition(
    observation: MeasuredBuildAndRunResult,
    expected: MeasurementCohortConditionEvidence,
) -> None:
    actual = _cohort_condition_from_observation(observation)

    if actual.subject != expected.subject:
        raise ValueError(
            "Measurement cohort observations must share the same Workspace and exact RIR state."
        )
    if actual.runtime_input != expected.runtime_input:
        raise ValueError(
            "Measurement cohort observations must share the same runtime input evidence."
        )
    if actual.environment != expected.environment:
        raise ValueError(
            "Measurement cohort observations must share the same execution environment evidence."
        )
    if actual.stages != expected.stages:
        raise ValueError(
            "Measurement cohort observations must share the same ordered stage contract."
        )


def create_build_and_run_measurement_cohort(
    observations: Iterable[MeasuredBuildAndRunResult],
) -> BuildAndRunMeasurementCohortEvidence:
    """Create one coherent repeated-measurement cohort without aggregating it.

    A cohort represents repeated observations of one exact Repository Zero
    measurement condition: logical Workspace, exact RIR state, runtime input,
    execution environment, and ordered build/runtime stage contract must all agree.
    The original measured result objects are retained in caller-supplied order.

    Build-work evidence and stage durations are deliberately not required to match;
    those are observations made under the condition, not part of the condition
    itself. This boundary computes no summary statistics, scores, outlier labels,
    warmup classifications, or causal interpretation.
    """

    ordered_observations = tuple(observations)
    if len(ordered_observations) < 2:
        raise ValueError("Measurement cohort requires at least two observations.")

    condition = _cohort_condition_from_observation(ordered_observations[0])
    return BuildAndRunMeasurementCohortEvidence(
        condition=condition,
        observations=ordered_observations,
    )
