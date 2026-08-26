from __future__ import annotations

import json
from pathlib import Path

import pytest

from pyxis.app.chromium_research_third_basis_epoch_reentry import (
    ChromiumResearchThirdBasisEpochReentryResult,
    reenter_chromium_research_third_basis_epoch,
)
from pyxis.app.chromium_research_third_basis_epoch_reentry_plan_document import (
    ChromiumResearchThirdBasisEpochReentryPlanCheckpointError,
    ChromiumResearchThirdBasisEpochReentryPlanDocumentError,
    load_chromium_research_third_basis_epoch_reentry_plan_document,
    persist_chromium_research_third_basis_epoch_reentry_plan_document,
)
from test_app_chromium_research_third_basis_epoch_reentry import (
    _prior_second_epoch_continuation,
    _third_epoch_fixture,
)


_OVERLAY_FORMAT = "pyxis.chromium.research_third_basis_epoch_reentry_locator_overlay.v1"
_ROOT_KEYS = {
    "format",
    "prior_second_basis_epoch_continuation_overlay_source",
    "appended_working_set_members",
    "changed_working_set_source",
    "changed_note_source",
    "transition_source",
    "root_source",
    "declared_edge_sources",
    "declaration_source",
}


def _persist_valid_overlay(tmp_path: Path, *, stem: str = "40b"):
    fixture = _third_epoch_fixture(tmp_path, stem=stem)
    earned = reenter_chromium_research_third_basis_epoch(fixture["plan"])
    destination = tmp_path / f"{stem}-third-epoch.overlay.json"
    checkpoint = persist_chromium_research_third_basis_epoch_reentry_plan_document(
        earned,
        prior_second_basis_epoch_continuation_overlay_source=fixture["prior_overlay"],
        destination=destination,
    )
    return fixture, earned, destination, checkpoint


def _root_shas(result: ChromiumResearchThirdBasisEpochReentryResult):
    prior = result.prior_second_basis_epoch_continuation_reentry
    second = prior.prior_second_basis_epoch_reentry
    first_root = (
        second.prior_continuation_reentry.prior_root_backed_reentry.loaded_root
        .verification.root_record_sha256
    )
    second_root = second.loaded_root.verification.root_record_sha256
    third_root = result.loaded_root.verification.root_record_sha256
    return first_root, second_root, third_root


def test_40b_checkpoint_writes_strict_overlay_and_roundtrips_exact_plan(
    tmp_path: Path,
) -> None:
    fixture, earned, destination, checkpoint = _persist_valid_overlay(tmp_path)

    assert checkpoint.reentry is earned
    assert checkpoint.plan.prior_second_basis_epoch_continuation_overlay_source == (
        fixture["prior_overlay"].resolve()
    )
    assert checkpoint.persistence.path == destination.resolve()
    assert checkpoint.fresh_reentry.controller.presentation == earned.controller.presentation
    assert (
        checkpoint.fresh_reentry.controller.declared_endpoint.verification.edge_record_sha256
        == earned.controller.declared_endpoint.verification.edge_record_sha256
    )
    assert _root_shas(checkpoint.fresh_reentry) == _root_shas(earned)

    document = json.loads(destination.read_text(encoding="utf-8"))
    assert set(document) == _ROOT_KEYS
    assert document["format"] == _OVERLAY_FORMAT
    assert document["prior_second_basis_epoch_continuation_overlay_source"] == (
        fixture["prior_overlay"].relative_to(tmp_path).as_posix()
    )
    assert len(document["appended_working_set_members"]) == 1
    assert len(document["declared_edge_sources"]) == 1

    decoded = load_chromium_research_third_basis_epoch_reentry_plan_document(destination)
    assert decoded == checkpoint.plan


def test_40b_fresh_overlay_reentry_retains_three_root_layers(tmp_path: Path) -> None:
    _, earned, destination, checkpoint = _persist_valid_overlay(
        tmp_path,
        stem="ancestry",
    )

    decoded = load_chromium_research_third_basis_epoch_reentry_plan_document(destination)
    fresh = reenter_chromium_research_third_basis_epoch(decoded)

    assert isinstance(fresh, ChromiumResearchThirdBasisEpochReentryResult)
    assert _root_shas(fresh) == _root_shas(earned)
    assert len(set(_root_shas(fresh))) == 3
    assert fresh.controller.presentation == checkpoint.fresh_reentry.controller.presentation
    assert (
        fresh.controller.declared_endpoint.verification.edge_record_sha256
        == earned.controller.declared_endpoint.verification.edge_record_sha256
    )


def test_40b_load_is_configuration_only_and_does_not_read_prior_overlay(
    tmp_path: Path,
) -> None:
    fixture, _, destination, checkpoint = _persist_valid_overlay(
        tmp_path,
        stem="config-only",
    )
    prior_overlay = fixture["prior_overlay"]
    moved = prior_overlay.rename(prior_overlay.with_name("temporarily-missing-prior.overlay.json"))

    decoded = load_chromium_research_third_basis_epoch_reentry_plan_document(destination)

    assert decoded == checkpoint.plan
    assert not prior_overlay.exists()
    moved.rename(prior_overlay)


