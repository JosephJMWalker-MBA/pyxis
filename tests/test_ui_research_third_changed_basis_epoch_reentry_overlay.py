from __future__ import annotations

from pathlib import Path

import pytest
from textual.widgets import Button, Input, TextArea

from pyxis.app.chromium_research_third_basis_epoch_reentry_plan_document import (
    load_chromium_research_third_basis_epoch_reentry_plan_document,
)
from pyxis.app.chromium_research_third_changed_basis_epoch_reentry import (
    verify_chromium_research_third_changed_basis_epoch_reentry,
)
from pyxis.app.chromium_research_third_changed_basis_epoch_reentry_overlay import (
    ChromiumResearchThirdChangedBasisEpochReentryOverlayResult,
    persist_chromium_research_third_changed_basis_epoch_reentry_overlay,
)
from pyxis.app.chromium_research_third_changed_basis_session_adoption import (
    adopt_chromium_research_third_changed_basis_governed_session,
)
from pyxis.ui.chromium_research_third_changed_basis_epoch_reentry_overlay_textual import (
    ResearchThirdChangedBasisEpochReentryOverlayControls,
)
from pyxis.ui.third_changed_basis_epoch_reentry_overlay_research_session_shell import (
    create_inspectable_third_changed_basis_epoch_reentry_overlay_handoff_research_session_shell,
    create_third_changed_basis_epoch_reentry_overlay_handoff_research_session_shell,
    create_third_changed_basis_epoch_reentry_overlay_research_session_shell,
)
from pyxis.ui.third_changed_basis_epoch_reentry_research_session_shell import (
    create_third_changed_basis_epoch_reentry_research_session_shell,
)
from test_app_chromium_research_session_working_set_extension import _new_paragraph_member
from test_ui_research_third_changed_basis_epoch_reentry import (
    _fill_and_verify_47e,
    _paragraph_locator,
)
from test_ui_research_third_changed_basis_session_adoption import (
    _adopt_ui,
    _reach_47c,
    _third_edge_direct,
)
from test_ui_research_third_changed_basis_transition import (
    _continuation,
    _press,
)


def _direct_47e_verification(tmp_path: Path, *, stem: str):
    _, lineage, prepared, transition, root, edge = _third_edge_direct(
        tmp_path,
        stem=stem,
    )
    adoption = adopt_chromium_research_third_changed_basis_governed_session(
        edge,
        edge_source=edge.persistence.path,
        declaration_destination=tmp_path / f"{stem}-adoption-declaration.json",
    )
    item = prepared.appended_items[0]
    verification = verify_chromium_research_third_changed_basis_epoch_reentry(
        adoption,
        lineage.overlay_source,
        (_paragraph_locator(item),),
        changed_working_set_source=prepared.working_set_persistence.path,
        changed_note_source=prepared.note_persistence.path,
        transition_source=transition.persistence.path,
        root_source=root.persistence.path,
        first_edge_source=edge.persistence.path,
        declaration_source=adoption.declaration.path,
    )
    return lineage, verification


def test_47f_application_persists_exact_47e_proof_through_public_40b(
    tmp_path: Path,
) -> None:
    lineage, verification = _direct_47e_verification(tmp_path, stem="47f-app")
    destination = tmp_path / "47f-app.overlay.json"

    result = persist_chromium_research_third_changed_basis_epoch_reentry_overlay(
        verification,
        prior_second_basis_epoch_continuation_overlay_source=lineage.overlay_source,
        destination=destination,
    )

    assert isinstance(result, ChromiumResearchThirdChangedBasisEpochReentryOverlayResult)
    assert result.verification_result is verification
    assert result.checkpoint.reentry is verification.fresh_reentry
    assert result.checkpoint.persistence.path == destination.resolve()
    assert (
        load_chromium_research_third_basis_epoch_reentry_plan_document(destination)
        == result.checkpoint.plan
    )
    assert (
        result.checkpoint.plan.prior_second_basis_epoch_continuation_overlay_source
        == lineage.overlay_source.resolve()
    )
    original = verification.fresh_reentry.plan
    candidate = result.checkpoint.plan
    for field_name in (
        "appended_working_set_members",
        "changed_working_set_source",
        "changed_note_source",
        "transition_source",
        "root_source",
        "declared_edge_sources",
        "declaration_source",
    ):
        assert getattr(candidate, field_name) == getattr(original, field_name)

    with pytest.raises(
        TypeError,
        match="exactly ChromiumResearchThirdChangedBasisEpochReentryResult",
    ):
        persist_chromium_research_third_changed_basis_epoch_reentry_overlay(
            object(),  # type: ignore[arg-type]
            prior_second_basis_epoch_continuation_overlay_source=lineage.overlay_source,
            destination=tmp_path / "wrong-type.overlay.json",
        )


