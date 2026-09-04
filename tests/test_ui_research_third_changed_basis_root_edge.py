from __future__ import annotations

from pathlib import Path

import pytest
from textual.widgets import Button, Input, Static, TextArea

from pyxis.app.chromium_research_third_changed_basis_revision_root import (
    persist_chromium_research_third_changed_basis_revision_root,
)
from pyxis.app.chromium_research_third_changed_basis_root_edge import (
    ChromiumResearchThirdChangedBasisRootEdgeResult,
    persist_chromium_research_third_changed_basis_root_edge,
)
from pyxis.ui.chromium_research_third_changed_basis_root_edge_textual import (
    ResearchThirdChangedBasisRootEdgeControls,
)
from pyxis.ui.third_changed_basis_revision_root_research_session_shell import (
    create_third_changed_basis_revision_root_research_session_shell,
)
from pyxis.ui.third_changed_basis_root_edge_research_session_shell import (
    create_inspectable_third_changed_basis_root_edge_handoff_research_session_shell,
    create_inspectable_third_changed_basis_root_edge_research_session_shell,
    create_third_changed_basis_root_edge_handoff_research_session_shell,
    create_third_changed_basis_root_edge_research_session_shell,
)
from test_app_chromium_research_session_working_set_extension import (
    _new_paragraph_member,
)
from test_ui_research_third_changed_basis_revision_root import (
    _persist_root_ui,
    _third_transition_direct,
)
from test_ui_research_third_changed_basis_transition import (
    _continuation,
    _persist_third_transition,
    _prepare_in_shell,
    _press,
)


def _third_root_direct(tmp_path: Path, *, stem: str):
    reentry, lineage, prepared, transition = _third_transition_direct(
        tmp_path,
        stem=stem,
    )
    fixture_root = transition.persistence.path.parent
    root = persist_chromium_research_third_changed_basis_revision_root(
        transition,
        revised_note_text=f"Explicit third-root rationale for {stem}.",
        prior_edge_source=transition.controller.declared_endpoint.verification.path,
        working_set_source=prepared.working_set_persistence.path,
        note_source=prepared.note_persistence.path,
        transition_source=transition.persistence.path,
        destination=fixture_root / f"{stem}-root.json",
    )
    return reentry, lineage, prepared, transition, root


async def _persist_edge_ui(
    shell,
    pilot,
    root,
    *,
    destination: Path,
    rationale: str,
    root_source: Path | None = None,
) -> None:
    shell.query_one(
        "#research-third-changed-basis-root-edge-rationale", TextArea
    ).text = rationale
    shell.query_one(
        "#research-third-changed-basis-root-edge-root-source", Input
    ).value = str(root_source or root.persistence.path)
    shell.query_one(
        "#research-third-changed-basis-root-edge-destination", Input
    ).value = str(destination)
    await _press(shell, pilot, "persist-research-third-changed-basis-root-edge")


def test_47c_application_persists_and_freshly_relinks_exact_first_third_root_edge(
    tmp_path: Path,
) -> None:
    _, _, _, _, root = _third_root_direct(tmp_path, stem="47c-app")
    destination = tmp_path / "47c-app-edge.json"
    revised_text = "First human rationale after the third changed-basis root."

    result = persist_chromium_research_third_changed_basis_root_edge(
        root,
        revised_note_text=revised_text,
        root_source=root.persistence.path,
        destination=destination,
    )

    assert isinstance(result, ChromiumResearchThirdChangedBasisRootEdgeResult)
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

    noop_destination = tmp_path / "47c-noop-edge.json"
    with pytest.raises(ValueError, match="differ exactly"):
        persist_chromium_research_third_changed_basis_root_edge(
            root,
            revised_note_text=root.loaded_root.root.revision.revised_note.note_text,
            root_source=root.persistence.path,
            destination=noop_destination,
        )
    assert not noop_destination.exists()

    with pytest.raises(
        TypeError,
        match="exactly ChromiumResearchThirdChangedBasisRevisionRootResult",
    ):
        persist_chromium_research_third_changed_basis_root_edge(
            object(),  # type: ignore[arg-type]
            revised_note_text="Must not write.",
            root_source=root.persistence.path,
            destination=tmp_path / "47c-wrong-type-edge.json",
        )
    assert not (tmp_path / "47c-wrong-type-edge.json").exists()


