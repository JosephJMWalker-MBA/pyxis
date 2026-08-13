from math import sqrt

import pytest

from pyxis.app.measurement_dispersion import (
    BuildAndRunMeasurementPopulationStandardDeviationEvidence,
    create_build_and_run_measurement_population_standard_deviation,
)
from test_app_measurement_mean import _chain


def test_population_standard_deviation(tmp_path):
    _, mean = _chain(tmp_path)
    result = create_build_and_run_measurement_population_standard_deviation(mean)
    expected = sqrt(0.13671875)

    assert result.mean is mean
    assert result.stage_values == ((0.0, expected), (0.0, expected))

    with pytest.raises(ValueError, match="exact 11K mean evidence"):
        BuildAndRunMeasurementPopulationStandardDeviationEvidence(
            mean=mean,
            stage_values=((0.0, 99.0), result.stage_values[1]),
        )
