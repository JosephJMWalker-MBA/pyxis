from pathlib import Path

import builtins
import pytest

import pyxis.cli as cli
from pyxis.app.chromium_research_third_basis_epoch_shell_lineage import (
    ChromiumResearchThirdBasisEpochContinuationShellLineage,
    ChromiumResearchThirdBasisEpochShellLineage,
)
from test_app_chromium_research_third_basis_epoch_continuation_checkpoint_extension import (
    _persist_extension,
)
from test_app_chromium_research_third_basis_epoch_continuation_reentry_plan_document import (
    _persist_valid_continuation,
)
from test_app_chromium_research_third_basis_epoch_reentry_plan_document import (
    _persist_valid_overlay,
)


def _forbid_other_or_controller_only_shells(monkeypatch) -> None:
    def fail(*args, **kwargs):
        raise AssertionError(
            "third-epoch CLI launch must retain proven third-epoch lineage rather than route through an older or controller-only shell"
        )

    monkeypatch.setattr(cli, "_run_research_session_shell", fail)
    monkeypatch.setattr(cli, "_run_root_backed_research_session_shell", fail)
    monkeypatch.setattr(
        cli,
        "_run_root_backed_continuation_research_session_shell",
        fail,
    )
    monkeypatch.setattr(cli, "_run_second_basis_epoch_research_session_shell", fail)
    monkeypatch.setattr(
        cli,
        "_run_second_basis_epoch_continuation_research_session_shell",
        fail,
    )
    monkeypatch.setattr(cli, "_run_controller_only_research_session_shell", fail)


def test_research_shell_launches_explicit_40b_overlay_with_proven_lineage(
    tmp_path: Path,
    monkeypatch,
) -> None:
    _, earned, overlay, checkpoint = _persist_valid_overlay(tmp_path, stem="41b-third")
    observed: dict[str, object] = {}

    def fail_workspace(*args, **kwargs):
        raise AssertionError("third-epoch research-shell must not build Workspace state")

    def dedicated(lineage) -> None:
        observed["lineage"] = lineage

    monkeypatch.setattr(cli, "build_and_run_workspace", fail_workspace)
    _forbid_other_or_controller_only_shells(monkeypatch)
    monkeypatch.setattr(cli, "_run_third_basis_epoch_research_session_shell", dedicated)

    exit_code = cli.main(
        ["research-shell", "--third-basis-epoch-overlay", str(overlay)]
    )

    assert exit_code == 0
    lineage = observed["lineage"]
    assert isinstance(lineage, ChromiumResearchThirdBasisEpochShellLineage)
    assert lineage.overlay_source == overlay.resolve()
    assert lineage.reentry is not earned
    assert lineage.reentry is not checkpoint.fresh_reentry
    assert lineage.reentry.controller.presentation == checkpoint.fresh_reentry.controller.presentation
    assert (
        lineage.reentry.controller.declared_endpoint.verification.edge_record_sha256
        == checkpoint.fresh_reentry.controller.declared_endpoint.verification.edge_record_sha256
    )


def test_research_shell_launches_explicit_40c_continuation_with_proven_lineage(
    tmp_path: Path,
    monkeypatch,
) -> None:
    values = _persist_valid_continuation(tmp_path, stem="41b-cont")
    overlay = values[6]
    checkpoint = values[8]
    observed: dict[str, object] = {}

    _forbid_other_or_controller_only_shells(monkeypatch)
    monkeypatch.setattr(
        cli,
        "_run_third_basis_epoch_continuation_research_session_shell",
        lambda lineage: observed.setdefault("lineage", lineage),
    )

    exit_code = cli.main(
        [
            "research-shell",
            "--third-basis-epoch-continuation-overlay",
            str(overlay),
        ]
    )

    assert exit_code == 0
    lineage = observed["lineage"]
    assert isinstance(
        lineage,
        ChromiumResearchThirdBasisEpochContinuationShellLineage,
    )
    assert lineage.overlay_source == overlay.resolve()
    assert lineage.reentry.controller.presentation == checkpoint.fresh_reentry.controller.presentation
    assert (
        lineage.reentry.controller.declared_endpoint.verification.edge_record_sha256
        == checkpoint.fresh_reentry.controller.declared_endpoint.verification.edge_record_sha256
    )


