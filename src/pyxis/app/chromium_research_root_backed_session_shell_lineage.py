from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .chromium_research_root_backed_session_continuation_reentry_plan_document import (
    ChromiumResearchRootBackedSessionContinuationReentryResult,
    load_chromium_research_root_backed_session_continuation_reentry_plan_document,
    reenter_chromium_research_root_backed_session_continuation,
)
from .chromium_research_root_backed_session_reentry import (
    ChromiumResearchRootBackedSessionReentryResult,
    reenter_chromium_research_root_backed_session,
)
from .chromium_research_root_backed_session_reentry_plan_document import (
    load_chromium_research_root_backed_session_reentry_plan_document,
)


@dataclass(frozen=True, slots=True)
class ChromiumResearchRootBackedSessionShellLineage:
    """One explicit 35C location bound to the fresh re-entry proven from it.

    `overlay_source` is launch location context only. `reentry` is a new root-backed
    reconstruction earned from that explicit source during proof, not the arbitrary
    caller-supplied object used as the comparison subject.
    """

    overlay_source: Path
    reentry: ChromiumResearchRootBackedSessionReentryResult


@dataclass(frozen=True, slots=True)
class ChromiumResearchRootBackedSessionContinuationShellLineage:
    """One explicit 35D/35E location bound to its freshly proven continuation."""

    overlay_source: Path
    reentry: ChromiumResearchRootBackedSessionContinuationReentryResult


class ChromiumResearchRootBackedSessionShellLineageError(ValueError):
    """Raised when an explicit one-root launch path cannot prove the earned lineage."""


def prove_chromium_research_root_backed_session_shell_lineage(
    earned: ChromiumResearchRootBackedSessionReentryResult,
    *,
    overlay_source: Path,
) -> ChromiumResearchRootBackedSessionShellLineage:
    """Bind one explicit 35C path to a fresh matching root-backed reconstruction.

    Path equality is not authority. The supplied overlay is strictly decoded and
    freshly re-entered, then compared with the already-earned result by governed
    presentation, terminal durable edge identity, and retained 34A root identity.

    No persistence, discovery, path inference, chronology, or latest/current/head
    selection occurs.
    """

    if not isinstance(earned, ChromiumResearchRootBackedSessionReentryResult):
        raise TypeError(
            "earned must be ChromiumResearchRootBackedSessionReentryResult."
        )
    source = _require_path(overlay_source, label="overlay_source").resolve()

    try:
        plan = load_chromium_research_root_backed_session_reentry_plan_document(source)
        fresh = reenter_chromium_research_root_backed_session(plan)
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchRootBackedSessionShellLineageError(
            "Explicit 35C overlay could not freshly reconstruct a root-backed session."
        ) from exc

    _require_root_backed_match(earned, fresh)
    return ChromiumResearchRootBackedSessionShellLineage(
        overlay_source=source,
        reentry=fresh,
    )


def prove_chromium_research_root_backed_session_continuation_shell_lineage(
    earned: ChromiumResearchRootBackedSessionContinuationReentryResult,
    *,
    overlay_source: Path,
) -> ChromiumResearchRootBackedSessionContinuationShellLineage:
    """Bind one explicit 35D/35E path to a fresh matching continuation reconstruction."""

    if not isinstance(
        earned,
        ChromiumResearchRootBackedSessionContinuationReentryResult,
    ):
        raise TypeError(
            "earned must be ChromiumResearchRootBackedSessionContinuationReentryResult."
        )
    source = _require_path(overlay_source, label="overlay_source").resolve()

    try:
        plan = load_chromium_research_root_backed_session_continuation_reentry_plan_document(
            source
        )
        fresh = reenter_chromium_research_root_backed_session_continuation(plan)
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchRootBackedSessionShellLineageError(
            "Explicit 35D/35E overlay could not freshly reconstruct a root-backed continuation."
        ) from exc

    if fresh.controller.presentation != earned.controller.presentation:
        raise ChromiumResearchRootBackedSessionShellLineageError(
            "Fresh continuation presentation does not match the earned continuation."
        )
    if (
        fresh.controller.declared_endpoint.verification.edge_record_sha256
        != earned.controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchRootBackedSessionShellLineageError(
            "Fresh continuation endpoint identity does not match the earned continuation."
        )
    _require_root_backed_match(
        earned.prior_root_backed_reentry,
        fresh.prior_root_backed_reentry,
    )

    return ChromiumResearchRootBackedSessionContinuationShellLineage(
        overlay_source=source,
        reentry=fresh,
    )


def _require_root_backed_match(
    earned: ChromiumResearchRootBackedSessionReentryResult,
    fresh: ChromiumResearchRootBackedSessionReentryResult,
) -> None:
    if fresh.controller.presentation != earned.controller.presentation:
        raise ChromiumResearchRootBackedSessionShellLineageError(
            "Fresh root-backed presentation does not match the earned session."
        )
    if (
        fresh.controller.declared_endpoint.verification.edge_record_sha256
        != earned.controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchRootBackedSessionShellLineageError(
            "Fresh root-backed endpoint identity does not match the earned session."
        )
    if (
        fresh.loaded_root.verification.root_record_sha256
        != earned.loaded_root.verification.root_record_sha256
    ):
        raise ChromiumResearchRootBackedSessionShellLineageError(
            "Fresh root identity does not match the earned root-backed session."
        )


def _require_path(value: Path, *, label: str) -> Path:
    if not isinstance(value, Path):
        raise TypeError(f"{label} must be pathlib.Path.")
    return value


__all__ = [
    "ChromiumResearchRootBackedSessionContinuationShellLineage",
    "ChromiumResearchRootBackedSessionShellLineage",
    "ChromiumResearchRootBackedSessionShellLineageError",
    "prove_chromium_research_root_backed_session_continuation_shell_lineage",
    "prove_chromium_research_root_backed_session_shell_lineage",
]
