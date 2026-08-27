from __future__ import annotations

from pathlib import Path

import pytest
from textual.widgets import Button, Input

from pyxis.ui.chromium_research_session_restart_plan_textual import (
    ResearchSessionRestartPlanControls,
)
from pyxis.ui.chromium_research_third_basis_epoch_continuation_checkpoint_extension_textual import (
    ThirdBasisEpochResearchSessionCumulativeCheckpointControls,
)
from pyxis.ui.third_basis_epoch_cumulative_handoff_shell import (
    ThirdBasisEpochContinuationHandoffResearchSessionShell,
    ThirdBasisEpochCumulativeHandoffResearchSessionShell,
    create_third_basis_epoch_continuation_handoff_research_session_shell,
    create_third_basis_epoch_cumulative_handoff_research_session_shell,
)
from test_ui_research_root_backed_session_continuation_checkpoint import (
    _press,
    _write_and_rollover,
)
from test_ui_third_basis_epoch_first_continuation_checkpoint import (
    _save_checkpoint,
    _shell_with_lineage,
)


@pytest.mark.asyncio
async def test_41e_handoff_control_is_absent_until_successful_40c_checkpoint(
    tmp_path: Path,
) -> None:
    lineage, _, _ = _shell_with_lineage(tmp_path, stem="41e-absent")
    shell = create_third_basis_epoch_cumulative_handoff_research_session_shell(lineage)
    prior = lineage.reentry
    successor = tmp_path / "successor.json"
    declaration = tmp_path / "declaration.json"

    async with shell.run_test(size=(165, 230)) as pilot:
        await pilot.pause()
        assert isinstance(shell, ThirdBasisEpochCumulativeHandoffResearchSessionShell)
        assert len(shell.query("#continue-third-basis-epoch-cumulative-mode")) == 0

        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=prior.controller.declared_endpoint.verification.path,
            successor=successor,
            declaration=declaration,
            text="Rollover alone must not earn third-epoch cumulative handoff.",
        )

        assert shell.last_third_basis_epoch_continuation_checkpoint is None
        assert len(shell.query("#continue-third-basis-epoch-cumulative-mode")) == 0
        assert shell.query_one("#persist-research-endpoint-revision", Button).disabled


@pytest.mark.asyncio
async def test_successful_40c_checkpoint_mounts_explicit_handoff_returning_exact_fresh_reentry(
    tmp_path: Path,
    monkeypatch,
) -> None:
    lineage, overlay, _ = _shell_with_lineage(tmp_path, stem="41e-success")
    shell = create_third_basis_epoch_cumulative_handoff_research_session_shell(lineage)
    prior = lineage.reentry
    successor = tmp_path / "successor.json"
    declaration = tmp_path / "declaration.json"
    next_overlay = tmp_path / "continuation.overlay.json"
    observed: dict[str, object] = {}

    def fake_exit(result=None, *args, **kwargs) -> None:
        observed["result"] = result

    monkeypatch.setattr(shell, "exit", fake_exit)

    async with shell.run_test(size=(165, 255)) as pilot:
        await pilot.pause()
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=prior.controller.declared_endpoint.verification.path,
            successor=successor,
            declaration=declaration,
            text="Explicitly hand this proven third-epoch continuation to cumulative mode.",
        )
        await _save_checkpoint(
            shell,
            pilot,
            prior_overlay=overlay,
            successor=successor,
            declaration=declaration,
            destination=next_overlay,
        )

        checkpoint = shell.last_third_basis_epoch_continuation_checkpoint
        assert checkpoint is not None
        button = shell.query_one(
            "#continue-third-basis-epoch-cumulative-mode",
            Button,
        )
        assert not button.disabled
        assert shell.query_one("#persist-research-endpoint-revision", Button).disabled
        assert shell.research_controller is checkpoint.rollover.continuation_controller
        assert next_overlay.exists()

        await _press(shell, pilot, "continue-third-basis-epoch-cumulative-mode")

        assert observed["result"] is checkpoint.fresh_reentry


