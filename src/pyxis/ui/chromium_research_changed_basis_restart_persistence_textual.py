from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from textual.widget import Widget
from textual.widgets import Input, Static

from .research_session_shell import ResearchSessionShell


@dataclass(frozen=True, slots=True)
class _ChangedBasisRestartPersistenceMountSpec:
    """Concrete surface details for one proof-gated restart-persistence form."""

    controls_selector: str
    duplicate_controls_error: str


@dataclass(frozen=True, slots=True)
class _ChangedBasisRestartPersistencePathSpec:
    """Concrete selectors and blank-error wording for two explicit path inputs."""

    source_selector: str
    destination_selector: str
    missing_source_error: str
    missing_destination_error: str


@dataclass(frozen=True, slots=True)
class _ChangedBasisRestartPersistencePathSubmission:
    """Exact caller-entered restart-persistence paths after ordered blank checks."""

    source: Path
    destination: Path


def _collect_changed_basis_restart_persistence_path_submission(
    shell: ResearchSessionShell,
    *,
    status: Static,
    spec: _ChangedBasisRestartPersistencePathSpec,
) -> _ChangedBasisRestartPersistencePathSubmission | None:
    """Read two explicit path fields without granting path-discovery authority.

    str.strip is used only to decide whether a field is blank. Successful conversion
    preserves the exact original entered string in Path(...) rather than normalizing
    or substituting the stripped value.
    """

    source = shell.query_one(spec.source_selector, Input)
    destination = shell.query_one(spec.destination_selector, Input)

    if not source.value.strip():
        status.update(spec.missing_source_error)
        return None
    if not destination.value.strip():
        status.update(spec.missing_destination_error)
        return None

    return _ChangedBasisRestartPersistencePathSubmission(
        source=Path(source.value),
        destination=Path(destination.value),
    )


async def _mount_changed_basis_restart_persistence_after_new_verification(
    shell: ResearchSessionShell,
    *,
    previous_verification: Any,
    current_verification: Any,
    spec: _ChangedBasisRestartPersistenceMountSpec,
    create_controls: Callable[[Any], Widget],
) -> Widget | None:
    """Mount concrete persistence controls only for one newly retained exact proof.

    This private helper owns only the now-triply-proven 44G/46F/47F Textual mount
    mechanics. Concrete callers still own verification execution and typing,
    persistence semantics, control classes, selectors, wording, ancestry, and paths.
    """

    if current_verification is None or current_verification is previous_verification:
        return None

    if len(shell.query(spec.controls_selector)) != 0:
        raise ValueError(spec.duplicate_controls_error)

    controls = create_controls(current_verification)
    await shell.mount(controls)
    return controls


__all__: list[str] = []
