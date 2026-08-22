from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest
from textual.widgets import Button, Input, Static

from pyxis.app import WorkspaceController, build_and_run_workspace, create_workspace_presentation
from pyxis.app.chromium_research_revision_edge_working_set_presentation import (
    present_chromium_research_revision_edge_working_set_context,
)
from pyxis.app.chromium_research_session_presentation import (
    present_chromium_research_session,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_sequence_presentation import (
    present_chromium_research_working_set_note_revision_edge_sequence_declaration,
)
from pyxis.authoring import create_workspace_spec
from pyxis.ui import create_workspace_shell
from pyxis.ui.chromium_research_rationale_working_set_textual import (
    ResearchRationaleWorkingSetDetail,
)
from pyxis.ui.chromium_research_revision_edge_sequence_textual import (
    ResearchRevisionEdgeSequenceDetail,
)
from test_app_chromium_research_working_set_note_revision_edge_sequence_presentation import (
    _loaded_declared_sequence,
)


def _session(tmp_path: Path):
    _, _, _, _, _, loaded = _loaded_declared_sequence(tmp_path)
    return loaded, present_chromium_research_session(loaded)


def _workspace(tmp_path: Path):
    root = tmp_path / "workspace"
    spec = create_workspace_spec(
        "Research session UI",
        "Workspace identity remains separate from research session presentation evidence.",
    )
    run = build_and_run_workspace(spec, root, "same runtime workload")
    return root, run, create_workspace_presentation(spec, run)


@pytest.mark.asyncio
async def test_complete_session_mounts_sequence_and_every_context(tmp_path: Path) -> None:
    _, session = _session(tmp_path)
    _, _, workspace = _workspace(tmp_path)
    shell = create_workspace_shell(workspace, research_session=session)

    async with shell.run_test(size=(150, 85)) as pilot:
        await pilot.pause()
        detail = shell.query_one(ResearchRevisionEdgeSequenceDetail)
        contexts = tuple(shell.query(ResearchRationaleWorkingSetDetail))

        assert detail.presentation is session.sequence
        assert tuple(context.presentation for context in contexts) == session.working_set_contexts
        assert {button.id for button in detail.query(Button)} == {
            "research-context-toggle-1",
            "research-context-toggle-2",
        }
        assert str(shell.query_one("#research-sequence-note-1", Static).content) == (
            "  v5 exact human wording 😀  "
        )
        assert str(shell.query_one("#research-sequence-note-2", Static).content) == (
            "v6 exact human wording\nStill tentative."
        )


def test_shell_retains_exact_session_and_subpresentations(tmp_path: Path) -> None:
    _, session = _session(tmp_path)
    _, _, workspace = _workspace(tmp_path)
    shell = create_workspace_shell(workspace, research_session=session)

    assert shell.research_session is session
    assert shell.research_presentation is session.sequence
    assert shell.research_working_set_contexts == session.working_set_contexts
    assert all(
        observed is expected
        for observed, expected in zip(
            shell.research_working_set_contexts,
            session.working_set_contexts,
        )
    )


def test_complete_session_and_split_sequence_are_mutually_exclusive(tmp_path: Path) -> None:
    _, session = _session(tmp_path)
    _, _, workspace = _workspace(tmp_path)

    with pytest.raises(ValueError, match="cannot be combined"):
        create_workspace_shell(
            workspace,
            research_session=session,
            research_presentation=session.sequence,
        )


def test_complete_session_and_split_contexts_are_mutually_exclusive(tmp_path: Path) -> None:
    _, session = _session(tmp_path)
    _, _, workspace = _workspace(tmp_path)

    with pytest.raises(ValueError, match="cannot be combined"):
        create_workspace_shell(
            workspace,
            research_session=session,
            research_working_set_contexts=session.working_set_contexts,
        )


def test_wrong_session_type_is_rejected(tmp_path: Path) -> None:
    _, _, workspace = _workspace(tmp_path)

    with pytest.raises(TypeError, match="ChromiumPageResearchSessionPresentation"):
        create_workspace_shell(
            workspace,
            research_session=object(),  # type: ignore[arg-type]
        )


def test_forged_session_mode_is_rejected(tmp_path: Path) -> None:
    _, session = _session(tmp_path)
    forged = replace(session, presentation_mode="forged-session-mode")
    _, _, workspace = _workspace(tmp_path)

    with pytest.raises(ValueError, match="session presentation mode"):
        create_workspace_shell(workspace, research_session=forged)


def test_incomplete_session_context_coverage_is_rejected(tmp_path: Path) -> None:
    _, session = _session(tmp_path)
    forged = replace(
        session,
        working_set_contexts=session.working_set_contexts[:1],
    )
    _, _, workspace = _workspace(tmp_path)

    with pytest.raises(ValueError, match="one context per declared position"):
        create_workspace_shell(workspace, research_session=forged)


def test_forged_session_context_attachment_is_rejected(tmp_path: Path) -> None:
    _, session = _session(tmp_path)
    forged_first = replace(
        session.working_set_contexts[0],
        edge_record_sha256="f" * 64,
    )
    forged = replace(
        session,
        working_set_contexts=(forged_first, *session.working_set_contexts[1:]),
    )
    _, _, workspace = _workspace(tmp_path)

    with pytest.raises(ValueError, match="edge identity does not match"):
        create_workspace_shell(workspace, research_session=forged)


def test_legacy_split_presentation_form_remains_supported(tmp_path: Path) -> None:
    loaded, session = _session(tmp_path)
    sequence = present_chromium_research_working_set_note_revision_edge_sequence_declaration(
        loaded
    )
    contexts = tuple(
        present_chromium_research_revision_edge_working_set_context(
            loaded,
            declared_position=member.declared_position,
        )
        for member in sequence.members
    )
    _, _, workspace = _workspace(tmp_path)
    shell = create_workspace_shell(
        workspace,
        research_presentation=sequence,
        research_working_set_contexts=contexts,
    )

    assert shell.research_session is None
    assert shell.research_presentation == session.sequence
    assert shell.research_working_set_contexts == session.working_set_contexts


@pytest.mark.asyncio
async def test_workspace_runtime_rerun_preserves_exact_complete_session(tmp_path: Path) -> None:
    _, session = _session(tmp_path)
    root, run, workspace = _workspace(tmp_path)
    controller = WorkspaceController(root, run)
    shell = create_workspace_shell(
        workspace,
        controller=controller,
        research_session=session,
    )

    async with shell.run_test(size=(150, 85)) as pilot:
        await pilot.pause()
        session_before = shell.research_session
        sequence_before = shell.research_presentation
        contexts_before = shell.research_working_set_contexts

        runtime_input = shell.query_one("#runtime-input", Input)
        runtime_input.value = "changed runtime input"
        runtime_input.focus()
        await pilot.press("enter")
        await pilot.pause()

        assert shell.research_session is session_before is session
        assert shell.research_presentation is sequence_before is session.sequence
        assert shell.research_working_set_contexts is contexts_before
        assert shell.research_working_set_contexts == session.working_set_contexts
        assert tuple(
            detail.presentation for detail in shell.query(ResearchRationaleWorkingSetDetail)
        ) == session.working_set_contexts
