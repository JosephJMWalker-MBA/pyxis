from __future__ import annotations

import json
from pathlib import Path

import pytest

from pyxis.app.chromium_research_root_backed_session_continuation_reentry_plan_document import (
    ChromiumResearchRootBackedSessionContinuationCheckpointError,
    ChromiumResearchRootBackedSessionContinuationPlanDocumentError,
    load_chromium_research_root_backed_session_continuation_reentry_plan_document,
    persist_chromium_research_root_backed_session_continuation_checkpoint,
    reenter_chromium_research_root_backed_session_continuation,
)
from pyxis.app.chromium_research_session_rollover import (
    rollover_chromium_research_session_to_persisted_successor,
)
from test_app_chromium_research_root_backed_session_reentry_plan_document import (
    _persist_valid_overlay,
)


_OVERLAY_FORMAT = (
    "pyxis.chromium.research_root_backed_session_continuation_locator_overlay.v1"
)
_ROOT_KEYS = {
    "format",
    "prior_root_backed_overlay_source",
    "declared_edge_sources",
    "declaration_source",
}


def _continuation_fixture(tmp_path: Path, *, stem: str = "35d"):
    fixture, plan, earned, prior_plan_path, root_overlay, _ = _persist_valid_overlay(
        tmp_path,
        stem=stem,
    )
    successor = tmp_path / f"{stem}-successor-edge.json"
    revision = earned.controller.persist_declared_endpoint_revision(
        "First ordinary continuation after persisted root-backed re-entry.",
        prior_edge_source=earned.controller.declared_endpoint.verification.path,
        destination=successor,
    )
    declaration = tmp_path / f"{stem}-continuation-declaration.json"
    rollover = rollover_chromium_research_session_to_persisted_successor(
        earned.controller,
        revision,
        successor_edge_source=successor,
        declaration_destination=declaration,
    )
    overlay = tmp_path / f"{stem}-continuation.overlay.json"
    return (
        fixture,
        plan,
        earned,
        prior_plan_path,
        root_overlay,
        successor,
        declaration,
        rollover,
        overlay,
    )


def _persist_valid_continuation(tmp_path: Path, *, stem: str = "35d"):
    values = _continuation_fixture(tmp_path, stem=stem)
    *_, earned, _, root_overlay, successor, declaration, rollover, overlay = values
    checkpoint = persist_chromium_research_root_backed_session_continuation_checkpoint(
        earned,
        rollover,
        prior_root_backed_overlay_source=root_overlay,
        successor_edge_source=successor,
        continuation_declaration_source=declaration,
        destination=overlay,
    )
    return (*values, checkpoint)


def test_35d_checkpoint_persists_only_compositional_continuation_locators(
    tmp_path: Path,
) -> None:
    (
        _,
        _,
        earned,
        _,
        root_overlay,
        successor,
        declaration,
        rollover,
        overlay,
        checkpoint,
    ) = _persist_valid_continuation(tmp_path)

    assert checkpoint.prior_reentry is earned
    assert checkpoint.rollover is rollover
    assert checkpoint.fresh_reentry.controller.presentation == (
        rollover.continuation_controller.presentation
    )
    assert checkpoint.persistence.path == overlay.resolve()

    document = json.loads(overlay.read_text(encoding="utf-8"))
    assert set(document) == _ROOT_KEYS
    assert document["format"] == _OVERLAY_FORMAT
    assert document["prior_root_backed_overlay_source"] == root_overlay.name
    assert document["declared_edge_sources"] == [successor.name]
    assert document["declaration_source"] == declaration.name
    assert "root_source" not in document
    assert "changed_working_set_source" not in document
    assert "prior_session_plan_source" not in document


def test_35d_roundtrip_plan_freshly_reconstructs_root_ancestry_then_continuation(
    tmp_path: Path,
) -> None:
    *_, rollover, overlay, checkpoint = _persist_valid_continuation(tmp_path)

    decoded = load_chromium_research_root_backed_session_continuation_reentry_plan_document(
        overlay
    )
    fresh = reenter_chromium_research_root_backed_session_continuation(decoded)

    assert decoded == checkpoint.plan
    assert fresh.controller.presentation == rollover.continuation_controller.presentation
    assert (
        fresh.controller.declared_endpoint.verification.edge_record_sha256
        == rollover.continuation_controller.declared_endpoint.verification.edge_record_sha256
    )
    assert fresh.prior_root_backed_reentry.loaded_root.verification.root_record_sha256
    assert fresh.prior_root_backed_reentry.controller.presentation.sequence.starting_record_format == (
        "pyxis.chromium.research_session_working_set_transition_revision_root.v1"
    )


