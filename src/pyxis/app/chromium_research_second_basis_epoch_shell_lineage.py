from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .chromium_research_second_basis_epoch_continuation_reentry_plan_document import (
    ChromiumResearchSecondBasisEpochContinuationReentryResult,
    load_chromium_research_second_basis_epoch_continuation_reentry_plan_document,
    reenter_chromium_research_second_basis_epoch_continuation,
)
from .chromium_research_second_basis_epoch_reentry import (
    ChromiumResearchSecondBasisEpochReentryResult,
    reenter_chromium_research_second_basis_epoch,
)
from .chromium_research_second_basis_epoch_reentry_plan_document import (
    load_chromium_research_second_basis_epoch_reentry_plan_document,
)


@dataclass(frozen=True, slots=True)
class ChromiumResearchSecondBasisEpochShellLineage:
    """One explicit 37B location bound to the fresh re-entry proven from that location.

    The source is operational location context only. `reentry` is not the arbitrary
    caller-supplied object: it is the new 37A result reconstructed from `overlay_source`
    during proof and shown to represent the same earned second-epoch authority.
    """

    overlay_source: Path
    reentry: ChromiumResearchSecondBasisEpochReentryResult


@dataclass(frozen=True, slots=True)
class ChromiumResearchSecondBasisEpochContinuationShellLineage:
    """One explicit 37C/37D location bound to its freshly proven continuation re-entry."""

    overlay_source: Path
    reentry: ChromiumResearchSecondBasisEpochContinuationReentryResult


class ChromiumResearchSecondBasisEpochShellLineageError(ValueError):
    """Raised when an explicit second-epoch launch path cannot prove the earned lineage."""


def prove_chromium_research_second_basis_epoch_shell_lineage(
    earned: ChromiumResearchSecondBasisEpochReentryResult,
    *,
    overlay_source: Path,
) -> ChromiumResearchSecondBasisEpochShellLineage:
    """Bind one explicit 37B path to a fresh matching second-epoch reconstruction.

    Path equality is not authority. The explicit source is strictly decoded and
    freshly re-entered, then compared with the already-earned result by retained prior
    continuation presentation/endpoint, retained first-root identity, second-root
    identity, current presentation, and current terminal edge identity.

    No persistence write, discovery, path inference, format autodetection, chronology,
    or latest/current/head selection occurs.
    """

    if not isinstance(earned, ChromiumResearchSecondBasisEpochReentryResult):
        raise TypeError(
            "earned must be ChromiumResearchSecondBasisEpochReentryResult."
        )
    source = _require_path(overlay_source, label="overlay_source").resolve()

    try:
        plan = load_chromium_research_second_basis_epoch_reentry_plan_document(source)
        fresh = reenter_chromium_research_second_basis_epoch(plan)
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchSecondBasisEpochShellLineageError(
            "Explicit 37B overlay could not freshly reconstruct a second-basis-epoch session."
        ) from exc

    _require_second_epoch_match(earned, fresh)
    return ChromiumResearchSecondBasisEpochShellLineage(
        overlay_source=source,
        reentry=fresh,
    )


def prove_chromium_research_second_basis_epoch_continuation_shell_lineage(
    earned: ChromiumResearchSecondBasisEpochContinuationReentryResult,
    *,
    overlay_source: Path,
) -> ChromiumResearchSecondBasisEpochContinuationShellLineage:
    """Bind one explicit 37C/37D path to a fresh matching continuation reconstruction.

    The current continuation and its nested second-epoch ancestry must all match the
    earned result. The returned wrapper retains the fresh continuation reconstructed
    from the explicit source rather than the caller-supplied object.
    """

    if not isinstance(
        earned,
        ChromiumResearchSecondBasisEpochContinuationReentryResult,
    ):
        raise TypeError(
            "earned must be ChromiumResearchSecondBasisEpochContinuationReentryResult."
        )
    source = _require_path(overlay_source, label="overlay_source").resolve()

    try:
        plan = load_chromium_research_second_basis_epoch_continuation_reentry_plan_document(
            source
        )
        fresh = reenter_chromium_research_second_basis_epoch_continuation(plan)
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchSecondBasisEpochShellLineageError(
            "Explicit 37C/37D overlay could not freshly reconstruct a second-basis-epoch continuation."
        ) from exc

    if fresh.controller.presentation != earned.controller.presentation:
        raise ChromiumResearchSecondBasisEpochShellLineageError(
            "Fresh continuation presentation does not match the earned continuation."
        )
    if (
        fresh.controller.declared_endpoint.verification.edge_record_sha256
        != earned.controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchSecondBasisEpochShellLineageError(
            "Fresh continuation endpoint identity does not match the earned continuation."
        )
    _require_second_epoch_match(
        earned.prior_second_basis_epoch_reentry,
        fresh.prior_second_basis_epoch_reentry,
    )

    return ChromiumResearchSecondBasisEpochContinuationShellLineage(
        overlay_source=source,
        reentry=fresh,
    )


def _require_second_epoch_match(
    earned: ChromiumResearchSecondBasisEpochReentryResult,
    fresh: ChromiumResearchSecondBasisEpochReentryResult,
) -> None:
    earned_prior = earned.prior_continuation_reentry
    fresh_prior = fresh.prior_continuation_reentry

    if fresh_prior.controller.presentation != earned_prior.controller.presentation:
        raise ChromiumResearchSecondBasisEpochShellLineageError(
            "Fresh retained prior continuation presentation does not match the earned ancestry."
        )
    if (
        fresh_prior.controller.declared_endpoint.verification.edge_record_sha256
        != earned_prior.controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchSecondBasisEpochShellLineageError(
            "Fresh retained prior continuation endpoint identity does not match the earned ancestry."
        )
    if (
        fresh_prior.prior_root_backed_reentry.loaded_root.verification.root_record_sha256
        != earned_prior.prior_root_backed_reentry.loaded_root.verification.root_record_sha256
    ):
        raise ChromiumResearchSecondBasisEpochShellLineageError(
            "Fresh retained first-root identity does not match the earned ancestry."
        )
    if (
        fresh.loaded_root.verification.root_record_sha256
        != earned.loaded_root.verification.root_record_sha256
    ):
        raise ChromiumResearchSecondBasisEpochShellLineageError(
            "Fresh second-root identity does not match the earned second epoch."
        )
    if fresh.controller.presentation != earned.controller.presentation:
        raise ChromiumResearchSecondBasisEpochShellLineageError(
            "Fresh second-epoch presentation does not match the earned session."
        )
    if (
        fresh.controller.declared_endpoint.verification.edge_record_sha256
        != earned.controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchSecondBasisEpochShellLineageError(
            "Fresh second-epoch endpoint identity does not match the earned session."
        )


def _require_path(value: Path, *, label: str) -> Path:
    if not isinstance(value, Path):
        raise TypeError(f"{label} must be pathlib.Path.")
    return value


__all__ = [
    "ChromiumResearchSecondBasisEpochContinuationShellLineage",
    "ChromiumResearchSecondBasisEpochShellLineage",
    "ChromiumResearchSecondBasisEpochShellLineageError",
    "prove_chromium_research_second_basis_epoch_continuation_shell_lineage",
    "prove_chromium_research_second_basis_epoch_shell_lineage",
]
