from __future__ import annotations

from pathlib import Path

import pytest
from textual.widgets import Button, Input, Static, TextArea

from pyxis.app.chromium_research_third_changed_basis_revision_root import (
    ChromiumResearchThirdChangedBasisRevisionRootResult,
    persist_chromium_research_third_changed_basis_revision_root,
)
from pyxis.app.chromium_research_third_changed_basis_transition import (
    persist_chromium_research_third_changed_basis_transition,
)
from pyxis.ui.chromium_research_third_changed_basis_revision_root_textual import (
    ResearchThirdChangedBasisRevisionRootControls,
)
from pyxis.ui.third_changed_basis_revision_root_research_session_shell import (
    create_inspectable_third_changed_basis_revision_root_handoff_research_session_shell,
    create_inspectable_third_changed_basis_revision_root_research_session_shell,
    create_third_changed_basis_revision_root_handoff_research_session_shell,
    create_third_changed_basis_revision_root_research_session_shell,
)
from pyxis.ui.third_changed_basis_transition_research_session_shell import (
    create_third_changed_basis_transition_research_session_shell,
)
from test_app_chromium_research_session_working_set_extension import (
    _new_paragraph_member,
)
from test_ui_research_third_changed_basis_transition import (
    _continuation,
    _persist_third_transition,
    _prepare_direct,
    _prepare_in_shell,
    _press,
)


def _third_transition_direct(tmp_path: Path, *, stem: str):
    _, _, reentry, lineage = _continuation(tmp_path, stem=stem)
    member, _ = _new_paragraph_member(tmp_path, stem=f"{stem}-member")
    prepared = _prepare_direct(tmp_path, reentry, member, stem=stem)
    destination = tmp_path / f"{stem}-transition.json"
    transition = persist_chromium_research_third_changed_basis_transition(
        reentry.controller,
        reentry,
        prepared,
        prior_edge_source=reentry.controller.declared_endpoint.verification.path,
        working_set_source=prepared.working_set_persistence.path,
        note_source=prepared.note_persistence.path,
        destination=destination,
    )
    return reentry, lineage, prepared, transition


async def _persist_root_ui(
    shell,
    pilot,
    transition,
    *,
    destination: Path,
    rationale: str,
    prior_edge_source: Path | None = None,
    working_set_source: Path | None = None,
    note_source: Path | None = None,
    transition_source: Path | None = None,
) -> None:
    shell.query_one(
        "#research-third-changed-basis-revision-root-rationale", TextArea
    ).text = rationale
    shell.query_one(
        "#research-third-changed-basis-revision-root-prior-edge-source", Input
    ).value = str(
        prior_edge_source or transition.controller.declared_endpoint.verification.path
    )
    shell.query_one(
        "#research-third-changed-basis-revision-root-working-set-source", Input
    ).value = str(working_set_source or transition.prepared.working_set_persistence.path)
    shell.query_one(
        "#research-third-changed-basis-revision-root-note-source", Input
    ).value = str(note_source or transition.prepared.note_persistence.path)
    shell.query_one(
        "#research-third-changed-basis-revision-root-transition-source", Input
    ).value = str(transition_source or transition.persistence.path)
    shell.query_one(
        "#research-third-changed-basis-revision-root-destination", Input
    ).value = str(destination)
    await _press(shell, pilot, "persist-research-third-changed-basis-revision-root")


