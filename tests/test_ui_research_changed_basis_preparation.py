from __future__ import annotations

from pathlib import Path

import pytest
from textual.widgets import Button, Input, Static, TextArea

from pyxis.app.chromium_research_changed_basis_candidate_presentation import (
    present_chromium_research_changed_basis_candidate,
)
from pyxis.ui import create_research_session_shell
from pyxis.ui.chromium_research_changed_basis_preparation_textual import (
    ResearchChangedBasisPreparationControls,
)
from test_app_chromium_research_session_working_set_extension import (
    _new_paragraph_member,
    _session,
)


async def _press(shell, pilot, button_id: str) -> None:
    button = shell.query_one(f"#{button_id}", Button)
    button.focus()
    await pilot.pause()
    await pilot.press("enter")
    await pilot.pause()


def test_candidate_projection_retains_exact_loaded_items_without_declared_position_authority(
    tmp_path: Path,
) -> None:
    _, reentry = _session(tmp_path)
    first, first_path = _new_paragraph_member(tmp_path, stem="candidate-a")
    second, _ = _new_paragraph_member(
        tmp_path,
        stem="candidate-b",
        paragraph_text="Second candidate paragraph",
        note_text="Second candidate note.",
    )

    first_path.unlink()
    presentation = present_chromium_research_changed_basis_candidate(
        reentry.controller,
        (second, first, second),
    )

    assert presentation.presentation_mode == "read_only_candidate_appended_research_evidence"
    assert presentation.candidate_role == "candidate_not_yet_working_set_or_adopted"
    assert presentation.candidate_member_count == 3
    assert [member.member_position for member in presentation.members] == [1, 2, 3]
    assert presentation.members[0].human_note_text == "Second candidate note."
    assert presentation.members[1].human_note_text == "New explicit evidence member."
    assert presentation.members[2].human_note_text == "Second candidate note."
    assert not hasattr(presentation, "declared_position")
    assert not hasattr(presentation, "edge_record_sha256")
    assert not hasattr(presentation, "transition")
    assert not hasattr(presentation, "epoch")


@pytest.mark.asyncio
async def test_configured_shell_renders_blank_preparation_inputs_and_persists_without_adoption(
    tmp_path: Path,
) -> None:
    _, reentry = _session(tmp_path)
    member, _ = _new_paragraph_member(tmp_path, stem="candidate-save")
    controller = reentry.controller
    original_session = controller.presentation
    original_endpoint = controller.declared_endpoint
    shell = create_research_session_shell(controller)
    presentation = shell.configure_changed_basis_candidate((member,))
    working_set_destination = tmp_path / "prepared-working-set.json"
    note_destination = tmp_path / "prepared-working-set-note.json"

    assert shell.changed_basis_candidate_items == (member,)
    assert shell.changed_basis_candidate_items[0] is member
    assert shell.changed_basis_candidate_presentation is presentation

    async with shell.run_test(size=(160, 150)) as pilot:
        await pilot.pause()
        controls = shell.query_one(ResearchChangedBasisPreparationControls)
        candidate_text = str(
            shell.query_one("#research-changed-basis-candidate", Static).content
        )
        assert "CANDIDATE APPENDED MEMBERS" in candidate_text
        assert "NOT YET WORKING SET / NOT ADOPTED" in candidate_text
        assert shell.query_one("#research-changed-basis-rationale", TextArea).text == ""
        assert shell.query_one(
            "#research-changed-basis-working-set-destination", Input
        ).value == ""
        assert shell.query_one("#research-changed-basis-note-destination", Input).value == ""
        assert not controls.stale
        assert controls.result is None

        exact_rationale = "  New evidence changes the basis 😀\nStill provisional.  "
        shell.query_one("#research-changed-basis-rationale", TextArea).text = exact_rationale
        shell.query_one(
            "#research-changed-basis-working-set-destination", Input
        ).value = str(working_set_destination)
        shell.query_one("#research-changed-basis-note-destination", Input).value = str(
            note_destination
        )
        await _press(shell, pilot, "persist-research-changed-basis-preparation")

        result = shell.last_changed_basis_preparation
        assert result is not None
        assert result.prior_session is original_session
        assert result.prior_endpoint is original_endpoint
        assert result.appended_items == (member,)
        assert result.appended_items[0] is member
        assert result.note.note_text == exact_rationale
        assert shell.research_controller is controller
        assert shell.research_session is original_session
        assert shell.research_controller.declared_endpoint is original_endpoint
        assert controls.result is result
        assert shell.query_one(
            "#persist-research-changed-basis-preparation", Button
        ).disabled
        receipt = str(shell.query_one("#research-changed-basis-status", Static).content)
        assert "displayed governed session unchanged" in receipt
        assert "not transitioned/adopted/current/latest/head" in receipt
        assert working_set_destination.exists()
        assert note_destination.exists()
        assert len(shell.query("#research-changed-basis-transition")) == 0
        assert len(shell.query("#adopt-research-changed-basis")) == 0


