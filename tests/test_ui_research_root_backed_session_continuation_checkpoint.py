from __future__ import annotations

from pathlib import Path

import pytest
from textual.widgets import Button, Input, Static, TextArea

from pyxis.app.chromium_research_root_backed_session_reentry import (
    reenter_chromium_research_root_backed_session,
)
from pyxis.app.chromium_research_root_backed_session_reentry_plan_document import (
    load_chromium_research_root_backed_session_reentry_plan_document,
)
from pyxis.ui.chromium_research_root_backed_session_continuation_checkpoint_textual import (
    RootBackedResearchSessionContinuationCheckpointControls,
)
from pyxis.ui.chromium_research_session_restart_plan_textual import (
    ResearchSessionRestartPlanControls,
)
from pyxis.ui.root_backed_research_session_shell import (
    RootBackedResearchSessionShell,
    create_root_backed_research_session_shell,
)
from test_app_chromium_research_root_backed_session_reentry_plan_document import (
    _persist_valid_overlay,
)


async def _press(shell, pilot, button_id: str) -> None:
    button = shell.query_one(f"#{button_id}", Button)
    button.focus()
    await pilot.pause()
    await pilot.press("enter")
    await pilot.pause()


def _shell_with_root_backed_reentry(tmp_path: Path, *, stem: str = "36b"):
    _, _, _, _, root_overlay, _ = _persist_valid_overlay(tmp_path, stem=stem)
    plan = load_chromium_research_root_backed_session_reentry_plan_document(root_overlay)
    reentry = reenter_chromium_research_root_backed_session(plan)
    shell = create_root_backed_research_session_shell(reentry)
    return reentry, root_overlay, shell


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


async def _save_root_backed_checkpoint(
    shell,
    pilot,
    *,
    prior_overlay: Path,
    successor: Path,
    declaration: Path,
    destination: Path,
) -> None:
    shell.query_one(
        "#research-root-backed-checkpoint-prior-overlay-source",
        Input,
    ).value = str(prior_overlay)
    shell.query_one(
        "#research-root-backed-checkpoint-successor-source",
        Input,
    ).value = str(successor)
    shell.query_one(
        "#research-root-backed-checkpoint-declaration-source",
        Input,
    ).value = str(declaration)
    shell.query_one(
        "#research-root-backed-checkpoint-destination",
        Input,
    ).value = str(destination)
    await _press(shell, pilot, "save-research-root-backed-continuation-checkpoint")


@pytest.mark.asyncio
async def test_root_backed_shell_retains_exact_35b_lineage_without_ordinary_restart_authority(
    tmp_path: Path,
) -> None:
    reentry, _, shell = _shell_with_root_backed_reentry(tmp_path)

    async with shell.run_test(size=(160, 130)) as pilot:
        await pilot.pause()
        assert isinstance(shell, RootBackedResearchSessionShell)
        assert shell.root_backed_reentry is reentry
        assert shell.research_reentry is None
        assert shell.research_controller is reentry.controller
        assert len(shell.query(RootBackedResearchSessionContinuationCheckpointControls)) == 0
        assert len(shell.query(ResearchSessionRestartPlanControls)) == 0
        assert not shell.query_one("#persist-research-endpoint-revision", Button).disabled


@pytest.mark.asyncio
async def test_first_rollover_mounts_blank_35d_checkpoint_and_locks_revision(
    tmp_path: Path,
) -> None:
    reentry, _, shell = _shell_with_root_backed_reentry(tmp_path)
    successor = tmp_path / "successor.json"
    declaration = tmp_path / "one-hop-declaration.json"

    async with shell.run_test(size=(160, 180)) as pilot:
        await pilot.pause()
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=reentry.controller.declared_endpoint.verification.path,
            successor=successor,
            declaration=declaration,
            text="First post-root continuation.",
        )

        controls = shell.query_one(
            RootBackedResearchSessionContinuationCheckpointControls
        )
        assert controls.rollover is shell.last_research_rollover
        assert shell.last_root_backed_continuation_checkpoint is None
        assert shell.query_one("#persist-research-endpoint-revision", Button).disabled
        assert len(shell.query(ResearchSessionRestartPlanControls)) == 0
        for selector in (
            "#research-root-backed-checkpoint-prior-overlay-source",
            "#research-root-backed-checkpoint-successor-source",
            "#research-root-backed-checkpoint-declaration-source",
            "#research-root-backed-checkpoint-destination",
        ):
            assert shell.query_one(selector, Input).value == ""
        assert "not yet checkpointed" in str(
            shell.query_one("#research-root-backed-checkpoint-candidate", Static).content
        )


