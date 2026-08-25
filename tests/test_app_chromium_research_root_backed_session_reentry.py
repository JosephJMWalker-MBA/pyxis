from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from pyxis.app.chromium_research_root_backed_session_reentry import (
    ChromiumResearchRootBackedSessionReentryError,
    ChromiumResearchRootBackedSessionReentryPlan,
    ChromiumResearchRootBackedSessionReentryResult,
    create_chromium_research_root_backed_session_reentry_plan,
    reenter_chromium_research_root_backed_session,
)
from pyxis.app.chromium_research_session_reentry import (
    ChromiumResearchParagraphNoteReentryLocator,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_sequence_load import (
    load_chromium_research_working_set_note_revision_edge_sequence,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_sequence_persistence import (
    persist_chromium_research_working_set_note_revision_edge_sequence,
)
from test_app_chromium_research_session_working_set_transition_revision_root_edge import (
    _first_edge,
)


_ROOT_FORMAT = (
    "pyxis.chromium.research_session_working_set_transition_revision_root.v1"
)
_EDGE_FORMAT = "pyxis.chromium.research_working_set_note_revision_edge.v1"


def _root_backed_fixture(tmp_path: Path, *, stem: str = "35b"):
    (
        fixture,
        prior_reentry,
        prepared,
        transition_persistence,
        root_persistence,
        loaded_root,
        _,
        edge_persistence,
        _,
    ) = _first_edge(tmp_path, stem=stem)

    sequence = load_chromium_research_working_set_note_revision_edge_sequence(
        loaded_root,
        (edge_persistence.path,),
    )
    declaration_path = tmp_path / f"{stem}-root-backed-declaration.json"
    persist_chromium_research_working_set_note_revision_edge_sequence(
        sequence,
        declaration_path,
    )

    assert len(prepared.appended_items) == 1
    appended = prepared.appended_items[0]
    locator = ChromiumResearchParagraphNoteReentryLocator(
        appended.note.selection.source.verification.path,
        appended.verification.path,
    )

    plan = create_chromium_research_root_backed_session_reentry_plan(
        fixture.plan,
        (locator,),
        changed_working_set_source=prepared.working_set_persistence.path,
        changed_note_source=prepared.note_persistence.path,
        transition_source=transition_persistence.path,
        root_source=root_persistence.path,
        declared_edge_sources=(edge_persistence.path,),
        declaration_source=declaration_path,
    )
    return (
        fixture,
        prior_reentry,
        prepared,
        transition_persistence,
        root_persistence,
        loaded_root,
        edge_persistence,
        declaration_path,
        locator,
        plan,
    )


def test_35b_plan_creation_is_locator_only_and_reads_no_changed_basis_files(
    tmp_path: Path,
) -> None:
    fixture, *_ = _root_backed_fixture(tmp_path)
    missing_capture = tmp_path / "missing-capture.json"
    missing_note = tmp_path / "missing-note.json"
    missing_paths = {
        "changed_working_set_source": tmp_path / "missing-working-set.json",
        "changed_note_source": tmp_path / "missing-working-set-note.json",
        "transition_source": tmp_path / "missing-transition.json",
        "root_source": tmp_path / "missing-root.json",
        "declaration_source": tmp_path / "missing-declaration.json",
    }
    missing_edge = tmp_path / "missing-root-edge.json"

    plan = create_chromium_research_root_backed_session_reentry_plan(
        fixture.plan,
        (ChromiumResearchParagraphNoteReentryLocator(missing_capture, missing_note),),
        declared_edge_sources=(missing_edge,),
        **missing_paths,
    )

    assert isinstance(plan, ChromiumResearchRootBackedSessionReentryPlan)
    assert plan.prior_session_plan is fixture.plan
    assert plan.appended_working_set_members[0].capture_source == missing_capture
    assert plan.declared_edge_sources == (missing_edge,)
    assert all(not path.exists() for path in (*missing_paths.values(), missing_capture, missing_note, missing_edge))


def test_35b_fresh_reentry_reconstructs_root_ancestry_and_governed_controller(
    tmp_path: Path,
) -> None:
    (
        fixture,
        prior_reentry,
        prepared,
        _,
        _,
        loaded_root,
        edge_persistence,
        _,
        _,
        plan,
    ) = _root_backed_fixture(tmp_path)

    result = reenter_chromium_research_root_backed_session(plan)

    assert isinstance(result, ChromiumResearchRootBackedSessionReentryResult)
    assert result.plan is plan
    assert result.prior_reentry is not prior_reentry
    assert result.prior_reentry.controller.presentation == prior_reentry.controller.presentation
    assert result.loaded_root is not loaded_root
    assert result.loaded_root.transition.prior_endpoint is result.prior_reentry.controller.declared_endpoint
    assert result.loaded_root.verification.root_record_sha256 == loaded_root.verification.root_record_sha256
    assert result.loaded_declaration.sequence.starting_predecessor is result.loaded_root
    assert result.loaded_declaration.sequence.edges[0].predecessor is result.loaded_root
    assert result.controller.loaded is result.loaded_declaration
    assert result.controller.declared_endpoint is result.loaded_declaration.sequence.edges[-1]
    assert result.controller.declared_endpoint.verification.edge_record_sha256 == edge_persistence.edge_record_sha256
    assert result.controller.presentation.sequence.starting_record_format == _ROOT_FORMAT
    assert result.controller.presentation.sequence.members[-1].record_format == _EDGE_FORMAT
    assert tuple(item.note.note_text for item in result.loaded_appended_members) == (
        prepared.appended_items[0].note.note_text,
    )


def test_35b_successor_member_order_is_fresh_prior_members_then_explicit_appended_members(
    tmp_path: Path,
) -> None:
    *_, prepared, _, _, _, _, _, _, plan = _root_backed_fixture(tmp_path)

    result = reenter_chromium_research_root_backed_session(plan)
    prior_items = result.prior_reentry.controller.declared_endpoint.revision.revised_note.working_set.items

    assert result.successor_items[: len(prior_items)] == prior_items
    assert all(
        observed is expected
        for observed, expected in zip(
            result.successor_items[: len(prior_items)],
            prior_items,
        )
    )
    assert result.successor_items[len(prior_items) :] == result.loaded_appended_members
    assert result.loaded_root.transition.successor_note.note.working_set.items == result.successor_items
    assert result.loaded_root.transition.successor_note.note.note_text == prepared.note.note_text


def test_35b_wrong_appended_member_locator_rejects_against_changed_working_set(
    tmp_path: Path,
) -> None:
    fixture, *_, plan = _root_backed_fixture(tmp_path)
    wrong_locator = fixture.plan.working_set_members[0]
    wrong_plan = replace(
        plan,
        appended_working_set_members=(wrong_locator,),
    )

    with pytest.raises(
        ChromiumResearchRootBackedSessionReentryError,
        match="changed working set, 33B transition, and 34A root",
    ):
        reenter_chromium_research_root_backed_session(wrong_plan)


def test_35b_tampered_root_rejects_before_root_backed_declaration_relink(
    tmp_path: Path,
) -> None:
    *_, plan = _root_backed_fixture(tmp_path)
    plan.root_source.write_bytes(plan.root_source.read_bytes() + b"tampered")

    with pytest.raises(
        ChromiumResearchRootBackedSessionReentryError,
        match="33B transition, and 34A root",
    ):
        reenter_chromium_research_root_backed_session(plan)


def test_35b_wrong_declared_edge_is_not_discovered_or_replaced(
    tmp_path: Path,
) -> None:
    fixture, *_, edge_persistence, _, _, plan = _root_backed_fixture(tmp_path)
    decoy = tmp_path / "obvious-root-backed-edge.json"
    decoy.write_bytes(edge_persistence.path.read_bytes())
    wrong_plan = replace(
        plan,
        declared_edge_sources=(fixture.v6_path,),
    )

    with pytest.raises(
        ChromiumResearchRootBackedSessionReentryError,
        match="root-backed declared segment",
    ):
        reenter_chromium_research_root_backed_session(wrong_plan)

    assert decoy.exists()


def test_35b_fresh_controller_resumes_existing_ordinary_revision_behavior(
    tmp_path: Path,
) -> None:
    *_, plan = _root_backed_fixture(tmp_path)
    result = reenter_chromium_research_root_backed_session(plan)
    destination = tmp_path / "post-reentry-ordinary-edge.json"

    revision = result.controller.persist_declared_endpoint_revision(
        "Ordinary rationale revision after fresh root-backed re-entry.",
        prior_edge_source=result.controller.declared_endpoint.verification.path,
        destination=destination,
    )

    assert revision.extension.prior_edge is result.controller.declared_endpoint
    assert revision.persistence.path == destination.resolve()
    assert revision.persistence.edge_format == _EDGE_FORMAT


def test_35b_loaded_application_evidence_survives_later_locator_loss(
    tmp_path: Path,
) -> None:
    *_, plan = _root_backed_fixture(tmp_path)
    result = reenter_chromium_research_root_backed_session(plan)
    expected_root_sha = result.loaded_root.verification.root_record_sha256
    expected_endpoint_sha = result.controller.declared_endpoint.verification.edge_record_sha256

    explicit_changed_paths = {
        *(locator.capture_source for locator in plan.appended_working_set_members),
        *(locator.note_source for locator in plan.appended_working_set_members),
        plan.changed_working_set_source,
        plan.changed_note_source,
        plan.transition_source,
        plan.root_source,
        *plan.declared_edge_sources,
        plan.declaration_source,
    }
    for path in explicit_changed_paths:
        if path.exists():
            path.unlink()

    assert result.loaded_root.verification.root_record_sha256 == expected_root_sha
    assert result.controller.declared_endpoint.verification.edge_record_sha256 == expected_endpoint_sha
    assert result.loaded_root.transition.successor_note.note.note_text
