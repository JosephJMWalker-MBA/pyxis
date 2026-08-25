from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

from .chromium_research_second_basis_epoch_reentry import (
    ChromiumResearchSecondBasisEpochReentryResult,
    reenter_chromium_research_second_basis_epoch,
)
from .chromium_research_second_basis_epoch_reentry_plan_document import (
    load_chromium_research_second_basis_epoch_reentry_plan_document,
)
from .chromium_research_session_controller import ChromiumResearchSessionController
from .chromium_research_session_reentry_plan_document import (
    _decode_path,
    _decode_path_array,
    _encode_path,
)
from .chromium_research_session_rollover import ChromiumResearchSessionRolloverResult
from .chromium_research_working_set_note_revision_edge_sequence_declaration_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceDeclarationRecord,
    load_chromium_research_working_set_note_revision_edge_sequence_declaration,
)


_OVERLAY_FORMAT = (
    "pyxis.chromium.research_second_basis_epoch_continuation_locator_overlay.v1"
)
_ROOT_KEYS = {
    "format",
    "prior_second_basis_epoch_overlay_source",
    "declared_edge_sources",
    "declaration_source",
}


@dataclass(frozen=True, slots=True)
class ChromiumResearchSecondBasisEpochContinuationReentryPlan:
    """Locator-only plan for one ordinary continuation after a persisted 37B epoch.

    The plan retains only the explicit prior 37B overlay location and the explicit
    ordinary continuation declaration locations. It does not duplicate or flatten
    either basis-change epoch. Fresh re-entry must decode the 37B overlay and re-earn
    both ancestry layers before the continuation can be reconciled.
    """

    prior_second_basis_epoch_overlay_source: Path
    declared_edge_sources: tuple[Path, ...]
    declaration_source: Path


@dataclass(frozen=True, slots=True)
class ChromiumResearchSecondBasisEpochContinuationReentryResult:
    """One fresh ordinary continuation above freshly reconstructed second-epoch ancestry."""

    plan: ChromiumResearchSecondBasisEpochContinuationReentryPlan
    prior_second_basis_epoch_reentry: ChromiumResearchSecondBasisEpochReentryResult
    loaded_declaration: ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceDeclarationRecord
    controller: ChromiumResearchSessionController


@dataclass(frozen=True, slots=True)
class ChromiumResearchSecondBasisEpochContinuationOverlayPersistenceResult:
    """One no-overwrite durable 37C locator overlay."""

    plan: ChromiumResearchSecondBasisEpochContinuationReentryPlan
    path: Path


@dataclass(frozen=True, slots=True)
class ChromiumResearchSecondBasisEpochContinuationCheckpointResult:
    """One chosen continuation proven restartable above persisted second-epoch ancestry."""

    prior_reentry: ChromiumResearchSecondBasisEpochReentryResult
    rollover: ChromiumResearchSessionRolloverResult
    plan: ChromiumResearchSecondBasisEpochContinuationReentryPlan
    fresh_reentry: ChromiumResearchSecondBasisEpochContinuationReentryResult
    persistence: ChromiumResearchSecondBasisEpochContinuationOverlayPersistenceResult


class ChromiumResearchSecondBasisEpochContinuationReentryError(ValueError):
    """Raised when one explicit 37C continuation cannot be freshly reconstructed."""


class ChromiumResearchSecondBasisEpochContinuationPlanDocumentError(ValueError):
    """Raised when one 37C continuation overlay is malformed or cannot be written."""


class ChromiumResearchSecondBasisEpochContinuationCheckpointError(ValueError):
    """Raised when one chosen continuation cannot be proven before 37C checkpointing."""


