from __future__ import annotations

import json
from pathlib import Path

import pytest
from textual.widgets import Button, Input, Static, TextArea

from pyxis.app.chromium_research_root_backed_session_continuation_reentry_plan_document import (
    load_chromium_research_root_backed_session_continuation_reentry_plan_document,
    reenter_chromium_research_root_backed_session_continuation,
)
from pyxis.ui.chromium_research_root_backed_session_continuation_checkpoint_extension_textual import (
    RootBackedResearchSessionCumulativeCheckpointControls,
)
from pyxis.ui.chromium_research_root_backed_session_continuation_checkpoint_textual import (
    RootBackedResearchSessionContinuationCheckpointControls,
)
from pyxis.ui.chromium_research_session_restart_plan_textual import (
    ResearchSessionRestartPlanControls,
)
from pyxis.ui.root_backed_continuation_research_session_shell import (
    RootBackedContinuationResearchSessionShell,
    create_root_backed_continuation_research_session_shell,
)
from test_app_chromium_research_root_backed_session_continuation_reentry_plan_document import (
    _persist_valid_continuation,
)


async def _press(shell, pilot, button_id: str) -> None:
    button = shell.query_one(f"#{button_id}", Button)
    button.focus()
    await pilot.pause()
    await pilot.press("enter")
    await pilot.pause()


def _shell_with_continuation_reentry(tmp_path: Path, *, stem: str = "36c"):
    *_, overlay, _ = _persist_valid_continuation(tmp_path, stem=stem)
    plan = load_chromium_research_root_backed_session_continuation_reentry_plan_document(
        overlay
    )
    reentry = reenter_chromium_research_root_backed_session_continuation(plan)
    shell = create_root_backed_continuation_research_session_shell(reentry)
    return reentry, overlay, shell


async def _write_and_rollover(
    shell,
    pilot,
    *,
    prior_edge: Path,
    successor: Path,
    declaration: Path,
    text: str,
) -> None:
    shell.query_one("#research-endpoint-revised-note", TextArea).text = text
    shell.query_one("#research-endpoint-prior-edge-source", Input).value = str(prior_edge)
    shell.query_one("#research-endpoint-destination", Input).value = str(successor)
    await _press(shell, pilot, "persist-research-endpoint-revision")
    shell.query_one("#research-session-rollover-successor-source", Input).value = str(successor)
    shell.query_one(
        "#research-session-rollover-declaration-destination",
        Input,
    ).value = str(declaration)
    await _press(shell, pilot, "rollover-research-session")


async def _save_cumulative_checkpoint(
    shell,
    pilot,
    *,
    current_overlay: Path,
    successor: Path,
    cumulative_declaration: Path,
    next_overlay: Path,
) -> None:
    shell.query_one(
        "#research-root-backed-cumulative-checkpoint-current-overlay-source",
        Input,
    ).value = str(current_overlay)
    shell.query_one(
        "#research-root-backed-cumulative-checkpoint-successor-source",
        Input,
    ).value = str(successor)
    shell.query_one(
        "#research-root-backed-cumulative-checkpoint-declaration-destination",
        Input,
    ).value = str(cumulative_declaration)
    shell.query_one(
        "#research-root-backed-cumulative-checkpoint-overlay-destination",
        Input,
    ).value = str(next_overlay)
    await _press(shell, pilot, "save-research-root-backed-cumulative-checkpoint")


@pytest.mark.asyncio
async def test_persisted_continuation_shell_starts_unlocked_with_exact_typed_lineage(
    tmp_path: Path,
) -> None:
    reentry, _, shell = _shell_with_continuation_reentry(tmp_path)

    async with shell.run_test(size=(165, 140)) as pilot:
        await pilot.pause()
        assert isinstance(shell, RootBackedContinuationResearchSessionShell)
        assert shell.root_backed_continuation_reentry is reentry
        assert shell.research_controller is reentry.controller
        assert shell.research_reentry is None
        assert len(shell.query(RootBackedResearchSessionCumulativeCheckpointControls)) == 0
        assert len(shell.query(RootBackedResearchSessionContinuationCheckpointControls)) == 0
        assert len(shell.query(ResearchSessionRestartPlanControls)) == 0
        assert not shell.query_one("#persist-research-endpoint-revision", Button).disabled


