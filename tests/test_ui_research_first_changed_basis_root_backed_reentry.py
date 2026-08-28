from __future__ import annotations

from pathlib import Path

import pytest
from textual.widgets import Button, Input, Static, TextArea

from pyxis.ui import (
    FirstChangedBasisRootBackedReentryResearchSessionShell,
    create_first_changed_basis_root_backed_reentry_research_session_shell,
    create_first_changed_basis_session_adoption_research_session_shell,
)
from pyxis.ui.chromium_research_first_changed_basis_root_backed_reentry_textual import (
    ResearchFirstChangedBasisRootBackedReentryControls,
)
from test_app_chromium_research_session_working_set_extension import (
    _new_paragraph_member,
    _session,
)
from test_ui_research_first_changed_basis_session_adoption import _build_44d_ui
from test_ui_research_first_changed_basis_transition import _press


async def _adopt_44e(
    shell,
    pilot,
    edge_path: Path,
    tmp_path: Path,
    *,
    stem: str,
):
    declaration = tmp_path / f"{stem}-adoption-declaration.json"
    shell.query_one(
        "#research-first-changed-basis-session-adoption-edge-source", Input
    ).value = str(edge_path)
    shell.query_one(
        "#research-first-changed-basis-session-adoption-declaration-destination",
        Input,
    ).value = str(declaration)
    await _press(shell, pilot, "adopt-research-first-changed-basis-session")
    adoption = shell.last_first_changed_basis_session_adoption
    assert adoption is not None
    return adoption, declaration


def _fill_44f_paragraph_inputs(
    shell,
    *,
    member,
    prepared,
    transition_path: Path,
    root_path: Path,
    edge_path: Path,
    declaration_path: Path,
) -> None:
    shell.query_one(
        "#research-first-changed-basis-reentry-member-0-capture-source", Input
    ).value = str(member.note.selection.source.verification.path)
    shell.query_one(
        "#research-first-changed-basis-reentry-member-0-note-source", Input
    ).value = str(member.verification.path)
    values = {
        "changed-working-set-source": prepared.working_set_persistence.path,
        "changed-note-source": prepared.note_persistence.path,
        "transition-source": transition_path,
        "root-source": root_path,
        "first-edge-source": edge_path,
        "declaration-source": declaration_path,
    }
    for suffix, path in values.items():
        shell.query_one(
            f"#research-first-changed-basis-reentry-{suffix}", Input
        ).value = str(path)


