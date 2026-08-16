from __future__ import annotations

from dataclasses import asdict, dataclass, fields, is_dataclass
import json
from pathlib import Path
import types
from typing import Any, get_args, get_origin, get_type_hints

from .chromium_headings import ChromiumPageHeadingsEvidence
from .chromium_lists import ChromiumPageListsEvidence
from .chromium_metadata import ChromiumPageMetadataEvidence
from .chromium_observation import ChromiumPageLinksEvidence, ChromiumPageObservationEvidence
from .chromium_paragraphs import ChromiumPageParagraphsEvidence
from .chromium_research_bundle import ChromiumPageResearchEvidenceBundle
from .chromium_research_capture import (
    ChromiumPageResearchCaptureVerificationEvidence,
    ChromiumResearchCaptureIntegrityError,
    verify_chromium_page_research_capture,
)
from .chromium_tables import ChromiumPageTablesEvidence


_ACQUISITION_MODE = "sequential_non_atomic_url_coherent"
_ACQUISITION_ORDER = (
    "page",
    "links",
    "headings",
    "metadata",
    "paragraphs",
    "tables",
    "lists",
)


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchLoadedCaptureEvidence:
    """One verified durable capture reopened as typed research evidence.

    `verification` retains the exact 16B file-level integrity evidence that
    authorized rehydration. `bundle` is a newly constructed immutable 16A-shaped
    evidence object reconstructed only after the persisted nested evidence passes
    structural and domain validation.

    Rehydration does not make the capture a fresh Chromium observation and does
    not strengthen source identity, authenticity, temporal provenance, quotation
    truth, citation stability, or atomic-snapshot claims.
    """

    verification: ChromiumPageResearchCaptureVerificationEvidence
    bundle: ChromiumPageResearchEvidenceBundle


