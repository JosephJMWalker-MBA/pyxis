from __future__ import annotations

import json
from pathlib import Path

import pytest

from pyxis.app.chromium_research_second_basis_epoch_reentry import (
    reenter_chromium_research_second_basis_epoch,
)
from pyxis.app.chromium_research_second_basis_epoch_reentry_plan_document import (
    ChromiumResearchSecondBasisEpochReentryPlanCheckpointError,
    ChromiumResearchSecondBasisEpochReentryPlanDocumentError,
    load_chromium_research_second_basis_epoch_reentry_plan_document,
    persist_chromium_research_second_basis_epoch_reentry_plan_document,
)
from test_app_chromium_research_second_basis_epoch_reentry import (
    _prior_continuation,
    _second_epoch_fixture,
)


_OVERLAY_FORMAT = (
    "pyxis.chromium.research_second_basis_epoch_reentry_locator_overlay.v1"
)
_ROOT_KEYS = {
    "format",
    "prior_root_backed_continuation_overlay_source",
    "appended_working_set_members",
    "changed_working_set_source",
    "changed_note_source",
    "transition_source",
    "root_source",
    "declared_edge_sources",
    "declaration_source",
}


def _checkpoint_fixture(tmp_path: Path, *, cumulative_prior: bool = False, stem: str = "37b"):
    fixture = _second_epoch_fixture(
        tmp_path,
        cumulative_prior=cumulative_prior,
        stem=stem,
    )
    earned = reenter_chromium_research_second_basis_epoch(fixture["plan"])
    overlay = tmp_path / f"{stem}-second-epoch.overlay.json"
    return fixture, earned, overlay


def _persist_valid_overlay(tmp_path: Path, *, cumulative_prior: bool = False, stem: str = "37b"):
    fixture, earned, overlay = _checkpoint_fixture(
        tmp_path,
        cumulative_prior=cumulative_prior,
        stem=stem,
    )
    checkpoint = persist_chromium_research_second_basis_epoch_reentry_plan_document(
        earned,
        prior_root_backed_continuation_overlay_source=fixture["prior_overlay"],
        destination=overlay,
    )
    return fixture, earned, overlay, checkpoint


def test_37b_checkpoint_writes_strict_locator_overlay_and_roundtrips_exact_plan(
    tmp_path: Path,
) -> None:
    fixture, earned, overlay, checkpoint = _persist_valid_overlay(tmp_path)

    assert checkpoint.reentry is earned
    assert checkpoint.fresh_reentry is not earned
    assert checkpoint.plan.prior_root_backed_continuation_overlay_source == (
        fixture["prior_overlay"].resolve()
    )
    assert checkpoint.persistence.path == overlay.resolve()

    document = json.loads(overlay.read_text(encoding="utf-8"))
    assert set(document) == _ROOT_KEYS
    assert document["format"] == _OVERLAY_FORMAT
    assert document["prior_root_backed_continuation_overlay_source"] == (
        fixture["prior_overlay"].relative_to(overlay.parent).as_posix()
    )
    assert len(document["appended_working_set_members"]) == 1
    assert "prior_session_plan" not in document
    assert "prior_root_backed_plan" not in document

    decoded = load_chromium_research_second_basis_epoch_reentry_plan_document(overlay)
    assert decoded == checkpoint.plan


def test_37b_loaded_overlay_freshly_reenters_same_second_epoch_and_both_ancestry_layers(
    tmp_path: Path,
) -> None:
    _, earned, overlay, checkpoint = _persist_valid_overlay(
        tmp_path,
        cumulative_prior=True,
        stem="fresh",
    )

    decoded = load_chromium_research_second_basis_epoch_reentry_plan_document(overlay)
    fresh = reenter_chromium_research_second_basis_epoch(decoded)

    assert fresh.controller.presentation == earned.controller.presentation
    assert (
        fresh.controller.declared_endpoint.verification.edge_record_sha256
        == earned.controller.declared_endpoint.verification.edge_record_sha256
    )
    assert fresh.loaded_root.verification.root_record_sha256 == (
        earned.loaded_root.verification.root_record_sha256
    )
    assert (
        fresh.prior_continuation_reentry.controller.declared_endpoint.verification.edge_record_sha256
        == earned.prior_continuation_reentry.controller.declared_endpoint.verification.edge_record_sha256
    )
    assert (
        fresh.prior_continuation_reentry.prior_root_backed_reentry.loaded_root.verification.root_record_sha256
        == earned.prior_continuation_reentry.prior_root_backed_reentry.loaded_root.verification.root_record_sha256
    )
    assert decoded == checkpoint.plan