@pytest.mark.asyncio
async def test_rollover_mounts_blank_cumulative_checkpoint_and_locks_revision(
    tmp_path: Path,
) -> None:
    reentry, _, shell = _shell_with_continuation_reentry(tmp_path)
    successor = tmp_path / "next-edge.json"
    one_hop_declaration = tmp_path / "one-hop.json"

    async with shell.run_test(size=(165, 190)) as pilot:
        await pilot.pause()
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=reentry.controller.declared_endpoint.verification.path,
            successor=successor,
            declaration=one_hop_declaration,
            text="Second post-root edge.",
        )

        controls = shell.query_one(RootBackedResearchSessionCumulativeCheckpointControls)
        assert controls.current_reentry is reentry
        assert controls.rollover is shell.last_research_rollover
        assert shell.root_backed_continuation_reentry is reentry
        assert shell.query_one("#persist-research-endpoint-revision", Button).disabled
        assert len(shell.query(ResearchSessionRestartPlanControls)) == 0
        for selector in (
            "#research-root-backed-cumulative-checkpoint-current-overlay-source",
            "#research-root-backed-cumulative-checkpoint-successor-source",
            "#research-root-backed-cumulative-checkpoint-declaration-destination",
            "#research-root-backed-cumulative-checkpoint-overlay-destination",
        ):
            assert shell.query_one(selector, Input).value == ""


@pytest.mark.asyncio
async def test_successful_35e_checkpoint_promotes_visible_shell_to_fresh_cumulative_controller(
    tmp_path: Path,
) -> None:
    current, current_overlay, shell = _shell_with_continuation_reentry(tmp_path)
    successor = tmp_path / "next-edge.json"
    one_hop_declaration = tmp_path / "one-hop.json"
    cumulative_declaration = tmp_path / "cumulative.json"
    next_overlay = tmp_path / "next.overlay.json"

    async with shell.run_test(size=(165, 220)) as pilot:
        await pilot.pause()
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=current.controller.declared_endpoint.verification.path,
            successor=successor,
            declaration=one_hop_declaration,
            text="Promote this terminal edge into cumulative context.",
        )
        one_hop_controller = shell.research_controller
        one_hop_members = len(one_hop_controller.presentation.sequence.members)
        assert one_hop_members == 1

        await _save_cumulative_checkpoint(
            shell,
            pilot,
            current_overlay=current_overlay,
            successor=successor,
            cumulative_declaration=cumulative_declaration,
            next_overlay=next_overlay,
        )

        result = shell.last_root_backed_cumulative_checkpoint
        assert result is not None
        assert result.current_reentry is current
        assert shell.root_backed_continuation_reentry is result.fresh_reentry
        assert shell.research_controller is result.fresh_reentry.controller
        assert shell.research_controller is not one_hop_controller
        assert len(shell.research_controller.presentation.sequence.members) == (
            len(current.plan.declared_edge_sources) + 1
        )
        assert len(shell.research_controller.presentation.sequence.members) > one_hop_members
        assert (
            shell.research_controller.declared_endpoint.verification.edge_record_sha256
            == one_hop_controller.declared_endpoint.verification.edge_record_sha256
        )
        assert shell.last_research_rollover is None
        assert len(shell.query(RootBackedResearchSessionCumulativeCheckpointControls)) == 0
        assert not shell.query_one("#persist-research-endpoint-revision", Button).disabled
        receipt = str(
            shell.query_one(
                "#research-root-backed-cumulative-checkpoint-success-receipt",
                Static,
            ).content
        )
        assert "not a global latest/current/head" in receipt
        assert next_overlay.exists()
        assert cumulative_declaration.exists()


