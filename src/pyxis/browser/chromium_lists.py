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


DEFAULT_LIST_LIMIT = 64
DEFAULT_LIST_ITEM_LIMIT = 128
DEFAULT_LIST_TEXT_LIMIT = 1024


@dataclass(frozen=True, slots=True)
class ChromiumPageListItemSnapshot:
    """One direct LI child fact from one observed OL/UL list."""

    ordinal: int
    value_attribute: str | None
    direct_text_prefix: str
    direct_text_character_count: int

    @property
    def direct_text_truncated(self) -> bool:
        return self.direct_text_character_count > len(self.direct_text_prefix)


@dataclass(frozen=True, slots=True)
class ChromiumPageListSnapshot:
    """One bounded literal OL/UL snapshot from the selected page target."""

    ordinal: int
    tag_name: str
    start_attribute: str | None
    parent_list_ordinal: int | None
    parent_item_ordinal: int | None
    items: tuple[ChromiumPageListItemSnapshot, ...]
    item_count: int

    @property
    def items_truncated(self) -> bool:
        return self.item_count > len(self.items)


@dataclass(frozen=True, slots=True)
class ChromiumPageListsSnapshot:
    """Bounded literal list-structure evidence from one selected page target."""

    url: str
    lists: tuple[ChromiumPageListSnapshot, ...]
    list_count: int

    @property
    def lists_truncated(self) -> bool:
        return self.list_count > len(self.lists)


