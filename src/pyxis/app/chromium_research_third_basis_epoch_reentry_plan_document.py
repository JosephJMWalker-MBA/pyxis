from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

from .chromium_research_session_reentry_plan_document import (
    ChromiumResearchSessionReentryPlanDocumentError,
    _decode_member,
    _decode_path,
    _decode_path_array,
    _encode_member,
    _encode_path,
)
from .chromium_research_third_basis_epoch_reentry import (
    ChromiumResearchThirdBasisEpochReentryPlan,
    ChromiumResearchThirdBasisEpochReentryResult,
    create_chromium_research_third_basis_epoch_reentry_plan,
    reenter_chromium_research_third_basis_epoch,
)


_OVERLAY_FORMAT = "pyxis.chromium.research_third_basis_epoch_reentry_locator_overlay.v1"
_ROOT_KEYS = {
    "format",
    "prior_second_basis_epoch_continuation_overlay_source",
    "appended_working_set_members",
    "changed_working_set_source",
    "changed_note_source",
    "transition_source",
    "root_source",
    "declared_edge_sources",
    "declaration_source",
}


@dataclass(frozen=True, slots=True)
class ChromiumResearchThirdBasisEpochReentryPlanDocumentPersistenceResult:
    """One strict no-overwrite third-epoch locator-overlay write.

    The document represents only the exact operational locator plan needed to attempt
    a fresh three-root reconstruction. It is configuration, not evidence or authority.
    """

    plan: ChromiumResearchThirdBasisEpochReentryPlan
    path: Path


@dataclass(frozen=True, slots=True)
class ChromiumResearchThirdBasisEpochReentryPlanCheckpointResult:
    """One earned 40A result freshly proven before a 40B overlay write."""

    reentry: ChromiumResearchThirdBasisEpochReentryResult
    plan: ChromiumResearchThirdBasisEpochReentryPlan
    fresh_reentry: ChromiumResearchThirdBasisEpochReentryResult
    persistence: ChromiumResearchThirdBasisEpochReentryPlanDocumentPersistenceResult


class ChromiumResearchThirdBasisEpochReentryPlanDocumentError(ValueError):
    """Raised when one 40B third-epoch locator overlay is malformed or incoherent."""


class ChromiumResearchThirdBasisEpochReentryPlanCheckpointError(ValueError):
    """Raised when one earned 40A result cannot be freshly proven before checkpointing."""


