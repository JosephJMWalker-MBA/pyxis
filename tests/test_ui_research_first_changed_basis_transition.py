from __future__ import annotations

from pathlib import Path

import pytest
from textual.widgets import Button, Input, Static, TextArea

from pyxis.app.chromium_research_first_changed_basis_transition import (
    ChromiumResearchFirstChangedBasisTransitionResult,
    persist_chromium_research_first_changed_basis_transition,
)
from pyxis.ui import (
    FirstChangedBasisResearchSessionShell,
    create_first_changed_basis_research_session_shell,
    create_research_session_shell,
)
from pyxis.ui.chromium_research_first_changed_basis_transition_textual import (
    ResearchFirstChangedBasisTransitionControls,
)
from test_app_chromium_research_session_working_set_extension import (
    _new_paragraph_member,
    _persist_extension,
    _session,
)


async def _press(shell, pilot, button_id: str) -> None:
    button = shell.query_one(f"#{button_id}", Button)
    button.focus()
    await pilot.pause()
    await pilot.press("enter")
    await pilot.pause()


async def _prepare(shell, pilot, tmp_path: Path, *, stem: str = "prepared"):
    working_set_destination = tmp_path / f"{stem}-working-set.json"
    note_destination = tmp_path / f"{stem}-working-set-note.json"
    shell.query_one("#research-changed-basis-rationale", TextArea).text = (
        "Explicit changed-basis rationale before transition."
    )
    shell.query_one(
        "#research-changed-basis-working-set-destination", Input
    ).value = str(working_set_destination)
    shell.query_one("#research-changed-basis-note-destination", Input).value = str(
        note_destination
    )
    await _press(shell, pilot, "persist-research-changed-basis-preparation")
    result = shell.last_changed_basis_preparation
    assert result is not None
    return result


def test_application_boundary_requires_exact_ordinary_reentry_and_freshly_relinks_transition(
    tmp_path: Path,
) -> None:
    fixture, reentry = _session(tmp_path)
    member, _ = _new_paragraph_member(tmp_path, stem="44b-app")
    prepared = _persist_extension(
        tmp_path,
        reentry,
        (member,),
        rationale_text="Prepared basis for direct 44B application proof.",
        stem="44b-app",
    )
    destination = tmp_path / "44b-transition.json"

    result = persist_chromium_research_first_changed_basis_transition(
        reentry.controller,
        reentry,
        prepared,
        prior_edge_source=fixture.v6_path,
        working_set_source=prepared.working_set_persistence.path,
        note_source=prepared.note_persistence.path,
        destination=destination,
    )

    assert isinstance(result, ChromiumResearchFirstChangedBasisTransitionResult)
    assert result.controller is reentry.controller
    assert result.ordinary_reentry is reentry
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

    with pytest.raises(TypeError, match="exactly ChromiumResearchSessionReentryResult"):
        persist_chromium_research_first_changed_basis_transition(
            reentry.controller,
            object(),  # type: ignore[arg-type]
            prepared,
            prior_edge_source=fixture.v6_path,
            working_set_source=prepared.working_set_persistence.path,
            note_source=prepared.note_persistence.path,
            destination=tmp_path / "should-not-write.json",
        )


def test_application_boundary_accepts_moved_prepared_files_only_via_explicit_new_paths(
    tmp_path: Path,
) -> None:
    fixture, reentry = _session(tmp_path)
    member, _ = _new_paragraph_member(tmp_path, stem="44b-moved")
    prepared = _persist_extension(
        tmp_path,
        reentry,
        (member,),
        rationale_text="Prepared basis whose durable files move explicitly.",
        stem="44b-moved",
    )
    moved_working_set = tmp_path / "moved-working-set.json"
    moved_note = tmp_path / "moved-working-set-note.json"
    prepared.working_set_persistence.path.rename(moved_working_set)
    prepared.note_persistence.path.rename(moved_note)

    result = persist_chromium_research_first_changed_basis_transition(
        reentry.controller,
        reentry,
        prepared,
        prior_edge_source=fixture.v6_path,
        working_set_source=moved_working_set,
        note_source=moved_note,
        destination=tmp_path / "moved-transition.json",
    )

    assert result.persistence.path.exists()
    assert result.persistence.fresh_successor_note.verification.path == moved_note.resolve()
    assert (
        result.persistence.fresh_successor_note.working_set.verification.path
        == moved_working_set.resolve()
    )