@pytest.mark.asyncio
async def test_two_cumulative_checkpoint_cycles_grow_same_direct_35c_anchored_sequence(
    tmp_path: Path,
) -> None:
    initial, current_overlay, shell = _shell_with_continuation_reentry(tmp_path)
    edge2 = tmp_path / "edge2.json"
    hop2 = tmp_path / "hop2.json"
    cumulative2 = tmp_path / "cumulative2.json"
    overlay2 = tmp_path / "overlay2.json"
    edge3 = tmp_path / "edge3.json"
    hop3 = tmp_path / "hop3.json"
    cumulative3 = tmp_path / "cumulative3.json"
    overlay3 = tmp_path / "overlay3.json"

    async with shell.run_test(size=(170, 240)) as pilot:
        await pilot.pause()
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=initial.controller.declared_endpoint.verification.path,
            successor=edge2,
            declaration=hop2,
            text="Cumulative cycle two.",
        )
        await _save_cumulative_checkpoint(
            shell,
            pilot,
            current_overlay=current_overlay,
            successor=edge2,
            cumulative_declaration=cumulative2,
            next_overlay=overlay2,
        )
        first = shell.last_root_backed_cumulative_checkpoint
        assert first is not None
        first_reentry = shell.root_backed_continuation_reentry
        first_anchor = first_reentry.plan.prior_root_backed_overlay_source
        assert len(first_reentry.plan.declared_edge_sources) == 2

        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=first_reentry.controller.declared_endpoint.verification.path,
            successor=edge3,
            declaration=hop3,
            text="Cumulative cycle three.",
        )
        controls = shell.query_one(RootBackedResearchSessionCumulativeCheckpointControls)
        assert controls.current_reentry is first_reentry
        for selector in (
            "#research-root-backed-cumulative-checkpoint-current-overlay-source",
            "#research-root-backed-cumulative-checkpoint-successor-source",
            "#research-root-backed-cumulative-checkpoint-declaration-destination",
            "#research-root-backed-cumulative-checkpoint-overlay-destination",
        ):
            assert shell.query_one(selector, Input).value == ""

        await _save_cumulative_checkpoint(
            shell,
            pilot,
            current_overlay=overlay2,
            successor=edge3,
            cumulative_declaration=cumulative3,
            next_overlay=overlay3,
        )
        second = shell.last_root_backed_cumulative_checkpoint
        assert second is not None
        second_reentry = shell.root_backed_continuation_reentry
        assert second_reentry is second.fresh_reentry
        assert second_reentry.plan.prior_root_backed_overlay_source == first_anchor
        assert len(second_reentry.plan.declared_edge_sources) == 3
        assert second_reentry.plan.declared_edge_sources == (
            *first_reentry.plan.declared_edge_sources,
            edge3.resolve(),
        )
        assert not shell.query_one("#persist-research-endpoint-revision", Button).disabled

        document = json.loads(overlay3.read_text(encoding="utf-8"))
        assert Path(document["prior_root_backed_overlay_source"]).name == Path(first_anchor).name
        assert Path(document["prior_root_backed_overlay_source"]).name != overlay2.name
        assert len(document["declared_edge_sources"]) == 3


