from dataclasses import FrozenInstanceError, fields
from pathlib import Path

import pytest

from pyxis.app import (
    ExecutionEnvironmentComparisonEvidence,
    ExecutionEnvironmentEvidence,
    compare_build_and_run_measurements,
    measure_build_and_run_workspace,
)
from pyxis.authoring import create_workspace_spec


class EventClock:
    def __init__(self, events: list[str], *values: float) -> None:
        self._events = events
        self._values = iter(values)

    def __call__(self) -> float:
        self._events.append("clock")
        return next(self._values)


class FakeClock:
    def __init__(self, *values: float) -> None:
        self._values = iter(values)

    def __call__(self) -> float:
        return next(self._values)


def test_measurement_acquires_injected_non_identifying_environment_before_timing(
    tmp_path: Path,
) -> None:
    events: list[str] = []
    environment = ExecutionEnvironmentEvidence(
        python_implementation="CPython",
        python_version="3.11.9",
        platform_system="Linux",
        platform_machine="x86_64",
    )

    def environment_provider() -> ExecutionEnvironmentEvidence:
        events.append("environment")
        return environment

    measured = measure_build_and_run_workspace(
        create_workspace_spec(
            "Text Lab",
            "Environment identity should be stable measurement context.",
        ),
        tmp_path / "workspace",
        "hello world",
        clock=EventClock(events, 0.0, 1.0, 2.0, 3.0),
        environment_provider=environment_provider,
    )

    assert measured.measurement.environment is environment
    assert events == ["environment", "clock", "clock", "clock", "clock"]
    assert tuple(field.name for field in fields(environment)) == (
        "python_implementation",
        "python_version",
        "platform_system",
        "platform_machine",
    )

    with pytest.raises(FrozenInstanceError):
        environment.python_version = "3.12.0"


def test_comparison_exposes_environment_match_without_rejecting_mismatch(
    tmp_path: Path,
) -> None:
    root = tmp_path / "workspace"
    spec = create_workspace_spec(
        "Text Lab",
        "Environment mismatch should remain descriptive evidence.",
    )
    text = "same workload"
    first_environment = ExecutionEnvironmentEvidence(
        python_implementation="CPython",
        python_version="3.11.9",
        platform_system="Linux",
        platform_machine="x86_64",
    )
    same_environment = ExecutionEnvironmentEvidence(
        python_implementation="CPython",
        python_version="3.11.9",
        platform_system="Linux",
        platform_machine="x86_64",
    )
    different_environment = ExecutionEnvironmentEvidence(
        python_implementation="CPython",
        python_version="3.12.4",
        platform_system="Linux",
        platform_machine="arm64",
    )

    first = measure_build_and_run_workspace(
        spec,
        root,
        text,
        clock=FakeClock(0.0, 2.0, 4.0, 5.0),
        environment_provider=lambda: first_environment,
    )
    same = measure_build_and_run_workspace(
        spec,
        root,
        text,
        clock=FakeClock(10.0, 11.0, 12.0, 13.0),
        environment_provider=lambda: same_environment,
    )
    different = measure_build_and_run_workspace(
        spec,
        root,
        text,
        clock=FakeClock(20.0, 20.5, 21.0, 23.0),
        environment_provider=lambda: different_environment,
    )

    same_comparison = compare_build_and_run_measurements(first, same)
    different_comparison = compare_build_and_run_measurements(same, different)

    assert same_comparison.environment == ExecutionEnvironmentComparisonEvidence(
        before=first_environment,
        after=same_environment,
        matches=True,
    )
    assert same_comparison.environment.before is first_environment
    assert same_comparison.environment.after is same_environment

    assert different_comparison.environment == ExecutionEnvironmentComparisonEvidence(
        before=same_environment,
        after=different_environment,
        matches=False,
    )
    assert different_comparison.environment.before is same_environment
    assert different_comparison.environment.after is different_environment
    assert different_comparison.runtime_input.matches is True
    assert tuple(stage.stage for stage in different_comparison.stages) == (
        "build",
        "runtime",
    )
    assert len(different_comparison.build_work.artifact_statuses) == 3
