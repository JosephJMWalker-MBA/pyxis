from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
import importlib

import pytest

from pyxis.app.chromium_headings import ChromiumPageHeadingsEvidence
from pyxis.app.chromium_lists import ChromiumPageListsEvidence
from pyxis.app.chromium_metadata import ChromiumPageMetadataEvidence
from pyxis.app.chromium_observation import (
    ChromiumPageContentEvidence,
    ChromiumPageLinksEvidence,
    ChromiumPageObservationEvidence,
)
from pyxis.app.chromium_paragraphs import ChromiumPageParagraphsEvidence
from pyxis.app.chromium_research_bundle import observe_chromium_page_research_bundle
from pyxis.app.chromium_tables import ChromiumPageTablesEvidence
from pyxis.browser import ChromiumReadError


bundle_module = importlib.import_module("pyxis.app.chromium_research_bundle")


ENDPOINT = "http://127.0.0.1:9222"
TARGET_ID = "page-1"
URL = "https://example.test/research"


def _members() -> tuple[
    ChromiumPageObservationEvidence,
    ChromiumPageLinksEvidence,
    ChromiumPageHeadingsEvidence,
    ChromiumPageMetadataEvidence,
    ChromiumPageParagraphsEvidence,
    ChromiumPageTablesEvidence,
    ChromiumPageListsEvidence,
]:
    page = ChromiumPageObservationEvidence(
        endpoint=ENDPOINT,
        target_id=TARGET_ID,
        url=URL,
        title="Research page",
        content=ChromiumPageContentEvidence(
            source="document.body.innerText",
            text_prefix="Body",
            text_character_count=4,
            text_limit=2048,
            truncated=False,
        ),
    )
    links = ChromiumPageLinksEvidence(
        endpoint=ENDPOINT,
        target_id=TARGET_ID,
        url=URL,
        source="document.querySelectorAll('a[href]')",
        links=(),
        link_count=0,
        link_limit=64,
        truncated=False,
    )
    headings = ChromiumPageHeadingsEvidence(
        endpoint=ENDPOINT,
        target_id=TARGET_ID,
        url=URL,
        source="document.querySelectorAll('h1,h2,h3,h4,h5,h6')",
        headings=(),
        heading_count=0,
        heading_limit=64,
        truncated=False,
    )
    metadata = ChromiumPageMetadataEvidence(
        endpoint=ENDPOINT,
        target_id=TARGET_ID,
        url=URL,
        document_language="en",
        language_source="document.documentElement.getAttribute('lang')",
        canonical_source="document.querySelectorAll('link[rel~='canonical' i]')",
        canonical_links=(),
        canonical_link_count=0,
        canonical_link_limit=8,
        canonical_links_truncated=False,
        description_source="document.querySelectorAll('meta[name='description' i]')",
        descriptions=(),
        description_count=0,
        description_limit=8,
        descriptions_truncated=False,
    )
    paragraphs = ChromiumPageParagraphsEvidence(
        endpoint=ENDPOINT,
        target_id=TARGET_ID,
        url=URL,
        source="document.querySelectorAll('p')",
        paragraphs=(),
        paragraph_count=0,
        paragraph_limit=128,
        truncated=False,
    )
    tables = ChromiumPageTablesEvidence(
        endpoint=ENDPOINT,
        target_id=TARGET_ID,
        url=URL,
        source="document.querySelectorAll('table')",
        tables=(),
        table_count=0,
        table_limit=32,
        truncated=False,
    )
    lists = ChromiumPageListsEvidence(
        endpoint=ENDPOINT,
        target_id=TARGET_ID,
        url=URL,
        source="document.querySelectorAll('ol,ul')",
        lists=(),
        list_count=0,
        list_limit=64,
        truncated=False,
    )
    return page, links, headings, metadata, paragraphs, tables, lists


