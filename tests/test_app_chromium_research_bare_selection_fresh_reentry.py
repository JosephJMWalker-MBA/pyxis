from __future__ import annotations

import json
from pathlib import Path

import pytest

from pyxis.app.chromium_research_first_changed_basis_revision_root import (
    persist_chromium_research_first_changed_basis_revision_root,
)
from pyxis.app.chromium_research_first_changed_basis_root_backed_reentry import (
    verify_chromium_research_first_changed_basis_root_backed_reentry,
)
from pyxis.app.chromium_research_first_changed_basis_root_edge import (
    persist_chromium_research_first_changed_basis_root_edge,
)
from pyxis.app.chromium_research_first_changed_basis_session_adoption import (
    adopt_chromium_research_first_changed_basis_governed_session,
)
from pyxis.app.chromium_research_first_changed_basis_transition import (
    persist_chromium_research_first_changed_basis_transition,
)
from pyxis.app.chromium_research_paragraph_text_selection import (
    select_chromium_research_paragraph_text,
)
from pyxis.app.chromium_research_paragraph_text_selection_load import (
    ChromiumPageResearchLoadedParagraphTextSelectionRecord,
    load_chromium_research_paragraph_text_selection,
)
from pyxis.app.chromium_research_paragraph_text_selection_persistence import (
    persist_chromium_research_paragraph_text_selection,
)
from pyxis.app.chromium_research_passage_selection import (
    select_chromium_research_capture_paragraph,
)
from pyxis.app.chromium_research_root_backed_session_reentry import (
    ChromiumResearchRootBackedSessionReentryError,
    create_chromium_research_root_backed_session_reentry_plan,
)
from pyxis.app.chromium_research_root_backed_session_reentry_plan_document import (
    ChromiumResearchRootBackedSessionReentryPlanDocumentError,
    load_chromium_research_root_backed_session_reentry_plan_document,
    persist_chromium_research_root_backed_session_reentry_plan_document,
)
from pyxis.app.chromium_research_session_reentry import (
    ChromiumResearchExactRangeSelectionReentryLocator,
    create_chromium_research_session_reentry_plan,
)
from pyxis.app.chromium_research_session_reentry_plan_document import (
    ChromiumResearchSessionReentryPlanDocumentError,
    load_chromium_research_session_reentry_plan_document,
    persist_chromium_research_session_reentry_plan_document,
)
from test_app_chromium_research_session_reentry import _persist_loaded_capture
from test_app_chromium_research_session_working_set_extension import (
    _persist_extension,
    _session,
)


def _bare_selection(tmp_path: Path):
    source = _persist_loaded_capture(
        tmp_path,
        stem="50f-bare",
        target_id="page-50f-bare",
        url="https://example.test/50f-bare",
        paragraph_text="Bare evidence survives a fresh process",
    )
    paragraph = select_chromium_research_capture_paragraph(
        source,
        paragraph_ordinal=1,
    )
    selection = select_chromium_research_paragraph_text(
        paragraph,
        start_offset=0,
        end_offset=4,
    )
    selection_path = tmp_path / "50f-bare-selection.json"
    persist_chromium_research_paragraph_text_selection(
        selection,
        selection_path,
    )
    loaded = load_chromium_research_paragraph_text_selection(
        source,
        selection_path,
    )
    locator = ChromiumResearchExactRangeSelectionReentryLocator(
        capture_source=source.verification.path,
        selection_source=selection_path,
    )
    return source, loaded, locator


def _bare_root_backed_lineage(tmp_path: Path):
    fixture, reentry = _session(tmp_path)
    source, bare, locator = _bare_selection(tmp_path)

    prepared = _persist_extension(
        tmp_path,
        reentry,
        (bare,),
        rationale_text="Changed basis retains one exact source passage without a note.",
        stem="50f",
    )
    transition = persist_chromium_research_first_changed_basis_transition(
        reentry.controller,
        reentry,
        prepared,
        prior_edge_source=fixture.v6_path,
        working_set_source=prepared.working_set_persistence.path,
        note_source=prepared.note_persistence.path,
        destination=tmp_path / "50f-transition.json",
    )
    root = persist_chromium_research_first_changed_basis_revision_root(
        transition,
        revised_note_text="First rationale revision after the bare-passage basis change.",
        prior_edge_source=fixture.v6_path,
        working_set_source=prepared.working_set_persistence.path,
        note_source=prepared.note_persistence.path,
        transition_source=transition.persistence.path,
        destination=tmp_path / "50f-root.json",
    )
    edge = persist_chromium_research_first_changed_basis_root_edge(
        root,
        revised_note_text="First ordinary edge after the bare-passage root.",
        root_source=root.persistence.path,
        destination=tmp_path / "50f-edge.json",
    )
    adoption = adopt_chromium_research_first_changed_basis_governed_session(
        edge,
        edge_source=edge.persistence.path,
        declaration_destination=tmp_path / "50f-adoption-declaration.json",
    )
    return (
        fixture,
        reentry,
        source,
        bare,
        locator,
        prepared,
        transition,
        root,
        edge,
        adoption,
    )


