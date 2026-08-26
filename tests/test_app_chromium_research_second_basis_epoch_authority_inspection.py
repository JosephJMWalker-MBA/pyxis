from __future__ import annotations

import json
from pathlib import Path

import pytest

from pyxis.app.chromium_research_second_basis_epoch_authority_inspection import (
    SecondBasisEpochAuthorityInspection,
    advance_chromium_research_second_basis_epoch_authority_from_continuation,
    advance_chromium_research_second_basis_epoch_authority_from_controller,
    inspect_chromium_research_second_basis_epoch_continuation_launch,
    inspect_chromium_research_second_basis_epoch_in_process_handoff,
    inspect_chromium_research_second_basis_epoch_launch,
    serialize_chromium_research_second_basis_epoch_authority_inspection,
)
from pyxis.app.chromium_research_second_basis_epoch_shell_lineage import (
    prove_chromium_research_second_basis_epoch_continuation_shell_lineage,
    prove_chromium_research_second_basis_epoch_shell_lineage,
)
from test_app_chromium_research_second_basis_epoch_continuation_reentry_plan_document import (
    _persist_valid_continuation,
)
from test_app_chromium_research_second_basis_epoch_reentry_plan_document import (
    _persist_valid_overlay,
)


def _persisted_second_epoch(tmp_path: Path, *, stem: str):
    tmp_path.mkdir(parents=True, exist_ok=True)
    _, earned, overlay, _ = _persist_valid_overlay(tmp_path, stem=stem)
    lineage = prove_chromium_research_second_basis_epoch_shell_lineage(
        earned,
        overlay_source=overlay,
    )
    return lineage, overlay


def _persisted_continuation(tmp_path: Path, *, stem: str):
    tmp_path.mkdir(parents=True, exist_ok=True)
    values = _persist_valid_continuation(tmp_path, stem=stem)
    overlay = values[6]
    earned = values[8].fresh_reentry
    lineage = prove_chromium_research_second_basis_epoch_continuation_shell_lineage(
        earned,
        overlay_source=overlay,
    )
    return values, lineage, overlay


def test_persisted_37b_projection_is_ui_independent_and_deterministically_serialized(
    tmp_path: Path,
) -> None:
    lineage, overlay = _persisted_second_epoch(tmp_path / "second", stem="39b-second")

    inspection = inspect_chromium_research_second_basis_epoch_launch(lineage)
    assert isinstance(inspection, SecondBasisEpochAuthorityInspection)
    assert inspection.launch_provenance.launch_location_context == overlay.resolve()
    assert inspection.launch_provenance.launch_family == (
        "persisted 37B second-basis-epoch launch"
    )
    assert inspection.current_state.state_source == "persisted 37B launch"
    assert inspection.current_state.declared_continuation_edge_count is None

    first = serialize_chromium_research_second_basis_epoch_authority_inspection(
        inspection
    )
    second = serialize_chromium_research_second_basis_epoch_authority_inspection(
        inspection
    )
    assert first == second
    assert first.endswith("\n")

    document = json.loads(first)
    assert document["format"] == (
        "pyxis.chromium.research_second_basis_epoch_authority_inspection.v1"
    )
    assert document["report_role"] == "read_only_inspection_not_authority"
    assert document["launch_provenance"]["launch_location_context_only"] == str(
        overlay.resolve()
    )
    assert "not current/latest/head" in document["authority_notice"]
    assert "do not establish authorship" in document["authority_notice"]


def test_persisted_continuation_and_in_process_handoff_share_projection_without_path_fabrication(
    tmp_path: Path,
) -> None:
    values, lineage, overlay = _persisted_continuation(
        tmp_path / "continuation",
        stem="39b-continuation",
    )
    handoff = values[8].fresh_reentry

    persisted = inspect_chromium_research_second_basis_epoch_continuation_launch(
        lineage
    )
    in_process = inspect_chromium_research_second_basis_epoch_in_process_handoff(
        handoff
    )

    assert persisted.launch_provenance.launch_location_context == overlay.resolve()
    assert persisted.current_state.declared_continuation_edge_count == len(
        lineage.reentry.plan.declared_edge_sources
    )
    assert in_process.launch_provenance.launch_location_context is None
    assert in_process.launch_provenance.launch_family == (
        "in-process 38F typed continuation handoff"
    )
    assert in_process.current_state.declared_continuation_edge_count == len(
        handoff.plan.declared_edge_sources
    )

    document = json.loads(
        serialize_chromium_research_second_basis_epoch_authority_inspection(in_process)
    )
    assert document["launch_provenance"]["launch_location_context_only"] is None
    assert str(overlay.resolve()) not in json.dumps(document, sort_keys=True)


def test_projection_advances_current_state_without_replacing_launch_provenance(
    tmp_path: Path,
) -> None:
    values, lineage, _ = _persisted_continuation(
        tmp_path / "advance",
        stem="39b-advance",
    )
    current = lineage.reentry
    inspection = inspect_chromium_research_second_basis_epoch_continuation_launch(
        lineage
    )
    launch = inspection.launch_provenance

    controller_advanced = (
        advance_chromium_research_second_basis_epoch_authority_from_controller(
            inspection,
            current.controller,
            state_kind="visible one-hop continuation",
            state_source="explicit rollover",
        )
    )
    assert controller_advanced.launch_provenance is launch
    assert controller_advanced.current_state.state_kind == "visible one-hop continuation"
    assert controller_advanced.current_state.declared_continuation_edge_count is None

    continuation_advanced = (
        advance_chromium_research_second_basis_epoch_authority_from_continuation(
            inspection,
            values[8].fresh_reentry,
            state_source="fresh typed continuation",
        )
    )
    assert continuation_advanced.launch_provenance is launch
    assert continuation_advanced.current_state.state_source == "fresh typed continuation"
    assert continuation_advanced.current_state.declared_continuation_edge_count == len(
        values[8].fresh_reentry.plan.declared_edge_sources
    )


def test_projection_rejects_current_continuation_from_different_root_ancestry(
    tmp_path: Path,
) -> None:
    _, lineage, _ = _persisted_continuation(
        tmp_path / "one",
        stem="39b-one",
    )
    other_values, _, _ = _persisted_continuation(
        tmp_path / "two",
        stem="39b-two",
    )
    inspection = inspect_chromium_research_second_basis_epoch_continuation_launch(
        lineage
    )

    with pytest.raises(ValueError, match="root identity"):
        advance_chromium_research_second_basis_epoch_authority_from_continuation(
            inspection,
            other_values[8].fresh_reentry,
            state_source="wrong ancestry",
        )


def test_serializer_rejects_non_projection() -> None:
    with pytest.raises(TypeError, match="inspection"):
        serialize_chromium_research_second_basis_epoch_authority_inspection(object())  # type: ignore[arg-type]
