from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

from .chromium_research_session_controller import ChromiumResearchSessionController
from .chromium_research_session_reentry_plan_document import (
    _decode_path,
    _decode_path_array,
    _encode_path,
)
from .chromium_research_session_rollover import ChromiumResearchSessionRolloverResult
from .chromium_research_third_basis_epoch_reentry import (
    ChromiumResearchThirdBasisEpochReentryResult,
    reenter_chromium_research_third_basis_epoch,
)
from .chromium_research_third_basis_epoch_reentry_plan_document import (
    load_chromium_research_third_basis_epoch_reentry_plan_document,
)
from .chromium_research_working_set_note_revision_edge_sequence_declaration_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceDeclarationRecord,
    load_chromium_research_working_set_note_revision_edge_sequence_declaration,
)


_OVERLAY_FORMAT = (
    "pyxis.chromium.research_third_basis_epoch_continuation_locator_overlay.v1"
)
_ROOT_KEYS = {
    "format",
    "prior_third_basis_epoch_overlay_source",
    "declared_edge_sources",
    "declaration_source",
}


@dataclass(frozen=True, slots=True)
class ChromiumResearchThirdBasisEpochContinuationReentryPlan:
    """Locator-only plan for one ordinary continuation after a persisted 40B epoch.

    The plan retains only the explicit prior 40B overlay location and the explicit
    ordinary continuation declaration locations. It does not duplicate or flatten
    any of the three basis-change roots. Fresh re-entry must decode the 40B overlay
    and independently re-earn all three ancestry layers before the continuation can
    be reconciled.
    """

    prior_third_basis_epoch_overlay_source: Path
    declared_edge_sources: tuple[Path, ...]
    declaration_source: Path


@dataclass(frozen=True, slots=True)
class ChromiumResearchThirdBasisEpochContinuationReentryResult:
    """One fresh ordinary continuation above freshly reconstructed three-root ancestry."""

    plan: ChromiumResearchThirdBasisEpochContinuationReentryPlan
    prior_third_basis_epoch_reentry: ChromiumResearchThirdBasisEpochReentryResult
    loaded_declaration: ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceDeclarationRecord
    controller: ChromiumResearchSessionController


@dataclass(frozen=True, slots=True)
class ChromiumResearchThirdBasisEpochContinuationOverlayPersistenceResult:
    """One no-overwrite durable 40C locator overlay."""

    plan: ChromiumResearchThirdBasisEpochContinuationReentryPlan
    path: Path


@dataclass(frozen=True, slots=True)
class ChromiumResearchThirdBasisEpochContinuationCheckpointResult:
    """One chosen continuation proven restartable above persisted three-root ancestry."""

    prior_reentry: ChromiumResearchThirdBasisEpochReentryResult
    rollover: ChromiumResearchSessionRolloverResult
    plan: ChromiumResearchThirdBasisEpochContinuationReentryPlan
    fresh_reentry: ChromiumResearchThirdBasisEpochContinuationReentryResult
    persistence: ChromiumResearchThirdBasisEpochContinuationOverlayPersistenceResult


class ChromiumResearchThirdBasisEpochContinuationReentryError(ValueError):
    """Raised when one explicit 40C continuation cannot be freshly reconstructed."""


class ChromiumResearchThirdBasisEpochContinuationPlanDocumentError(ValueError):
    """Raised when one 40C continuation overlay is malformed or cannot be written."""


class ChromiumResearchThirdBasisEpochContinuationCheckpointError(ValueError):
    """Raised when one chosen continuation cannot be proven before 40C checkpointing."""