@pytest.mark.asyncio
async def test_successful_35d_save_retains_live_controller_and_requires_explicit_relaunch(
    tmp_path: Path,
) -> None:
    prior, root_overlay, shell = _shell_with_root_backed_reentry(tmp_path)
    successor = tmp_path / "successor.json"
    declaration = tmp_path / "one-hop-declaration.json"
    next_overlay = tmp_path / "continuation.overlay.json"

    async with shell.run_test(size=(160, 210)) as pilot:
        await pilot.pause()
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=prior.controller.declared_endpoint.verification.path,
            successor=successor,
            declaration=declaration,
            text="Checkpoint me, but do not promote mode.",
        )
        live_controller = shell.research_controller
        await _save_root_backed_checkpoint(
            shell,
            pilot,
            prior_overlay=root_overlay,
            successor=successor,
            declaration=declaration,
            destination=next_overlay,
        )

        result = shell.last_root_backed_continuation_checkpoint
        assert result is not None
        assert result.prior_reentry is prior
        assert result.rollover is shell.last_research_rollover
        assert shell.root_backed_reentry is prior
        assert shell.research_controller is live_controller
        assert result.fresh_reentry.controller is not live_controller
        assert result.fresh_reentry.controller.presentation == live_controller.presentation
        assert next_overlay.exists()
        assert shell.query_one("#persist-research-endpoint-revision", Button).disabled
        assert shell.query_one(
            "#save-research-root-backed-continuation-checkpoint",
            Button,
        ).disabled
        status = str(
            shell.query_one("#research-root-backed-checkpoint-status", Static).content
        )
        assert "--root-backed-continuation-overlay" in status
        assert "not a global latest/current/head" in status


@pytest.mark.parametrize(
    ("missing_field", "expected"),
    [
        ("overlay", "35C overlay path is required"),
        ("successor", "successor edge path is required"),
        ("declaration", "continuation declaration path is required"),
        ("destination", "35D overlay destination is required"),
    ],
)
@pytest.mark.asyncio
async def test_missing_explicit_35d_path_keeps_root_backed_shell_locked(
    tmp_path: Path,
    missing_field: str,
    expected: str,
) -> None:
    prior, root_overlay, shell = _shell_with_root_backed_reentry(tmp_path)
    successor = tmp_path / "successor.json"
    declaration = tmp_path / "one-hop-declaration.json"
    next_overlay = tmp_path / "continuation.overlay.json"

    async with shell.run_test(size=(160, 210)) as pilot:
        await pilot.pause()
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=prior.controller.declared_endpoint.verification.path,
            successor=successor,
            declaration=declaration,
            text="Missing explicit location must fail.",
        )
        values = {
            "overlay": str(root_overlay),
            "successor": str(successor),
            "declaration": str(declaration),
            "destination": str(next_overlay),
        }
        values[missing_field] = ""
        shell.query_one(
            "#research-root-backed-checkpoint-prior-overlay-source",
            Input,
        ).value = values["overlay"]
        shell.query_one(
            "#research-root-backed-checkpoint-successor-source",
            Input,
        ).value = values["successor"]
        shell.query_one(
            "#research-root-backed-checkpoint-declaration-source",
            Input,
        ).value = values["declaration"]
        shell.query_one(
            "#research-root-backed-checkpoint-destination",
            Input,
        ).value = values["destination"]
        await _press(shell, pilot, "save-research-root-backed-continuation-checkpoint")

        assert expected in str(
            shell.query_one("#research-root-backed-checkpoint-status", Static).content
        )
        assert shell.last_root_backed_continuation_checkpoint is None
        assert shell.query_one("#persist-research-endpoint-revision", Button).disabled
        assert not next_overlay.exists()


@pytest.mark.asyncio
async def test_wrong_sibling_successor_cannot_become_root_backed_checkpoint(
    tmp_path: Path,
) -> None:
    prior, root_overlay, shell = _shell_with_root_backed_reentry(tmp_path)
    prior_controller = shell.research_controller
    successor = tmp_path / "chosen.json"
    declaration = tmp_path / "chosen-declaration.json"
    sibling = tmp_path / "sibling.json"
    next_overlay = tmp_path / "wrong.overlay.json"

    async with shell.run_test(size=(160, 210)) as pilot:
        await pilot.pause()
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=prior.controller.declared_endpoint.verification.path,
            successor=successor,
            declaration=declaration,
            text="Chosen post-root successor.",
        )
        prior_controller.persist_declared_endpoint_revision(
            "Different valid sibling.",
            prior_edge_source=prior.controller.declared_endpoint.verification.path,
            destination=sibling,
        )
        await _save_root_backed_checkpoint(
            shell,
            pilot,
            prior_overlay=root_overlay,
            successor=sibling,
            declaration=declaration,
            destination=next_overlay,
        )

        assert "failed" in str(
            shell.query_one("#research-root-backed-checkpoint-status", Static).content
        ).lower()
        assert shell.last_root_backed_continuation_checkpoint is None
        assert shell.query_one("#persist-research-endpoint-revision", Button).disabled
        assert not next_overlay.exists()


