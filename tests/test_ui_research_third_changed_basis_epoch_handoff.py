from __future__ import annotations

from pathlib import Path

import pytest
from textual.widgets import Button, Input, Static

from pyxis.app.chromium_research_third_basis_epoch_reentry import (
    ChromiumResearchThirdBasisEpochReentryResult,
)
from pyxis.app.chromium_research_third_basis_epoch_shell_lineage import (
    prove_chromium_research_third_basis_epoch_shell_lineage,
)
from pyxis.app.chromium_research_third_changed_basis_epoch_reentry_overlay import (
    persist_chromium_research_third_changed_basis_epoch_reentry_overlay,
)
from pyxis.ui.chromium_research_third_basis_epoch_continuation_checkpoint_textual import (
    ThirdBasisEpochResearchSessionContinuationCheckpointControls,
)
from pyxis.ui.third_basis_epoch_cumulative_handoff_shell import (
    ThirdBasisEpochHandoffResearchSessionShell,
    create_third_basis_epoch_handoff_research_session_shell,
)
from pyxis.ui.third_basis_epoch_research_session_shell import (
    create_third_basis_epoch_research_session_shell,
)
from pyxis.ui.third_basis_epoch_session_handoff_authority_inspection_shell import (
    create_inspectable_third_basis_epoch_handoff_research_session_shell,
)
from pyxis.ui.third_changed_basis_epoch_handoff_research_session_shell import (
    ThirdChangedBasisEpochPersistedSourceHandoffResearchSessionShell,
    create_third_changed_basis_epoch_persisted_source_handoff_research_session_shell,
    create_third_changed_basis_epoch_raw_source_handoff_research_session_shell,
)
import pyxis.ui.third_changed_basis_epoch_handoff_research_session_shell as handoff_ui
from pyxis.ui.third_changed_basis_epoch_reentry_overlay_research_session_shell import (
    create_third_changed_basis_epoch_reentry_overlay_research_session_shell,
)

from test_app_chromium_research_session_working_set_extension import _new_paragraph_member
from test_ui_research_root_backed_session_continuation_checkpoint import (
    _write_and_rollover,
)
from test_ui_research_third_changed_basis_epoch_reentry import (
    _fill_and_verify_47e,
)
from test_ui_research_third_changed_basis_epoch_reentry_overlay import (
    _direct_47e_verification,
    _persist_47f,
)
from test_ui_research_third_changed_basis_session_adoption import (
    _adopt_ui,
    _reach_47c,
)
from test_ui_research_third_changed_basis_transition import (
    _continuation,
    _press,
)


def _direct_47f(tmp_path: Path, *, stem: str):
    lineage, verification = _direct_47e_verification(tmp_path, stem=stem)
    destination = tmp_path / f"{stem}.third-epoch.overlay.json"
    result = persist_chromium_research_third_changed_basis_epoch_reentry_overlay(
        verification,
        prior_second_basis_epoch_continuation_overlay_source=lineage.overlay_source,
        destination=destination,
    )
    return lineage, verification, result, destination


