from __future__ import annotations

import json
from pathlib import Path

import pytest

from pyxis.app.chromium_research_first_changed_basis_root_backed_reentry_overlay import (
    persist_chromium_research_first_changed_basis_root_backed_reentry_overlay,
)
from pyxis.app.chromium_research_root_backed_session_reentry import (
    reenter_chromium_research_root_backed_session,
)
from pyxis.app.chromium_research_root_backed_session_reentry_plan_document import (
    ChromiumResearchRootBackedSessionReentryPlanDocumentError,
    load_chromium_research_root_backed_session_reentry_plan_document,
)
from pyxis.app.chromium_research_session_reentry_plan_document import (
    persist_chromium_research_session_reentry_plan_document,
)
from test_app_chromium_research_bare_selection_fresh_reentry import (
    _verify_fresh_50f,
)
from test_app_chromium_research_first_changed_basis_root_backed_reentry import (
    _verified_44f_inputs,
)
from test_app_chromium_research_root_backed_session_reentry_plan_document import (
    _persist_valid_overlay,
)


_OVERLAY_V1 = "pyxis.chromium.research_root_backed_session_reentry_locator_overlay.v1"
_OVERLAY_V2 = "pyxis.chromium.research_root_backed_session_reentry_locator_overlay.v2"
_PLAN_V1 = "pyxis.chromium.research_session_reentry_locator_plan.v1"


def _persist_bare_overlay(tmp_path: Path, *, stem: str = "50h"):
    (
        fixture,
        _,
        _,
        _,
        locator,
        _,
        _,
        root,
        edge,
        _,
        verification,
    ) = _verify_fresh_50f(tmp_path)
    prior_plan = tmp_path / f"{stem}-prior-plan.json"
    persist_chromium_research_session_reentry_plan_document(fixture.plan, prior_plan)
    destination = tmp_path / f"{stem}-overlay.json"
    result = persist_chromium_research_first_changed_basis_root_backed_reentry_overlay(
        verification,
        prior_session_plan_source=prior_plan,
        destination=destination,
    )
    return fixture, locator, root, edge, verification, prior_plan, destination, result


def test_50h_public_44g_persists_bare_selection_as_strict_overlay_v2(
    tmp_path: Path,
) -> None:
    (
        fixture,
        locator,
        root,
        edge,
        verification,
        prior_plan,
        destination,
        result,
    ) = _persist_bare_overlay(tmp_path)

    assert result.verification_result is verification
    assert result.checkpoint.reentry is verification.fresh_reentry
    assert result.checkpoint.plan == verification.plan
    assert result.checkpoint.persistence.path == destination.resolve()
    assert result.checkpoint.persistence.prior_session_plan_source == prior_plan
    assert result.checkpoint.persistence.overlay_format == _OVERLAY_V2

    prior_document = json.loads(prior_plan.read_text(encoding="utf-8"))
    assert prior_document["format"] == _PLAN_V1
    assert prior_document["working_set_members"] == [
        {
            "kind": member["kind"],
            **{key: value for key, value in member.items() if key != "kind"},
        }
        for member in prior_document["working_set_members"]
    ]

    document = json.loads(destination.read_text(encoding="utf-8"))
    assert document["format"] == _OVERLAY_V2
    assert set(document) == {
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
    assert len(document["appended_working_set_members"]) == 1
    member = document["appended_working_set_members"][0]
    assert set(member) == {"kind", "capture_source", "selection_source"}
    assert member["kind"] == "exact_range_selection"
    assert "note_source" not in member

    base = destination.parent
    assert (base / member["capture_source"]).resolve() == locator.capture_source.resolve()
    assert (base / member["selection_source"]).resolve() == locator.selection_source.resolve()

    serialized = json.dumps(document, sort_keys=True)
    for forbidden in (
        "selected_text",
        "note_text",
        "evidence_digest",
        "timestamp",
        "current_head",
        "latest",
        "semantic_support",
        "authorship",
        "citation",
    ):
        assert forbidden not in serialized

    decoded = load_chromium_research_root_backed_session_reentry_plan_document(
        destination
    )
    assert decoded == verification.plan
    assert decoded.prior_session_plan == fixture.plan

    fresh = reenter_chromium_research_root_backed_session(decoded)
    assert fresh.controller.presentation == verification.fresh_reentry.controller.presentation
    assert (
        fresh.loaded_root.verification.root_record_sha256
        == root.persistence.root_record_sha256
    )
    assert (
        fresh.controller.declared_endpoint.verification.edge_record_sha256
        == edge.persistence.edge_record_sha256
    )


def test_50h_note_only_35c_persistence_remains_overlay_v1(tmp_path: Path) -> None:
    _, plan, _, _, overlay_path, checkpoint = _persist_valid_overlay(tmp_path)

    document = json.loads(overlay_path.read_text(encoding="utf-8"))
    assert document["format"] == _OVERLAY_V1
    assert load_chromium_research_root_backed_session_reentry_plan_document(
        overlay_path
    ) == plan
    assert checkpoint.plan == plan
    assert checkpoint.persistence.overlay_format == _OVERLAY_V1
    assert all(
        member["kind"] in {"paragraph_note", "exact_range_note", "comparison_note"}
        for member in document["appended_working_set_members"]
    )


@pytest.mark.parametrize(
    ("mutation", "expected"),
    [
        ("missing_selection", "cannot form a valid explicit 35B locator plan"),
        ("extra_note", "cannot form a valid explicit 35B locator plan"),
        ("wrong_kind", "cannot form a valid explicit 35B locator plan"),
    ],
)
def test_50h_overlay_v2_rejects_cross_shaped_bare_members(
    tmp_path: Path,
    mutation: str,
    expected: str,
) -> None:
    *_, destination, _ = _persist_bare_overlay(tmp_path, stem=f"50h-{mutation}")
    document = json.loads(destination.read_text(encoding="utf-8"))
    member = document["appended_working_set_members"][0]

    if mutation == "missing_selection":
        member.pop("selection_source")
    elif mutation == "extra_note":
        member["note_source"] = "fake-note.json"
    else:
        member["kind"] = "exact_range_selection_note"

    invalid = tmp_path / f"{mutation}-invalid-v2.json"
    invalid.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ChromiumResearchRootBackedSessionReentryPlanDocumentError,
        match=expected,
    ):
        load_chromium_research_root_backed_session_reentry_plan_document(invalid)


