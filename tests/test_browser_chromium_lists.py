from __future__ import annotations

import importlib
import json

import pytest

from pyxis.browser import ChromiumPageTarget, ChromiumReadError, read_chromium_page_lists


lists_module = importlib.import_module("pyxis.browser.chromium_lists")


class _FakeWebSocket:
    def __init__(self, responses: list[dict]) -> None:
        self._responses = [json.dumps(response) for response in responses]
        self.sent: list[str] = []
        self.closed = False

    def send(self, message: str) -> None:
        self.sent.append(message)

    def recv(self) -> str:
        return self._responses.pop(0)

    def close(self) -> None:
        self.closed = True


def test_read_chromium_page_lists_preserves_literal_nesting_and_authored_attributes(monkeypatch) -> None:
    websocket = _FakeWebSocket(
        [
            {
                "id": 1,
                "result": {
                    "result": {
                        "type": "object",
                        "value": {
                            "url": "https://example.test/methods",
                            "listCount": 3,
                            "lists": [
                                {
                                    "ordinal": 1,
                                    "tagName": "OL",
                                    "startAttribute": "3",
                                    "parentListOrdinal": None,
                                    "parentItemOrdinal": None,
                                    "itemCount": 3,
                                    "items": [
                                        {
                                            "ordinal": 1,
                                            "valueAttribute": "7",
                                            "directTextPrefix": "Alpha 😀",
                                            "directTextCharacterCount": 12,
                                        },
                                        {
                                            "ordinal": 2,
                                            "valueAttribute": None,
                                            "directTextPrefix": "Parent",
                                            "directTextCharacterCount": 6,
                                        },
                                    ],
                                },
                                {
                                    "ordinal": 2,
                                    "tagName": "UL",
                                    "startAttribute": "99",
                                    "parentListOrdinal": 1,
                                    "parentItemOrdinal": 2,
                                    "itemCount": 1,
                                    "items": [
                                        {
                                            "ordinal": 1,
                                            "valueAttribute": "42",
                                            "directTextPrefix": "Nested",
                                            "directTextCharacterCount": 6,
                                        }
                                    ],
                                },
                            ],
                        },
                    }
                },
            }
        ]
    )
    opened: list[tuple[str, float]] = []

    def fake_open(url: str, *, timeout: float):
        opened.append((url, timeout))
        return websocket

    monkeypatch.setattr(lists_module, "_open_websocket", fake_open)

    target = ChromiumPageTarget(
        target_id="page-1",
        websocket_debugger_url="ws://127.0.0.1:9222/devtools/page/page-1",
    )
    snapshot = read_chromium_page_lists(
        target,
        list_limit=2,
        item_limit=2,
        text_limit=7,
        timeout=3.0,
    )

    assert snapshot.url == "https://example.test/methods"
    assert snapshot.list_count == 3
    assert snapshot.lists_truncated is True

    ordered = snapshot.lists[0]
    assert ordered.ordinal == 1
    assert ordered.tag_name == "OL"
    assert ordered.start_attribute == "3"
    assert ordered.parent_list_ordinal is None
    assert ordered.parent_item_ordinal is None
    assert ordered.item_count == 3
    assert ordered.items_truncated is True
    assert ordered.items[0].value_attribute == "7"
    assert ordered.items[0].direct_text_prefix == "Alpha 😀"
    assert ordered.items[0].direct_text_character_count == 12
    assert ordered.items[0].direct_text_truncated is True
    assert ordered.items[1].direct_text_prefix == "Parent"
    assert ordered.items[1].direct_text_truncated is False

    nested = snapshot.lists[1]
    assert nested.ordinal == 2
    assert nested.tag_name == "UL"
    assert nested.start_attribute == "99"
    assert nested.parent_list_ordinal == 1
    assert nested.parent_item_ordinal == 2
    assert nested.item_count == 1
    assert nested.items_truncated is False
    assert nested.items[0].value_attribute == "42"
    assert nested.items[0].direct_text_prefix == "Nested"

    assert opened == [(target.websocket_debugger_url, 3.0)]
    assert websocket.closed is True
    assert len(websocket.sent) == 1

    command = json.loads(websocket.sent[0])
    assert command["id"] == 1
    assert command["method"] == "Runtime.evaluate"
    assert command["params"]["returnByValue"] is True
    expression = command["params"]["expression"]
    assert "document.querySelectorAll('ol,ul')" in expression
    assert "listNodes.slice(0, 2)" in expression
    assert "Array.from(list.children).filter((child) => child.tagName === 'LI')" in expression
    assert "list.getAttribute('start')" in expression
    assert "item.getAttribute('value')" in expression
    assert "document.createTreeWalker(item, NodeFilter.SHOW_TEXT)" in expression
    assert "parentElement.closest('ol,ul') === list" in expression
    assert "parentListOrdinal" in expression
    assert "parentItemOrdinal" in expression
    assert "characters.slice(0, 7).join('')" in expression
    assert "Page.navigate" not in websocket.sent[0]
    assert "Target.activateTarget" not in websocket.sent[0]
    assert "Input.dispatchMouseEvent" not in websocket.sent[0]


def test_read_chromium_page_lists_rejects_non_ancestor_parent_ordinal(monkeypatch) -> None:
    websocket = _FakeWebSocket(
        [
            {
                "id": 1,
                "result": {
                    "result": {
                        "type": "object",
                        "value": {
                            "url": "https://example.test/",
                            "listCount": 2,
                            "lists": [
                                {
                                    "ordinal": 1,
                                    "tagName": "OL",
                                    "startAttribute": None,
                                    "parentListOrdinal": None,
                                    "parentItemOrdinal": None,
                                    "itemCount": 0,
                                    "items": [],
                                },
                                {
                                    "ordinal": 2,
                                    "tagName": "UL",
                                    "startAttribute": None,
                                    "parentListOrdinal": 2,
                                    "parentItemOrdinal": 1,
                                    "itemCount": 0,
                                    "items": [],
                                },
                            ],
                        },
                    }
                },
            }
        ]
    )
    monkeypatch.setattr(
        lists_module,
        "_open_websocket",
        lambda url, *, timeout: websocket,
    )

    target = ChromiumPageTarget("page-1", "ws://devtools/page/page-1")

    with pytest.raises(ChromiumReadError, match="earlier ancestor list"):
        read_chromium_page_lists(target)

    assert websocket.closed is True