def test_47b_application_persists_and_freshly_relinks_exact_third_34a_root(
    tmp_path: Path,
) -> None:
    _, _, prepared, transition = _third_transition_direct(tmp_path, stem="47b-app")
    destination = tmp_path / "47b-app-root.json"
    revised_text = "First human rationale revision in the third evidence basis."

    result = persist_chromium_research_third_changed_basis_revision_root(
        transition,
        revised_note_text=revised_text,
        prior_edge_source=transition.controller.declared_endpoint.verification.path,
        working_set_source=prepared.working_set_persistence.path,
        note_source=prepared.note_persistence.path,
        transition_source=transition.persistence.path,
        destination=destination,
    )

    assert isinstance(result, ChromiumResearchThirdChangedBasisRevisionRootResult)
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

    noop_destination = tmp_path / "47b-noop-root.json"
    with pytest.raises(ValueError, match="differ exactly"):
        persist_chromium_research_third_changed_basis_revision_root(
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
        match="exactly ChromiumResearchThirdChangedBasisTransitionResult",
    ):
        persist_chromium_research_third_changed_basis_revision_root(
            object(),  # type: ignore[arg-type]
            revised_note_text="Must not write.",
            prior_edge_source=transition.controller.declared_endpoint.verification.path,
            working_set_source=prepared.working_set_persistence.path,
            note_source=prepared.note_persistence.path,
            transition_source=transition.persistence.path,
            destination=tmp_path / "47b-wrong-type-root.json",
        )
    assert not (tmp_path / "47b-wrong-type-root.json").exists()


def test_47b_explicit_paths_support_moves_and_wrong_transition_rejects_without_overwrite(
    tmp_path: Path,
) -> None:
    _, _, prepared, transition = _third_transition_direct(tmp_path, stem="47b-paths")
    moved_working_set = tmp_path / "moved-third-working-set.json"
    moved_note = tmp_path / "moved-third-note.json"
    moved_transition = tmp_path / "moved-third-transition.json"
    prepared.working_set_persistence.path.rename(moved_working_set)
    prepared.note_persistence.path.rename(moved_note)
    transition.persistence.path.rename(moved_transition)

    result = persist_chromium_research_third_changed_basis_revision_root(
        transition,
        revised_note_text="Third root after explicit durable-location changes.",
        prior_edge_source=transition.controller.declared_endpoint.verification.path,
        working_set_source=moved_working_set,
        note_source=moved_note,
        transition_source=moved_transition,
        destination=tmp_path / "47b-moved-root.json",
    )
    assert result.loaded_root.transition.verification.path == moved_transition.resolve()
    assert result.loaded_root.transition.successor_note.verification.path == moved_note.resolve()
    assert (
        result.loaded_root.transition.successor_note.working_set.verification.path
        == moved_working_set.resolve()
    )

    _, _, prepared2, transition2 = _third_transition_direct(tmp_path, stem="47b-wrong")
    wrong_destination = tmp_path / "47b-wrong-root.json"
    with pytest.raises(Exception):
        persist_chromium_research_third_changed_basis_revision_root(
            transition2,
            revised_note_text="Valid new wording with an explicitly wrong transition source.",
            prior_edge_source=transition2.controller.declared_endpoint.verification.path,
            working_set_source=prepared2.working_set_persistence.path,
            note_source=prepared2.note_persistence.path,
            transition_source=prepared2.note_persistence.path,
            destination=wrong_destination,
        )
    assert not wrong_destination.exists()

    existing = tmp_path / "47b-existing-root.json"
    existing.write_text("preserve exactly\n", encoding="utf-8")
    with pytest.raises(Exception):
        persist_chromium_research_third_changed_basis_revision_root(
            transition2,
            revised_note_text="A different valid human rationale.",
            prior_edge_source=transition2.controller.declared_endpoint.verification.path,
            working_set_source=prepared2.working_set_persistence.path,
            note_source=prepared2.note_persistence.path,
            transition_source=transition2.persistence.path,
            destination=existing,
        )
    assert existing.read_text(encoding="utf-8") == "preserve exactly\n"


