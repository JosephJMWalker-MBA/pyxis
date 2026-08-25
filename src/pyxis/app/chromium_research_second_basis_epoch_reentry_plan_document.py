from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

from .chromium_research_second_basis_epoch_reentry import (
    ChromiumResearchSecondBasisEpochReentryPlan,
    ChromiumResearchSecondBasisEpochReentryResult,
    create_chromium_research_second_basis_epoch_reentry_plan,
    reenter_chromium_research_second_basis_epoch,
)
from .chromium_research_session_reentry_plan_document import (
    ChromiumResearchSessionReentryPlanDocumentError,
    _decode_member,
    _decode_path,
    _decode_path_array,
    _encode_member,
    _encode_path,
)


_OVERLAY_FORMAT = (
    "pyxis.chromium.research_second_basis_epoch_reentry_locator_overlay.v1"
)
_ROOT_KEYS = {
    "format",
    "prior_root_backed_continuation_overlay_source",
    "appended_working_set_members",
    "changed_working_set_source",
    "changed_note_source",
    "transition_source",
    "root_source",
    "declared_edge_sources",
    "declaration_source",
}


@dataclass(frozen=True, slots=True)
class ChromiumResearchSecondBasisEpochReentryPlanDocumentPersistenceResult:
    """One strict no-overwrite 37B locator-overlay write.

    `plan` is the exact second-epoch typed locator plan represented by the document.
    The document stores only operational locations and ordering. It stores no research
    evidence digest, timestamp, current/latest/head marker, branch identity, or
    semantic-support claim.
    """

    plan: ChromiumResearchSecondBasisEpochReentryPlan
    path: Path


@dataclass(frozen=True, slots=True)
class ChromiumResearchSecondBasisEpochReentryPlanCheckpointResult:
    """One earned 37A result freshly proven before a 37B overlay write."""

    reentry: ChromiumResearchSecondBasisEpochReentryResult
    plan: ChromiumResearchSecondBasisEpochReentryPlan
    fresh_reentry: ChromiumResearchSecondBasisEpochReentryResult
    persistence: ChromiumResearchSecondBasisEpochReentryPlanDocumentPersistenceResult


class ChromiumResearchSecondBasisEpochReentryPlanDocumentError(ValueError):
    """Raised when one 37B second-epoch locator overlay is malformed or incoherent."""


class ChromiumResearchSecondBasisEpochReentryPlanCheckpointError(ValueError):
    """Raised when one earned 37A result cannot be freshly proven before checkpointing."""


def load_chromium_research_second_basis_epoch_reentry_plan_document(
    source: Path,
) -> ChromiumResearchSecondBasisEpochReentryPlan:
    """Decode one strict 37B overlay into the established 37A typed plan.

    Loading is configuration-only. It reads only this overlay document. It does not
    open the referenced prior 35D/35E continuation overlay and does not read or verify
    any research artifact named by the plan. Relative locations are interpreted only
    relative to this overlay's parent directory.

    No directory scan, digest discovery, predecessor search, format guessing,
    chronology inference, browser work, or current/latest/head selection occurs.
    """

    if not isinstance(source, Path):
        raise TypeError("source must be pathlib.Path.")

    try:
        raw_text = source.read_text(encoding="utf-8")
    except OSError as exc:
        raise ChromiumResearchSecondBasisEpochReentryPlanDocumentError(
            "Second-basis-epoch re-entry overlay document could not be read."
        ) from exc

    try:
        document = json.loads(raw_text, object_pairs_hook=_unique_object)
    except (
        json.JSONDecodeError,
        ChromiumResearchSecondBasisEpochReentryPlanDocumentError,
    ) as exc:
        if isinstance(exc, ChromiumResearchSecondBasisEpochReentryPlanDocumentError):
            raise
        raise ChromiumResearchSecondBasisEpochReentryPlanDocumentError(
            "Second-basis-epoch re-entry overlay document is not valid JSON."
        ) from exc

    if not isinstance(document, dict):
        raise ChromiumResearchSecondBasisEpochReentryPlanDocumentError(
            "Second-basis-epoch re-entry overlay document must be one JSON object."
        )
    _require_exact_keys(document, _ROOT_KEYS, label="overlay document")

    if document["format"] != _OVERLAY_FORMAT:
        raise ChromiumResearchSecondBasisEpochReentryPlanDocumentError(
            "Second-basis-epoch re-entry overlay uses an unsupported format."
        )

    base = source.resolve().parent
    raw_members = document["appended_working_set_members"]
    if not isinstance(raw_members, list) or not raw_members:
        raise ChromiumResearchSecondBasisEpochReentryPlanDocumentError(
            "appended_working_set_members must be a non-empty JSON array."
        )

    try:
        appended = tuple(
            _decode_member(member, index=index, base=base)
            for index, member in enumerate(raw_members)
        )
        declared_sources = _decode_path_array(
            document["declared_edge_sources"],
            label="declared_edge_sources",
            base=base,
        )
        return create_chromium_research_second_basis_epoch_reentry_plan(
            _decode_path(
                document["prior_root_backed_continuation_overlay_source"],
                "prior_root_backed_continuation_overlay_source",
                base,
            ),
            appended,
            changed_working_set_source=_decode_path(
                document["changed_working_set_source"],
                "changed_working_set_source",
                base,
            ),
            changed_note_source=_decode_path(
                document["changed_note_source"],
                "changed_note_source",
                base,
            ),
            transition_source=_decode_path(
                document["transition_source"],
                "transition_source",
                base,
            ),
            root_source=_decode_path(
                document["root_source"],
                "root_source",
                base,
            ),
            declared_edge_sources=declared_sources,
            declaration_source=_decode_path(
                document["declaration_source"],
                "declaration_source",
                base,
            ),
        )
    except (
        ChromiumResearchSessionReentryPlanDocumentError,
        TypeError,
        ValueError,
    ) as exc:
        raise ChromiumResearchSecondBasisEpochReentryPlanDocumentError(
            "Second-basis-epoch overlay cannot form a valid explicit 37A locator plan."
        ) from exc


