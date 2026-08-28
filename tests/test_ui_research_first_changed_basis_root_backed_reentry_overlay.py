from __future__ import annotations

from pathlib import Path

import pytest
from textual.widgets import Button, Input, Static, TextArea

from pyxis.app.chromium_research_root_backed_session_reentry_plan_document import (
    load_chromium_research_root_backed_session_reentry_plan_document,
)
from pyxis.app.chromium_research_session_reentry_plan_document import (
    persist_chromium_research_session_reentry_plan_document,
)
from pyxis.ui import (
    FirstChangedBasisRootBackedReentryOverlayResearchSessionShell,
    create_first_changed_basis_root_backed_reentry_overlay_research_session_shell,
    create_first_changed_basis_root_backed_reentry_research_session_shell,
)
from pyxis.ui.chromium_research_first_changed_basis_root_backed_reentry_overlay_textual import (
    ResearchFirstChangedBasisRootBackedReentryOverlayControls,
)
from test_app_chromium_research_session_working_set_extension import (
    _new_paragraph_member,
    _session,
)
from test_ui_research_first_changed_basis_root_backed_reentry import (
    _adopt_44e,
    _fill_44f_paragraph_inputs,
)
from test_ui_research_first_changed_basis_session_adoption import _build_44d_ui
from test_ui_research_first_changed_basis_transition import _press


async def _build_44f_ui(shell, pilot, fixture, member, tmp_path: Path, *, stem: str):
    prepared, root, edge, edge_path = await _build_44d_ui(
        shell,
        pilot,
        fixture,
        tmp_path,
        stem=stem,
    )
    transition = shell.last_first_changed_basis_transition
    assert transition is not None
    adoption, declaration = await _adopt_44e(
        shell,
        pilot,
        edge_path,
        tmp_path,
        stem=stem,
    )
    _fill_44f_paragraph_inputs(
        shell,
        member=member,
        prepared=prepared,
        transition_path=transition.persistence.path,
        root_path=root.persistence.path,
        edge_path=edge_path,
        declaration_path=declaration,
    )
    await _press(shell, pilot, "verify-research-first-changed-basis-root-backed-reentry")
    verification = shell.last_first_changed_basis_root_backed_reentry_verification
    assert verification is not None
    return prepared, root, edge, edge_path, adoption, verification


@pytest.mark.asyncio
async def test_44g_mounts_only_after_44f_and_persists_without_promoting_active_restart(
    tmp_path: Path,
) -> None:
    fixture, reentry = _session(tmp_path)
    member, _ = _new_paragraph_member(tmp_path, stem="44g-ui")
    shell = create_first_changed_basis_root_backed_reentry_overlay_research_session_shell(
        reentry,
        (member,),
    )
    assert isinstance(shell, FirstChangedBasisRootBackedReentryOverlayResearchSessionShell)

    async with shell.run_test(size=(215, 610)) as pilot:
        await pilot.pause()
        assert len(shell.query(ResearchFirstChangedBasisRootBackedReentryOverlayControls)) == 0

        _, root, edge, _, _, verification = await _build_44f_ui(
            shell,
            pilot,
            fixture,
            member,
            tmp_path,
            stem="44g-ui",
        )
        controls = shell.query_one(ResearchFirstChangedBasisRootBackedReentryOverlayControls)
        assert controls.verification_result is verification
        assert shell.query_one(
            "#research-first-changed-basis-root-backed-reentry-overlay-prior-plan-source",
            Input,
        ).value == ""
        assert shell.query_one(
            "#research-first-changed-basis-root-backed-reentry-overlay-destination",
            Input,
        ).value == ""

        active_controller = shell.research_controller
        active_session = shell.research_session
        active_reentry = shell.research_reentry
        prior_plan = tmp_path / "44g-ui-prior-plan.json"
        persist_chromium_research_session_reentry_plan_document(reentry.plan, prior_plan)
        destination = tmp_path / "44g-ui-overlay.json"
        shell.query_one(
            "#research-first-changed-basis-root-backed-reentry-overlay-prior-plan-source",
            Input,
        ).value = str(prior_plan)
        shell.query_one(
            "#research-first-changed-basis-root-backed-reentry-overlay-destination",
            Input,
        ).value = str(destination)
        await _press(
            shell,
            pilot,
            "persist-research-first-changed-basis-root-backed-reentry-overlay",
        )

        result = shell.last_first_changed_basis_root_backed_reentry_overlay
        assert result is not None
        assert result.verification_result is verification
        assert result.checkpoint.reentry is verification.fresh_reentry
        assert result.checkpoint.plan == verification.plan
        assert result.checkpoint.persistence.path == destination.resolve()
        assert load_chromium_research_root_backed_session_reentry_plan_document(destination) == verification.plan
        assert shell.research_controller is active_controller
        assert shell.research_session is active_session
        assert shell.research_reentry is active_reentry
        assert len(shell.query("#research-session-restart-plan-controls")) == 0
        assert controls.prior_result is result
        assert shell.query_one(
            "#persist-research-first-changed-basis-root-backed-reentry-overlay",
            Button,
        ).disabled
        receipt = str(
            shell.query_one(
                "#research-first-changed-basis-root-backed-reentry-overlay-status",
                Static,
            ).content
        )
        assert "durable 35C root-backed restart overlay persisted" in receipt
        assert "Mounted governed session unchanged" in receipt
        assert root.persistence.root_record_sha256 in receipt
        assert edge.persistence.edge_record_sha256 in receipt
        assert "does not claim global current/latest/head" in receipt
        assert "does not checkpoint a later 35D continuation" in receipt


