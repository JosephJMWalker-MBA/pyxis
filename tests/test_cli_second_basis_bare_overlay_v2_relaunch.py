from __future__ import annotations

import json
from pathlib import Path

import pyxis.cli as cli
from pyxis.app.chromium_research_paragraph_text_selection_load import (
    ChromiumPageResearchLoadedParagraphTextSelectionRecord,
)
from pyxis.app.chromium_research_second_basis_epoch_authority_inspection import (
    inspect_chromium_research_second_basis_epoch_launch,
    serialize_chromium_research_second_basis_epoch_authority_inspection,
)
from pyxis.app.chromium_research_second_basis_epoch_reentry import (
    reenter_chromium_research_second_basis_epoch,
)
from pyxis.app.chromium_research_second_basis_epoch_reentry_plan_document import (
    load_chromium_research_second_basis_epoch_reentry_plan_document,
)
from pyxis.app.chromium_research_second_basis_epoch_shell_lineage import (
    ChromiumResearchSecondBasisEpochShellLineage,
    prove_chromium_research_second_basis_epoch_shell_lineage,
)
from test_app_chromium_research_second_basis_epoch_reentry_plan_document_v2 import (
    _persist_bare_second_basis_overlay,
)


_OVERLAY_V2 = "pyxis.chromium.research_second_basis_epoch_reentry_locator_overlay.v2"


def _assert_two_bare_passages_survive(reentry) -> None:
    first_bare = (
        reentry.prior_continuation_reentry.prior_root_backed_reentry
        .loaded_appended_members[0]
    )
    assert isinstance(
        first_bare,
        ChromiumPageResearchLoadedParagraphTextSelectionRecord,
    )
    assert first_bare.selection.selected_text == "Bare"
    assert not hasattr(first_bare, "note")
    assert (
        reentry.prior_continuation_reentry.prior_root_backed_reentry
        .loaded_root.transition.successor_note.note.working_set.items[-1]
        is first_bare
    )
    assert (
        reentry.prior_continuation_reentry.controller.declared_endpoint
        .revision.revised_note.working_set.items[-1]
        is first_bare
    )

    second_bare = reentry.loaded_appended_members[0]
    assert isinstance(
        second_bare,
        ChromiumPageResearchLoadedParagraphTextSelectionRecord,
    )
    assert second_bare.selection.selected_text == "Bare"
    assert not hasattr(second_bare, "note")
    assert (
        reentry.loaded_root.transition.successor_note.note.working_set.items[-1]
        is second_bare
    )
    assert (
        reentry.controller.declared_endpoint.revision.revised_note
        .working_set.items[-1]
        is second_bare
    )
    assert first_bare is not second_bare


