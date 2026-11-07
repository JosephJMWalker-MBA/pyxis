from __future__ import annotations

import json
from pathlib import Path

import pytest

import pyxis.cli as cli
import pyxis.cli_research_reopen as research_reopen_cli
from pyxis.app.chromium_research_initial_session_reentry import (
    reenter_chromium_research_initial_session,
)
from test_app_chromium_research_capture import ENDPOINT, TARGET_ID, URL
from test_app_chromium_research_initial_session_reentry import _durable_root


_RATIONALE = "  First governed rationale 😀\nStill explicitly human-owned.  "


def _command(paths: tuple[Path, Path, Path, Path], *, include_content: bool = False) -> list[str]:
    command = [
        "research-reopen",
        "--capture", str(paths[0]),
        "--selection", str(paths[1]),
        "--working-set", str(paths[2]),
        "--note", str(paths[3]),
    ]
    if include_content:
        command.append("--include-content")
    return command


def _snapshot(paths: tuple[Path, Path, Path, Path]) -> tuple[bytes, ...]:
    return tuple(path.read_bytes() for path in paths)


def test_51f_cli_reopens_valid_root_without_exposing_content_by_default(
    tmp_path: Path,
    capsys,
) -> None:
    paths = _durable_root(tmp_path, stem="root")
    before = _snapshot(paths)

    assert cli.main(_command(paths)) == 0
    output = capsys.readouterr().out
    receipt = json.loads(output)

    assert receipt == {
        "capture_input_context_only": str(paths[0].resolve()),
        "selection_input_context_only": str(paths[1].resolve()),
        "working_set_input_context_only": str(paths[2].resolve()),
        "note_input_context_only": str(paths[3].resolve()),
        "working_set_format": "pyxis.chromium.research_working_set.v2",
        "working_set_record_sha256": receipt["working_set_record_sha256"],
        "note_format": "pyxis.chromium.research_working_set_note.v2",
        "note_record_sha256": receipt["note_record_sha256"],
        "initial_session_mode": "read_only_initial_research_session_root",
        "member_count": 1,
        "content_included": False,
        "receipt_role": (
            "read_only_reentry_inspection_not_evidence_or_session_head_authority"
        ),
    }
    assert len(receipt["working_set_record_sha256"]) == 64
    assert len(receipt["note_record_sha256"]) == 64
    assert output == json.dumps(receipt, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    for secret_or_content in (_RATIONALE, "😀", URL, ENDPOINT, TARGET_ID):
        assert secret_or_content not in output
    assert "source_members" not in receipt
    assert "human_rationale" not in receipt
    assert "current" not in receipt
    assert "latest" not in receipt
    assert "head" not in receipt
    assert _snapshot(paths) == before


def test_51f_opt_in_shows_verified_source_separate_from_human_rationale(
    tmp_path: Path,
    capsys,
) -> None:
    paths = _durable_root(tmp_path, stem="root")
    before = _snapshot(paths)

    assert cli.main(_command(paths, include_content=True)) == 0
    receipt = json.loads(capsys.readouterr().out)

    assert receipt["content_included"] is True
    assert receipt["human_rationale"] == {
        "role": "human_authored_rationale_not_source_evidence",
        "text": _RATIONALE,
    }
    member = receipt["source_members"][0]
    assert member["member_kind"] == "exact_range_selection"
    assert member["member_position"] == 1
    assert member["human_note_text"] is None
    excerpt = member["excerpts"][0]
    assert excerpt["role"] == "bounded_observed_source_not_verified_truth"
    assert excerpt["text"] == "😀"
    assert excerpt["url_observed"] == URL
    assert excerpt["paragraph_ordinal"] == 1
    assert excerpt["start_offset"] == 6
    assert excerpt["end_offset"] == 7
    assert excerpt["offset_unit"] == "unicode_code_point"
    assert excerpt["paragraph_text_truncated"] is False
    assert _snapshot(paths) == before


def test_51f_cli_delegates_exactly_once_to_public_51e(
    tmp_path: Path,
    capsys,
    monkeypatch,
) -> None:
    paths = _durable_root(tmp_path, stem="root")
    actual = reenter_chromium_research_initial_session(
        capture_source=paths[0],
        selection_source=paths[1],
        working_set_source=paths[2],
        note_source=paths[3],
    )
    received: list[dict[str, Path]] = []

    def instrument(**kwargs):
        received.append(kwargs)
        return actual

    monkeypatch.setattr(
        research_reopen_cli, "reenter_chromium_research_initial_session", instrument
    )
    assert cli.main(_command(paths)) == 0
    assert json.loads(capsys.readouterr().out)["member_count"] == 1
    assert received == [{
        "capture_source": paths[0],
        "selection_source": paths[1],
        "working_set_source": paths[2],
        "note_source": paths[3],
    }]


@pytest.mark.parametrize("wrong_index", (0, 1, 2, 3))
def test_51f_wrong_valid_cross_root_input_fails_without_output_or_mutation(
    tmp_path: Path,
    capsys,
    wrong_index: int,
) -> None:
    paths_a = _durable_root(tmp_path, stem="root-a")
    paths_b = _durable_root(
        tmp_path, stem="root-b", text="Alpha 😀 other source", rationale="Other rationale"
    )
    supplied = list(paths_a)
    supplied[wrong_index] = paths_b[wrong_index]
    paths = tuple(supplied)
    before = _snapshot(paths)

    with pytest.raises(SystemExit) as exc:
        cli.main(_command(paths))
    assert exc.value.code == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "research-reopen failed:" in captured.err
    assert _snapshot(paths) == before


@pytest.mark.parametrize("tampered_index", (0, 1, 2, 3))
def test_51f_tampered_durable_input_fails_without_output_or_repair(
    tmp_path: Path,
    capsys,
    tampered_index: int,
) -> None:
    paths = _durable_root(tmp_path, stem="root")
    paths[tampered_index].write_bytes(b"{}\n")
    before = _snapshot(paths)

    with pytest.raises(SystemExit) as exc:
        cli.main(_command(paths))
    assert exc.value.code == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "research-reopen failed:" in captured.err
    assert _snapshot(paths) == before


def test_51f_missing_explicit_location_rejected_by_cli(tmp_path: Path, capsys) -> None:
    paths = _durable_root(tmp_path, stem="root")
    with pytest.raises(SystemExit) as exc:
        cli.main(_command(paths)[:-2])
    assert exc.value.code == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "--note" in captured.err


def test_51f_no_auto_browser_acquisition_in_cli_path(tmp_path: Path, capsys, monkeypatch) -> None:
    paths = _durable_root(tmp_path, stem="root")

    def no_browser(*args, **kwargs):
        pytest.fail("research-reopen must not acquire Chromium")

    monkeypatch.setattr(cli, "observe_chromium_page_research_bundle", no_browser)
    assert cli.main(_command(paths)) == 0
    assert json.loads(capsys.readouterr().out)["content_included"] is False