async def _reach_47f_ui(shell, pilot, tmp_path: Path, *, stem: str, overlay: Path):
    prepared, transition, root, edge = await _reach_47c(
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
    adoption = shell.last_third_changed_basis_session_adoption
    assert adoption is not None
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
    verification = shell.last_third_changed_basis_epoch_reentry_verification
    assert verification is not None
    destination = tmp_path / f"{stem}.third-epoch.overlay.json"
    await _persist_47f(
        shell,
        pilot,
        prior_overlay=overlay,
        destination=destination,
    )
    result = shell.last_third_changed_basis_epoch_reentry_overlay
    assert result is not None
    return verification, result, destination


def test_47g_narrow_refactor_preserves_persisted_40b_launch_and_adds_exact_active_reentry(
    tmp_path: Path,
) -> None:
    _, _, result, destination = _direct_47f(tmp_path, stem="47g-persisted")
    earned = result.checkpoint.fresh_reentry
    lineage = prove_chromium_research_third_basis_epoch_shell_lineage(
        earned,
        overlay_source=destination,
    )
    shell = create_third_basis_epoch_research_session_shell(lineage)

    assert shell.third_basis_epoch_launch_lineage is lineage
    assert shell.third_basis_epoch_reentry is lineage.reentry
    assert shell.research_controller is lineage.reentry.controller
    assert shell.research_reentry is None


def test_47g_raw_receiver_retains_exact_typed_handoff_without_path_authority(
    tmp_path: Path,
) -> None:
    _, _, result, _ = _direct_47f(tmp_path, stem="47g-raw")
    handoff = result.checkpoint.fresh_reentry
    shell = create_third_basis_epoch_handoff_research_session_shell(handoff)

    assert isinstance(shell, ThirdBasisEpochHandoffResearchSessionShell)
    assert shell.third_basis_epoch_launch_lineage is None
    assert shell.third_basis_epoch_handoff_reentry is handoff
    assert shell.third_basis_epoch_reentry is handoff
    assert shell.research_controller is handoff.controller
    assert shell.research_reentry is None
    assert not hasattr(shell, "third_basis_epoch_overlay_source")


@pytest.mark.asyncio
async def test_47g_raw_receiver_rollover_mounts_existing_blank_40c_surface(
    tmp_path: Path,
) -> None:
    _, _, result, _ = _direct_47f(tmp_path, stem="47g-rollover")
    handoff = result.checkpoint.fresh_reentry
    shell = create_third_basis_epoch_handoff_research_session_shell(handoff)

    async with shell.run_test(size=(190, 280)) as pilot:
        await pilot.pause()
        assert len(shell.query(ThirdBasisEpochResearchSessionContinuationCheckpointControls)) == 0
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=handoff.controller.declared_endpoint.verification.path,
            successor=tmp_path / "47g-rollover-successor.json",
            declaration=tmp_path / "47g-rollover-declaration.json",
            text="Explicit continuation after the pathless 47G third-epoch handoff.",
        )

        controls = shell.query_one(
            ThirdBasisEpochResearchSessionContinuationCheckpointControls
        )
        assert shell.third_basis_epoch_launch_lineage is None
        assert shell.third_basis_epoch_handoff_reentry is handoff
        assert shell.third_basis_epoch_reentry is handoff
        assert controls.rollover is shell.last_research_rollover
        for selector in (
            "#research-third-basis-epoch-checkpoint-prior-overlay-source",
            "#research-third-basis-epoch-checkpoint-successor-source",
            "#research-third-basis-epoch-checkpoint-declaration-source",
            "#research-third-basis-epoch-checkpoint-destination",
        ):
            assert shell.query_one(selector, Input).value == ""


@pytest.mark.asyncio
async def test_47g_inspection_is_pathless_and_rollover_preserves_exact_launch_object(
    tmp_path: Path,
) -> None:
    _, _, result, _ = _direct_47f(tmp_path, stem="47g-inspection")
    handoff = result.checkpoint.fresh_reentry
    shell = create_inspectable_third_basis_epoch_handoff_research_session_shell(handoff)
    panel = shell.third_basis_epoch_authority_inspection
    launch = panel.launch_provenance

    second_epoch = (
        handoff.prior_second_basis_epoch_continuation_reentry
        .prior_second_basis_epoch_reentry
    )
    assert launch.launch_family == "in-process 47G typed third-basis-epoch handoff"
    assert launch.launch_location_context is None
    assert (
        launch.first_root_sha256
        == second_epoch.prior_continuation_reentry.prior_root_backed_reentry.loaded_root.verification.root_record_sha256
    )
    assert launch.second_root_sha256 == second_epoch.loaded_root.verification.root_record_sha256
    assert launch.third_root_sha256 == handoff.loaded_root.verification.root_record_sha256
    assert (
        launch.launch_endpoint_sha256
        == handoff.controller.declared_endpoint.verification.edge_record_sha256
    )

    async with shell.run_test(size=(195, 300)) as pilot:
        await pilot.pause()
        current_before = panel.current_state
        await _write_and_rollover(
            shell,
            pilot,
            prior_edge=handoff.controller.declared_endpoint.verification.path,
            successor=tmp_path / "47g-inspection-successor.json",
            declaration=tmp_path / "47g-inspection-declaration.json",
            text="Visible continuation after the 47G handoff inspection launch.",
        )

        assert panel.launch_provenance is launch
        assert panel.launch_provenance.launch_location_context is None
        assert panel.current_state is not current_before
        assert panel.current_state.state_source == "explicit rollover after in-process 47G handoff"
        assert (
            panel.current_state.endpoint_sha256
            == shell.research_controller.declared_endpoint.verification.edge_record_sha256
        )


