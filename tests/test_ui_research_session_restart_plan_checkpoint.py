from __future__ import annotations

from pathlib import Path

import pytest
from textual.widgets import Button, Input, Static, TextArea

from pyxis.app.chromium_research_session_reentry import reenter_chromium_research_session
from pyxis.ui.research_session_shell import create_research_session_shell
from pyxis.ui.chromium_research_session_restart_plan_textual import (
    ResearchSessionRestartPlanControls,
)
from test_app_chromium_research_session_reentry import _durable_fixture


async def _press(shell, pilot, button_id: str) -> None:
    button = shell.query_one(f"#{button_id}", Button)
    button.focus()
    await pilot.pause()
    await pilot.press("enter")
    await pilot.pause()


def _shell_with_reentry(tmp_path: Path):
    fixture = _durable_fixture(tmp_path)
    reentry = reenter_chromium_research_session(fixture.plan)
    shell = create_research_session_shell(reentry.controller, reentry=reentry)
    return fixture, reentry, shell


async def _write_and_rollover(
    shell,
    pilot,
    *,
    prior_edge: Path,
    successor: Path,
    declaration: Path,
    text: str,
) -> None:
    shell.query_one("#research-endpoint-revised-note", TextArea).text = text
    shell.query_one("#research-endpoint-prior-edge-source", Input).value = str(prior_edge)
    shell.query_one("#research-endpoint-destination", Input).value = str(successor)
    await _press(shell, pilot, "persist-research-endpoint-revision")
    shell.query_one("#research-session-rollover-successor-source", Input).value = str(successor)
    shell.query_one(
        "#research-session-rollover-declaration-destination", Input
    ).value = str(declaration)
    await _press(shell, pilot, "rollover-research-session")


async def _save_restart_plan(
    shell,
    pilot,
    *,
    successor: Path,
    declaration: Path,
    destination: Path,
) -> None:
    shell.query_one("#research-session-restart-plan-successor-source", Input).value = str(
        successor
    )
    shell.query_one("#research-session-restart-plan-declaration-source", Input).value = str(
        declaration
    )
    shell.query_one("#research-session-restart-plan-destination", Input).value = str(
        destination
    )
    await _press(shell, pilot, "save-research-session-restart-plan")


@pytest.mark.asyncio
async def test_reentry_aware_shell_retains_exact_lineage_without_initial_checkpoint(
    tmp_path: Path,
) -> None:
    _, reentry, shell = _shell_with_reentry(tmp_path)

    async with shell.run_test(size=(150, 120)) as pilot:
        await pilot.pause()
        assert shell.research_reentry is reentry
        assert shell.research_controller is reentry.controller
        assert len(shell.query(ResearchSessionRestartPlanControls)) == 0
        assert not shell.query_one("#persist-research-endpoint-revision", Button).disabled


@pytest.mark.asyncio
async def test_rollover_mounts_blank_restart_checkpoint_and_locks_further_revision(
    tmp_path: Path,
) -> None:
    fixture, reentry, shell = _shell_with_reentry(tmp_path)
    v7 = tmp_path / "v7.json"
    declaration = tmp_path / "v7-declaration.json"

    async with shell.run_test(size=(150, 150)) as pilot:
        await pilot.pause()
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=fixture.v6_path,
            successor=v7,
            declaration=declaration,
            text="v7 checkpoint",
        )

        checkpoint = shell.query_one(ResearchSessionRestartPlanControls)
        assert checkpoint.rollover is shell.last_research_rollover
        assert shell.research_reentry is reentry
        assert shell.last_research_restart_plan is None
        assert shell.query_one("#persist-research-endpoint-revision", Button).disabled
        assert shell.query_one("#research-session-restart-plan-successor-source", Input).value == ""
        assert shell.query_one("#research-session-restart-plan-declaration-source", Input).value == ""
        assert shell.query_one("#research-session-restart-plan-destination", Input).value == ""
        assert "not yet proven restartable" in str(
            shell.query_one("#research-session-restart-plan-candidate", Static).content
        )


