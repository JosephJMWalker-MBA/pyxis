from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

from .chromium_research_root_backed_session_reentry import (
    ChromiumResearchRootBackedSessionReentryPlan,
    ChromiumResearchRootBackedSessionReentryResult,
    reenter_chromium_research_root_backed_session,
)
from .chromium_research_root_backed_session_reentry_plan_document import (
    load_chromium_research_root_backed_session_reentry_plan_document,
)
from .chromium_research_session_controller import ChromiumResearchSessionController
from .chromium_research_session_rollover import ChromiumResearchSessionRolloverResult
from .chromium_research_session_reentry_plan_document import (
    _decode_path,
    _decode_path_array,
    _encode_path,
)
from .chromium_research_working_set_note_revision_edge_sequence_declaration_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceDeclarationRecord,
    load_chromium_research_working_set_note_revision_edge_sequence_declaration,
)


_OVERLAY_FORMAT = (
    "pyxis.chromium.research_root_backed_session_continuation_locator_overlay.v1"
)
_ROOT_KEYS = {
    "format",
    "prior_root_backed_overlay_source",
    "declared_edge_sources",
    "declaration_source",
}


@dataclass(frozen=True, slots=True)
class ChromiumResearchRootBackedSessionContinuationReentryPlan:
    """Operational locator plan for one first ordinary continuation after 35C.

    `prior_root_backed_plan` is decoded through the explicitly supplied 35C overlay;
    it is not copied into this continuation document. `declared_edge_sources` and
    `declaration_source` describe only the explicit ordinary continuation segment
    whose starting predecessor is the prior root-backed session's declared endpoint.

    This is operational configuration only. It is not an evidence artifact, history
    index, chronology record, branch selector, or global head pointer.
    """

    prior_root_backed_overlay_source: Path
    prior_root_backed_plan: ChromiumResearchRootBackedSessionReentryPlan
    declared_edge_sources: tuple[Path, ...]
    declaration_source: Path


@dataclass(frozen=True, slots=True)
class ChromiumResearchRootBackedSessionContinuationReentryResult:
    """One fresh continuation reconstructed on top of one fresh 35B prior session."""

    plan: ChromiumResearchRootBackedSessionContinuationReentryPlan
    prior_root_backed_reentry: ChromiumResearchRootBackedSessionReentryResult
    loaded_declaration: ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceDeclarationRecord
    controller: ChromiumResearchSessionController


@dataclass(frozen=True, slots=True)
class ChromiumResearchRootBackedSessionContinuationOverlayPersistenceResult:
    """One no-overwrite durable 35D locator overlay."""

    plan: ChromiumResearchRootBackedSessionContinuationReentryPlan
    path: Path


@dataclass(frozen=True, slots=True)
class ChromiumResearchRootBackedSessionContinuationCheckpointResult:
    """One chosen 30A continuation proven restartable before 35D persistence."""

    prior_reentry: ChromiumResearchRootBackedSessionReentryResult
    rollover: ChromiumResearchSessionRolloverResult
    plan: ChromiumResearchRootBackedSessionContinuationReentryPlan
    fresh_reentry: ChromiumResearchRootBackedSessionContinuationReentryResult
    persistence: ChromiumResearchRootBackedSessionContinuationOverlayPersistenceResult


class ChromiumResearchRootBackedSessionContinuationReentryError(ValueError):
    """Raised when one explicit 35D continuation cannot be freshly reconstructed."""


class ChromiumResearchRootBackedSessionContinuationPlanDocumentError(ValueError):
    """Raised when one 35D continuation overlay is malformed or cannot be written."""


class ChromiumResearchRootBackedSessionContinuationCheckpointError(ValueError):
    """Raised when one chosen continuation cannot be proven before checkpointing."""


