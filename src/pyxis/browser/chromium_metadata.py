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


DEFAULT_CANONICAL_LINK_LIMIT = 8
DEFAULT_DESCRIPTION_LIMIT = 8
DEFAULT_DESCRIPTION_TEXT_LIMIT = 512


@dataclass(frozen=True, slots=True)
class ChromiumPageCanonicalLinkSnapshot:
    """One page-authored canonical-link declaration observed in DOM order."""

    ordinal: int
    raw_href: str
    resolved_href: str


@dataclass(frozen=True, slots=True)
class ChromiumPageDescriptionSnapshot:
    """One page-authored meta-description declaration observed in DOM order."""

    ordinal: int
    content_prefix: str
    content_character_count: int

    @property
    def content_truncated(self) -> bool:
        return self.content_character_count > len(self.content_prefix)


@dataclass(frozen=True, slots=True)
class ChromiumPageMetadataSnapshot:
    """Bounded page-declared metadata from one selected existing page target."""

    url: str
    document_language: str
    canonical_links: tuple[ChromiumPageCanonicalLinkSnapshot, ...]
    canonical_link_count: int
    descriptions: tuple[ChromiumPageDescriptionSnapshot, ...]
    description_count: int

    @property
    def canonical_links_truncated(self) -> bool:
        return self.canonical_link_count > len(self.canonical_links)

    @property
    def descriptions_truncated(self) -> bool:
        return self.description_count > len(self.descriptions)


