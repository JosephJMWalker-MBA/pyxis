from __future__ import annotations

import json
from pathlib import Path

import pytest

from pyxis.app.chromium_research_session_rollover import (
    rollover_chromium_research_session_to_persisted_successor,
)
from pyxis.app.chromium_research_third_basis_epoch_continuation_reentry_plan_document import (
    ChromiumResearchThirdBasisEpochContinuationCheckpointError,
    ChromiumResearchThirdBasisEpochContinuationPlanDocumentError,
    ChromiumResearchThirdBasisEpochContinuationReentryResult,
    load_chromium_research_third_basis_epoch_continuation_reentry_plan_document,
    persist_chromium_research_third_basis_epoch_continuation_checkpoint,
    reenter_chromium_research_third_basis_epoch_continuation,
)
from test_app_chromium_research_third_basis_epoch_reentry_plan_document import (
    _persist_valid_overlay,
    _root_shas,
)


_OVERLAY_FORMAT = (
    "pyxis.chromium.research_third_basis_epoch_continuation_locator_overlay.v1"
)
_ROOT_KEYS = {
    "format",
    "prior_third_basis_epoch_overlay_source",
    "declared_edge_sources",
    "declaration_source",
}


def _continuation_fixture(tmp_path: Path, *, stem: str = "40c"):
    fixture, _, third_overlay, third_checkpoint = _persist_valid_overlay(
        tmp_path,
        stem=stem,
    )
    prior = third_checkpoint.fresh_reentry
    successor = tmp_path / f"{stem}-post-third-successor.json"
    revision = prior.controller.persist_declared_endpoint_revision(
        "First ordinary continuation after the third evidence-basis epoch.",
        prior_edge_source=prior.controller.declared_endpoint.verification.path,
        destination=successor,
    )
    declaration = tmp_path / f"{stem}-post-third-declaration.json"
    rollover = rollover_chromium_research_session_to_persisted_successor(
        prior.controller,
        revision,
        successor_edge_source=successor,
        declaration_destination=declaration,
    )
    overlay = tmp_path / f"{stem}-post-third-continuation.overlay.json"
    return (
        fixture,
        prior,
        third_overlay,
        successor,
        declaration,
        rollover,
        overlay,
        third_checkpoint,
    )


def _persist_valid_continuation(tmp_path: Path, *, stem: str = "40c"):
    values = _continuation_fixture(tmp_path, stem=stem)
    _, prior, third_overlay, successor, declaration, rollover, overlay, _ = values
    checkpoint = persist_chromium_research_third_basis_epoch_continuation_checkpoint(
        prior,
        rollover,
        prior_third_basis_epoch_overlay_source=third_overlay,
        successor_edge_source=successor,
        continuation_declaration_source=declaration,
        destination=overlay,
    )
    return (*values, checkpoint)


def test_40c_checkpoint_writes_strict_overlay_and_roundtrips_exact_plan(
    tmp_path: Path,
) -> None:
    (
        _,
        prior,
        third_overlay,
        successor,
        declaration,
        rollover,
        overlay,
        _,
        checkpoint,
    ) = _persist_valid_continuation(tmp_path)

    assert checkpoint.prior_reentry is prior
    assert checkpoint.rollover is rollover
    assert checkpoint.plan.prior_third_basis_epoch_overlay_source == third_overlay.resolve()
    assert checkpoint.plan.declared_edge_sources == (successor.resolve(),)
    assert checkpoint.plan.declaration_source == declaration.resolve()
    assert checkpoint.persistence.path == overlay.resolve()
    assert checkpoint.fresh_reentry.controller.presentation == (
        rollover.continuation_controller.presentation
    )

    document = json.loads(overlay.read_text(encoding="utf-8"))
    assert set(document) == _ROOT_KEYS
    assert document["format"] == _OVERLAY_FORMAT
    assert document["prior_third_basis_epoch_overlay_source"] == third_overlay.name
    assert document["declared_edge_sources"] == [successor.name]
    assert document["declaration_source"] == declaration.name

    decoded = load_chromium_research_third_basis_epoch_continuation_reentry_plan_document(
        overlay
    )
    assert decoded == checkpoint.plan


