from __future__ import annotations

from pathlib import Path

import pytest
from textual.widgets import Button, Input, TextArea

from test_ui_research_root_backed_session_continuation_checkpoint import (
    _press,
    _save_root_backed_checkpoint,
    _shell_with_root_backed_reentry,
    _write_and_rollover,
)


@pytest.mark.asyncio
async def test_cumulative_handoff_control_is_absent_until_successful_35d_checkpoint(
    tmp_path: Path,
) -> None:
    prior, root_overlay, shell = _shell_with_root_backed_reentry(
        tmp_path,
        stem="36d-absent",
    )
    successor = tmp_path / "successor.json"
    declaration = tmp_path / "declaration.json"

    async with shell.run_test(size=(165, 210)) as pilot:
        await pilot.pause()
        assert len(shell.query("#continue-root-backed-cumulative-mode")) == 0

        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=prior.controller.declared_endpoint.verification.path,
            successor=successor,
            declaration=declaration,
            text="Handoff is not earned by rollover alone.",
        )

        assert len(shell.query("#continue-root-backed-cumulative-mode")) == 0
        assert shell.query_one("#persist-research-endpoint-revision", Button).disabled
        assert not root_overlay.samefile(root_overlay.parent / root_overlay.name) is False


@pytest.mark.asyncio
async def test_successful_35d_checkpoint_mounts_explicit_handoff_returning_exact_fresh_reentry(
    tmp_path: Path,
    monkeypatch,
) -> None:
    prior, root_overlay, shell = _shell_with_root_backed_reentry(
        tmp_path,
        stem="36d-success",
    )
    successor = tmp_path / "successor.json"
    declaration = tmp_path / "declaration.json"
    next_overlay = tmp_path / "continuation.overlay.json"
    observed: dict[str, object] = {}

    def fake_exit(result=None, *args, **kwargs) -> None:
        observed["result"] = result

    monkeypatch.setattr(shell, "exit", fake_exit)

    async with shell.run_test(size=(165, 230)) as pilot:
        await pilot.pause()
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=prior.controller.declared_endpoint.verification.path,
            successor=successor,
            declaration=declaration,
            text="Explicitly hand this proven continuation to cumulative mode.",
        )
        await _save_root_backed_checkpoint(
            shell,
            pilot,
            prior_overlay=root_overlay,
            successor=successor,
            declaration=declaration,
            destination=next_overlay,
        )

        checkpoint = shell.last_root_backed_continuation_checkpoint
        assert checkpoint is not None
        handoff_button = shell.query_one(
            "#continue-root-backed-cumulative-mode",
            Button,
        )
        assert not handoff_button.disabled
        assert shell.query_one("#persist-research-endpoint-revision", Button).disabled
        assert shell.research_controller is checkpoint.rollover.continuation_controller

        await _press(shell, pilot, "continue-root-backed-cumulative-mode")

        assert observed["result"] is checkpoint.fresh_reentry
        assert next_overlay.exists()


@pytest.mark.asyncio
async def test_failed_35d_checkpoint_never_exposes_cumulative_handoff(
    tmp_path: Path,
) -> None:
    prior, root_overlay, shell = _shell_with_root_backed_reentry(
        tmp_path,
        stem="36d-failure",
    )
    successor = tmp_path / "successor.json"
    declaration = tmp_path / "declaration.json"

    async with shell.run_test(size=(165, 220)) as pilot:
        await pilot.pause()
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=prior.controller.declared_endpoint.verification.path,
            successor=successor,
            declaration=declaration,
            text="Blank destination must not earn handoff authority.",
        )
        shell.query_one(
            "#research-root-backed-checkpoint-prior-overlay-source",
            Input,
        ).value = str(root_overlay)
        shell.query_one(
            "#research-root-backed-checkpoint-successor-source",
            Input,
        ).value = str(successor)
        shell.query_one(
            "#research-root-backed-checkpoint-declaration-source",
            Input,
        ).value = str(declaration)
        shell.query_one(
            "#research-root-backed-checkpoint-destination",
            Input,
        ).value = ""
        await _press(shell, pilot, "save-research-root-backed-continuation-checkpoint")

        assert shell.last_root_backed_continuation_checkpoint is None
        assert len(shell.query("#continue-root-backed-cumulative-mode")) == 0
        assert shell.query_one("#persist-research-endpoint-revision", Button).disabled
