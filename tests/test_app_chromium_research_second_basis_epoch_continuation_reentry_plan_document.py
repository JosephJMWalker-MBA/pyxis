from __future__ import annotations

import json
from pathlib import Path

import pytest

from pyxis.app.chromium_research_second_basis_epoch_continuation_reentry_plan_document import (
    ChromiumResearchSecondBasisEpochContinuationCheckpointError,
    ChromiumResearchSecondBasisEpochContinuationPlanDocumentError,
    ChromiumResearchSecondBasisEpochContinuationReentryResult,
    load_chromium_research_second_basis_epoch_continuation_reentry_plan_document,
    persist_chromium_research_second_basis_epoch_continuation_checkpoint,
    reenter_chromium_research_second_basis_epoch_continuation,
)
from pyxis.app.chromium_research_session_rollover import (
    rollover_chromium_research_session_to_persisted_successor,
)
from test_app_chromium_research_second_basis_epoch_reentry_plan_document import (
    _persist_valid_overlay,
)


_OVERLAY_FORMAT = (
    "pyxis.chromium.research_second_basis_epoch_continuation_locator_overlay.v1"
)
_ROOT_KEYS = {
    "format",
    "prior_second_basis_epoch_overlay_source",
    "declared_edge_sources",
    "declaration_source",
}


def _continuation_fixture(
    tmp_path: Path,
    *,
    cumulative_prior: bool = False,
    stem: str = "37c",
):
    fixture, _, second_overlay, second_checkpoint = _persist_valid_overlay(
        tmp_path,
        cumulative_prior=cumulative_prior,
        stem=stem,
    )
    prior = second_checkpoint.fresh_reentry
    successor = tmp_path / f"{stem}-post-second-successor.json"
    revision = prior.controller.persist_declared_endpoint_revision(
        "First ordinary continuation after the second evidence-basis epoch.",
        prior_edge_source=prior.controller.declared_endpoint.verification.path,
        destination=successor,
    )
    declaration = tmp_path / f"{stem}-post-second-declaration.json"
    rollover = rollover_chromium_research_session_to_persisted_successor(
        prior.controller,
        revision,
        successor_edge_source=successor,
        declaration_destination=declaration,
    )
    overlay = tmp_path / f"{stem}-post-second-continuation.overlay.json"
    return (
        fixture,
        prior,
        second_overlay,
        successor,
        declaration,
        rollover,
        overlay,
        second_checkpoint,
    )


def _persist_valid_continuation(
    tmp_path: Path,
    *,
    cumulative_prior: bool = False,
    stem: str = "37c",
):
    values = _continuation_fixture(
        tmp_path,
        cumulative_prior=cumulative_prior,
        stem=stem,
    )
    _, prior, second_overlay, successor, declaration, rollover, overlay, _ = values
    checkpoint = persist_chromium_research_second_basis_epoch_continuation_checkpoint(
        prior,
        rollover,
        prior_second_basis_epoch_overlay_source=second_overlay,
        successor_edge_source=successor,
        continuation_declaration_source=declaration,
        destination=overlay,
    )
    return (*values, checkpoint)


def test_37c_checkpoint_writes_strict_overlay_and_roundtrips_exact_plan(
    tmp_path: Path,
) -> None:
    (
        _,
        prior,
        second_overlay,
        successor,
        declaration,
        rollover,
        overlay,
        _,
        checkpoint,
    ) = _persist_valid_continuation(tmp_path)

    assert checkpoint.prior_reentry is prior
    assert checkpoint.rollover is rollover
    assert checkpoint.plan.prior_second_basis_epoch_overlay_source == second_overlay.resolve()
    assert checkpoint.plan.declared_edge_sources == (successor.resolve(),)
    assert checkpoint.plan.declaration_source == declaration.resolve()
    assert checkpoint.persistence.path == overlay.resolve()
    assert checkpoint.fresh_reentry.controller.presentation == (
        rollover.continuation_controller.presentation
    )

    document = json.loads(overlay.read_text(encoding="utf-8"))
    assert set(document) == _ROOT_KEYS
    assert document["format"] == _OVERLAY_FORMAT
    assert document["prior_second_basis_epoch_overlay_source"] == second_overlay.name
    assert document["declared_edge_sources"] == [successor.name]
    assert document["declaration_source"] == declaration.name

    decoded = load_chromium_research_second_basis_epoch_continuation_reentry_plan_document(
        overlay
    )
    assert decoded == checkpoint.plan


