from __future__ import annotations

import json
from pathlib import Path

import pytest
from textual.widgets import Input

import pyxis.cli as cli
from pyxis.app.chromium_research_third_basis_epoch_authority_inspection import (
    inspect_chromium_research_third_basis_epoch_continuation_launch,
)
from pyxis.app.chromium_research_third_basis_epoch_authority_inspection_report import (
    serialize_chromium_research_third_basis_epoch_authority_inspection,
)
from pyxis.app.chromium_research_third_basis_epoch_continuation_checkpoint_extension import (
    ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionError,
    persist_chromium_research_third_basis_epoch_continuation_checkpoint_extension,
)
from pyxis.app.chromium_research_third_basis_epoch_continuation_reentry_plan_document import (
    ChromiumResearchThirdBasisEpochContinuationReentryError,
    load_chromium_research_third_basis_epoch_continuation_reentry_plan_document,
    reenter_chromium_research_third_basis_epoch_continuation,
)
from pyxis.app.chromium_research_third_basis_epoch_shell_lineage import (
    ChromiumResearchThirdBasisEpochContinuationShellLineage,
    prove_chromium_research_third_basis_epoch_continuation_shell_lineage,
)
from pyxis.app.chromium_research_session_rollover import (
    rollover_chromium_research_session_to_persisted_successor,
)
from pyxis.ui.third_basis_epoch_authority_inspection_shell import (
    create_inspectable_third_basis_epoch_continuation_research_session_shell,
)
from test_third_basis_bare_continuation_v1 import (
    _assert_three_bare_passages_survive_continuation,
    _persist_bare_third_basis_continuation,
)
from test_ui_research_root_backed_session_continuation_checkpoint import (
    _write_and_rollover,
)
from test_ui_third_basis_epoch_cumulative_checkpoint import (
    _save_cumulative,
)


_THIRD_BASIS_OVERLAY_V2 = (
    "pyxis.chromium.research_third_basis_epoch_reentry_locator_overlay.v2"
)
_CONTINUATION_OVERLAY_V1 = (
    "pyxis.chromium.research_third_basis_epoch_continuation_locator_overlay.v1"
)


def _persist_bare_third_basis_cumulative(
    tmp_path: Path,
    *,
    stem: str = "50u",
):
    values = _persist_bare_third_basis_continuation(
        tmp_path,
        stem=f"{stem}-current",
    )
    third_overlay = values[14]
    current_overlay = values[22]
    current_checkpoint = values[23]
    current = current_checkpoint.fresh_reentry

    third_document = json.loads(third_overlay.read_text(encoding="utf-8"))
    current_document = json.loads(current_overlay.read_text(encoding="utf-8"))
    assert third_document["format"] == _THIRD_BASIS_OVERLAY_V2
    assert current_document["format"] == _CONTINUATION_OVERLAY_V1

    successor = tmp_path / f"{stem}-next-successor.json"
    revision = current.controller.persist_declared_endpoint_revision(
        "Second ordinary continuation above the persisted bare third-basis epoch.",
        prior_edge_source=current.controller.declared_endpoint.verification.path,
        destination=successor,
    )
    one_hop_declaration = tmp_path / f"{stem}-next-one-hop-declaration.json"
    rollover = rollover_chromium_research_session_to_persisted_successor(
        current.controller,
        revision,
        successor_edge_source=successor,
        declaration_destination=one_hop_declaration,
    )
    cumulative_declaration = tmp_path / f"{stem}-cumulative-declaration.json"
    next_overlay = tmp_path / f"{stem}-next-40c.overlay.json"

    current_overlay_bytes = current_overlay.read_bytes()
    one_hop_bytes = one_hop_declaration.read_bytes()

    result = persist_chromium_research_third_basis_epoch_continuation_checkpoint_extension(
        current,
        rollover,
        current_overlay_source=current_overlay,
        successor_edge_source=successor,
        cumulative_declaration_destination=cumulative_declaration,
        next_overlay_destination=next_overlay,
    )
    return (
        *values,
        third_overlay,
        current_overlay,
        current,
        successor,
        revision,
        one_hop_declaration,
        rollover,
        cumulative_declaration,
        next_overlay,
        current_overlay_bytes,
        one_hop_bytes,
        result,
    )


