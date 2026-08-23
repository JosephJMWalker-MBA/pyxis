from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest
from textual.widgets import Button, Input, Static, TextArea

from pyxis.app.chromium_research_session_reentry import reenter_chromium_research_session
from pyxis.ui import ResearchSessionShell, create_research_session_shell
from pyxis.ui.chromium_research_endpoint_revision_textual import (
    ResearchEndpointRevisionControls,
)
from pyxis.ui.chromium_research_revision_edge_sequence_textual import (
    ResearchRevisionEdgeSequenceDetail,
)
from pyxis.ui.chromium_research_session_rollover_textual import (
    ResearchSessionRolloverControls,
)
from test_app_chromium_research_session_reentry import _durable_fixture


async def _press(shell, pilot, button_id: str) -> None:
    button = shell.query_one(f"#{button_id}", Button)
    button.focus()
    await pilot.pause()
    await pilot.press("enter")
    await pilot.pause()


def _controller(tmp_path: Path):
    fixture = _durable_fixture(tmp_path)
    result = reenter_chromium_research_session(fixture.plan)
    return fixture, result.controller


@pytest.mark.asyncio
async def test_standalone_shell_mounts_exact_research_controller_without_workspace_surface(
    tmp_path: Path,
) -> None:
    fixture, controller = _controller(tmp_path)
    shell = create_research_session_shell(controller)

    assert isinstance(shell, ResearchSessionShell)
    async with shell.run_test(size=(150, 100)) as pilot:
        await pilot.pause()
        detail = shell.query_one(ResearchRevisionEdgeSequenceDetail)

        assert shell.research_controller is controller
        assert shell.research_session is controller.presentation
        assert detail.presentation is controller.presentation.sequence
        assert len(shell.query(ResearchEndpointRevisionControls)) == 1
        assert len(shell.query(ResearchSessionRolloverControls)) == 1
        assert len(shell.query("#runtime-input")) == 0
        assert len(shell.query("#preview-remove-normalize-text")) == 0
        assert len(shell.query("#preview-add-split-lines")) == 0
        assert len(shell.query("#refresh-export")) == 0
        assert fixture.declaration_path.exists()


@pytest.mark.asyncio
async def test_standalone_shell_writes_exact_successor_without_adopting_it(
    tmp_path: Path,
) -> None:
    fixture, controller = _controller(tmp_path)
    shell = create_research_session_shell(controller)
    successor = tmp_path / "v7-standalone.json"
    original_session = controller.presentation

    async with shell.run_test(size=(150, 110)) as pilot:
        await pilot.pause()
        shell.query_one("#research-endpoint-revised-note", TextArea).text = (
            "  v7 standalone exact human wording 😀\nStill provisional.  "
        )
        shell.query_one("#research-endpoint-prior-edge-source", Input).value = str(
            fixture.v6_path
        )
        shell.query_one("#research-endpoint-destination", Input).value = str(successor)
        await _press(shell, pilot, "persist-research-endpoint-revision")

        result = controller.last_endpoint_revision
        assert result is not None
        assert result.persistence.path == successor.resolve()
        assert result.extension.revision.revised_note.note_text == (
            "  v7 standalone exact human wording 😀\nStill provisional.  "
        )
        assert shell.research_controller is controller
        assert shell.research_session is original_session
        assert shell.query_one("#persist-research-endpoint-revision", Button).disabled
        rollover = shell.query_one(ResearchSessionRolloverControls)
        assert rollover.candidate_revision is result
        assert not shell.query_one("#rollover-research-session", Button).disabled


@pytest.mark.asyncio
async def test_standalone_shell_explicit_rollover_replaces_only_research_session(
    tmp_path: Path,
) -> None:
    fixture, old_controller = _controller(tmp_path)
    successor = tmp_path / "v7-rollover.json"
    chosen = old_controller.persist_declared_endpoint_revision(
        "v7 chosen continuation",
        prior_edge_source=fixture.v6_path,
        destination=successor,
    )
    shell = create_research_session_shell(old_controller)
    declaration = tmp_path / "v7-declaration.json"

    async with shell.run_test(size=(150, 120)) as pilot:
        await pilot.pause()
        shell.query_one("#research-session-rollover-successor-source", Input).value = str(
            successor
        )
        shell.query_one(
            "#research-session-rollover-declaration-destination", Input
        ).value = str(declaration)
        await _press(shell, pilot, "rollover-research-session")

        new_controller = shell.research_controller
        assert new_controller is not old_controller
        assert old_controller.last_endpoint_revision is chosen
        assert old_controller.presentation.sequence.members[-1].note_text == (
            "v6 exact human wording\nStill tentative."
        )
        assert new_controller.presentation.sequence.members[-1].note_text == (
            "v7 chosen continuation"
        )
        assert shell.last_research_rollover is not None
        receipt = str(
            shell.query_one("#research-rollover-success-receipt", Static).content
        )
        assert "not a global latest/current/head" in receipt
        assert declaration.exists()


@pytest.mark.asyncio
async def test_standalone_shell_repeats_write_and_rollover_cycle_without_head_state(
    tmp_path: Path,
) -> None:
    fixture, controller = _controller(tmp_path)
    shell = create_research_session_shell(controller)
    v7 = tmp_path / "v7-repeat.json"
    d7 = tmp_path / "d7.json"
    v8 = tmp_path / "v8-repeat.json"
    d8 = tmp_path / "d8.json"

    async with shell.run_test(size=(150, 130)) as pilot:
        await pilot.pause()
        shell.query_one("#research-endpoint-revised-note", TextArea).text = "v7 repeated loop"
        shell.query_one("#research-endpoint-prior-edge-source", Input).value = str(
            fixture.v6_path
        )
        shell.query_one("#research-endpoint-destination", Input).value = str(v7)
        await _press(shell, pilot, "persist-research-endpoint-revision")
        shell.query_one("#research-session-rollover-successor-source", Input).value = str(v7)
        shell.query_one(
            "#research-session-rollover-declaration-destination", Input
        ).value = str(d7)
        await _press(shell, pilot, "rollover-research-session")

        first_continuation = shell.research_controller
        shell.query_one("#research-endpoint-revised-note", TextArea).text = "v8 repeated loop"
        shell.query_one("#research-endpoint-prior-edge-source", Input).value = str(v7)
        shell.query_one("#research-endpoint-destination", Input).value = str(v8)
        await _press(shell, pilot, "persist-research-endpoint-revision")
        shell.query_one("#research-session-rollover-successor-source", Input).value = str(v8)
        shell.query_one(
            "#research-session-rollover-declaration-destination", Input
        ).value = str(d8)
        await _press(shell, pilot, "rollover-research-session")

        assert shell.research_controller is not first_continuation
        assert shell.research_controller.presentation.sequence.members[-1].note_text == (
            "v8 repeated loop"
        )
        assert not hasattr(shell.research_controller, "current_head")
        assert not hasattr(shell.research_controller, "latest")
        assert d7.exists()
        assert d8.exists()


def test_standalone_shell_revalidates_controller_before_it_becomes_ui_authority(
    tmp_path: Path,
) -> None:
    _, controller = _controller(tmp_path)
    controller._presentation = replace(  # type: ignore[attr-defined]
        controller.presentation,
        presentation_mode="forged-mode",
    )

    with pytest.raises(ValueError, match="incoherent"):
        create_research_session_shell(controller)
