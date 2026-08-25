from __future__ import annotations

from pathlib import Path

import pytest

from pyxis.app.chromium_research_session_controller import ChromiumResearchSessionController
from pyxis.app.chromium_research_session_rollover import (
    rollover_chromium_research_session_to_persisted_successor,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_sequence_declaration_load import (
    load_chromium_research_working_set_note_revision_edge_sequence_declaration,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_sequence_load import (
    ChromiumResearchWorkingSetNoteRevisionEdgeSequenceRelinkError,
    load_chromium_research_working_set_note_revision_edge_sequence,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_sequence_persistence import (
    persist_chromium_research_working_set_note_revision_edge_sequence,
    verify_chromium_research_working_set_note_revision_edge_sequence,
)
from test_app_chromium_research_session_working_set_transition_revision_root_edge import (
    _first_edge,
    _loaded_root,
)


_ROOT_FORMAT = (
    "pyxis.chromium.research_session_working_set_transition_revision_root.v1"
)
_EDGE_FORMAT = "pyxis.chromium.research_working_set_note_revision_edge.v1"


def _root_backed_declared_session(tmp_path: Path, *, stem: str = "35a"):
    (
        fixture,
        reentry,
        prepared,
        transition_persistence,
        root_persistence,
        loaded_root,
        extension,
        edge_persistence,
        _,
    ) = _first_edge(tmp_path, stem=stem)
    sequence = load_chromium_research_working_set_note_revision_edge_sequence(
        loaded_root,
        (edge_persistence.path,),
    )
    declaration = persist_chromium_research_working_set_note_revision_edge_sequence(
        sequence,
        tmp_path / f"{stem}-root-backed-declaration.json",
    )
    loaded_declaration = (
        load_chromium_research_working_set_note_revision_edge_sequence_declaration(
            loaded_root,
            (edge_persistence.path,),
            declaration.path,
        )
    )
    controller = ChromiumResearchSessionController(loaded_declaration)
    return (
        fixture,
        reentry,
        prepared,
        transition_persistence,
        root_persistence,
        loaded_root,
        extension,
        edge_persistence,
        sequence,
        declaration,
        loaded_declaration,
        controller,
    )


def test_35a_explicit_sequence_can_start_at_loaded_34a_root(tmp_path: Path) -> None:
    *_, loaded_root, extension, edge_persistence, _ = _first_edge(tmp_path)

    sequence = load_chromium_research_working_set_note_revision_edge_sequence(
        loaded_root,
        (edge_persistence.path,),
    )

    assert sequence.starting_predecessor is loaded_root
    assert len(sequence.edges) == 1
    edge = sequence.edges[0]
    assert edge.predecessor is loaded_root
    assert edge.verification.edge_record_sha256 == edge_persistence.edge_record_sha256
    assert edge.revision.prior_note is loaded_root.root.revision.revised_note
    assert edge.revision.revised_note.note_text == extension.revision.revised_note.note_text


def test_35a_root_started_sequence_rejects_edge_from_different_root(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    first.mkdir()
    second.mkdir()
    *_, first_edge_persistence, _ = _first_edge(first, stem="first")
    *_, other_loaded_root = _loaded_root(
        second,
        stem="second",
        root_note_text="Different 34A root wording.",
    )

    with pytest.raises(
        ChromiumResearchWorkingSetNoteRevisionEdgeSequenceRelinkError,
        match="member 0",
    ):
        load_chromium_research_working_set_note_revision_edge_sequence(
            other_loaded_root,
            (first_edge_persistence.path,),
        )


def test_35a_sequence_declaration_records_exact_root_start_identity(tmp_path: Path) -> None:
    *_, loaded_root, _, edge_persistence, _ = _first_edge(tmp_path)
    sequence = load_chromium_research_working_set_note_revision_edge_sequence(
        loaded_root,
        (edge_persistence.path,),
    )
    persistence = persist_chromium_research_working_set_note_revision_edge_sequence(
        sequence,
        tmp_path / "root-start-sequence.json",
    )
    verification = verify_chromium_research_working_set_note_revision_edge_sequence(
        persistence.path
    )

    assert verification.starting_predecessor.record_format == _ROOT_FORMAT
    assert (
        verification.starting_predecessor.record_sha256
        == loaded_root.verification.root_record_sha256
    )
    assert len(verification.edges) == 1
    assert verification.edges[0].record_format == _EDGE_FORMAT
    assert verification.edges[0].record_sha256 == edge_persistence.edge_record_sha256


def test_35a_root_backed_declaration_becomes_governed_session_controller(tmp_path: Path) -> None:
    *_, loaded_root, _, edge_persistence, sequence, declaration, loaded, controller = (
        _root_backed_declared_session(tmp_path)
    )

    assert loaded.sequence.starting_predecessor is loaded_root
    assert loaded.sequence.edges[0].predecessor is loaded_root
    assert (
        loaded.verification.starting_predecessor.record_sha256
        == loaded_root.verification.root_record_sha256
    )
    assert loaded.verification.sequence_record_sha256 == declaration.sequence_record_sha256
    assert controller.loaded is loaded
    assert controller.declared_endpoint is loaded.sequence.edges[0]
    assert controller.declared_endpoint.verification.edge_record_sha256 == edge_persistence.edge_record_sha256
    assert controller.presentation.sequence.starting_record_format == _ROOT_FORMAT
    assert controller.presentation.working_set_contexts[0].members
    assert sequence.starting_predecessor is loaded_root


def test_35a_governed_root_backed_session_resumes_ordinary_revision_and_rollover(
    tmp_path: Path,
) -> None:
    (
        *_,
        edge_persistence,
        _,
        _,
        _,
        controller,
    ) = _root_backed_declared_session(tmp_path)

    next_edge_path = tmp_path / "ordinary-after-root-session.json"
    revision = controller.persist_declared_endpoint_revision(
        "Third rationale wording after changed-basis adoption.",
        prior_edge_source=edge_persistence.path,
        destination=next_edge_path,
    )

    assert revision.extension.prior_edge is controller.declared_endpoint
    assert revision.persistence.path == next_edge_path.resolve()
    assert revision.persistence.edge_format == _EDGE_FORMAT

    rollover = rollover_chromium_research_session_to_persisted_successor(
        controller,
        revision,
        successor_edge_source=next_edge_path,
        declaration_destination=tmp_path / "ordinary-continuation-declaration.json",
    )

    assert rollover.prior_controller is controller
    assert rollover.prior_revision is revision
    assert rollover.continuation_controller.declared_endpoint.predecessor is controller.declared_endpoint
    assert (
        rollover.continuation_controller.declared_endpoint.verification.edge_record_sha256
        == revision.persistence.edge_record_sha256
    )
