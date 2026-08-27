from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .chromium_research_third_basis_epoch_continuation_reentry_plan_document import (
    ChromiumResearchThirdBasisEpochContinuationReentryResult,
    load_chromium_research_third_basis_epoch_continuation_reentry_plan_document,
    reenter_chromium_research_third_basis_epoch_continuation,
)
from .chromium_research_third_basis_epoch_reentry import (
    ChromiumResearchThirdBasisEpochReentryResult,
    reenter_chromium_research_third_basis_epoch,
)
from .chromium_research_third_basis_epoch_reentry_plan_document import (
    load_chromium_research_third_basis_epoch_reentry_plan_document,
)


@dataclass(frozen=True, slots=True)
class ChromiumResearchThirdBasisEpochShellLineage:
    """One explicit 40B location bound to the fresh re-entry proven from it.

    `overlay_source` is operational location context only. `reentry` is the fresh
    three-root result reconstructed from that exact explicit source during proof, not
    the arbitrary caller-supplied object.
    """

    overlay_source: Path
    reentry: ChromiumResearchThirdBasisEpochReentryResult


@dataclass(frozen=True, slots=True)
class ChromiumResearchThirdBasisEpochContinuationShellLineage:
    """One explicit 40C/40D location bound to its freshly proven continuation."""

    overlay_source: Path
    reentry: ChromiumResearchThirdBasisEpochContinuationReentryResult


class ChromiumResearchThirdBasisEpochShellLineageError(ValueError):
    """Raised when an explicit third-epoch launch location cannot prove the earned lineage."""


def prove_chromium_research_third_basis_epoch_shell_lineage(
    earned: ChromiumResearchThirdBasisEpochReentryResult,
    *,
    overlay_source: Path,
) -> ChromiumResearchThirdBasisEpochShellLineage:
    """Bind one explicit 40B path to a fresh matching three-root reconstruction.

    The exact supplied path is strictly decoded and freshly re-entered. The fresh
    result must match the already-earned result across retained second-epoch
    continuation state, first-/second-/third-root durable identities, third-epoch
    presentation, and terminal endpoint identity.

    No persistence write, discovery, path inference, format autodetection, chronology,
    branch semantics, or latest/current/head selection occurs.
    """

    if not isinstance(earned, ChromiumResearchThirdBasisEpochReentryResult):
        raise TypeError("earned must be ChromiumResearchThirdBasisEpochReentryResult.")
    source = _require_path(overlay_source, label="overlay_source").resolve()

    try:
        plan = load_chromium_research_third_basis_epoch_reentry_plan_document(source)
        fresh = reenter_chromium_research_third_basis_epoch(plan)
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchThirdBasisEpochShellLineageError(
            "Explicit 40B overlay could not freshly reconstruct a third-basis-epoch session."
        ) from exc

    _require_third_epoch_match(earned, fresh)
    return ChromiumResearchThirdBasisEpochShellLineage(
        overlay_source=source,
        reentry=fresh,
    )


