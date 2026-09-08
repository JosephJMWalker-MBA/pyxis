from __future__ import annotations

import json
from pathlib import Path

import pytest
from textual.widgets import Button, Input

import pyxis.cli as cli
from pyxis.app.chromium_research_root_backed_session_authority_inspection import (
    inspect_chromium_research_root_backed_session_continuation_launch,
)
from pyxis.app.chromium_research_root_backed_session_authority_inspection_report import (
    serialize_chromium_research_root_backed_session_authority_inspection,
)
from pyxis.app.chromium_research_root_backed_session_continuation_checkpoint_extension import (
    persist_chromium_research_root_backed_session_continuation_checkpoint_extension,
)
from pyxis.app.chromium_research_root_backed_session_continuation_reentry_plan_document import (
    load_chromium_research_root_backed_session_continuation_reentry_plan_document,
    reenter_chromium_research_root_backed_session_continuation,
)
from pyxis.app.chromium_research_root_backed_session_shell_lineage import (
    ChromiumResearchRootBackedSessionContinuationShellLineage,
    prove_chromium_research_root_backed_session_continuation_shell_lineage,
)
from pyxis.app.chromium_research_session_rollover import (
    rollover_chromium_research_session_to_persisted_successor,
)
from pyxis.ui.root_backed_continuation_research_session_shell import (
    create_root_backed_continuation_research_session_shell,
)
from test_bare_selection_root_backed_continuation_v1 import (
    _assert_bare_member_survives,
    _persist_bare_root_continuation,
)
from test_ui_research_root_backed_session_cumulative_checkpoint import (
    _save_cumulative_checkpoint,
    _write_and_rollover,
)


_CONTINUATION_OVERLAY_V1 = (
    "pyxis.chromium.research_root_backed_session_continuation_locator_overlay.v1"
)
_ROOT_OVERLAY_V2 = (
    "pyxis.chromium.research_root_backed_session_reentry_locator_overlay.v2"
)


def _persist_bare_cumulative_extension(tmp_path: Path, *, stem: str = "50k"):
    values = _persist_bare_root_continuation(tmp_path, stem=f"{stem}-first")
    root_overlay = values[6]
    first_successor = values[9]
    first_continuation_overlay = values[13]
    first_checkpoint = values[14]
    current = first_checkpoint.fresh_reentry

    successor = tmp_path / f"{stem}-second-successor.json"
    revision = current.controller.persist_declared_endpoint_revision(
        "Second ordinary continuation above the bare-selection first-root basis.",
        prior_edge_source=current.controller.declared_endpoint.verification.path,
        destination=successor,
    )
    one_hop_declaration = tmp_path / f"{stem}-second-one-hop-declaration.json"
    rollover = rollover_chromium_research_session_to_persisted_successor(
        current.controller,
        revision,
        successor_edge_source=successor,
        declaration_destination=one_hop_declaration,
    )
    cumulative_declaration = tmp_path / f"{stem}-cumulative-declaration.json"
    next_overlay = tmp_path / f"{stem}-cumulative-overlay.json"

    prior_overlay_bytes = first_continuation_overlay.read_bytes()
    one_hop_bytes = one_hop_declaration.read_bytes()

    result = persist_chromium_research_root_backed_session_continuation_checkpoint_extension(
        current,
        rollover,
        current_overlay_source=first_continuation_overlay,
        successor_edge_source=successor,
        cumulative_declaration_destination=cumulative_declaration,
        next_overlay_destination=next_overlay,
    )
    return (
        *values,
        root_overlay,
        first_successor,
        first_continuation_overlay,
        current,
        successor,
        revision,
        one_hop_declaration,
        rollover,
        cumulative_declaration,
        next_overlay,
        prior_overlay_bytes,
        one_hop_bytes,
        result,
    )


