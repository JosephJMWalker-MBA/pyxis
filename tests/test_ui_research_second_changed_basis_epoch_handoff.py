from __future__ import annotations

from pathlib import Path

import pytest
from textual.widgets import Button, Input, Static

from pyxis.app.chromium_research_second_basis_epoch_reentry import (
    ChromiumResearchSecondBasisEpochReentryResult,
)
from pyxis.app.chromium_research_second_basis_epoch_shell_lineage import (
    prove_chromium_research_second_basis_epoch_shell_lineage,
)
from pyxis.app.chromium_research_second_changed_basis_epoch_reentry_overlay import (
    persist_chromium_research_second_changed_basis_epoch_reentry_overlay,
)
from pyxis.ui.chromium_research_second_basis_epoch_continuation_checkpoint_textual import (
    SecondBasisEpochResearchSessionContinuationCheckpointControls,
)
from pyxis.ui.second_basis_epoch_cumulative_handoff_shell import (
    SecondBasisEpochHandoffResearchSessionShell,
    create_second_basis_epoch_handoff_research_session_shell,
)
from pyxis.ui.second_basis_epoch_research_session_shell import (
    create_second_basis_epoch_research_session_shell,
)
from pyxis.ui.second_basis_epoch_session_handoff_authority_inspection_shell import (
    create_inspectable_second_basis_epoch_handoff_research_session_shell,
)
from pyxis.ui.second_changed_basis_epoch_handoff_research_session_shell import (
    SecondChangedBasisEpochHandoffResearchSessionShell,
    create_second_changed_basis_epoch_handoff_research_session_shell,
)
import pyxis.ui.second_changed_basis_epoch_handoff_research_session_shell as handoff_ui

from test_app_chromium_research_session_working_set_extension import _new_paragraph_member
from test_ui_research_root_backed_session_continuation_checkpoint import (
    _write_and_rollover,
)
from test_ui_research_second_changed_basis_epoch_reentry import (
    _fill_and_verify_46e,
)
from test_ui_research_second_changed_basis_epoch_reentry_overlay import (
    _direct_46e_verification,
    _persist_46f,
)
from test_ui_research_second_changed_basis_session_adoption import (
    _adopt_ui,
    _reach_46c,
)
from test_ui_research_second_changed_basis_transition import (
    _continuation,
    _press,
)


def _direct_46f(tmp_path: Path, *, stem: str):
    values, verification = _direct_46e_verification(tmp_path, stem=stem)
    destination = tmp_path / f"{stem}.second-epoch.overlay.json"
    result = persist_chromium_research_second_changed_basis_epoch_reentry_overlay(
        verification,
        prior_root_backed_continuation_overlay_source=values[8],
        destination=destination,
    )
    return values, verification, result, destination


async def _reach_46f_ui(shell, pilot, tmp_path: Path, *, stem: str, values):
    prepared, transition, root, edge = await _reach_46c(
        shell,
        pilot,
        tmp_path,
        stem=stem,
    )
    await _adopt_ui(
        shell,
        pilot,
        edge,
        tmp_path / f"{stem}-adoption-declaration.json",
    )
    adoption = shell.last_second_changed_basis_session_adoption
    assert adoption is not None
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
    verification = shell.last_second_changed_basis_epoch_reentry_verification
    assert verification is not None
    destination = tmp_path / f"{stem}.second-epoch.overlay.json"
    await _persist_46f(
        shell,
        pilot,
        prior_overlay=values[8],
        destination=destination,
    )
    result = shell.last_second_changed_basis_epoch_reentry_overlay
    assert result is not None
    return verification, result, destination


def test_46g_narrow_refactor_preserves_persisted_37b_launch_and_adds_exact_active_reentry(
    tmp_path: Path,
) -> None:
    _, _, result, destination = _direct_46f(tmp_path, stem="46g-persisted")
    earned = result.checkpoint.fresh_reentry
    lineage = prove_chromium_research_second_basis_epoch_shell_lineage(
        earned,
        overlay_source=destination,
    )
    shell = create_second_basis_epoch_research_session_shell(lineage)

    assert shell.second_basis_epoch_launch_lineage is lineage
    assert shell.second_basis_epoch_reentry is lineage.reentry
    assert shell.research_controller is lineage.reentry.controller
    assert shell.research_reentry is None


def test_46g_raw_receiver_retains_exact_typed_handoff_without_path_authority(
    tmp_path: Path,
) -> None:
    _, _, result, _ = _direct_46f(tmp_path, stem="46g-raw")
    handoff = result.checkpoint.fresh_reentry
    shell = create_second_basis_epoch_handoff_research_session_shell(handoff)

    assert isinstance(shell, SecondBasisEpochHandoffResearchSessionShell)
    assert shell.second_basis_epoch_launch_lineage is None
    assert shell.second_basis_epoch_handoff_reentry is handoff
    assert shell.second_basis_epoch_reentry is handoff
    assert shell.research_controller is handoff.controller
    assert shell.research_reentry is None
    assert not hasattr(shell, "second_basis_epoch_overlay_source")


