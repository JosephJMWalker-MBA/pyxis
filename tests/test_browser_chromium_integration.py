from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import time
from urllib.request import urlopen

import pytest

from pyxis.app import ChromiumPageObservationEvidence, observe_chromium_page
from pyxis.browser import ChromiumReadError


def _wait_for_devtools_endpoint(
    profile: Path,
    process: subprocess.Popen,
    *,
    timeout_seconds: float = 30.0,
) -> str:
    """Wait for Chromium's own remote-debugging endpoint declaration."""

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


def _wait_for_page_evidence(
    endpoint: str,
    target_id: str,
    process: subprocess.Popen,
    *,
    expected_url: str,
    expected_title: str,
    expected_text: str,
    text_limit: int,
    timeout_seconds: float = 10.0,
) -> ChromiumPageObservationEvidence:
    """Synchronize the test with page readiness using production read evidence only."""

    deadline = time.monotonic() + timeout_seconds
    last_evidence: ChromiumPageObservationEvidence | None = None
    last_error: ChromiumReadError | None = None
    expected_prefix = expected_text[:text_limit]

    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise AssertionError(
                f"Chromium exited before page evidence became ready: {process.returncode}"
            )
        try:
            evidence = observe_chromium_page(
                endpoint,
                target_id=target_id,
                text_limit=text_limit,
                timeout=3.0,
            )
            last_evidence = evidence
            if (
                evidence.url == expected_url
                and evidence.title == expected_title
                and evidence.content.text_prefix == expected_prefix
                and evidence.content.text_character_count == len(expected_text)
            ):
                return evidence
        except ChromiumReadError as exc:
            last_error = exc
        time.sleep(0.1)

    raise AssertionError(
        "Timed out waiting for loaded Chromium page evidence; "
        f"last evidence={last_evidence!r}; last error={last_error!r}"
    )


def test_observe_chromium_page_against_real_headless_browser(tmp_path: Path) -> None:
    browser = shutil.which("google-chrome") or shutil.which("chromium")
    if browser is None:
        if os.environ.get("GITHUB_ACTIONS") == "true":
            pytest.fail("GitHub Actions browser integration requires Chrome or Chromium.")
        pytest.skip("Chrome/Chromium is not installed on this machine.")

    expected_title = "Pyxis 15A"
    expected_text = "alpha 😀 beta"
    text_limit = 7
    page = tmp_path / "page.html"
    page.write_text(
        "<!doctype html><meta charset='utf-8'><title>Pyxis 15A</title>"
        "<body>alpha 😀 beta</body>",
        encoding="utf-8",
    )
    page_url = page.as_uri()
    profile = tmp_path / "chromium-profile"

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
        target_id = _wait_for_page_target(endpoint, page_url, process)
        evidence = _wait_for_page_evidence(
            endpoint,
            target_id,
            process,
            expected_url=page_url,
            expected_title=expected_title,
            expected_text=expected_text,
            text_limit=text_limit,
        )

        assert evidence.endpoint == endpoint
        assert evidence.target_id == target_id
        assert evidence.url == page_url
        assert evidence.title == expected_title
        assert evidence.content.source == "document.body.innerText"
        assert evidence.content.text_prefix == "alpha 😀"
        assert evidence.content.text_character_count == len(expected_text)
        assert evidence.content.text_limit == text_limit
        assert evidence.content.truncated is True
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)
