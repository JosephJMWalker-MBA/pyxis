from __future__ import annotations

import json
from pathlib import Path

import pytest

import pyxis.cli as cli
from pyxis.app.chromium_research_paragraph_text_selection_load import (
    ChromiumPageResearchLoadedParagraphTextSelectionRecord,
)
from pyxis.app.chromium_research_second_basis_epoch_authority_inspection import (
    inspect_chromium_research_second_basis_epoch_continuation_launch,
    serialize_chromium_research_second_basis_epoch_authority_inspection,
)
from pyxis.app.chromium_research_second_basis_epoch_continuation_reentry_plan_document import (
    ChromiumResearchSecondBasisEpochContinuationReentryError,
    load_chromium_research_second_basis_epoch_continuation_reentry_plan_document,
    persist_chromium_research_second_basis_epoch_continuation_checkpoint,
    reenter_chromium_research_second_basis_epoch_continuation,
)
from pyxis.app.chromium_research_second_basis_epoch_reentry import (
    reenter_chromium_research_second_basis_epoch,
)
from pyxis.app.chromium_research_second_basis_epoch_reentry_plan_document import (
    load_chromium_research_second_basis_epoch_reentry_plan_document,
)
from pyxis.app.chromium_research_second_basis_epoch_shell_lineage import (
    ChromiumResearchSecondBasisEpochContinuationShellLineage,
    prove_chromium_research_second_basis_epoch_continuation_shell_lineage,
    prove_chromium_research_second_basis_epoch_shell_lineage,
)
from pyxis.app.chromium_research_session_rollover import (
    rollover_chromium_research_session_to_persisted_successor,
)
from pyxis.ui.second_basis_epoch_authority_inspection_shell import (
    create_inspectable_second_basis_epoch_cumulative_handoff_research_session_shell,
)
from test_app_chromium_research_second_basis_epoch_reentry_plan_document_v2 import (
    _persist_bare_second_basis_overlay,
)
from test_cli_second_basis_bare_overlay_v2_relaunch import (
    _assert_two_bare_passages_survive,
)
from test_ui_research_root_backed_session_continuation_checkpoint import (
    _write_and_rollover,
)
from test_ui_second_basis_epoch_first_continuation_checkpoint import (
    _save_checkpoint,
)


_SECOND_BASIS_OVERLAY_V2 = (
    "pyxis.chromium.research_second_basis_epoch_reentry_locator_overlay.v2"
)
_CONTINUATION_OVERLAY_V1 = (
    "pyxis.chromium.research_second_basis_epoch_continuation_locator_overlay.v1"
)


def _assert_bare_passages_survive_continuation(reentry) -> None:
    _assert_two_bare_passages_survive(
        reentry.prior_second_basis_epoch_reentry
    )
    second_bare = (
        reentry.prior_second_basis_epoch_reentry.loaded_appended_members[0]
    )
    assert isinstance(
        second_bare,
        ChromiumPageResearchLoadedParagraphTextSelectionRecord,
    )
    assert second_bare.selection.selected_text == "Bare"
    assert not hasattr(second_bare, "note")
    assert (
        reentry.controller.declared_endpoint.revision.revised_note
        .working_set.items[-1]
        is second_bare
    )


def _persist_bare_second_basis_continuation(
    tmp_path: Path,
    *,
    stem: str = "50o",
):
    values = _persist_bare_second_basis_overlay(
        tmp_path,
        stem=f"{stem}-second",
    )
    second_root = values[5]
    second_edge = values[6]
    second_overlay = values[9]
    second_checkpoint = values[10]

    second_document = json.loads(second_overlay.read_text(encoding="utf-8"))
    assert second_document["format"] == _SECOND_BASIS_OVERLAY_V2

    second_plan = load_chromium_research_second_basis_epoch_reentry_plan_document(
        second_overlay
    )
    earned = reenter_chromium_research_second_basis_epoch(second_plan)
    lineage = prove_chromium_research_second_basis_epoch_shell_lineage(
        earned,
        overlay_source=second_overlay,
    )
    prior = lineage.reentry

    successor = tmp_path / f"{stem}-post-second-successor.json"
    revision = prior.controller.persist_declared_endpoint_revision(
        "First ordinary continuation after persisted bare second-basis overlay-v2 relaunch.",
        prior_edge_source=prior.controller.declared_endpoint.verification.path,
        destination=successor,
    )
    declaration = tmp_path / f"{stem}-post-second-declaration.json"
    rollover = rollover_chromium_research_session_to_persisted_successor(
        prior.controller,
        revision,
        successor_edge_source=successor,
        declaration_destination=declaration,
    )
    continuation_overlay = tmp_path / f"{stem}-37c-continuation.overlay.json"
    checkpoint = persist_chromium_research_second_basis_epoch_continuation_checkpoint(
        prior,
        rollover,
        prior_second_basis_epoch_overlay_source=second_overlay,
        successor_edge_source=successor,
        continuation_declaration_source=declaration,
        destination=continuation_overlay,
    )
    return (
        *values,
        second_root,
        second_edge,
        second_overlay,
        second_checkpoint,
        lineage,
        prior,
        successor,
        revision,
        declaration,
        rollover,
        continuation_overlay,
        checkpoint,
    )


