from __future__ import annotations

from pathlib import Path

import pytest
from textual.widgets import Button, Input, Static, TextArea

from pyxis.app.chromium_research_root_backed_session_shell_lineage import (
    prove_chromium_research_root_backed_session_continuation_shell_lineage,
)
from pyxis.app.chromium_research_second_changed_basis_revision_root import (
    ChromiumResearchSecondChangedBasisRevisionRootResult,
    persist_chromium_research_second_changed_basis_revision_root,
)
from pyxis.app.chromium_research_second_changed_basis_transition import (
    ChromiumResearchSecondChangedBasisTransitionResult,
    persist_chromium_research_second_changed_basis_transition,
)
from pyxis.ui.chromium_research_second_changed_basis_revision_root_textual import (
    ResearchSecondChangedBasisRevisionRootControls,
)
from pyxis.ui.root_backed_authority_inspection_shell import (
    create_inspectable_root_backed_continuation_handoff_research_session_shell,
    create_inspectable_root_backed_continuation_research_session_shell,
)
from pyxis.ui.root_backed_continuation_research_session_shell import (
    create_root_backed_continuation_research_session_shell,
)
from test_app_chromium_research_session_working_set_extension import (
    _new_paragraph_member,
)
from test_ui_research_second_changed_basis_transition import (
    _continuation,
    _persist_second_transition,
    _prepare_direct,
    _prepare_in_shell,
    _press,
)


def _second_transition_direct(tmp_path: Path, *, stem: str):
    values, reentry = _continuation(tmp_path, stem=stem)
    member, _ = _new_paragraph_member(tmp_path, stem=f"{stem}-member")
    prepared = _prepare_direct(tmp_path, reentry, member, stem=stem)
    destination = tmp_path / f"{stem}-transition.json"
    transition = persist_chromium_research_second_changed_basis_transition(
        reentry.controller,
        reentry,
        prepared,
        prior_edge_source=reentry.controller.declared_endpoint.verification.path,
        working_set_source=prepared.working_set_persistence.path,
        note_source=prepared.note_persistence.path,
        destination=destination,
    )
    return values, reentry, prepared, transition


async def _persist_root_ui(
    shell,
    pilot,
    transition: ChromiumResearchSecondChangedBasisTransitionResult,
    *,
    destination: Path,
    rationale: str,
) -> None:
    shell.query_one(
        "#research-second-changed-basis-revision-root-rationale", TextArea
    ).text = rationale
    shell.query_one(
        "#research-second-changed-basis-revision-root-prior-edge-source", Input
    ).value = str(transition.controller.declared_endpoint.verification.path)
    shell.query_one(
        "#research-second-changed-basis-revision-root-working-set-source", Input
    ).value = str(transition.prepared.working_set_persistence.path)
    shell.query_one(
        "#research-second-changed-basis-revision-root-note-source", Input
    ).value = str(transition.prepared.note_persistence.path)
    shell.query_one(
        "#research-second-changed-basis-revision-root-transition-source", Input
    ).value = str(transition.persistence.path)
    shell.query_one(
        "#research-second-changed-basis-revision-root-destination", Input
    ).value = str(destination)
    await _press(shell, pilot, "persist-research-second-changed-basis-revision-root")


