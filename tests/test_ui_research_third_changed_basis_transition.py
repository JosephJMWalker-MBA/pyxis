from __future__ import annotations

from pathlib import Path

import pytest
from textual.widgets import Button, Input, Static, TextArea

from pyxis.app.chromium_research_second_basis_epoch_continuation_reentry_plan_document import (
    reenter_chromium_research_second_basis_epoch_continuation,
)
from pyxis.app.chromium_research_second_basis_epoch_shell_lineage import (
    prove_chromium_research_second_basis_epoch_continuation_shell_lineage,
)
from pyxis.app.chromium_research_session_working_set_extension import (
    persist_chromium_research_session_working_set_extension,
)
from pyxis.app.chromium_research_third_changed_basis_transition import (
    ChromiumResearchThirdChangedBasisTransitionError,
    ChromiumResearchThirdChangedBasisTransitionResult,
    persist_chromium_research_third_changed_basis_transition,
)
from pyxis.ui.chromium_research_third_changed_basis_transition_textual import (
    ResearchThirdChangedBasisTransitionControls,
)
from pyxis.ui.second_basis_epoch_research_session_shell import (
    create_second_basis_epoch_continuation_research_session_shell,
)
from pyxis.ui.third_changed_basis_transition_research_session_shell import (
    create_inspectable_third_changed_basis_transition_handoff_research_session_shell,
    create_inspectable_third_changed_basis_transition_research_session_shell,
    create_third_changed_basis_transition_handoff_research_session_shell,
    create_third_changed_basis_transition_research_session_shell,
)
from test_app_chromium_research_second_basis_epoch_continuation_reentry_plan_document import (
    _persist_valid_continuation,
)
from test_app_chromium_research_session_working_set_extension import (
    _new_paragraph_member,
)


async def _press(shell, pilot, button_id: str) -> None:
    button = shell.query_one(f"#{button_id}", Button)
    button.focus()
    await pilot.pause()
    await pilot.press("enter")
    await pilot.pause()


def _continuation(tmp_path: Path, *, stem: str):
    values = _persist_valid_continuation(tmp_path, stem=stem)
    overlay = values[6]
    earned = values[8].fresh_reentry
    lineage = prove_chromium_research_second_basis_epoch_continuation_shell_lineage(
        earned,
        overlay_source=overlay,
    )
    # Persisted second-epoch shells launch from the fresh proof-carrying re-entry,
    # not the pre-proof earned object supplied to the lineage verifier.
    return values, overlay, lineage.reentry, lineage


def _prepare_direct(tmp_path: Path, reentry, member, *, stem: str):
    return persist_chromium_research_session_working_set_extension(
        reentry.controller,
        (member,),
        rationale_text="Explicit third evidence-basis rationale.",
        working_set_destination=tmp_path / f"{stem}-working-set.json",
        note_destination=tmp_path / f"{stem}-working-set-note.json",
    )


async def _prepare_in_shell(shell, pilot, tmp_path: Path, *, stem: str):
    shell.query_one("#research-changed-basis-rationale", TextArea).text = (
        "Explicit third evidence-basis rationale in the live second-epoch continuation."
    )
    shell.query_one(
        "#research-changed-basis-working-set-destination", Input
    ).value = str(tmp_path / f"{stem}-working-set.json")
    shell.query_one("#research-changed-basis-note-destination", Input).value = str(
        tmp_path / f"{stem}-working-set-note.json"
    )
    await _press(shell, pilot, "persist-research-changed-basis-preparation")
    prepared = shell.last_changed_basis_preparation
    assert prepared is not None
    return prepared


async def _persist_third_transition(shell, pilot, prepared, destination: Path) -> None:
    shell.query_one(
        "#research-third-changed-basis-transition-prior-edge-source", Input
    ).value = str(shell.research_controller.declared_endpoint.verification.path)
    shell.query_one(
        "#research-third-changed-basis-transition-working-set-source", Input
    ).value = str(prepared.working_set_persistence.path)
    shell.query_one(
        "#research-third-changed-basis-transition-note-source", Input
    ).value = str(prepared.note_persistence.path)
    shell.query_one(
        "#research-third-changed-basis-transition-destination", Input
    ).value = str(destination)
    await _press(shell, pilot, "persist-research-third-changed-basis-transition")