def test_50o_37c_remains_locator_only_v1_above_second_basis_overlay_v2(
    tmp_path: Path,
) -> None:
    values = _persist_bare_second_basis_continuation(tmp_path)
    second_root = values[11]
    second_edge = values[12]
    second_overlay = values[13]
    prior = values[16]
    successor = values[17]
    declaration = values[19]
    rollover = values[20]
    continuation_overlay = values[21]
    checkpoint = values[22]

    assert checkpoint.prior_reentry is prior
    assert checkpoint.rollover is rollover
    assert checkpoint.persistence.path == continuation_overlay.resolve()
    assert (
        checkpoint.plan.prior_second_basis_epoch_overlay_source
        == second_overlay.resolve()
    )

    document = json.loads(continuation_overlay.read_text(encoding="utf-8"))
    assert document["format"] == _CONTINUATION_OVERLAY_V1
    assert set(document) == {
        "format",
        "prior_second_basis_epoch_overlay_source",
        "declared_edge_sources",
        "declaration_source",
    }
    base = continuation_overlay.parent
    assert (
        base / document["prior_second_basis_epoch_overlay_source"]
    ).resolve() == second_overlay.resolve()
    assert [
        (base / value).resolve()
        for value in document["declared_edge_sources"]
    ] == [successor.resolve()]
    assert (base / document["declaration_source"]).resolve() == declaration.resolve()

    serialized = json.dumps(document, sort_keys=True)
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

    fresh = checkpoint.fresh_reentry
    assert fresh.prior_second_basis_epoch_reentry is not prior
    assert (
        fresh.prior_second_basis_epoch_reentry.loaded_root
        .verification.root_record_sha256
        == second_root.persistence.root_record_sha256
    )
    assert (
        fresh.prior_second_basis_epoch_reentry.controller.declared_endpoint
        .verification.edge_record_sha256
        == second_edge.persistence.edge_record_sha256
    )
    assert fresh.controller.presentation == rollover.continuation_controller.presentation
    assert (
        fresh.controller.declared_endpoint.verification.edge_record_sha256
        == rollover.continuation_controller.declared_endpoint.verification.edge_record_sha256
    )
    _assert_bare_passages_survive_continuation(fresh)

    decoded = load_chromium_research_second_basis_epoch_continuation_reentry_plan_document(
        continuation_overlay
    )
    assert decoded == checkpoint.plan
    roundtrip = reenter_chromium_research_second_basis_epoch_continuation(decoded)
    assert roundtrip is not fresh
    assert roundtrip.controller.presentation == fresh.controller.presentation
    _assert_bare_passages_survive_continuation(roundtrip)


@pytest.mark.asyncio
async def test_50o_existing_first_checkpoint_product_persists_37c_v1_above_v2_launch(
    tmp_path: Path,
) -> None:
    values = _persist_bare_second_basis_overlay(
        tmp_path,
        stem="50o-ui-second",
    )
    second_overlay = values[9]
    plan = load_chromium_research_second_basis_epoch_reentry_plan_document(
        second_overlay
    )
    earned = reenter_chromium_research_second_basis_epoch(plan)
    lineage = prove_chromium_research_second_basis_epoch_shell_lineage(
        earned,
        overlay_source=second_overlay,
    )
    shell = create_inspectable_second_basis_epoch_cumulative_handoff_research_session_shell(
        lineage
    )
    prior = lineage.reentry
    successor = tmp_path / "50o-ui-successor.json"
    declaration = tmp_path / "50o-ui-declaration.json"
    continuation_overlay = tmp_path / "50o-ui-37c.overlay.json"

    async with shell.run_test(size=(175, 280)) as pilot:
        await pilot.pause()
        inspection = shell.second_basis_epoch_authority_inspection
        launch = inspection.launch_provenance
        mounted_before_rollover = shell.research_controller

        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=prior.controller.declared_endpoint.verification.path,
            successor=successor,
            declaration=declaration,
            text="50O one governed continuation above persisted second-basis overlay-v2.",
        )

        one_hop_controller = shell.research_controller
        rollover = shell.last_research_rollover
        assert rollover is not None
        assert one_hop_controller is not mounted_before_rollover
        assert inspection.launch_provenance is launch
        assert launch.launch_location_context == second_overlay.resolve()

        await _save_checkpoint(
            shell,
            pilot,
            prior_overlay=second_overlay,
            successor=successor,
            declaration=declaration,
            destination=continuation_overlay,
        )

        result = shell.last_second_basis_epoch_continuation_checkpoint
        assert result is not None
        assert result.prior_reentry is prior
        assert result.rollover is rollover
        assert shell.research_controller is one_hop_controller
        assert result.fresh_reentry.controller is not one_hop_controller
        assert result.fresh_reentry.controller.presentation == one_hop_controller.presentation
        assert inspection.launch_provenance is launch
        assert launch.launch_location_context == second_overlay.resolve()

        document = json.loads(continuation_overlay.read_text(encoding="utf-8"))
        assert document["format"] == _CONTINUATION_OVERLAY_V1
        base = continuation_overlay.parent
        assert (
            base / document["prior_second_basis_epoch_overlay_source"]
        ).resolve() == second_overlay.resolve()
        _assert_bare_passages_survive_continuation(result.fresh_reentry)


