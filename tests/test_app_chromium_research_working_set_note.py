from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
from pathlib import Path

import pytest

from test_app_chromium_research_working_set import _loaded_records
from pyxis.app.chromium_research_working_set import (
    ChromiumPageResearchWorkingSetRecord,
    create_chromium_research_working_set,
)
from pyxis.app.chromium_research_working_set_load import load_chromium_research_working_set
from pyxis.app.chromium_research_working_set_note import (
    ChromiumPageResearchWorkingSetNoteRecord,
    create_chromium_research_working_set_note,
)
from pyxis.app.chromium_research_working_set_persistence import (
    persist_chromium_research_working_set,
)


def test_working_set_note_retains_exact_working_set_and_verbatim_human_text(
    tmp_path: Path,
) -> None:
    paragraph_note, exact_note, comparison_note = _loaded_records(tmp_path)
    working_set = create_chromium_research_working_set(
        (exact_note, paragraph_note, comparison_note)
    )
    note_text = "  Why these travel together 😀\nKeep the tension unresolved.  "

    note = create_chromium_research_working_set_note(
        working_set,
        note_text=note_text,
    )

    assert isinstance(note, ChromiumPageResearchWorkingSetNoteRecord)
    assert note.note_mode == "caller_authored_note_on_research_working_set"
    assert note.working_set is working_set
    assert note.note_text == note_text

    with pytest.raises(FrozenInstanceError):
        note.note_text = "changed"  # type: ignore[misc]


def test_working_set_note_accepts_exact_20c_reconstructed_working_set(
    tmp_path: Path,
) -> None:
    paragraph_note, exact_note, comparison_note = _loaded_records(tmp_path)
    original = create_chromium_research_working_set(
        (paragraph_note, exact_note, comparison_note)
    )
    path = tmp_path / "working-set.json"
    persist_chromium_research_working_set(original, path)
    loaded = load_chromium_research_working_set(
        (paragraph_note, exact_note, comparison_note),
        path,
    )

    note = create_chromium_research_working_set_note(
        loaded.working_set,
        note_text="This is my current line of inquiry.",
    )

    assert note.working_set is loaded.working_set
    assert note.working_set is not original
    assert note.working_set.items[0] is paragraph_note
    assert note.working_set.items[1] is exact_note
    assert note.working_set.items[2] is comparison_note


def test_working_set_note_does_not_reread_working_set_or_member_sidecars(
    tmp_path: Path,
) -> None:
    paragraph_note, exact_note, comparison_note = _loaded_records(tmp_path)
    original = create_chromium_research_working_set(
        (paragraph_note, exact_note, comparison_note)
    )
    path = tmp_path / "working-set.json"
    persist_chromium_research_working_set(original, path)
    loaded = load_chromium_research_working_set(
        (paragraph_note, exact_note, comparison_note),
        path,
    )

    path.unlink()
    paragraph_note.verification.path.unlink()
    exact_note.verification.path.unlink()
    comparison_note.verification.path.unlink()

    note = create_chromium_research_working_set_note(
        loaded.working_set,
        note_text="Files moved; this rationale remains an in-memory human action.",
    )

    assert note.working_set is loaded.working_set
    assert not path.exists()
    assert not paragraph_note.verification.path.exists()
    assert not exact_note.verification.path.exists()
    assert not comparison_note.verification.path.exists()


def test_working_set_note_rejects_non_working_set_and_invalid_note_text(
    tmp_path: Path,
) -> None:
    paragraph_note, _, _ = _loaded_records(tmp_path)
    working_set = create_chromium_research_working_set((paragraph_note,))

    with pytest.raises(TypeError, match="working_set must be"):
        create_chromium_research_working_set_note(  # type: ignore[arg-type]
            paragraph_note,
            note_text="Wrong parent type",
        )

    with pytest.raises(TypeError, match="note_text must be a string"):
        create_chromium_research_working_set_note(  # type: ignore[arg-type]
            working_set,
            note_text=123,
        )

    with pytest.raises(ValueError, match="non-whitespace caller-authored text"):
        create_chromium_research_working_set_note(
            working_set,
            note_text=" \n\t ",
        )


def test_working_set_note_rejects_unsupported_working_set_mode(tmp_path: Path) -> None:
    paragraph_note, _, _ = _loaded_records(tmp_path)
    working_set = create_chromium_research_working_set((paragraph_note,))
    forged = replace(
        working_set,
        working_set_mode="machine_ranked_research_collection",
    )

    with pytest.raises(ValueError, match="working-set mode is unsupported"):
        create_chromium_research_working_set_note(
            forged,
            note_text="Do not accept a different grouping authority.",
        )


def test_working_set_note_reestablishes_20a_member_coherence(tmp_path: Path) -> None:
    paragraph_note, _, _ = _loaded_records(tmp_path)
    working_set = create_chromium_research_working_set((paragraph_note,))
    forged_member = replace(
        paragraph_note,
        verification=replace(
            paragraph_note.verification,
            note_text="Different retained verification text",
        ),
    )
    forged_working_set = replace(working_set, items=(forged_member,))

    with pytest.raises(
        ValueError,
        match=r"items\[0\] paragraph-note verification is incoherent",
    ):
        create_chromium_research_working_set_note(
            forged_working_set,
            note_text="The outer type alone is insufficient.",
        )


def test_working_set_note_module_is_publicly_importable(tmp_path: Path) -> None:
    paragraph_note, _, _ = _loaded_records(tmp_path)
    working_set = ChromiumPageResearchWorkingSetRecord(
        working_set_mode="caller_explicit_ordered_relinked_research_working_set",
        items=(paragraph_note,),
    )

    note = create_chromium_research_working_set_note(
        working_set,
        note_text="Human rationale only.",
    )

    assert note.working_set is working_set
    assert note.note_text == "Human rationale only."
