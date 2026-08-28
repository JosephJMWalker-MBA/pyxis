from __future__ import annotations

from pathlib import Path

import pytest
from textual.widgets import Button, Input, Static, TextArea

from pyxis.app.chromium_research_first_changed_basis_revision_root import (
    ChromiumResearchFirstChangedBasisRevisionRootResult,
    persist_chromium_research_first_changed_basis_revision_root,
)
from pyxis.app.chromium_research_first_changed_basis_transition import (
    persist_chromium_research_first_changed_basis_transition,
)
from pyxis.ui import (
    FirstChangedBasisRootResearchSessionShell,
    create_first_changed_basis_research_session_shell,
    create_first_changed_basis_root_research_session_shell,
)
from pyxis.ui.chromium_research_first_changed_basis_revision_root_textual import (
    ResearchFirstChangedBasisRevisionRootControls,
)
from pyxis.ui.chromium_research_first_changed_basis_transition_textual import (
    ResearchFirstChangedBasisTransitionControls,
)
from test_app_chromium_research_session_working_set_extension import (
    _new_paragraph_member,
    _persist_extension,
    _session,
)
from test_ui_research_first_changed_basis_transition import _prepare, _press


async def _persist_transition_ui(shell, pilot, fixture, prepared, tmp_path: Path, *, stem: str):
    destination = tmp_path / f"{stem}-transition.json"
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
    ).value = str(destination)
    await _press(shell, pilot, "persist-research-first-changed-basis-transition")
    result = shell.last_first_changed_basis_transition
    assert result is not None
    return result, destination


def test_44c_application_persists_and_freshly_relinks_exact_34a_root(
    tmp_path: Path,
) -> None:
    fixture, reentry = _session(tmp_path)
    member, _ = _new_paragraph_member(tmp_path, stem="44c-app")
    prepared = _persist_extension(
        tmp_path,
        reentry,
        (member,),
        rationale_text="Prepared changed basis before the first transition.",
        stem="44c-app",
    )
    transition = persist_chromium_research_first_changed_basis_transition(
        reentry.controller,
        reentry,
        prepared,
        prior_edge_source=fixture.v6_path,
        working_set_source=prepared.working_set_persistence.path,
        note_source=prepared.note_persistence.path,
        destination=tmp_path / "44c-app-transition.json",
    )
    root_destination = tmp_path / "44c-app-root.json"
    revised_text = "First human rationale revision after the changed evidence basis."

    result = persist_chromium_research_first_changed_basis_revision_root(
        transition,
        revised_note_text=revised_text,
        prior_edge_source=fixture.v6_path,
        working_set_source=prepared.working_set_persistence.path,
        note_source=prepared.note_persistence.path,
        transition_source=transition.persistence.path,
        destination=root_destination,
    )

    assert isinstance(result, ChromiumResearchFirstChangedBasisRevisionRootResult)
    assert result.transition_result is transition
    assert result.persistence.root is result.root
    assert result.persistence.path == root_destination.resolve()
    assert result.loaded_root.verification.root_record_sha256 == result.persistence.root_record_sha256
    assert (
        result.loaded_root.transition.verification.transition_record_sha256
        == transition.persistence.transition_record_sha256
    )
    assert result.loaded_root.root.revision.revised_note.note_text == revised_text
    assert result.loaded_root.root.revision.prior_note is result.loaded_root.transition.successor_note.note

    noop_destination = tmp_path / "44c-noop-root.json"
    with pytest.raises(ValueError, match="differ exactly"):
        persist_chromium_research_first_changed_basis_revision_root(
            transition,
            revised_note_text=transition.loaded_transition.successor_note.note.note_text,
            prior_edge_source=fixture.v6_path,
            working_set_source=prepared.working_set_persistence.path,
            note_source=prepared.note_persistence.path,
            transition_source=transition.persistence.path,
            destination=noop_destination,
        )
    assert not noop_destination.exists()


def test_44c_application_accepts_moved_durable_inputs_only_via_explicit_paths(
    tmp_path: Path,
) -> None:
    fixture, reentry = _session(tmp_path)
    member, _ = _new_paragraph_member(tmp_path, stem="44c-moved")
    prepared = _persist_extension(
        tmp_path,
        reentry,
        (member,),
        rationale_text="Prepared basis whose durable records later move.",
        stem="44c-moved",
    )
    transition = persist_chromium_research_first_changed_basis_transition(
        reentry.controller,
        reentry,
        prepared,
        prior_edge_source=fixture.v6_path,
        working_set_source=prepared.working_set_persistence.path,
        note_source=prepared.note_persistence.path,
        destination=tmp_path / "44c-moved-transition.json",
    )

    moved_working_set = tmp_path / "44c-explicit-moved-working-set.json"
    moved_note = tmp_path / "44c-explicit-moved-note.json"
    moved_transition = tmp_path / "44c-explicit-moved-transition.json"
    prepared.working_set_persistence.path.rename(moved_working_set)
    prepared.note_persistence.path.rename(moved_note)
    transition.persistence.path.rename(moved_transition)

    result = persist_chromium_research_first_changed_basis_revision_root(
        transition,
        revised_note_text="Root after explicit durable-location changes.",
        prior_edge_source=fixture.v6_path,
        working_set_source=moved_working_set,
        note_source=moved_note,
        transition_source=moved_transition,
        destination=tmp_path / "44c-moved-root.json",
    )

    assert result.persistence.path.exists()
    assert result.loaded_root.transition.verification.path == moved_transition.resolve()
    assert result.loaded_root.transition.successor_note.verification.path == moved_note.resolve()
    assert (
        result.loaded_root.transition.successor_note.working_set.verification.path
        == moved_working_set.resolve()
    )