def persist_chromium_research_second_basis_epoch_reentry_plan_document(
    reentry: ChromiumResearchSecondBasisEpochReentryResult,
    *,
    prior_root_backed_continuation_overlay_source: Path,
    destination: Path,
) -> ChromiumResearchSecondBasisEpochReentryPlanCheckpointResult:
    """Freshly prove and checkpoint one earned 37A result as a strict 37B overlay.

    The caller explicitly supplies the current prior 35D/35E continuation-overlay
    location. A candidate 37A plan is formed from that current location plus the
    second-epoch locator layer retained by the earned result. Before any bytes are
    written, the candidate is freshly re-entered through the public 37A boundary.

    The fresh reconstruction must match the earned result at both ancestry layers:
    the prior continuation's governed presentation, terminal durable edge identity,
    and retained first-root identity; then the second-root durable identity, final
    governed presentation, and final durable endpoint identity.

    Path equality is not used as durable identity. A path-distinct prior continuation
    may therefore be accepted when explicit fresh reconstruction proves the same
    durable authority. No moved path is discovered automatically.
    """

    if not isinstance(reentry, ChromiumResearchSecondBasisEpochReentryResult):
        raise TypeError(
            "reentry must be ChromiumResearchSecondBasisEpochReentryResult."
        )
    if not isinstance(prior_root_backed_continuation_overlay_source, Path):
        raise TypeError(
            "prior_root_backed_continuation_overlay_source must be pathlib.Path."
        )
    if not isinstance(destination, Path):
        raise TypeError("destination must be pathlib.Path.")

    overlay_source = prior_root_backed_continuation_overlay_source.resolve()
    overlay_destination = destination.resolve()

    candidate_plan = create_chromium_research_second_basis_epoch_reentry_plan(
        overlay_source,
        reentry.plan.appended_working_set_members,
        changed_working_set_source=reentry.plan.changed_working_set_source,
        changed_note_source=reentry.plan.changed_note_source,
        transition_source=reentry.plan.transition_source,
        root_source=reentry.plan.root_source,
        declared_edge_sources=reentry.plan.declared_edge_sources,
        declaration_source=reentry.plan.declaration_source,
    )

    try:
        fresh_reentry = reenter_chromium_research_second_basis_epoch(candidate_plan)
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchSecondBasisEpochReentryPlanCheckpointError(
            "Candidate second-basis-epoch overlay locations could not freshly reconstruct a governed session."
        ) from exc

    _require_fresh_reentry_match(reentry, fresh_reentry)

    persistence = _persist_overlay_document(
        candidate_plan,
        destination=overlay_destination,
    )

    try:
        decoded = load_chromium_research_second_basis_epoch_reentry_plan_document(
            persistence.path
        )
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchSecondBasisEpochReentryPlanCheckpointError(
            "Persisted second-basis-epoch overlay could not be round-trip decoded."
        ) from exc
    if decoded != candidate_plan:
        raise ChromiumResearchSecondBasisEpochReentryPlanCheckpointError(
            "Persisted second-basis-epoch overlay did not round-trip to the exact candidate plan."
        )

    return ChromiumResearchSecondBasisEpochReentryPlanCheckpointResult(
        reentry=reentry,
        plan=candidate_plan,
        fresh_reentry=fresh_reentry,
        persistence=persistence,
    )