def test_40c_fresh_reentry_retains_all_three_basis_change_roots(tmp_path: Path) -> None:
    *_, rollover, overlay, _, checkpoint = _persist_valid_continuation(
        tmp_path,
        stem="ancestry",
    )

    decoded = load_chromium_research_third_basis_epoch_continuation_reentry_plan_document(
        overlay
    )
    fresh = reenter_chromium_research_third_basis_epoch_continuation(decoded)

    assert isinstance(fresh, ChromiumResearchThirdBasisEpochContinuationReentryResult)
    assert _root_shas(fresh.prior_third_basis_epoch_reentry) == _root_shas(
        checkpoint.prior_reentry
    )
    assert len(set(_root_shas(fresh.prior_third_basis_epoch_reentry))) == 3
    assert fresh.controller.presentation == rollover.continuation_controller.presentation
    assert (
        fresh.controller.declared_endpoint.verification.edge_record_sha256
        == rollover.continuation_controller.declared_endpoint.verification.edge_record_sha256
    )


def test_40c_overlay_load_is_configuration_only_and_does_not_read_prior_overlay(
    tmp_path: Path,
) -> None:
    _, _, third_overlay, _, _, _, overlay, _, checkpoint = _persist_valid_continuation(
        tmp_path,
        stem="config-only",
    )
    moved = third_overlay.rename(
        tmp_path / "temporarily-missing-third-epoch.overlay.json"
    )

    decoded = load_chromium_research_third_basis_epoch_continuation_reentry_plan_document(
        overlay
    )

    assert decoded == checkpoint.plan
    assert not third_overlay.exists()
    moved.rename(third_overlay)


def test_40c_checkpoint_reverifies_first_second_and_third_roots_before_write(
    tmp_path: Path,
) -> None:
    for layer in ("first", "second", "third"):
        case = tmp_path / layer
        case.mkdir()
        _, prior, third_overlay, successor, declaration, rollover, overlay, _ = (
            _continuation_fixture(case, stem=f"tampered-{layer}")
        )

        second_epoch = (
            prior.prior_second_basis_epoch_continuation_reentry
            .prior_second_basis_epoch_reentry
        )
        if layer == "first":
            path = (
                second_epoch.prior_continuation_reentry.prior_root_backed_reentry
                .plan.root_source
            )
        elif layer == "second":
            path = second_epoch.plan.root_source
        else:
            path = prior.plan.root_source
        path.write_bytes(path.read_bytes() + b"tampered")

        with pytest.raises(
            ChromiumResearchThirdBasisEpochContinuationCheckpointError,
            match="could not freshly reconstruct",
        ):
            persist_chromium_research_third_basis_epoch_continuation_checkpoint(
                prior,
                rollover,
                prior_third_basis_epoch_overlay_source=third_overlay,
                successor_edge_source=successor,
                continuation_declaration_source=declaration,
                destination=overlay,
            )

        assert not overlay.exists()


def test_40c_path_distinct_equivalent_40b_overlay_is_valid_location_context(
    tmp_path: Path,
) -> None:
    _, prior, third_overlay, successor, declaration, rollover, overlay, _ = (
        _continuation_fixture(tmp_path, stem="path-distinct")
    )
    alternate = tmp_path / "alternate-third-epoch.overlay.json"
    alternate.write_bytes(third_overlay.read_bytes())

    checkpoint = persist_chromium_research_third_basis_epoch_continuation_checkpoint(
        prior,
        rollover,
        prior_third_basis_epoch_overlay_source=alternate,
        successor_edge_source=successor,
        continuation_declaration_source=declaration,
        destination=overlay,
    )

    assert checkpoint.plan.prior_third_basis_epoch_overlay_source == alternate.resolve()
    assert _root_shas(checkpoint.fresh_reentry.prior_third_basis_epoch_reentry) == (
        _root_shas(prior)
    )
    assert checkpoint.fresh_reentry.controller.presentation == (
        rollover.continuation_controller.presentation
    )


def test_40c_rejects_different_chosen_continuation_content(tmp_path: Path) -> None:
    _, prior, third_overlay, successor, declaration, _, overlay, _ = _continuation_fixture(
        tmp_path,
        stem="different-choice",
    )
    sibling = tmp_path / "different-successor.json"
    sibling_revision = prior.controller.persist_declared_endpoint_revision(
        "Different explicitly chosen post-third-epoch continuation.",
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
        ChromiumResearchThirdBasisEpochContinuationCheckpointError,
        match="presentation does not match",
    ):
        persist_chromium_research_third_basis_epoch_continuation_checkpoint(
            prior,
            sibling_rollover,
            prior_third_basis_epoch_overlay_source=third_overlay,
            successor_edge_source=successor,
            continuation_declaration_source=declaration,
            destination=overlay,
        )

    assert not overlay.exists()


