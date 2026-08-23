from __future__ import annotations

import json
from pathlib import Path

import pytest

from pyxis.app.chromium_research_session_reentry import (
    ChromiumResearchParagraphNoteReentryLocator,
    create_chromium_research_session_reentry_plan,
)
from pyxis.app.chromium_research_session_reentry_plan_document import (
    ChromiumResearchSessionReentryPlanDocumentError,
    ChromiumResearchSessionReentryPlanDocumentPersistenceResult,
    load_chromium_research_session_reentry_plan_document,
    persist_chromium_research_session_reentry_plan_document,
)
from test_app_chromium_research_session_reentry import _durable_fixture


def _fixture(tmp_path: Path):
    root = tmp_path / "evidence"
    root.mkdir()
    return _durable_fixture(root)


def test_persisted_locator_plan_round_trips_with_destination_relative_paths(
    tmp_path: Path,
) -> None:
    fixture = _fixture(tmp_path)
    destination = tmp_path / "next.plan.json"

    result = persist_chromium_research_session_reentry_plan_document(
        fixture.plan,
        destination,
    )
    loaded = load_chromium_research_session_reentry_plan_document(destination)
    document = json.loads(destination.read_text(encoding="utf-8"))

    assert isinstance(result, ChromiumResearchSessionReentryPlanDocumentPersistenceResult)
    assert result.path == destination.resolve()
    assert result.plan == fixture.plan
    assert loaded == fixture.plan
    assert document["format"] == "pyxis.chromium.research_session_reentry_locator_plan.v1"
    assert not Path(document["working_set_source"]).is_absolute()
    assert not Path(document["declaration_source"]).is_absolute()
    assert ".." not in Path(document["working_set_source"]).parts
    assert ".." not in Path(document["declaration_source"]).parts


def test_plan_document_persistence_is_no_overwrite(tmp_path: Path) -> None:
    fixture = _fixture(tmp_path)
    destination = tmp_path / "existing.plan.json"
    destination.write_text("keep me\n", encoding="utf-8")

    with pytest.raises(ChromiumResearchSessionReentryPlanDocumentError, match="already exists"):
        persist_chromium_research_session_reentry_plan_document(
            fixture.plan,
            destination,
        )

    assert destination.read_text(encoding="utf-8") == "keep me\n"


def test_persisted_plan_contains_locations_and_order_but_no_authority_registry(
    tmp_path: Path,
) -> None:
    fixture = _fixture(tmp_path)
    destination = tmp_path / "plan.json"

    persist_chromium_research_session_reentry_plan_document(fixture.plan, destination)
    document = json.loads(destination.read_text(encoding="utf-8"))
    serialized = destination.read_text(encoding="utf-8").lower()

    assert list(document) == [
        "format",
        "working_set_members",
        "working_set_source",
        "prior_note_source",
        "prior_revision_source",
        "continuation_source",
        "starting_predecessor_edge_sources",
        "declared_edge_sources",
        "declaration_source",
    ]
    for forbidden in (
        "sha256",
        "latest",
        "current_head",
        "canonical_head",
        "timestamp",
        "complete_history",
    ):
        assert forbidden not in serialized


def test_plan_document_persistence_does_not_read_referenced_artifacts(
    tmp_path: Path,
) -> None:
    missing = tmp_path / "missing"
    plan = create_chromium_research_session_reentry_plan(
        (
            ChromiumResearchParagraphNoteReentryLocator(
                missing / "capture.json",
                missing / "note.json",
            ),
        ),
        working_set_source=missing / "working-set.json",
        prior_note_source=missing / "prior-note.json",
        prior_revision_source=missing / "revision.json",
        continuation_source=missing / "continuation.json",
        starting_predecessor_edge_sources=(),
        declared_edge_sources=(missing / "edge.json",),
        declaration_source=missing / "declaration.json",
    )
    destination = tmp_path / "missing-artifacts.plan.json"

    persist_chromium_research_session_reentry_plan_document(plan, destination)
    loaded = load_chromium_research_session_reentry_plan_document(destination)

    assert loaded == plan
    assert not loaded.working_set_source.exists()
    assert not loaded.declaration_source.exists()


def test_forged_plan_shape_rejects_before_document_write(tmp_path: Path) -> None:
    fixture = _fixture(tmp_path)
    forged = object.__new__(type(fixture.plan))
    object.__setattr__(forged, "working_set_members", fixture.plan.working_set_members)
    object.__setattr__(forged, "working_set_source", "not-a-path")
    object.__setattr__(forged, "prior_note_source", fixture.plan.prior_note_source)
    object.__setattr__(forged, "prior_revision_source", fixture.plan.prior_revision_source)
    object.__setattr__(forged, "continuation_source", fixture.plan.continuation_source)
    object.__setattr__(
        forged,
        "starting_predecessor_edge_sources",
        fixture.plan.starting_predecessor_edge_sources,
    )
    object.__setattr__(forged, "declared_edge_sources", fixture.plan.declared_edge_sources)
    object.__setattr__(forged, "declaration_source", fixture.plan.declaration_source)
    destination = tmp_path / "forged.plan.json"

    with pytest.raises(ChromiumResearchSessionReentryPlanDocumentError, match="cannot be serialized"):
        persist_chromium_research_session_reentry_plan_document(forged, destination)

    assert not destination.exists()
