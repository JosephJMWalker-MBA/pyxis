from __future__ import annotations

from pathlib import Path

import pytest
from textual.widgets import Button, Input, Static, TextArea

from pyxis.app.chromium_research_third_changed_basis_root_edge import (
    persist_chromium_research_third_changed_basis_root_edge,
)
from pyxis.app.chromium_research_third_changed_basis_session_adoption import (
    ChromiumResearchThirdChangedBasisSessionAdoptionResult,
    adopt_chromium_research_third_changed_basis_governed_session,
)
from pyxis.ui.chromium_research_third_changed_basis_session_adoption_textual import (
    ResearchThirdChangedBasisSessionAdoptionControls,
)
from pyxis.ui.third_changed_basis_root_edge_research_session_shell import (
    create_third_changed_basis_root_edge_research_session_shell,
)
from pyxis.ui.third_changed_basis_session_adoption_research_session_shell import (
    create_inspectable_third_changed_basis_session_adoption_handoff_research_session_shell,
    create_inspectable_third_changed_basis_session_adoption_research_session_shell,
    create_third_changed_basis_session_adoption_handoff_research_session_shell,
    create_third_changed_basis_session_adoption_research_session_shell,
)
from test_app_chromium_research_session_working_set_extension import _new_paragraph_member
from test_ui_research_third_changed_basis_revision_root import _persist_root_ui
from test_ui_research_third_changed_basis_root_edge import (
    _persist_edge_ui,
    _third_root_direct,
)
from test_ui_research_third_changed_basis_transition import (
    _continuation,
    _persist_third_transition,
    _prepare_in_shell,
    _press,
)


def _third_edge_direct(tmp_path: Path, *, stem: str):
    reentry, lineage, prepared, transition, root = _third_root_direct(
        tmp_path,
        stem=stem,
    )
    fixture_root = root.persistence.path.parent
    edge = persist_chromium_research_third_changed_basis_root_edge(
        root,
        revised_note_text=f"{stem} first post-third-root rationale.",
        root_source=root.persistence.path,
        destination=fixture_root / f"{stem}-edge.json",
    )
    return reentry, lineage, prepared, transition, root, edge


async def _reach_47c(shell, pilot, tmp_path: Path, *, stem: str):
    prepared = await _prepare_in_shell(shell, pilot, tmp_path, stem=stem)
    await _persist_third_transition(
        shell,
        pilot,
        prepared,
        tmp_path / f"{stem}-transition.json",
    )
    transition = shell.last_third_changed_basis_transition
    assert transition is not None
    await _persist_root_ui(
        shell,
        pilot,
        transition,
        destination=tmp_path / f"{stem}-root.json",
        rationale=f"{stem} exact third-root rationale before declaration.",
    )
    root = shell.last_third_changed_basis_revision_root
    assert root is not None
    await _persist_edge_ui(
        shell,
        pilot,
        root,
        destination=tmp_path / f"{stem}-edge.json",
        rationale=f"{stem} exact first post-third-root edge rationale.",
    )
    edge = shell.last_third_changed_basis_root_edge
    assert edge is not None
    return prepared, transition, root, edge


async def _adopt_ui(shell, pilot, edge, destination: Path) -> None:
    shell.query_one(
        "#research-third-changed-basis-session-adoption-edge-source", Input
    ).value = str(edge.persistence.path)
    shell.query_one(
        "#research-third-changed-basis-session-adoption-declaration-destination", Input
    ).value = str(destination)
    await _press(shell, pilot, "adopt-research-third-changed-basis-session")


def test_47d_application_declares_and_adopts_exact_47c_lineage(tmp_path: Path) -> None:
    *_, root, edge = _third_edge_direct(tmp_path, stem="47d-app")
    destination = tmp_path / "47d-app-declaration.json"

    result = adopt_chromium_research_third_changed_basis_governed_session(
        edge,
        edge_source=edge.persistence.path,
        declaration_destination=destination,
    )

    assert isinstance(result, ChromiumResearchThirdChangedBasisSessionAdoptionResult)
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
        match="exactly ChromiumResearchThirdChangedBasisRootEdgeResult",
    ):
        adopt_chromium_research_third_changed_basis_governed_session(
            object(),  # type: ignore[arg-type]
            edge_source=edge.persistence.path,
            declaration_destination=tmp_path / "47d-wrong-type.json",
        )
    assert not (tmp_path / "47d-wrong-type.json").exists()