def prove_chromium_research_third_basis_epoch_continuation_shell_lineage(
    earned: ChromiumResearchThirdBasisEpochContinuationReentryResult,
    *,
    overlay_source: Path,
) -> ChromiumResearchThirdBasisEpochContinuationShellLineage:
    """Bind one explicit 40C/40D path to a fresh matching continuation reconstruction.

    The current continuation and all nested three-root ancestry must match the earned
    result. The returned wrapper retains the fresh continuation reconstructed from the
    explicit source rather than the caller-supplied object.
    """

    if not isinstance(
        earned,
        ChromiumResearchThirdBasisEpochContinuationReentryResult,
    ):
        raise TypeError(
            "earned must be ChromiumResearchThirdBasisEpochContinuationReentryResult."
        )
    source = _require_path(overlay_source, label="overlay_source").resolve()

    try:
        plan = (
            load_chromium_research_third_basis_epoch_continuation_reentry_plan_document(
                source
            )
        )
        fresh = reenter_chromium_research_third_basis_epoch_continuation(plan)
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchThirdBasisEpochShellLineageError(
            "Explicit 40C/40D overlay could not freshly reconstruct a third-basis-epoch continuation."
        ) from exc

    if fresh.controller.presentation != earned.controller.presentation:
        raise ChromiumResearchThirdBasisEpochShellLineageError(
            "Fresh continuation presentation does not match the earned continuation."
        )
    if (
        fresh.controller.declared_endpoint.verification.edge_record_sha256
        != earned.controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchThirdBasisEpochShellLineageError(
            "Fresh continuation endpoint identity does not match the earned continuation."
        )
    _require_third_epoch_match(
        earned.prior_third_basis_epoch_reentry,
        fresh.prior_third_basis_epoch_reentry,
    )

    return ChromiumResearchThirdBasisEpochContinuationShellLineage(
        overlay_source=source,
        reentry=fresh,
    )


def _require_third_epoch_match(
    earned: ChromiumResearchThirdBasisEpochReentryResult,
    fresh: ChromiumResearchThirdBasisEpochReentryResult,
) -> None:
    earned_prior = earned.prior_second_basis_epoch_continuation_reentry
    fresh_prior = fresh.prior_second_basis_epoch_continuation_reentry

    if fresh_prior.controller.presentation != earned_prior.controller.presentation:
        raise ChromiumResearchThirdBasisEpochShellLineageError(
            "Fresh retained second-epoch continuation presentation does not match the earned ancestry."
        )
    if (
        fresh_prior.controller.declared_endpoint.verification.edge_record_sha256
        != earned_prior.controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchThirdBasisEpochShellLineageError(
            "Fresh retained second-epoch continuation endpoint identity does not match the earned ancestry."
        )

    earned_second = earned_prior.prior_second_basis_epoch_reentry
    fresh_second = fresh_prior.prior_second_basis_epoch_reentry
    earned_first_root = (
        earned_second.prior_continuation_reentry.prior_root_backed_reentry.loaded_root
    )
    fresh_first_root = (
        fresh_second.prior_continuation_reentry.prior_root_backed_reentry.loaded_root
    )

    if (
        fresh_first_root.verification.root_record_sha256
        != earned_first_root.verification.root_record_sha256
    ):
        raise ChromiumResearchThirdBasisEpochShellLineageError(
            "Fresh retained first-root identity does not match the earned ancestry."
        )
    if (
        fresh_second.loaded_root.verification.root_record_sha256
        != earned_second.loaded_root.verification.root_record_sha256
    ):
        raise ChromiumResearchThirdBasisEpochShellLineageError(
            "Fresh retained second-root identity does not match the earned ancestry."
        )
    if (
        fresh.loaded_root.verification.root_record_sha256
        != earned.loaded_root.verification.root_record_sha256
    ):
        raise ChromiumResearchThirdBasisEpochShellLineageError(
            "Fresh third-root identity does not match the earned third epoch."
        )
    if fresh.controller.presentation != earned.controller.presentation:
        raise ChromiumResearchThirdBasisEpochShellLineageError(
            "Fresh third-epoch presentation does not match the earned session."
        )
    if (
        fresh.controller.declared_endpoint.verification.edge_record_sha256
        != earned.controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchThirdBasisEpochShellLineageError(
            "Fresh third-epoch endpoint identity does not match the earned session."
        )


def _require_path(value: Path, *, label: str) -> Path:
    if not isinstance(value, Path):
        raise TypeError(f"{label} must be pathlib.Path.")
    return value


__all__ = [
    "ChromiumResearchThirdBasisEpochContinuationShellLineage",
    "ChromiumResearchThirdBasisEpochShellLineage",
    "ChromiumResearchThirdBasisEpochShellLineageError",
    "prove_chromium_research_third_basis_epoch_continuation_shell_lineage",
    "prove_chromium_research_third_basis_epoch_shell_lineage",
]
