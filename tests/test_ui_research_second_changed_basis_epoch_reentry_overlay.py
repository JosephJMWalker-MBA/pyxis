from __future__ import annotations

from pathlib import Path

import pytest
from textual.widgets import Button, Input, TextArea

from pyxis.app.chromium_research_second_basis_epoch_reentry_plan_document import (
    load_chromium_research_second_basis_epoch_reentry_plan_document,
)
from pyxis.app.chromium_research_second_changed_basis_epoch_reentry import (
    verify_chromium_research_second_changed_basis_epoch_reentry,
)
from pyxis.app.chromium_research_second_changed_basis_epoch_reentry_overlay import (
    ChromiumResearchSecondChangedBasisEpochReentryOverlayResult,
    persist_chromium_research_second_changed_basis_epoch_reentry_overlay,
)
from pyxis.app.chromium_research_second_changed_basis_session_adoption import (
    adopt_chromium_research_second_changed_basis_governed_session,
)
from pyxis.ui.chromium_research_second_changed_basis_epoch_reentry_overlay_textual import (
    ResearchSecondChangedBasisEpochReentryOverlayControls,
)
from pyxis.ui.root_backed_authority_inspection_shell import (
    create_inspectable_root_backed_continuation_handoff_research_session_shell,
)
from pyxis.ui.second_changed_basis_epoch_reentry_overlay_research_session_shell import (
    create_second_changed_basis_epoch_reentry_overlay_research_session_shell,
)
from test_app_chromium_research_session_working_set_extension import _new_paragraph_member
from test_ui_research_second_changed_basis_epoch_reentry import (
    _fill_and_verify_46e,
    _paragraph_locator,
)
from test_ui_research_second_changed_basis_session_adoption import (
    _adopt_ui,
    _reach_46c,
    _second_edge_direct,
)
from test_ui_research_second_changed_basis_transition import (
    _continuation,
    _press,
)


def _direct_46e_verification(tmp_path: Path, *, stem: str):
    values, _, prepared, transition, root, edge = _second_edge_direct(
        tmp_path,
        stem=stem,
    )
    adoption = adopt_chromium_research_second_changed_basis_governed_session(
        edge,
        edge_source=edge.persistence.path,
        declaration_destination=tmp_path / f"{stem}-adoption-declaration.json",
    )
    item = prepared.appended_items[0]
    verification = verify_chromium_research_second_changed_basis_epoch_reentry(
        adoption,
        values[8],
        (_paragraph_locator(item),),
        changed_working_set_source=prepared.working_set_persistence.path,
        changed_note_source=prepared.note_persistence.path,
        transition_source=transition.persistence.path,
        root_source=root.persistence.path,
        first_edge_source=edge.persistence.path,
        declaration_source=adoption.declaration.path,
    )
    return values, verification


def test_46f_application_persists_exact_46e_proof_through_public_37b(
    tmp_path: Path,
) -> None:
    values, verification = _direct_46e_verification(tmp_path, stem="46f-app")
    destination = tmp_path / "46f-app.overlay.json"

    result = persist_chromium_research_second_changed_basis_epoch_reentry_overlay(
        verification,
        prior_root_backed_continuation_overlay_source=values[8],
        destination=destination,
    )

    assert isinstance(result, ChromiumResearchSecondChangedBasisEpochReentryOverlayResult)
    assert result.verification_result is verification
    assert result.checkpoint.reentry is verification.fresh_reentry
    assert result.checkpoint.persistence.path == destination.resolve()
    assert (
        load_chromium_research_second_basis_epoch_reentry_plan_document(destination)
        == result.checkpoint.plan
    )
    assert (
        result.checkpoint.plan.prior_root_backed_continuation_overlay_source
        == values[8].resolve()
    )

    with pytest.raises(
        TypeError,
        match="exactly ChromiumResearchSecondChangedBasisEpochReentryResult",
    ):
        persist_chromium_research_second_changed_basis_epoch_reentry_overlay(
            object(),  # type: ignore[arg-type]
            prior_root_backed_continuation_overlay_source=values[8],
            destination=tmp_path / "wrong-type.overlay.json",
        )


def test_46f_wrong_prior_overlay_rejects_before_write_and_existing_destination_survives(
    tmp_path: Path,
) -> None:
    values, verification = _direct_46e_verification(tmp_path, stem="46f-negative")
    wrong_destination = tmp_path / "46f-wrong-prior.overlay.json"

    with pytest.raises(Exception):
        persist_chromium_research_second_changed_basis_epoch_reentry_overlay(
            verification,
            prior_root_backed_continuation_overlay_source=verification.fresh_reentry.plan.root_source,
            destination=wrong_destination,
        )
    assert not wrong_destination.exists()

    existing = tmp_path / "46f-existing.overlay.json"
    existing.write_text("sentinel\n", encoding="utf-8")
    with pytest.raises(Exception):
        persist_chromium_research_second_changed_basis_epoch_reentry_overlay(
            verification,
            prior_root_backed_continuation_overlay_source=values[8],
            destination=existing,
        )
    assert existing.read_text(encoding="utf-8") == "sentinel\n"


