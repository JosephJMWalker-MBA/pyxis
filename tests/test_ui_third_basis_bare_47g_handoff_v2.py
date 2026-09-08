from __future__ import annotations

import json
from pathlib import Path

import pytest
from textual.widgets import Button, Input, Static

from pyxis.app.chromium_research_second_basis_epoch_shell_lineage import (
    prove_chromium_research_second_basis_epoch_continuation_shell_lineage,
)
from pyxis.app.chromium_research_third_basis_epoch_reentry import (
    ChromiumResearchThirdBasisEpochReentryResult,
)
from pyxis.ui.chromium_research_third_basis_epoch_continuation_checkpoint_textual import (
    ThirdBasisEpochResearchSessionContinuationCheckpointControls,
)
from pyxis.ui.chromium_research_third_changed_basis_epoch_reentry_overlay_textual import (
    ResearchThirdChangedBasisEpochReentryOverlayControls,
)
from pyxis.ui.third_basis_epoch_session_handoff_authority_inspection_shell import (
    create_inspectable_third_basis_epoch_handoff_research_session_shell,
)
from pyxis.ui.third_changed_basis_epoch_handoff_research_session_shell import (
    create_inspectable_third_changed_basis_epoch_persisted_source_handoff_research_session_shell,
)
from test_cli_third_basis_bare_overlay_v2_relaunch import (
    _assert_three_bare_passages_survive,
)
from test_second_basis_bare_cumulative_v1 import (
    _persist_bare_second_basis_cumulative,
)
from test_ui_research_root_backed_session_continuation_checkpoint import (
    _write_and_rollover,
)
from test_ui_research_third_changed_basis_session_adoption import (
    _adopt_ui,
    _reach_47c,
)
from test_ui_research_third_changed_basis_transition import _press
from test_ui_third_basis_bare_selection_reentry import _third_bare_selection


_OVERLAY_V2 = "pyxis.chromium.research_third_basis_epoch_reentry_locator_overlay.v2"