def test_47a_application_requires_exact_second_epoch_continuation_and_reuses_public_33b(
    tmp_path: Path,
) -> None:
    _, _, reentry, _ = _continuation(tmp_path, stem="47a-app")
    member, _ = _new_paragraph_member(tmp_path, stem="47a-app-member")
    prepared = _prepare_direct(tmp_path, reentry, member, stem="47a-app")
    destination = tmp_path / "47a-transition.json"

    result = persist_chromium_research_third_changed_basis_transition(
        reentry.controller,
        reentry,
        prepared,
        prior_edge_source=reentry.controller.declared_endpoint.verification.path,
        working_set_source=prepared.working_set_persistence.path,
        note_source=prepared.note_persistence.path,
        destination=destination,
    )

    assert isinstance(result, ChromiumResearchThirdChangedBasisTransitionResult)
    assert result.controller is reentry.controller
    assert result.continuation_reentry is reentry
    assert result.prepared is prepared
    assert result.persistence.transition is result.transition
    assert result.persistence.path == destination.resolve()
    assert (
        result.loaded_transition.verification.transition_record_sha256
        == result.persistence.transition_record_sha256
    )
    assert (
        result.loaded_transition.prior_endpoint.verification.edge_record_sha256
        == reentry.controller.declared_endpoint.verification.edge_record_sha256
    )
    assert (
        result.loaded_transition.successor_note.working_set.verification.working_set_record_sha256
        == prepared.working_set_persistence.working_set_record_sha256
    )
    assert (
        result.loaded_transition.successor_note.verification.note_record_sha256
        == prepared.note_persistence.note_record_sha256
    )

    with pytest.raises(
        TypeError,
        match="exactly ChromiumResearchSecondBasisEpochContinuationReentryResult",
    ):
        persist_chromium_research_third_changed_basis_transition(
            reentry.controller,
            object(),  # type: ignore[arg-type]
            prepared,
            prior_edge_source=reentry.controller.declared_endpoint.verification.path,
            working_set_source=prepared.working_set_persistence.path,
            note_source=prepared.note_persistence.path,
            destination=tmp_path / "must-not-write-wrong-type.json",
        )
    assert not (tmp_path / "must-not-write-wrong-type.json").exists()


def test_47a_rejects_structurally_equivalent_fresh_controller_without_exact_object_identity(
    tmp_path: Path,
) -> None:
    _, _, reentry, _ = _continuation(tmp_path, stem="47a-identity")
    equivalent = reenter_chromium_research_second_basis_epoch_continuation(reentry.plan)
    assert equivalent is not reentry
    assert equivalent.controller is not reentry.controller
    assert equivalent.controller.presentation == reentry.controller.presentation

    member, _ = _new_paragraph_member(tmp_path, stem="47a-identity-member")
    prepared = _prepare_direct(tmp_path, reentry, member, stem="47a-identity")
    destination = tmp_path / "must-not-write-equivalent-controller.json"

    with pytest.raises(
        ChromiumResearchThirdChangedBasisTransitionError,
        match="exact controller object",
    ):
        persist_chromium_research_third_changed_basis_transition(
            reentry.controller,
            equivalent,
            prepared,
            prior_edge_source=reentry.controller.declared_endpoint.verification.path,
            working_set_source=prepared.working_set_persistence.path,
            note_source=prepared.note_persistence.path,
            destination=destination,
        )
    assert not destination.exists()


def test_47a_application_accepts_moved_preparation_only_through_explicit_current_paths(
    tmp_path: Path,
) -> None:
    _, _, reentry, _ = _continuation(tmp_path, stem="47a-moved")
    member, _ = _new_paragraph_member(tmp_path, stem="47a-moved-member")
    prepared = _prepare_direct(tmp_path, reentry, member, stem="47a-moved")
    moved_working_set = tmp_path / "moved-third-working-set.json"
    moved_note = tmp_path / "moved-third-working-set-note.json"
    prepared.working_set_persistence.path.rename(moved_working_set)
    prepared.note_persistence.path.rename(moved_note)

    result = persist_chromium_research_third_changed_basis_transition(
        reentry.controller,
        reentry,
        prepared,
        prior_edge_source=reentry.controller.declared_endpoint.verification.path,
        working_set_source=moved_working_set,
        note_source=moved_note,
        destination=tmp_path / "moved-third-transition.json",
    )

    assert result.persistence.fresh_successor_note.verification.path == moved_note.resolve()
    assert (
        result.persistence.fresh_successor_note.working_set.verification.path
        == moved_working_set.resolve()
    )


@pytest.mark.parametrize("wrong_locator", ["prior", "working-set", "note"])
def test_47a_wrong_explicit_locator_rejects_without_successful_destination(
    tmp_path: Path,
    wrong_locator: str,
) -> None:
    _, _, reentry, _ = _continuation(tmp_path, stem=f"47a-wrong-{wrong_locator}")
    member, _ = _new_paragraph_member(
        tmp_path,
        stem=f"47a-wrong-{wrong_locator}-member",
    )
    prepared = _prepare_direct(
        tmp_path,
        reentry,
        member,
        stem=f"47a-wrong-{wrong_locator}",
    )
    destination = tmp_path / f"must-not-write-{wrong_locator}.json"

    prior = reentry.controller.declared_endpoint.verification.path
    working_set = prepared.working_set_persistence.path
    note = prepared.note_persistence.path
    missing = tmp_path / f"missing-{wrong_locator}.json"
    if wrong_locator == "prior":
        prior = missing
    elif wrong_locator == "working-set":
        working_set = missing
    else:
        note = missing

    with pytest.raises(Exception):
        persist_chromium_research_third_changed_basis_transition(
            reentry.controller,
            reentry,
            prepared,
            prior_edge_source=prior,
            working_set_source=working_set,
            note_source=note,
            destination=destination,
        )
    assert not destination.exists()


