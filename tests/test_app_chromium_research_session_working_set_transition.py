from __future__ import annotations

from dataclasses import fields
import hashlib
import json
from pathlib import Path

import pytest

from pyxis.app.chromium_research_session_controller import ChromiumResearchSessionController
from pyxis.app.chromium_research_session_working_set_extension import (
    persist_chromium_research_session_working_set_extension,
)
from pyxis.app.chromium_research_session_working_set_transition_revision_root import (
    ChromiumResearchSessionWorkingSetTransitionRevisionRootError,
    create_chromium_research_session_working_set_transition_revision_root,
)
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
from test_app_chromium_research_bare_selection_presentation import (
    _declared_v2_bare_sequence,
)
from test_app_chromium_research_session_working_set_extension import (
    _new_paragraph_member,
    _persist_extension,
    _session,
)


def _canonical_bytes(payload: object) -> bytes:
    return json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def _write_recomputed_transition_document(path: Path, document: dict[str, object]) -> None:
    document["transition_record_sha256"] = hashlib.sha256(
        _canonical_bytes(document["transition_record"])
    ).hexdigest()
    path.write_bytes(_canonical_bytes(document) + b"\n")


def _prepared_v2_transition(tmp_path: Path):
    (
        paragraph_note,
        bare,
        bare_path,
        _,
        _,
        _,
        _,
        _,
        successor_path,
        _,
        _,
        loaded,
    ) = _declared_v2_bare_sequence(tmp_path)
    controller = ChromiumResearchSessionController(loaded)
    new_member, new_member_path = _new_paragraph_member(
        tmp_path,
        stem="50c",
        paragraph_text="Additional evidence after saved passage",
        note_text="Additional explicit evidence note.",
    )
    prepared = persist_chromium_research_session_working_set_extension(
        controller,
        (new_member,),
        rationale_text="Changed rationale retaining a bare saved passage.",
        working_set_destination=tmp_path / "50c-v2-working-set.json",
        note_destination=tmp_path / "50c-v2-working-set-note.json",
    )
    transition = create_chromium_research_session_working_set_transition(
        controller,
        prepared,
    )
    return (
        paragraph_note,
        bare,
        bare_path,
        new_member,
        new_member_path,
        controller,
        successor_path,
        prepared,
        transition,
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



def test_50c_v2_successor_pair_uses_existing_transition_v1_and_freshly_relinks(
    tmp_path: Path,
) -> None:
    (
        paragraph_note,
        bare,
        bare_path,
        new_member,
        new_member_path,
        controller,
        prior_edge_path,
        prepared,
        transition,
    ) = _prepared_v2_transition(tmp_path)

    bare_path.unlink(missing_ok=True)
    paragraph_note.verification.path.unlink(missing_ok=True)
    new_member_path.unlink(missing_ok=True)

    destination = tmp_path / "50c-transition-v1.json"
    persistence = persist_chromium_research_session_working_set_transition(
        transition,
        prior_edge_source=prior_edge_path,
        working_set_source=prepared.working_set_persistence.path,
        note_source=prepared.note_persistence.path,
        destination=destination,
    )
    verification = verify_chromium_research_session_working_set_transition(destination)

    assert persistence.transition_format == (
        "pyxis.chromium.research_session_working_set_transition.v1"
    )
    assert verification.transition_format == persistence.transition_format
    assert verification.successor_working_set_format == (
        "pyxis.chromium.research_working_set.v2"
    )
    assert verification.successor_note_format == (
        "pyxis.chromium.research_working_set_note.v2"
    )
    assert verification.successor_working_set_record_sha256 == (
        prepared.working_set_persistence.working_set_record_sha256
    )
    assert verification.successor_note_record_sha256 == (
        prepared.note_persistence.note_record_sha256
    )

    raw = destination.read_text(encoding="utf-8")
    assert bare.selection.selected_text not in raw
    assert prepared.note.note_text not in raw
    assert str(prepared.working_set_persistence.path) not in raw
    assert str(prepared.note_persistence.path) not in raw

    loaded = load_chromium_research_session_working_set_transition(
        controller.declared_endpoint,
        prepared.working_set.items,
        prior_edge_source=prior_edge_path,
        working_set_source=prepared.working_set_persistence.path,
        note_source=prepared.note_persistence.path,
        transition_source=destination,
    )
    assert loaded.verification.transition_format == persistence.transition_format
    assert loaded.successor_note.verification.note_format == (
        "pyxis.chromium.research_working_set_note.v2"
    )
    assert loaded.successor_note.working_set.verification.working_set_format == (
        "pyxis.chromium.research_working_set.v2"
    )
    assert all(
        observed is expected
        for observed, expected in zip(
            loaded.successor_note.working_set.working_set.items,
            prepared.working_set.items,
        )
    )
    assert loaded.successor_note.working_set.working_set.items[-1] is new_member
    assert not bare.verification.path.exists()
    assert not new_member.verification.path.exists()


@pytest.mark.parametrize(
    ("working_set_format", "note_format"),
    (
        (
            "pyxis.chromium.research_working_set.v1",
            "pyxis.chromium.research_working_set_note.v2",
        ),
        (
            "pyxis.chromium.research_working_set.v2",
            "pyxis.chromium.research_working_set_note.v1",
        ),
    ),
)
def test_50c_file_valid_cross_version_successor_pair_rejects(
    tmp_path: Path,
    working_set_format: str,
    note_format: str,
) -> None:
    *_, controller, prior_edge_path, prepared, transition = _prepared_v2_transition(tmp_path)
    destination = tmp_path / "50c-cross-version-transition.json"
    persist_chromium_research_session_working_set_transition(
        transition,
        prior_edge_source=prior_edge_path,
        working_set_source=prepared.working_set_persistence.path,
        note_source=prepared.note_persistence.path,
        destination=destination,
    )
    document = json.loads(destination.read_text(encoding="utf-8"))
    record = document["transition_record"]
    record["successor_working_set_reference"]["format"] = working_set_format
    record["successor_note_reference"]["format"] = note_format
    _write_recomputed_transition_document(destination, document)

    with pytest.raises(
        ChromiumResearchSessionWorkingSetTransitionIntegrityError,
        match="successor format pair is unsupported",
    ):
        verify_chromium_research_session_working_set_transition(destination)


def test_50c_file_valid_wrong_v2_successor_digest_fails_fresh_relink(
    tmp_path: Path,
) -> None:
    *_, controller, prior_edge_path, prepared, transition = _prepared_v2_transition(tmp_path)
    destination = tmp_path / "50c-wrong-digest-transition.json"
    persist_chromium_research_session_working_set_transition(
        transition,
        prior_edge_source=prior_edge_path,
        working_set_source=prepared.working_set_persistence.path,
        note_source=prepared.note_persistence.path,
        destination=destination,
    )
    document = json.loads(destination.read_text(encoding="utf-8"))
    document["transition_record"]["successor_note_reference"]["record_sha256"] = "f" * 64
    _write_recomputed_transition_document(destination, document)

    verified = verify_chromium_research_session_working_set_transition(destination)
    assert verified.successor_note_format == "pyxis.chromium.research_working_set_note.v2"

    with pytest.raises(ValueError, match="different successor-note record"):
        load_chromium_research_session_working_set_transition(
            controller.declared_endpoint,
            prepared.working_set.items,
            prior_edge_source=prior_edge_path,
            working_set_source=prepared.working_set_persistence.path,
            note_source=prepared.note_persistence.path,
            transition_source=destination,
        )


def test_50c_existing_34a_remains_closed_to_v2_backed_transition(
    tmp_path: Path,
) -> None:
    *_, controller, prior_edge_path, prepared, transition = _prepared_v2_transition(tmp_path)
    destination = tmp_path / "50c-transition-before-root.json"
    persist_chromium_research_session_working_set_transition(
        transition,
        prior_edge_source=prior_edge_path,
        working_set_source=prepared.working_set_persistence.path,
        note_source=prepared.note_persistence.path,
        destination=destination,
    )
    loaded = load_chromium_research_session_working_set_transition(
        controller.declared_endpoint,
        prepared.working_set.items,
        prior_edge_source=prior_edge_path,
        working_set_source=prepared.working_set_persistence.path,
        note_source=prepared.note_persistence.path,
        transition_source=destination,
    )

    with pytest.raises(
        ChromiumResearchSessionWorkingSetTransitionRevisionRootError,
        match="successor working set uses an unsupported format",
    ):
        create_chromium_research_session_working_set_transition_revision_root(
            loaded,
            revised_note_text="First revision after the v2-backed transition.",
        )
