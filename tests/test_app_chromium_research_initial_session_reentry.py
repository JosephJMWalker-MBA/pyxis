from __future__ import annotations

from dataclasses import FrozenInstanceError
from pathlib import Path

import pytest

import pyxis.app.chromium_research_initial_session_reentry as reentry_module
from pyxis.app.chromium_research_capture_load import (
    load_chromium_page_research_capture,
)
from pyxis.app.chromium_research_initial_session_reentry import (
    ChromiumResearchInitialSessionReentryResult,
    reenter_chromium_research_initial_session,
)
from pyxis.app.chromium_research_paragraph_text_selection import (
    select_chromium_research_paragraph_text,
)
from pyxis.app.chromium_research_paragraph_text_selection_load import (
    load_chromium_research_paragraph_text_selection,
)
from pyxis.app.chromium_research_paragraph_text_selection_persistence import (
    persist_chromium_research_paragraph_text_selection,
)
from pyxis.app.chromium_research_passage_selection import (
    select_chromium_research_capture_paragraph,
)
from pyxis.app.chromium_research_working_set import (
    create_chromium_research_working_set,
)
from pyxis.app.chromium_research_working_set_note import (
    create_chromium_research_working_set_note,
)
from pyxis.app.chromium_research_working_set_note_persistence import (
    persist_chromium_research_working_set_note_v2,
)
from pyxis.app.chromium_research_working_set_persistence import (
    persist_chromium_research_working_set_v2,
)
from test_cli_research_start import _capture_with_text, _saved_selection


_TEXT = "Alpha 😀 beta"
_RATIONALE = "  First governed rationale 😀\nStill explicitly human-owned.  "


def _durable_root(
    tmp_path: Path,
    *,
    stem: str,
    text: str = _TEXT,
    rationale: str = _RATIONALE,
) -> tuple[Path, Path, Path, Path]:
    root = tmp_path / stem
    root.mkdir()
    capture_path = _capture_with_text(root, name="capture.json", text=text)
    selection_path = _saved_selection(
        root,
        capture_path,
        name="selection.json",
    )
    loaded_capture = load_chromium_page_research_capture(capture_path)
    loaded_selection = load_chromium_research_paragraph_text_selection(
        loaded_capture,
        selection_path,
    )
    working_set = create_chromium_research_working_set((loaded_selection,))
    note = create_chromium_research_working_set_note(
        working_set,
        note_text=rationale,
    )
    working_set_path = root / "working-set.json"
    note_path = root / "working-set-note.json"
    persist_chromium_research_working_set_v2(working_set, working_set_path)
    persist_chromium_research_working_set_note_v2(
        note,
        working_set_path,
        note_path,
    )
    return capture_path, selection_path, working_set_path, note_path


def _alternate_selection(capture_path: Path, destination: Path) -> Path:
    loaded_capture = load_chromium_page_research_capture(capture_path)
    paragraph = select_chromium_research_capture_paragraph(
        loaded_capture,
        paragraph_ordinal=1,
    )
    selection = select_chromium_research_paragraph_text(
        paragraph,
        start_offset=0,
        end_offset=5,
    )
    persist_chromium_research_paragraph_text_selection(selection, destination)
    return destination


def _snapshot(paths: tuple[Path, ...]) -> dict[Path, bytes]:
    return {path: path.read_bytes() for path in paths}


def _assert_snapshot(snapshot: dict[Path, bytes]) -> None:
    for path, expected in snapshot.items():
        assert path.read_bytes() == expected


def test_51e_fresh_four_path_reentry_mounts_exact_new_chain(tmp_path: Path) -> None:
    paths = _durable_root(tmp_path, stem="root")

    result = reenter_chromium_research_initial_session(
        capture_source=paths[0],
        selection_source=paths[1],
        working_set_source=paths[2],
        note_source=paths[3],
    )

    assert isinstance(result, ChromiumResearchInitialSessionReentryResult)
    assert result.loaded_selection.selection.source.source is result.loaded_capture
    assert result.loaded_root.note.working_set.items == (result.loaded_selection,)
    assert result.loaded_root.note.working_set.items[0] is result.loaded_selection
    assert result.controller.loaded is result.loaded_root
    assert result.controller.presentation.rationale_text == _RATIONALE
    assert result.controller.presentation.members[0].member_kind == "exact_range_selection"
    assert result.controller.presentation.members[0].human_note_text is None
    assert result.controller.presentation.members[0].excerpts[0].text == "😀"

    with pytest.raises(FrozenInstanceError):
        result.loaded_root = result.loaded_root  # type: ignore[misc]


def test_51e_reentry_calls_only_existing_boundaries_in_exact_order(
    tmp_path: Path,
    monkeypatch,
) -> None:
    capture_path = tmp_path / "capture.json"
    selection_path = tmp_path / "selection.json"
    working_set_path = tmp_path / "working-set.json"
    note_path = tmp_path / "note.json"
    loaded_capture = object()
    loaded_selection = object()
    loaded_root = object()
    controller = object()
    calls: list[tuple[object, ...]] = []

    def load_capture(source):
        calls.append(("16C", source))
        return loaded_capture

    def load_selection(source, selection_source):
        calls.append(("49B", source, selection_source))
        return loaded_selection

    def load_root(items, working_set_source, note_source):
        calls.append(("21C", tuple(items), working_set_source, note_source))
        return loaded_root

    def make_controller(root):
        calls.append(("51C", root))
        return controller

    monkeypatch.setattr(reentry_module, "load_chromium_page_research_capture", load_capture)
    monkeypatch.setattr(
        reentry_module,
        "load_chromium_research_paragraph_text_selection",
        load_selection,
    )
    monkeypatch.setattr(
        reentry_module,
        "load_chromium_research_working_set_note",
        load_root,
    )
    monkeypatch.setattr(
        reentry_module,
        "ChromiumResearchInitialSessionController",
        make_controller,
    )

    result = reenter_chromium_research_initial_session(
        capture_source=capture_path,
        selection_source=selection_path,
        working_set_source=working_set_path,
        note_source=note_path,
    )

    assert calls == [
        ("16C", capture_path),
        ("49B", loaded_capture, selection_path),
        ("21C", (loaded_selection,), working_set_path, note_path),
        ("51C", loaded_root),
    ]
    assert result.loaded_capture is loaded_capture
    assert result.loaded_selection is loaded_selection
    assert result.loaded_root is loaded_root
    assert result.controller is controller


