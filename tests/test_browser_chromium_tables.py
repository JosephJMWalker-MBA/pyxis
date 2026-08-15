from __future__ import annotations

import importlib
import json

import pytest

from pyxis.browser import ChromiumPageTarget, ChromiumReadError, read_chromium_page_tables


tables_module = importlib.import_module("pyxis.browser.chromium_tables")


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


def test_read_chromium_page_tables_preserves_nested_literal_structure(monkeypatch) -> None:
    websocket = _FakeWebSocket(
        [
            {
                "id": 1,
                "result": {
                    "result": {
                        "type": "object",
                        "value": {
                            "url": "https://example.test/data",
                            "tableCount": 2,
                            "tables": [
                                {
                                    "ordinal": 1,
                                    "captionTextPrefix": "Study 😀",
                                    "captionTextCharacterCount": 13,
                                    "rowCount": 2,
                                    "rows": [
                                        {
                                            "ordinal": 1,
                                            "cellCount": 3,
                                            "cells": [
                                                {
                                                    "ordinal": 1,
                                                    "tagName": "TH",
                                                    "rowSpan": 2,
                                                    "colSpan": 1,
                                                    "textPrefix": "Metric",
                                                    "textCharacterCount": 6,
                                                },
                                                {
                                                    "ordinal": 2,
                                                    "tagName": "TD",
                                                    "rowSpan": 1,
                                                    "colSpan": 2,
                                                    "textPrefix": "Alpha 😀",
                                                    "textCharacterCount": 12,
                                                },
                                            ],
                                        }
                                    ],
                                }
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

    monkeypatch.setattr(tables_module, "_open_websocket", fake_open)

    target = ChromiumPageTarget(
        target_id="page-1",
        websocket_debugger_url="ws://127.0.0.1:9222/devtools/page/page-1",
    )
    snapshot = read_chromium_page_tables(
        target,
        table_limit=1,
        row_limit=1,
        cell_limit=2,
        text_limit=7,
        timeout=3.0,
    )

    assert snapshot.url == "https://example.test/data"
    assert snapshot.table_count == 2
    assert snapshot.tables_truncated is True
    table = snapshot.tables[0]
    assert table.ordinal == 1
    assert table.caption_text_prefix == "Study 😀"
    assert table.caption_text_character_count == 13
    assert table.caption_text_truncated is True
    assert table.row_count == 2
    assert table.rows_truncated is True
    row = table.rows[0]
    assert row.ordinal == 1
    assert row.cell_count == 3
    assert row.cells_truncated is True
    assert row.cells[0].tag_name == "TH"
    assert row.cells[0].row_span == 2
    assert row.cells[0].col_span == 1
    assert row.cells[0].text_prefix == "Metric"
    assert row.cells[0].text_truncated is False
    assert row.cells[1].tag_name == "TD"
    assert row.cells[1].row_span == 1
    assert row.cells[1].col_span == 2
    assert row.cells[1].text_prefix == "Alpha 😀"
    assert row.cells[1].text_character_count == 12
    assert row.cells[1].text_truncated is True
    assert opened == [(target.websocket_debugger_url, 3.0)]
    assert websocket.closed is True
    assert len(websocket.sent) == 1

    command = json.loads(websocket.sent[0])
    assert command["id"] == 1
    assert command["method"] == "Runtime.evaluate"
    assert command["params"]["returnByValue"] is True
    expression = command["params"]["expression"]
    assert "document.querySelectorAll('table')" in expression
    assert "tableNodes.slice(0, 1)" in expression
    assert "row.closest('table') === table" in expression
    assert "row.children" in expression
    assert "cell.tagName === 'TH' || cell.tagName === 'TD'" in expression
    assert "rowSpan: cell.rowSpan" in expression
    assert "colSpan: cell.colSpan" in expression
    assert "characters.slice(0, 7).join('')" in expression
    assert "Page.navigate" not in websocket.sent[0]
    assert "Target.activateTarget" not in websocket.sent[0]
    assert "Input.dispatchMouseEvent" not in websocket.sent[0]


def test_read_chromium_page_tables_rejects_non_cell_tag(monkeypatch) -> None:
    websocket = _FakeWebSocket(
        [
            {
                "id": 1,
                "result": {
                    "result": {
                        "type": "object",
                        "value": {
                            "url": "https://example.test/",
                            "tableCount": 1,
                            "tables": [
                                {
                                    "ordinal": 1,
                                    "captionTextPrefix": "",
                                    "captionTextCharacterCount": 0,
                                    "rowCount": 1,
                                    "rows": [
                                        {
                                            "ordinal": 1,
                                            "cellCount": 1,
                                            "cells": [
                                                {
                                                    "ordinal": 1,
                                                    "tagName": "DIV",
                                                    "rowSpan": 1,
                                                    "colSpan": 1,
                                                    "textPrefix": "Wrong",
                                                    "textCharacterCount": 5,
                                                }
                                            ],
                                        }
                                    ],
                                }
                            ],
                        },
                    }
                },
            }
        ]
    )
    monkeypatch.setattr(
        tables_module,
        "_open_websocket",
        lambda url, *, timeout: websocket,
    )

    target = ChromiumPageTarget("page-1", "ws://devtools/page/page-1")

    with pytest.raises(ChromiumReadError, match="literal TH or TD"):
        read_chromium_page_tables(target)

    assert websocket.closed is True