@pytest.mark.asyncio
async def test_successful_restart_plan_save_advances_only_lineage_and_unlocks_revision(
    tmp_path: Path,
) -> None:
    fixture, prior_reentry, shell = _shell_with_reentry(tmp_path)
    v7 = tmp_path / "v7.json"
    declaration = tmp_path / "v7-declaration.json"
    plan_path = tmp_path / "v7.plan.json"

    async with shell.run_test(size=(150, 170)) as pilot:
        await pilot.pause()
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=fixture.v6_path,
            successor=v7,
            declaration=declaration,
            text="v7 restartable",
        )
        live_controller = shell.research_controller
        await _save_restart_plan(
            shell,
            pilot,
            successor=v7,
            declaration=declaration,
            destination=plan_path,
        )

        result = shell.last_research_restart_plan
        assert result is not None
        assert result.prior_reentry is prior_reentry
        assert shell.research_reentry is result.fresh_reentry
        assert shell.research_controller is live_controller
        assert shell.research_reentry.controller is not live_controller
        assert shell.research_reentry.controller.presentation == live_controller.presentation
        assert plan_path.exists()
        assert not shell.query_one("#persist-research-endpoint-revision", Button).disabled
        assert shell.query_one("#save-research-session-restart-plan", Button).disabled
        assert "not a global latest/current/head" in str(
            shell.query_one("#research-session-restart-plan-status", Static).content
        )


@pytest.mark.parametrize(
    ("missing_field", "expected"),
    [
        ("successor", "successor edge path is required"),
        ("declaration", "continuation declaration path is required"),
        ("destination", "restart plan destination is required"),
    ],
)
@pytest.mark.asyncio
async def test_checkpoint_missing_explicit_path_never_unlocks_revision(
    tmp_path: Path,
    missing_field: str,
    expected: str,
) -> None:
    fixture, _, shell = _shell_with_reentry(tmp_path)
    v7 = tmp_path / "v7.json"
    declaration = tmp_path / "v7-declaration.json"
    plan_path = tmp_path / "v7.plan.json"

    async with shell.run_test(size=(150, 170)) as pilot:
        await pilot.pause()
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=fixture.v6_path,
            successor=v7,
            declaration=declaration,
            text="v7 missing path",
        )
        values = {
            "successor": str(v7),
            "declaration": str(declaration),
            "destination": str(plan_path),
        }
        values[missing_field] = ""
        shell.query_one("#research-session-restart-plan-successor-source", Input).value = values[
            "successor"
        ]
        shell.query_one("#research-session-restart-plan-declaration-source", Input).value = values[
            "declaration"
        ]
        shell.query_one("#research-session-restart-plan-destination", Input).value = values[
            "destination"
        ]
        await _press(shell, pilot, "save-research-session-restart-plan")

        assert expected in str(
            shell.query_one("#research-session-restart-plan-status", Static).content
        )
        assert shell.query_one("#persist-research-endpoint-revision", Button).disabled
        assert shell.last_research_restart_plan is None
        assert not plan_path.exists()


@pytest.mark.asyncio
async def test_wrong_sibling_cannot_become_restart_plan_and_checkpoint_stays_locked(
    tmp_path: Path,
) -> None:
    fixture, _, shell = _shell_with_reentry(tmp_path)
    old_controller = shell.research_controller
    v7 = tmp_path / "v7.json"
    declaration = tmp_path / "v7-declaration.json"
    sibling = tmp_path / "sibling.json"
    plan_path = tmp_path / "wrong.plan.json"

    async with shell.run_test(size=(150, 170)) as pilot:
        await pilot.pause()
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=fixture.v6_path,
            successor=v7,
            declaration=declaration,
            text="v7 chosen",
        )
        old_controller.persist_declared_endpoint_revision(
            "different valid sibling",
            prior_edge_source=fixture.v6_path,
            destination=sibling,
        )
        await _save_restart_plan(
            shell,
            pilot,
            successor=sibling,
            declaration=declaration,
            destination=plan_path,
        )

        assert "failed" in str(
            shell.query_one("#research-session-restart-plan-status", Static).content
        ).lower()
        assert shell.query_one("#persist-research-endpoint-revision", Button).disabled
        assert shell.last_research_restart_plan is None
        assert not plan_path.exists()