def _require_fresh_reentry_match(
    earned: ChromiumResearchSecondBasisEpochReentryResult,
    fresh: ChromiumResearchSecondBasisEpochReentryResult,
) -> None:
    earned_prior = earned.prior_continuation_reentry
    fresh_prior = fresh.prior_continuation_reentry

    if fresh_prior.controller.presentation != earned_prior.controller.presentation:
        raise ChromiumResearchSecondBasisEpochReentryPlanCheckpointError(
            "Fresh prior continuation presentation does not match the earned second-epoch ancestry."
        )
    if (
        fresh_prior.controller.declared_endpoint.verification.edge_record_sha256
        != earned_prior.controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchSecondBasisEpochReentryPlanCheckpointError(
            "Fresh prior continuation endpoint identity does not match the earned second-epoch ancestry."
        )
    if (
        fresh_prior.prior_root_backed_reentry.loaded_root.verification.root_record_sha256
        != earned_prior.prior_root_backed_reentry.loaded_root.verification.root_record_sha256
    ):
        raise ChromiumResearchSecondBasisEpochReentryPlanCheckpointError(
            "Fresh retained first-root identity does not match the earned second-epoch ancestry."
        )
    if (
        fresh.loaded_root.verification.root_record_sha256
        != earned.loaded_root.verification.root_record_sha256
    ):
        raise ChromiumResearchSecondBasisEpochReentryPlanCheckpointError(
            "Fresh second-root identity does not match the earned second epoch."
        )
    if fresh.controller.presentation != earned.controller.presentation:
        raise ChromiumResearchSecondBasisEpochReentryPlanCheckpointError(
            "Fresh second-epoch governed presentation does not match the earned session."
        )
    if (
        fresh.controller.declared_endpoint.verification.edge_record_sha256
        != earned.controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchSecondBasisEpochReentryPlanCheckpointError(
            "Fresh second-epoch endpoint identity does not match the earned session."
        )


def _persist_overlay_document(
    plan: ChromiumResearchSecondBasisEpochReentryPlan,
    *,
    destination: Path,
) -> ChromiumResearchSecondBasisEpochReentryPlanDocumentPersistenceResult:
    base = destination.parent
    document: dict[str, object] = {
        "format": _OVERLAY_FORMAT,
        "prior_root_backed_continuation_overlay_source": _encode_path(
            plan.prior_root_backed_continuation_overlay_source,
            base,
        ),
        "appended_working_set_members": [
            _encode_member(member, base=base)
            for member in plan.appended_working_set_members
        ],
        "changed_working_set_source": _encode_path(
            plan.changed_working_set_source,
            base,
        ),
        "changed_note_source": _encode_path(plan.changed_note_source, base),
        "transition_source": _encode_path(plan.transition_source, base),
        "root_source": _encode_path(plan.root_source, base),
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
        raise ChromiumResearchSecondBasisEpochReentryPlanDocumentError(
            "Second-basis-epoch re-entry overlay destination already exists."
        ) from exc
    except OSError as exc:
        raise ChromiumResearchSecondBasisEpochReentryPlanDocumentError(
            "Second-basis-epoch re-entry overlay could not be written."
        ) from exc

    return ChromiumResearchSecondBasisEpochReentryPlanDocumentPersistenceResult(
        plan=plan,
        path=destination,
    )


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
    raise ChromiumResearchSecondBasisEpochReentryPlanDocumentError(
        f"{label} keys are invalid: {'; '.join(details)}."
    )


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ChromiumResearchSecondBasisEpochReentryPlanDocumentError(
                f"Duplicate JSON object key is not allowed: {key!r}."
            )
        result[key] = value
    return result


__all__ = [
    "ChromiumResearchSecondBasisEpochReentryPlanCheckpointError",
    "ChromiumResearchSecondBasisEpochReentryPlanCheckpointResult",
    "ChromiumResearchSecondBasisEpochReentryPlanDocumentError",
    "ChromiumResearchSecondBasisEpochReentryPlanDocumentPersistenceResult",
    "load_chromium_research_second_basis_epoch_reentry_plan_document",
    "persist_chromium_research_second_basis_epoch_reentry_plan_document",
]