def _verify_fresh_50f(tmp_path: Path):
    (
        fixture,
        reentry,
        source,
        bare,
        locator,
        prepared,
        transition,
        root,
        edge,
        adoption,
    ) = _bare_root_backed_lineage(tmp_path)

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
    return (
        fixture,
        reentry,
        source,
        bare,
        locator,
        prepared,
        transition,
        root,
        edge,
        adoption,
        result,
    )


def test_50f_typed_bare_locator_plan_creation_reads_no_files(tmp_path: Path) -> None:
    fixture, _ = _session(tmp_path)
    capture = tmp_path / "missing-bare-capture.json"
    selection = tmp_path / "missing-bare-selection.json"
    locator = ChromiumResearchExactRangeSelectionReentryLocator(
        capture_source=capture,
        selection_source=selection,
    )

    plan = create_chromium_research_root_backed_session_reentry_plan(
        fixture.plan,
        (locator,),
        changed_working_set_source=tmp_path / "missing-working-set.json",
        changed_note_source=tmp_path / "missing-working-set-note.json",
        transition_source=tmp_path / "missing-transition.json",
        root_source=tmp_path / "missing-root.json",
        declared_edge_sources=(tmp_path / "missing-edge.json",),
        declaration_source=tmp_path / "missing-declaration.json",
    )

    assert plan.appended_working_set_members == (locator,)
    assert locator.capture_source == capture
    assert locator.selection_source == selection
    assert not capture.exists()
    assert not selection.exists()


def test_50f_fresh_35b_reconstructs_bare_passage_adopted_session(
    tmp_path: Path,
) -> None:
    (
        _,
        _,
        source,
        bare,
        locator,
        prepared,
        _,
        root,
        edge,
        adoption,
        result,
    ) = _verify_fresh_50f(tmp_path)

    fresh = result.fresh_reentry
    loaded_bare = fresh.loaded_appended_members[0]

    assert result.plan.appended_working_set_members == (locator,)
    assert isinstance(loaded_bare, ChromiumPageResearchLoadedParagraphTextSelectionRecord)
    assert loaded_bare is not bare
    assert loaded_bare.verification.path == locator.selection_source.resolve()
    assert loaded_bare.selection.source.source.verification.path == source.verification.path
    assert loaded_bare.selection.selected_text == bare.selection.selected_text == "Bare"
    assert not hasattr(loaded_bare, "note")

    assert (
        fresh.loaded_root.transition.successor_note.working_set.verification.working_set_format
        == "pyxis.chromium.research_working_set.v2"
    )
    assert (
        fresh.loaded_root.transition.successor_note.verification.note_format
        == "pyxis.chromium.research_working_set_note.v2"
    )
    assert fresh.successor_items[-1] is loaded_bare
    assert (
        fresh.loaded_root.transition.successor_note.note.working_set.items[-1]
        is loaded_bare
    )
    assert fresh.loaded_root.verification.root_record_sha256 == root.persistence.root_record_sha256
    assert (
        fresh.loaded_declaration.verification.sequence_record_sha256
        == adoption.declaration.sequence_record_sha256
    )
    assert (
        fresh.controller.declared_endpoint.verification.edge_record_sha256
        == edge.persistence.edge_record_sha256
    )
    assert fresh.controller.presentation == adoption.controller.presentation
    assert (
        fresh.controller.declared_endpoint.revision.revised_note.working_set.items[-1]
        is loaded_bare
    )

    destination = tmp_path / "50f-post-fresh-reentry-edge.json"
    revision = fresh.controller.persist_declared_endpoint_revision(
        "Ordinary governed revision after fresh bare-passage re-entry.",
        prior_edge_source=fresh.controller.declared_endpoint.verification.path,
        destination=destination,
    )
    assert revision.persistence.path == destination.resolve()
    assert revision.extension.prior_edge is fresh.controller.declared_endpoint
    assert (
        revision.extension.revision.revised_note.working_set.items[-1]
        is loaded_bare
    )
    assert prepared.working_set.items[-1] is bare


def test_50f_wrong_capture_fails_49b_attachment_inside_fresh_reentry(
    tmp_path: Path,
) -> None:
    (
        _,
        reentry,
        _,
        _,
        locator,
        prepared,
        transition,
        root,
        edge,
        adoption,
    ) = _bare_root_backed_lineage(tmp_path)
    wrong = _persist_loaded_capture(
        tmp_path,
        stem="50f-wrong",
        target_id="page-50f-wrong",
        url="https://example.test/50f-wrong",
        paragraph_text="Different evidence source",
    )
    wrong_locator = ChromiumResearchExactRangeSelectionReentryLocator(
        capture_source=wrong.verification.path,
        selection_source=locator.selection_source,
    )

    with pytest.raises(
        ChromiumResearchRootBackedSessionReentryError,
        match="appended working-set member 0",
    ):
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


