from __future__ import annotations

from pathlib import Path

import pytest
from textual.widgets import Input, TextArea

from pyxis.app.chromium_research_root_backed_session_shell_lineage import (
    prove_chromium_research_root_backed_session_continuation_shell_lineage,
)
from pyxis.ui.root_backed_authority_inspection_shell import (
    create_inspectable_root_backed_continuation_research_session_shell,
)
from test_app_chromium_research_session_working_set_extension import _new_paragraph_member
from test_ui_research_second_changed_basis_session_adoption import (
    _adopt_ui,
    _reach_46c,
)
from test_ui_research_second_changed_basis_transition import (
    _continuation,
    _press,
)


@pytest.mark.asyncio
async def test_46d_inspection_advances_after_post_adoption_ordinary_rollover(
    tmp_path: Path,
) -> None:
    values, reentry = _continuation(tmp_path, stem="46d-inspection-rollover")
    overlay = values[8]
    lineage = prove_chromium_research_root_backed_session_continuation_shell_lineage(
        reentry,
        overlay_source=overlay,
    )
    shell = create_inspectable_root_backed_continuation_research_session_shell(lineage)
    member, _ = _new_paragraph_member(
        tmp_path,
        stem="46d-inspection-rollover-member",
    )
    shell.configure_changed_basis_candidate((member,))
    panel = shell.root_backed_authority_inspection
    launch = panel.launch_provenance

    async with shell.run_test(size=(220, 540)) as pilot:
        await pilot.pause()
        *_, edge = await _reach_46c(
            shell,
            pilot,
            tmp_path,
            stem="46d-inspection-rollover",
        )
        await _adopt_ui(
            shell,
            pilot,
            edge,
            tmp_path / "46d-inspection-rollover-adoption-declaration.json",
        )
        adoption = shell.last_second_changed_basis_session_adoption
        assert adoption is not None
        assert panel.launch_provenance is launch
        assert panel.current_state.state_source == (
            "explicit 46D second changed-basis adoption"
        )

        successor = tmp_path / "46d-inspection-rollover-successor.json"
        shell.query_one("#research-endpoint-revised-note", TextArea).text = (
            "Ordinary continuation after inspectable second changed-basis adoption."
        )
        shell.query_one("#research-endpoint-prior-edge-source", Input).value = str(
            edge.persistence.path
        )
        shell.query_one("#research-endpoint-destination", Input).value = str(successor)
        await _press(shell, pilot, "persist-research-endpoint-revision")
        shell.query_one("#research-session-rollover-successor-source", Input).value = str(
            successor
        )
        shell.query_one(
            "#research-session-rollover-declaration-destination", Input
        ).value = str(tmp_path / "46d-inspection-rollover-next-declaration.json")
        await _press(shell, pilot, "rollover-research-session")

        assert panel.launch_provenance is launch
        assert launch.launch_location_context == overlay.resolve()
        assert panel.current_state.state_kind == (
            "visible continuation after second changed-basis adoption"
        )
        assert panel.current_state.state_source == (
            "explicit rollover after 46D second changed-basis adoption"
        )
        assert panel.current_state.endpoint_sha256 == (
            shell.research_controller.declared_endpoint.verification.edge_record_sha256
        )
        assert len(shell.query("#research-root-backed-cumulative-checkpoint-controls")) == 0
        assert shell.root_backed_continuation_reentry is reentry
