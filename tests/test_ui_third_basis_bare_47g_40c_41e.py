from __future__ import annotations

import json
from pathlib import Path

import pytest
from textual.widgets import Button, Input

from pyxis.ui.chromium_research_third_basis_epoch_continuation_checkpoint_extension_textual import (
    ThirdBasisEpochResearchSessionCumulativeCheckpointControls,
)
from pyxis.ui.chromium_research_third_basis_epoch_continuation_checkpoint_textual import (
    ThirdBasisEpochResearchSessionContinuationCheckpointControls,
)
from pyxis.ui.third_basis_epoch_authority_inspection_shell import (
    create_inspectable_third_basis_epoch_continuation_handoff_research_session_shell,
)
from pyxis.ui.third_basis_epoch_session_handoff_authority_inspection_shell import (
    create_inspectable_third_basis_epoch_handoff_research_session_shell,
)
from test_app_chromium_research_third_basis_epoch_reentry_plan_document_v2 import (
    _persist_bare_third_basis_overlay,
)
from test_cli_third_basis_bare_overlay_v2_relaunch import (
    _assert_three_bare_passages_survive,
)
from test_third_basis_bare_continuation_v1 import (
    _assert_three_bare_passages_survive_continuation,
)
from test_ui_research_root_backed_session_continuation_checkpoint import (
    _press,
    _write_and_rollover,
)
from test_ui_third_basis_epoch_first_continuation_checkpoint import (
    _save_checkpoint,
)


_OVERLAY_V2 = "pyxis.chromium.research_third_basis_epoch_reentry_locator_overlay.v2"
_CONTINUATION_V1 = (
    "pyxis.chromium.research_third_basis_epoch_continuation_locator_overlay.v1"
)


