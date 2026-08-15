from __future__ import annotations

from dataclasses import dataclass

from pyxis.browser import (
    ChromiumPageTablesSnapshot,
    ChromiumReadError,
    list_chromium_page_targets,
    normalize_chromium_endpoint,
    read_chromium_page_tables,
)

from .chromium_observation import _select_page_target


@dataclass(frozen=True, slots=True)
class ChromiumPageTableCellEvidence:
    """One literal TH/TD cell observed in one table row."""

    ordinal: int
    tag_name: str
    row_span: int
    col_span: int
    text_prefix: str
    text_character_count: int
    text_limit: int
    truncated: bool


@dataclass(frozen=True, slots=True)
class ChromiumPageTableRowEvidence:
    """One bounded DOM-order table row."""

    ordinal: int
    cells: tuple[ChromiumPageTableCellEvidence, ...]
    cell_count: int
    cell_limit: int
    truncated: bool


@dataclass(frozen=True, slots=True)
class ChromiumPageTableEvidence:
    """One bounded literal table observed on the selected page."""

    ordinal: int
    caption_text_prefix: str
    caption_text_character_count: int
    text_limit: int
    caption_truncated: bool
    rows: tuple[ChromiumPageTableRowEvidence, ...]
    row_count: int
    row_limit: int
    rows_truncated: bool


@dataclass(frozen=True, slots=True)
class ChromiumPageTablesEvidence:
    """Bounded literal HTML-table evidence from one explicit Chromium page."""

    endpoint: str
    target_id: str
    url: str
    source: str
    tables: tuple[ChromiumPageTableEvidence, ...]
    table_count: int
    table_limit: int
    truncated: bool


def observe_chromium_page_tables(
    endpoint: str,
    *,
    target_id: str | None = None,
    table_limit: int = 32,
    row_limit: int = 128,
    cell_limit: int = 64,
    text_limit: int = 1024,
    timeout: float = 5.0,
) -> ChromiumPageTablesEvidence:
    """Observe literal HTML-table structure without inventing table semantics.

    Evidence preserves DOM table/row/cell order, direct TH/TD tag identity,
    browser-exposed row/column spans, direct caption text, bounded cell text,
    complete counts, and mechanical truncation. It does not infer header-to-cell
    relationships, expand spans, coerce values, flatten tables, rank tables,
    navigate, persist, or interpret the observed structure.
    """

    normalized_endpoint = normalize_chromium_endpoint(endpoint)
    targets = list_chromium_page_targets(normalized_endpoint, timeout=timeout)
    target = _select_page_target(targets, target_id=target_id)
    snapshot = read_chromium_page_tables(
        target,
        table_limit=table_limit,
        row_limit=row_limit,
        cell_limit=cell_limit,
        text_limit=text_limit,
        timeout=timeout,
    )
    return _create_tables_observation(
        endpoint=normalized_endpoint,
        target_id=target.target_id,
        snapshot=snapshot,
        table_limit=table_limit,
        row_limit=row_limit,
        cell_limit=cell_limit,
        text_limit=text_limit,
    )


