from __future__ import annotations

import json
from pathlib import Path

import pytest

from pyxis.app.chromium_research_root_backed_session_reentry import (
    reenter_chromium_research_root_backed_session,
)
from pyxis.app.chromium_research_root_backed_session_reentry_plan_document import (
    ChromiumResearchRootBackedSessionReentryPlanCheckpointError,
    ChromiumResearchRootBackedSessionReentryPlanDocumentError,
    load_chromium_research_root_backed_session_reentry_plan_document,
    persist_chromium_research_root_backed_session_reentry_plan_document,
)
from pyxis.app.chromium_research_session_reentry_plan_document import (
    persist_chromium_research_session_reentry_plan_document,
)
from test_app_chromium_research_root_backed_session_reentry import (
    _root_backed_fixture,
)
from test_app_chromium_research_session_reentry import _all_plan_paths


_OVERLAY_FORMAT = (
    "pyxis.chromium.research_root_backed_session_reentry_locator_overlay.v1"
)
_ROOT_KEYS = {
    "format",
    "prior_session_plan_source",
    "appended_working_set_members",
    "changed_working_set_source",
    "changed_note_source",
    "transition_source",
    "root_source",
    "declared_edge_sources",
    "declaration_source",
}


def _checkpoint_fixture(tmp_path: Path, *, stem: str = "35c"):
    (
        fixture,
        _,
        _,
        _,
        _,
        _,
        _,
        _,
        _,
        plan,
    ) = _root_backed_fixture(tmp_path, stem=stem)
    prior_plan_path = tmp_path / f"{stem}-prior.plan.json"
    persist_chromium_research_session_reentry_plan_document(
        fixture.plan,
        prior_plan_path,
    )
    earned = reenter_chromium_research_root_backed_session(plan)
    overlay_path = tmp_path / f"{stem}-root-backed.overlay.json"
    return fixture, plan, earned, prior_plan_path, overlay_path


def _persist_valid_overlay(tmp_path: Path, *, stem: str = "35c"):
    fixture, plan, earned, prior_plan_path, overlay_path = _checkpoint_fixture(
        tmp_path,
        stem=stem,
    )
    checkpoint = persist_chromium_research_root_backed_session_reentry_plan_document(
        earned,
        prior_session_plan_source=prior_plan_path,
        destination=overlay_path,
    )
    return fixture, plan, earned, prior_plan_path, overlay_path, checkpoint


def test_35c_checkpoint_writes_separate_overlay_and_roundtrips_exact_plan(
    tmp_path: Path,
) -> None:
    fixture, plan, earned, prior_plan_path, overlay_path, checkpoint = (
        _persist_valid_overlay(tmp_path)
    )

    assert checkpoint.reentry is earned
    assert checkpoint.plan == plan
    assert checkpoint.fresh_reentry is not earned
    assert checkpoint.fresh_reentry.controller.presentation == earned.controller.presentation
    assert checkpoint.persistence.path == overlay_path.resolve()
    assert checkpoint.persistence.prior_session_plan_source == prior_plan_path

    document = json.loads(overlay_path.read_text(encoding="utf-8"))
    assert set(document) == _ROOT_KEYS
    assert document["format"] == _OVERLAY_FORMAT
    assert document["prior_session_plan_source"] == prior_plan_path.name
    assert "working_set_source" not in document
    assert "prior_note_source" not in document
    assert "prior_revision_source" not in document
    assert "continuation_source" not in document
    assert "starting_predecessor_edge_sources" not in document

    decoded = load_chromium_research_root_backed_session_reentry_plan_document(
        overlay_path
    )
    assert decoded == checkpoint.plan
    assert decoded.prior_session_plan == fixture.plan


def test_35c_loaded_overlay_freshly_reenters_same_root_backed_governed_session(
    tmp_path: Path,
) -> None:
    _, _, earned, _, overlay_path, _ = _persist_valid_overlay(tmp_path)

    decoded = load_chromium_research_root_backed_session_reentry_plan_document(
        overlay_path
    )
    fresh = reenter_chromium_research_root_backed_session(decoded)

    assert fresh.controller.presentation == earned.controller.presentation
    assert (
        fresh.controller.declared_endpoint.verification.edge_record_sha256
        == earned.controller.declared_endpoint.verification.edge_record_sha256
    )
    assert (
        fresh.loaded_root.verification.root_record_sha256
        == earned.loaded_root.verification.root_record_sha256
    )


def test_35c_overlay_load_reads_configuration_not_referenced_research_evidence(
    tmp_path: Path,
) -> None:
    fixture, plan, _, prior_plan_path, overlay_path, _ = _persist_valid_overlay(tmp_path)

    research_paths = {
        *_all_plan_paths(fixture.plan),
        *(locator.capture_source for locator in plan.appended_working_set_members),
        *(locator.note_source for locator in plan.appended_working_set_members),
        plan.changed_working_set_source,
        plan.changed_note_source,
        plan.transition_source,
        plan.root_source,
        *plan.declared_edge_sources,
        plan.declaration_source,
    }
    for path in research_paths:
        if path not in {prior_plan_path, overlay_path} and path.exists():
            path.unlink()

    decoded = load_chromium_research_root_backed_session_reentry_plan_document(
        overlay_path
    )

    assert decoded == plan
    assert prior_plan_path.exists()
    assert overlay_path.exists()


