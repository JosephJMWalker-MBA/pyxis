from dataclasses import fields
from pathlib import Path

import pytest

from pyxis.app.chromium_research_second_basis_epoch_shell_lineage import (
    ChromiumResearchSecondBasisEpochContinuationShellLineage,
    ChromiumResearchSecondBasisEpochShellLineage,
    ChromiumResearchSecondBasisEpochShellLineageError,
    prove_chromium_research_second_basis_epoch_continuation_shell_lineage,
    prove_chromium_research_second_basis_epoch_shell_lineage,
)
from test_app_chromium_research_second_basis_epoch_continuation_checkpoint_extension import (
    _persist_extension as _persist_cumulative_continuation,
)
from test_app_chromium_research_second_basis_epoch_continuation_reentry_plan_document import (
    _persist_valid_continuation,
)
from test_app_chromium_research_second_basis_epoch_reentry_plan_document import (
    _persist_valid_overlay,
)


def test_38b_proves_37b_path_and_retains_fresh_result_from_that_path(
    tmp_path: Path,
) -> None:
    _, earned, overlay, checkpoint = _persist_valid_overlay(tmp_path, stem="38b-second")

    lineage = prove_chromium_research_second_basis_epoch_shell_lineage(
        earned,
        overlay_source=overlay,
    )

    assert isinstance(lineage, ChromiumResearchSecondBasisEpochShellLineage)
    assert lineage.overlay_source == overlay.resolve()
    assert lineage.reentry is not earned
    assert lineage.reentry is not checkpoint.fresh_reentry
    assert lineage.reentry.controller.presentation == earned.controller.presentation
    assert (
        lineage.reentry.controller.declared_endpoint.verification.edge_record_sha256
        == earned.controller.declared_endpoint.verification.edge_record_sha256
    )
    assert lineage.reentry.loaded_root.verification.root_record_sha256 == (
        earned.loaded_root.verification.root_record_sha256
    )


def test_38b_proves_37c_continuation_path_and_retains_fresh_result(
    tmp_path: Path,
) -> None:
    values = _persist_valid_continuation(tmp_path, stem="38b-cont")
    overlay = values[6]
    earned = values[8].fresh_reentry

    lineage = prove_chromium_research_second_basis_epoch_continuation_shell_lineage(
        earned,
        overlay_source=overlay,
    )

    assert isinstance(
        lineage,
        ChromiumResearchSecondBasisEpochContinuationShellLineage,
    )
    assert lineage.overlay_source == overlay.resolve()
    assert lineage.reentry is not earned
    assert lineage.reentry.controller.presentation == earned.controller.presentation
    assert (
        lineage.reentry.controller.declared_endpoint.verification.edge_record_sha256
        == earned.controller.declared_endpoint.verification.edge_record_sha256
    )
    assert lineage.reentry.prior_second_basis_epoch_reentry.loaded_root.verification.root_record_sha256 == (
        earned.prior_second_basis_epoch_reentry.loaded_root.verification.root_record_sha256
    )


def test_38b_proves_cumulative_37d_through_same_continuation_lineage_type(
    tmp_path: Path,
) -> None:
    values = _persist_cumulative_continuation(tmp_path, stem="38b-cumulative")
    overlay = values[6]
    earned = values[8].fresh_reentry

    lineage = prove_chromium_research_second_basis_epoch_continuation_shell_lineage(
        earned,
        overlay_source=overlay,
    )

    assert lineage.reentry.plan == earned.plan
    assert len(lineage.reentry.plan.declared_edge_sources) >= 2
    assert lineage.reentry.controller.presentation == earned.controller.presentation


def test_38b_path_distinct_durably_equivalent_37b_overlay_is_valid_authority(
    tmp_path: Path,
) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    first.mkdir()
    second.mkdir()
    _, earned, first_overlay, _ = _persist_valid_overlay(first, stem="same")
    _, other_earned, other_overlay, _ = _persist_valid_overlay(second, stem="same")

    assert first_overlay.resolve() != other_overlay.resolve()
    assert earned.controller.presentation == other_earned.controller.presentation
    assert earned.controller.declared_endpoint.verification.path != (
        other_earned.controller.declared_endpoint.verification.path
    )
    assert (
        earned.controller.declared_endpoint.verification.edge_record_sha256
        == other_earned.controller.declared_endpoint.verification.edge_record_sha256
    )

    lineage = prove_chromium_research_second_basis_epoch_shell_lineage(
        earned,
        overlay_source=other_overlay,
    )

    assert lineage.overlay_source == other_overlay.resolve()
    assert lineage.reentry.controller.presentation == earned.controller.presentation
    assert lineage.reentry.controller.declared_endpoint.verification.path != (
        earned.controller.declared_endpoint.verification.path
    )