def test_46b_application_persists_and_freshly_relinks_exact_second_34a_root(
    tmp_path: Path,
) -> None:
    _, _, prepared, transition = _second_transition_direct(tmp_path, stem="46b-app")
    destination = tmp_path / "46b-app-root.json"
    revised_text = "First human rationale revision in the second evidence basis."

    result = persist_chromium_research_second_changed_basis_revision_root(
        transition,
        revised_note_text=revised_text,
        prior_edge_source=transition.controller.declared_endpoint.verification.path,
        working_set_source=prepared.working_set_persistence.path,
        note_source=prepared.note_persistence.path,
        transition_source=transition.persistence.path,
        destination=destination,
    )

    assert isinstance(result, ChromiumResearchSecondChangedBasisRevisionRootResult)
    assert result.transition_result is transition
    assert result.persistence.root is result.root
    assert result.persistence.path == destination.resolve()
    assert (
        result.loaded_root.verification.root_record_sha256
        == result.persistence.root_record_sha256
    )
    assert (
        result.loaded_root.transition.verification.transition_record_sha256
        == transition.persistence.transition_record_sha256
    )
    assert result.loaded_root.root.revision.revised_note.note_text == revised_text
    assert (
        result.loaded_root.root.revision.prior_note
        is result.loaded_root.transition.successor_note.note
    )

    noop_destination = tmp_path / "46b-noop-root.json"
    with pytest.raises(ValueError, match="differ exactly"):
        persist_chromium_research_second_changed_basis_revision_root(
            transition,
            revised_note_text=transition.loaded_transition.successor_note.note.note_text,
            prior_edge_source=transition.controller.declared_endpoint.verification.path,
            working_set_source=prepared.working_set_persistence.path,
            note_source=prepared.note_persistence.path,
            transition_source=transition.persistence.path,
            destination=noop_destination,
        )
    assert not noop_destination.exists()

    with pytest.raises(
        TypeError,
        match="exactly ChromiumResearchSecondChangedBasisTransitionResult",
    ):
        persist_chromium_research_second_changed_basis_revision_root(
            object(),  # type: ignore[arg-type]
            revised_note_text="Must not write.",
            prior_edge_source=transition.controller.declared_endpoint.verification.path,
            working_set_source=prepared.working_set_persistence.path,
            note_source=prepared.note_persistence.path,
            transition_source=transition.persistence.path,
            destination=tmp_path / "46b-wrong-type-root.json",
        )
    assert not (tmp_path / "46b-wrong-type-root.json").exists()


def test_46b_application_accepts_moved_durable_inputs_only_via_explicit_paths(
    tmp_path: Path,
) -> None:
    _, _, prepared, transition = _second_transition_direct(tmp_path, stem="46b-moved")
    moved_working_set = tmp_path / "46b-explicit-moved-working-set.json"
    moved_note = tmp_path / "46b-explicit-moved-note.json"
    moved_transition = tmp_path / "46b-explicit-moved-transition.json"
    prepared.working_set_persistence.path.rename(moved_working_set)
    prepared.note_persistence.path.rename(moved_note)
    transition.persistence.path.rename(moved_transition)

    result = persist_chromium_research_second_changed_basis_revision_root(
        transition,
        revised_note_text="Second root after explicit durable-location changes.",
        prior_edge_source=transition.controller.declared_endpoint.verification.path,
        working_set_source=moved_working_set,
        note_source=moved_note,
        transition_source=moved_transition,
        destination=tmp_path / "46b-moved-root.json",
    )

    assert result.loaded_root.transition.verification.path == moved_transition.resolve()
    assert result.loaded_root.transition.successor_note.verification.path == moved_note.resolve()
    assert (
        result.loaded_root.transition.successor_note.working_set.verification.path
        == moved_working_set.resolve()
    )


def test_46b_wrong_transition_locator_rejects_before_root_write(tmp_path: Path) -> None:
    _, _, prepared, transition = _second_transition_direct(tmp_path, stem="46b-wrong")
    destination = tmp_path / "46b-wrong-root.json"

    with pytest.raises(Exception):
        persist_chromium_research_second_changed_basis_revision_root(
            transition,
            revised_note_text="Valid new wording with an explicitly wrong transition source.",
            prior_edge_source=transition.controller.declared_endpoint.verification.path,
            working_set_source=prepared.working_set_persistence.path,
            note_source=prepared.note_persistence.path,
            transition_source=prepared.note_persistence.path,
            destination=destination,
        )

    assert not destination.exists()