def test_50h_overlay_loader_rejects_unknown_version(tmp_path: Path) -> None:
    *_, destination, _ = _persist_bare_overlay(tmp_path, stem="50h-unknown")
    document = json.loads(destination.read_text(encoding="utf-8"))
    document["format"] = (
        "pyxis.chromium.research_root_backed_session_reentry_locator_overlay.v3"
    )
    invalid = tmp_path / "50h-unknown-version.json"
    invalid.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ChromiumResearchRootBackedSessionReentryPlanDocumentError,
        match="unsupported format",
    ):
        load_chromium_research_root_backed_session_reentry_plan_document(invalid)


def test_50h_bare_overlay_wrong_prior_plan_rejects_before_write(tmp_path: Path) -> None:
    *_, verification = _verify_fresh_50f(tmp_path)
    other = tmp_path / "other"
    other.mkdir()
    other_fixture, *_ = _verified_44f_inputs(other, stem="50h-other")
    wrong_prior = tmp_path / "50h-wrong-prior.json"
    persist_chromium_research_session_reentry_plan_document(
        other_fixture.plan,
        wrong_prior,
    )
    destination = tmp_path / "50h-wrong-prior-overlay.json"

    with pytest.raises(Exception, match="prior-session plan document"):
        persist_chromium_research_first_changed_basis_root_backed_reentry_overlay(
            verification,
            prior_session_plan_source=wrong_prior,
            destination=destination,
        )

    assert not destination.exists()


def test_50h_bare_overlay_tampered_root_rejects_before_write(tmp_path: Path) -> None:
    fixture, *_, verification = _verify_fresh_50f(tmp_path)
    prior_plan = tmp_path / "50h-tamper-prior.json"
    persist_chromium_research_session_reentry_plan_document(fixture.plan, prior_plan)
    destination = tmp_path / "50h-tamper-overlay.json"
    verification.plan.root_source.write_bytes(
        verification.plan.root_source.read_bytes() + b"tampered"
    )

    with pytest.raises(Exception, match="freshly reconstruct"):
        persist_chromium_research_first_changed_basis_root_backed_reentry_overlay(
            verification,
            prior_session_plan_source=prior_plan,
            destination=destination,
        )

    assert not destination.exists()


def test_50h_bare_overlay_destination_remains_no_overwrite(tmp_path: Path) -> None:
    fixture, *_, verification = _verify_fresh_50f(tmp_path)
    prior_plan = tmp_path / "50h-existing-prior.json"
    persist_chromium_research_session_reentry_plan_document(fixture.plan, prior_plan)
    destination = tmp_path / "50h-existing-overlay.json"
    destination.write_text("preserve exactly\n", encoding="utf-8")

    with pytest.raises(Exception, match="already exists"):
        persist_chromium_research_first_changed_basis_root_backed_reentry_overlay(
            verification,
            prior_session_plan_source=prior_plan,
            destination=destination,
        )

    assert destination.read_text(encoding="utf-8") == "preserve exactly\n"
