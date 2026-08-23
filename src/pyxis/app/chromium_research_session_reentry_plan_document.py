from __future__ import annotations

from collections.abc import Iterable
import json
from pathlib import Path
from typing import Any

from .chromium_research_session_reentry import (
    ChromiumResearchComparisonNoteReentryLocator,
    ChromiumResearchExactRangeNoteReentryLocator,
    ChromiumResearchParagraphNoteReentryLocator,
    ChromiumResearchSessionReentryPlan,
    ChromiumResearchWorkingSetMemberReentryLocator,
    create_chromium_research_session_reentry_plan,
)


_PLAN_FORMAT = "pyxis.chromium.research_session_reentry_locator_plan.v1"
_ROOT_KEYS = {
    "format",
    "working_set_members",
    "working_set_source",
    "prior_note_source",
    "prior_revision_source",
    "continuation_source",
    "starting_predecessor_edge_sources",
    "declared_edge_sources",
    "declaration_source",
}


class ChromiumResearchSessionReentryPlanDocumentError(ValueError):
    """Raised when one operational re-entry locator document is malformed."""


def load_chromium_research_session_reentry_plan_document(
    source: Path,
) -> ChromiumResearchSessionReentryPlan:
    """Load one strict locator-only JSON document into the established 31A plan.

    This document is operational configuration, not research evidence. It stores
    only caller-supplied locations, member family labels, and explicit ordering.
    It stores no content digests and performs no referenced-file verification,
    directory scanning, digest search, predecessor discovery, head selection, or
    browser work. Relative locations are interpreted only relative to this plan
    document's directory before public 31A constructs the typed locator plan.
    """

    if not isinstance(source, Path):
        raise TypeError("source must be pathlib.Path.")

    try:
        raw_text = source.read_text(encoding="utf-8")
    except OSError as exc:
        raise ChromiumResearchSessionReentryPlanDocumentError(
            "Research-session re-entry plan document could not be read."
        ) from exc

    try:
        document = json.loads(raw_text, object_pairs_hook=_unique_object)
    except (json.JSONDecodeError, ChromiumResearchSessionReentryPlanDocumentError) as exc:
        if isinstance(exc, ChromiumResearchSessionReentryPlanDocumentError):
            raise
        raise ChromiumResearchSessionReentryPlanDocumentError(
            "Research-session re-entry plan document is not valid JSON."
        ) from exc

    if not isinstance(document, dict):
        raise ChromiumResearchSessionReentryPlanDocumentError(
            "Research-session re-entry plan document must be one JSON object."
        )
    _require_exact_keys(document, _ROOT_KEYS, label="plan document")

    if document["format"] != _PLAN_FORMAT:
        raise ChromiumResearchSessionReentryPlanDocumentError(
            "Research-session re-entry plan document uses an unsupported format."
        )

    base = source.resolve().parent
    raw_members = document["working_set_members"]
    if not isinstance(raw_members, list) or not raw_members:
        raise ChromiumResearchSessionReentryPlanDocumentError(
            "working_set_members must be a non-empty JSON array."
        )

    members = tuple(
        _decode_member(member, index=index, base=base)
        for index, member in enumerate(raw_members)
    )

    predecessor_sources = _decode_path_array(
        document["starting_predecessor_edge_sources"],
        label="starting_predecessor_edge_sources",
        base=base,
    )
    declared_sources = _decode_path_array(
        document["declared_edge_sources"],
        label="declared_edge_sources",
        base=base,
    )

    try:
        return create_chromium_research_session_reentry_plan(
            members,
            working_set_source=_decode_path(
                document["working_set_source"], "working_set_source", base
            ),
            prior_note_source=_decode_path(
                document["prior_note_source"], "prior_note_source", base
            ),
            prior_revision_source=_decode_path(
                document["prior_revision_source"], "prior_revision_source", base
            ),
            continuation_source=_decode_path(
                document["continuation_source"], "continuation_source", base
            ),
            starting_predecessor_edge_sources=predecessor_sources,
            declared_edge_sources=declared_sources,
            declaration_source=_decode_path(
                document["declaration_source"], "declaration_source", base
            ),
        )
    except (TypeError, ValueError) as exc:
        raise ChromiumResearchSessionReentryPlanDocumentError(
            "Research-session re-entry plan document cannot form a valid explicit 31A locator plan."
        ) from exc