def load_chromium_research_second_basis_epoch_continuation_reentry_plan_document(
    source: Path,
) -> ChromiumResearchSecondBasisEpochContinuationReentryPlan:
    """Decode one strict locator-only 37C continuation overlay.

    Loading is configuration-only. It reads only this document and does not open the
    referenced 37B overlay or any research evidence. Successful decoding therefore
    proves only configuration shape, never ancestry or session coherence.
    """

    if not isinstance(source, Path):
        raise TypeError("source must be pathlib.Path.")
    try:
        raw_text = source.read_text(encoding="utf-8")
    except OSError as exc:
        raise ChromiumResearchSecondBasisEpochContinuationPlanDocumentError(
            "Second-basis-epoch continuation overlay document could not be read."
        ) from exc

    try:
        document = json.loads(raw_text, object_pairs_hook=_unique_object)
    except (
        json.JSONDecodeError,
        ChromiumResearchSecondBasisEpochContinuationPlanDocumentError,
    ) as exc:
        if isinstance(
            exc,
            ChromiumResearchSecondBasisEpochContinuationPlanDocumentError,
        ):
            raise
        raise ChromiumResearchSecondBasisEpochContinuationPlanDocumentError(
            "Second-basis-epoch continuation overlay document is not valid JSON."
        ) from exc

    if not isinstance(document, dict):
        raise ChromiumResearchSecondBasisEpochContinuationPlanDocumentError(
            "Second-basis-epoch continuation overlay document must be one JSON object."
        )
    _require_exact_keys(document, _ROOT_KEYS, label="continuation overlay document")
    if document["format"] != _OVERLAY_FORMAT:
        raise ChromiumResearchSecondBasisEpochContinuationPlanDocumentError(
            "Second-basis-epoch continuation overlay uses an unsupported format."
        )

    base = source.resolve().parent
    try:
        prior_overlay_source = _decode_path(
            document["prior_second_basis_epoch_overlay_source"],
            "prior_second_basis_epoch_overlay_source",
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
        raise ChromiumResearchSecondBasisEpochContinuationPlanDocumentError(
            "Second-basis-epoch continuation overlay cannot form a valid explicit locator plan."
        ) from exc

    return ChromiumResearchSecondBasisEpochContinuationReentryPlan(
        prior_second_basis_epoch_overlay_source=prior_overlay_source,
        declared_edge_sources=declared_sources,
        declaration_source=declaration_source,
    )


def reenter_chromium_research_second_basis_epoch_continuation(
    plan: ChromiumResearchSecondBasisEpochContinuationReentryPlan,
) -> ChromiumResearchSecondBasisEpochContinuationReentryResult:
    """Freshly reconstruct one ordinary continuation above explicit 37B ancestry.

    Pyxis first decodes the exact 37B overlay named by the plan and freshly
    reconstructs its complete second evidence-basis epoch, including the retained
    first root-backed continuation. Only that fresh second-epoch endpoint is supplied
    to existing 26C declaration relinking for the explicitly ordered continuation
    edge paths and declaration.

    No directory scanning, predecessor discovery, format guessing, chronology,
    branch selection, or current/latest/head authority is introduced.
    """

    if not isinstance(plan, ChromiumResearchSecondBasisEpochContinuationReentryPlan):
        raise TypeError(
            "plan must be ChromiumResearchSecondBasisEpochContinuationReentryPlan."
        )
    _validate_plan(plan)

    try:
        prior_plan = load_chromium_research_second_basis_epoch_reentry_plan_document(
            plan.prior_second_basis_epoch_overlay_source
        )
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchSecondBasisEpochContinuationReentryError(
            "Explicit prior 37B second-basis-epoch overlay could not be decoded."
        ) from exc

    try:
        prior_reentry = reenter_chromium_research_second_basis_epoch(prior_plan)
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchSecondBasisEpochContinuationReentryError(
            "Prior second-basis-epoch session could not be freshly re-entered."
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
        raise ChromiumResearchSecondBasisEpochContinuationReentryError(
            "Explicit post-second-epoch continuation segment could not be freshly reconciled with its declaration."
        ) from exc

    try:
        controller = ChromiumResearchSessionController(loaded_declaration)
    except (TypeError, ValueError) as exc:
        raise ChromiumResearchSecondBasisEpochContinuationReentryError(
            "Fresh post-second-epoch continuation declaration could not become a governed controller."
        ) from exc

    return ChromiumResearchSecondBasisEpochContinuationReentryResult(
        plan=plan,
        prior_second_basis_epoch_reentry=prior_reentry,
        loaded_declaration=loaded_declaration,
        controller=controller,
    )


def persist_chromium_research_second_basis_epoch_continuation_checkpoint(
    prior_reentry: ChromiumResearchSecondBasisEpochReentryResult,
    rollover: ChromiumResearchSessionRolloverResult,
    *,
    prior_second_basis_epoch_overlay_source: Path,
    successor_edge_source: Path,
    continuation_declaration_source: Path,
    destination: Path,
) -> ChromiumResearchSecondBasisEpochContinuationCheckpointResult:
    """Proof-gate one chosen first continuation before writing a 37C overlay.

    The explicitly supplied 37B overlay is freshly decoded and re-entered. Path
    equality with the earned plan is deliberately not authority: a path-distinct
    overlay may be accepted only when fresh reconstruction proves the same retained
    first-root ancestry, second-root identity, governed second-epoch presentation,
    and terminal endpoint identity.
    """

    if not isinstance(prior_reentry, ChromiumResearchSecondBasisEpochReentryResult):
        raise TypeError(
            "prior_reentry must be ChromiumResearchSecondBasisEpochReentryResult."
        )
    if not isinstance(rollover, ChromiumResearchSessionRolloverResult):
        raise TypeError("rollover must be ChromiumResearchSessionRolloverResult.")
    for value, label in (
        (prior_second_basis_epoch_overlay_source, "prior_second_basis_epoch_overlay_source"),
        (successor_edge_source, "successor_edge_source"),
        (continuation_declaration_source, "continuation_declaration_source"),
        (destination, "destination"),
    ):
        if not isinstance(value, Path):
            raise TypeError(f"{label} must be pathlib.Path.")

    overlay_source = prior_second_basis_epoch_overlay_source.resolve()
    successor_source = successor_edge_source.resolve()
    declaration_source = continuation_declaration_source.resolve()
    overlay_destination = destination.resolve()

    try:
        explicit_prior_plan = (
            load_chromium_research_second_basis_epoch_reentry_plan_document(
                overlay_source
            )
        )
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchSecondBasisEpochContinuationCheckpointError(
            "Explicit prior 37B overlay could not be decoded."
        ) from exc

    try:
        fresh_prior = reenter_chromium_research_second_basis_epoch(
            explicit_prior_plan
        )
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchSecondBasisEpochContinuationCheckpointError(
            "Explicit prior 37B overlay could not freshly reconstruct the second-basis-epoch session."
        ) from exc

    _require_second_epoch_match(prior_reentry, fresh_prior)
    _require_rollover_prior_match(prior_reentry, rollover)

    candidate_plan = ChromiumResearchSecondBasisEpochContinuationReentryPlan(
        prior_second_basis_epoch_overlay_source=overlay_source,
        declared_edge_sources=(successor_source,),
        declaration_source=declaration_source,
    )

    try:
        fresh_continuation = reenter_chromium_research_second_basis_epoch_continuation(
            candidate_plan
        )
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchSecondBasisEpochContinuationCheckpointError(
            "Explicit post-second-epoch continuation locations could not freshly reconstruct a governed session."
        ) from exc
    _require_continuation_match(rollover, fresh_continuation)

    persistence = _persist_overlay(candidate_plan, overlay_destination)
    try:
        decoded = load_chromium_research_second_basis_epoch_continuation_reentry_plan_document(
            persistence.path
        )
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchSecondBasisEpochContinuationCheckpointError(
            "Persisted 37C continuation overlay could not be round-trip decoded."
        ) from exc
    if decoded != candidate_plan:
        raise ChromiumResearchSecondBasisEpochContinuationCheckpointError(
            "Persisted 37C continuation overlay did not round-trip to the exact candidate plan."
        )

    return ChromiumResearchSecondBasisEpochContinuationCheckpointResult(
        prior_reentry=prior_reentry,
        rollover=rollover,
        plan=candidate_plan,
        fresh_reentry=fresh_continuation,
        persistence=persistence,
    )


def _require_second_epoch_match(
    earned: ChromiumResearchSecondBasisEpochReentryResult,
    fresh: ChromiumResearchSecondBasisEpochReentryResult,
) -> None:
    earned_prior = earned.prior_continuation_reentry
    fresh_prior = fresh.prior_continuation_reentry

    if fresh_prior.controller.presentation != earned_prior.controller.presentation:
        raise ChromiumResearchSecondBasisEpochContinuationCheckpointError(
            "Fresh retained prior continuation presentation does not match the earned second-epoch ancestry."
        )
    if (
        fresh_prior.controller.declared_endpoint.verification.edge_record_sha256
        != earned_prior.controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchSecondBasisEpochContinuationCheckpointError(
            "Fresh retained prior continuation endpoint identity does not match the earned second-epoch ancestry."
        )
    if (
        fresh_prior.prior_root_backed_reentry.loaded_root.verification.root_record_sha256
        != earned_prior.prior_root_backed_reentry.loaded_root.verification.root_record_sha256
    ):
        raise ChromiumResearchSecondBasisEpochContinuationCheckpointError(
            "Fresh retained first-root identity does not match the earned second-epoch ancestry."
        )
    if (
        fresh.loaded_root.verification.root_record_sha256
        != earned.loaded_root.verification.root_record_sha256
    ):
        raise ChromiumResearchSecondBasisEpochContinuationCheckpointError(
            "Fresh second-root identity does not match the earned second epoch."
        )
    if fresh.controller.presentation != earned.controller.presentation:
        raise ChromiumResearchSecondBasisEpochContinuationCheckpointError(
            "Fresh second-epoch governed presentation does not match the earned session."
        )
    if (
        fresh.controller.declared_endpoint.verification.edge_record_sha256
        != earned.controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchSecondBasisEpochContinuationCheckpointError(
            "Fresh second-epoch endpoint identity does not match the earned session."
        )


def _require_rollover_prior_match(
    prior: ChromiumResearchSecondBasisEpochReentryResult,
    rollover: ChromiumResearchSessionRolloverResult,
) -> None:
    if rollover.prior_controller.presentation != prior.controller.presentation:
        raise ChromiumResearchSecondBasisEpochContinuationCheckpointError(
            "Chosen rollover does not belong to the supplied second-epoch session presentation."
        )
    if (
        rollover.prior_controller.declared_endpoint.verification.edge_record_sha256
        != prior.controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchSecondBasisEpochContinuationCheckpointError(
            "Chosen rollover prior endpoint identity does not match the second-epoch session."
        )


def _require_continuation_match(
    rollover: ChromiumResearchSessionRolloverResult,
    fresh: ChromiumResearchSecondBasisEpochContinuationReentryResult,
) -> None:
    if fresh.controller.presentation != rollover.continuation_controller.presentation:
        raise ChromiumResearchSecondBasisEpochContinuationCheckpointError(
            "Fresh 37C continuation presentation does not match the chosen rollover."
        )
    if (
        fresh.controller.declared_endpoint.verification.edge_record_sha256
        != rollover.continuation_controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchSecondBasisEpochContinuationCheckpointError(
            "Fresh 37C continuation endpoint identity does not match the chosen rollover."
        )


def _persist_overlay(
    plan: ChromiumResearchSecondBasisEpochContinuationReentryPlan,
    destination: Path,
) -> ChromiumResearchSecondBasisEpochContinuationOverlayPersistenceResult:
    base = destination.parent
    document: dict[str, object] = {
        "format": _OVERLAY_FORMAT,
        "prior_second_basis_epoch_overlay_source": _encode_path(
            plan.prior_second_basis_epoch_overlay_source,
            base,
        ),
        "declared_edge_sources": [
            _encode_path(path, base) for path in plan.declared_edge_sources
        ],
        "declaration_source": _encode_path(plan.declaration_source, base),
    }
    payload = json.dumps(document, ensure_ascii=False, indent=2) + "\n"
    try:
        with destination.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(payload)
    except FileExistsError as exc:
        raise ChromiumResearchSecondBasisEpochContinuationPlanDocumentError(
            "Second-basis-epoch continuation overlay destination already exists."
        ) from exc
    except OSError as exc:
        raise ChromiumResearchSecondBasisEpochContinuationPlanDocumentError(
            "Second-basis-epoch continuation overlay could not be written."
        ) from exc
    return ChromiumResearchSecondBasisEpochContinuationOverlayPersistenceResult(
        plan=plan,
        path=destination,
    )


def _validate_plan(plan: ChromiumResearchSecondBasisEpochContinuationReentryPlan) -> None:
    if not isinstance(plan.prior_second_basis_epoch_overlay_source, Path):
        raise TypeError("plan.prior_second_basis_epoch_overlay_source must be pathlib.Path.")
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
    raise ChromiumResearchSecondBasisEpochContinuationPlanDocumentError(
        f"{label} keys are invalid: {'; '.join(details)}."
    )


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ChromiumResearchSecondBasisEpochContinuationPlanDocumentError(
                f"Duplicate JSON object key is not allowed: {key!r}."
            )
        result[key] = value
    return result


__all__ = [
    "ChromiumResearchSecondBasisEpochContinuationCheckpointError",
    "ChromiumResearchSecondBasisEpochContinuationCheckpointResult",
    "ChromiumResearchSecondBasisEpochContinuationOverlayPersistenceResult",
    "ChromiumResearchSecondBasisEpochContinuationPlanDocumentError",
    "ChromiumResearchSecondBasisEpochContinuationReentryError",
    "ChromiumResearchSecondBasisEpochContinuationReentryPlan",
    "ChromiumResearchSecondBasisEpochContinuationReentryResult",
    "load_chromium_research_second_basis_epoch_continuation_reentry_plan_document",
    "persist_chromium_research_second_basis_epoch_continuation_checkpoint",
    "reenter_chromium_research_second_basis_epoch_continuation",
]
