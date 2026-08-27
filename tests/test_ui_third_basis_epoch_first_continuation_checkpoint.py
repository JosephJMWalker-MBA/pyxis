from __future__ import annotations

from pathlib import Path

import pytest
from textual.widgets import Button, Input, Static

from pyxis.app.chromium_research_third_basis_epoch_shell_lineage import (
    prove_chromium_research_third_basis_epoch_shell_lineage,
)
from pyxis.ui.chromium_research_session_restart_plan_textual import (
    ResearchSessionRestartPlanControls,
)
from pyxis.ui.chromium_research_third_basis_epoch_continuation_checkpoint_textual import (
    ThirdBasisEpochResearchSessionContinuationCheckpointControls,
)
from pyxis.ui.third_basis_epoch_research_session_shell import (
    create_third_basis_epoch_research_session_shell,
)
from test_app_chromium_research_third_basis_epoch_reentry_plan_document import (
    _persist_valid_overlay,
    _root_shas,
)
from test_ui_research_root_backed_session_continuation_checkpoint import (
    _press,
    _write_and_rollover,
)


def _shell_with_lineage(tmp_path: Path, *, stem: str):
    _, earned, overlay, _ = _persist_valid_overlay(tmp_path, stem=stem)
    lineage = prove_chromium_research_third_basis_epoch_shell_lineage(
        earned,
        overlay_source=overlay,
    )
    shell = create_third_basis_epoch_research_session_shell(lineage)
    return lineage, overlay, shell


async def _save_checkpoint(
    shell,
    pilot,
    *,
    prior_overlay: Path,
    successor: Path,
    declaration: Path,
    destination: Path,
) -> None:
    shell.query_one(
        "#research-third-basis-epoch-checkpoint-prior-overlay-source",
        Input,
    ).value = str(prior_overlay)
    shell.query_one(
        "#research-third-basis-epoch-checkpoint-successor-source",
        Input,
    ).value = str(successor)
    shell.query_one(
        "#research-third-basis-epoch-checkpoint-declaration-source",
        Input,
    ).value = str(declaration)
    shell.query_one(
        "#research-third-basis-epoch-checkpoint-destination",
        Input,
    ).value = str(destination)
    await _press(
        shell,
        pilot,
        "save-research-third-basis-epoch-continuation-checkpoint",
    )


@pytest.mark.asyncio
async def test_40b_rollover_exposes_blank_40c_checkpoint_form_and_locks_revision(
    tmp_path: Path,
) -> None:
    lineage, _, shell = _shell_with_lineage(tmp_path, stem="41c-form")
    prior = lineage.reentry
    successor = tmp_path / "successor.json"
    declaration = tmp_path / "one-hop-declaration.json"

    async with shell.run_test(size=(160, 220)) as pilot:
        await pilot.pause()
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=prior.controller.declared_endpoint.verification.path,
            successor=successor,
            declaration=declaration,
            text="First checkpoint candidate above the third root.",
        )

        controls = shell.query_one(
            "#research-third-basis-epoch-continuation-checkpoint-controls",
            ThirdBasisEpochResearchSessionContinuationCheckpointControls,
        )
        assert controls.rollover is shell.last_research_rollover
        for selector in (
            "#research-third-basis-epoch-checkpoint-prior-overlay-source",
            "#research-third-basis-epoch-checkpoint-successor-source",
            "#research-third-basis-epoch-checkpoint-declaration-source",
            "#research-third-basis-epoch-checkpoint-destination",
        ):
            assert shell.query_one(selector, Input).value == ""
        assert shell.query_one("#persist-research-endpoint-revision", Button).disabled
        assert len(shell.query(ResearchSessionRestartPlanControls)) == 0


