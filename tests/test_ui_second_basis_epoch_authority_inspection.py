from __future__ import annotations

from pathlib import Path

import pytest
from textual.widgets import Static

from pyxis.app.chromium_research_second_basis_epoch_shell_lineage import (
    prove_chromium_research_second_basis_epoch_continuation_shell_lineage,
    prove_chromium_research_second_basis_epoch_shell_lineage,
)
from pyxis.ui.chromium_research_second_basis_epoch_authority_inspection_textual import (
    SecondBasisEpochAuthorityInspectionPanel,
)
from pyxis.ui.second_basis_epoch_authority_inspection_shell import (
    create_inspectable_second_basis_epoch_continuation_handoff_research_session_shell,
    create_inspectable_second_basis_epoch_continuation_research_session_shell,
    create_inspectable_second_basis_epoch_cumulative_handoff_research_session_shell,
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
from test_ui_second_basis_epoch_cumulative_checkpoint import _save_cumulative


def _first_launch(tmp_path: Path, *, stem: str):
    tmp_path.mkdir(parents=True, exist_ok=True)
    _, earned, overlay, _ = _persist_valid_overlay(tmp_path, stem=stem)
    lineage = prove_chromium_research_second_basis_epoch_shell_lineage(
        earned,
        overlay_source=overlay,
    )
    shell = create_inspectable_second_basis_epoch_cumulative_handoff_research_session_shell(
        lineage
    )
    return lineage, overlay, shell


def _continuation_launch(tmp_path: Path, *, stem: str):
    tmp_path.mkdir(parents=True, exist_ok=True)
    values = _persist_valid_continuation(tmp_path, stem=stem)
    overlay = values[6]
    earned = values[8].fresh_reentry
    lineage = prove_chromium_research_second_basis_epoch_continuation_shell_lineage(
        earned,
        overlay_source=overlay,
    )
    shell = create_inspectable_second_basis_epoch_continuation_research_session_shell(
        lineage
    )
    return values, lineage, overlay, shell


def _first_root_sha_from_second_epoch(reentry) -> str:
    return (
        reentry.prior_continuation_reentry.prior_root_backed_reentry
        .loaded_root.verification.root_record_sha256
    )


def _first_root_sha_from_continuation(reentry) -> str:
    return _first_root_sha_from_second_epoch(reentry.prior_second_basis_epoch_reentry)


@pytest.mark.asyncio
async def test_persisted_37b_launch_visibly_separates_location_and_root_authority(
    tmp_path: Path,
) -> None:
    lineage, overlay, shell = _first_launch(tmp_path / "first", stem="39a-first")
    reentry = lineage.reentry
    inspection = shell.second_basis_epoch_authority_inspection

    assert isinstance(inspection, SecondBasisEpochAuthorityInspectionPanel)
    assert inspection.launch_provenance.launch_location_context == overlay.resolve()
    assert (
        inspection.launch_provenance.first_root_sha256
        == _first_root_sha_from_second_epoch(reentry)
    )
    assert (
        inspection.launch_provenance.second_root_sha256
        == reentry.loaded_root.verification.root_record_sha256
    )
    assert (
        inspection.current_state.endpoint_sha256
        == reentry.controller.declared_endpoint.verification.edge_record_sha256
    )
    assert inspection.current_state.declared_continuation_edge_count is None

    async with shell.run_test(size=(165, 220)) as pilot:
        await pilot.pause()
        text = str(
            shell.query_one(
                "#research-second-basis-epoch-authority-inspection",
                Static,
            ).content
        )
        assert "persisted 37B second-basis-epoch launch" in text
        assert str(overlay.resolve()) in text
        assert "launch location context only" in text.lower()
        assert "not current/latest/head" in text
        assert "do not establish authorship" in text


@pytest.mark.asyncio
async def test_first_shell_rollover_updates_only_current_visible_state(
    tmp_path: Path,
) -> None:
    lineage, overlay, shell = _first_launch(tmp_path / "rollover", stem="39a-rollover")
    launch = shell.second_basis_epoch_authority_inspection.launch_provenance
    prior = lineage.reentry
    successor = tmp_path / "successor.json"
    declaration = tmp_path / "declaration.json"

    async with shell.run_test(size=(165, 230)) as pilot:
        await pilot.pause()
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=prior.controller.declared_endpoint.verification.path,
            successor=successor,
            declaration=declaration,
            text="Visible current state advances without rewriting launch provenance.",
        )

        inspection = shell.second_basis_epoch_authority_inspection
        assert inspection.launch_provenance is launch
        assert inspection.launch_provenance.launch_location_context == overlay.resolve()
        assert inspection.current_state.state_kind == "visible one-hop continuation"
        assert inspection.current_state.state_source == (
            "explicit rollover from persisted 37B launch"
        )
        assert (
            inspection.current_state.endpoint_sha256
            == shell.research_controller.declared_endpoint.verification.edge_record_sha256
        )
        assert inspection.current_state.declared_continuation_edge_count is None


