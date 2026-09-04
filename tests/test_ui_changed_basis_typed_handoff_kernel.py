from __future__ import annotations

from types import SimpleNamespace

import pytest
from textual.widgets import Button, Static

import pyxis.ui.chromium_research_changed_basis_typed_handoff_textual as kernel
import pyxis.ui.first_changed_basis_root_backed_handoff_research_session_shell as first
import pyxis.ui.second_changed_basis_epoch_handoff_research_session_shell as second
import pyxis.ui.third_changed_basis_epoch_handoff_research_session_shell as third


class _FakeShell:
    def __init__(self) -> None:
        self.mounted: list[object] = []
        self.existing_selectors: set[str] = set()

    def query(self, selector: str):
        return [object()] if selector in self.existing_selectors else []

    async def mount(self, widget) -> None:
        self.mounted.append(widget)


def _result_with(handoff: object):
    return SimpleNamespace(checkpoint=SimpleNamespace(fresh_reentry=handoff))


def _spec() -> kernel._ChangedBasisTypedHandoffSurfaceSpec:
    return kernel._ChangedBasisTypedHandoffSurfaceSpec(
        button_id="continue-test-handoff",
        notice_id="test-handoff-notice",
        notice_text="Exact concrete handoff notice.",
        button_label="Continue exact handoff",
        missing_result_error="missing exact persistence",
        invalid_handoff_error="invalid exact handoff",
        duplicate_controls_error="duplicate exact handoff controls",
    )


def test_48a_private_kernel_exports_no_public_authority_surface() -> None:
    assert kernel.__all__ == []


def test_48a_requires_exact_retained_checkpoint_fresh_object_via_concrete_validator() -> None:
    spec = _spec()
    handoff = object()
    result = _result_with(handoff)

    assert (
        kernel._require_changed_basis_checkpoint_fresh_handoff(
            result,
            spec=spec,
            validate_handoff=lambda value: value is handoff,
        )
        is handoff
    )

    with pytest.raises(ValueError, match="missing exact persistence"):
        kernel._require_changed_basis_checkpoint_fresh_handoff(
            None,
            spec=spec,
            validate_handoff=lambda value: True,
        )

    with pytest.raises(TypeError, match="invalid exact handoff"):
        kernel._require_changed_basis_checkpoint_fresh_handoff(
            result,
            spec=spec,
            validate_handoff=lambda value: False,
        )


@pytest.mark.asyncio
async def test_48a_new_result_gate_mounts_only_concrete_notice_and_button() -> None:
    spec = _spec()
    shell = _FakeShell()
    prior = _result_with(object())

    assert (
        await kernel._mount_changed_basis_typed_handoff_after_new_persistence(
            shell,  # type: ignore[arg-type]
            previous_result=prior,
            current_result=prior,
            spec=spec,
            validate_handoff=lambda value: True,
        )
        is None
    )
    assert shell.mounted == []

    handoff = object()
    current = _result_with(handoff)
    returned = await kernel._mount_changed_basis_typed_handoff_after_new_persistence(
        shell,  # type: ignore[arg-type]
        previous_result=prior,
        current_result=current,
        spec=spec,
        validate_handoff=lambda value: value is handoff,
    )

    assert returned is handoff
    assert len(shell.mounted) == 2
    notice, button = shell.mounted
    assert isinstance(notice, Static)
    assert notice.id == spec.notice_id
    assert str(notice.content) == spec.notice_text
    assert isinstance(button, Button)
    assert button.id == spec.button_id
    assert str(button.label) == spec.button_label


@pytest.mark.asyncio
async def test_48a_duplicate_guard_and_invalid_type_fire_before_mount() -> None:
    spec = _spec()
    handoff = object()
    result = _result_with(handoff)

    invalid_shell = _FakeShell()
    with pytest.raises(TypeError, match="invalid exact handoff"):
        await kernel._mount_changed_basis_typed_handoff_after_new_persistence(
            invalid_shell,  # type: ignore[arg-type]
            previous_result=None,
            current_result=result,
            spec=spec,
            validate_handoff=lambda value: False,
        )
    assert invalid_shell.mounted == []

    duplicate_shell = _FakeShell()
    duplicate_shell.existing_selectors.add(f"#{spec.notice_id}")
    with pytest.raises(ValueError, match="duplicate exact handoff controls"):
        await kernel._mount_changed_basis_typed_handoff_after_new_persistence(
            duplicate_shell,  # type: ignore[arg-type]
            previous_result=None,
            current_result=result,
            spec=spec,
            validate_handoff=lambda value: value is handoff,
        )
    assert duplicate_shell.mounted == []


