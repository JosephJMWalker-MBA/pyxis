from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import time
from urllib.request import urlopen

import pytest

from pyxis.app import ChromiumPageTablesEvidence, observe_chromium_page_tables
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


def _wait_for_table_evidence(
    endpoint: str,
    target_id: str,
    process: subprocess.Popen,
    *,
    expected_url: str,
    timeout_seconds: float = 10.0,
) -> ChromiumPageTablesEvidence:
    deadline = time.monotonic() + timeout_seconds
    last_evidence: ChromiumPageTablesEvidence | None = None
    last_error: ChromiumReadError | None = None

    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise AssertionError(
                f"Chromium exited before table evidence became ready: {process.returncode}"
            )
        try:
            evidence = observe_chromium_page_tables(
                endpoint,
                target_id=target_id,
                table_limit=1,
                row_limit=1,
                cell_limit=2,
                text_limit=7,
                timeout=3.0,
            )
            last_evidence = evidence
            if (
                evidence.url == expected_url
                and evidence.table_count == 2
                and len(evidence.tables) == 1
                and evidence.tables[0].caption_text_prefix == "Study 😀"
                and evidence.tables[0].row_count == 2
                and len(evidence.tables[0].rows) == 1
                and evidence.tables[0].rows[0].cell_count == 3
                and len(evidence.tables[0].rows[0].cells) == 2
            ):
                return evidence
        except ChromiumReadError as exc:
            last_error = exc
        time.sleep(0.1)

    raise AssertionError(
        "Timed out waiting for loaded Chromium table evidence; "
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
        profile = tmp_path / f"chromium-table-profile-{index}"
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


def test_observe_chromium_tables_against_real_headless_browser(tmp_path: Path) -> None:
    browsers = _installed_browser_binaries()
    if not browsers:
        if os.environ.get("GITHUB_ACTIONS") == "true":
            pytest.fail("GitHub Actions browser integration requires Chrome or Chromium.")
        pytest.skip("Chrome/Chromium is not installed on this machine.")

    page = tmp_path / "table-page.html"
    page.write_text(
        "<!doctype html><html><head><meta charset='utf-8'>"
        "<title>Pyxis table evidence</title></head><body>"
        "<table><caption>Study 😀 table</caption>"
        "<tr><th rowspan='2'>Metric</th><td colspan='2'>Alpha 😀 value</td><td>Extra</td></tr>"
        "<tr><td>Beta</td><td>Gamma</td></tr></table>"
        "<table><tr><td>Second table</td></tr></table>"
        "</body></html>",
        encoding="utf-8",
    )
    page_url = page.as_uri()

    process, endpoint = _launch_browser_with_devtools(browsers, tmp_path, page_url)
    try:
        target_id = _wait_for_page_target(endpoint, page_url, process)
        evidence = _wait_for_table_evidence(
            endpoint,
            target_id,
            process,
            expected_url=page_url,
        )

        assert evidence.endpoint == endpoint
        assert evidence.target_id == target_id
        assert evidence.url == page_url
        assert evidence.source == "document.querySelectorAll('table')"
        assert evidence.table_count == 2
        assert evidence.table_limit == 1
        assert evidence.truncated is True

        table = evidence.tables[0]
        assert table.ordinal == 1
        assert table.caption_text_prefix == "Study 😀"
        assert table.caption_text_character_count == len("Study 😀 table")
        assert table.text_limit == 7
        assert table.caption_truncated is True
        assert table.row_count == 2
        assert table.row_limit == 1
        assert table.rows_truncated is True

        row = table.rows[0]
        assert row.ordinal == 1
        assert row.cell_count == 3
        assert row.cell_limit == 2
        assert row.truncated is True

        first = row.cells[0]
        assert first.ordinal == 1
        assert first.tag_name == "TH"
        assert first.row_span == 2
        assert first.col_span == 1
        assert first.text_prefix == "Metric"
        assert first.text_character_count == len("Metric")
        assert first.truncated is False

        second = row.cells[1]
        assert second.ordinal == 2
        assert second.tag_name == "TD"
        assert second.row_span == 1
        assert second.col_span == 2
        assert second.text_prefix == "Alpha 😀"
        assert second.text_character_count == len("Alpha 😀 value")
        assert second.truncated is True
    finally:
        _terminate_browser(process)
