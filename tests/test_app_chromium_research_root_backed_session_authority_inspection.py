from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from pyxis.app.chromium_research_root_backed_session_authority_inspection import (
    RootBackedAuthorityInspection,
    advance_chromium_research_root_backed_authority_from_continuation,
    advance_chromium_research_root_backed_authority_from_controller,
    inspect_chromium_research_root_backed_session_continuation_in_process_handoff,
    inspect_chromium_research_root_backed_session_continuation_launch,
    inspect_chromium_research_root_backed_session_in_process_handoff,
    inspect_chromium_research_root_backed_session_launch,
    root_backed_authority_notice,
)
from pyxis.app.chromium_research_root_backed_session_shell_lineage import (
    prove_chromium_research_root_backed_session_continuation_shell_lineage,
    prove_chromium_research_root_backed_session_shell_lineage,
)
from test_app_chromium_research_root_backed_session_continuation_reentry_plan_document import (
    _persist_valid_continuation,
)
from test_app_chromium_research_root_backed_session_reentry_plan_document import (
    _persist_valid_overlay,
)


def test_45a_persisted_35c_projection_retains_only_proven_launch_path(
    tmp_path: Path,
) -> None:
    _, _, earned, _, overlay, _ = _persist_valid_overlay(tmp_path, stem="45a-35c")
    lineage = prove_chromium_research_root_backed_session_shell_lineage(
        earned,
        overlay_source=overlay,
    )

    inspection = inspect_chromium_research_root_backed_session_launch(lineage)

    assert isinstance(inspection, RootBackedAuthorityInspection)
    assert inspection.launch_provenance.launch_family == "persisted 35C root-backed launch"
    assert inspection.launch_provenance.launch_location_context == overlay.resolve()
    assert inspection.launch_provenance.root_sha256 == (
        lineage.reentry.loaded_root.verification.root_record_sha256
    )
    assert inspection.current_state.state_source == "persisted 35C launch"
    assert inspection.current_state.declared_continuation_edge_count is None


def test_45a_raw_44h_projection_fabricates_no_persistent_path(
    tmp_path: Path,
) -> None:
    _, _, earned, _, overlay, _ = _persist_valid_overlay(tmp_path, stem="45a-44h")

    inspection = inspect_chromium_research_root_backed_session_in_process_handoff(earned)

    assert inspection.launch_provenance.launch_family == (
        "in-process 44H typed root-backed handoff"
    )
    assert inspection.launch_provenance.launch_location_context is None
    assert str(overlay.resolve()) not in inspection.launch_provenance.launch_family


def test_45a_persisted_and_raw_continuation_launches_keep_path_semantics_distinct(
    tmp_path: Path,
) -> None:
    values = _persist_valid_continuation(tmp_path, stem="45a-cont")
    overlay = values[8]
    handoff = values[9].fresh_reentry
    lineage = prove_chromium_research_root_backed_session_continuation_shell_lineage(
        handoff,
        overlay_source=overlay,
    )

    persisted = inspect_chromium_research_root_backed_session_continuation_launch(lineage)
    raw = inspect_chromium_research_root_backed_session_continuation_in_process_handoff(
        handoff
    )

    assert persisted.launch_provenance.launch_location_context == overlay.resolve()
    assert persisted.launch_provenance.launch_family == (
        "persisted 35D/35E root-backed continuation launch"
    )
    assert raw.launch_provenance.launch_location_context is None
    assert raw.launch_provenance.launch_family == (
        "in-process 36D typed root-backed continuation handoff"
    )
    assert persisted.launch_provenance.root_sha256 == raw.launch_provenance.root_sha256
    assert persisted.current_state.declared_continuation_edge_count == len(
        lineage.reentry.plan.declared_edge_sources
    )
    assert raw.current_state.declared_continuation_edge_count == len(
        handoff.plan.declared_edge_sources
    )


def test_45a_current_state_advances_without_replacing_launch_provenance(
    tmp_path: Path,
) -> None:
    values = _persist_valid_continuation(tmp_path, stem="45a-advance")
    overlay = values[8]
    current = values[9].fresh_reentry
    lineage = prove_chromium_research_root_backed_session_continuation_shell_lineage(
        current,
        overlay_source=overlay,
    )
    inspection = inspect_chromium_research_root_backed_session_continuation_launch(lineage)
    launch = inspection.launch_provenance

    controller_advanced = advance_chromium_research_root_backed_authority_from_controller(
        inspection,
        current.controller,
        state_kind="visible one-hop continuation",
        state_source="explicit rollover",
    )
    assert controller_advanced.launch_provenance is launch
    assert controller_advanced.current_state.state_kind == "visible one-hop continuation"
    assert controller_advanced.current_state.declared_continuation_edge_count is None

    continuation_advanced = advance_chromium_research_root_backed_authority_from_continuation(
        inspection,
        current,
        state_source="fresh typed continuation",
    )
    assert continuation_advanced.launch_provenance is launch
    assert continuation_advanced.current_state.state_source == "fresh typed continuation"
    assert continuation_advanced.current_state.declared_continuation_edge_count == len(
        current.plan.declared_edge_sources
    )


def test_45a_projection_rejects_current_continuation_when_launch_root_identity_differs(
    tmp_path: Path,
) -> None:
    values = _persist_valid_continuation(tmp_path, stem="45a-wrong-root")
    overlay = values[8]
    current = values[9].fresh_reentry
    lineage = prove_chromium_research_root_backed_session_continuation_shell_lineage(
        current,
        overlay_source=overlay,
    )
    inspection = inspect_chromium_research_root_backed_session_continuation_launch(lineage)
    mismatched = replace(
        inspection,
        launch_provenance=replace(
            inspection.launch_provenance,
            root_sha256="0" * 64,
        ),
    )

    assert current.prior_root_backed_reentry.loaded_root.verification.root_record_sha256 != (
        mismatched.launch_provenance.root_sha256
    )
    with pytest.raises(ValueError, match="root identity"):
        advance_chromium_research_root_backed_authority_from_continuation(
            mismatched,
            current,
            state_source="wrong root",
        )


def test_45a_authority_notice_keeps_inspection_negative_and_read_only() -> None:
    notice = root_backed_authority_notice()

    assert "read-only" in notice
    assert "not evidence" in notice
    assert "not current/latest/head" in notice
    assert "do not establish authorship" in notice
    assert "grants no mutation" in notice
