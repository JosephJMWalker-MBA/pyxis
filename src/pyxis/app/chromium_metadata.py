from __future__ import annotations

from dataclasses import dataclass

from pyxis.browser import (
    ChromiumPageMetadataSnapshot,
    ChromiumReadError,
    list_chromium_page_targets,
    normalize_chromium_endpoint,
    read_chromium_page_metadata,
)

from .chromium_observation import _select_page_target


@dataclass(frozen=True, slots=True)
class ChromiumCanonicalLinkEvidence:
    """One literal page-declared canonical-link fact."""

    ordinal: int
    raw_href: str
    resolved_href: str


@dataclass(frozen=True, slots=True)
class ChromiumMetaDescriptionEvidence:
    """One literal page-declared meta-description fact."""

    ordinal: int
    content_prefix: str
    content_character_count: int
    content_limit: int
    truncated: bool


@dataclass(frozen=True, slots=True)
class ChromiumPageMetadataEvidence:
    """Bounded page-declared metadata from one explicit Chromium page."""

    endpoint: str
    target_id: str
    url: str
    document_language: str
    language_source: str
    canonical_source: str
    canonical_links: tuple[ChromiumCanonicalLinkEvidence, ...]
    canonical_link_count: int
    canonical_link_limit: int
    canonical_links_truncated: bool
    description_source: str
    descriptions: tuple[ChromiumMetaDescriptionEvidence, ...]
    description_count: int
    description_limit: int
    descriptions_truncated: bool


def observe_chromium_page_metadata(
    endpoint: str,
    *,
    target_id: str | None = None,
    canonical_link_limit: int = 8,
    description_limit: int = 8,
    description_text_limit: int = 512,
    timeout: float = 5.0,
) -> ChromiumPageMetadataEvidence:
    """Observe page-declared metadata without treating declarations as verified truth.

    Duplicate or conflicting canonical links and descriptions remain visible.
    Document language is preserved as authored and is not validated or normalized.
    The operation does not choose a canonical identity, fetch destinations,
    navigate, persist, rank, summarize, or interpret the declarations.
    """

    normalized_endpoint = normalize_chromium_endpoint(endpoint)
    targets = list_chromium_page_targets(normalized_endpoint, timeout=timeout)
    target = _select_page_target(targets, target_id=target_id)
    snapshot = read_chromium_page_metadata(
        target,
        canonical_link_limit=canonical_link_limit,
        description_limit=description_limit,
        description_text_limit=description_text_limit,
        timeout=timeout,
    )
    return _create_metadata_observation(
        endpoint=normalized_endpoint,
        target_id=target.target_id,
        snapshot=snapshot,
        canonical_link_limit=canonical_link_limit,
        description_limit=description_limit,
        description_text_limit=description_text_limit,
    )


def _create_metadata_observation(
    *,
    endpoint: str,
    target_id: str,
    snapshot: ChromiumPageMetadataSnapshot,
    canonical_link_limit: int,
    description_limit: int,
    description_text_limit: int,
) -> ChromiumPageMetadataEvidence:
    if canonical_link_limit < 0:
        raise ValueError("canonical_link_limit must be >= 0.")
    if description_limit < 0:
        raise ValueError("description_limit must be >= 0.")
    if description_text_limit < 0:
        raise ValueError("description_text_limit must be >= 0.")
    if len(snapshot.canonical_links) > canonical_link_limit:
        raise ChromiumReadError(
            "Chromium metadata exceeded the requested canonical-link limit."
        )
    if snapshot.canonical_link_count < len(snapshot.canonical_links):
        raise ChromiumReadError(
            "Chromium metadata canonical-link count is smaller than the returned declarations."
        )
    if len(snapshot.descriptions) > description_limit:
        raise ChromiumReadError(
            "Chromium metadata exceeded the requested description limit."
        )
    if snapshot.description_count < len(snapshot.descriptions):
        raise ChromiumReadError(
            "Chromium metadata description count is smaller than the returned declarations."
        )

    canonical_links: list[ChromiumCanonicalLinkEvidence] = []
    for expected_ordinal, declaration in enumerate(snapshot.canonical_links, start=1):
        if declaration.ordinal != expected_ordinal:
            raise ChromiumReadError(
                "Chromium canonical-link evidence ordinals were not contiguous DOM order."
            )
        canonical_links.append(
            ChromiumCanonicalLinkEvidence(
                ordinal=declaration.ordinal,
                raw_href=declaration.raw_href,
                resolved_href=declaration.resolved_href,
            )
        )

    descriptions: list[ChromiumMetaDescriptionEvidence] = []
    for expected_ordinal, declaration in enumerate(snapshot.descriptions, start=1):
        if declaration.ordinal != expected_ordinal:
            raise ChromiumReadError(
                "Chromium meta-description evidence ordinals were not contiguous DOM order."
            )
        if len(declaration.content_prefix) > description_text_limit:
            raise ChromiumReadError(
                "Chromium meta-description exceeded the requested text limit."
            )
        if declaration.content_character_count < len(declaration.content_prefix):
            raise ChromiumReadError(
                "Chromium meta-description count is smaller than the returned prefix."
            )
        descriptions.append(
            ChromiumMetaDescriptionEvidence(
                ordinal=declaration.ordinal,
                content_prefix=declaration.content_prefix,
                content_character_count=declaration.content_character_count,
                content_limit=description_text_limit,
                truncated=declaration.content_truncated,
            )
        )

    return ChromiumPageMetadataEvidence(
        endpoint=endpoint,
        target_id=target_id,
        url=snapshot.url,
        document_language=snapshot.document_language,
        language_source="document.documentElement.getAttribute('lang')",
        canonical_source="document.querySelectorAll(\"link[rel~='canonical' i][href]\")",
        canonical_links=tuple(canonical_links),
        canonical_link_count=snapshot.canonical_link_count,
        canonical_link_limit=canonical_link_limit,
        canonical_links_truncated=snapshot.canonical_links_truncated,
        description_source="document.querySelectorAll(\"meta[name='description' i]\")",
        descriptions=tuple(descriptions),
        description_count=snapshot.description_count,
        description_limit=description_limit,
        descriptions_truncated=snapshot.descriptions_truncated,
    )