def test_37b_overlay_load_is_configuration_only_and_reads_no_referenced_artifacts(
    tmp_path: Path,
) -> None:
    fixture, _, overlay, checkpoint = _persist_valid_overlay(tmp_path, stem="config-only")
    plan = checkpoint.plan

    moved_prior_overlay = fixture["prior_overlay"].rename(
        fixture["prior_overlay"].with_name("temporarily-missing-prior.overlay.json")
    )
    removed_root = plan.root_source.rename(
        plan.root_source.with_name("temporarily-missing-second-root.json")
    )
    removed_edge = plan.declared_edge_sources[0].rename(
        plan.declared_edge_sources[0].with_name("temporarily-missing-second-edge.json")
    )

    decoded = load_chromium_research_second_basis_epoch_reentry_plan_document(overlay)

    assert decoded == checkpoint.plan
    assert not fixture["prior_overlay"].exists()
    assert not plan.root_source.exists()
    assert not plan.declared_edge_sources[0].exists()

    moved_prior_overlay.rename(fixture["prior_overlay"])
    removed_root.rename(plan.root_source)
    removed_edge.rename(plan.declared_edge_sources[0])


def test_37b_checkpoint_freshly_reverifies_second_epoch_before_write(tmp_path: Path) -> None:
    fixture, earned, overlay = _checkpoint_fixture(tmp_path, stem="tampered-second")
    fixture["plan"].root_source.write_bytes(
        fixture["plan"].root_source.read_bytes() + b"tampered"
    )

    with pytest.raises(
        ChromiumResearchSecondBasisEpochReentryPlanCheckpointError,
        match="could not freshly reconstruct",
    ):
        persist_chromium_research_second_basis_epoch_reentry_plan_document(
            earned,
            prior_root_backed_continuation_overlay_source=fixture["prior_overlay"],
            destination=overlay,
        )

    assert not overlay.exists()


def test_37b_checkpoint_freshly_reverifies_prior_root_backed_ancestry_before_write(
    tmp_path: Path,
) -> None:
    fixture, earned, overlay = _checkpoint_fixture(tmp_path, stem="tampered-prior")
    prior_root = earned.prior_continuation_reentry.prior_root_backed_reentry.plan.root_source
    prior_root.write_bytes(prior_root.read_bytes() + b"tampered")

    with pytest.raises(
        ChromiumResearchSecondBasisEpochReentryPlanCheckpointError,
        match="could not freshly reconstruct",
    ):
        persist_chromium_research_second_basis_epoch_reentry_plan_document(
            earned,
            prior_root_backed_continuation_overlay_source=fixture["prior_overlay"],
            destination=overlay,
        )

    assert not overlay.exists()


def test_37b_explicit_path_distinct_content_identical_prior_overlay_is_valid_authority(
    tmp_path: Path,
) -> None:
    earned_dir = tmp_path / "earned"
    other_dir = tmp_path / "other"
    fixture = _second_epoch_fixture(earned_dir, stem="same")
    earned = reenter_chromium_research_second_basis_epoch(fixture["plan"])
    other_overlay, other_prior = _prior_continuation(
        other_dir,
        cumulative=False,
        stem="same",
    )
    destination = earned_dir / "path-distinct.overlay.json"

    assert other_prior.controller.declared_endpoint.verification.path != (
        earned.prior_continuation_reentry.controller.declared_endpoint.verification.path
    )
    assert (
        other_prior.controller.declared_endpoint.verification.edge_record_sha256
        == earned.prior_continuation_reentry.controller.declared_endpoint.verification.edge_record_sha256
    )

    checkpoint = persist_chromium_research_second_basis_epoch_reentry_plan_document(
        earned,
        prior_root_backed_continuation_overlay_source=other_overlay,
        destination=destination,
    )

    assert checkpoint.plan.prior_root_backed_continuation_overlay_source == other_overlay.resolve()
    assert checkpoint.fresh_reentry.controller.presentation == earned.controller.presentation
    assert destination.exists()


