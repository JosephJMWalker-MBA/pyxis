from __future__ import annotations

import builtins
import json
from pathlib import Path

import pytest

import pyxis.cli as cli
from pyxis.app.chromium_research_third_basis_epoch_authority_inspection import (
    inspect_chromium_research_third_basis_epoch_continuation_launch,
)
from pyxis.app.chromium_research_third_basis_epoch_authority_inspection_report import (
    serialize_chromium_research_third_basis_epoch_authority_inspection,
)
from pyxis.app.chromium_research_third_basis_epoch_continuation_reentry_plan_document import (
    load_chromium_research_third_basis_epoch_continuation_reentry_plan_document,
    reenter_chromium_research_third_basis_epoch_continuation,
)
from pyxis.app.chromium_research_third_basis_epoch_shell_lineage import (
    prove_chromium_research_third_basis_epoch_continuation_shell_lineage,
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


def test_research_inspect_emits_deterministic_40b_json_from_explicit_proven_path(
    tmp_path: Path,
    capsys,
) -> None:
    _, _, overlay, _ = _persist_valid_overlay(tmp_path, stem="42b-cli-40b")

    assert cli.main(["research-inspect", "--third-basis-epoch-overlay", str(overlay)]) == 0
    first = capsys.readouterr().out
    assert cli.main(["research-inspect", "--third-basis-epoch-overlay", str(overlay)]) == 0
    second = capsys.readouterr().out

    assert first == second
    document = json.loads(first)
    assert document["format"] == (
        "pyxis.chromium.research_third_basis_epoch_authority_inspection.v1"
    )
    assert document["report_role"] == "read_only_inspection_not_authority"
    assert document["launch_provenance"]["launch_family"] == (
        "persisted 40B third-basis-epoch launch"
    )
    assert document["launch_provenance"]["launch_location_context_only"] == str(
        overlay.resolve()
    )
    assert "third_root_sha256" in document["launch_provenance"]
    assert document["current_governed_state"]["declared_continuation_edge_count"] is None


def test_research_inspect_40c_output_equals_direct_shared_projection_serialization(
    tmp_path: Path,
    capsys,
) -> None:
    values = _persist_valid_continuation(tmp_path, stem="42b-cli-40c")
    overlay = values[6]

    assert (
        cli.main(
            [
                "research-inspect",
                "--third-basis-epoch-continuation-overlay",
                str(overlay),
            ]
        )
        == 0
    )
    emitted = capsys.readouterr().out

    plan = load_chromium_research_third_basis_epoch_continuation_reentry_plan_document(
        overlay
    )
    reentry = reenter_chromium_research_third_basis_epoch_continuation(plan)
    lineage = prove_chromium_research_third_basis_epoch_continuation_shell_lineage(
        reentry,
        overlay_source=overlay,
    )
    expected = serialize_chromium_research_third_basis_epoch_authority_inspection(
        inspect_chromium_research_third_basis_epoch_continuation_launch(lineage)
    )

    assert emitted == expected
    document = json.loads(emitted)
    assert document["launch_provenance"]["launch_family"] == (
        "persisted 40C/40D continuation launch"
    )
    assert document["current_governed_state"]["declared_continuation_edge_count"] == len(
        reentry.plan.declared_edge_sources
    )
    assert document["current_governed_state"]["endpoint_sha256"] == (
        reentry.controller.declared_endpoint.verification.edge_record_sha256
    )


def test_research_inspect_accepts_cumulative_40d_through_same_continuation_flag(
    tmp_path: Path,
    capsys,
) -> None:
    *_, result = _persist_extension(tmp_path, stem="42b-cli-40d")

    assert (
        cli.main(
            [
                "research-inspect",
                "--third-basis-epoch-continuation-overlay",
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


def test_third_epoch_research_inspect_never_imports_or_launches_textual(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    _, _, overlay, _ = _persist_valid_overlay(tmp_path, stem="42b-cli-no-ui")
    original_import = builtins.__import__

    def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name == "textual" or name.startswith("textual.") or name.startswith("pyxis.ui"):
            raise AssertionError(
                "non-interactive third-epoch research-inspect must not import or launch Textual"
            )
        return original_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    assert cli.main(["research-inspect", "--third-basis-epoch-overlay", str(overlay)]) == 0
    document = json.loads(capsys.readouterr().out)
    assert document["report_role"] == "read_only_inspection_not_authority"


def test_third_epoch_research_inspect_invalid_overlay_fails_before_report_emission(
    tmp_path: Path,
    capsys,
) -> None:
    overlay = tmp_path / "invalid-third.overlay.json"
    overlay.write_text("{}\n", encoding="utf-8")

    with pytest.raises(SystemExit) as exc_info:
        cli.main(["research-inspect", "--third-basis-epoch-overlay", str(overlay)])

    captured = capsys.readouterr()
    assert exc_info.value.code == 2
    assert captured.out == ""
    assert "research-inspect failed" in captured.err


def test_all_four_research_inspect_entry_families_remain_mutually_exclusive(
    tmp_path: Path,
) -> None:
    first = tmp_path / "first.json"
    second = tmp_path / "second.json"
    pairs = (
        ("--second-basis-epoch-overlay", "--third-basis-epoch-overlay"),
        (
            "--second-basis-epoch-continuation-overlay",
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