def test_37c_fresh_reentry_retains_both_basis_change_ancestry_layers(
    tmp_path: Path,
) -> None:
    *_, rollover, overlay, _, checkpoint = _persist_valid_continuation(
        tmp_path,
        cumulative_prior=True,
        stem="ancestry",
    )

    decoded = load_chromium_research_second_basis_epoch_continuation_reentry_plan_document(
        overlay
    )
    fresh = reenter_chromium_research_second_basis_epoch_continuation(decoded)

    assert isinstance(fresh, ChromiumResearchSecondBasisEpochContinuationReentryResult)
    assert fresh.controller.presentation == rollover.continuation_controller.presentation
    assert fresh.prior_second_basis_epoch_reentry.loaded_root.verification.root_record_sha256 == (
        checkpoint.prior_reentry.loaded_root.verification.root_record_sha256
    )
    assert (
        fresh.prior_second_basis_epoch_reentry.prior_continuation_reentry.prior_root_backed_reentry.loaded_root.verification.root_record_sha256
        == checkpoint.prior_reentry.prior_continuation_reentry.prior_root_backed_reentry.loaded_root.verification.root_record_sha256
    )
    assert (
        fresh.controller.declared_endpoint.verification.edge_record_sha256
        == rollover.continuation_controller.declared_endpoint.verification.edge_record_sha256
    )


def test_37c_overlay_load_is_configuration_only_and_does_not_read_prior_overlay(
    tmp_path: Path,
) -> None:
    *_, second_overlay, _, _, _, overlay, _, checkpoint = _persist_valid_continuation(
        tmp_path,
        stem="config-only",
    )[1:]
    moved = second_overlay.rename(tmp_path / "temporarily-missing-second-epoch.overlay.json")

    decoded = load_chromium_research_second_basis_epoch_continuation_reentry_plan_document(
        overlay
    )

    assert decoded == checkpoint.plan
    assert not second_overlay.exists()
    moved.rename(second_overlay)


def test_37c_checkpoint_reverifies_second_root_before_write(tmp_path: Path) -> None:
    _, prior, second_overlay, successor, declaration, rollover, overlay, _ = (
        _continuation_fixture(tmp_path, stem="tampered-second-root")
    )
    prior.plan.root_source.write_bytes(prior.plan.root_source.read_bytes() + b"tampered")

    with pytest.raises(
        ChromiumResearchSecondBasisEpochContinuationCheckpointError,
        match="could not freshly reconstruct",
    ):
        persist_chromium_research_second_basis_epoch_continuation_checkpoint(
            prior,
            rollover,
            prior_second_basis_epoch_overlay_source=second_overlay,
            successor_edge_source=successor,
            continuation_declaration_source=declaration,
            destination=overlay,
        )

    assert not overlay.exists()


def test_37c_checkpoint_reverifies_retained_first_root_before_write(tmp_path: Path) -> None:
    _, prior, second_overlay, successor, declaration, rollover, overlay, _ = (
        _continuation_fixture(tmp_path, stem="tampered-first-root")
    )
    first_root = (
        prior.prior_continuation_reentry.prior_root_backed_reentry.plan.root_source
    )
    first_root.write_bytes(first_root.read_bytes() + b"tampered")

    with pytest.raises(
        ChromiumResearchSecondBasisEpochContinuationCheckpointError,
        match="could not freshly reconstruct",
    ):
        persist_chromium_research_second_basis_epoch_continuation_checkpoint(
            prior,
            rollover,
            prior_second_basis_epoch_overlay_source=second_overlay,
            successor_edge_source=successor,
            continuation_declaration_source=declaration,
            destination=overlay,
        )

    assert not overlay.exists()


