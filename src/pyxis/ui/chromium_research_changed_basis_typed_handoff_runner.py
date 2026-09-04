from __future__ import annotations

from collections.abc import Callable
from typing import Any


def _run_changed_basis_typed_handoff(
    *,
    run_source: Callable[[], Any],
    validate_handoff: Callable[[Any], bool],
    invalid_handoff_error: str,
    create_receiver: Callable[[Any], Any],
) -> Any | None:
    """Run one already-earned concrete changed-basis typed handoff.

    This private helper owns only the now-triply-proven runner procedure shared by
    44H, 46G, and 47G. Concrete callers still own source construction, source
    arguments, type semantics, error wording, receiver selection, public return
    annotation, and all ancestry/persistence meaning.
    """

    handoff = run_source()
    if handoff is None:
        return None

    if not validate_handoff(handoff):
        raise TypeError(invalid_handoff_error)

    receiver = create_receiver(handoff)
    receiver.run()
    return handoff


__all__: list[str] = []