def test_40c_wrong_successor_is_not_discovered_or_replaced(tmp_path: Path) -> None:
    _, prior, third_overlay, successor, declaration, rollover, overlay, _ = (
        _continuation_fixture(tmp_path, stem="wrong-successor")
    )
    sibling = tmp_path / "wrong-sibling.json"
    prior.controller.persist_declared_endpoint_revision(
        "Wrong explicit sibling after third epoch.",
        prior_edge_source=prior.controller.declared_endpoint.verification.path,
        destination=sibling,
    )
    decoy = tmp_path / "obvious-correct-successor.json"
    decoy.write_bytes(successor.read_bytes())

    with pytest.raises(
        ChromiumResearchThirdBasisEpochContinuationCheckpointError,
        match="could not freshly reconstruct",
    ):
        persist_chromium_research_third_basis_epoch_continuation_checkpoint(
            prior,
            rollover,
            prior_third_basis_epoch_overlay_source=third_overlay,
            successor_edge_source=sibling,
            continuation_declaration_source=declaration,
            destination=overlay,
        )

    assert decoy.exists()
    assert not overlay.exists()


def test_40c_destination_is_no_overwrite(tmp_path: Path) -> None:
    _, prior, third_overlay, successor, declaration, rollover, overlay, _ = (
        _continuation_fixture(tmp_path, stem="no-overwrite")
    )
    overlay.write_text("keep exact\n", encoding="utf-8")

    with pytest.raises(
        ChromiumResearchThirdBasisEpochContinuationPlanDocumentError,
        match="already exists",
    ):
        persist_chromium_research_third_basis_epoch_continuation_checkpoint(
            prior,
            rollover,
            prior_third_basis_epoch_overlay_source=third_overlay,
            successor_edge_source=successor,
            continuation_declaration_source=declaration,
            destination=overlay,
        )

    assert overlay.read_text(encoding="utf-8") == "keep exact\n"


def test_40c_duplicate_missing_unknown_bad_format_and_empty_edge_shapes_reject(
    tmp_path: Path,
) -> None:
    *_, overlay, _, _ = _persist_valid_continuation(tmp_path, stem="strict")[-3:]

    duplicate = tmp_path / "duplicate.overlay.json"
    duplicate.write_text('{"format":"x","format":"y"}\n', encoding="utf-8")
    with pytest.raises(
        ChromiumResearchThirdBasisEpochContinuationPlanDocumentError,
        match="Duplicate JSON object key",
    ):
        load_chromium_research_third_basis_epoch_continuation_reentry_plan_document(
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

    wrong_format_doc = dict(document)
    wrong_format_doc["format"] = "pyxis.not-third-continuation.v1"
    wrong_format = tmp_path / "wrong-format.overlay.json"
    wrong_format.write_text(json.dumps(wrong_format_doc) + "\n", encoding="utf-8")

    for path in (missing, unknown):
        with pytest.raises(
            ChromiumResearchThirdBasisEpochContinuationPlanDocumentError,
            match="keys are invalid",
        ):
            load_chromium_research_third_basis_epoch_continuation_reentry_plan_document(
                path
            )

    with pytest.raises(
        ChromiumResearchThirdBasisEpochContinuationPlanDocumentError,
        match="valid explicit locator plan",
    ):
        load_chromium_research_third_basis_epoch_continuation_reentry_plan_document(
            empty
        )

    with pytest.raises(
        ChromiumResearchThirdBasisEpochContinuationPlanDocumentError,
        match="unsupported format",
    ):
        load_chromium_research_third_basis_epoch_continuation_reentry_plan_document(
            wrong_format
        )


def test_40c_overlay_contains_only_locator_configuration_not_authority(
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


def test_40c_rejects_wrong_prior_reentry_type_before_any_write(tmp_path: Path) -> None:
    destination = tmp_path / "never-written.overlay.json"

    with pytest.raises(TypeError, match="ChromiumResearchThirdBasisEpochReentryResult"):
        persist_chromium_research_third_basis_epoch_continuation_checkpoint(
            object(),  # type: ignore[arg-type]
            object(),  # type: ignore[arg-type]
            prior_third_basis_epoch_overlay_source=tmp_path / "prior.overlay.json",
            successor_edge_source=tmp_path / "successor.json",
            continuation_declaration_source=tmp_path / "declaration.json",
            destination=destination,
        )

    assert not destination.exists()