@pytest.mark.asyncio
async def test_46g_raw_receiver_rollover_mounts_existing_blank_37c_surface(
    tmp_path: Path,
) -> None:
    _, _, result, _ = _direct_46f(tmp_path, stem="46g-rollover")
    handoff = result.checkpoint.fresh_reentry
    shell = create_second_basis_epoch_handoff_research_session_shell(handoff)

    async with shell.run_test(size=(180, 240)) as pilot:
        await pilot.pause()
        assert len(shell.query(SecondBasisEpochResearchSessionContinuationCheckpointControls)) == 0
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=handoff.controller.declared_endpoint.verification.path,
            successor=tmp_path / "46g-rollover-successor.json",
            declaration=tmp_path / "46g-rollover-declaration.json",
            text="Explicit continuation after the pathless 46G second-epoch handoff.",
        )

        controls = shell.query_one(
            SecondBasisEpochResearchSessionContinuationCheckpointControls
        )
        assert shell.second_basis_epoch_launch_lineage is None
        assert shell.second_basis_epoch_handoff_reentry is handoff
        assert shell.second_basis_epoch_reentry is handoff
        assert controls.rollover is shell.last_research_rollover
        for selector in (
            "#research-second-basis-epoch-checkpoint-prior-overlay-source",
            "#research-second-basis-epoch-checkpoint-successor-source",
            "#research-second-basis-epoch-checkpoint-declaration-source",
            "#research-second-basis-epoch-checkpoint-destination",
        ):
            assert shell.query_one(selector, Input).value == ""


@pytest.mark.asyncio
async def test_46g_inspection_is_pathless_and_rollover_preserves_exact_launch_object(
    tmp_path: Path,
) -> None:
    _, _, result, _ = _direct_46f(tmp_path, stem="46g-inspection")
    handoff = result.checkpoint.fresh_reentry
    shell = create_inspectable_second_basis_epoch_handoff_research_session_shell(handoff)
    panel = shell.second_basis_epoch_authority_inspection
    launch = panel.launch_provenance

    assert launch.launch_family == "in-process 46G typed second-basis-epoch handoff"
    assert launch.launch_location_context is None
    assert (
        launch.first_root_sha256
        == handoff.prior_continuation_reentry.prior_root_backed_reentry.loaded_root.verification.root_record_sha256
    )
    assert launch.second_root_sha256 == handoff.loaded_root.verification.root_record_sha256
    assert (
        launch.launch_endpoint_sha256
        == handoff.controller.declared_endpoint.verification.edge_record_sha256
    )

    async with shell.run_test(size=(185, 260)) as pilot:
        await pilot.pause()
        current_before = panel.current_state
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=handoff.controller.declared_endpoint.verification.path,
            successor=tmp_path / "46g-inspection-successor.json",
            declaration=tmp_path / "46g-inspection-declaration.json",
            text="Visible continuation after the 46G handoff inspection launch.",
        )

        assert panel.launch_provenance is launch
        assert panel.launch_provenance.launch_location_context is None
        assert panel.current_state is not current_before
        assert panel.current_state.state_source == "explicit rollover after in-process 46G handoff"
        assert (
            panel.current_state.endpoint_sha256
            == shell.research_controller.declared_endpoint.verification.edge_record_sha256
        )


