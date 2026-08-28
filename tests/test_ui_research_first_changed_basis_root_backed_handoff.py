from __future__ import annotations

from pathlib import Path

import pytest
from textual.widgets import Button, Input, Static, TextArea

from pyxis.app.chromium_research_session_reentry_plan_document import (
    persist_chromium_research_session_reentry_plan_document,
)
from pyxis.ui import (
    FirstChangedBasisRootBackedHandoffResearchSessionShell,
    create_first_changed_basis_root_backed_handoff_research_session_shell,
    create_first_changed_basis_root_backed_reentry_overlay_research_session_shell,
)
from pyxis.ui.root_backed_research_session_shell import (
    RootBackedResearchSessionShell,
    create_root_backed_research_session_shell,
)
from test_app_chromium_research_session_working_set_extension import (
    _new_paragraph_member,
    _session,
)
from test_ui_research_first_changed_basis_root_backed_reentry_overlay import (
    _build_44f_ui,
)
from test_ui_research_first_changed_basis_transition import _press


async def _persist_44g(
    shell,
    pilot,
    reentry,
    tmp_path: Path,
    *,
    stem: str,
):
    prior_plan = tmp_path / f"{stem}-prior-plan.json"
    persist_chromium_research_session_reentry_plan_document(reentry.plan, prior_plan)
    destination = tmp_path / f"{stem}-root-backed.overlay.json"
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
    return result, destination


@pytest.mark.asyncio
async def test_44h_handoff_is_absent_until_exact_successful_44g_persistence(
    tmp_path: Path,
) -> None:
    fixture, reentry = _session(tmp_path)
    member, _ = _new_paragraph_member(tmp_path, stem="44h-gated")
    shell = create_first_changed_basis_root_backed_handoff_research_session_shell(
        reentry,
        (member,),
    )
    assert isinstance(shell, FirstChangedBasisRootBackedHandoffResearchSessionShell)

    async with shell.run_test(size=(220, 650)) as pilot:
        await pilot.pause()
        assert len(shell.query("#continue-first-changed-basis-root-backed-session")) == 0
        assert len(shell.query("#research-first-changed-basis-root-backed-handoff-notice")) == 0

        await _build_44f_ui(
            shell,
            pilot,
            fixture,
            member,
            tmp_path,
            stem="44h-gated",
        )
        assert len(shell.query("#continue-first-changed-basis-root-backed-session")) == 0

        prior_plan = tmp_path / "44h-gated-prior-plan.json"
        persist_chromium_research_session_reentry_plan_document(reentry.plan, prior_plan)
        destination = tmp_path / "44h-gated-existing.overlay.json"
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
        assert destination.read_text(encoding="utf-8") == "preserve exactly\n"
        assert len(shell.query("#continue-first-changed-basis-root-backed-session")) == 0
        assert len(shell.query("#research-first-changed-basis-root-backed-handoff-notice")) == 0


@pytest.mark.asyncio
async def test_44h_success_requires_explicit_choice_and_returns_exact_35c_fresh_reentry(
    tmp_path: Path,
    monkeypatch,
) -> None:
    fixture, reentry = _session(tmp_path)
    member, _ = _new_paragraph_member(tmp_path, stem="44h-success")
    shell = create_first_changed_basis_root_backed_handoff_research_session_shell(
        reentry,
        (member,),
    )
    observed: dict[str, object] = {}

    def fake_exit(result=None, *args, **kwargs) -> None:
        observed["result"] = result

    monkeypatch.setattr(shell, "exit", fake_exit)

    async with shell.run_test(size=(220, 690)) as pilot:
        await pilot.pause()
        await _build_44f_ui(
            shell,
            pilot,
            fixture,
            member,
            tmp_path,
            stem="44h-success",
        )
        mounted_controller = shell.research_controller
        mounted_session = shell.research_session
        mounted_reentry = shell.research_reentry

        result, destination = await _persist_44g(
            shell,
            pilot,
            reentry,
            tmp_path,
            stem="44h-success",
        )

        assert "result" not in observed
        assert shell.research_controller is mounted_controller
        assert shell.research_session is mounted_session
        assert shell.research_reentry is mounted_reentry
        assert shell.query_one(
            "#persist-research-first-changed-basis-root-backed-reentry-overlay",
            Button,
        ).disabled
        handoff_button = shell.query_one(
            "#continue-first-changed-basis-root-backed-session",
            Button,
        )
        assert not handoff_button.disabled
        notice = str(
            shell.query_one(
                "#research-first-changed-basis-root-backed-handoff-notice",
                Static,
            ).content
        )
        assert "currently mounted governed session remains unchanged" in notice
        assert "exact freshly proven 35C root-backed session" in notice
        assert "saved overlay path is not reloaded" in notice

        # The in-process handoff must not need the just-written overlay to still exist.
        destination.unlink()
        await _press(shell, pilot, "continue-first-changed-basis-root-backed-session")

        assert observed["result"] is result.checkpoint.fresh_reentry
        assert observed["result"] is not result.verification_result.fresh_reentry

    receiving = create_root_backed_research_session_shell(result.checkpoint.fresh_reentry)
    assert isinstance(receiving, RootBackedResearchSessionShell)
    assert receiving.root_backed_reentry is result.checkpoint.fresh_reentry
    assert receiving.research_controller is result.checkpoint.fresh_reentry.controller
    async with receiving.run_test(size=(170, 220)) as pilot:
        await pilot.pause()
        assert len(receiving.query("#research-endpoint-revision-controls")) == 1
        assert len(receiving.query("#research-session-rollover-controls")) == 1
        assert len(receiving.query("#continue-first-changed-basis-root-backed-session")) == 0


