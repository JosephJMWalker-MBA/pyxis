from __future__ import annotations

from dataclasses import dataclass

from pyxis.browser import (
    ChromiumPageListsSnapshot,
    ChromiumReadError,
    list_chromium_page_targets,
    normalize_chromium_endpoint,
    read_chromium_page_lists,
)

from .chromium_observation import _select_page_target


@dataclass(frozen=True, slots=True)
class ChromiumPageListItemEvidence:
    """One direct LI child observed in one literal list."""

    ordinal: int
    value_attribute: str | None
    direct_text_prefix: str
    direct_text_character_count: int
    text_limit: int
    truncated: bool


@dataclass(frozen=True, slots=True)
class ChromiumPageListEvidence:
    """One bounded literal OL/UL observed on the selected page."""

    ordinal: int
    tag_name: str
    start_attribute: str | None
    parent_list_ordinal: int | None
    parent_item_ordinal: int | None
    items: tuple[ChromiumPageListItemEvidence, ...]
    item_count: int
    item_limit: int
    truncated: bool


@dataclass(frozen=True, slots=True)
class ChromiumPageListsEvidence:
    """Bounded literal list-structure evidence from one explicit Chromium page."""

    endpoint: str
    target_id: str
    url: str
    source: str
    lists: tuple[ChromiumPageListEvidence, ...]
    list_count: int
    list_limit: int
    truncated: bool


def observe_chromium_page_lists(
    endpoint: str,
    *,
    target_id: str | None = None,
    list_limit: int = 64,
    item_limit: int = 128,
    text_limit: int = 1024,
    timeout: float = 5.0,
) -> ChromiumPageListsEvidence:
    """Observe literal OL/UL structure without inventing list semantics.

    Evidence preserves global list DOM order, literal OL/UL identity, raw authored
    `start` and `value` attributes, nearest ancestor-list/item ordinals, only
    direct LI children, bounded direct-list text-node evidence, complete counts,
    and mechanical truncation. It does not repair numbering, flatten nesting,
    infer semantic hierarchy, rank items, navigate, persist, or interpret.
    """

    normalized_endpoint = normalize_chromium_endpoint(endpoint)
    targets = list_chromium_page_targets(normalized_endpoint, timeout=timeout)
    target = _select_page_target(targets, target_id=target_id)
    snapshot = read_chromium_page_lists(
        target,
        list_limit=list_limit,
        item_limit=item_limit,
        text_limit=text_limit,
        timeout=timeout,
    )
    return _create_lists_observation(
        endpoint=normalized_endpoint,
        target_id=target.target_id,
        snapshot=snapshot,
        list_limit=list_limit,
        item_limit=item_limit,
        text_limit=text_limit,
    )


def _create_lists_observation(
    *,
    endpoint: str,
    target_id: str,
    snapshot: ChromiumPageListsSnapshot,
    list_limit: int,
    item_limit: int,
    text_limit: int,
) -> ChromiumPageListsEvidence:
    if list_limit < 0:
        raise ValueError("list_limit must be >= 0.")
    if item_limit < 0:
        raise ValueError("item_limit must be >= 0.")
    if text_limit < 0:
        raise ValueError("text_limit must be >= 0.")
    if len(snapshot.lists) > list_limit:
        raise ChromiumReadError(
            "Chromium lists snapshot exceeded the requested list limit."
        )
    if snapshot.list_count < len(snapshot.lists):
        raise ChromiumReadError(
            "Chromium lists snapshot count is smaller than the returned lists."
        )

    lists: list[ChromiumPageListEvidence] = []
    for expected_list_ordinal, observed_list in enumerate(snapshot.lists, start=1):
        if observed_list.ordinal != expected_list_ordinal:
            raise ChromiumReadError(
                "Chromium list evidence ordinals were not contiguous DOM order."
            )
        if observed_list.tag_name not in {"OL", "UL"}:
            raise ChromiumReadError("Chromium list tag was not literal OL or UL.")
        if (
            observed_list.start_attribute is not None
            and not isinstance(observed_list.start_attribute, str)
        ):
            raise ChromiumReadError(
                "Chromium list start attribute was not a string or null."
            )
        if observed_list.parent_list_ordinal is None:
            if observed_list.parent_item_ordinal is not None:
                raise ChromiumReadError(
                    "Chromium list parent item existed without a parent list."
                )
        else:
            if (
                observed_list.parent_list_ordinal < 1
                or observed_list.parent_list_ordinal >= observed_list.ordinal
            ):
                raise ChromiumReadError(
                    "Chromium list parent ordinal did not identify an earlier ancestor list."
                )
            if (
                observed_list.parent_item_ordinal is None
                or observed_list.parent_item_ordinal < 1
            ):
                raise ChromiumReadError(
                    "Chromium list parent item ordinal was not a positive integer."
                )
        if len(observed_list.items) > item_limit:
            raise ChromiumReadError(
                "Chromium list snapshot exceeded the requested item limit."
            )
        if observed_list.item_count < len(observed_list.items):
            raise ChromiumReadError(
                "Chromium list item count is smaller than the returned items."
            )

        items: list[ChromiumPageListItemEvidence] = []
        for expected_item_ordinal, item in enumerate(observed_list.items, start=1):
            if item.ordinal != expected_item_ordinal:
                raise ChromiumReadError(
                    "Chromium list item evidence ordinals were not contiguous DOM order."
                )
            if item.value_attribute is not None and not isinstance(item.value_attribute, str):
                raise ChromiumReadError(
                    "Chromium list item value attribute was not a string or null."
                )
            if len(item.direct_text_prefix) > text_limit:
                raise ChromiumReadError(
                    "Chromium list item direct text exceeded the requested text limit."
                )
            if item.direct_text_character_count < len(item.direct_text_prefix):
                raise ChromiumReadError(
                    "Chromium list item direct text count is smaller than the returned prefix."
                )
            items.append(
                ChromiumPageListItemEvidence(
                    ordinal=item.ordinal,
                    value_attribute=item.value_attribute,
                    direct_text_prefix=item.direct_text_prefix,
                    direct_text_character_count=item.direct_text_character_count,
                    text_limit=text_limit,
                    truncated=item.direct_text_truncated,
                )
            )

        lists.append(
            ChromiumPageListEvidence(
                ordinal=observed_list.ordinal,
                tag_name=observed_list.tag_name,
                start_attribute=observed_list.start_attribute,
                parent_list_ordinal=observed_list.parent_list_ordinal,
                parent_item_ordinal=observed_list.parent_item_ordinal,
                items=tuple(items),
                item_count=observed_list.item_count,
                item_limit=item_limit,
                truncated=observed_list.items_truncated,
            )
        )

    return ChromiumPageListsEvidence(
        endpoint=endpoint,
        target_id=target_id,
        url=snapshot.url,
        source="document.querySelectorAll('ol,ul')",
        lists=tuple(lists),
        list_count=snapshot.list_count,
        list_limit=list_limit,
        truncated=snapshot.lists_truncated,
    )