@pytest.mark.asyncio
async def test_46b_shell_mounts_only_after_46a_success_and_persists_without_adoption(
    tmp_path: Path,
) -> None:
    _, reentry = _continuation(tmp_path, stem="46b-ui")
    member, _ = _new_paragraph_member(tmp_path, stem="46b-ui-member")
    shell = create_root_backed_continuation_research_session_shell(reentry)
    shell.configure_changed_basis_candidate((member,))
    original_controller = shell.research_controller
    original_session = shell.research_session
    original_reentry = shell.root_backed_continuation_reentry

    async with shell.run_test(size=(190, 300)) as pilot:
        await pilot.pause()
        assert len(shell.query(ResearchSecondChangedBasisRevisionRootControls)) == 0

        prepared = await _prepare_in_shell(shell, pilot, tmp_path, stem="46b-ui")
        assert len(shell.query(ResearchSecondChangedBasisRevisionRootControls)) == 0
        await _persist_second_transition(
            shell,
            pilot,
            prepared,
            tmp_path / "46b-ui-transition.json",
        )
        transition = shell.last_second_changed_basis_transition
        assert transition is not None

        controls = shell.query_one(ResearchSecondChangedBasisRevisionRootControls)
        summary = str(
            shell.query_one(
                "#research-second-changed-basis-revision-root-transition-summary", Static
            ).content
        )
        assert "PERSISTED SECOND CHANGED-BASIS TRANSITION" in summary
        assert "NOT YET ROOTED / NOT ADOPTED" in summary
        assert transition.persistence.transition_record_sha256 in summary
        assert shell.query_one(
            "#research-second-changed-basis-revision-root-rationale", TextArea
        ).text == ""
        for widget_id in (
            "#research-second-changed-basis-revision-root-prior-edge-source",
            "#research-second-changed-basis-revision-root-working-set-source",
            "#research-second-changed-basis-revision-root-note-source",
            "#research-second-changed-basis-revision-root-transition-source",
            "#research-second-changed-basis-revision-root-destination",
        ):
            assert shell.query_one(widget_id, Input).value == ""

        await _persist_root_ui(
            shell,
            pilot,
            transition,
            destination=tmp_path / "46b-ui-root.json",
            rationale="  Second changed-basis root rationale 😀\nStill human-owned.  ",
        )

        result = shell.last_second_changed_basis_revision_root
        assert result is not None
        assert result.transition_result is transition
        assert shell.research_controller is original_controller
        assert shell.research_session is original_session
        assert shell.root_backed_continuation_reentry is original_reentry
        assert controls.prior_result is result
        assert shell.query_one(
            "#persist-research-second-changed-basis-revision-root", Button
        ).disabled
        receipt = str(
            shell.query_one(
                "#research-second-changed-basis-revision-root-status", Static
            ).content
        )
        assert "Mounted one-root continuation unchanged" in receipt
        assert "No 34B first edge" in receipt
        assert len(shell.query("#persist-research-second-root-edge")) == 0
        assert len(shell.query("#adopt-second-basis-epoch")) == 0


@pytest.mark.asyncio
async def test_46b_historical_transition_root_authority_survives_later_one_root_rollover(
    tmp_path: Path,
) -> None:
    _, reentry = _continuation(tmp_path, stem="46b-history")
    member, _ = _new_paragraph_member(tmp_path, stem="46b-history-member")
    shell = create_root_backed_continuation_research_session_shell(reentry)
    shell.configure_changed_basis_candidate((member,))

    async with shell.run_test(size=(195, 320)) as pilot:
        await pilot.pause()
        prepared = await _prepare_in_shell(shell, pilot, tmp_path, stem="46b-history")
        await _persist_second_transition(
            shell,
            pilot,
            prepared,
            tmp_path / "46b-history-transition.json",
        )
        transition = shell.last_second_changed_basis_transition
        assert transition is not None
        root_controls = shell.query_one(ResearchSecondChangedBasisRevisionRootControls)

        successor = tmp_path / "46b-history-successor.json"
        shell.query_one("#research-endpoint-revised-note", TextArea).text = (
            "The older one-root branch continues after the second transition was persisted."
        )
        shell.query_one("#research-endpoint-prior-edge-source", Input).value = str(
            transition.controller.declared_endpoint.verification.path
        )
        shell.query_one("#research-endpoint-destination", Input).value = str(successor)
        await _press(shell, pilot, "persist-research-endpoint-revision")
        shell.query_one("#research-session-rollover-successor-source", Input).value = str(
            successor
        )
        shell.query_one(
            "#research-session-rollover-declaration-destination", Input
        ).value = str(tmp_path / "46b-history-declaration.json")
        await _press(shell, pilot, "rollover-research-session")

        assert shell.research_controller is not transition.controller
        assert root_controls.prior_result is None
        assert not shell.query_one(
            "#persist-research-second-changed-basis-revision-root", Button
        ).disabled

        await _persist_root_ui(
            shell,
            pilot,
            transition,
            destination=tmp_path / "46b-history-root.json",
            rationale=(
                "The historical second transition receives its explicit root after "
                "the older one-root branch continued."
            ),
        )

        result = shell.last_second_changed_basis_revision_root
        assert result is not None
        assert result.transition_result is transition
        assert (
            result.loaded_root.transition.verification.transition_record_sha256
            == transition.persistence.transition_record_sha256
        )
        assert shell.research_controller is not transition.controller
        assert shell.root_backed_continuation_reentry is reentry


