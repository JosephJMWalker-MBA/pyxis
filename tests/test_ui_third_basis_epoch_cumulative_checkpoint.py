from __future__ import annotations

from pathlib import Path

import pytest
from textual.widgets import Button, Input, Static

from pyxis.app.chromium_research_third_basis_epoch_shell_lineage import (
    prove_chromium_research_third_basis_epoch_continuation_shell_lineage,
)
from pyxis.ui.chromium_research_session_restart_plan_textual import (
    ResearchSessionRestartPlanControls,
)
from pyxis.ui.chromium_research_third_basis_epoch_continuation_checkpoint_extension_textual import (
    ThirdBasisEpochResearchSessionCumulativeCheckpointControls,
)
from pyxis.ui.third_basis_epoch_research_session_shell import (
    create_third_basis_epoch_continuation_research_session_shell,
)
from test_app_chromium_research_third_basis_epoch_continuation_checkpoint_extension import (
    _persist_extension,
)
from test_app_chromium_research_third_basis_epoch_continuation_reentry_plan_document import (
    _persist_valid_continuation,
)
from test_app_chromium_research_third_basis_epoch_reentry_plan_document import _root_shas
from test_ui_research_root_backed_session_continuation_checkpoint import (
    _press,
    _write_and_rollover,
)


def _shell_with_continuation_lineage(tmp_path: Path, *, stem: str):
    values = _persist_valid_continuation(tmp_path, stem=stem)
    overlay = values[6]
    earned = values[8].fresh_reentry
    lineage = prove_chromium_research_third_basis_epoch_continuation_shell_lineage(
        earned,
        overlay_source=overlay,
    )
    shell = create_third_basis_epoch_continuation_research_session_shell(lineage)
    return lineage, overlay, shell


def _shell_with_cumulative_lineage(tmp_path: Path, *, stem: str):
    *_, result = _persist_extension(tmp_path, stem=stem)
    lineage = prove_chromium_research_third_basis_epoch_continuation_shell_lineage(
        result.fresh_reentry,
        overlay_source=result.overlay.path,
    )
    shell = create_third_basis_epoch_continuation_research_session_shell(lineage)
    return lineage, result.overlay.path, shell


async def _save_cumulative(
    shell,
    pilot,
    *,
    current_overlay: Path,
    successor: Path,
    declaration_destination: Path,
    next_overlay: Path,
) -> None:
    shell.query_one(
        "#research-third-basis-epoch-cumulative-checkpoint-current-overlay-source",
        Input,
    ).value = str(current_overlay)
    shell.query_one(
        "#research-third-basis-epoch-cumulative-checkpoint-successor-source",
        Input,
    ).value = str(successor)
    shell.query_one(
        "#research-third-basis-epoch-cumulative-checkpoint-declaration-destination",
        Input,
    ).value = str(declaration_destination)
    shell.query_one(
        "#research-third-basis-epoch-cumulative-checkpoint-overlay-destination",
        Input,
    ).value = str(next_overlay)
    await _press(
        shell,
        pilot,
        "save-research-third-basis-epoch-cumulative-checkpoint",
    )