def test_40b_path_distinct_durably_equivalent_prior_continuation_is_valid_authority(
    tmp_path: Path,
) -> None:
    fixture = _third_epoch_fixture(tmp_path / "earned", stem="same")
    earned = reenter_chromium_research_third_basis_epoch(fixture["plan"])
    other_overlay, other_prior = _prior_second_epoch_continuation(
        tmp_path / "other-prior",
        stem="same-prior",
    )
    earned_prior = earned.prior_second_basis_epoch_continuation_reentry

    assert other_prior.controller is not earned_prior.controller
    assert other_prior.controller.presentation == earned_prior.controller.presentation
    assert (
        other_prior.controller.declared_endpoint.verification.edge_record_sha256
        == earned_prior.controller.declared_endpoint.verification.edge_record_sha256
    )

    destination = tmp_path / "path-distinct.overlay.json"
    checkpoint = persist_chromium_research_third_basis_epoch_reentry_plan_document(
        earned,
        prior_second_basis_epoch_continuation_overlay_source=other_overlay,
        destination=destination,
    )

    assert checkpoint.plan.prior_second_basis_epoch_continuation_overlay_source == (
        other_overlay.resolve()
    )
    assert _root_shas(checkpoint.fresh_reentry) == _root_shas(earned)
    assert checkpoint.fresh_reentry.controller.presentation == earned.controller.presentation


def test_40b_checkpoint_reverifies_retained_first_root_before_write(
    tmp_path: Path,
) -> None:
    fixture = _third_epoch_fixture(tmp_path, stem="tampered-first-root")
    earned = reenter_chromium_research_third_basis_epoch(fixture["plan"])
    second = earned.prior_second_basis_epoch_continuation_reentry.prior_second_basis_epoch_reentry
    first_root_path = (
        second.prior_continuation_reentry.prior_root_backed_reentry.plan.root_source
    )
    first_root_path.write_bytes(first_root_path.read_bytes() + b"tampered")
    destination = tmp_path / "never-written.overlay.json"

    with pytest.raises(
        ChromiumResearchThirdBasisEpochReentryPlanCheckpointError,
        match="could not freshly reconstruct",
    ):
        persist_chromium_research_third_basis_epoch_reentry_plan_document(
            earned,
            prior_second_basis_epoch_continuation_overlay_source=fixture["prior_overlay"],
            destination=destination,
        )

    assert not destination.exists()


def test_40b_checkpoint_reverifies_retained_second_root_before_write(
    tmp_path: Path,
) -> None:
    fixture = _third_epoch_fixture(tmp_path, stem="tampered-second-root")
    earned = reenter_chromium_research_third_basis_epoch(fixture["plan"])
    second = earned.prior_second_basis_epoch_continuation_reentry.prior_second_basis_epoch_reentry
    second_root_path = second.plan.root_source
    second_root_path.write_bytes(second_root_path.read_bytes() + b"tampered")
    destination = tmp_path / "never-written.overlay.json"

    with pytest.raises(
        ChromiumResearchThirdBasisEpochReentryPlanCheckpointError,
        match="could not freshly reconstruct",
    ):
        persist_chromium_research_third_basis_epoch_reentry_plan_document(
            earned,
            prior_second_basis_epoch_continuation_overlay_source=fixture["prior_overlay"],
            destination=destination,
        )

    assert not destination.exists()


def test_40b_checkpoint_reverifies_third_root_before_write(tmp_path: Path) -> None:
    fixture = _third_epoch_fixture(tmp_path, stem="tampered-third-root")
    earned = reenter_chromium_research_third_basis_epoch(fixture["plan"])
    fixture["root"].path.write_bytes(fixture["root"].path.read_bytes() + b"tampered")
    destination = tmp_path / "never-written.overlay.json"

    with pytest.raises(
        ChromiumResearchThirdBasisEpochReentryPlanCheckpointError,
        match="could not freshly reconstruct",
    ):
        persist_chromium_research_third_basis_epoch_reentry_plan_document(
            earned,
            prior_second_basis_epoch_continuation_overlay_source=fixture["prior_overlay"],
            destination=destination,
        )

    assert not destination.exists()


def test_40b_checkpoint_reverifies_third_declared_segment_before_write(
    tmp_path: Path,
) -> None:
    fixture = _third_epoch_fixture(tmp_path, stem="tampered-declaration")
    earned = reenter_chromium_research_third_basis_epoch(fixture["plan"])
    fixture["declaration"].write_bytes(
        fixture["declaration"].read_bytes() + b"tampered"
    )
    destination = tmp_path / "never-written.overlay.json"

    with pytest.raises(
        ChromiumResearchThirdBasisEpochReentryPlanCheckpointError,
        match="could not freshly reconstruct",
    ):
        persist_chromium_research_third_basis_epoch_reentry_plan_document(
            earned,
            prior_second_basis_epoch_continuation_overlay_source=fixture["prior_overlay"],
            destination=destination,
        )

    assert not destination.exists()