@pytest.mark.asyncio
async def test_47g_success_requires_explicit_choice_and_returns_exact_40b_fresh_reentry(
    tmp_path: Path,
    monkeypatch,
) -> None:
    _, overlay, _, lineage = _continuation(tmp_path, stem="47g-success")
    member, _ = _new_paragraph_member(tmp_path, stem="47g-success-member")
    shell = create_third_changed_basis_epoch_persisted_source_handoff_research_session_shell(
        lineage,
        (member,),
    )
    assert isinstance(shell, ThirdChangedBasisEpochPersistedSourceHandoffResearchSessionShell)
    observed: dict[str, object] = {}

    def fake_exit(result=None, *args, **kwargs) -> None:
        observed["result"] = result

    monkeypatch.setattr(shell, "exit", fake_exit)

    async with shell.run_test(size=(235, 900)) as pilot:
        await pilot.pause()
        assert len(shell.query("#continue-third-changed-basis-epoch-session")) == 0

        verification, result, destination = await _reach_47f_ui(
            shell,
            pilot,
            tmp_path,
            stem="47g-success",
            overlay=overlay,
        )

        assert "result" not in observed
        mounted_controller = shell.research_controller
        mounted_session = shell.research_session
        mounted_reentry = shell.research_reentry
        button = shell.query_one("#continue-third-changed-basis-epoch-session", Button)
        assert not button.disabled
        notice = str(
            shell.query_one("#research-third-changed-basis-epoch-handoff-notice", Static).content
        )
        assert "currently mounted changed-basis product remains unchanged" in notice
        assert "saved 40B overlay path is not reloaded" in notice

        destination.unlink()
        await _press(shell, pilot, "continue-third-changed-basis-epoch-session")

        assert observed["result"] is result.checkpoint.fresh_reentry
        assert observed["result"] is not verification.fresh_reentry
        assert type(observed["result"]) is ChromiumResearchThirdBasisEpochReentryResult
        assert shell.research_controller is mounted_controller
        assert shell.research_session is mounted_session
        assert shell.research_reentry is mounted_reentry


@pytest.mark.asyncio
async def test_47g_failed_47f_persistence_never_exposes_handoff(tmp_path: Path) -> None:
    _, overlay, _, lineage = _continuation(tmp_path, stem="47g-gated")
    member, _ = _new_paragraph_member(tmp_path, stem="47g-gated-member")
    shell = create_third_changed_basis_epoch_persisted_source_handoff_research_session_shell(
        lineage,
        (member,),
    )

    async with shell.run_test(size=(235, 880)) as pilot:
        await pilot.pause()
        prepared, transition, root, edge = await _reach_47c(
            shell,
            pilot,
            tmp_path,
            stem="47g-gated",
        )
        await _adopt_ui(
            shell,
            pilot,
            edge,
            tmp_path / "47g-gated-adoption-declaration.json",
        )
        adoption = shell.last_third_changed_basis_session_adoption
        assert adoption is not None
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

        existing = tmp_path / "47g-gated-existing.overlay.json"
        existing.write_text("preserve exactly\n", encoding="utf-8")
        await _persist_47f(
            shell,
            pilot,
            prior_overlay=overlay,
            destination=existing,
        )

        assert shell.last_third_changed_basis_epoch_reentry_overlay is None
        assert existing.read_text(encoding="utf-8") == "preserve exactly\n"
        assert len(shell.query("#continue-third-changed-basis-epoch-session")) == 0
        assert len(shell.query("#research-third-changed-basis-epoch-handoff-notice")) == 0


