from __future__ import annotations

from dataclasses import FrozenInstanceError
import importlib

import pytest

from pyxis.app import observe_chromium_page_paragraphs
from pyxis.browser import (
    ChromiumPageParagraphSnapshot,
    ChromiumPageParagraphsSnapshot,
    ChromiumPageTarget,
    ChromiumReadError,
)


paragraphs_module = importlib.import_module("pyxis.app.chromium_paragraphs")


def test_observe_chromium_page_paragraphs_projects_frozen_bounded_evidence(monkeypatch) -> None:
    target = ChromiumPageTarget(
        target_id="page-1",
        websocket_debugger_url="ws://127.0.0.1:9222/devtools/page/page-1",
    )
    snapshot = ChromiumPageParagraphsSnapshot(
        url="https://example.test/research",
        paragraphs=(
            ChromiumPageParagraphSnapshot(
                ordinal=1,
                element_id="intro",
                text_prefix="First 😀",
                text_character_count=15,
            ),
            ChromiumPageParagraphSnapshot(
                ordinal=2,
                element_id="intro",
                text_prefix="Methods",
                text_character_count=7,
            ),
        ),
        paragraph_count=4,
    )
    calls: list[tuple] = []

    def fake_list(endpoint: str, *, timeout: float):
        calls.append(("list", endpoint, timeout))
        return (target,)

    def fake_read(selected, *, paragraph_limit: int, paragraph_text_limit: int, timeout: float):
        calls.append(("read", selected, paragraph_limit, paragraph_text_limit, timeout))
        return snapshot

    monkeypatch.setattr(paragraphs_module, "list_chromium_page_targets", fake_list)
    monkeypatch.setattr(paragraphs_module, "read_chromium_page_paragraphs", fake_read)

    evidence = observe_chromium_page_paragraphs(
        " http://127.0.0.1:9222/ ",
        paragraph_limit=2,
        paragraph_text_limit=7,
        timeout=2.0,
    )

    assert evidence.endpoint == "http://127.0.0.1:9222"
    assert evidence.target_id == "page-1"
    assert evidence.url == "https://example.test/research"
    assert evidence.source == "document.querySelectorAll('p')"
    assert evidence.paragraph_count == 4
    assert evidence.paragraph_limit == 2
    assert evidence.truncated is True
    assert evidence.paragraphs[0].ordinal == 1
    assert evidence.paragraphs[0].element_id == "intro"
    assert evidence.paragraphs[0].text_prefix == "First 😀"
    assert evidence.paragraphs[0].text_character_count == 15
    assert evidence.paragraphs[0].text_limit == 7
    assert evidence.paragraphs[0].truncated is True
    assert evidence.paragraphs[1].ordinal == 2
    assert evidence.paragraphs[1].element_id == "intro"
    assert evidence.paragraphs[1].text_prefix == "Methods"
    assert evidence.paragraphs[1].truncated is False
    assert calls == [
        ("list", "http://127.0.0.1:9222", 2.0),
        ("read", target, 2, 7, 2.0),
    ]

    with pytest.raises(FrozenInstanceError):
        evidence.url = "changed"  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        evidence.paragraphs[0].element_id = "changed"  # type: ignore[misc]


def test_observe_chromium_page_paragraphs_refuses_ambiguous_target_before_read(monkeypatch) -> None:
    targets = (
        ChromiumPageTarget("page-1", "ws://devtools/page/page-1"),
        ChromiumPageTarget("page-2", "ws://devtools/page/page-2"),
    )
    monkeypatch.setattr(
        paragraphs_module,
        "list_chromium_page_targets",
        lambda endpoint, *, timeout: targets,
    )

    def fail_if_read(*args, **kwargs):
        raise AssertionError("Ambiguous target selection must fail before paragraph read.")

    monkeypatch.setattr(paragraphs_module, "read_chromium_page_paragraphs", fail_if_read)

    with pytest.raises(ChromiumReadError, match="supply target_id explicitly"):
        observe_chromium_page_paragraphs("http://127.0.0.1:9222")


def test_observe_chromium_page_paragraphs_preserves_duplicate_and_empty_ids(monkeypatch) -> None:
    target = ChromiumPageTarget("page-1", "ws://devtools/page/page-1")
    monkeypatch.setattr(
        paragraphs_module,
        "list_chromium_page_targets",
        lambda endpoint, *, timeout: (target,),
    )
    monkeypatch.setattr(
        paragraphs_module,
        "read_chromium_page_paragraphs",
        lambda selected, *, paragraph_limit, paragraph_text_limit, timeout: ChromiumPageParagraphsSnapshot(
            url="https://example.test/",
            paragraphs=(
                ChromiumPageParagraphSnapshot(1, "same", "One", 3),
                ChromiumPageParagraphSnapshot(2, "same", "Two", 3),
                ChromiumPageParagraphSnapshot(3, "", "Three", 5),
            ),
            paragraph_count=3,
        ),
    )

    evidence = observe_chromium_page_paragraphs("http://127.0.0.1:9222")

    assert tuple(paragraph.element_id for paragraph in evidence.paragraphs) == (
        "same",
        "same",
        "",
    )
