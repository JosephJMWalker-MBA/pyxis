from __future__ import annotations

from pathlib import Path

import pytest
from textual.widgets import Button, Input, Static, TextArea

from pyxis.app.chromium_research_root_backed_session_shell_lineage import (
    prove_chromium_research_root_backed_session_continuation_shell_lineage,
)
from pyxis.app.chromium_research_second_changed_basis_revision_root import (
    persist_chromium_research_second_changed_basis_revision_root,
)
from pyxis.app.chromium_research_second_changed_basis_root_edge import (
    ChromiumResearchSecondChangedBasisRootEdgeResult,
    persist_chromium_research_second_changed_basis_root_edge,
)
from pyxis.ui.chromium_research_second_changed_basis_root_edge_textual import (
    ResearchSecondChangedBasisRootEdgeControls,
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
from test_ui_research_second_changed_basis_revision_root import (
    _persist_root_ui,
    _second_transition_direct,
)
from test_ui_research_second_changed_basis_transition import (
    _continuation,
    _persist_second_transition,
    _prepare_in_shell,
    _press,
)


def _second_root_direct(tmp_path: Path, *, stem: str):
    values, reentry, prepared, transition = _second_transition_direct(
        tmp_path,
        stem=stem,
    )
    root = persist_chromium_research_second_changed_basis_revision_root(
        transition,
        revised_note_text=f"{stem} explicit second-root rationale.",
        prior_edge_source=transition.controller.declared_endpoint.verification.path,
        working_set_source=prepared.working_set_persistence.path,
        note_source=prepared.note_persistence.path,
        transition_source=transition.persistence.path,
        destination=tmp_path / f"{stem}-root.json",
    )
    return values, reentry, prepared, transition, root


async def _persist_edge_ui(
    shell,
    pilot,
    root_result,
    *,
    destination: Path,
    rationale: str,
) -> None:
    shell.query_one(
        "#research-second-changed-basis-root-edge-rationale", TextArea
    ).text = rationale
    shell.query_one(
        "#research-second-changed-basis-root-edge-root-source", Input
    ).value = str(root_result.persistence.path)
    shell.query_one(
        "#research-second-changed-basis-root-edge-destination", Input
    ).value = str(destination)
    await _press(shell, pilot, "persist-research-second-changed-basis-root-edge")


def test_46c_application_persists_and_freshly_relinks_exact_first_34b_edge(
    tmp_path: Path,
) -> None:
    *_, root = _second_root_direct(tmp_path, stem="46c-app")
    destination = tmp_path / "46c-app-edge.json"
    revised_text = "First ordinary rationale after the exact second changed-basis root."

    result = persist_chromium_research_second_changed_basis_root_edge(
        root,
        revised_note_text=revised_text,
        root_source=root.persistence.path,
        destination=destination,
    )

    assert isinstance(result, ChromiumResearchSecondChangedBasisRootEdgeResult)
    assert result.root_result is root
    assert result.persistence.extension is result.extension
    assert result.persistence.path == destination.resolve()
    assert (
        result.loaded_edge.verification.edge_record_sha256
        == result.persistence.edge_record_sha256
    )
    assert (
        result.loaded_edge.verification.predecessor_record_sha256
        == root.persistence.root_record_sha256
    )
    assert result.loaded_edge.revision.revised_note.note_text == revised_text

    noop_destination = tmp_path / "46c-noop-edge.json"
    with pytest.raises(ValueError, match="differ exactly"):
        persist_chromium_research_second_changed_basis_root_edge(
            root,
            revised_note_text=root.loaded_root.root.revision.revised_note.note_text,
            root_source=root.persistence.path,
            destination=noop_destination,
        )
    assert not noop_destination.exists()

    with pytest.raises(
        TypeError,
        match="exactly ChromiumResearchSecondChangedBasisRevisionRootResult",
    ):
        persist_chromium_research_second_changed_basis_root_edge(
            object(),  # type: ignore[arg-type]
            revised_note_text="Must not write.",
            root_source=root.persistence.path,
            destination=tmp_path / "46c-wrong-type-edge.json",
        )
    assert not (tmp_path / "46c-wrong-type-edge.json").exists()


def test_46c_application_accepts_moved_root_only_via_explicit_current_path(
    tmp_path: Path,
) -> None:
    *_, root = _second_root_direct(tmp_path, stem="46c-moved")
    moved_root = tmp_path / "46c-explicit-moved-root.json"
    root.persistence.path.rename(moved_root)

    result = persist_chromium_research_second_changed_basis_root_edge(
        root,
        revised_note_text="Explicit local continuation after the moved second root.",
        root_source=moved_root,
        destination=tmp_path / "46c-moved-edge.json",
    )

    assert result.persistence.root_verification.path == moved_root.resolve()
    assert (
        result.persistence.root_verification.root_record_sha256
        == root.persistence.root_record_sha256
    )


def test_46c_wrong_root_locator_rejects_before_edge_write(tmp_path: Path) -> None:
    *_, transition, root = _second_root_direct(tmp_path, stem="46c-wrong")
    destination = tmp_path / "46c-wrong-edge.json"

    with pytest.raises(Exception):
        persist_chromium_research_second_changed_basis_root_edge(
            root,
            revised_note_text="Valid new wording with an explicitly wrong root source.",
            root_source=transition.persistence.path,
            destination=destination,
        )

    assert not destination.exists()


@pytest.mark.asyncio
async def test_46c_shell_mounts_only_after_46b_success_and_persists_without_adoption(
    tmp_path: Path,
) -> None:
    _, reentry = _continuation(tmp_path, stem="46c-ui")
    member, _ = _new_paragraph_member(tmp_path, stem="46c-ui-member")
    shell = create_root_backed_continuation_research_session_shell(reentry)
    shell.configure_changed_basis_candidate((member,))
    original_controller = shell.research_controller
    original_session = shell.research_session
    original_reentry = shell.root_backed_continuation_reentry

    async with shell.run_test(size=(200, 390)) as pilot:
        await pilot.pause()
        assert len(shell.query(ResearchSecondChangedBasisRootEdgeControls)) == 0

        prepared = await _prepare_in_shell(shell, pilot, tmp_path, stem="46c-ui")
        await _persist_second_transition(
            shell,
            pilot,
            prepared,
            tmp_path / "46c-ui-transition.json",
        )
        transition = shell.last_second_changed_basis_transition
        assert transition is not None
        assert len(shell.query(ResearchSecondChangedBasisRootEdgeControls)) == 0

        await _persist_root_ui(
            shell,
            pilot,
            transition,
            destination=tmp_path / "46c-ui-root.json",
            rationale="Second root rationale before the first local ordinary edge.",
        )
        root = shell.last_second_changed_basis_revision_root
        assert root is not None

        controls = shell.query_one(ResearchSecondChangedBasisRootEdgeControls)
        summary = str(
            shell.query_one(
                "#research-second-changed-basis-root-edge-root-summary", Static
            ).content
        )
        assert "PERSISTED SECOND CHANGED-BASIS ROOT" in summary
        assert "NO SECOND-EPOCH SESSION YET" in summary
        assert root.persistence.root_record_sha256 in summary
        assert shell.query_one(
            "#research-second-changed-basis-root-edge-rationale", TextArea
        ).text == ""
        assert shell.query_one(
            "#research-second-changed-basis-root-edge-root-source", Input
        ).value == ""
        assert shell.query_one(
            "#research-second-changed-basis-root-edge-destination", Input
        ).value == ""

        await _persist_edge_ui(
            shell,
            pilot,
            root,
            destination=tmp_path / "46c-ui-edge.json",
            rationale="  First local post-second-root rationale 😀\nStill explicit.  ",
        )

        result = shell.last_second_changed_basis_root_edge
        assert result is not None
        assert result.root_result is root
        assert shell.research_controller is original_controller
        assert shell.research_session is original_session
        assert shell.root_backed_continuation_reentry is original_reentry
        assert controls.prior_result is result
        assert shell.query_one(
            "#persist-research-second-changed-basis-root-edge", Button
        ).disabled
        receipt = str(
            shell.query_one(
                "#research-second-changed-basis-root-edge-status", Static
            ).content
        )
        assert "Mounted one-root continuation unchanged" in receipt
        assert "no sequence declaration" in receipt
        assert len(shell.query("#adopt-second-basis-epoch")) == 0
        assert len(shell.query("#persist-second-basis-epoch-overlay")) == 0


@pytest.mark.asyncio
async def test_46c_historical_second_root_edge_authority_survives_later_one_root_rollover(
    tmp_path: Path,
) -> None:
    _, reentry = _continuation(tmp_path, stem="46c-history")
    member, _ = _new_paragraph_member(tmp_path, stem="46c-history-member")
    shell = create_root_backed_continuation_research_session_shell(reentry)
    shell.configure_changed_basis_candidate((member,))

    async with shell.run_test(size=(205, 410)) as pilot:
        await pilot.pause()
        prepared = await _prepare_in_shell(shell, pilot, tmp_path, stem="46c-history")
        await _persist_second_transition(
            shell,
            pilot,
            prepared,
            tmp_path / "46c-history-transition.json",
        )
        transition = shell.last_second_changed_basis_transition
        assert transition is not None
        await _persist_root_ui(
            shell,
            pilot,
            transition,
            destination=tmp_path / "46c-history-root.json",
            rationale="Historical exact second root before the old branch continues.",
        )
        root = shell.last_second_changed_basis_revision_root
        assert root is not None
        edge_controls = shell.query_one(ResearchSecondChangedBasisRootEdgeControls)

        successor = tmp_path / "46c-history-successor.json"
        shell.query_one("#research-endpoint-revised-note", TextArea).text = (
            "The older one-root branch continues after the exact second root exists."
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
        ).value = str(tmp_path / "46c-history-declaration.json")
        await _press(shell, pilot, "rollover-research-session")

        assert shell.research_controller is not transition.controller
        assert edge_controls.prior_result is None
        assert not shell.query_one(
            "#persist-research-second-changed-basis-root-edge", Button
        ).disabled

        await _persist_edge_ui(
            shell,
            pilot,
            root,
            destination=tmp_path / "46c-history-edge.json",
            rationale=(
                "The historical second root receives its first local edge after the "
                "older one-root branch continued."
            ),
        )

        result = shell.last_second_changed_basis_root_edge
        assert result is not None
        assert result.root_result is root
        assert (
            result.loaded_edge.verification.predecessor_record_sha256
            == root.persistence.root_record_sha256
        )
        assert shell.research_controller is not transition.controller
        assert shell.root_backed_continuation_reentry is reentry


@pytest.mark.asyncio
async def test_46c_persisted_and_raw_inspection_provenance_remains_unchanged(
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
        stem="persisted-46c-member",
    )
    persisted_shell.configure_changed_basis_candidate((persisted_member,))
    persisted_launch = persisted_shell.root_backed_authority_inspection.launch_provenance

    async with persisted_shell.run_test(size=(205, 390)) as pilot:
        await pilot.pause()
        prepared = await _prepare_in_shell(
            persisted_shell,
            pilot,
            persisted_dir,
            stem="persisted-46c",
        )
        await _persist_second_transition(
            persisted_shell,
            pilot,
            prepared,
            persisted_dir / "persisted-46c-transition.json",
        )
        transition = persisted_shell.last_second_changed_basis_transition
        assert transition is not None
        await _persist_root_ui(
            persisted_shell,
            pilot,
            transition,
            destination=persisted_dir / "persisted-46c-root.json",
            rationale="Persisted-launch second root before local edge.",
        )
        root = persisted_shell.last_second_changed_basis_revision_root
        assert root is not None
        await _persist_edge_ui(
            persisted_shell,
            pilot,
            root,
            destination=persisted_dir / "persisted-46c-edge.json",
            rationale="Persisted-launch first post-second-root edge.",
        )
        assert persisted_shell.last_second_changed_basis_root_edge is not None
        assert persisted_shell.root_backed_authority_inspection.launch_provenance is persisted_launch
        assert persisted_launch.launch_location_context == persisted_overlay.resolve()

    _, raw_reentry = _continuation(raw_dir, stem="raw")
    raw_shell = create_inspectable_root_backed_continuation_handoff_research_session_shell(
        raw_reentry
    )
    raw_member, _ = _new_paragraph_member(raw_dir, stem="raw-46c-member")
    raw_shell.configure_changed_basis_candidate((raw_member,))
    raw_launch = raw_shell.root_backed_authority_inspection.launch_provenance
    assert raw_launch.launch_location_context is None

    async with raw_shell.run_test(size=(205, 390)) as pilot:
        await pilot.pause()
        prepared = await _prepare_in_shell(raw_shell, pilot, raw_dir, stem="raw-46c")
        await _persist_second_transition(
            raw_shell,
            pilot,
            prepared,
            raw_dir / "raw-46c-transition.json",
        )
        transition = raw_shell.last_second_changed_basis_transition
        assert transition is not None
        await _persist_root_ui(
            raw_shell,
            pilot,
            transition,
            destination=raw_dir / "raw-46c-root.json",
            rationale="Raw-handoff second root before local edge.",
        )
        root = raw_shell.last_second_changed_basis_revision_root
        assert root is not None
        await _persist_edge_ui(
            raw_shell,
            pilot,
            root,
            destination=raw_dir / "raw-46c-edge.json",
            rationale="Raw-handoff first post-second-root edge.",
        )
        assert raw_shell.last_second_changed_basis_root_edge is not None
        assert raw_shell.root_backed_authority_inspection.launch_provenance is raw_launch
        assert raw_launch.launch_location_context is None