def test_40b_destination_is_no_overwrite(tmp_path: Path) -> None:
    fixture = _third_epoch_fixture(tmp_path, stem="no-overwrite")
    earned = reenter_chromium_research_third_basis_epoch(fixture["plan"])
    destination = tmp_path / "existing.overlay.json"
    destination.write_text("keep exact\n", encoding="utf-8")

    with pytest.raises(
        ChromiumResearchThirdBasisEpochReentryPlanDocumentError,
        match="already exists",
    ):
        persist_chromium_research_third_basis_epoch_reentry_plan_document(
            earned,
            prior_second_basis_epoch_continuation_overlay_source=fixture["prior_overlay"],
            destination=destination,
        )

    assert destination.read_text(encoding="utf-8") == "keep exact\n"


def test_40b_duplicate_missing_unknown_empty_and_wrong_format_shapes_reject(
    tmp_path: Path,
) -> None:
    _, _, destination, _ = _persist_valid_overlay(tmp_path, stem="strict")
    document = json.loads(destination.read_text(encoding="utf-8"))

    duplicate = tmp_path / "duplicate.overlay.json"
    duplicate.write_text('{"format":"x","format":"y"}\n', encoding="utf-8")
    with pytest.raises(
        ChromiumResearchThirdBasisEpochReentryPlanDocumentError,
        match="Duplicate JSON object key",
    ):
        load_chromium_research_third_basis_epoch_reentry_plan_document(duplicate)

    missing_doc = dict(document)
    missing_doc.pop("declaration_source")
    missing = tmp_path / "missing.overlay.json"
    missing.write_text(json.dumps(missing_doc) + "\n", encoding="utf-8")

    unknown_doc = dict(document)
    unknown_doc["latest"] = True
    unknown = tmp_path / "unknown.overlay.json"
    unknown.write_text(json.dumps(unknown_doc) + "\n", encoding="utf-8")

    empty_members_doc = dict(document)
    empty_members_doc["appended_working_set_members"] = []
    empty_members = tmp_path / "empty-members.overlay.json"
    empty_members.write_text(json.dumps(empty_members_doc) + "\n", encoding="utf-8")

    empty_edges_doc = dict(document)
    empty_edges_doc["declared_edge_sources"] = []
    empty_edges = tmp_path / "empty-edges.overlay.json"
    empty_edges.write_text(json.dumps(empty_edges_doc) + "\n", encoding="utf-8")

    wrong_format_doc = dict(document)
    wrong_format_doc["format"] = "pyxis.not-third-epoch.v1"
    wrong_format = tmp_path / "wrong-format.overlay.json"
    wrong_format.write_text(json.dumps(wrong_format_doc) + "\n", encoding="utf-8")

    for path in (missing, unknown):
        with pytest.raises(
            ChromiumResearchThirdBasisEpochReentryPlanDocumentError,
            match="keys are invalid",
        ):
            load_chromium_research_third_basis_epoch_reentry_plan_document(path)

    with pytest.raises(
        ChromiumResearchThirdBasisEpochReentryPlanDocumentError,
        match="appended_working_set_members must be a non-empty JSON array",
    ):
        load_chromium_research_third_basis_epoch_reentry_plan_document(empty_members)

    with pytest.raises(
        ChromiumResearchThirdBasisEpochReentryPlanDocumentError,
        match="valid explicit 40A locator plan",
    ):
        load_chromium_research_third_basis_epoch_reentry_plan_document(empty_edges)

    with pytest.raises(
        ChromiumResearchThirdBasisEpochReentryPlanDocumentError,
        match="unsupported format",
    ):
        load_chromium_research_third_basis_epoch_reentry_plan_document(wrong_format)


def test_40b_overlay_contains_only_locator_configuration_not_authority(
    tmp_path: Path,
) -> None:
    _, _, destination, _ = _persist_valid_overlay(tmp_path, stem="semantics")
    text = destination.read_text(encoding="utf-8")
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


def test_40b_rejects_wrong_types_before_any_write(tmp_path: Path) -> None:
    destination = tmp_path / "never-written.overlay.json"

    with pytest.raises(TypeError, match="ChromiumResearchThirdBasisEpochReentryResult"):
        persist_chromium_research_third_basis_epoch_reentry_plan_document(
            object(),  # type: ignore[arg-type]
            prior_second_basis_epoch_continuation_overlay_source=tmp_path / "prior.json",
            destination=destination,
        )
    assert not destination.exists()

    fixture = _third_epoch_fixture(tmp_path / "valid", stem="wrong-path-type")
    earned = reenter_chromium_research_third_basis_epoch(fixture["plan"])
    with pytest.raises(TypeError, match="prior_second_basis_epoch_continuation_overlay_source"):
        persist_chromium_research_third_basis_epoch_reentry_plan_document(
            earned,
            prior_second_basis_epoch_continuation_overlay_source="bad",  # type: ignore[arg-type]
            destination=destination,
        )
    assert not destination.exists()

    with pytest.raises(TypeError, match="destination must be pathlib.Path"):
        persist_chromium_research_third_basis_epoch_reentry_plan_document(
            earned,
            prior_second_basis_epoch_continuation_overlay_source=fixture["prior_overlay"],
            destination="bad",  # type: ignore[arg-type]
        )
    assert not destination.exists()
