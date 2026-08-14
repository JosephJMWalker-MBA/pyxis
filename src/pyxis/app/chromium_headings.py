from __future__ import annotations

from dataclasses import dataclass

from pyxis.browser import (
    ChromiumPageHeadingsSnapshot,
    ChromiumReadError,
    list_chromium_page_targets,
    normalize_chromium_endpoint,
    read_chromium_page_headings,
)

from .chromium_observation import _select_page_target


@dataclass(frozen=True, slots=True)
class ChromiumPageHeadingEvidence:
    """One read-only DOM-order heading marker observed on an existing page."""

    ordinal: int
    level: int
    text_prefix: str
    text_character_count: int
    text_limit: int
    truncated: bool


@dataclass(frozen=True, slots=True)
class ChromiumPageHeadingsEvidence:
    """Bounded heading-outline evidence acquired from one explicit Chromium page."""

    endpoint: str
    target_id: str
    url: str
    source: str
    headings: tuple[ChromiumPageHeadingEvidence, ...]
    heading_count: int
    heading_limit: int
    truncated: bool


def observe_chromium_page_headings(
    endpoint: str,
    *,
    target_id: str | None = None,
    heading_limit: int = 64,
    heading_text_limit: int = 256,
    timeout: float = 5.0,
) -> ChromiumPageHeadingsEvidence:
    """Observe h1-h6 markers without summarizing or inferring a hierarchy.

    Evidence preserves exact DOM order, explicit HTML heading levels, and bounded
    `innerText`. Skipped heading levels remain skipped; Pyxis does not repair,
    score, rank, summarize, navigate, persist, or interpret the outline.
    """

    normalized_endpoint = normalize_chromium_endpoint(endpoint)
    targets = list_chromium_page_targets(normalized_endpoint, timeout=timeout)
    target = _select_page_target(targets, target_id=target_id)
    snapshot = read_chromium_page_headings(
        target,
        heading_limit=heading_limit,
        heading_text_limit=heading_text_limit,
        timeout=timeout,
    )
    return _create_headings_observation(
        endpoint=normalized_endpoint,
        target_id=target.target_id,
        snapshot=snapshot,
        heading_limit=heading_limit,
        heading_text_limit=heading_text_limit,
    )


def _create_headings_observation(
    *,
    endpoint: str,
    target_id: str,
    snapshot: ChromiumPageHeadingsSnapshot,
    heading_limit: int,
    heading_text_limit: int,
) -> ChromiumPageHeadingsEvidence:
    if heading_limit < 0:
        raise ValueError("heading_limit must be >= 0.")
    if heading_text_limit < 0:
        raise ValueError("heading_text_limit must be >= 0.")
    if len(snapshot.headings) > heading_limit:
        raise ChromiumReadError(
            "Chromium headings snapshot exceeded the requested heading limit."
        )
    if snapshot.heading_count < len(snapshot.headings):
        raise ChromiumReadError(
            "Chromium headings snapshot count is smaller than the returned headings."
        )

    headings: list[ChromiumPageHeadingEvidence] = []
    for expected_ordinal, heading in enumerate(snapshot.headings, start=1):
        if heading.ordinal != expected_ordinal:
            raise ChromiumReadError(
                "Chromium heading evidence ordinals were not contiguous DOM order."
            )
        if not 1 <= heading.level <= 6:
            raise ChromiumReadError(
                "Chromium heading evidence level was not from 1 through 6."
            )
        if len(heading.text_prefix) > heading_text_limit:
            raise ChromiumReadError(
                "Chromium heading snapshot exceeded the requested text limit."
            )
        if heading.text_character_count < len(heading.text_prefix):
            raise ChromiumReadError(
                "Chromium heading snapshot text count is smaller than the returned prefix."
            )
        headings.append(
            ChromiumPageHeadingEvidence(
                ordinal=heading.ordinal,
                level=heading.level,
                text_prefix=heading.text_prefix,
                text_character_count=heading.text_character_count,
                text_limit=heading_text_limit,
                truncated=heading.text_truncated,
            )
        )

    return ChromiumPageHeadingsEvidence(
        endpoint=endpoint,
        target_id=target_id,
        url=snapshot.url,
        source="document.querySelectorAll('h1,h2,h3,h4,h5,h6')",
        headings=tuple(headings),
        heading_count=snapshot.heading_count,
        heading_limit=heading_limit,
        truncated=snapshot.headings_truncated,
    )
