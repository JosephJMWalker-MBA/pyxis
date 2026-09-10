from __future__ import annotations

from dataclasses import fields
from pathlib import Path

import pytest

from test_app_chromium_research_working_set import (
    _loaded_bare_selection,
    _loaded_records,
)
from test_app_chromium_research_working_set_note_load import (
    _persist_note,
    _persist_note_v2,
)
from pyxis.app.chromium_research_initial_session_controller import (
    ChromiumResearchInitialSessionController,
    ChromiumResearchInitialSessionFirstRevisionPersistenceResult,
)
from pyxis.app.chromium_research_initial_session_presentation import (
    ChromiumPageResearchInitialSessionPresentation,
    present_chromium_research_initial_session,
)
from pyxis.app.chromium_research_working_set_note_load import (
    load_chromium_research_working_set_note,
)
from pyxis.app.chromium_research_working_set_note_revision_persistence import (
    verify_chromium_research_working_set_note_revision,
)


def _loaded_v1_root(tmp_path: Path):
    paragraph_note, exact_note, comparison_note = _loaded_records(tmp_path)
    items = (paragraph_note, exact_note, comparison_note)
    working_set_path, note_path = _persist_note(
        tmp_path,
        items,
        note_text="First human rationale over the note-only basis.",
    )
    loaded = load_chromium_research_working_set_note(
        items,
        working_set_path,
        note_path,
    )
    return loaded, working_set_path, note_path


def _loaded_v2_root(tmp_path: Path):
    paragraph_note, _, _ = _loaded_records(tmp_path)
    bare, bare_path = _loaded_bare_selection(tmp_path)
    items = (bare, paragraph_note, bare)
    working_set_path, note_path = _persist_note_v2(
        tmp_path,
        items,
        note_text="  First human rationale over saved evidence 😀\nStill tentative.  ",
    )
    loaded = load_chromium_research_working_set_note(
        items,
        working_set_path,
        note_path,
    )
    return loaded, working_set_path, note_path, bare_path


def test_51c_v2_bare_root_presents_exact_loaded_evidence_without_fake_history(
    tmp_path: Path,
) -> None:
    loaded, _, _, _ = _loaded_v2_root(tmp_path)

    presentation = present_chromium_research_initial_session(loaded)
    controller = ChromiumResearchInitialSessionController(loaded)

    assert isinstance(presentation, ChromiumPageResearchInitialSessionPresentation)
    assert controller.loaded is loaded
    assert controller.presentation == presentation
    assert presentation.note_format == "pyxis.chromium.research_working_set_note.v2"
    assert presentation.working_set_format == "pyxis.chromium.research_working_set.v2"
    assert presentation.note_record_sha256 == loaded.verification.note_record_sha256
    assert (
        presentation.working_set_record_sha256
        == loaded.verification.working_set_record_sha256
    )
    assert presentation.rationale_text == loaded.note.note_text
    assert tuple(member.member_kind for member in presentation.members) == (
        "exact_range_selection",
        "paragraph_note",
        "exact_range_selection",
    )
    assert presentation.members[0].human_note_text is None
    assert presentation.members[0].excerpts[0].text == (
        loaded.note.working_set.items[0].selection.selected_text
    )
    assert presentation.members[2].human_note_text is None

    names = {field.name for field in fields(presentation)}
    assert names == {
        "presentation_mode",
        "note_format",
        "note_record_sha256",
        "working_set_format",
        "working_set_record_sha256",
        "rationale_text",
        "working_set_mode",
        "members",
    }
    assert not any(
        forbidden in name
        for name in names
        for forbidden in (
            "declaration",
            "edge",
            "position",
            "revision",
            "timestamp",
            "current",
            "latest",
            "head",
            "predecessor",
        )
    )


def test_51c_initial_presentation_requires_no_durable_files_after_root_load(
    tmp_path: Path,
) -> None:
    loaded, working_set_path, note_path, bare_path = _loaded_v2_root(tmp_path)
    member_paths = {
        item.verification.path
        for item in loaded.note.working_set.items
        if hasattr(item.verification, "path")
    }

    for path in (*member_paths, working_set_path, note_path, bare_path):
        path.unlink(missing_ok=True)

    presentation = present_chromium_research_initial_session(loaded)
    controller = ChromiumResearchInitialSessionController(loaded)

    assert controller.loaded is loaded
    assert controller.presentation == presentation
    assert presentation.rationale_text == loaded.note.note_text
    assert presentation.members[0].excerpts[0].text


