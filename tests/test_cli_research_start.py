from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

import pyxis.cli as cli
import pyxis.cli_research_start as research_start_cli
from pyxis.app import (
    load_chromium_page_research_capture,
    load_chromium_research_paragraph_text_selection,
    persist_chromium_page_research_capture,
    persist_chromium_research_paragraph_text_selection,
    select_chromium_research_capture_paragraph,
    select_chromium_research_paragraph_text,
)
from pyxis.app.chromium_paragraphs import (
    ChromiumPageParagraphEvidence,
    ChromiumPageParagraphsEvidence,
)
from pyxis.app.chromium_research_working_set_note_load import (
    load_chromium_research_working_set_note,
)
from pyxis.app.chromium_research_working_set_persistence import (
    verify_chromium_research_working_set,
)
from test_app_chromium_research_capture import (
    ENDPOINT,
    TARGET_ID,
    URL,
    _bundle,
)


_TEXT = "Alpha 😀 beta"
_RATIONALE = "  First governed rationale 😀\nStill explicitly human-owned.  "


def _capture_with_text(tmp_path: Path, *, name: str, text: str) -> Path:
    base = _bundle()
    paragraph = ChromiumPageParagraphEvidence(
        ordinal=1,
        element_id="passage",
        text_prefix=text,
        text_character_count=len(text),
        text_limit=max(64, len(text)),
        truncated=False,
    )
    paragraphs = ChromiumPageParagraphsEvidence(
        endpoint=ENDPOINT,
        target_id=TARGET_ID,
        url=URL,
        source="document.querySelectorAll('p')",
        paragraphs=(paragraph,),
        paragraph_count=1,
        paragraph_limit=128,
        truncated=False,
    )
    path = tmp_path / name
    persist_chromium_page_research_capture(
        replace(base, paragraphs=paragraphs),
        path,
    )
    return path


def _saved_selection(
    tmp_path: Path,
    capture_path: Path,
    *,
    name: str = "saved-selection.json",
) -> Path:
    capture = load_chromium_page_research_capture(capture_path)
    paragraph = select_chromium_research_capture_paragraph(
        capture,
        paragraph_ordinal=1,
    )
    selection = select_chromium_research_paragraph_text(
        paragraph,
        start_offset=6,
        end_offset=7,
    )
    path = tmp_path / name
    persist_chromium_research_paragraph_text_selection(selection, path)
    return path


def _command(
    capture: Path,
    selection: Path,
    working_set: Path,
    note: Path,
    *,
    rationale: str = _RATIONALE,
) -> list[str]:
    return [
        "research-start",
        "--capture",
        str(capture),
        "--selection",
        str(selection),
        "--rationale",
        rationale,
        "--working-set-destination",
        str(working_set),
        "--note-destination",
        str(note),
    ]


def test_51d_research_start_creates_existing_v2_root_and_fresh_51c_receipt(
    tmp_path: Path,
    capsys,
) -> None:
    capture_path = _capture_with_text(tmp_path, name="capture.json", text=_TEXT)
    selection_path = _saved_selection(tmp_path, capture_path)
    working_set_path = tmp_path / "working-set.json"
    note_path = tmp_path / "working-set-note.json"

    assert (
        cli.main(
            _command(
                capture_path,
                selection_path,
                working_set_path,
                note_path,
            )
        )
        == 0
    )

    output = capsys.readouterr().out
    receipt = json.loads(output)

    fresh_capture = load_chromium_page_research_capture(capture_path)
    fresh_member = load_chromium_research_paragraph_text_selection(
        fresh_capture,
        selection_path,
    )
    loaded = load_chromium_research_working_set_note(
        (fresh_member,),
        working_set_path,
        note_path,
    )

    expected = {
        "capture_input_context_only": str(capture_path.resolve()),
        "initial_session_mode": "read_only_initial_research_session_root",
        "note_format": "pyxis.chromium.research_working_set_note.v2",
        "note_output_path": str(note_path.resolve()),
        "note_record_sha256": loaded.verification.note_record_sha256,
        "receipt_role": "operation_receipt_not_evidence_or_session_head_authority",
        "selection_input_context_only": str(selection_path.resolve()),
        "working_set_format": "pyxis.chromium.research_working_set.v2",
        "working_set_output_path": str(working_set_path.resolve()),
        "working_set_record_sha256": (
            loaded.working_set.verification.working_set_record_sha256
        ),
    }
    assert receipt == expected
    assert output == json.dumps(
        expected,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    ) + "\n"

    assert loaded.note.note_text == _RATIONALE
    assert len(loaded.note.working_set.items) == 1
    assert loaded.note.working_set.items[0] is fresh_member
    assert fresh_member.selection.selected_text == "😀"
    assert _RATIONALE not in output
    assert "😀" not in output
    assert URL not in output
    assert ENDPOINT not in output
    assert TARGET_ID not in output
    assert "current" not in receipt
    assert "latest" not in receipt
    assert "head" not in receipt


