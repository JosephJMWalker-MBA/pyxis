from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest
from textual.widgets import Button, Input, Static, TextArea

from pyxis.app import WorkspaceController, build_and_run_workspace, create_workspace_presentation
from pyxis.app.chromium_research_session_controller import ChromiumResearchSessionController
from pyxis.authoring import create_workspace_spec
from pyxis.ui import create_workspace_shell
from pyxis.ui.chromium_research_endpoint_revision_textual import (
    REVISION_AUTHORITY_NOTICE,
    ResearchEndpointRevisionControls,
)
from pyxis.ui.chromium_research_revision_edge_sequence_textual import (
    ResearchRevisionEdgeSequenceDetail,
)
from test_app_chromium_research_session_presentation import _loaded


def _research_controller(tmp_path: Path):
    prefix, v4_path, v5_path, v6_path, declaration_path, loaded = _loaded(tmp_path)
    return (
        prefix,
        v4_path,
        v5_path,
        v6_path,
        declaration_path,
        loaded,
        ChromiumResearchSessionController(loaded),
    )


def _workspace(tmp_path: Path):
    root = tmp_path / "workspace"
    spec = create_workspace_spec(
        "Research endpoint revision UI",
        "Workspace provenance remains separate from research mutation evidence.",
    )
    run = build_and_run_workspace(spec, root, "same runtime workload")
    return root, run, create_workspace_presentation(spec, run)


@pytest.mark.asyncio
async def test_research_controller_mounts_exact_session_and_endpoint_controls(
    tmp_path: Path,
) -> None:
    *_, controller = _research_controller(tmp_path)
    _, _, workspace = _workspace(tmp_path)
    shell = create_workspace_shell(workspace, research_controller=controller)

    async with shell.run_test(size=(150, 90)) as pilot:
        await pilot.pause()
        detail = shell.query_one(ResearchRevisionEdgeSequenceDetail)
        controls = shell.query_one(ResearchEndpointRevisionControls)

        assert shell.research_controller is controller
        assert shell.research_session is controller.presentation
        assert shell.research_presentation is controller.presentation.sequence
        assert detail.presentation is controller.presentation.sequence
        assert controls.prior_result is None
        assert REVISION_AUTHORITY_NOTICE in str(
            shell.query_one("#research-endpoint-revision-authority-notice", Static).content
        )
        assert not shell.query_one("#persist-research-endpoint-revision", Button).disabled


def test_research_controller_cannot_be_mixed_with_read_only_forms(tmp_path: Path) -> None:
    *_, controller = _research_controller(tmp_path)
    _, _, workspace = _workspace(tmp_path)

    with pytest.raises(ValueError, match="cannot be combined"):
        create_workspace_shell(
            workspace,
            research_controller=controller,
            research_session=controller.presentation,
        )
    with pytest.raises(ValueError, match="cannot be combined"):
        create_workspace_shell(
            workspace,
            research_controller=controller,
            research_presentation=controller.presentation.sequence,
        )
    with pytest.raises(ValueError, match="cannot be combined"):
        create_workspace_shell(
            workspace,
            research_controller=controller,
            research_working_set_contexts=controller.presentation.working_set_contexts,
        )


@pytest.mark.asyncio
async def test_read_only_session_remains_control_free(tmp_path: Path) -> None:
    *_, controller = _research_controller(tmp_path)
    _, _, workspace = _workspace(tmp_path)
    shell = create_workspace_shell(
        workspace,
        research_session=controller.presentation,
    )

    async with shell.run_test(size=(150, 80)) as pilot:
        await pilot.pause()
        assert shell.research_controller is None
        assert len(shell.query("#research-endpoint-revision-controls")) == 0
        assert len(shell.query("#persist-research-endpoint-revision")) == 0