@pytest.mark.asyncio
async def test_46b_persisted_and_raw_inspection_provenance_remains_unchanged(
    tmp_path: Path,
) -> None:
    persisted_dir = tmp_path / "persisted"
    raw_dir = tmp_path / "raw"
    persisted_dir.mkdir()
    raw_dir.mkdir()

    persisted_values, persisted_reentry = _continuation(persisted_dir, stem="persisted")
    persisted_overlay = persisted_values[8]
    persisted_lineage = prove_chromium_research_root_backed_session_continuation_shell_lineage(
        persisted_reentry,
        overlay_source=persisted_overlay,
    )
    persisted_shell = create_inspectable_root_backed_continuation_research_session_shell(
        persisted_lineage
    )
    persisted_member, _ = _new_paragraph_member(
        persisted_dir,
        stem="persisted-46b-member",
    )
    persisted_shell.configure_changed_basis_candidate((persisted_member,))
    persisted_launch = persisted_shell.root_backed_authority_inspection.launch_provenance

    async with persisted_shell.run_test(size=(195, 300)) as pilot:
        await pilot.pause()
        prepared = await _prepare_in_shell(
            persisted_shell,
            pilot,
            persisted_dir,
            stem="persisted-46b",
        )
        await _persist_second_transition(
            persisted_shell,
            pilot,
            prepared,
            persisted_dir / "persisted-46b-transition.json",
        )
        transition = persisted_shell.last_second_changed_basis_transition
        assert transition is not None
        await _persist_root_ui(
            persisted_shell,
            pilot,
            transition,
            destination=persisted_dir / "persisted-46b-root.json",
            rationale="Persisted-launch second root rationale.",
        )
        assert persisted_shell.last_second_changed_basis_revision_root is not None
        assert persisted_shell.root_backed_authority_inspection.launch_provenance is persisted_launch
        assert persisted_launch.launch_location_context == persisted_overlay.resolve()

    _, raw_reentry = _continuation(raw_dir, stem="raw")
    raw_shell = create_inspectable_root_backed_continuation_handoff_research_session_shell(
        raw_reentry
    )
    raw_member, _ = _new_paragraph_member(raw_dir, stem="raw-46b-member")
    raw_shell.configure_changed_basis_candidate((raw_member,))
    raw_launch = raw_shell.root_backed_authority_inspection.launch_provenance
    assert raw_launch.launch_location_context is None

    async with raw_shell.run_test(size=(195, 300)) as pilot:
        await pilot.pause()
        prepared = await _prepare_in_shell(raw_shell, pilot, raw_dir, stem="raw-46b")
        await _persist_second_transition(
            raw_shell,
            pilot,
            prepared,
            raw_dir / "raw-46b-transition.json",
        )
        transition = raw_shell.last_second_changed_basis_transition
        assert transition is not None
        await _persist_root_ui(
            raw_shell,
            pilot,
            transition,
            destination=raw_dir / "raw-46b-root.json",
            rationale="Raw-handoff second root rationale.",
        )
        assert raw_shell.last_second_changed_basis_revision_root is not None
        assert raw_shell.root_backed_authority_inspection.launch_provenance is raw_launch
        assert raw_launch.launch_location_context is None