@pytest.mark.asyncio
async def test_46g_success_requires_explicit_choice_and_returns_exact_37b_fresh_reentry(
    tmp_path: Path,
    monkeypatch,
) -> None:
    values, reentry = _continuation(tmp_path, stem="46g-success")
    member, _ = _new_paragraph_member(tmp_path, stem="46g-success-member")
    shell = create_second_changed_basis_epoch_handoff_research_session_shell(
        reentry,
        (member,),
    )
    assert isinstance(shell, SecondChangedBasisEpochHandoffResearchSessionShell)
    observed: dict[str, object] = {}

    def fake_exit(result=None, *args, **kwargs) -> None:
        observed["result"] = result

    monkeypatch.setattr(shell, "exit", fake_exit)

    async with shell.run_test(size=(230, 820)) as pilot:
        await pilot.pause()
        assert len(shell.query("#continue-second-changed-basis-epoch-session")) == 0

        prepared, transition, root, edge = await _reach_46c(
            shell,
            pilot,
            tmp_path,
            stem="46g-success",
        )
        await _adopt_ui(
            shell,
            pilot,
            edge,
            tmp_path / "46g-success-adoption-declaration.json",
        )
        adoption = shell.last_second_changed_basis_session_adoption
        assert adoption is not None
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
        verification = shell.last_second_changed_basis_epoch_reentry_verification
        assert verification is not None
        assert len(shell.query("#continue-second-changed-basis-epoch-session")) == 0

        mounted_controller = shell.research_controller
        mounted_session = shell.research_session
        mounted_reentry = shell.research_reentry
        destination = tmp_path / "46g-success.second-epoch.overlay.json"
        await _persist_46f(
            shell,
            pilot,
            prior_overlay=values[8],
            destination=destination,
        )
        result = shell.last_second_changed_basis_epoch_reentry_overlay
        assert result is not None

        assert "result" not in observed
        assert shell.research_controller is mounted_controller
        assert shell.research_session is mounted_session
        assert shell.research_reentry is mounted_reentry
        button = shell.query_one("#continue-second-changed-basis-epoch-session", Button)
        assert not button.disabled
        notice = str(
            shell.query_one("#research-second-changed-basis-epoch-handoff-notice", Static).content
        )
        assert "currently mounted prior product remains unchanged" in notice
        assert "saved 37B overlay path is not reloaded" in notice

        # Typed handoff authority must survive loss of the just-written locator file.
        destination.unlink()
        await _press(shell, pilot, "continue-second-changed-basis-epoch-session")

        assert observed["result"] is result.checkpoint.fresh_reentry
        assert observed["result"] is not verification.fresh_reentry
        assert type(observed["result"]) is ChromiumResearchSecondBasisEpochReentryResult


@pytest.mark.asyncio
async def test_46g_failed_46f_persistence_never_exposes_handoff(tmp_path: Path) -> None:
    values, reentry = _continuation(tmp_path, stem="46g-gated")
    member, _ = _new_paragraph_member(tmp_path, stem="46g-gated-member")
    shell = create_second_changed_basis_epoch_handoff_research_session_shell(
        reentry,
        (member,),
    )

    async with shell.run_test(size=(230, 800)) as pilot:
        await pilot.pause()
        prepared, transition, root, edge = await _reach_46c(
            shell,
            pilot,
            tmp_path,
            stem="46g-gated",
        )
        await _adopt_ui(
            shell,
            pilot,
            edge,
            tmp_path / "46g-gated-adoption-declaration.json",
        )
        adoption = shell.last_second_changed_basis_session_adoption
        assert adoption is not None
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

        existing = tmp_path / "46g-gated-existing.overlay.json"
        existing.write_text("preserve exactly\n", encoding="utf-8")
        await _persist_46f(
            shell,
            pilot,
            prior_overlay=values[8],
            destination=existing,
        )

        assert shell.last_second_changed_basis_epoch_reentry_overlay is None
        assert existing.read_text(encoding="utf-8") == "preserve exactly\n"
        assert len(shell.query("#continue-second-changed-basis-epoch-session")) == 0
        assert len(shell.query("#research-second-changed-basis-epoch-handoff-notice")) == 0


def test_46g_runner_chains_only_exact_explicit_handoff_and_normal_close_launches_nothing(
    tmp_path: Path,
    monkeypatch,
) -> None:
    _, reentry = _continuation(tmp_path, stem="46g-runner-source")
    _, _, result, _ = _direct_46f(tmp_path, stem="46g-runner-target")
    handoff = result.checkpoint.fresh_reentry
    received: list[object] = []

    class SourceShell:
        def __init__(self, returned):
            self.returned = returned

        def run(self):
            return self.returned

    class ReceiverShell:
        def run(self):
            received.append("ran")

    monkeypatch.setattr(
        handoff_ui,
        "create_second_changed_basis_epoch_handoff_research_session_shell",
        lambda *args, **kwargs: SourceShell(None),
    )
    monkeypatch.setattr(
        handoff_ui,
        "create_inspectable_second_basis_epoch_handoff_research_session_shell",
        lambda value: (_ for _ in ()).throw(AssertionError("receiver must not launch")),
    )
    assert handoff_ui.run_second_changed_basis_epoch_handoff_research_session_shell(reentry) is None

    observed: dict[str, object] = {}
    monkeypatch.setattr(
        handoff_ui,
        "create_second_changed_basis_epoch_handoff_research_session_shell",
        lambda *args, **kwargs: SourceShell(handoff),
    )

    def create_receiver(value):
        observed["handoff"] = value
        return ReceiverShell()

    monkeypatch.setattr(
        handoff_ui,
        "create_inspectable_second_basis_epoch_handoff_research_session_shell",
        create_receiver,
    )
    returned = handoff_ui.run_second_changed_basis_epoch_handoff_research_session_shell(reentry)

    assert returned is handoff
    assert observed["handoff"] is handoff
    assert received == ["ran"]