@pytest.mark.asyncio
async def test_successful_ui_write_preserves_exact_text_locks_form_and_does_not_adopt(
    tmp_path: Path,
) -> None:
    _, _, _, v6_path, _, loaded, controller = _research_controller(tmp_path)
    _, _, workspace = _workspace(tmp_path)
    destination = tmp_path / "v7-edge.json"
    shell = create_workspace_shell(workspace, research_controller=controller)
    original_presentation = controller.presentation
    original_endpoint = controller.declared_endpoint
    revised = "  revised from UI 😀\nsecond exact line  "

    async with shell.run_test(size=(150, 95)) as pilot:
        await pilot.pause()
        shell.query_one("#research-endpoint-revised-note", TextArea).text = revised
        shell.query_one("#research-endpoint-prior-edge-source", Input).value = str(v6_path)
        shell.query_one("#research-endpoint-destination", Input).value = str(destination)
        button = shell.query_one("#persist-research-endpoint-revision", Button)
        button.focus()
        await pilot.pause()
        await pilot.press("enter")
        await pilot.pause()

        result = controller.last_endpoint_revision
        assert result is not None
        assert destination.exists()
        assert result.extension.revision.revised_note.note_text == revised
        assert result.prior_session is original_presentation
        assert controller.presentation is original_presentation
        assert controller.loaded is loaded
        assert controller.declared_endpoint is original_endpoint
        assert shell.research_session is original_presentation
        assert shell.research_presentation is original_presentation.sequence
        assert shell.query_one(ResearchRevisionEdgeSequenceDetail).presentation is (
            original_presentation.sequence
        )
        assert button.disabled
        assert shell.query_one("#research-endpoint-revised-note", TextArea).disabled
        status = str(shell.query_one("#research-endpoint-revision-status", Static).content)
        assert "declared session unchanged" in status
        assert "not adopted/current/head" in status
        assert result.persistence.edge_record_sha256 in status
        assert str(result.persistence.path) in status


@pytest.mark.asyncio
async def test_wrong_explicit_predecessor_fails_without_lock_or_false_success(
    tmp_path: Path,
) -> None:
    _, _, v5_path, _, _, _, controller = _research_controller(tmp_path)
    _, _, workspace = _workspace(tmp_path)
    destination = tmp_path / "wrong-predecessor-successor.json"
    shell = create_workspace_shell(workspace, research_controller=controller)

    async with shell.run_test(size=(150, 95)) as pilot:
        await pilot.pause()
        shell.query_one("#research-endpoint-revised-note", TextArea).text = "new wording"
        shell.query_one("#research-endpoint-prior-edge-source", Input).value = str(v5_path)
        shell.query_one("#research-endpoint-destination", Input).value = str(destination)
        button = shell.query_one("#persist-research-endpoint-revision", Button)
        button.focus()
        await pilot.pause()
        await pilot.press("enter")
        await pilot.pause()

        assert controller.last_endpoint_revision is None
        assert not destination.exists()
        assert not button.disabled
        assert not shell.query_one("#research-endpoint-revised-note", TextArea).disabled
        assert "Write failed:" in str(
            shell.query_one("#research-endpoint-revision-status", Static).content
        )


@pytest.mark.asyncio
async def test_blank_explicit_paths_are_rejected_in_ui_before_persistence(
    tmp_path: Path,
) -> None:
    *_, controller = _research_controller(tmp_path)
    _, _, workspace = _workspace(tmp_path)
    shell = create_workspace_shell(workspace, research_controller=controller)

    async with shell.run_test(size=(150, 95)) as pilot:
        await pilot.pause()
        shell.query_one("#research-endpoint-revised-note", TextArea).text = "new wording"
        button = shell.query_one("#persist-research-endpoint-revision", Button)
        button.focus()
        await pilot.pause()
        await pilot.press("enter")
        await pilot.pause()

        assert controller.last_endpoint_revision is None
        assert not button.disabled
        status = str(shell.query_one("#research-endpoint-revision-status", Static).content)
        assert "explicit durable endpoint path is required" in status


