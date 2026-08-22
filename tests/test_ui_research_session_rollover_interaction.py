from __future__ import annotations

from pathlib import Path

import pytest
from textual.widgets import Button, Input, Static, TextArea

from pyxis.app import WorkspaceController
from pyxis.ui import create_workspace_shell
from pyxis.ui.chromium_research_endpoint_revision_textual import (
    ResearchEndpointRevisionControls,
)
from pyxis.ui.chromium_research_revision_edge_sequence_textual import (
    ResearchRevisionEdgeSequenceDetail,
)
from pyxis.ui.chromium_research_session_rollover_textual import (
    ROLLOVER_AUTHORITY_NOTICE,
    ResearchSessionRolloverControls,
)
from test_ui_research_endpoint_revision_interaction import (
    _research_controller,
    _workspace,
)


async def _press(shell, pilot, button_id: str) -> None:
    button = shell.query_one(f"#{button_id}", Button)
    button.focus()
    await pilot.pause()
    await pilot.press("enter")
    await pilot.pause()


def _prior_success(tmp_path: Path, *, text: str = "v7 chosen in UI rollover"):
    _, _, _, v6_path, old_declaration, loaded, controller = _research_controller(tmp_path)
    successor = tmp_path / "v7.json"
    result = controller.persist_declared_endpoint_revision(
        text,
        prior_edge_source=v6_path,
        destination=successor,
    )
    return v6_path, old_declaration, loaded, controller, result, successor


@pytest.mark.asyncio
async def test_rollover_controls_start_disabled_without_successor_and_infer_no_paths(
    tmp_path: Path,
) -> None:
    *_, controller = _research_controller(tmp_path)
    _, _, workspace = _workspace(tmp_path)
    shell = create_workspace_shell(workspace, research_controller=controller)

    async with shell.run_test(size=(150, 105)) as pilot:
        await pilot.pause()
        controls = shell.query_one(ResearchSessionRolloverControls)
        successor_source = shell.query_one(
            "#research-session-rollover-successor-source", Input
        )
        declaration_destination = shell.query_one(
            "#research-session-rollover-declaration-destination", Input
        )

        assert controls.candidate_revision is None
        assert successor_source.disabled
        assert declaration_destination.disabled
        assert successor_source.value == ""
        assert declaration_destination.value == ""
        assert shell.query_one("#rollover-research-session", Button).disabled
        assert ROLLOVER_AUTHORITY_NOTICE in str(
            shell.query_one(
                "#research-session-rollover-authority-notice", Static
            ).content
        )


@pytest.mark.asyncio
async def test_successful_ui_successor_write_enables_exact_rollover_candidate_without_path_inference(
    tmp_path: Path,
) -> None:
    _, _, _, v6_path, _, _, controller = _research_controller(tmp_path)
    _, _, workspace = _workspace(tmp_path)
    successor = tmp_path / "v7-ui.json"
    shell = create_workspace_shell(workspace, research_controller=controller)

    async with shell.run_test(size=(150, 115)) as pilot:
        await pilot.pause()
        shell.query_one("#research-endpoint-revised-note", TextArea).text = (
            "  v7 exact UI successor 😀\nline two  "
        )
        shell.query_one("#research-endpoint-prior-edge-source", Input).value = str(v6_path)
        shell.query_one("#research-endpoint-destination", Input).value = str(successor)
        await _press(shell, pilot, "persist-research-endpoint-revision")

        result = controller.last_endpoint_revision
        controls = shell.query_one(ResearchSessionRolloverControls)
        successor_source = shell.query_one(
            "#research-session-rollover-successor-source", Input
        )
        declaration_destination = shell.query_one(
            "#research-session-rollover-declaration-destination", Input
        )

        assert result is not None
        assert controls.candidate_revision is result
        assert not successor_source.disabled
        assert not declaration_destination.disabled
        assert successor_source.value == ""
        assert declaration_destination.value == ""
        assert not shell.query_one("#rollover-research-session", Button).disabled
        candidate = str(
            shell.query_one("#research-session-rollover-candidate", Static).content
        )
        assert result.persistence.edge_record_sha256 in candidate
        assert "Other sibling successors, if any, are not discovered" in candidate


