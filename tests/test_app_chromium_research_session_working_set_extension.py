from __future__ import annotations

from dataclasses import fields
from pathlib import Path

import pytest

from pyxis.app.chromium_research_passage_selection import (
    select_chromium_research_capture_paragraph,
)
from pyxis.app.chromium_research_selection_note import create_chromium_research_paragraph_note
from pyxis.app.chromium_research_selection_note_load import load_chromium_research_paragraph_note
from pyxis.app.chromium_research_selection_note_persistence import (
    persist_chromium_research_paragraph_note,
)
from pyxis.app.chromium_research_session_reentry import reenter_chromium_research_session
from pyxis.app.chromium_research_session_working_set_extension import (
    ChromiumResearchSessionWorkingSetExtensionPersistenceResult,
    persist_chromium_research_session_working_set_extension,
)
from pyxis.app.chromium_research_working_set_load import load_chromium_research_working_set
from pyxis.app.chromium_research_working_set_note_load import (
    load_chromium_research_working_set_note,
)
from test_app_chromium_research_session_reentry import (
    _durable_fixture,
    _persist_loaded_capture,
)


def _session(tmp_path: Path):
    fixture = _durable_fixture(tmp_path)
    reentry = reenter_chromium_research_session(fixture.plan)
    return fixture, reentry


def _new_paragraph_member(
    tmp_path: Path,
    *,
    stem: str = "c",
    paragraph_text: str = "Gamma evidence paragraph",
    note_text: str = "New explicit evidence member.",
):
    source = _persist_loaded_capture(
        tmp_path,
        stem=stem,
        target_id=f"page-{stem}",
        url=f"https://example.test/{stem}",
        paragraph_text=paragraph_text,
    )
    paragraph = select_chromium_research_capture_paragraph(
        source,
        paragraph_ordinal=1,
    )
    note = create_chromium_research_paragraph_note(
        paragraph,
        note_text=note_text,
    )
    note_path = tmp_path / f"new-{stem}-paragraph-note.json"
    persist_chromium_research_paragraph_note(note, note_path)
    loaded = load_chromium_research_paragraph_note(source, note_path)
    return loaded, note_path


def _persist_extension(
    tmp_path: Path,
    reentry,
    appended,
    *,
    rationale_text: str = "Rationale over the explicitly extended evidence basis.",
    stem: str = "extended",
):
    return persist_chromium_research_session_working_set_extension(
        reentry.controller,
        appended,
        rationale_text=rationale_text,
        working_set_destination=tmp_path / f"{stem}-working-set.json",
        note_destination=tmp_path / f"{stem}-working-set-note.json",
    )


def test_extension_preserves_prior_members_then_appends_exact_new_member(tmp_path: Path) -> None:
    _, reentry = _session(tmp_path)
    new_member, _ = _new_paragraph_member(tmp_path)
    prior = reentry.controller.declared_endpoint.revision.revised_note.working_set

    result = _persist_extension(tmp_path, reentry, (new_member,))

    assert result.prior_working_set is prior
    assert result.appended_items == (new_member,)
    assert result.working_set.items[: len(prior.items)] == prior.items
    assert all(
        observed is expected
        for observed, expected in zip(
            result.working_set.items[: len(prior.items)],
            prior.items,
        )
    )
    assert result.working_set.items[-1] is new_member


def test_multiple_appended_members_preserve_exact_order_and_duplicates(tmp_path: Path) -> None:
    _, reentry = _session(tmp_path)
    first, _ = _new_paragraph_member(tmp_path, stem="c")
    second, _ = _new_paragraph_member(
        tmp_path,
        stem="d",
        paragraph_text="Delta evidence paragraph",
        note_text="Delta explicit note.",
    )
    duplicate = reentry.loaded_members[0]

    result = _persist_extension(
        tmp_path,
        reentry,
        (second, first, second, duplicate),
    )

    assert result.appended_items == (second, first, second, duplicate)
    assert result.working_set.items[-4] is second
    assert result.working_set.items[-3] is first
    assert result.working_set.items[-2] is second
    assert result.working_set.items[-1] is duplicate


