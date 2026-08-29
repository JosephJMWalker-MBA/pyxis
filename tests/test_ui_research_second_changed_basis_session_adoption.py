from __future__ import annotations

from pathlib import Path

import pytest
from textual.widgets import Button, Input, Static, TextArea

from pyxis.app.chromium_research_root_backed_session_shell_lineage import (
    prove_chromium_research_root_backed_session_continuation_shell_lineage,
)
from pyxis.app.chromium_research_second_changed_basis_root_edge import (
    persist_chromium_research_second_changed_basis_root_edge,
)
from pyxis.app.chromium_research_second_changed_basis_session_adoption import (
    ChromiumResearchSecondChangedBasisSessionAdoptionResult,
    adopt_chromium_research_second_changed_basis_governed_session,
)
from pyxis.ui.chromium_research_second_changed_basis_session_adoption_textual import (
    ResearchSecondChangedBasisSessionAdoptionControls,
)
from pyxis.ui.root_backed_authority_inspection_shell import (
    create_inspectable_root_backed_continuation_handoff_research_session_shell,
    create_inspectable_root_backed_continuation_research_session_shell,
)
from pyxis.ui.second_changed_basis_session_adoption_research_session_shell import (
    create_second_changed_basis_session_adoption_research_session_shell,
)
from test_app_chromium_research_session_working_set_extension import _new_paragraph_member
from test_ui_research_second_changed_basis_revision_root import _persist_root_ui
from test_ui_research_second_changed_basis_root_edge import (
    _persist_edge_ui,
    _second_root_direct,
)
from test_ui_research_second_changed_basis_transition import (
    _continuation,
    _persist_second_transition,
    _prepare_in_shell,
    _press,
)


def _second_edge_direct(tmp_path: Path, *, stem: str):
    values, reentry, prepared, transition, root = _second_root_direct(
        tmp_path,
        stem=stem,
    )
    edge = persist_chromium_research_second_changed_basis_root_edge(
        root,
        revised_note_text=f"{stem} first post-second-root rationale.",
        root_source=root.persistence.path,
        destination=tmp_path / f"{stem}-edge.json",
    )
    return values, reentry, prepared, transition, root, edge


async def _reach_46c(shell, pilot, tmp_path: Path, *, stem: str):
    prepared = await _prepare_in_shell(shell, pilot, tmp_path, stem=stem)
    await _persist_second_transition(
        shell,
        pilot,
        prepared,
        tmp_path / f"{stem}-transition.json",
    )
    transition = shell.last_second_changed_basis_transition
    assert transition is not None
    await _persist_root_ui(
        shell,
        pilot,
        transition,
        destination=tmp_path / f"{stem}-root.json",
        rationale=f"{stem} exact second-root rationale before declaration.",
    )
    root = shell.last_second_changed_basis_revision_root
    assert root is not None
    await _persist_edge_ui(
        shell,
        pilot,
        root,
        destination=tmp_path / f"{stem}-edge.json",
        rationale=f"{stem} exact first post-second-root edge rationale.",
    )
    edge = shell.last_second_changed_basis_root_edge
    assert edge is not None
    return prepared, transition, root, edge


async def _adopt_ui(shell, pilot, edge, destination: Path) -> None:
    shell.query_one(
        "#research-second-changed-basis-session-adoption-edge-source", Input
    ).value = str(edge.persistence.path)
    shell.query_one(
        "#research-second-changed-basis-session-adoption-declaration-destination", Input
    ).value = str(destination)
    await _press(shell, pilot, "adopt-research-second-changed-basis-session")


