from __future__ import annotations

from pathlib import Path

import pytest
from textual.widgets import Input, Static, TextArea

from pyxis.ui import create_first_changed_basis_session_adoption_research_session_shell
from test_app_chromium_research_session_working_set_extension import _session
from test_app_chromium_research_working_set import _loaded_bare_selection
from test_ui_research_first_changed_basis_session_adoption import _build_44d_ui
from test_ui_research_first_changed_basis_transition import _press


@pytest.mark.asyncio
async def test_50e_existing_first_changed_basis_shell_adopts_bare_saved_passage(
    tmp_path: Path,
) -> None:
    fixture, reentry = _session(tmp_path)
    bare, bare_path = _loaded_bare_selection(
        tmp_path,
        paragraph_text="Bare evidence carried through governed adoption",
        start_offset=0,
        end_offset=4,
    )
    shell = create_first_changed_basis_session_adoption_research_session_shell(
        reentry,
        (bare,),
    )
    original_controller = shell.research_controller
    bare_path.unlink()

    async with shell.run_test(size=(210, 450)) as pilot:
        await pilot.pause()

        candidate_text = str(
            shell.query_one("#research-changed-basis-candidate", Static).content
        )
        assert "Candidate member 1: exact_range_selection" in candidate_text
        assert "Human note: none attached — saved source passage only" in candidate_text
        assert "Human note: None" not in candidate_text
        assert "Excerpt: Bare" in candidate_text
        assert shell.research_controller is original_controller

        prepared, root, edge, edge_path = await _build_44d_ui(
            shell,
            pilot,
            fixture,
            tmp_path,
            stem="50e-bare",
        )

        assert prepared.appended_items == (bare,)
        assert prepared.appended_items[0] is bare
        assert prepared.working_set.items[-1] is bare
        assert prepared.working_set_persistence.working_set_format == (
            "pyxis.chromium.research_working_set.v2"
        )
        assert prepared.note_persistence.note_format == (
            "pyxis.chromium.research_working_set_note.v2"
        )
        assert root.transition_result.persistence.transition_format == (
            "pyxis.chromium.research_session_working_set_transition.v1"
        )
        assert root.persistence.root_format == (
            "pyxis.chromium.research_session_working_set_transition_revision_root.v1"
        )
        assert edge.persistence.edge_format == (
            "pyxis.chromium.research_working_set_note_revision_edge.v1"
        )
        assert edge.loaded_edge.revision.revised_note.working_set.items[-1] is bare
        assert not bare.verification.path.exists()
        assert shell.research_controller is original_controller

        declaration = tmp_path / "50e-root-started-sequence.json"
        shell.query_one(
            "#research-first-changed-basis-session-adoption-edge-source",
            Input,
        ).value = str(edge_path)
        shell.query_one(
            "#research-first-changed-basis-session-adoption-declaration-destination",
            Input,
        ).value = str(declaration)
        await _press(shell, pilot, "adopt-research-first-changed-basis-session")

        result = shell.last_first_changed_basis_session_adoption
        assert result is not None
        assert result.edge_result is edge
        assert result.declaration.sequence_format == (
            "pyxis.chromium.research_working_set_note_revision_edge_sequence.v1"
        )
        assert result.loaded_declaration.verification.sequence_format == (
            "pyxis.chromium.research_working_set_note_revision_edge_sequence.v1"
        )
        assert shell.research_controller is result.controller
        assert shell.research_controller is not original_controller
        assert shell.research_controller.declared_endpoint is result.controller.declared_endpoint
        assert (
            result.controller.declared_endpoint.verification.edge_record_sha256
            == edge.persistence.edge_record_sha256
        )
        adopted_items = result.controller.declared_endpoint.revision.revised_note.working_set.items
        assert adopted_items[-1] is bare
        assert any(item is bare for item in adopted_items)

        rendered = tuple(str(widget.content) for widget in shell.query(Static))
        assert "No human note attached — saved source passage only" in rendered
        assert any(
            "Working-set member" in value and "exact_range_selection" in value
            for value in rendered
        )
        assert declaration.exists()
        assert not bare.verification.path.exists()

        successor = tmp_path / "50e-ordinary-post-adoption-edge.json"
        shell.query_one("#research-endpoint-revised-note", TextArea).text = (
            "Ordinary governed revision after adopting the bare-passage changed basis."
        )
        shell.query_one("#research-endpoint-prior-edge-source", Input).value = str(edge_path)
        shell.query_one("#research-endpoint-destination", Input).value = str(successor)
        await _press(shell, pilot, "persist-research-endpoint-revision")

        assert successor.exists()
        assert shell.research_controller.declared_endpoint.revision.revised_note.working_set.items[-1] is bare