def load_chromium_research_third_basis_epoch_continuation_reentry_plan_document(
    source: Path,
) -> ChromiumResearchThirdBasisEpochContinuationReentryPlan:
    """Decode one strict locator-only 40C continuation overlay.

    Loading is configuration-only. It reads only this document and does not open the
    referenced 40B overlay or any research evidence. Successful decoding therefore
    proves only configuration shape, never ancestry, evidence integrity, restartability,
    or governed-session coherence.
    """

    if not isinstance(source, Path):
        raise TypeError("source must be pathlib.Path.")
    try:
        raw_text = source.read_text(encoding="utf-8")
    except OSError as exc:
        raise ChromiumResearchThirdBasisEpochContinuationPlanDocumentError(
            "Third-basis-epoch continuation overlay document could not be read."
        ) from exc

    try:
        document = json.loads(raw_text, object_pairs_hook=_unique_object)
    except (
        json.JSONDecodeError,
        ChromiumResearchThirdBasisEpochContinuationPlanDocumentError,
    ) as exc:
        if isinstance(
            exc,
            ChromiumResearchThirdBasisEpochContinuationPlanDocumentError,
        ):
            raise
        raise ChromiumResearchThirdBasisEpochContinuationPlanDocumentError(
            "Third-basis-epoch continuation overlay document is not valid JSON."
        ) from exc

    if not isinstance(document, dict):
        raise ChromiumResearchThirdBasisEpochContinuationPlanDocumentError(
            "Third-basis-epoch continuation overlay document must be one JSON object."
        )
    _require_exact_keys(document, _ROOT_KEYS, label="continuation overlay document")
    if document["format"] != _OVERLAY_FORMAT:
        raise ChromiumResearchThirdBasisEpochContinuationPlanDocumentError(
            "Third-basis-epoch continuation overlay uses an unsupported format."
        )

    base = source.resolve().parent
    try:
        prior_overlay_source = _decode_path(
            document["prior_third_basis_epoch_overlay_source"],
            "prior_third_basis_epoch_overlay_source",
            base,
        )
        declared_sources = _decode_path_array(
            document["declared_edge_sources"],
            label="declared_edge_sources",
            base=base,
        )
        if not declared_sources:
            raise ValueError("declared_edge_sources must contain at least one path.")
        declaration_source = _decode_path(
            document["declaration_source"],
            "declaration_source",
            base,
        )
    except (TypeError, ValueError) as exc:
        raise ChromiumResearchThirdBasisEpochContinuationPlanDocumentError(
            "Third-basis-epoch continuation overlay cannot form a valid explicit locator plan."
        ) from exc

    return ChromiumResearchThirdBasisEpochContinuationReentryPlan(
        prior_third_basis_epoch_overlay_source=prior_overlay_source,
        declared_edge_sources=declared_sources,
        declaration_source=declaration_source,
    )


def reenter_chromium_research_third_basis_epoch_continuation(
    plan: ChromiumResearchThirdBasisEpochContinuationReentryPlan,
) -> ChromiumResearchThirdBasisEpochContinuationReentryResult:
    """Freshly reconstruct one ordinary continuation above explicit 40B ancestry.

    Pyxis first decodes the exact 40B overlay named by the plan and freshly
    reconstructs its complete third evidence-basis epoch, including retained first-
    and second-root ancestry. Only that fresh third-epoch endpoint is supplied to the
    existing declaration relinker for the explicitly ordered continuation edge paths
    and declaration.

    No directory scanning, predecessor discovery, format guessing, chronology,
    branch selection, or current/latest/head authority is introduced.
    """

    if not isinstance(plan, ChromiumResearchThirdBasisEpochContinuationReentryPlan):
        raise TypeError(
            "plan must be ChromiumResearchThirdBasisEpochContinuationReentryPlan."
        )
    _validate_plan(plan)

    try:
        prior_plan = load_chromium_research_third_basis_epoch_reentry_plan_document(
            plan.prior_third_basis_epoch_overlay_source
        )
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchThirdBasisEpochContinuationReentryError(
            "Explicit prior 40B third-basis-epoch overlay could not be decoded."
        ) from exc

    try:
        prior_reentry = reenter_chromium_research_third_basis_epoch(prior_plan)
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchThirdBasisEpochContinuationReentryError(
            "Prior third-basis-epoch session could not be freshly re-entered."
        ) from exc

    try:
        loaded_declaration = (
            load_chromium_research_working_set_note_revision_edge_sequence_declaration(
                prior_reentry.controller.declared_endpoint,
                plan.declared_edge_sources,
                plan.declaration_source,
            )
        )
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchThirdBasisEpochContinuationReentryError(
            "Explicit post-third-epoch continuation segment could not be freshly reconciled with its declaration."
        ) from exc

    try:
        controller = ChromiumResearchSessionController(loaded_declaration)
    except (TypeError, ValueError) as exc:
        raise ChromiumResearchThirdBasisEpochContinuationReentryError(
            "Fresh post-third-epoch continuation declaration could not become a governed controller."
        ) from exc

    return ChromiumResearchThirdBasisEpochContinuationReentryResult(
        plan=plan,
        prior_third_basis_epoch_reentry=prior_reentry,
        loaded_declaration=loaded_declaration,
        controller=controller,
    )