@pytest.mark.asyncio
async def test_47b_shell_mounts_only_after_47a_and_persists_without_adoption(
    tmp_path: Path,
) -> None:
    _, _, _, lineage = _continuation(tmp_path, stem="47b-ui")
    member, _ = _new_paragraph_member(tmp_path, stem="47b-ui-member")
    shell = create_third_changed_basis_revision_root_research_session_shell(lineage)
    shell.configure_changed_basis_candidate((member,))
    original_controller = shell.research_controller
    original_session = shell.research_session
    original_reentry = shell.second_basis_epoch_continuation_reentry

    async with shell.run_test(size=(195, 340)) as pilot:
        await pilot.pause()
        assert len(shell.query(ResearchThirdChangedBasisRevisionRootControls)) == 0

        prepared = await _prepare_in_shell(shell, pilot, tmp_path, stem="47b-ui")
        assert len(shell.query(ResearchThirdChangedBasisRevisionRootControls)) == 0
        await _persist_third_transition(
            shell,
            pilot,
            prepared,
            tmp_path / "47b-ui-transition.json",
        )
        transition = shell.last_third_changed_basis_transition
        assert transition is not None

        controls = shell.query_one(ResearchThirdChangedBasisRevisionRootControls)
        summary = str(
            shell.query_one(
                "#research-third-changed-basis-revision-root-transition-summary", Static
            ).content
        )
        assert "PERSISTED THIRD CHANGED-BASIS TRANSITION" in summary
        assert "NOT YET ROOTED / NOT ADOPTED" in summary
        assert transition.persistence.transition_record_sha256 in summary
        assert shell.query_one(
            "#research-third-changed-basis-revision-root-rationale", TextArea
        ).text == ""
        for widget_id in (
            "#research-third-changed-basis-revision-root-prior-edge-source",
            "#research-third-changed-basis-revision-root-working-set-source",
            "#research-third-changed-basis-revision-root-note-source",
            "#research-third-changed-basis-revision-root-transition-source",
            "#research-third-changed-basis-revision-root-destination",
        ):
            assert shell.query_one(widget_id, Input).value == ""

        await _persist_root_ui(
            shell,
            pilot,
            transition,
            destination=tmp_path / "47b-ui-root.json",
            rationale="  Third changed-basis root rationale 😀\nStill human-owned.  ",
        )

        result = shell.last_third_changed_basis_revision_root
        assert result is not None
        assert result.transition_result is transition
        assert shell.research_controller is original_controller
        assert shell.research_session is original_session
        assert shell.second_basis_epoch_continuation_reentry is original_reentry
        assert controls.prior_result is result
        assert shell.query_one(
            "#persist-research-third-changed-basis-revision-root", Button
        ).disabled
        receipt = str(
            shell.query_one(
                "#research-third-changed-basis-revision-root-status", Static
            ).content
        )
        assert "Mounted second-epoch continuation unchanged" in receipt
        assert "No first post-root edge" in receipt
        assert len(shell.query("#persist-research-third-root-edge")) == 0
        assert len(shell.query("#adopt-third-basis-epoch")) == 0


@pytest.mark.asyncio
async def test_47b_historical_third_transition_can_receive_root_after_older_branch_rollover(
    tmp_path: Path,
) -> None:
    _, _, _, lineage = _continuation(tmp_path, stem="47b-history")
    member, _ = _new_paragraph_member(tmp_path, stem="47b-history-member")
    shell = create_third_changed_basis_revision_root_research_session_shell(lineage)
    shell.configure_changed_basis_candidate((member,))

    async with shell.run_test(size=(195, 360)) as pilot:
        await pilot.pause()
        prepared = await _prepare_in_shell(shell, pilot, tmp_path, stem="47b-history")
        await _persist_third_transition(
            shell,
            pilot,
            prepared,
            tmp_path / "47b-history-transition.json",
        )
        transition = shell.last_third_changed_basis_transition
        assert transition is not None
        root_controls = shell.query_one(ResearchThirdChangedBasisRevisionRootControls)

        successor = tmp_path / "47b-history-successor.json"
        shell.query_one("#research-endpoint-revised-note", TextArea).text = (
            "The older second-epoch branch continues after the third transition persisted."
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
        ).value = str(tmp_path / "47b-history-declaration.json")
        await _press(shell, pilot, "rollover-research-session")

        assert shell.research_controller is not transition.controller
        assert root_controls.prior_result is None
        assert not shell.query_one(
            "#persist-research-third-changed-basis-revision-root", Button
        ).disabled

        current_reentry = shell.second_basis_epoch_continuation_reentry
        await _persist_root_ui(
            shell,
            pilot,
            transition,
            destination=tmp_path / "47b-history-root.json",
            rationale=(
                "The historical third transition receives its explicit root after "
                "the older second-epoch branch continued."
            ),
        )

        result = shell.last_third_changed_basis_revision_root
        assert result is not None
        assert result.transition_result is transition
        assert (
            result.loaded_root.transition.verification.transition_record_sha256
            == transition.persistence.transition_record_sha256
        )
        assert shell.research_controller is not transition.controller
        assert shell.second_basis_epoch_continuation_reentry is current_reentry