@pytest.mark.parametrize(
    ("missing_field", "expected"),
    [
        ("overlay", "35D/35E overlay path is required"),
        ("successor", "successor edge path is required"),
        ("declaration", "cumulative declaration destination is required"),
        ("next_overlay", "next overlay destination is required"),
    ],
)
@pytest.mark.asyncio
async def test_missing_cumulative_checkpoint_path_keeps_one_hop_shell_locked(
    tmp_path: Path,
    missing_field: str,
    expected: str,
) -> None:
    current, current_overlay, shell = _shell_with_continuation_reentry(tmp_path)
    successor = tmp_path / "next.json"
    one_hop = tmp_path / "hop.json"
    cumulative = tmp_path / "cumulative.json"
    next_overlay = tmp_path / "next.overlay.json"

    async with shell.run_test(size=(165, 220)) as pilot:
        await pilot.pause()
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=current.controller.declared_endpoint.verification.path,
            successor=successor,
            declaration=one_hop,
            text="Missing cumulative field.",
        )
        values = {
            "overlay": str(current_overlay),
            "successor": str(successor),
            "declaration": str(cumulative),
            "next_overlay": str(next_overlay),
        }
        values[missing_field] = ""
        shell.query_one(
            "#research-root-backed-cumulative-checkpoint-current-overlay-source",
            Input,
        ).value = values["overlay"]
        shell.query_one(
            "#research-root-backed-cumulative-checkpoint-successor-source",
            Input,
        ).value = values["successor"]
        shell.query_one(
            "#research-root-backed-cumulative-checkpoint-declaration-destination",
            Input,
        ).value = values["declaration"]
        shell.query_one(
            "#research-root-backed-cumulative-checkpoint-overlay-destination",
            Input,
        ).value = values["next_overlay"]
        await _press(shell, pilot, "save-research-root-backed-cumulative-checkpoint")

        assert expected in str(
            shell.query_one(
                "#research-root-backed-cumulative-checkpoint-status",
                Static,
            ).content
        )
        assert shell.root_backed_continuation_reentry is current
        assert shell.last_root_backed_cumulative_checkpoint is None
        assert shell.query_one("#persist-research-endpoint-revision", Button).disabled
        assert not cumulative.exists()
        assert not next_overlay.exists()


@pytest.mark.asyncio
async def test_wrong_sibling_successor_cannot_advance_cumulative_lineage(
    tmp_path: Path,
) -> None:
    current, current_overlay, shell = _shell_with_continuation_reentry(tmp_path)
    prior_controller = shell.research_controller
    successor = tmp_path / "chosen.json"
    sibling = tmp_path / "sibling.json"
    one_hop = tmp_path / "hop.json"
    cumulative = tmp_path / "cumulative.json"
    next_overlay = tmp_path / "next.overlay.json"

    async with shell.run_test(size=(165, 220)) as pilot:
        await pilot.pause()
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=current.controller.declared_endpoint.verification.path,
            successor=successor,
            declaration=one_hop,
            text="Chosen cumulative successor.",
        )
        prior_controller.persist_declared_endpoint_revision(
            "Different sibling.",
            prior_edge_source=current.controller.declared_endpoint.verification.path,
            destination=sibling,
        )
        await _save_cumulative_checkpoint(
            shell,
            pilot,
            current_overlay=current_overlay,
            successor=sibling,
            cumulative_declaration=cumulative,
            next_overlay=next_overlay,
        )

        assert "failed" in str(
            shell.query_one(
                "#research-root-backed-cumulative-checkpoint-status",
                Static,
            ).content
        ).lower()
        assert shell.root_backed_continuation_reentry is current
        assert shell.last_root_backed_cumulative_checkpoint is None
        assert shell.query_one("#persist-research-endpoint-revision", Button).disabled
        assert not cumulative.exists()
        assert not next_overlay.exists()


@pytest.mark.asyncio
async def test_tampered_current_overlay_rejects_without_visible_promotion(
    tmp_path: Path,
) -> None:
    current, current_overlay, shell = _shell_with_continuation_reentry(tmp_path)
    successor = tmp_path / "next.json"
    one_hop = tmp_path / "hop.json"
    cumulative = tmp_path / "cumulative.json"
    next_overlay = tmp_path / "next.overlay.json"

    async with shell.run_test(size=(165, 220)) as pilot:
        await pilot.pause()
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=current.controller.declared_endpoint.verification.path,
            successor=successor,
            declaration=one_hop,
            text="Tampered overlay must fail.",
        )
        one_hop_controller = shell.research_controller
        current_overlay.write_text("{}\n", encoding="utf-8")
        await _save_cumulative_checkpoint(
            shell,
            pilot,
            current_overlay=current_overlay,
            successor=successor,
            cumulative_declaration=cumulative,
            next_overlay=next_overlay,
        )

        assert shell.root_backed_continuation_reentry is current
        assert shell.research_controller is one_hop_controller
        assert shell.last_root_backed_cumulative_checkpoint is None
        assert shell.query_one("#persist-research-endpoint-revision", Button).disabled
        assert not cumulative.exists()
        assert not next_overlay.exists()


