from __future__ import annotations

from pathlib import Path

import pytest
from textual.widgets import Input

from pyxis.app.chromium_research_session_reentry import (
    ChromiumResearchParagraphNoteReentryLocator,
)
from pyxis.app.chromium_research_third_changed_basis_epoch_reentry import (
    ChromiumResearchThirdChangedBasisEpochReentryResult,
    verify_chromium_research_third_changed_basis_epoch_reentry,
)
from pyxis.app.chromium_research_third_changed_basis_session_adoption import (
    adopt_chromium_research_third_changed_basis_governed_session,
)
from pyxis.ui.chromium_research_third_changed_basis_epoch_reentry_textual import (
    ResearchThirdChangedBasisEpochReentryControls,
)
from pyxis.ui.third_changed_basis_epoch_reentry_research_session_shell import (
    create_inspectable_third_changed_basis_epoch_reentry_handoff_research_session_shell,
    create_third_changed_basis_epoch_reentry_handoff_research_session_shell,
    create_third_changed_basis_epoch_reentry_research_session_shell,
)
from pyxis.ui.third_changed_basis_session_adoption_research_session_shell import (
    create_third_changed_basis_session_adoption_research_session_shell,
)
from test_app_chromium_research_session_working_set_extension import _new_paragraph_member
from test_ui_research_third_changed_basis_session_adoption import (
    _adopt_ui,
    _reach_47c,
    _third_edge_direct,
)
from test_ui_research_third_changed_basis_transition import (
    _continuation,
    _press,
)


def _paragraph_locator(item) -> ChromiumResearchParagraphNoteReentryLocator:
    return ChromiumResearchParagraphNoteReentryLocator(
        capture_source=item.note.selection.source.verification.path,
        note_source=item.verification.path,
    )


def test_47e_application_freshly_reconstructs_all_three_exact_ancestry_layers(
    tmp_path: Path,
) -> None:
    _, lineage, prepared, transition, root, edge = _third_edge_direct(
        tmp_path,
        stem="47e-app",
    )
    adoption = adopt_chromium_research_third_changed_basis_governed_session(
        edge,
        edge_source=edge.persistence.path,
        declaration_destination=tmp_path / "47e-app-declaration.json",
    )
    item = prepared.appended_items[0]

    result = verify_chromium_research_third_changed_basis_epoch_reentry(
        adoption,
        lineage.overlay_source,
        (_paragraph_locator(item),),
        changed_working_set_source=prepared.working_set_persistence.path,
        changed_note_source=prepared.note_persistence.path,
        transition_source=transition.persistence.path,
        root_source=root.persistence.path,
        first_edge_source=edge.persistence.path,
        declaration_source=adoption.declaration.path,
    )

    assert isinstance(result, ChromiumResearchThirdChangedBasisEpochReentryResult)
    assert result.adoption_result is adoption
    fresh = result.fresh_reentry
    retained_prior = transition.continuation_reentry
    fresh_prior = fresh.prior_second_basis_epoch_continuation_reentry

    assert fresh.controller is not adoption.controller
    assert fresh.controller.presentation == adoption.controller.presentation
    assert (
        fresh.controller.declared_endpoint.verification.edge_record_sha256
        == edge.persistence.edge_record_sha256
    )
    assert (
        fresh.loaded_root.verification.root_record_sha256
        == root.persistence.root_record_sha256
    )
    assert fresh_prior.controller.presentation == retained_prior.controller.presentation
    assert (
        fresh_prior.controller.declared_endpoint.verification.edge_record_sha256
        == retained_prior.controller.declared_endpoint.verification.edge_record_sha256
    )

    fresh_second = fresh_prior.prior_second_basis_epoch_reentry
    retained_second = retained_prior.prior_second_basis_epoch_reentry
    fresh_first_root = (
        fresh_second.prior_continuation_reentry.prior_root_backed_reentry.loaded_root
        .verification.root_record_sha256
    )
    retained_first_root = (
        retained_second.prior_continuation_reentry.prior_root_backed_reentry.loaded_root
        .verification.root_record_sha256
    )
    assert fresh_first_root == retained_first_root
    assert (
        fresh_second.loaded_root.verification.root_record_sha256
        == retained_second.loaded_root.verification.root_record_sha256
    )
    assert len(
        {
            fresh_first_root,
            fresh_second.loaded_root.verification.root_record_sha256,
            fresh.loaded_root.verification.root_record_sha256,
        }
    ) == 3

    with pytest.raises(
        TypeError,
        match="exactly ChromiumResearchThirdChangedBasisSessionAdoptionResult",
    ):
        verify_chromium_research_third_changed_basis_epoch_reentry(
            object(),  # type: ignore[arg-type]
            lineage.overlay_source,
            (_paragraph_locator(item),),
            changed_working_set_source=prepared.working_set_persistence.path,
            changed_note_source=prepared.note_persistence.path,
            transition_source=transition.persistence.path,
            root_source=root.persistence.path,
            first_edge_source=edge.persistence.path,
            declaration_source=adoption.declaration.path,
        )