def test_50k_35e_keeps_direct_v2_root_anchor_and_existing_continuation_v1(
    tmp_path: Path,
) -> None:
    values = _persist_bare_cumulative_extension(tmp_path)
    root_overlay = values[15]
    first_successor = values[16]
    current_overlay = values[17]
    current = values[18]
    successor = values[19]
    one_hop_declaration = values[21]
    rollover = values[22]
    cumulative_declaration = values[23]
    next_overlay = values[24]
    prior_overlay_bytes = values[25]
    one_hop_bytes = values[26]
    result = values[27]

    root_document = json.loads(root_overlay.read_text(encoding="utf-8"))
    assert root_document["format"] == _ROOT_OVERLAY_V2

    assert result.current_reentry is current
    assert result.rollover is rollover
    assert result.current_plan == current.plan
    assert result.next_plan.prior_root_backed_overlay_source == root_overlay.resolve()
    assert result.next_plan.prior_root_backed_overlay_source == (
        current.plan.prior_root_backed_overlay_source
    )
    assert result.next_plan.declared_edge_sources == (
        first_successor.resolve(),
        successor.resolve(),
    )
    assert result.next_plan.declaration_source == cumulative_declaration.resolve()
    assert len(result.explicit_sequence.edges) == 2

    document = json.loads(next_overlay.read_text(encoding="utf-8"))
    assert document["format"] == _CONTINUATION_OVERLAY_V1
    assert set(document) == {
        "format",
        "prior_root_backed_overlay_source",
        "declared_edge_sources",
        "declaration_source",
    }
    base = next_overlay.parent
    assert (
        base / document["prior_root_backed_overlay_source"]
    ).resolve() == root_overlay.resolve()
    assert (
        base / document["prior_root_backed_overlay_source"]
    ).resolve() != current_overlay.resolve()
    assert [(base / path).resolve() for path in document["declared_edge_sources"]] == [
        first_successor.resolve(),
        successor.resolve(),
    ]
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
        "root_source",
    ):
        assert forbidden not in serialized

    assert current_overlay.read_bytes() == prior_overlay_bytes
    assert one_hop_declaration.read_bytes() == one_hop_bytes
    assert result.fresh_reentry is not current
    assert (
        result.fresh_reentry.controller.presentation.sequence.members[-1]
        == rollover.continuation_controller.presentation.sequence.members[-1]
    )
    assert (
        result.fresh_reentry.controller.declared_endpoint.verification.edge_record_sha256
        == rollover.continuation_controller.declared_endpoint.verification.edge_record_sha256
    )
    _assert_bare_member_survives(result.fresh_reentry)

    decoded = load_chromium_research_root_backed_session_continuation_reentry_plan_document(
        next_overlay
    )
    fresh = reenter_chromium_research_root_backed_session_continuation(decoded)
    assert decoded == result.next_plan
    assert fresh is not result.fresh_reentry
    assert fresh.controller.presentation == result.fresh_reentry.controller.presentation
    assert fresh.plan.prior_root_backed_overlay_source == root_overlay.resolve()
    _assert_bare_member_survives(fresh)


@pytest.mark.asyncio
async def test_50k_existing_36c_shell_promotes_v2_anchored_cumulative_checkpoint(
    tmp_path: Path,
) -> None:
    values = _persist_bare_root_continuation(tmp_path, stem="50k-ui-first")
    root_overlay = values[6]
    current_overlay = values[13]
    current = values[14].fresh_reentry
    first_successor = values[9]
    shell = create_root_backed_continuation_research_session_shell(current)

    successor = tmp_path / "50k-ui-second-successor.json"
    one_hop = tmp_path / "50k-ui-second-hop.json"
    cumulative = tmp_path / "50k-ui-cumulative.json"
    next_overlay = tmp_path / "50k-ui-cumulative-overlay.json"

    async with shell.run_test(size=(190, 280)) as pilot:
        await pilot.pause()
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=current.controller.declared_endpoint.verification.path,
            successor=successor,
            declaration=one_hop,
            text="Second cumulative edge while preserving bare-selection ancestry.",
        )

        assert shell.root_backed_continuation_reentry is current
        assert shell.query_one("#persist-research-endpoint-revision", Button).disabled
        for selector in (
            "#research-root-backed-cumulative-checkpoint-current-overlay-source",
            "#research-root-backed-cumulative-checkpoint-successor-source",
            "#research-root-backed-cumulative-checkpoint-declaration-destination",
            "#research-root-backed-cumulative-checkpoint-overlay-destination",
        ):
            assert shell.query_one(selector, Input).value == ""

        one_hop_controller = shell.research_controller
        await _save_cumulative_checkpoint(
            shell,
            pilot,
            current_overlay=current_overlay,
            successor=successor,
            cumulative_declaration=cumulative,
            next_overlay=next_overlay,
        )

        result = shell.last_root_backed_cumulative_checkpoint
        assert result is not None
        assert result.current_reentry is current
        assert result.next_plan.prior_root_backed_overlay_source == root_overlay.resolve()
        assert result.next_plan.declared_edge_sources == (
            first_successor.resolve(),
            successor.resolve(),
        )
        assert shell.root_backed_continuation_reentry is result.fresh_reentry
        assert shell.research_controller is result.fresh_reentry.controller
        assert shell.research_controller is not one_hop_controller
        assert (
            shell.research_controller.declared_endpoint.verification.edge_record_sha256
            == one_hop_controller.declared_endpoint.verification.edge_record_sha256
        )
        assert len(shell.research_controller.presentation.sequence.members) == 2
        assert not shell.query_one("#persist-research-endpoint-revision", Button).disabled
        _assert_bare_member_survives(result.fresh_reentry)

        document = json.loads(next_overlay.read_text(encoding="utf-8"))
        assert document["format"] == _CONTINUATION_OVERLAY_V1
        assert (
            next_overlay.parent / document["prior_root_backed_overlay_source"]
        ).resolve() == root_overlay.resolve()
        assert (
            next_overlay.parent / document["prior_root_backed_overlay_source"]
        ).resolve() != current_overlay.resolve()


