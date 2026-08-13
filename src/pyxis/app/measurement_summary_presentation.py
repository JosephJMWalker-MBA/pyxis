from dataclasses import dataclass

from .measurement import BuildWorkEvidence, MeasurementStage
from .measurement_summary import BuildAndRunMeasurementDescriptiveSummaryEvidence


@dataclass(frozen=True, slots=True)
class MeasurementWorkContextSummaryPresentation:
    build_work: BuildWorkEvidence
    sample_count: int
    minimum_seconds: float
    maximum_seconds: float
    median_seconds: float
    mean_seconds: float
    population_standard_deviation_seconds: float


@dataclass(frozen=True, slots=True)
class MeasurementStageSummaryPresentation:
    stage: MeasurementStage
    groups: tuple[MeasurementWorkContextSummaryPresentation, ...]


@dataclass(frozen=True, slots=True)
class BuildAndRunMeasurementSummaryPresentation:
    source: BuildAndRunMeasurementDescriptiveSummaryEvidence
    stages: tuple[MeasurementStageSummaryPresentation, ...]

    def __post_init__(self) -> None:
        expected = _project_stages(self.source)
        if len(self.stages) != len(expected):
            raise ValueError("Measurement summary presentation must preserve every source stage.")
        for actual_stage, expected_stage in zip(self.stages, expected, strict=True):
            if actual_stage.stage != expected_stage.stage or len(actual_stage.groups) != len(expected_stage.groups):
                raise ValueError("Measurement summary presentation must preserve source stage/group order.")
            for actual, wanted in zip(actual_stage.groups, expected_stage.groups, strict=True):
                if actual.build_work is not wanted.build_work or actual != wanted:
                    raise ValueError("Measurement summary presentation must match exact source evidence.")


def _project_stages(source: BuildAndRunMeasurementDescriptiveSummaryEvidence):
    stages = []
    for envelope_stage, median_stage, mean_stage, dispersion_values in zip(
        source.envelope.stages,
        source.median.stages,
        source.mean.stages,
        source.dispersion.stage_values,
        strict=True,
    ):
        groups = tuple(
            MeasurementWorkContextSummaryPresentation(
                build_work=envelope_group.group.build_work,
                sample_count=envelope_group.sample_count,
                minimum_seconds=envelope_group.minimum_seconds,
                maximum_seconds=envelope_group.maximum_seconds,
                median_seconds=median_group.median_seconds,
                mean_seconds=mean_group.mean_seconds,
                population_standard_deviation_seconds=dispersion,
            )
            for envelope_group, median_group, mean_group, dispersion in zip(
                envelope_stage.groups, median_stage.groups, mean_stage.groups, dispersion_values, strict=True
            )
        )
        stages.append(MeasurementStageSummaryPresentation(stage=envelope_stage.stage, groups=groups))
    return tuple(stages)


def create_build_and_run_measurement_summary_presentation(source):
    """Project existing 11M evidence for read-only rendering; compute nothing new."""
    return BuildAndRunMeasurementSummaryPresentation(source=source, stages=_project_stages(source))
