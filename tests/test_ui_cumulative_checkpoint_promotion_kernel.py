from __future__ import annotations

import asyncio
from types import SimpleNamespace

import pyxis.ui.chromium_research_cumulative_checkpoint_promotion_textual as kernel_module
import pyxis.ui.root_backed_continuation_research_session_shell as root_module
import pyxis.ui.second_basis_epoch_research_session_shell as second_module
import pyxis.ui.third_basis_epoch_research_session_shell as third_module


def _exercise_concrete_promotion(
    monkeypatch,
    *,
    module,
    method,
    receipt_name: str,
    spec,
    current_reentry_attr: str,
    last_checkpoint_attr: str,
) -> None:
    prior_reentry = object()
    fresh_reentry = object()
    result = SimpleNamespace(fresh_reentry=fresh_reentry)
    shell = SimpleNamespace()
    setattr(shell, current_reentry_attr, prior_reentry)
    setattr(shell, last_checkpoint_attr, None)
    calls: list[dict[str, object]] = []

    async def promotion_spy(received_shell, **kwargs) -> None:
        assert received_shell is shell
        calls.append(kwargs)
        kwargs["advance_current_reentry"](kwargs["fresh_reentry"])
        kwargs["record_checkpoint"](kwargs["checkpoint_result"])

    monkeypatch.setattr(module, "_promote_cumulative_checkpoint_surface", promotion_spy)
    monkeypatch.setattr(module, receipt_name, lambda received: "concrete receipt")

    asyncio.run(method(shell, result))

    assert len(calls) == 1
    call = calls[0]
    assert call["fresh_reentry"] is fresh_reentry
    assert call["checkpoint_result"] is result
    assert call["spec"] is spec
    assert call["success_receipt_text"] == "concrete receipt"
    assert getattr(shell, current_reentry_attr) is fresh_reentry
    assert getattr(shell, last_checkpoint_attr) is result


def test_all_three_concrete_promotion_methods_delegate_to_private_kernel(monkeypatch) -> None:
    _exercise_concrete_promotion(
        monkeypatch,
        module=root_module,
        method=root_module.RootBackedContinuationResearchSessionShell._promote_cumulative_checkpoint,
        receipt_name="cumulative_checkpoint_success_receipt",
        spec=root_module._ROOT_BACKED_CUMULATIVE_PROMOTION,
        current_reentry_attr="root_backed_continuation_reentry",
        last_checkpoint_attr="last_root_backed_cumulative_checkpoint",
    )
    _exercise_concrete_promotion(
        monkeypatch,
        module=second_module,
        method=(
            second_module.SecondBasisEpochContinuationResearchSessionShell
            ._promote_second_basis_epoch_cumulative_checkpoint
        ),
        receipt_name="second_basis_epoch_cumulative_checkpoint_success_receipt",
        spec=second_module._SECOND_BASIS_EPOCH_CUMULATIVE_PROMOTION,
        current_reentry_attr="second_basis_epoch_continuation_reentry",
        last_checkpoint_attr="last_second_basis_epoch_cumulative_checkpoint",
    )
    _exercise_concrete_promotion(
        monkeypatch,
        module=third_module,
        method=(
            third_module.ThirdBasisEpochContinuationResearchSessionShell
            ._promote_third_basis_epoch_cumulative_checkpoint
        ),
        receipt_name="third_basis_epoch_cumulative_checkpoint_success_receipt",
        spec=third_module._THIRD_BASIS_EPOCH_CUMULATIVE_PROMOTION,
        current_reentry_attr="third_basis_epoch_continuation_reentry",
        last_checkpoint_attr="last_third_basis_epoch_cumulative_checkpoint",
    )


def test_concrete_promotion_specs_preserve_existing_surface_contracts() -> None:
    assert root_module._ROOT_BACKED_CUMULATIVE_PROMOTION.checkpoint_controls_selector == (
        "#research-root-backed-cumulative-checkpoint-controls"
    )
    assert root_module._ROOT_BACKED_CUMULATIVE_PROMOTION.success_receipt_id == (
        "research-root-backed-cumulative-checkpoint-success-receipt"
    )
    assert second_module._SECOND_BASIS_EPOCH_CUMULATIVE_PROMOTION.checkpoint_controls_selector == (
        "#research-second-basis-epoch-cumulative-checkpoint-controls"
    )
    assert second_module._SECOND_BASIS_EPOCH_CUMULATIVE_PROMOTION.success_receipt_id == (
        "research-second-basis-epoch-cumulative-checkpoint-success-receipt"
    )
    assert third_module._THIRD_BASIS_EPOCH_CUMULATIVE_PROMOTION.checkpoint_controls_selector == (
        "#research-third-basis-epoch-cumulative-checkpoint-controls"
    )
    assert third_module._THIRD_BASIS_EPOCH_CUMULATIVE_PROMOTION.success_receipt_id == (
        "research-third-basis-epoch-cumulative-checkpoint-success-receipt"
    )


def test_private_promotion_kernel_exposes_no_public_authority_surface() -> None:
    assert kernel_module.__all__ == []
    assert not hasattr(kernel_module, "Epoch")
    assert not hasattr(kernel_module, "Root")