@pytest.mark.asyncio
async def test_first_root_shell_mounts_only_after_44b_success_and_persists_without_adoption(
    tmp_path: Path,
) -> None:
    fixture, reentry = _session(tmp_path)
    member, _ = _new_paragraph_member(tmp_path, stem="44c-ui")
    shell = create_first_changed_basis_root_research_session_shell(reentry, (member,))
    original_controller = shell.research_controller
    original_session = shell.research_session

    assert isinstance(shell, FirstChangedBasisRootResearchSessionShell)

    async with shell.run_test(size=(180, 260)) as pilot:
        await pilot.pause()
        assert len(shell.query(ResearchFirstChangedBasisRevisionRootControls)) == 0

        prepared = await _prepare(shell, pilot, tmp_path, stem="44c-ui")
        assert len(shell.query(ResearchFirstChangedBasisRevisionRootControls)) == 0
        transition, transition_path = await _persist_transition_ui(
            shell,
            pilot,
            fixture,
            prepared,
            tmp_path,
            stem="44c-ui",
        )

        controls = shell.query_one(ResearchFirstChangedBasisRevisionRootControls)
        summary = str(
            shell.query_one(
                "#research-first-changed-basis-revision-root-transition-summary", Static
            ).content
        )
        assert "PERSISTED FIRST CHANGED-BASIS TRANSITION" in summary
        assert "NOT YET ROOTED / NOT ADOPTED" in summary
        assert transition.persistence.transition_record_sha256 in summary
        assert transition.loaded_transition.successor_note.note.note_text in summary
        assert shell.query_one(
            "#research-first-changed-basis-revision-root-rationale", TextArea
        ).text == ""
        for widget_id in (
            "#research-first-changed-basis-revision-root-prior-edge-source",
            "#research-first-changed-basis-revision-root-working-set-source",
            "#research-first-changed-basis-revision-root-note-source",
            "#research-first-changed-basis-revision-root-transition-source",
            "#research-first-changed-basis-revision-root-destination",
        ):
            assert shell.query_one(widget_id, Input).value == ""

        revised_text = "  First changed-basis root rationale 😀\nStill human-owned.  "
        root_destination = tmp_path / "44c-ui-root.json"
        shell.query_one(
            "#research-first-changed-basis-revision-root-rationale", TextArea
        ).text = revised_text
        shell.query_one(
            "#research-first-changed-basis-revision-root-prior-edge-source", Input
        ).value = str(fixture.v6_path)
        shell.query_one(
            "#research-first-changed-basis-revision-root-working-set-source", Input
        ).value = str(prepared.working_set_persistence.path)
        shell.query_one(
            "#research-first-changed-basis-revision-root-note-source", Input
        ).value = str(prepared.note_persistence.path)
        shell.query_one(
            "#research-first-changed-basis-revision-root-transition-source", Input
        ).value = str(transition_path)
        shell.query_one(
            "#research-first-changed-basis-revision-root-destination", Input
        ).value = str(root_destination)
        await _press(shell, pilot, "persist-research-first-changed-basis-revision-root")

        result = shell.last_first_changed_basis_revision_root
        assert result is not None
        assert result.transition_result is transition
        assert result.loaded_root.root.revision.revised_note.note_text == revised_text
        assert shell.research_controller is original_controller
        assert shell.research_session is original_session
        assert controls.prior_result is result
        assert shell.query_one(
            "#persist-research-first-changed-basis-revision-root", Button
        ).disabled
        receipt = str(
            shell.query_one(
                "#research-first-changed-basis-revision-root-status", Static
            ).content
        )
        assert "Mounted governed session unchanged" in receipt
        assert "No 34B first edge" in receipt
        assert "35A declared root-backed session" in receipt
        assert root_destination.exists()
        assert len(shell.query("#persist-research-first-root-edge")) == 0
        assert len(shell.query("#adopt-root-backed-research-session")) == 0