def _create_tables_observation(
    *,
    endpoint: str,
    target_id: str,
    snapshot: ChromiumPageTablesSnapshot,
    table_limit: int,
    row_limit: int,
    cell_limit: int,
    text_limit: int,
) -> ChromiumPageTablesEvidence:
    if table_limit < 0:
        raise ValueError("table_limit must be >= 0.")
    if row_limit < 0:
        raise ValueError("row_limit must be >= 0.")
    if cell_limit < 0:
        raise ValueError("cell_limit must be >= 0.")
    if text_limit < 0:
        raise ValueError("text_limit must be >= 0.")
    if len(snapshot.tables) > table_limit:
        raise ChromiumReadError(
            "Chromium tables snapshot exceeded the requested table limit."
        )
    if snapshot.table_count < len(snapshot.tables):
        raise ChromiumReadError(
            "Chromium tables snapshot count is smaller than the returned tables."
        )

    tables: list[ChromiumPageTableEvidence] = []
    for expected_table_ordinal, table in enumerate(snapshot.tables, start=1):
        if table.ordinal != expected_table_ordinal:
            raise ChromiumReadError(
                "Chromium table evidence ordinals were not contiguous DOM order."
            )
        if len(table.caption_text_prefix) > text_limit:
            raise ChromiumReadError(
                "Chromium table caption exceeded the requested text limit."
            )
        if table.caption_text_character_count < len(table.caption_text_prefix):
            raise ChromiumReadError(
                "Chromium table caption count is smaller than the returned prefix."
            )
        if len(table.rows) > row_limit:
            raise ChromiumReadError(
                "Chromium table snapshot exceeded the requested row limit."
            )
        if table.row_count < len(table.rows):
            raise ChromiumReadError(
                "Chromium table row count is smaller than the returned rows."
            )

        rows: list[ChromiumPageTableRowEvidence] = []
        for expected_row_ordinal, row in enumerate(table.rows, start=1):
            if row.ordinal != expected_row_ordinal:
                raise ChromiumReadError(
                    "Chromium table row evidence ordinals were not contiguous DOM order."
                )
            if len(row.cells) > cell_limit:
                raise ChromiumReadError(
                    "Chromium table row exceeded the requested cell limit."
                )
            if row.cell_count < len(row.cells):
                raise ChromiumReadError(
                    "Chromium table cell count is smaller than the returned cells."
                )

            cells: list[ChromiumPageTableCellEvidence] = []
            for expected_cell_ordinal, cell in enumerate(row.cells, start=1):
                if cell.ordinal != expected_cell_ordinal:
                    raise ChromiumReadError(
                        "Chromium table cell evidence ordinals were not contiguous DOM order."
                    )
                if cell.tag_name not in {"TH", "TD"}:
                    raise ChromiumReadError(
                        "Chromium table cell tag was not literal TH or TD."
                    )
                if cell.row_span < 0 or cell.col_span < 0:
                    raise ChromiumReadError(
                        "Chromium table cell spans were not non-negative integers."
                    )
                if len(cell.text_prefix) > text_limit:
                    raise ChromiumReadError(
                        "Chromium table cell exceeded the requested text limit."
                    )
                if cell.text_character_count < len(cell.text_prefix):
                    raise ChromiumReadError(
                        "Chromium table cell text count is smaller than the returned prefix."
                    )
                cells.append(
                    ChromiumPageTableCellEvidence(
                        ordinal=cell.ordinal,
                        tag_name=cell.tag_name,
                        row_span=cell.row_span,
                        col_span=cell.col_span,
                        text_prefix=cell.text_prefix,
                        text_character_count=cell.text_character_count,
                        text_limit=text_limit,
                        truncated=cell.text_truncated,
                    )
                )

            rows.append(
                ChromiumPageTableRowEvidence(
                    ordinal=row.ordinal,
                    cells=tuple(cells),
                    cell_count=row.cell_count,
                    cell_limit=cell_limit,
                    truncated=row.cells_truncated,
                )
            )

        tables.append(
            ChromiumPageTableEvidence(
                ordinal=table.ordinal,
                caption_text_prefix=table.caption_text_prefix,
                caption_text_character_count=table.caption_text_character_count,
                text_limit=text_limit,
                caption_truncated=table.caption_text_truncated,
                rows=tuple(rows),
                row_count=table.row_count,
                row_limit=row_limit,
                rows_truncated=table.rows_truncated,
            )
        )

    return ChromiumPageTablesEvidence(
        endpoint=endpoint,
        target_id=target_id,
        url=snapshot.url,
        source="document.querySelectorAll('table')",
        tables=tuple(tables),
        table_count=snapshot.table_count,
        table_limit=table_limit,
        truncated=snapshot.tables_truncated,
    )
