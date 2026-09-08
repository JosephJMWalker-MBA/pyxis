from __future__ import annotations

import json
from pathlib import Path

import pytest
from textual.widgets import Button, Input, Static

from pyxis.app.chromium_research_paragraph_text_selection_load import (
    ChromiumPageResearchLoadedParagraphTextSelectionRecord,
)
from pyxis.app.chromium_research_second_changed_basis_epoch_reentry import (
    verify_chromium_research_second_changed_basis_epoch_reentry,
)
from pyxis.app.chromium_research_second_changed_basis_epoch_reentry_overlay import (
    persist_chromium_research_second_changed_basis_epoch_reentry_overlay,
)
from pyxis.app.chromium_research_session_reentry_plan_document import (
    ChromiumResearchSessionReentryPlanDocumentError,
)
from pyxis.ui.chromium_research_second_changed_basis_epoch_reentry_textual import (
    ResearchSecondChangedBasisEpochReentryControls,
)
from pyxis.ui.second_changed_basis_epoch_reentry_research_session_shell import (
    create_second_changed_basis_epoch_reentry_research_session_shell,
)
from test_app_chromium_research_bare_selection_fresh_reentry import _bare_selection
from test_bare_selection_root_backed_continuation_v1 import (
    _assert_bare_member_survives,
)
from test_bare_selection_root_backed_cumulative_v1 import (
    _persist_bare_cumulative_extension,
)
from test_ui_research_second_changed_basis_session_adoption import (
    _adopt_ui,
    _reach_46c,
)
from test_ui_research_second_changed_basis_transition import _press


def _second_bare_selection(tmp_path: Path):
    member_dir = tmp_path / "second-bare-member"
    member_dir.mkdir()
    source, bare, locator = _bare_selection(member_dir)
    assert bare.selection.selected_text == "Bare"
    return source, bare, locator