@pytest.mark.asyncio
async def test_44g_after_later_rollover_persists_historical_44f_target_without_retargeting(
    tmp_path: Path,
) -> None:
    fixture, reentry = _session(tmp_path)
    member, _ = _new_paragraph_member(tmp_path, stem="44g-rollover")
    shell = create_first_changed_basis_root_backed_reentry_overlay_research_session_shell(
        reentry,
        (member,),
    )

    async with shell.run_test(size=(220, 650)) as pilot:
        await pilot.pause()
        _, _, edge, edge_path, adoption, verification = await _build_44f_ui(
            shell,
            pilot,
            fixture,
            member,
            tmp_path,
            stem="44g-rollover",
        )
        historical_presentation = verification.fresh_reentry.controller.presentation
        assert historical_presentation == adoption.controller.presentation

        successor = tmp_path / "44g-rollover-successor.json"
        shell.query_one("#research-endpoint-revised-note", TextArea).text = (
            "Later mounted continuation before historical restart overlay persistence."
        )
        shell.query_one("#research-endpoint-prior-edge-source", Input).value = str(edge_path)
        shell.query_one("#research-endpoint-destination", Input).value = str(successor)
        await _press(shell, pilot, "persist-research-endpoint-revision")
        shell.query_one("#research-session-rollover-successor-source", Input).value = str(successor)
        shell.query_one(
            "#research-session-rollover-declaration-destination", Input
        ).value = str(tmp_path / "44g-rollover-continuation-declaration.json")
        await _press(shell, pilot, "rollover-research-session")
        continuation_controller = shell.research_controller
        assert continuation_controller.presentation != historical_presentation

        prior_plan = tmp_path / "44g-rollover-prior-plan.json"
        persist_chromium_research_session_reentry_plan_document(reentry.plan, prior_plan)
        destination = tmp_path / "44g-rollover-overlay.json"
        shell.query_one(
            "#research-first-changed-basis-root-backed-reentry-overlay-prior-plan-source",
            Input,
        ).value = str(prior_plan)
        shell.query_one(
            "#research-first-changed-basis-root-backed-reentry-overlay-destination",
            Input,
        ).value = str(destination)
        await _press(
            shell,
            pilot,
            "persist-research-first-changed-basis-root-backed-reentry-overlay",
        )

        result = shell.last_first_changed_basis_root_backed_reentry_overlay
        assert result is not None
        assert result.verification_result is verification
        assert result.checkpoint.fresh_reentry.controller.presentation == historical_presentation
        assert (
            result.checkpoint.fresh_reentry.controller.declared_endpoint.verification.edge_record_sha256
            == edge.persistence.edge_record_sha256
        )
        assert shell.research_controller is continuation_controller
        assert shell.research_controller.presentation != historical_presentation
        assert shell.research_reentry is None
        assert len(shell.query("#research-session-restart-plan-controls")) == 0


@pytest.mark.asyncio
async def test_44g_existing_destination_failure_is_retryable_and_keeps_mounted_state(
    tmp_path: Path,
) -> None:
    fixture, reentry = _session(tmp_path)
    member, _ = _new_paragraph_member(tmp_path, stem="44g-existing-ui")
    shell = create_first_changed_basis_root_backed_reentry_overlay_research_session_shell(
        reentry,
        (member,),
    )

    async with shell.run_test(size=(215, 610)) as pilot:
        await pilot.pause()
        await _build_44f_ui(
            shell,
            pilot,
            fixture,
            member,
            tmp_path,
            stem="44g-existing-ui",
        )
        active_controller = shell.research_controller
        prior_plan = tmp_path / "44g-existing-ui-prior-plan.json"
        persist_chromium_research_session_reentry_plan_document(reentry.plan, prior_plan)
        destination = tmp_path / "44g-existing-ui-overlay.json"
        destination.write_text("preserve exactly\n", encoding="utf-8")
        shell.query_one(
            "#research-first-changed-basis-root-backed-reentry-overlay-prior-plan-source",
            Input,
        ).value = str(prior_plan)
        shell.query_one(
            "#research-first-changed-basis-root-backed-reentry-overlay-destination",
            Input,
        ).value = str(destination)
        await _press(
            shell,
            pilot,
            "persist-research-first-changed-basis-root-backed-reentry-overlay",
        )

        assert shell.last_first_changed_basis_root_backed_reentry_overlay is None
        assert shell.research_controller is active_controller
        assert destination.read_text(encoding="utf-8") == "preserve exactly\n"
        assert not shell.query_one(
            "#persist-research-first-changed-basis-root-backed-reentry-overlay",
            Button,
        ).disabled
        assert "Overlay persistence failed:" in str(
            shell.query_one(
                "#research-first-changed-basis-root-backed-reentry-overlay-status",
                Static,
            ).content
        )


@pytest.mark.asyncio
async def test_plain_44f_shell_never_gains_44g_overlay_controls(tmp_path: Path) -> None:
    fixture, reentry = _session(tmp_path)
    member, _ = _new_paragraph_member(tmp_path, stem="44g-plain-44f")
    shell = create_first_changed_basis_root_backed_reentry_research_session_shell(
        reentry,
        (member,),
    )

    async with shell.run_test(size=(215, 580)) as pilot:
        await pilot.pause()
        await _build_44f_ui(
            shell,
            pilot,
            fixture,
            member,
            tmp_path,
            stem="44g-plain-44f",
        )
        assert shell.last_first_changed_basis_root_backed_reentry_verification is not None
        assert len(shell.query(ResearchFirstChangedBasisRootBackedReentryOverlayControls)) == 0
        assert not hasattr(
            shell,
            "last_first_changed_basis_root_backed_reentry_overlay",
        )