@pytest.mark.asyncio
async def test_successful_rollover_replaces_only_research_surface_with_new_continuation_controller(
    tmp_path: Path,
) -> None:
    _, old_declaration, loaded, controller, revision, successor = _prior_success(tmp_path)
    _, _, workspace = _workspace(tmp_path)
    declaration = tmp_path / "v7-continuation.json"
    old_presentation = controller.presentation
    old_endpoint = controller.declared_endpoint
    old_declaration_bytes = old_declaration.read_bytes()
    shell = create_workspace_shell(workspace, research_controller=controller)

    async with shell.run_test(size=(150, 120)) as pilot:
        await pilot.pause()
        shell.query_one("#research-session-rollover-successor-source", Input).value = str(
            successor
        )
        shell.query_one(
            "#research-session-rollover-declaration-destination", Input
        ).value = str(declaration)
        await _press(shell, pilot, "rollover-research-session")

        rollover = shell.last_research_rollover
        assert rollover is not None
        continuation = rollover.continuation_controller
        assert rollover.prior_controller is controller
        assert rollover.prior_revision is revision
        assert shell.research_controller is continuation
        assert shell.research_session is continuation.presentation
        assert shell.research_presentation is continuation.presentation.sequence
        assert shell.research_working_set_contexts == (
            continuation.presentation.working_set_contexts
        )
        assert continuation.declared_endpoint.revision.revised_note.note_text == (
            revision.extension.revision.revised_note.note_text
        )
        assert len(continuation.presentation.sequence.members) == 1
        assert shell.query_one(ResearchRevisionEdgeSequenceDetail).presentation is (
            continuation.presentation.sequence
        )
        assert controller.loaded is loaded
        assert controller.presentation is old_presentation
        assert controller.declared_endpoint is old_endpoint
        assert controller.last_endpoint_revision is revision
        assert old_declaration.read_bytes() == old_declaration_bytes
        assert declaration.exists()

        revision_controls = shell.query_one(ResearchEndpointRevisionControls)
        rollover_controls = shell.query_one(ResearchSessionRolloverControls)
        assert revision_controls.prior_result is None
        assert not shell.query_one("#persist-research-endpoint-revision", Button).disabled
        assert rollover_controls.candidate_revision is None
        assert shell.query_one("#rollover-research-session", Button).disabled
        receipt = str(shell.query_one("#research-rollover-success-receipt", Static).content)
        assert revision.persistence.edge_record_sha256 in receipt
        assert rollover.declaration.sequence_record_sha256 in receipt
        assert "not a global latest/current/head claim" in receipt


@pytest.mark.asyncio
async def test_moved_identical_successor_can_be_explicitly_selected_for_ui_rollover(
    tmp_path: Path,
) -> None:
    _, _, _, controller, revision, successor = _prior_success(tmp_path)
    moved = tmp_path / "moved" / "renamed-v7.edge"
    moved.parent.mkdir()
    moved.write_bytes(successor.read_bytes())
    successor.unlink()
    _, _, workspace = _workspace(tmp_path)
    shell = create_workspace_shell(workspace, research_controller=controller)

    async with shell.run_test(size=(150, 115)) as pilot:
        await pilot.pause()
        shell.query_one("#research-session-rollover-successor-source", Input).value = str(
            moved
        )
        shell.query_one(
            "#research-session-rollover-declaration-destination", Input
        ).value = str(tmp_path / "moved-continuation.json")
        await _press(shell, pilot, "rollover-research-session")

        assert shell.last_research_rollover is not None
        assert shell.last_research_rollover.prior_revision is revision
        assert shell.research_controller is (
            shell.last_research_rollover.continuation_controller
        )
        assert not successor.exists()
        assert moved.exists()


