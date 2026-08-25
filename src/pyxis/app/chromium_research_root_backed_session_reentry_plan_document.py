from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any

from .chromium_research_root_backed_session_reentry import (
    ChromiumResearchRootBackedSessionReentryPlan,
    ChromiumResearchRootBackedSessionReentryResult,
    create_chromium_research_root_backed_session_reentry_plan,
    reenter_chromium_research_root_backed_session,
)
from .chromium_research_session_reentry_plan_document import (
    ChromiumResearchSessionReentryPlanDocumentError,
    _decode_member,
    _decode_path,
    _decode_path_array,
    _encode_member,
    _encode_path,
    load_chromium_research_session_reentry_plan_document,
)


_OVERLAY_FORMAT = (
    "pyxis.chromium.research_root_backed_session_reentry_locator_overlay.v1"
)
_ROOT_KEYS = {
    "format",
    "prior_session_plan_source",
    "appended_working_set_members",
    "changed_working_set_source",
    "changed_note_source",
    "transition_source",
    "root_source",
    "declared_edge_sources",
    "declaration_source",
}


@dataclass(frozen=True, slots=True)
class ChromiumResearchRootBackedSessionReentryPlanDocumentPersistenceResult:
    """One no-overwrite 35C overlay write after fresh session proof.

    `plan` is the exact 35B typed plan represented by the overlay. The ordinary
    pre-change locator lineage remains in the separately supplied 31B v1 plan
    document at `prior_session_plan_source`; the overlay stores only that explicit
    plan-document location plus the changed-basis/root/declaration locator layer.

    The document is operational configuration only. It stores no evidence digest,
    timestamp, current/latest/head marker, branch identity, or semantic-support
    claim.
    """

    plan: ChromiumResearchRootBackedSessionReentryPlan
    prior_session_plan_source: Path
    path: Path


@dataclass(frozen=True, slots=True)
class ChromiumResearchRootBackedSessionReentryPlanCheckpointResult:
    """One proven 35B session checkpointed as a strict 35C overlay document.

    `reentry` is the already-earned root-backed session supplied by the caller.
    `fresh_reentry` is a new reconstruction performed immediately before the write
    from the ordinary plan document plus overlay locators. `persistence` is written
    only after the two governed-session presentations and durable endpoint/root
    identities agree.
    """

    reentry: ChromiumResearchRootBackedSessionReentryResult
    plan: ChromiumResearchRootBackedSessionReentryPlan
    fresh_reentry: ChromiumResearchRootBackedSessionReentryResult
    persistence: ChromiumResearchRootBackedSessionReentryPlanDocumentPersistenceResult


class ChromiumResearchRootBackedSessionReentryPlanDocumentError(ValueError):
    """Raised when one 35C root-backed overlay document is malformed or incoherent."""


class ChromiumResearchRootBackedSessionReentryPlanCheckpointError(ValueError):
    """Raised when one 35B session cannot be proven before 35C checkpointing."""