def test_38b_path_distinct_durably_equivalent_37c_overlay_is_valid_authority(
    tmp_path: Path,
) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    first.mkdir()
    second.mkdir()
    first_values = _persist_valid_continuation(first, stem="same")
    second_values = _persist_valid_continuation(second, stem="same")
    earned = first_values[8].fresh_reentry
    other = second_values[8].fresh_reentry
    other_overlay = second_values[6]

    assert earned.controller.presentation == other.controller.presentation
    assert earned.controller.declared_endpoint.verification.path != (
        other.controller.declared_endpoint.verification.path
    )
    assert (
        earned.controller.declared_endpoint.verification.edge_record_sha256
        == other.controller.declared_endpoint.verification.edge_record_sha256
    )

    lineage = prove_chromium_research_second_basis_epoch_continuation_shell_lineage(
        earned,
        overlay_source=other_overlay,
    )

    assert lineage.overlay_source == other_overlay.resolve()
    assert lineage.reentry.controller.presentation == earned.controller.presentation


def test_38b_different_37b_overlay_rejects(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    first.mkdir()
    second.mkdir()
    _, earned, _, _ = _persist_valid_overlay(first, stem="first")
    _, _, different_overlay, _ = _persist_valid_overlay(second, stem="different")

    with pytest.raises(
        ChromiumResearchSecondBasisEpochShellLineageError,
        match="does not match",
    ):
        prove_chromium_research_second_basis_epoch_shell_lineage(
            earned,
            overlay_source=different_overlay,
        )


def test_38b_different_37c_overlay_rejects(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    first.mkdir()
    second.mkdir()
    first_values = _persist_valid_continuation(first, stem="first")
    second_values = _persist_valid_continuation(second, stem="different")
    earned = first_values[8].fresh_reentry
    different_overlay = second_values[6]

    with pytest.raises(
        ChromiumResearchSecondBasisEpochShellLineageError,
        match="does not match",
    ):
        prove_chromium_research_second_basis_epoch_continuation_shell_lineage(
            earned,
            overlay_source=different_overlay,
        )


def test_38b_tampered_second_root_rejects_before_lineage_is_returned(
    tmp_path: Path,
) -> None:
    _, earned, overlay, _ = _persist_valid_overlay(tmp_path, stem="tampered-second")
    earned.plan.root_source.write_bytes(earned.plan.root_source.read_bytes() + b"tampered")

    with pytest.raises(
        ChromiumResearchSecondBasisEpochShellLineageError,
        match="could not freshly reconstruct",
    ):
        prove_chromium_research_second_basis_epoch_shell_lineage(
            earned,
            overlay_source=overlay,
        )


def test_38b_tampered_retained_first_root_rejects_continuation_lineage(
    tmp_path: Path,
) -> None:
    values = _persist_valid_continuation(tmp_path, stem="tampered-first")
    overlay = values[6]
    earned = values[8].fresh_reentry
    first_root = (
        earned.prior_second_basis_epoch_reentry.prior_continuation_reentry.prior_root_backed_reentry.plan.root_source
    )
    first_root.write_bytes(first_root.read_bytes() + b"tampered")

    with pytest.raises(
        ChromiumResearchSecondBasisEpochShellLineageError,
        match="could not freshly reconstruct",
    ):
        prove_chromium_research_second_basis_epoch_continuation_shell_lineage(
            earned,
            overlay_source=overlay,
        )


def test_38b_wrapper_shapes_carry_only_explicit_source_and_fresh_reentry(
    tmp_path: Path,
) -> None:
    _, earned, overlay, _ = _persist_valid_overlay(tmp_path, stem="shape")
    lineage = prove_chromium_research_second_basis_epoch_shell_lineage(
        earned,
        overlay_source=overlay,
    )

    assert tuple(field.name for field in fields(lineage)) == (
        "overlay_source",
        "reentry",
    )
    for forbidden in (
        "latest",
        "current_head",
        "canonical_head",
        "discovered_source",
        "checkpoint",
        "rollover",
        "semantic_support",
        "chronology",
    ):
        assert not hasattr(lineage, forbidden)


def test_38b_wrong_result_families_reject_before_path_work(tmp_path: Path) -> None:
    source = tmp_path / "does-not-need-to-exist.overlay.json"

    with pytest.raises(TypeError, match="ChromiumResearchSecondBasisEpochReentryResult"):
        prove_chromium_research_second_basis_epoch_shell_lineage(
            object(),  # type: ignore[arg-type]
            overlay_source=source,
        )

    with pytest.raises(
        TypeError,
        match="ChromiumResearchSecondBasisEpochContinuationReentryResult",
    ):
        prove_chromium_research_second_basis_epoch_continuation_shell_lineage(
            object(),  # type: ignore[arg-type]
            overlay_source=source,
        )