@pytest.mark.asyncio
async def test_unadopted_endpoint_revision_does_not_stale_changed_basis_candidate(
    tmp_path: Path,
) -> None:
    fixture, reentry = _session(tmp_path)
    member, _ = _new_paragraph_member(tmp_path, stem="candidate-unadopted")
    controller = reentry.controller
    original_endpoint = controller.declared_endpoint
    shell = create_research_session_shell(controller)
    shell.configure_changed_basis_candidate((member,))
    successor = tmp_path / "unadopted-successor.json"

    async with shell.run_test(size=(160, 155)) as pilot:
        await pilot.pause()
        shell.query_one("#research-endpoint-revised-note", TextArea).text = (
            "Unadopted successor does not retarget 44A."
        )
        shell.query_one("#research-endpoint-prior-edge-source", Input).value = str(
            fixture.v6_path
        )
        shell.query_one("#research-endpoint-destination", Input).value = str(successor)
        await _press(shell, pilot, "persist-research-endpoint-revision")

        controls = shell.query_one(ResearchChangedBasisPreparationControls)
        assert controller.last_endpoint_revision is not None
        assert controller.declared_endpoint is original_endpoint
        assert not controls.stale
        assert not shell.query_one(
            "#persist-research-changed-basis-preparation", Button
        ).disabled

        working_set_destination = tmp_path / "unadopted-working-set.json"
        note_destination = tmp_path / "unadopted-working-set-note.json"
        shell.query_one("#research-changed-basis-rationale", TextArea).text = (
            "Candidate remains based on the declared endpoint."
        )
        shell.query_one(
            "#research-changed-basis-working-set-destination", Input
        ).value = str(working_set_destination)
        shell.query_one("#research-changed-basis-note-destination", Input).value = str(
            note_destination
        )
        await _press(shell, pilot, "persist-research-changed-basis-preparation")

        result = shell.last_changed_basis_preparation
        assert result is not None
        assert result.prior_endpoint is original_endpoint
        assert result.prior_endpoint is not controller.last_endpoint_revision.extension.revision


@pytest.mark.asyncio
async def test_adopted_rollover_stales_unsaved_changed_basis_candidate_instead_of_retargeting(
    tmp_path: Path,
) -> None:
    fixture, reentry = _session(tmp_path)
    member, _ = _new_paragraph_member(tmp_path, stem="candidate-stale")
    controller = reentry.controller
    successor = tmp_path / "chosen-successor.json"
    controller.persist_declared_endpoint_revision(
        "Chosen ordinary continuation.",
        prior_edge_source=fixture.v6_path,
        destination=successor,
    )
    shell = create_research_session_shell(controller)
    shell.configure_changed_basis_candidate((member,))
    declaration = tmp_path / "chosen-continuation-declaration.json"

    async with shell.run_test(size=(160, 160)) as pilot:
        await pilot.pause()
        shell.query_one("#research-session-rollover-successor-source", Input).value = str(
            successor
        )
        shell.query_one(
            "#research-session-rollover-declaration-destination", Input
        ).value = str(declaration)
        await _press(shell, pilot, "rollover-research-session")

        controls = shell.query_one(ResearchChangedBasisPreparationControls)
        assert shell.research_controller is not controller
        assert controls.stale
        assert controls.result is None
        assert shell.query_one("#research-changed-basis-rationale", TextArea).disabled
        assert shell.query_one(
            "#research-changed-basis-working-set-destination", Input
        ).disabled
        assert shell.query_one("#research-changed-basis-note-destination", Input).disabled
        assert shell.query_one(
            "#persist-research-changed-basis-preparation", Button
        ).disabled
        status = str(shell.query_one("#research-changed-basis-status", Static).content)
        assert "will not silently retarget" in status
        assert shell.last_changed_basis_preparation is None


@pytest.mark.asyncio
async def test_default_shell_mounts_no_changed_basis_surface_without_explicit_candidate(
    tmp_path: Path,
) -> None:
    _, reentry = _session(tmp_path)
    shell = create_research_session_shell(reentry.controller)

    async with shell.run_test(size=(150, 100)) as pilot:
        await pilot.pause()
        assert len(shell.query(ResearchChangedBasisPreparationControls)) == 0
        assert shell.changed_basis_candidate_items is None
        assert shell.changed_basis_candidate_presentation is None
        assert shell.last_changed_basis_preparation is None
