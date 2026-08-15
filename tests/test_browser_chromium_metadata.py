from __future__ import annotations

import importlib
import json

import pytest

from pyxis.browser import ChromiumPageTarget, ChromiumReadError, read_chromium_page_metadata


metadata_module = importlib.import_module("pyxis.browser.chromium_metadata")


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


def test_read_chromium_page_metadata_uses_one_fixed_read_only_runtime_command(monkeypatch) -> None:
    websocket = _FakeWebSocket(
        [
            {
                "id": 1,
                "result": {
                    "result": {
                        "type": "object",
                        "value": {
                            "url": "https://example.test/article",
                            "documentLanguage": "EN-us",
                            "canonicalLinkCount": 3,
                            "canonicalLinks": [
                                {
                                    "ordinal": 1,
                                    "rawHref": "/article",
                                    "resolvedHref": "https://example.test/article",
                                },
                                {
                                    "ordinal": 2,
                                    "rawHref": "https://mirror.test/item",
                                    "resolvedHref": "https://mirror.test/item",
                                },
                            ],
                            "descriptionCount": 2,
                            "descriptions": [
                                {
                                    "ordinal": 1,
                                    "contentPrefix": "Study 😀",
                                    "contentCharacterCount": 16,
                                }
                            ],
                        },
                    }
                },
            }
        ]
    )
    monkeypatch.setattr(
        metadata_module,
        "_open_websocket",
        lambda url, *, timeout: websocket,
    )
    target = ChromiumPageTarget("page-1", "ws://devtools/page/page-1")

    snapshot = read_chromium_page_metadata(
        target,
        canonical_link_limit=2,
        description_limit=1,
        description_text_limit=7,
        timeout=3.0,
    )

    assert snapshot.url == "https://example.test/article"
    assert snapshot.document_language == "EN-us"
    assert snapshot.canonical_link_count == 3
    assert snapshot.canonical_links_truncated is True
    assert snapshot.canonical_links[0].raw_href == "/article"
    assert snapshot.canonical_links[0].resolved_href == "https://example.test/article"
    assert snapshot.canonical_links[1].resolved_href == "https://mirror.test/item"
    assert snapshot.description_count == 2
    assert snapshot.descriptions_truncated is True
    assert snapshot.descriptions[0].content_prefix == "Study 😀"
    assert snapshot.descriptions[0].content_character_count == 16
    assert snapshot.descriptions[0].content_truncated is True
    assert websocket.closed is True
    assert len(websocket.sent) == 1

    command = json.loads(websocket.sent[0])
    assert command["method"] == "Runtime.evaluate"
    expression = command["params"]["expression"]
    assert "document.documentElement" in expression
    assert "getAttribute('lang')" in expression
    assert "link[rel~='canonical' i][href]" in expression
    assert "link.getAttribute('href')" in expression
    assert "resolvedHref: link.href" in expression
    assert "meta[name='description' i]" in expression
    assert "canonicalNodes.slice(0, 2)" in expression
    assert "descriptionNodes.slice(0, 1)" in expression
    assert "characters.slice(0, 7).join('')" in expression
    assert "Page.navigate" not in websocket.sent[0]
    assert "Target.activateTarget" not in websocket.sent[0]
    assert "fetch(" not in websocket.sent[0]


def test_read_chromium_page_metadata_rejects_noncontiguous_declaration_ordinals(monkeypatch) -> None:
    websocket = _FakeWebSocket(
        [
            {
                "id": 1,
                "result": {
                    "result": {
                        "type": "object",
                        "value": {
                            "url": "https://example.test/",
                            "documentLanguage": "",
                            "canonicalLinkCount": 1,
                            "canonicalLinks": [
                                {
                                    "ordinal": 2,
                                    "rawHref": "/wrong",
                                    "resolvedHref": "https://example.test/wrong",
                                }
                            ],
                            "descriptionCount": 0,
                            "descriptions": [],
                        },
                    }
                },
            }
        ]
    )
    monkeypatch.setattr(
        metadata_module,
        "_open_websocket",
        lambda url, *, timeout: websocket,
    )
    target = ChromiumPageTarget("page-1", "ws://devtools/page/page-1")

    with pytest.raises(ChromiumReadError, match="canonical-link ordinals"):
        read_chromium_page_metadata(target)

    assert websocket.closed is True