@pytest.mark.asyncio
async def test_44f_mounts_only_after_44e_and_verifies_without_replacing_mounted_session(
    tmp_path: Path,
) -> None:
    fixture, reentry = _session(tmp_path)
    member, _ = _new_paragraph_member(tmp_path, stem="44f-ui")
    shell = create_first_changed_basis_root_backed_reentry_research_session_shell(
        reentry,
        (member,),
    )
    assert isinstance(shell, FirstChangedBasisRootBackedReentryResearchSessionShell)

    async with shell.run_test(size=(210, 520)) as pilot:
        await pilot.pause()
        assert len(shell.query(ResearchFirstChangedBasisRootBackedReentryControls)) == 0

        prepared, root, edge, edge_path = await _build_44d_ui(
            shell,
            pilot,
            fixture,
            tmp_path,
            stem="44f-ui",
        )
        assert len(shell.query(ResearchFirstChangedBasisRootBackedReentryControls)) == 0
        transition = shell.last_first_changed_basis_transition
        assert transition is not None

        adoption, declaration = await _adopt_44e(
            shell,
            pilot,
            edge_path,
            tmp_path,
            stem="44f-ui",
        )
        controls = shell.query_one(ResearchFirstChangedBasisRootBackedReentryControls)
        active_controller = shell.research_controller
        active_session = shell.research_session

        summary = str(
            shell.query_one(
                "#research-first-changed-basis-root-backed-reentry-summary", Static
            ).content
        )
        assert "RESTARTABILITY NOT YET PERSISTED" in summary
        assert root.persistence.root_record_sha256 in summary
        assert adoption.declaration.sequence_record_sha256 in summary
        assert edge.persistence.edge_record_sha256 in summary
        assert "Appended evidence members: 1" in summary

        assert shell.query_one(
            "#research-first-changed-basis-reentry-member-0-capture-source", Input
        ).value == ""
        assert shell.query_one(
            "#research-first-changed-basis-reentry-member-0-note-source", Input
        ).value == ""
        assert len(shell.query("#research-first-changed-basis-reentry-member-0-first-capture-source")) == 0
        assert len(shell.query("#research-first-changed-basis-reentry-member-0-second-capture-source")) == 0
        for suffix in (
            "changed-working-set-source",
            "changed-note-source",
            "transition-source",
            "root-source",
            "first-edge-source",
            "declaration-source",
        ):
            assert shell.query_one(
                f"#research-first-changed-basis-reentry-{suffix}", Input
            ).value == ""
        assert len(shell.query("#research-first-changed-basis-reentry-overlay-destination")) == 0

        before = set(tmp_path.iterdir())
        _fill_44f_paragraph_inputs(
            shell,
            member=member,
            prepared=prepared,
            transition_path=transition.persistence.path,
            root_path=root.persistence.path,
            edge_path=edge_path,
            declaration_path=declaration,
        )
        await _press(shell, pilot, "verify-research-first-changed-basis-root-backed-reentry")

        result = shell.last_first_changed_basis_root_backed_reentry_verification
        assert result is not None
        assert result.adoption_result is adoption
        assert result.initial_ordinary_reentry is reentry
        assert result.fresh_reentry.controller is not active_controller
        assert result.fresh_reentry.controller.presentation == adoption.controller.presentation
        assert shell.research_controller is active_controller
        assert shell.research_session is active_session
        assert shell.research_reentry is None
        assert set(tmp_path.iterdir()) == before
        assert controls.prior_result is result
        assert shell.query_one(
            "#verify-research-first-changed-basis-root-backed-reentry", Button
        ).disabled
        receipt = str(
            shell.query_one(
                "#research-first-changed-basis-root-backed-reentry-status", Static
            ).content
        )
        assert "freshly reconstructed through 35B" in receipt
        assert "Mounted governed session unchanged" in receipt
        assert "no durable 35C overlay" in receipt


@pytest.mark.asyncio
async def test_44f_wrong_appended_locator_leaves_mounted_controller_and_form_unlocked(
    tmp_path: Path,
) -> None:
    fixture, reentry = _session(tmp_path)
    member, _ = _new_paragraph_member(tmp_path, stem="44f-wrong-ui")
    shell = create_first_changed_basis_root_backed_reentry_research_session_shell(
        reentry,
        (member,),
    )

    async with shell.run_test(size=(210, 520)) as pilot:
        await pilot.pause()
        prepared, root, _, edge_path = await _build_44d_ui(
            shell,
            pilot,
            fixture,
            tmp_path,
            stem="44f-wrong-ui",
        )
        transition = shell.last_first_changed_basis_transition
        assert transition is not None
        _, declaration = await _adopt_44e(
            shell,
            pilot,
            edge_path,
            tmp_path,
            stem="44f-wrong-ui",
        )
        active_controller = shell.research_controller

        wrong = fixture.plan.working_set_members[0]
        shell.query_one(
            "#research-first-changed-basis-reentry-member-0-capture-source", Input
        ).value = str(wrong.capture_source)
        shell.query_one(
            "#research-first-changed-basis-reentry-member-0-note-source", Input
        ).value = str(wrong.note_source)
        values = {
            "changed-working-set-source": prepared.working_set_persistence.path,
            "changed-note-source": prepared.note_persistence.path,
            "transition-source": transition.persistence.path,
            "root-source": root.persistence.path,
            "first-edge-source": edge_path,
            "declaration-source": declaration,
        }
        for suffix, path in values.items():
            shell.query_one(
                f"#research-first-changed-basis-reentry-{suffix}", Input
            ).value = str(path)

        before = set(tmp_path.iterdir())
        await _press(shell, pilot, "verify-research-first-changed-basis-root-backed-reentry")

        assert shell.last_first_changed_basis_root_backed_reentry_verification is None
        assert shell.research_controller is active_controller
        assert set(tmp_path.iterdir()) == before
        assert not shell.query_one(
            "#verify-research-first-changed-basis-root-backed-reentry", Button
        ).disabled
        assert "Re-entry verification failed:" in str(
            shell.query_one(
                "#research-first-changed-basis-root-backed-reentry-status", Static
            ).content
        )


