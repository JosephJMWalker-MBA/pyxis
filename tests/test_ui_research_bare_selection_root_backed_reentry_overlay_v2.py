from __future__ import annotations

import json
from pathlib import Path

import pytest
from textual.widgets import Input, Static

from pyxis.app.chromium_research_root_backed_session_reentry_plan_document import (
    load_chromium_research_root_backed_session_reentry_plan_document,
)
from pyxis.app.chromium_research_session_reentry_plan_document import (
    persist_chromium_research_session_reentry_plan_document,
)
from pyxis.ui import (
    create_first_changed_basis_root_backed_reentry_overlay_research_session_shell,
)
from pyxis.ui.chromium_research_first_changed_basis_root_backed_reentry_overlay_textual import (
    ResearchFirstChangedBasisRootBackedReentryOverlayControls,
)
from test_app_chromium_research_bare_selection_fresh_reentry import _bare_selection
from test_app_chromium_research_session_working_set_extension import _session
from test_ui_research_first_changed_basis_root_backed_reentry import _adopt_44e
from test_ui_research_first_changed_basis_session_adoption import _build_44d_ui
from test_ui_research_first_changed_basis_transition import _press


@pytest.mark.asyncio
async def test_50h_existing_44g_ui_inherits_bare_selection_overlay_v2(
    tmp_path: Path,
) -> None:
    fixture, reentry = _session(tmp_path)
    _, bare, locator = _bare_selection(tmp_path)
    shell = create_first_changed_basis_root_backed_reentry_overlay_research_session_shell(
        reentry,
        (bare,),
    )

    async with shell.run_test(size=(220, 650)) as pilot:
        await pilot.pause()

        prepared, root, _, edge_path = await _build_44d_ui(
            shell,
            pilot,
            fixture,
            tmp_path,
            stem="50h-ui",
        )
        transition = shell.last_first_changed_basis_transition
        assert transition is not None
        _, declaration_path = await _adopt_44e(
            shell,
            pilot,
            edge_path,
            tmp_path,
            stem="50h-ui",
        )

        shell.query_one(
            "#research-first-changed-basis-reentry-member-0-capture-source",
            Input,
        ).value = str(locator.capture_source)
        shell.query_one(
            "#research-first-changed-basis-reentry-member-0-selection-source",
            Input,
        ).value = str(locator.selection_source)

        general = {
            "changed-working-set-source": prepared.working_set_persistence.path,
            "changed-note-source": prepared.note_persistence.path,
            "transition-source": transition.persistence.path,
            "root-source": root.persistence.path,
            "first-edge-source": edge_path,
            "declaration-source": declaration_path,
        }
        for suffix, path in general.items():
            shell.query_one(
                f"#research-first-changed-basis-reentry-{suffix}",
                Input,
            ).value = str(path)

        mounted_controller = shell.research_controller
        mounted_session = shell.research_session
        await _press(
            shell,
            pilot,
            "verify-research-first-changed-basis-root-backed-reentry",
        )

        verification = shell.last_first_changed_basis_root_backed_reentry_verification
        assert verification is not None
        controls = shell.query_one(
            ResearchFirstChangedBasisRootBackedReentryOverlayControls
        )
        assert controls.verification_result is verification

        prior_plan = tmp_path / "50h-ui-prior-plan.json"
        persist_chromium_research_session_reentry_plan_document(
            reentry.plan,
            prior_plan,
        )
        destination = tmp_path / "50h-ui-overlay.json"
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
        assert result.checkpoint.plan == verification.plan
        assert shell.research_controller is mounted_controller
        assert shell.research_session is mounted_session

        document = json.loads(destination.read_text(encoding="utf-8"))
        assert (
            document["format"]
            == "pyxis.chromium.research_root_backed_session_reentry_locator_overlay.v2"
        )
        assert document["appended_working_set_members"] == [
            {
                "kind": "exact_range_selection",
                "capture_source": document["appended_working_set_members"][0][
                    "capture_source"
                ],
                "selection_source": document["appended_working_set_members"][0][
                    "selection_source"
                ],
            }
        ]
        assert "note_source" not in document["appended_working_set_members"][0]
        assert (
            load_chromium_research_root_backed_session_reentry_plan_document(
                destination
            )
            == verification.plan
        )

        receipt = str(
            shell.query_one(
                "#research-first-changed-basis-root-backed-reentry-overlay-status",
                Static,
            ).content
        )
        assert (
            "Overlay format: "
            "pyxis.chromium.research_root_backed_session_reentry_locator_overlay.v2"
            in receipt
        )
        assert (
            "Overlay format: "
            "pyxis.chromium.research_root_backed_session_reentry_locator_overlay.v1"
            not in receipt
        )
