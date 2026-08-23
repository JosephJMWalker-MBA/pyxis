from __future__ import annotations

from pathlib import Path

import pytest

from pyxis.app.chromium_research_session_continuation_reentry_plan import (
    ChromiumResearchSessionContinuationReentryPlanError,
    ChromiumResearchSessionContinuationReentryPlanResult,
    persist_chromium_research_session_continuation_reentry_plan,
)
from pyxis.app.chromium_research_session_reentry import reenter_chromium_research_session
from pyxis.app.chromium_research_session_reentry_plan_document import (
    ChromiumResearchSessionReentryPlanDocumentError,
    load_chromium_research_session_reentry_plan_document,
)
from pyxis.app.chromium_research_session_rollover import (
    rollover_chromium_research_session_to_persisted_successor,
)
from test_app_chromium_research_session_reentry import _durable_fixture


def _prior_and_rollover(tmp_path: Path, *, text: str = "v7 explicit continuation"):
    fixture = _durable_fixture(tmp_path / "base")
    prior = reenter_chromium_research_session(fixture.plan)
    controller = prior.controller
    successor = tmp_path / "v7-edge.json"
    revision = controller.persist_declared_endpoint_revision(
        text,
        prior_edge_source=fixture.v6_path,
        destination=successor,
    )
    declaration = tmp_path / "v7-declaration.json"
    rollover = rollover_chromium_research_session_to_persisted_successor(
        controller,
        revision,
        successor_edge_source=successor,
        declaration_destination=declaration,
    )
    return fixture, prior, controller, revision, successor, declaration, rollover


def test_continuation_plan_freshly_reenters_then_persists_exact_restart_configuration(
    tmp_path: Path,
) -> None:
    fixture, prior, _, _, successor, declaration, rollover = _prior_and_rollover(tmp_path)
    destination = tmp_path / "v7.plan.json"

    result = persist_chromium_research_session_continuation_reentry_plan(
        prior,
        rollover,
        successor_edge_source=successor,
        continuation_declaration_source=declaration,
        destination=destination,
    )
    decoded = load_chromium_research_session_reentry_plan_document(destination)
    restarted = reenter_chromium_research_session(decoded)

    assert isinstance(result, ChromiumResearchSessionContinuationReentryPlanResult)
    assert result.prior_reentry is prior
    assert result.rollover is rollover
    assert result.persistence.path == destination.resolve()
    assert decoded == result.plan
    assert restarted.controller.presentation == rollover.continuation_controller.presentation
    assert restarted.controller.declared_endpoint.verification.edge_record_sha256 == (
        rollover.continuation_controller.declared_endpoint.verification.edge_record_sha256
    )
    assert fixture.declaration_path != result.plan.declaration_source


def test_next_plan_moves_old_declared_edges_into_explicit_predecessor_order(
    tmp_path: Path,
) -> None:
    _, prior, _, _, successor, declaration, rollover = _prior_and_rollover(tmp_path)

    result = persist_chromium_research_session_continuation_reentry_plan(
        prior,
        rollover,
        successor_edge_source=successor,
        continuation_declaration_source=declaration,
        destination=tmp_path / "next.plan.json",
    )

    assert result.plan.starting_predecessor_edge_sources == (
        *prior.plan.starting_predecessor_edge_sources,
        *prior.plan.declared_edge_sources,
    )
    assert result.plan.declared_edge_sources == (successor,)
    assert result.plan.declaration_source == declaration


def test_next_plan_preserves_exact_prior_source_locator_choices(tmp_path: Path) -> None:
    _, prior, _, _, successor, declaration, rollover = _prior_and_rollover(tmp_path)

    result = persist_chromium_research_session_continuation_reentry_plan(
        prior,
        rollover,
        successor_edge_source=successor,
        continuation_declaration_source=declaration,
        destination=tmp_path / "next.plan.json",
    )

    assert result.plan.working_set_members == prior.plan.working_set_members
    assert result.plan.working_set_source == prior.plan.working_set_source
    assert result.plan.prior_note_source == prior.plan.prior_note_source
    assert result.plan.prior_revision_source == prior.plan.prior_revision_source
    assert result.plan.continuation_source == prior.plan.continuation_source


def test_moved_successor_and_declaration_work_only_from_explicit_new_locations(
    tmp_path: Path,
) -> None:
    _, prior, _, _, successor, declaration, rollover = _prior_and_rollover(tmp_path)
    moved = tmp_path / "moved"
    moved.mkdir()
    moved_successor = successor.rename(moved / "chosen-edge.json")
    moved_declaration = declaration.rename(moved / "chosen-declaration.json")

    result = persist_chromium_research_session_continuation_reentry_plan(
        prior,
        rollover,
        successor_edge_source=moved_successor,
        continuation_declaration_source=moved_declaration,
        destination=moved / "restart.plan.json",
    )

    assert result.plan.declared_edge_sources == (moved_successor,)
    assert result.plan.declaration_source == moved_declaration
    assert result.fresh_reentry.controller.presentation == (
        rollover.continuation_controller.presentation
    )
    assert not successor.exists()
    assert not declaration.exists()


