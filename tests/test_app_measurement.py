from dataclasses import FrozenInstanceError
import importlib
from pathlib import Path

import pytest

from pyxis.app import (
    StageDurationEvidence,
    build_and_run_workspace,
    measure_build_and_run_workspace,
)
from pyxis.authoring import create_workspace_spec


measurement_module = importlib.import_module("pyxis.app.measurement")


class FakeClock:
    def __init__(self, *values: float) -> None:
        self._values = iter(values)
        self.calls = 0

    def __call__(self) -> float:
        self.calls += 1
        return next(self._values)


def _relative_paths(paths: tuple[Path, ...], root: Path) -> tuple[str, ...]:
    return tuple(path.relative_to(root).as_posix() for path in paths)


def _assert_semantically_equal_builds(
    measured_root: Path,
    measured,
    baseline_root: Path,
    baseline,
) -> None:
    assert measured.repository == baseline.repository
    assert measured.artifacts == baseline.artifacts
    assert measured.manifest == baseline.manifest
    assert measured.generation_statuses == baseline.generation_statuses
    assert measured.canonical_path.relative_to(measured_root) == (
        baseline.canonical_path.relative_to(baseline_root)
    )
    assert measured.rir_path.relative_to(measured_root) == (
        baseline.rir_path.relative_to(baseline_root)
    )
    assert measured.manifest_path.relative_to(measured_root) == (
        baseline.manifest_path.relative_to(baseline_root)
    )
    assert _relative_paths(measured.written_paths, measured_root) == _relative_paths(
        baseline.written_paths,
        baseline_root,
    )
    assert _relative_paths(measured.reused_paths, measured_root) == _relative_paths(
        baseline.reused_paths,
        baseline_root,
    )
    assert _relative_paths(measured.removed_paths, measured_root) == _relative_paths(
        baseline.removed_paths,
        baseline_root,
    )


def test_measurement_wraps_existing_build_and_run_with_exact_stage_timing(
    tmp_path: Path,
    monkeypatch,
) -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "Measurement must observe rather than replace the stable operation.",
    )
    text = "  hello   world  "
    baseline_root = tmp_path / "baseline"
    measured_root = tmp_path / "measured"
    baseline = build_and_run_workspace(spec, baseline_root, text)
    fake_clock = FakeClock(10.0, 12.5, 20.0, 24.25)

    real_build_and_run = measurement_module.build_and_run_workspace
    calls = []

    def tracked_build_and_run(*args, **kwargs):
        calls.append((args, kwargs))
        return real_build_and_run(*args, **kwargs)

    monkeypatch.setattr(
        measurement_module,
        "build_and_run_workspace",
        tracked_build_and_run,
    )

    measured = measure_build_and_run_workspace(
        spec,
        measured_root,
        text,
        clock=fake_clock,
    )

    assert len(calls) == 1
    assert calls[0][0] == (spec, measured_root, text)
    assert callable(calls[0][1]["_stage_observer"])
    assert fake_clock.calls == 4
    assert measured.measurement.stages == (
        StageDurationEvidence(stage="build", duration_seconds=2.5),
        StageDurationEvidence(stage="runtime", duration_seconds=4.25),
    )
    assert tuple(stage.stage for stage in measured.measurement.stages) == (
        "build",
        "runtime",
    )

    _assert_semantically_equal_builds(
        measured_root,
        measured.result.build,
        baseline_root,
        baseline.build,
    )
    assert measured.result.runtime_result == baseline.runtime_result

    work = measured.measurement.build_work
    assert work.generation_statuses is measured.result.build.generation_statuses
    assert work.written_paths is measured.result.build.written_paths
    assert work.reused_paths is measured.result.build.reused_paths
    assert work.removed_paths is measured.result.build.removed_paths

    with pytest.raises(FrozenInstanceError):
        measured.measurement.stages[0].duration_seconds = 99.0


def test_measurement_carries_incremental_work_facts_without_reclassification(
    tmp_path: Path,
) -> None:
    root = tmp_path / "workspace"
    spec = create_workspace_spec(
        "Text Lab",
        "Measurement should carry compiler-owned work facts unchanged.",
    )
    build_and_run_workspace(spec, root, "hello world")
    proposed = spec.without_capability("normalize_text")
    fake_clock = FakeClock(0.0, 1.0, 3.0, 5.0)

    measured = measure_build_and_run_workspace(
        proposed,
        root,
        "hello world",
        clock=fake_clock,
    )

    build = measured.result.build
    work = measured.measurement.build_work

    assert tuple((entry.path, entry.status) for entry in build.generation_statuses) == (
        ("generated/capabilities/inspect_text.py", "reused"),
        ("generated/workspaces/text_lab/main.py", "regenerated"),
        ("generated/capabilities/normalize_text.py", "removed"),
    )
    assert work.generation_statuses is build.generation_statuses
    assert work.written_paths is build.written_paths
    assert work.reused_paths is build.reused_paths
    assert work.removed_paths is build.removed_paths
    assert _relative_paths(work.written_paths, root) == (
        "generated/workspaces/text_lab/main.py",
    )
    assert _relative_paths(work.reused_paths, root) == (
        "generated/capabilities/inspect_text.py",
    )
    assert _relative_paths(work.removed_paths, root) == (
        "generated/capabilities/normalize_text.py",
    )
    assert measured.measurement.stages == (
        StageDurationEvidence(stage="build", duration_seconds=1.0),
        StageDurationEvidence(stage="runtime", duration_seconds=2.0),
    )
    assert set(measured.result.runtime_result) == {"inspect_text"}