def _install_observers(monkeypatch, members, calls: list[tuple]) -> None:
    page, links, headings, metadata, paragraphs, tables, lists = members

    def observe_page(endpoint: str, *, target_id: str | None, timeout: float):
        calls.append(("page", endpoint, target_id, timeout))
        return page

    def observer(name: str, evidence):
        def observe(endpoint: str, *, target_id: str | None, timeout: float):
            calls.append((name, endpoint, target_id, timeout))
            return evidence

        return observe

    monkeypatch.setattr(bundle_module, "observe_chromium_page", observe_page)
    monkeypatch.setattr(bundle_module, "observe_chromium_page_links", observer("links", links))
    monkeypatch.setattr(
        bundle_module,
        "observe_chromium_page_headings",
        observer("headings", headings),
    )
    monkeypatch.setattr(
        bundle_module,
        "observe_chromium_page_metadata",
        observer("metadata", metadata),
    )
    monkeypatch.setattr(
        bundle_module,
        "observe_chromium_page_paragraphs",
        observer("paragraphs", paragraphs),
    )
    monkeypatch.setattr(bundle_module, "observe_chromium_page_tables", observer("tables", tables))
    monkeypatch.setattr(bundle_module, "observe_chromium_page_lists", observer("lists", lists))


def test_research_bundle_composes_public_evidence_in_fixed_non_atomic_order(monkeypatch) -> None:
    members = _members()
    calls: list[tuple] = []
    _install_observers(monkeypatch, members, calls)

    evidence = observe_chromium_page_research_bundle(
        " http://caller.example:9222/ ",
        timeout=2.5,
    )

    assert evidence.endpoint == ENDPOINT
    assert evidence.target_id == TARGET_ID
    assert evidence.url == URL
    assert evidence.acquisition_mode == "sequential_non_atomic_url_coherent"
    assert evidence.acquisition_order == (
        "page",
        "links",
        "headings",
        "metadata",
        "paragraphs",
        "tables",
        "lists",
    )
    assert (
        evidence.page,
        evidence.links,
        evidence.headings,
        evidence.metadata,
        evidence.paragraphs,
        evidence.tables,
        evidence.lists,
    ) == members
    assert calls == [
        ("page", " http://caller.example:9222/ ", None, 2.5),
        ("links", ENDPOINT, TARGET_ID, 2.5),
        ("headings", ENDPOINT, TARGET_ID, 2.5),
        ("metadata", ENDPOINT, TARGET_ID, 2.5),
        ("paragraphs", ENDPOINT, TARGET_ID, 2.5),
        ("tables", ENDPOINT, TARGET_ID, 2.5),
        ("lists", ENDPOINT, TARGET_ID, 2.5),
    ]

    with pytest.raises(FrozenInstanceError):
        evidence.url = "changed"  # type: ignore[misc]


@pytest.mark.parametrize(
    ("replacement", "message"),
    [
        ({"endpoint": "http://different.example:9222"}, "changed endpoint"),
        ({"target_id": "page-2"}, "changed target"),
        ({"url": "https://example.test/changed"}, "URL changed"),
    ],
)
def test_research_bundle_rejects_incoherent_member_before_later_reads(
    monkeypatch,
    replacement,
    message,
) -> None:
    page, links, headings, metadata, paragraphs, tables, lists = _members()
    changed_links = replace(links, **replacement)
    calls: list[tuple] = []
    _install_observers(
        monkeypatch,
        (page, changed_links, headings, metadata, paragraphs, tables, lists),
        calls,
    )

    with pytest.raises(ChromiumReadError, match=message):
        observe_chromium_page_research_bundle(ENDPOINT)

    assert tuple(call[0] for call in calls) == ("page", "links")


def test_research_bundle_reuses_explicit_initial_target(monkeypatch) -> None:
    members = _members()
    calls: list[tuple] = []
    _install_observers(monkeypatch, members, calls)

    evidence = observe_chromium_page_research_bundle(
        ENDPOINT,
        target_id=TARGET_ID,
    )

    assert evidence.target_id == TARGET_ID
    assert calls[0][2] == TARGET_ID
    assert all(call[2] == TARGET_ID for call in calls[1:])
