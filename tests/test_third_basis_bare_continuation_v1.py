from __future__ import annotations

import json
from pathlib import Path

import pytest
from textual.widgets import Button, Input

import pyxis.cli as cli
from pyxis.app.chromium_research_third_basis_epoch_authority_inspection import (
    inspect_chromium_research_third_basis_epoch_continuation_launch,
)
from pyxis.app.chromium_research_third_basis_epoch_authority_inspection_report import (
    serialize_chromium_research_third_basis_epoch_authority_inspection,
)
from pyxis.app.chromium_research_third_basis_epoch_continuation_reentry_plan_document import (
    ChromiumResearchThirdBasisEpochContinuationReentryError,
    load_chromium_research_third_basis_epoch_continuation_reentry_plan_document,
    persist_chromium_research_third_basis_epoch_continuation_checkpoint,
    reenter_chromium_research_third_basis_epoch_continuation,
)
from pyxis.app.chromium_research_third_basis_epoch_reentry import (
    reenter_chromium_research_third_basis_epoch,
)
from pyxis.app.chromium_research_third_basis_epoch_reentry_plan_document import (
    load_chromium_research_third_basis_epoch_reentry_plan_document,
)
from pyxis.app.chromium_research_third_basis_epoch_shell_lineage import (
    ChromiumResearchThirdBasisEpochContinuationShellLineage,
    prove_chromium_research_third_basis_epoch_continuation_shell_lineage,
    prove_chromium_research_third_basis_epoch_shell_lineage,
)
from pyxis.app.chromium_research_session_rollover import (
    rollover_chromium_research_session_to_persisted_successor,
)
from pyxis.ui.chromium_research_third_basis_epoch_continuation_checkpoint_textual import (
    ThirdBasisEpochResearchSessionContinuationCheckpointControls,
)
from pyxis.ui.third_basis_epoch_authority_inspection_shell import (
    create_inspectable_third_basis_epoch_cumulative_handoff_research_session_shell,
)
from test_app_chromium_research_third_basis_epoch_reentry_plan_document_v2 import (
    _persist_bare_third_basis_overlay,
)
from test_cli_third_basis_bare_overlay_v2_relaunch import (
    _assert_three_bare_passages_survive,
)
from test_ui_research_root_backed_session_continuation_checkpoint import (
    _write_and_rollover,
)
from test_ui_third_basis_epoch_first_continuation_checkpoint import (
    _save_checkpoint,
)


_THIRD_BASIS_OVERLAY_V2 = (
    "pyxis.chromium.research_third_basis_epoch_reentry_locator_overlay.v2"
)
_CONTINUATION_OVERLAY_V1 = (
    "pyxis.chromium.research_third_basis_epoch_continuation_locator_overlay.v1"
)


def _assert_three_bare_passages_survive_continuation(reentry) -> None:
    _assert_three_bare_passages_survive(reentry.prior_third_basis_epoch_reentry)
    third_bare = reentry.prior_third_basis_epoch_reentry.loaded_appended_members[0]
    assert (
        reentry.controller.declared_endpoint.revision.revised_note.working_set.items[-1]
        is third_bare
    )