@pytest.mark.asyncio
async def test_old_basis_rollover_after_44b_does_not_invalidate_exact_transition_root_authority(
    tmp_path: Path,
) -> None:
    fixture, reentry = _session(tmp_path)
    member, _ = _new_paragraph_member(tmp_path, stem="44c-branch")
    shell = create_first_changed_basis_root_research_session_shell(reentry, (member,))
    original_controller = shell.research_controller

    async with shell.run_test(size=(185, 275)) as pilot:
        await pilot.pause()
        prepared = await _prepare(shell, pilot, tmp_path, stem="44c-branch")
        transition, transition_path = await _persist_transition_ui(
            shell,
            pilot,
            fixture,
            prepared,
            tmp_path,
            stem="44c-branch",
        )
        root_controls = shell.query_one(ResearchFirstChangedBasisRevisionRootControls)

        successor = tmp_path / "44c-old-basis-successor.json"
        shell.query_one("#research-endpoint-revised-note", TextArea).text = (
            "Old-basis branch continues after the changed-basis transition was persisted."
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
        ).value = str(tmp_path / "44c-old-basis-declaration.json")
        await _press(shell, pilot, "rollover-research-session")

        assert shell.research_controller is not original_controller
        assert root_controls.prior_result is None
        assert not shell.query_one(
            "#persist-research-first-changed-basis-revision-root", Button
        ).disabled

        shell.query_one(
            "#research-first-changed-basis-revision-root-rationale", TextArea
        ).text = "Changed-basis branch receives its first explicit root after old-basis rollover."
        shell.query_one(
            "#research-first-changed-basis-revision-root-prior-edge-source", Input
        ).value = str(fixture.v6_path)
        shell.query_one(
            "#research-first-changed-basis-revision-root-working-set-source", Input
        ).value = str(prepared.working_set_persistence.path)
        shell.query_one(
            "#research-first-changed-basis-revision-root-note-source", Input
        ).value = str(prepared.note_persistence.path)
        shell.query_one(
            "#research-first-changed-basis-revision-root-transition-source", Input
        ).value = str(transition_path)
        shell.query_one(
            "#research-first-changed-basis-revision-root-destination", Input
        ).value = str(tmp_path / "44c-branch-root.json")
        await _press(shell, pilot, "persist-research-first-changed-basis-revision-root")

        root_result = shell.last_first_changed_basis_revision_root
        assert root_result is not None
        assert root_result.transition_result is transition
        assert (
            root_result.loaded_root.transition.verification.transition_record_sha256
            == transition.persistence.transition_record_sha256
        )
        assert shell.research_controller is not original_controller


@pytest.mark.asyncio
async def test_plain_44b_shell_never_gains_44c_root_controls_after_transition_success(
    tmp_path: Path,
) -> None:
    fixture, reentry = _session(tmp_path)
    member, _ = _new_paragraph_member(tmp_path, stem="44c-plain-44b")
    shell = create_first_changed_basis_research_session_shell(reentry, (member,))

    async with shell.run_test(size=(175, 210)) as pilot:
        await pilot.pause()
        prepared = await _prepare(shell, pilot, tmp_path, stem="44c-plain-44b")
        await _persist_transition_ui(
            shell,
            pilot,
            fixture,
            prepared,
            tmp_path,
            stem="44c-plain-44b",
        )
        assert shell.last_first_changed_basis_transition is not None
        assert len(shell.query(ResearchFirstChangedBasisRevisionRootControls)) == 0
        assert not hasattr(shell, "last_first_changed_basis_revision_root")


@pytest.mark.asyncio
async def test_wrong_transition_locator_rejects_44c_without_root_write(
    tmp_path: Path,
) -> None:
    fixture, reentry = _session(tmp_path)
    member, _ = _new_paragraph_member(tmp_path, stem="44c-wrong")
    shell = create_first_changed_basis_root_research_session_shell(reentry, (member,))

    async with shell.run_test(size=(180, 250)) as pilot:
        await pilot.pause()
        prepared = await _prepare(shell, pilot, tmp_path, stem="44c-wrong")
        await _persist_transition_ui(
            shell,
            pilot,
            fixture,
            prepared,
            tmp_path,
            stem="44c-wrong",
        )
        destination = tmp_path / "44c-wrong-root.json"
        shell.query_one(
            "#research-first-changed-basis-revision-root-rationale", TextArea
        ).text = "A valid new rationale with the wrong transition locator."
        shell.query_one(
            "#research-first-changed-basis-revision-root-prior-edge-source", Input
        ).value = str(fixture.v6_path)
        shell.query_one(
            "#research-first-changed-basis-revision-root-working-set-source", Input
        ).value = str(prepared.working_set_persistence.path)
        shell.query_one(
            "#research-first-changed-basis-revision-root-note-source", Input
        ).value = str(prepared.note_persistence.path)
        shell.query_one(
            "#research-first-changed-basis-revision-root-transition-source", Input
        ).value = str(prepared.note_persistence.path)
        shell.query_one(
            "#research-first-changed-basis-revision-root-destination", Input
        ).value = str(destination)
        await _press(shell, pilot, "persist-research-first-changed-basis-revision-root")

        assert shell.last_first_changed_basis_revision_root is None
        assert not destination.exists()
        status = str(
            shell.query_one(
                "#research-first-changed-basis-revision-root-status", Static
            ).content
        )
        assert status.startswith("Root failed:")
