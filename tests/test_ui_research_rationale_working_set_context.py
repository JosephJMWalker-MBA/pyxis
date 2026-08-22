from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest
from textual.widgets import Button, Input, Static

from pyxis.app import WorkspaceController, build_and_run_workspace, create_workspace_presentation
from pyxis.app.chromium_research_revision_edge_working_set_presentation import (
    present_chromium_research_revision_edge_working_set_context,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_sequence_presentation import (
    present_chromium_research_working_set_note_revision_edge_sequence_declaration,
)
from pyxis.authoring import create_workspace_spec
from pyxis.ui import create_workspace_shell
from pyxis.ui.chromium_research_rationale_working_set_textual import (
    ATTACHMENT_NOTICE,
    ResearchRationaleWorkingSetDetail,
)
from pyxis.ui.chromium_research_revision_edge_sequence_textual import (
    ResearchRevisionEdgeSequenceDetail,
)
from test_app_chromium_research_working_set_note_revision_edge_sequence_presentation import (
    _loaded_declared_sequence,
)


def _research(tmp_path: Path):
    _, _, _, _, _, loaded = _loaded_declared_sequence(tmp_path)
    segment = present_chromium_research_working_set_note_revision_edge_sequence_declaration(
        loaded
    )
    first = present_chromium_research_revision_edge_working_set_context(
        loaded,
        declared_position=1,
    )
    second = present_chromium_research_revision_edge_working_set_context(
        loaded,
        declared_position=2,
    )
    return segment, first, second


def _workspace(tmp_path: Path):
    root = tmp_path / "workspace"
    spec = create_workspace_spec(
        "Research context UI",
        "Workspace identity remains separate from research evidence.",
    )
    run = build_and_run_workspace(spec, root, "same runtime workload")
    return root, run, create_workspace_presentation(spec, run)


@pytest.mark.asyncio
async def test_explicit_context_mounts_only_for_matching_position_and_starts_collapsed(
    tmp_path: Path,
) -> None:
    segment, _, second = _research(tmp_path)
    _, _, workspace = _workspace(tmp_path)
    shell = create_workspace_shell(
        workspace,
        research_presentation=segment,
        research_working_set_contexts=(second,),
    )

    async with shell.run_test(size=(140, 70)) as pilot:
        await pilot.pause()
        research = shell.query_one(ResearchRevisionEdgeSequenceDetail)
        assert {button.id for button in research.query(Button)} == {
            "research-context-toggle-2"
        }
        detail = research.query_one(ResearchRationaleWorkingSetDetail)
        assert detail.presentation is second
        assert detail.has_class("research-context-collapsed")
        assert len(research.query("#research-context-toggle-1")) == 0


@pytest.mark.asyncio
async def test_context_button_reveals_and_hides_exact_three_layer_evidence(
    tmp_path: Path,
) -> None:
    segment, first, _ = _research(tmp_path)
    _, _, workspace = _workspace(tmp_path)
    shell = create_workspace_shell(
        workspace,
        research_presentation=segment,
        research_working_set_contexts=(first,),
    )

    async with shell.run_test(size=(150, 80)) as pilot:
        await pilot.pause()
        button = shell.query_one("#research-context-toggle-1", Button)
        detail = shell.query_one(ResearchRationaleWorkingSetDetail)
        assert detail.has_class("research-context-collapsed")

        button.focus()
        await pilot.pause()
        await pilot.press("enter")
        await pilot.pause()
        assert not detail.has_class("research-context-collapsed")
        assert detail.presentation is first

        static_widgets = tuple(detail.query(Static))
        source_texts = tuple(
            str(widget.content)
            for widget in static_widgets
            if widget.has_class("research-source-excerpt-text")
        )
        note_texts = tuple(
            str(widget.content)
            for widget in static_widgets
            if widget.has_class("research-working-set-note-text")
        )
        rationale_texts = tuple(
            str(widget.content)
            for widget in static_widgets
            if widget.has_class("research-rationale-context-text")
        )
        assert source_texts == (
            "Alpha evidence paragraph",
            "Alpha",
            "Alpha",
            "Beta",
        )
        assert note_texts == (
            "  Whole paragraph matters.  ",
            "Exact range note 😀",
            "  Human comparison; no machine relation claim.\nKeep exact.  ",
        )
        assert rationale_texts == ("  v5 exact human wording 😀  ",)
        assert source_texts[0] not in note_texts
        assert rationale_texts[0] not in source_texts

        button.focus()
        await pilot.pause()
        await pilot.press("enter")
        await pilot.pause()
        assert detail.has_class("research-context-collapsed")


@pytest.mark.asyncio
async def test_comparison_context_keeps_two_explicit_selections_and_attachment_notice(
    tmp_path: Path,
) -> None:
    segment, first, _ = _research(tmp_path)
    _, _, workspace = _workspace(tmp_path)
    shell = create_workspace_shell(
        workspace,
        research_presentation=segment,
        research_working_set_contexts=(first,),
    )

    async with shell.run_test(size=(150, 80)) as pilot:
        await pilot.pause()
        detail = shell.query_one(ResearchRationaleWorkingSetDetail)
        rendered = "\n".join(str(widget.content) for widget in detail.query(Static))
        assert ATTACHMENT_NOTICE in rendered
        assert "Working-set member 3: comparison_note" in rendered
        assert "first_selection: Exact returned text range" in rendered
        assert "second_selection: Exact returned text range" in rendered
        assert "Observed URL: https://example.test/a" in rendered
        assert "Observed URL: https://example.test/b" in rendered
        assert "Range: [0, 5)" in rendered
        assert "Range: [0, 4)" in rendered


def test_contexts_require_a_research_segment(tmp_path: Path) -> None:
    _, first, _ = _research(tmp_path)
    _, _, workspace = _workspace(tmp_path)

    with pytest.raises(ValueError, match="require a research_presentation"):
        create_workspace_shell(
            workspace,
            research_working_set_contexts=(first,),
        )


def test_context_with_wrong_declaration_is_rejected(tmp_path: Path) -> None:
    segment, first, _ = _research(tmp_path)
    forged = replace(first, declaration_record_sha256="f" * 64)
    _, _, workspace = _workspace(tmp_path)

    with pytest.raises(ValueError, match="different declaration"):
        create_workspace_shell(
            workspace,
            research_presentation=segment,
            research_working_set_contexts=(forged,),
        )


def test_context_with_wrong_edge_identity_is_rejected(tmp_path: Path) -> None:
    segment, first, _ = _research(tmp_path)
    forged = replace(first, edge_record_sha256="f" * 64)
    _, _, workspace = _workspace(tmp_path)

    with pytest.raises(ValueError, match="edge identity does not match"):
        create_workspace_shell(
            workspace,
            research_presentation=segment,
            research_working_set_contexts=(forged,),
        )


def test_context_with_wrong_rationale_text_is_rejected(tmp_path: Path) -> None:
    segment, first, _ = _research(tmp_path)
    forged = replace(first, rationale_text="different rationale")
    _, _, workspace = _workspace(tmp_path)

    with pytest.raises(ValueError, match="rationale text does not match"):
        create_workspace_shell(
            workspace,
            research_presentation=segment,
            research_working_set_contexts=(forged,),
        )


def test_duplicate_context_positions_are_rejected(tmp_path: Path) -> None:
    segment, first, _ = _research(tmp_path)
    _, _, workspace = _workspace(tmp_path)

    with pytest.raises(ValueError, match="declared positions must be unique"):
        create_workspace_shell(
            workspace,
            research_presentation=segment,
            research_working_set_contexts=(first, first),
        )


def test_forged_context_excerpt_shape_is_rejected_before_shell_mount(tmp_path: Path) -> None:
    segment, first, _ = _research(tmp_path)
    paragraph = first.members[0]
    forged_excerpt = replace(
        paragraph.excerpts[0],
        excerpt_kind="exact_returned_text_range",
    )
    forged_member = replace(paragraph, excerpts=(forged_excerpt,))
    forged = replace(first, members=(forged_member, *first.members[1:]))
    _, _, workspace = _workspace(tmp_path)

    with pytest.raises(ValueError, match="excerpt kind is incoherent"):
        create_workspace_shell(
            workspace,
            research_presentation=segment,
            research_working_set_contexts=(forged,),
        )


@pytest.mark.asyncio
async def test_workspace_runtime_rerun_preserves_exact_context_presentations(
    tmp_path: Path,
) -> None:
    segment, first, second = _research(tmp_path)
    root, run, workspace = _workspace(tmp_path)
    controller = WorkspaceController(root, run)
    shell = create_workspace_shell(
        workspace,
        controller=controller,
        research_presentation=segment,
        research_working_set_contexts=(first, second),
    )

    async with shell.run_test(size=(150, 80)) as pilot:
        await pilot.pause()
        context_tuple = shell.research_working_set_contexts
        runtime_input = shell.query_one("#runtime-input", Input)
        runtime_input.value = "changed runtime input"
        runtime_input.focus()
        await pilot.press("enter")
        await pilot.pause()

        assert shell.research_presentation is segment
        assert shell.research_working_set_contexts is context_tuple
        assert shell.research_working_set_contexts == (first, second)
        details = tuple(shell.query(ResearchRationaleWorkingSetDetail))
        assert tuple(detail.presentation for detail in details) == (first, second)
