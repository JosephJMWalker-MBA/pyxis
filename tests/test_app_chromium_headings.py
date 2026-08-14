from __future__ import annotations

from dataclasses import FrozenInstanceError
import importlib

import pytest

from pyxis.app import observe_chromium_page_headings
from pyxis.browser import (
    ChromiumPageHeadingSnapshot,
    ChromiumPageHeadingsSnapshot,
    ChromiumPageTarget,
    ChromiumReadError,
)


headings_module = importlib.import_module("pyxis.app.chromium_headings")


def test_observe_chromium_page_headings_projects_frozen_bounded_evidence(monkeypatch) -> None:
    target = ChromiumPageTarget(
        target_id="page-1",
        websocket_debugger_url="ws://127.0.0.1:9222/devtools/page/page-1",
    )
    snapshot = ChromiumPageHeadingsSnapshot(
        url="https://example.test/research",
        headings=(
            ChromiumPageHeadingSnapshot(
                ordinal=1,
                level=1,
                text_prefix="Intro 😀",
                text_character_count=15,
            ),
            ChromiumPageHeadingSnapshot(
                ordinal=2,
                level=3,
                text_prefix="Methods",
                text_character_count=7,
            ),
        ),
        heading_count=4,
    )
    calls: list[tuple] = []

    def fake_list(endpoint: str, *, timeout: float):
        calls.append(("list", endpoint, timeout))
        return (target,)

    def fake_read(selected, *, heading_limit: int, heading_text_limit: int, timeout: float):
        calls.append(("read", selected, heading_limit, heading_text_limit, timeout))
        return snapshot

    monkeypatch.setattr(headings_module, "list_chromium_page_targets", fake_list)
    monkeypatch.setattr(headings_module, "read_chromium_page_headings", fake_read)

    evidence = observe_chromium_page_headings(
        " http://127.0.0.1:9222/ ",
        heading_limit=2,
        heading_text_limit=7,
        timeout=2.0,
    )

    assert evidence.endpoint == "http://127.0.0.1:9222"
    assert evidence.target_id == "page-1"
    assert evidence.url == "https://example.test/research"
    assert evidence.source == "document.querySelectorAll('h1,h2,h3,h4,h5,h6')"
    assert evidence.heading_count == 4
    assert evidence.heading_limit == 2
    assert evidence.truncated is True
    assert evidence.headings[0].ordinal == 1
    assert evidence.headings[0].level == 1
    assert evidence.headings[0].text_prefix == "Intro 😀"
    assert evidence.headings[0].text_character_count == 15
    assert evidence.headings[0].text_limit == 7
    assert evidence.headings[0].truncated is True
    assert evidence.headings[1].ordinal == 2
    assert evidence.headings[1].level == 3
    assert evidence.headings[1].text_prefix == "Methods"
    assert evidence.headings[1].truncated is False
    assert calls == [
        ("list", "http://127.0.0.1:9222", 2.0),
        ("read", target, 2, 7, 2.0),
    ]

    with pytest.raises(FrozenInstanceError):
        evidence.url = "changed"  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        evidence.headings[0].level = 2  # type: ignore[misc]


def test_observe_chromium_page_headings_refuses_ambiguous_target_before_read(monkeypatch) -> None:
    targets = (
        ChromiumPageTarget("page-1", "ws://devtools/page/page-1"),
        ChromiumPageTarget("page-2", "ws://devtools/page/page-2"),
    )
    monkeypatch.setattr(
        headings_module,
        "list_chromium_page_targets",
        lambda endpoint, *, timeout: targets,
    )

    def fail_if_read(*args, **kwargs):
        raise AssertionError("Ambiguous target selection must fail before heading read.")

    monkeypatch.setattr(headings_module, "read_chromium_page_headings", fail_if_read)

    with pytest.raises(ChromiumReadError, match="supply target_id explicitly"):
        observe_chromium_page_headings("http://127.0.0.1:9222")


def test_observe_chromium_page_headings_preserves_skipped_levels_without_repair(monkeypatch) -> None:
    target = ChromiumPageTarget("page-1", "ws://devtools/page/page-1")
    monkeypatch.setattr(
        headings_module,
        "list_chromium_page_targets",
        lambda endpoint, *, timeout: (target,),
    )
    monkeypatch.setattr(
        headings_module,
        "read_chromium_page_headings",
        lambda selected, *, heading_limit, heading_text_limit, timeout: ChromiumPageHeadingsSnapshot(
            url="https://example.test/",
            headings=(
                ChromiumPageHeadingSnapshot(1, 1, "Title", 5),
                ChromiumPageHeadingSnapshot(2, 4, "Detail", 6),
            ),
            heading_count=2,
        ),
    )

    evidence = observe_chromium_page_headings("http://127.0.0.1:9222")

    assert tuple(heading.level for heading in evidence.headings) == (1, 4)
