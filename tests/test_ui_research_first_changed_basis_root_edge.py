from __future__ import annotations

from pathlib import Path

import pytest
from textual.widgets import Button, Input, Static, TextArea

from pyxis.app.chromium_research_first_changed_basis_revision_root import (
    persist_chromium_research_first_changed_basis_revision_root,
)
from pyxis.app.chromium_research_first_changed_basis_root_edge import (
    ChromiumResearchFirstChangedBasisRootEdgeResult,
    persist_chromium_research_first_changed_basis_root_edge,
)
from pyxis.app.chromium_research_first_changed_basis_transition import (
    persist_chromium_research_first_changed_basis_transition,
)
from pyxis.ui import (
    FirstChangedBasisRootEdgeResearchSessionShell,
    create_first_changed_basis_root_edge_research_session_shell,
    create_first_changed_basis_root_research_session_shell,
)
from pyxis.ui.chromium_research_first_changed_basis_root_edge_textual import (
    ResearchFirstChangedBasisRootEdgeControls,
)
from test_app_chromium_research_session_working_set_extension import (
    _new_paragraph_member,
    _persist_extension,
    _session,
)
from test_ui_research_first_changed_basis_revision_root import (
    _persist_transition_ui,
)
from test_ui_research_first_changed_basis_transition import _prepare, _press


async def _persist_root_ui(
    shell,
    pilot,
    fixture,
    prepared,
    transition_path: Path,
    tmp_path: Path,
    *,
    stem: str,
):
    destination = tmp_path / f"{stem}-root.json"
    shell.query_one(
        "#research-first-changed-basis-revision-root-rationale", TextArea
    ).text = f"First changed-basis root rationale for {stem}."
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
    ).value = str(destination)
    await _press(shell, pilot, "persist-research-first-changed-basis-revision-root")
    result = shell.last_first_changed_basis_revision_root
    assert result is not None
    return result, destination


def _direct_root(tmp_path: Path, *, stem: str):
    fixture, reentry = _session(tmp_path)
    member, _ = _new_paragraph_member(tmp_path, stem=stem)
    prepared = _persist_extension(
        tmp_path,
        reentry,
        (member,),
        rationale_text=f"Prepared changed basis for {stem}.",
        stem=stem,
    )
    transition = persist_chromium_research_first_changed_basis_transition(
        reentry.controller,
        reentry,
        prepared,
        prior_edge_source=fixture.v6_path,
        working_set_source=prepared.working_set_persistence.path,
        note_source=prepared.note_persistence.path,
        destination=tmp_path / f"{stem}-transition.json",
    )
    root = persist_chromium_research_first_changed_basis_revision_root(
        transition,
        revised_note_text=f"First root rationale for {stem}.",
        prior_edge_source=fixture.v6_path,
        working_set_source=prepared.working_set_persistence.path,
        note_source=prepared.note_persistence.path,
        transition_source=transition.persistence.path,
        destination=tmp_path / f"{stem}-root.json",
    )
    return fixture, reentry, prepared, transition, root


def test_44d_application_persists_existing_format_edge_and_freshly_relinks_root(
    tmp_path: Path,
) -> None:
    _, _, _, _, root = _direct_root(tmp_path, stem="44d-app")
    edge_destination = tmp_path / "44d-app-edge.json"
    revised_text = "First ordinary rationale after the changed-basis root."

    result = persist_chromium_research_first_changed_basis_root_edge(
        root,
        revised_note_text=revised_text,
        root_source=root.persistence.path,
        destination=edge_destination,
    )

    assert isinstance(result, ChromiumResearchFirstChangedBasisRootEdgeResult)
    assert result.root_result is root
    assert result.persistence.extension is result.extension
    assert result.persistence.path == edge_destination.resolve()
    assert result.persistence.edge_format == "pyxis.chromium.research_working_set_note_revision_edge.v1"
    assert result.loaded_edge.verification.edge_record_sha256 == result.persistence.edge_record_sha256
    assert (
        result.loaded_edge.verification.predecessor_record_sha256
        == root.persistence.root_record_sha256
    )
    assert (
        result.loaded_edge.verification.predecessor_format
        == "pyxis.chromium.research_session_working_set_transition_revision_root.v1"
    )
    assert result.loaded_edge.predecessor is root.loaded_root
    assert result.loaded_edge.revision.revised_note.note_text == revised_text

    noop_destination = tmp_path / "44d-noop-edge.json"
    with pytest.raises(ValueError, match="differ exactly"):
        persist_chromium_research_first_changed_basis_root_edge(
            root,
            revised_note_text=root.loaded_root.root.revision.revised_note.note_text,
            root_source=root.persistence.path,
            destination=noop_destination,
        )
    assert not noop_destination.exists()


