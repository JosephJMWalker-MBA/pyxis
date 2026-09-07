from __future__ import annotations

from pathlib import Path

from pyxis.app.chromium_research_first_changed_basis_revision_root import (
    persist_chromium_research_first_changed_basis_revision_root,
)
from pyxis.app.chromium_research_first_changed_basis_root_backed_reentry import (
    ChromiumResearchFirstChangedBasisRootBackedReentryResult,
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
from pyxis.app.chromium_research_revision_edge_working_set_presentation import (
    present_chromium_research_revision_edge_working_set_context,
)
from pyxis.app.chromium_research_session_reentry import (
    ChromiumResearchExactRangeSelectionReentryLocator,
)
from test_app_chromium_research_session_reentry import _persist_loaded_capture
from test_app_chromium_research_session_working_set_extension import (
    _persist_extension,
    _session,
)


def test_50f_fresh_process_reentry_reconstructs_bare_saved_passage(
    tmp_path: Path,
) -> None:
    fixture, ordinary_reentry = _session(tmp_path)

    source = _persist_loaded_capture(
        tmp_path,
        stem="50f-bare",
        target_id="page-50f-bare",
        url="https://example.test/50f-bare",
        paragraph_text="Bare durable passage survives a fresh process",
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
    selection_persistence = persist_chromium_research_paragraph_text_selection(
        selection,
        selection_path,
    )
    original_bare = load_chromium_research_paragraph_text_selection(
        source,
        selection_path,
    )

    prepared = _persist_extension(
        tmp_path,
        ordinary_reentry,
        (original_bare,),
        rationale_text="Changed basis containing one durable bare passage.",
        stem="50f",
    )
    transition = persist_chromium_research_first_changed_basis_transition(
        ordinary_reentry.controller,
        ordinary_reentry,
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
        declaration_destination=tmp_path / "50f-sequence-declaration.json",
    )

    locator = ChromiumResearchExactRangeSelectionReentryLocator(
        capture_source=source.verification.path,
        selection_source=selection_path,
    )
    result = verify_chromium_research_first_changed_basis_root_backed_reentry(
        adoption,
        ordinary_reentry,
        (locator,),
        changed_working_set_source=prepared.working_set_persistence.path,
        changed_note_source=prepared.note_persistence.path,
        transition_source=transition.persistence.path,
        root_source=root.persistence.path,
        first_edge_source=edge.persistence.path,
        declaration_source=adoption.declaration.path,
    )

    assert isinstance(result, ChromiumResearchFirstChangedBasisRootBackedReentryResult)
    assert result.plan.appended_working_set_members == (locator,)
    assert result.fresh_reentry.controller is not adoption.controller
    assert result.fresh_reentry.controller.presentation == adoption.controller.presentation

    fresh_bare = result.fresh_reentry.loaded_appended_members[0]
    assert isinstance(fresh_bare, ChromiumPageResearchLoadedParagraphTextSelectionRecord)
    assert fresh_bare is not original_bare
    assert fresh_bare.selection is not original_bare.selection
    assert fresh_bare.selection.selected_text == original_bare.selection.selected_text == "Bare"
    assert fresh_bare.selection.start_offset == original_bare.selection.start_offset == 0
    assert fresh_bare.selection.end_offset == original_bare.selection.end_offset == 4
    assert fresh_bare.verification.selection_record_sha256 == (
        original_bare.verification.selection_record_sha256
        == selection_persistence.selection_record_sha256
    )
    assert fresh_bare.verification.source_bundle_sha256 == (
        original_bare.verification.source_bundle_sha256
        == source.verification.bundle_sha256
    )
    assert fresh_bare.selection.source.verification.bundle_sha256 == (
        original_bare.selection.source.verification.bundle_sha256
        == source.verification.bundle_sha256
    )

    assert result.fresh_reentry.loaded_root.transition.successor_note.working_set.verification.working_set_format == (
        "pyxis.chromium.research_working_set.v2"
    )
    assert result.fresh_reentry.loaded_root.transition.successor_note.verification.note_format == (
        "pyxis.chromium.research_working_set_note.v2"
    )
    assert result.fresh_reentry.loaded_root.verification.root_record_sha256 == (
        root.persistence.root_record_sha256
    )
    assert result.fresh_reentry.loaded_declaration.verification.sequence_record_sha256 == (
        adoption.declaration.sequence_record_sha256
    )
    assert result.fresh_reentry.controller.declared_endpoint.verification.edge_record_sha256 == (
        edge.persistence.edge_record_sha256
    )

    fresh_items = result.fresh_reentry.controller.declared_endpoint.revision.revised_note.working_set.items
    assert fresh_items[-1] is fresh_bare
    assert fresh_items[-1] is not original_bare

    presentation = present_chromium_research_revision_edge_working_set_context(
        result.fresh_reentry.loaded_declaration,
        declared_position=1,
    )
    presented_bare = presentation.members[-1]
    assert presented_bare.member_kind == "exact_range_selection"
    assert presented_bare.human_note_text is None
    assert presented_bare.excerpts[0].text == "Bare"

    assert source.verification.path.exists()
    assert selection_path.exists()
    assert result.fresh_reentry.loaded_appended_members[0].verification.path == selection_path.resolve()