def test_51c_v2_first_genuine_revision_uses_unchanged_revision_v2_and_keeps_root(
    tmp_path: Path,
) -> None:
    loaded, working_set_path, note_path, _ = _loaded_v2_root(tmp_path)
    controller = ChromiumResearchInitialSessionController(loaded)
    prior_presentation = controller.presentation
    destination = tmp_path / "first-revision-v2.json"

    result = controller.persist_first_revision(
        "Second genuine human rationale after rereading the evidence.",
        working_set_source=working_set_path,
        prior_note_source=note_path,
        destination=destination,
    )
    verified = verify_chromium_research_working_set_note_revision(destination)

    assert isinstance(
        result,
        ChromiumResearchInitialSessionFirstRevisionPersistenceResult,
    )
    assert result.prior_session is prior_presentation
    assert result.revision.prior_note is loaded.note
    assert result.revision.revised_note.working_set is loaded.note.working_set
    assert result.persistence.revision is result.revision
    assert result.persistence.revision_format == (
        "pyxis.chromium.research_working_set_note_revision.v2"
    )
    assert verified.revision_format == result.persistence.revision_format
    assert verified.prior_note_record_sha256 == loaded.verification.note_record_sha256
    assert controller.presentation is prior_presentation
    assert controller.loaded is loaded
    assert controller.last_revision is result


def test_51c_v1_first_genuine_revision_uses_frozen_revision_v1(
    tmp_path: Path,
) -> None:
    loaded, working_set_path, note_path = _loaded_v1_root(tmp_path)
    controller = ChromiumResearchInitialSessionController(loaded)
    destination = tmp_path / "first-revision-v1.json"

    result = controller.persist_first_revision(
        "A real second wording over the same note-only basis.",
        working_set_source=working_set_path,
        prior_note_source=note_path,
        destination=destination,
    )
    verified = verify_chromium_research_working_set_note_revision(destination)

    assert result.revision.prior_note is loaded.note
    assert result.persistence.revision_format == (
        "pyxis.chromium.research_working_set_note_revision.v1"
    )
    assert verified.revision_format == result.persistence.revision_format
    assert controller.presentation.note_format == (
        "pyxis.chromium.research_working_set_note.v1"
    )


def test_51c_exact_same_wording_is_not_a_first_revision(
    tmp_path: Path,
) -> None:
    loaded, working_set_path, note_path, _ = _loaded_v2_root(tmp_path)
    controller = ChromiumResearchInitialSessionController(loaded)
    destination = tmp_path / "must-not-exist.json"

    with pytest.raises(ValueError, match="must differ exactly"):
        controller.persist_first_revision(
            loaded.note.note_text,
            working_set_source=working_set_path,
            prior_note_source=note_path,
            destination=destination,
        )

    assert not destination.exists()
    assert controller.last_revision is None


def test_51c_wrong_valid_predecessor_note_fails_before_destination_mutation(
    tmp_path: Path,
) -> None:
    loaded, _, _, _ = _loaded_v2_root(tmp_path)
    controller = ChromiumResearchInitialSessionController(loaded)
    items = loaded.note.working_set.items

    wrong_root = tmp_path / "wrong-root"
    wrong_root.mkdir()
    wrong_working_set_path, wrong_note_path = _persist_note_v2(
        wrong_root,
        items,
        note_text="Different but individually valid predecessor rationale.",
    )
    destination = tmp_path / "wrong-predecessor-output.json"

    with pytest.raises(ValueError, match="durable predecessor note text"):
        controller.persist_first_revision(
            "A genuine revision of the mounted root.",
            working_set_source=wrong_working_set_path,
            prior_note_source=wrong_note_path,
            destination=destination,
        )

    assert not destination.exists()
    assert controller.last_revision is None


def test_51c_existing_destination_is_preserved_on_failure(
    tmp_path: Path,
) -> None:
    loaded, working_set_path, note_path, _ = _loaded_v2_root(tmp_path)
    controller = ChromiumResearchInitialSessionController(loaded)
    destination = tmp_path / "existing.json"
    sentinel = b"do not replace\n"
    destination.write_bytes(sentinel)

    with pytest.raises(FileExistsError):
        controller.persist_first_revision(
            "A genuine new human rationale.",
            working_set_source=working_set_path,
            prior_note_source=note_path,
            destination=destination,
        )

    assert destination.read_bytes() == sentinel
    assert controller.last_revision is None
