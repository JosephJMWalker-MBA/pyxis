from __future__ import annotations

from pathlib import Path

import pytest

from pyxis.app.chromium_research_first_changed_basis_root_backed_reentry import (
    ChromiumResearchFirstChangedBasisRootBackedReentryResult,
    verify_chromium_research_first_changed_basis_root_backed_reentry,
)
from pyxis.app.chromium_research_first_changed_basis_session_adoption import (
    adopt_chromium_research_first_changed_basis_governed_session,
)
from pyxis.app.chromium_research_session_reentry import (
    ChromiumResearchParagraphNoteReentryLocator,
)
from test_ui_research_first_changed_basis_session_adoption import _direct_edge


def _verified_44f_inputs(tmp_path: Path, *, stem: str):
    fixture, reentry, prepared, transition, root, edge = _direct_edge(
        tmp_path,
        stem=stem,
    )
    declaration = tmp_path / f"{stem}-adoption-declaration.json"
    adoption = adopt_chromium_research_first_changed_basis_governed_session(
        edge,
        edge_source=edge.persistence.path,
        declaration_destination=declaration,
    )
    assert len(prepared.appended_items) == 1
    appended = prepared.appended_items[0]
    locator = ChromiumResearchParagraphNoteReentryLocator(
        capture_source=appended.note.selection.source.verification.path,
        note_source=appended.verification.path,
    )
    return fixture, reentry, prepared, transition, root, edge, adoption, locator


def test_44f_freshly_reconstructs_exact_44e_root_backed_session(
    tmp_path: Path,
) -> None:
    (
        _,
        reentry,
        prepared,
        transition,
        root,
        edge,
        adoption,
        locator,
    ) = _verified_44f_inputs(tmp_path, stem="44f-app")

    result = verify_chromium_research_first_changed_basis_root_backed_reentry(
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

    assert isinstance(result, ChromiumResearchFirstChangedBasisRootBackedReentryResult)
    assert result.adoption_result is adoption
    assert result.initial_ordinary_reentry is reentry
    assert result.plan.prior_session_plan is reentry.plan
    assert result.plan.appended_working_set_members == (locator,)
    assert result.fresh_reentry.plan is result.plan
    assert result.fresh_reentry.controller is not adoption.controller
    assert result.fresh_reentry.controller.presentation == adoption.controller.presentation
    assert (
        result.fresh_reentry.loaded_root.verification.root_record_sha256
        == root.persistence.root_record_sha256
    )
    assert (
        result.fresh_reentry.loaded_declaration.verification.sequence_record_sha256
        == adoption.declaration.sequence_record_sha256
    )
    assert (
        result.fresh_reentry.controller.declared_endpoint.verification.edge_record_sha256
        == edge.persistence.edge_record_sha256
    )
    assert result.fresh_reentry.loaded_appended_members[0].note.note_text == prepared.appended_items[0].note.note_text


def test_44f_accepts_moved_appended_capture_only_via_explicit_new_locator(
    tmp_path: Path,
) -> None:
    (
        _,
        reentry,
        prepared,
        transition,
        root,
        edge,
        adoption,
        locator,
    ) = _verified_44f_inputs(tmp_path, stem="44f-moved")
    moved_capture = tmp_path / "44f-moved-appended-capture.json"
    locator.capture_source.rename(moved_capture)
    moved_locator = ChromiumResearchParagraphNoteReentryLocator(
        capture_source=moved_capture,
        note_source=locator.note_source,
    )

    result = verify_chromium_research_first_changed_basis_root_backed_reentry(
        adoption,
        reentry,
        (moved_locator,),
        changed_working_set_source=prepared.working_set_persistence.path,
        changed_note_source=prepared.note_persistence.path,
        transition_source=transition.persistence.path,
        root_source=root.persistence.path,
        first_edge_source=edge.persistence.path,
        declaration_source=adoption.declaration.path,
    )

    assert result.plan.appended_working_set_members == (moved_locator,)
    assert result.fresh_reentry.loaded_appended_members[0].note.note_text == prepared.appended_items[0].note.note_text


def test_44f_wrong_appended_member_rejects_without_creating_restart_artifact(
    tmp_path: Path,
) -> None:
    (
        fixture,
        reentry,
        prepared,
        transition,
        root,
        edge,
        adoption,
        _,
    ) = _verified_44f_inputs(tmp_path, stem="44f-wrong-member")
    wrong_locator = fixture.plan.working_set_members[0]
    before = set(tmp_path.iterdir())

    with pytest.raises(Exception):
        verify_chromium_research_first_changed_basis_root_backed_reentry(
            adoption,
            reentry,
            (wrong_locator,),
            changed_working_set_source=prepared.working_set_persistence.path,
            changed_note_source=prepared.note_persistence.path,
            transition_source=transition.persistence.path,
            root_source=root.persistence.path,
            first_edge_source=edge.persistence.path,
            declaration_source=adoption.declaration.path,
        )

    assert set(tmp_path.iterdir()) == before


def test_44f_wrong_declaration_rejects_without_promoting_decoy_or_writing_overlay(
    tmp_path: Path,
) -> None:
    (
        _,
        reentry,
        prepared,
        transition,
        root,
        edge,
        adoption,
        locator,
    ) = _verified_44f_inputs(tmp_path, stem="44f-wrong-declaration")
    before = set(tmp_path.iterdir())

    with pytest.raises(Exception):
        verify_chromium_research_first_changed_basis_root_backed_reentry(
            adoption,
            reentry,
            (locator,),
            changed_working_set_source=prepared.working_set_persistence.path,
            changed_note_source=prepared.note_persistence.path,
            transition_source=transition.persistence.path,
            root_source=root.persistence.path,
            first_edge_source=edge.persistence.path,
            declaration_source=root.persistence.path,
        )

    assert set(tmp_path.iterdir()) == before