@pytest.mark.asyncio
async def test_44h_explicit_handoff_selects_historical_44g_target_after_later_rollover(
    tmp_path: Path,
    monkeypatch,
) -> None:
    fixture, reentry = _session(tmp_path)
    member, _ = _new_paragraph_member(tmp_path, stem="44h-historical")
    shell = create_first_changed_basis_root_backed_handoff_research_session_shell(
        reentry,
        (member,),
    )
    observed: dict[str, object] = {}

    def fake_exit(result=None, *args, **kwargs) -> None:
        observed["result"] = result

    monkeypatch.setattr(shell, "exit", fake_exit)

    async with shell.run_test(size=(225, 720)) as pilot:
        await pilot.pause()
        _, _, _, edge_path, _, verification = await _build_44f_ui(
            shell,
            pilot,
            fixture,
            member,
            tmp_path,
            stem="44h-historical",
        )
        historical_presentation = verification.fresh_reentry.controller.presentation

        successor = tmp_path / "44h-historical-successor.json"
        shell.query_one("#research-endpoint-revised-note", TextArea).text = (
            "Later mounted continuation remains separate until explicit 44H handoff."
        )
        shell.query_one("#research-endpoint-prior-edge-source", Input).value = str(edge_path)
        shell.query_one("#research-endpoint-destination", Input).value = str(successor)
        await _press(shell, pilot, "persist-research-endpoint-revision")
        shell.query_one("#research-session-rollover-successor-source", Input).value = str(successor)
        shell.query_one(
            "#research-session-rollover-declaration-destination",
            Input,
        ).value = str(tmp_path / "44h-historical-continuation-declaration.json")
        await _press(shell, pilot, "rollover-research-session")
        later_controller = shell.research_controller
        assert later_controller.presentation != historical_presentation

        result, _ = await _persist_44g(
            shell,
            pilot,
            reentry,
            tmp_path,
            stem="44h-historical",
        )
        assert shell.research_controller is later_controller
        assert result.checkpoint.fresh_reentry.controller.presentation == historical_presentation

        await _press(shell, pilot, "continue-first-changed-basis-root-backed-session")

        assert observed["result"] is result.checkpoint.fresh_reentry
        assert observed["result"].controller.presentation == historical_presentation
        assert observed["result"].controller is not later_controller


@pytest.mark.asyncio
async def test_plain_44g_shell_never_gains_44h_handoff_controls(tmp_path: Path) -> None:
    fixture, reentry = _session(tmp_path)
    member, _ = _new_paragraph_member(tmp_path, stem="44h-plain-44g")
    shell = create_first_changed_basis_root_backed_reentry_overlay_research_session_shell(
        reentry,
        (member,),
    )

    async with shell.run_test(size=(220, 650)) as pilot:
        await pilot.pause()
        await _build_44f_ui(
            shell,
            pilot,
            fixture,
            member,
            tmp_path,
            stem="44h-plain-44g",
        )
        result, _ = await _persist_44g(
            shell,
            pilot,
            reentry,
            tmp_path,
            stem="44h-plain-44g",
        )
        assert result is shell.last_first_changed_basis_root_backed_reentry_overlay
        assert len(shell.query("#continue-first-changed-basis-root-backed-session")) == 0
        assert len(shell.query("#research-first-changed-basis-root-backed-handoff-notice")) == 0