def test_51d_cli_composes_existing_boundaries_in_mutation_safe_order(
    tmp_path: Path,
    capsys,
    monkeypatch,
) -> None:
    capture_path = tmp_path / "capture.json"
    selection_path = tmp_path / "selection.json"
    working_set_path = tmp_path / "working-set.json"
    note_path = tmp_path / "note.json"

    capture = SimpleNamespace(verification=SimpleNamespace(path=capture_path.resolve()))
    member = SimpleNamespace(verification=SimpleNamespace(path=selection_path.resolve()))
    working_set = object()
    note = object()
    persisted_working_set = SimpleNamespace(path=working_set_path.resolve())
    persisted_note = SimpleNamespace(path=note_path.resolve())
    loaded = SimpleNamespace(
        verification=SimpleNamespace(
            path=note_path.resolve(),
            note_format="pyxis.chromium.research_working_set_note.v2",
            note_record_sha256="b" * 64,
        ),
        working_set=SimpleNamespace(
            verification=SimpleNamespace(
                path=working_set_path.resolve(),
                working_set_format="pyxis.chromium.research_working_set.v2",
                working_set_record_sha256="a" * 64,
            )
        ),
        note=SimpleNamespace(
            working_set=SimpleNamespace(items=(member,)),
        ),
    )
    controller = SimpleNamespace(
        presentation=SimpleNamespace(
            presentation_mode="read_only_initial_research_session_root"
        )
    )
    calls: list[tuple[object, ...]] = []

    def load_capture(path):
        calls.append(("16C", path))
        return capture

    def load_selection(source, path):
        calls.append(("49B", source, path))
        return member

    def create_working_set(items):
        calls.append(("20A", tuple(items)))
        return working_set

    def create_note(parent, *, note_text):
        calls.append(("21A", parent, note_text))
        return note

    def persist_working_set(parent, destination):
        calls.append(("20B-v2", parent, destination))
        return persisted_working_set

    def persist_note(record, parent_source, destination):
        calls.append(("21B-v2", record, parent_source, destination))
        return persisted_note

    def load_note(items, parent_source, source):
        calls.append(("21C", tuple(items), parent_source, source))
        return loaded

    def make_controller(root):
        calls.append(("51C", root))
        return controller

    monkeypatch.setattr(research_start_cli, "load_chromium_page_research_capture", load_capture)
    monkeypatch.setattr(
        research_start_cli,
        "load_chromium_research_paragraph_text_selection",
        load_selection,
    )
    monkeypatch.setattr(
        research_start_cli,
        "create_chromium_research_working_set",
        create_working_set,
    )
    monkeypatch.setattr(
        research_start_cli,
        "create_chromium_research_working_set_note",
        create_note,
    )
    monkeypatch.setattr(
        research_start_cli,
        "persist_chromium_research_working_set_v2",
        persist_working_set,
    )
    monkeypatch.setattr(
        research_start_cli,
        "persist_chromium_research_working_set_note_v2",
        persist_note,
    )
    monkeypatch.setattr(
        research_start_cli,
        "load_chromium_research_working_set_note",
        load_note,
    )
    monkeypatch.setattr(
        research_start_cli,
        "ChromiumResearchInitialSessionController",
        make_controller,
    )

    assert (
        cli.main(
            _command(
                capture_path,
                selection_path,
                working_set_path,
                note_path,
            )
        )
        == 0
    )

    assert calls == [
        ("16C", capture_path),
        ("49B", capture, selection_path),
        ("20A", (member,)),
        ("21A", working_set, _RATIONALE),
        ("20B-v2", working_set, working_set_path.resolve()),
        ("21B-v2", note, working_set_path.resolve(), note_path.resolve()),
        ("21C", (member,), working_set_path.resolve(), note_path.resolve()),
        ("51C", loaded),
    ]
    receipt = json.loads(capsys.readouterr().out)
    assert receipt["working_set_record_sha256"] == "a" * 64
    assert receipt["note_record_sha256"] == "b" * 64