@pytest.mark.asyncio
async def test_failed_40c_checkpoint_never_exposes_third_epoch_cumulative_handoff(
    tmp_path: Path,
) -> None:
    lineage, overlay, _ = _shell_with_lineage(tmp_path, stem="41e-failure")
    shell = create_third_basis_epoch_cumulative_handoff_research_session_shell(lineage)
    prior = lineage.reentry
    successor = tmp_path / "successor.json"
    declaration = tmp_path / "declaration.json"

    async with shell.run_test(size=(165, 240)) as pilot:
        await pilot.pause()
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=prior.controller.declared_endpoint.verification.path,
            successor=successor,
            declaration=declaration,
            text="Blank destination must not earn third-epoch cumulative handoff.",
        )
        shell.query_one(
            "#research-third-basis-epoch-checkpoint-prior-overlay-source",
            Input,
        ).value = str(overlay)
        shell.query_one(
            "#research-third-basis-epoch-checkpoint-successor-source",
            Input,
        ).value = str(successor)
        shell.query_one(
            "#research-third-basis-epoch-checkpoint-declaration-source",
            Input,
        ).value = str(declaration)
        shell.query_one(
            "#research-third-basis-epoch-checkpoint-destination",
            Input,
        ).value = ""
        await _press(
            shell,
            pilot,
            "save-research-third-basis-epoch-continuation-checkpoint",
        )

        assert shell.last_third_basis_epoch_continuation_checkpoint is None
        assert len(shell.query("#continue-third-basis-epoch-cumulative-mode")) == 0
        assert shell.query_one("#persist-research-endpoint-revision", Button).disabled


@pytest.mark.asyncio
async def test_raw_typed_handoff_shell_starts_without_path_authority_and_next_form_is_blank(
    tmp_path: Path,
) -> None:
    lineage, overlay, _ = _shell_with_lineage(tmp_path, stem="41e-receive")
    first_shell = create_third_basis_epoch_cumulative_handoff_research_session_shell(lineage)
    prior = lineage.reentry
    successor = tmp_path / "successor.json"
    declaration = tmp_path / "declaration.json"
    persisted_overlay = tmp_path / "continuation.overlay.json"

    async with first_shell.run_test(size=(165, 255)) as pilot:
        await pilot.pause()
        await _write_and_rollover(
            first_shell,
            pilot,
            prior_edge=prior.controller.declared_endpoint.verification.path,
            successor=successor,
            declaration=declaration,
            text="Earn the exact raw typed third-epoch handoff.",
        )
        await _save_checkpoint(
            first_shell,
            pilot,
            prior_overlay=overlay,
            successor=successor,
            declaration=declaration,
            destination=persisted_overlay,
        )
        checkpoint = first_shell.last_third_basis_epoch_continuation_checkpoint
        assert checkpoint is not None
        handoff = checkpoint.fresh_reentry

    shell = create_third_basis_epoch_continuation_handoff_research_session_shell(handoff)
    assert isinstance(shell, ThirdBasisEpochContinuationHandoffResearchSessionShell)
    assert shell.third_basis_epoch_continuation_launch_lineage is None
    assert shell.third_basis_epoch_continuation_handoff_reentry is handoff
    assert shell.third_basis_epoch_continuation_reentry is handoff
    assert shell.research_controller is handoff.controller
    assert not hasattr(shell, "current_overlay_source")
    assert not hasattr(shell, "overlay_source")

    next_successor = tmp_path / "next-successor.json"
    next_one_hop = tmp_path / "next-one-hop.json"
    async with shell.run_test(size=(165, 245)) as pilot:
        await pilot.pause()
        assert len(shell.query(ResearchSessionRestartPlanControls)) == 0
        assert len(shell.query(ThirdBasisEpochResearchSessionCumulativeCheckpointControls)) == 0
        assert not shell.query_one("#persist-research-endpoint-revision", Button).disabled

        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=handoff.controller.declared_endpoint.verification.path,
            successor=next_successor,
            declaration=next_one_hop,
            text="First cumulative successor after the exact in-process third-epoch handoff.",
        )

        controls = shell.query_one(
            ThirdBasisEpochResearchSessionCumulativeCheckpointControls
        )
        assert controls.current_reentry is handoff
        assert shell.query_one("#persist-research-endpoint-revision", Button).disabled
        for selector in (
            "#research-third-basis-epoch-cumulative-checkpoint-current-overlay-source",
            "#research-third-basis-epoch-cumulative-checkpoint-successor-source",
            "#research-third-basis-epoch-cumulative-checkpoint-declaration-destination",
            "#research-third-basis-epoch-cumulative-checkpoint-overlay-destination",
        ):
            assert shell.query_one(selector, Input).value == ""


def test_41e_handoff_factories_reject_wrong_authority_families() -> None:
    with pytest.raises(TypeError, match="ChromiumResearchThirdBasisEpochShellLineage"):
        create_third_basis_epoch_cumulative_handoff_research_session_shell(  # type: ignore[arg-type]
            object()
        )

    with pytest.raises(
        TypeError,
        match="ChromiumResearchThirdBasisEpochContinuationReentryResult",
    ):
        create_third_basis_epoch_continuation_handoff_research_session_shell(  # type: ignore[arg-type]
            object()
        )
