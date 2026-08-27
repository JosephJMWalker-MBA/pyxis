from dataclasses import fields
from pathlib import Path

import pytest

from pyxis.app.chromium_research_third_basis_epoch_shell_lineage import (
    ChromiumResearchThirdBasisEpochContinuationShellLineage,
    ChromiumResearchThirdBasisEpochShellLineage,
    ChromiumResearchThirdBasisEpochShellLineageError,
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
    _root_shas,
)


def test_41a_proves_40b_path_and_retains_fresh_three_root_result(
    tmp_path: Path,
) -> None:
    _, earned, overlay, checkpoint = _persist_valid_overlay(tmp_path, stem="41a-third")

    lineage = prove_chromium_research_third_basis_epoch_shell_lineage(
        earned,
        overlay_source=overlay,
    )

    assert isinstance(lineage, ChromiumResearchThirdBasisEpochShellLineage)
    assert lineage.overlay_source == overlay.resolve()
    assert lineage.reentry is not earned
    assert lineage.reentry is not checkpoint.fresh_reentry
    assert lineage.reentry.controller.presentation == earned.controller.presentation
    assert (
        lineage.reentry.controller.declared_endpoint.verification.edge_record_sha256
        == earned.controller.declared_endpoint.verification.edge_record_sha256
    )
    assert _root_shas(lineage.reentry) == _root_shas(earned)
    assert len(set(_root_shas(lineage.reentry))) == 3


def test_41a_proves_40c_path_and_retains_fresh_continuation_result(
    tmp_path: Path,
) -> None:
    values = _persist_valid_continuation(tmp_path, stem="41a-continuation")
    overlay = values[6]
    checkpoint = values[8]
    earned = checkpoint.fresh_reentry

    lineage = prove_chromium_research_third_basis_epoch_continuation_shell_lineage(
        earned,
        overlay_source=overlay,
    )

    assert isinstance(lineage, ChromiumResearchThirdBasisEpochContinuationShellLineage)
    assert lineage.overlay_source == overlay.resolve()
    assert lineage.reentry is not earned
    assert lineage.reentry is not checkpoint.fresh_reentry
    assert lineage.reentry.controller.presentation == earned.controller.presentation
    assert (
        lineage.reentry.controller.declared_endpoint.verification.edge_record_sha256
        == earned.controller.declared_endpoint.verification.edge_record_sha256
    )
    assert _root_shas(lineage.reentry.prior_third_basis_epoch_reentry) == _root_shas(
        earned.prior_third_basis_epoch_reentry
    )


def test_41a_same_continuation_lineage_type_accepts_cumulative_40d_overlay(
    tmp_path: Path,
) -> None:
    *_, result = _persist_extension(tmp_path, stem="41a-cumulative")
    earned = result.fresh_reentry

    lineage = prove_chromium_research_third_basis_epoch_continuation_shell_lineage(
        earned,
        overlay_source=result.overlay.path,
    )

    assert isinstance(lineage, ChromiumResearchThirdBasisEpochContinuationShellLineage)
    assert lineage.overlay_source == result.overlay.path.resolve()
    assert lineage.reentry.plan == result.next_plan
    assert lineage.reentry.controller.presentation == earned.controller.presentation
    assert (
        lineage.reentry.controller.declared_endpoint.verification.edge_record_sha256
        == earned.controller.declared_endpoint.verification.edge_record_sha256
    )
    assert _root_shas(lineage.reentry.prior_third_basis_epoch_reentry) == _root_shas(
        earned.prior_third_basis_epoch_reentry
    )


def test_41a_path_distinct_equivalent_40b_overlay_is_valid_location_context(
    tmp_path: Path,
) -> None:
    _, earned, overlay, _ = _persist_valid_overlay(tmp_path, stem="41a-path-third")
    alternate = tmp_path / "alternate-third-epoch.overlay.json"
    alternate.write_bytes(overlay.read_bytes())

    lineage = prove_chromium_research_third_basis_epoch_shell_lineage(
        earned,
        overlay_source=alternate,
    )

    assert lineage.overlay_source == alternate.resolve()
    assert lineage.reentry.controller.presentation == earned.controller.presentation
    assert _root_shas(lineage.reentry) == _root_shas(earned)