def test_51d_wrong_capture_for_saved_selection_fails_before_root_mutation(
    tmp_path: Path,
    capsys,
) -> None:
    first_capture = _capture_with_text(tmp_path, name="first.json", text=_TEXT)
    second_capture = _capture_with_text(
        tmp_path,
        name="second.json",
        text="Different captured paragraph",
    )
    selection_path = _saved_selection(tmp_path, first_capture)
    working_set_path = tmp_path / "working-set.json"
    note_path = tmp_path / "note.json"

    with pytest.raises(SystemExit) as exc_info:
        cli.main(
            _command(
                second_capture,
                selection_path,
                working_set_path,
                note_path,
            )
        )

    assert exc_info.value.code == 2
    assert not working_set_path.exists()
    assert not note_path.exists()
    assert "research-start failed" in capsys.readouterr().err


def test_51d_whitespace_rationale_fails_through_public_21a_before_mutation(
    tmp_path: Path,
    capsys,
) -> None:
    capture_path = _capture_with_text(tmp_path, name="capture.json", text=_TEXT)
    selection_path = _saved_selection(tmp_path, capture_path)
    working_set_path = tmp_path / "working-set.json"
    note_path = tmp_path / "note.json"

    with pytest.raises(SystemExit) as exc_info:
        cli.main(
            _command(
                capture_path,
                selection_path,
                working_set_path,
                note_path,
                rationale=" \t\n ",
            )
        )

    assert exc_info.value.code == 2
    assert not working_set_path.exists()
    assert not note_path.exists()
    assert "research-start failed" in capsys.readouterr().err


def test_51d_same_resolved_destinations_fail_before_any_load_or_mutation(
    tmp_path: Path,
    capsys,
    monkeypatch,
) -> None:
    capture_path = tmp_path / "missing-capture.json"
    selection_path = tmp_path / "missing-selection.json"
    destination = tmp_path / "same.json"

    def fail_load(*args, **kwargs):
        raise AssertionError("51D path preflight must happen before source loading")

    monkeypatch.setattr(
        research_start_cli,
        "load_chromium_page_research_capture",
        fail_load,
    )

    with pytest.raises(SystemExit) as exc_info:
        cli.main(
            _command(
                capture_path,
                selection_path,
                destination,
                destination,
            )
        )

    assert exc_info.value.code == 2
    assert not destination.exists()
    assert "distinct paths" in capsys.readouterr().err


@pytest.mark.parametrize("missing", ["working-set", "note"])
def test_51d_missing_output_parent_fails_before_any_durable_mutation(
    tmp_path: Path,
    capsys,
    missing: str,
) -> None:
    capture_path = _capture_with_text(tmp_path, name="capture.json", text=_TEXT)
    selection_path = _saved_selection(tmp_path, capture_path)
    existing_parent = tmp_path / "existing"
    existing_parent.mkdir()
    missing_parent = tmp_path / "missing"

    if missing == "working-set":
        working_set_path = missing_parent / "working-set.json"
        note_path = existing_parent / "note.json"
    else:
        working_set_path = existing_parent / "working-set.json"
        note_path = missing_parent / "note.json"

    with pytest.raises(SystemExit) as exc_info:
        cli.main(
            _command(
                capture_path,
                selection_path,
                working_set_path,
                note_path,
            )
        )

    assert exc_info.value.code == 2
    assert not working_set_path.exists()
    assert not note_path.exists()
    assert "parent directory does not exist" in capsys.readouterr().err


