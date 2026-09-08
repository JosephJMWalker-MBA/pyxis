from __future__ import annotations

import json
from pathlib import Path

import pytest

import pyxis.cli as cli
from pyxis.app.chromium_research_paragraph_text_selection_load import (
    ChromiumPageResearchLoadedParagraphTextSelectionRecord,
)
from pyxis.app.chromium_research_third_basis_epoch_authority_inspection import (
    inspect_chromium_research_third_basis_epoch_launch,
)
from pyxis.app.chromium_research_third_basis_epoch_authority_inspection_report import (
    serialize_chromium_research_third_basis_epoch_authority_inspection,
)
from pyxis.app.chromium_research_third_basis_epoch_reentry import (
    reenter_chromium_research_third_basis_epoch,
)
from pyxis.app.chromium_research_third_basis_epoch_reentry_plan_document import (
    load_chromium_research_third_basis_epoch_reentry_plan_document,
)
from pyxis.app.chromium_research_third_basis_epoch_shell_lineage import (
    ChromiumResearchThirdBasisEpochShellLineage,
    ChromiumResearchThirdBasisEpochShellLineageError,
    prove_chromium_research_third_basis_epoch_shell_lineage,
)
from pyxis.ui.third_basis_epoch_authority_inspection_shell import (
    create_inspectable_third_basis_epoch_cumulative_handoff_research_session_shell,
)
from test_app_chromium_research_third_basis_epoch_reentry_plan_document_v2 import (
    _persist_bare_third_basis_overlay,
)
from test_second_basis_bare_continuation_v1 import (
    _assert_bare_passages_survive_continuation,
)


_OVERLAY_V2 = "pyxis.chromium.research_third_basis_epoch_reentry_locator_overlay.v2"


def _assert_three_bare_passages_survive(reentry) -> None:
    _assert_bare_passages_survive_continuation(
        reentry.prior_second_basis_epoch_continuation_reentry
    )

    third_bare = reentry.loaded_appended_members[0]
    assert isinstance(
        third_bare,
        ChromiumPageResearchLoadedParagraphTextSelectionRecord,
    )
    assert third_bare.selection.selected_text == "Bare"
    assert not hasattr(third_bare, "note")
    assert (
        reentry.loaded_root.transition.successor_note.note.working_set.items[-1]
        is third_bare
    )
    assert (
        reentry.controller.declared_endpoint.revision.revised_note.working_set.items[-1]
        is third_bare
    )

    second_bare = (
        reentry.prior_second_basis_epoch_continuation_reentry
        .prior_second_basis_epoch_reentry.loaded_appended_members[0]
    )
    first_bare = (
        reentry.prior_second_basis_epoch_continuation_reentry
        .prior_second_basis_epoch_reentry.prior_continuation_reentry
        .prior_root_backed_reentry.loaded_appended_members[0]
    )
    assert first_bare is not second_bare
    assert second_bare is not third_bare
    assert first_bare is not third_bare


def test_50s_public_40b_v2_loader_reconstructs_three_bare_passages_and_41a_lineage(
    tmp_path: Path,
) -> None:
    values = _persist_bare_third_basis_overlay(tmp_path, stem="50s-lineage")
    root = values[6]
    edge = values[7]
    adoption = values[8]
    verification = values[9]
    overlay = values[10]
    checkpoint_wrapper = values[11]

    document = json.loads(overlay.read_text(encoding="utf-8"))
    assert document["format"] == _OVERLAY_V2

    plan = load_chromium_research_third_basis_epoch_reentry_plan_document(overlay)
    fresh = reenter_chromium_research_third_basis_epoch(plan)
    lineage = prove_chromium_research_third_basis_epoch_shell_lineage(
        fresh,
        overlay_source=overlay,
    )

    assert isinstance(lineage, ChromiumResearchThirdBasisEpochShellLineage)
    assert lineage.overlay_source == overlay.resolve()
    assert lineage.reentry is not fresh
    assert lineage.reentry is not verification.fresh_reentry
    assert lineage.reentry is not checkpoint_wrapper.checkpoint.fresh_reentry

    relaunched = lineage.reentry
    assert relaunched.controller.presentation == (
        checkpoint_wrapper.checkpoint.fresh_reentry.controller.presentation
    )
    assert (
        relaunched.loaded_root.verification.root_record_sha256
        == root.persistence.root_record_sha256
    )
    assert (
        relaunched.loaded_declaration.verification.sequence_record_sha256
        == adoption.declaration.sequence_record_sha256
    )
    assert (
        relaunched.controller.declared_endpoint.verification.edge_record_sha256
        == edge.persistence.edge_record_sha256
    )
    _assert_three_bare_passages_survive(relaunched)