def test_research_shell_launches_cumulative_40d_overlay_through_same_continuation_family(
    tmp_path: Path,
    monkeypatch,
) -> None:
    *_, result = _persist_extension(tmp_path, stem="41b-cumulative")
    observed: dict[str, object] = {}

    _forbid_other_or_controller_only_shells(monkeypatch)
    monkeypatch.setattr(
        cli,
        "_run_third_basis_epoch_continuation_research_session_shell",
        lambda lineage: observed.setdefault("lineage", lineage),
    )

    exit_code = cli.main(
        [
            "research-shell",
            "--third-basis-epoch-continuation-overlay",
            str(result.overlay.path),
        ]
    )

    assert exit_code == 0
    lineage = observed["lineage"]
    assert isinstance(
        lineage,
        ChromiumResearchThirdBasisEpochContinuationShellLineage,
    )
    assert lineage.overlay_source == result.overlay.path.resolve()
    assert lineage.reentry.plan == result.next_plan
    assert lineage.reentry.controller.presentation == result.fresh_reentry.controller.presentation
    assert (
        lineage.reentry.controller.declared_endpoint.verification.edge_record_sha256
        == result.fresh_reentry.controller.declared_endpoint.verification.edge_record_sha256
    )


def test_invalid_third_epoch_overlay_rejects_before_ui(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    overlay = tmp_path / "invalid-third.overlay.json"
    overlay.write_text("{}\n", encoding="utf-8")

    def fail_if_launched(*args, **kwargs):
        raise AssertionError("invalid third-epoch overlay must fail before UI")

    monkeypatch.setattr(
        cli,
        "_run_third_basis_epoch_research_session_shell",
        fail_if_launched,
    )

    with pytest.raises(SystemExit) as exc_info:
        cli.main(["research-shell", "--third-basis-epoch-overlay", str(overlay)])

    assert exc_info.value.code == 2
    assert "research-shell failed" in capsys.readouterr().err


def test_invalid_third_epoch_continuation_overlay_rejects_before_ui(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    overlay = tmp_path / "invalid-third-continuation.overlay.json"
    overlay.write_text("{}\n", encoding="utf-8")

    def fail_if_launched(*args, **kwargs):
        raise AssertionError("invalid third-epoch continuation must fail before UI")

    monkeypatch.setattr(
        cli,
        "_run_third_basis_epoch_continuation_research_session_shell",
        fail_if_launched,
    )

    with pytest.raises(SystemExit) as exc_info:
        cli.main(
            [
                "research-shell",
                "--third-basis-epoch-continuation-overlay",
                str(overlay),
            ]
        )

    assert exc_info.value.code == 2
    assert "research-shell failed" in capsys.readouterr().err


def test_third_epoch_entry_families_remain_mutually_exclusive_with_existing_families(
    tmp_path: Path,
    capsys,
) -> None:
    first = tmp_path / "first.json"
    second = tmp_path / "second.json"

    for left, right in (
        ("--plan", "--third-basis-epoch-overlay"),
        ("--root-backed-overlay", "--third-basis-epoch-overlay"),
        (
            "--second-basis-epoch-overlay",
            "--third-basis-epoch-overlay",
        ),
        (
            "--second-basis-epoch-continuation-overlay",
            "--third-basis-epoch-continuation-overlay",
        ),
        (
            "--third-basis-epoch-overlay",
            "--third-basis-epoch-continuation-overlay",
        ),
    ):
        with pytest.raises(SystemExit) as exc_info:
            cli.main(["research-shell", left, str(first), right, str(second)])
        assert exc_info.value.code == 2

    error = capsys.readouterr().err
    assert "not allowed with argument" in error or "one of the arguments" in error


def test_research_shell_help_exposes_third_epoch_families_without_discovery_flags(
    capsys,
) -> None:
    with pytest.raises(SystemExit) as exc_info:
        cli.main(["research-shell", "--help"])

    output = capsys.readouterr().out
    assert exc_info.value.code == 0
    for explicit in (
        "--third-basis-epoch-overlay",
        "--third-basis-epoch-continuation-overlay",
    ):
        assert explicit in output

    for forbidden in (
        "--latest",
        "--head",
        "--directory",
        "--auto",
        "--detect",
        "--format",
    ):
        assert forbidden not in output


def test_third_epoch_shell_ui_dependency_remains_lazy(
    tmp_path: Path,
    monkeypatch,
) -> None:
    _, earned, overlay, _ = _persist_valid_overlay(tmp_path, stem="41b-lazy")
    lineage = cli.prove_chromium_research_third_basis_epoch_shell_lineage(
        earned,
        overlay_source=overlay,
    )
    original_import = builtins.__import__

    def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name == "pyxis.ui.third_basis_epoch_research_session_shell":
            raise ModuleNotFoundError("No module named 'textual'", name="textual")
        return original_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    with pytest.raises(RuntimeError, match=r"pyxis\[ui\]"):
        cli._run_third_basis_epoch_research_session_shell(lineage)
