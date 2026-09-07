from __future__ import annotations

from pathlib import Path

import pytest
from textual.widgets import Button, Input, Static

from pyxis.app.chromium_research_paragraph_text_selection_load import (
    ChromiumPageResearchLoadedParagraphTextSelectionRecord,
)
from pyxis.app.chromium_research_session_reentry import (
    ChromiumResearchExactRangeSelectionReentryLocator,
)
from pyxis.ui import (
    create_first_changed_basis_root_backed_reentry_research_session_shell,
)
from pyxis.ui.chromium_research_first_changed_basis_root_backed_reentry_textual import (
    ResearchFirstChangedBasisRootBackedReentryControls,
)
from test_app_chromium_research_bare_selection_fresh_reentry import _bare_selection
from test_app_chromium_research_session_working_set_extension import _session
from test_ui_research_first_changed_basis_root_backed_reentry import _adopt_44e
from test_ui_research_first_changed_basis_session_adoption import _build_44d_ui
from test_ui_research_first_changed_basis_transition import _press


@pytest.mark.asyncio
async def test_50g_44f_form_freshly_reenters_bare_selection_without_fake_note_locator(
    tmp_path: Path,
) -> None:
    fixture, reentry = _session(tmp_path)
    source, bare, original_locator = _bare_selection(tmp_path)
    shell = create_first_changed_basis_root_backed_reentry_research_session_shell(
        reentry,
        (bare,),
    )

    async with shell.run_test(size=(210, 520)) as pilot:
        await pilot.pause()

        prepared, root, edge, edge_path = await _build_44d_ui(
            shell,
            pilot,
            fixture,
            tmp_path,
            stem="50g-bare",
        )
        adoption, declaration_path = await _adopt_44e(
            shell,
            pilot,
            edge_path,
            tmp_path,
            stem="50g-bare",
        )

        controls = shell.query_one(
            ResearchFirstChangedBasisRootBackedReentryControls
        )
        assert controls.adoption_result is adoption
        assert controls.appended_items == (bare,)

        member_summary = str(
            shell.query_one(
                "#research-first-changed-basis-reentry-member-0-summary",
                Static,
            ).content
        )
        assert "Appended member 0 — exact-range selection" in member_summary
        assert "Human note: none attached — saved source passage only" in member_summary
        assert "Selected text:\nBare" in member_summary
        assert "Note text:" not in member_summary
        assert "None" not in member_summary

        capture_selector = "#research-first-changed-basis-reentry-member-0-capture-source"
        selection_selector = "#research-first-changed-basis-reentry-member-0-selection-source"
        status = shell.query_one(
            "#research-first-changed-basis-root-backed-reentry-status",
            Static,
        )
        assert shell.query_one(capture_selector, Input).value == ""
        assert shell.query_one(selection_selector, Input).value == ""
        assert len(
            shell.query(
                "#research-first-changed-basis-reentry-member-0-note-source"
            )
        ) == 0
        assert len(
            shell.query(
                "#research-first-changed-basis-reentry-member-0-first-capture-source"
            )
        ) == 0
        assert len(
            shell.query(
                "#research-first-changed-basis-reentry-member-0-second-capture-source"
            )
        ) == 0

        # Falsify each bare-member field independently against the live collector.
        # This avoids coupling validation semantics to Textual focus behavior between
        # repeated failed button submissions while still proving the form stays
        # unlocked/retryable after each incomplete locator state.
        shell.query_one(selection_selector, Input).value = str(
            original_locator.selection_source
        )
        assert shell._collect_44f_appended_locators(controls, status) is None
        assert "appended member 0 capture path is required" in str(status.content)
        assert not shell.query_one(
            "#verify-research-first-changed-basis-root-backed-reentry",
            Button,
        ).disabled

        shell.query_one(capture_selector, Input).value = str(
            original_locator.capture_source
        )
        shell.query_one(selection_selector, Input).value = ""
        assert shell._collect_44f_appended_locators(controls, status) is None
        assert "appended member 0 selection path is required" in str(status.content)
        assert not shell.query_one(
            "#verify-research-first-changed-basis-root-backed-reentry",
            Button,
        ).disabled

        general = {
            "changed-working-set-source": prepared.working_set_persistence.path,
            "changed-note-source": prepared.note_persistence.path,
            "transition-source": root.transition_result.persistence.path,
            "root-source": root.persistence.path,
            "first-edge-source": edge_path,
            "declaration-source": declaration_path,
        }
        for suffix, path in general.items():
            shell.query_one(
                f"#research-first-changed-basis-reentry-{suffix}",
                Input,
            ).value = str(path)

        shell.query_one(capture_selector, Input).value = str(
            original_locator.capture_source
        )
        shell.query_one(selection_selector, Input).value = str(
            original_locator.selection_source
        )
        mounted_controller = shell.research_controller
        mounted_session = shell.research_session

        await _press(
            shell,
            pilot,
            "verify-research-first-changed-basis-root-backed-reentry",
        )

        result = shell.last_first_changed_basis_root_backed_reentry_verification
        assert result is not None
        assert result.adoption_result is adoption
        assert result.initial_ordinary_reentry is reentry
        assert shell.research_controller is mounted_controller
        assert shell.research_session is mounted_session

        typed_locator = result.plan.appended_working_set_members[0]
        assert isinstance(
            typed_locator,
            ChromiumResearchExactRangeSelectionReentryLocator,
        )
        assert typed_locator.capture_source == original_locator.capture_source
        assert typed_locator.selection_source == original_locator.selection_source

        fresh_bare = result.fresh_reentry.loaded_appended_members[0]
        assert isinstance(
            fresh_bare,
            ChromiumPageResearchLoadedParagraphTextSelectionRecord,
        )
        assert fresh_bare.selection.selected_text == bare.selection.selected_text == "Bare"
        assert (
            fresh_bare.selection.source.source.verification.path
            == source.verification.path
        )
        assert not hasattr(fresh_bare, "note")
        assert (
            result.fresh_reentry.controller.declared_endpoint.revision.revised_note.working_set.items[-1]
            is fresh_bare
        )

        assert controls.prior_result is result
        assert shell.query_one(capture_selector, Input).disabled
        assert shell.query_one(selection_selector, Input).disabled
        assert shell.query_one(
            "#verify-research-first-changed-basis-root-backed-reentry",
            Button,
        ).disabled
        receipt = str(status.content)
        assert "freshly reconstructed through 35B" in receipt
        assert "no durable 35C overlay/restart locator has been written" in receipt
        assert len(
            shell.query("#research-first-changed-basis-reentry-overlay-destination")
        ) == 0