def test_37c_path_distinct_durably_equivalent_second_epoch_overlay_is_valid_authority(
    tmp_path: Path,
) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    first.mkdir()
    second.mkdir()
    _, prior, _, successor, declaration, rollover, overlay, _ = _continuation_fixture(
        first,
        stem="same",
    )
    _, _, other_overlay, other_checkpoint = _persist_valid_overlay(
        second,
        stem="same",
    )
    other_prior = other_checkpoint.fresh_reentry

    assert other_prior.controller.declared_endpoint.verification.path != (
        prior.controller.declared_endpoint.verification.path
    )
    assert (
        other_prior.controller.declared_endpoint.verification.edge_record_sha256
        == prior.controller.declared_endpoint.verification.edge_record_sha256
    )
    assert other_prior.loaded_root.verification.root_record_sha256 == (
        prior.loaded_root.verification.root_record_sha256
    )

    checkpoint = persist_chromium_research_second_basis_epoch_continuation_checkpoint(
        prior,
        rollover,
        prior_second_basis_epoch_overlay_source=other_overlay,
        successor_edge_source=successor,
        continuation_declaration_source=declaration,
        destination=overlay,
    )

    assert checkpoint.plan.prior_second_basis_epoch_overlay_source == other_overlay.resolve()
    assert checkpoint.fresh_reentry.controller.presentation == (
        rollover.continuation_controller.presentation
    )
    assert overlay.exists()


def test_37c_rejects_different_chosen_continuation_content(tmp_path: Path) -> None:
    _, prior, second_overlay, successor, declaration, _, overlay, _ = _continuation_fixture(
        tmp_path,
        stem="different-choice",
    )
    sibling = tmp_path / "different-successor.json"
    sibling_revision = prior.controller.persist_declared_endpoint_revision(
        "Different explicitly chosen post-second-epoch continuation.",
        prior_edge_source=prior.controller.declared_endpoint.verification.path,
        destination=sibling,
    )
    sibling_declaration = tmp_path / "different-declaration.json"
    sibling_rollover = rollover_chromium_research_session_to_persisted_successor(
        prior.controller,
        sibling_revision,
        successor_edge_source=sibling,
        declaration_destination=sibling_declaration,
    )

    with pytest.raises(
        ChromiumResearchSecondBasisEpochContinuationCheckpointError,
        match="presentation does not match",
    ):
        persist_chromium_research_second_basis_epoch_continuation_checkpoint(
            prior,
            sibling_rollover,
            prior_second_basis_epoch_overlay_source=second_overlay,
            successor_edge_source=successor,
            continuation_declaration_source=declaration,
            destination=overlay,
        )

    assert not overlay.exists()


def test_37c_wrong_successor_is_not_discovered_or_replaced(tmp_path: Path) -> None:
    _, prior, second_overlay, successor, declaration, rollover, overlay, _ = (
        _continuation_fixture(tmp_path, stem="wrong-successor")
    )
    sibling = tmp_path / "wrong-sibling.json"
    prior.controller.persist_declared_endpoint_revision(
        "Wrong explicit sibling after second epoch.",
        prior_edge_source=prior.controller.declared_endpoint.verification.path,
        destination=sibling,
    )
    decoy = tmp_path / "obvious-correct-successor.json"
    decoy.write_bytes(successor.read_bytes())

    with pytest.raises(
        ChromiumResearchSecondBasisEpochContinuationCheckpointError,
        match="could not freshly reconstruct",
    ):
        persist_chromium_research_second_basis_epoch_continuation_checkpoint(
            prior,
            rollover,
            prior_second_basis_epoch_overlay_source=second_overlay,
            successor_edge_source=sibling,
            continuation_declaration_source=declaration,
            destination=overlay,
        )

    assert decoy.exists()
    assert not overlay.exists()