@pytest.mark.parametrize(
    "field",
    ("capture_source", "selection_source", "working_set_source", "note_source"),
)
def test_51e_reentry_rejects_non_path_inputs_before_loading(
    tmp_path: Path,
    monkeypatch,
    field: str,
) -> None:
    values: dict[str, object] = {
        "capture_source": tmp_path / "capture.json",
        "selection_source": tmp_path / "selection.json",
        "working_set_source": tmp_path / "working-set.json",
        "note_source": tmp_path / "note.json",
    }
    values[field] = "not-a-path"

    monkeypatch.setattr(
        reentry_module,
        "load_chromium_page_research_capture",
        lambda source: pytest.fail("16C must not run after invalid path input"),
    )

    with pytest.raises(TypeError, match=f"{field} must be pathlib.Path"):
        reenter_chromium_research_initial_session(**values)  # type: ignore[arg-type]


def test_51e_wrong_valid_capture_fails_closed_without_mutation(tmp_path: Path) -> None:
    root_paths = _durable_root(tmp_path, stem="root-a")
    wrong_paths = _durable_root(
        tmp_path,
        stem="root-b",
        text="Alpha 😀 different source",
        rationale="Different root rationale.",
    )
    snapshot = _snapshot(root_paths)

    with pytest.raises(ValueError):
        reenter_chromium_research_initial_session(
            capture_source=wrong_paths[0],
            selection_source=root_paths[1],
            working_set_source=root_paths[2],
            note_source=root_paths[3],
        )

    _assert_snapshot(snapshot)


def test_51e_wrong_valid_selection_fails_working_set_membership_without_mutation(
    tmp_path: Path,
) -> None:
    paths = _durable_root(tmp_path, stem="root")
    alternate_path = _alternate_selection(paths[0], tmp_path / "alternate-selection.json")
    snapshot = _snapshot(paths + (alternate_path,))

    with pytest.raises(ValueError):
        reenter_chromium_research_initial_session(
            capture_source=paths[0],
            selection_source=alternate_path,
            working_set_source=paths[2],
            note_source=paths[3],
        )

    _assert_snapshot(snapshot)


def test_51e_wrong_valid_working_set_fails_without_mutation(tmp_path: Path) -> None:
    paths = _durable_root(tmp_path, stem="root-a")
    wrong_paths = _durable_root(
        tmp_path,
        stem="root-b",
        text="Alpha 😀 other evidence",
        rationale="Other human rationale.",
    )
    observed = (paths[0], paths[1], wrong_paths[2], paths[3])
    snapshot = _snapshot(observed)

    with pytest.raises(ValueError):
        reenter_chromium_research_initial_session(
            capture_source=observed[0],
            selection_source=observed[1],
            working_set_source=observed[2],
            note_source=observed[3],
        )

    _assert_snapshot(snapshot)


def test_51e_wrong_valid_note_fails_parent_reconciliation_without_mutation(
    tmp_path: Path,
) -> None:
    paths = _durable_root(tmp_path, stem="root-a")
    wrong_paths = _durable_root(
        tmp_path,
        stem="root-b",
        text="Alpha 😀 other evidence",
        rationale="Other human rationale.",
    )
    observed = (paths[0], paths[1], paths[2], wrong_paths[3])
    snapshot = _snapshot(observed)

    with pytest.raises(ValueError):
        reenter_chromium_research_initial_session(
            capture_source=observed[0],
            selection_source=observed[1],
            working_set_source=observed[2],
            note_source=observed[3],
        )

    _assert_snapshot(snapshot)


@pytest.mark.parametrize("tampered_index", (0, 1, 2, 3))
def test_51e_tampered_durable_layer_is_rejected_without_reentry_mutation(
    tmp_path: Path,
    tampered_index: int,
) -> None:
    paths = _durable_root(tmp_path, stem=f"root-{tampered_index}")
    paths[tampered_index].write_bytes(b"{}\n")
    snapshot = _snapshot(paths)

    with pytest.raises((OSError, TypeError, ValueError)):
        reenter_chromium_research_initial_session(
            capture_source=paths[0],
            selection_source=paths[1],
            working_set_source=paths[2],
            note_source=paths[3],
        )

    _assert_snapshot(snapshot)


def test_51e_successful_mount_survives_deletion_of_all_four_durable_inputs(
    tmp_path: Path,
) -> None:
    paths = _durable_root(tmp_path, stem="root")
    result = reenter_chromium_research_initial_session(
        capture_source=paths[0],
        selection_source=paths[1],
        working_set_source=paths[2],
        note_source=paths[3],
    )
    presentation = result.controller.presentation

    for path in paths:
        path.unlink()

    assert presentation is result.controller.presentation
    assert result.controller.loaded is result.loaded_root
    assert presentation.rationale_text == _RATIONALE
    assert presentation.members[0].excerpts[0].text == "😀"
    assert result.loaded_selection.selection.selected_text == "😀"