def _persist_bare_third_basis_continuation(
    tmp_path: Path,
    *,
    stem: str = "50t",
):
    values = _persist_bare_third_basis_overlay(
        tmp_path,
        stem=f"{stem}-third",
    )
    third_root = values[6]
    third_edge = values[7]
    third_overlay = values[10]
    third_checkpoint = values[11]

    document = json.loads(third_overlay.read_text(encoding="utf-8"))
    assert document["format"] == _THIRD_BASIS_OVERLAY_V2

    plan = load_chromium_research_third_basis_epoch_reentry_plan_document(third_overlay)
    earned = reenter_chromium_research_third_basis_epoch(plan)
    lineage = prove_chromium_research_third_basis_epoch_shell_lineage(
        earned,
        overlay_source=third_overlay,
    )
    prior = lineage.reentry
    _assert_three_bare_passages_survive(prior)

    successor = tmp_path / f"{stem}-post-third-successor.json"
    revision = prior.controller.persist_declared_endpoint_revision(
        "First ordinary continuation after persisted bare third-basis overlay-v2 relaunch.",
        prior_edge_source=prior.controller.declared_endpoint.verification.path,
        destination=successor,
    )
    declaration = tmp_path / f"{stem}-post-third-declaration.json"
    rollover = rollover_chromium_research_session_to_persisted_successor(
        prior.controller,
        revision,
        successor_edge_source=successor,
        declaration_destination=declaration,
    )
    continuation_overlay = tmp_path / f"{stem}-40c-continuation.overlay.json"
    checkpoint = persist_chromium_research_third_basis_epoch_continuation_checkpoint(
        prior,
        rollover,
        prior_third_basis_epoch_overlay_source=third_overlay,
        successor_edge_source=successor,
        continuation_declaration_source=declaration,
        destination=continuation_overlay,
    )
    return (
        *values,
        third_root,
        third_edge,
        third_overlay,
        third_checkpoint,
        lineage,
        prior,
        successor,
        revision,
        declaration,
        rollover,
        continuation_overlay,
        checkpoint,
    )


def test_50t_40c_remains_locator_only_v1_above_third_basis_overlay_v2(
    tmp_path: Path,
) -> None:
    values = _persist_bare_third_basis_continuation(tmp_path)
    third_root = values[12]
    third_edge = values[13]
    third_overlay = values[14]
    prior = values[17]
    successor = values[18]
    declaration = values[20]
    rollover = values[21]
    continuation_overlay = values[22]
    checkpoint = values[23]

    assert checkpoint.prior_reentry is prior
    assert checkpoint.rollover is rollover
    assert checkpoint.persistence.path == continuation_overlay.resolve()
    assert checkpoint.plan.prior_third_basis_epoch_overlay_source == (
        third_overlay.resolve()
    )

    document = json.loads(continuation_overlay.read_text(encoding="utf-8"))
    assert document["format"] == _CONTINUATION_OVERLAY_V1
    assert set(document) == {
        "format",
        "prior_third_basis_epoch_overlay_source",
        "declared_edge_sources",
        "declaration_source",
    }
    base = continuation_overlay.parent
    assert (
        base / document["prior_third_basis_epoch_overlay_source"]
    ).resolve() == third_overlay.resolve()
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
    assert fresh.prior_third_basis_epoch_reentry is not prior
    assert (
        fresh.prior_third_basis_epoch_reentry.loaded_root.verification.root_record_sha256
        == third_root.persistence.root_record_sha256
    )
    assert (
        fresh.prior_third_basis_epoch_reentry.controller.declared_endpoint
        .verification.edge_record_sha256
        == third_edge.persistence.edge_record_sha256
    )
    assert fresh.controller.presentation == rollover.continuation_controller.presentation
    assert (
        fresh.controller.declared_endpoint.verification.edge_record_sha256
        == rollover.continuation_controller.declared_endpoint.verification.edge_record_sha256
    )
    _assert_three_bare_passages_survive_continuation(fresh)

    decoded = load_chromium_research_third_basis_epoch_continuation_reentry_plan_document(
        continuation_overlay
    )
    assert decoded == checkpoint.plan
    roundtrip = reenter_chromium_research_third_basis_epoch_continuation(decoded)
    assert roundtrip is not fresh
    assert roundtrip.controller.presentation == fresh.controller.presentation
    _assert_three_bare_passages_survive_continuation(roundtrip)


