from __future__ import annotations

import builtins
import json
from pathlib import Path

import pytest

import pyxis.cli as cli
from pyxis.app.chromium_research_root_backed_session_authority_inspection import (
    inspect_chromium_research_root_backed_session_continuation_launch,
)
from pyxis.app.chromium_research_root_backed_session_authority_inspection_report import (
    serialize_chromium_research_root_backed_session_authority_inspection,
)
from pyxis.app.chromium_research_root_backed_session_continuation_reentry_plan_document import (
    load_chromium_research_root_backed_session_continuation_reentry_plan_document,
    reenter_chromium_research_root_backed_session_continuation,
)
from pyxis.app.chromium_research_root_backed_session_shell_lineage import (
    prove_chromium_research_root_backed_session_continuation_shell_lineage,
)
from test_app_chromium_research_root_backed_session_continuation_checkpoint_extension import (
    _persist_extension,
)
from test_app_chromium_research_root_backed_session_continuation_reentry_plan_document import (
    _persist_valid_continuation,
)
from test_app_chromium_research_root_backed_session_reentry_plan_document import (
    _persist_valid_overlay,
)


def test_research_inspect_emits_deterministic_35c_json_from_explicit_proven_path(
    tmp_path: Path,
    capsys,
) -> None:
    _, _, _, _, overlay, _ = _persist_valid_overlay(tmp_path, stem="45b-cli-35c")

    assert cli.main(["research-inspect", "--root-backed-overlay", str(overlay)]) == 0
    first = capsys.readouterr().out
    assert cli.main(["research-inspect", "--root-backed-overlay", str(overlay)]) == 0
    second = capsys.readouterr().out

    assert first == second
    document = json.loads(first)
    assert document["format"] == (
        "pyxis.chromium.research_root_backed_session_authority_inspection.v1"
    )
    assert document["report_role"] == "read_only_inspection_not_authority"
    assert document["launch_provenance"]["launch_family"] == (
        "persisted 35C root-backed launch"
    )
    assert document["launch_provenance"]["launch_location_context_only"] == str(
        overlay.resolve()
    )
    assert "root_sha256" in document["launch_provenance"]
    assert document["current_governed_state"]["declared_continuation_edge_count"] is None


def test_research_inspect_35d_output_equals_direct_shared_projection_serialization(
    tmp_path: Path,
    capsys,
) -> None:
    values = _persist_valid_continuation(tmp_path, stem="45b-cli-35d")
    overlay = values[8]

    assert (
        cli.main(
            [
                "research-inspect",
                "--root-backed-continuation-overlay",
                str(overlay),
            ]
        )
        == 0
    )
    emitted = capsys.readouterr().out

    plan = load_chromium_research_root_backed_session_continuation_reentry_plan_document(
        overlay
    )
    reentry = reenter_chromium_research_root_backed_session_continuation(plan)
    lineage = prove_chromium_research_root_backed_session_continuation_shell_lineage(
        reentry,
        overlay_source=overlay,
    )
    expected = serialize_chromium_research_root_backed_session_authority_inspection(
        inspect_chromium_research_root_backed_session_continuation_launch(lineage)
    )

    assert emitted == expected
    document = json.loads(emitted)
    assert document["launch_provenance"]["launch_family"] == (
        "persisted 35D/35E root-backed continuation launch"
    )
    assert document["current_governed_state"]["declared_continuation_edge_count"] == len(
        reentry.plan.declared_edge_sources
    )
    assert document["current_governed_state"]["endpoint_sha256"] == (
        reentry.controller.declared_endpoint.verification.edge_record_sha256
    )


def test_research_inspect_accepts_cumulative_35e_through_same_continuation_flag(
    tmp_path: Path,
    capsys,
) -> None:
    *_, result = _persist_extension(tmp_path, stem="45b-cli-35e")

    assert (
        cli.main(
            [
                "research-inspect",
                "--root-backed-continuation-overlay",
                str(result.overlay.path),
            ]
        )
        == 0
    )
    document = json.loads(capsys.readouterr().out)

    assert document["launch_provenance"]["launch_location_context_only"] == str(
        result.overlay.path.resolve()
    )
    assert document["current_governed_state"]["declared_continuation_edge_count"] == len(
        result.fresh_reentry.plan.declared_edge_sources
    )


def test_root_backed_research_inspect_never_imports_or_launches_textual(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    _, _, _, _, overlay, _ = _persist_valid_overlay(tmp_path, stem="45b-cli-no-ui")
    original_import = builtins.__import__

    def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name == "textual" or name.startswith("textual.") or name.startswith("pyxis.ui"):
            raise AssertionError(
                "non-interactive one-root research-inspect must not import or launch Textual"
            )
        return original_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    assert cli.main(["research-inspect", "--root-backed-overlay", str(overlay)]) == 0
    document = json.loads(capsys.readouterr().out)
    assert document["report_role"] == "read_only_inspection_not_authority"


def test_root_backed_research_inspect_invalid_overlay_fails_before_report_emission(
    tmp_path: Path,
    capsys,
) -> None:
    overlay = tmp_path / "invalid-root-backed.overlay.json"
    overlay.write_text("{}\n", encoding="utf-8")

    with pytest.raises(SystemExit) as exc_info:
        cli.main(["research-inspect", "--root-backed-overlay", str(overlay)])

    captured = capsys.readouterr()
    assert exc_info.value.code == 2
    assert captured.out == ""
    assert "research-inspect failed" in captured.err


def test_all_six_research_inspect_entry_families_remain_mutually_exclusive(
    tmp_path: Path,
) -> None:
    first = tmp_path / "first.json"
    second = tmp_path / "second.json"
    pairs = (
        ("--root-backed-overlay", "--root-backed-continuation-overlay"),
        ("--root-backed-overlay", "--second-basis-epoch-overlay"),
        (
            "--root-backed-continuation-overlay",
            "--second-basis-epoch-continuation-overlay",
        ),
        ("--root-backed-overlay", "--third-basis-epoch-overlay"),
        (
            "--second-basis-epoch-overlay",
            "--third-basis-epoch-continuation-overlay",
        ),
        ("--third-basis-epoch-overlay", "--third-basis-epoch-continuation-overlay"),
    )

    for left, right in pairs:
        with pytest.raises(SystemExit) as exc_info:
            cli.main(
                [
                    "research-inspect",
                    left,
                    str(first),
                    right,
                    str(second),
                ]
            )
        assert exc_info.value.code == 2


def test_research_inspect_help_exposes_persisted_families_only(capsys) -> None:
    with pytest.raises(SystemExit) as exc_info:
        cli.main(["research-inspect", "--help"])

    output = capsys.readouterr().out
    assert exc_info.value.code == 0
    for flag in (
        "--root-backed-overlay",
        "--root-backed-continuation-overlay",
        "--second-basis-epoch-overlay",
        "--second-basis-epoch-continuation-overlay",
        "--third-basis-epoch-overlay",
        "--third-basis-epoch-continuation-overlay",
    ):
        assert flag in output
    for forbidden in (
        "--44h",
        "--36d",
        "--handoff",
        "--latest",
        "--head",
        "--directory",
        "--auto",
        "--format",
    ):
        assert forbidden not in output