def test_47a_existing_destination_survives_no_overwrite_failure(tmp_path: Path) -> None:
    _, _, reentry, _ = _continuation(tmp_path, stem="47a-existing")
    member, _ = _new_paragraph_member(tmp_path, stem="47a-existing-member")
    prepared = _prepare_direct(tmp_path, reentry, member, stem="47a-existing")
    destination = tmp_path / "existing-third-transition.json"
    destination.write_text("preserve exactly\n", encoding="utf-8")

    with pytest.raises(Exception):
        persist_chromium_research_third_changed_basis_transition(
            reentry.controller,
            reentry,
            prepared,
            prior_edge_source=reentry.controller.declared_endpoint.verification.path,
            working_set_source=prepared.working_set_persistence.path,
            note_source=prepared.note_persistence.path,
            destination=destination,
        )
    assert destination.read_text(encoding="utf-8") == "preserve exactly\n"


@pytest.mark.asyncio
async def test_47a_persisted_product_mounts_only_after_44a_and_does_not_adopt_transition(
    tmp_path: Path,
) -> None:
    _, _, _, lineage = _continuation(tmp_path, stem="47a-ui")
    member, _ = _new_paragraph_member(tmp_path, stem="47a-ui-member")
    shell = create_third_changed_basis_transition_research_session_shell(lineage)
    shell.configure_changed_basis_candidate((member,))
    original_controller = shell.research_controller
    original_session = shell.research_session
    original_reentry = shell.second_basis_epoch_continuation_reentry

    async with shell.run_test(size=(190, 250)) as pilot:
        await pilot.pause()
        assert len(shell.query(ResearchThirdChangedBasisTransitionControls)) == 0
        prepared = await _prepare_in_shell(shell, pilot, tmp_path, stem="47a-ui")
        controls = shell.query_one(ResearchThirdChangedBasisTransitionControls)
        summary = str(
            shell.query_one(
                "#research-third-changed-basis-transition-prepared-summary",
                Static,
            ).content
        )
        assert "PREPARED THIRD CHANGED BASIS" in summary
        assert "NOT YET TRANSITIONED / NOT ROOTED" in summary
        for widget_id in (
            "#research-third-changed-basis-transition-prior-edge-source",
            "#research-third-changed-basis-transition-working-set-source",
            "#research-third-changed-basis-transition-note-source",
            "#research-third-changed-basis-transition-destination",
        ):
            assert shell.query_one(widget_id, Input).value == ""

        destination = tmp_path / "47a-ui-transition.json"
        await _persist_third_transition(shell, pilot, prepared, destination)
        result = shell.last_third_changed_basis_transition
        assert result is not None
        assert result.continuation_reentry is original_reentry
        assert result.prepared is prepared
        assert shell.research_controller is original_controller
        assert shell.research_session is original_session
        assert shell.second_basis_epoch_continuation_reentry is original_reentry
        assert controls.prior_result is result
        assert shell.query_one(
            "#persist-research-third-changed-basis-transition", Button
        ).disabled
        receipt = str(
            shell.query_one(
                "#research-third-changed-basis-transition-status", Static
            ).content
        )
        assert "Mounted governed second-epoch continuation unchanged" in receipt
        assert "no third root/epoch was created" in receipt
        assert destination.exists()
        assert len(shell.query("#research-third-changed-basis-revision-root-controls")) == 0
        assert len(shell.query("#adopt-third-basis-epoch")) == 0


@pytest.mark.asyncio
async def test_47a_rollover_stales_unsaved_transition_without_retargeting(
    tmp_path: Path,
) -> None:
    _, _, reentry, lineage = _continuation(tmp_path, stem="47a-stale")
    member, _ = _new_paragraph_member(tmp_path, stem="47a-stale-member")
    shell = create_third_changed_basis_transition_research_session_shell(lineage)
    shell.configure_changed_basis_candidate((member,))

    async with shell.run_test(size=(190, 280)) as pilot:
        await pilot.pause()
        await _prepare_in_shell(shell, pilot, tmp_path, stem="47a-stale")
        controls = shell.query_one(ResearchThirdChangedBasisTransitionControls)
        successor = tmp_path / "47a-stale-successor.json"
        shell.query_one("#research-endpoint-revised-note", TextArea).text = (
            "Explicit one-hop second-epoch continuation before saving the third basis transition."
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
        ).value = str(tmp_path / "47a-stale-declaration.json")
        await _press(shell, pilot, "rollover-research-session")

        assert controls.stale
        assert controls.prior_result is None
        assert shell.query_one(
            "#persist-research-third-changed-basis-transition", Button
        ).disabled
        assert shell.last_third_changed_basis_transition is None
        assert shell.research_controller is not reentry.controller
        assert shell.second_basis_epoch_continuation_reentry is reentry
        status = str(
            shell.query_one(
                "#research-third-changed-basis-transition-status", Static
            ).content
        )
        assert "will not silently retarget" in status