def test_47f_wrong_prior_overlay_rejects_before_write_and_existing_destination_survives(
    tmp_path: Path,
) -> None:
    lineage, verification = _direct_47e_verification(tmp_path, stem="47f-negative")
    wrong_destination = tmp_path / "47f-wrong-prior.overlay.json"

    with pytest.raises(Exception):
        persist_chromium_research_third_changed_basis_epoch_reentry_overlay(
            verification,
            prior_second_basis_epoch_continuation_overlay_source=(
                verification.fresh_reentry.plan.root_source
            ),
            destination=wrong_destination,
        )
    assert not wrong_destination.exists()

    existing = tmp_path / "47f-existing.overlay.json"
    existing.write_text("sentinel\n", encoding="utf-8")
    with pytest.raises(Exception):
        persist_chromium_research_third_changed_basis_epoch_reentry_overlay(
            verification,
            prior_second_basis_epoch_continuation_overlay_source=lineage.overlay_source,
            destination=existing,
        )
    assert existing.read_text(encoding="utf-8") == "sentinel\n"


async def _persist_47f(shell, pilot, *, prior_overlay: Path, destination: Path) -> None:
    shell.query_one(
        "#research-third-changed-basis-epoch-reentry-overlay-prior-continuation-overlay-source",
        Input,
    ).value = str(prior_overlay)
    shell.query_one(
        "#research-third-changed-basis-epoch-reentry-overlay-destination",
        Input,
    ).value = str(destination)
    await _press(shell, pilot, "persist-research-third-changed-basis-epoch-reentry-overlay")


@pytest.mark.asyncio
async def test_47f_ui_persists_historical_47e_target_after_later_mounted_rollover(
    tmp_path: Path,
) -> None:
    _, overlay, _, lineage = _continuation(tmp_path, stem="47f-ui")
    member, _ = _new_paragraph_member(tmp_path, stem="47f-ui-member")
    shell = create_third_changed_basis_epoch_reentry_overlay_research_session_shell(
        lineage
    )
    shell.configure_changed_basis_candidate((member,))

    async with shell.run_test(size=(230, 840)) as pilot:
        await pilot.pause()
        assert len(shell.query(ResearchThirdChangedBasisEpochReentryOverlayControls)) == 0
        prepared, transition, root, edge = await _reach_47c(
            shell,
            pilot,
            tmp_path,
            stem="47f-ui",
        )
        await _adopt_ui(
            shell,
            pilot,
            edge,
            tmp_path / "47f-ui-adoption-declaration.json",
        )
        adoption = shell.last_third_changed_basis_session_adoption
        assert adoption is not None
        await _fill_and_verify_47e(
            shell,
            pilot,
            prior_overlay=overlay,
            prepared=prepared,
            transition=transition,
            root=root,
            edge=edge,
            adoption=adoption,
        )
        verification = shell.last_third_changed_basis_epoch_reentry_verification
        assert verification is not None

        controls = shell.query_one(ResearchThirdChangedBasisEpochReentryOverlayControls)
        prior_input = controls.query_one(
            "#research-third-changed-basis-epoch-reentry-overlay-prior-continuation-overlay-source",
            Input,
        )
        destination_input = controls.query_one(
            "#research-third-changed-basis-epoch-reentry-overlay-destination",
            Input,
        )
        assert prior_input.value == ""
        assert destination_input.value == ""

        successor = tmp_path / "47f-ui-later-edge.json"
        shell.query_one("#research-endpoint-revised-note", TextArea).text = (
            "Later mounted continuation after the historical 47E proof."
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
        ).value = str(tmp_path / "47f-ui-later-declaration.json")
        await _press(shell, pilot, "rollover-research-session")

        later_controller = shell.research_controller
        later_session = shell.research_session
        later_reentry = shell.research_reentry
        historical_continuation = shell.second_basis_epoch_continuation_reentry

        destination = tmp_path / "47f-ui.overlay.json"
        await _persist_47f(
            shell,
            pilot,
            prior_overlay=overlay,
            destination=destination,
        )

        result = shell.last_third_changed_basis_epoch_reentry_overlay
        assert result is not None
        assert result.verification_result is verification
        assert result.checkpoint.reentry is verification.fresh_reentry
        assert shell.research_controller is later_controller
        assert shell.research_session is later_session
        assert shell.research_reentry is later_reentry
        assert shell.second_basis_epoch_continuation_reentry is historical_continuation
        assert prior_input.disabled
        assert destination_input.disabled
        assert controls.query_one(
            "#persist-research-third-changed-basis-epoch-reentry-overlay", Button
        ).disabled


