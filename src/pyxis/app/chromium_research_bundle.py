from __future__ import annotations

from dataclasses import dataclass

from pyxis.browser import ChromiumReadError

from .chromium_headings import (
    ChromiumPageHeadingsEvidence,
    observe_chromium_page_headings,
)
from .chromium_lists import ChromiumPageListsEvidence, observe_chromium_page_lists
from .chromium_metadata import (
    ChromiumPageMetadataEvidence,
    observe_chromium_page_metadata,
)
from .chromium_observation import (
    ChromiumPageLinksEvidence,
    ChromiumPageObservationEvidence,
    observe_chromium_page,
    observe_chromium_page_links,
)
from .chromium_paragraphs import (
    ChromiumPageParagraphsEvidence,
    observe_chromium_page_paragraphs,
)
from .chromium_tables import ChromiumPageTablesEvidence, observe_chromium_page_tables


_ACQUISITION_ORDER = (
    "page",
    "links",
    "headings",
    "metadata",
    "paragraphs",
    "tables",
    "lists",
)


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchEvidenceBundle:
    """One ordered, non-atomic bundle of already-proven page evidence families."""

    endpoint: str
    target_id: str
    url: str
    acquisition_mode: str
    acquisition_order: tuple[str, ...]
    page: ChromiumPageObservationEvidence
    links: ChromiumPageLinksEvidence
    headings: ChromiumPageHeadingsEvidence
    metadata: ChromiumPageMetadataEvidence
    paragraphs: ChromiumPageParagraphsEvidence
    tables: ChromiumPageTablesEvidence
    lists: ChromiumPageListsEvidence


def observe_chromium_page_research_bundle(
    endpoint: str,
    *,
    target_id: str | None = None,
    timeout: float = 5.0,
) -> ChromiumPageResearchEvidenceBundle:
    """Compose the seven proven read-only Chromium evidence families.

    The first page observation selects the target under the existing 15A rules.
    Every later observation reuses that exact target id. Acquisition is deliberately
    sequential and therefore not an atomic DOM snapshot. Pyxis requires every
    returned evidence object to retain the same normalized endpoint, exact target
    id, and exact page URL before it will emit a bundle, but same-URL DOM mutation
    may still occur between reads and is not hidden by this contract.

    This convenience boundary adds no navigation, persistence, interpretation,
    source verification, citation authority, browser-control authority, or new
    bundle-wide limit policy. Each constituent observer keeps its established
    bounded defaults and remains independently usable.
    """

    page = observe_chromium_page(
        endpoint,
        target_id=target_id,
        timeout=timeout,
    )
    normalized_endpoint = page.endpoint
    selected_target_id = page.target_id
    selected_url = page.url

    links = observe_chromium_page_links(
        normalized_endpoint,
        target_id=selected_target_id,
        timeout=timeout,
    )
    _require_coherent_member("links", links, page)

    headings = observe_chromium_page_headings(
        normalized_endpoint,
        target_id=selected_target_id,
        timeout=timeout,
    )
    _require_coherent_member("headings", headings, page)

    metadata = observe_chromium_page_metadata(
        normalized_endpoint,
        target_id=selected_target_id,
        timeout=timeout,
    )
    _require_coherent_member("metadata", metadata, page)

    paragraphs = observe_chromium_page_paragraphs(
        normalized_endpoint,
        target_id=selected_target_id,
        timeout=timeout,
    )
    _require_coherent_member("paragraphs", paragraphs, page)

    tables = observe_chromium_page_tables(
        normalized_endpoint,
        target_id=selected_target_id,
        timeout=timeout,
    )
    _require_coherent_member("tables", tables, page)

    lists = observe_chromium_page_lists(
        normalized_endpoint,
        target_id=selected_target_id,
        timeout=timeout,
    )
    _require_coherent_member("lists", lists, page)

    return ChromiumPageResearchEvidenceBundle(
        endpoint=normalized_endpoint,
        target_id=selected_target_id,
        url=selected_url,
        acquisition_mode="sequential_non_atomic_url_coherent",
        acquisition_order=_ACQUISITION_ORDER,
        page=page,
        links=links,
        headings=headings,
        metadata=metadata,
        paragraphs=paragraphs,
        tables=tables,
        lists=lists,
    )


def _require_coherent_member(
    name: str,
    evidence: object,
    page: ChromiumPageObservationEvidence,
) -> None:
    endpoint = getattr(evidence, "endpoint", None)
    target_id = getattr(evidence, "target_id", None)
    url = getattr(evidence, "url", None)

    if endpoint != page.endpoint:
        raise ChromiumReadError(
            f"Chromium research bundle {name} evidence changed endpoint during acquisition."
        )
    if target_id != page.target_id:
        raise ChromiumReadError(
            f"Chromium research bundle {name} evidence changed target during acquisition."
        )
    if url != page.url:
        raise ChromiumReadError(
            "Chromium page URL changed during sequential research-bundle acquisition; "
            f"{name} observed {url!r} after the initial page observed {page.url!r}."
        )
