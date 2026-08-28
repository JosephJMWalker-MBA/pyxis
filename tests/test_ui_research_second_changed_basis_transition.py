from __future__ import annotations

from pathlib import Path

import pytest
from textual.widgets import Button, Input, Static, TextArea

from pyxis.app.chromium_research_second_changed_basis_transition import (
    ChromiumResearchSecondChangedBasisTransitionError,
    ChromiumResearchSecondChangedBasisTransitionResult,
    persist_chromium_research_second_changed_basis_transition,
)
from pyxis.app.chromium_research_root_backed_session_shell_lineage import (
    prove_chromium_research_root_backed_session_continuation_shell_lineage,
)
from pyxis.app.chromium_research_session_rollover import (
    rollover_chromium_research_session_to_persisted_successor,
)
from pyxis.app.chromium_research_session_working_set_extension import (
    persist_chromium_research_session_working_set_extension,
)
from pyxis.ui.root_backed_authority_inspection_shell import (
    create_inspectable_root_backed_continuation_handoff_research_session_shell,
    create_inspectable_root_backed_continuation_research_session_shell,
)
from pyxis.ui.root_backed_continuation_research_session_shell import (
    create_root_backed_continuation_research_session_shell,
)
from pyxis.ui.chromium_research_second_changed_basis_transition_textual import (
    ResearchSecondChangedBasisTransitionControls,
)
from test_app_chromium_research_root_backed_session_continuation_reentry_plan_document import (
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
    return values, values[-1].fresh_reentry


def _prepare_direct(tmp_path: Path, reentry, member, *, stem: str):
    return persist_chromium_research_session_working_set_extension(
        reentry.controller,
        (member,),
        rationale_text="Explicit second evidence-basis rationale.",
        working_set_destination=tmp_path / f"{stem}-working-set.json",
        note_destination=tmp_path / f"{stem}-working-set-note.json",
    )


async def _prepare_in_shell(shell, pilot, tmp_path: Path, *, stem: str):
    shell.query_one("#research-changed-basis-rationale", TextArea).text = (
        "Explicit second evidence-basis rationale in the live one-root continuation."
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


async def _persist_second_transition(shell, pilot, prepared, destination: Path) -> None:
    shell.query_one(
        "#research-second-changed-basis-transition-prior-edge-source", Input
    ).value = str(shell.research_controller.declared_endpoint.verification.path)
    shell.query_one(
        "#research-second-changed-basis-transition-working-set-source", Input
    ).value = str(prepared.working_set_persistence.path)
    shell.query_one(
        "#research-second-changed-basis-transition-note-source", Input
    ).value = str(prepared.note_persistence.path)
    shell.query_one(
        "#research-second-changed-basis-transition-destination", Input
    ).value = str(destination)
    await _press(shell, pilot, "persist-research-second-changed-basis-transition")


def test_46a_application_boundary_requires_exact_continuation_and_freshly_relinks(
    tmp_path: Path,
) -> None:
    _, reentry = _continuation(tmp_path, stem="46a-app")
    member, _ = _new_paragraph_member(tmp_path, stem="46a-app-member")
    prepared = _prepare_direct(tmp_path, reentry, member, stem="46a-app")
    destination = tmp_path / "46a-transition.json"

    result = persist_chromium_research_second_changed_basis_transition(
        reentry.controller,
        reentry,
        prepared,
        prior_edge_source=reentry.controller.declared_endpoint.verification.path,
        working_set_source=prepared.working_set_persistence.path,
        note_source=prepared.note_persistence.path,
        destination=destination,
    )

    assert isinstance(result, ChromiumResearchSecondChangedBasisTransitionResult)
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

    with pytest.raises(TypeError, match="exactly ChromiumResearchRootBackedSessionContinuationReentryResult"):
        persist_chromium_research_second_changed_basis_transition(
            reentry.controller,
            object(),  # type: ignore[arg-type]
            prepared,
            prior_edge_source=reentry.controller.declared_endpoint.verification.path,
            working_set_source=prepared.working_set_persistence.path,
            note_source=prepared.note_persistence.path,
            destination=tmp_path / "must-not-write.json",
        )
    assert not (tmp_path / "must-not-write.json").exists()


def test_46a_application_accepts_moved_prepared_files_only_via_explicit_paths(
    tmp_path: Path,
) -> None:
    _, reentry = _continuation(tmp_path, stem="46a-moved")
    member, _ = _new_paragraph_member(tmp_path, stem="46a-moved-member")
    prepared = _prepare_direct(tmp_path, reentry, member, stem="46a-moved")
    moved_working_set = tmp_path / "moved-second-working-set.json"
    moved_note = tmp_path / "moved-second-working-set-note.json"
    prepared.working_set_persistence.path.rename(moved_working_set)
    prepared.note_persistence.path.rename(moved_note)

    result = persist_chromium_research_second_changed_basis_transition(
        reentry.controller,
        reentry,
        prepared,
        prior_edge_source=reentry.controller.declared_endpoint.verification.path,
        working_set_source=moved_working_set,
        note_source=moved_note,
        destination=tmp_path / "moved-second-transition.json",
    )

    assert result.persistence.fresh_successor_note.verification.path == moved_note.resolve()
    assert (
        result.persistence.fresh_successor_note.working_set.verification.path
        == moved_working_set.resolve()
    )


def test_46a_application_rejects_mismatched_typed_continuation_before_write(
    tmp_path: Path,
) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    first.mkdir()
    second.mkdir()
    _, first_reentry = _continuation(first, stem="first")
    _, second_reentry = _continuation(second, stem="second")
    member, _ = _new_paragraph_member(first, stem="46a-mismatch-member")
    prepared = _prepare_direct(first, first_reentry, member, stem="46a-mismatch")
    destination = first / "must-not-write-mismatch.json"

    with pytest.raises(
        ChromiumResearchSecondChangedBasisTransitionError,
        match="does not describe|does not match",
    ):
        persist_chromium_research_second_changed_basis_transition(
            first_reentry.controller,
            second_reentry,
            prepared,
            prior_edge_source=first_reentry.controller.declared_endpoint.verification.path,
            working_set_source=prepared.working_set_persistence.path,
            note_source=prepared.note_persistence.path,
            destination=destination,
        )

    assert not destination.exists()


@pytest.mark.asyncio
async def test_46a_shell_mounts_only_after_preparation_and_persists_without_adoption(
    tmp_path: Path,
) -> None:
    _, reentry = _continuation(tmp_path, stem="46a-ui")
    member, _ = _new_paragraph_member(tmp_path, stem="46a-ui-member")
    shell = create_root_backed_continuation_research_session_shell(reentry)
    shell.configure_changed_basis_candidate((member,))
    original_controller = shell.research_controller
    original_session = shell.research_session
    original_reentry = shell.root_backed_continuation_reentry

    async with shell.run_test(size=(180, 205)) as pilot:
        await pilot.pause()
        assert len(shell.query(ResearchSecondChangedBasisTransitionControls)) == 0

        prepared = await _prepare_in_shell(shell, pilot, tmp_path, stem="46a-ui")
        controls = shell.query_one(ResearchSecondChangedBasisTransitionControls)
        summary = str(
            shell.query_one(
                "#research-second-changed-basis-transition-prepared-summary", Static
            ).content
        )
        assert "PREPARED SECOND CHANGED BASIS" in summary
        assert "NOT YET TRANSITIONED / NOT ROOTED" in summary
        for widget_id in (
            "#research-second-changed-basis-transition-prior-edge-source",
            "#research-second-changed-basis-transition-working-set-source",
            "#research-second-changed-basis-transition-note-source",
            "#research-second-changed-basis-transition-destination",
        ):
            assert shell.query_one(widget_id, Input).value == ""

        destination = tmp_path / "46a-ui-transition.json"
        await _persist_second_transition(shell, pilot, prepared, destination)

        result = shell.last_second_changed_basis_transition
        assert result is not None
        assert result.continuation_reentry is original_reentry
        assert result.prepared is prepared
        assert shell.research_controller is original_controller
        assert shell.research_session is original_session
        assert shell.root_backed_continuation_reentry is original_reentry
        assert controls.prior_result is result
        assert shell.query_one(
            "#persist-research-second-changed-basis-transition", Button
        ).disabled
        receipt = str(
            shell.query_one(
                "#research-second-changed-basis-transition-status", Static
            ).content
        )
        assert "Mounted governed session unchanged" in receipt
        assert "no second root/epoch was created" in receipt
        assert destination.exists()
        assert len(shell.query("#create-research-transition-revision-root")) == 0
        assert len(shell.query("#adopt-second-basis-epoch")) == 0


@pytest.mark.asyncio
async def test_46a_rollover_stales_unsaved_second_transition_without_retargeting(
    tmp_path: Path,
) -> None:
    _, reentry = _continuation(tmp_path, stem="46a-stale")
    member, _ = _new_paragraph_member(tmp_path, stem="46a-stale-member")
    shell = create_root_backed_continuation_research_session_shell(reentry)
    shell.configure_changed_basis_candidate((member,))

    async with shell.run_test(size=(180, 215)) as pilot:
        await pilot.pause()
        await _prepare_in_shell(shell, pilot, tmp_path, stem="46a-stale")
        controls = shell.query_one(ResearchSecondChangedBasisTransitionControls)

        successor = tmp_path / "46a-stale-successor.json"
        shell.query_one("#research-endpoint-revised-note", TextArea).text = (
            "Explicit one-hop continuation before saving the second basis transition."
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
        ).value = str(tmp_path / "46a-stale-declaration.json")
        await _press(shell, pilot, "rollover-research-session")

        assert controls.stale
        assert controls.prior_result is None
        assert shell.query_one(
            "#persist-research-second-changed-basis-transition", Button
        ).disabled
        assert shell.last_second_changed_basis_transition is None
        assert shell.research_controller is not reentry.controller
        assert shell.root_backed_continuation_reentry is reentry
        status = str(
            shell.query_one(
                "#research-second-changed-basis-transition-status", Static
            ).content
        )
        assert "will not silently retarget" in status


@pytest.mark.asyncio
async def test_46a_persisted_and_raw_inspection_provenance_remains_unchanged(
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
        stem="persisted-member",
    )
    persisted_shell.configure_changed_basis_candidate((persisted_member,))
    persisted_launch = persisted_shell.root_backed_authority_inspection.launch_provenance

    async with persisted_shell.run_test(size=(180, 205)) as pilot:
        await pilot.pause()
        prepared = await _prepare_in_shell(
            persisted_shell,
            pilot,
            persisted_dir,
            stem="persisted",
        )
        await _persist_second_transition(
            persisted_shell,
            pilot,
            prepared,
            persisted_dir / "persisted-second-transition.json",
        )
        assert persisted_shell.last_second_changed_basis_transition is not None
        assert persisted_shell.root_backed_authority_inspection.launch_provenance is persisted_launch
        assert persisted_launch.launch_location_context == persisted_overlay.resolve()

    _, raw_reentry = _continuation(raw_dir, stem="raw")
    raw_shell = create_inspectable_root_backed_continuation_handoff_research_session_shell(
        raw_reentry
    )
    raw_member, _ = _new_paragraph_member(raw_dir, stem="raw-member")
    raw_shell.configure_changed_basis_candidate((raw_member,))
    raw_launch = raw_shell.root_backed_authority_inspection.launch_provenance
    assert raw_launch.launch_location_context is None

    async with raw_shell.run_test(size=(180, 205)) as pilot:
        await pilot.pause()
        prepared = await _prepare_in_shell(raw_shell, pilot, raw_dir, stem="raw")
        await _persist_second_transition(
            raw_shell,
            pilot,
            prepared,
            raw_dir / "raw-second-transition.json",
        )
        assert raw_shell.last_second_changed_basis_transition is not None
        assert raw_shell.root_backed_authority_inspection.launch_provenance is raw_launch
        assert raw_launch.launch_location_context is None


def test_46a_plain_continuation_without_candidate_has_no_second_transition_surface(
    tmp_path: Path,
) -> None:
    _, reentry = _continuation(tmp_path, stem="46a-plain")
    shell = create_root_backed_continuation_research_session_shell(reentry)

    assert shell.changed_basis_candidate_items is None
    assert shell.last_changed_basis_preparation is None
    assert shell.last_second_changed_basis_transition is None
