from __future__ import annotations

from pathlib import Path

import pytest
from textual.widgets import Input, TextArea

from pyxis.ui.chromium_research_third_changed_basis_transition_textual import (
    ResearchThirdChangedBasisTransitionControls,
)
from pyxis.ui.third_changed_basis_transition_research_session_shell import (
    create_third_changed_basis_transition_research_session_shell,
)
from test_app_chromium_research_session_working_set_extension import (
    _new_paragraph_member,
)
from test_ui_research_third_changed_basis_transition import (
    _continuation,
    _persist_third_transition,
    _prepare_in_shell,
    _press,
)


@pytest.mark.asyncio
async def test_47a_persisted_transition_remains_historical_after_later_second_epoch_rollover(
    tmp_path: Path,
) -> None:
    _, _, reentry, lineage = _continuation(tmp_path, stem="47a-history")
    member, _ = _new_paragraph_member(tmp_path, stem="47a-history-member")
    shell = create_third_changed_basis_transition_research_session_shell(lineage)
    shell.configure_changed_basis_candidate((member,))

    async with shell.run_test(size=(190, 300)) as pilot:
        await pilot.pause()
        prepared = await _prepare_in_shell(
            shell,
            pilot,
            tmp_path,
            stem="47a-history",
        )
        await _persist_third_transition(
            shell,
            pilot,
            prepared,
            tmp_path / "47a-history-transition.json",
        )
        historical = shell.last_third_changed_basis_transition
        controls = shell.query_one(ResearchThirdChangedBasisTransitionControls)
        assert historical is not None
        assert historical.continuation_reentry is reentry
        assert controls.prior_result is historical
        assert not controls.stale

        successor = tmp_path / "47a-history-later-successor.json"
        shell.query_one("#research-endpoint-revised-note", TextArea).text = (
            "Later second-epoch continuation after durable historical third transition."
        )
        shell.query_one("#research-endpoint-prior-edge-source", Input).value = str(
            reentry.controller.declared_endpoint.verification.path
        )
        shell.query_one("#research-endpoint-destination", Input).value = str(successor)
        await _press(shell, pilot, "persist-research-endpoint-revision")
        shell.query_one("#research-session-rollover-successor-source", Input).value = str(
            successor
        )
        shell.query_one(
            "#research-session-rollover-declaration-destination", Input
        ).value = str(tmp_path / "47a-history-later-declaration.json")
        await _press(shell, pilot, "rollover-research-session")

        assert shell.last_third_changed_basis_transition is historical
        assert controls.prior_result is historical
        assert not controls.stale
        assert historical.controller is reentry.controller
        assert historical.continuation_reentry is reentry
        assert shell.research_controller is not reentry.controller
        assert shell.second_basis_epoch_continuation_reentry is reentry