@pytest.mark.parametrize("existing", ["working-set", "note"])
def test_51d_existing_output_is_preserved_and_other_output_is_not_created(
    tmp_path: Path,
    capsys,
    existing: str,
) -> None:
    capture_path = _capture_with_text(tmp_path, name="capture.json", text=_TEXT)
    selection_path = _saved_selection(tmp_path, capture_path)
    working_set_path = tmp_path / "working-set.json"
    note_path = tmp_path / "note.json"
    sentinel = b"preserve exactly\n"
    target = working_set_path if existing == "working-set" else note_path
    target.write_bytes(sentinel)

    with pytest.raises(SystemExit) as exc_info:
        cli.main(
            _command(
                capture_path,
                selection_path,
                working_set_path,
                note_path,
            )
        )

    assert exc_info.value.code == 2
    assert target.read_bytes() == sentinel
    other = note_path if existing == "working-set" else working_set_path
    assert not other.exists()
    assert "destination already exists" in capsys.readouterr().err


def test_51d_unpredictable_note_stage_failure_keeps_valid_working_set_without_receipt(
    tmp_path: Path,
    capsys,
    monkeypatch,
) -> None:
    capture_path = _capture_with_text(tmp_path, name="capture.json", text=_TEXT)
    selection_path = _saved_selection(tmp_path, capture_path)
    working_set_path = tmp_path / "working-set.json"
    note_path = tmp_path / "note.json"

    def fail_note_persistence(*args, **kwargs):
        raise OSError("simulated note-stage I/O failure")

    monkeypatch.setattr(
        research_start_cli,
        "persist_chromium_research_working_set_note_v2",
        fail_note_persistence,
    )

    with pytest.raises(SystemExit) as exc_info:
        cli.main(
            _command(
                capture_path,
                selection_path,
                working_set_path,
                note_path,
            )
        )

    captured = capsys.readouterr()
    assert exc_info.value.code == 2
    verified = verify_chromium_research_working_set(working_set_path)
    assert verified.working_set_format == "pyxis.chromium.research_working_set.v2"
    assert not note_path.exists()
    assert captured.out == ""
    assert "simulated note-stage I/O failure" in captured.err


def test_51d_fresh_21c_failure_emits_no_success_receipt_and_preserves_written_root_files(
    tmp_path: Path,
    capsys,
    monkeypatch,
) -> None:
    capture_path = _capture_with_text(tmp_path, name="capture.json", text=_TEXT)
    selection_path = _saved_selection(tmp_path, capture_path)
    working_set_path = tmp_path / "working-set.json"
    note_path = tmp_path / "note.json"

    def fail_fresh_relink(*args, **kwargs):
        raise ValueError("simulated fresh 21C relink failure")

    monkeypatch.setattr(
        research_start_cli,
        "load_chromium_research_working_set_note",
        fail_fresh_relink,
    )

    with pytest.raises(SystemExit) as exc_info:
        cli.main(
            _command(
                capture_path,
                selection_path,
                working_set_path,
                note_path,
            )
        )

    captured = capsys.readouterr()
    assert exc_info.value.code == 2
    assert working_set_path.is_file()
    assert note_path.is_file()
    assert captured.out == ""
    assert "simulated fresh 21C relink failure" in captured.err


def test_51d_help_exposes_only_one_saved_member_and_initial_root_inputs(capsys) -> None:
    with pytest.raises(SystemExit) as exc_info:
        cli.main(["research-start", "--help"])

    output = capsys.readouterr().out
    assert exc_info.value.code == 0
    for option in (
        "--capture",
        "--selection",
        "--rationale",
        "--working-set-destination",
        "--note-destination",
    ):
        assert option in output
    for forbidden in (
        "--latest",
        "--current",
        "--head",
        "--plan",
        "--member",
        "--tag",
        "--project",
        "--revision",
        "--declaration",
        "--endpoint",
        "--target-id",
    ):
        assert forbidden not in output