@pytest.mark.asyncio
async def test_wrong_sibling_file_rejects_without_replacing_displayed_session(
    tmp_path: Path,
) -> None:
    _, _, _, v6_path, _, loaded, controller = _research_controller(tmp_path)
    first_path = tmp_path / "v7-first.json"
    second_path = tmp_path / "v7-second.json"
    controller.persist_declared_endpoint_revision(
        "first sibling",
        prior_edge_source=v6_path,
        destination=first_path,
    )
    selected = controller.persist_declared_endpoint_revision(
        "second displayed sibling",
        prior_edge_source=v6_path,
        destination=second_path,
    )
    _, _, workspace = _workspace(tmp_path)
    shell = create_workspace_shell(workspace, research_controller=controller)
    original_presentation = controller.presentation
    destination = tmp_path / "wrong-sibling-declaration.json"

    async with shell.run_test(size=(150, 115)) as pilot:
        await pilot.pause()
        controls = shell.query_one(ResearchSessionRolloverControls)
        assert controls.candidate_revision is selected
        shell.query_one("#research-session-rollover-successor-source", Input).value = str(
            first_path
        )
        shell.query_one(
            "#research-session-rollover-declaration-destination", Input
        ).value = str(destination)
        await _press(shell, pilot, "rollover-research-session")

        assert shell.last_research_rollover is None
        assert shell.research_controller is controller
        assert shell.research_session is original_presentation
        assert shell.research_presentation is original_presentation.sequence
        assert controller.loaded is loaded
        assert not destination.exists()
        assert not shell.query_one("#rollover-research-session", Button).disabled
        assert "Continuation failed:" in str(
            shell.query_one("#research-session-rollover-status", Static).content
        )


@pytest.mark.asyncio
async def test_blank_rollover_paths_reject_before_30a_without_state_change(
    tmp_path: Path,
) -> None:
    _, _, _, controller, revision, _ = _prior_success(tmp_path)
    _, _, workspace = _workspace(tmp_path)
    shell = create_workspace_shell(workspace, research_controller=controller)

    async with shell.run_test(size=(150, 110)) as pilot:
        await pilot.pause()
        await _press(shell, pilot, "rollover-research-session")

        assert shell.last_research_rollover is None
        assert shell.research_controller is controller
        assert controller.last_endpoint_revision is revision
        status = str(shell.query_one("#research-session-rollover-status", Static).content)
        assert "explicit successor edge path is required" in status
        assert not shell.query_one("#rollover-research-session", Button).disabled


@pytest.mark.asyncio
async def test_occupied_declaration_destination_is_no_overwrite_and_keeps_old_session(
    tmp_path: Path,
) -> None:
    _, _, _, controller, _, successor = _prior_success(tmp_path)
    _, _, workspace = _workspace(tmp_path)
    occupied = tmp_path / "occupied-declaration.json"
    occupied.write_bytes(b"do-not-overwrite")
    shell = create_workspace_shell(workspace, research_controller=controller)
    original_session = controller.presentation

    async with shell.run_test(size=(150, 115)) as pilot:
        await pilot.pause()
        shell.query_one("#research-session-rollover-successor-source", Input).value = str(
            successor
        )
        shell.query_one(
            "#research-session-rollover-declaration-destination", Input
        ).value = str(occupied)
        await _press(shell, pilot, "rollover-research-session")

        assert occupied.read_bytes() == b"do-not-overwrite"
        assert shell.last_research_rollover is None
        assert shell.research_controller is controller
        assert shell.research_session is original_session
        assert "Continuation failed:" in str(
            shell.query_one("#research-session-rollover-status", Static).content
        )


@pytest.mark.asyncio
async def test_read_only_research_session_remains_free_of_mutation_and_rollover_controls(
    tmp_path: Path,
) -> None:
    *_, controller = _research_controller(tmp_path)
    _, _, workspace = _workspace(tmp_path)
    shell = create_workspace_shell(workspace, research_session=controller.presentation)

    async with shell.run_test(size=(150, 90)) as pilot:
        await pilot.pause()
        assert shell.research_controller is None
        assert len(shell.query("#research-endpoint-revision-controls")) == 0
        assert len(shell.query("#research-session-rollover-controls")) == 0
        assert len(shell.query("#rollover-research-session")) == 0