@pytest.mark.asyncio
async def test_successful_40d_checkpoint_visibly_promotes_fresh_cumulative_controller(
    tmp_path: Path,
) -> None:
    lineage, current_overlay, shell = _shell_with_continuation_lineage(
        tmp_path,
        stem="41d-promote",
    )
    current = lineage.reentry
    initial_count = len(current.plan.declared_edge_sources)
    fixed_anchor = current.plan.prior_third_basis_epoch_overlay_source
    original_roots = _root_shas(current.prior_third_basis_epoch_reentry)
    successor = tmp_path / "successor.json"
    one_hop_declaration = tmp_path / "one-hop-declaration.json"
    cumulative_declaration = tmp_path / "cumulative-declaration.json"
    next_overlay = tmp_path / "next.overlay.json"

    async with shell.run_test(size=(160, 250)) as pilot:
        await pilot.pause()
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=current.controller.declared_endpoint.verification.path,
            successor=successor,
            declaration=one_hop_declaration,
            text="Next cumulative successor above the third root.",
        )
        rollover = shell.last_research_rollover
        one_hop_controller = shell.research_controller
        assert rollover is not None
        assert shell.third_basis_epoch_continuation_reentry is current
        assert shell.query_one("#persist-research-endpoint-revision", Button).disabled
        controls = shell.query_one(ThirdBasisEpochResearchSessionCumulativeCheckpointControls)
        assert controls.current_reentry is current
        assert controls.rollover is rollover
        for selector in (
            "#research-third-basis-epoch-cumulative-checkpoint-current-overlay-source",
            "#research-third-basis-epoch-cumulative-checkpoint-successor-source",
            "#research-third-basis-epoch-cumulative-checkpoint-declaration-destination",
            "#research-third-basis-epoch-cumulative-checkpoint-overlay-destination",
        ):
            assert shell.query_one(selector, Input).value == ""

        await _save_cumulative(
            shell,
            pilot,
            current_overlay=current_overlay,
            successor=successor,
            declaration_destination=cumulative_declaration,
            next_overlay=next_overlay,
        )

        result = shell.last_third_basis_epoch_cumulative_checkpoint
        assert result is not None
        assert result.current_reentry is current
        assert result.rollover is rollover
        assert shell.third_basis_epoch_continuation_launch_lineage is lineage
        assert shell.third_basis_epoch_continuation_reentry is result.fresh_reentry
        assert shell.research_controller is result.fresh_reentry.controller
        assert shell.research_controller is not one_hop_controller
        assert shell.last_research_rollover is None
        assert result.next_plan.prior_third_basis_epoch_overlay_source == fixed_anchor
        assert len(result.next_plan.declared_edge_sources) == initial_count + 1
        assert _root_shas(result.fresh_reentry.prior_third_basis_epoch_reentry) == original_roots
        assert len(set(original_roots)) == 3
        assert (
            shell.research_controller.declared_endpoint.verification.edge_record_sha256
            == one_hop_controller.declared_endpoint.verification.edge_record_sha256
        )
        assert (
            shell.research_controller.declared_endpoint.revision.revised_note.note_text
            == one_hop_controller.declared_endpoint.revision.revised_note.note_text
        )
        assert len(shell.research_presentation.members) == len(
            result.next_plan.declared_edge_sources
        )
        assert len(shell.query(ThirdBasisEpochResearchSessionCumulativeCheckpointControls)) == 0
        assert len(shell.query(ResearchSessionRestartPlanControls)) == 0
        assert not shell.query_one("#persist-research-endpoint-revision", Button).disabled
        receipt = str(
            shell.query_one(
                "#research-third-basis-epoch-cumulative-checkpoint-success-receipt",
                Static,
            ).content
        )
        assert f"edge count: {initial_count + 1}" in receipt
        assert "not a global latest/current/head" in receipt