def test_50s_research_shell_relaunches_third_basis_v2_into_existing_product_family(
    tmp_path: Path,
    monkeypatch,
) -> None:
    *_, overlay, checkpoint_wrapper = _persist_bare_third_basis_overlay(
        tmp_path,
        stem="50s-shell",
    )
    assert json.loads(overlay.read_text(encoding="utf-8"))["format"] == _OVERLAY_V2
    observed: dict[str, object] = {}

    def fail_wrong_product(*args, **kwargs):
        raise AssertionError(
            "50S persisted third-basis v2 launch must retain dedicated 40B lineage"
        )

    def dedicated(lineage):
        observed["lineage"] = lineage
        return None

    monkeypatch.setattr(cli, "build_and_run_workspace", fail_wrong_product)
    monkeypatch.setattr(cli, "_run_research_session_shell", fail_wrong_product)
    monkeypatch.setattr(cli, "_run_root_backed_research_session_shell", fail_wrong_product)
    monkeypatch.setattr(
        cli,
        "_run_root_backed_continuation_research_session_shell",
        fail_wrong_product,
    )
    monkeypatch.setattr(cli, "_run_second_basis_epoch_research_session_shell", fail_wrong_product)
    monkeypatch.setattr(
        cli,
        "_run_second_basis_epoch_continuation_research_session_shell",
        fail_wrong_product,
    )
    monkeypatch.setattr(cli, "_run_controller_only_research_session_shell", fail_wrong_product)
    monkeypatch.setattr(
        cli,
        "_run_third_basis_epoch_continuation_research_session_shell",
        fail_wrong_product,
    )
    monkeypatch.setattr(cli, "_run_third_basis_epoch_research_session_shell", dedicated)

    assert (
        cli.main(
            [
                "research-shell",
                "--third-basis-epoch-overlay",
                str(overlay),
            ]
        )
        == 0
    )

    lineage = observed["lineage"]
    assert isinstance(lineage, ChromiumResearchThirdBasisEpochShellLineage)
    assert lineage.overlay_source == overlay.resolve()
    assert lineage.reentry is not checkpoint_wrapper.checkpoint.fresh_reentry
    assert lineage.reentry.controller.presentation == (
        checkpoint_wrapper.checkpoint.fresh_reentry.controller.presentation
    )
    _assert_three_bare_passages_survive(lineage.reentry)


def test_50s_existing_inspectable_first_checkpoint_product_mounts_v2_backed_lineage(
    tmp_path: Path,
) -> None:
    *_, overlay, checkpoint_wrapper = _persist_bare_third_basis_overlay(
        tmp_path,
        stem="50s-product",
    )
    plan = load_chromium_research_third_basis_epoch_reentry_plan_document(overlay)
    earned = reenter_chromium_research_third_basis_epoch(plan)
    lineage = prove_chromium_research_third_basis_epoch_shell_lineage(
        earned,
        overlay_source=overlay,
    )

    shell = create_inspectable_third_basis_epoch_cumulative_handoff_research_session_shell(
        lineage
    )

    assert shell.third_basis_epoch_launch_lineage is lineage
    assert shell.third_basis_epoch_reentry is lineage.reentry
    assert shell.research_controller is lineage.reentry.controller
    assert shell.third_basis_epoch_authority_inspection.launch_provenance.launch_location_context == (
        overlay.resolve()
    )
    assert (
        shell.third_basis_epoch_authority_inspection.launch_provenance.launch_family
        == "persisted 40B third-basis-epoch launch"
    )
    assert lineage.reentry is not checkpoint_wrapper.checkpoint.fresh_reentry
    _assert_three_bare_passages_survive(lineage.reentry)


def test_50s_research_inspect_is_deterministic_and_unchanged_for_40b_v2(
    tmp_path: Path,
    capsys,
) -> None:
    values = _persist_bare_third_basis_overlay(
        tmp_path,
        stem="50s-inspect",
    )
    root = values[6]
    edge = values[7]
    overlay = values[10]

    args = [
        "research-inspect",
        "--third-basis-epoch-overlay",
        str(overlay),
    ]
    assert cli.main(args) == 0
    first = capsys.readouterr().out
    assert cli.main(args) == 0
    second = capsys.readouterr().out
    assert first == second

    plan = load_chromium_research_third_basis_epoch_reentry_plan_document(overlay)
    reentry = reenter_chromium_research_third_basis_epoch(plan)
    lineage = prove_chromium_research_third_basis_epoch_shell_lineage(
        reentry,
        overlay_source=overlay,
    )
    expected = serialize_chromium_research_third_basis_epoch_authority_inspection(
        inspect_chromium_research_third_basis_epoch_launch(lineage)
    )
    assert first == expected

    report = json.loads(first)
    assert (
        report["format"]
        == "pyxis.chromium.research_third_basis_epoch_authority_inspection.v1"
    )
    assert report["report_role"] == "read_only_inspection_not_authority"
    assert report["launch_provenance"]["launch_family"] == (
        "persisted 40B third-basis-epoch launch"
    )
    assert report["launch_provenance"]["launch_location_context_only"] == str(
        overlay.resolve()
    )
    assert report["launch_provenance"]["third_root_sha256"] == (
        root.persistence.root_record_sha256
    )
    assert report["launch_provenance"]["launch_endpoint_sha256"] == (
        edge.persistence.edge_record_sha256
    )
    assert report["current_governed_state"]["declared_continuation_edge_count"] is None
    _assert_three_bare_passages_survive(lineage.reentry)


def test_50s_v2_configuration_still_decodes_after_referenced_root_tamper_but_41a_fails(
    tmp_path: Path,
) -> None:
    values = _persist_bare_third_basis_overlay(
        tmp_path,
        stem="50s-tamper",
    )
    root = values[6]
    overlay = values[10]
    checkpoint_wrapper = values[11]

    decoded = load_chromium_research_third_basis_epoch_reentry_plan_document(overlay)
    assert decoded == checkpoint_wrapper.checkpoint.plan

    root.persistence.path.write_bytes(root.persistence.path.read_bytes() + b"tampered")

    decoded_again = load_chromium_research_third_basis_epoch_reentry_plan_document(
        overlay
    )
    assert decoded_again == decoded

    with pytest.raises(
        ChromiumResearchThirdBasisEpochShellLineageError,
        match="could not freshly reconstruct",
    ):
        prove_chromium_research_third_basis_epoch_shell_lineage(
            checkpoint_wrapper.checkpoint.fresh_reentry,
            overlay_source=overlay,
        )