@pytest.mark.asyncio
async def test_restart_plan_destination_is_no_overwrite_and_failure_keeps_checkpoint(
    tmp_path: Path,
) -> None:
    fixture, _, shell = _shell_with_reentry(tmp_path)
    v7 = tmp_path / "v7.json"
    declaration = tmp_path / "v7-declaration.json"
    plan_path = tmp_path / "existing.plan.json"
    plan_path.write_text("keep exact\n", encoding="utf-8")

    async with shell.run_test(size=(150, 170)) as pilot:
        await pilot.pause()
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=fixture.v6_path,
            successor=v7,
            declaration=declaration,
            text="v7 no overwrite",
        )
        await _save_restart_plan(
            shell,
            pilot,
            successor=v7,
            declaration=declaration,
            destination=plan_path,
        )

        assert plan_path.read_text(encoding="utf-8") == "keep exact\n"
        assert shell.query_one("#persist-research-endpoint-revision", Button).disabled
        assert shell.last_research_restart_plan is None


@pytest.mark.asyncio
async def test_moved_successor_and_declaration_require_explicit_new_locations_in_checkpoint(
    tmp_path: Path,
) -> None:
    fixture, _, shell = _shell_with_reentry(tmp_path)
    v7 = tmp_path / "v7.json"
    declaration = tmp_path / "v7-declaration.json"
    moved = tmp_path / "moved"
    plan_path = moved / "v7.plan.json"

    async with shell.run_test(size=(150, 170)) as pilot:
        await pilot.pause()
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=fixture.v6_path,
            successor=v7,
            declaration=declaration,
            text="v7 moved",
        )
        moved.mkdir()
        moved_v7 = v7.rename(moved / "chosen-edge.json")
        moved_declaration = declaration.rename(moved / "chosen-declaration.json")
        await _save_restart_plan(
            shell,
            pilot,
            successor=moved_v7,
            declaration=moved_declaration,
            destination=plan_path,
        )

        assert shell.last_research_restart_plan is not None
        assert shell.research_reentry.plan.declared_edge_sources == (moved_v7,)
        assert shell.research_reentry.plan.declaration_source == moved_declaration
        assert not shell.query_one("#persist-research-endpoint-revision", Button).disabled


@pytest.mark.asyncio
async def test_checkpoint_repeats_v7_then_v8_restart_lineage_without_head_state(
    tmp_path: Path,
) -> None:
    fixture, _, shell = _shell_with_reentry(tmp_path)
    v7 = tmp_path / "v7.json"
    d7 = tmp_path / "d7.json"
    p7 = tmp_path / "v7.plan.json"
    v8 = tmp_path / "v8.json"
    d8 = tmp_path / "d8.json"
    p8 = tmp_path / "v8.plan.json"

    async with shell.run_test(size=(150, 190)) as pilot:
        await pilot.pause()
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=fixture.v6_path,
            successor=v7,
            declaration=d7,
            text="v7 governed checkpoint",
        )
        await _save_restart_plan(
            shell,
            pilot,
            successor=v7,
            declaration=d7,
            destination=p7,
        )
        v7_reentry = shell.research_reentry

        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=v7,
            successor=v8,
            declaration=d8,
            text="v8 governed checkpoint",
        )
        assert shell.query_one("#persist-research-endpoint-revision", Button).disabled
        await _save_restart_plan(
            shell,
            pilot,
            successor=v8,
            declaration=d8,
            destination=p8,
        )

        assert shell.research_reentry is not v7_reentry
        assert shell.research_reentry.plan.starting_predecessor_edge_sources == (
            *v7_reentry.plan.starting_predecessor_edge_sources,
            *v7_reentry.plan.declared_edge_sources,
        )
        assert shell.research_reentry.plan.declared_edge_sources == (v8,)
        assert shell.research_controller.presentation.sequence.members[-1].note_text == (
            "v8 governed checkpoint"
        )
        assert not hasattr(shell.research_controller, "latest")
        assert not hasattr(shell.research_controller, "current_head")
        assert p7.exists()
        assert p8.exists()
        assert not shell.query_one("#persist-research-endpoint-revision", Button).disabled


def test_forged_reentry_lineage_rejects_before_shell_mount(tmp_path: Path) -> None:
    first_root = tmp_path / "first"
    second_root = tmp_path / "second"
    first_root.mkdir()
    second_root.mkdir()
    first = reenter_chromium_research_session(_durable_fixture(first_root).plan)
    second = reenter_chromium_research_session(_durable_fixture(second_root).plan)
    second.controller._presentation = object()  # type: ignore[attr-defined]

    with pytest.raises(ValueError, match="does not describe"):
        create_research_session_shell(first.controller, reentry=second)