def load_chromium_research_root_backed_session_continuation_reentry_plan_document(
    source: Path,
) -> ChromiumResearchRootBackedSessionContinuationReentryPlan:
    """Decode one strict 35D continuation overlay without reading research evidence.

    Loading reads the explicit 35D document and the explicitly referenced 35C
    configuration document (which itself composes the ordinary 31B plan document).
    No research artifact referenced by those plans is freshly verified here.
    """

    if not isinstance(source, Path):
        raise TypeError("source must be pathlib.Path.")
    try:
        raw_text = source.read_text(encoding="utf-8")
    except OSError as exc:
        raise ChromiumResearchRootBackedSessionContinuationPlanDocumentError(
            "Root-backed continuation overlay document could not be read."
        ) from exc

    try:
        document = json.loads(raw_text, object_pairs_hook=_unique_object)
    except (
        json.JSONDecodeError,
        ChromiumResearchRootBackedSessionContinuationPlanDocumentError,
    ) as exc:
        if isinstance(
            exc,
            ChromiumResearchRootBackedSessionContinuationPlanDocumentError,
        ):
            raise
        raise ChromiumResearchRootBackedSessionContinuationPlanDocumentError(
            "Root-backed continuation overlay document is not valid JSON."
        ) from exc

    if not isinstance(document, dict):
        raise ChromiumResearchRootBackedSessionContinuationPlanDocumentError(
            "Root-backed continuation overlay document must be one JSON object."
        )
    _require_exact_keys(document, _ROOT_KEYS, label="continuation overlay document")
    if document["format"] != _OVERLAY_FORMAT:
        raise ChromiumResearchRootBackedSessionContinuationPlanDocumentError(
            "Root-backed continuation overlay uses an unsupported format."
        )

    base = source.resolve().parent
    try:
        prior_overlay_source = _decode_path(
            document["prior_root_backed_overlay_source"],
            "prior_root_backed_overlay_source",
            base,
        )
        prior_plan = load_chromium_research_root_backed_session_reentry_plan_document(
            prior_overlay_source
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
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchRootBackedSessionContinuationPlanDocumentError(
            "Root-backed continuation overlay cannot form a valid explicit locator plan."
        ) from exc

    return ChromiumResearchRootBackedSessionContinuationReentryPlan(
        prior_root_backed_overlay_source=prior_overlay_source,
        prior_root_backed_plan=prior_plan,
        declared_edge_sources=declared_sources,
        declaration_source=declaration_source,
    )


def reenter_chromium_research_root_backed_session_continuation(
    plan: ChromiumResearchRootBackedSessionContinuationReentryPlan,
) -> ChromiumResearchRootBackedSessionContinuationReentryResult:
    """Freshly reconstruct one ordinary continuation above explicit 35B ancestry.

    Pyxis first freshly reconstructs the complete prior root-backed session through
    public 35B using the typed plan obtained from the 35C overlay. It then delegates
    the explicitly ordered continuation edge paths and declaration to existing 26C,
    using only the freshly reconstructed prior declared endpoint as the starting
    predecessor.
    """

    if not isinstance(plan, ChromiumResearchRootBackedSessionContinuationReentryPlan):
        raise TypeError(
            "plan must be ChromiumResearchRootBackedSessionContinuationReentryPlan."
        )
    _validate_plan(plan)

    try:
        prior_reentry = reenter_chromium_research_root_backed_session(
            plan.prior_root_backed_plan
        )
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchRootBackedSessionContinuationReentryError(
            "Prior root-backed session could not be freshly re-entered."
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
        raise ChromiumResearchRootBackedSessionContinuationReentryError(
            "Explicit continuation segment could not be freshly reconciled with its declaration."
        ) from exc

    try:
        controller = ChromiumResearchSessionController(loaded_declaration)
    except (TypeError, ValueError) as exc:
        raise ChromiumResearchRootBackedSessionContinuationReentryError(
            "Fresh continuation declaration could not become a governed controller."
        ) from exc

    return ChromiumResearchRootBackedSessionContinuationReentryResult(
        plan=plan,
        prior_root_backed_reentry=prior_reentry,
        loaded_declaration=loaded_declaration,
        controller=controller,
    )


def persist_chromium_research_root_backed_session_continuation_checkpoint(
    prior_reentry: ChromiumResearchRootBackedSessionReentryResult,
    rollover: ChromiumResearchSessionRolloverResult,
    *,
    prior_root_backed_overlay_source: Path,
    successor_edge_source: Path,
    continuation_declaration_source: Path,
    destination: Path,
) -> ChromiumResearchRootBackedSessionContinuationCheckpointResult:
    """Proof-gate one chosen 30A continuation before writing a 35D overlay."""

    if not isinstance(prior_reentry, ChromiumResearchRootBackedSessionReentryResult):
        raise TypeError(
            "prior_reentry must be ChromiumResearchRootBackedSessionReentryResult."
        )
    if not isinstance(rollover, ChromiumResearchSessionRolloverResult):
        raise TypeError("rollover must be ChromiumResearchSessionRolloverResult.")
    for value, label in (
        (prior_root_backed_overlay_source, "prior_root_backed_overlay_source"),
        (successor_edge_source, "successor_edge_source"),
        (continuation_declaration_source, "continuation_declaration_source"),
        (destination, "destination"),
    ):
        if not isinstance(value, Path):
            raise TypeError(f"{label} must be pathlib.Path.")

    overlay_source = prior_root_backed_overlay_source.resolve()
    successor_source = successor_edge_source.resolve()
    declaration_source = continuation_declaration_source.resolve()
    overlay_destination = destination.resolve()

    try:
        prior_plan = load_chromium_research_root_backed_session_reentry_plan_document(
            overlay_source
        )
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchRootBackedSessionContinuationCheckpointError(
            "Explicit prior 35C overlay could not be decoded."
        ) from exc
    if prior_plan != prior_reentry.plan:
        raise ChromiumResearchRootBackedSessionContinuationCheckpointError(
            "Explicit prior 35C overlay does not describe the earned root-backed session plan."
        )

    try:
        fresh_prior = reenter_chromium_research_root_backed_session(prior_plan)
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchRootBackedSessionContinuationCheckpointError(
            "Explicit prior 35C overlay could not freshly reconstruct the root-backed session."
        ) from exc
    _require_prior_match(prior_reentry, fresh_prior)
    _require_rollover_prior_match(prior_reentry, rollover)

    candidate_plan = ChromiumResearchRootBackedSessionContinuationReentryPlan(
        prior_root_backed_overlay_source=overlay_source,
        prior_root_backed_plan=prior_plan,
        declared_edge_sources=(successor_source,),
        declaration_source=declaration_source,
    )

    try:
        fresh_continuation = reenter_chromium_research_root_backed_session_continuation(
            candidate_plan
        )
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchRootBackedSessionContinuationCheckpointError(
            "Explicit continuation locations could not freshly reconstruct a governed session."
        ) from exc
    _require_continuation_match(rollover, fresh_continuation)

    persistence = _persist_overlay(candidate_plan, overlay_destination)
    try:
        decoded = load_chromium_research_root_backed_session_continuation_reentry_plan_document(
            persistence.path
        )
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchRootBackedSessionContinuationCheckpointError(
            "Persisted 35D continuation overlay could not be round-trip decoded."
        ) from exc
    if decoded != candidate_plan:
        raise ChromiumResearchRootBackedSessionContinuationCheckpointError(
            "Persisted 35D continuation overlay did not round-trip to the exact candidate plan."
        )

    return ChromiumResearchRootBackedSessionContinuationCheckpointResult(
        prior_reentry=prior_reentry,
        rollover=rollover,
        plan=candidate_plan,
        fresh_reentry=fresh_continuation,
        persistence=persistence,
    )


def _require_prior_match(
    earned: ChromiumResearchRootBackedSessionReentryResult,
    fresh: ChromiumResearchRootBackedSessionReentryResult,
) -> None:
    if fresh.controller.presentation != earned.controller.presentation:
        raise ChromiumResearchRootBackedSessionContinuationCheckpointError(
            "Fresh prior root-backed presentation does not match the earned session."
        )
    if (
        fresh.controller.declared_endpoint.verification.edge_record_sha256
        != earned.controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchRootBackedSessionContinuationCheckpointError(
            "Fresh prior root-backed endpoint identity does not match the earned session."
        )
    if (
        fresh.loaded_root.verification.root_record_sha256
        != earned.loaded_root.verification.root_record_sha256
    ):
        raise ChromiumResearchRootBackedSessionContinuationCheckpointError(
            "Fresh prior root identity does not match the earned session."
        )


def _require_rollover_prior_match(
    prior: ChromiumResearchRootBackedSessionReentryResult,
    rollover: ChromiumResearchSessionRolloverResult,
) -> None:
    if rollover.prior_controller.presentation != prior.controller.presentation:
        raise ChromiumResearchRootBackedSessionContinuationCheckpointError(
            "Chosen rollover does not belong to the supplied root-backed session presentation."
        )
    if (
        rollover.prior_controller.declared_endpoint.verification.edge_record_sha256
        != prior.controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchRootBackedSessionContinuationCheckpointError(
            "Chosen rollover prior endpoint identity does not match the root-backed session."
        )


def _require_continuation_match(
    rollover: ChromiumResearchSessionRolloverResult,
    fresh: ChromiumResearchRootBackedSessionContinuationReentryResult,
) -> None:
    if fresh.controller.presentation != rollover.continuation_controller.presentation:
        raise ChromiumResearchRootBackedSessionContinuationCheckpointError(
            "Fresh 35D continuation presentation does not match the chosen rollover."
        )
    if (
        fresh.controller.declared_endpoint.verification.edge_record_sha256
        != rollover.continuation_controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchRootBackedSessionContinuationCheckpointError(
            "Fresh 35D continuation endpoint identity does not match the chosen rollover."
        )


def _persist_overlay(
    plan: ChromiumResearchRootBackedSessionContinuationReentryPlan,
    destination: Path,
) -> ChromiumResearchRootBackedSessionContinuationOverlayPersistenceResult:
    base = destination.parent
    document: dict[str, object] = {
        "format": _OVERLAY_FORMAT,
        "prior_root_backed_overlay_source": _encode_path(
            plan.prior_root_backed_overlay_source,
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
        raise ChromiumResearchRootBackedSessionContinuationPlanDocumentError(
            "Root-backed continuation overlay destination already exists."
        ) from exc
    except OSError as exc:
        raise ChromiumResearchRootBackedSessionContinuationPlanDocumentError(
            "Root-backed continuation overlay could not be written."
        ) from exc
    return ChromiumResearchRootBackedSessionContinuationOverlayPersistenceResult(
        plan=plan,
        path=destination,
    )


def _validate_plan(plan: ChromiumResearchRootBackedSessionContinuationReentryPlan) -> None:
    if not isinstance(plan.prior_root_backed_overlay_source, Path):
        raise TypeError("plan.prior_root_backed_overlay_source must be pathlib.Path.")
    if not isinstance(plan.prior_root_backed_plan, ChromiumResearchRootBackedSessionReentryPlan):
        raise TypeError("plan.prior_root_backed_plan has an unsupported type.")
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
    raise ChromiumResearchRootBackedSessionContinuationPlanDocumentError(
        f"{label} keys are invalid: {'; '.join(details)}."
    )


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ChromiumResearchRootBackedSessionContinuationPlanDocumentError(
                f"Duplicate JSON object key is not allowed: {key!r}."
            )
        result[key] = value
    return result


__all__ = [
    "ChromiumResearchRootBackedSessionContinuationCheckpointError",
    "ChromiumResearchRootBackedSessionContinuationCheckpointResult",
    "ChromiumResearchRootBackedSessionContinuationOverlayPersistenceResult",
    "ChromiumResearchRootBackedSessionContinuationPlanDocumentError",
    "ChromiumResearchRootBackedSessionContinuationReentryError",
    "ChromiumResearchRootBackedSessionContinuationReentryPlan",
    "ChromiumResearchRootBackedSessionContinuationReentryResult",
    "load_chromium_research_root_backed_session_continuation_reentry_plan_document",
    "persist_chromium_research_root_backed_session_continuation_checkpoint",
    "reenter_chromium_research_root_backed_session_continuation",
]