@pytest.mark.asyncio
async def test_50l_46e_product_freshly_reenters_second_basis_with_bare_selection(
    tmp_path: Path,
) -> None:
    prior_values = _persist_bare_cumulative_extension(
        tmp_path,
        stem="50l-prior",
    )
    prior_overlay = prior_values[24]
    prior_result = prior_values[27]
    prior = prior_result.fresh_reentry
    _assert_bare_member_survives(prior)

    _, bare, bare_locator = _second_bare_selection(tmp_path)
    shell = create_second_changed_basis_epoch_reentry_research_session_shell(prior)
    shell.configure_changed_basis_candidate((bare,))

    mounted_prior_controller = shell.research_controller
    historical_first_root_continuation = shell.root_backed_continuation_reentry

    async with shell.run_test(size=(230, 820)) as pilot:
        await pilot.pause()
        assert len(shell.query(ResearchSecondChangedBasisEpochReentryControls)) == 0

        prepared, transition, root, edge = await _reach_46c(
            shell,
            pilot,
            tmp_path,
            stem="50l",
        )

        assert prepared.appended_items == (bare,)
        assert prepared.appended_items[0] is bare
        assert prepared.working_set.items[-1] is bare
        assert (
            prepared.working_set_persistence.working_set_format
            == "pyxis.chromium.research_working_set.v2"
        )
        assert (
            prepared.note_persistence.note_format
            == "pyxis.chromium.research_working_set_note.v2"
        )
        assert json.loads(
            transition.persistence.path.read_text(encoding="utf-8")
        )["format"] == "pyxis.chromium.research_session_working_set_transition.v1"
        assert json.loads(
            root.persistence.path.read_text(encoding="utf-8")
        )["format"] == (
            "pyxis.chromium.research_session_working_set_transition_revision_root.v1"
        )
        assert json.loads(
            edge.persistence.path.read_text(encoding="utf-8")
        )["format"] == "pyxis.chromium.research_working_set_note_revision_edge.v1"

        await _adopt_ui(
            shell,
            pilot,
            edge,
            tmp_path / "50l-adoption-declaration.json",
        )
        adoption = shell.last_second_changed_basis_session_adoption
        assert adoption is not None
        assert shell.research_controller is adoption.controller
        assert shell.research_controller is not mounted_prior_controller
        assert shell.root_backed_continuation_reentry is historical_first_root_continuation

        direct = verify_chromium_research_second_changed_basis_epoch_reentry(
            adoption,
            prior_overlay,
            (bare_locator,),
            changed_working_set_source=prepared.working_set_persistence.path,
            changed_note_source=prepared.note_persistence.path,
            transition_source=transition.persistence.path,
            root_source=root.persistence.path,
            first_edge_source=edge.persistence.path,
            declaration_source=adoption.declaration.path,
        )
        assert direct.fresh_reentry.controller.presentation == adoption.controller.presentation
        direct_bare = direct.fresh_reentry.loaded_appended_members[0]
        assert isinstance(
            direct_bare,
            ChromiumPageResearchLoadedParagraphTextSelectionRecord,
        )
        assert direct_bare.selection.selected_text == "Bare"
        assert not hasattr(direct_bare, "note")

        controls = shell.query_one(ResearchSecondChangedBasisEpochReentryControls)
        summary = str(
            shell.query_one(
                "#research-second-changed-basis-epoch-reentry-member-0-summary",
                Static,
            ).content
        )
        assert "exact-range selection" in summary
        assert "Human note: none attached — saved source passage only" in summary
        assert "Human note: None" not in summary
        assert "Note text:\nNone" not in summary
        assert len(
            shell.query(
                "#research-second-changed-basis-epoch-reentry-member-0-note-source"
            )
        ) == 0
        assert len(
            shell.query(
                "#research-second-changed-basis-epoch-reentry-member-0-selection-source"
            )
        ) == 1

        inputs = list(controls.query(Input))
        assert inputs
        assert all(widget.value == "" for widget in inputs)

        shell.query_one(
            "#research-second-changed-basis-epoch-reentry-prior-continuation-overlay-source",
            Input,
        ).value = str(prior_overlay)
        shell.query_one(
            "#research-second-changed-basis-epoch-reentry-member-0-capture-source",
            Input,
        ).value = str(bare_locator.capture_source)
        for suffix, path in (
            ("changed-working-set-source", prepared.working_set_persistence.path),
            ("changed-note-source", prepared.note_persistence.path),
            ("transition-source", transition.persistence.path),
            ("root-source", root.persistence.path),
            ("first-edge-source", edge.persistence.path),
            ("declaration-source", adoption.declaration.path),
        ):
            shell.query_one(
                f"#research-second-changed-basis-epoch-reentry-{suffix}",
                Input,
            ).value = str(path)

        await _press(
            shell,
            pilot,
            "verify-research-second-changed-basis-epoch-reentry",
        )
        assert shell.last_second_changed_basis_epoch_reentry_verification is None
        status = str(
            shell.query_one(
                "#research-second-changed-basis-epoch-reentry-status",
                Static,
            ).content
        )
        assert "bare selection member 0 requires capture and selection paths" in status
        assert not controls.query_one(
            "#research-second-changed-basis-epoch-reentry-member-0-selection-source",
            Input,
        ).disabled

        # Textual keeps a pressed Button in its transient "-active" state while
        # the visual press effect is running. A second Enter/click during that
        # state is intentionally ignored, so wait for the first validation press
        # to become activatable again before exercising the corrected retry.
        verify_button = controls.query_one(
            "#verify-research-second-changed-basis-epoch-reentry",
            Button,
        )
        for _ in range(20):
            if not verify_button.has_class("-active"):
                break
            await pilot.pause(delay=0.02)
        assert not verify_button.has_class("-active")

        selection_input = controls.query_one(
            "#research-second-changed-basis-epoch-reentry-member-0-selection-source",
            Input,
        )
        selection_input.value = str(bare_locator.selection_source)
        assert selection_input.value == str(bare_locator.selection_source)

        adopted_controller = shell.research_controller
        adopted_session = shell.research_session
        await _press(
            shell,
            pilot,
            "verify-research-second-changed-basis-epoch-reentry",
        )

        # 46E schedules its verifier with call_after_refresh; wait on the proof
        # state rather than assuming one scheduler turn is enough on every lane.
        for _ in range(20):
            verification = shell.last_second_changed_basis_epoch_reentry_verification
            if verification is not None:
                break
            await pilot.pause(delay=0.01)
        else:
            verification = None

        second_status = str(
            shell.query_one(
                "#research-second-changed-basis-epoch-reentry-status",
                Static,
            ).content
        )
        assert verification is not None, second_status
        assert verification.adoption_result is adoption
        fresh = verification.fresh_reentry
        assert fresh.controller is not adopted_controller
        assert fresh.controller.presentation == adoption.controller.presentation
        assert (
            fresh.loaded_root.verification.root_record_sha256
            == root.persistence.root_record_sha256
        )
        assert (
            fresh.loaded_declaration.verification.sequence_record_sha256
            == adoption.declaration.sequence_record_sha256
        )
        assert (
            fresh.controller.declared_endpoint.verification.edge_record_sha256
            == edge.persistence.edge_record_sha256
        )

        fresh_second_bare = fresh.loaded_appended_members[0]
        assert isinstance(
            fresh_second_bare,
            ChromiumPageResearchLoadedParagraphTextSelectionRecord,
        )
        assert fresh_second_bare.selection.selected_text == "Bare"
        assert not hasattr(fresh_second_bare, "note")
        assert fresh.loaded_root.transition.successor_note.note.working_set.items[-1] is (
            fresh_second_bare
        )
        assert (
            fresh.controller.declared_endpoint.revision.revised_note.working_set.items[-1]
            is fresh_second_bare
        )
        _assert_bare_member_survives(fresh.prior_continuation_reentry)

        assert shell.research_controller is adopted_controller
        assert shell.research_session is adopted_session
        assert shell.root_backed_continuation_reentry is historical_first_root_continuation
        assert all(widget.disabled for widget in inputs)

        stop_destination = tmp_path / "50l-37b-must-remain-closed.json"
        with pytest.raises(
            ChromiumResearchSessionReentryPlanDocumentError,
            match="unsupported member locator",
        ):
            persist_chromium_research_second_changed_basis_epoch_reentry_overlay(
                verification,
                prior_root_backed_continuation_overlay_source=prior_overlay,
                destination=stop_destination,
            )
        assert not stop_destination.exists()


