from __future__ import annotations

import importlib
import json

import pytest

from pyxis.browser import (
    ChromiumPageTarget,
    ChromiumReadError,
    list_chromium_page_targets,
    read_chromium_page_snapshot,
)


chromium_module = importlib.import_module("pyxis.browser.chromium")


class _FakeHttpResponse:
    def __init__(self, payload) -> None:
        self._payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        return None

    def read(self) -> bytes:
        return json.dumps(self._payload).encode("utf-8")


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


def test_list_chromium_page_targets_reads_json_list_and_filters_non_pages(
    monkeypatch,
) -> None:
    calls: list[tuple[str, float]] = []
    payload = [
        {
            "id": "page-1",
            "type": "page",
            "webSocketDebuggerUrl": "ws://127.0.0.1:9222/devtools/page/page-1",
        },
        {
            "id": "worker-1",
            "type": "service_worker",
            "webSocketDebuggerUrl": "ws://127.0.0.1:9222/devtools/page/worker-1",
        },
        {
            "id": "page-2",
            "type": "page",
            "webSocketDebuggerUrl": "ws://127.0.0.1:9222/devtools/page/page-2",
        },
    ]

    def fake_urlopen(url: str, *, timeout: float):
        calls.append((url, timeout))
        return _FakeHttpResponse(payload)

    monkeypatch.setattr(chromium_module, "urlopen", fake_urlopen)

    targets = list_chromium_page_targets(" http://127.0.0.1:9222/ ", timeout=2.5)

    assert targets == (
        ChromiumPageTarget(
            target_id="page-1",
            websocket_debugger_url="ws://127.0.0.1:9222/devtools/page/page-1",
        ),
        ChromiumPageTarget(
            target_id="page-2",
            websocket_debugger_url="ws://127.0.0.1:9222/devtools/page/page-2",
        ),
    )
    assert calls == [("http://127.0.0.1:9222/json/list", 2.5)]


def test_read_chromium_page_snapshot_uses_one_fixed_read_only_runtime_command(
    monkeypatch,
) -> None:
    websocket = _FakeWebSocket(
        [
            {"method": "Runtime.executionContextCreated", "params": {}},
            {
                "id": 1,
                "result": {
                    "result": {
                        "type": "object",
                        "value": {
                            "url": "https://example.test/article",
                            "title": "Example article",
                            "textPrefix": "first rendered text",
                            "textCharacterCount": 42,
                        },
                    }
                },
            },
        ]
    )
    opened: list[tuple[str, float]] = []

    def fake_open(url: str, *, timeout: float):
        opened.append((url, timeout))
        return websocket

    monkeypatch.setattr(chromium_module, "_open_websocket", fake_open)

    target = ChromiumPageTarget(
        target_id="page-1",
        websocket_debugger_url="ws://127.0.0.1:9222/devtools/page/page-1",
    )
    snapshot = read_chromium_page_snapshot(target, text_limit=64, timeout=3.0)

    assert snapshot.url == "https://example.test/article"
    assert snapshot.title == "Example article"
    assert snapshot.text_prefix == "first rendered text"
    assert snapshot.text_character_count == 42
    assert snapshot.text_truncated is True
    assert opened == [(target.websocket_debugger_url, 3.0)]
    assert websocket.closed is True
    assert len(websocket.sent) == 1

    command = json.loads(websocket.sent[0])
    assert command["id"] == 1
    assert command["method"] == "Runtime.evaluate"
    assert command["params"]["returnByValue"] is True
    expression = command["params"]["expression"]
    assert "window.location.href" in expression
    assert "document.title" in expression
    assert "document.body.innerText" in expression
    assert "Array.from(text)" in expression
    assert "characters.slice(0, 64).join('')" in expression
    assert "Page.navigate" not in websocket.sent[0]
    assert "Target.activateTarget" not in websocket.sent[0]


def test_read_chromium_page_snapshot_surfaces_cdp_command_error(monkeypatch) -> None:
    websocket = _FakeWebSocket(
        [{"id": 1, "error": {"code": -32000, "message": "target closed"}}]
    )
    monkeypatch.setattr(
        chromium_module,
        "_open_websocket",
        lambda url, *, timeout: websocket,
    )

    target = ChromiumPageTarget(
        target_id="page-1",
        websocket_debugger_url="ws://127.0.0.1:9222/devtools/page/page-1",
    )

    with pytest.raises(ChromiumReadError, match="Runtime.evaluate failed"):
        read_chromium_page_snapshot(target)

    assert websocket.closed is True