def test_50u_40d_preserves_direct_v2_anchor_and_unchanged_40c_v1(
    tmp_path: Path,
) -> None:
    values = _persist_bare_third_basis_cumulative(tmp_path)
    third_overlay = values[24]
    current_overlay = values[25]
    current = values[26]
    successor = values[27]
    one_hop_declaration = values[29]
    rollover = values[30]
    cumulative_declaration = values[31]
    next_overlay = values[32]
    current_overlay_bytes = values[33]
    one_hop_bytes = values[34]
    result = values[35]

    assert result.current_reentry is current
    assert result.rollover is rollover
    assert result.current_plan == current.plan
    assert result.next_plan.prior_third_basis_epoch_overlay_source == (
        current.plan.prior_third_basis_epoch_overlay_source
    )
    assert result.next_plan.prior_third_basis_epoch_overlay_source == (
        third_overlay.resolve()
    )
    assert result.next_plan.prior_third_basis_epoch_overlay_source != (
        current_overlay.resolve()
    )
    assert result.next_plan.declared_edge_sources == (
        *result.current_plan.declared_edge_sources,
        successor.resolve(),
    )
    assert result.next_plan.declaration_source == cumulative_declaration.resolve()
    assert len(result.explicit_sequence.edges) == len(
        result.current_plan.declared_edge_sources
    ) + 1
    assert (
        result.fresh_reentry.controller.declared_endpoint.verification.edge_record_sha256
        == rollover.continuation_controller.declared_endpoint.verification.edge_record_sha256
    )

    document = json.loads(next_overlay.read_text(encoding="utf-8"))
    assert document["format"] == _CONTINUATION_OVERLAY_V1
    assert set(document) == {
        "format",
        "prior_third_basis_epoch_overlay_source",
        "declared_edge_sources",
        "declaration_source",
    }
    base = next_overlay.parent
    assert (
        base / document["prior_third_basis_epoch_overlay_source"]
    ).resolve() == third_overlay.resolve()
    assert (
        base / document["prior_third_basis_epoch_overlay_source"]
    ).resolve() != current_overlay.resolve()
    assert [
        (base / value).resolve()
        for value in document["declared_edge_sources"]
    ] == list(result.next_plan.declared_edge_sources)
    assert (base / document["declaration_source"]).resolve() == (
        cumulative_declaration.resolve()
    )

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

    assert current_overlay.read_bytes() == current_overlay_bytes
    assert one_hop_declaration.read_bytes() == one_hop_bytes

    _assert_three_bare_passages_survive_continuation(result.fresh_reentry)
    assert (
        result.fresh_reentry.prior_third_basis_epoch_reentry.loaded_root
        .verification.root_record_sha256
        == current.prior_third_basis_epoch_reentry.loaded_root
        .verification.root_record_sha256
    )
    assert (
        result.fresh_reentry.prior_third_basis_epoch_reentry
        .prior_second_basis_epoch_continuation_reentry
        .prior_second_basis_epoch_reentry.loaded_root.verification.root_record_sha256
        == current.prior_third_basis_epoch_reentry
        .prior_second_basis_epoch_continuation_reentry
        .prior_second_basis_epoch_reentry.loaded_root.verification.root_record_sha256
    )
    assert (
        result.fresh_reentry.prior_third_basis_epoch_reentry
        .prior_second_basis_epoch_continuation_reentry
        .prior_second_basis_epoch_reentry.prior_continuation_reentry
        .prior_root_backed_reentry.loaded_root.verification.root_record_sha256
        == current.prior_third_basis_epoch_reentry
        .prior_second_basis_epoch_continuation_reentry
        .prior_second_basis_epoch_reentry.prior_continuation_reentry
        .prior_root_backed_reentry.loaded_root.verification.root_record_sha256
    )

    decoded = load_chromium_research_third_basis_epoch_continuation_reentry_plan_document(
        next_overlay
    )
    assert decoded == result.next_plan
    roundtrip = reenter_chromium_research_third_basis_epoch_continuation(decoded)
    assert roundtrip is not result.fresh_reentry
    assert roundtrip.controller.presentation == result.fresh_reentry.controller.presentation
    _assert_three_bare_passages_survive_continuation(roundtrip)