@pytest.mark.asyncio
async def test_two_cumulative_cycles_grow_edge_tuple_without_recursive_overlay_ancestry(
    tmp_path: Path,
) -> None:
    lineage, current_overlay, shell = _shell_with_continuation_lineage(
        tmp_path,
        stem="41d-repeat",
    )
    original_launch_reentry = lineage.reentry
    initial_count = len(original_launch_reentry.plan.declared_edge_sources)
    fixed_anchor = original_launch_reentry.plan.prior_third_basis_epoch_overlay_source
    original_roots = _root_shas(original_launch_reentry.prior_third_basis_epoch_reentry)

    async with shell.run_test(size=(160, 270)) as pilot:
        await pilot.pause()
        prior = shell.third_basis_epoch_continuation_reentry
        successor1 = tmp_path / "successor-1.json"
        one_hop1 = tmp_path / "one-hop-1.json"
        cumulative1 = tmp_path / "cumulative-1.json"
        overlay1 = tmp_path / "overlay-1.json"
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=prior.controller.declared_endpoint.verification.path,
            successor=successor1,
            declaration=one_hop1,
            text="Cumulative successor one above the third root.",
        )
        await _save_cumulative(
            shell,
            pilot,
            current_overlay=current_overlay,
            successor=successor1,
            declaration_destination=cumulative1,
            next_overlay=overlay1,
        )
        first = shell.last_third_basis_epoch_cumulative_checkpoint
        assert first is not None
        assert len(first.next_plan.declared_edge_sources) == initial_count + 1
        assert first.next_plan.prior_third_basis_epoch_overlay_source == fixed_anchor
        assert shell.third_basis_epoch_continuation_reentry is first.fresh_reentry
        assert shell.third_basis_epoch_continuation_launch_lineage is lineage
        assert _root_shas(first.fresh_reentry.prior_third_basis_epoch_reentry) == original_roots

        prior2 = shell.third_basis_epoch_continuation_reentry
        successor2 = tmp_path / "successor-2.json"
        one_hop2 = tmp_path / "one-hop-2.json"
        cumulative2 = tmp_path / "cumulative-2.json"
        overlay2 = tmp_path / "overlay-2.json"
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=prior2.controller.declared_endpoint.verification.path,
            successor=successor2,
            declaration=one_hop2,
            text="Cumulative successor two above the third root.",
        )
        controls = shell.query_one(ThirdBasisEpochResearchSessionCumulativeCheckpointControls)
        assert controls.current_reentry is prior2
        for selector in (
            "#research-third-basis-epoch-cumulative-checkpoint-current-overlay-source",
            "#research-third-basis-epoch-cumulative-checkpoint-successor-source",
            "#research-third-basis-epoch-cumulative-checkpoint-declaration-destination",
            "#research-third-basis-epoch-cumulative-checkpoint-overlay-destination",
        ):
            assert shell.query_one(selector, Input).value == ""

        await _save_cumulative(
            shell,
            pilot,
            current_overlay=overlay1,
            successor=successor2,
            declaration_destination=cumulative2,
            next_overlay=overlay2,
        )
        second = shell.last_third_basis_epoch_cumulative_checkpoint
        assert second is not None
        assert second.current_reentry is prior2
        assert len(second.next_plan.declared_edge_sources) == initial_count + 2
        assert second.next_plan.prior_third_basis_epoch_overlay_source == fixed_anchor
        assert second.next_plan.prior_third_basis_epoch_overlay_source != overlay1.resolve()
        assert shell.third_basis_epoch_continuation_reentry is second.fresh_reentry
        assert shell.third_basis_epoch_continuation_launch_lineage is lineage
        assert lineage.reentry is original_launch_reentry
        assert _root_shas(second.fresh_reentry.prior_third_basis_epoch_reentry) == original_roots
        assert shell.last_research_rollover is None
        assert not shell.query_one("#persist-research-endpoint-revision", Button).disabled
        assert len(shell.research_presentation.members) == initial_count + 2


@pytest.mark.asyncio
async def test_failed_cumulative_checkpoint_keeps_one_hop_visible_locked_and_typed_state_unadvanced(
    tmp_path: Path,
) -> None:
    lineage, current_overlay, shell = _shell_with_continuation_lineage(
        tmp_path,
        stem="41d-failure",
    )
    current = lineage.reentry
    successor = tmp_path / "chosen.json"
    one_hop = tmp_path / "one-hop.json"
    wrong = tmp_path / "wrong.json"
    cumulative = tmp_path / "cumulative.json"
    next_overlay = tmp_path / "next.json"

    async with shell.run_test(size=(160, 250)) as pilot:
        await pilot.pause()
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=current.controller.declared_endpoint.verification.path,
            successor=successor,
            declaration=one_hop,
            text="Chosen cumulative third-epoch successor.",
        )
        one_hop_controller = shell.research_controller
        current.controller.persist_declared_endpoint_revision(
            "Wrong sibling successor.",
            prior_edge_source=current.controller.declared_endpoint.verification.path,
            destination=wrong,
        )
        await _save_cumulative(
            shell,
            pilot,
            current_overlay=current_overlay,
            successor=wrong,
            declaration_destination=cumulative,
            next_overlay=next_overlay,
        )

        assert shell.last_third_basis_epoch_cumulative_checkpoint is None
        assert shell.third_basis_epoch_continuation_reentry is current
        assert shell.third_basis_epoch_continuation_launch_lineage is lineage
        assert shell.research_controller is one_hop_controller
        assert shell.last_research_rollover is not None
        assert shell.query_one("#persist-research-endpoint-revision", Button).disabled
        assert len(shell.query(ThirdBasisEpochResearchSessionCumulativeCheckpointControls)) == 1
        assert not cumulative.exists()
        assert not next_overlay.exists()


