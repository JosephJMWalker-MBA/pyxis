from __future__ import annotations

import json
from pathlib import Path

import pytest

from pyxis.app.chromium_research_third_basis_epoch_authority_inspection import (
    inspect_chromium_research_third_basis_epoch_continuation_launch,
    inspect_chromium_research_third_basis_epoch_launch,
)
from pyxis.app.chromium_research_third_basis_epoch_authority_inspection_report import (
    serialize_chromium_research_third_basis_epoch_authority_inspection,
)
from pyxis.app.chromium_research_third_basis_epoch_shell_lineage import (
    prove_chromium_research_third_basis_epoch_continuation_shell_lineage,
    prove_chromium_research_third_basis_epoch_shell_lineage,
)
from test_app_chromium_research_third_basis_epoch_continuation_checkpoint_extension import (
    _persist_extension,
)
from test_app_chromium_research_third_basis_epoch_continuation_reentry_plan_document import (
    _persist_valid_continuation,
)
from test_app_chromium_research_third_basis_epoch_reentry_plan_document import (
    _persist_valid_overlay,
)


def _root_shas_from_third_epoch(reentry) -> tuple[str, str, str]:
    second_epoch = (
        reentry.prior_second_basis_epoch_continuation_reentry
        .prior_second_basis_epoch_reentry
    )
    first_root = (
        second_epoch.prior_continuation_reentry.prior_root_backed_reentry.loaded_root
        .verification.root_record_sha256
    )
    return (
        first_root,
        second_epoch.loaded_root.verification.root_record_sha256,
        reentry.loaded_root.verification.root_record_sha256,
    )


def test_persisted_40b_projection_serializes_deterministically_with_three_roots(
    tmp_path: Path,
) -> None:
    _, earned, overlay, _ = _persist_valid_overlay(tmp_path, stem="42b-40b")
    lineage = prove_chromium_research_third_basis_epoch_shell_lineage(
        earned,
        overlay_source=overlay,
    )
    inspection = inspect_chromium_research_third_basis_epoch_launch(lineage)

    first = serialize_chromium_research_third_basis_epoch_authority_inspection(
        inspection
    )
    second = serialize_chromium_research_third_basis_epoch_authority_inspection(
        inspection
    )
    assert first == second
    assert first.endswith("\n")

    document = json.loads(first)
    roots = _root_shas_from_third_epoch(lineage.reentry)
    assert document["format"] == (
        "pyxis.chromium.research_third_basis_epoch_authority_inspection.v1"
    )
    assert document["report_role"] == "read_only_inspection_not_authority"
    assert document["launch_provenance"]["launch_location_context_only"] == str(
        overlay.resolve()
    )
    assert document["launch_provenance"]["first_root_sha256"] == roots[0]
    assert document["launch_provenance"]["second_root_sha256"] == roots[1]
    assert document["launch_provenance"]["third_root_sha256"] == roots[2]
    assert document["launch_provenance"]["launch_endpoint_sha256"] == (
        lineage.reentry.controller.declared_endpoint.verification.edge_record_sha256
    )
    assert document["current_governed_state"]["endpoint_sha256"] == (
        lineage.reentry.controller.declared_endpoint.verification.edge_record_sha256
    )
    assert document["current_governed_state"]["declared_continuation_edge_count"] is None
    assert "not current/latest/head" in document["authority_notice"]
    assert "do not establish authorship" in document["authority_notice"]


def test_persisted_40c_projection_serializes_typed_current_state(
    tmp_path: Path,
) -> None:
    values = _persist_valid_continuation(tmp_path, stem="42b-40c")
    overlay = values[6]
    current = values[8].fresh_reentry
    lineage = prove_chromium_research_third_basis_epoch_continuation_shell_lineage(
        current,
        overlay_source=overlay,
    )
    inspection = inspect_chromium_research_third_basis_epoch_continuation_launch(
        lineage
    )
    document = json.loads(
        serialize_chromium_research_third_basis_epoch_authority_inspection(
            inspection
        )
    )

    assert document["launch_provenance"]["launch_family"] == (
        "persisted 40C/40D continuation launch"
    )
    assert document["launch_provenance"]["launch_location_context_only"] == str(
        overlay.resolve()
    )
    assert document["current_governed_state"]["state_kind"] == (
        "typed third-basis-epoch continuation"
    )
    assert document["current_governed_state"]["declared_continuation_edge_count"] == len(
        current.plan.declared_edge_sources
    )
    assert document["current_governed_state"]["endpoint_sha256"] == (
        current.controller.declared_endpoint.verification.edge_record_sha256
    )


def test_persisted_40d_projection_uses_same_deterministic_continuation_report_family(
    tmp_path: Path,
) -> None:
    *_, result = _persist_extension(tmp_path, stem="42b-40d")
    lineage = prove_chromium_research_third_basis_epoch_continuation_shell_lineage(
        result.fresh_reentry,
        overlay_source=result.overlay.path,
    )
    inspection = inspect_chromium_research_third_basis_epoch_continuation_launch(
        lineage
    )
    document = json.loads(
        serialize_chromium_research_third_basis_epoch_authority_inspection(
            inspection
        )
    )

    assert document["launch_provenance"]["launch_location_context_only"] == str(
        result.overlay.path.resolve()
    )
    assert document["current_governed_state"]["declared_continuation_edge_count"] == len(
        result.fresh_reentry.plan.declared_edge_sources
    )
    assert document["current_governed_state"]["endpoint_sha256"] == (
        result.fresh_reentry.controller.declared_endpoint.verification.edge_record_sha256
    )


def test_serializer_rejects_non_projection() -> None:
    with pytest.raises(TypeError, match="inspection"):
        serialize_chromium_research_third_basis_epoch_authority_inspection(object())  # type: ignore[arg-type]
