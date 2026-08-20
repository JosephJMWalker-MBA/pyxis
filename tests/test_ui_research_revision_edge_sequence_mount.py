from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest
from textual.widgets import Button, Input, Static

from pyxis.app import WorkspaceController, build_and_run_workspace, create_workspace_presentation
from pyxis.app.chromium_research_working_set_note_revision_edge_sequence_presentation import (
    present_chromium_research_working_set_note_revision_edge_sequence_declaration,
)
from pyxis.authoring import create_workspace_spec
from pyxis.ui import WorkspaceShell as ExportedWorkspaceShell
from pyxis.ui import create_workspace_shell
from pyxis.ui.chromium_research_revision_edge_sequence_textual import (
    INDEPENDENT_RESEARCH_NOTICE,
    ResearchRevisionEdgeSequenceDetail,
)
from pyxis.ui.research_workspace_shell import WorkspaceShell as ResearchWorkspaceShell
from pyxis.ui.workspace_shell import WorkspaceShell as BaseWorkspaceShell
from test_app_chromium_research_working_set_note_revision_edge_sequence_presentation import (
    _loaded_declared_sequence,
)


def _research_presentation(tmp_path: Path):
    _, _, _, _, _, loaded = _loaded_declared_sequence(tmp_path)
    return present_chromium_research_working_set_note_revision_edge_sequence_declaration(
        loaded
    )


def _workspace(tmp_path: Path, *, name: str = "Research UI"):
    root = tmp_path / name.lower().replace(" ", "-")
    spec = create_workspace_spec(name, "Workspace identity is separate from research evidence.")
    run = build_and_run_workspace(spec, root, "same runtime workload")
    return root, spec, run, create_workspace_presentation(spec, run)


@pytest.mark.asyncio
async def test_workspace_shell_mounts_supplied_research_presentation_verbatim(
    tmp_path: Path,
) -> None:
    research = _research_presentation(tmp_path)
    _, _, _, workspace = _workspace(tmp_path)
    shell = create_workspace_shell(workspace, research_presentation=research)

    assert shell.research_presentation is research

    async with shell.run_test(size=(130, 55)) as pilot:
        await pilot.pause()
        detail = shell.query_one(ResearchRevisionEdgeSequenceDetail)
        assert detail.presentation is research
        assert str(shell.query_one("#research-sequence-note-1", Static).content) == (
            "  v5 exact human wording 😀  "
        )
        assert str(shell.query_one("#research-sequence-note-2", Static).content) == (
            "v6 exact human wording\nStill tentative."
        )
        assert research.declaration_record_sha256 in str(
            shell.query_one("#research-sequence-declaration-identity", Static).content
        )


@pytest.mark.asyncio
async def test_research_panel_states_independent_workspace_boundary(tmp_path: Path) -> None:
    research = _research_presentation(tmp_path)
    _, _, _, workspace = _workspace(tmp_path)
    shell = create_workspace_shell(workspace, research_presentation=research)

    async with shell.run_test(size=(120, 45)) as pilot:
        await pilot.pause()
        notice = str(
            shell.query_one("#research-sequence-independence-notice", Static).content
        )
        assert notice == INDEPENDENT_RESEARCH_NOTICE
        assert "no association with this Workspace is asserted" in notice
        assert "independently supplied" in notice.lower()


@pytest.mark.asyncio
async def test_workspace_shell_omits_research_panel_when_none_is_supplied(
    tmp_path: Path,
) -> None:
    _, _, _, workspace = _workspace(tmp_path)
    shell = create_workspace_shell(workspace)

    async with shell.run_test(size=(100, 30)) as pilot:
        await pilot.pause()
        assert len(shell.query(ResearchRevisionEdgeSequenceDetail)) == 0
        assert shell.research_presentation is None


def test_workspace_shell_rejects_wrong_research_presentation_type(tmp_path: Path) -> None:
    _, _, _, workspace = _workspace(tmp_path)

    with pytest.raises(TypeError, match="ChromiumPageResearchRevisionEdgeSequencePresentation"):
        create_workspace_shell(workspace, research_presentation=object())  # type: ignore[arg-type]


