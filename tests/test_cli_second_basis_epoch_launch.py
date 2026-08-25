from pathlib import Path

import pytest

import pyxis.cli as cli
from test_app_chromium_research_second_basis_epoch_continuation_checkpoint_extension import (
    _persist_extension as _persist_second_epoch_extension,
)
from test_app_chromium_research_second_basis_epoch_continuation_reentry_plan_document import (
    _persist_valid_continuation as _persist_second_epoch_continuation,
)
from test_app_chromium_research_second_basis_epoch_reentry_plan_document import (
    _persist_valid_overlay as _persist_second_epoch_overlay,
)


def _forbid_legacy_lineage_shells(monkeypatch) -> None:
    def fail(*args, **kwargs):
        raise AssertionError(
            "second-epoch CLI launch must not fabricate ordinary or first-root checkpoint lineage"
        )

    monkeypatch.setattr(cli, "_run_research_session_shell", fail)
    monkeypatch.setattr(cli, "_run_root_backed_research_session_shell", fail)
    monkeypatch.setattr(
        cli,
        "_run_root_backed_continuation_research_session_shell",
        fail,
    )


def test_research_shell_launches_explicit_37b_overlay_controller_only(
    tmp_path: Path,
    monkeypatch,
) -> None:
    _, earned, overlay, checkpoint = _persist_second_epoch_overlay(
        tmp_path,
        stem="38a-second",
    )
    observed: dict[str, object] = {}

    def fail_workspace(*args, **kwargs):
        raise AssertionError("second-epoch research-shell must not build Workspace state")

    def controller_only(controller) -> None:
        observed["controller"] = controller

    monkeypatch.setattr(cli, "build_and_run_workspace", fail_workspace)
    _forbid_legacy_lineage_shells(monkeypatch)
    monkeypatch.setattr(cli, "_run_controller_only_research_session_shell", controller_only)

    exit_code = cli.main(
        ["research-shell", "--second-basis-epoch-overlay", str(overlay)]
    )

    assert exit_code == 0
    controller = observed["controller"]
    assert controller is not earned.controller
    assert controller.presentation == checkpoint.fresh_reentry.controller.presentation
    assert (
        controller.declared_endpoint.verification.edge_record_sha256
        == checkpoint.fresh_reentry.controller.declared_endpoint.verification.edge_record_sha256
    )


def test_research_shell_launches_explicit_37c_continuation_controller_only(
    tmp_path: Path,
    monkeypatch,
) -> None:
    values = _persist_second_epoch_continuation(tmp_path, stem="38a-cont")
    rollover = values[5]
    overlay = values[6]
    checkpoint = values[8]
    observed: dict[str, object] = {}

    _forbid_legacy_lineage_shells(monkeypatch)
    monkeypatch.setattr(
        cli,
        "_run_controller_only_research_session_shell",
        lambda controller: observed.setdefault("controller", controller),
    )

    exit_code = cli.main(
        [
            "research-shell",
            "--second-basis-epoch-continuation-overlay",
            str(overlay),
        ]
    )

    assert exit_code == 0
    controller = observed["controller"]
    assert controller.presentation == rollover.continuation_controller.presentation
    assert (
        controller.declared_endpoint.verification.edge_record_sha256
        == checkpoint.fresh_reentry.controller.declared_endpoint.verification.edge_record_sha256
    )


def test_research_shell_launches_cumulative_37d_overlay_through_same_explicit_family(
    tmp_path: Path,
    monkeypatch,
) -> None:
    values = _persist_second_epoch_extension(tmp_path, stem="38a-cumulative")
    next_overlay = values[6]
    result = values[8]
    observed: dict[str, object] = {}

    _forbid_legacy_lineage_shells(monkeypatch)
    monkeypatch.setattr(
        cli,
        "_run_controller_only_research_session_shell",
        lambda controller: observed.setdefault("controller", controller),
    )

    exit_code = cli.main(
        [
            "research-shell",
            "--second-basis-epoch-continuation-overlay",
            str(next_overlay),
        ]
    )

    assert exit_code == 0
    controller = observed["controller"]
    assert (
        controller.declared_endpoint.verification.edge_record_sha256
        == result.fresh_reentry.controller.declared_endpoint.verification.edge_record_sha256
    )
    assert controller.presentation == result.fresh_reentry.controller.presentation
    assert len(controller.presentation.sequence.members) == len(
        result.next_plan.declared_edge_sources
    )


def test_invalid_second_epoch_overlay_rejects_before_ui(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    overlay = tmp_path / "invalid-second.overlay.json"
    overlay.write_text("{}\n", encoding="utf-8")

    def fail_if_launched(*args, **kwargs):
        raise AssertionError("invalid second-epoch overlay must fail before UI")

    monkeypatch.setattr(
        cli,
        "_run_controller_only_research_session_shell",
        fail_if_launched,
    )

    with pytest.raises(SystemExit) as exc_info:
        cli.main(
            ["research-shell", "--second-basis-epoch-overlay", str(overlay)]
        )

    assert exc_info.value.code == 2
    assert "research-shell failed" in capsys.readouterr().err


def test_invalid_second_epoch_continuation_overlay_rejects_before_ui(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    overlay = tmp_path / "invalid-second-continuation.overlay.json"
    overlay.write_text("{}\n", encoding="utf-8")

    def fail_if_launched(*args, **kwargs):
        raise AssertionError("invalid second-epoch continuation must fail before UI")

    monkeypatch.setattr(
        cli,
        "_run_controller_only_research_session_shell",
        fail_if_launched,
    )

    with pytest.raises(SystemExit) as exc_info:
        cli.main(
            [
                "research-shell",
                "--second-basis-epoch-continuation-overlay",
                str(overlay),
            ]
        )

    assert exc_info.value.code == 2
    assert "research-shell failed" in capsys.readouterr().err


def test_second_epoch_entry_families_remain_mutually_exclusive_with_every_other_family(
    tmp_path: Path,
    capsys,
) -> None:
    first = tmp_path / "first.json"
    second = tmp_path / "second.json"

    for left, right in (
        ("--plan", "--second-basis-epoch-overlay"),
        ("--root-backed-overlay", "--second-basis-epoch-overlay"),
        (
            "--root-backed-continuation-overlay",
            "--second-basis-epoch-continuation-overlay",
        ),
        (
            "--second-basis-epoch-overlay",
            "--second-basis-epoch-continuation-overlay",
        ),
    ):
        with pytest.raises(SystemExit) as exc_info:
            cli.main(["research-shell", left, str(first), right, str(second)])
        assert exc_info.value.code == 2

    error = capsys.readouterr().err
    assert "not allowed with argument" in error or "one of the arguments" in error


def test_research_shell_help_exposes_second_epoch_families_without_discovery_flags(
    capsys,
) -> None:
    with pytest.raises(SystemExit) as exc_info:
        cli.main(["research-shell", "--help"])

    output = capsys.readouterr().out
    assert exc_info.value.code == 0
    for explicit in (
        "--plan",
        "--root-backed-overlay",
        "--root-backed-continuation-overlay",
        "--second-basis-epoch-overlay",
        "--second-basis-epoch-continuation-overlay",
    ):
        assert explicit in output

    for forbidden in (
        "--latest",
        "--head",
        "--directory",
        "--auto",
        "--overlay ",
        "--detect",
        "--format",
    ):
        assert forbidden not in output
