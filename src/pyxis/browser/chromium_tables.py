from __future__ import annotations

from dataclasses import dataclass
import json

from .chromium import (
    DEFAULT_TIMEOUT_SECONDS,
    ChromiumPageTarget,
    ChromiumReadError,
    _extract_runtime_value,
    _open_websocket,
    _receive_command_response,
)


DEFAULT_TABLE_LIMIT = 32
DEFAULT_TABLE_ROW_LIMIT = 128
DEFAULT_TABLE_CELL_LIMIT = 64
DEFAULT_TABLE_TEXT_LIMIT = 1024


@dataclass(frozen=True, slots=True)
class ChromiumPageTableCellSnapshot:
    """One literal table-cell DOM fact from the selected page target."""

    ordinal: int
    tag_name: str
    row_span: int
    col_span: int
    text_prefix: str
    text_character_count: int

    @property
    def text_truncated(self) -> bool:
        return self.text_character_count > len(self.text_prefix)


@dataclass(frozen=True, slots=True)
class ChromiumPageTableRowSnapshot:
    """One bounded DOM-order row from one observed HTML table."""

    ordinal: int
    cells: tuple[ChromiumPageTableCellSnapshot, ...]
    cell_count: int

    @property
    def cells_truncated(self) -> bool:
        return self.cell_count > len(self.cells)


@dataclass(frozen=True, slots=True)
class ChromiumPageTableSnapshot:
    """One bounded literal HTML-table snapshot from the selected page target."""

    ordinal: int
    caption_text_prefix: str
    caption_text_character_count: int
    rows: tuple[ChromiumPageTableRowSnapshot, ...]
    row_count: int

    @property
    def caption_text_truncated(self) -> bool:
        return self.caption_text_character_count > len(self.caption_text_prefix)

    @property
    def rows_truncated(self) -> bool:
        return self.row_count > len(self.rows)


@dataclass(frozen=True, slots=True)
class ChromiumPageTablesSnapshot:
    """Bounded literal table evidence from one selected existing page target."""

    url: str
    tables: tuple[ChromiumPageTableSnapshot, ...]
    table_count: int

    @property
    def tables_truncated(self) -> bool:
        return self.table_count > len(self.tables)