@pytest.mark.asyncio
async def test_50v_explicit_47g_handoff_reuses_exact_v2_checkpoint_fresh_reentry(
    tmp_path: Path,
    monkeypatch,
) -> None:
    prior_values = _persist_bare_second_basis_cumulative(
        tmp_path,
        stem="50v-prior",
    )
    prior_overlay = prior_values[31]
    prior_result = prior_values[34]
    lineage = prove_chromium_research_second_basis_epoch_continuation_shell_lineage(
        prior_result.fresh_reentry,
        overlay_source=prior_overlay,
    )
    _, bare, bare_locator = _third_bare_selection(tmp_path)

    shell = (
        create_inspectable_third_changed_basis_epoch_persisted_source_handoff_research_session_shell(
            lineage,
            (bare,),
        )
    )
    observed: dict[str, object] = {}

    def fake_exit(result=None, *args, **kwargs) -> None:
        observed["result"] = result

    monkeypatch.setattr(shell, "exit", fake_exit)

    async with shell.run_test(size=(255, 1060)) as pilot:
        await pilot.pause()

        source_panel = shell.second_basis_epoch_authority_inspection
        source_launch = source_panel.launch_provenance
        source_current_before = source_panel.current_state
        assert len(shell.query("#continue-third-changed-basis-epoch-session")) == 0

        prepared, transition, root, edge = await _reach_47c(
            shell,
            pilot,
            tmp_path,
            stem="50v",
        )
        await _adopt_ui(
            shell,
            pilot,
            edge,
            tmp_path / "50v-adoption.json",
        )
        adoption = shell.last_third_changed_basis_session_adoption
        assert adoption is not None

        shell.query_one(
            "#research-third-changed-basis-epoch-reentry-prior-continuation-overlay-source",
            Input,
        ).value = str(prior_overlay)
        shell.query_one(
            "#research-third-changed-basis-epoch-reentry-member-0-capture-source",
            Input,
        ).value = str(bare_locator.capture_source)
        shell.query_one(
            "#research-third-changed-basis-epoch-reentry-member-0-selection-source",
            Input,
        ).value = str(bare_locator.selection_source)
        for suffix, path in (
            ("changed-working-set-source", prepared.working_set_persistence.path),
            ("changed-note-source", prepared.note_persistence.path),
            ("transition-source", transition.persistence.path),
            ("root-source", root.persistence.path),
            ("first-edge-source", edge.persistence.path),
            ("declaration-source", adoption.declaration.path),
        ):
            shell.query_one(
                f"#research-third-changed-basis-epoch-reentry-{suffix}",
                Input,
            ).value = str(path)

        await _press(
            shell,
            pilot,
            "verify-research-third-changed-basis-epoch-reentry",
        )
        for _ in range(30):
            verification = shell.last_third_changed_basis_epoch_reentry_verification
            if verification is not None:
                break
            await pilot.pause(delay=0.01)
        else:
            verification = None
        assert verification is not None
        assert verification.adoption_result is adoption
        _assert_three_bare_passages_survive(verification.fresh_reentry)

        for _ in range(30):
            if len(shell.query(ResearchThirdChangedBasisEpochReentryOverlayControls)):
                break
            await pilot.pause(delay=0.01)
        controls = shell.query_one(ResearchThirdChangedBasisEpochReentryOverlayControls)
        assert controls.verification_result is verification

        mounted_controller = shell.research_controller
        mounted_session = shell.research_session
        mounted_reentry = shell.research_reentry
        retained_second_epoch = shell.second_basis_epoch_continuation_reentry

        destination = tmp_path / "50v-third-basis.overlay.json"
        shell.query_one(
            "#research-third-changed-basis-epoch-reentry-overlay-prior-continuation-overlay-source",
            Input,
        ).value = str(prior_overlay)
        shell.query_one(
            "#research-third-changed-basis-epoch-reentry-overlay-destination",
            Input,
        ).value = str(destination)

        await _press(
            shell,
            pilot,
            "persist-research-third-changed-basis-epoch-reentry-overlay",
        )
        for _ in range(30):
            result = shell.last_third_changed_basis_epoch_reentry_overlay
            if result is not None:
                break
            await pilot.pause(delay=0.01)
        else:
            result = None
        assert result is not None

        assert result.verification_result is verification
        assert result.checkpoint.persistence.overlay_format == _OVERLAY_V2
        document = json.loads(destination.read_text(encoding="utf-8"))
        assert document["format"] == _OVERLAY_V2
        assert document["appended_working_set_members"][0]["kind"] == (
            "exact_range_selection"
        )

        # Persistence alone must not leave the source product.
        assert "result" not in observed
        assert shell.research_controller is mounted_controller
        assert shell.research_session is mounted_session
        assert shell.research_reentry is mounted_reentry
        assert shell.second_basis_epoch_continuation_reentry is retained_second_epoch
        assert source_panel.launch_provenance is source_launch
        assert source_panel.current_state is source_current_before

        handoff_button = shell.query_one(
            "#continue-third-changed-basis-epoch-session",
            Button,
        )
        assert not handoff_button.disabled
        assert len(shell.query("#continue-third-changed-basis-epoch-session")) == 1
        notice = str(
            shell.query_one(
                "#research-third-changed-basis-epoch-handoff-notice",
                Static,
            ).content
        )
        assert "saved 40B overlay path is not reloaded" in notice

        expected_handoff = result.checkpoint.fresh_reentry
        assert type(expected_handoff) is ChromiumResearchThirdBasisEpochReentryResult
        assert expected_handoff is not verification.fresh_reentry
        _assert_three_bare_passages_survive(expected_handoff)

        # Prove 47G is an in-memory typed transfer, not a disk re-entry.
        destination.unlink()
        assert not destination.exists()

        await _press(
            shell,
            pilot,
            "continue-third-changed-basis-epoch-session",
        )

        assert observed["result"] is expected_handoff
        assert shell.research_controller is mounted_controller
        assert shell.research_session is mounted_session
        assert shell.research_reentry is mounted_reentry
        assert shell.second_basis_epoch_continuation_reentry is retained_second_epoch
        assert source_panel.launch_provenance is source_launch
        assert source_panel.current_state is source_current_before

    handoff = observed["result"]
    assert type(handoff) is ChromiumResearchThirdBasisEpochReentryResult
    _assert_three_bare_passages_survive(handoff)

    receiver = create_inspectable_third_basis_epoch_handoff_research_session_shell(
        handoff
    )
    assert receiver.third_basis_epoch_launch_lineage is None
    assert receiver.third_basis_epoch_handoff_reentry is handoff
    assert receiver.third_basis_epoch_reentry is handoff
    assert receiver.research_controller is handoff.controller
    assert not hasattr(receiver, "third_basis_epoch_overlay_source")
    assert not hasattr(receiver, "overlay_source")

    panel = receiver.third_basis_epoch_authority_inspection
    launch = panel.launch_provenance
    second_epoch = (
        handoff.prior_second_basis_epoch_continuation_reentry
        .prior_second_basis_epoch_reentry
    )
    assert launch.launch_family == "in-process 47G typed third-basis-epoch handoff"
    assert launch.launch_location_context is None
    assert (
        launch.first_root_sha256
        == second_epoch.prior_continuation_reentry.prior_root_backed_reentry
        .loaded_root.verification.root_record_sha256
    )
    assert (
        launch.second_root_sha256
        == second_epoch.loaded_root.verification.root_record_sha256
    )
    assert (
        launch.third_root_sha256
        == handoff.loaded_root.verification.root_record_sha256
    )
    assert (
        launch.launch_endpoint_sha256
        == handoff.controller.declared_endpoint.verification.edge_record_sha256
    )

    successor = tmp_path / "50v-receiver-successor.json"
    declaration = tmp_path / "50v-receiver-declaration.json"
    third_bare = handoff.loaded_appended_members[0]

    async with receiver.run_test(size=(195, 320)) as pilot:
        await pilot.pause()
        assert len(
            receiver.query(ThirdBasisEpochResearchSessionContinuationCheckpointControls)
        ) == 0
        current_before = panel.current_state

        await _write_and_rollover(
            receiver,
            pilot,
            prior_edge=handoff.controller.declared_endpoint.verification.path,
            successor=successor,
            declaration=declaration,
            text="50V ordinary rollover after exact bare 47G typed handoff.",
        )

        controls = receiver.query_one(
            ThirdBasisEpochResearchSessionContinuationCheckpointControls
        )
        assert controls.rollover is receiver.last_research_rollover
        assert receiver.third_basis_epoch_launch_lineage is None
        assert receiver.third_basis_epoch_handoff_reentry is handoff
        assert receiver.third_basis_epoch_reentry is handoff

        for selector in (
            "#research-third-basis-epoch-checkpoint-prior-overlay-source",
            "#research-third-basis-epoch-checkpoint-successor-source",
            "#research-third-basis-epoch-checkpoint-declaration-source",
            "#research-third-basis-epoch-checkpoint-destination",
        ):
            assert receiver.query_one(selector, Input).value == ""

        assert panel.launch_provenance is launch
        assert panel.launch_provenance.launch_location_context is None
        assert panel.current_state is not current_before
        assert panel.current_state.state_source == (
            "explicit rollover after in-process 47G handoff"
        )
        assert (
            panel.current_state.endpoint_sha256
            == receiver.research_controller.declared_endpoint.verification.edge_record_sha256
        )
        assert (
            receiver.research_controller.declared_endpoint.revision.revised_note
            .working_set.items[-1]
            is third_bare
        )