def test_new_human_rationale_preserves_exact_unicode_whitespace(tmp_path: Path) -> None:
    _, reentry = _session(tmp_path)
    new_member, _ = _new_paragraph_member(tmp_path)
    text = "  New evidence changes my question 😀\nStill tentative.  "

    result = _persist_extension(
        tmp_path,
        reentry,
        (new_member,),
        rationale_text=text,
    )

    assert result.note.note_text == text
    assert result.note_persistence.note.note_text == text


def test_same_rationale_text_is_allowed_when_explicitly_supplied(tmp_path: Path) -> None:
    _, reentry = _session(tmp_path)
    new_member, _ = _new_paragraph_member(tmp_path)
    old_text = reentry.controller.declared_endpoint.revision.revised_note.note_text

    result = _persist_extension(
        tmp_path,
        reentry,
        (new_member,),
        rationale_text=old_text,
    )

    assert result.note.note_text == old_text
    assert result.note.working_set is result.working_set
    assert result.note.working_set is not result.prior_working_set


def test_empty_appended_items_reject_before_any_write(tmp_path: Path) -> None:
    _, reentry = _session(tmp_path)
    working_set_path = tmp_path / "empty-working-set.json"
    note_path = tmp_path / "empty-note.json"

    with pytest.raises(ValueError, match="at least one"):
        persist_chromium_research_session_working_set_extension(
            reentry.controller,
            (),
            rationale_text="Explicit rationale.",
            working_set_destination=working_set_path,
            note_destination=note_path,
        )

    assert not working_set_path.exists()
    assert not note_path.exists()


def test_unsupported_appended_item_rejects_before_any_write(tmp_path: Path) -> None:
    _, reentry = _session(tmp_path)
    working_set_path = tmp_path / "bad-working-set.json"
    note_path = tmp_path / "bad-note.json"

    with pytest.raises(TypeError, match="supported relinked"):
        persist_chromium_research_session_working_set_extension(
            reentry.controller,
            (object(),),  # type: ignore[arg-type]
            rationale_text="Explicit rationale.",
            working_set_destination=working_set_path,
            note_destination=note_path,
        )

    assert not working_set_path.exists()
    assert not note_path.exists()


def test_whitespace_only_new_rationale_rejects_before_any_write(tmp_path: Path) -> None:
    _, reentry = _session(tmp_path)
    new_member, _ = _new_paragraph_member(tmp_path)
    working_set_path = tmp_path / "blank-working-set.json"
    note_path = tmp_path / "blank-note.json"

    with pytest.raises(ValueError, match="non-whitespace"):
        persist_chromium_research_session_working_set_extension(
            reentry.controller,
            (new_member,),
            rationale_text="  \n\t  ",
            working_set_destination=working_set_path,
            note_destination=note_path,
        )

    assert not working_set_path.exists()
    assert not note_path.exists()


def test_existing_working_set_destination_rejects_before_note_write(tmp_path: Path) -> None:
    _, reentry = _session(tmp_path)
    new_member, _ = _new_paragraph_member(tmp_path)
    working_set_path = tmp_path / "existing-working-set.json"
    note_path = tmp_path / "should-not-exist-note.json"
    working_set_path.write_text("keep exact\n", encoding="utf-8")

    with pytest.raises(FileExistsError, match="working_set_destination"):
        persist_chromium_research_session_working_set_extension(
            reentry.controller,
            (new_member,),
            rationale_text="Explicit rationale.",
            working_set_destination=working_set_path,
            note_destination=note_path,
        )

    assert working_set_path.read_text(encoding="utf-8") == "keep exact\n"
    assert not note_path.exists()


def test_existing_note_destination_rejects_before_working_set_write(tmp_path: Path) -> None:
    _, reentry = _session(tmp_path)
    new_member, _ = _new_paragraph_member(tmp_path)
    working_set_path = tmp_path / "should-not-exist-working-set.json"
    note_path = tmp_path / "existing-note.json"
    note_path.write_text("keep note exact\n", encoding="utf-8")

    with pytest.raises(FileExistsError, match="note_destination"):
        persist_chromium_research_session_working_set_extension(
            reentry.controller,
            (new_member,),
            rationale_text="Explicit rationale.",
            working_set_destination=working_set_path,
            note_destination=note_path,
        )

    assert not working_set_path.exists()
    assert note_path.read_text(encoding="utf-8") == "keep note exact\n"


