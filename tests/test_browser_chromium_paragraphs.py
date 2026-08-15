from __future__ import annotations

import importlib
import json

import pytest

from pyxis.browser import ChromiumPageTarget, ChromiumReadError, read_chromium_page_paragraphs


paragraphs_module = importlib.import_module("pyxis.browser.chromium_paragraphs")


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


def test_read_chromium_page_paragraphs_uses_one_fixed_read_only_runtime_command(monkeypatch) -> None:
    websocket = _FakeWebSocket(
        [
            {
                "id": 1,
                "result": {
                    "result": {
                        "type": "object",
                        "value": {
                            "url": "https://example.test/article",
                            "paragraphCount": 3,
                            "paragraphs": [
                                {
                                    "ordinal": 1,
                                    "elementId": "intro",
                                    "textPrefix": "First 😀",
                                    "textCharacterCount": 15,
                                },
                                {
                                    "ordinal": 2,
                                    "elementId": "intro",
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

    monkeypatch.setattr(paragraphs_module, "_open_websocket", fake_open)

    target = ChromiumPageTarget(
        target_id="page-1",
        websocket_debugger_url="ws://127.0.0.1:9222/devtools/page/page-1",
    )
    snapshot = read_chromium_page_paragraphs(
        target,
        paragraph_limit=2,
        paragraph_text_limit=7,
        timeout=3.0,
    )

    assert snapshot.url == "https://example.test/article"
    assert snapshot.paragraph_count == 3
    assert snapshot.paragraphs_truncated is True
    assert snapshot.paragraphs[0].ordinal == 1
    assert snapshot.paragraphs[0].element_id == "intro"
    assert snapshot.paragraphs[0].text_prefix == "First 😀"
    assert snapshot.paragraphs[0].text_character_count == 15
    assert snapshot.paragraphs[0].text_truncated is True
    assert snapshot.paragraphs[1].ordinal == 2
    assert snapshot.paragraphs[1].element_id == "intro"
    assert snapshot.paragraphs[1].text_prefix == "Methods"
    assert snapshot.paragraphs[1].text_truncated is False
    assert opened == [(target.websocket_debugger_url, 3.0)]
    assert websocket.closed is True
    assert len(websocket.sent) == 1

    command = json.loads(websocket.sent[0])
    assert command["id"] == 1
    assert command["method"] == "Runtime.evaluate"
    assert command["params"]["returnByValue"] is True
    expression = command["params"]["expression"]
    assert "document.querySelectorAll('p')" in expression
    assert "nodes.slice(0, 2)" in expression
    assert "paragraph.getAttribute('id')" in expression
    assert "paragraph.innerText" in expression
    assert "characters.slice(0, 7).join('')" in expression
    assert "Page.navigate" not in websocket.sent[0]
    assert "Target.activateTarget" not in websocket.sent[0]
    assert "Input.dispatchMouseEvent" not in websocket.sent[0]


def test_read_chromium_page_paragraphs_rejects_non_string_element_id(monkeypatch) -> None:
    websocket = _FakeWebSocket(
        [
            {
                "id": 1,
                "result": {
                    "result": {
                        "type": "object",
                        "value": {
                            "url": "https://example.test/",
                            "paragraphCount": 1,
                            "paragraphs": [
                                {
                                    "ordinal": 1,
                                    "elementId": 7,
                                    "textPrefix": "Text",
                                    "textCharacterCount": 4,
                                }
                            ],
                        },
                    }
                },
            }
        ]
    )
    monkeypatch.setattr(
        paragraphs_module,
        "_open_websocket",
        lambda url, *, timeout: websocket,
    )

    target = ChromiumPageTarget("page-1", "ws://devtools/page/page-1")

    with pytest.raises(ChromiumReadError, match="element id was not a string"):
        read_chromium_page_paragraphs(target)

    assert websocket.closed is True