def _decode_member(
    raw: object,
    *,
    index: int,
    base: Path,
) -> ChromiumResearchWorkingSetMemberReentryLocator:
    if not isinstance(raw, dict):
        raise ChromiumResearchSessionReentryPlanDocumentError(
            f"working_set_members[{index}] must be one JSON object."
        )

    kind = raw.get("kind")
    if kind == "paragraph_note":
        _require_exact_keys(
            raw,
            {"kind", "capture_source", "note_source"},
            label=f"working_set_members[{index}]",
        )
        return ChromiumResearchParagraphNoteReentryLocator(
            capture_source=_decode_path(
                raw["capture_source"],
                f"working_set_members[{index}].capture_source",
                base,
            ),
            note_source=_decode_path(
                raw["note_source"],
                f"working_set_members[{index}].note_source",
                base,
            ),
        )

    if kind == "exact_range_note":
        _require_exact_keys(
            raw,
            {"kind", "capture_source", "note_source"},
            label=f"working_set_members[{index}]",
        )
        return ChromiumResearchExactRangeNoteReentryLocator(
            capture_source=_decode_path(
                raw["capture_source"],
                f"working_set_members[{index}].capture_source",
                base,
            ),
            note_source=_decode_path(
                raw["note_source"],
                f"working_set_members[{index}].note_source",
                base,
            ),
        )

    if kind == "comparison_note":
        _require_exact_keys(
            raw,
            {
                "kind",
                "first_capture_source",
                "second_capture_source",
                "note_source",
            },
            label=f"working_set_members[{index}]",
        )
        return ChromiumResearchComparisonNoteReentryLocator(
            first_capture_source=_decode_path(
                raw["first_capture_source"],
                f"working_set_members[{index}].first_capture_source",
                base,
            ),
            second_capture_source=_decode_path(
                raw["second_capture_source"],
                f"working_set_members[{index}].second_capture_source",
                base,
            ),
            note_source=_decode_path(
                raw["note_source"],
                f"working_set_members[{index}].note_source",
                base,
            ),
        )

    raise ChromiumResearchSessionReentryPlanDocumentError(
        f"working_set_members[{index}].kind must be paragraph_note, exact_range_note, or comparison_note."
    )


def _decode_path_array(value: object, *, label: str, base: Path) -> tuple[Path, ...]:
    if not isinstance(value, list):
        raise ChromiumResearchSessionReentryPlanDocumentError(
            f"{label} must be a JSON array of explicit path strings."
        )
    return tuple(
        _decode_path(item, f"{label}[{index}]", base)
        for index, item in enumerate(value)
    )


def _decode_path(value: object, label: str, base: Path) -> Path:
    if type(value) is not str or not value:
        raise ChromiumResearchSessionReentryPlanDocumentError(
            f"{label} must be a non-empty path string."
        )
    path = Path(value)
    return path if path.is_absolute() else base / path


def _require_exact_keys(
    value: dict[str, Any],
    expected: Iterable[str],
    *,
    label: str,
) -> None:
    expected_keys = set(expected)
    observed_keys = set(value)
    if observed_keys != expected_keys:
        missing = sorted(expected_keys - observed_keys)
        unexpected = sorted(observed_keys - expected_keys)
        details: list[str] = []
        if missing:
            details.append(f"missing={missing}")
        if unexpected:
            details.append(f"unexpected={unexpected}")
        suffix = "; ".join(details)
        raise ChromiumResearchSessionReentryPlanDocumentError(
            f"{label} keys are invalid: {suffix}."
        )


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ChromiumResearchSessionReentryPlanDocumentError(
                f"Duplicate JSON object key is not allowed: {key!r}."
            )
        result[key] = value
    return result
