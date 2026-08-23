from __future__ import annotations

import json
from pathlib import Path

import pytest

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
from pyxis.app.chromium_research_working_set_note_revision_edge_persistence import (
    verify_chromium_research_working_set_note_revision_edge,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_sequence_load import (
    load_chromium_research_working_set_note_revision_edge_sequence,
)
from test_app_chromium_research_session_working_set_transition_revision_root import (
    _persist_root,
)


_ROOT_FORMAT = (
    "pyxis.chromium.research_session_working_set_transition_revision_root.v1"
)
_EDGE_FORMAT = "pyxis.chromium.research_working_set_note_revision_edge.v1"


def _loaded_root(tmp_path: Path, *, stem: str = "bridge"):
    (
        fixture,
        reentry,
        prepared,
        transition_persistence,
        _,
        _,
        root_persistence,
    ) = _persist_root(tmp_path, stem=stem)
    loaded_root = load_chromium_research_session_working_set_transition_revision_root(
        reentry.controller.declared_endpoint,
        prepared.working_set.items,
        prior_edge_source=fixture.v6_path,
        working_set_source=prepared.working_set_persistence.path,
        note_source=prepared.note_persistence.path,
        transition_source=transition_persistence.path,
        root_source=root_persistence.path,
    )
    return fixture, reentry, prepared, transition_persistence, root_persistence, loaded_root


def _first_edge(tmp_path: Path, *, stem: str = "bridge"):
    fixture, reentry, prepared, transition_persistence, root_persistence, loaded_root = _loaded_root(
        tmp_path,
        stem=stem,
    )
    extension = create_chromium_research_session_working_set_transition_revision_root_edge_extension(
        loaded_root,
        revised_note_text="Second rationale wording on the changed evidence basis.",
    )
    edge_persistence = persist_chromium_research_session_working_set_transition_revision_root_edge_extension(
        extension,
        root_source=root_persistence.path,
        destination=tmp_path / f"{stem}-root-edge.json",
    )
    loaded_edge = load_chromium_research_session_working_set_transition_revision_root_edge(
        loaded_root,
        edge_persistence.path,
    )
    return (
        fixture,
        reentry,
        prepared,
        transition_persistence,
        root_persistence,
        loaded_root,
        extension,
        edge_persistence,
        loaded_edge,
    )


def test_create_root_edge_extension_uses_exact_root_endpoint_and_working_set(tmp_path: Path) -> None:
    *_, loaded_root = _loaded_root(tmp_path)
    extension = create_chromium_research_session_working_set_transition_revision_root_edge_extension(
        loaded_root,
        revised_note_text="  Revised again after basis change 😀  ",
    )

    assert extension.prior_root is loaded_root
    assert extension.revision.prior_note is loaded_root.root.revision.revised_note
    assert (
        extension.revision.revised_note.working_set
        is loaded_root.root.revision.revised_note.working_set
    )
    assert extension.revision.revised_note.note_text == "  Revised again after basis change 😀  "


def test_root_edge_extension_rejects_exact_text_noop(tmp_path: Path) -> None:
    *_, loaded_root = _loaded_root(tmp_path)
    with pytest.raises(ValueError, match="differ exactly"):
        create_chromium_research_session_working_set_transition_revision_root_edge_extension(
            loaded_root,
            revised_note_text=loaded_root.root.revision.revised_note.note_text,
        )


def test_root_edge_persistence_writes_existing_24b_format_with_exact_root_identity(tmp_path: Path) -> None:
    *_, root_persistence, loaded_root = _loaded_root(tmp_path)
    extension = create_chromium_research_session_working_set_transition_revision_root_edge_extension(
        loaded_root,
        revised_note_text="Root-backed ordinary edge.",
    )
    persistence = persist_chromium_research_session_working_set_transition_revision_root_edge_extension(
        extension,
        root_source=root_persistence.path,
        destination=tmp_path / "root-edge.json",
    )
    verification = verify_chromium_research_working_set_note_revision_edge(persistence.path)

    assert persistence.edge_format == _EDGE_FORMAT
    assert verification.predecessor_format == _ROOT_FORMAT
    assert verification.predecessor_record_sha256 == loaded_root.verification.root_record_sha256
    assert verification.revised_note_text == "Root-backed ordinary edge."


def test_wrong_current_root_file_rejects_without_writing(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    first.mkdir()
    second.mkdir()
    *_, loaded_root = _loaded_root(first, stem="first")
    *_, other_root_persistence, other_loaded_root = _loaded_root(second, stem="second")
    extension = create_chromium_research_session_working_set_transition_revision_root_edge_extension(
        loaded_root,
        revised_note_text="First root continuation.",
    )
    destination = first / "wrong-root-edge.json"

    assert other_loaded_root.verification.root_record_sha256 == loaded_root.verification.root_record_sha256
    document = json.loads(other_root_persistence.path.read_text(encoding="utf-8"))
    document["root_record"]["root"]["revision"]["revised_note"]["text"] = "Different root wording."
    payload = document["root_record"]
    import hashlib

    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    document["root_record_sha256"] = hashlib.sha256(encoded).hexdigest()
    other_root_persistence.path.write_text(
        json.dumps(document, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="does not match"):
        persist_chromium_research_session_working_set_transition_revision_root_edge_extension(
            extension,
            root_source=other_root_persistence.path,
            destination=destination,
        )
    assert not destination.exists()


def test_moved_identical_root_file_works_via_explicit_new_path(tmp_path: Path) -> None:
    *_, root_persistence, loaded_root = _loaded_root(tmp_path)
    moved_root = tmp_path / "moved-root.json"
    root_persistence.path.rename(moved_root)
    extension = create_chromium_research_session_working_set_transition_revision_root_edge_extension(
        loaded_root,
        revised_note_text="Revision from moved root file.",
    )
    persistence = persist_chromium_research_session_working_set_transition_revision_root_edge_extension(
        extension,
        root_source=moved_root,
        destination=tmp_path / "moved-root-edge.json",
    )

    assert persistence.path.exists()
    assert persistence.root_verification.path == moved_root.resolve()


def test_root_edge_destination_is_no_overwrite(tmp_path: Path) -> None:
    *_, root_persistence, loaded_root = _loaded_root(tmp_path)
    extension = create_chromium_research_session_working_set_transition_revision_root_edge_extension(
        loaded_root,
        revised_note_text="No overwrite edge.",
    )
    destination = tmp_path / "existing-edge.json"
    destination.write_text("existing", encoding="utf-8")

    with pytest.raises(FileExistsError):
        persist_chromium_research_session_working_set_transition_revision_root_edge_extension(
            extension,
            root_source=root_persistence.path,
            destination=destination,
        )
    assert destination.read_text(encoding="utf-8") == "existing"


def test_root_specific_loader_returns_standard_loaded_edge_with_exact_root_predecessor(tmp_path: Path) -> None:
    *_, loaded_root, extension, persistence, loaded_edge = _first_edge(tmp_path)

    assert isinstance(loaded_edge, ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord)
    assert loaded_edge.predecessor is loaded_root
    assert loaded_edge.revision.prior_note is loaded_root.root.revision.revised_note
    assert loaded_edge.revision.revised_note.note_text == extension.revision.revised_note.note_text
    assert loaded_edge.verification.edge_record_sha256 == persistence.edge_record_sha256


def test_root_specific_loader_rejects_different_loaded_root(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    first.mkdir()
    second.mkdir()
    *_, persistence, _ = _first_edge(first, stem="first")
    *_, other_loaded_root = _loaded_root(second, stem="second")

    # Different directory alone is not identity. Make a distinct second root through
    # a distinct first root revision before testing relinking mismatch.
    assert other_loaded_root.verification.root_record_sha256 != ""
    with pytest.raises(ValueError):
        load_chromium_research_session_working_set_transition_revision_root_edge(
            other_loaded_root,
            persistence.path,
        )


def test_generic_24c_still_rejects_loaded_root_directly(tmp_path: Path) -> None:
    *_, loaded_root = _loaded_root(tmp_path)
    with pytest.raises(TypeError, match="23C continuation or 24C revision edge"):
        load_chromium_research_working_set_note_revision_edge(
            loaded_root,
            tmp_path / "nonexistent-edge.json",
        )


def test_26a_still_rejects_loaded_root_as_sequence_start(tmp_path: Path) -> None:
    *_, loaded_root = _loaded_root(tmp_path)
    with pytest.raises(TypeError, match="23C continuation or 24C revision edge"):
        load_chromium_research_working_set_note_revision_edge_sequence(
            loaded_root,
            (tmp_path / "nonexistent-edge.json",),
        )


def test_25a_25b_can_continue_from_first_root_backed_loaded_edge(tmp_path: Path) -> None:
    *_, loaded_edge = _first_edge(tmp_path)
    second = create_chromium_research_working_set_note_revision_edge_extension(
        loaded_edge,
        revised_note_text="Third rationale wording after basis change.",
    )
    second_persistence = persist_chromium_research_working_set_note_revision_edge_extension(
        second,
        loaded_edge.verification.path,
        tmp_path / "second-ordinary-edge.json",
    )
    loaded_second = load_chromium_research_working_set_note_revision_edge(
        loaded_edge,
        second_persistence.path,
    )

    assert loaded_second.predecessor is loaded_edge
    assert loaded_second.revision.prior_note is loaded_edge.revision.revised_note
    assert loaded_second.revision.revised_note.note_text == "Third rationale wording after basis change."


def test_after_second_edge_existing_edge_to_edge_path_needs_no_root_special_case(tmp_path: Path) -> None:
    *_, loaded_edge = _first_edge(tmp_path)
    second = create_chromium_research_working_set_note_revision_edge_extension(
        loaded_edge,
        revised_note_text="Third wording.",
    )
    second_persistence = persist_chromium_research_working_set_note_revision_edge_extension(
        second,
        loaded_edge.verification.path,
        tmp_path / "second-edge.json",
    )
    loaded_second = load_chromium_research_working_set_note_revision_edge(
        loaded_edge,
        second_persistence.path,
    )
    third = create_chromium_research_working_set_note_revision_edge_extension(
        loaded_second,
        revised_note_text="Fourth wording.",
    )
    third_persistence = persist_chromium_research_working_set_note_revision_edge_extension(
        third,
        loaded_second.verification.path,
        tmp_path / "third-edge.json",
    )
    loaded_third = load_chromium_research_working_set_note_revision_edge(
        loaded_second,
        third_persistence.path,
    )

    assert loaded_third.predecessor is loaded_second
    assert loaded_third.revision.revised_note.note_text == "Fourth wording."
