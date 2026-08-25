from __future__ import annotations

from pathlib import Path

import pytest
from textual.widgets import Button

from pyxis.app.chromium_research_second_basis_epoch_shell_lineage import (
    prove_chromium_research_second_basis_epoch_continuation_shell_lineage,
    prove_chromium_research_second_basis_epoch_shell_lineage,
)
from pyxis.ui.chromium_research_session_restart_plan_textual import (
    ResearchSessionRestartPlanControls,
)
from pyxis.ui.second_basis_epoch_research_session_shell import (
    SecondBasisEpochContinuationResearchSessionShell,
    SecondBasisEpochResearchSessionShell,
    create_second_basis_epoch_continuation_research_session_shell,
    create_second_basis_epoch_research_session_shell,
)
from test_app_chromium_research_second_basis_epoch_continuation_reentry_plan_document import (
    _persist_valid_continuation,
)
from test_app_chromium_research_second_basis_epoch_reentry_plan_document import (
    _persist_valid_overlay,
)
from test_ui_research_root_backed_session_continuation_checkpoint import (
    _write_and_rollover,
)


def _second_epoch_shell(tmp_path: Path, *, stem: str):
    _, earned, overlay, _ = _persist_valid_overlay(tmp_path, stem=stem)
    lineage = prove_chromium_research_second_basis_epoch_shell_lineage(
        earned,
        overlay_source=overlay,
    )
    return lineage, create_second_basis_epoch_research_session_shell(lineage)


def _continuation_shell(tmp_path: Path, *, stem: str):
    values = _persist_valid_continuation(tmp_path, stem=stem)
    overlay = values[6]
    earned = values[8].fresh_reentry
    lineage = prove_chromium_research_second_basis_epoch_continuation_shell_lineage(
        earned,
        overlay_source=overlay,
    )
    return lineage, create_second_basis_epoch_continuation_research_session_shell(lineage)


@pytest.mark.asyncio
async def test_37b_shell_retains_exact_proven_launch_lineage_without_ordinary_restart_authority(
    tmp_path: Path,
) -> None:
    lineage, shell = _second_epoch_shell(tmp_path, stem="38c-ui-second")

    async with shell.run_test(size=(160, 130)) as pilot:
        await pilot.pause()
        assert isinstance(shell, SecondBasisEpochResearchSessionShell)
        assert shell.second_basis_epoch_launch_lineage is lineage
        assert shell.research_reentry is None
        assert shell.research_controller is lineage.reentry.controller
        assert len(shell.query(ResearchSessionRestartPlanControls)) == 0
        assert len(shell.query("#research-second-basis-epoch-checkpoint-controls")) == 0
        assert not shell.query_one("#persist-research-endpoint-revision", Button).disabled


@pytest.mark.asyncio
async def test_37c_shell_retains_exact_proven_continuation_launch_lineage_without_ordinary_restart_authority(
    tmp_path: Path,
) -> None:
    lineage, shell = _continuation_shell(tmp_path, stem="38c-ui-cont")

    async with shell.run_test(size=(160, 130)) as pilot:
        await pilot.pause()
        assert isinstance(shell, SecondBasisEpochContinuationResearchSessionShell)
        assert shell.second_basis_epoch_continuation_launch_lineage is lineage
        assert shell.research_reentry is None
        assert shell.research_controller is lineage.reentry.controller
        assert len(shell.query(ResearchSessionRestartPlanControls)) == 0
        assert len(shell.query("#research-second-basis-epoch-cumulative-checkpoint-controls")) == 0
        assert not shell.query_one("#persist-research-endpoint-revision", Button).disabled


@pytest.mark.asyncio
async def test_37b_shell_rollover_moves_live_controller_without_promoting_launch_lineage(
    tmp_path: Path,
) -> None:
    lineage, shell = _second_epoch_shell(tmp_path, stem="38c-ui-second-rollover")
    launch_controller = lineage.reentry.controller
    successor = tmp_path / "successor.json"
    declaration = tmp_path / "continuation-declaration.json"

    async with shell.run_test(size=(160, 170)) as pilot:
        await pilot.pause()
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=launch_controller.declared_endpoint.verification.path,
            successor=successor,
            declaration=declaration,
            text="Uncheckpointed continuation above the second basis epoch.",
        )

        assert shell.second_basis_epoch_launch_lineage is lineage
        assert shell.research_reentry is None
        assert shell.last_research_rollover is not None
        assert shell.research_controller is shell.last_research_rollover.continuation_controller
        assert shell.research_controller is not launch_controller
        assert len(shell.query(ResearchSessionRestartPlanControls)) == 0
        assert len(shell.query("#research-second-basis-epoch-checkpoint-controls")) == 0
        assert not shell.query_one("#persist-research-endpoint-revision", Button).disabled


@pytest.mark.asyncio
async def test_37c_shell_rollover_moves_live_controller_without_promoting_continuation_launch_lineage(
    tmp_path: Path,
) -> None:
    lineage, shell = _continuation_shell(tmp_path, stem="38c-ui-cont-rollover")
    launch_controller = lineage.reentry.controller
    successor = tmp_path / "next-successor.json"
    declaration = tmp_path / "next-continuation-declaration.json"

    async with shell.run_test(size=(160, 170)) as pilot:
        await pilot.pause()
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=launch_controller.declared_endpoint.verification.path,
            successor=successor,
            declaration=declaration,
            text="Another uncheckpointed continuation above the second root.",
        )

        assert shell.second_basis_epoch_continuation_launch_lineage is lineage
        assert shell.research_reentry is None
        assert shell.last_research_rollover is not None
        assert shell.research_controller is shell.last_research_rollover.continuation_controller
        assert shell.research_controller is not launch_controller
        assert len(shell.query(ResearchSessionRestartPlanControls)) == 0
        assert len(shell.query("#research-second-basis-epoch-cumulative-checkpoint-controls")) == 0
        assert not shell.query_one("#persist-research-endpoint-revision", Button).disabled


def test_second_epoch_shell_factories_reject_wrong_lineage_family_before_mount() -> None:
    with pytest.raises(TypeError, match="ChromiumResearchSecondBasisEpochShellLineage"):
        create_second_basis_epoch_research_session_shell(object())  # type: ignore[arg-type]

    with pytest.raises(
        TypeError,
        match="ChromiumResearchSecondBasisEpochContinuationShellLineage",
    ):
        create_second_basis_epoch_continuation_research_session_shell(object())  # type: ignore[arg-type]
