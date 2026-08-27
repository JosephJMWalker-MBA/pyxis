from __future__ import annotations

from pathlib import Path

import pyxis.app.chromium_research_fixed_anchor_cumulative_extension as kernel_module
import pyxis.app.chromium_research_root_backed_session_continuation_checkpoint_extension as root_module
import pyxis.app.chromium_research_second_basis_epoch_continuation_checkpoint_extension as second_module
import pyxis.app.chromium_research_third_basis_epoch_continuation_checkpoint_extension as third_module
from test_app_chromium_research_root_backed_session_continuation_checkpoint_extension import (
    _persist_extension as _persist_root_extension,
)
from test_app_chromium_research_second_basis_epoch_continuation_checkpoint_extension import (
    _persist_extension as _persist_second_extension,
)
from test_app_chromium_research_third_basis_epoch_continuation_checkpoint_extension import (
    _persist_extension as _persist_third_extension,
)


def _record_kernel_calls(monkeypatch, module):
    calls: list[object] = []
    original = module._extend_fixed_anchor_cumulative_continuation

    def recording_kernel(*args, **kwargs):
        calls.append(kwargs["adapter"])
        return original(*args, **kwargs)

    monkeypatch.setattr(
        module,
        "_extend_fixed_anchor_cumulative_continuation",
        recording_kernel,
    )
    return calls


def _fixture_directory(tmp_path: Path, name: str) -> Path:
    destination = tmp_path / name
    destination.mkdir(parents=True, exist_ok=False)
    return destination


def test_all_three_concrete_extension_families_execute_through_private_kernel(
    tmp_path: Path,
    monkeypatch,
) -> None:
    root_calls = _record_kernel_calls(monkeypatch, root_module)
    second_calls = _record_kernel_calls(monkeypatch, second_module)
    third_calls = _record_kernel_calls(monkeypatch, third_module)

    root_values = _persist_root_extension(
        _fixture_directory(tmp_path, "root"),
        stem="43a-root",
    )
    second_values = _persist_second_extension(
        _fixture_directory(tmp_path, "second"),
        stem="43a-second",
    )
    third_values = _persist_third_extension(
        _fixture_directory(tmp_path, "third"),
        stem="43a-third",
    )

    assert root_calls == [root_module._ADAPTER]
    assert second_calls == [second_module._ADAPTER]
    assert third_calls == [third_module._ADAPTER]

    root_current, root_result = root_values[0], root_values[-1]
    assert root_result.next_plan.prior_root_backed_overlay_source == (
        root_current.plan.prior_root_backed_overlay_source
    )

    second_current, second_result = second_values[0], second_values[-1]
    assert second_result.next_plan.prior_second_basis_epoch_overlay_source == (
        second_current.plan.prior_second_basis_epoch_overlay_source
    )

    third_current, third_result = third_values[0], third_values[-1]
    assert third_result.next_plan.prior_third_basis_epoch_overlay_source == (
        third_current.plan.prior_third_basis_epoch_overlay_source
    )


def test_fixed_anchor_kernel_has_no_public_authority_surface() -> None:
    assert kernel_module.__all__ == []
    assert not hasattr(kernel_module, "Epoch")
    assert not hasattr(kernel_module, "epoch")