@pytest.mark.asyncio
async def test_50t_existing_first_checkpoint_product_persists_40c_v1_above_v2_launch(
    tmp_path: Path,
) -> None:
    values = _persist_bare_third_basis_overlay(
        tmp_path,
        stem="50t-ui-third",
    )
    third_overlay = values[10]
    plan = load_chromium_research_third_basis_epoch_reentry_plan_document(third_overlay)
    earned = reenter_chromium_research_third_basis_epoch(plan)
    lineage = prove_chromium_research_third_basis_epoch_shell_lineage(
        earned,
        overlay_source=third_overlay,
    )
    shell = create_inspectable_third_basis_epoch_cumulative_handoff_research_session_shell(
        lineage
    )
    prior = lineage.reentry
    successor = tmp_path / "50t-ui-successor.json"
    declaration = tmp_path / "50t-ui-declaration.json"
    continuation_overlay = tmp_path / "50t-ui-40c.overlay.json"

    async with shell.run_test(size=(190, 320)) as pilot:
        await pilot.pause()
        panel = shell.third_basis_epoch_authority_inspection
        launch = panel.launch_provenance
        launch_controller = shell.research_controller
        assert launch.launch_location_context == third_overlay.resolve()
        assert len(shell.query(ThirdBasisEpochResearchSessionContinuationCheckpointControls)) == 0

        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=prior.controller.declared_endpoint.verification.path,
            successor=successor,
            declaration=declaration,
            text="50T one governed continuation above persisted third-basis overlay-v2.",
        )

        controls = shell.query_one(ThirdBasisEpochResearchSessionContinuationCheckpointControls)
        rollover = shell.last_research_rollover
        one_hop_controller = shell.research_controller
        assert rollover is not None
        assert one_hop_controller is not launch_controller
        assert controls.rollover is rollover
        assert panel.launch_provenance is launch
        for selector in (
            "#research-third-basis-epoch-checkpoint-prior-overlay-source",
            "#research-third-basis-epoch-checkpoint-successor-source",
            "#research-third-basis-epoch-checkpoint-declaration-source",
            "#research-third-basis-epoch-checkpoint-destination",
        ):
            assert shell.query_one(selector, Input).value == ""

        await _save_checkpoint(
            shell,
            pilot,
            prior_overlay=third_overlay,
            successor=successor,
            declaration=declaration,
            destination=continuation_overlay,
        )

        result = shell.last_third_basis_epoch_continuation_checkpoint
        assert result is not None
        assert result.prior_reentry is prior
        assert result.rollover is rollover
        assert shell.third_basis_epoch_launch_lineage is lineage
        assert shell.research_controller is one_hop_controller
        assert result.fresh_reentry.controller is not one_hop_controller
        assert result.fresh_reentry.controller.presentation == one_hop_controller.presentation
        assert panel.launch_provenance is launch
        assert launch.launch_location_context == third_overlay.resolve()
        assert panel.current_state.endpoint_sha256 == (
            one_hop_controller.declared_endpoint.verification.edge_record_sha256
        )
        assert shell.query_one(
            "#save-research-third-basis-epoch-continuation-checkpoint",
            Button,
        ).disabled

        document = json.loads(continuation_overlay.read_text(encoding="utf-8"))
        assert document["format"] == _CONTINUATION_OVERLAY_V1
        _assert_three_bare_passages_survive_continuation(result.fresh_reentry)


def test_50t_cli_relaunches_40c_v1_above_third_basis_v2_ancestry(
    tmp_path: Path,
    monkeypatch,
) -> None:
    *_, continuation_overlay, checkpoint = _persist_bare_third_basis_continuation(
        tmp_path,
        stem="50t-shell",
    )
    observed: dict[str, object] = {}

    def fail_wrong_product(*args, **kwargs):
        raise AssertionError(
            "50T continuation relaunch must retain dedicated persisted 40C lineage"
        )

    def dedicated(lineage):
        observed["lineage"] = lineage

    monkeypatch.setattr(cli, "build_and_run_workspace", fail_wrong_product)
    monkeypatch.setattr(cli, "_run_research_session_shell", fail_wrong_product)
    monkeypatch.setattr(cli, "_run_root_backed_research_session_shell", fail_wrong_product)
    monkeypatch.setattr(
        cli,
        "_run_root_backed_continuation_research_session_shell",
        fail_wrong_product,
    )
    monkeypatch.setattr(cli, "_run_controller_only_research_session_shell", fail_wrong_product)
    monkeypatch.setattr(cli, "_run_second_basis_epoch_research_session_shell", fail_wrong_product)
    monkeypatch.setattr(
        cli,
        "_run_second_basis_epoch_continuation_research_session_shell",
        fail_wrong_product,
    )
    monkeypatch.setattr(cli, "_run_third_basis_epoch_research_session_shell", fail_wrong_product)
    monkeypatch.setattr(
        cli,
        "_run_third_basis_epoch_continuation_research_session_shell",
        dedicated,
    )

    assert (
        cli.main(
            [
                "research-shell",
                "--third-basis-epoch-continuation-overlay",
                str(continuation_overlay),
            ]
        )
        == 0
    )

    lineage = observed["lineage"]
    assert isinstance(lineage, ChromiumResearchThirdBasisEpochContinuationShellLineage)
    assert lineage.overlay_source == continuation_overlay.resolve()
    assert lineage.reentry is not checkpoint.fresh_reentry
    assert lineage.reentry.controller.presentation == checkpoint.fresh_reentry.controller.presentation
    _assert_three_bare_passages_survive_continuation(lineage.reentry)


