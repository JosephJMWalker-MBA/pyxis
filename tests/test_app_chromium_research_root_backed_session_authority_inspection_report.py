from __future__ import annotations

import json
from pathlib import Path

import pytest

from pyxis.app.chromium_research_root_backed_session_authority_inspection import (
    inspect_chromium_research_root_backed_session_continuation_launch,
    inspect_chromium_research_root_backed_session_launch,
)
from pyxis.app.chromium_research_root_backed_session_authority_inspection_report import (
    serialize_chromium_research_root_backed_session_authority_inspection,
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


def test_45b_persisted_35c_serializes_deterministically_from_shared_projection(
    tmp_path: Path,
) -> None:
    _, _, earned, _, overlay, _ = _persist_valid_overlay(tmp_path, stem="45b-35c")
    lineage = prove_chromium_research_root_backed_session_shell_lineage(
        earned,
        overlay_source=overlay,
    )
    inspection = inspect_chromium_research_root_backed_session_launch(lineage)

    first = serialize_chromium_research_root_backed_session_authority_inspection(
        inspection
    )
    second = serialize_chromium_research_root_backed_session_authority_inspection(
        inspection
    )

    assert first == second
    assert first.endswith("\n")
    document = json.loads(first)
    assert document["format"] == (
        "pyxis.chromium.research_root_backed_session_authority_inspection.v1"
    )
    assert document["report_role"] == "read_only_inspection_not_authority"
    assert document["launch_provenance"]["launch_family"] == (
        "persisted 35C root-backed launch"
    )
    assert document["launch_provenance"]["launch_location_context_only"] == str(
        overlay.resolve()
    )
    assert document["launch_provenance"]["root_sha256"] == (
        lineage.reentry.loaded_root.verification.root_record_sha256
    )
    assert document["launch_provenance"]["launch_endpoint_sha256"] == (
        lineage.reentry.controller.declared_endpoint.verification.edge_record_sha256
    )
    assert document["current_governed_state"]["endpoint_sha256"] == (
        lineage.reentry.controller.declared_endpoint.verification.edge_record_sha256
    )
    assert document["current_governed_state"]["declared_continuation_edge_count"] is None
    assert "not current/latest/head" in document["authority_notice"]


def test_45b_persisted_35d_serializes_exact_typed_continuation_edge_count(
    tmp_path: Path,
) -> None:
    values = _persist_valid_continuation(tmp_path, stem="45b-35d")
    overlay = values[8]
    earned = values[9].fresh_reentry
    lineage = prove_chromium_research_root_backed_session_continuation_shell_lineage(
        earned,
        overlay_source=overlay,
    )
    inspection = inspect_chromium_research_root_backed_session_continuation_launch(
        lineage
    )

    document = json.loads(
        serialize_chromium_research_root_backed_session_authority_inspection(
            inspection
        )
    )

    assert document["launch_provenance"]["launch_family"] == (
        "persisted 35D/35E root-backed continuation launch"
    )
    assert document["launch_provenance"]["launch_location_context_only"] == str(
        overlay.resolve()
    )
    assert document["current_governed_state"]["declared_continuation_edge_count"] == len(
        lineage.reentry.plan.declared_edge_sources
    )
    assert document["current_governed_state"]["endpoint_sha256"] == (
        lineage.reentry.controller.declared_endpoint.verification.edge_record_sha256
    )


def test_45b_path_distinct_equivalent_35c_reports_differ_only_in_launch_location_context(
    tmp_path: Path,
) -> None:
    first_dir = tmp_path / "first"
    second_dir = tmp_path / "second"
    first_dir.mkdir()
    second_dir.mkdir()
    _, _, first_earned, _, first_overlay, _ = _persist_valid_overlay(
        first_dir,
        stem="same",
    )
    _, _, second_earned, _, second_overlay, _ = _persist_valid_overlay(
        second_dir,
        stem="same",
    )
    first_lineage = prove_chromium_research_root_backed_session_shell_lineage(
        first_earned,
        overlay_source=first_overlay,
    )
    second_lineage = prove_chromium_research_root_backed_session_shell_lineage(
        second_earned,
        overlay_source=second_overlay,
    )

    first = json.loads(
        serialize_chromium_research_root_backed_session_authority_inspection(
            inspect_chromium_research_root_backed_session_launch(first_lineage)
        )
    )
    second = json.loads(
        serialize_chromium_research_root_backed_session_authority_inspection(
            inspect_chromium_research_root_backed_session_launch(second_lineage)
        )
    )

    first_location = first["launch_provenance"].pop("launch_location_context_only")
    second_location = second["launch_provenance"].pop("launch_location_context_only")
    assert first_location == str(first_overlay.resolve())
    assert second_location == str(second_overlay.resolve())
    assert first_location != second_location
    assert first == second


def test_45b_serializer_rejects_non_projection() -> None:
    with pytest.raises(TypeError, match="RootBackedAuthorityInspection"):
        serialize_chromium_research_root_backed_session_authority_inspection(object())  # type: ignore[arg-type]
