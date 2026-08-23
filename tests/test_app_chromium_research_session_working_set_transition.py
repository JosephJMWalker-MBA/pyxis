from __future__ import annotations

from dataclasses import fields
import json
from pathlib import Path

import pytest

from pyxis.app.chromium_research_session_working_set_transition import (
    ChromiumResearchSessionWorkingSetTransitionError,
    ChromiumResearchSessionWorkingSetTransitionRecord,
    create_chromium_research_session_working_set_transition,
)
from pyxis.app.chromium_research_session_working_set_transition_load import (
    ChromiumPageResearchLoadedWorkingSetTransitionRecord,
    load_chromium_research_session_working_set_transition,
)
from pyxis.app.chromium_research_session_working_set_transition_persistence import (
    ChromiumResearchSessionWorkingSetTransitionIntegrityError,
    persist_chromium_research_session_working_set_transition,
    verify_chromium_research_session_working_set_transition,
)
from test_app_chromium_research_session_working_set_extension import (
    _new_paragraph_member,
    _persist_extension,
    _session,
)


def _prepared_transition(tmp_path: Path, *, stem: str = "bridge"):
    fixture, reentry = _session(tmp_path)
    new_member, _ = _new_paragraph_member(tmp_path, stem="c")
    prepared = _persist_extension(
        tmp_path,
        reentry,
        (new_member,),
        rationale_text="  Explicit rationale over changed evidence 😀\nStill human-owned.  ",
        stem=stem,
    )
    transition = create_chromium_research_session_working_set_transition(
        reentry.controller,
        prepared,
    )
    return fixture, reentry, new_member, prepared, transition


def _persist_transition(tmp_path: Path, *, stem: str = "bridge"):
    fixture, reentry, new_member, prepared, transition = _prepared_transition(
        tmp_path,
        stem=stem,
    )
    destination = tmp_path / f"{stem}-transition.json"
    persistence = persist_chromium_research_session_working_set_transition(
        transition,
        prior_edge_source=fixture.v6_path,
        working_set_source=prepared.working_set_persistence.path,
        note_source=prepared.note_persistence.path,
        destination=destination,
    )
    return fixture, reentry, new_member, prepared, transition, persistence


def test_create_transition_retains_exact_declared_endpoint_and_changed_basis(tmp_path: Path) -> None:
    _, reentry, _, prepared, transition = _prepared_transition(tmp_path)

    assert isinstance(transition, ChromiumResearchSessionWorkingSetTransitionRecord)
    assert transition.prior_endpoint is reentry.controller.declared_endpoint
    assert transition.successor_working_set is prepared.working_set
    assert transition.successor_note is prepared.note
    assert transition.successor_note.working_set is transition.successor_working_set
    assert transition.transition_mode == "caller_explicit_transition_to_changed_research_working_set"
    assert {field.name for field in fields(transition)} == {
        "transition_mode",
        "prior_endpoint",
        "successor_working_set",
        "successor_note",
    }


def test_prepared_basis_from_different_session_rejects(tmp_path: Path) -> None:
    first_root = tmp_path / "first"
    second_root = tmp_path / "second"
    first_root.mkdir()
    second_root.mkdir()
    _, first_reentry = _session(first_root)
    _, second_reentry = _session(second_root)
    member, _ = _new_paragraph_member(second_root, stem="c")
    prepared = _persist_extension(second_root, second_reentry, (member,))

    with pytest.raises(
        ChromiumResearchSessionWorkingSetTransitionError,
        match="different prior session|different declared endpoint",
    ):
        create_chromium_research_session_working_set_transition(
            first_reentry.controller,
            prepared,
        )


def test_persist_transition_freshly_records_exact_durable_identities(tmp_path: Path) -> None:
    fixture, reentry, _, prepared, transition, persistence = _persist_transition(tmp_path)
    verification = verify_chromium_research_session_working_set_transition(
        persistence.path
    )

    assert persistence.transition is transition
    assert persistence.fresh_prior_endpoint is not reentry.controller.declared_endpoint
    assert (
        verification.prior_endpoint_record_sha256
        == reentry.controller.declared_endpoint.verification.edge_record_sha256
    )
    assert (
        verification.successor_working_set_record_sha256
        == prepared.working_set_persistence.working_set_record_sha256
    )
    assert (
        verification.successor_note_record_sha256
        == prepared.note_persistence.note_record_sha256
    )
    assert persistence.path == tmp_path / "bridge-transition.json"
    assert fixture.v6_path.exists()