def test_50t_research_inspect_is_deterministic_for_40c_above_third_basis_v2(
    tmp_path: Path,
    capsys,
) -> None:
    *_, continuation_overlay, checkpoint = _persist_bare_third_basis_continuation(
        tmp_path,
        stem="50t-inspect",
    )

    args = [
        "research-inspect",
        "--third-basis-epoch-continuation-overlay",
        str(continuation_overlay),
    ]
    assert cli.main(args) == 0
    first = capsys.readouterr().out
    assert cli.main(args) == 0
    second = capsys.readouterr().out
    assert first == second

    plan = load_chromium_research_third_basis_epoch_continuation_reentry_plan_document(
        continuation_overlay
    )
    reentry = reenter_chromium_research_third_basis_epoch_continuation(plan)
    lineage = prove_chromium_research_third_basis_epoch_continuation_shell_lineage(
        reentry,
        overlay_source=continuation_overlay,
    )
    expected = serialize_chromium_research_third_basis_epoch_authority_inspection(
        inspect_chromium_research_third_basis_epoch_continuation_launch(lineage)
    )
    assert first == expected

    report = json.loads(first)
    assert (
        report["format"]
        == "pyxis.chromium.research_third_basis_epoch_authority_inspection.v1"
    )
    assert report["report_role"] == "read_only_inspection_not_authority"
    assert report["launch_provenance"]["launch_family"] == (
        "persisted 40C/40D continuation launch"
    )
    assert report["launch_provenance"]["launch_location_context_only"] == str(
        continuation_overlay.resolve()
    )
    assert report["current_governed_state"]["declared_continuation_edge_count"] == 1
    assert report["current_governed_state"]["endpoint_sha256"] == (
        checkpoint.fresh_reentry.controller.declared_endpoint.verification.edge_record_sha256
    )
    _assert_three_bare_passages_survive_continuation(lineage.reentry)


def test_50t_tampered_40b_v2_breaks_fresh_40c_reentry_after_config_decode(
    tmp_path: Path,
) -> None:
    values = _persist_bare_third_basis_continuation(
        tmp_path,
        stem="50t-tamper",
    )
    third_overlay = values[14]
    continuation_overlay = values[22]

    decoded = load_chromium_research_third_basis_epoch_continuation_reentry_plan_document(
        continuation_overlay
    )
    assert decoded.prior_third_basis_epoch_overlay_source == third_overlay.resolve()

    third_overlay.write_bytes(third_overlay.read_bytes() + b"tampered")

    decoded_again = (
        load_chromium_research_third_basis_epoch_continuation_reentry_plan_document(
            continuation_overlay
        )
    )
    assert decoded_again == decoded

    with pytest.raises(
        ChromiumResearchThirdBasisEpochContinuationReentryError,
        match="prior 40B third-basis-epoch overlay",
    ):
        reenter_chromium_research_third_basis_epoch_continuation(decoded_again)