def test_41a_path_distinct_equivalent_40c_overlay_is_valid_location_context(
    tmp_path: Path,
) -> None:
    values = _persist_valid_continuation(tmp_path, stem="41a-path-continuation")
    overlay = values[6]
    earned = values[8].fresh_reentry
    alternate = tmp_path / "alternate-third-continuation.overlay.json"
    alternate.write_bytes(overlay.read_bytes())

    lineage = prove_chromium_research_third_basis_epoch_continuation_shell_lineage(
        earned,
        overlay_source=alternate,
    )

    assert lineage.overlay_source == alternate.resolve()
    assert lineage.reentry.controller.presentation == earned.controller.presentation
    assert (
        lineage.reentry.controller.declared_endpoint.verification.edge_record_sha256
        == earned.controller.declared_endpoint.verification.edge_record_sha256
    )


@pytest.mark.parametrize("root_name", ["first", "second", "third"])
def test_41a_40b_lineage_rejects_tampered_retained_root(
    tmp_path: Path,
    root_name: str,
) -> None:
    _, earned, overlay, _ = _persist_valid_overlay(tmp_path, stem=f"41a-tamper-{root_name}")
    prior = earned.prior_second_basis_epoch_continuation_reentry
    second = prior.prior_second_basis_epoch_reentry
    paths = {
        "first": second.prior_continuation_reentry.prior_root_backed_reentry.plan.root_source,
        "second": second.plan.root_source,
        "third": earned.plan.root_source,
    }
    path = paths[root_name]
    path.write_bytes(path.read_bytes() + b"tampered")

    with pytest.raises(
        ChromiumResearchThirdBasisEpochShellLineageError,
        match="could not freshly reconstruct",
    ):
        prove_chromium_research_third_basis_epoch_shell_lineage(
            earned,
            overlay_source=overlay,
        )


def test_41a_wrong_explicit_40b_overlay_is_not_discovered_or_replaced(
    tmp_path: Path,
) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    first.mkdir()
    second.mkdir()
    _, earned, _, _ = _persist_valid_overlay(first, stem="earned")
    _, _, wrong_overlay, _ = _persist_valid_overlay(second, stem="different")

    with pytest.raises(
        ChromiumResearchThirdBasisEpochShellLineageError,
        match="does not match",
    ):
        prove_chromium_research_third_basis_epoch_shell_lineage(
            earned,
            overlay_source=wrong_overlay,
        )


def test_41a_wrong_explicit_40c_overlay_is_not_discovered_or_replaced(
    tmp_path: Path,
) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    first.mkdir()
    second.mkdir()
    earned_values = _persist_valid_continuation(first, stem="earned")
    wrong_values = _persist_valid_continuation(second, stem="different")
    earned = earned_values[8].fresh_reentry
    wrong_overlay = wrong_values[6]

    with pytest.raises(
        ChromiumResearchThirdBasisEpochShellLineageError,
        match="does not match",
    ):
        prove_chromium_research_third_basis_epoch_continuation_shell_lineage(
            earned,
            overlay_source=wrong_overlay,
        )


def test_41a_wrappers_carry_only_explicit_source_plus_fresh_reentry() -> None:
    assert tuple(field.name for field in fields(ChromiumResearchThirdBasisEpochShellLineage)) == (
        "overlay_source",
        "reentry",
    )
    assert tuple(
        field.name
        for field in fields(ChromiumResearchThirdBasisEpochContinuationShellLineage)
    ) == (
        "overlay_source",
        "reentry",
    )


def test_41a_rejects_wrong_result_families_before_path_work(tmp_path: Path) -> None:
    missing = tmp_path / "missing.overlay.json"

    with pytest.raises(TypeError, match="ChromiumResearchThirdBasisEpochReentryResult"):
        prove_chromium_research_third_basis_epoch_shell_lineage(
            object(),  # type: ignore[arg-type]
            overlay_source=missing,
        )

    with pytest.raises(
        TypeError,
        match="ChromiumResearchThirdBasisEpochContinuationReentryResult",
    ):
        prove_chromium_research_third_basis_epoch_continuation_shell_lineage(
            object(),  # type: ignore[arg-type]
            overlay_source=missing,
        )