@pytest.mark.asyncio
async def test_47b_persisted_and_raw_launch_provenance_remains_exactly_unchanged(
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
        create_inspectable_third_changed_basis_revision_root_research_session_shell(
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

    async with persisted_shell.run_test(size=(195, 340)) as pilot:
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
        transition = persisted_shell.last_third_changed_basis_transition
        assert transition is not None
        await _persist_root_ui(
            persisted_shell,
            pilot,
            transition,
            destination=persisted_dir / "persisted-third-root.json",
            rationale="Persisted-launch third root rationale.",
        )
        assert persisted_shell.last_third_changed_basis_revision_root is not None
        assert persisted_panel.launch_provenance is persisted_launch
        assert persisted_panel.current_state is persisted_current
        assert persisted_launch.launch_location_context == persisted_overlay.resolve()

    _, _, raw_reentry, _ = _continuation(raw_dir, stem="raw")
    raw_shell = (
        create_inspectable_third_changed_basis_revision_root_handoff_research_session_shell(
            raw_reentry
        )
    )
    raw_member, _ = _new_paragraph_member(raw_dir, stem="raw-member")
    raw_shell.configure_changed_basis_candidate((raw_member,))
    raw_panel = raw_shell.second_basis_epoch_authority_inspection
    raw_launch = raw_panel.launch_provenance
    raw_current = raw_panel.current_state
    assert raw_launch.launch_location_context is None

    async with raw_shell.run_test(size=(195, 340)) as pilot:
        await pilot.pause()
        prepared = await _prepare_in_shell(raw_shell, pilot, raw_dir, stem="raw")
        await _persist_third_transition(
            raw_shell,
            pilot,
            prepared,
            raw_dir / "raw-third-transition.json",
        )
        transition = raw_shell.last_third_changed_basis_transition
        assert transition is not None
        await _persist_root_ui(
            raw_shell,
            pilot,
            transition,
            destination=raw_dir / "raw-third-root.json",
            rationale="Pathless-launch third root rationale.",
        )
        assert raw_shell.last_third_changed_basis_revision_root is not None
        assert raw_shell.second_basis_epoch_continuation_handoff_reentry is raw_reentry
        assert raw_panel.launch_provenance is raw_launch
        assert raw_panel.current_state is raw_current
        assert raw_launch.launch_location_context is None


@pytest.mark.asyncio
async def test_plain_47a_product_does_not_gain_47b_surface(tmp_path: Path) -> None:
    _, _, _, lineage = _continuation(tmp_path, stem="47b-plain")
    member, _ = _new_paragraph_member(tmp_path, stem="47b-plain-member")
    shell = create_third_changed_basis_transition_research_session_shell(lineage)
    shell.configure_changed_basis_candidate((member,))

    async with shell.run_test(size=(190, 280)) as pilot:
        await pilot.pause()
        prepared = await _prepare_in_shell(shell, pilot, tmp_path, stem="47b-plain")
        await _persist_third_transition(
            shell,
            pilot,
            prepared,
            tmp_path / "47b-plain-transition.json",
        )
        assert shell.last_third_changed_basis_transition is not None
        assert not hasattr(shell, "last_third_changed_basis_revision_root")
        assert len(shell.query(ResearchThirdChangedBasisRevisionRootControls)) == 0


def test_47b_product_factories_reject_wrong_authority_family() -> None:
    with pytest.raises(
        TypeError,
        match="ChromiumResearchSecondBasisEpochContinuationShellLineage",
    ):
        create_third_changed_basis_revision_root_research_session_shell(object())  # type: ignore[arg-type]

    with pytest.raises(
        TypeError,
        match="exactly ChromiumResearchSecondBasisEpochContinuationReentryResult",
    ):
        create_third_changed_basis_revision_root_handoff_research_session_shell(object())  # type: ignore[arg-type]