@pytest.mark.asyncio
async def test_50l_historical_note_member_46e_fields_remain_unchanged(
    tmp_path: Path,
) -> None:
    from test_app_chromium_research_session_working_set_extension import (
        _new_paragraph_member,
    )
    from test_ui_research_second_changed_basis_transition import _continuation

    _, reentry = _continuation(tmp_path, stem="50l-control")
    member, _ = _new_paragraph_member(tmp_path, stem="50l-control-member")
    shell = create_second_changed_basis_epoch_reentry_research_session_shell(reentry)
    shell.configure_changed_basis_candidate((member,))

    async with shell.run_test(size=(220, 650)) as pilot:
        await pilot.pause()
        _, _, _, edge = await _reach_46c(
            shell,
            pilot,
            tmp_path,
            stem="50l-control",
        )
        await _adopt_ui(
            shell,
            pilot,
            edge,
            tmp_path / "50l-control-adoption.json",
        )

        summary = str(
            shell.query_one(
                "#research-second-changed-basis-epoch-reentry-member-0-summary",
                Static,
            ).content
        )
        assert "paragraph note" in summary
        assert "Note text:" in summary
        assert len(
            shell.query(
                "#research-second-changed-basis-epoch-reentry-member-0-capture-source"
            )
        ) == 1
        assert len(
            shell.query(
                "#research-second-changed-basis-epoch-reentry-member-0-note-source"
            )
        ) == 1
        assert len(
            shell.query(
                "#research-second-changed-basis-epoch-reentry-member-0-selection-source"
            )
        ) == 0