def test_fresh_load_relinks_transition_to_explicit_prior_and_successor(tmp_path: Path) -> None:
    fixture, reentry, _, prepared, _, persistence = _persist_transition(tmp_path)

    loaded = load_chromium_research_session_working_set_transition(
        reentry.controller.declared_endpoint,
        prepared.working_set.items,
        prior_edge_source=fixture.v6_path,
        working_set_source=prepared.working_set_persistence.path,
        note_source=prepared.note_persistence.path,
        transition_source=persistence.path,
    )

    assert isinstance(loaded, ChromiumPageResearchLoadedWorkingSetTransitionRecord)
    assert loaded.prior_endpoint is not reentry.controller.declared_endpoint
    assert (
        loaded.prior_endpoint.verification.edge_record_sha256
        == reentry.controller.declared_endpoint.verification.edge_record_sha256
    )
    assert loaded.successor_note.note.note_text == prepared.note.note_text
    assert tuple(loaded.successor_note.working_set.working_set.items) == prepared.working_set.items
    assert all(
        observed is expected
        for observed, expected in zip(
            loaded.successor_note.working_set.working_set.items,
            prepared.working_set.items,
        )
    )


def test_moved_identical_durable_inputs_work_only_when_new_paths_are_supplied(tmp_path: Path) -> None:
    fixture, _, _, prepared, transition = _prepared_transition(tmp_path)
    moved_prior = tmp_path / "moved-v6.edge.json"
    moved_working_set = tmp_path / "moved-working-set.json"
    moved_note = tmp_path / "moved-note.json"
    fixture.v6_path.rename(moved_prior)
    prepared.working_set_persistence.path.rename(moved_working_set)
    prepared.note_persistence.path.rename(moved_note)

    persistence = persist_chromium_research_session_working_set_transition(
        transition,
        prior_edge_source=moved_prior,
        working_set_source=moved_working_set,
        note_source=moved_note,
        destination=tmp_path / "moved-transition.json",
    )

    assert persistence.path.exists()
    assert not fixture.v6_path.exists()
    assert not prepared.working_set_persistence.path.exists()
    assert not prepared.note_persistence.path.exists()


def test_wrong_prior_edge_rejects_without_transition_write(tmp_path: Path) -> None:
    fixture, _, _, prepared, transition = _prepared_transition(tmp_path)
    destination = tmp_path / "wrong-prior-transition.json"

    with pytest.raises(ValueError):
        persist_chromium_research_session_working_set_transition(
            transition,
            prior_edge_source=fixture.v5_path,
            working_set_source=prepared.working_set_persistence.path,
            note_source=prepared.note_persistence.path,
            destination=destination,
        )

    assert not destination.exists()


def test_wrong_successor_working_set_rejects_without_transition_write(tmp_path: Path) -> None:
    fixture, reentry, _, prepared, transition = _prepared_transition(tmp_path, stem="first")
    other_member, _ = _new_paragraph_member(
        tmp_path,
        stem="d",
        paragraph_text="Delta evidence paragraph",
        note_text="Different member.",
    )
    other = _persist_extension(tmp_path, reentry, (other_member,), stem="other")
    destination = tmp_path / "wrong-working-set-transition.json"

    with pytest.raises(ValueError):
        persist_chromium_research_session_working_set_transition(
            transition,
            prior_edge_source=fixture.v6_path,
            working_set_source=other.working_set_persistence.path,
            note_source=prepared.note_persistence.path,
            destination=destination,
        )

    assert not destination.exists()


def test_wrong_successor_note_rejects_without_transition_write(tmp_path: Path) -> None:
    fixture, reentry, _, prepared, transition = _prepared_transition(tmp_path, stem="first")
    other_member, _ = _new_paragraph_member(
        tmp_path,
        stem="d",
        paragraph_text="Delta evidence paragraph",
        note_text="Different member.",
    )
    other = _persist_extension(tmp_path, reentry, (other_member,), stem="other")
    destination = tmp_path / "wrong-note-transition.json"

    with pytest.raises(ValueError):
        persist_chromium_research_session_working_set_transition(
            transition,
            prior_edge_source=fixture.v6_path,
            working_set_source=prepared.working_set_persistence.path,
            note_source=other.note_persistence.path,
            destination=destination,
        )

    assert not destination.exists()


def test_transition_destination_is_no_overwrite(tmp_path: Path) -> None:
    fixture, _, _, prepared, transition = _prepared_transition(tmp_path)
    destination = tmp_path / "existing-transition.json"
    destination.write_text("existing", encoding="utf-8")

    with pytest.raises(FileExistsError):
        persist_chromium_research_session_working_set_transition(
            transition,
            prior_edge_source=fixture.v6_path,
            working_set_source=prepared.working_set_persistence.path,
            note_source=prepared.note_persistence.path,
            destination=destination,
        )

    assert destination.read_text(encoding="utf-8") == "existing"