def test_50f_wrong_selection_sidecar_rejects_changed_basis_relink(
    tmp_path: Path,
) -> None:
    (
        _,
        reentry,
        source,
        _,
        locator,
        prepared,
        transition,
        root,
        edge,
        adoption,
    ) = _bare_root_backed_lineage(tmp_path)
    paragraph = select_chromium_research_capture_paragraph(source, paragraph_ordinal=1)
    other = select_chromium_research_paragraph_text(
        paragraph,
        start_offset=5,
        end_offset=13,
    )
    other_path = tmp_path / "50f-other-selection.json"
    persist_chromium_research_paragraph_text_selection(other, other_path)
    wrong_locator = ChromiumResearchExactRangeSelectionReentryLocator(
        capture_source=locator.capture_source,
        selection_source=other_path,
    )

    with pytest.raises(
        ChromiumResearchRootBackedSessionReentryError,
        match="changed working set",
    ):
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


def test_50f_31b_plan_v1_refuses_bare_locator_serialization_and_decoding(
    tmp_path: Path,
) -> None:
    fixture, _ = _session(tmp_path)
    _, _, locator = _bare_selection(tmp_path)
    typed = create_chromium_research_session_reentry_plan(
        (locator,),
        working_set_source=fixture.plan.working_set_source,
        prior_note_source=fixture.plan.prior_note_source,
        prior_revision_source=fixture.plan.prior_revision_source,
        continuation_source=fixture.plan.continuation_source,
        starting_predecessor_edge_sources=fixture.plan.starting_predecessor_edge_sources,
        declared_edge_sources=fixture.plan.declared_edge_sources,
        declaration_source=fixture.plan.declaration_source,
    )
    destination = tmp_path / "50f-must-not-be-plan-v1.json"

    with pytest.raises(
        ChromiumResearchSessionReentryPlanDocumentError,
        match="unsupported member locator",
    ):
        persist_chromium_research_session_reentry_plan_document(
            typed,
            destination,
        )
    assert not destination.exists()

    valid = tmp_path / "50f-valid-prior-plan-v1.json"
    persist_chromium_research_session_reentry_plan_document(fixture.plan, valid)
    document = json.loads(valid.read_text(encoding="utf-8"))
    document["working_set_members"][0] = {
        "kind": "exact_range_selection",
        "capture_source": str(locator.capture_source),
        "selection_source": str(locator.selection_source),
    }
    unsupported = tmp_path / "50f-unsupported-kind-plan-v1.json"
    unsupported.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ChromiumResearchSessionReentryPlanDocumentError,
        match="paragraph_note, exact_range_note, or comparison_note",
    ):
        load_chromium_research_session_reentry_plan_document(unsupported)


def test_50f_35c_overlay_v1_refuses_bare_locator_serialization_and_decoding(
    tmp_path: Path,
) -> None:
    (
        fixture,
        _,
        _,
        _,
        locator,
        _,
        _,
        _,
        _,
        _,
        result,
    ) = _verify_fresh_50f(tmp_path)

    prior_plan = tmp_path / "50f-prior-plan-v1.json"
    persist_chromium_research_session_reentry_plan_document(
        fixture.plan,
        prior_plan,
    )
    overlay = tmp_path / "50f-must-not-be-overlay-v1.json"
    with pytest.raises(
        ChromiumResearchSessionReentryPlanDocumentError,
        match="unsupported member locator",
    ):
        persist_chromium_research_root_backed_session_reentry_plan_document(
            result.fresh_reentry,
            prior_session_plan_source=prior_plan,
            destination=overlay,
        )
    assert not overlay.exists()

    document = {
        "format": "pyxis.chromium.research_root_backed_session_reentry_locator_overlay.v1",
        "prior_session_plan_source": str(prior_plan),
        "appended_working_set_members": [
            {
                "kind": "exact_range_selection",
                "capture_source": str(locator.capture_source),
                "selection_source": str(locator.selection_source),
            }
        ],
        "changed_working_set_source": str(result.plan.changed_working_set_source),
        "changed_note_source": str(result.plan.changed_note_source),
        "transition_source": str(result.plan.transition_source),
        "root_source": str(result.plan.root_source),
        "declared_edge_sources": [
            str(path) for path in result.plan.declared_edge_sources
        ],
        "declaration_source": str(result.plan.declaration_source),
    }
    unsupported = tmp_path / "50f-unsupported-kind-overlay-v1.json"
    unsupported.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ChromiumResearchRootBackedSessionReentryPlanDocumentError,
        match="cannot form a valid explicit 35B locator plan",
    ):
        load_chromium_research_root_backed_session_reentry_plan_document(unsupported)
