from __future__ import annotations

from dataclasses import FrozenInstanceError
import importlib

import pytest

from pyxis.app.chromium_observation import observe_chromium_page_links
from pyxis.browser import (
    ChromiumPageLinkSnapshot,
    ChromiumPageLinksSnapshot,
    ChromiumPageTarget,
    ChromiumReadError,
)


observation_module = importlib.import_module("pyxis.app.chromium_observation")


def test_observe_chromium_page_links_projects_frozen_bounded_evidence(monkeypatch) -> None:
    target = ChromiumPageTarget(
        target_id="page-1",
        websocket_debugger_url="ws://127.0.0.1:9222/devtools/page/page-1",
    )
    snapshot = ChromiumPageLinksSnapshot(
        url="https://example.test/research",
        links=(
            ChromiumPageLinkSnapshot(
                ordinal=1,
                href="https://example.test/first",
                text_prefix="First 😀",
                text_character_count=13,
            ),
            ChromiumPageLinkSnapshot(
                ordinal=2,
                href="mailto:research@example.test",
                text_prefix="Email",
                text_character_count=5,
            ),
        ),
        link_count=5,
    )
    calls: list[tuple] = []

    def fake_list(endpoint: str, *, timeout: float):
        calls.append(("list", endpoint, timeout))
        return (target,)

    def fake_read(selected, *, link_limit: int, link_text_limit: int, timeout: float):
        calls.append(("read", selected, link_limit, link_text_limit, timeout))
        return snapshot

    monkeypatch.setattr(observation_module, "list_chromium_page_targets", fake_list)
    monkeypatch.setattr(observation_module, "read_chromium_page_links", fake_read)

    evidence = observe_chromium_page_links(
        " http://127.0.0.1:9222/ ",
        link_limit=2,
        link_text_limit=7,
        timeout=2.0,
    )

    assert evidence.endpoint == "http://127.0.0.1:9222"
    assert evidence.target_id == "page-1"
    assert evidence.url == "https://example.test/research"
    assert evidence.source == "document.querySelectorAll('a[href]')"
    assert evidence.link_count == 5
    assert evidence.link_limit == 2
    assert evidence.truncated is True
    assert evidence.links[0].ordinal == 1
    assert evidence.links[0].href == "https://example.test/first"
    assert evidence.links[0].text_prefix == "First 😀"
    assert evidence.links[0].text_character_count == 13
    assert evidence.links[0].text_limit == 7
    assert evidence.links[0].truncated is True
    assert evidence.links[1].href == "mailto:research@example.test"
    assert evidence.links[1].truncated is False
    assert calls == [
        ("list", "http://127.0.0.1:9222", 2.0),
        ("read", target, 2, 7, 2.0),
    ]

    with pytest.raises(FrozenInstanceError):
        evidence.url = "changed"  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        evidence.links[0].href = "changed"  # type: ignore[misc]


def test_observe_chromium_page_links_refuses_ambiguous_target_before_link_read(
    monkeypatch,
) -> None:
    targets = (
        ChromiumPageTarget("page-1", "ws://devtools/page/page-1"),
        ChromiumPageTarget("page-2", "ws://devtools/page/page-2"),
    )
    monkeypatch.setattr(
        observation_module,
        "list_chromium_page_targets",
        lambda endpoint, *, timeout: targets,
    )

    def fail_if_read(*args, **kwargs):
        raise AssertionError("Ambiguous target selection must fail before link read.")

    monkeypatch.setattr(observation_module, "read_chromium_page_links", fail_if_read)

    with pytest.raises(ChromiumReadError, match="supply target_id explicitly"):
        observe_chromium_page_links("http://127.0.0.1:9222")


def test_observe_chromium_page_links_preserves_non_http_href_without_classification(
    monkeypatch,
) -> None:
    target = ChromiumPageTarget("page-1", "ws://devtools/page/page-1")
    monkeypatch.setattr(
        observation_module,
        "list_chromium_page_targets",
        lambda endpoint, *, timeout: (target,),
    )
    monkeypatch.setattr(
        observation_module,
        "read_chromium_page_links",
        lambda selected, *, link_limit, link_text_limit, timeout: ChromiumPageLinksSnapshot(
            url="https://example.test/",
            links=(
                ChromiumPageLinkSnapshot(
                    ordinal=1,
                    href="javascript:void(0)",
                    text_prefix="Action",
                    text_character_count=6,
                ),
            ),
            link_count=1,
        ),
    )

    evidence = observe_chromium_page_links("http://127.0.0.1:9222")

    assert evidence.links[0].href == "javascript:void(0)"
    assert evidence.links[0].text_prefix == "Action"