@pytest.mark.asyncio
async def test_50u_existing_cumulative_product_promotes_above_v2_anchor_without_rewriting_launch(
    tmp_path: Path,
) -> None:
    values = _persist_bare_third_basis_continuation(
        tmp_path,
        stem="50u-ui-current",
    )
    third_overlay = values[14]
    current_overlay = values[22]
    current_checkpoint = values[23]
    earned = current_checkpoint.fresh_reentry
    lineage = prove_chromium_research_third_basis_epoch_continuation_shell_lineage(
        earned,
        overlay_source=current_overlay,
    )
    shell = create_inspectable_third_basis_epoch_continuation_research_session_shell(
        lineage
    )
    current = lineage.reentry
    successor = tmp_path / "50u-ui-successor.json"
    one_hop = tmp_path / "50u-ui-one-hop.json"
    cumulative = tmp_path / "50u-ui-cumulative.json"
    next_overlay = tmp_path / "50u-ui-next.overlay.json"

    async with shell.run_test(size=(190, 340)) as pilot:
        await pilot.pause()
        inspection = shell.third_basis_epoch_authority_inspection
        launch = inspection.launch_provenance
        assert launch.launch_location_context == current_overlay.resolve()

        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=current.controller.declared_endpoint.verification.path,
            successor=successor,
            declaration=one_hop,
            text="50U cumulative successor above v2-backed third-basis ancestry.",
        )

        rollover = shell.last_research_rollover
        one_hop_controller = shell.research_controller
        assert rollover is not None
        assert inspection.launch_provenance is launch

        for selector in (
            "#research-third-basis-epoch-cumulative-checkpoint-current-overlay-source",
            "#research-third-basis-epoch-cumulative-checkpoint-successor-source",
            "#research-third-basis-epoch-cumulative-checkpoint-declaration-destination",
            "#research-third-basis-epoch-cumulative-checkpoint-overlay-destination",
        ):
            assert shell.query_one(selector, Input).value == ""

        await _save_cumulative(
            shell,
            pilot,
            current_overlay=current_overlay,
            successor=successor,
            declaration_destination=cumulative,
            next_overlay=next_overlay,
        )

        result = shell.last_third_basis_epoch_cumulative_checkpoint
        assert result is not None
        assert result.current_reentry is current
        assert result.rollover is rollover
        assert result.next_plan.prior_third_basis_epoch_overlay_source == (
            third_overlay.resolve()
        )
        assert result.next_plan.prior_third_basis_epoch_overlay_source != (
            current_overlay.resolve()
        )
        assert shell.third_basis_epoch_continuation_launch_lineage is lineage
        assert shell.third_basis_epoch_continuation_reentry is result.fresh_reentry
        assert shell.research_controller is result.fresh_reentry.controller
        assert shell.research_controller is not one_hop_controller
        assert inspection.launch_provenance is launch
        assert launch.launch_location_context == current_overlay.resolve()
        assert inspection.current_state.state_source == "40D cumulative promotion"
        assert (
            inspection.current_state.endpoint_sha256
            == result.fresh_reentry.controller.declared_endpoint.verification.edge_record_sha256
        )

        document = json.loads(next_overlay.read_text(encoding="utf-8"))
        assert document["format"] == _CONTINUATION_OVERLAY_V1
        _assert_three_bare_passages_survive_continuation(result.fresh_reentry)


def test_50u_cli_relaunches_cumulative_40c_v1_above_v2_anchor(
    tmp_path: Path,
    monkeypatch,
) -> None:
    *_, next_overlay, _, _, result = _persist_bare_third_basis_cumulative(
        tmp_path,
        stem="50u-shell",
    )
    observed: dict[str, object] = {}

    def fail_wrong_product(*args, **kwargs):
        raise AssertionError(
            "50U cumulative relaunch must retain dedicated persisted continuation lineage"
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
                str(next_overlay),
            ]
        )
        == 0
    )

    lineage = observed["lineage"]
    assert isinstance(
        lineage,
        ChromiumResearchThirdBasisEpochContinuationShellLineage,
    )
    assert lineage.overlay_source == next_overlay.resolve()
    assert lineage.reentry is not result.fresh_reentry
    assert lineage.reentry.controller.presentation == result.fresh_reentry.controller.presentation
    assert len(lineage.reentry.plan.declared_edge_sources) == 2
    _assert_three_bare_passages_survive_continuation(lineage.reentry)


