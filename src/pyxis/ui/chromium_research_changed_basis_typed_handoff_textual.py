from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from textual.widgets import Button, Static

from .research_session_shell import ResearchSessionShell


@dataclass(frozen=True, slots=True)
class _ChangedBasisTypedHandoffSurfaceSpec:
    """Concrete visible details for one already-earned changed-basis handoff."""

    button_id: str
    notice_id: str
    notice_text: str
    button_label: str
    missing_result_error: str
    invalid_handoff_error: str
    duplicate_controls_error: str


def _require_changed_basis_checkpoint_fresh_handoff(
    persistence_result: Any,
    *,
    spec: _ChangedBasisTypedHandoffSurfaceSpec,
    validate_handoff: Callable[[Any], bool],
) -> Any:
    """Return the exact checkpoint fresh re-entry after concrete-family validation.

    The helper knows only the now-triply-proven product shape that 44G/46F/47F
    persistence results retain one checkpoint whose mandatory fresh reconstruction is
    the explicit in-process handoff subject. The concrete caller still owns the
    persistence-result attribute, result type, validator semantics, receiver product,
    and exit action.
    """

    if persistence_result is None:
        raise ValueError(spec.missing_result_error)

    handoff = persistence_result.checkpoint.fresh_reentry
    if not validate_handoff(handoff):
        raise TypeError(spec.invalid_handoff_error)
    return handoff


async def _mount_changed_basis_typed_handoff_after_new_persistence(
    shell: ResearchSessionShell,
    *,
    previous_result: Any,
    current_result: Any,
    spec: _ChangedBasisTypedHandoffSurfaceSpec,
    validate_handoff: Callable[[Any], bool],
) -> Any | None:
    """Mount one explicit handoff only after a newly retained concrete persistence.

    This private procedure owns only repeated Textual mechanics. It performs no
    persistence, reconstruction, path lookup, ancestry interpretation, receiver
    selection, or mode promotion.
    """

    if current_result is None or current_result is previous_result:
        return None

    handoff = _require_changed_basis_checkpoint_fresh_handoff(
        current_result,
        spec=spec,
        validate_handoff=validate_handoff,
    )
    if len(shell.query(f"#{spec.notice_id}")) != 0:
        raise ValueError(spec.duplicate_controls_error)

    await shell.mount(
        Static(
            spec.notice_text,
            id=spec.notice_id,
            markup=False,
        )
    )
    await shell.mount(
        Button(
            spec.button_label,
            id=spec.button_id,
            variant="primary",
        )
    )
    return handoff


__all__: list[str] = []
