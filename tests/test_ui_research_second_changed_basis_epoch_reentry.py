from __future__ import annotations

from pathlib import Path

import pytest
from textual.widgets import Input

from pyxis.app.chromium_research_second_changed_basis_epoch_reentry import (
    ChromiumResearchSecondChangedBasisEpochReentryResult,
    verify_chromium_research_second_changed_basis_epoch_reentry,
)
from pyxis.app.chromium_research_second_changed_basis_session_adoption import (
    adopt_chromium_research_second_changed_basis_governed_session,
)
from pyxis.app.chromium_research_session_reentry import (
    ChromiumResearchParagraphNoteReentryLocator,
)
from pyxis.ui.chromium_research_second_changed_basis_epoch_reentry_textual import (
    ResearchSecondChangedBasisEpochReentryControls,
)
from pyxis.ui.root_backed_authority_inspection_shell import (
    create_inspectable_root_backed_continuation_handoff_research_session_shell,
)
from pyxis.ui.second_changed_basis_epoch_reentry_research_session_shell import (
    create_second_changed_basis_epoch_reentry_research_session_shell,
)
from test_app_chromium_research_session_working_set_extension import _new_paragraph_member
from test_ui_research_second_changed_basis_session_adoption import (
    _adopt_ui,
    _reach_46c,
    _second_edge_direct,
)
from test_ui_research_second_changed_basis_transition import (
    _continuation,
    _press,
)


def _paragraph_locator(item) -> ChromiumResearchParagraphNoteReentryLocator:
    return ChromiumResearchParagraphNoteReentryLocator(
        capture_source=item.note.selection.source.verification.path,
        note_source=item.verification.path,
    )


def test_46e_application_freshly_reconstructs_both_exact_ancestry_layers(
    tmp_path: Path,
) -> None:
    values, _, prepared, transition, root, edge = _second_edge_direct(
        tmp_path,
        stem="46e-app",
    )
    adoption = adopt_chromium_research_second_changed_basis_governed_session(
        edge,
        edge_source=edge.persistence.path,
        declaration_destination=tmp_path / "46e-app-declaration.json",
    )
    item = prepared.appended_items[0]

    result = verify_chromium_research_second_changed_basis_epoch_reentry(
        adoption,
        values[8],
        (_paragraph_locator(item),),
        changed_working_set_source=prepared.working_set_persistence.path,
        changed_note_source=prepared.note_persistence.path,
        transition_source=transition.persistence.path,
        root_source=root.persistence.path,
        first_edge_source=edge.persistence.path,
        declaration_source=adoption.declaration.path,
    )

    assert isinstance(result, ChromiumResearchSecondChangedBasisEpochReentryResult)
    assert result.adoption_result is adoption
    fresh = result.fresh_reentry
    retained_prior = transition.continuation_reentry
    assert fresh.controller is not adoption.controller
    assert fresh.controller.presentation == adoption.controller.presentation
    assert (
        fresh.loaded_root.verification.root_record_sha256
        == root.persistence.root_record_sha256
    )
    assert (
        fresh.controller.declared_endpoint.verification.edge_record_sha256
        == edge.persistence.edge_record_sha256
    )
    assert (
        fresh.prior_continuation_reentry.controller.presentation
        == retained_prior.controller.presentation
    )
    assert (
        fresh.prior_continuation_reentry.prior_root_backed_reentry.loaded_root.verification.root_record_sha256
        == retained_prior.prior_root_backed_reentry.loaded_root.verification.root_record_sha256
    )

    with pytest.raises(
        TypeError,
        match="exactly ChromiumResearchSecondChangedBasisSessionAdoptionResult",
    ):
        verify_chromium_research_second_changed_basis_epoch_reentry(
            object(),  # type: ignore[arg-type]
            values[8],
            (_paragraph_locator(item),),
            changed_working_set_source=prepared.working_set_persistence.path,
            changed_note_source=prepared.note_persistence.path,
            transition_source=transition.persistence.path,
            root_source=root.persistence.path,
            first_edge_source=edge.persistence.path,
            declaration_source=adoption.declaration.path,
        )


def test_46e_application_rejects_wrong_prior_overlay_or_second_root(tmp_path: Path) -> None:
    values, _, prepared, transition, root, edge = _second_edge_direct(
        tmp_path,
        stem="46e-negative",
    )
    adoption = adopt_chromium_research_second_changed_basis_governed_session(
        edge,
        edge_source=edge.persistence.path,
        declaration_destination=tmp_path / "46e-negative-declaration.json",
    )
    item = prepared.appended_items[0]
    locator = _paragraph_locator(item)

    with pytest.raises(Exception):
        verify_chromium_research_second_changed_basis_epoch_reentry(
            adoption,
            root.persistence.path,
            (locator,),
            changed_working_set_source=prepared.working_set_persistence.path,
            changed_note_source=prepared.note_persistence.path,
            transition_source=transition.persistence.path,
            root_source=root.persistence.path,
            first_edge_source=edge.persistence.path,
            declaration_source=adoption.declaration.path,
        )

    with pytest.raises(Exception):
        verify_chromium_research_second_changed_basis_epoch_reentry(
            adoption,
            values[8],
            (locator,),
            changed_working_set_source=prepared.working_set_persistence.path,
            changed_note_source=prepared.note_persistence.path,
            transition_source=transition.persistence.path,
            root_source=edge.persistence.path,
            first_edge_source=edge.persistence.path,
            declaration_source=adoption.declaration.path,
        )