def test_47e_application_rejects_wrong_prior_overlay_or_third_root(tmp_path: Path) -> None:
    _, lineage, prepared, transition, root, edge = _third_edge_direct(
        tmp_path,
        stem="47e-negative",
    )
    adoption = adopt_chromium_research_third_changed_basis_governed_session(
        edge,
        edge_source=edge.persistence.path,
        declaration_destination=tmp_path / "47e-negative-declaration.json",
    )
    locator = _paragraph_locator(prepared.appended_items[0])

    with pytest.raises(Exception):
        verify_chromium_research_third_changed_basis_epoch_reentry(
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
        verify_chromium_research_third_changed_basis_epoch_reentry(
            adoption,
            lineage.overlay_source,
            (locator,),
            changed_working_set_source=prepared.working_set_persistence.path,
            changed_note_source=prepared.note_persistence.path,
            transition_source=transition.persistence.path,
            root_source=edge.persistence.path,
            first_edge_source=edge.persistence.path,
            declaration_source=adoption.declaration.path,
        )


async def _fill_and_verify_47e(
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
        "#research-third-changed-basis-epoch-reentry-prior-continuation-overlay-source",
        Input,
    ).value = str(prior_overlay)
    shell.query_one(
        "#research-third-changed-basis-epoch-reentry-member-0-capture-source", Input
    ).value = str(item.note.selection.source.verification.path)
    shell.query_one(
        "#research-third-changed-basis-epoch-reentry-member-0-note-source", Input
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
            f"#research-third-changed-basis-epoch-reentry-{suffix}", Input
        ).value = str(path)
    await _press(shell, pilot, "verify-research-third-changed-basis-epoch-reentry")


@pytest.mark.asyncio
async def test_47e_shell_mounts_only_after_47d_all_inputs_blank_and_does_not_replace_mounted_state(
    tmp_path: Path,
) -> None:
    _, overlay, _, lineage = _continuation(tmp_path, stem="47e-ui")
    member, _ = _new_paragraph_member(tmp_path, stem="47e-ui-member")
    shell = create_third_changed_basis_epoch_reentry_research_session_shell(lineage)
    shell.configure_changed_basis_candidate((member,))

    async with shell.run_test(size=(225, 760)) as pilot:
        await pilot.pause()
        assert len(shell.query(ResearchThirdChangedBasisEpochReentryControls)) == 0
        prepared, transition, root, edge = await _reach_47c(
            shell,
            pilot,
            tmp_path,
            stem="47e-ui",
        )
        assert len(shell.query(ResearchThirdChangedBasisEpochReentryControls)) == 0
        await _adopt_ui(
            shell,
            pilot,
            edge,
            tmp_path / "47e-ui-adoption-declaration.json",
        )
        adoption = shell.last_third_changed_basis_session_adoption
        assert adoption is not None
        controls = shell.query_one(ResearchThirdChangedBasisEpochReentryControls)
        inputs = list(controls.query(Input))
        assert inputs
        assert all(widget.value == "" for widget in inputs)

        mounted_controller = shell.research_controller
        mounted_session = shell.research_session
        mounted_reentry = shell.research_reentry
        historical_continuation = shell.second_basis_epoch_continuation_reentry

        await _fill_and_verify_47e(
            shell,
            pilot,
            prior_overlay=overlay,
            prepared=prepared,
            transition=transition,
            root=root,
            edge=edge,
            adoption=adoption,
        )

        result = shell.last_third_changed_basis_epoch_reentry_verification
        assert result is not None
        assert result.adoption_result is adoption
        assert result.fresh_reentry.controller is not mounted_controller
        assert result.fresh_reentry.controller.presentation == adoption.controller.presentation
        assert shell.research_controller is mounted_controller
        assert shell.research_session is mounted_session
        assert shell.research_reentry is mounted_reentry
        assert shell.second_basis_epoch_continuation_reentry is historical_continuation
        assert all(widget.disabled for widget in inputs)
        assert not hasattr(shell, "last_third_basis_epoch_reentry_overlay")


@pytest.mark.asyncio
async def test_47e_raw_38f_launch_stays_pathless_and_current_inspection_unchanged(
    tmp_path: Path,
) -> None:
    _, overlay, reentry, _ = _continuation(tmp_path, stem="47e-raw")
    member, _ = _new_paragraph_member(tmp_path, stem="47e-raw-member")
    shell = (
        create_inspectable_third_changed_basis_epoch_reentry_handoff_research_session_shell(
            reentry
        )
    )
    shell.configure_changed_basis_candidate((member,))
    panel = shell.second_basis_epoch_authority_inspection
    launch = panel.launch_provenance
    assert launch.launch_location_context is None

    async with shell.run_test(size=(225, 760)) as pilot:
        await pilot.pause()
        prepared, transition, root, edge = await _reach_47c(
            shell,
            pilot,
            tmp_path,
            stem="47e-raw",
        )
        await _adopt_ui(
            shell,
            pilot,
            edge,
            tmp_path / "47e-raw-adoption-declaration.json",
        )
        adoption = shell.last_third_changed_basis_session_adoption
        assert adoption is not None
        current_before = panel.current_state

        await _fill_and_verify_47e(
            shell,
            pilot,
            prior_overlay=overlay,
            prepared=prepared,
            transition=transition,
            root=root,
            edge=edge,
            adoption=adoption,
        )

        result = shell.last_third_changed_basis_epoch_reentry_verification
        assert result is not None
        assert panel.launch_provenance is launch
        assert panel.launch_provenance.launch_location_context is None
        assert panel.current_state is current_before
        assert shell.research_controller is adoption.controller


@pytest.mark.asyncio
async def test_plain_47d_product_does_not_gain_47e_surface(tmp_path: Path) -> None:
    _, _, _, lineage = _continuation(tmp_path, stem="47e-plain")
    member, _ = _new_paragraph_member(tmp_path, stem="47e-plain-member")
    shell = create_third_changed_basis_session_adoption_research_session_shell(lineage)
    shell.configure_changed_basis_candidate((member,))

    async with shell.run_test(size=(220, 620)) as pilot:
        await pilot.pause()
        *_, edge = await _reach_47c(shell, pilot, tmp_path, stem="47e-plain")
        await _adopt_ui(
            shell,
            pilot,
            edge,
            tmp_path / "47e-plain-adoption-declaration.json",
        )
        assert shell.last_third_changed_basis_session_adoption is not None
        assert not hasattr(
            shell,
            "last_third_changed_basis_epoch_reentry_verification",
        )
        assert len(shell.query(ResearchThirdChangedBasisEpochReentryControls)) == 0


def test_47e_product_factories_reject_wrong_authority_family() -> None:
    with pytest.raises(
        TypeError,
        match="ChromiumResearchSecondBasisEpochContinuationShellLineage",
    ):
        create_third_changed_basis_epoch_reentry_research_session_shell(object())  # type: ignore[arg-type]

    with pytest.raises(
        TypeError,
        match="exactly ChromiumResearchSecondBasisEpochContinuationReentryResult",
    ):
        create_third_changed_basis_epoch_reentry_handoff_research_session_shell(object())  # type: ignore[arg-type]