@pytest.mark.asyncio
async def test_first_transition_shell_mounts_only_after_44a_success_and_persists_without_session_adoption(
    tmp_path: Path,
) -> None:
    fixture, reentry = _session(tmp_path)
    member, _ = _new_paragraph_member(tmp_path, stem="44b-ui")
    shell = create_first_changed_basis_research_session_shell(reentry, (member,))
    original_controller = shell.research_controller
    original_session = shell.research_session
    original_endpoint = shell.research_controller.declared_endpoint

    assert isinstance(shell, FirstChangedBasisResearchSessionShell)

    async with shell.run_test(size=(170, 190)) as pilot:
        await pilot.pause()
        assert len(shell.query(ResearchFirstChangedBasisTransitionControls)) == 0

        prepared = await _prepare(shell, pilot, tmp_path, stem="44b-ui")
        controls = shell.query_one(ResearchFirstChangedBasisTransitionControls)
        summary = str(
            shell.query_one(
                "#research-first-changed-basis-transition-prepared-summary", Static
            ).content
        )
        assert "PREPARED CHANGED BASIS" in summary
        assert "NOT YET TRANSITIONED / NOT ROOTED" in summary
        assert prepared.working_set_persistence.working_set_record_sha256 in summary
        assert prepared.note_persistence.note_record_sha256 in summary

        for widget_id in (
            "#research-first-changed-basis-transition-prior-edge-source",
            "#research-first-changed-basis-transition-working-set-source",
            "#research-first-changed-basis-transition-note-source",
            "#research-first-changed-basis-transition-destination",
        ):
            assert shell.query_one(widget_id, Input).value == ""

        transition_destination = tmp_path / "44b-ui-transition.json"
        shell.query_one(
            "#research-first-changed-basis-transition-prior-edge-source", Input
        ).value = str(fixture.v6_path)
        shell.query_one(
            "#research-first-changed-basis-transition-working-set-source", Input
        ).value = str(prepared.working_set_persistence.path)
        shell.query_one(
            "#research-first-changed-basis-transition-note-source", Input
        ).value = str(prepared.note_persistence.path)
        shell.query_one(
            "#research-first-changed-basis-transition-destination", Input
        ).value = str(transition_destination)
        await _press(shell, pilot, "persist-research-first-changed-basis-transition")

        result = shell.last_first_changed_basis_transition
        assert result is not None
        assert result.prepared is prepared
        assert shell.research_controller is original_controller
        assert shell.research_session is original_session
        assert shell.research_controller.declared_endpoint is original_endpoint
        assert controls.prior_result is result
        assert shell.query_one(
            "#persist-research-first-changed-basis-transition", Button
        ).disabled
        receipt = str(
            shell.query_one(
                "#research-first-changed-basis-transition-status", Static
            ).content
        )
        assert "Mounted governed session unchanged" in receipt
        assert "no root/epoch was created" in receipt
        assert "not itself a root-backed declared session" in receipt
        assert transition_destination.exists()
        assert len(shell.query("#create-research-transition-revision-root")) == 0
        assert len(shell.query("#adopt-root-backed-research-session")) == 0