def test_wrong_sibling_successor_rejects_before_plan_write(tmp_path: Path) -> None:
    fixture, prior, controller, _, successor, declaration, rollover = _prior_and_rollover(
        tmp_path
    )
    sibling = tmp_path / "sibling-edge.json"
    controller.persist_declared_endpoint_revision(
        "different sibling successor",
        prior_edge_source=fixture.v6_path,
        destination=sibling,
    )
    destination = tmp_path / "must-not-exist.plan.json"

    with pytest.raises(
        ChromiumResearchSessionContinuationReentryPlanError,
        match="could not freshly reconstruct",
    ):
        persist_chromium_research_session_continuation_reentry_plan(
            prior,
            rollover,
            successor_edge_source=sibling,
            continuation_declaration_source=declaration,
            destination=destination,
        )

    assert successor.exists()
    assert not destination.exists()


def test_wrong_or_stale_declaration_rejects_before_plan_write(tmp_path: Path) -> None:
    fixture, prior, _, _, successor, _, rollover = _prior_and_rollover(tmp_path)
    destination = tmp_path / "must-not-exist.plan.json"

    with pytest.raises(
        ChromiumResearchSessionContinuationReentryPlanError,
        match="could not freshly reconstruct",
    ):
        persist_chromium_research_session_continuation_reentry_plan(
            prior,
            rollover,
            successor_edge_source=successor,
            continuation_declaration_source=fixture.declaration_path,
            destination=destination,
        )

    assert not destination.exists()


def test_tampered_prior_lineage_rejects_fresh_restart_plan_even_after_rollover_succeeded(
    tmp_path: Path,
) -> None:
    fixture, prior, _, _, successor, declaration, rollover = _prior_and_rollover(tmp_path)
    fixture.v5_path.write_text("{}\n", encoding="utf-8")
    destination = tmp_path / "must-not-exist.plan.json"

    with pytest.raises(
        ChromiumResearchSessionContinuationReentryPlanError,
        match="could not freshly reconstruct",
    ):
        persist_chromium_research_session_continuation_reentry_plan(
            prior,
            rollover,
            successor_edge_source=successor,
            continuation_declaration_source=declaration,
            destination=destination,
        )

    assert not destination.exists()


def test_existing_plan_destination_is_never_overwritten(tmp_path: Path) -> None:
    _, prior, _, _, successor, declaration, rollover = _prior_and_rollover(tmp_path)
    destination = tmp_path / "existing.plan.json"
    destination.write_text("keep this exact text\n", encoding="utf-8")

    with pytest.raises(ChromiumResearchSessionReentryPlanDocumentError, match="already exists"):
        persist_chromium_research_session_continuation_reentry_plan(
            prior,
            rollover,
            successor_edge_source=successor,
            continuation_declaration_source=declaration,
            destination=destination,
        )

    assert destination.read_text(encoding="utf-8") == "keep this exact text\n"


def test_equivalent_fresh_prior_reentry_is_valid_without_object_identity_privilege(
    tmp_path: Path,
) -> None:
    fixture, prior, _, _, successor, declaration, rollover = _prior_and_rollover(tmp_path)
    equivalent_prior = reenter_chromium_research_session(fixture.plan)
    assert equivalent_prior.controller is not prior.controller
    assert equivalent_prior.controller.presentation == prior.controller.presentation

    result = persist_chromium_research_session_continuation_reentry_plan(
        equivalent_prior,
        rollover,
        successor_edge_source=successor,
        continuation_declaration_source=declaration,
        destination=tmp_path / "equivalent.plan.json",
    )

    assert result.prior_reentry is equivalent_prior
    assert result.fresh_reentry.controller.presentation == (
        rollover.continuation_controller.presentation
    )


def test_mismatched_prior_session_rejects_and_repeated_rollover_builds_restart_lineage(
    tmp_path: Path,
) -> None:
    _, prior, _, _, v7, v7_declaration, rollover7 = _prior_and_rollover(tmp_path)
    first = persist_chromium_research_session_continuation_reentry_plan(
        prior,
        rollover7,
        successor_edge_source=v7,
        continuation_declaration_source=v7_declaration,
        destination=tmp_path / "v7.plan.json",
    )

    with pytest.raises(
        ChromiumResearchSessionContinuationReentryPlanError,
        match="does not describe the session",
    ):
        persist_chromium_research_session_continuation_reentry_plan(
            first.fresh_reentry,
            rollover7,
            successor_edge_source=v7,
            continuation_declaration_source=v7_declaration,
            destination=tmp_path / "mismatch.plan.json",
        )

    live_v7 = rollover7.continuation_controller
    v8 = tmp_path / "v8-edge.json"
    revision8 = live_v7.persist_declared_endpoint_revision(
        "v8 explicit continuation",
        prior_edge_source=v7,
        destination=v8,
    )
    v8_declaration = tmp_path / "v8-declaration.json"
    rollover8 = rollover_chromium_research_session_to_persisted_successor(
        live_v7,
        revision8,
        successor_edge_source=v8,
        declaration_destination=v8_declaration,
    )
    second = persist_chromium_research_session_continuation_reentry_plan(
        first.fresh_reentry,
        rollover8,
        successor_edge_source=v8,
        continuation_declaration_source=v8_declaration,
        destination=tmp_path / "v8.plan.json",
    )

    assert second.plan.starting_predecessor_edge_sources == (
        *first.plan.starting_predecessor_edge_sources,
        *first.plan.declared_edge_sources,
    )
    assert second.plan.declared_edge_sources == (v8,)
    assert second.fresh_reentry.controller.presentation == (
        rollover8.continuation_controller.presentation
    )