@pytest.mark.asyncio
async def test_50w_pathless_47g_can_checkpoint_40c_then_handoff_41e_pathlessly(
    tmp_path: Path,
    monkeypatch,
) -> None:
    values = _persist_bare_third_basis_overlay(
        tmp_path,
        stem="50w-third",
    )
    third_overlay = values[10]
    third_checkpoint = values[11]
    third_handoff = third_checkpoint.checkpoint.fresh_reentry

    assert json.loads(third_overlay.read_text(encoding="utf-8"))["format"] == _OVERLAY_V2
    _assert_three_bare_passages_survive(third_handoff)

    source = create_inspectable_third_basis_epoch_handoff_research_session_shell(
        third_handoff
    )
    assert source.third_basis_epoch_launch_lineage is None
    assert source.third_basis_epoch_handoff_reentry is third_handoff
    assert source.third_basis_epoch_reentry is third_handoff
    assert source.research_controller is third_handoff.controller

    source_panel = source.third_basis_epoch_authority_inspection
    source_launch = source_panel.launch_provenance
    assert source_launch.launch_family == (
        "in-process 47G typed third-basis-epoch handoff"
    )
    assert source_launch.launch_location_context is None

    observed: dict[str, object] = {}
    monkeypatch.setattr(
        source,
        "exit",
        lambda result=None, *args, **kwargs: observed.__setitem__("result", result),
    )

    successor = tmp_path / "50w-successor.json"
    declaration = tmp_path / "50w-declaration.json"
    continuation_overlay = tmp_path / "50w-40c.overlay.json"

    async with source.run_test(size=(205, 360)) as pilot:
        await pilot.pause()
        assert len(
            source.query(ThirdBasisEpochResearchSessionContinuationCheckpointControls)
        ) == 0
        assert len(source.query("#continue-third-basis-epoch-cumulative-mode")) == 0

        await _write_and_rollover(
            source,
            pilot,
            prior_edge=third_handoff.controller.declared_endpoint.verification.path,
            successor=successor,
            declaration=declaration,
            text="50W first continuation after pathless bare 47G handoff.",
        )

        controls = source.query_one(
            ThirdBasisEpochResearchSessionContinuationCheckpointControls
        )
        assert controls.rollover is source.last_research_rollover
        for selector in (
            "#research-third-basis-epoch-checkpoint-prior-overlay-source",
            "#research-third-basis-epoch-checkpoint-successor-source",
            "#research-third-basis-epoch-checkpoint-declaration-source",
            "#research-third-basis-epoch-checkpoint-destination",
        ):
            assert source.query_one(selector, Input).value == ""

        assert source_panel.launch_provenance is source_launch
        assert source_panel.launch_provenance.launch_location_context is None
        rollover_state = source_panel.current_state
        assert rollover_state.state_source == (
            "explicit rollover after in-process 47G handoff"
        )

        await _save_checkpoint(
            source,
            pilot,
            prior_overlay=third_overlay,
            successor=successor,
            declaration=declaration,
            destination=continuation_overlay,
        )

        checkpoint = source.last_third_basis_epoch_continuation_checkpoint
        assert checkpoint is not None
        assert checkpoint.prior_reentry is third_handoff
        assert checkpoint.rollover is source.last_research_rollover
        assert checkpoint.plan.prior_third_basis_epoch_overlay_source == (
            third_overlay.resolve()
        )
        assert checkpoint.persistence.path == continuation_overlay.resolve()
        assert source_panel.launch_provenance is source_launch
        assert source_panel.current_state is rollover_state
        _assert_three_bare_passages_survive_continuation(checkpoint.fresh_reentry)

        document = json.loads(continuation_overlay.read_text(encoding="utf-8"))
        assert document["format"] == _CONTINUATION_V1
        assert set(document) == {
            "format",
            "prior_third_basis_epoch_overlay_source",
            "declared_edge_sources",
            "declaration_source",
        }
        assert (
            continuation_overlay.parent
            / document["prior_third_basis_epoch_overlay_source"]
        ).resolve() == third_overlay.resolve()

        assert "result" not in observed
        button = source.query_one(
            "#continue-third-basis-epoch-cumulative-mode",
            Button,
        )
        assert not button.disabled
        assert len(source.query("#continue-third-basis-epoch-cumulative-mode")) == 1

        expected_41e = checkpoint.fresh_reentry
        # 41E must transfer the exact typed proof already in memory, not reload 40C.
        continuation_overlay.unlink()
        assert not continuation_overlay.exists()

        await _press(
            source,
            pilot,
            "continue-third-basis-epoch-cumulative-mode",
        )
        assert observed["result"] is expected_41e
        assert source.third_basis_epoch_launch_lineage is None
        assert source.third_basis_epoch_handoff_reentry is third_handoff
        assert source.third_basis_epoch_reentry is third_handoff
        assert source_panel.launch_provenance is source_launch
        assert source_panel.current_state is rollover_state

    handoff = observed["result"]
    assert handoff is expected_41e
    _assert_three_bare_passages_survive_continuation(handoff)

    cumulative = (
        create_inspectable_third_basis_epoch_continuation_handoff_research_session_shell(
            handoff
        )
    )
    assert cumulative.third_basis_epoch_continuation_launch_lineage is None
    assert cumulative.third_basis_epoch_continuation_handoff_reentry is handoff
    assert cumulative.third_basis_epoch_continuation_reentry is handoff
    assert cumulative.research_controller is handoff.controller
    assert not hasattr(cumulative, "current_overlay_source")
    assert not hasattr(cumulative, "overlay_source")

    panel = cumulative.third_basis_epoch_authority_inspection
    launch = panel.launch_provenance
    assert launch.launch_family == "in-process 41E typed continuation handoff"
    assert launch.launch_location_context is None
    assert panel.current_state.state_source == "in-process 41E handoff"
    assert panel.current_state.declared_continuation_edge_count == 1

    next_successor = tmp_path / "50w-next-successor.json"
    next_one_hop = tmp_path / "50w-next-one-hop.json"

    async with cumulative.run_test(size=(205, 340)) as pilot:
        await pilot.pause()
        assert len(
            cumulative.query(ThirdBasisEpochResearchSessionCumulativeCheckpointControls)
        ) == 0

        current_before = panel.current_state
        await _write_and_rollover(
            cumulative,
            pilot,
            prior_edge=handoff.controller.declared_endpoint.verification.path,
            successor=next_successor,
            declaration=next_one_hop,
            text="50W first cumulative successor after exact pathless 41E handoff.",
        )

        controls = cumulative.query_one(
            ThirdBasisEpochResearchSessionCumulativeCheckpointControls
        )
        assert controls.current_reentry is handoff
        for selector in (
            "#research-third-basis-epoch-cumulative-checkpoint-current-overlay-source",
            "#research-third-basis-epoch-cumulative-checkpoint-successor-source",
            "#research-third-basis-epoch-cumulative-checkpoint-declaration-destination",
            "#research-third-basis-epoch-cumulative-checkpoint-overlay-destination",
        ):
            assert cumulative.query_one(selector, Input).value == ""

        assert panel.launch_provenance is launch
        assert panel.launch_provenance.launch_location_context is None
        assert panel.current_state is not current_before
        assert panel.current_state.state_kind == "visible one-hop continuation"
        assert panel.current_state.state_source == (
            "explicit rollover after in-process 41E handoff"
        )
        assert (
            panel.current_state.endpoint_sha256
            == cumulative.research_controller.declared_endpoint.verification.edge_record_sha256
        )
