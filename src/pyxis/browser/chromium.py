from __future__ import annotations

from dataclasses import dataclass
import json
from typing import Any
from urllib.parse import urlsplit, urlunsplit
from urllib.request import urlopen


DEFAULT_TEXT_LIMIT = 2048
DEFAULT_TIMEOUT_SECONDS = 5.0


class ChromiumReadError(RuntimeError):
    """Raised when read-only Chromium evidence cannot be acquired safely."""


@dataclass(frozen=True, slots=True)
class ChromiumPageTarget:
    """One Chromium page target discovered through the DevTools HTTP endpoint."""

    target_id: str
    websocket_debugger_url: str


@dataclass(frozen=True, slots=True)
class ChromiumPageSnapshot:
    """One bounded read-only snapshot returned by the selected page target."""

    url: str
    title: str
    text_prefix: str
    text_character_count: int

    @property
    def text_truncated(self) -> bool:
        return self.text_character_count > len(self.text_prefix)


def normalize_chromium_endpoint(endpoint: str) -> str:
    """Normalize one explicit Chromium DevTools HTTP endpoint.

    15A intentionally accepts only an explicit HTTP(S) DevTools endpoint and
    does not discover local browsers, ports, profiles, or processes.
    """

    value = endpoint.strip()
    if not value:
        raise ValueError("Chromium endpoint must be non-empty.")

    parsed = urlsplit(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError(
            "Chromium endpoint must be an explicit http:// or https:// endpoint."
        )
    if parsed.query or parsed.fragment:
        raise ValueError("Chromium endpoint must not contain a query or fragment.")

    path = parsed.path.rstrip("/")
    return urlunsplit((parsed.scheme, parsed.netloc, path, "", ""))


def list_chromium_page_targets(
    endpoint: str,
    *,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
) -> tuple[ChromiumPageTarget, ...]:
    """Return page targets exposed by one explicit Chromium DevTools endpoint.

    The function performs one read-only GET against `/json/list`. Non-page
    targets are ignored. No target is activated, created, closed, or navigated.
    """

    base = normalize_chromium_endpoint(endpoint)
    payload = _read_json(f"{base}/json/list", timeout=timeout)
    if not isinstance(payload, list):
        raise ChromiumReadError("Chromium /json/list response was not a JSON list.")

    targets: list[ChromiumPageTarget] = []
    seen_ids: set[str] = set()
    for item in payload:
        if not isinstance(item, dict) or item.get("type") != "page":
            continue

        target_id = item.get("id")
        websocket_debugger_url = item.get("webSocketDebuggerUrl")
        if not isinstance(target_id, str) or not target_id:
            raise ChromiumReadError("Chromium page target is missing a valid id.")
        if target_id in seen_ids:
            raise ChromiumReadError(f"Duplicate Chromium page target id: {target_id}")
        if not isinstance(websocket_debugger_url, str) or not websocket_debugger_url:
            raise ChromiumReadError(
                f"Chromium page target {target_id} is missing webSocketDebuggerUrl."
            )

        seen_ids.add(target_id)
        targets.append(
            ChromiumPageTarget(
                target_id=target_id,
                websocket_debugger_url=websocket_debugger_url,
            )
        )

    return tuple(targets)


def read_chromium_page_snapshot(
    target: ChromiumPageTarget,
    *,
    text_limit: int = DEFAULT_TEXT_LIMIT,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
) -> ChromiumPageSnapshot:
    """Read URL/title plus a bounded rendered-text prefix from one page target.

    The DevTools command is fixed by Pyxis. Callers cannot supply JavaScript or
    arbitrary CDP methods. The expression only reads `location.href`,
    `document.title`, and `document.body.innerText`; it does not navigate,
    activate, click, submit, mutate DOM state, or create/close targets.
    """

    if text_limit < 0:
        raise ValueError("text_limit must be >= 0.")
    if timeout <= 0:
        raise ValueError("timeout must be > 0.")

    expression = (
        "(() => {"
        'const text = document.body ? document.body.innerText : "";'
        "return {"
        'url: window.location.href,'
        'title: document.title,'
        f"textPrefix: text.slice(0, {text_limit}),"
        "textCharacterCount: text.length"
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
            f"Failed to read Chromium page target {target.target_id}: {exc}"
        ) from exc
    finally:
        websocket.close()

    value = _extract_runtime_value(response)
    url = value.get("url")
    title = value.get("title")
    text_prefix = value.get("textPrefix")
    text_character_count = value.get("textCharacterCount")

    if not isinstance(url, str):
        raise ChromiumReadError("Chromium snapshot URL was not a string.")
    if not isinstance(title, str):
        raise ChromiumReadError("Chromium snapshot title was not a string.")
    if not isinstance(text_prefix, str):
        raise ChromiumReadError("Chromium snapshot text prefix was not a string.")
    if not isinstance(text_character_count, int) or text_character_count < 0:
        raise ChromiumReadError(
            "Chromium snapshot text character count was not a non-negative integer."
        )
    if len(text_prefix) > text_limit:
        raise ChromiumReadError("Chromium snapshot exceeded the requested text limit.")
    if text_character_count < len(text_prefix):
        raise ChromiumReadError(
            "Chromium snapshot text count is smaller than the returned prefix."
        )

    return ChromiumPageSnapshot(
        url=url,
        title=title,
        text_prefix=text_prefix,
        text_character_count=text_character_count,
    )


def _read_json(url: str, *, timeout: float) -> Any:
    if timeout <= 0:
        raise ValueError("timeout must be > 0.")
    try:
        with urlopen(url, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        raise ChromiumReadError(f"Failed to read Chromium DevTools JSON: {exc}") from exc


def _open_websocket(url: str, *, timeout: float):
    try:
        from websocket import create_connection
    except ImportError as exc:  # pragma: no cover - depends on installation extras
        raise ChromiumReadError(
            "Chromium page reads require the optional 'browser' dependency: "
            "install Pyxis with pyxis[browser]."
        ) from exc

    try:
        return create_connection(url, timeout=timeout, suppress_origin=True)
    except Exception as exc:  # pragma: no cover - transport-specific failure shape
        raise ChromiumReadError(f"Failed to open Chromium DevTools WebSocket: {exc}") from exc


def _receive_command_response(websocket, *, command_id: int) -> dict[str, Any]:
    while True:
        raw = websocket.recv()
        try:
            message = json.loads(raw)
        except (TypeError, json.JSONDecodeError) as exc:
            raise ChromiumReadError(
                "Chromium DevTools WebSocket returned invalid JSON."
            ) from exc

        if not isinstance(message, dict):
            raise ChromiumReadError("Chromium DevTools message was not a JSON object.")
        if message.get("id") != command_id:
            continue
        if "error" in message:
            raise ChromiumReadError(
                f"Chromium DevTools Runtime.evaluate failed: {message['error']}"
            )
        return message


def _extract_runtime_value(response: dict[str, Any]) -> dict[str, Any]:
    result = response.get("result")
    if not isinstance(result, dict):
        raise ChromiumReadError("Chromium Runtime.evaluate response is missing result.")
    if "exceptionDetails" in result:
        raise ChromiumReadError(
            f"Chromium Runtime.evaluate raised an exception: {result['exceptionDetails']}"
        )

    remote_object = result.get("result")
    if not isinstance(remote_object, dict):
        raise ChromiumReadError("Chromium Runtime.evaluate result is malformed.")
    value = remote_object.get("value")
    if not isinstance(value, dict):
        raise ChromiumReadError("Chromium Runtime.evaluate did not return an object value.")
    return value