@pytest.mark.asyncio
async def test_tampered_explicit_35c_ancestry_rejects_before_overlay_write(
    tmp_path: Path,
) -> None:
    prior, root_overlay, shell = _shell_with_root_backed_reentry(tmp_path)
    successor = tmp_path / "successor.json"
    declaration = tmp_path / "one-hop-declaration.json"
    next_overlay = tmp_path / "continuation.overlay.json"

    async with shell.run_test(size=(160, 210)) as pilot:
        await pilot.pause()
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=prior.controller.declared_endpoint.verification.path,
            successor=successor,
            declaration=declaration,
            text="Ancestry must be fresh at checkpoint.",
        )
        prior.plan.root_source.write_bytes(prior.plan.root_source.read_bytes() + b"tampered")
        await _save_root_backed_checkpoint(
            shell,
            pilot,
            prior_overlay=root_overlay,
            successor=successor,
            declaration=declaration,
            destination=next_overlay,
        )

        assert "failed" in str(
            shell.query_one("#research-root-backed-checkpoint-status", Static).content
        ).lower()
        assert shell.last_root_backed_continuation_checkpoint is None
        assert not next_overlay.exists()
        assert shell.query_one("#persist-research-endpoint-revision", Button).disabled


@pytest.mark.asyncio
async def test_35d_destination_is_no_overwrite_and_failure_keeps_revision_locked(
    tmp_path: Path,
) -> None:
    prior, root_overlay, shell = _shell_with_root_backed_reentry(tmp_path)
    successor = tmp_path / "successor.json"
    declaration = tmp_path / "one-hop-declaration.json"
    next_overlay = tmp_path / "existing.overlay.json"
    next_overlay.write_text("keep exact\n", encoding="utf-8")

    async with shell.run_test(size=(160, 210)) as pilot:
        await pilot.pause()
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=prior.controller.declared_endpoint.verification.path,
            successor=successor,
            declaration=declaration,
            text="No overwrite.",
        )
        await _save_root_backed_checkpoint(
            shell,
            pilot,
            prior_overlay=root_overlay,
            successor=successor,
            declaration=declaration,
            destination=next_overlay,
        )

        assert next_overlay.read_text(encoding="utf-8") == "keep exact\n"
        assert shell.last_root_backed_continuation_checkpoint is None
        assert shell.query_one("#persist-research-endpoint-revision", Button).disabled


@pytest.mark.asyncio
async def test_checkpoint_accepts_explicit_moved_current_locations_without_path_inference(
    tmp_path: Path,
) -> None:
    prior, root_overlay, shell = _shell_with_root_backed_reentry(tmp_path)
    successor = tmp_path / "successor.json"
    declaration = tmp_path / "one-hop-declaration.json"
    next_overlay = tmp_path / "continuation.overlay.json"

    async with shell.run_test(size=(160, 210)) as pilot:
        await pilot.pause()
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=prior.controller.declared_endpoint.verification.path,
            successor=successor,
            declaration=declaration,
            text="Moved locations remain explicit.",
        )
        moved_root_overlay = root_overlay.rename(tmp_path / "moved-root.overlay.json")
        moved_successor = successor.rename(tmp_path / "moved-successor.json")
        moved_declaration = declaration.rename(tmp_path / "moved-declaration.json")
        await _save_root_backed_checkpoint(
            shell,
            pilot,
            prior_overlay=moved_root_overlay,
            successor=moved_successor,
            declaration=moved_declaration,
            destination=next_overlay,
        )

        result = shell.last_root_backed_continuation_checkpoint
        assert result is not None
        assert result.plan.prior_root_backed_overlay_source == moved_root_overlay.resolve()
        assert result.plan.declared_edge_sources == (moved_successor.resolve(),)
        assert result.plan.declaration_source == moved_declaration.resolve()
        assert next_overlay.exists()
        assert shell.query_one("#persist-research-endpoint-revision", Button).disabled


def test_root_backed_shell_rejects_non_35b_lineage_before_mount() -> None:
    with pytest.raises(TypeError, match="ChromiumResearchRootBackedSessionReentryResult"):
        create_root_backed_research_session_shell(object())  # type: ignore[arg-type]
