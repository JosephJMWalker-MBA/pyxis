from dataclasses import dataclass
from math import sqrt

from .measurement_mean import BuildAndRunMeasurementMeanEvidence, StageWorkContextMeanEvidence


def _pstdev(group: StageWorkContextMeanEvidence) -> float:
    values = tuple(x.duration_seconds for x in group.median.envelope.group.observations)
    return sqrt(sum((x - group.mean_seconds) ** 2 for x in values) / len(values))


@dataclass(frozen=True, slots=True)
class BuildAndRunMeasurementPopulationStandardDeviationEvidence:
    mean: BuildAndRunMeasurementMeanEvidence
    stage_values: tuple[tuple[float, ...], ...]

    def __post_init__(self) -> None:
        expected = tuple(
            tuple(_pstdev(group) for group in stage.groups)
            for stage in self.mean.stages
        )
        if self.stage_values != expected:
            raise ValueError("Population standard deviation must match exact 11K mean evidence.")


def create_build_and_run_measurement_population_standard_deviation(
    mean: BuildAndRunMeasurementMeanEvidence,
) -> BuildAndRunMeasurementPopulationStandardDeviationEvidence:
    return BuildAndRunMeasurementPopulationStandardDeviationEvidence(
        mean=mean,
        stage_values=tuple(
            tuple(_pstdev(group) for group in stage.groups)
            for stage in mean.stages
        ),
    )
