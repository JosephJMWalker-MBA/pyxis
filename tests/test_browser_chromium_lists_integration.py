from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import time
from urllib.request import urlopen

import pytest

from pyxis.app import ChromiumPageListsEvidence, observe_chromium_page_lists
from pyxis.browser import ChromiumReadError


def _wait_for_devtools_endpoint(
    profile: Path,
    process: subprocess.Popen,
    *,
    timeout_seconds: float = 30.0,
) -> str:
    active_port = profile / "DevToolsActivePort"
    deadline = time.monotonic() + timeout_seconds
    last_error: Exception | None = None

    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise AssertionError(
                "Chromium exited before publishing DevToolsActivePort: "
                f"{process.returncode}"
            )
        try:
            lines = active_port.read_text(encoding="utf-8").splitlines()
            if lines and int(lines[0]) > 0:
                return f"http://127.0.0.1:{int(lines[0])}"
        except (OSError, ValueError) as exc:
            last_error = exc
        time.sleep(0.1)

    raise AssertionError(
        "Timed out waiting for Chromium DevToolsActivePort; "
        f"last error={last_error!r}"
    )


def _wait_for_page_target(
    endpoint: str,
    expected_url: str,
    process: subprocess.Popen,
    *,
    timeout_seconds: float = 10.0,
) -> str:
    deadline = time.monotonic() + timeout_seconds
    last_error: Exception | None = None

    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise AssertionError(
                f"Chromium exited before its DevTools page became available: {process.returncode}"
            )
        try:
            with urlopen(f"{endpoint}/json/list", timeout=0.5) as response:
                targets = json.loads(response.read().decode("utf-8"))
            for target in targets:
                if target.get("type") == "page" and target.get("url") == expected_url:
                    return str(target["id"])
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            last_error = exc
        time.sleep(0.1)

    raise AssertionError(
        f"Timed out waiting for Chromium page target {expected_url!r}; last error={last_error!r}"
    )


def _wait_for_list_evidence(
    endpoint: str,
    target_id: str,
    process: subprocess.Popen,
    *,
    expected_url: str,
    timeout_seconds: float = 10.0,
) -> ChromiumPageListsEvidence:
    deadline = time.monotonic() + timeout_seconds
    last_evidence: ChromiumPageListsEvidence | None = None
    last_error: ChromiumReadError | None = None

    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise AssertionError(
                f"Chromium exited before list evidence became ready: {process.returncode}"
            )
        try:
            evidence = observe_chromium_page_lists(
                endpoint,
                target_id=target_id,
                list_limit=2,
                item_limit=2,
                text_limit=7,
                timeout=3.0,
            )
            last_evidence = evidence
            if (
                evidence.url == expected_url
                and evidence.list_count == 3
                and len(evidence.lists) == 2
                and evidence.lists[0].item_count == 3
                and len(evidence.lists[0].items) == 2
                and evidence.lists[1].parent_list_ordinal == 1
                and evidence.lists[1].parent_item_ordinal == 2
            ):
                return evidence
        except ChromiumReadError as exc:
            last_error = exc
        time.sleep(0.1)

    raise AssertionError(
        "Timed out waiting for loaded Chromium list evidence; "
        f"last evidence={last_evidence!r}; last error={last_error!r}"
    )


def _installed_browser_binaries() -> tuple[str, ...]:
    binaries: list[str] = []
    for command in ("google-chrome", "chromium"):
        resolved = shutil.which(command)
        if resolved is not None and resolved not in binaries:
            binaries.append(resolved)
    return tuple(binaries)


def _terminate_browser(process: subprocess.Popen) -> None:
    if process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=5)


def _launch_browser_with_devtools(
    binaries: tuple[str, ...],
    tmp_path: Path,
    page_url: str,
) -> tuple[subprocess.Popen, str]:
    startup_failures: list[str] = []
    for index, browser in enumerate(binaries):
        profile = tmp_path / f"chromium-list-profile-{index}"
        process = subprocess.Popen(
            [
                browser,
                "--headless=new",
                "--no-sandbox",
                "--disable-gpu",
                "--disable-dev-shm-usage",
                "--no-first-run",
                "--no-default-browser-check",
                "--remote-debugging-port=0",
                f"--user-data-dir={profile}",
                page_url,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        try:
            endpoint = _wait_for_devtools_endpoint(profile, process)
        except AssertionError as exc:
            startup_failures.append(f"{browser}: {exc}")
            _terminate_browser(process)
            continue
        return process, endpoint

    details = "; ".join(startup_failures) or "no launch attempts were made"
    raise AssertionError(
        "No installed Chromium-family browser published a DevTools endpoint; "
        f"{details}"
    )


def test_observe_chromium_lists_against_real_headless_browser(tmp_path: Path) -> None:
    browsers = _installed_browser_binaries()
    if not browsers:
        if os.environ.get("GITHUB_ACTIONS") == "true":
            pytest.fail("GitHub Actions browser integration requires Chrome or Chromium.")
        pytest.skip("Chrome/Chromium is not installed on this machine.")

    page = tmp_path / "list-page.html"
    page.write_text(
        "<!doctype html><html><head><meta charset='utf-8'>"
        "<title>Pyxis list evidence</title></head><body>"
        "<ol start='3'>"
        "<li value='7'>Alpha 😀 item</li>"
        "<li>Parent<ul start='99'><li value='42'>Nested</li></ul> tail</li>"
        "<li>Third</li>"
        "</ol>"
        "<ul><li>Separate</li></ul>"
        "</body></html>",
        encoding="utf-8",
    )
    page_url = page.as_uri()

    process, endpoint = _launch_browser_with_devtools(browsers, tmp_path, page_url)
    try:
        target_id = _wait_for_page_target(endpoint, page_url, process)
        evidence = _wait_for_list_evidence(
            endpoint,
            target_id,
            process,
            expected_url=page_url,
        )

        assert evidence.endpoint == endpoint
        assert evidence.target_id == target_id
        assert evidence.url == page_url
        assert evidence.source == "document.querySelectorAll('ol,ul')"
        assert evidence.list_count == 3
        assert evidence.list_limit == 2
        assert evidence.truncated is True

        ordered = evidence.lists[0]
        assert ordered.ordinal == 1
        assert ordered.tag_name == "OL"
        assert ordered.start_attribute == "3"
        assert ordered.parent_list_ordinal is None
        assert ordered.parent_item_ordinal is None
        assert ordered.item_count == 3
        assert ordered.item_limit == 2
        assert ordered.truncated is True

        first = ordered.items[0]
        assert first.ordinal == 1
        assert first.value_attribute == "7"
        assert first.direct_text_prefix == "Alpha 😀"
        assert first.direct_text_character_count == len("Alpha 😀 item")
        assert first.text_limit == 7
        assert first.truncated is True

        parent = ordered.items[1]
        assert parent.ordinal == 2
        assert parent.value_attribute is None
        assert parent.direct_text_prefix == "Parent "
        assert parent.direct_text_character_count == len("Parent tail")
        assert parent.truncated is True
        assert "Nested" not in parent.direct_text_prefix

        nested = evidence.lists[1]
        assert nested.ordinal == 2
        assert nested.tag_name == "UL"
        assert nested.start_attribute == "99"
        assert nested.parent_list_ordinal == 1
        assert nested.parent_item_ordinal == 2
        assert nested.item_count == 1
        assert nested.truncated is False
        assert nested.items[0].value_attribute == "42"
        assert nested.items[0].direct_text_prefix == "Nested"
        assert nested.items[0].direct_text_character_count == len("Nested")
        assert nested.items[0].truncated is False
    finally:
        _terminate_browser(process)