def test_47d_application_uses_only_explicit_current_edge_path(tmp_path: Path) -> None:
    *_, root, edge = _third_edge_direct(tmp_path, stem="47d-moved")
    moved_edge = tmp_path / "47d-explicit-moved-edge.json"
    edge.persistence.path.rename(moved_edge)

    result = adopt_chromium_research_third_changed_basis_governed_session(
        edge,
        edge_source=moved_edge,
        declaration_destination=tmp_path / "47d-moved-declaration.json",
    )

    assert result.sequence.starting_predecessor is root.loaded_root
    assert result.sequence.edges[0].verification.path == moved_edge.resolve()
    assert (
        result.sequence.edges[0].verification.edge_record_sha256
        == edge.persistence.edge_record_sha256
    )


def test_47d_wrong_edge_locator_and_existing_destination_reject_before_write(
    tmp_path: Path,
) -> None:
    *_, root, edge = _third_edge_direct(tmp_path, stem="47d-wrong")
    destination = tmp_path / "47d-wrong-declaration.json"

    with pytest.raises(Exception):
        adopt_chromium_research_third_changed_basis_governed_session(
            edge,
            edge_source=root.persistence.path,
            declaration_destination=destination,
        )
    assert not destination.exists()

    existing = tmp_path / "47d-existing-declaration.json"
    existing.write_text("preserve exactly\n", encoding="utf-8")
    with pytest.raises(Exception):
        adopt_chromium_research_third_changed_basis_governed_session(
            edge,
            edge_source=edge.persistence.path,
            declaration_destination=existing,
        )
    assert existing.read_text(encoding="utf-8") == "preserve exactly\n"


@pytest.mark.asyncio
async def test_47d_shell_mounts_only_after_47c_and_explicitly_promotes_controller(
    tmp_path: Path,
) -> None:
    _, _, _, lineage = _continuation(tmp_path, stem="47d-ui")
    member, _ = _new_paragraph_member(tmp_path, stem="47d-ui-member")
    shell = create_third_changed_basis_session_adoption_research_session_shell(lineage)
    shell.configure_changed_basis_candidate((member,))
    original_controller = shell.research_controller
    original_reentry = shell.second_basis_epoch_continuation_reentry

    async with shell.run_test(size=(215, 530)) as pilot:
        await pilot.pause()
        assert len(shell.query(ResearchThirdChangedBasisSessionAdoptionControls)) == 0

        *_, edge = await _reach_47c(shell, pilot, tmp_path, stem="47d-ui")
        controls = shell.query_one(ResearchThirdChangedBasisSessionAdoptionControls)
        summary = str(
            shell.query_one(
                "#research-third-changed-basis-session-adoption-summary", Static
            ).content
        )
        assert "THIRD CHANGED-BASIS LINEAGE READY" in summary
        assert edge.persistence.edge_record_sha256 in summary
        assert shell.query_one(
            "#research-third-changed-basis-session-adoption-edge-source", Input
        ).value == ""
        assert shell.query_one(
            "#research-third-changed-basis-session-adoption-declaration-destination",
            Input,
        ).value == ""

        await _adopt_ui(
            shell,
            pilot,
            edge,
            tmp_path / "47d-ui-declaration.json",
        )

        result = shell.last_third_changed_basis_session_adoption
        assert result is not None
        assert result.edge_result is edge
        assert shell.research_controller is result.controller
        assert shell.research_controller is not original_controller
        assert shell.second_basis_epoch_continuation_reentry is original_reentry
        assert shell.research_reentry is None
        assert shell.changed_basis_candidate_items is None
        assert controls.prior_result is result
        assert shell.query_one(
            "#adopt-research-third-changed-basis-session", Button
        ).disabled
        receipt = str(
            shell.query_one(
                "#research-third-changed-basis-session-adoption-status", Static
            ).content
        )
        assert "explicitly adopted" in receipt
        assert "No 40A third-epoch fresh-process" in receipt
        assert len(shell.query("#research-second-basis-epoch-continuation-checkpoint-controls")) == 0
        assert len(shell.query("#research-second-basis-epoch-cumulative-checkpoint-controls")) == 0


@pytest.mark.asyncio
async def test_47d_post_adoption_rollover_does_not_mount_historical_second_epoch_checkpoint(
    tmp_path: Path,
) -> None:
    _, _, _, lineage = _continuation(tmp_path, stem="47d-rollover")
    member, _ = _new_paragraph_member(tmp_path, stem="47d-rollover-member")
    shell = create_third_changed_basis_session_adoption_research_session_shell(lineage)
    shell.configure_changed_basis_candidate((member,))

    async with shell.run_test(size=(220, 550)) as pilot:
        await pilot.pause()
        *_, edge = await _reach_47c(shell, pilot, tmp_path, stem="47d-rollover")
        await _adopt_ui(
            shell,
            pilot,
            edge,
            tmp_path / "47d-rollover-adoption-declaration.json",
        )
        adoption = shell.last_third_changed_basis_session_adoption
        assert adoption is not None
        adopted_controller = adoption.controller

        successor = tmp_path / "47d-rollover-successor.json"
        shell.query_one("#research-endpoint-revised-note", TextArea).text = (
            "Ordinary continuation after explicit third changed-basis adoption."
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
        ).value = str(tmp_path / "47d-rollover-next-declaration.json")
        await _press(shell, pilot, "rollover-research-session")

        assert shell.research_controller is not adopted_controller
        assert shell.last_research_rollover is not None
        assert len(shell.query("#research-second-basis-epoch-continuation-checkpoint-controls")) == 0
        assert len(shell.query("#research-second-basis-epoch-cumulative-checkpoint-controls")) == 0
        assert shell.second_basis_epoch_continuation_reentry is not None
        assert shell.last_third_changed_basis_session_adoption is adoption


