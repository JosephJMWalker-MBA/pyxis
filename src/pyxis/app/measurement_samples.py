from __future__ import annotations

from dataclasses import dataclass

from .measurement import BuildWorkEvidence, MeasurementStage
from .measurement_cohort import (
    BuildAndRunMeasurementCohortEvidence,
    MeasurementCohortConditionEvidence,
)


@dataclass(frozen=True, slots=True)
class StageSampleObservationEvidence:
    """One raw stage duration paired with the exact work evidence from its cycle."""

    duration_seconds: float
    build_work: BuildWorkEvidence

    def __post_init__(self) -> None:
        if self.duration_seconds < 0:
            raise ValueError("Stage sample duration cannot be negative.")


@dataclass(frozen=True, slots=True)
class MeasurementStageSamplesEvidence:
    """Ordered raw observations for one stage in a coherent measurement cohort."""

    stage: MeasurementStage
    observations: tuple[StageSampleObservationEvidence, ...]

    def __post_init__(self) -> None:
        if len(self.observations) < 2:
            raise ValueError("Measurement stage samples require at least two observations.")


@dataclass(frozen=True, slots=True)
class BuildAndRunMeasurementStageSamplesEvidence:
    """Pure raw-sample projection of one coherent build/run measurement cohort."""

    condition: MeasurementCohortConditionEvidence
    stages: tuple[MeasurementStageSamplesEvidence, ...]

    def __post_init__(self) -> None:
        stage_names = tuple(stage.stage for stage in self.stages)
        if stage_names != self.condition.stages:
            raise ValueError(
                "Measurement stage samples must preserve the cohort stage contract."
            )

        observation_counts = {len(stage.observations) for stage in self.stages}
        if len(observation_counts) != 1:
            raise ValueError(
                "Measurement stage samples must preserve the same observation count for every stage."
            )


def project_build_and_run_measurement_stage_samples(
    cohort: BuildAndRunMeasurementCohortEvidence,
) -> BuildAndRunMeasurementStageSamplesEvidence:
    """Project a coherent cohort into ordered raw stage/work observations.

    The projection performs no execution, timing, filesystem access, aggregation,
    classification, or interpretation. Every raw stage duration is copied in cohort
    observation order and paired with the exact immutable ``BuildWorkEvidence``
    object retained by the same measured cycle. The cohort condition is retained by
    object identity so subject, RIR, workload, environment, and stage coherence stay
    explicit beside the samples.
    """

    stages = tuple(
        MeasurementStageSamplesEvidence(
            stage=stage_name,
            observations=tuple(
                StageSampleObservationEvidence(
                    duration_seconds=observation.measurement.stages[stage_index].duration_seconds,
                    build_work=observation.measurement.build_work,
                )
                for observation in cohort.observations
            ),
        )
        for stage_index, stage_name in enumerate(cohort.condition.stages)
    )

    return BuildAndRunMeasurementStageSamplesEvidence(
        condition=cohort.condition,
        stages=stages,
    )