@pytest.mark.asyncio
async def test_workspace_runtime_rerun_after_rollover_preserves_exact_new_research_session(
    tmp_path: Path,
) -> None:
    _, _, _, controller, _, successor = _prior_success(tmp_path)
    root, run, workspace = _workspace(tmp_path)
    workspace_controller = WorkspaceController(root, run)
    shell = create_workspace_shell(
        workspace,
        controller=workspace_controller,
        research_controller=controller,
    )

    async with shell.run_test(size=(150, 120)) as pilot:
        await pilot.pause()
        shell.query_one("#research-session-rollover-successor-source", Input).value = str(
            successor
        )
        shell.query_one(
            "#research-session-rollover-declaration-destination", Input
        ).value = str(tmp_path / "runtime-independent-continuation.json")
        await _press(shell, pilot, "rollover-research-session")
        continuation = shell.research_controller
        continuation_session = shell.research_session
        assert continuation is not None

        runtime_input = shell.query_one("#runtime-input", Input)
        runtime_input.value = "Workspace changed after research rollover"
        runtime_input.focus()
        await pilot.pause()
        await pilot.press("enter")
        await pilot.pause()

        assert shell.research_controller is continuation
        assert shell.research_session is continuation_session
        assert shell.research_presentation is continuation_session.sequence
        assert shell.query_one(ResearchRevisionEdgeSequenceDetail).presentation is (
            continuation_session.sequence
        )


@pytest.mark.asyncio
async def test_ui_can_repeat_write_rollover_cycle_without_latest_or_head_state(
    tmp_path: Path,
) -> None:
    _, _, _, controller, _, v7 = _prior_success(tmp_path, text="v7 first continuation")
    _, _, workspace = _workspace(tmp_path)
    shell = create_workspace_shell(workspace, research_controller=controller)

    async with shell.run_test(size=(150, 135)) as pilot:
        await pilot.pause()
        shell.query_one("#research-session-rollover-successor-source", Input).value = str(v7)
        shell.query_one(
            "#research-session-rollover-declaration-destination", Input
        ).value = str(tmp_path / "v7-declaration.json")
        await _press(shell, pilot, "rollover-research-session")

        v7_controller = shell.research_controller
        assert v7_controller is not None
        v8 = tmp_path / "v8.json"
        shell.query_one("#research-endpoint-revised-note", TextArea).text = (
            "v8 second explicit continuation"
        )
        shell.query_one("#research-endpoint-prior-edge-source", Input).value = str(v7)
        shell.query_one("#research-endpoint-destination", Input).value = str(v8)
        await _press(shell, pilot, "persist-research-endpoint-revision")

        v8_revision = v7_controller.last_endpoint_revision
        assert v8_revision is not None
        assert shell.query_one(ResearchSessionRolloverControls).candidate_revision is v8_revision
        shell.query_one("#research-session-rollover-successor-source", Input).value = str(v8)
        shell.query_one(
            "#research-session-rollover-declaration-destination", Input
        ).value = str(tmp_path / "v8-declaration.json")
        await _press(shell, pilot, "rollover-research-session")

        v8_controller = shell.research_controller
        assert v8_controller is not None
        assert v8_controller is not v7_controller
        assert v8_controller.declared_endpoint.revision.revised_note.note_text == (
            "v8 second explicit continuation"
        )
        assert v8_controller.last_endpoint_revision is None
        assert shell.last_research_rollover is not None
        assert shell.last_research_rollover.prior_controller is v7_controller
        assert shell.last_research_rollover.prior_revision is v8_revision
        assert not hasattr(shell, "current_head")
        assert not hasattr(shell, "latest_research_revision")
