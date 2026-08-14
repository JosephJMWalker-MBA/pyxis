from pathlib import Path

import pytest
from textual.widgets import Button, Input, Static

from pyxis.app import (
    WorkspaceController,
    build_and_run_workspace,
    query_workspace_presentation,
)
from pyxis.authoring import create_workspace_spec
from pyxis.ui import create_workspace_shell
from pyxis.ui.architecture_consequence_trace_textual import (
    ArchitectureConsequenceTraceDetail,
)
from pyxis.ui.architecture_reconciliation_textual import (
    ArchitectureReconciliationDetail,
)


@pytest.mark.asyncio
async def test_split_lines_apply_replaces_proposed_trace_with_observed_reconciliation(
    tmp_path: Path,
) -> None:
    source = tmp_path / "workspace"
    text = "first line\nsecond line"
    spec = create_workspace_spec(
        "Text Lab",
        "Visible proposed-to-observed architecture reconciliation proof.",
    )
    run = build_and_run_workspace(spec, source, text)
    presentation = query_workspace_presentation(source, run=run)
    controller = WorkspaceController(source, run)
    shell = create_workspace_shell(presentation, controller=controller)

    async with shell.run_test(size=(120, 58)) as pilot:
        await pilot.pause()

        trace_detail = shell.query_one(ArchitectureConsequenceTraceDetail)
        reconciliation_detail = shell.query_one(ArchitectureReconciliationDetail)
        trace_static = shell.query_one(
            "#architecture-consequence-trace-evidence",
            Static,
        )
        reconciliation_static = shell.query_one(
            "#architecture-reconciliation-evidence",
            Static,
        )

        assert trace_detail.presentation is None
        assert reconciliation_detail.presentation is None
        assert trace_static.content == "No pending architecture consequence trace."
        assert (
            reconciliation_static.content
            == "No post-Apply architecture reconciliation."
        )

        preview_button = shell.query_one("#preview-add-split-lines", Button)
        preview_button.focus()
        await pilot.press("enter")
        await pilot.pause()

        proposed = trace_detail.presentation
        assert proposed is not None
        assert reconciliation_detail.presentation is None
        assert "PROPOSED CONSEQUENCE TRACE — NOT APPLIED" in str(trace_static.content)
        assert "add capability: split_lines" in str(trace_static.content)
        assert (
            reconciliation_static.content
            == "No post-Apply architecture reconciliation."
        )

        shell.query_one("#split-lines-rationale", Input).value = (
            "Observe the exact consequences after applying split_lines."
        )
        shell.query_one("#runtime-input", Input).value = text
        apply_button = shell.query_one("#apply-add-split-lines", Button)
        apply_button.focus()
        await pilot.press("enter")
        await pilot.pause()

        reconciliation = controller.last_architecture_reconciliation
        assert reconciliation is not None
        assert reconciliation.proposed == proposed
        assert trace_detail.presentation is None
        assert trace_static.content == "No pending architecture consequence trace."
        assert reconciliation_detail.presentation is reconciliation

        observed_text = str(reconciliation_static.content)
        expected_fragments = (
            "POST-APPLY RECONCILIATION — OBSERVED EVIDENCE",
            "Earlier preview remains separate proposed evidence.",
            "→ operation: add_capability:split_lines",
            "→ preview canonical transition vs observed revision: MATCH",
            "→ proposed canonical identity: MATCH",
            "→ proposed RIR capabilities: MATCH",
            "generated/capabilities/split_lines.py: proposed add; expected status new; observed new; MATCH",
            "generated/workspaces/text_lab/main.py: proposed change; expected status regenerated; observed regenerated; MATCH",
            "→ proposed runtime keys: MATCH",
        )
        for fragment in expected_fragments:
            assert fragment in observed_text

        assert shell.presentation.canonical.capabilities == (
            "inspect_text",
            "normalize_text",
            "split_lines",
        )
        assert tuple(shell.presentation.runtime_result) == (
            "inspect_text",
            "normalize_text",
            "split_lines",
        )
