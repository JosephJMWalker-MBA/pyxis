from __future__ import annotations

from dataclasses import fields
import json
from pathlib import Path

import pytest

from pyxis.app.chromium_research_session_working_set_transition_load import (
    load_chromium_research_session_working_set_transition,
)
from pyxis.app.chromium_research_session_working_set_transition_revision_root import (
    ChromiumResearchSessionWorkingSetTransitionRevisionRootRecord,
    create_chromium_research_session_working_set_transition_revision_root,
)
from pyxis.app.chromium_research_session_working_set_transition_revision_root_load import (
    ChromiumPageResearchLoadedWorkingSetTransitionRevisionRootRecord,
    load_chromium_research_session_working_set_transition_revision_root,
)
from pyxis.app.chromium_research_session_working_set_transition_revision_root_persistence import (
    ChromiumResearchSessionWorkingSetTransitionRevisionRootIntegrityError,
    persist_chromium_research_session_working_set_transition_revision_root,
    verify_chromium_research_session_working_set_transition_revision_root,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_load import (
    load_chromium_research_working_set_note_revision_edge,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_sequence_load import (
    load_chromium_research_working_set_note_revision_edge_sequence,
)
from test_app_chromium_research_session_working_set_transition import (
    _persist_transition,
)


def _loaded_transition(tmp_path: Path, *, stem: str = "bridge"):
    fixture, reentry, _, prepared, _, persistence = _persist_transition(
        tmp_path,
        stem=stem,
    )
    loaded = load_chromium_research_session_working_set_transition(
        reentry.controller.declared_endpoint,
        prepared.working_set.items,
        prior_edge_source=fixture.v6_path,
        working_set_source=prepared.working_set_persistence.path,
        note_source=prepared.note_persistence.path,
        transition_source=persistence.path,
    )
    return fixture, reentry, prepared, persistence, loaded


def _persist_root(
    tmp_path: Path,
    *,
    stem: str = "bridge",
    revised_note_text: str = "First rationale revision after the evidence-basis change.",
):
    fixture, reentry, prepared, transition_persistence, loaded_transition = _loaded_transition(
        tmp_path,
        stem=stem,
    )
    root = create_chromium_research_session_working_set_transition_revision_root(
        loaded_transition,
        revised_note_text=revised_note_text,
    )
    persistence = persist_chromium_research_session_working_set_transition_revision_root(
        root,
        prior_edge_source=fixture.v6_path,
        working_set_source=prepared.working_set_persistence.path,
        note_source=prepared.note_persistence.path,
        transition_source=transition_persistence.path,
        destination=tmp_path / f"{stem}-revision-root.json",
    )
    return fixture, reentry, prepared, transition_persistence, loaded_transition, root, persistence


def test_create_root_revises_exact_transition_successor_note(tmp_path: Path) -> None:
    _, _, _, _, loaded_transition = _loaded_transition(tmp_path)

    root = create_chromium_research_session_working_set_transition_revision_root(
        loaded_transition,
        revised_note_text="Reconsidered after reading the expanded evidence set.",
    )

    assert isinstance(root, ChromiumResearchSessionWorkingSetTransitionRevisionRootRecord)
    assert root.transition is loaded_transition
    assert root.revision.prior_note is loaded_transition.successor_note.note
    assert (
        root.revision.revised_note.working_set
        is loaded_transition.successor_note.note.working_set
    )
    assert root.revision.revised_note.note_text == (
        "Reconsidered after reading the expanded evidence set."
    )
    assert root.root_mode == (
        "caller_authored_revision_root_after_changed_research_working_set_transition"
    )
    assert {field.name for field in fields(root)} == {
        "root_mode",
        "transition",
        "revision",
    }


def test_exact_text_noop_rejects_at_root_creation(tmp_path: Path) -> None:
    _, _, _, _, loaded_transition = _loaded_transition(tmp_path)
    prior_text = loaded_transition.successor_note.note.note_text

    with pytest.raises(ValueError, match="differ exactly"):
        create_chromium_research_session_working_set_transition_revision_root(
            loaded_transition,
            revised_note_text=prior_text,
        )


def test_wrong_root_input_type_rejects(tmp_path: Path) -> None:
    with pytest.raises(TypeError, match="LoadedWorkingSetTransitionRecord"):
        create_chromium_research_session_working_set_transition_revision_root(
            object(),
            revised_note_text="Human revision.",
        )


def test_persistence_freshly_records_exact_transition_identity(tmp_path: Path) -> None:
    *_, loaded_transition, root, persistence = _persist_root(tmp_path)
    verification = verify_chromium_research_session_working_set_transition_revision_root(
        persistence.path
    )

    assert persistence.root is root
    assert persistence.fresh_transition is not loaded_transition
    assert verification.transition_format == loaded_transition.verification.transition_format
    assert (
        verification.transition_record_sha256
        == loaded_transition.verification.transition_record_sha256
    )
    assert verification.revised_note_text == root.revision.revised_note.note_text


def test_fresh_load_reconstructs_root_through_exact_transition(tmp_path: Path) -> None:
    (
        fixture,
        reentry,
        prepared,
        transition_persistence,
        loaded_transition,
        root,
        persistence,
    ) = _persist_root(tmp_path)

    loaded = load_chromium_research_session_working_set_transition_revision_root(
        reentry.controller.declared_endpoint,
        prepared.working_set.items,
        prior_edge_source=fixture.v6_path,
        working_set_source=prepared.working_set_persistence.path,
        note_source=prepared.note_persistence.path,
        transition_source=transition_persistence.path,
        root_source=persistence.path,
    )

    assert isinstance(loaded, ChromiumPageResearchLoadedWorkingSetTransitionRevisionRootRecord)
    assert loaded.transition is not loaded_transition
    assert loaded.root.transition is loaded.transition
    assert loaded.root.revision.prior_note is loaded.transition.successor_note.note
    assert loaded.root.revision.revised_note.note_text == root.revision.revised_note.note_text
    assert (
        loaded.verification.transition_record_sha256
        == loaded.transition.verification.transition_record_sha256
    )


def test_moved_identical_inputs_work_only_with_explicit_new_paths(tmp_path: Path) -> None:
    fixture, _, prepared, transition_persistence, loaded_transition = _loaded_transition(tmp_path)
    moved_prior = tmp_path / "moved-v6.edge.json"
    moved_working_set = tmp_path / "moved-working-set.json"
    moved_note = tmp_path / "moved-note.json"
    moved_transition = tmp_path / "moved-transition.json"
    fixture.v6_path.rename(moved_prior)
    prepared.working_set_persistence.path.rename(moved_working_set)
    prepared.note_persistence.path.rename(moved_note)
    transition_persistence.path.rename(moved_transition)

    root = create_chromium_research_session_working_set_transition_revision_root(
        loaded_transition,
        revised_note_text="Revision from moved durable inputs.",
    )
    persistence = persist_chromium_research_session_working_set_transition_revision_root(
        root,
        prior_edge_source=moved_prior,
        working_set_source=moved_working_set,
        note_source=moved_note,
        transition_source=moved_transition,
        destination=tmp_path / "moved-root.json",
    )

    assert persistence.path.exists()
    assert not fixture.v6_path.exists()
    assert not prepared.working_set_persistence.path.exists()
    assert not prepared.note_persistence.path.exists()
    assert not transition_persistence.path.exists()


def test_wrong_transition_rejects_root_persistence_without_write(tmp_path: Path) -> None:
    first_root = tmp_path / "first"
    second_root = tmp_path / "second"
    first_root.mkdir()
    second_root.mkdir()
    fixture, _, prepared, _, loaded_transition = _loaded_transition(first_root, stem="first")
    _, _, _, other_transition_persistence, _ = _loaded_transition(second_root, stem="second")
    root = create_chromium_research_session_working_set_transition_revision_root(
        loaded_transition,
        revised_note_text="First-session revision.",
    )
    destination = first_root / "wrong-transition-root.json"

    with pytest.raises(ValueError):
        persist_chromium_research_session_working_set_transition_revision_root(
            root,
            prior_edge_source=fixture.v6_path,
            working_set_source=prepared.working_set_persistence.path,
            note_source=prepared.note_persistence.path,
            transition_source=other_transition_persistence.path,
            destination=destination,
        )

    assert not destination.exists()


def test_wrong_successor_basis_rejects_root_persistence_without_write(tmp_path: Path) -> None:
    first_root = tmp_path / "first"
    second_root = tmp_path / "second"
    first_root.mkdir()
    second_root.mkdir()
    fixture, _, _, transition_persistence, loaded_transition = _loaded_transition(
        first_root,
        stem="first",
    )
    _, _, other_prepared, _, _ = _loaded_transition(second_root, stem="second")
    root = create_chromium_research_session_working_set_transition_revision_root(
        loaded_transition,
        revised_note_text="First-session revision.",
    )
    destination = first_root / "wrong-basis-root.json"

    with pytest.raises(ValueError):
        persist_chromium_research_session_working_set_transition_revision_root(
            root,
            prior_edge_source=fixture.v6_path,
            working_set_source=other_prepared.working_set_persistence.path,
            note_source=other_prepared.note_persistence.path,
            transition_source=transition_persistence.path,
            destination=destination,
        )

    assert not destination.exists()


def test_root_destination_is_no_overwrite(tmp_path: Path) -> None:
    fixture, _, prepared, transition_persistence, loaded_transition = _loaded_transition(tmp_path)
    root = create_chromium_research_session_working_set_transition_revision_root(
        loaded_transition,
        revised_note_text="A new root revision.",
    )
    destination = tmp_path / "existing-root.json"
    destination.write_text("existing", encoding="utf-8")

    with pytest.raises(FileExistsError):
        persist_chromium_research_session_working_set_transition_revision_root(
            root,
            prior_edge_source=fixture.v6_path,
            working_set_source=prepared.working_set_persistence.path,
            note_source=prepared.note_persistence.path,
            transition_source=transition_persistence.path,
            destination=destination,
        )

    assert destination.read_text(encoding="utf-8") == "existing"


def test_tampered_root_bytes_fail_file_local_verification(tmp_path: Path) -> None:
    *_, persistence = _persist_root(tmp_path)
    document = json.loads(persistence.path.read_text(encoding="utf-8"))
    document["root_record"]["root"]["revision"]["revised_note"]["text"] = "tampered"
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

    with pytest.raises(ChromiumResearchSessionWorkingSetTransitionRevisionRootIntegrityError):
        verify_chromium_research_session_working_set_transition_revision_root(
            persistence.path
        )


def test_root_document_retains_transition_identity_not_duplicated_basis_or_head_state(tmp_path: Path) -> None:
    *_, persistence = _persist_root(tmp_path)
    document = json.loads(persistence.path.read_text(encoding="utf-8"))
    text = persistence.path.read_text(encoding="utf-8")

    assert set(document) == {"format", "root_record", "root_record_sha256"}
    assert set(document["root_record"]) == {"root", "transition_reference"}
    assert set(document["root_record"]["transition_reference"]) == {
        "format",
        "record_sha256",
    }
    assert set(document["root_record"]["root"]) == {"mode", "revision"}
    forbidden = (
        "prior_endpoint_reference",
        "successor_working_set_reference",
        "successor_note_reference",
        "path",
        "timestamp",
        "latest",
        "current_head",
        "canonical_head",
        "semantic_support",
        "chronology",
    )
    assert all(term not in text for term in forbidden)


def test_fresh_load_rejects_a_different_valid_transition(tmp_path: Path) -> None:
    first_root = tmp_path / "first"
    second_root = tmp_path / "second"
    first_root.mkdir()
    second_root.mkdir()
    (
        fixture,
        reentry,
        prepared,
        _,
        _,
        _,
        root_persistence,
    ) = _persist_root(first_root, stem="first")
    _, _, _, other_transition_persistence, _ = _loaded_transition(second_root, stem="second")

    with pytest.raises(ValueError):
        load_chromium_research_session_working_set_transition_revision_root(
            reentry.controller.declared_endpoint,
            prepared.working_set.items,
            prior_edge_source=fixture.v6_path,
            working_set_source=prepared.working_set_persistence.path,
            note_source=prepared.note_persistence.path,
            transition_source=other_transition_persistence.path,
            root_source=root_persistence.path,
        )


def test_loaded_root_survives_later_locator_loss_as_application_evidence(tmp_path: Path) -> None:
    (
        fixture,
        reentry,
        prepared,
        transition_persistence,
        _,
        _,
        persistence,
    ) = _persist_root(tmp_path)
    loaded = load_chromium_research_session_working_set_transition_revision_root(
        reentry.controller.declared_endpoint,
        prepared.working_set.items,
        prior_edge_source=fixture.v6_path,
        working_set_source=prepared.working_set_persistence.path,
        note_source=prepared.note_persistence.path,
        transition_source=transition_persistence.path,
        root_source=persistence.path,
    )
    expected_sha = loaded.verification.root_record_sha256
    expected_text = loaded.root.revision.revised_note.note_text

    fixture.v6_path.unlink()
    prepared.working_set_persistence.path.unlink()
    prepared.note_persistence.path.unlink()
    transition_persistence.path.unlink()
    persistence.path.unlink()

    assert loaded.verification.root_record_sha256 == expected_sha
    assert loaded.root.revision.revised_note.note_text == expected_text
    assert loaded.transition.successor_note.note.note_text


def test_root_revised_note_preserves_exact_changed_working_set_object(tmp_path: Path) -> None:
    _, _, _, _, loaded_transition = _loaded_transition(tmp_path)
    root = create_chromium_research_session_working_set_transition_revision_root(
        loaded_transition,
        revised_note_text="  Unicode revision 😀\nStill exact.  ",
    )

    assert root.revision.prior_note.working_set is loaded_transition.successor_note.note.working_set
    assert root.revision.revised_note.working_set is loaded_transition.successor_note.note.working_set
    assert root.revision.revised_note.note_text == "  Unicode revision 😀\nStill exact.  "


def test_loaded_root_is_not_yet_accepted_as_an_ordinary_edge_predecessor(tmp_path: Path) -> None:
    (
        fixture,
        reentry,
        prepared,
        transition_persistence,
        _,
        _,
        persistence,
    ) = _persist_root(tmp_path)
    loaded = load_chromium_research_session_working_set_transition_revision_root(
        reentry.controller.declared_endpoint,
        prepared.working_set.items,
        prior_edge_source=fixture.v6_path,
        working_set_source=prepared.working_set_persistence.path,
        note_source=prepared.note_persistence.path,
        transition_source=transition_persistence.path,
        root_source=persistence.path,
    )

    with pytest.raises(TypeError, match="23C continuation or 24C revision edge"):
        load_chromium_research_working_set_note_revision_edge(
            loaded,
            tmp_path / "nonexistent-edge.json",
        )


def test_loaded_root_is_not_yet_accepted_as_a_sequence_start(tmp_path: Path) -> None:
    (
        fixture,
        reentry,
        prepared,
        transition_persistence,
        _,
        _,
        persistence,
    ) = _persist_root(tmp_path)
    loaded = load_chromium_research_session_working_set_transition_revision_root(
        reentry.controller.declared_endpoint,
        prepared.working_set.items,
        prior_edge_source=fixture.v6_path,
        working_set_source=prepared.working_set_persistence.path,
        note_source=prepared.note_persistence.path,
        transition_source=transition_persistence.path,
        root_source=persistence.path,
    )

    with pytest.raises(TypeError, match="23C continuation or 24C revision edge"):
        load_chromium_research_working_set_note_revision_edge_sequence(
            loaded,
            (tmp_path / "nonexistent-edge.json",),
        )