def test_50o_cli_relaunches_37c_v1_above_second_basis_v2_ancestry(
    tmp_path: Path,
    monkeypatch,
) -> None:
    *_, continuation_overlay, checkpoint = _persist_bare_second_basis_continuation(
        tmp_path,
        stem="50o-shell",
    )
    observed: dict[str, object] = {}

    def fail_wrong_product(*args, **kwargs):
        raise AssertionError(
            "50O continuation relaunch must retain dedicated persisted 37C lineage"
        )

    def dedicated(lineage):
        observed["lineage"] = lineage

    monkeypatch.setattr(cli, "_run_controller_only_research_session_shell", fail_wrong_product)
    monkeypatch.setattr(cli, "_run_second_basis_epoch_research_session_shell", fail_wrong_product)
    monkeypatch.setattr(
        cli,
        "_run_root_backed_continuation_research_session_shell",
        fail_wrong_product,
    )
    monkeypatch.setattr(
        cli,
        "_run_second_basis_epoch_continuation_research_session_shell",
        dedicated,
    )

    assert (
        cli.main(
            [
                "research-shell",
                "--second-basis-epoch-continuation-overlay",
                str(continuation_overlay),
            ]
        )
        == 0
    )

    lineage = observed["lineage"]
    assert isinstance(
        lineage,
        ChromiumResearchSecondBasisEpochContinuationShellLineage,
    )
    assert lineage.overlay_source == continuation_overlay.resolve()
    assert lineage.reentry is not checkpoint.fresh_reentry
    assert (
        lineage.reentry.controller.presentation
        == checkpoint.fresh_reentry.controller.presentation
    )
    _assert_bare_passages_survive_continuation(lineage.reentry)


def test_50o_research_inspect_is_deterministic_for_37c_above_second_basis_v2(
    tmp_path: Path,
    capsys,
) -> None:
    *_, continuation_overlay, checkpoint = _persist_bare_second_basis_continuation(
        tmp_path,
        stem="50o-inspect",
    )

    args = [
        "research-inspect",
        "--second-basis-epoch-continuation-overlay",
        str(continuation_overlay),
    ]
    assert cli.main(args) == 0
    first = capsys.readouterr().out
    assert cli.main(args) == 0
    second = capsys.readouterr().out
    assert first == second

    plan = load_chromium_research_second_basis_epoch_continuation_reentry_plan_document(
        continuation_overlay
    )
    reentry = reenter_chromium_research_second_basis_epoch_continuation(plan)
    lineage = prove_chromium_research_second_basis_epoch_continuation_shell_lineage(
        reentry,
        overlay_source=continuation_overlay,
    )
    expected = serialize_chromium_research_second_basis_epoch_authority_inspection(
        inspect_chromium_research_second_basis_epoch_continuation_launch(lineage)
    )
    assert first == expected

    report = json.loads(first)
    assert (
        report["format"]
        == "pyxis.chromium.research_second_basis_epoch_authority_inspection.v1"
    )
    assert report["report_role"] == "read_only_inspection_not_authority"
    assert report["launch_provenance"]["launch_family"] == (
        "persisted 37C/37D continuation launch"
    )
    assert report["launch_provenance"]["launch_location_context_only"] == str(
        continuation_overlay.resolve()
    )
    assert report["current_governed_state"]["declared_continuation_edge_count"] == 1
    assert report["current_governed_state"]["endpoint_sha256"] == (
        checkpoint.fresh_reentry.controller.declared_endpoint.verification.edge_record_sha256
    )
    _assert_bare_passages_survive_continuation(lineage.reentry)


def test_50o_tampered_37b_v2_breaks_fresh_37c_reentry_after_config_decode(
    tmp_path: Path,
) -> None:
    values = _persist_bare_second_basis_continuation(
        tmp_path,
        stem="50o-tamper",
    )
    second_overlay = values[13]
    continuation_overlay = values[21]

    decoded = load_chromium_research_second_basis_epoch_continuation_reentry_plan_document(
        continuation_overlay
    )
    assert decoded.prior_second_basis_epoch_overlay_source == second_overlay.resolve()

    second_overlay.write_bytes(second_overlay.read_bytes() + b"tampered")

    # The 37C file remains valid locator-only configuration; authority reconstruction
    # fails only when the explicitly referenced 37B ancestry is opened and re-proven.
    decoded_again = (
        load_chromium_research_second_basis_epoch_continuation_reentry_plan_document(
            continuation_overlay
        )
    )
    assert decoded_again == decoded

    with pytest.raises(
        ChromiumResearchSecondBasisEpochContinuationReentryError,
        match="prior 37B second-basis-epoch overlay",
    ):
        reenter_chromium_research_second_basis_epoch_continuation(decoded_again)