def persist_chromium_research_third_basis_epoch_continuation_checkpoint(
    prior_reentry: ChromiumResearchThirdBasisEpochReentryResult,
    rollover: ChromiumResearchSessionRolloverResult,
    *,
    prior_third_basis_epoch_overlay_source: Path,
    successor_edge_source: Path,
    continuation_declaration_source: Path,
    destination: Path,
) -> ChromiumResearchThirdBasisEpochContinuationCheckpointResult:
    """Proof-gate one chosen first continuation before writing a 40C overlay.

    The explicitly supplied 40B overlay is freshly decoded and re-entered. Path
    equality with the earned plan is deliberately not authority: a path-distinct
    overlay may be accepted only when fresh reconstruction proves the same retained
    first-, second-, and third-root identities, governed third-epoch presentation,
    and terminal endpoint identity.
    """

    if not isinstance(prior_reentry, ChromiumResearchThirdBasisEpochReentryResult):
        raise TypeError(
            "prior_reentry must be ChromiumResearchThirdBasisEpochReentryResult."
        )
    if not isinstance(rollover, ChromiumResearchSessionRolloverResult):
        raise TypeError("rollover must be ChromiumResearchSessionRolloverResult.")
    for value, label in (
        (prior_third_basis_epoch_overlay_source, "prior_third_basis_epoch_overlay_source"),
        (successor_edge_source, "successor_edge_source"),
        (continuation_declaration_source, "continuation_declaration_source"),
        (destination, "destination"),
    ):
        if not isinstance(value, Path):
            raise TypeError(f"{label} must be pathlib.Path.")

    overlay_source = prior_third_basis_epoch_overlay_source.resolve()
    successor_source = successor_edge_source.resolve()
    declaration_source = continuation_declaration_source.resolve()
    overlay_destination = destination.resolve()

    try:
        explicit_prior_plan = load_chromium_research_third_basis_epoch_reentry_plan_document(
            overlay_source
        )
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchThirdBasisEpochContinuationCheckpointError(
            "Explicit prior 40B overlay could not be decoded."
        ) from exc

    try:
        fresh_prior = reenter_chromium_research_third_basis_epoch(explicit_prior_plan)
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchThirdBasisEpochContinuationCheckpointError(
            "Explicit prior 40B overlay could not freshly reconstruct the third-basis-epoch session."
        ) from exc

    _require_third_epoch_match(prior_reentry, fresh_prior)
    _require_rollover_prior_match(prior_reentry, rollover)

    candidate_plan = ChromiumResearchThirdBasisEpochContinuationReentryPlan(
        prior_third_basis_epoch_overlay_source=overlay_source,
        declared_edge_sources=(successor_source,),
        declaration_source=declaration_source,
    )

    try:
        fresh_continuation = reenter_chromium_research_third_basis_epoch_continuation(
            candidate_plan
        )
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchThirdBasisEpochContinuationCheckpointError(
            "Explicit post-third-epoch continuation locations could not freshly reconstruct a governed session."
        ) from exc
    _require_continuation_match(rollover, fresh_continuation)

    persistence = _persist_overlay(candidate_plan, overlay_destination)
    try:
        decoded = load_chromium_research_third_basis_epoch_continuation_reentry_plan_document(
            persistence.path
        )
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchThirdBasisEpochContinuationCheckpointError(
            "Persisted 40C continuation overlay could not be round-trip decoded."
        ) from exc
    if decoded != candidate_plan:
        raise ChromiumResearchThirdBasisEpochContinuationCheckpointError(
            "Persisted 40C continuation overlay did not round-trip to the exact candidate plan."
        )

    return ChromiumResearchThirdBasisEpochContinuationCheckpointResult(
        prior_reentry=prior_reentry,
        rollover=rollover,
        plan=candidate_plan,
        fresh_reentry=fresh_continuation,
        persistence=persistence,
    )