@pytest.mark.asyncio
async def test_occupied_destination_preserves_existing_bytes_and_leaves_form_active(
    tmp_path: Path,
) -> None:
    _, _, _, v6_path, _, _, controller = _research_controller(tmp_path)
    _, _, workspace = _workspace(tmp_path)
    destination = tmp_path / "occupied.json"
    destination.write_bytes(b"do-not-overwrite")
    shell = create_workspace_shell(workspace, research_controller=controller)

    async with shell.run_test(size=(150, 95)) as pilot:
        await pilot.pause()
        shell.query_one("#research-endpoint-revised-note", TextArea).text = "new wording"
        shell.query_one("#research-endpoint-prior-edge-source", Input).value = str(v6_path)
        shell.query_one("#research-endpoint-destination", Input).value = str(destination)
        button = shell.query_one("#persist-research-endpoint-revision", Button)
        button.focus()
        await pilot.pause()
        await pilot.press("enter")
        await pilot.pause()

        assert controller.last_endpoint_revision is None
        assert destination.read_bytes() == b"do-not-overwrite"
        assert not button.disabled
        assert "Write failed:" in str(
            shell.query_one("#research-endpoint-revision-status", Static).content
        )


@pytest.mark.asyncio
async def test_controller_with_prior_success_mounts_locked_receipt(tmp_path: Path) -> None:
    _, _, _, v6_path, _, _, controller = _research_controller(tmp_path)
    destination = tmp_path / "prior-success.json"
    result = controller.persist_declared_endpoint_revision(
        "prior successful UI-independent revision",
        prior_edge_source=v6_path,
        destination=destination,
    )
    _, _, workspace = _workspace(tmp_path)
    shell = create_workspace_shell(workspace, research_controller=controller)

    async with shell.run_test(size=(150, 95)) as pilot:
        await pilot.pause()
        controls = shell.query_one(ResearchEndpointRevisionControls)
        assert controls.prior_result is result
        assert shell.query_one("#persist-research-endpoint-revision", Button).disabled
        assert shell.query_one("#research-endpoint-revised-note", TextArea).disabled
        assert shell.query_one("#research-endpoint-prior-edge-source", Input).disabled
        assert shell.query_one("#research-endpoint-destination", Input).disabled
        status = str(shell.query_one("#research-endpoint-revision-status", Static).content)
        assert result.persistence.edge_record_sha256 in status
        assert "Reopen and explicitly redeclare" in status


@pytest.mark.asyncio
async def test_workspace_runtime_rerun_preserves_exact_research_controller_and_session(
    tmp_path: Path,
) -> None:
    *_, research_controller = _research_controller(tmp_path)
    root, run, workspace = _workspace(tmp_path)
    workspace_controller = WorkspaceController(root, run)
    shell = create_workspace_shell(
        workspace,
        controller=workspace_controller,
        research_controller=research_controller,
    )
    original_session = research_controller.presentation

    async with shell.run_test(size=(150, 95)) as pilot:
        await pilot.pause()
        runtime_input = shell.query_one("#runtime-input", Input)
        runtime_input.value = "changed runtime input"
        runtime_input.focus()
        await pilot.pause()
        await pilot.press("enter")
        await pilot.pause()

        assert shell.research_controller is research_controller
        assert shell.research_session is original_session
        assert shell.research_presentation is original_session.sequence
        assert research_controller.presentation is original_session
        assert len(shell.query("#research-endpoint-revision-controls")) == 1


def test_forged_controller_presentation_is_rejected_before_mutating_shell_mount(
    tmp_path: Path,
) -> None:
    *_, controller = _research_controller(tmp_path)
    controller._presentation = replace(  # noqa: SLF001 - deliberate adversarial test
        controller.presentation,
        presentation_mode="forged-controller-session-mode",
    )
    _, _, workspace = _workspace(tmp_path)

    with pytest.raises(ValueError, match="incoherent with its retained loaded evidence"):
        create_workspace_shell(workspace, research_controller=controller)