def test_35c_checkpoint_rejects_different_valid_prior_plan_document_before_write(
    tmp_path: Path,
) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    first.mkdir()
    second.mkdir()
    _, _, earned, _, overlay_path = _checkpoint_fixture(first, stem="first")
    other_fixture, *_ = _root_backed_fixture(second, stem="second")
    other_prior_plan = second / "other-prior.plan.json"
    persist_chromium_research_session_reentry_plan_document(
        other_fixture.plan,
        other_prior_plan,
    )

    with pytest.raises(
        ChromiumResearchRootBackedSessionReentryPlanCheckpointError,
        match="does not match",
    ):
        persist_chromium_research_root_backed_session_reentry_plan_document(
            earned,
            prior_session_plan_source=other_prior_plan,
            destination=overlay_path,
        )

    assert not overlay_path.exists()


def test_35c_checkpoint_freshly_reverifies_changed_artifacts_before_write(
    tmp_path: Path,
) -> None:
    _, plan, earned, prior_plan_path, overlay_path = _checkpoint_fixture(tmp_path)
    plan.root_source.write_bytes(plan.root_source.read_bytes() + b"tampered")

    with pytest.raises(
        ChromiumResearchRootBackedSessionReentryPlanCheckpointError,
        match="could not freshly reconstruct",
    ):
        persist_chromium_research_root_backed_session_reentry_plan_document(
            earned,
            prior_session_plan_source=prior_plan_path,
            destination=overlay_path,
        )

    assert not overlay_path.exists()


def test_35c_overlay_destination_is_no_overwrite(tmp_path: Path) -> None:
    _, _, earned, prior_plan_path, overlay_path = _checkpoint_fixture(tmp_path)
    overlay_path.write_text("keep exact\n", encoding="utf-8")

    with pytest.raises(
        ChromiumResearchRootBackedSessionReentryPlanDocumentError,
        match="already exists",
    ):
        persist_chromium_research_root_backed_session_reentry_plan_document(
            earned,
            prior_session_plan_source=prior_plan_path,
            destination=overlay_path,
        )

    assert overlay_path.read_text(encoding="utf-8") == "keep exact\n"


def test_35c_overlay_rejects_duplicate_json_keys(tmp_path: Path) -> None:
    _, _, _, _, overlay_path, _ = _persist_valid_overlay(tmp_path)
    duplicate = tmp_path / "duplicate.overlay.json"
    duplicate.write_text(
        '{"format":"x","format":"y"}\n',
        encoding="utf-8",
    )

    with pytest.raises(
        ChromiumResearchRootBackedSessionReentryPlanDocumentError,
        match="Duplicate JSON object key",
    ):
        load_chromium_research_root_backed_session_reentry_plan_document(duplicate)

    assert overlay_path.exists()


@pytest.mark.parametrize("mutation", ["missing", "unknown"])
def test_35c_overlay_rejects_missing_or_unknown_top_level_fields(
    tmp_path: Path,
    mutation: str,
) -> None:
    _, _, _, _, overlay_path, _ = _persist_valid_overlay(tmp_path)
    document = json.loads(overlay_path.read_text(encoding="utf-8"))
    if mutation == "missing":
        document.pop("root_source")
    else:
        document["latest"] = True
    invalid = tmp_path / f"{mutation}.overlay.json"
    invalid.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ChromiumResearchRootBackedSessionReentryPlanDocumentError,
        match="keys are invalid",
    ):
        load_chromium_research_root_backed_session_reentry_plan_document(invalid)


def test_35c_missing_explicit_prior_plan_is_not_replaced_by_decoy(tmp_path: Path) -> None:
    _, _, _, prior_plan_path, overlay_path, _ = _persist_valid_overlay(tmp_path)
    document = json.loads(overlay_path.read_text(encoding="utf-8"))
    document["prior_session_plan_source"] = "missing-prior.plan.json"
    wrong = tmp_path / "wrong-prior.overlay.json"
    wrong.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    decoy = tmp_path / "obvious-prior.plan.json"
    decoy.write_bytes(prior_plan_path.read_bytes())

    with pytest.raises(
        ChromiumResearchRootBackedSessionReentryPlanDocumentError,
        match="Referenced ordinary re-entry plan",
    ):
        load_chromium_research_root_backed_session_reentry_plan_document(wrong)

    assert decoy.exists()


def test_35c_overlay_contains_locator_configuration_not_evidence_or_head_state(
    tmp_path: Path,
) -> None:
    _, _, _, _, overlay_path, _ = _persist_valid_overlay(tmp_path)
    text = overlay_path.read_text(encoding="utf-8")
    document = json.loads(text)

    assert set(document) == _ROOT_KEYS
    assert "sha256" not in text.lower()
    assert "current_head" not in text
    assert "latest" not in text
    assert "chronology" not in text
    assert "semantic_support" not in text
    assert "authorship" not in text
    assert "citation" not in text