def load_chromium_page_research_capture(
    source: Path,
) -> ChromiumPageResearchLoadedCaptureEvidence:
    """Verify and losslessly reopen one durable capture as typed evidence.

    File verification remains owned by the established 16B boundary. Only after
    that succeeds does 16C reconstruct the exact nested application dataclasses,
    validate their evidence invariants, and prove that serialization of the new
    typed bundle reproduces the persisted JSON payload without normalization.

    This function performs no Chromium acquisition, browser discovery, target
    selection, navigation, persistence, ranking, interpretation, or provenance
    authentication.
    """

    verification = verify_chromium_page_research_capture(source)
    document = json.loads(verification.document_json)
    payload = document["bundle"]

    bundle = _decode_dataclass(
        ChromiumPageResearchEvidenceBundle,
        payload,
        path="bundle",
    )
    _validate_rehydrated_bundle(bundle)

    round_trip_payload = json.loads(
        json.dumps(
            asdict(bundle),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    )
    if round_trip_payload != payload:
        raise ChromiumResearchCaptureIntegrityError(
            "Research capture typed rehydration did not reproduce the persisted bundle payload."
        )

    return ChromiumPageResearchLoadedCaptureEvidence(
        verification=verification,
        bundle=bundle,
    )


def _decode_dataclass(cls: type[Any], payload: Any, *, path: str) -> Any:
    if not is_dataclass(cls):
        raise TypeError(f"{cls!r} is not a dataclass type.")
    if type(payload) is not dict:
        raise ChromiumResearchCaptureIntegrityError(
            f"Research capture {path} must be a JSON object."
        )

    dataclass_fields = fields(cls)
    expected_keys = {field.name for field in dataclass_fields}
    if set(payload) != expected_keys:
        raise ChromiumResearchCaptureIntegrityError(
            f"Research capture {path} has an invalid field set."
        )

    hints = get_type_hints(cls)
    values: dict[str, Any] = {}
    for field in dataclass_fields:
        field_path = f"{path}.{field.name}"
        values[field.name] = _decode_value(
            hints[field.name],
            payload[field.name],
            path=field_path,
        )
    return cls(**values)


def _decode_value(annotation: Any, value: Any, *, path: str) -> Any:
    if annotation is str:
        if type(value) is not str:
            _type_error(path, "string")
        return value
    if annotation is int:
        if type(value) is not int:
            _type_error(path, "integer")
        return value
    if annotation is bool:
        if type(value) is not bool:
            _type_error(path, "boolean")
        return value
    if annotation is type(None):
        if value is not None:
            _type_error(path, "null")
        return None

    origin = get_origin(annotation)
    if origin is tuple:
        args = get_args(annotation)
        if len(args) != 2 or args[1] is not Ellipsis:
            raise TypeError(f"Unsupported tuple annotation at {path}: {annotation!r}")
        if type(value) is not list:
            _type_error(path, "array")
        return tuple(
            _decode_value(args[0], item, path=f"{path}[{index}]")
            for index, item in enumerate(value)
        )

    if origin is types.UnionType:
        options = get_args(annotation)
        if value is None and type(None) in options:
            return None
        non_none = tuple(option for option in options if option is not type(None))
        if len(non_none) == 1:
            return _decode_value(non_none[0], value, path=path)
        raise TypeError(f"Unsupported union annotation at {path}: {annotation!r}")

    if isinstance(annotation, type) and is_dataclass(annotation):
        return _decode_dataclass(annotation, value, path=path)

    raise TypeError(f"Unsupported capture annotation at {path}: {annotation!r}")


def _type_error(path: str, expected: str) -> None:
    raise ChromiumResearchCaptureIntegrityError(
        f"Research capture {path} must be a JSON {expected}."
    )


def _validate_rehydrated_bundle(bundle: ChromiumPageResearchEvidenceBundle) -> None:
    if bundle.acquisition_mode != _ACQUISITION_MODE:
        _invalid("bundle acquisition mode is unsupported")
    if bundle.acquisition_order != _ACQUISITION_ORDER:
        _invalid("bundle acquisition order is unsupported")
    if not all((bundle.endpoint, bundle.target_id, bundle.url)):
        _invalid("bundle identity fields must be non-empty strings")

    members = (
        ("page", bundle.page),
        ("links", bundle.links),
        ("headings", bundle.headings),
        ("metadata", bundle.metadata),
        ("paragraphs", bundle.paragraphs),
        ("tables", bundle.tables),
        ("lists", bundle.lists),
    )
    for name, member in members:
        if member.endpoint != bundle.endpoint:
            _invalid(f"{name} endpoint is incoherent")
        if member.target_id != bundle.target_id:
            _invalid(f"{name} target_id is incoherent")
        if member.url != bundle.url:
            _invalid(f"{name} url is incoherent")

    _validate_page(bundle.page)
    _validate_links(bundle.links)
    _validate_headings(bundle.headings)
    _validate_metadata(bundle.metadata)
    _validate_paragraphs(bundle.paragraphs)
    _validate_tables(bundle.tables)
    _validate_lists(bundle.lists)


def _validate_page(page: ChromiumPageObservationEvidence) -> None:
    if page.content.source != "document.body.innerText":
        _invalid("page content source is unsupported")
    _validate_text(
        page.content.text_prefix,
        page.content.text_character_count,
        page.content.text_limit,
        page.content.truncated,
        "page content",
    )


def _validate_links(links: ChromiumPageLinksEvidence) -> None:
    if links.source != "document.querySelectorAll('a[href]')":
        _invalid("links source is unsupported")
    _validate_collection(
        links.links,
        links.link_count,
        links.link_limit,
        links.truncated,
        "links",
    )
    for expected, link in enumerate(links.links, start=1):
        if link.ordinal != expected:
            _invalid("link ordinals are not contiguous DOM order")
        _validate_text(
            link.text_prefix,
            link.text_character_count,
            link.text_limit,
            link.truncated,
            f"link {expected} text",
        )


def _validate_headings(headings: ChromiumPageHeadingsEvidence) -> None:
    if headings.source != "document.querySelectorAll('h1,h2,h3,h4,h5,h6')":
        _invalid("headings source is unsupported")
    _validate_collection(
        headings.headings,
        headings.heading_count,
        headings.heading_limit,
        headings.truncated,
        "headings",
    )
    for expected, heading in enumerate(headings.headings, start=1):
        if heading.ordinal != expected:
            _invalid("heading ordinals are not contiguous DOM order")
        if not 1 <= heading.level <= 6:
            _invalid("heading level is not from 1 through 6")
        _validate_text(
            heading.text_prefix,
            heading.text_character_count,
            heading.text_limit,
            heading.truncated,
            f"heading {expected} text",
        )


def _validate_metadata(metadata: ChromiumPageMetadataEvidence) -> None:
    if metadata.language_source != "document.documentElement.getAttribute('lang')":
        _invalid("metadata language source is unsupported")
    if metadata.canonical_source != 'document.querySelectorAll("link[rel~=\'canonical\' i][href]")':
        _invalid("metadata canonical source is unsupported")
    if metadata.description_source != 'document.querySelectorAll("meta[name=\'description\' i]")':
        _invalid("metadata description source is unsupported")

    _validate_collection(
        metadata.canonical_links,
        metadata.canonical_link_count,
        metadata.canonical_link_limit,
        metadata.canonical_links_truncated,
        "canonical links",
    )
    for expected, link in enumerate(metadata.canonical_links, start=1):
        if link.ordinal != expected:
            _invalid("canonical-link ordinals are not contiguous DOM order")

    _validate_collection(
        metadata.descriptions,
        metadata.description_count,
        metadata.description_limit,
        metadata.descriptions_truncated,
        "meta descriptions",
    )
    for expected, description in enumerate(metadata.descriptions, start=1):
        if description.ordinal != expected:
            _invalid("meta-description ordinals are not contiguous DOM order")
        _validate_text(
            description.content_prefix,
            description.content_character_count,
            description.content_limit,
            description.truncated,
            f"meta description {expected} text",
        )


def _validate_paragraphs(paragraphs: ChromiumPageParagraphsEvidence) -> None:
    if paragraphs.source != "document.querySelectorAll('p')":
        _invalid("paragraphs source is unsupported")
    _validate_collection(
        paragraphs.paragraphs,
        paragraphs.paragraph_count,
        paragraphs.paragraph_limit,
        paragraphs.truncated,
        "paragraphs",
    )
    for expected, paragraph in enumerate(paragraphs.paragraphs, start=1):
        if paragraph.ordinal != expected:
            _invalid("paragraph ordinals are not contiguous DOM order")
        _validate_text(
            paragraph.text_prefix,
            paragraph.text_character_count,
            paragraph.text_limit,
            paragraph.truncated,
            f"paragraph {expected} text",
        )


def _validate_tables(tables: ChromiumPageTablesEvidence) -> None:
    if tables.source != "document.querySelectorAll('table')":
        _invalid("tables source is unsupported")
    _validate_collection(
        tables.tables,
        tables.table_count,
        tables.table_limit,
        tables.truncated,
        "tables",
    )
    for expected_table, table in enumerate(tables.tables, start=1):
        if table.ordinal != expected_table:
            _invalid("table ordinals are not contiguous DOM order")
        _validate_text(
            table.caption_text_prefix,
            table.caption_text_character_count,
            table.text_limit,
            table.caption_truncated,
            f"table {expected_table} caption",
        )
        _validate_collection(
            table.rows,
            table.row_count,
            table.row_limit,
            table.rows_truncated,
            f"table {expected_table} rows",
        )
        for expected_row, row in enumerate(table.rows, start=1):
            if row.ordinal != expected_row:
                _invalid("table row ordinals are not contiguous DOM order")
            _validate_collection(
                row.cells,
                row.cell_count,
                row.cell_limit,
                row.truncated,
                f"table {expected_table} row {expected_row} cells",
            )
            for expected_cell, cell in enumerate(row.cells, start=1):
                if cell.ordinal != expected_cell:
                    _invalid("table cell ordinals are not contiguous DOM order")
                if cell.tag_name not in {"TH", "TD"}:
                    _invalid("table cell tag is not literal TH or TD")
                if cell.row_span < 0 or cell.col_span < 0:
                    _invalid("table cell spans are negative")
                if cell.text_limit != table.text_limit:
                    _invalid("table cell text limit differs from its table text limit")
                _validate_text(
                    cell.text_prefix,
                    cell.text_character_count,
                    cell.text_limit,
                    cell.truncated,
                    f"table {expected_table} row {expected_row} cell {expected_cell} text",
                )


def _validate_lists(lists: ChromiumPageListsEvidence) -> None:
    if lists.source != "document.querySelectorAll('ol,ul')":
        _invalid("lists source is unsupported")
    _validate_collection(
        lists.lists,
        lists.list_count,
        lists.list_limit,
        lists.truncated,
        "lists",
    )
    for expected_list, observed_list in enumerate(lists.lists, start=1):
        if observed_list.ordinal != expected_list:
            _invalid("list ordinals are not contiguous DOM order")
        if observed_list.tag_name not in {"OL", "UL"}:
            _invalid("list tag is not literal OL or UL")
        if observed_list.parent_list_ordinal is None:
            if observed_list.parent_item_ordinal is not None:
                _invalid("list parent item exists without a parent list")
        else:
            if not 1 <= observed_list.parent_list_ordinal < observed_list.ordinal:
                _invalid("list parent ordinal does not identify an earlier ancestor list")
            if observed_list.parent_item_ordinal is None or observed_list.parent_item_ordinal < 1:
                _invalid("list parent item ordinal is not a positive integer")
        _validate_collection(
            observed_list.items,
            observed_list.item_count,
            observed_list.item_limit,
            observed_list.truncated,
            f"list {expected_list} items",
        )
        for expected_item, item in enumerate(observed_list.items, start=1):
            if item.ordinal != expected_item:
                _invalid("list item ordinals are not contiguous DOM order")
            _validate_text(
                item.direct_text_prefix,
                item.direct_text_character_count,
                item.text_limit,
                item.truncated,
                f"list {expected_list} item {expected_item} text",
            )


def _validate_collection(
    returned: tuple[Any, ...],
    complete_count: int,
    limit: int,
    truncated: bool,
    label: str,
) -> None:
    if complete_count < 0:
        _invalid(f"{label} count is negative")
    if limit < 0:
        _invalid(f"{label} limit is negative")
    if len(returned) > limit:
        _invalid(f"{label} exceed the recorded limit")
    if complete_count < len(returned):
        _invalid(f"{label} count is smaller than the returned evidence")
    if truncated != (complete_count > len(returned)):
        _invalid(f"{label} truncation flag is incoherent")


def _validate_text(
    prefix: str,
    complete_count: int,
    limit: int,
    truncated: bool,
    label: str,
) -> None:
    if complete_count < 0:
        _invalid(f"{label} character count is negative")
    if limit < 0:
        _invalid(f"{label} limit is negative")
    if len(prefix) > limit:
        _invalid(f"{label} exceeds the recorded text limit")
    if complete_count < len(prefix):
        _invalid(f"{label} character count is smaller than the returned prefix")
    if truncated != (complete_count > len(prefix)):
        _invalid(f"{label} truncation flag is incoherent")


def _invalid(message: str) -> None:
    raise ChromiumResearchCaptureIntegrityError(
        f"Research capture cannot be rehydrated: {message}."
    )