def test_35d_document_load_is_locator_only_and_does_not_read_prior_overlay(
    tmp_path: Path,
) -> None:
    *_, root_overlay, _, _, _, overlay, checkpoint = _persist_valid_continuation(tmp_path)
    moved_prior = root_overlay.rename(tmp_path / "temporarily-missing-root-overlay.json")

    decoded = load_chromium_research_root_backed_session_continuation_reentry_plan_document(
        overlay
    )

    assert decoded == checkpoint.plan
    assert decoded.prior_root_backed_overlay_source == root_overlay
    assert not root_overlay.exists()
    moved_prior.rename(root_overlay)


def test_35d_checkpoint_rejects_different_valid_prior_root_overlay_before_write(
    tmp_path: Path,
) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    first.mkdir()
    second.mkdir()
    *_, earned, _, _, successor, declaration, rollover, overlay = _continuation_fixture(
        first,
        stem="first",
    )
    *_, other_root_overlay, _ = _persist_valid_overlay(second, stem="second")[3:]

    with pytest.raises(
        ChromiumResearchRootBackedSessionContinuationCheckpointError,
        match="does not describe",
    ):
        persist_chromium_research_root_backed_session_continuation_checkpoint(
            earned,
            rollover,
            prior_root_backed_overlay_source=other_root_overlay,
            successor_edge_source=successor,
            continuation_declaration_source=declaration,
            destination=overlay,
        )

    assert not overlay.exists()


def test_35d_path_distinct_content_identical_rollover_is_same_authority(
    tmp_path: Path,
) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    first.mkdir()
    second.mkdir()
    *_, earned, _, root_overlay, successor, declaration, _, overlay = _continuation_fixture(
        first,
        stem="first",
    )
    *_, second_earned, _, _, _, _, second_rollover, _ = _continuation_fixture(
        second,
        stem="second",
    )

    assert second_earned.controller is not earned.controller
    assert (
        second_earned.controller.declared_endpoint.verification.path
        != earned.controller.declared_endpoint.verification.path
    )
    assert (
        second_earned.controller.declared_endpoint.verification.edge_record_sha256
        == earned.controller.declared_endpoint.verification.edge_record_sha256
    )

    checkpoint = persist_chromium_research_root_backed_session_continuation_checkpoint(
        earned,
        second_rollover,
        prior_root_backed_overlay_source=root_overlay,
        successor_edge_source=successor,
        continuation_declaration_source=declaration,
        destination=overlay,
    )

    assert checkpoint.fresh_reentry.controller.presentation == (
        second_rollover.continuation_controller.presentation
    )
    assert overlay.exists()


def test_35d_checkpoint_rejects_different_chosen_continuation_content(
    tmp_path: Path,
) -> None:
    *_, earned, _, root_overlay, successor, declaration, _, overlay = (
        _continuation_fixture(tmp_path)
    )
    sibling = tmp_path / "different-chosen-successor.json"
    sibling_revision = earned.controller.persist_declared_endpoint_revision(
        "Different explicitly chosen continuation content.",
        prior_edge_source=earned.controller.declared_endpoint.verification.path,
        destination=sibling,
    )
    sibling_declaration = tmp_path / "different-chosen-declaration.json"
    sibling_rollover = rollover_chromium_research_session_to_persisted_successor(
        earned.controller,
        sibling_revision,
        successor_edge_source=sibling,
        declaration_destination=sibling_declaration,
    )

    with pytest.raises(
        ChromiumResearchRootBackedSessionContinuationCheckpointError,
        match="continuation presentation does not match",
    ):
        persist_chromium_research_root_backed_session_continuation_checkpoint(
            earned,
            sibling_rollover,
            prior_root_backed_overlay_source=root_overlay,
            successor_edge_source=successor,
            continuation_declaration_source=declaration,
            destination=overlay,
        )

    assert not overlay.exists()