def test_37b_missing_explicit_prior_overlay_is_not_replaced_by_decoy(tmp_path: Path) -> None:
    fixture, earned, overlay = _checkpoint_fixture(tmp_path, stem="missing-prior")
    decoy = tmp_path / "obvious-prior.overlay.json"
    decoy.write_bytes(fixture["prior_overlay"].read_bytes())

    with pytest.raises(
        ChromiumResearchSecondBasisEpochReentryPlanCheckpointError,
        match="could not freshly reconstruct",
    ):
        persist_chromium_research_second_basis_epoch_reentry_plan_document(
            earned,
            prior_root_backed_continuation_overlay_source=tmp_path / "missing.overlay.json",
            destination=overlay,
        )

    assert decoy.exists()
    assert not overlay.exists()


def test_37b_destination_is_no_overwrite(tmp_path: Path) -> None:
    fixture, earned, overlay = _checkpoint_fixture(tmp_path, stem="no-overwrite")
    overlay.write_text("keep exact\n", encoding="utf-8")

    with pytest.raises(
        ChromiumResearchSecondBasisEpochReentryPlanDocumentError,
        match="already exists",
    ):
        persist_chromium_research_second_basis_epoch_reentry_plan_document(
            earned,
            prior_root_backed_continuation_overlay_source=fixture["prior_overlay"],
            destination=overlay,
        )

    assert overlay.read_text(encoding="utf-8") == "keep exact\n"


def test_37b_duplicate_missing_unknown_and_bad_member_shapes_reject(tmp_path: Path) -> None:
    _, _, overlay, _ = _persist_valid_overlay(tmp_path, stem="strict")

    duplicate = tmp_path / "duplicate.overlay.json"
    duplicate.write_text('{"format":"x","format":"y"}\n', encoding="utf-8")
    with pytest.raises(
        ChromiumResearchSecondBasisEpochReentryPlanDocumentError,
        match="Duplicate JSON object key",
    ):
        load_chromium_research_second_basis_epoch_reentry_plan_document(duplicate)

    document = json.loads(overlay.read_text(encoding="utf-8"))

    missing_document = dict(document)
    missing_document.pop("root_source")
    missing = tmp_path / "missing-field.overlay.json"
    missing.write_text(json.dumps(missing_document) + "\n", encoding="utf-8")

    unknown_document = dict(document)
    unknown_document["latest"] = True
    unknown = tmp_path / "unknown-field.overlay.json"
    unknown.write_text(json.dumps(unknown_document) + "\n", encoding="utf-8")

    bad_member_document = dict(document)
    bad_member_document["appended_working_set_members"] = [{"kind": "unknown"}]
    bad_member = tmp_path / "bad-member.overlay.json"
    bad_member.write_text(json.dumps(bad_member_document) + "\n", encoding="utf-8")

    for path in (missing, unknown):
        with pytest.raises(
            ChromiumResearchSecondBasisEpochReentryPlanDocumentError,
            match="keys are invalid",
        ):
            load_chromium_research_second_basis_epoch_reentry_plan_document(path)

    with pytest.raises(
        ChromiumResearchSecondBasisEpochReentryPlanDocumentError,
        match="cannot form a valid explicit 37A locator plan",
    ):
        load_chromium_research_second_basis_epoch_reentry_plan_document(bad_member)


def test_37b_overlay_contains_locator_configuration_not_evidence_or_head_state(
    tmp_path: Path,
) -> None:
    _, _, overlay, _ = _persist_valid_overlay(tmp_path, stem="semantics")
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


def test_37b_rejects_wrong_reentry_type_before_any_write(tmp_path: Path) -> None:
    destination = tmp_path / "never-written.overlay.json"

    with pytest.raises(TypeError, match="ChromiumResearchSecondBasisEpochReentryResult"):
        persist_chromium_research_second_basis_epoch_reentry_plan_document(
            object(),  # type: ignore[arg-type]
            prior_root_backed_continuation_overlay_source=tmp_path / "prior.overlay.json",
            destination=destination,
        )

    assert not destination.exists()