@pytest.mark.asyncio
async def test_47d_inspection_preserves_launch_and_advances_only_current_state(
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
        create_inspectable_third_changed_basis_session_adoption_research_session_shell(
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

    async with persisted_shell.run_test(size=(220, 540)) as pilot:
        await pilot.pause()
        *_, edge = await _reach_47c(
            persisted_shell,
            pilot,
            persisted_dir,
            stem="persisted-47d",
        )
        await _adopt_ui(
            persisted_shell,
            pilot,
            edge,
            persisted_dir / "persisted-47d-declaration.json",
        )
        adoption = persisted_shell.last_third_changed_basis_session_adoption
        assert adoption is not None
        assert persisted_panel.launch_provenance is persisted_launch
        assert persisted_launch.launch_location_context == persisted_overlay.resolve()
        current = persisted_panel.current_state
        assert current.state_kind == "adopted third changed-basis governed session"
        assert current.state_source == "explicit 47D third changed-basis adoption"
        assert (
            current.endpoint_sha256
            == adoption.controller.declared_endpoint.verification.edge_record_sha256
        )

    _, _, raw_reentry, _ = _continuation(raw_dir, stem="raw")
    raw_shell = (
        create_inspectable_third_changed_basis_session_adoption_handoff_research_session_shell(
            raw_reentry
        )
    )
    raw_member, _ = _new_paragraph_member(raw_dir, stem="raw-member")
    raw_shell.configure_changed_basis_candidate((raw_member,))
    raw_panel = raw_shell.second_basis_epoch_authority_inspection
    raw_launch = raw_panel.launch_provenance
    assert raw_launch.launch_location_context is None

    async with raw_shell.run_test(size=(220, 540)) as pilot:
        await pilot.pause()
        *_, edge = await _reach_47c(raw_shell, pilot, raw_dir, stem="raw-47d")
        await _adopt_ui(
            raw_shell,
            pilot,
            edge,
            raw_dir / "raw-47d-declaration.json",
        )
        adoption = raw_shell.last_third_changed_basis_session_adoption
        assert adoption is not None
        assert raw_panel.launch_provenance is raw_launch
        assert raw_launch.launch_location_context is None
        current = raw_panel.current_state
        assert current.state_kind == "adopted third changed-basis governed session"
        assert current.state_source == (
            "explicit 47D third changed-basis adoption after in-process 38F handoff"
        )
        assert (
            current.endpoint_sha256
            == adoption.controller.declared_endpoint.verification.edge_record_sha256
        )


@pytest.mark.asyncio
async def test_plain_47c_product_does_not_gain_47d_surface(tmp_path: Path) -> None:
    _, _, _, lineage = _continuation(tmp_path, stem="47d-plain")
    member, _ = _new_paragraph_member(tmp_path, stem="47d-plain-member")
    shell = create_third_changed_basis_root_edge_research_session_shell(lineage)
    shell.configure_changed_basis_candidate((member,))

    async with shell.run_test(size=(205, 430)) as pilot:
        await pilot.pause()
        await _reach_47c(shell, pilot, tmp_path, stem="47d-plain")
        assert shell.last_third_changed_basis_root_edge is not None
        assert not hasattr(shell, "last_third_changed_basis_session_adoption")
        assert len(shell.query(ResearchThirdChangedBasisSessionAdoptionControls)) == 0


def test_47d_product_factories_reject_wrong_authority_family() -> None:
    with pytest.raises(
        TypeError,
        match="ChromiumResearchSecondBasisEpochContinuationShellLineage",
    ):
        create_third_changed_basis_session_adoption_research_session_shell(object())  # type: ignore[arg-type]

    with pytest.raises(
        TypeError,
        match="exactly ChromiumResearchSecondBasisEpochContinuationReentryResult",
    ):
        create_third_changed_basis_session_adoption_handoff_research_session_shell(object())  # type: ignore[arg-type]
