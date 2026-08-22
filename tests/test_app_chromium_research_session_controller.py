from __future__ import annotations

from dataclasses import fields, replace
import importlib
from pathlib import Path

import pytest

from pyxis.app.chromium_research_session_controller import (
    ChromiumResearchSessionController,
    ChromiumResearchSessionEndpointRevisionPersistenceResult,
)
from pyxis.app.chromium_research_session_presentation import (
    present_chromium_research_session,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_load import (
    load_chromium_research_working_set_note_revision_edge,
)
from test_app_chromium_research_session_presentation import _loaded


def _session(tmp_path: Path):
    return _loaded(tmp_path)


def test_controller_retains_exact_loaded_evidence_and_complete_presentation(
    tmp_path: Path,
) -> None:
    _, _, _, _, _, loaded = _session(tmp_path)

    controller = ChromiumResearchSessionController(loaded)

    assert controller.loaded is loaded
    assert controller.presentation == present_chromium_research_session(loaded)
    assert controller.last_endpoint_revision is None


def test_declared_endpoint_is_exact_final_edge_not_global_head(tmp_path: Path) -> None:
    _, _, _, _, _, loaded = _session(tmp_path)
    controller = ChromiumResearchSessionController(loaded)

    assert controller.declared_endpoint is loaded.sequence.edges[-1]
    assert controller.declared_endpoint is not loaded.sequence.edges[0]


def test_persist_declared_endpoint_revision_reuses_25a_25b_and_preserves_exact_text(
    tmp_path: Path,
) -> None:
    _, _, _, v6_path, _, loaded = _session(tmp_path)
    controller = ChromiumResearchSessionController(loaded)
    destination = tmp_path / "v7.json"
    revised_text = "  v7 explicit human revision 😀\nStill provisional.  "

    result = controller.persist_declared_endpoint_revision(
        revised_text,
        prior_edge_source=v6_path,
        destination=destination,
    )

    assert isinstance(result, ChromiumResearchSessionEndpointRevisionPersistenceResult)
    assert result.prior_session is controller.presentation
    assert result.extension.prior_edge is controller.declared_endpoint
    assert result.extension.revision.revised_note.note_text == revised_text
    assert result.persistence.extension is result.extension
    assert result.persistence.path == destination.resolve()
    assert controller.last_endpoint_revision is result

    loaded_successor = load_chromium_research_working_set_note_revision_edge(
        controller.declared_endpoint,
        destination,
    )
    assert loaded_successor.predecessor is controller.declared_endpoint
    assert loaded_successor.revision.revised_note.note_text == revised_text


def test_wrong_explicit_endpoint_file_rejects_without_controller_state_change(
    tmp_path: Path,
) -> None:
    _, _, v5_path, _, _, loaded = _session(tmp_path)
    controller = ChromiumResearchSessionController(loaded)
    destination = tmp_path / "wrong-source-v7.json"

    with pytest.raises(ValueError):
        controller.persist_declared_endpoint_revision(
            "new human wording",
            prior_edge_source=v5_path,
            destination=destination,
        )

    assert controller.last_endpoint_revision is None
    assert not destination.exists()


def test_moved_endpoint_file_remains_location_only(tmp_path: Path) -> None:
    _, _, _, v6_path, _, loaded = _session(tmp_path)
    controller = ChromiumResearchSessionController(loaded)
    moved = tmp_path / "moved" / "renamed-v6.edge"
    moved.parent.mkdir()
    moved.write_bytes(v6_path.read_bytes())
    v6_path.unlink()
    destination = tmp_path / "v7-from-moved.json"

    result = controller.persist_declared_endpoint_revision(
        "v7 from explicitly moved predecessor",
        prior_edge_source=moved,
        destination=destination,
    )

    assert result.persistence.path == destination.resolve()
    assert result.extension.prior_edge is controller.declared_endpoint


def test_noop_and_existing_destination_reject_without_false_success(tmp_path: Path) -> None:
    _, _, _, v6_path, _, loaded = _session(tmp_path)
    controller = ChromiumResearchSessionController(loaded)
    destination = tmp_path / "occupied.json"
    destination.write_text("do not overwrite", encoding="utf-8")

    with pytest.raises(ValueError):
        controller.persist_declared_endpoint_revision(
            controller.declared_endpoint.revision.revised_note.note_text,
            prior_edge_source=v6_path,
            destination=tmp_path / "noop.json",
        )
    assert controller.last_endpoint_revision is None
    assert not (tmp_path / "noop.json").exists()

    with pytest.raises(FileExistsError):
        controller.persist_declared_endpoint_revision(
            "different valid human wording",
            prior_edge_source=v6_path,
            destination=destination,
        )
    assert controller.last_endpoint_revision is None
    assert destination.read_text(encoding="utf-8") == "do not overwrite"


def test_older_durable_inputs_may_disappear_if_loaded_state_and_endpoint_file_remain(
    tmp_path: Path,
) -> None:
    prefix, v4_path, v5_path, v6_path, declaration_path, loaded = _session(tmp_path)
    controller = ChromiumResearchSessionController(loaded)

    for item in prefix[:3]:
        item.verification.path.unlink(missing_ok=True)
    for path in (*prefix[3:7], v4_path, v5_path, declaration_path):
        path.unlink(missing_ok=True)

    destination = tmp_path / "v7-after-cleanup.json"
    result = controller.persist_declared_endpoint_revision(
        "v7 after older durable cleanup",
        prior_edge_source=v6_path,
        destination=destination,
    )

    assert result.persistence.path == destination.resolve()
    assert destination.exists()
    assert not declaration_path.exists()
    assert not v5_path.exists()


def test_success_does_not_adopt_successor_or_mutate_declared_session(tmp_path: Path) -> None:
    _, _, _, v6_path, _, loaded = _session(tmp_path)
    controller = ChromiumResearchSessionController(loaded)
    original_presentation = controller.presentation
    original_endpoint = controller.declared_endpoint
    destination = tmp_path / "v7-not-adopted.json"

    result = controller.persist_declared_endpoint_revision(
        "persisted but not adopted",
        prior_edge_source=v6_path,
        destination=destination,
    )
    loaded_successor = load_chromium_research_working_set_note_revision_edge(
        original_endpoint,
        destination,
    )

    assert controller.loaded is loaded
    assert controller.presentation is original_presentation
    assert controller.declared_endpoint is original_endpoint
    assert loaded_successor is not controller.declared_endpoint
    assert result.prior_session is original_presentation


def test_failed_later_write_does_not_erase_last_success(tmp_path: Path) -> None:
    _, _, v5_path, v6_path, _, loaded = _session(tmp_path)
    controller = ChromiumResearchSessionController(loaded)
    first = controller.persist_declared_endpoint_revision(
        "first durable successor",
        prior_edge_source=v6_path,
        destination=tmp_path / "first-v7.json",
    )

    with pytest.raises(ValueError):
        controller.persist_declared_endpoint_revision(
            "second attempt with wrong predecessor file",
            prior_edge_source=v5_path,
            destination=tmp_path / "bad-v7.json",
        )

    assert controller.last_endpoint_revision is first
    assert not (tmp_path / "bad-v7.json").exists()


def test_wrong_or_forged_loaded_state_rejects_before_controller_becomes_authority(
    tmp_path: Path,
) -> None:
    with pytest.raises(TypeError, match="loaded must be"):
        ChromiumResearchSessionController(object())  # type: ignore[arg-type]

    _, _, _, _, _, loaded = _session(tmp_path)
    forged = replace(
        loaded,
        verification=replace(
            loaded.verification,
            edges=tuple(reversed(loaded.verification.edges)),
        ),
    )
    with pytest.raises(ValueError):
        ChromiumResearchSessionController(forged)


def test_result_surface_adds_no_head_or_adoption_authority_and_module_is_explicit(
    tmp_path: Path,
) -> None:
    _, _, _, v6_path, _, loaded = _session(tmp_path)
    controller = ChromiumResearchSessionController(loaded)
    result = controller.persist_declared_endpoint_revision(
        "v7 authority bounded",
        prior_edge_source=v6_path,
        destination=tmp_path / "v7-authority-bounded.json",
    )

    field_names = {
        field.name
        for field in fields(ChromiumResearchSessionEndpointRevisionPersistenceResult)
    }
    assert field_names == {"prior_session", "extension", "persistence"}
    assert field_names.isdisjoint(
        {"latest", "current", "current_head", "adopted", "chronology", "truth"}
    )
    assert result.prior_session is controller.presentation

    module = importlib.import_module("pyxis.app.chromium_research_session_controller")
    assert hasattr(module, "ChromiumResearchSessionController")
    assert hasattr(module, "ChromiumResearchSessionEndpointRevisionPersistenceResult")