def test_46d_application_declares_and_adopts_exact_46c_lineage(tmp_path: Path) -> None:
    *_, root, edge = _second_edge_direct(tmp_path, stem="46d-app")
    destination = tmp_path / "46d-app-declaration.json"

    result = adopt_chromium_research_second_changed_basis_governed_session(
        edge,
        edge_source=edge.persistence.path,
        declaration_destination=destination,
    )

    assert isinstance(result, ChromiumResearchSecondChangedBasisSessionAdoptionResult)
    assert result.edge_result is edge
    assert result.sequence.starting_predecessor is root.loaded_root
    assert len(result.sequence.edges) == 1
    assert (
        result.sequence.edges[0].verification.edge_record_sha256
        == edge.persistence.edge_record_sha256
    )
    assert result.declaration.path == destination.resolve()
    assert (
        result.loaded_declaration.verification.sequence_record_sha256
        == result.declaration.sequence_record_sha256
    )
    assert result.loaded_declaration.sequence.starting_predecessor is root.loaded_root
    assert (
        result.controller.declared_endpoint.verification.edge_record_sha256
        == edge.persistence.edge_record_sha256
    )

    with pytest.raises(
        TypeError,
        match="exactly ChromiumResearchSecondChangedBasisRootEdgeResult",
    ):
        adopt_chromium_research_second_changed_basis_governed_session(
            object(),  # type: ignore[arg-type]
            edge_source=edge.persistence.path,
            declaration_destination=tmp_path / "46d-wrong-type.json",
        )
    assert not (tmp_path / "46d-wrong-type.json").exists()


def test_46d_application_uses_only_explicit_current_edge_path(tmp_path: Path) -> None:
    *_, root, edge = _second_edge_direct(tmp_path, stem="46d-moved")
    moved_edge = tmp_path / "46d-explicit-moved-edge.json"
    edge.persistence.path.rename(moved_edge)

    result = adopt_chromium_research_second_changed_basis_governed_session(
        edge,
        edge_source=moved_edge,
        declaration_destination=tmp_path / "46d-moved-declaration.json",
    )

    assert result.sequence.starting_predecessor is root.loaded_root
    assert result.sequence.edges[0].verification.path == moved_edge.resolve()
    assert (
        result.sequence.edges[0].verification.edge_record_sha256
        == edge.persistence.edge_record_sha256
    )


def test_46d_wrong_edge_locator_rejects_before_declaration_write(tmp_path: Path) -> None:
    *_, root, edge = _second_edge_direct(tmp_path, stem="46d-wrong")
    destination = tmp_path / "46d-wrong-declaration.json"

    with pytest.raises(Exception):
        adopt_chromium_research_second_changed_basis_governed_session(
            edge,
            edge_source=root.persistence.path,
            declaration_destination=destination,
        )

    assert not destination.exists()


@pytest.mark.asyncio
async def test_46d_shell_mounts_only_after_46c_and_explicitly_promotes_controller(
    tmp_path: Path,
) -> None:
    _, reentry = _continuation(tmp_path, stem="46d-ui")
    member, _ = _new_paragraph_member(tmp_path, stem="46d-ui-member")
    shell = create_second_changed_basis_session_adoption_research_session_shell(reentry)
    shell.configure_changed_basis_candidate((member,))
    original_controller = shell.research_controller
    original_reentry = shell.root_backed_continuation_reentry

    async with shell.run_test(size=(210, 500)) as pilot:
        await pilot.pause()
        assert len(shell.query(ResearchSecondChangedBasisSessionAdoptionControls)) == 0

        *_, edge = await _reach_46c(shell, pilot, tmp_path, stem="46d-ui")
        controls = shell.query_one(ResearchSecondChangedBasisSessionAdoptionControls)
        summary = str(
            shell.query_one(
                "#research-second-changed-basis-session-adoption-summary", Static
            ).content
        )
        assert "SECOND CHANGED-BASIS LINEAGE READY" in summary
        assert edge.persistence.edge_record_sha256 in summary
        assert shell.query_one(
            "#research-second-changed-basis-session-adoption-edge-source", Input
        ).value == ""
        assert shell.query_one(
            "#research-second-changed-basis-session-adoption-declaration-destination", Input
        ).value == ""

        await _adopt_ui(
            shell,
            pilot,
            edge,
            tmp_path / "46d-ui-declaration.json",
        )

        result = shell.last_second_changed_basis_session_adoption
        assert result is not None
        assert result.edge_result is edge
        assert shell.research_controller is result.controller
        assert shell.research_controller is not original_controller
        assert shell.root_backed_continuation_reentry is original_reentry
        assert shell.research_reentry is None
        assert shell.changed_basis_candidate_items is None
        assert controls.prior_result is result
        assert shell.query_one(
            "#adopt-research-second-changed-basis-session", Button
        ).disabled
        receipt = str(
            shell.query_one(
                "#research-second-changed-basis-session-adoption-status", Static
            ).content
        )
        assert "explicitly adopted" in receipt
        assert "No second-epoch fresh-process re-entry/overlay" in receipt
        assert len(shell.query("#persist-second-basis-epoch-overlay")) == 0