@pytest.mark.asyncio
async def test_persisted_37c_launch_shows_path_context_and_typed_edge_count(
    tmp_path: Path,
) -> None:
    _, lineage, overlay, shell = _continuation_launch(
        tmp_path / "persisted",
        stem="39a-persisted",
    )
    current = lineage.reentry
    inspection = shell.second_basis_epoch_authority_inspection

    assert inspection.launch_provenance.launch_location_context == overlay.resolve()
    assert inspection.launch_provenance.launch_family == (
        "persisted 37C/37D continuation launch"
    )
    assert (
        inspection.launch_provenance.first_root_sha256
        == _first_root_sha_from_continuation(current)
    )
    assert (
        inspection.launch_provenance.second_root_sha256
        == current.prior_second_basis_epoch_reentry.loaded_root.verification.root_record_sha256
    )
    assert inspection.current_state.declared_continuation_edge_count == len(
        current.plan.declared_edge_sources
    )

    async with shell.run_test(size=(165, 220)) as pilot:
        await pilot.pause()
        text = str(
            shell.query_one(
                "#research-second-basis-epoch-authority-inspection",
                Static,
            ).content
        )
        assert str(overlay.resolve()) in text
        assert "Current governed state" in text
        assert "typed second-basis-epoch continuation" in text


@pytest.mark.asyncio
async def test_in_process_handoff_exposes_no_persistent_launch_path(
    tmp_path: Path,
) -> None:
    values = _persist_valid_continuation(tmp_path, stem="39a-handoff")
    persisted_overlay = values[6]
    handoff = values[8].fresh_reentry
    shell = create_inspectable_second_basis_epoch_continuation_handoff_research_session_shell(
        handoff
    )
    inspection = shell.second_basis_epoch_authority_inspection

    assert inspection.launch_provenance.launch_location_context is None
    assert inspection.launch_provenance.launch_family == (
        "in-process 38F typed continuation handoff"
    )
    assert inspection.current_state.state_source == "in-process 38F handoff"
    assert inspection.current_state.declared_continuation_edge_count == len(
        handoff.plan.declared_edge_sources
    )

    async with shell.run_test(size=(165, 220)) as pilot:
        await pilot.pause()
        text = str(
            shell.query_one(
                "#research-second-basis-epoch-authority-inspection",
                Static,
            ).content
        )
        assert "no persistent launch path" in text
        assert str(persisted_overlay.resolve()) not in text
        assert "not current/latest/head" in text


@pytest.mark.asyncio
async def test_persisted_cumulative_promotion_preserves_launch_and_advances_current(
    tmp_path: Path,
) -> None:
    _, lineage, current_overlay, shell = _continuation_launch(
        tmp_path / "cumulative",
        stem="39a-cumulative",
    )
    current = lineage.reentry
    inspection = shell.second_basis_epoch_authority_inspection
    launch = inspection.launch_provenance
    initial_count = len(current.plan.declared_edge_sources)
    successor = tmp_path / "cumulative-successor.json"
    one_hop_declaration = tmp_path / "cumulative-one-hop.json"
    cumulative_declaration = tmp_path / "cumulative-declaration.json"
    next_overlay = tmp_path / "cumulative-next.overlay.json"

    async with shell.run_test(size=(165, 240)) as pilot:
        await pilot.pause()
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=current.controller.declared_endpoint.verification.path,
            successor=successor,
            declaration=one_hop_declaration,
            text="Promote current typed continuation without rewriting launch provenance.",
        )
        await _save_cumulative(
            shell,
            pilot,
            current_overlay=current_overlay,
            successor=successor,
            declaration_destination=cumulative_declaration,
            next_overlay=next_overlay,
        )

        result = shell.last_second_basis_epoch_cumulative_checkpoint
        assert result is not None
        assert inspection.launch_provenance is launch
        assert launch.launch_location_context == current_overlay.resolve()
        assert inspection.current_state.state_source == "37D cumulative promotion"
        assert inspection.current_state.declared_continuation_edge_count == initial_count + 1
        assert (
            inspection.current_state.endpoint_sha256
            == result.fresh_reentry.controller.declared_endpoint.verification.edge_record_sha256
        )


@pytest.mark.asyncio
async def test_handoff_checkpoint_path_never_backfills_launch_provenance(
    tmp_path: Path,
) -> None:
    values = _persist_valid_continuation(tmp_path / "handoff-cumulative", stem="39a-handoff-cumulative")
    current_overlay = values[6]
    handoff = values[8].fresh_reentry
    shell = create_inspectable_second_basis_epoch_continuation_handoff_research_session_shell(
        handoff
    )
    inspection = shell.second_basis_epoch_authority_inspection
    launch = inspection.launch_provenance
    initial_count = len(handoff.plan.declared_edge_sources)
    successor = tmp_path / "handoff-successor.json"
    one_hop_declaration = tmp_path / "handoff-one-hop.json"
    cumulative_declaration = tmp_path / "handoff-cumulative-declaration.json"
    next_overlay = tmp_path / "handoff-next.overlay.json"

    async with shell.run_test(size=(165, 240)) as pilot:
        await pilot.pause()
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=handoff.controller.declared_endpoint.verification.path,
            successor=successor,
            declaration=one_hop_declaration,
            text="Explicit checkpoint path must not become launch provenance.",
        )
        await _save_cumulative(
            shell,
            pilot,
            current_overlay=current_overlay,
            successor=successor,
            declaration_destination=cumulative_declaration,
            next_overlay=next_overlay,
        )

        result = shell.last_second_basis_epoch_cumulative_checkpoint
        assert result is not None
        assert inspection.launch_provenance is launch
        assert inspection.launch_provenance.launch_location_context is None
        assert inspection.current_state.state_source == (
            "37D cumulative promotion after in-process handoff"
        )
        assert inspection.current_state.declared_continuation_edge_count == initial_count + 1
        text = str(
            shell.query_one(
                "#research-second-basis-epoch-authority-inspection",
                Static,
            ).content
        )
        assert "no persistent launch path" in text
        assert str(current_overlay.resolve()) not in text
