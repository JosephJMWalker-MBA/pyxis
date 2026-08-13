from __future__ import annotations

from dataclasses import dataclass

from .measurement import MeasurementStage
from .measurement_median import (
    BuildAndRunMeasurementMedianEvidence,
    StageWorkContextMedianEvidence,
)


@dataclass(frozen=True, slots=True)
class StageWorkContextMeanEvidence:
    """Arithmetic mean duration for one exact 11J median evidence object."""

    median: StageWorkContextMedianEvidence
    mean_seconds: float

    def __post_init__(self) -> None:
        durations = tuple(
            observation.duration_seconds
            for observation in self.median.envelope.group.observations
        )
        expected = sum(durations) / len(durations)
        if self.mean_seconds != expected:
            raise ValueError(
                "Work-context mean_seconds must match the exact source median envelope observations."
            )


@dataclass(frozen=True, slots=True)
class MeasurementStageMeanEvidence:
    """Ordered arithmetic means for the exact work contexts of one stage."""

    stage: MeasurementStage
    groups: tuple[StageWorkContextMeanEvidence, ...]

    def __post_init__(self) -> None:
        if not self.groups:
            raise ValueError("Measurement stage mean evidence requires at least one group.")


@dataclass(frozen=True, slots=True)
class BuildAndRunMeasurementMeanEvidence:
    """Mean-only evidence over one exact 11J median result."""

    median: BuildAndRunMeasurementMedianEvidence
    stages: tuple[MeasurementStageMeanEvidence, ...]

    def __post_init__(self) -> None:
        stage_names = tuple(stage.stage for stage in self.stages)
        median_stage_names = tuple(stage.stage for stage in self.median.stages)
        if stage_names != median_stage_names:
            raise ValueError(
                "Measurement mean evidence must preserve the source median stage contract."
            )

        for source_stage, mean_stage in zip(
            self.median.stages,
            self.stages,
            strict=True,
        ):
            if len(source_stage.groups) != len(mean_stage.groups):
                raise ValueError(
                    "Measurement mean evidence must preserve every source median group."
                )
            for source_group, mean_group in zip(
                source_stage.groups,
                mean_stage.groups,
                strict=True,
            ):
                if mean_group.median is not source_group:
                    raise ValueError(
                        "Measurement mean evidence must retain the exact source median group object."
                    )


def create_build_and_run_measurement_mean(
    median_evidence: BuildAndRunMeasurementMedianEvidence,
) -> BuildAndRunMeasurementMeanEvidence:
    """Compute arithmetic mean only within each exact 11J work context.

    Stage and work-context ordering are preserved. Every mean retains the exact
    source ``StageWorkContextMedianEvidence`` object, while ``mean_seconds`` is
    computed independently from the raw durations behind that source object's 11I
    envelope. This boundary computes no variance, standard deviation, confidence
    interval, additional quantile, semantic label, score, or causal interpretation.
    """

    return BuildAndRunMeasurementMeanEvidence(
        median=median_evidence,
        stages=tuple(
            MeasurementStageMeanEvidence(
                stage=stage.stage,
                groups=tuple(
                    StageWorkContextMeanEvidence(
                        median=group,
                        mean_seconds=(
                            sum(
                                observation.duration_seconds
                                for observation in group.envelope.group.observations
                            )
                            / len(group.envelope.group.observations)
                        ),
                    )
                    for group in stage.groups
                ),
            )
            for stage in median_evidence.stages
        ),
    )