def load_chromium_research_third_basis_epoch_reentry_plan_document(
    source: Path,
) -> ChromiumResearchThirdBasisEpochReentryPlan:
    """Decode one strict 40B overlay into the established 40A typed plan.

    Loading is deliberately configuration-only. It reads only this overlay document.
    It does not open the referenced prior 37C/37D continuation overlay, member sources,
    changed working-set/note records, transition, third root, declared edges, or
    declaration. Relative paths are interpreted only relative to this document.

    Successful decode therefore proves only that one explicit locator configuration
    has the required shape. It proves no evidence integrity, retained ancestry,
    governed session state, chronology, branch identity, or current/latest/head state.
    """

    if not isinstance(source, Path):
        raise TypeError("source must be pathlib.Path.")

    try:
        raw_text = source.read_text(encoding="utf-8")
    except OSError as exc:
        raise ChromiumResearchThirdBasisEpochReentryPlanDocumentError(
            "Third-basis-epoch re-entry overlay document could not be read."
        ) from exc

    try:
        document = json.loads(raw_text, object_pairs_hook=_unique_object)
    except (
        json.JSONDecodeError,
        ChromiumResearchThirdBasisEpochReentryPlanDocumentError,
    ) as exc:
        if isinstance(exc, ChromiumResearchThirdBasisEpochReentryPlanDocumentError):
            raise
        raise ChromiumResearchThirdBasisEpochReentryPlanDocumentError(
            "Third-basis-epoch re-entry overlay document is not valid JSON."
        ) from exc

    if not isinstance(document, dict):
        raise ChromiumResearchThirdBasisEpochReentryPlanDocumentError(
            "Third-basis-epoch re-entry overlay document must be one JSON object."
        )
    _require_exact_keys(document, _ROOT_KEYS, label="overlay document")

    if document["format"] != _OVERLAY_FORMAT:
        raise ChromiumResearchThirdBasisEpochReentryPlanDocumentError(
            "Third-basis-epoch re-entry overlay uses an unsupported format."
        )

    base = source.resolve().parent
    raw_members = document["appended_working_set_members"]
    if not isinstance(raw_members, list) or not raw_members:
        raise ChromiumResearchThirdBasisEpochReentryPlanDocumentError(
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
        return create_chromium_research_third_basis_epoch_reentry_plan(
            _decode_path(
                document["prior_second_basis_epoch_continuation_overlay_source"],
                "prior_second_basis_epoch_continuation_overlay_source",
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
        raise ChromiumResearchThirdBasisEpochReentryPlanDocumentError(
            "Third-basis-epoch overlay cannot form a valid explicit 40A locator plan."
        ) from exc


def persist_chromium_research_third_basis_epoch_reentry_plan_document(
    reentry: ChromiumResearchThirdBasisEpochReentryResult,
    *,
    prior_second_basis_epoch_continuation_overlay_source: Path,
    destination: Path,
) -> ChromiumResearchThirdBasisEpochReentryPlanCheckpointResult:
    """Freshly prove and checkpoint one earned 40A result as a strict 40B overlay.

    The caller explicitly supplies the current location of the prior 37C/37D
    continuation overlay. A candidate third-epoch plan is formed from that explicit
    location plus the third-epoch locator layer retained by the earned 40A result.
    Before any bytes are written, the candidate is independently re-entered through
    the public 40A boundary.

    Fresh reconstruction must match the earned result across all three retained roots
    and the governed state around them: first-root identity, second-root identity,
    selected post-second-epoch continuation presentation and terminal endpoint,
    third-root identity, final third-epoch presentation, and final durable endpoint.

    Path equality is never treated as durable identity. A path-distinct prior
    continuation overlay can be accepted only when explicit fresh reconstruction proves
    the same durable ancestry and governed state. No moved path is discovered.
    """

    if not isinstance(reentry, ChromiumResearchThirdBasisEpochReentryResult):
        raise TypeError(
            "reentry must be ChromiumResearchThirdBasisEpochReentryResult."
        )
    if not isinstance(prior_second_basis_epoch_continuation_overlay_source, Path):
        raise TypeError(
            "prior_second_basis_epoch_continuation_overlay_source must be pathlib.Path."
        )
    if not isinstance(destination, Path):
        raise TypeError("destination must be pathlib.Path.")

    prior_overlay_source = prior_second_basis_epoch_continuation_overlay_source.resolve()
    overlay_destination = destination.resolve()

    candidate_plan = create_chromium_research_third_basis_epoch_reentry_plan(
        prior_overlay_source,
        reentry.plan.appended_working_set_members,
        changed_working_set_source=reentry.plan.changed_working_set_source,
        changed_note_source=reentry.plan.changed_note_source,
        transition_source=reentry.plan.transition_source,
        root_source=reentry.plan.root_source,
        declared_edge_sources=reentry.plan.declared_edge_sources,
        declaration_source=reentry.plan.declaration_source,
    )

    try:
        fresh_reentry = reenter_chromium_research_third_basis_epoch(candidate_plan)
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchThirdBasisEpochReentryPlanCheckpointError(
            "Candidate third-basis-epoch overlay locations could not freshly reconstruct a governed three-root session."
        ) from exc

    _require_fresh_reentry_match(reentry, fresh_reentry)

    persistence = _persist_overlay_document(
        candidate_plan,
        destination=overlay_destination,
    )

    try:
        decoded = load_chromium_research_third_basis_epoch_reentry_plan_document(
            persistence.path
        )
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchThirdBasisEpochReentryPlanCheckpointError(
            "Persisted third-basis-epoch overlay could not be round-trip decoded."
        ) from exc
    if decoded != candidate_plan:
        raise ChromiumResearchThirdBasisEpochReentryPlanCheckpointError(
            "Persisted third-basis-epoch overlay did not round-trip to the exact candidate plan."
        )

    return ChromiumResearchThirdBasisEpochReentryPlanCheckpointResult(
        reentry=reentry,
        plan=candidate_plan,
        fresh_reentry=fresh_reentry,
        persistence=persistence,
    )


def _require_fresh_reentry_match(
    earned: ChromiumResearchThirdBasisEpochReentryResult,
    fresh: ChromiumResearchThirdBasisEpochReentryResult,
) -> None:
    earned_prior = earned.prior_second_basis_epoch_continuation_reentry
    fresh_prior = fresh.prior_second_basis_epoch_continuation_reentry

    if fresh_prior.controller.presentation != earned_prior.controller.presentation:
        raise ChromiumResearchThirdBasisEpochReentryPlanCheckpointError(
            "Fresh prior second-epoch continuation presentation does not match the earned third-epoch ancestry."
        )
    if (
        fresh_prior.controller.declared_endpoint.verification.edge_record_sha256
        != earned_prior.controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchThirdBasisEpochReentryPlanCheckpointError(
            "Fresh prior second-epoch continuation endpoint identity does not match the earned third-epoch ancestry."
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
        raise ChromiumResearchThirdBasisEpochReentryPlanCheckpointError(
            "Fresh retained first-root identity does not match the earned third-epoch ancestry."
        )
    if (
        fresh_second.loaded_root.verification.root_record_sha256
        != earned_second.loaded_root.verification.root_record_sha256
    ):
        raise ChromiumResearchThirdBasisEpochReentryPlanCheckpointError(
            "Fresh retained second-root identity does not match the earned third-epoch ancestry."
        )
    if (
        fresh.loaded_root.verification.root_record_sha256
        != earned.loaded_root.verification.root_record_sha256
    ):
        raise ChromiumResearchThirdBasisEpochReentryPlanCheckpointError(
            "Fresh third-root identity does not match the earned third epoch."
        )
    if fresh.controller.presentation != earned.controller.presentation:
        raise ChromiumResearchThirdBasisEpochReentryPlanCheckpointError(
            "Fresh third-epoch governed presentation does not match the earned session."
        )
    if (
        fresh.controller.declared_endpoint.verification.edge_record_sha256
        != earned.controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchThirdBasisEpochReentryPlanCheckpointError(
            "Fresh third-epoch endpoint identity does not match the earned session."
        )


def _persist_overlay_document(
    plan: ChromiumResearchThirdBasisEpochReentryPlan,
    *,
    destination: Path,
) -> ChromiumResearchThirdBasisEpochReentryPlanDocumentPersistenceResult:
    base = destination.parent
    document: dict[str, object] = {
        "format": _OVERLAY_FORMAT,
        "prior_second_basis_epoch_continuation_overlay_source": _encode_path(
            plan.prior_second_basis_epoch_continuation_overlay_source,
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
        raise ChromiumResearchThirdBasisEpochReentryPlanDocumentError(
            "Third-basis-epoch re-entry overlay destination already exists."
        ) from exc
    except OSError as exc:
        raise ChromiumResearchThirdBasisEpochReentryPlanDocumentError(
            "Third-basis-epoch re-entry overlay could not be written."
        ) from exc

    return ChromiumResearchThirdBasisEpochReentryPlanDocumentPersistenceResult(
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
    raise ChromiumResearchThirdBasisEpochReentryPlanDocumentError(
        f"{label} keys are invalid: {'; '.join(details)}."
    )


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ChromiumResearchThirdBasisEpochReentryPlanDocumentError(
                f"Duplicate JSON object key is not allowed: {key!r}."
            )
        result[key] = value
    return result


__all__ = [
    "ChromiumResearchThirdBasisEpochReentryPlanCheckpointError",
    "ChromiumResearchThirdBasisEpochReentryPlanCheckpointResult",
    "ChromiumResearchThirdBasisEpochReentryPlanDocumentError",
    "ChromiumResearchThirdBasisEpochReentryPlanDocumentPersistenceResult",
    "load_chromium_research_third_basis_epoch_reentry_plan_document",
    "persist_chromium_research_third_basis_epoch_reentry_plan_document",
]