def test_workspace_shell_rejects_forged_noncontiguous_declared_positions(
    tmp_path: Path,
) -> None:
    research = _research_presentation(tmp_path)
    forged_first = replace(research.members[0], declared_position=2)
    forged = replace(research, members=(forged_first, *research.members[1:]))
    _, _, _, workspace = _workspace(tmp_path)

    with pytest.raises(ValueError, match="contiguous declaration positions"):
        create_workspace_shell(workspace, research_presentation=forged)


@pytest.mark.asyncio
async def test_research_panel_adds_no_controls_or_mutation_surface(tmp_path: Path) -> None:
    research = _research_presentation(tmp_path)
    root, _, run, workspace = _workspace(tmp_path)
    controller = WorkspaceController(root, run)
    shell = create_workspace_shell(
        workspace,
        controller=controller,
        research_presentation=research,
    )

    async with shell.run_test(size=(120, 55)) as pilot:
        await pilot.pause()
        detail = shell.query_one(ResearchRevisionEdgeSequenceDetail)
        assert len(detail.query(Button)) == 0
        assert len(detail.query(Input)) == 0
        assert {button.id for button in shell.query(Button)} == {
            "preview-remove-normalize-text",
            "preview-add-split-lines",
            "refresh-export",
        }
        assert {widget.id for widget in shell.query(Input)} == {
            "runtime-input",
            "export-destination",
        }


@pytest.mark.asyncio
async def test_workspace_runtime_rerun_preserves_exact_research_presentation(
    tmp_path: Path,
) -> None:
    research = _research_presentation(tmp_path)
    root, _, run, workspace = _workspace(tmp_path)
    controller = WorkspaceController(root, run)
    shell = create_workspace_shell(
        workspace,
        controller=controller,
        research_presentation=research,
    )

    async with shell.run_test(size=(120, 55)) as pilot:
        await pilot.pause()
        detail = shell.query_one(ResearchRevisionEdgeSequenceDetail)
        runtime_input = shell.query_one("#runtime-input", Input)
        runtime_input.value = "different runtime input"
        runtime_input.focus()
        await pilot.press("enter")
        await pilot.pause()

        assert shell.presentation is not workspace
        assert shell.research_presentation is research
        assert detail.presentation is research
        assert str(shell.query_one("#research-sequence-note-2", Static).content) == (
            "v6 exact human wording\nStill tentative."
        )


@pytest.mark.asyncio
async def test_research_panel_uses_declared_positions_without_head_or_latest_language(
    tmp_path: Path,
) -> None:
    research = _research_presentation(tmp_path)
    _, _, _, workspace = _workspace(tmp_path)
    shell = create_workspace_shell(workspace, research_presentation=research)

    async with shell.run_test(size=(120, 55)) as pilot:
        await pilot.pause()
        detail = shell.query_one(ResearchRevisionEdgeSequenceDetail)
        rendered = "\n".join(str(widget.content) for widget in detail.query(Static))
        assert "Declared position 1 — not a global revision number" in rendered
        assert "Declared position 2 — not a global revision number" in rendered
        assert "Human-authored rationale — not source evidence" in rendered
        assert "Latest" not in rendered
        assert "Current head" not in rendered
        assert "Revision 1" not in rendered
        assert "Revision 2" not in rendered


def test_same_research_presentation_can_be_displayed_beside_different_workspaces(
    tmp_path: Path,
) -> None:
    research = _research_presentation(tmp_path)
    _, _, _, workspace_a = _workspace(tmp_path, name="Workspace A")
    _, _, _, workspace_b = _workspace(tmp_path, name="Workspace B")

    shell_a = create_workspace_shell(workspace_a, research_presentation=research)
    shell_b = create_workspace_shell(workspace_b, research_presentation=research)

    assert shell_a.research_presentation is research
    assert shell_b.research_presentation is research
    assert shell_a.presentation.rir.workspace_id != shell_b.presentation.rir.workspace_id


def test_package_level_shell_is_additive_wrapper_over_existing_normal_shell(
    tmp_path: Path,
) -> None:
    research = _research_presentation(tmp_path)
    _, _, _, workspace = _workspace(tmp_path)
    shell = create_workspace_shell(workspace, research_presentation=research)

    assert ExportedWorkspaceShell is ResearchWorkspaceShell
    assert isinstance(shell, ResearchWorkspaceShell)
    assert isinstance(shell, BaseWorkspaceShell)
    assert shell.research_presentation is research