async def _persist_46f(shell, pilot, *, prior_overlay: Path, destination: Path) -> None:
    shell.query_one(
        "#research-second-changed-basis-epoch-reentry-overlay-prior-continuation-overlay-source",
        Input,
    ).value = str(prior_overlay)
    shell.query_one(
        "#research-second-changed-basis-epoch-reentry-overlay-destination",
        Input,
    ).value = str(destination)
    await _press(shell, pilot, "persist-research-second-changed-basis-epoch-reentry-overlay")


@pytest.mark.asyncio
async def test_46f_ui_persists_historical_46e_target_after_later_mounted_rollover(
    tmp_path: Path,
) -> None:
    values, reentry = _continuation(tmp_path, stem="46f-ui")
    member, _ = _new_paragraph_member(tmp_path, stem="46f-ui-member")
    shell = create_second_changed_basis_epoch_reentry_overlay_research_session_shell(reentry)
    shell.configure_changed_basis_candidate((member,))

    async with shell.run_test(size=(225, 760)) as pilot:
        await pilot.pause()
        assert len(shell.query(ResearchSecondChangedBasisEpochReentryOverlayControls)) == 0
        prepared, transition, root, edge = await _reach_46c(
            shell,
            pilot,
            tmp_path,
            stem="46f-ui",
        )
        await _adopt_ui(
            shell,
            pilot,
            edge,
            tmp_path / "46f-ui-adoption-declaration.json",
        )
        adoption = shell.last_second_changed_basis_session_adoption
        assert adoption is not None
        await _fill_and_verify_46e(
            shell,
            pilot,
            prior_overlay=values[8],
            prepared=prepared,
            transition=transition,
            root=root,
            edge=edge,
            adoption=adoption,
        )
        verification = shell.last_second_changed_basis_epoch_reentry_verification
        assert verification is not None
        controls = shell.query_one(ResearchSecondChangedBasisEpochReentryOverlayControls)
        prior_input = controls.query_one(
            "#research-second-changed-basis-epoch-reentry-overlay-prior-continuation-overlay-source",
            Input,
        )
        destination_input = controls.query_one(
            "#research-second-changed-basis-epoch-reentry-overlay-destination",
            Input,
        )
        assert prior_input.value == ""
        assert destination_input.value == ""

        successor = tmp_path / "46f-ui-later-edge.json"
        shell.query_one("#research-endpoint-revised-note", TextArea).text = (
            "Later mounted continuation after the historical 46E proof."
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
        ).value = str(tmp_path / "46f-ui-later-declaration.json")
        await _press(shell, pilot, "rollover-research-session")

        later_controller = shell.research_controller
        later_session = shell.research_session
        later_reentry = shell.research_reentry
        historical_continuation = shell.root_backed_continuation_reentry
        restart_controls_before = len(shell.query("#research-session-restart-plan-controls"))
        destination = tmp_path / "46f-ui.overlay.json"
        await _persist_46f(
            shell,
            pilot,
            prior_overlay=values[8],
            destination=destination,
        )

        result = shell.last_second_changed_basis_epoch_reentry_overlay
        assert result is not None
        assert result.verification_result is verification
        assert result.checkpoint.reentry is verification.fresh_reentry
        assert shell.research_controller is later_controller
        assert shell.research_session is later_session
        assert shell.research_reentry is later_reentry
        assert shell.root_backed_continuation_reentry is historical_continuation
        assert prior_input.disabled
        assert destination_input.disabled
        assert controls.query_one(
            "#persist-research-second-changed-basis-epoch-reentry-overlay", Button
        ).disabled
        assert len(shell.query("#research-session-restart-plan-controls")) == restart_controls_before


@pytest.mark.asyncio
async def test_46f_raw_36d_launch_remains_exactly_pathless_and_current_state_unchanged(
    tmp_path: Path,
) -> None:
    values, reentry = _continuation(tmp_path, stem="46f-raw")
    member, _ = _new_paragraph_member(tmp_path, stem="46f-raw-member")
    shell = create_inspectable_root_backed_continuation_handoff_research_session_shell(
        reentry
    )
    shell.configure_changed_basis_candidate((member,))
    panel = shell.root_backed_authority_inspection
    launch = panel.launch_provenance

    async with shell.run_test(size=(225, 760)) as pilot:
        await pilot.pause()
        prepared, transition, root, edge = await _reach_46c(
            shell,
            pilot,
            tmp_path,
            stem="46f-raw",
        )
        await _adopt_ui(
            shell,
            pilot,
            edge,
            tmp_path / "46f-raw-adoption-declaration.json",
        )
        adoption = shell.last_second_changed_basis_session_adoption
        assert adoption is not None
        await _fill_and_verify_46e(
            shell,
            pilot,
            prior_overlay=values[8],
            prepared=prepared,
            transition=transition,
            root=root,
            edge=edge,
            adoption=adoption,
        )
        current_before = panel.current_state
        mounted_controller = shell.research_controller
        await _persist_46f(
            shell,
            pilot,
            prior_overlay=values[8],
            destination=tmp_path / "46f-raw.overlay.json",
        )

        result = shell.last_second_changed_basis_epoch_reentry_overlay
        assert result is not None
        assert panel.launch_provenance is launch
        assert panel.launch_provenance.launch_location_context is None
        assert panel.current_state is current_before
        assert shell.research_controller is mounted_controller