@pytest.mark.asyncio
async def test_successful_first_40c_checkpoint_retains_exact_launch_prior_and_three_roots_and_stays_locked(
    tmp_path: Path,
) -> None:
    lineage, overlay, shell = _shell_with_lineage(tmp_path, stem="41c-success")
    prior = lineage.reentry
    successor = tmp_path / "successor.json"
    declaration = tmp_path / "one-hop-declaration.json"
    next_overlay = tmp_path / "continuation.overlay.json"

    async with shell.run_test(size=(160, 240)) as pilot:
        await pilot.pause()
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=prior.controller.declared_endpoint.verification.path,
            successor=successor,
            declaration=declaration,
            text="First checkpointed continuation above the third root.",
        )
        live_controller = shell.research_controller
        rollover = shell.last_research_rollover
        assert rollover is not None

        await _save_checkpoint(
            shell,
            pilot,
            prior_overlay=overlay,
            successor=successor,
            declaration=declaration,
            destination=next_overlay,
        )

        result = shell.last_third_basis_epoch_continuation_checkpoint
        assert result is not None
        assert result.prior_reentry is prior
        assert result.rollover is rollover
        assert shell.third_basis_epoch_launch_lineage is lineage
        assert shell.research_controller is live_controller
        assert result.fresh_reentry.controller is not live_controller
        assert result.fresh_reentry.controller.presentation == live_controller.presentation
        assert (
            result.fresh_reentry.controller.declared_endpoint.verification.edge_record_sha256
            == live_controller.declared_endpoint.verification.edge_record_sha256
        )
        assert _root_shas(result.fresh_reentry.prior_third_basis_epoch_reentry) == _root_shas(
            prior
        )
        assert len(set(_root_shas(prior))) == 3
        assert next_overlay.exists()
        assert shell.query_one("#persist-research-endpoint-revision", Button).disabled
        assert shell.query_one(
            "#save-research-third-basis-epoch-continuation-checkpoint",
            Button,
        ).disabled
        assert len(shell.query(ResearchSessionRestartPlanControls)) == 0
        assert len(shell.query("#continue-third-basis-epoch-cumulative-mode")) == 0
        status = str(
            shell.query_one("#research-third-basis-epoch-checkpoint-status", Static).content
        )
        assert "--third-basis-epoch-continuation-overlay" in status
        assert "not a global latest/current/head" in status
        assert "Retained first-root SHA-256" in status
        assert "Retained second-root SHA-256" in status
        assert "Retained third-root SHA-256" in status


@pytest.mark.parametrize(
    ("missing_field", "expected"),
    [
        ("overlay", "40B overlay path is required"),
        ("successor", "successor edge path is required"),
        ("declaration", "continuation declaration path is required"),
        ("destination", "40C overlay destination is required"),
    ],
)
@pytest.mark.asyncio
async def test_missing_explicit_40c_path_keeps_third_epoch_shell_locked(
    tmp_path: Path,
    missing_field: str,
    expected: str,
) -> None:
    lineage, overlay, shell = _shell_with_lineage(
        tmp_path,
        stem=f"41c-missing-{missing_field}",
    )
    prior = lineage.reentry
    successor = tmp_path / "successor.json"
    declaration = tmp_path / "one-hop-declaration.json"
    next_overlay = tmp_path / "continuation.overlay.json"

    async with shell.run_test(size=(160, 240)) as pilot:
        await pilot.pause()
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=prior.controller.declared_endpoint.verification.path,
            successor=successor,
            declaration=declaration,
            text="Blank third-epoch checkpoint input must fail.",
        )
        values = {
            "overlay": str(overlay),
            "successor": str(successor),
            "declaration": str(declaration),
            "destination": str(next_overlay),
        }
        values[missing_field] = ""
        shell.query_one(
            "#research-third-basis-epoch-checkpoint-prior-overlay-source",
            Input,
        ).value = values["overlay"]
        shell.query_one(
            "#research-third-basis-epoch-checkpoint-successor-source",
            Input,
        ).value = values["successor"]
        shell.query_one(
            "#research-third-basis-epoch-checkpoint-declaration-source",
            Input,
        ).value = values["declaration"]
        shell.query_one(
            "#research-third-basis-epoch-checkpoint-destination",
            Input,
        ).value = values["destination"]
        await _press(
            shell,
            pilot,
            "save-research-third-basis-epoch-continuation-checkpoint",
        )

        assert expected in str(
            shell.query_one("#research-third-basis-epoch-checkpoint-status", Static).content
        )
        assert shell.last_third_basis_epoch_continuation_checkpoint is None
        assert shell.query_one("#persist-research-endpoint-revision", Button).disabled
        assert not next_overlay.exists()


@pytest.mark.asyncio
async def test_wrong_sibling_successor_cannot_become_40c_checkpoint(
    tmp_path: Path,
) -> None:
    lineage, overlay, shell = _shell_with_lineage(tmp_path, stem="41c-wrong-successor")
    prior = lineage.reentry
    prior_controller = shell.research_controller
    successor = tmp_path / "chosen.json"
    declaration = tmp_path / "chosen-declaration.json"
    sibling = tmp_path / "sibling.json"
    next_overlay = tmp_path / "wrong.overlay.json"

    async with shell.run_test(size=(160, 240)) as pilot:
        await pilot.pause()
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=prior.controller.declared_endpoint.verification.path,
            successor=successor,
            declaration=declaration,
            text="Chosen third-epoch successor.",
        )
        prior_controller.persist_declared_endpoint_revision(
            "Different valid sibling above the same third epoch.",
            prior_edge_source=prior.controller.declared_endpoint.verification.path,
            destination=sibling,
        )
        await _save_checkpoint(
            shell,
            pilot,
            prior_overlay=overlay,
            successor=sibling,
            declaration=declaration,
            destination=next_overlay,
        )

        assert "failed" in str(
            shell.query_one("#research-third-basis-epoch-checkpoint-status", Static).content
        ).lower()
        assert shell.last_third_basis_epoch_continuation_checkpoint is None
        assert shell.query_one("#persist-research-endpoint-revision", Button).disabled
        assert not next_overlay.exists()


