from __future__ import annotations

from pathlib import Path

import pytest
from textual.widgets import Button, Input

from pyxis.app.chromium_research_second_basis_epoch_shell_lineage import (
    prove_chromium_research_second_basis_epoch_continuation_shell_lineage,
    prove_chromium_research_second_basis_epoch_shell_lineage,
)
from pyxis.ui.chromium_research_second_basis_epoch_continuation_checkpoint_extension_textual import (
    SecondBasisEpochResearchSessionCumulativeCheckpointControls,
)
from pyxis.ui.chromium_research_second_basis_epoch_continuation_checkpoint_textual import (
    SecondBasisEpochResearchSessionContinuationCheckpointControls,
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
    lineage, shell = _second_epoch_shell(tmp_path, stem="38e-ui-second")

    async with shell.run_test(size=(160, 130)) as pilot:
        await pilot.pause()
        assert isinstance(shell, SecondBasisEpochResearchSessionShell)
        assert shell.second_basis_epoch_launch_lineage is lineage
        assert shell.research_reentry is None
        assert shell.research_controller is lineage.reentry.controller
        assert shell.last_second_basis_epoch_continuation_checkpoint is None
        assert len(shell.query(ResearchSessionRestartPlanControls)) == 0
        assert len(shell.query(SecondBasisEpochResearchSessionContinuationCheckpointControls)) == 0
        assert not shell.query_one("#persist-research-endpoint-revision", Button).disabled


@pytest.mark.asyncio
async def test_37c_shell_retains_launch_lineage_and_exact_current_typed_continuation(
    tmp_path: Path,
) -> None:
    lineage, shell = _continuation_shell(tmp_path, stem="38e-ui-cont")

    async with shell.run_test(size=(160, 130)) as pilot:
        await pilot.pause()
        assert isinstance(shell, SecondBasisEpochContinuationResearchSessionShell)
        assert shell.second_basis_epoch_continuation_launch_lineage is lineage
        assert shell.second_basis_epoch_continuation_reentry is lineage.reentry
        assert shell.research_reentry is None
        assert shell.research_controller is lineage.reentry.controller
        assert shell.last_second_basis_epoch_cumulative_checkpoint is None
        assert len(shell.query(ResearchSessionRestartPlanControls)) == 0
        assert len(shell.query(SecondBasisEpochResearchSessionCumulativeCheckpointControls)) == 0
        assert not shell.query_one("#persist-research-endpoint-revision", Button).disabled


@pytest.mark.asyncio
async def test_37b_shell_rollover_keeps_launch_lineage_and_mounts_blank_locked_37c_checkpoint(
    tmp_path: Path,
) -> None:
    lineage, shell = _second_epoch_shell(tmp_path, stem="38e-ui-second-rollover")
    launch_controller = lineage.reentry.controller
    successor = tmp_path / "successor.json"
    declaration = tmp_path / "continuation-declaration.json"

    async with shell.run_test(size=(160, 210)) as pilot:
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
        assert shell.last_second_basis_epoch_continuation_checkpoint is None
        assert len(shell.query(ResearchSessionRestartPlanControls)) == 0
        controls = shell.query_one(
            SecondBasisEpochResearchSessionContinuationCheckpointControls
        )
        assert controls.rollover is shell.last_research_rollover
        assert shell.query_one("#persist-research-endpoint-revision", Button).disabled
        for selector in (
            "#research-second-basis-epoch-checkpoint-prior-overlay-source",
            "#research-second-basis-epoch-checkpoint-successor-source",
            "#research-second-basis-epoch-checkpoint-declaration-source",
            "#research-second-basis-epoch-checkpoint-destination",
        ):
            assert shell.query_one(selector, Input).value == ""


@pytest.mark.asyncio
async def test_37c_shell_rollover_keeps_current_typed_lineage_and_mounts_blank_locked_37d_checkpoint(
    tmp_path: Path,
) -> None:
    lineage, shell = _continuation_shell(tmp_path, stem="38e-ui-cont-rollover")
    launch_controller = lineage.reentry.controller
    successor = tmp_path / "next-successor.json"
    declaration = tmp_path / "next-continuation-declaration.json"

    async with shell.run_test(size=(160, 210)) as pilot:
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
        assert shell.second_basis_epoch_continuation_reentry is lineage.reentry
        assert shell.research_reentry is None
        assert shell.last_research_rollover is not None
        assert shell.research_controller is shell.last_research_rollover.continuation_controller
        assert shell.research_controller is not launch_controller
        assert len(shell.query(ResearchSessionRestartPlanControls)) == 0
        controls = shell.query_one(
            SecondBasisEpochResearchSessionCumulativeCheckpointControls
        )
        assert controls.current_reentry is lineage.reentry
        assert controls.rollover is shell.last_research_rollover
        assert shell.query_one("#persist-research-endpoint-revision", Button).disabled
        for selector in (
            "#research-second-basis-epoch-cumulative-checkpoint-current-overlay-source",
            "#research-second-basis-epoch-cumulative-checkpoint-successor-source",
            "#research-second-basis-epoch-cumulative-checkpoint-declaration-destination",
            "#research-second-basis-epoch-cumulative-checkpoint-overlay-destination",
        ):
            assert shell.query_one(selector, Input).value == ""


def test_second_epoch_shell_factories_reject_wrong_lineage_family_before_mount() -> None:
    with pytest.raises(TypeError, match="ChromiumResearchSecondBasisEpochShellLineage"):
        create_second_basis_epoch_research_session_shell(object())  # type: ignore[arg-type]

    with pytest.raises(
        TypeError,
        match="ChromiumResearchSecondBasisEpochContinuationShellLineage",
    ):
        create_second_basis_epoch_continuation_research_session_shell(object())  # type: ignore[arg-type]