def test_44d_application_accepts_moved_root_only_via_explicit_new_path(
    tmp_path: Path,
) -> None:
    _, _, _, _, root = _direct_root(tmp_path, stem="44d-moved")
    moved_root = tmp_path / "44d-explicit-moved-root.json"
    root.persistence.path.rename(moved_root)

    result = persist_chromium_research_first_changed_basis_root_edge(
        root,
        revised_note_text="First ordinary edge after the explicitly relocated root.",
        root_source=moved_root,
        destination=tmp_path / "44d-moved-edge.json",
    )

    assert result.persistence.path.exists()
    assert result.persistence.root_verification.path == moved_root.resolve()
    assert result.loaded_edge.verification.predecessor_record_sha256 == root.persistence.root_record_sha256


def test_44d_wrong_root_source_rejects_without_edge_write(tmp_path: Path) -> None:
    _, _, _, transition, root = _direct_root(tmp_path, stem="44d-wrong-root")
    destination = tmp_path / "44d-wrong-root-edge.json"

    with pytest.raises(Exception):
        persist_chromium_research_first_changed_basis_root_edge(
            root,
            revised_note_text="A valid new rationale with the wrong root locator.",
            root_source=transition.persistence.path,
            destination=destination,
        )
    assert not destination.exists()


@pytest.mark.asyncio
async def test_first_root_edge_shell_mounts_only_after_44c_success_and_persists_without_adoption(
    tmp_path: Path,
) -> None:
    fixture, reentry = _session(tmp_path)
    member, _ = _new_paragraph_member(tmp_path, stem="44d-ui")
    shell = create_first_changed_basis_root_edge_research_session_shell(
        reentry,
        (member,),
    )
    original_controller = shell.research_controller
    original_session = shell.research_session

    assert isinstance(shell, FirstChangedBasisRootEdgeResearchSessionShell)

    async with shell.run_test(size=(190, 330)) as pilot:
        await pilot.pause()
        assert len(shell.query(ResearchFirstChangedBasisRootEdgeControls)) == 0

        prepared = await _prepare(shell, pilot, tmp_path, stem="44d-ui")
        transition, transition_path = await _persist_transition_ui(
            shell,
            pilot,
            fixture,
            prepared,
            tmp_path,
            stem="44d-ui",
        )
        assert transition is shell.last_first_changed_basis_transition
        assert len(shell.query(ResearchFirstChangedBasisRootEdgeControls)) == 0

        root, root_path = await _persist_root_ui(
            shell,
            pilot,
            fixture,
            prepared,
            transition_path,
            tmp_path,
            stem="44d-ui",
        )
        controls = shell.query_one(ResearchFirstChangedBasisRootEdgeControls)
        summary = str(
            shell.query_one(
                "#research-first-changed-basis-root-edge-root-summary", Static
            ).content
        )
        assert "PERSISTED FIRST CHANGED-BASIS ROOT" in summary
        assert "NO ROOT-BACKED SESSION YET" in summary
        assert root.persistence.root_record_sha256 in summary
        assert root.loaded_root.root.revision.revised_note.note_text in summary
        assert shell.query_one(
            "#research-first-changed-basis-root-edge-rationale", TextArea
        ).text == ""
        assert shell.query_one(
            "#research-first-changed-basis-root-edge-root-source", Input
        ).value == ""
        assert shell.query_one(
            "#research-first-changed-basis-root-edge-destination", Input
        ).value == ""

        revised_text = "  First ordinary edge after the root 😀\nStill explicit.  "
        edge_destination = tmp_path / "44d-ui-edge.json"
        shell.query_one(
            "#research-first-changed-basis-root-edge-rationale", TextArea
        ).text = revised_text
        shell.query_one(
            "#research-first-changed-basis-root-edge-root-source", Input
        ).value = str(root_path)
        shell.query_one(
            "#research-first-changed-basis-root-edge-destination", Input
        ).value = str(edge_destination)
        await _press(shell, pilot, "persist-research-first-changed-basis-root-edge")

        result = shell.last_first_changed_basis_root_edge
        assert result is not None
        assert result.root_result is root
        assert result.loaded_edge.revision.revised_note.note_text == revised_text
        assert shell.research_controller is original_controller
        assert shell.research_session is original_session
        assert controls.prior_result is result
        assert shell.query_one(
            "#persist-research-first-changed-basis-root-edge", Button
        ).disabled
        receipt = str(
            shell.query_one(
                "#research-first-changed-basis-root-edge-status", Static
            ).content
        )
        assert "Mounted governed session unchanged" in receipt
        assert "Ordinary edge lineage has resumed locally" in receipt
        assert "no sequence declaration" in receipt
        assert "35A" in receipt
        assert edge_destination.exists()
        assert len(shell.query("#adopt-root-backed-research-session")) == 0