def test_50u_research_inspect_is_deterministic_for_cumulative_v1_above_v2_anchor(
    tmp_path: Path,
    capsys,
) -> None:
    *_, next_overlay, _, _, result = _persist_bare_third_basis_cumulative(
        tmp_path,
        stem="50u-inspect",
    )

    args = [
        "research-inspect",
        "--third-basis-epoch-continuation-overlay",
        str(next_overlay),
    ]
    assert cli.main(args) == 0
    first = capsys.readouterr().out
    assert cli.main(args) == 0
    second = capsys.readouterr().out
    assert first == second

    plan = load_chromium_research_third_basis_epoch_continuation_reentry_plan_document(
        next_overlay
    )
    reentry = reenter_chromium_research_third_basis_epoch_continuation(plan)
    lineage = prove_chromium_research_third_basis_epoch_continuation_shell_lineage(
        reentry,
        overlay_source=next_overlay,
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
        next_overlay.resolve()
    )
    assert report["current_governed_state"]["declared_continuation_edge_count"] == 2
    assert report["current_governed_state"]["endpoint_sha256"] == (
        result.fresh_reentry.controller.declared_endpoint.verification.edge_record_sha256
    )
    _assert_three_bare_passages_survive_continuation(lineage.reentry)


def test_50u_tampered_fixed_40b_v2_breaks_cumulative_fresh_reentry_after_config_decode(
    tmp_path: Path,
) -> None:
    values = _persist_bare_third_basis_cumulative(
        tmp_path,
        stem="50u-tamper",
    )
    third_overlay = values[24]
    next_overlay = values[32]

    decoded = load_chromium_research_third_basis_epoch_continuation_reentry_plan_document(
        next_overlay
    )
    assert decoded.prior_third_basis_epoch_overlay_source == third_overlay.resolve()

    third_overlay.write_bytes(third_overlay.read_bytes() + b"tampered")

    decoded_again = (
        load_chromium_research_third_basis_epoch_continuation_reentry_plan_document(
            next_overlay
        )
    )
    assert decoded_again == decoded

    with pytest.raises(
        ChromiumResearchThirdBasisEpochContinuationReentryError,
        match="prior 40B third-basis-epoch overlay",
    ):
        reenter_chromium_research_third_basis_epoch_continuation(decoded_again)


def test_50u_tampered_current_40c_rejects_before_cumulative_writes(
    tmp_path: Path,
) -> None:
    values = _persist_bare_third_basis_continuation(
        tmp_path,
        stem="50u-current-tamper",
    )
    current_overlay = values[22]
    current = values[23].fresh_reentry
    successor = tmp_path / "50u-current-tamper-successor.json"
    revision = current.controller.persist_declared_endpoint_revision(
        "Chosen successor must not bypass a tampered current 40C overlay.",
        prior_edge_source=current.controller.declared_endpoint.verification.path,
        destination=successor,
    )
    one_hop = tmp_path / "50u-current-tamper-one-hop.json"
    rollover = rollover_chromium_research_session_to_persisted_successor(
        current.controller,
        revision,
        successor_edge_source=successor,
        declaration_destination=one_hop,
    )
    cumulative = tmp_path / "50u-current-tamper-cumulative.json"
    next_overlay = tmp_path / "50u-current-tamper-next.overlay.json"

    current_overlay.write_bytes(current_overlay.read_bytes() + b"tampered")

    with pytest.raises(
        ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionError,
        match="current 40C overlay could not be decoded",
    ):
        persist_chromium_research_third_basis_epoch_continuation_checkpoint_extension(
            current,
            rollover,
            current_overlay_source=current_overlay,
            successor_edge_source=successor,
            cumulative_declaration_destination=cumulative,
            next_overlay_destination=next_overlay,
        )

    assert not cumulative.exists()
    assert not next_overlay.exists()
