from pyxis.app.measurement_dispersion import create_build_and_run_measurement_population_standard_deviation as sd
from pyxis.app.measurement_summary import create_build_and_run_measurement_descriptive_summary as bundle
from pyxis.app.measurement_summary_presentation import create_build_and_run_measurement_summary_presentation as project
from test_app_measurement_mean import _chain


def test_projection_source(tmp_path):
    median, mean = _chain(tmp_path)
    envelope = median.envelope
    summary = bundle(envelope, median, mean, sd(mean))
    view = project(summary)
    assert view.source is summary
    assert tuple(x.stage for x in view.stages) == ("build", "runtime")