@pytest.mark.asyncio
async def test_cumulative_checkpoint_accepts_explicit_path_distinct_equivalent_current_overlay(
    tmp_path: Path,
) -> None:
    first_dir = tmp_path / "first"
    second_dir = tmp_path / "second"
    first_dir.mkdir()
    second_dir.mkdir()
    first_values = _persist_valid_continuation(first_dir, stem="same")
    second_values = _persist_valid_continuation(second_dir, stem="same")
    first_overlay = first_values[6]
    first_earned = first_values[8].fresh_reentry
    other_overlay = second_values[6]
    other_earned = second_values[8].fresh_reentry
    lineage = prove_chromium_research_third_basis_epoch_continuation_shell_lineage(
        first_earned,
        overlay_source=first_overlay,
    )
    shell = create_third_basis_epoch_continuation_research_session_shell(lineage)
    successor = tmp_path / "successor.json"
    one_hop = tmp_path / "one-hop.json"
    cumulative = tmp_path / "cumulative.json"
    next_overlay = tmp_path / "next.json"

    assert other_overlay.resolve() != lineage.overlay_source
    assert other_earned.controller.presentation == lineage.reentry.controller.presentation
    assert _root_shas(other_earned.prior_third_basis_epoch_reentry) == _root_shas(
        lineage.reentry.prior_third_basis_epoch_reentry
    )

    async with shell.run_test(size=(160, 250)) as pilot:
        await pilot.pause()
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=lineage.reentry.controller.declared_endpoint.verification.path,
            successor=successor,
            declaration=one_hop,
            text="Path-distinct cumulative third-epoch successor.",
        )
        await _save_cumulative(
            shell,
            pilot,
            current_overlay=other_overlay,
            successor=successor,
            declaration_destination=cumulative,
            next_overlay=next_overlay,
        )

        result = shell.last_third_basis_epoch_cumulative_checkpoint
        assert result is not None
        assert result.current_reentry is lineage.reentry
        assert result.current_plan.prior_third_basis_epoch_overlay_source == (
            other_earned.plan.prior_third_basis_epoch_overlay_source
        )
        assert shell.third_basis_epoch_continuation_reentry is result.fresh_reentry
        assert next_overlay.exists()


@pytest.mark.asyncio
async def test_existing_cumulative_40d_launch_can_checkpoint_another_successor(
    tmp_path: Path,
) -> None:
    lineage, current_overlay, shell = _shell_with_cumulative_lineage(
        tmp_path,
        stem="41d-existing-cumulative",
    )
    current = lineage.reentry
    initial_count = len(current.plan.declared_edge_sources)
    successor = tmp_path / "next-successor.json"
    one_hop = tmp_path / "next-one-hop.json"
    cumulative = tmp_path / "next-cumulative.json"
    next_overlay = tmp_path / "next-overlay.json"

    async with shell.run_test(size=(160, 250)) as pilot:
        await pilot.pause()
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=current.controller.declared_endpoint.verification.path,
            successor=successor,
            declaration=one_hop,
            text="Continuation after an already cumulative 40D launch.",
        )
        await _save_cumulative(
            shell,
            pilot,
            current_overlay=current_overlay,
            successor=successor,
            declaration_destination=cumulative,
            next_overlay=next_overlay,
        )

        result = shell.last_third_basis_epoch_cumulative_checkpoint
        assert result is not None
        assert len(result.next_plan.declared_edge_sources) == initial_count + 1
        assert shell.third_basis_epoch_continuation_reentry is result.fresh_reentry
        assert shell.third_basis_epoch_continuation_launch_lineage is lineage
        assert not shell.query_one("#persist-research-endpoint-revision", Button).disabled