@pytest.mark.asyncio
async def test_adopted_session_rollover_before_44f_does_not_retarget_historical_verification(
    tmp_path: Path,
) -> None:
    fixture, reentry = _session(tmp_path)
    member, _ = _new_paragraph_member(tmp_path, stem="44f-rollover")
    shell = create_first_changed_basis_root_backed_reentry_research_session_shell(
        reentry,
        (member,),
    )

    async with shell.run_test(size=(215, 560)) as pilot:
        await pilot.pause()
        prepared, root, edge, edge_path = await _build_44d_ui(
            shell,
            pilot,
            fixture,
            tmp_path,
            stem="44f-rollover",
        )
        transition = shell.last_first_changed_basis_transition
        assert transition is not None
        adoption, declaration = await _adopt_44e(
            shell,
            pilot,
            edge_path,
            tmp_path,
            stem="44f-rollover",
        )
        historical_adopted_controller = shell.research_controller

        successor = tmp_path / "44f-rollover-successor.json"
        shell.query_one("#research-endpoint-revised-note", TextArea).text = (
            "Ordinary continuation after 44E but before restartability verification."
        )
        shell.query_one("#research-endpoint-prior-edge-source", Input).value = str(edge_path)
        shell.query_one("#research-endpoint-destination", Input).value = str(successor)
        await _press(shell, pilot, "persist-research-endpoint-revision")
        shell.query_one("#research-session-rollover-successor-source", Input).value = str(successor)
        shell.query_one(
            "#research-session-rollover-declaration-destination", Input
        ).value = str(tmp_path / "44f-rollover-continuation-declaration.json")
        await _press(shell, pilot, "rollover-research-session")

        continuation_controller = shell.research_controller
        assert continuation_controller is not historical_adopted_controller
        controls = shell.query_one(ResearchFirstChangedBasisRootBackedReentryControls)
        assert controls.adoption_result is adoption

        _fill_44f_paragraph_inputs(
            shell,
            member=member,
            prepared=prepared,
            transition_path=transition.persistence.path,
            root_path=root.persistence.path,
            edge_path=edge_path,
            declaration_path=declaration,
        )
        await _press(shell, pilot, "verify-research-first-changed-basis-root-backed-reentry")

        result = shell.last_first_changed_basis_root_backed_reentry_verification
        assert result is not None
        assert result.adoption_result is adoption
        assert result.fresh_reentry.controller.presentation == adoption.controller.presentation
        assert (
            result.fresh_reentry.controller.declared_endpoint.verification.edge_record_sha256
            == edge.persistence.edge_record_sha256
        )
        assert shell.research_controller is continuation_controller
        assert shell.research_controller.presentation != adoption.controller.presentation


@pytest.mark.asyncio
async def test_plain_44e_shell_never_gains_44f_reentry_verification_controls(
    tmp_path: Path,
) -> None:
    fixture, reentry = _session(tmp_path)
    member, _ = _new_paragraph_member(tmp_path, stem="44f-plain-44e")
    shell = create_first_changed_basis_session_adoption_research_session_shell(
        reentry,
        (member,),
    )

    async with shell.run_test(size=(205, 470)) as pilot:
        await pilot.pause()
        _, _, _, edge_path = await _build_44d_ui(
            shell,
            pilot,
            fixture,
            tmp_path,
            stem="44f-plain-44e",
        )
        await _adopt_44e(
            shell,
            pilot,
            edge_path,
            tmp_path,
            stem="44f-plain-44e",
        )
        assert shell.last_first_changed_basis_session_adoption is not None
        assert len(shell.query(ResearchFirstChangedBasisRootBackedReentryControls)) == 0
        assert not hasattr(
            shell,
            "last_first_changed_basis_root_backed_reentry_verification",
        )
