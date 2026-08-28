from __future__ import annotations

from pathlib import Path

import pytest

from pyxis.app.chromium_research_root_backed_session_shell_lineage import (
    prove_chromium_research_root_backed_session_continuation_shell_lineage,
    prove_chromium_research_root_backed_session_shell_lineage,
)
from pyxis.ui.root_backed_authority_inspection_shell import (
    create_inspectable_root_backed_continuation_handoff_research_session_shell,
    create_inspectable_root_backed_continuation_research_session_shell,
    create_inspectable_root_backed_handoff_research_session_shell,
    create_inspectable_root_backed_research_session_shell,
)
from test_app_chromium_research_root_backed_session_continuation_reentry_plan_document import (
    _persist_valid_continuation,
)
from test_app_chromium_research_root_backed_session_reentry_plan_document import (
    _persist_valid_overlay,
)
from test_ui_research_root_backed_session_continuation_checkpoint import (
    _write_and_rollover as _write_first_rollover,
)
from test_ui_research_root_backed_session_cumulative_checkpoint import (
    _save_cumulative_checkpoint,
    _write_and_rollover as _write_cumulative_rollover,
)


@pytest.mark.asyncio
async def test_persisted_35c_shell_keeps_exact_launch_provenance_through_rollover(
    tmp_path: Path,
) -> None:
    _, _, earned, _, overlay, _ = _persist_valid_overlay(tmp_path, stem="45a-ui-35c")
    lineage = prove_chromium_research_root_backed_session_shell_lineage(
        earned,
        overlay_source=overlay,
    )
    shell = create_inspectable_root_backed_research_session_shell(lineage)
    successor = tmp_path / "successor.json"
    declaration = tmp_path / "one-hop-declaration.json"

    async with shell.run_test(size=(170, 200)) as pilot:
        await pilot.pause()
        panel = shell.root_backed_authority_inspection
        launch = panel.launch_provenance
        assert launch.launch_location_context == overlay.resolve()
        assert launch.launch_family == "persisted 35C root-backed launch"
        assert panel.current_state.state_source == "persisted 35C launch"

        await _write_first_rollover(
            shell,
            pilot,
            prior_edge=lineage.reentry.controller.declared_endpoint.verification.path,
            successor=successor,
            declaration=declaration,
            text="Visible one-hop continuation after persisted 35C launch.",
        )

        assert panel.launch_provenance is launch
        assert panel.launch_provenance.launch_location_context == overlay.resolve()
        assert panel.current_state.state_kind == "visible one-hop continuation"
        assert panel.current_state.state_source == (
            "explicit rollover from persisted 35C launch"
        )
        assert panel.current_state.endpoint_sha256 == (
            shell.research_controller.declared_endpoint.verification.edge_record_sha256
        )


@pytest.mark.asyncio
async def test_raw_44h_shell_visibly_fabricates_no_persistent_launch_path(
    tmp_path: Path,
) -> None:
    _, _, handoff, _, overlay, _ = _persist_valid_overlay(tmp_path, stem="45a-ui-44h")
    shell = create_inspectable_root_backed_handoff_research_session_shell(handoff)

    async with shell.run_test(size=(170, 150)) as pilot:
        await pilot.pause()
        panel = shell.root_backed_authority_inspection
        assert panel.launch_provenance.launch_family == (
            "in-process 44H typed root-backed handoff"
        )
        assert panel.launch_provenance.launch_location_context is None
        rendered = str(panel.content)
        assert "no persistent launch path" in rendered
        assert str(overlay.resolve()) not in rendered


@pytest.mark.asyncio
async def test_persisted_35d_and_raw_36d_shells_render_distinct_launch_location_semantics(
    tmp_path: Path,
) -> None:
    values = _persist_valid_continuation(tmp_path, stem="45a-ui-cont")
    overlay = values[8]
    handoff = values[9].fresh_reentry
    lineage = prove_chromium_research_root_backed_session_continuation_shell_lineage(
        handoff,
        overlay_source=overlay,
    )
    persisted_shell = create_inspectable_root_backed_continuation_research_session_shell(
        lineage
    )
    raw_shell = create_inspectable_root_backed_continuation_handoff_research_session_shell(
        handoff
    )

    async with persisted_shell.run_test(size=(170, 150)) as pilot:
        await pilot.pause()
        persisted = persisted_shell.root_backed_authority_inspection
        assert persisted.launch_provenance.launch_location_context == overlay.resolve()
        assert str(overlay.resolve()) in str(persisted.content)

    async with raw_shell.run_test(size=(170, 150)) as pilot:
        await pilot.pause()
        raw = raw_shell.root_backed_authority_inspection
        assert raw.launch_provenance.launch_location_context is None
        rendered = str(raw.content)
        assert "no persistent launch path" in rendered
        assert str(overlay.resolve()) not in rendered


@pytest.mark.asyncio
async def test_persisted_continuation_launch_provenance_survives_35e_promotion(
    tmp_path: Path,
) -> None:
    values = _persist_valid_continuation(tmp_path, stem="45a-ui-35e")
    overlay = values[8]
    earned = values[9].fresh_reentry
    lineage = prove_chromium_research_root_backed_session_continuation_shell_lineage(
        earned,
        overlay_source=overlay,
    )
    shell = create_inspectable_root_backed_continuation_research_session_shell(lineage)
    current = lineage.reentry
    successor = tmp_path / "next-edge.json"
    one_hop_declaration = tmp_path / "one-hop.json"
    cumulative_declaration = tmp_path / "cumulative.json"
    next_overlay = tmp_path / "next.overlay.json"

    async with shell.run_test(size=(175, 240)) as pilot:
        await pilot.pause()
        panel = shell.root_backed_authority_inspection
        launch = panel.launch_provenance
        assert launch.launch_location_context == overlay.resolve()

        await _write_cumulative_rollover(
            shell,
            pilot,
            prior_edge=current.controller.declared_endpoint.verification.path,
            successor=successor,
            declaration=one_hop_declaration,
            text="Promote while preserving exact launch provenance.",
        )
        assert panel.launch_provenance is launch
        assert panel.current_state.state_source == "persisted 35D/35E launch"

        await _save_cumulative_checkpoint(
            shell,
            pilot,
            current_overlay=overlay,
            successor=successor,
            cumulative_declaration=cumulative_declaration,
            next_overlay=next_overlay,
        )

        result = shell.last_root_backed_cumulative_checkpoint
        assert result is not None
        assert panel.launch_provenance is launch
        assert panel.launch_provenance.launch_location_context == overlay.resolve()
        assert panel.current_state.state_source == "35E cumulative promotion"
        assert panel.current_state.endpoint_sha256 == (
            result.fresh_reentry.controller.declared_endpoint.verification.edge_record_sha256
        )
        assert panel.current_state.declared_continuation_edge_count == len(
            result.fresh_reentry.plan.declared_edge_sources
        )