@pytest.mark.asyncio
async def test_47a_persisted_and_raw_launch_provenance_remains_exactly_unchanged(
    tmp_path: Path,
) -> None:
    persisted_dir = tmp_path / "persisted"
    raw_dir = tmp_path / "raw"
    persisted_dir.mkdir()
    raw_dir.mkdir()

    _, persisted_overlay, _, persisted_lineage = _continuation(
        persisted_dir,
        stem="persisted",
    )
    persisted_shell = (
        create_inspectable_third_changed_basis_transition_research_session_shell(
            persisted_lineage
        )
    )
    persisted_member, _ = _new_paragraph_member(
        persisted_dir,
        stem="persisted-member",
    )
    persisted_shell.configure_changed_basis_candidate((persisted_member,))
    persisted_panel = persisted_shell.second_basis_epoch_authority_inspection
    persisted_launch = persisted_panel.launch_provenance
    persisted_current = persisted_panel.current_state

    async with persisted_shell.run_test(size=(190, 260)) as pilot:
        await pilot.pause()
        prepared = await _prepare_in_shell(
            persisted_shell,
            pilot,
            persisted_dir,
            stem="persisted",
        )
        await _persist_third_transition(
            persisted_shell,
            pilot,
            prepared,
            persisted_dir / "persisted-third-transition.json",
        )
        assert persisted_shell.last_third_changed_basis_transition is not None
        assert persisted_panel.launch_provenance is persisted_launch
        assert persisted_panel.current_state is persisted_current
        assert persisted_launch.launch_location_context == persisted_overlay.resolve()

    _, _, raw_reentry, _ = _continuation(raw_dir, stem="raw")
    raw_shell = (
        create_inspectable_third_changed_basis_transition_handoff_research_session_shell(
            raw_reentry
        )
    )
    raw_member, _ = _new_paragraph_member(raw_dir, stem="raw-member")
    raw_shell.configure_changed_basis_candidate((raw_member,))
    raw_panel = raw_shell.second_basis_epoch_authority_inspection
    raw_launch = raw_panel.launch_provenance
    raw_current = raw_panel.current_state
    assert raw_launch.launch_location_context is None

    async with raw_shell.run_test(size=(190, 260)) as pilot:
        await pilot.pause()
        prepared = await _prepare_in_shell(raw_shell, pilot, raw_dir, stem="raw")
        await _persist_third_transition(
            raw_shell,
            pilot,
            prepared,
            raw_dir / "raw-third-transition.json",
        )
        assert raw_shell.last_third_changed_basis_transition is not None
        assert raw_shell.second_basis_epoch_continuation_handoff_reentry is raw_reentry
        assert raw_panel.launch_provenance is raw_launch
        assert raw_panel.current_state is raw_current
        assert raw_launch.launch_location_context is None


@pytest.mark.asyncio
async def test_plain_second_epoch_continuation_does_not_gain_47a_surface(
    tmp_path: Path,
) -> None:
    _, _, _, lineage = _continuation(tmp_path, stem="47a-plain")
    member, _ = _new_paragraph_member(tmp_path, stem="47a-plain-member")
    shell = create_second_basis_epoch_continuation_research_session_shell(lineage)
    shell.configure_changed_basis_candidate((member,))

    async with shell.run_test(size=(180, 220)) as pilot:
        await pilot.pause()
        await _prepare_in_shell(shell, pilot, tmp_path, stem="47a-plain")
        assert shell.last_changed_basis_preparation is not None
        assert not hasattr(shell, "last_third_changed_basis_transition")
        assert len(shell.query(ResearchThirdChangedBasisTransitionControls)) == 0


def test_47a_product_factories_reject_wrong_authority_family() -> None:
    with pytest.raises(
        TypeError,
        match="ChromiumResearchSecondBasisEpochContinuationShellLineage",
    ):
        create_third_changed_basis_transition_research_session_shell(object())  # type: ignore[arg-type]

    with pytest.raises(
        TypeError,
        match="exactly ChromiumResearchSecondBasisEpochContinuationReentryResult",
    ):
        create_third_changed_basis_transition_handoff_research_session_shell(object())  # type: ignore[arg-type]
