from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
from pathlib import Path

import pytest

from test_app_chromium_research_working_set import _loaded_records
from pyxis.app.chromium_research_working_set import create_chromium_research_working_set
from pyxis.app.chromium_research_working_set_load import load_chromium_research_working_set
from pyxis.app.chromium_research_working_set_note import (
    ChromiumPageResearchWorkingSetNoteRecord,
    create_chromium_research_working_set_note,
)
from pyxis.app.chromium_research_working_set_note_load import (
    load_chromium_research_working_set_note,
)
from pyxis.app.chromium_research_working_set_note_persistence import (
    persist_chromium_research_working_set_note,
)
from pyxis.app.chromium_research_working_set_note_revision import (
    ChromiumPageResearchWorkingSetNoteRevisionRecord,
    create_chromium_research_working_set_note_revision,
)
from pyxis.app.chromium_research_working_set_persistence import (
    persist_chromium_research_working_set,
)


def test_revision_retains_exact_prior_note_and_same_working_set_with_verbatim_text(
    tmp_path: Path,
) -> None:
    paragraph_note, exact_note, comparison_note = _loaded_records(tmp_path)
    working_set = create_chromium_research_working_set(
        (paragraph_note, exact_note, comparison_note)
    )
    prior = create_chromium_research_working_set_note(
        working_set,
        note_text="Initial interpretation.",
    )
    revised_text = "  Revised interpretation 😀\nKeep uncertainty explicit.  "

    revision = create_chromium_research_working_set_note_revision(
        prior,
        revised_note_text=revised_text,
    )

    assert isinstance(revision, ChromiumPageResearchWorkingSetNoteRevisionRecord)
    assert revision.revision_mode == "caller_authored_revision_of_research_working_set_note"
    assert revision.prior_note is prior
    assert revision.revised_note is not prior
    assert revision.revised_note.working_set is prior.working_set
    assert revision.revised_note.working_set is working_set
    assert revision.revised_note.note_text == revised_text
    assert prior.note_text == "Initial interpretation."

    with pytest.raises(FrozenInstanceError):
        revision.revision_mode = "changed"  # type: ignore[misc]


def test_revision_accepts_note_reconstructed_through_21c(tmp_path: Path) -> None:
    paragraph_note, exact_note, comparison_note = _loaded_records(tmp_path)
    items = (paragraph_note, exact_note, comparison_note)
    working_set = create_chromium_research_working_set(items)
    working_set_path = tmp_path / "working-set.json"
    persist_chromium_research_working_set(working_set, working_set_path)
    live_note = create_chromium_research_working_set_note(
        working_set,
        note_text="Earlier durable rationale.",
    )
    note_path = tmp_path / "working-set-note.json"
    persist_chromium_research_working_set_note(
        live_note,
        working_set_path,
        note_path,
    )
    loaded = load_chromium_research_working_set_note(
        items,
        working_set_path,
        note_path,
    )

    revision = create_chromium_research_working_set_note_revision(
        loaded.note,
        revised_note_text="I changed my interpretation after more research.",
    )

    assert revision.prior_note is loaded.note
    assert revision.revised_note.working_set is loaded.note.working_set
    assert revision.revised_note.working_set is loaded.working_set.working_set
    assert revision.revised_note.note_text == (
        "I changed my interpretation after more research."
    )


def test_revision_does_not_reread_any_sidecars_after_21c_load(tmp_path: Path) -> None:
    paragraph_note, exact_note, comparison_note = _loaded_records(tmp_path)
    items = (paragraph_note, exact_note, comparison_note)
    working_set = create_chromium_research_working_set(items)
    working_set_path = tmp_path / "working-set.json"
    persist_chromium_research_working_set(working_set, working_set_path)
    live_note = create_chromium_research_working_set_note(
        working_set,
        note_text="Prior rationale.",
    )
    note_path = tmp_path / "working-set-note.json"
    persist_chromium_research_working_set_note(
        live_note,
        working_set_path,
        note_path,
    )
    loaded = load_chromium_research_working_set_note(
        items,
        working_set_path,
        note_path,
    )

    note_path.unlink()
    working_set_path.unlink()
    paragraph_note.verification.path.unlink()
    exact_note.verification.path.unlink()
    comparison_note.verification.path.unlink()

    revision = create_chromium_research_working_set_note_revision(
        loaded.note,
        revised_note_text="New in-memory human wording after files moved.",
    )

    assert revision.prior_note is loaded.note
    assert revision.revised_note.working_set is loaded.note.working_set
    assert not note_path.exists()
    assert not working_set_path.exists()
    assert not paragraph_note.verification.path.exists()
    assert not exact_note.verification.path.exists()
    assert not comparison_note.verification.path.exists()


