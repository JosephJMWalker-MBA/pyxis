from __future__ import annotations

import importlib
import json

import pytest

from pyxis.browser import ChromiumPageTarget, ChromiumReadError, read_chromium_page_headings


headings_module = importlib.import_module("pyxis.browser.chromium_headings")


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


def test_read_chromium_page_headings_uses_one_fixed_read_only_runtime_command(monkeypatch) -> None:
    websocket = _FakeWebSocket(
        [
            {
                "id": 1,
                "result": {
                    "result": {
                        "type": "object",
                        "value": {
                            "url": "https://example.test/article",
                            "headingCount": 3,
                            "headings": [
                                {
                                    "ordinal": 1,
                                    "level": 1,
                                    "textPrefix": "Intro 😀",
                                    "textCharacterCount": 15,
                                },
                                {
                                    "ordinal": 2,
                                    "level": 3,
                                    "textPrefix": "Methods",
                                    "textCharacterCount": 7,
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

    monkeypatch.setattr(headings_module, "_open_websocket", fake_open)

    target = ChromiumPageTarget(
        target_id="page-1",
        websocket_debugger_url="ws://127.0.0.1:9222/devtools/page/page-1",
    )
    snapshot = read_chromium_page_headings(
        target,
        heading_limit=2,
        heading_text_limit=7,
        timeout=3.0,
    )

    assert snapshot.url == "https://example.test/article"
    assert snapshot.heading_count == 3
    assert snapshot.headings_truncated is True
    assert snapshot.headings[0].ordinal == 1
    assert snapshot.headings[0].level == 1
    assert snapshot.headings[0].text_prefix == "Intro 😀"
    assert snapshot.headings[0].text_character_count == 15
    assert snapshot.headings[0].text_truncated is True
    assert snapshot.headings[1].ordinal == 2
    assert snapshot.headings[1].level == 3
    assert snapshot.headings[1].text_prefix == "Methods"
    assert snapshot.headings[1].text_truncated is False
    assert opened == [(target.websocket_debugger_url, 3.0)]
    assert websocket.closed is True
    assert len(websocket.sent) == 1

    command = json.loads(websocket.sent[0])
    assert command["id"] == 1
    assert command["method"] == "Runtime.evaluate"
    assert command["params"]["returnByValue"] is True
    expression = command["params"]["expression"]
    assert "document.querySelectorAll('h1,h2,h3,h4,h5,h6')" in expression
    assert "nodes.slice(0, 2)" in expression
    assert "Number(heading.tagName.slice(1))" in expression
    assert "heading.innerText" in expression
    assert "characters.slice(0, 7).join('')" in expression
    assert "Page.navigate" not in websocket.sent[0]
    assert "Target.activateTarget" not in websocket.sent[0]
    assert "Input.dispatchMouseEvent" not in websocket.sent[0]


def test_read_chromium_page_headings_rejects_invalid_heading_level(monkeypatch) -> None:
    websocket = _FakeWebSocket(
        [
            {
                "id": 1,
                "result": {
                    "result": {
                        "type": "object",
                        "value": {
                            "url": "https://example.test/",
                            "headingCount": 1,
                            "headings": [
                                {
                                    "ordinal": 1,
                                    "level": 7,
                                    "textPrefix": "Impossible",
                                    "textCharacterCount": 10,
                                }
                            ],
                        },
                    }
                },
            }
        ]
    )
    monkeypatch.setattr(
        headings_module,
        "_open_websocket",
        lambda url, *, timeout: websocket,
    )

    target = ChromiumPageTarget("page-1", "ws://devtools/page/page-1")

    with pytest.raises(ChromiumReadError, match="level was not an integer from 1 through 6"):
        read_chromium_page_headings(target)

    assert websocket.closed is True