def test_50k_cli_relaunches_cumulative_overlay_above_direct_bare_v2_anchor(
    tmp_path: Path,
    monkeypatch,
) -> None:
    values = _persist_bare_cumulative_extension(tmp_path, stem="50k-cli")
    root_overlay = values[15]
    next_overlay = values[24]
    result = values[27]
    observed: dict[str, object] = {}

    def fail_controller_only(*args, **kwargs):
        raise AssertionError("50K cumulative relaunch must retain typed continuation lineage")

    def fail_root_only(*args, **kwargs):
        raise AssertionError("50K cumulative relaunch must use continuation product")

    def fake_continuation_shell(lineage) -> None:
        observed["lineage"] = lineage

    monkeypatch.setattr(
        cli,
        "_run_controller_only_research_session_shell",
        fail_controller_only,
    )
    monkeypatch.setattr(
        cli,
        "_run_root_backed_research_session_shell",
        fail_root_only,
    )
    monkeypatch.setattr(
        cli,
        "_run_root_backed_continuation_research_session_shell",
        fake_continuation_shell,
    )

    assert (
        cli.main(
            [
                "research-shell",
                "--root-backed-continuation-overlay",
                str(next_overlay),
            ]
        )
        == 0
    )

    lineage = observed["lineage"]
    assert isinstance(
        lineage,
        ChromiumResearchRootBackedSessionContinuationShellLineage,
    )
    assert lineage.overlay_source == next_overlay.resolve()
    assert lineage.reentry is not result.fresh_reentry
    assert lineage.reentry.plan.prior_root_backed_overlay_source == root_overlay.resolve()
    assert len(lineage.reentry.plan.declared_edge_sources) == 2
    assert lineage.reentry.controller.presentation == result.fresh_reentry.controller.presentation
    _assert_bare_member_survives(lineage.reentry)


def test_50k_inspection_of_cumulative_overlay_is_deterministic_and_counts_two_edges(
    tmp_path: Path,
    capsys,
) -> None:
    values = _persist_bare_cumulative_extension(tmp_path, stem="50k-inspect")
    next_overlay = values[24]
    result = values[27]

    args = [
        "research-inspect",
        "--root-backed-continuation-overlay",
        str(next_overlay),
    ]
    assert cli.main(args) == 0
    first = capsys.readouterr().out
    assert cli.main(args) == 0
    second = capsys.readouterr().out
    assert first == second

    plan = load_chromium_research_root_backed_session_continuation_reentry_plan_document(
        next_overlay
    )
    reentry = reenter_chromium_research_root_backed_session_continuation(plan)
    lineage = prove_chromium_research_root_backed_session_continuation_shell_lineage(
        reentry,
        overlay_source=next_overlay,
    )
    expected = serialize_chromium_research_root_backed_session_authority_inspection(
        inspect_chromium_research_root_backed_session_continuation_launch(lineage)
    )
    assert first == expected

    report = json.loads(first)
    assert report["report_role"] == "read_only_inspection_not_authority"
    assert report["launch_provenance"]["launch_family"] == (
        "persisted 35D/35E root-backed continuation launch"
    )
    assert report["launch_provenance"]["launch_location_context_only"] == str(
        next_overlay.resolve()
    )
    assert report["current_governed_state"]["declared_continuation_edge_count"] == 2
    assert report["current_governed_state"]["endpoint_sha256"] == (
        result.fresh_reentry.controller.declared_endpoint.verification.edge_record_sha256
    )
    _assert_bare_member_survives(lineage.reentry)