def test_revision_rejects_wrong_parent_type_and_invalid_revised_text(
    tmp_path: Path,
) -> None:
    paragraph_note, _, _ = _loaded_records(tmp_path)
    working_set = create_chromium_research_working_set((paragraph_note,))
    prior = create_chromium_research_working_set_note(
        working_set,
        note_text="Prior.",
    )

    with pytest.raises(TypeError, match="prior_note must be"):
        create_chromium_research_working_set_note_revision(  # type: ignore[arg-type]
            working_set,
            revised_note_text="Wrong prior type.",
        )

    with pytest.raises(TypeError, match="revised_note_text must be a string"):
        create_chromium_research_working_set_note_revision(  # type: ignore[arg-type]
            prior,
            revised_note_text=123,
        )

    with pytest.raises(ValueError, match="non-whitespace caller-authored text"):
        create_chromium_research_working_set_note_revision(
            prior,
            revised_note_text=" \n\t ",
        )


def test_revision_rejects_exact_noop_but_accepts_exact_whitespace_change(
    tmp_path: Path,
) -> None:
    paragraph_note, _, _ = _loaded_records(tmp_path)
    working_set = create_chromium_research_working_set((paragraph_note,))
    prior = create_chromium_research_working_set_note(
        working_set,
        note_text="Same visible words",
    )

    with pytest.raises(ValueError, match="must differ exactly"):
        create_chromium_research_working_set_note_revision(
            prior,
            revised_note_text="Same visible words",
        )

    revision = create_chromium_research_working_set_note_revision(
        prior,
        revised_note_text=" Same visible words ",
    )

    assert revision.revised_note.note_text == " Same visible words "


def test_revision_reestablishes_prior_note_contract_through_21a(tmp_path: Path) -> None:
    paragraph_note, _, _ = _loaded_records(tmp_path)
    working_set = create_chromium_research_working_set((paragraph_note,))
    prior = create_chromium_research_working_set_note(
        working_set,
        note_text="Prior rationale.",
    )
    forged_member = replace(
        paragraph_note,
        verification=replace(
            paragraph_note.verification,
            note_text="Different retained verification text",
        ),
    )
    forged_working_set = replace(working_set, items=(forged_member,))
    forged_prior = replace(prior, working_set=forged_working_set)

    with pytest.raises(
        ValueError,
        match=r"items\[0\] paragraph-note verification is incoherent",
    ):
        create_chromium_research_working_set_note_revision(
            forged_prior,
            revised_note_text="Do not revise from incoherent prior state.",
        )


def test_revision_rejects_unsupported_prior_note_mode(tmp_path: Path) -> None:
    paragraph_note, _, _ = _loaded_records(tmp_path)
    working_set = create_chromium_research_working_set((paragraph_note,))
    prior = create_chromium_research_working_set_note(
        working_set,
        note_text="Prior rationale.",
    )
    forged_prior = replace(prior, note_mode="machine_generated_summary")

    with pytest.raises(ValueError, match="prior working-set note mode is unsupported"):
        create_chromium_research_working_set_note_revision(
            forged_prior,
            revised_note_text="Human revision.",
        )


def test_revision_can_chain_append_only_without_mutating_earlier_records(
    tmp_path: Path,
) -> None:
    paragraph_note, _, _ = _loaded_records(tmp_path)
    working_set = create_chromium_research_working_set((paragraph_note,))
    first = create_chromium_research_working_set_note(
        working_set,
        note_text="v1",
    )
    first_revision = create_chromium_research_working_set_note_revision(
        first,
        revised_note_text="v2",
    )

    second_revision = create_chromium_research_working_set_note_revision(
        first_revision.revised_note,
        revised_note_text="v3",
    )

    assert first.note_text == "v1"
    assert first_revision.prior_note is first
    assert first_revision.revised_note.note_text == "v2"
    assert second_revision.prior_note is first_revision.revised_note
    assert second_revision.revised_note.note_text == "v3"
    assert second_revision.revised_note.working_set is working_set


def test_working_set_note_revision_module_is_publicly_importable(tmp_path: Path) -> None:
    paragraph_note, _, _ = _loaded_records(tmp_path)
    working_set = create_chromium_research_working_set((paragraph_note,))
    prior = ChromiumPageResearchWorkingSetNoteRecord(
        note_mode="caller_authored_note_on_research_working_set",
        working_set=working_set,
        note_text="v1",
    )

    revision = create_chromium_research_working_set_note_revision(
        prior,
        revised_note_text="v2",
    )

    assert revision.prior_note is prior
    assert revision.revised_note.note_text == "v2"