@pytest.mark.parametrize("root_name", ["first", "second", "third"])
@pytest.mark.asyncio
async def test_tampered_retained_root_rejects_before_40c_overlay_write(
    tmp_path: Path,
    root_name: str,
) -> None:
    lineage, overlay, shell = _shell_with_lineage(
        tmp_path,
        stem=f"41c-tamper-{root_name}",
    )
    prior = lineage.reentry
    successor = tmp_path / "successor.json"
    declaration = tmp_path / "one-hop-declaration.json"
    next_overlay = tmp_path / "continuation.overlay.json"

    async with shell.run_test(size=(160, 240)) as pilot:
        await pilot.pause()
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=prior.controller.declared_endpoint.verification.path,
            successor=successor,
            declaration=declaration,
            text=f"{root_name.title()}-root ancestry must remain fresh.",
        )
        second_epoch = (
            prior.prior_second_basis_epoch_continuation_reentry
            .prior_second_basis_epoch_reentry
        )
        paths = {
            "first": (
                second_epoch.prior_continuation_reentry.prior_root_backed_reentry
                .plan.root_source
            ),
            "second": second_epoch.plan.root_source,
            "third": prior.plan.root_source,
        }
        path = paths[root_name]
        path.write_bytes(path.read_bytes() + b"tampered")
        await _save_checkpoint(
            shell,
            pilot,
            prior_overlay=overlay,
            successor=successor,
            declaration=declaration,
            destination=next_overlay,
        )

        assert shell.last_third_basis_epoch_continuation_checkpoint is None
        assert not next_overlay.exists()
        assert shell.query_one("#persist-research-endpoint-revision", Button).disabled


@pytest.mark.asyncio
async def test_40c_destination_is_no_overwrite_and_failure_keeps_revision_locked(
    tmp_path: Path,
) -> None:
    lineage, overlay, shell = _shell_with_lineage(tmp_path, stem="41c-no-overwrite")
    prior = lineage.reentry
    successor = tmp_path / "successor.json"
    declaration = tmp_path / "one-hop-declaration.json"
    next_overlay = tmp_path / "existing.overlay.json"
    next_overlay.write_text("keep exact\n", encoding="utf-8")

    async with shell.run_test(size=(160, 240)) as pilot:
        await pilot.pause()
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=prior.controller.declared_endpoint.verification.path,
            successor=successor,
            declaration=declaration,
            text="No overwrite above the third root.",
        )
        await _save_checkpoint(
            shell,
            pilot,
            prior_overlay=overlay,
            successor=successor,
            declaration=declaration,
            destination=next_overlay,
        )

        assert next_overlay.read_text(encoding="utf-8") == "keep exact\n"
        assert shell.last_third_basis_epoch_continuation_checkpoint is None
        assert shell.query_one("#persist-research-endpoint-revision", Button).disabled


@pytest.mark.asyncio
async def test_checkpoint_accepts_explicit_path_distinct_equivalent_40b_overlay(
    tmp_path: Path,
) -> None:
    lineage, overlay, shell = _shell_with_lineage(tmp_path, stem="41c-path-distinct")
    prior = lineage.reentry
    alternate = tmp_path / "alternate-third-epoch.overlay.json"
    alternate.write_bytes(overlay.read_bytes())
    successor = tmp_path / "successor.json"
    declaration = tmp_path / "one-hop-declaration.json"
    next_overlay = tmp_path / "path-distinct-continuation.overlay.json"

    assert alternate.resolve() != lineage.overlay_source

    async with shell.run_test(size=(160, 240)) as pilot:
        await pilot.pause()
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=prior.controller.declared_endpoint.verification.path,
            successor=successor,
            declaration=declaration,
            text="Explicit path-distinct equivalent third-epoch prior remains valid.",
        )
        await _save_checkpoint(
            shell,
            pilot,
            prior_overlay=alternate,
            successor=successor,
            declaration=declaration,
            destination=next_overlay,
        )

        result = shell.last_third_basis_epoch_continuation_checkpoint
        assert result is not None
        assert result.prior_reentry is prior
        assert result.plan.prior_third_basis_epoch_overlay_source == alternate.resolve()
        assert _root_shas(result.fresh_reentry.prior_third_basis_epoch_reentry) == _root_shas(
            prior
        )
        assert next_overlay.exists()
        assert shell.query_one("#persist-research-endpoint-revision", Button).disabled
