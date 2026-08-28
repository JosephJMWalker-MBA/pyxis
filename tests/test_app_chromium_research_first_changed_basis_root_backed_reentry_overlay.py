from __future__ import annotations

from pathlib import Path

import pytest

from pyxis.app.chromium_research_first_changed_basis_root_backed_reentry import (
    verify_chromium_research_first_changed_basis_root_backed_reentry,
)
from pyxis.app.chromium_research_first_changed_basis_root_backed_reentry_overlay import (
    ChromiumResearchFirstChangedBasisRootBackedReentryOverlayResult,
    persist_chromium_research_first_changed_basis_root_backed_reentry_overlay,
)
from pyxis.app.chromium_research_root_backed_session_reentry_plan_document import (
    load_chromium_research_root_backed_session_reentry_plan_document,
)
from pyxis.app.chromium_research_session_reentry_plan_document import (
    persist_chromium_research_session_reentry_plan_document,
)
from test_app_chromium_research_first_changed_basis_root_backed_reentry import (
    _verified_44f_inputs,
)


def _verified_44f(tmp_path: Path, *, stem: str):
    (
        fixture,
        reentry,
        prepared,
        transition,
        root,
        edge,
        adoption,
        locator,
    ) = _verified_44f_inputs(tmp_path, stem=stem)
    verification = verify_chromium_research_first_changed_basis_root_backed_reentry(
        adoption,
        reentry,
        (locator,),
        changed_working_set_source=prepared.working_set_persistence.path,
        changed_note_source=prepared.note_persistence.path,
        transition_source=transition.persistence.path,
        root_source=root.persistence.path,
        first_edge_source=edge.persistence.path,
        declaration_source=adoption.declaration.path,
    )
    return fixture, reentry, prepared, transition, root, edge, adoption, verification


def test_44g_persists_exact_44f_proof_as_strict_35c_overlay(tmp_path: Path) -> None:
    fixture, _, _, _, root, edge, _, verification = _verified_44f(
        tmp_path,
        stem="44g-app",
    )
    prior_plan = tmp_path / "44g-app-prior-plan.json"
    persist_chromium_research_session_reentry_plan_document(fixture.plan, prior_plan)
    destination = tmp_path / "44g-app-overlay.json"

    result = persist_chromium_research_first_changed_basis_root_backed_reentry_overlay(
        verification,
        prior_session_plan_source=prior_plan,
        destination=destination,
    )

    assert isinstance(result, ChromiumResearchFirstChangedBasisRootBackedReentryOverlayResult)
    assert result.verification_result is verification
    assert result.checkpoint.reentry is verification.fresh_reentry
    assert result.checkpoint.plan == verification.plan
    assert result.checkpoint.persistence.path == destination.resolve()
    assert result.checkpoint.persistence.prior_session_plan_source == prior_plan
    assert (
        result.checkpoint.fresh_reentry.loaded_root.verification.root_record_sha256
        == root.persistence.root_record_sha256
    )
    assert (
        result.checkpoint.fresh_reentry.controller.declared_endpoint.verification.edge_record_sha256
        == edge.persistence.edge_record_sha256
    )
    assert load_chromium_research_root_backed_session_reentry_plan_document(destination) == verification.plan


def test_44g_different_valid_ordinary_plan_rejects_before_overlay_write(
    tmp_path: Path,
) -> None:
    _, _, _, _, _, _, _, verification = _verified_44f(tmp_path, stem="44g-wrong-prior")
    other_tmp_path = tmp_path / "other-ordinary-plan"
    other_tmp_path.mkdir()
    other_fixture, *_ = _verified_44f_inputs(
        other_tmp_path,
        stem="44g-other-prior",
    )
    wrong_prior = tmp_path / "44g-wrong-prior-plan.json"
    persist_chromium_research_session_reentry_plan_document(other_fixture.plan, wrong_prior)
    destination = tmp_path / "44g-wrong-prior-overlay.json"

    with pytest.raises(Exception, match="prior-session plan document"):
        persist_chromium_research_first_changed_basis_root_backed_reentry_overlay(
            verification,
            prior_session_plan_source=wrong_prior,
            destination=destination,
        )

    assert not destination.exists()


def test_44g_existing_destination_is_not_overwritten(tmp_path: Path) -> None:
    fixture, _, _, _, _, _, _, verification = _verified_44f(tmp_path, stem="44g-existing")
    prior_plan = tmp_path / "44g-existing-prior-plan.json"
    persist_chromium_research_session_reentry_plan_document(fixture.plan, prior_plan)
    destination = tmp_path / "44g-existing-overlay.json"
    destination.write_text("keep me exactly\n", encoding="utf-8")

    with pytest.raises(Exception, match="already exists"):
        persist_chromium_research_first_changed_basis_root_backed_reentry_overlay(
            verification,
            prior_session_plan_source=prior_plan,
            destination=destination,
        )

    assert destination.read_text(encoding="utf-8") == "keep me exactly\n"


def test_44g_tampered_root_after_44f_rejects_before_overlay_write(tmp_path: Path) -> None:
    fixture, _, _, _, _, _, _, verification = _verified_44f(tmp_path, stem="44g-tamper")
    prior_plan = tmp_path / "44g-tamper-prior-plan.json"
    persist_chromium_research_session_reentry_plan_document(fixture.plan, prior_plan)
    destination = tmp_path / "44g-tamper-overlay.json"
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
