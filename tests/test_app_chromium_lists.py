from __future__ import annotations

from dataclasses import FrozenInstanceError
import importlib

import pytest

from pyxis.app import observe_chromium_page_lists
from pyxis.browser import (
    ChromiumPageListItemSnapshot,
    ChromiumPageListSnapshot,
    ChromiumPageListsSnapshot,
    ChromiumPageTarget,
    ChromiumReadError,
)


lists_module = importlib.import_module("pyxis.app.chromium_lists")


def test_observe_chromium_page_lists_projects_frozen_nested_evidence(monkeypatch) -> None:
    target = ChromiumPageTarget(
        target_id="page-1",
        websocket_debugger_url="ws://127.0.0.1:9222/devtools/page/page-1",
    )
    snapshot = ChromiumPageListsSnapshot(
        url="https://example.test/methods",
        lists=(
            ChromiumPageListSnapshot(
                ordinal=1,
                tag_name="OL",
                start_attribute="3",
                parent_list_ordinal=None,
                parent_item_ordinal=None,
                items=(
                    ChromiumPageListItemSnapshot(1, "7", "Alpha 😀", 12),
                    ChromiumPageListItemSnapshot(2, None, "Parent", 6),
                ),
                item_count=3,
            ),
            ChromiumPageListSnapshot(
                ordinal=2,
                tag_name="UL",
                start_attribute="99",
                parent_list_ordinal=1,
                parent_item_ordinal=2,
                items=(ChromiumPageListItemSnapshot(1, "42", "Nested", 6),),
                item_count=1,
            ),
        ),
        list_count=3,
    )
    calls: list[tuple] = []

    def fake_list(endpoint: str, *, timeout: float):
        calls.append(("list", endpoint, timeout))
        return (target,)

    def fake_read(
        selected,
        *,
        list_limit: int,
        item_limit: int,
        text_limit: int,
        timeout: float,
    ):
        calls.append(("read", selected, list_limit, item_limit, text_limit, timeout))
        return snapshot

    monkeypatch.setattr(lists_module, "list_chromium_page_targets", fake_list)
    monkeypatch.setattr(lists_module, "read_chromium_page_lists", fake_read)

    evidence = observe_chromium_page_lists(
        " http://127.0.0.1:9222/ ",
        list_limit=2,
        item_limit=2,
        text_limit=7,
        timeout=2.0,
    )

    assert evidence.endpoint == "http://127.0.0.1:9222"
    assert evidence.target_id == "page-1"
    assert evidence.url == "https://example.test/methods"
    assert evidence.source == "document.querySelectorAll('ol,ul')"
    assert evidence.list_count == 3
    assert evidence.list_limit == 2
    assert evidence.truncated is True

    ordered = evidence.lists[0]
    assert ordered.ordinal == 1
    assert ordered.tag_name == "OL"
    assert ordered.start_attribute == "3"
    assert ordered.parent_list_ordinal is None
    assert ordered.parent_item_ordinal is None
    assert ordered.item_count == 3
    assert ordered.item_limit == 2
    assert ordered.truncated is True
    assert ordered.items[0].value_attribute == "7"
    assert ordered.items[0].direct_text_prefix == "Alpha 😀"
    assert ordered.items[0].direct_text_character_count == 12
    assert ordered.items[0].text_limit == 7
    assert ordered.items[0].truncated is True

    nested = evidence.lists[1]
    assert nested.tag_name == "UL"
    assert nested.start_attribute == "99"
    assert nested.parent_list_ordinal == 1
    assert nested.parent_item_ordinal == 2
    assert nested.items[0].value_attribute == "42"
    assert nested.items[0].direct_text_prefix == "Nested"
    assert nested.items[0].truncated is False

    assert calls == [
        ("list", "http://127.0.0.1:9222", 2.0),
        ("read", target, 2, 2, 7, 2.0),
    ]

    with pytest.raises(FrozenInstanceError):
        evidence.url = "changed"  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        evidence.lists[1].parent_item_ordinal = 1  # type: ignore[misc]


def test_observe_chromium_page_lists_refuses_ambiguous_target_before_read(monkeypatch) -> None:
    targets = (
        ChromiumPageTarget("page-1", "ws://devtools/page/page-1"),
        ChromiumPageTarget("page-2", "ws://devtools/page/page-2"),
    )
    monkeypatch.setattr(
        lists_module,
        "list_chromium_page_targets",
        lambda endpoint, *, timeout: targets,
    )

    def fail_if_read(*args, **kwargs):
        raise AssertionError("Ambiguous target selection must fail before list read.")

    monkeypatch.setattr(lists_module, "read_chromium_page_lists", fail_if_read)

    with pytest.raises(ChromiumReadError, match="supply target_id explicitly"):
        observe_chromium_page_lists("http://127.0.0.1:9222")


def test_observe_chromium_page_lists_preserves_invalid_authored_attributes_without_repair(monkeypatch) -> None:
    target = ChromiumPageTarget("page-1", "ws://devtools/page/page-1")
    monkeypatch.setattr(
        lists_module,
        "list_chromium_page_targets",
        lambda endpoint, *, timeout: (target,),
    )
    monkeypatch.setattr(
        lists_module,
        "read_chromium_page_lists",
        lambda selected, *, list_limit, item_limit, text_limit, timeout: ChromiumPageListsSnapshot(
            url="https://example.test/",
            lists=(
                ChromiumPageListSnapshot(
                    ordinal=1,
                    tag_name="UL",
                    start_attribute="not-standard-here",
                    parent_list_ordinal=None,
                    parent_item_ordinal=None,
                    items=(
                        ChromiumPageListItemSnapshot(
                            ordinal=1,
                            value_attribute="also-authored",
                            direct_text_prefix="Literal",
                            direct_text_character_count=7,
                        ),
                    ),
                    item_count=1,
                ),
            ),
            list_count=1,
        ),
    )

    evidence = observe_chromium_page_lists("http://127.0.0.1:9222")

    assert evidence.lists[0].tag_name == "UL"
    assert evidence.lists[0].start_attribute == "not-standard-here"
    assert evidence.lists[0].items[0].value_attribute == "also-authored"