def test_same_output_destination_rejects_before_write(tmp_path: Path) -> None:
    _, reentry = _session(tmp_path)
    new_member, _ = _new_paragraph_member(tmp_path)
    destination = tmp_path / "same.json"

    with pytest.raises(ValueError, match="distinct"):
        persist_chromium_research_session_working_set_extension(
            reentry.controller,
            (new_member,),
            rationale_text="Explicit rationale.",
            working_set_destination=destination,
            note_destination=destination,
        )

    assert not destination.exists()


def test_durable_outputs_freshly_relink_to_exact_new_members_and_rationale(tmp_path: Path) -> None:
    _, reentry = _session(tmp_path)
    new_member, _ = _new_paragraph_member(tmp_path)
    result = _persist_extension(tmp_path, reentry, (new_member,))

    loaded_working_set = load_chromium_research_working_set(
        result.working_set.items,
        result.working_set_persistence.path,
    )
    loaded_note = load_chromium_research_working_set_note(
        result.working_set.items,
        result.working_set_persistence.path,
        result.note_persistence.path,
    )

    assert loaded_working_set.working_set.items == result.working_set.items
    assert all(
        observed is expected
        for observed, expected in zip(
            loaded_working_set.working_set.items,
            result.working_set.items,
        )
    )
    assert loaded_note.note.note_text == result.note.note_text
    assert loaded_note.verification.working_set_record_sha256 == (
        result.working_set_persistence.working_set_record_sha256
    )


def test_extension_does_not_mutate_or_adopt_current_session(tmp_path: Path) -> None:
    _, reentry = _session(tmp_path)
    new_member, _ = _new_paragraph_member(tmp_path)
    controller = reentry.controller
    loaded = controller.loaded
    presentation = controller.presentation
    endpoint = controller.declared_endpoint
    prior_working_set = endpoint.revision.revised_note.working_set

    result = _persist_extension(tmp_path, reentry, (new_member,))

    assert controller.loaded is loaded
    assert controller.presentation is presentation
    assert controller.declared_endpoint is endpoint
    assert controller.declared_endpoint.revision.revised_note.working_set is prior_working_set
    assert result.working_set is not prior_working_set
    assert result.note.working_set is result.working_set


def test_result_shape_contains_no_adoption_head_or_transition_authority(tmp_path: Path) -> None:
    _, reentry = _session(tmp_path)
    new_member, _ = _new_paragraph_member(tmp_path)
    result = _persist_extension(tmp_path, reentry, (new_member,))

    assert isinstance(result, ChromiumResearchSessionWorkingSetExtensionPersistenceResult)
    assert tuple(field.name for field in fields(result)) == (
        "prior_session",
        "prior_endpoint",
        "prior_working_set",
        "appended_items",
        "working_set",
        "working_set_persistence",
        "note",
        "note_persistence",
    )
    for forbidden in (
        "latest",
        "current_head",
        "canonical_head",
        "adopted",
        "continuation",
        "transition",
        "semantic_support",
    ):
        assert not hasattr(result, forbidden)


def test_unadopted_last_endpoint_write_is_not_used_as_extension_basis(tmp_path: Path) -> None:
    fixture, reentry = _session(tmp_path)
    controller = reentry.controller
    declared_endpoint = controller.declared_endpoint
    unadopted = controller.persist_declared_endpoint_revision(
        "v7 unadopted bookkeeping only",
        prior_edge_source=fixture.v6_path,
        destination=tmp_path / "v7-unadopted.json",
    )
    new_member, _ = _new_paragraph_member(tmp_path)

    result = _persist_extension(tmp_path, reentry, (new_member,))

    assert controller.last_endpoint_revision is unadopted
    assert result.prior_endpoint is declared_endpoint
    assert result.prior_endpoint.revision.revised_note.note_text == (
        "v6 exact human wording\nStill tentative."
    )
    assert unadopted.extension.revision.revised_note.note_text == (
        "v7 unadopted bookkeeping only"
    )


def test_loaded_new_member_can_extend_basis_after_its_sidecar_is_deleted(tmp_path: Path) -> None:
    _, reentry = _session(tmp_path)
    new_member, note_path = _new_paragraph_member(tmp_path)
    note_path.unlink()

    result = _persist_extension(tmp_path, reentry, (new_member,))

    assert result.working_set.items[-1] is new_member
    assert result.working_set_persistence.path.exists()
    assert result.note_persistence.path.exists()
