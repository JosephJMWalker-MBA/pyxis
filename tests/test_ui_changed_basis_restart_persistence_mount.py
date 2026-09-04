from __future__ import annotations

from pathlib import Path

import pytest
from textual.widgets import Static

import pyxis.ui.chromium_research_changed_basis_restart_persistence_textual as kernel
import pyxis.ui.first_changed_basis_root_backed_reentry_overlay_research_session_shell as first
import pyxis.ui.second_changed_basis_epoch_reentry_overlay_research_session_shell as second
import pyxis.ui.third_changed_basis_epoch_reentry_overlay_research_session_shell as third


class _FakeInput:
    def __init__(self, value: str) -> None:
        self.value = value


class _FakeStatus:
    def __init__(self) -> None:
        self.value = ""

    def update(self, value: str) -> None:
        self.value = value


class _FakeShell:
    def __init__(self) -> None:
        self.existing_selectors: set[str] = set()
        self.mounted: list[object] = []
        self.inputs: dict[str, _FakeInput] = {}

    def query(self, selector: str):
        return [object()] if selector in self.existing_selectors else []

    def query_one(self, selector: str, widget_type):
        return self.inputs[selector]

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


def _path_spec() -> kernel._ChangedBasisRestartPersistencePathSpec:
    return kernel._ChangedBasisRestartPersistencePathSpec(
        source_selector="#test-restart-source",
        destination_selector="#test-restart-destination",
        missing_source_error="missing exact restart source",
        missing_destination_error="missing exact restart destination",
    )


def test_48d_blank_source_fails_before_destination() -> None:
    shell = _FakeShell()
    spec = _path_spec()
    shell.inputs[spec.source_selector] = _FakeInput("   ")
    shell.inputs[spec.destination_selector] = _FakeInput("")
    status = _FakeStatus()

    result = kernel._collect_changed_basis_restart_persistence_path_submission(
        shell,  # type: ignore[arg-type]
        status=status,  # type: ignore[arg-type]
        spec=spec,
    )

    assert result is None
    assert status.value == "missing exact restart source"


def test_48d_blank_destination_fails_only_after_nonblank_source() -> None:
    shell = _FakeShell()
    spec = _path_spec()
    shell.inputs[spec.source_selector] = _FakeInput("source.json")
    shell.inputs[spec.destination_selector] = _FakeInput("\t  ")
    status = _FakeStatus()

    result = kernel._collect_changed_basis_restart_persistence_path_submission(
        shell,  # type: ignore[arg-type]
        status=status,  # type: ignore[arg-type]
        spec=spec,
    )

    assert result is None
    assert status.value == "missing exact restart destination"


def test_48d_success_uses_exact_unstripped_path_strings() -> None:
    shell = _FakeShell()
    spec = _path_spec()
    source_value = "  explicit/source.json  "
    destination_value = "  explicit/destination.json  "
    shell.inputs[spec.source_selector] = _FakeInput(source_value)
    shell.inputs[spec.destination_selector] = _FakeInput(destination_value)
    status = _FakeStatus()

    result = kernel._collect_changed_basis_restart_persistence_path_submission(
        shell,  # type: ignore[arg-type]
        status=status,  # type: ignore[arg-type]
        spec=spec,
    )

    assert result is not None
    assert result.source == Path(source_value)
    assert result.destination == Path(destination_value)
    assert str(result.source) == source_value
    assert str(result.destination) == destination_value
    assert status.value == ""


def test_48d_three_concrete_products_retain_exact_path_specs_and_shared_collector() -> None:
    assert (
        first._collect_changed_basis_restart_persistence_path_submission
        is kernel._collect_changed_basis_restart_persistence_path_submission
    )
    assert (
        second._collect_changed_basis_restart_persistence_path_submission
        is kernel._collect_changed_basis_restart_persistence_path_submission
    )
    assert (
        third._collect_changed_basis_restart_persistence_path_submission
        is kernel._collect_changed_basis_restart_persistence_path_submission
    )

    assert first._FIRST_CHANGED_BASIS_ROOT_BACKED_RESTART_PERSISTENCE_PATHS == (
        kernel._ChangedBasisRestartPersistencePathSpec(
            source_selector=(
                "#research-first-changed-basis-root-backed-reentry-overlay-prior-plan-source"
            ),
            destination_selector=(
                "#research-first-changed-basis-root-backed-reentry-overlay-destination"
            ),
            missing_source_error=(
                "Overlay persistence failed: explicit ordinary 31B plan-document path is required."
            ),
            missing_destination_error=(
                "Overlay persistence failed: explicit no-overwrite 35C overlay destination is required."
            ),
        )
    )
    assert second._SECOND_CHANGED_BASIS_EPOCH_RESTART_PERSISTENCE_PATHS == (
        kernel._ChangedBasisRestartPersistencePathSpec(
            source_selector=(
                "#research-second-changed-basis-epoch-reentry-overlay-prior-continuation-overlay-source"
            ),
            destination_selector=(
                "#research-second-changed-basis-epoch-reentry-overlay-destination"
            ),
            missing_source_error=(
                "Overlay persistence failed: explicit current prior 35D/35E continuation-overlay path is required."
            ),
            missing_destination_error=(
                "Overlay persistence failed: explicit no-overwrite 37B destination is required."
            ),
        )
    )
    assert third._THIRD_CHANGED_BASIS_EPOCH_RESTART_PERSISTENCE_PATHS == (
        kernel._ChangedBasisRestartPersistencePathSpec(
            source_selector=(
                "#research-third-changed-basis-epoch-reentry-overlay-prior-continuation-overlay-source"
            ),
            destination_selector=(
                "#research-third-changed-basis-epoch-reentry-overlay-destination"
            ),
            missing_source_error=(
                "Overlay persistence failed: explicit current prior 37C/37D second-epoch continuation-overlay path is required."
            ),
            missing_destination_error=(
                "Overlay persistence failed: explicit no-overwrite 40B destination is required."
            ),
        )
    )
