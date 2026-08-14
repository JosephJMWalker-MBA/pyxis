from __future__ import annotations

from dataclasses import FrozenInstanceError
import importlib

import pytest

from pyxis.app.chromium_observation import observe_chromium_page
from pyxis.browser import ChromiumPageSnapshot, ChromiumPageTarget, ChromiumReadError


observation_module = importlib.import_module("pyxis.app.chromium_observation")


def test_observe_chromium_page_projects_frozen_evidence_from_one_page(monkeypatch) -> None:
    target = ChromiumPageTarget(
        target_id="page-1",
        websocket_debugger_url="ws://127.0.0.1:9222/devtools/page/page-1",
    )
    snapshot = ChromiumPageSnapshot(
        url="https://example.test/research",
        title="Research page",
        text_prefix="alpha beta gamma",
        text_character_count=31,
    )
    calls: list[tuple] = []

    def fake_list(endpoint: str, *, timeout: float):
        calls.append(("list", endpoint, timeout))
        return (target,)

    def fake_read(selected, *, text_limit: int, timeout: float):
        calls.append(("read", selected, text_limit, timeout))
        return snapshot

    monkeypatch.setattr(observation_module, "list_chromium_page_targets", fake_list)
    monkeypatch.setattr(observation_module, "read_chromium_page_snapshot", fake_read)

    evidence = observe_chromium_page(
        " http://127.0.0.1:9222/ ",
        text_limit=16,
        timeout=2.0,
    )

    assert evidence.endpoint == "http://127.0.0.1:9222"
    assert evidence.target_id == "page-1"
    assert evidence.url == "https://example.test/research"
    assert evidence.title == "Research page"
    assert evidence.content.source == "document.body.innerText"
    assert evidence.content.text_prefix == "alpha beta gamma"
    assert evidence.content.text_character_count == 31
    assert evidence.content.text_limit == 16
    assert evidence.content.truncated is True
    assert calls == [
        ("list", "http://127.0.0.1:9222", 2.0),
        ("read", target, 16, 2.0),
    ]

    with pytest.raises(FrozenInstanceError):
        evidence.title = "changed"  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        evidence.content.text_prefix = "changed"  # type: ignore[misc]


def test_observe_chromium_page_refuses_to_guess_among_multiple_pages(monkeypatch) -> None:
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
        raise AssertionError("Ambiguous target selection must fail before page read.")

    monkeypatch.setattr(
        observation_module,
        "read_chromium_page_snapshot",
        fail_if_read,
    )

    with pytest.raises(ChromiumReadError, match="supply target_id explicitly"):
        observe_chromium_page("http://127.0.0.1:9222")


def test_observe_chromium_page_uses_exact_explicit_target_id(monkeypatch) -> None:
    first = ChromiumPageTarget("page-1", "ws://devtools/page/page-1")
    second = ChromiumPageTarget("page-2", "ws://devtools/page/page-2")
    selected: list[ChromiumPageTarget] = []

    monkeypatch.setattr(
        observation_module,
        "list_chromium_page_targets",
        lambda endpoint, *, timeout: (first, second),
    )

    def fake_read(target, *, text_limit: int, timeout: float):
        selected.append(target)
        return ChromiumPageSnapshot(
            url="https://example.test/second",
            title="Second",
            text_prefix="text",
            text_character_count=4,
        )

    monkeypatch.setattr(
        observation_module,
        "read_chromium_page_snapshot",
        fake_read,
    )

    evidence = observe_chromium_page(
        "http://127.0.0.1:9222",
        target_id="page-2",
    )

    assert selected == [second]
    assert evidence.target_id == "page-2"
    assert evidence.url == "https://example.test/second"
    assert evidence.content.truncated is False