@pytest.mark.asyncio
async def test_46d_post_adoption_rollover_does_not_mount_historical_first_root_35e(
    tmp_path: Path,
) -> None:
    _, reentry = _continuation(tmp_path, stem="46d-rollover")
    member, _ = _new_paragraph_member(tmp_path, stem="46d-rollover-member")
    shell = create_second_changed_basis_session_adoption_research_session_shell(reentry)
    shell.configure_changed_basis_candidate((member,))

    async with shell.run_test(size=(215, 520)) as pilot:
        await pilot.pause()
        *_, edge = await _reach_46c(shell, pilot, tmp_path, stem="46d-rollover")
        await _adopt_ui(
            shell,
            pilot,
            edge,
            tmp_path / "46d-rollover-adoption-declaration.json",
        )
        adoption = shell.last_second_changed_basis_session_adoption
        assert adoption is not None
        adopted_controller = adoption.controller

        successor = tmp_path / "46d-rollover-successor.json"
        shell.query_one("#research-endpoint-revised-note", TextArea).text = (
            "Ordinary continuation after explicit second changed-basis adoption."
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
        ).value = str(tmp_path / "46d-rollover-next-declaration.json")
        await _press(shell, pilot, "rollover-research-session")

        assert shell.research_controller is not adopted_controller
        assert shell.last_research_rollover is not None
        assert len(shell.query("#research-root-backed-cumulative-checkpoint-controls")) == 0
        assert shell.root_backed_continuation_reentry is reentry
        assert shell.last_second_changed_basis_session_adoption is adoption


@pytest.mark.asyncio
async def test_46d_inspection_preserves_launch_and_advances_only_current_state(
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
        stem="persisted-46d-member",
    )
    persisted_shell.configure_changed_basis_candidate((persisted_member,))
    persisted_launch = persisted_shell.root_backed_authority_inspection.launch_provenance

    async with persisted_shell.run_test(size=(215, 500)) as pilot:
        await pilot.pause()
        *_, edge = await _reach_46c(
            persisted_shell,
            pilot,
            persisted_dir,
            stem="persisted-46d",
        )
        await _adopt_ui(
            persisted_shell,
            pilot,
            edge,
            persisted_dir / "persisted-46d-declaration.json",
        )
        adoption = persisted_shell.last_second_changed_basis_session_adoption
        assert adoption is not None
        assert persisted_shell.root_backed_authority_inspection.launch_provenance is persisted_launch
        assert persisted_launch.launch_location_context == persisted_overlay.resolve()
        current = persisted_shell.root_backed_authority_inspection.current_state
        assert current.state_kind == "adopted second changed-basis governed session"
        assert current.state_source == "explicit 46D second changed-basis adoption"
        assert current.endpoint_sha256 == adoption.controller.declared_endpoint.verification.edge_record_sha256

    _, raw_reentry = _continuation(raw_dir, stem="raw")
    raw_shell = create_inspectable_root_backed_continuation_handoff_research_session_shell(
        raw_reentry
    )
    raw_member, _ = _new_paragraph_member(raw_dir, stem="raw-46d-member")
    raw_shell.configure_changed_basis_candidate((raw_member,))
    raw_launch = raw_shell.root_backed_authority_inspection.launch_provenance
    assert raw_launch.launch_location_context is None

    async with raw_shell.run_test(size=(215, 500)) as pilot:
        await pilot.pause()
        *_, edge = await _reach_46c(raw_shell, pilot, raw_dir, stem="raw-46d")
        await _adopt_ui(
            raw_shell,
            pilot,
            edge,
            raw_dir / "raw-46d-declaration.json",
        )
        adoption = raw_shell.last_second_changed_basis_session_adoption
        assert adoption is not None
        assert raw_shell.root_backed_authority_inspection.launch_provenance is raw_launch
        assert raw_launch.launch_location_context is None
        current = raw_shell.root_backed_authority_inspection.current_state
        assert current.state_kind == "adopted second changed-basis governed session"
        assert current.state_source == (
            "explicit 46D second changed-basis adoption after in-process 36D handoff"
        )
        assert current.endpoint_sha256 == adoption.controller.declared_endpoint.verification.edge_record_sha256
