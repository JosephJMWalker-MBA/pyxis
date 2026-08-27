from __future__ import annotations

from pathlib import Path

import pytest

import pyxis.cli as cli
from pyxis.app.chromium_research_third_basis_epoch_shell_lineage import (
    prove_chromium_research_third_basis_epoch_shell_lineage,
)
from test_app_chromium_research_third_basis_epoch_continuation_reentry_plan_document import (
    _persist_valid_continuation,
)
from test_app_chromium_research_third_basis_epoch_reentry_plan_document import (
    _persist_valid_overlay,
)


def test_third_epoch_cli_chains_only_explicit_typed_handoff_into_cumulative_shell(
    tmp_path: Path,
    monkeypatch,
) -> None:
    first_dir = tmp_path / "first"
    first_dir.mkdir(parents=True, exist_ok=True)
    _, _, overlay, _ = _persist_valid_overlay(first_dir, stem="41e-cli-first")
    continuation_dir = tmp_path / "continuation"
    continuation_dir.mkdir(parents=True, exist_ok=True)
    values = _persist_valid_continuation(continuation_dir, stem="41e-cli-cont")
    handoff = values[8].fresh_reentry
    observed: dict[str, object] = {}

    def fake_first_shell(lineage):
        observed["first_lineage"] = lineage
        return handoff

    def fake_handoff_shell(reentry) -> None:
        observed["handoff"] = reentry

    def fail_continuation_overlay_reload(*args, **kwargs):
        raise AssertionError("41E in-process handoff must not reload a continuation overlay")

    def fail_continuation_lineage_proof(*args, **kwargs):
        raise AssertionError("41E in-process handoff must not synthesize a 41A path proof")

    monkeypatch.setattr(cli, "_run_third_basis_epoch_research_session_shell", fake_first_shell)
    monkeypatch.setattr(
        cli,
        "_run_third_basis_epoch_continuation_handoff_research_session_shell",
        fake_handoff_shell,
    )
    monkeypatch.setattr(
        cli,
        "load_chromium_research_third_basis_epoch_continuation_reentry_plan_document",
        fail_continuation_overlay_reload,
    )
    monkeypatch.setattr(
        cli,
        "prove_chromium_research_third_basis_epoch_continuation_shell_lineage",
        fail_continuation_lineage_proof,
    )

    assert cli.main(["research-shell", "--third-basis-epoch-overlay", str(overlay)]) == 0
    assert "first_lineage" in observed
    assert observed["handoff"] is handoff


def test_third_epoch_cli_normal_close_does_not_launch_cumulative_mode(
    tmp_path: Path,
    monkeypatch,
) -> None:
    _, _, overlay, _ = _persist_valid_overlay(tmp_path, stem="41e-cli-close")
    observed = {"cumulative": 0}

    monkeypatch.setattr(
        cli,
        "_run_third_basis_epoch_research_session_shell",
        lambda lineage: None,
    )

    def fail_handoff_shell(reentry) -> None:
        observed["cumulative"] += 1
        raise AssertionError("normal close must not implicitly change third-epoch modes")

    monkeypatch.setattr(
        cli,
        "_run_third_basis_epoch_continuation_handoff_research_session_shell",
        fail_handoff_shell,
    )

    assert cli.main(["research-shell", "--third-basis-epoch-overlay", str(overlay)]) == 0
    assert observed["cumulative"] == 0


def test_third_epoch_first_shell_runner_returns_exact_typed_handoff_from_textual_app(
    tmp_path: Path,
    monkeypatch,
) -> None:
    import pyxis.ui.third_basis_epoch_cumulative_handoff_shell as shell_module

    first_dir = tmp_path / "first"
    first_dir.mkdir(parents=True, exist_ok=True)
    _, earned, overlay, _ = _persist_valid_overlay(first_dir, stem="41e-runner")
    lineage = prove_chromium_research_third_basis_epoch_shell_lineage(
        earned,
        overlay_source=overlay,
    )
    continuation_dir = tmp_path / "cont"
    continuation_dir.mkdir(parents=True, exist_ok=True)
    values = _persist_valid_continuation(continuation_dir, stem="41e-handoff")
    handoff = values[8].fresh_reentry

    class FakeShell:
        def run(self):
            return handoff

    monkeypatch.setattr(
        shell_module,
        "create_third_basis_epoch_cumulative_handoff_research_session_shell",
        lambda supplied: FakeShell(),
    )

    assert cli._run_third_basis_epoch_research_session_shell(lineage) is handoff


def test_third_epoch_first_shell_runner_rejects_untyped_app_return(
    tmp_path: Path,
    monkeypatch,
) -> None:
    import pyxis.ui.third_basis_epoch_cumulative_handoff_shell as shell_module

    _, earned, overlay, _ = _persist_valid_overlay(tmp_path, stem="41e-invalid")
    lineage = prove_chromium_research_third_basis_epoch_shell_lineage(
        earned,
        overlay_source=overlay,
    )

    class FakeShell:
        def run(self):
            return object()

    monkeypatch.setattr(
        shell_module,
        "create_third_basis_epoch_cumulative_handoff_research_session_shell",
        lambda supplied: FakeShell(),
    )

    with pytest.raises(TypeError, match="invalid cumulative handoff"):
        cli._run_third_basis_epoch_research_session_shell(lineage)


def test_raw_third_epoch_handoff_runner_passes_exact_reentry_to_distinct_factory(
    tmp_path: Path,
    monkeypatch,
) -> None:
    import pyxis.ui.third_basis_epoch_cumulative_handoff_shell as shell_module

    values = _persist_valid_continuation(tmp_path, stem="41e-raw-runner")
    handoff = values[8].fresh_reentry
    observed: dict[str, object] = {}

    class FakeShell:
        def run(self):
            observed["ran"] = True
            return None

    def fake_factory(reentry):
        observed["reentry"] = reentry
        return FakeShell()

    monkeypatch.setattr(
        shell_module,
        "create_third_basis_epoch_continuation_handoff_research_session_shell",
        fake_factory,
    )

    cli._run_third_basis_epoch_continuation_handoff_research_session_shell(handoff)
    assert observed["reentry"] is handoff
    assert observed["ran"] is True


def test_persisted_third_epoch_continuation_cli_route_still_uses_41a_path_proof_family(
    tmp_path: Path,
    monkeypatch,
) -> None:
    values = _persist_valid_continuation(tmp_path, stem="41e-persisted")
    overlay = values[6]
    observed: dict[str, object] = {}

    def persisted_shell(lineage) -> None:
        observed["lineage"] = lineage

    def fail_raw_handoff(reentry) -> None:
        raise AssertionError("persisted continuation launch must not use raw handoff authority")

    monkeypatch.setattr(
        cli,
        "_run_third_basis_epoch_continuation_research_session_shell",
        persisted_shell,
    )
    monkeypatch.setattr(
        cli,
        "_run_third_basis_epoch_continuation_handoff_research_session_shell",
        fail_raw_handoff,
    )

    assert (
        cli.main(
            [
                "research-shell",
                "--third-basis-epoch-continuation-overlay",
                str(overlay),
            ]
        )
        == 0
    )
    assert "lineage" in observed
