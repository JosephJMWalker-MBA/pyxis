from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

import pyxis.cli as cli
from pyxis.app.chromium_paragraphs import (
    ChromiumPageParagraphEvidence,
    ChromiumPageParagraphsEvidence,
)
from pyxis.app.chromium_research_capture import (
    persist_chromium_page_research_capture,
)
from pyxis.app.chromium_research_paragraph_text_selection_persistence import (
    verify_chromium_research_paragraph_text_selection,
)
from test_app_chromium_research_capture import (
    ENDPOINT,
    TARGET_ID,
    URL,
    _bundle,
)


_TEXT = "Alpha 😀 beta"


def _capture_with_paragraph(tmp_path: Path, *, name: str = "capture.json") -> Path:
    base = _bundle()
    paragraph = ChromiumPageParagraphEvidence(
        ordinal=1,
        element_id="passage",
        text_prefix=_TEXT,
        text_character_count=len(_TEXT),
        text_limit=64,
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
    bundle = replace(base, paragraphs=paragraphs)
    path = tmp_path / name
    persist_chromium_page_research_capture(bundle, path)
    return path


def test_50y_research_save_selection_cli_writes_exact_49a_sidecar_and_deterministic_receipt(
    tmp_path: Path,
    capsys,
) -> None:
    capture = _capture_with_paragraph(tmp_path)
    destination = tmp_path / "saved-selection.json"

    assert (
        cli.main(
            [
                "research-save-selection",
                "--capture",
                str(capture),
                "--paragraph",
                "1",
                "--start",
                "6",
                "--end",
                "7",
                "--destination",
                str(destination),
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    receipt = json.loads(output)
    verified = verify_chromium_research_paragraph_text_selection(destination)

    expected = {
        "byte_count": verified.byte_count,
        "capture_input_context_only": str(capture.resolve()),
        "end_offset": 7,
        "offset_unit": "unicode_code_point",
        "paragraph_ordinal": 1,
        "receipt_role": "operation_receipt_not_source_evidence",
        "selection_format": "pyxis.chromium.research_paragraph_text_selection.v1",
        "selection_output_path": str(destination.resolve()),
        "selection_record_sha256": verified.selection_record_sha256,
        "source_bundle_sha256": verified.source_bundle_sha256,
        "source_capture_format": "pyxis.chromium.research_capture.v1",
        "start_offset": 6,
    }
    assert receipt == expected
    assert output == json.dumps(
        expected,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    ) + "\n"

    sidecar_text = destination.read_text(encoding="utf-8")
    assert _TEXT not in sidecar_text
    assert "😀" not in sidecar_text
    assert str(capture.resolve()) not in sidecar_text
    assert "😀" not in output
    assert _TEXT not in output
    assert URL not in output
    assert ENDPOINT not in output
    assert TARGET_ID not in output

    document = json.loads(sidecar_text)
    assert document["format"] == "pyxis.chromium.research_paragraph_text_selection.v1"
    assert document["selection_record"]["selection"]["paragraph"] == {
        "mode": "caller_explicit_returned_paragraph_ordinal",
        "ordinal": 1,
    }
    assert document["selection_record"]["selection"]["text_range"] == {
        "end_offset": 7,
        "mode": "caller_explicit_returned_paragraph_text_range",
        "offset_unit": "unicode_code_point",
        "start_offset": 6,
    }


def test_50y_cli_delegates_exactly_through_public_16c_17a_18a_49a_boundaries(
    tmp_path: Path,
    capsys,
    monkeypatch,
) -> None:
    capture_path = tmp_path / "capture.json"
    destination = tmp_path / "selection.json"
    capture = SimpleNamespace(
        verification=SimpleNamespace(path=capture_path.resolve())
    )
    paragraph = object()
    selection = object()
    persisted = SimpleNamespace(
        path=destination.resolve(),
        selection_format="pyxis.chromium.research_paragraph_text_selection.v1",
        selection_record_sha256="a" * 64,
        byte_count=321,
    )
    verified = SimpleNamespace(
        path=destination.resolve(),
        selection_format=persisted.selection_format,
        selection_record_sha256=persisted.selection_record_sha256,
        byte_count=persisted.byte_count,
        source_capture_format="pyxis.chromium.research_capture.v1",
        source_bundle_sha256="b" * 64,
        paragraph_ordinal=2,
        offset_unit="unicode_code_point",
        start_offset=3,
        end_offset=8,
    )
    calls: list[tuple[object, ...]] = []

    def load_capture(path):
        calls.append(("16C", path))
        return capture

    def select_paragraph(source, *, paragraph_ordinal):
        calls.append(("17A", source, paragraph_ordinal))
        return paragraph

    def select_text(source, *, start_offset, end_offset):
        calls.append(("18A", source, start_offset, end_offset))
        return selection

    def persist_text(received, path):
        calls.append(("49A-persist", received, path))
        return persisted

    def verify_text(path):
        calls.append(("49A-verify", path))
        return verified

    monkeypatch.setattr(cli, "load_chromium_page_research_capture", load_capture)
    monkeypatch.setattr(cli, "select_chromium_research_capture_paragraph", select_paragraph)
    monkeypatch.setattr(cli, "select_chromium_research_paragraph_text", select_text)
    monkeypatch.setattr(
        cli,
        "persist_chromium_research_paragraph_text_selection",
        persist_text,
    )
    monkeypatch.setattr(
        cli,
        "verify_chromium_research_paragraph_text_selection",
        verify_text,
    )

    assert (
        cli.main(
            [
                "research-save-selection",
                "--capture",
                str(capture_path),
                "--paragraph",
                "2",
                "--start",
                "3",
                "--end",
                "8",
                "--destination",
                str(destination),
            ]
        )
        == 0
    )

    assert calls == [
        ("16C", capture_path),
        ("17A", capture, 2),
        ("18A", paragraph, 3, 8),
        ("49A-persist", selection, destination),
        ("49A-verify", destination.resolve()),
    ]
    receipt = json.loads(capsys.readouterr().out)
    assert receipt["selection_record_sha256"] == "a" * 64
    assert receipt["source_bundle_sha256"] == "b" * 64


def test_50y_cli_overwrite_fails_without_mutating_existing_destination(
    tmp_path: Path,
    capsys,
) -> None:
    capture = _capture_with_paragraph(tmp_path)
    destination = tmp_path / "existing-selection.json"
    destination.write_bytes(b"preserve exactly\n")

    with pytest.raises(SystemExit) as exc_info:
        cli.main(
            [
                "research-save-selection",
                "--capture",
                str(capture),
                "--paragraph",
                "1",
                "--start",
                "0",
                "--end",
                "5",
                "--destination",
                str(destination),
            ]
        )

    assert exc_info.value.code == 2
    assert destination.read_bytes() == b"preserve exactly\n"
    assert "research-save-selection failed" in capsys.readouterr().err


def test_50y_cli_missing_capture_fails_before_destination_write(
    tmp_path: Path,
    capsys,
) -> None:
    destination = tmp_path / "must-not-exist.json"

    with pytest.raises(SystemExit) as exc_info:
        cli.main(
            [
                "research-save-selection",
                "--capture",
                str(tmp_path / "missing-capture.json"),
                "--paragraph",
                "1",
                "--start",
                "0",
                "--end",
                "1",
                "--destination",
                str(destination),
            ]
        )

    assert exc_info.value.code == 2
    assert not destination.exists()
    assert "research-save-selection failed" in capsys.readouterr().err


@pytest.mark.parametrize(
    ("paragraph", "start", "end", "match"),
    [
        ("2", "0", "1", "paragraph_ordinal"),
        ("1", "0", "99", "outside returned paragraph text evidence"),
    ],
)
def test_50y_cli_invalid_explicit_coordinates_fail_closed(
    tmp_path: Path,
    capsys,
    paragraph: str,
    start: str,
    end: str,
    match: str,
) -> None:
    capture = _capture_with_paragraph(tmp_path)
    destination = tmp_path / f"invalid-{paragraph}-{start}-{end}.json"

    with pytest.raises(SystemExit) as exc_info:
        cli.main(
            [
                "research-save-selection",
                "--capture",
                str(capture),
                "--paragraph",
                paragraph,
                "--start",
                start,
                "--end",
                end,
                "--destination",
                str(destination),
            ]
        )

    assert exc_info.value.code == 2
    assert not destination.exists()
    assert match in capsys.readouterr().err


@pytest.mark.parametrize(
    ("flag", "value"),
    [
        ("--paragraph", "True"),
        ("--start", "False"),
        ("--end", "True"),
    ],
)
def test_50y_cli_coordinate_arguments_require_integer_syntax(
    tmp_path: Path,
    capsys,
    flag: str,
    value: str,
) -> None:
    capture = _capture_with_paragraph(tmp_path)
    destination = tmp_path / "invalid-type.json"
    args = [
        "research-save-selection",
        "--capture",
        str(capture),
        "--paragraph",
        "1",
        "--start",
        "0",
        "--end",
        "1",
        "--destination",
        str(destination),
    ]
    args[args.index(flag) + 1] = value

    with pytest.raises(SystemExit) as exc_info:
        cli.main(args)

    assert exc_info.value.code == 2
    assert not destination.exists()
    assert "invalid int value" in capsys.readouterr().err


def test_50y_cli_save_selection_does_not_acquire_chromium(
    tmp_path: Path,
    monkeypatch,
) -> None:
    capture = _capture_with_paragraph(tmp_path)
    destination = tmp_path / "offline-selection.json"

    import pyxis.app.chromium_paragraphs as paragraphs_module

    def fail_browser(*args, **kwargs):
        raise AssertionError("50Y must not acquire live Chromium state")

    monkeypatch.setattr(paragraphs_module, "observe_chromium_page_paragraphs", fail_browser)

    assert (
        cli.main(
            [
                "research-save-selection",
                "--capture",
                str(capture),
                "--paragraph",
                "1",
                "--start",
                "6",
                "--end",
                "7",
                "--destination",
                str(destination),
            ]
        )
        == 0
    )
    assert destination.is_file()


def test_50y_cli_help_exposes_only_explicit_save_inputs(capsys) -> None:
    with pytest.raises(SystemExit) as exc_info:
        cli.main(["research-save-selection", "--help"])

    output = capsys.readouterr().out
    assert exc_info.value.code == 0
    for option in (
        "--capture",
        "--paragraph",
        "--start",
        "--end",
        "--interactive",
        "--destination",
    ):
        assert option in output
    for forbidden in (
        "--latest",
        "--head",
        "--current",
        "--auto",
        "--url",
        "--endpoint",
        "--target",
        "--note",
    ):
        assert forbidden not in output



def test_51b_cli_interactive_mode_uses_loaded_capture_and_exact_ui_selection(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    capture_path = _capture_with_paragraph(tmp_path)
    destination = tmp_path / "interactive-selection.json"
    loaded = cli.load_chromium_page_research_capture(capture_path)
    paragraph = cli.select_chromium_research_capture_paragraph(
        loaded,
        paragraph_ordinal=1,
    )
    selection = cli.select_chromium_research_paragraph_text(
        paragraph,
        start_offset=6,
        end_offset=7,
    )
    calls: list[tuple[object, ...]] = []

    real_load = cli.load_chromium_page_research_capture

    def load_capture(path):
        calls.append(("16C", path))
        return real_load(path)

    def load_runner():
        calls.append(("load-ui",))

        def run_ui(source):
            calls.append(("ui", source))
            assert source.verification.path == capture_path.resolve()
            return selection

        return run_ui

    monkeypatch.setattr(cli, "load_chromium_page_research_capture", load_capture)
    monkeypatch.setattr(cli, "_load_interactive_research_selection_runner", load_runner)

    assert (
        cli.main(
            [
                "research-save-selection",
                "--capture",
                str(capture_path),
                "--destination",
                str(destination),
                "--interactive",
            ]
        )
        == 0
    )

    assert calls[0] == ("16C", capture_path)
    assert calls[1] == ("load-ui",)
    assert calls[2][0] == "ui"
    verified = verify_chromium_research_paragraph_text_selection(destination)
    assert verified.paragraph_ordinal == 1
    assert verified.start_offset == 6
    assert verified.end_offset == 7
    assert json.loads(capsys.readouterr().out)["selection_record_sha256"] == (
        verified.selection_record_sha256
    )


@pytest.mark.parametrize(
    "extra",
    [
        ["--paragraph", "1"],
        ["--start", "0"],
        ["--end", "1"],
        ["--paragraph", "1", "--start", "0", "--end", "1"],
    ],
)
def test_51b_cli_interactive_rejects_all_explicit_coordinate_inputs_before_loading(
    tmp_path: Path,
    monkeypatch,
    capsys,
    extra: list[str],
) -> None:
    destination = tmp_path / "must-not-exist.json"

    def fail_load(*args, **kwargs):
        raise AssertionError("invalid input mode must fail before 16C")

    monkeypatch.setattr(cli, "load_chromium_page_research_capture", fail_load)

    with pytest.raises(SystemExit) as exc_info:
        cli.main(
            [
                "research-save-selection",
                "--capture",
                str(tmp_path / "capture.json"),
                "--destination",
                str(destination),
                "--interactive",
                *extra,
            ]
        )

    assert exc_info.value.code == 2
    assert not destination.exists()
    assert "mutually exclusive" in capsys.readouterr().err


@pytest.mark.parametrize(
    "coordinates",
    [
        [],
        ["--paragraph", "1"],
        ["--start", "0", "--end", "1"],
        ["--paragraph", "1", "--end", "1"],
    ],
)
def test_51b_cli_partial_coordinate_mode_fails_before_loading(
    tmp_path: Path,
    monkeypatch,
    capsys,
    coordinates: list[str],
) -> None:
    destination = tmp_path / "must-not-exist.json"

    def fail_load(*args, **kwargs):
        raise AssertionError("partial coordinate mode must fail before 16C")

    monkeypatch.setattr(cli, "load_chromium_page_research_capture", fail_load)

    with pytest.raises(SystemExit) as exc_info:
        cli.main(
            [
                "research-save-selection",
                "--capture",
                str(tmp_path / "capture.json"),
                "--destination",
                str(destination),
                *coordinates,
            ]
        )

    assert exc_info.value.code == 2
    assert not destination.exists()
    assert "requires --paragraph, --start, and --end together" in capsys.readouterr().err


def test_51b_cli_explicit_coordinate_mode_never_loads_textual_runner(
    tmp_path: Path,
    monkeypatch,
) -> None:
    capture = _capture_with_paragraph(tmp_path)
    destination = tmp_path / "explicit-still-core.json"

    def fail_ui():
        raise AssertionError("coordinate-explicit mode must not import Textual")

    monkeypatch.setattr(cli, "_load_interactive_research_selection_runner", fail_ui)

    assert (
        cli.main(
            [
                "research-save-selection",
                "--capture",
                str(capture),
                "--paragraph",
                "1",
                "--start",
                "6",
                "--end",
                "7",
                "--destination",
                str(destination),
            ]
        )
        == 0
    )
    assert destination.is_file()


def test_51b_cli_interactive_cancel_is_clean_noop_without_persistence(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    capture = _capture_with_paragraph(tmp_path)
    destination = tmp_path / "cancelled.json"

    monkeypatch.setattr(
        cli,
        "_load_interactive_research_selection_runner",
        lambda: (lambda source: None),
    )

    assert (
        cli.main(
            [
                "research-save-selection",
                "--capture",
                str(capture),
                "--destination",
                str(destination),
                "--interactive",
            ]
        )
        == 0
    )
    assert not destination.exists()
    assert capsys.readouterr().out == ""
