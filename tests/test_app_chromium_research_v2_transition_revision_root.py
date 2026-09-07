from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path

import pytest

from pyxis.app.chromium_research_session_working_set_transition_load import (
    load_chromium_research_session_working_set_transition,
)
from pyxis.app.chromium_research_session_working_set_transition_persistence import (
    persist_chromium_research_session_working_set_transition,
)
from pyxis.app.chromium_research_session_working_set_transition_revision_root import (
    ChromiumResearchSessionWorkingSetTransitionRevisionRootError,
    create_chromium_research_session_working_set_transition_revision_root,
)
from pyxis.app.chromium_research_session_working_set_transition_revision_root_edge_extension import (
    create_chromium_research_session_working_set_transition_revision_root_edge_extension,
)
from pyxis.app.chromium_research_session_working_set_transition_revision_root_edge_extension_persistence import (
    persist_chromium_research_session_working_set_transition_revision_root_edge_extension,
)
from pyxis.app.chromium_research_session_working_set_transition_revision_root_edge_load import (
    load_chromium_research_session_working_set_transition_revision_root_edge,
)
from pyxis.app.chromium_research_session_working_set_transition_revision_root_load import (
    load_chromium_research_session_working_set_transition_revision_root,
)
from pyxis.app.chromium_research_session_working_set_transition_revision_root_persistence import (
    persist_chromium_research_session_working_set_transition_revision_root,
    verify_chromium_research_session_working_set_transition_revision_root,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_extension import (
    create_chromium_research_working_set_note_revision_edge_extension,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_extension_persistence import (
    persist_chromium_research_working_set_note_revision_edge_extension,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord,
    load_chromium_research_working_set_note_revision_edge,
)
from test_app_chromium_research_session_working_set_transition import (
    _prepared_v2_transition,
)


_ROOT_FORMAT = (
    "pyxis.chromium.research_session_working_set_transition_revision_root.v1"
)
_TRANSITION_FORMAT = "pyxis.chromium.research_session_working_set_transition.v1"
_EDGE_FORMAT = "pyxis.chromium.research_working_set_note_revision_edge.v1"


def _v2_root(tmp_path: Path):
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

    transition_path = tmp_path / "50d-transition-v1.json"
    transition_persistence = persist_chromium_research_session_working_set_transition(
        transition,
        prior_edge_source=prior_edge_path,
        working_set_source=prepared.working_set_persistence.path,
        note_source=prepared.note_persistence.path,
        destination=transition_path,
    )
    loaded_transition = load_chromium_research_session_working_set_transition(
        controller.declared_endpoint,
        prepared.working_set.items,
        prior_edge_source=prior_edge_path,
        working_set_source=prepared.working_set_persistence.path,
        note_source=prepared.note_persistence.path,
        transition_source=transition_path,
    )

    root = create_chromium_research_session_working_set_transition_revision_root(
        loaded_transition,
        revised_note_text="First exact human revision after the v2-backed basis change.",
    )
    root_path = tmp_path / "50d-root-v1.json"
    root_persistence = persist_chromium_research_session_working_set_transition_revision_root(
        root,
        prior_edge_source=prior_edge_path,
        working_set_source=prepared.working_set_persistence.path,
        note_source=prepared.note_persistence.path,
        transition_source=transition_path,
        destination=root_path,
    )
    loaded_root = load_chromium_research_session_working_set_transition_revision_root(
        controller.declared_endpoint,
        prepared.working_set.items,
        prior_edge_source=prior_edge_path,
        working_set_source=prepared.working_set_persistence.path,
        note_source=prepared.note_persistence.path,
        transition_source=transition_path,
        root_source=root_path,
    )
    return (
        paragraph_note,
        bare,
        new_member,
        controller,
        prior_edge_path,
        prepared,
        transition_persistence,
        loaded_transition,
        root_persistence,
        loaded_root,
    )


def test_50d_v2_backed_transition_roots_through_existing_root_v1(
    tmp_path: Path,
) -> None:
    (
        paragraph_note,
        bare,
        new_member,
        _,
        _,
        prepared,
        transition_persistence,
        loaded_transition,
        root_persistence,
        loaded_root,
    ) = _v2_root(tmp_path)

    root = loaded_root.root
    verification = verify_chromium_research_session_working_set_transition_revision_root(
        root_persistence.path
    )

    assert loaded_transition.verification.transition_format == _TRANSITION_FORMAT
    assert loaded_transition.successor_note.working_set.verification.working_set_format == (
        "pyxis.chromium.research_working_set.v2"
    )
    assert loaded_transition.successor_note.verification.note_format == (
        "pyxis.chromium.research_working_set_note.v2"
    )
    assert root_persistence.root_format == _ROOT_FORMAT
    assert verification.root_format == _ROOT_FORMAT
    assert verification.transition_format == _TRANSITION_FORMAT
    assert verification.transition_record_sha256 == (
        transition_persistence.transition_record_sha256
    )
    assert root.transition is loaded_root.transition
    assert root.revision.prior_note is loaded_root.transition.successor_note.note
    assert root.revision.revised_note.working_set is (
        loaded_root.transition.successor_note.note.working_set
    )
    assert all(
        observed is expected
        for observed, expected in zip(
            root.revision.revised_note.working_set.items,
            prepared.working_set.items,
        )
    )
    assert any(item is bare for item in root.revision.revised_note.working_set.items)
    assert root.revision.revised_note.working_set.items[-1] is new_member

    document = json.loads(root_persistence.path.read_text(encoding="utf-8"))
    text = root_persistence.path.read_text(encoding="utf-8")
    assert set(document["root_record"]) == {"root", "transition_reference"}
    assert set(document["root_record"]["transition_reference"]) == {
        "format",
        "record_sha256",
    }
    assert document["root_record"]["transition_reference"]["format"] == _TRANSITION_FORMAT
    assert "pyxis.chromium.research_working_set.v2" not in text
    assert "pyxis.chromium.research_working_set_note.v2" not in text
    assert bare.selection.selected_text not in text
    assert prepared.note.note_text not in text

    assert not bare.verification.path.exists()
    assert not paragraph_note.verification.path.exists()
    assert not new_member.verification.path.exists()


def test_50d_root_creation_rejects_hand_forged_cross_version_loaded_transition(
    tmp_path: Path,
) -> None:
    *_, loaded_transition, _, _ = _v2_root(tmp_path)
    forged_note_verification = replace(
        loaded_transition.successor_note.verification,
        note_format="pyxis.chromium.research_working_set_note.v1",
    )
    forged_successor = replace(
        loaded_transition.successor_note,
        verification=forged_note_verification,
    )
    forged_transition = replace(
        loaded_transition,
        successor_note=forged_successor,
    )

    with pytest.raises(
        ChromiumResearchSessionWorkingSetTransitionRevisionRootError,
        match="working-set/note format pair is unsupported",
    ):
        create_chromium_research_session_working_set_transition_revision_root(
            forged_transition,
            revised_note_text="This forged pair must not root.",
        )


def test_50d_unchanged_34b_rejoins_existing_edge_v1_and_25a_25b_lineage(
    tmp_path: Path,
) -> None:
    *_, loaded_root = _v2_root(tmp_path)

    root_extension = (
        create_chromium_research_session_working_set_transition_revision_root_edge_extension(
            loaded_root,
            revised_note_text="Second wording after the v2-backed basis change.",
        )
    )
    first_edge_path = tmp_path / "50d-first-root-backed-edge.json"
    first_persistence = (
        persist_chromium_research_session_working_set_transition_revision_root_edge_extension(
            root_extension,
            root_source=loaded_root.verification.path,
            destination=first_edge_path,
        )
    )
    first_loaded = load_chromium_research_session_working_set_transition_revision_root_edge(
        loaded_root,
        first_edge_path,
    )

    assert isinstance(first_loaded, ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord)
    assert first_persistence.edge_format == _EDGE_FORMAT
    assert first_loaded.verification.edge_format == _EDGE_FORMAT
    assert first_loaded.predecessor is loaded_root
    assert first_loaded.revision.prior_note is loaded_root.root.revision.revised_note
    assert first_loaded.revision.revised_note.working_set is (
        loaded_root.root.revision.revised_note.working_set
    )

    second = create_chromium_research_working_set_note_revision_edge_extension(
        first_loaded,
        revised_note_text="Third ordinary wording after rejoining edge v1.",
    )
    second_path = tmp_path / "50d-second-ordinary-edge.json"
    persist_chromium_research_working_set_note_revision_edge_extension(
        second,
        first_edge_path,
        second_path,
    )
    second_loaded = load_chromium_research_working_set_note_revision_edge(
        first_loaded,
        second_path,
    )

    assert second_loaded.predecessor is first_loaded
    assert second_loaded.verification.edge_format == _EDGE_FORMAT
    assert second_loaded.revision.prior_note is first_loaded.revision.revised_note
    assert second_loaded.revision.revised_note.working_set is (
        first_loaded.revision.revised_note.working_set
    )
    assert second_loaded.revision.revised_note.note_text == (
        "Third ordinary wording after rejoining edge v1."
    )


def test_50d_generic_24c_still_rejects_root_directly(tmp_path: Path) -> None:
    *_, loaded_root = _v2_root(tmp_path)

    with pytest.raises(TypeError, match="23C continuation or 24C revision edge"):
        load_chromium_research_working_set_note_revision_edge(
            loaded_root,
            tmp_path / "nonexistent-edge.json",
        )
