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


DEFAULT_HEADING_LIMIT = 64
DEFAULT_HEADING_TEXT_LIMIT = 256


@dataclass(frozen=True, slots=True)
class ChromiumPageHeadingSnapshot:
    """One DOM-order heading snapshot returned by the selected page target."""

    ordinal: int
    level: int
    text_prefix: str
    text_character_count: int

    @property
    def text_truncated(self) -> bool:
        return self.text_character_count > len(self.text_prefix)


@dataclass(frozen=True, slots=True)
class ChromiumPageHeadingsSnapshot:
    """One bounded read-only heading collection from the selected page target."""

    url: str
    headings: tuple[ChromiumPageHeadingSnapshot, ...]
    heading_count: int

    @property
    def headings_truncated(self) -> bool:
        return self.heading_count > len(self.headings)


def read_chromium_page_headings(
    target: ChromiumPageTarget,
    *,
    heading_limit: int = DEFAULT_HEADING_LIMIT,
    heading_text_limit: int = DEFAULT_HEADING_TEXT_LIMIT,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
) -> ChromiumPageHeadingsSnapshot:
    """Read bounded DOM-order heading evidence without interpreting structure.

    The fixed DevTools expression reads only h1-h6 elements in DOM order, their
    explicit HTML heading level, and bounded `innerText`. It does not repair
    skipped levels, infer hierarchy, summarize content, rank sections, mutate
    the DOM, activate targets, or navigate.
    """

    if heading_limit < 0:
        raise ValueError("heading_limit must be >= 0.")
    if heading_text_limit < 0:
        raise ValueError("heading_text_limit must be >= 0.")
    if timeout <= 0:
        raise ValueError("timeout must be > 0.")

    expression = (
        "(() => {"
        "const nodes = Array.from(document.querySelectorAll('h1,h2,h3,h4,h5,h6'));"
        f"const headings = nodes.slice(0, {heading_limit}).map((heading, index) => {{"
        'const text = heading.innerText || "";'
        "const characters = Array.from(text);"
        "return {"
        "ordinal: index + 1,"
        "level: Number(heading.tagName.slice(1)),"
        f"textPrefix: characters.slice(0, {heading_text_limit}).join(''),"
        "textCharacterCount: characters.length"
        "};"
        "});"
        "return {url: window.location.href, headingCount: nodes.length, headings};"
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
            f"Failed to read Chromium page headings for target {target.target_id}: {exc}"
        ) from exc
    finally:
        websocket.close()

    value = _extract_runtime_value(response)
    url = value.get("url")
    heading_count = value.get("headingCount")
    raw_headings = value.get("headings")

    if not isinstance(url, str):
        raise ChromiumReadError("Chromium headings snapshot URL was not a string.")
    if not isinstance(heading_count, int) or heading_count < 0:
        raise ChromiumReadError(
            "Chromium headings snapshot count was not a non-negative integer."
        )
    if not isinstance(raw_headings, list):
        raise ChromiumReadError("Chromium headings snapshot headings were not a list.")
    if len(raw_headings) > heading_limit:
        raise ChromiumReadError(
            "Chromium headings snapshot exceeded the requested heading limit."
        )
    if heading_count < len(raw_headings):
        raise ChromiumReadError(
            "Chromium headings snapshot count is smaller than the returned headings."
        )

    headings: list[ChromiumPageHeadingSnapshot] = []
    for expected_ordinal, item in enumerate(raw_headings, start=1):
        if not isinstance(item, dict):
            raise ChromiumReadError("Chromium heading snapshot item was not an object.")

        ordinal = item.get("ordinal")
        level = item.get("level")
        text_prefix = item.get("textPrefix")
        text_character_count = item.get("textCharacterCount")

        if ordinal != expected_ordinal:
            raise ChromiumReadError(
                "Chromium heading snapshot ordinals were not contiguous DOM order."
            )
        if not isinstance(level, int) or not 1 <= level <= 6:
            raise ChromiumReadError(
                "Chromium heading snapshot level was not an integer from 1 through 6."
            )
        if not isinstance(text_prefix, str):
            raise ChromiumReadError("Chromium heading snapshot text prefix was not a string.")
        if not isinstance(text_character_count, int) or text_character_count < 0:
            raise ChromiumReadError(
                "Chromium heading snapshot text count was not a non-negative integer."
            )
        if len(text_prefix) > heading_text_limit:
            raise ChromiumReadError(
                "Chromium heading snapshot exceeded the requested text limit."
            )
        if text_character_count < len(text_prefix):
            raise ChromiumReadError(
                "Chromium heading snapshot text count is smaller than the returned prefix."
            )

        headings.append(
            ChromiumPageHeadingSnapshot(
                ordinal=ordinal,
                level=level,
                text_prefix=text_prefix,
                text_character_count=text_character_count,
            )
        )

    return ChromiumPageHeadingsSnapshot(
        url=url,
        headings=tuple(headings),
        heading_count=heading_count,
    )
