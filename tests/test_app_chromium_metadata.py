from __future__ import annotations

from dataclasses import FrozenInstanceError
import importlib

import pytest

from pyxis.app import observe_chromium_page_metadata
from pyxis.browser import (
    ChromiumPageCanonicalLinkSnapshot,
    ChromiumPageDescriptionSnapshot,
    ChromiumPageMetadataSnapshot,
    ChromiumPageTarget,
    ChromiumReadError,
)


metadata_module = importlib.import_module("pyxis.app.chromium_metadata")


def test_observe_chromium_page_metadata_projects_frozen_literal_evidence(monkeypatch) -> None:
    target = ChromiumPageTarget("page-1", "ws://devtools/page/page-1")
    snapshot = ChromiumPageMetadataSnapshot(
        url="https://example.test/article",
        document_language="EN-us",
        canonical_links=(
            ChromiumPageCanonicalLinkSnapshot(1, "/article", "https://example.test/article"),
            ChromiumPageCanonicalLinkSnapshot(2, "https://mirror.test/item", "https://mirror.test/item"),
        ),
        canonical_link_count=3,
        descriptions=(
            ChromiumPageDescriptionSnapshot(1, "Study 😀", 16),
        ),
        description_count=2,
    )
    calls: list[tuple] = []

    def fake_list(endpoint: str, *, timeout: float):
        calls.append(("list", endpoint, timeout))
        return (target,)

    def fake_read(
        selected,
        *,
        canonical_link_limit: int,
        description_limit: int,
        description_text_limit: int,
        timeout: float,
    ):
        calls.append(
            (
                "read",
                selected,
                canonical_link_limit,
                description_limit,
                description_text_limit,
                timeout,
            )
        )
        return snapshot

    monkeypatch.setattr(metadata_module, "list_chromium_page_targets", fake_list)
    monkeypatch.setattr(metadata_module, "read_chromium_page_metadata", fake_read)

    evidence = observe_chromium_page_metadata(
        " http://127.0.0.1:9222/ ",
        canonical_link_limit=2,
        description_limit=1,
        description_text_limit=7,
        timeout=2.0,
    )

    assert evidence.endpoint == "http://127.0.0.1:9222"
    assert evidence.target_id == "page-1"
    assert evidence.url == "https://example.test/article"
    assert evidence.document_language == "EN-us"
    assert evidence.language_source == "document.documentElement.getAttribute('lang')"
    assert evidence.canonical_link_count == 3
    assert evidence.canonical_link_limit == 2
    assert evidence.canonical_links_truncated is True
    assert evidence.canonical_links[0].raw_href == "/article"
    assert evidence.canonical_links[0].resolved_href == "https://example.test/article"
    assert evidence.canonical_links[1].resolved_href == "https://mirror.test/item"
    assert evidence.description_count == 2
    assert evidence.description_limit == 1
    assert evidence.descriptions_truncated is True
    assert evidence.descriptions[0].content_prefix == "Study 😀"
    assert evidence.descriptions[0].content_character_count == 16
    assert evidence.descriptions[0].content_limit == 7
    assert evidence.descriptions[0].truncated is True
    assert calls == [
        ("list", "http://127.0.0.1:9222", 2.0),
        ("read", target, 2, 1, 7, 2.0),
    ]

    with pytest.raises(FrozenInstanceError):
        evidence.document_language = "en"  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        evidence.canonical_links[0].raw_href = "/changed"  # type: ignore[misc]


def test_observe_chromium_page_metadata_refuses_ambiguous_target_before_read(monkeypatch) -> None:
    targets = (
        ChromiumPageTarget("page-1", "ws://devtools/page/page-1"),
        ChromiumPageTarget("page-2", "ws://devtools/page/page-2"),
    )
    monkeypatch.setattr(
        metadata_module,
        "list_chromium_page_targets",
        lambda endpoint, *, timeout: targets,
    )

    def fail_if_read(*args, **kwargs):
        raise AssertionError("Ambiguous target selection must fail before metadata read.")

    monkeypatch.setattr(metadata_module, "read_chromium_page_metadata", fail_if_read)

    with pytest.raises(ChromiumReadError, match="supply target_id explicitly"):
        observe_chromium_page_metadata("http://127.0.0.1:9222")


def test_observe_chromium_page_metadata_preserves_conflicting_declarations(monkeypatch) -> None:
    target = ChromiumPageTarget("page-1", "ws://devtools/page/page-1")
    monkeypatch.setattr(
        metadata_module,
        "list_chromium_page_targets",
        lambda endpoint, *, timeout: (target,),
    )
    monkeypatch.setattr(
        metadata_module,
        "read_chromium_page_metadata",
        lambda selected, **kwargs: ChromiumPageMetadataSnapshot(
            url="https://example.test/article",
            document_language="not-normalized",
            canonical_links=(
                ChromiumPageCanonicalLinkSnapshot(1, "/one", "https://example.test/one"),
                ChromiumPageCanonicalLinkSnapshot(2, "/two", "https://example.test/two"),
            ),
            canonical_link_count=2,
            descriptions=(
                ChromiumPageDescriptionSnapshot(1, "First description", 17),
                ChromiumPageDescriptionSnapshot(2, "Second description", 18),
            ),
            description_count=2,
        ),
    )

    evidence = observe_chromium_page_metadata("http://127.0.0.1:9222")

    assert evidence.document_language == "not-normalized"
    assert tuple(item.raw_href for item in evidence.canonical_links) == ("/one", "/two")
    assert tuple(item.content_prefix for item in evidence.descriptions) == (
        "First description",
        "Second description",
    )