def read_chromium_page_tables(
    target: ChromiumPageTarget,
    *,
    table_limit: int = DEFAULT_TABLE_LIMIT,
    row_limit: int = DEFAULT_TABLE_ROW_LIMIT,
    cell_limit: int = DEFAULT_TABLE_CELL_LIMIT,
    text_limit: int = DEFAULT_TABLE_TEXT_LIMIT,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
) -> ChromiumPageTablesSnapshot:
    """Read literal HTML-table structure without normalizing it into a dataset.

    The fixed DevTools expression reads existing `table` elements in DOM order,
    their direct caption text when present, rows belonging to each exact table,
    and direct TH/TD children for each row. It preserves literal TH/TD tag names,
    browser-exposed row/column spans, bounded rendered text, and complete counts.

    It does not infer header relationships, expand spans, coerce values, flatten
    tables, rank tables, mutate the DOM, activate targets, or navigate.
    """

    if table_limit < 0:
        raise ValueError("table_limit must be >= 0.")
    if row_limit < 0:
        raise ValueError("row_limit must be >= 0.")
    if cell_limit < 0:
        raise ValueError("cell_limit must be >= 0.")
    if text_limit < 0:
        raise ValueError("text_limit must be >= 0.")
    if timeout <= 0:
        raise ValueError("timeout must be > 0.")

    expression = (
        "(() => {"
        "const tableNodes = Array.from(document.querySelectorAll('table'));"
        f"const tables = tableNodes.slice(0, {table_limit}).map((table, tableIndex) => {{"
        "const caption = Array.from(table.children).find((child) => child.tagName === 'CAPTION');"
        "const captionText = caption ? (caption.innerText || '') : '';"
        "const captionCharacters = Array.from(captionText);"
        "const rowNodes = Array.from(table.querySelectorAll('tr')).filter((row) => row.closest('table') === table);"
        f"const rows = rowNodes.slice(0, {row_limit}).map((row, rowIndex) => {{"
        "const cellNodes = Array.from(row.children).filter((cell) => cell.tagName === 'TH' || cell.tagName === 'TD');"
        f"const cells = cellNodes.slice(0, {cell_limit}).map((cell, cellIndex) => {{"
        "const text = cell.innerText || '';"
        "const characters = Array.from(text);"
        "return {"
        "ordinal: cellIndex + 1,"
        "tagName: cell.tagName,"
        "rowSpan: cell.rowSpan,"
        "colSpan: cell.colSpan,"
        f"textPrefix: characters.slice(0, {text_limit}).join(''),"
        "textCharacterCount: characters.length"
        "};"
        "});"
        "return {ordinal: rowIndex + 1, cellCount: cellNodes.length, cells};"
        "});"
        "return {"
        "ordinal: tableIndex + 1,"
        f"captionTextPrefix: captionCharacters.slice(0, {text_limit}).join(''),"
        "captionTextCharacterCount: captionCharacters.length,"
        "rowCount: rowNodes.length,"
        "rows"
        "};"
        "});"
        "return {url: window.location.href, tableCount: tableNodes.length, tables};"
        "})()"
    )
    command = {
        "id": 1,
        "method": "Runtime.evaluate",
        "params": {
            "expression": expression,
            "returnByValue": True,
        },
    }

    websocket = _open_websocket(target.websocket_debugger_url, timeout=timeout)
    try:
        websocket.send(json.dumps(command, sort_keys=True, separators=(",", ":")))
        response = _receive_command_response(websocket, command_id=1)
    except ChromiumReadError:
        raise
    except Exception as exc:  # pragma: no cover - transport-specific failure shape
        raise ChromiumReadError(
            f"Failed to read Chromium page tables for target {target.target_id}: {exc}"
        ) from exc
    finally:
        websocket.close()

    value = _extract_runtime_value(response)
    url = value.get("url")
    table_count = value.get("tableCount")
    raw_tables = value.get("tables")

    if not isinstance(url, str):
        raise ChromiumReadError("Chromium tables snapshot URL was not a string.")
    if not isinstance(table_count, int) or table_count < 0:
        raise ChromiumReadError(
            "Chromium tables snapshot count was not a non-negative integer."
        )
    if not isinstance(raw_tables, list):
        raise ChromiumReadError("Chromium tables snapshot tables were not a list.")
    if len(raw_tables) > table_limit:
        raise ChromiumReadError(
            "Chromium tables snapshot exceeded the requested table limit."
        )
    if table_count < len(raw_tables):
        raise ChromiumReadError(
            "Chromium tables snapshot count is smaller than the returned tables."
        )

    tables: list[ChromiumPageTableSnapshot] = []
    for expected_table_ordinal, raw_table in enumerate(raw_tables, start=1):
        if not isinstance(raw_table, dict):
            raise ChromiumReadError("Chromium table snapshot item was not an object.")

        table_ordinal = raw_table.get("ordinal")
        caption_text_prefix = raw_table.get("captionTextPrefix")
        caption_text_character_count = raw_table.get("captionTextCharacterCount")
        row_count = raw_table.get("rowCount")
        raw_rows = raw_table.get("rows")

        if table_ordinal != expected_table_ordinal:
            raise ChromiumReadError(
                "Chromium table snapshot ordinals were not contiguous DOM order."
            )
        if not isinstance(caption_text_prefix, str):
            raise ChromiumReadError("Chromium table caption prefix was not a string.")
        if (
            not isinstance(caption_text_character_count, int)
            or caption_text_character_count < 0
        ):
            raise ChromiumReadError(
                "Chromium table caption count was not a non-negative integer."
            )
        if len(caption_text_prefix) > text_limit:
            raise ChromiumReadError(
                "Chromium table caption exceeded the requested text limit."
            )
        if caption_text_character_count < len(caption_text_prefix):
            raise ChromiumReadError(
                "Chromium table caption count is smaller than the returned prefix."
            )
        if not isinstance(row_count, int) or row_count < 0:
            raise ChromiumReadError(
                "Chromium table row count was not a non-negative integer."
            )
        if not isinstance(raw_rows, list):
            raise ChromiumReadError("Chromium table rows were not a list.")
        if len(raw_rows) > row_limit:
            raise ChromiumReadError(
                "Chromium table snapshot exceeded the requested row limit."
            )
        if row_count < len(raw_rows):
            raise ChromiumReadError(
                "Chromium table row count is smaller than the returned rows."
            )

        rows: list[ChromiumPageTableRowSnapshot] = []
        for expected_row_ordinal, raw_row in enumerate(raw_rows, start=1):
            if not isinstance(raw_row, dict):
                raise ChromiumReadError("Chromium table row was not an object.")

            row_ordinal = raw_row.get("ordinal")
            cell_count = raw_row.get("cellCount")
            raw_cells = raw_row.get("cells")

            if row_ordinal != expected_row_ordinal:
                raise ChromiumReadError(
                    "Chromium table row ordinals were not contiguous DOM order."
                )
            if not isinstance(cell_count, int) or cell_count < 0:
                raise ChromiumReadError(
                    "Chromium table cell count was not a non-negative integer."
                )
            if not isinstance(raw_cells, list):
                raise ChromiumReadError("Chromium table cells were not a list.")
            if len(raw_cells) > cell_limit:
                raise ChromiumReadError(
                    "Chromium table row exceeded the requested cell limit."
                )
            if cell_count < len(raw_cells):
                raise ChromiumReadError(
                    "Chromium table cell count is smaller than the returned cells."
                )

            cells: list[ChromiumPageTableCellSnapshot] = []
            for expected_cell_ordinal, raw_cell in enumerate(raw_cells, start=1):
                if not isinstance(raw_cell, dict):
                    raise ChromiumReadError("Chromium table cell was not an object.")

                cell_ordinal = raw_cell.get("ordinal")
                tag_name = raw_cell.get("tagName")
                row_span = raw_cell.get("rowSpan")
                col_span = raw_cell.get("colSpan")
                text_prefix = raw_cell.get("textPrefix")
                text_character_count = raw_cell.get("textCharacterCount")

                if cell_ordinal != expected_cell_ordinal:
                    raise ChromiumReadError(
                        "Chromium table cell ordinals were not contiguous DOM order."
                    )
                if tag_name not in {"TH", "TD"}:
                    raise ChromiumReadError(
                        "Chromium table cell tag was not literal TH or TD."
                    )
                if not isinstance(row_span, int) or row_span < 0:
                    raise ChromiumReadError(
                        "Chromium table row span was not a non-negative integer."
                    )
                if not isinstance(col_span, int) or col_span < 0:
                    raise ChromiumReadError(
                        "Chromium table column span was not a non-negative integer."
                    )
                if not isinstance(text_prefix, str):
                    raise ChromiumReadError("Chromium table cell text prefix was not a string.")
                if not isinstance(text_character_count, int) or text_character_count < 0:
                    raise ChromiumReadError(
                        "Chromium table cell text count was not a non-negative integer."
                    )
                if len(text_prefix) > text_limit:
                    raise ChromiumReadError(
                        "Chromium table cell exceeded the requested text limit."
                    )
                if text_character_count < len(text_prefix):
                    raise ChromiumReadError(
                        "Chromium table cell text count is smaller than the returned prefix."
                    )

                cells.append(
                    ChromiumPageTableCellSnapshot(
                        ordinal=cell_ordinal,
                        tag_name=tag_name,
                        row_span=row_span,
                        col_span=col_span,
                        text_prefix=text_prefix,
                        text_character_count=text_character_count,
                    )
                )

            rows.append(
                ChromiumPageTableRowSnapshot(
                    ordinal=row_ordinal,
                    cells=tuple(cells),
                    cell_count=cell_count,
                )
            )

        tables.append(
            ChromiumPageTableSnapshot(
                ordinal=table_ordinal,
                caption_text_prefix=caption_text_prefix,
                caption_text_character_count=caption_text_character_count,
                rows=tuple(rows),
                row_count=row_count,
            )
        )

    return ChromiumPageTablesSnapshot(
        url=url,
        tables=tuple(tables),
        table_count=table_count,
    )