@pytest.mark.asyncio
async def test_old_basis_rollover_after_44c_does_not_invalidate_first_root_edge(
    tmp_path: Path,
) -> None:
    fixture, reentry = _session(tmp_path)
    member, _ = _new_paragraph_member(tmp_path, stem="44d-branch")
    shell = create_first_changed_basis_root_edge_research_session_shell(
        reentry,
        (member,),
    )
    original_controller = shell.research_controller

    async with shell.run_test(size=(195, 350)) as pilot:
        await pilot.pause()
        prepared = await _prepare(shell, pilot, tmp_path, stem="44d-branch")
        _, transition_path = await _persist_transition_ui(
            shell,
            pilot,
            fixture,
            prepared,
            tmp_path,
            stem="44d-branch",
        )
        root, root_path = await _persist_root_ui(
            shell,
            pilot,
            fixture,
            prepared,
            transition_path,
            tmp_path,
            stem="44d-branch",
        )
        edge_controls = shell.query_one(ResearchFirstChangedBasisRootEdgeControls)

        successor = tmp_path / "44d-old-basis-successor.json"
        shell.query_one("#research-endpoint-revised-note", TextArea).text = (
            "Old-basis branch continues after changed-basis root persistence."
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
        ).value = str(tmp_path / "44d-old-basis-declaration.json")
        await _press(shell, pilot, "rollover-research-session")

        assert shell.research_controller is not original_controller
        assert edge_controls.prior_result is None
        assert not shell.query_one(
            "#persist-research-first-changed-basis-root-edge", Button
        ).disabled

        shell.query_one(
            "#research-first-changed-basis-root-edge-rationale", TextArea
        ).text = "Changed-basis root receives its first ordinary edge after old-basis rollover."
        shell.query_one(
            "#research-first-changed-basis-root-edge-root-source", Input
        ).value = str(root_path)
        shell.query_one(
            "#research-first-changed-basis-root-edge-destination", Input
        ).value = str(tmp_path / "44d-branch-edge.json")
        await _press(shell, pilot, "persist-research-first-changed-basis-root-edge")

        edge = shell.last_first_changed_basis_root_edge
        assert edge is not None
        assert edge.root_result is root
        assert shell.research_controller is not original_controller


@pytest.mark.asyncio
async def test_plain_44c_shell_never_gains_44d_edge_controls_after_root_success(
    tmp_path: Path,
) -> None:
    fixture, reentry = _session(tmp_path)
    member, _ = _new_paragraph_member(tmp_path, stem="44d-plain-44c")
    shell = create_first_changed_basis_root_research_session_shell(reentry, (member,))

    async with shell.run_test(size=(185, 290)) as pilot:
        await pilot.pause()
        prepared = await _prepare(shell, pilot, tmp_path, stem="44d-plain-44c")
        _, transition_path = await _persist_transition_ui(
            shell,
            pilot,
            fixture,
            prepared,
            tmp_path,
            stem="44d-plain-44c",
        )
        await _persist_root_ui(
            shell,
            pilot,
            fixture,
            prepared,
            transition_path,
            tmp_path,
            stem="44d-plain-44c",
        )
        assert shell.last_first_changed_basis_revision_root is not None
        assert len(shell.query(ResearchFirstChangedBasisRootEdgeControls)) == 0
        assert not hasattr(shell, "last_first_changed_basis_root_edge")
