from __future__ import annotations

import asyncio
import inspect

import pytest

import pyxis.ui.chromium_research_cumulative_checkpoint_rollover_textual as kernel_module
import pyxis.ui.root_backed_continuation_research_session_shell as root_module
import pyxis.ui.second_basis_epoch_research_session_shell as second_module
import pyxis.ui.third_basis_epoch_research_session_shell as third_module
from pyxis.ui.chromium_research_endpoint_revision_textual import ResearchEndpointRevisionControls
from pyxis.ui.chromium_research_session_restart_plan_textual import ResearchSessionRestartPlanControls
from pyxis.ui.chromium_research_session_rollover_textual import ResearchSessionRolloverControls


class _Removable:
    def __init__(self, name: str) -> None:
        self.name = name
        self.removed = False

    async def remove(self) -> None:
        self.removed = True


class _FakeShell:
    def __init__(self, rollover) -> None:
        self.last_research_rollover = rollover
        self.stale_receipt = _Removable("receipt")
        self.revision = _Removable("revision")
        self.rollover_controls = _Removable("rollover")
        self.restart_controls: list[object] = []
        self.mounted: list[object] = []

    def query(self, selector_or_type):
        if selector_or_type == "#stale-receipt":
            return [self.stale_receipt]
        if selector_or_type is ResearchSessionRestartPlanControls:
            return self.restart_controls
        return []

    def query_one(self, selector, expected_type):
        if selector == "#stale-receipt":
            return self.stale_receipt
        if selector == "#research-endpoint-revision-controls":
            assert expected_type is ResearchEndpointRevisionControls
            return self.revision
        if selector == "#research-session-rollover-controls":
            assert expected_type is ResearchSessionRolloverControls
            return self.rollover_controls
        raise AssertionError(f"unexpected query_one: {selector!r}")

    async def mount(self, widget) -> None:
        self.mounted.append(widget)


def test_private_rollover_kernel_preserves_post_base_surface_ordering() -> None:
    rollover = object()
    current_reentry = object()
    shell = _FakeShell(rollover)
    checkpoint_controls = object()
    factory_calls: list[tuple[object, object]] = []

    def create_checkpoint_controls(current, received_rollover):
        factory_calls.append((current, received_rollover))
        return checkpoint_controls

    spec = kernel_module._CumulativeCheckpointRolloverMountSpec(
        stale_success_receipt_selector="#stale-receipt",
        retained_rollover_error="retained rollover mismatch",
        restart_plan_error="ordinary restart plan forbidden",
    )

    asyncio.run(
        kernel_module._mount_cumulative_checkpoint_after_rollover(
            shell,
            current_reentry=current_reentry,
            rollover=rollover,
            spec=spec,
            create_checkpoint_controls=create_checkpoint_controls,
        )
    )

    assert shell.stale_receipt.removed is True
    assert shell.revision.removed is True
    assert shell.rollover_controls.removed is True
    assert factory_calls == [(current_reentry, rollover)]
    assert len(shell.mounted) == 3
    locked_revision, empty_rollover, mounted_checkpoint = shell.mounted
    assert isinstance(locked_revision, ResearchEndpointRevisionControls)
    assert locked_revision.restart_checkpoint_required is True
    assert isinstance(empty_rollover, ResearchSessionRolloverControls)
    assert mounted_checkpoint is checkpoint_controls


