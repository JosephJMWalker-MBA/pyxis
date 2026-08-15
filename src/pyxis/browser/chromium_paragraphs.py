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


DEFAULT_PARAGRAPH_LIMIT = 128
DEFAULT_PARAGRAPH_TEXT_LIMIT = 1024


@dataclass(frozen=True, slots=True)
class ChromiumPageParagraphSnapshot:
    """One DOM-order paragraph snapshot from the selected page target."""

    ordinal: int
    element_id: str
    text_prefix: str
    text_character_count: int

    @property
    def text_truncated(self) -> bool:
        return self.text_character_count > len(self.text_prefix)


@dataclass(frozen=True, slots=True)
class ChromiumPageParagraphsSnapshot:
    """One bounded read-only paragraph collection from the selected page target."""

    url: str
    paragraphs: tuple[ChromiumPageParagraphSnapshot, ...]
    paragraph_count: int

    @property
    def paragraphs_truncated(self) -> bool:
        return self.paragraph_count > len(self.paragraphs)


def read_chromium_page_paragraphs(
    target: ChromiumPageTarget,
    *,
    paragraph_limit: int = DEFAULT_PARAGRAPH_LIMIT,
    paragraph_text_limit: int = DEFAULT_PARAGRAPH_TEXT_LIMIT,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
) -> ChromiumPageParagraphsSnapshot:
    """Read literal paragraph elements without segmenting or ranking passages.

    The fixed DevTools expression reads only existing `<p>` elements in DOM
    order, each authored `id` string, and bounded `innerText`. It does not infer
    sentences, paragraph importance, citation identity, locator stability,
    uniqueness of IDs, mutate the DOM, activate targets, or navigate.
    """

    if paragraph_limit < 0:
        raise ValueError("paragraph_limit must be >= 0.")
    if paragraph_text_limit < 0:
        raise ValueError("paragraph_text_limit must be >= 0.")
    if timeout <= 0:
        raise ValueError("timeout must be > 0.")

    expression = (
        "(() => {"
        "const nodes = Array.from(document.querySelectorAll('p'));"
        f"const paragraphs = nodes.slice(0, {paragraph_limit}).map((paragraph, index) => {{"
        "const text = paragraph.innerText || '';"
        "const characters = Array.from(text);"
        "return {"
        "ordinal: index + 1,"
        "elementId: paragraph.getAttribute('id') || '',"
        f"textPrefix: characters.slice(0, {paragraph_text_limit}).join(''),"
        "textCharacterCount: characters.length"
        "};"
        "});"
        "return {url: window.location.href, paragraphCount: nodes.length, paragraphs};"
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
            f"Failed to read Chromium page paragraphs for target {target.target_id}: {exc}"
        ) from exc
    finally:
        websocket.close()

    value = _extract_runtime_value(response)
    url = value.get("url")
    paragraph_count = value.get("paragraphCount")
    raw_paragraphs = value.get("paragraphs")

    if not isinstance(url, str):
        raise ChromiumReadError("Chromium paragraphs snapshot URL was not a string.")
    if not isinstance(paragraph_count, int) or paragraph_count < 0:
        raise ChromiumReadError(
            "Chromium paragraphs snapshot count was not a non-negative integer."
        )
    if not isinstance(raw_paragraphs, list):
        raise ChromiumReadError("Chromium paragraphs snapshot paragraphs were not a list.")
    if len(raw_paragraphs) > paragraph_limit:
        raise ChromiumReadError(
            "Chromium paragraphs snapshot exceeded the requested paragraph limit."
        )
    if paragraph_count < len(raw_paragraphs):
        raise ChromiumReadError(
            "Chromium paragraphs snapshot count is smaller than the returned paragraphs."
        )

    paragraphs: list[ChromiumPageParagraphSnapshot] = []
    for expected_ordinal, item in enumerate(raw_paragraphs, start=1):
        if not isinstance(item, dict):
            raise ChromiumReadError("Chromium paragraph snapshot item was not an object.")

        ordinal = item.get("ordinal")
        element_id = item.get("elementId")
        text_prefix = item.get("textPrefix")
        text_character_count = item.get("textCharacterCount")

        if ordinal != expected_ordinal:
            raise ChromiumReadError(
                "Chromium paragraph snapshot ordinals were not contiguous DOM order."
            )
        if not isinstance(element_id, str):
            raise ChromiumReadError("Chromium paragraph element id was not a string.")
        if not isinstance(text_prefix, str):
            raise ChromiumReadError("Chromium paragraph text prefix was not a string.")
        if not isinstance(text_character_count, int) or text_character_count < 0:
            raise ChromiumReadError(
                "Chromium paragraph text count was not a non-negative integer."
            )
        if len(text_prefix) > paragraph_text_limit:
            raise ChromiumReadError(
                "Chromium paragraph snapshot exceeded the requested text limit."
            )
        if text_character_count < len(text_prefix):
            raise ChromiumReadError(
                "Chromium paragraph text count is smaller than the returned prefix."
            )

        paragraphs.append(
            ChromiumPageParagraphSnapshot(
                ordinal=ordinal,
                element_id=element_id,
                text_prefix=text_prefix,
                text_character_count=text_character_count,
            )
        )

    return ChromiumPageParagraphsSnapshot(
        url=url,
        paragraphs=tuple(paragraphs),
        paragraph_count=paragraph_count,
    )
