from __future__ import annotations

from dataclasses import fields, replace
import importlib
from pathlib import Path

import pytest

from pyxis.app.chromium_research_session_controller import (
    ChromiumResearchSessionController,
    ChromiumResearchSessionEndpointRevisionPersistenceResult,
)
from pyxis.app.chromium_research_session_rollover import (
    ChromiumResearchSessionRolloverResult,
    rollover_chromium_research_session_to_persisted_successor,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_sequence_persistence import (
    verify_chromium_research_working_set_note_revision_edge_sequence,
)
from test_app_chromium_research_session_controller import _session


def _written_successor(tmp_path: Path, *, text: str = "v7 chosen continuation"):
    tmp_path.mkdir(parents=True, exist_ok=True)
    _, _, _, v6_path, old_declaration, loaded = _session(tmp_path)
    controller = ChromiumResearchSessionController(loaded)
    successor = tmp_path / "v7.json"
    revision = controller.persist_declared_endpoint_revision(
        text,
        prior_edge_source=v6_path,
        destination=successor,
    )
    return controller, revision, successor, v6_path, old_declaration


def test_rollover_creates_new_one_edge_declared_session_from_exact_successor(
    tmp_path: Path,
) -> None:
    controller, revision, successor, _, _ = _written_successor(tmp_path)
    declaration = tmp_path / "continuation-sequence.json"

    result = rollover_chromium_research_session_to_persisted_successor(
        controller,
        revision,
        successor_edge_source=successor,
        declaration_destination=declaration,
    )

    assert isinstance(result, ChromiumResearchSessionRolloverResult)
    assert result.prior_controller is controller
    assert result.prior_revision is revision
    assert result.explicit_sequence.starting_predecessor is controller.declared_endpoint
    assert len(result.explicit_sequence.edges) == 1
    assert result.explicit_sequence.edges[0].predecessor is controller.declared_endpoint
    assert (
        result.explicit_sequence.edges[0].verification.edge_record_sha256
        == revision.persistence.edge_record_sha256
    )
    assert result.declaration.path == declaration.resolve()
    assert result.loaded_declaration.sequence.starting_predecessor is controller.declared_endpoint
    assert len(result.loaded_declaration.sequence.edges) == 1
    assert (
        result.continuation_controller.declared_endpoint
        is result.loaded_declaration.sequence.edges[0]
    )
    assert result.continuation_controller.presentation.sequence.members[0].note_text == (
        revision.extension.revision.revised_note.note_text
    )


def test_rollover_uses_explicit_revision_selection_not_controller_last_write(
    tmp_path: Path,
) -> None:
    _, _, _, v6_path, _, loaded = _session(tmp_path)
    controller = ChromiumResearchSessionController(loaded)
    first_path = tmp_path / "v7-first.json"
    second_path = tmp_path / "v7-second.json"
    first = controller.persist_declared_endpoint_revision(
        "first sibling explicitly selected",
        prior_edge_source=v6_path,
        destination=first_path,
    )
    second = controller.persist_declared_endpoint_revision(
        "second sibling retained as controller last",
        prior_edge_source=v6_path,
        destination=second_path,
    )
    assert controller.last_endpoint_revision is second

    result = rollover_chromium_research_session_to_persisted_successor(
        controller,
        first,
        successor_edge_source=first_path,
        declaration_destination=tmp_path / "first-selected-declaration.json",
    )

    assert result.prior_revision is first
    assert result.prior_revision is not controller.last_endpoint_revision
    assert result.continuation_controller.declared_endpoint.revision.revised_note.note_text == (
        "first sibling explicitly selected"
    )


def test_selected_revision_and_explicit_successor_identity_must_match(
    tmp_path: Path,
) -> None:
    _, _, _, v6_path, _, loaded = _session(tmp_path)
    controller = ChromiumResearchSessionController(loaded)
    first_path = tmp_path / "v7-a.json"
    second_path = tmp_path / "v7-b.json"
    first = controller.persist_declared_endpoint_revision(
        "sibling A",
        prior_edge_source=v6_path,
        destination=first_path,
    )
    controller.persist_declared_endpoint_revision(
        "sibling B",
        prior_edge_source=v6_path,
        destination=second_path,
    )
    declaration = tmp_path / "wrong-sibling-declaration.json"

    with pytest.raises(ValueError, match="identity does not match"):
        rollover_chromium_research_session_to_persisted_successor(
            controller,
            first,
            successor_edge_source=second_path,
            declaration_destination=declaration,
        )

    assert not declaration.exists()


def test_moved_successor_file_remains_location_not_identity(tmp_path: Path) -> None:
    controller, revision, successor, _, _ = _written_successor(tmp_path)
    moved = tmp_path / "moved" / "renamed-successor.edge"
    moved.parent.mkdir()
    moved.write_bytes(successor.read_bytes())
    successor.unlink()

    result = rollover_chromium_research_session_to_persisted_successor(
        controller,
        revision,
        successor_edge_source=moved,
        declaration_destination=tmp_path / "moved-successor-declaration.json",
    )

    assert result.prior_revision.persistence.path != moved.resolve()
    assert (
        result.continuation_controller.declared_endpoint.verification.edge_record_sha256
        == revision.persistence.edge_record_sha256
    )


def test_declaration_destination_is_no_overwrite(tmp_path: Path) -> None:
    controller, revision, successor, _, _ = _written_successor(tmp_path)
    occupied = tmp_path / "occupied-declaration.json"
    occupied.write_text("do not overwrite", encoding="utf-8")

    with pytest.raises(FileExistsError):
        rollover_chromium_research_session_to_persisted_successor(
            controller,
            revision,
            successor_edge_source=successor,
            declaration_destination=occupied,
        )

    assert occupied.read_text(encoding="utf-8") == "do not overwrite"
    assert controller.last_endpoint_revision is revision


def test_rollover_leaves_prior_controller_and_prior_declaration_unchanged(
    tmp_path: Path,
) -> None:
    controller, revision, successor, _, old_declaration = _written_successor(tmp_path)
    old_loaded = controller.loaded
    old_presentation = controller.presentation
    old_endpoint = controller.declared_endpoint
    old_bytes = old_declaration.read_bytes()

    result = rollover_chromium_research_session_to_persisted_successor(
        controller,
        revision,
        successor_edge_source=successor,
        declaration_destination=tmp_path / "new-declaration.json",
    )

    assert controller.loaded is old_loaded
    assert controller.presentation is old_presentation
    assert controller.declared_endpoint is old_endpoint
    assert controller.last_endpoint_revision is revision
    assert old_declaration.read_bytes() == old_bytes
    assert result.continuation_controller is not controller
    assert result.loaded_declaration is not old_loaded


def test_old_declaration_and_prior_edge_files_may_disappear_before_rollover(
    tmp_path: Path,
) -> None:
    _, v4_path, v5_path, v6_path, old_declaration, loaded = _session(tmp_path)
    controller = ChromiumResearchSessionController(loaded)
    successor = tmp_path / "v7-after-cleanup.json"
    revision = controller.persist_declared_endpoint_revision(
        "continue after prior durable cleanup",
        prior_edge_source=v6_path,
        destination=successor,
    )

    for path in (v4_path, v5_path, v6_path, old_declaration):
        path.unlink(missing_ok=True)

    result = rollover_chromium_research_session_to_persisted_successor(
        controller,
        revision,
        successor_edge_source=successor,
        declaration_destination=tmp_path / "continuation-after-cleanup.json",
    )

    assert result.continuation_controller.declared_endpoint.revision.revised_note.note_text == (
        "continue after prior durable cleanup"
    )
    assert not old_declaration.exists()
    assert not v6_path.exists()


def test_continuation_controller_can_write_next_explicit_successor(tmp_path: Path) -> None:
    controller, revision, successor, _, _ = _written_successor(tmp_path)
    rollover = rollover_chromium_research_session_to_persisted_successor(
        controller,
        revision,
        successor_edge_source=successor,
        declaration_destination=tmp_path / "v7-declaration.json",
    )
    continuation = rollover.continuation_controller
    assert continuation.last_endpoint_revision is None

    v8 = continuation.persist_declared_endpoint_revision(
        "v8 explicit continuation",
        prior_edge_source=successor,
        destination=tmp_path / "v8.json",
    )

    assert v8.extension.prior_edge is continuation.declared_endpoint
    assert v8.extension.revision.revised_note.note_text == "v8 explicit continuation"


def test_cross_controller_or_forged_revision_rejects_before_declaration(tmp_path: Path) -> None:
    controller, revision, successor, _, _ = _written_successor(tmp_path / "a")
    other_controller, _, _, _, _ = _written_successor(tmp_path / "b", text="other")

    with pytest.raises(ValueError, match="does not belong"):
        rollover_chromium_research_session_to_persisted_successor(
            other_controller,
            revision,
            successor_edge_source=successor,
            declaration_destination=tmp_path / "cross-controller.json",
        )

    forged = replace(
        revision,
        persistence=replace(
            revision.persistence,
            edge_record_sha256="0" * 64,
        ),
    )
    forged_destination = tmp_path / "forged.json"
    with pytest.raises(ValueError, match="identity does not match"):
        rollover_chromium_research_session_to_persisted_successor(
            controller,
            forged,
            successor_edge_source=successor,
            declaration_destination=forged_destination,
        )
    assert not forged_destination.exists()


def test_new_declaration_records_old_endpoint_then_exact_chosen_successor(
    tmp_path: Path,
) -> None:
    controller, revision, successor, _, _ = _written_successor(tmp_path)
    destination = tmp_path / "identity-declaration.json"
    result = rollover_chromium_research_session_to_persisted_successor(
        controller,
        revision,
        successor_edge_source=successor,
        declaration_destination=destination,
    )

    verified = verify_chromium_research_working_set_note_revision_edge_sequence(destination)
    assert verified.starting_predecessor.record_format == (
        controller.declared_endpoint.verification.edge_format
    )
    assert verified.starting_predecessor.record_sha256 == (
        controller.declared_endpoint.verification.edge_record_sha256
    )
    assert len(verified.edges) == 1
    assert verified.edges[0].record_sha256 == revision.persistence.edge_record_sha256
    assert result.loaded_declaration.verification.sequence_record_sha256 == (
        verified.sequence_record_sha256
    )


def test_rollover_surface_adds_no_global_head_authority_and_module_is_explicit(
    tmp_path: Path,
) -> None:
    controller, revision, successor, _, _ = _written_successor(tmp_path)
    result = rollover_chromium_research_session_to_persisted_successor(
        controller,
        revision,
        successor_edge_source=successor,
        declaration_destination=tmp_path / "bounded-authority.json",
    )

    names = {field.name for field in fields(ChromiumResearchSessionRolloverResult)}
    assert names == {
        "prior_controller",
        "prior_revision",
        "explicit_sequence",
        "declaration",
        "loaded_declaration",
        "continuation_controller",
    }
    assert names.isdisjoint(
        {"latest", "current", "head", "canonical_head", "complete_history", "truth"}
    )
    assert isinstance(result.prior_revision, ChromiumResearchSessionEndpointRevisionPersistenceResult)

    module = importlib.import_module("pyxis.app.chromium_research_session_rollover")
    assert hasattr(module, "ChromiumResearchSessionRolloverResult")
    assert hasattr(module, "rollover_chromium_research_session_to_persisted_successor")
