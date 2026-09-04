from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from textual.widget import Widget

from .research_session_shell import ResearchSessionShell


@dataclass(frozen=True, slots=True)
class _ChangedBasisRestartPersistenceMountSpec:
    """Concrete surface details for one proof-gated restart-persistence form."""

    controls_selector: str
    duplicate_controls_error: str


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