def test_37c_destination_is_no_overwrite(tmp_path: Path) -> None:
    _, prior, second_overlay, successor, declaration, rollover, overlay, _ = (
        _continuation_fixture(tmp_path, stem="no-overwrite")
    )
    overlay.write_text("keep exact\n", encoding="utf-8")

    with pytest.raises(
        ChromiumResearchSecondBasisEpochContinuationPlanDocumentError,
        match="already exists",
    ):
        persist_chromium_research_second_basis_epoch_continuation_checkpoint(
            prior,
            rollover,
            prior_second_basis_epoch_overlay_source=second_overlay,
            successor_edge_source=successor,
            continuation_declaration_source=declaration,
            destination=overlay,
        )

    assert overlay.read_text(encoding="utf-8") == "keep exact\n"


def test_37c_duplicate_missing_unknown_and_empty_edge_shapes_reject(tmp_path: Path) -> None:
    *_, overlay, _, _ = _persist_valid_continuation(tmp_path, stem="strict")[-3:]

    duplicate = tmp_path / "duplicate.overlay.json"
    duplicate.write_text('{"format":"x","format":"y"}\n', encoding="utf-8")
    with pytest.raises(
        ChromiumResearchSecondBasisEpochContinuationPlanDocumentError,
        match="Duplicate JSON object key",
    ):
        load_chromium_research_second_basis_epoch_continuation_reentry_plan_document(
            duplicate
        )

    document = json.loads(overlay.read_text(encoding="utf-8"))
    missing_doc = dict(document)
    missing_doc.pop("declaration_source")
    missing = tmp_path / "missing.overlay.json"
    missing.write_text(json.dumps(missing_doc) + "\n", encoding="utf-8")

    unknown_doc = dict(document)
    unknown_doc["latest"] = True
    unknown = tmp_path / "unknown.overlay.json"
    unknown.write_text(json.dumps(unknown_doc) + "\n", encoding="utf-8")

    empty_doc = dict(document)
    empty_doc["declared_edge_sources"] = []
    empty = tmp_path / "empty.overlay.json"
    empty.write_text(json.dumps(empty_doc) + "\n", encoding="utf-8")

    for path in (missing, unknown):
        with pytest.raises(
            ChromiumResearchSecondBasisEpochContinuationPlanDocumentError,
            match="keys are invalid",
        ):
            load_chromium_research_second_basis_epoch_continuation_reentry_plan_document(
                path
            )

    with pytest.raises(
        ChromiumResearchSecondBasisEpochContinuationPlanDocumentError,
        match="valid explicit locator plan",
    ):
        load_chromium_research_second_basis_epoch_continuation_reentry_plan_document(
            empty
        )


def test_37c_overlay_contains_only_locator_configuration_not_evidence_or_head_state(
    tmp_path: Path,
) -> None:
    *_, overlay, _, _ = _persist_valid_continuation(tmp_path, stem="semantics")[-3:]
    text = overlay.read_text(encoding="utf-8")
    document = json.loads(text)

    assert set(document) == _ROOT_KEYS
    assert "sha256" not in text.lower()
    assert "latest" not in text
    assert "current_head" not in text
    assert "canonical_head" not in text
    assert "chronology" not in text
    assert "semantic_support" not in text
    assert "authorship" not in text
    assert "citation" not in text


def test_37c_rejects_wrong_prior_reentry_type_before_any_write(tmp_path: Path) -> None:
    destination = tmp_path / "never-written.overlay.json"

    with pytest.raises(TypeError, match="ChromiumResearchSecondBasisEpochReentryResult"):
        persist_chromium_research_second_basis_epoch_continuation_checkpoint(
            object(),  # type: ignore[arg-type]
            object(),  # type: ignore[arg-type]
            prior_second_basis_epoch_overlay_source=tmp_path / "prior.overlay.json",
            successor_edge_source=tmp_path / "successor.json",
            continuation_declaration_source=tmp_path / "declaration.json",
            destination=destination,
        )

    assert not destination.exists()
