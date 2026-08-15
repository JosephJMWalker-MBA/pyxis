from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import time
from urllib.request import urlopen

import pytest

from pyxis.app import ChromiumPageParagraphsEvidence, observe_chromium_page_paragraphs
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
        profile = tmp_path / f"paragraph-profile-{index}"
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


def _wait_for_paragraph_evidence(
    endpoint: str,
    target_id: str,
    process: subprocess.Popen,
    *,
    expected_url: str,
    timeout_seconds: float = 10.0,
) -> ChromiumPageParagraphsEvidence:
    deadline = time.monotonic() + timeout_seconds
    last_evidence: ChromiumPageParagraphsEvidence | None = None
    last_error: ChromiumReadError | None = None
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise AssertionError(
                f"Chromium exited before paragraph evidence became ready: {process.returncode}"
            )
        try:
            evidence = observe_chromium_page_paragraphs(
                endpoint,
                target_id=target_id,
                paragraph_limit=2,
                paragraph_text_limit=7,
                timeout=3.0,
            )
            last_evidence = evidence
            if (
                evidence.url == expected_url
                and evidence.paragraph_count == 3
                and len(evidence.paragraphs) == 2
                and evidence.paragraphs[0].element_id == "passage"
                and evidence.paragraphs[0].text_prefix == "First 😀"
                and evidence.paragraphs[0].text_character_count == len("First 😀 paragraph")
                and evidence.paragraphs[1].element_id == "passage"
                and evidence.paragraphs[1].text_prefix == "Methods"
            ):
                return evidence
        except ChromiumReadError as exc:
            last_error = exc
        time.sleep(0.1)
    raise AssertionError(
        "Timed out waiting for loaded Chromium paragraph evidence; "
        f"last evidence={last_evidence!r}; last error={last_error!r}"
    )


def test_observe_chromium_paragraphs_against_real_headless_browser(tmp_path: Path) -> None:
    browsers = _installed_browser_binaries()
    if not browsers:
        if os.environ.get("GITHUB_ACTIONS") == "true":
            pytest.fail("GitHub Actions paragraph integration requires Chrome or Chromium.")
        pytest.skip("Chrome/Chromium is not installed on this machine.")

    page = tmp_path / "paragraphs.html"
    page.write_text(
        "<!doctype html><meta charset='utf-8'><title>Paragraph evidence</title>"
        "<body>"
        "<p id='passage'>First 😀 paragraph</p>"
        "<p id='passage'>Methods</p>"
        "<p>Appendix passage</p>"
        "</body>",
        encoding="utf-8",
    )
    page_url = page.as_uri()

    process, endpoint = _launch_browser_with_devtools(browsers, tmp_path, page_url)
    try:
        target_id = _wait_for_page_target(endpoint, page_url, process)
        evidence = _wait_for_paragraph_evidence(
            endpoint,
            target_id,
            process,
            expected_url=page_url,
        )

        assert evidence.endpoint == endpoint
        assert evidence.target_id == target_id
        assert evidence.url == page_url
        assert evidence.source == "document.querySelectorAll('p')"
        assert evidence.paragraph_count == 3
        assert evidence.paragraph_limit == 2
        assert evidence.truncated is True
        assert evidence.paragraphs[0].ordinal == 1
        assert evidence.paragraphs[0].element_id == "passage"
        assert evidence.paragraphs[0].text_prefix == "First 😀"
        assert evidence.paragraphs[0].text_character_count == len("First 😀 paragraph")
        assert evidence.paragraphs[0].text_limit == 7
        assert evidence.paragraphs[0].truncated is True
        assert evidence.paragraphs[1].ordinal == 2
        assert evidence.paragraphs[1].element_id == "passage"
        assert evidence.paragraphs[1].text_prefix == "Methods"
        assert evidence.paragraphs[1].truncated is False
    finally:
        _terminate_browser(process)