@pytest.mark.asyncio
async def test_unadopted_endpoint_revision_does_not_stale_first_transition(
    tmp_path: Path,
) -> None:
    fixture, reentry = _session(tmp_path)
    member, _ = _new_paragraph_member(tmp_path, stem="44b-unadopted")
    shell = create_first_changed_basis_research_session_shell(reentry, (member,))
    original_endpoint = shell.research_controller.declared_endpoint

    async with shell.run_test(size=(170, 195)) as pilot:
        await pilot.pause()
        prepared = await _prepare(shell, pilot, tmp_path, stem="44b-unadopted")
        controls = shell.query_one(ResearchFirstChangedBasisTransitionControls)

        successor = tmp_path / "44b-unadopted-successor.json"
        shell.query_one("#research-endpoint-revised-note", TextArea).text = (
            "Unadopted endpoint write remains outside 44B prior authority."
        )
        shell.query_one("#research-endpoint-prior-edge-source", Input).value = str(
            fixture.v6_path
        )
        shell.query_one("#research-endpoint-destination", Input).value = str(successor)
        await _press(shell, pilot, "persist-research-endpoint-revision")

        assert shell.research_controller.declared_endpoint is original_endpoint
        assert not controls.stale
        assert not shell.query_one(
            "#persist-research-first-changed-basis-transition", Button
        ).disabled

        shell.query_one(
            "#research-first-changed-basis-transition-prior-edge-source", Input
        ).value = str(fixture.v6_path)
        shell.query_one(
            "#research-first-changed-basis-transition-working-set-source", Input
        ).value = str(prepared.working_set_persistence.path)
        shell.query_one(
            "#research-first-changed-basis-transition-note-source", Input
        ).value = str(prepared.note_persistence.path)
        shell.query_one(
            "#research-first-changed-basis-transition-destination", Input
        ).value = str(tmp_path / "44b-after-unadopted-transition.json")
        await _press(shell, pilot, "persist-research-first-changed-basis-transition")

        assert shell.last_first_changed_basis_transition is not None
        assert shell.last_first_changed_basis_transition.transition.prior_endpoint is original_endpoint


@pytest.mark.asyncio
async def test_adopted_rollover_stales_unsaved_first_transition_without_retargeting(
    tmp_path: Path,
) -> None:
    fixture, reentry = _session(tmp_path)
    member, _ = _new_paragraph_member(tmp_path, stem="44b-stale")
    shell = create_first_changed_basis_research_session_shell(reentry, (member,))
    original_controller = shell.research_controller

    async with shell.run_test(size=(170, 200)) as pilot:
        await pilot.pause()
        await _prepare(shell, pilot, tmp_path, stem="44b-stale")
        transition_controls = shell.query_one(
            ResearchFirstChangedBasisTransitionControls
        )

        successor = tmp_path / "44b-chosen-successor.json"
        shell.query_one("#research-endpoint-revised-note", TextArea).text = (
            "Chosen ordinary continuation before changed-basis transition."
        )
        shell.query_one("#research-endpoint-prior-edge-source", Input).value = str(
            fixture.v6_path
        )
        shell.query_one("#research-endpoint-destination", Input).value = str(successor)
        await _press(shell, pilot, "persist-research-endpoint-revision")
        shell.query_one("#research-session-rollover-successor-source", Input).value = str(
            successor
        )
        shell.query_one(
            "#research-session-rollover-declaration-destination", Input
        ).value = str(tmp_path / "44b-rollover-declaration.json")
        await _press(shell, pilot, "rollover-research-session")

        assert shell.research_controller is not original_controller
        assert transition_controls.stale
        assert transition_controls.prior_result is None
        assert shell.query_one(
            "#persist-research-first-changed-basis-transition", Button
        ).disabled
        for widget_id in (
            "#research-first-changed-basis-transition-prior-edge-source",
            "#research-first-changed-basis-transition-working-set-source",
            "#research-first-changed-basis-transition-note-source",
            "#research-first-changed-basis-transition-destination",
        ):
            assert shell.query_one(widget_id, Input).disabled
        status = str(
            shell.query_one(
                "#research-first-changed-basis-transition-status", Static
            ).content
        )
        assert "will not silently retarget" in status
        assert shell.last_first_changed_basis_transition is None


@pytest.mark.asyncio
async def test_plain_44a_shell_without_ordinary_reentry_never_gains_44b_transition_controls(
    tmp_path: Path,
) -> None:
    _, reentry = _session(tmp_path)
    member, _ = _new_paragraph_member(tmp_path, stem="44b-no-reentry")
    shell = create_research_session_shell(reentry.controller)
    shell.configure_changed_basis_candidate((member,))

    async with shell.run_test(size=(160, 160)) as pilot:
        await pilot.pause()
        await _prepare(shell, pilot, tmp_path, stem="44b-no-reentry")
        assert shell.last_changed_basis_preparation is not None
        assert len(shell.query(ResearchFirstChangedBasisTransitionControls)) == 0
        assert not hasattr(shell, "last_first_changed_basis_transition")
