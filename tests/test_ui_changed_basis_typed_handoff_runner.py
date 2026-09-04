from __future__ import annotations

import pytest

import pyxis.ui.chromium_research_changed_basis_typed_handoff_runner as kernel
import pyxis.ui.first_changed_basis_root_backed_handoff_research_session_shell as first
import pyxis.ui.second_changed_basis_epoch_handoff_research_session_shell as second
import pyxis.ui.third_changed_basis_epoch_handoff_research_session_shell as third


def test_48b_private_runner_kernel_exports_no_public_authority_surface() -> None:
    assert kernel.__all__ == []


def test_48b_normal_close_returns_none_without_receiver_construction() -> None:
    observed = {"receiver": 0}

    def create_receiver(value):
        observed["receiver"] += 1
        raise AssertionError("normal close must not create a receiver")

    assert (
        kernel._run_changed_basis_typed_handoff(
            run_source=lambda: None,
            validate_handoff=lambda value: True,
            invalid_handoff_error="invalid concrete handoff",
            create_receiver=create_receiver,
        )
        is None
    )
    assert observed["receiver"] == 0


def test_48b_invalid_handoff_rejects_before_receiver_construction() -> None:
    observed = {"receiver": 0}
    invalid = object()

    def create_receiver(value):
        observed["receiver"] += 1
        raise AssertionError("invalid handoff must not reach receiver construction")

    with pytest.raises(TypeError, match="invalid exact runner handoff"):
        kernel._run_changed_basis_typed_handoff(
            run_source=lambda: invalid,
            validate_handoff=lambda value: False,
            invalid_handoff_error="invalid exact runner handoff",
            create_receiver=create_receiver,
        )

    assert observed["receiver"] == 0


def test_48b_valid_handoff_reaches_receiver_by_exact_identity_runs_once_and_returns_same_object() -> None:
    handoff = object()
    observed: dict[str, object] = {"runs": 0}

    class Receiver:
        def run(self):
            observed["runs"] = int(observed["runs"]) + 1
            return object()

    def create_receiver(value):
        observed["received"] = value
        return Receiver()

    returned = kernel._run_changed_basis_typed_handoff(
        run_source=lambda: handoff,
        validate_handoff=lambda value: value is handoff,
        invalid_handoff_error="invalid exact runner handoff",
        create_receiver=create_receiver,
    )

    assert returned is handoff
    assert observed["received"] is handoff
    assert observed["runs"] == 1


def test_48b_all_three_concrete_runners_delegate_same_private_procedure() -> None:
    assert first._run_changed_basis_typed_handoff is kernel._run_changed_basis_typed_handoff
    assert second._run_changed_basis_typed_handoff is kernel._run_changed_basis_typed_handoff
    assert third._run_changed_basis_typed_handoff is kernel._run_changed_basis_typed_handoff

    assert first._is_first_changed_basis_root_backed_handoff is not (
        second._is_second_changed_basis_epoch_handoff
    )
    assert second._is_second_changed_basis_epoch_handoff is not (
        third._is_third_changed_basis_epoch_handoff
    )