def test_private_rollover_kernel_rejects_wrong_base_retention_and_restart_plan() -> None:
    expected_rollover = object()
    shell = _FakeShell(object())
    spec = kernel_module._CumulativeCheckpointRolloverMountSpec(
        stale_success_receipt_selector="#stale-receipt",
        retained_rollover_error="retained rollover mismatch",
        restart_plan_error="ordinary restart plan forbidden",
    )

    with pytest.raises(ValueError, match="retained rollover mismatch"):
        asyncio.run(
            kernel_module._mount_cumulative_checkpoint_after_rollover(
                shell,
                current_reentry=object(),
                rollover=expected_rollover,
                spec=spec,
                create_checkpoint_controls=lambda current, rollover: object(),
            )
        )

    shell = _FakeShell(expected_rollover)
    shell.restart_controls.append(object())
    with pytest.raises(ValueError, match="ordinary restart plan forbidden"):
        asyncio.run(
            kernel_module._mount_cumulative_checkpoint_after_rollover(
                shell,
                current_reentry=object(),
                rollover=expected_rollover,
                spec=spec,
                create_checkpoint_controls=lambda current, rollover: object(),
            )
        )

    assert shell.stale_receipt.removed is True
    assert shell.revision.removed is False
    assert shell.rollover_controls.removed is False
    assert shell.mounted == []


def test_all_three_cumulative_rollover_methods_delegate_after_base_rollover() -> None:
    families = (
        (
            root_module.RootBackedContinuationResearchSessionShell._mount_research_rollover,
            "_ROOT_BACKED_CUMULATIVE_ROLLOVER",
        ),
        (
            second_module.SecondBasisEpochContinuationResearchSessionShell._mount_research_rollover,
            "_SECOND_BASIS_EPOCH_CUMULATIVE_ROLLOVER",
        ),
        (
            third_module.ThirdBasisEpochContinuationResearchSessionShell._mount_research_rollover,
            "_THIRD_BASIS_EPOCH_CUMULATIVE_ROLLOVER",
        ),
    )

    for method, spec_name in families:
        source = inspect.getsource(method)
        base_call = "await super()._mount_research_rollover(result)"
        kernel_call = "await _mount_cumulative_checkpoint_after_rollover("
        assert base_call in source
        assert kernel_call in source
        assert source.index(base_call) < source.index(kernel_call)
        assert "current_reentry=current_reentry" in source
        assert "rollover=result" in source
        assert f"spec={spec_name}" in source
        assert "create_checkpoint_controls=create_checkpoint_controls" in source


def test_concrete_rollover_specs_preserve_existing_surface_contracts() -> None:
    assert root_module._ROOT_BACKED_CUMULATIVE_ROLLOVER == (
        kernel_module._CumulativeCheckpointRolloverMountSpec(
            stale_success_receipt_selector=(
                "#research-root-backed-cumulative-checkpoint-success-receipt"
            ),
            retained_rollover_error=(
                "Base research shell did not retain the exact cumulative-lineage rollover."
            ),
            restart_plan_error=(
                "Cumulative root-backed shell must not mount ordinary restart-plan controls."
            ),
        )
    )
    assert second_module._SECOND_BASIS_EPOCH_CUMULATIVE_ROLLOVER == (
        kernel_module._CumulativeCheckpointRolloverMountSpec(
            stale_success_receipt_selector=(
                "#research-second-basis-epoch-cumulative-checkpoint-success-receipt"
            ),
            retained_rollover_error=(
                "Base research shell did not retain the exact cumulative second-epoch rollover."
            ),
            restart_plan_error=(
                "Cumulative second-epoch shell must not mount ordinary restart-plan controls."
            ),
        )
    )
    assert third_module._THIRD_BASIS_EPOCH_CUMULATIVE_ROLLOVER == (
        kernel_module._CumulativeCheckpointRolloverMountSpec(
            stale_success_receipt_selector=(
                "#research-third-basis-epoch-cumulative-checkpoint-success-receipt"
            ),
            retained_rollover_error=(
                "Base research shell did not retain the exact cumulative third-epoch rollover."
            ),
            restart_plan_error=(
                "Cumulative third-epoch shell must not mount ordinary restart-plan controls."
            ),
        )
    )


def test_private_rollover_kernel_exposes_no_public_authority_surface() -> None:
    assert kernel_module.__all__ == []
    assert not hasattr(kernel_module, "Epoch")
    assert not hasattr(kernel_module, "Root")
