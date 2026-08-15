from __future__ import annotations

from dataclasses import FrozenInstanceError
import importlib

import pytest

from pyxis.app import observe_chromium_page_tables
from pyxis.browser import (
    ChromiumPageTableCellSnapshot,
    ChromiumPageTableRowSnapshot,
    ChromiumPageTableSnapshot,
    ChromiumPageTablesSnapshot,
    ChromiumPageTarget,
    ChromiumReadError,
)


tables_module = importlib.import_module("pyxis.app.chromium_tables")


def test_observe_chromium_page_tables_projects_frozen_nested_evidence(monkeypatch) -> None:
    target = ChromiumPageTarget(
        target_id="page-1",
        websocket_debugger_url="ws://127.0.0.1:9222/devtools/page/page-1",
    )
    snapshot = ChromiumPageTablesSnapshot(
        url="https://example.test/data",
        tables=(
            ChromiumPageTableSnapshot(
                ordinal=1,
                caption_text_prefix="Study 😀",
                caption_text_character_count=13,
                rows=(
                    ChromiumPageTableRowSnapshot(
                        ordinal=1,
                        cells=(
                            ChromiumPageTableCellSnapshot(1, "TH", 2, 1, "Metric", 6),
                            ChromiumPageTableCellSnapshot(2, "TD", 1, 2, "Alpha 😀", 12),
                        ),
                        cell_count=3,
                    ),
                ),
                row_count=2,
            ),
        ),
        table_count=2,
    )
    calls: list[tuple] = []

    def fake_list(endpoint: str, *, timeout: float):
        calls.append(("list", endpoint, timeout))
        return (target,)

    def fake_read(
        selected,
        *,
        table_limit: int,
        row_limit: int,
        cell_limit: int,
        text_limit: int,
        timeout: float,
    ):
        calls.append(
            (
                "read",
                selected,
                table_limit,
                row_limit,
                cell_limit,
                text_limit,
                timeout,
            )
        )
        return snapshot

    monkeypatch.setattr(tables_module, "list_chromium_page_targets", fake_list)
    monkeypatch.setattr(tables_module, "read_chromium_page_tables", fake_read)

    evidence = observe_chromium_page_tables(
        " http://127.0.0.1:9222/ ",
        table_limit=1,
        row_limit=1,
        cell_limit=2,
        text_limit=7,
        timeout=2.0,
    )

    assert evidence.endpoint == "http://127.0.0.1:9222"
    assert evidence.target_id == "page-1"
    assert evidence.url == "https://example.test/data"
    assert evidence.source == "document.querySelectorAll('table')"
    assert evidence.table_count == 2
    assert evidence.table_limit == 1
    assert evidence.truncated is True
    table = evidence.tables[0]
    assert table.ordinal == 1
    assert table.caption_text_prefix == "Study 😀"
    assert table.caption_text_character_count == 13
    assert table.text_limit == 7
    assert table.caption_truncated is True
    assert table.row_count == 2
    assert table.row_limit == 1
    assert table.rows_truncated is True
    row = table.rows[0]
    assert row.ordinal == 1
    assert row.cell_count == 3
    assert row.cell_limit == 2
    assert row.truncated is True
    assert row.cells[0].tag_name == "TH"
    assert row.cells[0].row_span == 2
    assert row.cells[0].col_span == 1
    assert row.cells[0].text_prefix == "Metric"
    assert row.cells[0].truncated is False
    assert row.cells[1].tag_name == "TD"
    assert row.cells[1].col_span == 2
    assert row.cells[1].text_prefix == "Alpha 😀"
    assert row.cells[1].text_character_count == 12
    assert row.cells[1].text_limit == 7
    assert row.cells[1].truncated is True
    assert calls == [
        ("list", "http://127.0.0.1:9222", 2.0),
        ("read", target, 1, 1, 2, 7, 2.0),
    ]

    with pytest.raises(FrozenInstanceError):
        evidence.url = "changed"  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        evidence.tables[0].rows[0].cells[0].tag_name = "TD"  # type: ignore[misc]


def test_observe_chromium_page_tables_refuses_ambiguous_target_before_read(monkeypatch) -> None:
    targets = (
        ChromiumPageTarget("page-1", "ws://devtools/page/page-1"),
        ChromiumPageTarget("page-2", "ws://devtools/page/page-2"),
    )
    monkeypatch.setattr(
        tables_module,
        "list_chromium_page_targets",
        lambda endpoint, *, timeout: targets,
    )

    def fail_if_read(*args, **kwargs):
        raise AssertionError("Ambiguous target selection must fail before table read.")

    monkeypatch.setattr(tables_module, "read_chromium_page_tables", fail_if_read)

    with pytest.raises(ChromiumReadError, match="supply target_id explicitly"):
        observe_chromium_page_tables("http://127.0.0.1:9222")


def test_observe_chromium_page_tables_preserves_th_td_and_spans_without_expansion(monkeypatch) -> None:
    target = ChromiumPageTarget("page-1", "ws://devtools/page/page-1")
    monkeypatch.setattr(
        tables_module,
        "list_chromium_page_targets",
        lambda endpoint, *, timeout: (target,),
    )
    monkeypatch.setattr(
        tables_module,
        "read_chromium_page_tables",
        lambda selected, *, table_limit, row_limit, cell_limit, text_limit, timeout: ChromiumPageTablesSnapshot(
            url="https://example.test/",
            tables=(
                ChromiumPageTableSnapshot(
                    ordinal=1,
                    caption_text_prefix="",
                    caption_text_character_count=0,
                    rows=(
                        ChromiumPageTableRowSnapshot(
                            ordinal=1,
                            cells=(
                                ChromiumPageTableCellSnapshot(1, "TH", 2, 1, "Head", 4),
                                ChromiumPageTableCellSnapshot(2, "TD", 1, 3, "Value", 5),
                            ),
                            cell_count=2,
                        ),
                    ),
                    row_count=1,
                ),
            ),
            table_count=1,
        ),
    )

    evidence = observe_chromium_page_tables("http://127.0.0.1:9222")

    cells = evidence.tables[0].rows[0].cells
    assert tuple(cell.tag_name for cell in cells) == ("TH", "TD")
    assert tuple((cell.row_span, cell.col_span) for cell in cells) == ((2, 1), (1, 3))
    assert len(cells) == 2