def _require_third_epoch_match(
    earned: ChromiumResearchThirdBasisEpochReentryResult,
    fresh: ChromiumResearchThirdBasisEpochReentryResult,
) -> None:
    earned_prior = earned.prior_second_basis_epoch_continuation_reentry
    fresh_prior = fresh.prior_second_basis_epoch_continuation_reentry

    if fresh_prior.controller.presentation != earned_prior.controller.presentation:
        raise ChromiumResearchThirdBasisEpochContinuationCheckpointError(
            "Fresh retained second-epoch continuation presentation does not match the earned third-epoch ancestry."
        )
    if (
        fresh_prior.controller.declared_endpoint.verification.edge_record_sha256
        != earned_prior.controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchThirdBasisEpochContinuationCheckpointError(
            "Fresh retained second-epoch continuation endpoint identity does not match the earned third-epoch ancestry."
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
        raise ChromiumResearchThirdBasisEpochContinuationCheckpointError(
            "Fresh retained first-root identity does not match the earned third-epoch ancestry."
        )
    if (
        fresh_second.loaded_root.verification.root_record_sha256
        != earned_second.loaded_root.verification.root_record_sha256
    ):
        raise ChromiumResearchThirdBasisEpochContinuationCheckpointError(
            "Fresh retained second-root identity does not match the earned third-epoch ancestry."
        )
    if (
        fresh.loaded_root.verification.root_record_sha256
        != earned.loaded_root.verification.root_record_sha256
    ):
        raise ChromiumResearchThirdBasisEpochContinuationCheckpointError(
            "Fresh retained third-root identity does not match the earned third epoch."
        )
    if fresh.controller.presentation != earned.controller.presentation:
        raise ChromiumResearchThirdBasisEpochContinuationCheckpointError(
            "Fresh third-epoch governed presentation does not match the earned session."
        )
    if (
        fresh.controller.declared_endpoint.verification.edge_record_sha256
        != earned.controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchThirdBasisEpochContinuationCheckpointError(
            "Fresh third-epoch endpoint identity does not match the earned session."
        )


def _require_rollover_prior_match(
    prior: ChromiumResearchThirdBasisEpochReentryResult,
    rollover: ChromiumResearchSessionRolloverResult,
) -> None:
    if rollover.prior_controller.presentation != prior.controller.presentation:
        raise ChromiumResearchThirdBasisEpochContinuationCheckpointError(
            "Chosen rollover does not belong to the supplied third-epoch session presentation."
        )
    if (
        rollover.prior_controller.declared_endpoint.verification.edge_record_sha256
        != prior.controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchThirdBasisEpochContinuationCheckpointError(
            "Chosen rollover prior endpoint identity does not match the third-epoch session."
        )


def _require_continuation_match(
    rollover: ChromiumResearchSessionRolloverResult,
    fresh: ChromiumResearchThirdBasisEpochContinuationReentryResult,
) -> None:
    if fresh.controller.presentation != rollover.continuation_controller.presentation:
        raise ChromiumResearchThirdBasisEpochContinuationCheckpointError(
            "Fresh 40C continuation presentation does not match the chosen rollover."
        )
    if (
        fresh.controller.declared_endpoint.verification.edge_record_sha256
        != rollover.continuation_controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchThirdBasisEpochContinuationCheckpointError(
            "Fresh 40C continuation endpoint identity does not match the chosen rollover."
        )


def _persist_overlay(
    plan: ChromiumResearchThirdBasisEpochContinuationReentryPlan,
    destination: Path,
) -> ChromiumResearchThirdBasisEpochContinuationOverlayPersistenceResult:
    base = destination.parent
    document: dict[str, object] = {
        "format": _OVERLAY_FORMAT,
        "prior_third_basis_epoch_overlay_source": _encode_path(
            plan.prior_third_basis_epoch_overlay_source,
            base,
        ),
        "declared_edge_sources": [
            _encode_path(path, base) for path in plan.declared_edge_sources
        ],
        "declaration_source": _encode_path(plan.declaration_source, base),
    }
    payload = json.dumps(
        document,
        ensure_ascii=False,
        indent=2,
        sort_keys=False,
    ) + "\n"

    try:
        with destination.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(payload)
    except FileExistsError as exc:
        raise ChromiumResearchThirdBasisEpochContinuationPlanDocumentError(
            "Third-basis-epoch continuation overlay destination already exists."
        ) from exc
    except OSError as exc:
        raise ChromiumResearchThirdBasisEpochContinuationPlanDocumentError(
            "Third-basis-epoch continuation overlay could not be written."
        ) from exc

    return ChromiumResearchThirdBasisEpochContinuationOverlayPersistenceResult(
        plan=plan,
        path=destination,
    )


def _validate_plan(plan: ChromiumResearchThirdBasisEpochContinuationReentryPlan) -> None:
    if not isinstance(plan.prior_third_basis_epoch_overlay_source, Path):
        raise TypeError("plan.prior_third_basis_epoch_overlay_source must be pathlib.Path.")
    if not isinstance(plan.declared_edge_sources, tuple) or not plan.declared_edge_sources:
        raise TypeError("plan.declared_edge_sources must be a non-empty tuple of Paths.")
    for index, source in enumerate(plan.declared_edge_sources):
        if not isinstance(source, Path):
            raise TypeError(f"plan.declared_edge_sources[{index}] must be pathlib.Path.")
    if not isinstance(plan.declaration_source, Path):
        raise TypeError("plan.declaration_source must be pathlib.Path.")


def _require_exact_keys(
    value: dict[str, Any],
    expected: set[str],
    *,
    label: str,
) -> None:
    observed = set(value)
    if observed == expected:
        return
    missing = sorted(expected - observed)
    unexpected = sorted(observed - expected)
    details: list[str] = []
    if missing:
        details.append(f"missing={missing}")
    if unexpected:
        details.append(f"unexpected={unexpected}")
    raise ChromiumResearchThirdBasisEpochContinuationPlanDocumentError(
        f"{label} keys are invalid: {'; '.join(details)}."
    )


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ChromiumResearchThirdBasisEpochContinuationPlanDocumentError(
                f"Duplicate JSON object key is not allowed: {key!r}."
            )
        result[key] = value
    return result


__all__ = [
    "ChromiumResearchThirdBasisEpochContinuationCheckpointError",
    "ChromiumResearchThirdBasisEpochContinuationCheckpointResult",
    "ChromiumResearchThirdBasisEpochContinuationOverlayPersistenceResult",
    "ChromiumResearchThirdBasisEpochContinuationPlanDocumentError",
    "ChromiumResearchThirdBasisEpochContinuationReentryError",
    "ChromiumResearchThirdBasisEpochContinuationReentryPlan",
    "ChromiumResearchThirdBasisEpochContinuationReentryResult",
    "load_chromium_research_third_basis_epoch_continuation_reentry_plan_document",
    "persist_chromium_research_third_basis_epoch_continuation_checkpoint",
    "reenter_chromium_research_third_basis_epoch_continuation",
]
