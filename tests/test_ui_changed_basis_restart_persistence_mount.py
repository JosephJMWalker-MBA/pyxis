from __future__ import annotations

import pytest
from textual.widgets import Static

import pyxis.ui.chromium_research_changed_basis_restart_persistence_textual as kernel
import pyxis.ui.first_changed_basis_root_backed_reentry_overlay_research_session_shell as first
import pyxis.ui.second_changed_basis_epoch_reentry_overlay_research_session_shell as second
import pyxis.ui.third_changed_basis_epoch_reentry_overlay_research_session_shell as third


class _FakeShell:
    def __init__(self) -> None:
        self.existing_selectors: set[str] = set()
        self.mounted: list[object] = []

    def query(self, selector: str):
        return [object()] if selector in self.existing_selectors else []

    async def mount(self, widget) -> None:
        self.mounted.append(widget)


def _spec() -> kernel._ChangedBasisRestartPersistenceMountSpec:
    return kernel._ChangedBasisRestartPersistenceMountSpec(
        controls_selector="#test-restart-persistence-controls",
        duplicate_controls_error="duplicate exact persistence controls",
    )


def test_48c_private_mount_kernel_exports_no_public_authority_surface() -> None:
    assert kernel.__all__ == []


@pytest.mark.asyncio
async def test_48c_none_or_same_verification_mounts_nothing_and_skips_factory() -> None:
    shell = _FakeShell()
    calls = {"factory": 0}
    prior = object()

    def create_controls(value):
        calls["factory"] += 1
        raise AssertionError("no-new-verification path must not create controls")

    assert (
        await kernel._mount_changed_basis_restart_persistence_after_new_verification(
            shell,  # type: ignore[arg-type]
            previous_verification=prior,
            current_verification=None,
            spec=_spec(),
            create_controls=create_controls,
        )
        is None
    )
    assert (
        await kernel._mount_changed_basis_restart_persistence_after_new_verification(
            shell,  # type: ignore[arg-type]
            previous_verification=prior,
            current_verification=prior,
            spec=_spec(),
            create_controls=create_controls,
        )
        is None
    )
    assert calls["factory"] == 0
    assert shell.mounted == []


@pytest.mark.asyncio
async def test_48c_duplicate_controls_reject_before_new_controls_construction() -> None:
    shell = _FakeShell()
    spec = _spec()
    shell.existing_selectors.add(spec.controls_selector)
    calls = {"factory": 0}

    def create_controls(value):
        calls["factory"] += 1
        raise AssertionError("duplicate guard must fire before controls construction")

    with pytest.raises(ValueError, match="duplicate exact persistence controls"):
        await kernel._mount_changed_basis_restart_persistence_after_new_verification(
            shell,  # type: ignore[arg-type]
            previous_verification=object(),
            current_verification=object(),
            spec=spec,
            create_controls=create_controls,
        )

    assert calls["factory"] == 0
    assert shell.mounted == []


@pytest.mark.asyncio
async def test_48c_new_exact_verification_is_passed_to_and_mounts_exact_created_controls() -> None:
    shell = _FakeShell()
    verification = object()
    observed: dict[str, object] = {}
    controls = Static("exact controls")

    def create_controls(value):
        observed["verification"] = value
        return controls

    returned = await kernel._mount_changed_basis_restart_persistence_after_new_verification(
        shell,  # type: ignore[arg-type]
        previous_verification=object(),
        current_verification=verification,
        spec=_spec(),
        create_controls=create_controls,
    )

    assert observed["verification"] is verification
    assert returned is controls
    assert shell.mounted == [controls]
    assert shell.mounted[0] is controls


def test_48c_three_concrete_products_retain_specs_and_share_only_mount_procedure() -> None:
    assert (
        first._mount_changed_basis_restart_persistence_after_new_verification
        is kernel._mount_changed_basis_restart_persistence_after_new_verification
    )
    assert (
        second._mount_changed_basis_restart_persistence_after_new_verification
        is kernel._mount_changed_basis_restart_persistence_after_new_verification
    )
    assert (
        third._mount_changed_basis_restart_persistence_after_new_verification
        is kernel._mount_changed_basis_restart_persistence_after_new_verification
    )

    assert first._FIRST_CHANGED_BASIS_ROOT_BACKED_RESTART_PERSISTENCE_MOUNT == (
        kernel._ChangedBasisRestartPersistenceMountSpec(
            controls_selector=(
                "#research-first-changed-basis-root-backed-reentry-overlay-controls"
            ),
            duplicate_controls_error=(
                "44G overlay persistence controls are already mounted."
            ),
        )
    )
    assert second._SECOND_CHANGED_BASIS_EPOCH_RESTART_PERSISTENCE_MOUNT == (
        kernel._ChangedBasisRestartPersistenceMountSpec(
            controls_selector=(
                "#research-second-changed-basis-epoch-reentry-overlay-controls"
            ),
            duplicate_controls_error=(
                "Second-basis re-entry overlay controls are already mounted."
            ),
        )
    )
    assert third._THIRD_CHANGED_BASIS_EPOCH_RESTART_PERSISTENCE_MOUNT == (
        kernel._ChangedBasisRestartPersistenceMountSpec(
            controls_selector=(
                "#research-third-changed-basis-epoch-reentry-overlay-controls"
            ),
            duplicate_controls_error=(
                "Third-basis re-entry overlay controls are already mounted."
            ),
        )
    )