def test_35d_wrong_successor_is_not_replaced_by_decoy_before_write(tmp_path: Path) -> None:
    *_, earned, _, root_overlay, successor, declaration, rollover, overlay = (
        _continuation_fixture(tmp_path)
    )
    sibling = tmp_path / "different-valid-sibling.json"
    earned.controller.persist_declared_endpoint_revision(
        "Different valid sibling continuation.",
        prior_edge_source=earned.controller.declared_endpoint.verification.path,
        destination=sibling,
    )
    decoy = tmp_path / "obvious-successor.json"
    decoy.write_bytes(successor.read_bytes())

    with pytest.raises(
        ChromiumResearchRootBackedSessionContinuationCheckpointError,
        match="could not freshly reconstruct",
    ):
        persist_chromium_research_root_backed_session_continuation_checkpoint(
            earned,
            rollover,
            prior_root_backed_overlay_source=root_overlay,
            successor_edge_source=sibling,
            continuation_declaration_source=declaration,
            destination=overlay,
        )

    assert decoy.exists()
    assert not overlay.exists()


def test_35d_checkpoint_freshly_reverifies_prior_root_backed_evidence(tmp_path: Path) -> None:
    _, plan, earned, _, root_overlay, successor, declaration, rollover, overlay = (
        _continuation_fixture(tmp_path)
    )
    plan.root_source.write_bytes(plan.root_source.read_bytes() + b"tampered")

    with pytest.raises(
        ChromiumResearchRootBackedSessionContinuationCheckpointError,
        match="could not freshly reconstruct",
    ):
        persist_chromium_research_root_backed_session_continuation_checkpoint(
            earned,
            rollover,
            prior_root_backed_overlay_source=root_overlay,
            successor_edge_source=successor,
            continuation_declaration_source=declaration,
            destination=overlay,
        )

    assert not overlay.exists()


def test_35d_destination_is_no_overwrite(tmp_path: Path) -> None:
    *_, earned, _, root_overlay, successor, declaration, rollover, overlay = (
        _continuation_fixture(tmp_path)
    )
    overlay.write_text("keep exact\n", encoding="utf-8")

    with pytest.raises(
        ChromiumResearchRootBackedSessionContinuationPlanDocumentError,
        match="already exists",
    ):
        persist_chromium_research_root_backed_session_continuation_checkpoint(
            earned,
            rollover,
            prior_root_backed_overlay_source=root_overlay,
            successor_edge_source=successor,
            continuation_declaration_source=declaration,
            destination=overlay,
        )

    assert overlay.read_text(encoding="utf-8") == "keep exact\n"


def test_35d_duplicate_missing_and_unknown_fields_reject(tmp_path: Path) -> None:
    *_, overlay, _ = _persist_valid_continuation(tmp_path)
    duplicate = tmp_path / "duplicate.json"
    duplicate.write_text('{"format":"x","format":"y"}\n', encoding="utf-8")
    with pytest.raises(
        ChromiumResearchRootBackedSessionContinuationPlanDocumentError,
        match="Duplicate JSON object key",
    ):
        load_chromium_research_root_backed_session_continuation_reentry_plan_document(
            duplicate
        )

    document = json.loads(overlay.read_text(encoding="utf-8"))
    missing = tmp_path / "missing.json"
    missing_document = dict(document)
    missing_document.pop("declaration_source")
    missing.write_text(json.dumps(missing_document) + "\n", encoding="utf-8")
    unknown = tmp_path / "unknown.json"
    unknown_document = dict(document)
    unknown_document["latest"] = True
    unknown.write_text(json.dumps(unknown_document) + "\n", encoding="utf-8")

    for path in (missing, unknown):
        with pytest.raises(
            ChromiumResearchRootBackedSessionContinuationPlanDocumentError,
            match="keys are invalid",
        ):
            load_chromium_research_root_backed_session_continuation_reentry_plan_document(
                path
            )


def test_35d_overlay_contains_no_evidence_digest_or_head_semantics(tmp_path: Path) -> None:
    *_, overlay, _ = _persist_valid_continuation(tmp_path)
    text = overlay.read_text(encoding="utf-8")
    assert "sha256" not in text.lower()
    assert "latest" not in text
    assert "current_head" not in text
    assert "chronology" not in text
    assert "semantic_support" not in text
    assert "authorship" not in text
    assert "citation" not in text
