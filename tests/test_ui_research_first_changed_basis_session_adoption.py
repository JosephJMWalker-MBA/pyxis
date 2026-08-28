from __future__ import annotations

from pathlib import Path

import pytest
from textual.widgets import Button, Input, Static, TextArea

from pyxis.app.chromium_research_first_changed_basis_root_edge import (
    persist_chromium_research_first_changed_basis_root_edge,
)
from pyxis.app.chromium_research_first_changed_basis_session_adoption import (
    ChromiumResearchFirstChangedBasisSessionAdoptionResult,
    adopt_chromium_research_first_changed_basis_governed_session,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_sequence_persistence import (
    verify_chromium_research_working_set_note_revision_edge_sequence,
)
from pyxis.ui import (
    FirstChangedBasisSessionAdoptionResearchSessionShell,
    create_first_changed_basis_root_edge_research_session_shell,
    create_first_changed_basis_session_adoption_research_session_shell,
)
from pyxis.ui.chromium_research_first_changed_basis_session_adoption_textual import (
    ResearchFirstChangedBasisSessionAdoptionControls,
)
from test_app_chromium_research_session_working_set_extension import (
    _new_paragraph_member,
    _session,
)
from test_ui_research_first_changed_basis_revision_root import _persist_transition_ui
from test_ui_research_first_changed_basis_root_edge import (
    _direct_root,
    _persist_root_ui,
)
from test_ui_research_first_changed_basis_transition import _prepare, _press


_ROOT_FORMAT = (
    "pyxis.chromium.research_session_working_set_transition_revision_root.v1"
)
_EDGE_FORMAT = "pyxis.chromium.research_working_set_note_revision_edge.v1"
_SEQUENCE_FORMAT = "pyxis.chromium.research_working_set_note_revision_edge_sequence.v1"


def _direct_edge(tmp_path: Path, *, stem: str):
    fixture, reentry, prepared, transition, root = _direct_root(tmp_path, stem=stem)
    edge = persist_chromium_research_first_changed_basis_root_edge(
        root,
        revised_note_text=f"First post-root rationale for {stem}.",
        root_source=root.persistence.path,
        destination=tmp_path / f"{stem}-edge.json",
    )
    return fixture, reentry, prepared, transition, root, edge


async def _persist_edge_ui(
    shell,
    pilot,
    root_path: Path,
    tmp_path: Path,
    *,
    stem: str,
):
    destination = tmp_path / f"{stem}-edge.json"
    shell.query_one(
        "#research-first-changed-basis-root-edge-rationale", TextArea
    ).text = f"First ordinary edge rationale for {stem}."
    shell.query_one(
        "#research-first-changed-basis-root-edge-root-source", Input
    ).value = str(root_path)
    shell.query_one(
        "#research-first-changed-basis-root-edge-destination", Input
    ).value = str(destination)
    await _press(shell, pilot, "persist-research-first-changed-basis-root-edge")
    result = shell.last_first_changed_basis_root_edge
    assert result is not None
    return result, destination


async def _build_44d_ui(shell, pilot, fixture, tmp_path: Path, *, stem: str):
    prepared = await _prepare(shell, pilot, tmp_path, stem=stem)
    _, transition_path = await _persist_transition_ui(
        shell,
        pilot,
        fixture,
        prepared,
        tmp_path,
        stem=stem,
    )
    root, root_path = await _persist_root_ui(
        shell,
        pilot,
        fixture,
        prepared,
        transition_path,
        tmp_path,
        stem=stem,
    )
    edge, edge_path = await _persist_edge_ui(
        shell,
        pilot,
        root_path,
        tmp_path,
        stem=stem,
    )
    return prepared, root, edge, edge_path


def test_44e_application_declares_and_freshly_relinks_exact_root_backed_session(
    tmp_path: Path,
) -> None:
    _, _, _, _, root, edge = _direct_edge(tmp_path, stem="44e-app")
    destination = tmp_path / "44e-app-declaration.json"

    result = adopt_chromium_research_first_changed_basis_governed_session(
        edge,
        edge_source=edge.persistence.path,
        declaration_destination=destination,
    )

    assert isinstance(result, ChromiumResearchFirstChangedBasisSessionAdoptionResult)
    assert result.edge_result is edge
    assert result.sequence.starting_predecessor is root.loaded_root
    assert len(result.sequence.edges) == 1
    assert result.sequence.edges[0].verification.edge_record_sha256 == edge.persistence.edge_record_sha256
    assert result.declaration.path == destination.resolve()
    assert result.declaration.sequence_format == _SEQUENCE_FORMAT
    assert result.loaded_declaration.verification.sequence_record_sha256 == result.declaration.sequence_record_sha256
    assert result.loaded_declaration.sequence.starting_predecessor is root.loaded_root
    assert result.controller.loaded is result.loaded_declaration
    assert result.controller.declared_endpoint.verification.edge_record_sha256 == edge.persistence.edge_record_sha256
    assert result.controller.presentation.sequence.starting_record_format == _ROOT_FORMAT

    verification = verify_chromium_research_working_set_note_revision_edge_sequence(destination)
    assert verification.starting_predecessor.record_format == _ROOT_FORMAT
    assert verification.starting_predecessor.record_sha256 == root.persistence.root_record_sha256
    assert len(verification.edges) == 1
    assert verification.edges[0].record_format == _EDGE_FORMAT
    assert verification.edges[0].record_sha256 == edge.persistence.edge_record_sha256


def test_44e_application_accepts_moved_edge_only_through_explicit_new_path(
    tmp_path: Path,
) -> None:
    _, _, _, _, _, edge = _direct_edge(tmp_path, stem="44e-moved")
    moved_edge = tmp_path / "44e-explicit-moved-edge.json"
    edge.persistence.path.rename(moved_edge)

    result = adopt_chromium_research_first_changed_basis_governed_session(
        edge,
        edge_source=moved_edge,
        declaration_destination=tmp_path / "44e-moved-declaration.json",
    )

    assert result.sequence.edges[0].verification.path == moved_edge.resolve()
    assert result.loaded_declaration.sequence.edges[0].verification.path == moved_edge.resolve()
    assert result.controller.declared_endpoint.verification.edge_record_sha256 == edge.persistence.edge_record_sha256


def test_44e_wrong_edge_source_rejects_without_declaration_write(tmp_path: Path) -> None:
    _, _, _, _, root, edge = _direct_edge(tmp_path, stem="44e-wrong-edge")
    destination = tmp_path / "44e-wrong-edge-declaration.json"

    with pytest.raises(Exception):
        adopt_chromium_research_first_changed_basis_governed_session(
            edge,
            edge_source=root.persistence.path,
            declaration_destination=destination,
        )
    assert not destination.exists()


@pytest.mark.asyncio
async def test_44e_mounts_only_after_44d_and_explicitly_replaces_governed_session(
    tmp_path: Path,
) -> None:
    fixture, reentry = _session(tmp_path)
    member, _ = _new_paragraph_member(tmp_path, stem="44e-ui")
    shell = create_first_changed_basis_session_adoption_research_session_shell(
        reentry,
        (member,),
    )
    original_controller = shell.research_controller

    assert isinstance(shell, FirstChangedBasisSessionAdoptionResearchSessionShell)

    async with shell.run_test(size=(200, 420)) as pilot:
        await pilot.pause()
        assert len(shell.query(ResearchFirstChangedBasisSessionAdoptionControls)) == 0

        _, root, edge, edge_path = await _build_44d_ui(
            shell,
            pilot,
            fixture,
            tmp_path,
            stem="44e-ui",
        )

        controls = shell.query_one(ResearchFirstChangedBasisSessionAdoptionControls)
        summary = str(
            shell.query_one(
                "#research-first-changed-basis-session-adoption-summary",
                Static,
            ).content
        )
        assert "READY FOR EXPLICIT SHELL ADOPTION" in summary
        assert root.persistence.root_record_sha256 in summary
        assert edge.persistence.edge_record_sha256 in summary
        assert edge.loaded_edge.revision.revised_note.note_text in summary
        assert shell.query_one(
            "#research-first-changed-basis-session-adoption-edge-source", Input
        ).value == ""
        assert shell.query_one(
            "#research-first-changed-basis-session-adoption-declaration-destination",
            Input,
        ).value == ""
        assert len(shell.query("#research-first-changed-basis-session-adoption-root-source")) == 0
        assert shell.research_controller is original_controller

        declaration = tmp_path / "44e-ui-declaration.json"
        shell.query_one(
            "#research-first-changed-basis-session-adoption-edge-source", Input
        ).value = str(edge_path)
        shell.query_one(
            "#research-first-changed-basis-session-adoption-declaration-destination",
            Input,
        ).value = str(declaration)
        await _press(shell, pilot, "adopt-research-first-changed-basis-session")

        result = shell.last_first_changed_basis_session_adoption
        assert result is not None
        assert result.edge_result is edge
        assert shell.research_controller is result.controller
        assert shell.research_controller is not original_controller
        assert shell.research_session is result.controller.presentation
        assert shell.research_reentry is None
        assert shell.last_research_rollover is None
        assert shell.last_research_restart_plan is None
        assert shell.research_presentation.starting_record_format == _ROOT_FORMAT
        assert shell.research_controller.declared_endpoint.verification.edge_record_sha256 == edge.persistence.edge_record_sha256
        assert controls.prior_result is result
        assert shell.query_one(
            "#adopt-research-first-changed-basis-session", Button
        ).disabled
        assert len(shell.query("#research-revision-edge-sequence")) == 1
        assert len(shell.query("#research-endpoint-revision-controls")) == 1
        assert len(shell.query("#research-session-rollover-controls")) == 1
        assert len(shell.query("#research-session-restart-plan-controls")) == 0
        receipt = str(
            shell.query_one(
                "#research-first-changed-basis-session-adoption-status", Static
            ).content
        )
        assert "explicitly adopted as this shell's governed session" in receipt
        assert "No global current/latest/head" in receipt
        assert "no 35B fresh-process" in receipt
        assert declaration.exists()

        successor = tmp_path / "44e-ui-successor.json"
        shell.query_one("#research-endpoint-revised-note", TextArea).text = (
            "Ordinary governed revision after explicit changed-basis adoption."
        )
        shell.query_one("#research-endpoint-prior-edge-source", Input).value = str(edge_path)
        shell.query_one("#research-endpoint-destination", Input).value = str(successor)
        await _press(shell, pilot, "persist-research-endpoint-revision")
        assert successor.exists()

        adopted_controller = shell.research_controller
        shell.query_one("#research-session-rollover-successor-source", Input).value = str(
            successor
        )
        shell.query_one(
            "#research-session-rollover-declaration-destination", Input
        ).value = str(tmp_path / "44e-ui-continuation-declaration.json")
        await _press(shell, pilot, "rollover-research-session")
        assert shell.research_controller is not adopted_controller
        assert shell.research_reentry is None
        assert len(shell.query("#research-session-restart-plan-controls")) == 0


@pytest.mark.asyncio
async def test_44e_wrong_edge_locator_keeps_old_controller_and_form_unlocked(
    tmp_path: Path,
) -> None:
    fixture, reentry = _session(tmp_path)
    member, _ = _new_paragraph_member(tmp_path, stem="44e-wrong-ui")
    shell = create_first_changed_basis_session_adoption_research_session_shell(
        reentry,
        (member,),
    )

    async with shell.run_test(size=(195, 400)) as pilot:
        await pilot.pause()
        _, root, _, _ = await _build_44d_ui(
            shell,
            pilot,
            fixture,
            tmp_path,
            stem="44e-wrong-ui",
        )
        before = shell.research_controller
        declaration = tmp_path / "44e-wrong-ui-declaration.json"
        shell.query_one(
            "#research-first-changed-basis-session-adoption-edge-source", Input
        ).value = str(root.persistence.path)
        shell.query_one(
            "#research-first-changed-basis-session-adoption-declaration-destination",
            Input,
        ).value = str(declaration)
        await _press(shell, pilot, "adopt-research-first-changed-basis-session")

        assert shell.last_first_changed_basis_session_adoption is None
        assert shell.research_controller is before
        assert not declaration.exists()
        assert not shell.query_one(
            "#adopt-research-first-changed-basis-session", Button
        ).disabled
        assert "Adoption failed:" in str(
            shell.query_one(
                "#research-first-changed-basis-session-adoption-status", Static
            ).content
        )


@pytest.mark.asyncio
async def test_old_basis_rollover_before_44e_does_not_block_explicit_changed_basis_adoption(
    tmp_path: Path,
) -> None:
    fixture, reentry = _session(tmp_path)
    member, _ = _new_paragraph_member(tmp_path, stem="44e-branch")
    shell = create_first_changed_basis_session_adoption_research_session_shell(
        reentry,
        (member,),
    )
    original_controller = shell.research_controller

    async with shell.run_test(size=(205, 450)) as pilot:
        await pilot.pause()
        _, _, edge, edge_path = await _build_44d_ui(
            shell,
            pilot,
            fixture,
            tmp_path,
            stem="44e-branch",
        )
        adoption_controls = shell.query_one(
            ResearchFirstChangedBasisSessionAdoptionControls
        )

        old_successor = tmp_path / "44e-old-basis-successor.json"
        shell.query_one("#research-endpoint-revised-note", TextArea).text = (
            "Old-basis branch continues before explicit changed-basis adoption."
        )
        shell.query_one("#research-endpoint-prior-edge-source", Input).value = str(
            fixture.v6_path
        )
        shell.query_one("#research-endpoint-destination", Input).value = str(old_successor)
        await _press(shell, pilot, "persist-research-endpoint-revision")
        shell.query_one("#research-session-rollover-successor-source", Input).value = str(
            old_successor
        )
        shell.query_one(
            "#research-session-rollover-declaration-destination", Input
        ).value = str(tmp_path / "44e-old-basis-declaration.json")
        await _press(shell, pilot, "rollover-research-session")

        old_continuation_controller = shell.research_controller
        assert old_continuation_controller is not original_controller
        assert adoption_controls.prior_result is None

        shell.query_one(
            "#research-first-changed-basis-session-adoption-edge-source", Input
        ).value = str(edge_path)
        shell.query_one(
            "#research-first-changed-basis-session-adoption-declaration-destination",
            Input,
        ).value = str(tmp_path / "44e-branch-adoption.json")
        await _press(shell, pilot, "adopt-research-first-changed-basis-session")

        result = shell.last_first_changed_basis_session_adoption
        assert result is not None
        assert result.edge_result is edge
        assert shell.research_controller is result.controller
        assert shell.research_controller is not old_continuation_controller
        assert shell.research_controller.declared_endpoint.verification.edge_record_sha256 == edge.persistence.edge_record_sha256
        assert shell.research_reentry is None
        assert len(shell.query("#research-session-restart-plan-controls")) == 0


@pytest.mark.asyncio
async def test_plain_44d_shell_never_gains_44e_adoption_controls_after_edge_success(
    tmp_path: Path,
) -> None:
    fixture, reentry = _session(tmp_path)
    member, _ = _new_paragraph_member(tmp_path, stem="44e-plain-44d")
    shell = create_first_changed_basis_root_edge_research_session_shell(
        reentry,
        (member,),
    )

    async with shell.run_test(size=(195, 360)) as pilot:
        await pilot.pause()
        await _build_44d_ui(
            shell,
            pilot,
            fixture,
            tmp_path,
            stem="44e-plain-44d",
        )
        assert shell.last_first_changed_basis_root_edge is not None
        assert len(shell.query(ResearchFirstChangedBasisSessionAdoptionControls)) == 0
        assert not hasattr(shell, "last_first_changed_basis_session_adoption")