def read_chromium_page_lists(
    target: ChromiumPageTarget,
    *,
    list_limit: int = DEFAULT_LIST_LIMIT,
    item_limit: int = DEFAULT_LIST_ITEM_LIMIT,
    text_limit: int = DEFAULT_LIST_TEXT_LIMIT,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
) -> ChromiumPageListsSnapshot:
    """Read literal OL/UL structure without flattening or repairing it.

    The fixed DevTools expression reads existing OL/UL elements in global DOM
    order. Each list preserves its literal tag, raw authored `start` attribute,
    nearest ancestor-list/item ordinals when nested, and only its direct LI
    children. Each item preserves its raw authored `value` attribute and a
    bounded direct-list text-node prefix that mechanically excludes text inside
    descendant OL/UL elements.

    It does not infer semantic hierarchy, repair numbering, flatten nested lists,
    rank items, mutate the DOM, activate targets, or navigate.
    """

    if list_limit < 0:
        raise ValueError("list_limit must be >= 0.")
    if item_limit < 0:
        raise ValueError("item_limit must be >= 0.")
    if text_limit < 0:
        raise ValueError("text_limit must be >= 0.")
    if timeout <= 0:
        raise ValueError("timeout must be > 0.")

    expression = (
        "(() => {"
        "const listNodes = Array.from(document.querySelectorAll('ol,ul'));"
        f"const lists = listNodes.slice(0, {list_limit}).map((list, listIndex) => {{"
        "const parentItem = list.parentElement ? list.parentElement.closest('li') : null;"
        "const parentList = parentItem ? parentItem.closest('ol,ul') : null;"
        "const parentListOrdinal = parentList ? listNodes.indexOf(parentList) + 1 : null;"
        "const parentItemNodes = parentList ? Array.from(parentList.children).filter((child) => child.tagName === 'LI') : [];"
        "const parentItemOrdinal = parentItem ? parentItemNodes.indexOf(parentItem) + 1 : null;"
        "const itemNodes = Array.from(list.children).filter((child) => child.tagName === 'LI');"
        f"const items = itemNodes.slice(0, {item_limit}).map((item, itemIndex) => {{"
        "const textParts = [];"
        "const walker = document.createTreeWalker(item, NodeFilter.SHOW_TEXT);"
        "while (walker.nextNode()) {"
        "const node = walker.currentNode;"
        "const parentElement = node.parentElement;"
        "if (parentElement && parentElement.closest('ol,ul') === list) {"
        "textParts.push(node.nodeValue || '');"
        "}"
        "}"
        "const directText = textParts.join('');"
        "const characters = Array.from(directText);"
        "return {"
        "ordinal: itemIndex + 1,"
        "valueAttribute: item.getAttribute('value'),"
        f"directTextPrefix: characters.slice(0, {text_limit}).join(''),"
        "directTextCharacterCount: characters.length"
        "};"
        "});"
        "return {"
        "ordinal: listIndex + 1,"
        "tagName: list.tagName,"
        "startAttribute: list.getAttribute('start'),"
        "parentListOrdinal,"
        "parentItemOrdinal,"
        "itemCount: itemNodes.length,"
        "items"
        "};"
        "});"
        "return {url: window.location.href, listCount: listNodes.length, lists};"
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
            f"Failed to read Chromium page lists for target {target.target_id}: {exc}"
        ) from exc
    finally:
        websocket.close()

    value = _extract_runtime_value(response)
    url = value.get("url")
    list_count = value.get("listCount")
    raw_lists = value.get("lists")

    if not isinstance(url, str):
        raise ChromiumReadError("Chromium lists snapshot URL was not a string.")
    if not isinstance(list_count, int) or list_count < 0:
        raise ChromiumReadError(
            "Chromium lists snapshot count was not a non-negative integer."
        )
    if not isinstance(raw_lists, list):
        raise ChromiumReadError("Chromium lists snapshot lists were not a list.")
    if len(raw_lists) > list_limit:
        raise ChromiumReadError(
            "Chromium lists snapshot exceeded the requested list limit."
        )
    if list_count < len(raw_lists):
        raise ChromiumReadError(
            "Chromium lists snapshot count is smaller than the returned lists."
        )

    lists: list[ChromiumPageListSnapshot] = []
    for expected_list_ordinal, raw_list in enumerate(raw_lists, start=1):
        if not isinstance(raw_list, dict):
            raise ChromiumReadError("Chromium list snapshot item was not an object.")

        list_ordinal = raw_list.get("ordinal")
        tag_name = raw_list.get("tagName")
        start_attribute = raw_list.get("startAttribute")
        parent_list_ordinal = raw_list.get("parentListOrdinal")
        parent_item_ordinal = raw_list.get("parentItemOrdinal")
        item_count = raw_list.get("itemCount")
        raw_items = raw_list.get("items")

        if list_ordinal != expected_list_ordinal:
            raise ChromiumReadError(
                "Chromium list snapshot ordinals were not contiguous DOM order."
            )
        if tag_name not in {"OL", "UL"}:
            raise ChromiumReadError("Chromium list tag was not literal OL or UL.")
        if start_attribute is not None and not isinstance(start_attribute, str):
            raise ChromiumReadError(
                "Chromium list start attribute was not a string or null."
            )
        if parent_list_ordinal is None:
            if parent_item_ordinal is not None:
                raise ChromiumReadError(
                    "Chromium list parent item existed without a parent list."
                )
        else:
            if (
                not isinstance(parent_list_ordinal, int)
                or parent_list_ordinal < 1
                or parent_list_ordinal >= list_ordinal
            ):
                raise ChromiumReadError(
                    "Chromium list parent ordinal did not identify an earlier ancestor list."
                )
            if not isinstance(parent_item_ordinal, int) or parent_item_ordinal < 1:
                raise ChromiumReadError(
                    "Chromium list parent item ordinal was not a positive integer."
                )
        if not isinstance(item_count, int) or item_count < 0:
            raise ChromiumReadError(
                "Chromium list item count was not a non-negative integer."
            )
        if not isinstance(raw_items, list):
            raise ChromiumReadError("Chromium list items were not a list.")
        if len(raw_items) > item_limit:
            raise ChromiumReadError(
                "Chromium list snapshot exceeded the requested item limit."
            )
        if item_count < len(raw_items):
            raise ChromiumReadError(
                "Chromium list item count is smaller than the returned items."
            )

        items: list[ChromiumPageListItemSnapshot] = []
        for expected_item_ordinal, raw_item in enumerate(raw_items, start=1):
            if not isinstance(raw_item, dict):
                raise ChromiumReadError("Chromium list item was not an object.")

            item_ordinal = raw_item.get("ordinal")
            value_attribute = raw_item.get("valueAttribute")
            direct_text_prefix = raw_item.get("directTextPrefix")
            direct_text_character_count = raw_item.get("directTextCharacterCount")

            if item_ordinal != expected_item_ordinal:
                raise ChromiumReadError(
                    "Chromium list item ordinals were not contiguous DOM order."
                )
            if value_attribute is not None and not isinstance(value_attribute, str):
                raise ChromiumReadError(
                    "Chromium list item value attribute was not a string or null."
                )
            if not isinstance(direct_text_prefix, str):
                raise ChromiumReadError(
                    "Chromium list item direct text prefix was not a string."
                )
            if (
                not isinstance(direct_text_character_count, int)
                or direct_text_character_count < 0
            ):
                raise ChromiumReadError(
                    "Chromium list item direct text count was not a non-negative integer."
                )
            if len(direct_text_prefix) > text_limit:
                raise ChromiumReadError(
                    "Chromium list item direct text exceeded the requested text limit."
                )
            if direct_text_character_count < len(direct_text_prefix):
                raise ChromiumReadError(
                    "Chromium list item direct text count is smaller than the returned prefix."
                )

            items.append(
                ChromiumPageListItemSnapshot(
                    ordinal=item_ordinal,
                    value_attribute=value_attribute,
                    direct_text_prefix=direct_text_prefix,
                    direct_text_character_count=direct_text_character_count,
                )
            )

        lists.append(
            ChromiumPageListSnapshot(
                ordinal=list_ordinal,
                tag_name=tag_name,
                start_attribute=start_attribute,
                parent_list_ordinal=parent_list_ordinal,
                parent_item_ordinal=parent_item_ordinal,
                items=tuple(items),
                item_count=item_count,
            )
        )

    return ChromiumPageListsSnapshot(
        url=url,
        lists=tuple(lists),
        list_count=list_count,
    )