async def _fill_and_verify_46e(
    shell,
    pilot,
    *,
    prior_overlay: Path,
    prepared,
    transition,
    root,
    edge,
    adoption,
) -> None:
    item = prepared.appended_items[0]
    shell.query_one(
        "#research-second-changed-basis-epoch-reentry-prior-continuation-overlay-source",
        Input,
    ).value = str(prior_overlay)
    shell.query_one(
        "#research-second-changed-basis-epoch-reentry-member-0-capture-source", Input
    ).value = str(item.note.selection.source.verification.path)
    shell.query_one(
        "#research-second-changed-basis-epoch-reentry-member-0-note-source", Input
    ).value = str(item.verification.path)
    for suffix, path in (
        ("changed-working-set-source", prepared.working_set_persistence.path),
        ("changed-note-source", prepared.note_persistence.path),
        ("transition-source", transition.persistence.path),
        ("root-source", root.persistence.path),
        ("first-edge-source", edge.persistence.path),
        ("declaration-source", adoption.declaration.path),
    ):
        shell.query_one(
            f"#research-second-changed-basis-epoch-reentry-{suffix}", Input
        ).value = str(path)
    await _press(shell, pilot, "verify-research-second-changed-basis-epoch-reentry")


@pytest.mark.asyncio
async def test_46e_shell_mounts_only_after_46d_all_inputs_blank_and_does_not_replace_mounted_state(
    tmp_path: Path,
) -> None:
    values, reentry = _continuation(tmp_path, stem="46e-ui")
    member, _ = _new_paragraph_member(tmp_path, stem="46e-ui-member")
    shell = create_second_changed_basis_epoch_reentry_research_session_shell(reentry)
    shell.configure_changed_basis_candidate((member,))

    async with shell.run_test(size=(220, 650)) as pilot:
        await pilot.pause()
        assert len(shell.query(ResearchSecondChangedBasisEpochReentryControls)) == 0
        prepared, transition, root, edge = await _reach_46c(
            shell,
            pilot,
            tmp_path,
            stem="46e-ui",
        )
        assert len(shell.query(ResearchSecondChangedBasisEpochReentryControls)) == 0
        await _adopt_ui(
            shell,
            pilot,
            edge,
            tmp_path / "46e-ui-adoption-declaration.json",
        )
        adoption = shell.last_second_changed_basis_session_adoption
        assert adoption is not None
        controls = shell.query_one(ResearchSecondChangedBasisEpochReentryControls)
        inputs = list(controls.query(Input))
        assert inputs
        assert all(widget.value == "" for widget in inputs)
        assert len(shell.query("#research-second-basis-epoch-overlay-destination")) == 0
        assert len(shell.query("#persist-second-basis-epoch-overlay")) == 0

        mounted_controller = shell.research_controller
        mounted_session = shell.research_session
        historical_continuation = shell.root_backed_continuation_reentry
        await _fill_and_verify_46e(
            shell,
            pilot,
            prior_overlay=values[8],
            prepared=prepared,
            transition=transition,
            root=root,
            edge=edge,
            adoption=adoption,
        )

        result = shell.last_second_changed_basis_epoch_reentry_verification
        assert result is not None
        assert result.adoption_result is adoption
        assert result.fresh_reentry.controller is not mounted_controller
        assert result.fresh_reentry.controller.presentation == adoption.controller.presentation
        assert shell.research_controller is mounted_controller
        assert shell.research_session is mounted_session
        assert shell.root_backed_continuation_reentry is historical_continuation
        assert all(widget.disabled for widget in inputs)
        assert len(shell.query("#persist-second-basis-epoch-overlay")) == 0


@pytest.mark.asyncio
async def test_46e_raw_36d_launch_stays_pathless_after_explicit_persisted_overlay_proof(
    tmp_path: Path,
) -> None:
    values, reentry = _continuation(tmp_path, stem="46e-raw")
    member, _ = _new_paragraph_member(tmp_path, stem="46e-raw-member")
    shell = create_inspectable_root_backed_continuation_handoff_research_session_shell(
        reentry
    )
    shell.configure_changed_basis_candidate((member,))
    panel = shell.root_backed_authority_inspection
    launch = panel.launch_provenance
    assert launch.launch_location_context is None

    async with shell.run_test(size=(220, 650)) as pilot:
        await pilot.pause()
        prepared, transition, root, edge = await _reach_46c(
            shell,
            pilot,
            tmp_path,
            stem="46e-raw",
        )
        await _adopt_ui(
            shell,
            pilot,
            edge,
            tmp_path / "46e-raw-adoption-declaration.json",
        )
        adoption = shell.last_second_changed_basis_session_adoption
        assert adoption is not None
        current_before = panel.current_state

        await _fill_and_verify_46e(
            shell,
            pilot,
            prior_overlay=values[8],
            prepared=prepared,
            transition=transition,
            root=root,
            edge=edge,
            adoption=adoption,
        )

        result = shell.last_second_changed_basis_epoch_reentry_verification
        assert result is not None
        assert panel.launch_provenance is launch
        assert panel.launch_provenance.launch_location_context is None
        assert panel.current_state is current_before
        assert shell.research_controller is adoption.controller