def test_47c_explicit_root_path_supports_move_and_rejects_wrong_locator_without_overwrite(
    tmp_path: Path,
) -> None:
    _, _, _, _, root = _third_root_direct(tmp_path, stem="47c-moved")
    moved_root = tmp_path / "moved-third-root.json"
    root.persistence.path.rename(moved_root)

    result = persist_chromium_research_third_changed_basis_root_edge(
        root,
        revised_note_text="First local edge after explicitly moving the third root.",
        root_source=moved_root,
        destination=tmp_path / "47c-moved-edge.json",
    )
    assert (
        result.loaded_edge.verification.predecessor_record_sha256
        == root.persistence.root_record_sha256
    )
    assert result.persistence.root_verification.path == moved_root.resolve()

    _, _, _, transition2, root2 = _third_root_direct(tmp_path, stem="47c-wrong")
    wrong_destination = tmp_path / "47c-wrong-edge.json"
    with pytest.raises(Exception):
        persist_chromium_research_third_changed_basis_root_edge(
            root2,
            revised_note_text="Valid new wording with an explicitly wrong root source.",
            root_source=transition2.persistence.path,
            destination=wrong_destination,
        )
    assert not wrong_destination.exists()

    existing = tmp_path / "47c-existing-edge.json"
    existing.write_text("preserve exactly\n", encoding="utf-8")
    with pytest.raises(Exception):
        persist_chromium_research_third_changed_basis_root_edge(
            root2,
            revised_note_text="Another valid post-third-root rationale.",
            root_source=root2.persistence.path,
            destination=existing,
        )
    assert existing.read_text(encoding="utf-8") == "preserve exactly\n"


@pytest.mark.asyncio
async def test_47c_shell_mounts_only_after_47b_and_persists_without_third_epoch_adoption(
    tmp_path: Path,
) -> None:
    _, _, _, lineage = _continuation(tmp_path, stem="47c-ui")
    member, _ = _new_paragraph_member(tmp_path, stem="47c-ui-member")
    shell = create_third_changed_basis_root_edge_research_session_shell(lineage)
    shell.configure_changed_basis_candidate((member,))
    original_controller = shell.research_controller
    original_session = shell.research_session
    original_reentry = shell.second_basis_epoch_continuation_reentry

    async with shell.run_test(size=(200, 390)) as pilot:
        await pilot.pause()
        assert len(shell.query(ResearchThirdChangedBasisRootEdgeControls)) == 0

        prepared = await _prepare_in_shell(shell, pilot, tmp_path, stem="47c-ui")
        await _persist_third_transition(
            shell,
            pilot,
            prepared,
            tmp_path / "47c-ui-transition.json",
        )
        transition = shell.last_third_changed_basis_transition
        assert transition is not None
        assert len(shell.query(ResearchThirdChangedBasisRootEdgeControls)) == 0

        await _persist_root_ui(
            shell,
            pilot,
            transition,
            destination=tmp_path / "47c-ui-root.json",
            rationale="Explicit third-root rationale before the first local edge.",
        )
        root = shell.last_third_changed_basis_revision_root
        assert root is not None

        controls = shell.query_one(ResearchThirdChangedBasisRootEdgeControls)
        summary = str(
            shell.query_one(
                "#research-third-changed-basis-root-edge-root-summary", Static
            ).content
        )
        assert "PERSISTED THIRD CHANGED-BASIS ROOT" in summary
        assert "NO THIRD-EPOCH SESSION YET" in summary
        assert root.persistence.root_record_sha256 in summary
        assert shell.query_one(
            "#research-third-changed-basis-root-edge-rationale", TextArea
        ).text == ""
        assert shell.query_one(
            "#research-third-changed-basis-root-edge-root-source", Input
        ).value == ""
        assert shell.query_one(
            "#research-third-changed-basis-root-edge-destination", Input
        ).value == ""

        await _persist_edge_ui(
            shell,
            pilot,
            root,
            destination=tmp_path / "47c-ui-edge.json",
            rationale="First explicit ordinary rationale after the third root.",
        )

        result = shell.last_third_changed_basis_root_edge
        assert result is not None
        assert result.root_result is root
        assert shell.research_controller is original_controller
        assert shell.research_session is original_session
        assert shell.second_basis_epoch_continuation_reentry is original_reentry
        assert controls.prior_result is result
        assert shell.query_one(
            "#persist-research-third-changed-basis-root-edge", Button
        ).disabled
        receipt = str(
            shell.query_one(
                "#research-third-changed-basis-root-edge-status", Static
            ).content
        )
        assert "Mounted second-epoch continuation unchanged" in receipt
        assert "no root-started sequence declaration" in receipt
        assert len(shell.query("#adopt-third-basis-epoch")) == 0


