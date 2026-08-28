from __future__ import annotations

from pathlib import Path

import pytest

import pyxis.cli as cli
from pyxis.app.chromium_research_root_backed_session_shell_lineage import (
    ChromiumResearchRootBackedSessionContinuationShellLineage,
    ChromiumResearchRootBackedSessionShellLineage,
    prove_chromium_research_root_backed_session_shell_lineage,
)
from test_app_chromium_research_root_backed_session_continuation_reentry_plan_document import (
    _persist_valid_continuation,
)
from test_app_chromium_research_root_backed_session_reentry_plan_document import (
    _persist_valid_overlay,
)


def test_root_backed_cli_proves_persisted_launch_then_chains_only_explicit_typed_handoff(
    tmp_path: Path,
    monkeypatch,
) -> None:
    root_dir = tmp_path / "root"
    root_dir.mkdir(parents=True, exist_ok=True)
    _, _, _, _, root_overlay, _ = _persist_valid_overlay(root_dir, stem="36d-root")
    continuation_dir = tmp_path / "continuation"
    continuation_dir.mkdir(parents=True, exist_ok=True)
    *_, checkpoint = _persist_valid_continuation(continuation_dir, stem="36d-cont")
    handoff = checkpoint.fresh_reentry
    observed: dict[str, object] = {}

    def fake_first_shell(lineage):
        observed["first_lineage"] = lineage
        return handoff

    def fake_cumulative_handoff_shell(reentry) -> None:
        observed["handoff"] = reentry

    def fail_continuation_overlay_reload(*args, **kwargs):
        raise AssertionError("36D in-process handoff must not reload a continuation overlay")

    monkeypatch.setattr(cli, "_run_root_backed_research_session_shell", fake_first_shell)
    monkeypatch.setattr(
        cli,
        "_run_root_backed_continuation_handoff_research_session_shell",
        fake_cumulative_handoff_shell,
    )
    monkeypatch.setattr(
        cli,
        "load_chromium_research_root_backed_session_continuation_reentry_plan_document",
        fail_continuation_overlay_reload,
    )

    assert cli.main(["research-shell", "--root-backed-overlay", str(root_overlay)]) == 0
    lineage = observed["first_lineage"]
    assert isinstance(lineage, ChromiumResearchRootBackedSessionShellLineage)
    assert lineage.overlay_source == root_overlay.resolve()
    assert observed["handoff"] is handoff


def test_root_backed_cli_normal_close_does_not_launch_cumulative_handoff_shell(
    tmp_path: Path,
    monkeypatch,
) -> None:
    root_dir = tmp_path / "root"
    root_dir.mkdir(parents=True, exist_ok=True)
    _, _, _, _, root_overlay, _ = _persist_valid_overlay(root_dir, stem="36d-close")
    observed = {"cumulative": 0}

    def fake_first_shell(lineage):
        assert isinstance(lineage, ChromiumResearchRootBackedSessionShellLineage)
        return None

    def fail_cumulative_shell(reentry) -> None:
        observed["cumulative"] += 1
        raise AssertionError("normal close must not implicitly change research modes")

    monkeypatch.setattr(cli, "_run_root_backed_research_session_shell", fake_first_shell)
    monkeypatch.setattr(
        cli,
        "_run_root_backed_continuation_handoff_research_session_shell",
        fail_cumulative_shell,
    )

    assert cli.main(["research-shell", "--root-backed-overlay", str(root_overlay)]) == 0
    assert observed["cumulative"] == 0


def test_root_backed_persisted_continuation_cli_retains_exact_overlay_as_launch_context(
    tmp_path: Path,
    monkeypatch,
) -> None:
    values = _persist_valid_continuation(tmp_path, stem="45a-persisted-continuation")
    overlay = values[8]
    observed: dict[str, object] = {}

    def fake_continuation_shell(lineage) -> None:
        observed["lineage"] = lineage

    monkeypatch.setattr(
        cli,
        "_run_root_backed_continuation_research_session_shell",
        fake_continuation_shell,
    )

    assert (
        cli.main(
            [
                "research-shell",
                "--root-backed-continuation-overlay",
                str(overlay),
            ]
        )
        == 0
    )
    lineage = observed["lineage"]
    assert isinstance(lineage, ChromiumResearchRootBackedSessionContinuationShellLineage)
    assert lineage.overlay_source == overlay.resolve()


def test_root_backed_shell_runner_returns_exact_typed_handoff_from_inspectable_app(
    tmp_path: Path,
    monkeypatch,
) -> None:
    root_dir = tmp_path / "root"
    root_dir.mkdir(parents=True, exist_ok=True)
    _, _, earned, _, root_overlay, _ = _persist_valid_overlay(
        root_dir,
        stem="36d-runner",
    )
    lineage = prove_chromium_research_root_backed_session_shell_lineage(
        earned,
        overlay_source=root_overlay,
    )
    continuation_dir = tmp_path / "continuation"
    continuation_dir.mkdir(parents=True, exist_ok=True)
    *_, checkpoint = _persist_valid_continuation(continuation_dir, stem="36d-handoff")
    handoff = checkpoint.fresh_reentry
    observed: dict[str, object] = {}

    class FakeShell:
        def run(self):
            return handoff

    def fake_factory(value):
        observed["lineage"] = value
        return FakeShell()

    monkeypatch.setattr(cli, "_load_root_backed_research_shell_factory", lambda: fake_factory)

    assert cli._run_root_backed_research_session_shell(lineage) is handoff
    assert observed["lineage"] is lineage


def test_root_backed_shell_runner_rejects_untyped_app_return(
    tmp_path: Path,
    monkeypatch,
) -> None:
    root_dir = tmp_path / "root"
    root_dir.mkdir(parents=True, exist_ok=True)
    _, _, earned, _, root_overlay, _ = _persist_valid_overlay(
        root_dir,
        stem="36d-invalid",
    )
    lineage = prove_chromium_research_root_backed_session_shell_lineage(
        earned,
        overlay_source=root_overlay,
    )

    class FakeShell:
        def run(self):
            return object()

    monkeypatch.setattr(
        cli,
        "_load_root_backed_research_shell_factory",
        lambda: lambda value: FakeShell(),
    )

    with pytest.raises(TypeError, match="invalid cumulative handoff"):
        cli._run_root_backed_research_session_shell(lineage)


def test_root_backed_shell_runner_rejects_raw_reentry_without_persisted_lineage(
    tmp_path: Path,
) -> None:
    _, _, earned, _, _, _ = _persist_valid_overlay(tmp_path, stem="45a-raw-reject")

    with pytest.raises(TypeError, match="ShellLineage"):
        cli._run_root_backed_research_session_shell(earned)  # type: ignore[arg-type]
