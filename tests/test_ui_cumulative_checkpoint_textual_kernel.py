from __future__ import annotations

import pyxis.ui.chromium_research_cumulative_checkpoint_textual as kernel_module
import pyxis.ui.chromium_research_root_backed_session_continuation_checkpoint_extension_textual as root_module
import pyxis.ui.chromium_research_second_basis_epoch_continuation_checkpoint_extension_textual as second_module
import pyxis.ui.chromium_research_third_basis_epoch_continuation_checkpoint_extension_textual as third_module
from pyxis.app.chromium_research_root_backed_session_continuation_checkpoint_extension import (
    ChromiumResearchRootBackedSessionContinuationCheckpointExtensionResult,
)
from pyxis.app.chromium_research_second_basis_epoch_continuation_checkpoint_extension import (
    ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionResult,
)
from pyxis.app.chromium_research_third_basis_epoch_continuation_checkpoint_extension import (
    ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionResult,
)


class _LockSpy:
    def __init__(self) -> None:
        self.calls: list[tuple[object, dict[str, object]]] = []

    def _lock_cumulative_checkpoint_after_success(self, result, **kwargs) -> None:
        self.calls.append((result, kwargs))


def _assert_concrete_lock_delegates(public_class, result_type) -> None:
    spy = _LockSpy()
    marker = object()
    public_class.lock_after_success(spy, marker)

    assert len(spy.calls) == 1
    result, kwargs = spy.calls[0]
    assert result is marker
    assert kwargs["result_type"] is result_type
    assert isinstance(kwargs["result_type_error"], str)
    assert isinstance(kwargs["current_identity_error"], str)
    assert isinstance(kwargs["rollover_identity_error"], str)


def test_all_three_public_controls_use_private_compose_and_lock_mechanics() -> None:
    families = (
        (
            root_module.RootBackedResearchSessionCumulativeCheckpointControls,
            ChromiumResearchRootBackedSessionContinuationCheckpointExtensionResult,
        ),
        (
            second_module.SecondBasisEpochResearchSessionCumulativeCheckpointControls,
            ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionResult,
        ),
        (
            third_module.ThirdBasisEpochResearchSessionCumulativeCheckpointControls,
            ChromiumResearchThirdBasisEpochContinuationCheckpointExtensionResult,
        ),
    )

    for public_class, result_type in families:
        assert issubclass(
            public_class,
            kernel_module._CumulativeCheckpointTextualControls,
        )
        assert public_class.compose is kernel_module._CumulativeCheckpointTextualControls.compose
        _assert_concrete_lock_delegates(public_class, result_type)


def test_concrete_specs_preserve_four_explicit_blank_path_roles() -> None:
    specs = (root_module._SPEC, second_module._SPEC, third_module._SPEC)

    for spec in specs:
        assert len(spec.input_ids) == 4
        assert len(set(spec.input_ids)) == 4
        assert spec.current_overlay_input_id in spec.input_ids
        assert spec.successor_input_id in spec.input_ids
        assert spec.declaration_input_id in spec.input_ids
        assert spec.overlay_input_id in spec.input_ids
        assert spec.save_button_id
        assert spec.status_id


def test_private_textual_kernel_exposes_no_public_authority_surface() -> None:
    assert kernel_module.__all__ == []
    assert not hasattr(kernel_module, "Epoch")
    assert not hasattr(kernel_module, "Root")
