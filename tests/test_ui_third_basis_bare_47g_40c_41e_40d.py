from __future__ import annotations

import json
from pathlib import Path

import pytest
from textual.widgets import Button, Input

from pyxis.ui.chromium_research_third_basis_epoch_continuation_checkpoint_extension_textual import (
    ThirdBasisEpochResearchSessionCumulativeCheckpointControls,
)
from pyxis.ui.third_basis_epoch_authority_inspection_shell import (
    create_inspectable_third_basis_epoch_continuation_handoff_research_session_shell,
)
from pyxis.ui.third_basis_epoch_session_handoff_authority_inspection_shell import (
    create_inspectable_third_basis_epoch_handoff_research_session_shell,
)
from test_app_chromium_research_third_basis_epoch_reentry_plan_document import (
    _root_shas,
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
from test_ui_third_basis_epoch_cumulative_checkpoint import (
    _save_cumulative,
)
from test_ui_third_basis_epoch_first_continuation_checkpoint import (
    _save_checkpoint,
)


_OVERLAY_V2 = "pyxis.chromium.research_third_basis_epoch_reentry_locator_overlay.v2"
_CONTINUATION_V1 = (
    "pyxis.chromium.research_third_basis_epoch_continuation_locator_overlay.v1"
)


@pytest.mark.asyncio
async def test_50x_pathless_47g_40c_41e_chain_can_persist_and_promote_40d(
    tmp_path: Path,
    monkeypatch,
) -> None:
    values = _persist_bare_third_basis_overlay(
        tmp_path,
        stem="50x-third",
    )
    third_overlay = values[10]
    third_checkpoint = values[11]
    third_handoff = third_checkpoint.checkpoint.fresh_reentry

    assert json.loads(third_overlay.read_text(encoding="utf-8"))["format"] == _OVERLAY_V2
    _assert_three_bare_passages_survive(third_handoff)
    original_roots = _root_shas(third_handoff)

    source = create_inspectable_third_basis_epoch_handoff_research_session_shell(
        third_handoff
    )
    source_launch = source.third_basis_epoch_authority_inspection.launch_provenance
    assert source.third_basis_epoch_launch_lineage is None
    assert source_launch.launch_location_context is None

    observed: dict[str, object] = {}
    monkeypatch.setattr(
        source,
        "exit",
        lambda result=None, *args, **kwargs: observed.__setitem__("result", result),
    )

    first_successor = tmp_path / "50x-first-successor.json"
    first_declaration = tmp_path / "50x-first-declaration.json"
    current_overlay = tmp_path / "50x-current-40c.overlay.json"

    async with source.run_test(size=(205, 360)) as pilot:
        await pilot.pause()
        await _write_and_rollover(
            source,
            pilot,
            prior_edge=third_handoff.controller.declared_endpoint.verification.path,
            successor=first_successor,
            declaration=first_declaration,
            text="50X first continuation after pathless bare 47G handoff.",
        )

        for selector in (
            "#research-third-basis-epoch-checkpoint-prior-overlay-source",
            "#research-third-basis-epoch-checkpoint-successor-source",
            "#research-third-basis-epoch-checkpoint-declaration-source",
            "#research-third-basis-epoch-checkpoint-destination",
        ):
            assert source.query_one(selector, Input).value == ""

        await _save_checkpoint(
            source,
            pilot,
            prior_overlay=third_overlay,
            successor=first_successor,
            declaration=first_declaration,
            destination=current_overlay,
        )

        checkpoint = source.last_third_basis_epoch_continuation_checkpoint
        assert checkpoint is not None
        assert checkpoint.prior_reentry is third_handoff
        assert checkpoint.plan.prior_third_basis_epoch_overlay_source == third_overlay.resolve()
        assert checkpoint.persistence.path == current_overlay.resolve()
        _assert_three_bare_passages_survive_continuation(checkpoint.fresh_reentry)
        assert _root_shas(checkpoint.fresh_reentry.prior_third_basis_epoch_reentry) == (
            original_roots
        )

        current_document = json.loads(current_overlay.read_text(encoding="utf-8"))
        assert current_document["format"] == _CONTINUATION_V1

        handoff_button = source.query_one(
            "#continue-third-basis-epoch-cumulative-mode",
            Button,
        )
        assert not handoff_button.disabled
        expected_41e = checkpoint.fresh_reentry

        await _press(
            source,
            pilot,
            "continue-third-basis-epoch-cumulative-mode",
        )
        assert observed["result"] is expected_41e
        assert source.third_basis_epoch_authority_inspection.launch_provenance is (
            source_launch
        )
        assert source_launch.launch_location_context is None

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

    current_overlay_bytes = current_overlay.read_bytes()
    second_successor = tmp_path / "50x-second-successor.json"
    second_one_hop = tmp_path / "50x-second-one-hop.json"
    cumulative_declaration = tmp_path / "50x-cumulative-declaration.json"
    next_overlay = tmp_path / "50x-next-40c.overlay.json"

    async with cumulative.run_test(size=(205, 360)) as pilot:
        await pilot.pause()
        current_typed_state = panel.current_state

        await _write_and_rollover(
            cumulative,
            pilot,
            prior_edge=handoff.controller.declared_endpoint.verification.path,
            successor=second_successor,
            declaration=second_one_hop,
            text="50X cumulative successor after exact pathless 41E handoff.",
        )

        rollover = cumulative.last_research_rollover
        one_hop_controller = cumulative.research_controller
        assert rollover is not None
        controls = cumulative.query_one(
            ThirdBasisEpochResearchSessionCumulativeCheckpointControls
        )
        assert controls.current_reentry is handoff
        assert controls.rollover is rollover

        for selector in (
            "#research-third-basis-epoch-cumulative-checkpoint-current-overlay-source",
            "#research-third-basis-epoch-cumulative-checkpoint-successor-source",
            "#research-third-basis-epoch-cumulative-checkpoint-declaration-destination",
            "#research-third-basis-epoch-cumulative-checkpoint-overlay-destination",
        ):
            assert cumulative.query_one(selector, Input).value == ""

        assert panel.launch_provenance is launch
        assert panel.current_state is current_typed_state
        assert panel.current_state.endpoint_sha256 == (
            handoff.controller.declared_endpoint.verification.edge_record_sha256
        )
        assert (
            one_hop_controller.declared_endpoint.verification.edge_record_sha256
            != panel.current_state.endpoint_sha256
        )

        await _save_cumulative(
            cumulative,
            pilot,
            current_overlay=current_overlay,
            successor=second_successor,
            declaration_destination=cumulative_declaration,
            next_overlay=next_overlay,
        )

        result = cumulative.last_third_basis_epoch_cumulative_checkpoint
        assert result is not None
        assert result.current_reentry is handoff
        assert result.rollover is rollover
        assert result.next_plan.prior_third_basis_epoch_overlay_source == (
            third_overlay.resolve()
        )
        assert result.next_plan.prior_third_basis_epoch_overlay_source != (
            current_overlay.resolve()
        )
        assert result.next_plan.declared_edge_sources == (
            *handoff.plan.declared_edge_sources,
            second_successor.resolve(),
        )
        assert len(result.next_plan.declared_edge_sources) == 2

        next_document = json.loads(next_overlay.read_text(encoding="utf-8"))
        assert next_document["format"] == _CONTINUATION_V1
        assert set(next_document) == {
            "format",
            "prior_third_basis_epoch_overlay_source",
            "declared_edge_sources",
            "declaration_source",
        }
        assert (
            next_overlay.parent
            / next_document["prior_third_basis_epoch_overlay_source"]
        ).resolve() == third_overlay.resolve()
        serialized = json.dumps(next_document, sort_keys=True)
        for forbidden in (
            "appended_working_set_members",
            "exact_range_selection",
            "capture_source",
            "selection_source",
            "changed_working_set_source",
            "changed_note_source",
            "transition_source",
            "root_source",
        ):
            assert forbidden not in serialized

        assert current_overlay.read_bytes() == current_overlay_bytes
        _assert_three_bare_passages_survive_continuation(result.fresh_reentry)
        assert _root_shas(result.fresh_reentry.prior_third_basis_epoch_reentry) == (
            original_roots
        )
        assert (
            result.fresh_reentry.controller.declared_endpoint.verification.edge_record_sha256
            == one_hop_controller.declared_endpoint.verification.edge_record_sha256
        )

        assert cumulative.third_basis_epoch_continuation_launch_lineage is None
        assert cumulative.third_basis_epoch_continuation_handoff_reentry is handoff
        assert cumulative.third_basis_epoch_continuation_reentry is result.fresh_reentry
        assert cumulative.research_controller is result.fresh_reentry.controller
        assert cumulative.research_controller is not one_hop_controller
        assert cumulative.last_research_rollover is None

        assert panel.launch_provenance is launch
        assert panel.launch_provenance.launch_location_context is None
        assert panel.current_state is not current_typed_state
        assert panel.current_state.state_kind == "typed third-basis-epoch continuation"
        assert panel.current_state.state_source == (
            "40D cumulative promotion after in-process 41E handoff"
        )
        assert panel.current_state.declared_continuation_edge_count == 2
        assert panel.current_state.endpoint_sha256 == (
            result.fresh_reentry.controller.declared_endpoint.verification.edge_record_sha256
        )

        assert len(
            cumulative.query(ThirdBasisEpochResearchSessionCumulativeCheckpointControls)
        ) == 0
        assert not cumulative.query_one(
            "#persist-research-endpoint-revision",
            Button,
        ).disabled