@pytest.mark.asyncio
async def test_cumulative_destinations_must_be_distinct_and_no_overwrite_preflighted(
    tmp_path: Path,
) -> None:
    current, current_overlay, shell = _shell_with_continuation_reentry(tmp_path)
    successor = tmp_path / "next.json"
    one_hop = tmp_path / "hop.json"
    collision = tmp_path / "collision.json"

    async with shell.run_test(size=(165, 220)) as pilot:
        await pilot.pause()
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=current.controller.declared_endpoint.verification.path,
            successor=successor,
            declaration=one_hop,
            text="Destination collision.",
        )
        await _save_cumulative_checkpoint(
            shell,
            pilot,
            current_overlay=current_overlay,
            successor=successor,
            cumulative_declaration=collision,
            next_overlay=collision,
        )

        assert not collision.exists()
        assert shell.last_root_backed_cumulative_checkpoint is None
        assert shell.query_one("#persist-research-endpoint-revision", Button).disabled


@pytest.mark.asyncio
async def test_existing_next_overlay_prevents_cumulative_declaration_write(
    tmp_path: Path,
) -> None:
    current, current_overlay, shell = _shell_with_continuation_reentry(tmp_path)
    successor = tmp_path / "next.json"
    one_hop = tmp_path / "hop.json"
    cumulative = tmp_path / "cumulative.json"
    next_overlay = tmp_path / "existing.overlay.json"
    next_overlay.write_text("keep exact\n", encoding="utf-8")

    async with shell.run_test(size=(165, 220)) as pilot:
        await pilot.pause()
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=current.controller.declared_endpoint.verification.path,
            successor=successor,
            declaration=one_hop,
            text="Preflight both destinations.",
        )
        await _save_cumulative_checkpoint(
            shell,
            pilot,
            current_overlay=current_overlay,
            successor=successor,
            cumulative_declaration=cumulative,
            next_overlay=next_overlay,
        )

        assert next_overlay.read_text(encoding="utf-8") == "keep exact\n"
        assert not cumulative.exists()
        assert shell.last_root_backed_cumulative_checkpoint is None
        assert shell.query_one("#persist-research-endpoint-revision", Button).disabled


@pytest.mark.asyncio
async def test_explicit_moved_current_overlay_and_successor_locations_can_checkpoint(
    tmp_path: Path,
) -> None:
    current, current_overlay, shell = _shell_with_continuation_reentry(tmp_path)
    successor = tmp_path / "next.json"
    one_hop = tmp_path / "hop.json"
    cumulative = tmp_path / "cumulative.json"
    next_overlay = tmp_path / "next.overlay.json"

    async with shell.run_test(size=(165, 220)) as pilot:
        await pilot.pause()
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=current.controller.declared_endpoint.verification.path,
            successor=successor,
            declaration=one_hop,
            text="Moved current locations remain caller-owned.",
        )
        moved_overlay = current_overlay.rename(tmp_path / "moved-current.overlay.json")
        moved_successor = successor.rename(tmp_path / "moved-successor.json")
        await _save_cumulative_checkpoint(
            shell,
            pilot,
            current_overlay=moved_overlay,
            successor=moved_successor,
            cumulative_declaration=cumulative,
            next_overlay=next_overlay,
        )

        result = shell.last_root_backed_cumulative_checkpoint
        assert result is not None
        assert result.current_plan == current.plan
        assert result.next_plan.declared_edge_sources[-1] == moved_successor.resolve()
        assert shell.root_backed_continuation_reentry is result.fresh_reentry
        assert not shell.query_one("#persist-research-endpoint-revision", Button).disabled


def test_cumulative_shell_rejects_non_continuation_lineage_before_mount() -> None:
    with pytest.raises(
        TypeError,
        match="ChromiumResearchRootBackedSessionContinuationReentryResult",
    ):
        create_root_backed_continuation_research_session_shell(object())  # type: ignore[arg-type]
