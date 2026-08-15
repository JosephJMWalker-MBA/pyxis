from __future__ import annotations

from dataclasses import dataclass

from pyxis.browser import (
    ChromiumPageParagraphsSnapshot,
    ChromiumReadError,
    list_chromium_page_targets,
    normalize_chromium_endpoint,
    read_chromium_page_paragraphs,
)

from .chromium_observation import _select_page_target


@dataclass(frozen=True, slots=True)
class ChromiumPageParagraphEvidence:
    """One literal DOM-order paragraph observed on an existing page."""

    ordinal: int
    element_id: str
    text_prefix: str
    text_character_count: int
    text_limit: int
    truncated: bool


@dataclass(frozen=True, slots=True)
class ChromiumPageParagraphsEvidence:
    """Bounded paragraph evidence acquired from one explicit Chromium page."""

    endpoint: str
    target_id: str
    url: str
    source: str
    paragraphs: tuple[ChromiumPageParagraphEvidence, ...]
    paragraph_count: int
    paragraph_limit: int
    truncated: bool


def observe_chromium_page_paragraphs(
    endpoint: str,
    *,
    target_id: str | None = None,
    paragraph_limit: int = 128,
    paragraph_text_limit: int = 1024,
    timeout: float = 5.0,
) -> ChromiumPageParagraphsEvidence:
    """Observe literal `<p>` elements without segmenting or interpreting passages.

    Evidence preserves DOM order, the authored element `id` exactly as present,
    and bounded `innerText`. Duplicate IDs remain duplicate and empty IDs remain
    empty. Pyxis does not infer sentence boundaries, citation stability,
    relevance, source quality, navigation authority, or semantic importance.
    """

    normalized_endpoint = normalize_chromium_endpoint(endpoint)
    targets = list_chromium_page_targets(normalized_endpoint, timeout=timeout)
    target = _select_page_target(targets, target_id=target_id)
    snapshot = read_chromium_page_paragraphs(
        target,
        paragraph_limit=paragraph_limit,
        paragraph_text_limit=paragraph_text_limit,
        timeout=timeout,
    )
    return _create_paragraphs_observation(
        endpoint=normalized_endpoint,
        target_id=target.target_id,
        snapshot=snapshot,
        paragraph_limit=paragraph_limit,
        paragraph_text_limit=paragraph_text_limit,
    )


def _create_paragraphs_observation(
    *,
    endpoint: str,
    target_id: str,
    snapshot: ChromiumPageParagraphsSnapshot,
    paragraph_limit: int,
    paragraph_text_limit: int,
) -> ChromiumPageParagraphsEvidence:
    if paragraph_limit < 0:
        raise ValueError("paragraph_limit must be >= 0.")
    if paragraph_text_limit < 0:
        raise ValueError("paragraph_text_limit must be >= 0.")
    if len(snapshot.paragraphs) > paragraph_limit:
        raise ChromiumReadError(
            "Chromium paragraphs snapshot exceeded the requested paragraph limit."
        )
    if snapshot.paragraph_count < len(snapshot.paragraphs):
        raise ChromiumReadError(
            "Chromium paragraphs snapshot count is smaller than the returned paragraphs."
        )

    paragraphs: list[ChromiumPageParagraphEvidence] = []
    for expected_ordinal, paragraph in enumerate(snapshot.paragraphs, start=1):
        if paragraph.ordinal != expected_ordinal:
            raise ChromiumReadError(
                "Chromium paragraph evidence ordinals were not contiguous DOM order."
            )
        if len(paragraph.text_prefix) > paragraph_text_limit:
            raise ChromiumReadError(
                "Chromium paragraph snapshot exceeded the requested text limit."
            )
        if paragraph.text_character_count < len(paragraph.text_prefix):
            raise ChromiumReadError(
                "Chromium paragraph text count is smaller than the returned prefix."
            )
        paragraphs.append(
            ChromiumPageParagraphEvidence(
                ordinal=paragraph.ordinal,
                element_id=paragraph.element_id,
                text_prefix=paragraph.text_prefix,
                text_character_count=paragraph.text_character_count,
                text_limit=paragraph_text_limit,
                truncated=paragraph.text_truncated,
            )
        )

    return ChromiumPageParagraphsEvidence(
        endpoint=endpoint,
        target_id=target_id,
        url=snapshot.url,
        source="document.querySelectorAll('p')",
        paragraphs=tuple(paragraphs),
        paragraph_count=snapshot.paragraph_count,
        paragraph_limit=paragraph_limit,
        truncated=snapshot.paragraphs_truncated,
    )
