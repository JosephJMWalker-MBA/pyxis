from __future__ import annotations

import builtins
import json
from pathlib import Path

import pytest

import pyxis.cli as cli
from test_app_chromium_research_second_basis_epoch_continuation_reentry_plan_document import (
    _persist_valid_continuation,
)
from test_app_chromium_research_second_basis_epoch_reentry_plan_document import (
    _persist_valid_overlay,
)


def test_research_inspect_emits_deterministic_37b_json_from_explicit_proven_path(
    tmp_path: Path,
    capsys,
) -> None:
    _, _, overlay, _ = _persist_valid_overlay(tmp_path, stem="39b-cli-second")

    assert (
        cli.main(["research-inspect", "--second-basis-epoch-overlay", str(overlay)])
        == 0
    )
    first = capsys.readouterr().out
    assert (
        cli.main(["research-inspect", "--second-basis-epoch-overlay", str(overlay)])
        == 0
    )
    second = capsys.readouterr().out

    assert first == second
    document = json.loads(first)
    assert document["report_role"] == "read_only_inspection_not_authority"
    assert document["launch_provenance"]["launch_family"] == (
        "persisted 37B second-basis-epoch launch"
    )
    assert document["launch_provenance"]["launch_location_context_only"] == str(
        overlay.resolve()
    )
    assert document["current_governed_state"]["declared_continuation_edge_count"] is None


def test_research_inspect_emits_typed_continuation_edge_count(
    tmp_path: Path,
    capsys,
) -> None:
    values = _persist_valid_continuation(tmp_path, stem="39b-cli-continuation")
    overlay = values[6]
    expected = values[8].fresh_reentry

    assert (
        cli.main(
            [
                "research-inspect",
                "--second-basis-epoch-continuation-overlay",
                str(overlay),
            ]
        )
        == 0
    )
    document = json.loads(capsys.readouterr().out)

    assert document["launch_provenance"]["launch_family"] == (
        "persisted 37C/37D continuation launch"
    )
    assert document["launch_provenance"]["launch_location_context_only"] == str(
        overlay.resolve()
    )
    assert document["current_governed_state"]["declared_continuation_edge_count"] == len(
        expected.plan.declared_edge_sources
    )
    assert document["current_governed_state"]["endpoint_sha256"] == (
        expected.controller.declared_endpoint.verification.edge_record_sha256
    )


def test_research_inspect_never_imports_or_launches_textual(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    _, _, overlay, _ = _persist_valid_overlay(tmp_path, stem="39b-cli-no-ui")
    original_import = builtins.__import__

    def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name == "textual" or name.startswith("textual.") or name.startswith("pyxis.ui"):
            raise AssertionError(
                "non-interactive research-inspect must not import or launch Textual"
            )
        return original_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    assert (
        cli.main(["research-inspect", "--second-basis-epoch-overlay", str(overlay)])
        == 0
    )
    document = json.loads(capsys.readouterr().out)
    assert document["report_role"] == "read_only_inspection_not_authority"


def test_research_inspect_invalid_overlay_fails_before_report_emission(
    tmp_path: Path,
    capsys,
) -> None:
    overlay = tmp_path / "invalid.overlay.json"
    overlay.write_text("{}\n", encoding="utf-8")

    with pytest.raises(SystemExit) as exc_info:
        cli.main(["research-inspect", "--second-basis-epoch-overlay", str(overlay)])

    captured = capsys.readouterr()
    assert exc_info.value.code == 2
    assert captured.out == ""
    assert "research-inspect failed" in captured.err


def test_research_inspect_help_exposes_only_explicit_persisted_families(
    capsys,
) -> None:
    with pytest.raises(SystemExit) as exc_info:
        cli.main(["research-inspect", "--help"])

    output = capsys.readouterr().out
    assert exc_info.value.code == 0
    for expected in (
        "--root-backed-overlay",
        "--root-backed-continuation-overlay",
        "--second-basis-epoch-overlay",
        "--second-basis-epoch-continuation-overlay",
        "--third-basis-epoch-overlay",
        "--third-basis-epoch-continuation-overlay",
    ):
        assert expected in output

    for forbidden in (
        "--plan",
        "--latest",
        "--head",
        "--directory",
        "--auto",
        "--handoff",
        "--detect",
        "--format",
    ):
        assert forbidden not in output


def test_research_inspect_entry_families_are_mutually_exclusive(
    tmp_path: Path,
) -> None:
    first = tmp_path / "first.json"
    second = tmp_path / "second.json"

    with pytest.raises(SystemExit) as exc_info:
        cli.main(
            [
                "research-inspect",
                "--second-basis-epoch-overlay",
                str(first),
                "--second-basis-epoch-continuation-overlay",
                str(second),
            ]
        )

    assert exc_info.value.code == 2
