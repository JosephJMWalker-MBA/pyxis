from __future__ import annotations

import json
from pathlib import Path

import pytest
from textual.widgets import Input, Static

from pyxis.ui.chromium_research_second_changed_basis_epoch_reentry_overlay_textual import (
    ResearchSecondChangedBasisEpochReentryOverlayControls,
)
from pyxis.ui.root_backed_authority_inspection_shell import (
    create_inspectable_root_backed_continuation_handoff_research_session_shell,
)
from test_bare_selection_root_backed_cumulative_v1 import (
    _persist_bare_cumulative_extension,
)
from test_ui_research_second_changed_basis_session_adoption import (
    _adopt_ui,
    _reach_46c,
)
from test_ui_research_second_changed_basis_transition import _press
from test_ui_second_basis_bare_selection_reentry import _second_bare_selection


_OVERLAY_V2 = "pyxis.chromium.research_second_basis_epoch_reentry_locator_overlay.v2"


@pytest.mark.asyncio
async def test_50m_existing_46f_product_persists_bare_second_basis_as_overlay_v2(
    tmp_path: Path,
) -> None:
    prior_values = _persist_bare_cumulative_extension(
        tmp_path,
        stem="50m-ui-prior",
    )
    prior_overlay = prior_values[24]
    prior = prior_values[27].fresh_reentry
    _, bare, bare_locator = _second_bare_selection(tmp_path)

    shell = create_inspectable_root_backed_continuation_handoff_research_session_shell(
        prior
    )
    shell.configure_changed_basis_candidate((bare,))
    panel = shell.root_backed_authority_inspection
    launch = panel.launch_provenance

    async with shell.run_test(size=(235, 900)) as pilot:
        await pilot.pause()

        prepared, transition, root, edge = await _reach_46c(
            shell,
            pilot,
            tmp_path,
            stem="50m-ui",
        )
        await _adopt_ui(
            shell,
            pilot,
            edge,
            tmp_path / "50m-ui-adoption.json",
        )
        adoption = shell.last_second_changed_basis_session_adoption
        assert adoption is not None

        shell.query_one(
            "#research-second-changed-basis-epoch-reentry-prior-continuation-overlay-source",
            Input,
        ).value = str(prior_overlay)
        shell.query_one(
            "#research-second-changed-basis-epoch-reentry-member-0-capture-source",
            Input,
        ).value = str(bare_locator.capture_source)
        shell.query_one(
            "#research-second-changed-basis-epoch-reentry-member-0-selection-source",
            Input,
        ).value = str(bare_locator.selection_source)
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
        for _ in range(20):
            verification = shell.last_second_changed_basis_epoch_reentry_verification
            if verification is not None:
                break
            await pilot.pause(delay=0.01)
        else:
            verification = None
        assert verification is not None
        assert verification.adoption_result is adoption

        for _ in range(20):
            matches = list(
                shell.query(
                    "#research-second-changed-basis-epoch-reentry-overlay-controls"
                )
            )
            if matches:
                break
            await pilot.pause(delay=0.01)
        controls = shell.query_one(
            ResearchSecondChangedBasisEpochReentryOverlayControls
        )
        assert controls.verification_result is verification

        mounted_controller = shell.research_controller
        mounted_session = shell.research_session
        mounted_reentry = shell.research_reentry
        historical_continuation = shell.root_backed_continuation_reentry
        current_before = panel.current_state

        destination = tmp_path / "50m-ui-second-basis.overlay.json"
        shell.query_one(
            "#research-second-changed-basis-epoch-reentry-overlay-prior-continuation-overlay-source",
            Input,
        ).value = str(prior_overlay)
        shell.query_one(
            "#research-second-changed-basis-epoch-reentry-overlay-destination",
            Input,
        ).value = str(destination)

        await _press(
            shell,
            pilot,
            "persist-research-second-changed-basis-epoch-reentry-overlay",
        )
        for _ in range(20):
            result = shell.last_second_changed_basis_epoch_reentry_overlay
            if result is not None:
                break
            await pilot.pause(delay=0.01)
        else:
            result = None
        assert result is not None
        assert result.verification_result is verification
        assert result.checkpoint.persistence.overlay_format == _OVERLAY_V2

        document = json.loads(destination.read_text(encoding="utf-8"))
        assert document["format"] == _OVERLAY_V2
        assert document["appended_working_set_members"][0]["kind"] == (
            "exact_range_selection"
        )
        assert "note_source" not in document["appended_working_set_members"][0]

        receipt = str(
            shell.query_one(
                "#research-second-changed-basis-epoch-reentry-overlay-status",
                Static,
            ).content
        )
        assert f"Overlay format: {_OVERLAY_V2}" in receipt
        assert (
            "Overlay format: "
            "pyxis.chromium.research_second_basis_epoch_reentry_locator_overlay.v1"
            not in receipt
        )

        assert shell.research_controller is mounted_controller
        assert shell.research_session is mounted_session
        assert shell.research_reentry is mounted_reentry
        assert shell.root_backed_continuation_reentry is historical_continuation
        assert panel.launch_provenance is launch
        assert panel.current_state is current_before