def read_chromium_page_metadata(
    target: ChromiumPageTarget,
    *,
    canonical_link_limit: int = DEFAULT_CANONICAL_LINK_LIMIT,
    description_limit: int = DEFAULT_DESCRIPTION_LIMIT,
    description_text_limit: int = DEFAULT_DESCRIPTION_TEXT_LIMIT,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
) -> ChromiumPageMetadataSnapshot:
    """Read literal page-declared metadata without treating declarations as truth.

    The fixed expression reads the authored document `lang` attribute, bounded
    canonical-link declarations, and bounded meta-description declarations.
    Duplicate or conflicting declarations remain separate evidence. This read
    does not validate language tags, choose a canonical URL, fetch a destination,
    mutate the page, activate a target, or navigate.
    """

    if canonical_link_limit < 0:
        raise ValueError("canonical_link_limit must be >= 0.")
    if description_limit < 0:
        raise ValueError("description_limit must be >= 0.")
    if description_text_limit < 0:
        raise ValueError("description_text_limit must be >= 0.")
    if timeout <= 0:
        raise ValueError("timeout must be > 0.")

    expression = (
        "(() => {"
        "const root = document.documentElement;"
        "const documentLanguage = root ? (root.getAttribute('lang') || '') : '';"
        "const canonicalNodes = Array.from(document.querySelectorAll(\"link[rel~='canonical' i][href]\"));"
        f"const canonicalLinks = canonicalNodes.slice(0, {canonical_link_limit}).map((link, index) => ({{"
        "ordinal: index + 1,"
        "rawHref: link.getAttribute('href') || '',"
        "resolvedHref: link.href"
        "}));"
        "const descriptionNodes = Array.from(document.querySelectorAll(\"meta[name='description' i]\"));"
        f"const descriptions = descriptionNodes.slice(0, {description_limit}).map((meta, index) => {{"
        "const content = meta.getAttribute('content') || '';"
        "const characters = Array.from(content);"
        "return {"
        "ordinal: index + 1,"
        f"contentPrefix: characters.slice(0, {description_text_limit}).join(''),"
        "contentCharacterCount: characters.length"
        "};"
        "});"
        "return {"
        "url: window.location.href,"
        "documentLanguage,"
        "canonicalLinkCount: canonicalNodes.length,"
        "canonicalLinks,"
        "descriptionCount: descriptionNodes.length,"
        "descriptions"
        "};"
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
            f"Failed to read Chromium page metadata for target {target.target_id}: {exc}"
        ) from exc
    finally:
        websocket.close()

    value = _extract_runtime_value(response)
    url = value.get("url")
    document_language = value.get("documentLanguage")
    canonical_link_count = value.get("canonicalLinkCount")
    raw_canonical_links = value.get("canonicalLinks")
    description_count = value.get("descriptionCount")
    raw_descriptions = value.get("descriptions")

    if not isinstance(url, str):
        raise ChromiumReadError("Chromium metadata snapshot URL was not a string.")
    if not isinstance(document_language, str):
        raise ChromiumReadError("Chromium metadata document language was not a string.")
    if not isinstance(canonical_link_count, int) or canonical_link_count < 0:
        raise ChromiumReadError(
            "Chromium metadata canonical-link count was not a non-negative integer."
        )
    if not isinstance(raw_canonical_links, list):
        raise ChromiumReadError("Chromium metadata canonical links were not a list.")
    if len(raw_canonical_links) > canonical_link_limit:
        raise ChromiumReadError(
            "Chromium metadata exceeded the requested canonical-link limit."
        )
    if canonical_link_count < len(raw_canonical_links):
        raise ChromiumReadError(
            "Chromium metadata canonical-link count is smaller than the returned declarations."
        )
    if not isinstance(description_count, int) or description_count < 0:
        raise ChromiumReadError(
            "Chromium metadata description count was not a non-negative integer."
        )
    if not isinstance(raw_descriptions, list):
        raise ChromiumReadError("Chromium metadata descriptions were not a list.")
    if len(raw_descriptions) > description_limit:
        raise ChromiumReadError(
            "Chromium metadata exceeded the requested description limit."
        )
    if description_count < len(raw_descriptions):
        raise ChromiumReadError(
            "Chromium metadata description count is smaller than the returned declarations."
        )

    canonical_links: list[ChromiumPageCanonicalLinkSnapshot] = []
    for expected_ordinal, item in enumerate(raw_canonical_links, start=1):
        if not isinstance(item, dict):
            raise ChromiumReadError("Chromium canonical-link declaration was not an object.")
        ordinal = item.get("ordinal")
        raw_href = item.get("rawHref")
        resolved_href = item.get("resolvedHref")
        if ordinal != expected_ordinal:
            raise ChromiumReadError(
                "Chromium canonical-link ordinals were not contiguous DOM order."
            )
        if not isinstance(raw_href, str):
            raise ChromiumReadError("Chromium canonical-link raw href was not a string.")
        if not isinstance(resolved_href, str):
            raise ChromiumReadError("Chromium canonical-link resolved href was not a string.")
        canonical_links.append(
            ChromiumPageCanonicalLinkSnapshot(
                ordinal=ordinal,
                raw_href=raw_href,
                resolved_href=resolved_href,
            )
        )

    descriptions: list[ChromiumPageDescriptionSnapshot] = []
    for expected_ordinal, item in enumerate(raw_descriptions, start=1):
        if not isinstance(item, dict):
            raise ChromiumReadError("Chromium meta-description declaration was not an object.")
        ordinal = item.get("ordinal")
        content_prefix = item.get("contentPrefix")
        content_character_count = item.get("contentCharacterCount")
        if ordinal != expected_ordinal:
            raise ChromiumReadError(
                "Chromium meta-description ordinals were not contiguous DOM order."
            )
        if not isinstance(content_prefix, str):
            raise ChromiumReadError("Chromium meta-description prefix was not a string.")
        if not isinstance(content_character_count, int) or content_character_count < 0:
            raise ChromiumReadError(
                "Chromium meta-description count was not a non-negative integer."
            )
        if len(content_prefix) > description_text_limit:
            raise ChromiumReadError(
                "Chromium meta-description exceeded the requested text limit."
            )
        if content_character_count < len(content_prefix):
            raise ChromiumReadError(
                "Chromium meta-description count is smaller than the returned prefix."
            )
        descriptions.append(
            ChromiumPageDescriptionSnapshot(
                ordinal=ordinal,
                content_prefix=content_prefix,
                content_character_count=content_character_count,
            )
        )

    return ChromiumPageMetadataSnapshot(
        url=url,
        document_language=document_language,
        canonical_links=tuple(canonical_links),
        canonical_link_count=canonical_link_count,
        descriptions=tuple(descriptions),
        description_count=description_count,
    )