def test_48a_three_concrete_families_retain_exact_surface_contracts() -> None:
    assert first._FIRST_CHANGED_BASIS_ROOT_BACKED_HANDOFF == (
        kernel._ChangedBasisTypedHandoffSurfaceSpec(
            button_id="continue-first-changed-basis-root-backed-session",
            notice_id="research-first-changed-basis-root-backed-handoff-notice",
            notice_text=(
                "44G persistence is complete and the currently mounted governed session "
                "remains unchanged. Choose the explicit handoff below to leave that mounted "
                "state and continue with the exact freshly proven 35C root-backed session in "
                "the established root-backed product. This transfers typed in-memory proof; "
                "the saved overlay path is not reloaded or promoted to current/latest/head "
                "authority."
            ),
            button_label="Continue with verified changed-basis session",
            missing_result_error=(
                "44H handoff requires one exact successful retained 44G persistence result."
            ),
            invalid_handoff_error=(
                "44G checkpoint fresh re-entry must be a root-backed session re-entry result."
            ),
            duplicate_controls_error=(
                "44H handoff controls are already mounted after successful 44G persistence."
            ),
        )
    )
    assert second._SECOND_CHANGED_BASIS_EPOCH_HANDOFF.button_id == (
        "continue-second-changed-basis-epoch-session"
    )
    assert second._SECOND_CHANGED_BASIS_EPOCH_HANDOFF.notice_id == (
        "research-second-changed-basis-epoch-handoff-notice"
    )
    assert second._SECOND_CHANGED_BASIS_EPOCH_HANDOFF.button_label == (
        "Continue with verified second-basis-epoch session"
    )
    assert second._SECOND_CHANGED_BASIS_EPOCH_HANDOFF.invalid_handoff_error == (
        "46F checkpoint fresh re-entry must be exactly "
        "ChromiumResearchSecondBasisEpochReentryResult."
    )
    assert third._THIRD_CHANGED_BASIS_EPOCH_HANDOFF.button_id == (
        "continue-third-changed-basis-epoch-session"
    )
    assert third._THIRD_CHANGED_BASIS_EPOCH_HANDOFF.notice_id == (
        "research-third-changed-basis-epoch-handoff-notice"
    )
    assert third._THIRD_CHANGED_BASIS_EPOCH_HANDOFF.button_label == (
        "Continue with verified third-basis-epoch session"
    )
    assert third._THIRD_CHANGED_BASIS_EPOCH_HANDOFF.invalid_handoff_error == (
        "47F checkpoint fresh re-entry must be exactly "
        "ChromiumResearchThirdBasisEpochReentryResult."
    )

    assert first._mount_changed_basis_typed_handoff_after_new_persistence is (
        kernel._mount_changed_basis_typed_handoff_after_new_persistence
    )
    assert second._mount_changed_basis_typed_handoff_after_new_persistence is (
        kernel._mount_changed_basis_typed_handoff_after_new_persistence
    )
    assert third._mount_changed_basis_typed_handoff_after_new_persistence is (
        kernel._mount_changed_basis_typed_handoff_after_new_persistence
    )
    assert first._require_changed_basis_checkpoint_fresh_handoff is (
        kernel._require_changed_basis_checkpoint_fresh_handoff
    )
    assert second._require_changed_basis_checkpoint_fresh_handoff is (
        kernel._require_changed_basis_checkpoint_fresh_handoff
    )
    assert third._require_changed_basis_checkpoint_fresh_handoff is (
        kernel._require_changed_basis_checkpoint_fresh_handoff
    )
