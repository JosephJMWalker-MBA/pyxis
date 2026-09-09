from __future__ import annotations

import builtins
from dataclasses import replace
from pathlib import Path

import pytest

import pyxis.cli as cli
from pyxis.app import ChromiumPageResearchLoadedParagraphTextSelectionRecord
from pyxis.app.chromium_paragraphs import (
    ChromiumPageParagraphEvidence,
    ChromiumPageParagraphsEvidence,
)
from pyxis.app.chromium_research_capture import (
    persist_chromium_page_research_capture,
)
from test_app_chromium_research_capture import (
    ENDPOINT,
    TARGET_ID,
    URL,
    _bundle,
)
from test_app_chromium_research_session_reentry import _durable_fixture
from test_app_chromium_research_session_reentry_plan_document import (
    _document_for,
    _write_document,
)


def _capture_with_text(
    tmp_path: Path,
    *,
    name: str,
    text: str,
) -> Path:
    base = _bundle()
    paragraph = ChromiumPageParagraphEvidence(
        ordinal=1,
        element_id="candidate",
        text_prefix=text,
        text_character_count=len(text),
        text_limit=128,
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


def _ordinary_plan(tmp_path: Path) -> tuple[Path, object]:
    fixture = _durable_fixture(tmp_path)
    plan_path = tmp_path / "ordinary.plan.json"
    _write_document(plan_path, _document_for(fixture.plan, tmp_path))
    return plan_path, fixture


def _save_selection(
    tmp_path: Path,
    capsys,
    *,
    capture: Path,
    name: str = "candidate.selection.json",
) -> Path:
    destination = tmp_path / name
    assert (
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
        == 0
    )
    capsys.readouterr()
    return destination


def test_50z_saved_selection_pair_relinks_exact_record_and_launches_existing_44h_runner(
    tmp_path: Path,
    capsys,
    monkeypatch,
) -> None:
    plan_path, fixture = _ordinary_plan(tmp_path)
    capture = _capture_with_text(
        tmp_path,
        name="candidate.capture.json",
        text="Alpha candidate passage",
    )
    selection = _save_selection(
        tmp_path,
        capsys,
        capture=capture,
    )

    observed: dict[str, object] = {}
    real_relink = cli.load_chromium_research_paragraph_text_selection

    def recording_relink(source, selection_source):
        observed["relink_source"] = source
        observed["relink_path"] = selection_source
        result = real_relink(source, selection_source)
        observed["relinked"] = result
        return result

    def fail_plain_shell(*args, **kwargs):
        raise AssertionError(
            "paired saved-selection candidate must use the established changed-basis product"
        )

    def fake_changed_basis(reentry, candidate):
        observed["reentry"] = reentry
        observed["candidate"] = candidate

    monkeypatch.setattr(
        cli,
        "load_chromium_research_paragraph_text_selection",
        recording_relink,
    )
    monkeypatch.setattr(cli, "_run_research_session_shell", fail_plain_shell)
    monkeypatch.setattr(
        cli,
        "_run_first_changed_basis_saved_selection_shell",
        fake_changed_basis,
    )

    assert (
        cli.main(
            [
                "research-shell",
                "--plan",
                str(plan_path),
                "--candidate-capture",
                str(capture),
                "--candidate-selection",
                str(selection),
            ]
        )
        == 0
    )

    reentry = observed["reentry"]
    candidate = observed["candidate"]
    assert reentry.plan == fixture.plan
    assert candidate is observed["relinked"]
    assert type(candidate) is ChromiumPageResearchLoadedParagraphTextSelectionRecord
    assert candidate.verification.path == selection.resolve()
    assert candidate.selection.selected_text == "Alpha"
    assert candidate.selection.source.source is observed["relink_source"]
    assert observed["relink_source"].verification.path == capture.resolve()
    assert observed["relink_path"] == selection


def test_50z_private_cli_handoff_seam_passes_exact_reentry_and_candidate_to_44h_runner(
    tmp_path: Path,
    capsys,
    monkeypatch,
) -> None:
    plan_path, _ = _ordinary_plan(tmp_path)
    plan = cli.load_chromium_research_session_reentry_plan_document(plan_path)
    reentry = cli.reenter_chromium_research_session(plan)
    capture_path = _capture_with_text(
        tmp_path,
        name="handoff.capture.json",
        text="Alpha handoff passage",
    )
    selection_path = _save_selection(
        tmp_path,
        capsys,
        capture=capture_path,
        name="handoff.selection.json",
    )
    capture = cli.load_chromium_page_research_capture(capture_path)
    candidate = cli.load_chromium_research_paragraph_text_selection(
        capture,
        selection_path,
    )
    observed: dict[str, object] = {}

    def fake_runner(received_reentry, items):
        observed["reentry"] = received_reentry
        observed["items"] = tuple(items)
        return None

    monkeypatch.setattr(
        cli,
        "_load_first_changed_basis_handoff_runner",
        lambda: fake_runner,
    )

    cli._run_first_changed_basis_saved_selection_shell(reentry, candidate)

    assert observed["reentry"] is reentry
    assert observed["items"] == (candidate,)
    assert observed["items"][0] is candidate


def test_50z_plain_ordinary_plan_launch_remains_unchanged(
    tmp_path: Path,
    monkeypatch,
) -> None:
    plan_path, fixture = _ordinary_plan(tmp_path)
    observed: dict[str, object] = {}

    def fake_plain(reentry):
        observed["reentry"] = reentry

    def fail_changed(*args, **kwargs):
        raise AssertionError("plain --plan must not enter candidate mode")

    monkeypatch.setattr(cli, "_run_research_session_shell", fake_plain)
    monkeypatch.setattr(
        cli,
        "_run_first_changed_basis_saved_selection_shell",
        fail_changed,
    )

    assert cli.main(["research-shell", "--plan", str(plan_path)]) == 0
    assert observed["reentry"].plan == fixture.plan


@pytest.mark.parametrize(
    "args",
    [
        ["--candidate-capture", "capture.json"],
        ["--candidate-selection", "selection.json"],
    ],
)
def test_50z_candidate_flags_must_be_supplied_as_exact_pair_before_any_ui_launch(
    tmp_path: Path,
    capsys,
    monkeypatch,
    args: list[str],
) -> None:
    observed = {"ui": 0}

    def fail_ui(*_args, **_kwargs):
        observed["ui"] += 1
        raise AssertionError("incomplete candidate pair must fail before UI")

    monkeypatch.setattr(cli, "_run_research_session_shell", fail_ui)
    monkeypatch.setattr(
        cli,
        "_run_first_changed_basis_saved_selection_shell",
        fail_ui,
    )

    with pytest.raises(SystemExit) as exc_info:
        cli.main(
            [
                "research-shell",
                "--plan",
                str(tmp_path / "not-even-read.plan.json"),
                *args,
            ]
        )

    assert exc_info.value.code == 2
    assert observed["ui"] == 0
    assert "must be supplied together" in capsys.readouterr().err


@pytest.mark.parametrize(
    "entry_flag",
    [
        "--root-backed-overlay",
        "--root-backed-continuation-overlay",
        "--second-basis-epoch-overlay",
        "--second-basis-epoch-continuation-overlay",
        "--third-basis-epoch-overlay",
        "--third-basis-epoch-continuation-overlay",
    ],
)
def test_50z_saved_selection_candidate_is_closed_to_nonordinary_entry_families(
    tmp_path: Path,
    capsys,
    monkeypatch,
    entry_flag: str,
) -> None:
    observed = {"ui": 0}

    def fail_ui(*_args, **_kwargs):
        observed["ui"] += 1
        raise AssertionError("nonordinary candidate launch must fail before UI")

    monkeypatch.setattr(cli, "_run_root_backed_research_session_shell", fail_ui)
    monkeypatch.setattr(
        cli,
        "_run_root_backed_continuation_research_session_shell",
        fail_ui,
    )
    monkeypatch.setattr(cli, "_run_second_basis_epoch_research_session_shell", fail_ui)
    monkeypatch.setattr(
        cli,
        "_run_second_basis_epoch_continuation_research_session_shell",
        fail_ui,
    )
    monkeypatch.setattr(cli, "_run_third_basis_epoch_research_session_shell", fail_ui)
    monkeypatch.setattr(
        cli,
        "_run_third_basis_epoch_continuation_research_session_shell",
        fail_ui,
    )

    with pytest.raises(SystemExit) as exc_info:
        cli.main(
            [
                "research-shell",
                entry_flag,
                str(tmp_path / "not-read.overlay.json"),
                "--candidate-capture",
                str(tmp_path / "not-read.capture.json"),
                "--candidate-selection",
                str(tmp_path / "not-read.selection.json"),
            ]
        )

    assert exc_info.value.code == 2
    assert observed["ui"] == 0
    assert "supported only with ordinary --plan entry" in capsys.readouterr().err


def test_50z_mismatched_explicit_capture_fails_in_49b_before_changed_basis_ui(
    tmp_path: Path,
    capsys,
    monkeypatch,
) -> None:
    plan_path, _ = _ordinary_plan(tmp_path)
    original_capture = _capture_with_text(
        tmp_path,
        name="original.capture.json",
        text="Alpha original passage",
    )
    selection = _save_selection(
        tmp_path,
        capsys,
        capture=original_capture,
        name="mismatch.selection.json",
    )
    different_capture = _capture_with_text(
        tmp_path,
        name="different.capture.json",
        text="Bravo different passage",
    )

    def fail_changed(*args, **kwargs):
        raise AssertionError("49B mismatch must fail before changed-basis UI")

    monkeypatch.setattr(
        cli,
        "_run_first_changed_basis_saved_selection_shell",
        fail_changed,
    )

    with pytest.raises(SystemExit) as exc_info:
        cli.main(
            [
                "research-shell",
                "--plan",
                str(plan_path),
                "--candidate-capture",
                str(different_capture),
                "--candidate-selection",
                str(selection),
            ]
        )

    assert exc_info.value.code == 2
    assert "different capture bundle" in capsys.readouterr().err


def test_50z_saved_selection_candidate_loading_never_acquires_live_chromium(
    tmp_path: Path,
    capsys,
    monkeypatch,
) -> None:
    plan_path, _ = _ordinary_plan(tmp_path)
    capture = _capture_with_text(
        tmp_path,
        name="offline.capture.json",
        text="Alpha offline candidate",
    )
    selection = _save_selection(
        tmp_path,
        capsys,
        capture=capture,
        name="offline.selection.json",
    )

    import pyxis.app.chromium_paragraphs as paragraphs_module

    def fail_browser(*args, **kwargs):
        raise AssertionError("50Z candidate relinking must not acquire Chromium state")

    monkeypatch.setattr(
        paragraphs_module,
        "observe_chromium_page_paragraphs",
        fail_browser,
    )
    monkeypatch.setattr(
        cli,
        "_run_first_changed_basis_saved_selection_shell",
        lambda reentry, candidate: None,
    )

    assert (
        cli.main(
            [
                "research-shell",
                "--plan",
                str(plan_path),
                "--candidate-capture",
                str(capture),
                "--candidate-selection",
                str(selection),
            ]
        )
        == 0
    )


def test_50z_changed_basis_ui_dependency_remains_lazy(monkeypatch) -> None:
    original_import = builtins.__import__

    def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name == (
            "pyxis.ui.first_changed_basis_root_backed_handoff_research_session_shell"
        ):
            raise ModuleNotFoundError("No module named 'textual'", name="textual")
        return original_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    with pytest.raises(RuntimeError, match=r"pyxis\[ui\]"):
        cli._load_first_changed_basis_handoff_runner()


def test_50z_research_shell_help_exposes_explicit_candidate_pair_only(capsys) -> None:
    with pytest.raises(SystemExit) as exc_info:
        cli.main(["research-shell", "--help"])

    output = capsys.readouterr().out
    assert exc_info.value.code == 0
    assert "--candidate-capture" in output
    assert "--candidate-selection" in output
    for forbidden in (
        "--candidate-directory",
        "--candidate-url",
        "--candidate-latest",
        "--candidate-head",
        "--candidate-auto",
    ):
        assert forbidden not in output