@pytest.mark.asyncio
async def test_47c_historical_third_root_can_receive_edge_after_older_branch_rollover(
    tmp_path: Path,
) -> None:
    _, _, _, lineage = _continuation(tmp_path, stem="47c-history")
    member, _ = _new_paragraph_member(tmp_path, stem="47c-history-member")
    shell = create_third_changed_basis_root_edge_research_session_shell(lineage)
    shell.configure_changed_basis_candidate((member,))

    async with shell.run_test(size=(200, 410)) as pilot:
        await pilot.pause()
        prepared = await _prepare_in_shell(shell, pilot, tmp_path, stem="47c-history")
        await _persist_third_transition(
            shell,
            pilot,
            prepared,
            tmp_path / "47c-history-transition.json",
        )
        transition = shell.last_third_changed_basis_transition
        assert transition is not None
        await _persist_root_ui(
            shell,
            pilot,
            transition,
            destination=tmp_path / "47c-history-root.json",
            rationale="Third root retained before the older branch continues.",
        )
        root = shell.last_third_changed_basis_revision_root
        assert root is not None
        edge_controls = shell.query_one(ResearchThirdChangedBasisRootEdgeControls)

        successor = tmp_path / "47c-history-successor.json"
        shell.query_one("#research-endpoint-revised-note", TextArea).text = (
            "The older second-epoch branch continues after the third root was persisted."
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
        ).value = str(tmp_path / "47c-history-declaration.json")
        await _press(shell, pilot, "rollover-research-session")

        assert shell.research_controller is not transition.controller
        assert edge_controls.prior_result is None
        assert not shell.query_one(
            "#persist-research-third-changed-basis-root-edge", Button
        ).disabled

        current_reentry = shell.second_basis_epoch_continuation_reentry
        await _persist_edge_ui(
            shell,
            pilot,
            root,
            destination=tmp_path / "47c-history-edge.json",
            rationale=(
                "The historical third root receives its first local edge after "
                "the older second-epoch branch continued."
            ),
        )

        result = shell.last_third_changed_basis_root_edge
        assert result is not None
        assert result.root_result is root
        assert (
            result.loaded_edge.verification.predecessor_record_sha256
            == root.persistence.root_record_sha256
        )
        assert shell.research_controller is not transition.controller
        assert shell.second_basis_epoch_continuation_reentry is current_reentry


@pytest.mark.asyncio
async def test_47c_persisted_and_raw_launch_provenance_remains_exactly_unchanged(
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
        create_inspectable_third_changed_basis_root_edge_research_session_shell(
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

    async with persisted_shell.run_test(size=(200, 390)) as pilot:
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
        root = persisted_shell.last_third_changed_basis_revision_root
        assert root is not None
        await _persist_edge_ui(
            persisted_shell,
            pilot,
            root,
            destination=persisted_dir / "persisted-third-edge.json",
            rationale="Persisted-launch first post-third-root edge.",
        )
        assert persisted_shell.last_third_changed_basis_root_edge is not None
        assert persisted_panel.launch_provenance is persisted_launch
        assert persisted_panel.current_state is persisted_current
        assert persisted_launch.launch_location_context == persisted_overlay.resolve()

    _, _, raw_reentry, _ = _continuation(raw_dir, stem="raw")
    raw_shell = (
        create_inspectable_third_changed_basis_root_edge_handoff_research_session_shell(
            raw_reentry
        )
    )
    raw_member, _ = _new_paragraph_member(raw_dir, stem="raw-member")
    raw_shell.configure_changed_basis_candidate((raw_member,))
    raw_panel = raw_shell.second_basis_epoch_authority_inspection
    raw_launch = raw_panel.launch_provenance
    raw_current = raw_panel.current_state
    assert raw_launch.launch_location_context is None

    async with raw_shell.run_test(size=(200, 390)) as pilot:
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
        root = raw_shell.last_third_changed_basis_revision_root
        assert root is not None
        await _persist_edge_ui(
            raw_shell,
            pilot,
            root,
            destination=raw_dir / "raw-third-edge.json",
            rationale="Pathless-launch first post-third-root edge.",
        )
        assert raw_shell.last_third_changed_basis_root_edge is not None
        assert raw_shell.second_basis_epoch_continuation_handoff_reentry is raw_reentry
        assert raw_panel.launch_provenance is raw_launch
        assert raw_panel.current_state is raw_current
        assert raw_launch.launch_location_context is None


@pytest.mark.asyncio
async def test_plain_47b_product_does_not_gain_47c_surface(tmp_path: Path) -> None:
    _, _, _, lineage = _continuation(tmp_path, stem="47c-plain")
    member, _ = _new_paragraph_member(tmp_path, stem="47c-plain-member")
    shell = create_third_changed_basis_revision_root_research_session_shell(lineage)
    shell.configure_changed_basis_candidate((member,))

    async with shell.run_test(size=(195, 340)) as pilot:
        await pilot.pause()
        prepared = await _prepare_in_shell(shell, pilot, tmp_path, stem="47c-plain")
        await _persist_third_transition(
            shell,
            pilot,
            prepared,
            tmp_path / "47c-plain-transition.json",
        )
        transition = shell.last_third_changed_basis_transition
        assert transition is not None
        await _persist_root_ui(
            shell,
            pilot,
            transition,
            destination=tmp_path / "47c-plain-root.json",
            rationale="Plain 47B root should not acquire 47C controls.",
        )
        assert shell.last_third_changed_basis_revision_root is not None
        assert not hasattr(shell, "last_third_changed_basis_root_edge")
        assert len(shell.query(ResearchThirdChangedBasisRootEdgeControls)) == 0


def test_47c_product_factories_reject_wrong_authority_family() -> None:
    with pytest.raises(
        TypeError,
        match="ChromiumResearchSecondBasisEpochContinuationShellLineage",
    ):
        create_third_changed_basis_root_edge_research_session_shell(object())  # type: ignore[arg-type]

    with pytest.raises(
        TypeError,
        match="exactly ChromiumResearchSecondBasisEpochContinuationReentryResult",
    ):
        create_third_changed_basis_root_edge_handoff_research_session_shell(object())  # type: ignore[arg-type]