def test_50n_research_shell_relaunches_second_basis_bare_overlay_v2_into_existing_product(
    tmp_path: Path,
    monkeypatch,
) -> None:
    (
        _,
        _,
        _,
        _,
        _,
        root,
        edge,
        _,
        verification,
        overlay,
        checkpoint_wrapper,
    ) = _persist_bare_second_basis_overlay(tmp_path, stem="50n-shell")

    document = json.loads(overlay.read_text(encoding="utf-8"))
    assert document["format"] == _OVERLAY_V2

    observed: dict[str, object] = {}

    def fail_workspace(*args, **kwargs):
        raise AssertionError("50N second-basis relaunch must not build Workspace state")

    def fail_wrong_product(*args, **kwargs):
        raise AssertionError(
            "50N second-basis relaunch must retain dedicated persisted 37B lineage"
        )

    def dedicated(lineage):
        observed["lineage"] = lineage
        return None

    monkeypatch.setattr(cli, "build_and_run_workspace", fail_workspace)
    monkeypatch.setattr(cli, "_run_research_session_shell", fail_wrong_product)
    monkeypatch.setattr(cli, "_run_root_backed_research_session_shell", fail_wrong_product)
    monkeypatch.setattr(
        cli,
        "_run_root_backed_continuation_research_session_shell",
        fail_wrong_product,
    )
    monkeypatch.setattr(
        cli,
        "_run_controller_only_research_session_shell",
        fail_wrong_product,
    )
    monkeypatch.setattr(
        cli,
        "_run_second_basis_epoch_research_session_shell",
        dedicated,
    )

    assert (
        cli.main(
            [
                "research-shell",
                "--second-basis-epoch-overlay",
                str(overlay),
            ]
        )
        == 0
    )

    lineage = observed["lineage"]
    assert isinstance(lineage, ChromiumResearchSecondBasisEpochShellLineage)
    assert lineage.overlay_source == overlay.resolve()

    fresh = lineage.reentry
    assert fresh is not verification.fresh_reentry
    assert fresh is not checkpoint_wrapper.checkpoint.fresh_reentry
    assert (
        fresh.controller.presentation
        == checkpoint_wrapper.checkpoint.fresh_reentry.controller.presentation
    )
    assert (
        fresh.loaded_root.verification.root_record_sha256
        == root.persistence.root_record_sha256
    )
    assert (
        fresh.controller.declared_endpoint.verification.edge_record_sha256
        == edge.persistence.edge_record_sha256
    )
    assert (
        fresh.prior_continuation_reentry.prior_root_backed_reentry
        .loaded_root.verification.root_record_sha256
        == checkpoint_wrapper.checkpoint.fresh_reentry.prior_continuation_reentry
        .prior_root_backed_reentry.loaded_root.verification.root_record_sha256
    )

    _assert_two_bare_passages_survive(fresh)


def test_50n_research_inspect_is_deterministic_for_second_basis_bare_overlay_v2(
    tmp_path: Path,
    capsys,
) -> None:
    (
        _,
        _,
        _,
        _,
        _,
        root,
        edge,
        _,
        _,
        overlay,
        _,
    ) = _persist_bare_second_basis_overlay(tmp_path, stem="50n-inspect")

    document = json.loads(overlay.read_text(encoding="utf-8"))
    assert document["format"] == _OVERLAY_V2

    assert (
        cli.main(
            [
                "research-inspect",
                "--second-basis-epoch-overlay",
                str(overlay),
            ]
        )
        == 0
    )
    first = capsys.readouterr().out
    assert (
        cli.main(
            [
                "research-inspect",
                "--second-basis-epoch-overlay",
                str(overlay),
            ]
        )
        == 0
    )
    second = capsys.readouterr().out
    assert first == second

    plan = load_chromium_research_second_basis_epoch_reentry_plan_document(overlay)
    reentry = reenter_chromium_research_second_basis_epoch(plan)
    lineage = prove_chromium_research_second_basis_epoch_shell_lineage(
        reentry,
        overlay_source=overlay,
    )
    expected = serialize_chromium_research_second_basis_epoch_authority_inspection(
        inspect_chromium_research_second_basis_epoch_launch(lineage)
    )
    assert first == expected

    report = json.loads(first)
    assert (
        report["format"]
        == "pyxis.chromium.research_second_basis_epoch_authority_inspection.v1"
    )
    assert report["report_role"] == "read_only_inspection_not_authority"
    assert report["launch_provenance"]["launch_family"] == (
        "persisted 37B second-basis-epoch launch"
    )
    assert report["launch_provenance"]["launch_location_context_only"] == str(
        overlay.resolve()
    )
    assert (
        report["launch_provenance"]["second_root_sha256"]
        == root.persistence.root_record_sha256
    )
    assert (
        report["launch_provenance"]["launch_endpoint_sha256"]
        == edge.persistence.edge_record_sha256
    )
    assert report["current_governed_state"]["endpoint_sha256"] == (
        edge.persistence.edge_record_sha256
    )
    assert (
        report["current_governed_state"]["declared_continuation_edge_count"]
        is None
    )

    _assert_two_bare_passages_survive(lineage.reentry)