@pytest.mark.asyncio
async def test_47g_raw_source_family_exposes_same_typed_handoff_after_exact_47f(
    tmp_path: Path,
    monkeypatch,
) -> None:
    _, overlay, reentry, _ = _continuation(tmp_path, stem="47g-raw-source")
    member, _ = _new_paragraph_member(tmp_path, stem="47g-raw-source-member")
    shell = create_third_changed_basis_epoch_raw_source_handoff_research_session_shell(
        reentry,
        (member,),
    )
    observed: dict[str, object] = {}
    monkeypatch.setattr(
        shell,
        "exit",
        lambda result=None, *args, **kwargs: observed.__setitem__("result", result),
    )

    async with shell.run_test(size=(235, 900)) as pilot:
        await pilot.pause()
        verification, result, _ = await _reach_47f_ui(
            shell,
            pilot,
            tmp_path,
            stem="47g-raw-source",
            overlay=overlay,
        )
        assert shell.second_basis_epoch_continuation_launch_lineage is None
        assert len(shell.query("#continue-third-changed-basis-epoch-session")) == 1
        await _press(shell, pilot, "continue-third-changed-basis-epoch-session")
        assert observed["result"] is result.checkpoint.fresh_reentry
        assert observed["result"] is not verification.fresh_reentry


@pytest.mark.asyncio
async def test_plain_47f_product_does_not_gain_47g_handoff_surface(
    tmp_path: Path,
) -> None:
    _, overlay, _, lineage = _continuation(tmp_path, stem="47g-plain")
    member, _ = _new_paragraph_member(tmp_path, stem="47g-plain-member")
    shell = create_third_changed_basis_epoch_reentry_overlay_research_session_shell(
        lineage
    )
    shell.configure_changed_basis_candidate((member,))

    async with shell.run_test(size=(235, 880)) as pilot:
        await pilot.pause()
        await _reach_47f_ui(
            shell,
            pilot,
            tmp_path,
            stem="47g-plain",
            overlay=overlay,
        )
        assert shell.last_third_changed_basis_epoch_reentry_overlay is not None
        assert len(shell.query("#continue-third-changed-basis-epoch-session")) == 0
        assert len(shell.query("#research-third-changed-basis-epoch-handoff-notice")) == 0


def test_47g_runner_chains_only_exact_explicit_handoff_and_normal_close_launches_nothing(
    tmp_path: Path,
    monkeypatch,
) -> None:
    _, _, _, lineage = _continuation(tmp_path, stem="47g-runner-source")
    _, _, result, _ = _direct_47f(tmp_path, stem="47g-runner-target")
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
        "create_third_changed_basis_epoch_persisted_source_handoff_research_session_shell",
        lambda *args, **kwargs: SourceShell(None),
    )
    monkeypatch.setattr(
        handoff_ui,
        "create_inspectable_third_basis_epoch_handoff_research_session_shell",
        lambda value: (_ for _ in ()).throw(AssertionError("receiver must not launch")),
    )
    assert handoff_ui.run_third_changed_basis_epoch_handoff_research_session_shell(lineage) is None

    observed: dict[str, object] = {}
    monkeypatch.setattr(
        handoff_ui,
        "create_third_changed_basis_epoch_persisted_source_handoff_research_session_shell",
        lambda *args, **kwargs: SourceShell(handoff),
    )

    def create_receiver(value):
        observed["handoff"] = value
        return ReceiverShell()

    monkeypatch.setattr(
        handoff_ui,
        "create_inspectable_third_basis_epoch_handoff_research_session_shell",
        create_receiver,
    )
    returned = handoff_ui.run_third_changed_basis_epoch_handoff_research_session_shell(lineage)

    assert returned is handoff
    assert observed["handoff"] is handoff
    assert received == ["ran"]


def test_47g_factories_reject_wrong_authority_families() -> None:
    with pytest.raises(
        TypeError,
        match="ChromiumResearchSecondBasisEpochContinuationShellLineage",
    ):
        create_third_changed_basis_epoch_persisted_source_handoff_research_session_shell(object())  # type: ignore[arg-type]

    with pytest.raises(
        TypeError,
        match="exactly ChromiumResearchSecondBasisEpochContinuationReentryResult",
    ):
        create_third_changed_basis_epoch_raw_source_handoff_research_session_shell(object())  # type: ignore[arg-type]

    with pytest.raises(
        TypeError,
        match="exactly ChromiumResearchThirdBasisEpochReentryResult",
    ):
        create_third_basis_epoch_handoff_research_session_shell(object())  # type: ignore[arg-type]
