from __future__ import annotations

from pathlib import Path

import pytest

import pyxis.cli as cli
from test_app_chromium_research_root_backed_session_continuation_reentry_plan_document import (
    _persist_valid_continuation,
)
from test_app_chromium_research_root_backed_session_reentry_plan_document import (
    _persist_valid_overlay,
)


def test_root_backed_cli_chains_only_explicit_typed_handoff_into_cumulative_shell(
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

    def fake_first_shell(reentry):
        observed["first_reentry"] = reentry
        return handoff

    def fake_cumulative_shell(reentry) -> None:
        observed["handoff"] = reentry

    def fail_continuation_overlay_reload(*args, **kwargs):
        raise AssertionError("36D in-process handoff must not reload a continuation overlay")

    monkeypatch.setattr(cli, "_run_root_backed_research_session_shell", fake_first_shell)
    monkeypatch.setattr(
        cli,
        "_run_root_backed_continuation_research_session_shell",
        fake_cumulative_shell,
    )
    monkeypatch.setattr(
        cli,
        "load_chromium_research_root_backed_session_continuation_reentry_plan_document",
        fail_continuation_overlay_reload,
    )

    assert cli.main(["research-shell", "--root-backed-overlay", str(root_overlay)]) == 0
    assert "first_reentry" in observed
    assert observed["first_reentry"] is not handoff
    assert observed["handoff"] is handoff


def test_root_backed_cli_normal_close_does_not_launch_cumulative_shell(
    tmp_path: Path,
    monkeypatch,
) -> None:
    root_dir = tmp_path / "root"
    root_dir.mkdir(parents=True, exist_ok=True)
    _, _, _, _, root_overlay, _ = _persist_valid_overlay(root_dir, stem="36d-close")
    observed = {"cumulative": 0}

    def fake_first_shell(reentry):
        return None

    def fail_cumulative_shell(reentry) -> None:
        observed["cumulative"] += 1
        raise AssertionError("normal close must not implicitly change research modes")

    monkeypatch.setattr(cli, "_run_root_backed_research_session_shell", fake_first_shell)
    monkeypatch.setattr(
        cli,
        "_run_root_backed_continuation_research_session_shell",
        fail_cumulative_shell,
    )

    assert cli.main(["research-shell", "--root-backed-overlay", str(root_overlay)]) == 0
    assert observed["cumulative"] == 0


def test_root_backed_shell_runner_returns_exact_typed_handoff_from_textual_app(
    tmp_path: Path,
    monkeypatch,
) -> None:
    import pyxis.ui.root_backed_research_session_shell as shell_module

    root_dir = tmp_path / "root"
    root_dir.mkdir(parents=True, exist_ok=True)
    _, _, earned, _, _, _ = _persist_valid_overlay(root_dir, stem="36d-runner")
    continuation_dir = tmp_path / "continuation"
    continuation_dir.mkdir(parents=True, exist_ok=True)
    *_, checkpoint = _persist_valid_continuation(continuation_dir, stem="36d-handoff")
    handoff = checkpoint.fresh_reentry

    class FakeShell:
        def run(self):
            return handoff

    monkeypatch.setattr(
        shell_module,
        "create_root_backed_research_session_shell",
        lambda reentry: FakeShell(),
    )

    assert cli._run_root_backed_research_session_shell(earned) is handoff


def test_root_backed_shell_runner_rejects_untyped_app_return(
    tmp_path: Path,
    monkeypatch,
) -> None:
    import pyxis.ui.root_backed_research_session_shell as shell_module

    root_dir = tmp_path / "root"
    root_dir.mkdir(parents=True, exist_ok=True)
    _, _, earned, _, _, _ = _persist_valid_overlay(root_dir, stem="36d-invalid")

    class FakeShell:
        def run(self):
            return object()

    monkeypatch.setattr(
        shell_module,
        "create_root_backed_research_session_shell",
        lambda reentry: FakeShell(),
    )

    with pytest.raises(TypeError, match="invalid cumulative handoff"):
        cli._run_root_backed_research_session_shell(earned)