@pytest.mark.asyncio
async def test_47f_raw_38f_launch_remains_exactly_pathless_and_current_state_unchanged(
    tmp_path: Path,
) -> None:
    _, overlay, reentry, _ = _continuation(tmp_path, stem="47f-raw")
    member, _ = _new_paragraph_member(tmp_path, stem="47f-raw-member")
    shell = (
        create_inspectable_third_changed_basis_epoch_reentry_overlay_handoff_research_session_shell(
            reentry
        )
    )
    shell.configure_changed_basis_candidate((member,))
    panel = shell.second_basis_epoch_authority_inspection
    launch = panel.launch_provenance
    assert launch.launch_location_context is None

    async with shell.run_test(size=(230, 840)) as pilot:
        await pilot.pause()
        prepared, transition, root, edge = await _reach_47c(
            shell,
            pilot,
            tmp_path,
            stem="47f-raw",
        )
        await _adopt_ui(
            shell,
            pilot,
            edge,
            tmp_path / "47f-raw-adoption-declaration.json",
        )
        adoption = shell.last_third_changed_basis_session_adoption
        assert adoption is not None
        await _fill_and_verify_47e(
            shell,
            pilot,
            prior_overlay=overlay,
            prepared=prepared,
            transition=transition,
            root=root,
            edge=edge,
            adoption=adoption,
        )
        current_before = panel.current_state
        mounted_controller = shell.research_controller
        await _persist_47f(
            shell,
            pilot,
            prior_overlay=overlay,
            destination=tmp_path / "47f-raw.overlay.json",
        )

        result = shell.last_third_changed_basis_epoch_reentry_overlay
        assert result is not None
        assert panel.launch_provenance is launch
        assert panel.launch_provenance.launch_location_context is None
        assert panel.current_state is current_before
        assert shell.research_controller is mounted_controller


@pytest.mark.asyncio
async def test_plain_47e_product_does_not_gain_47f_persistence_surface(
    tmp_path: Path,
) -> None:
    _, overlay, _, lineage = _continuation(tmp_path, stem="47f-plain")
    member, _ = _new_paragraph_member(tmp_path, stem="47f-plain-member")
    shell = create_third_changed_basis_epoch_reentry_research_session_shell(lineage)
    shell.configure_changed_basis_candidate((member,))

    async with shell.run_test(size=(225, 760)) as pilot:
        await pilot.pause()
        prepared, transition, root, edge = await _reach_47c(
            shell,
            pilot,
            tmp_path,
            stem="47f-plain",
        )
        await _adopt_ui(
            shell,
            pilot,
            edge,
            tmp_path / "47f-plain-adoption-declaration.json",
        )
        adoption = shell.last_third_changed_basis_session_adoption
        assert adoption is not None
        await _fill_and_verify_47e(
            shell,
            pilot,
            prior_overlay=overlay,
            prepared=prepared,
            transition=transition,
            root=root,
            edge=edge,
            adoption=adoption,
        )
        assert shell.last_third_changed_basis_epoch_reentry_verification is not None
        assert not hasattr(shell, "last_third_changed_basis_epoch_reentry_overlay")
        assert len(shell.query(ResearchThirdChangedBasisEpochReentryOverlayControls)) == 0


def test_47f_product_factories_reject_wrong_authority_family() -> None:
    with pytest.raises(
        TypeError,
        match="ChromiumResearchSecondBasisEpochContinuationShellLineage",
    ):
        create_third_changed_basis_epoch_reentry_overlay_research_session_shell(object())  # type: ignore[arg-type]

    with pytest.raises(
        TypeError,
        match="exactly ChromiumResearchSecondBasisEpochContinuationReentryResult",
    ):
        create_third_changed_basis_epoch_reentry_overlay_handoff_research_session_shell(object())  # type: ignore[arg-type]