def test_tampered_transition_bytes_fail_file_local_verification(tmp_path: Path) -> None:
    *_, persistence = _persist_transition(tmp_path)
    document = json.loads(persistence.path.read_text(encoding="utf-8"))
    document["transition_record"]["transition_mode"] = "forged-mode"
    persistence.path.write_text(
        json.dumps(
            document,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
        + "\n",
        encoding="utf-8",
    )

    with pytest.raises(ChromiumResearchSessionWorkingSetTransitionIntegrityError):
        verify_chromium_research_session_working_set_transition(persistence.path)


def test_fresh_load_rejects_wrong_successor_member_order(tmp_path: Path) -> None:
    fixture, reentry, _, prepared, _, persistence = _persist_transition(tmp_path)
    destination_items = tuple(reversed(prepared.working_set.items))

    with pytest.raises(ValueError):
        load_chromium_research_session_working_set_transition(
            reentry.controller.declared_endpoint,
            destination_items,
            prior_edge_source=fixture.v6_path,
            working_set_source=prepared.working_set_persistence.path,
            note_source=prepared.note_persistence.path,
            transition_source=persistence.path,
        )


def test_transition_document_contains_only_identity_relationship_not_locators_or_head_state(tmp_path: Path) -> None:
    *_, persistence = _persist_transition(tmp_path)
    document = json.loads(persistence.path.read_text(encoding="utf-8"))
    text = persistence.path.read_text(encoding="utf-8")

    assert set(document) == {
        "format",
        "transition_record",
        "transition_record_sha256",
    }
    assert set(document["transition_record"]) == {
        "prior_endpoint_reference",
        "successor_note_reference",
        "successor_working_set_reference",
        "transition_mode",
    }
    forbidden = (
        "path",
        "timestamp",
        "latest",
        "current_head",
        "canonical_head",
        "semantic_support",
        "chronology",
    )
    assert all(term not in text for term in forbidden)


def test_same_rationale_text_can_cross_basis_only_by_explicit_human_preparation(tmp_path: Path) -> None:
    fixture, reentry = _session(tmp_path)
    member, _ = _new_paragraph_member(tmp_path)
    old_text = reentry.controller.declared_endpoint.revision.revised_note.note_text
    prepared = _persist_extension(
        tmp_path,
        reentry,
        (member,),
        rationale_text=old_text,
        stem="same-text",
    )
    transition = create_chromium_research_session_working_set_transition(
        reentry.controller,
        prepared,
    )
    persistence = persist_chromium_research_session_working_set_transition(
        transition,
        prior_edge_source=fixture.v6_path,
        working_set_source=prepared.working_set_persistence.path,
        note_source=prepared.note_persistence.path,
        destination=tmp_path / "same-text-transition.json",
    )

    assert transition.successor_note.note_text == old_text
    assert persistence.path.exists()


def test_unadopted_endpoint_write_does_not_become_transition_prior_authority(tmp_path: Path) -> None:
    fixture, reentry = _session(tmp_path)
    unadopted = reentry.controller.persist_declared_endpoint_revision(
        "Unadopted v7 rationale.",
        prior_edge_source=fixture.v6_path,
        destination=tmp_path / "unadopted-v7.edge.json",
    )
    member, _ = _new_paragraph_member(tmp_path)
    prepared = _persist_extension(tmp_path, reentry, (member,))
    transition = create_chromium_research_session_working_set_transition(
        reentry.controller,
        prepared,
    )

    assert transition.prior_endpoint is reentry.controller.declared_endpoint
    assert (
        transition.prior_endpoint.verification.edge_record_sha256
        != unadopted.persistence.verification.edge_record_sha256
        if hasattr(unadopted.persistence, "verification")
        else transition.prior_endpoint.verification.edge_record_sha256
        != unadopted.persistence.edge_record_sha256
    )


def test_loaded_transition_remains_application_evidence_after_files_are_removed(tmp_path: Path) -> None:
    fixture, reentry, _, prepared, _, persistence = _persist_transition(tmp_path)
    loaded = load_chromium_research_session_working_set_transition(
        reentry.controller.declared_endpoint,
        prepared.working_set.items,
        prior_edge_source=fixture.v6_path,
        working_set_source=prepared.working_set_persistence.path,
        note_source=prepared.note_persistence.path,
        transition_source=persistence.path,
    )
    expected_transition_sha = loaded.verification.transition_record_sha256
    expected_note_text = loaded.successor_note.note.note_text

    fixture.v6_path.unlink()
    prepared.working_set_persistence.path.unlink()
    prepared.note_persistence.path.unlink()
    persistence.path.unlink()

    assert loaded.verification.transition_record_sha256 == expected_transition_sha
    assert loaded.successor_note.note.note_text == expected_note_text
    assert loaded.prior_endpoint.revision.revised_note.note_text