def load_chromium_research_root_backed_session_reentry_plan_document(
    source: Path,
) -> ChromiumResearchRootBackedSessionReentryPlan:
    """Decode one strict 35C overlay into the established 35B typed plan.

    The overlay is locator-only operational configuration. Loading it reads the
    overlay itself and the explicitly referenced ordinary 31B v1 plan document, but
    it does not read or verify the research artifacts named by either plan. It does
    not perform directory scanning, digest discovery, predecessor search, browser
    work, chronology inference, or current/latest/head selection.

    Relative paths are interpreted only relative to the overlay document's parent.
    The referenced ordinary plan is decoded through the existing 31B loader rather
    than copied into a second schema.
    """

    if not isinstance(source, Path):
        raise TypeError("source must be pathlib.Path.")

    try:
        raw_text = source.read_text(encoding="utf-8")
    except OSError as exc:
        raise ChromiumResearchRootBackedSessionReentryPlanDocumentError(
            "Root-backed re-entry overlay document could not be read."
        ) from exc

    try:
        document = json.loads(raw_text, object_pairs_hook=_unique_object)
    except (
        json.JSONDecodeError,
        ChromiumResearchRootBackedSessionReentryPlanDocumentError,
    ) as exc:
        if isinstance(exc, ChromiumResearchRootBackedSessionReentryPlanDocumentError):
            raise
        raise ChromiumResearchRootBackedSessionReentryPlanDocumentError(
            "Root-backed re-entry overlay document is not valid JSON."
        ) from exc

    if not isinstance(document, dict):
        raise ChromiumResearchRootBackedSessionReentryPlanDocumentError(
            "Root-backed re-entry overlay document must be one JSON object."
        )
    _require_exact_keys(document, _ROOT_KEYS, label="overlay document")

    if document["format"] != _OVERLAY_FORMAT:
        raise ChromiumResearchRootBackedSessionReentryPlanDocumentError(
            "Root-backed re-entry overlay document uses an unsupported format."
        )

    base = source.resolve().parent
    try:
        prior_plan_source = _decode_path(
            document["prior_session_plan_source"],
            "prior_session_plan_source",
            base,
        )
        prior_plan = load_chromium_research_session_reentry_plan_document(
            prior_plan_source
        )
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchRootBackedSessionReentryPlanDocumentError(
            "Referenced ordinary re-entry plan document could not be decoded."
        ) from exc

    raw_members = document["appended_working_set_members"]
    if not isinstance(raw_members, list) or not raw_members:
        raise ChromiumResearchRootBackedSessionReentryPlanDocumentError(
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
        return create_chromium_research_root_backed_session_reentry_plan(
            prior_plan,
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
        raise ChromiumResearchRootBackedSessionReentryPlanDocumentError(
            "Root-backed re-entry overlay cannot form a valid explicit 35B locator plan."
        ) from exc


def persist_chromium_research_root_backed_session_reentry_plan_document(
    reentry: ChromiumResearchRootBackedSessionReentryResult,
    *,
    prior_session_plan_source: Path,
    destination: Path,
) -> ChromiumResearchRootBackedSessionReentryPlanCheckpointResult:
    """Freshly prove and checkpoint one earned 35B session as a 35C overlay.

    The caller supplies the exact ordinary 31B plan-document location to compose and
    the destination for the new overlay. Pyxis first decodes that ordinary plan and
    requires it to equal the prior plan retained by the earned 35B result. It then
    reconstructs a candidate 35B plan using only that decoded ordinary plan plus the
    overlay locator layer already present in `reentry.plan`.

    Before any overlay write, Pyxis freshly re-enters the candidate plan and requires
    its governed presentation, declared endpoint content identity, and 34A root
    content identity to match the already-earned session. Only then is the strict
    no-overwrite overlay written and round-trip decoded.

    This does not authenticate paths, infer a global head, discover moved files, or
    upgrade operational configuration into research evidence.
    """

    if not isinstance(reentry, ChromiumResearchRootBackedSessionReentryResult):
        raise TypeError(
            "reentry must be ChromiumResearchRootBackedSessionReentryResult."
        )
    if not isinstance(prior_session_plan_source, Path):
        raise TypeError("prior_session_plan_source must be pathlib.Path.")
    if not isinstance(destination, Path):
        raise TypeError("destination must be pathlib.Path.")

    prior_source = prior_session_plan_source
    overlay_destination = destination.resolve()

    try:
        decoded_prior_plan = load_chromium_research_session_reentry_plan_document(
            prior_source
        )
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchRootBackedSessionReentryPlanCheckpointError(
            "Explicit ordinary prior-session plan document could not be decoded."
        ) from exc

    if decoded_prior_plan != reentry.plan.prior_session_plan:
        raise ChromiumResearchRootBackedSessionReentryPlanCheckpointError(
            "Explicit ordinary prior-session plan document does not match the earned 35B session lineage."
        )

    candidate_plan = create_chromium_research_root_backed_session_reentry_plan(
        decoded_prior_plan,
        reentry.plan.appended_working_set_members,
        changed_working_set_source=reentry.plan.changed_working_set_source,
        changed_note_source=reentry.plan.changed_note_source,
        transition_source=reentry.plan.transition_source,
        root_source=reentry.plan.root_source,
        declared_edge_sources=reentry.plan.declared_edge_sources,
        declaration_source=reentry.plan.declaration_source,
    )

    try:
        fresh_reentry = reenter_chromium_research_root_backed_session(candidate_plan)
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchRootBackedSessionReentryPlanCheckpointError(
            "Candidate root-backed overlay locations could not freshly reconstruct a governed session."
        ) from exc

    _require_fresh_session_match(reentry, fresh_reentry)

    persistence = _persist_overlay_document(
        candidate_plan,
        prior_session_plan_source=prior_source,
        destination=overlay_destination,
    )

    try:
        decoded_overlay = load_chromium_research_root_backed_session_reentry_plan_document(
            persistence.path
        )
    except (OSError, TypeError, ValueError) as exc:
        raise ChromiumResearchRootBackedSessionReentryPlanCheckpointError(
            "Persisted root-backed overlay could not be round-trip decoded."
        ) from exc
    if decoded_overlay != candidate_plan:
        raise ChromiumResearchRootBackedSessionReentryPlanCheckpointError(
            "Persisted root-backed overlay did not round-trip to the exact candidate plan."
        )

    return ChromiumResearchRootBackedSessionReentryPlanCheckpointResult(
        reentry=reentry,
        plan=candidate_plan,
        fresh_reentry=fresh_reentry,
        persistence=persistence,
    )


def _require_fresh_session_match(
    earned: ChromiumResearchRootBackedSessionReentryResult,
    fresh: ChromiumResearchRootBackedSessionReentryResult,
) -> None:
    if fresh.controller.presentation != earned.controller.presentation:
        raise ChromiumResearchRootBackedSessionReentryPlanCheckpointError(
            "Fresh overlay re-entry presentation does not match the earned root-backed session."
        )
    if (
        fresh.controller.declared_endpoint.verification.edge_record_sha256
        != earned.controller.declared_endpoint.verification.edge_record_sha256
    ):
        raise ChromiumResearchRootBackedSessionReentryPlanCheckpointError(
            "Fresh overlay re-entry endpoint identity does not match the earned root-backed session."
        )
    if (
        fresh.loaded_root.verification.root_record_sha256
        != earned.loaded_root.verification.root_record_sha256
    ):
        raise ChromiumResearchRootBackedSessionReentryPlanCheckpointError(
            "Fresh overlay re-entry root identity does not match the earned root-backed session."
        )


def _persist_overlay_document(
    plan: ChromiumResearchRootBackedSessionReentryPlan,
    *,
    prior_session_plan_source: Path,
    destination: Path,
) -> ChromiumResearchRootBackedSessionReentryPlanDocumentPersistenceResult:
    base = destination.parent
    document: dict[str, object] = {
        "format": _OVERLAY_FORMAT,
        "prior_session_plan_source": _encode_path(prior_session_plan_source, base),
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
        raise ChromiumResearchRootBackedSessionReentryPlanDocumentError(
            "Root-backed re-entry overlay destination already exists."
        ) from exc
    except OSError as exc:
        raise ChromiumResearchRootBackedSessionReentryPlanDocumentError(
            "Root-backed re-entry overlay document could not be written."
        ) from exc

    return ChromiumResearchRootBackedSessionReentryPlanDocumentPersistenceResult(
        plan=plan,
        prior_session_plan_source=prior_session_plan_source,
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
    raise ChromiumResearchRootBackedSessionReentryPlanDocumentError(
        f"{label} keys are invalid: {'; '.join(details)}."
    )


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ChromiumResearchRootBackedSessionReentryPlanDocumentError(
                f"Duplicate JSON object key is not allowed: {key!r}."
            )
        result[key] = value
    return result


__all__ = [
    "ChromiumResearchRootBackedSessionReentryPlanCheckpointError",
    "ChromiumResearchRootBackedSessionReentryPlanCheckpointResult",
    "ChromiumResearchRootBackedSessionReentryPlanDocumentError",
    "ChromiumResearchRootBackedSessionReentryPlanDocumentPersistenceResult",
    "load_chromium_research_root_backed_session_reentry_plan_document",
    "persist_chromium_research_root_backed_session_reentry_plan_document",
]
