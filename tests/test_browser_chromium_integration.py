from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import time
from urllib.request import urlopen

import pytest

from pyxis.app import (
    ChromiumPageHeadingsEvidence,
    ChromiumPageLinksEvidence,
    ChromiumPageObservationEvidence,
    observe_chromium_page,
    observe_chromium_page_headings,
    observe_chromium_page_links,
)
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


def _wait_for_link_evidence(
    endpoint: str,
    target_id: str,
    process: subprocess.Popen,
    *,
    expected_url: str,
    expected_first_href: str,
    timeout_seconds: float = 10.0,
) -> ChromiumPageLinksEvidence:
    """Synchronize the test with link-DOM readiness using production reads only."""

    deadline = time.monotonic() + timeout_seconds
    last_evidence: ChromiumPageLinksEvidence | None = None
    last_error: ChromiumReadError | None = None

    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise AssertionError(
                f"Chromium exited before link evidence became ready: {process.returncode}"
            )
        try:
            evidence = observe_chromium_page_links(
                endpoint,
                target_id=target_id,
                link_limit=2,
                link_text_limit=7,
                timeout=3.0,
            )
            last_evidence = evidence
            if (
                evidence.url == expected_url
                and evidence.link_count == 3
                and len(evidence.links) == 2
                and evidence.links[0].href == expected_first_href
                and evidence.links[0].text_prefix == "First 😀"
                and evidence.links[0].text_character_count == len("First 😀 link")
                and evidence.links[1].href == "mailto:research@example.test"
            ):
                return evidence
        except ChromiumReadError as exc:
            last_error = exc
        time.sleep(0.1)

    raise AssertionError(
        "Timed out waiting for loaded Chromium link evidence; "
        f"last evidence={last_evidence!r}; last error={last_error!r}"
    )


def _wait_for_heading_evidence(
    endpoint: str,
    target_id: str,
    process: subprocess.Popen,
    *,
    expected_url: str,
    timeout_seconds: float = 10.0,
) -> ChromiumPageHeadingsEvidence:
    """Synchronize the test with heading-DOM readiness using production reads only."""

    deadline = time.monotonic() + timeout_seconds
    last_evidence: ChromiumPageHeadingsEvidence | None = None
    last_error: ChromiumReadError | None = None

    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise AssertionError(
                f"Chromium exited before heading evidence became ready: {process.returncode}"
            )
        try:
            evidence = observe_chromium_page_headings(
                endpoint,
                target_id=target_id,
                heading_limit=2,
                heading_text_limit=7,
                timeout=3.0,
            )
            last_evidence = evidence
            if (
                evidence.url == expected_url
                and evidence.heading_count == 3
                and len(evidence.headings) == 2
                and evidence.headings[0].level == 1
                and evidence.headings[0].text_prefix == "Intro 😀"
                and evidence.headings[0].text_character_count == len("Intro 😀 section")
                and evidence.headings[1].level == 3
                and evidence.headings[1].text_prefix == "Methods"
            ):
                return evidence
        except ChromiumReadError as exc:
            last_error = exc
        time.sleep(0.1)

    raise AssertionError(
        "Timed out waiting for loaded Chromium heading evidence; "
        f"last evidence={last_evidence!r}; last error={last_error!r}"
    )


def _installed_browser_binaries() -> tuple[str, ...]:
    """Return distinct installed Chromium-family binaries in deterministic order."""

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
    """Launch one installed browser that successfully publishes DevTools.

    This is test-fixture resilience only. A browser process that never publishes
    its debugging endpoint is torn down and the next installed Chromium-family
    binary is tried with a fresh profile. Once an endpoint exists, the test does
    not fall back around target discovery or production observation failures.
    """

    startup_failures: list[str] = []
    for index, browser in enumerate(binaries):
        profile = tmp_path / f"chromium-profile-{index}"
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


def test_observe_chromium_evidence_against_real_headless_browser(tmp_path: Path) -> None:
    browsers = _installed_browser_binaries()
    if not browsers:
        if os.environ.get("GITHUB_ACTIONS") == "true":
            pytest.fail("GitHub Actions browser integration requires Chrome or Chromium.")
        pytest.skip("Chrome/Chromium is not installed on this machine.")

    expected_title = "Pyxis browser evidence"
    expected_text = "alpha 😀 beta First 😀 link Email Action Intro 😀 section Methods Appendix"
    text_limit = 7
    page = tmp_path / "page.html"
    page.write_text(
        "<!doctype html><meta charset='utf-8'><title>Pyxis browser evidence</title>"
        "<style>h1,h3,h6{display:inline;font-size:inherit}</style>"
        "<body>alpha 😀 beta "
        "<a href='first.html'>First 😀 link</a> "
        "<a href='mailto:research@example.test'>Email</a> "
        "<a href='javascript:void(0)'>Action</a> "
        "<h1>Intro 😀 section</h1> "
        "<h3>Methods</h3> "
        "<h6>Appendix</h6>"
        "</body>",
        encoding="utf-8",
    )
    page_url = page.as_uri()
    expected_first_href = (tmp_path / "first.html").as_uri()

    process, endpoint = _launch_browser_with_devtools(browsers, tmp_path, page_url)
    try:
        target_id = _wait_for_page_target(endpoint, page_url, process)
        page_evidence = _wait_for_page_evidence(
            endpoint,
            target_id,
            process,
            expected_url=page_url,
            expected_title=expected_title,
            expected_text=expected_text,
            text_limit=text_limit,
        )

        assert page_evidence.endpoint == endpoint
        assert page_evidence.target_id == target_id
        assert page_evidence.url == page_url
        assert page_evidence.title == expected_title
        assert page_evidence.content.source == "document.body.innerText"
        assert page_evidence.content.text_prefix == "alpha 😀"
        assert page_evidence.content.text_character_count == len(expected_text)
        assert page_evidence.content.text_limit == text_limit
        assert page_evidence.content.truncated is True

        link_evidence = _wait_for_link_evidence(
            endpoint,
            target_id,
            process,
            expected_url=page_url,
            expected_first_href=expected_first_href,
        )

        assert link_evidence.endpoint == endpoint
        assert link_evidence.target_id == target_id
        assert link_evidence.url == page_url
        assert link_evidence.source == "document.querySelectorAll('a[href]')"
        assert link_evidence.link_count == 3
        assert link_evidence.link_limit == 2
        assert link_evidence.truncated is True
        assert link_evidence.links[0].ordinal == 1
        assert link_evidence.links[0].href == expected_first_href
        assert link_evidence.links[0].text_prefix == "First 😀"
        assert link_evidence.links[0].text_character_count == len("First 😀 link")
        assert link_evidence.links[0].text_limit == 7
        assert link_evidence.links[0].truncated is True
        assert link_evidence.links[1].ordinal == 2
        assert link_evidence.links[1].href == "mailto:research@example.test"
        assert link_evidence.links[1].text_prefix == "Email"
        assert link_evidence.links[1].truncated is False

        heading_evidence = _wait_for_heading_evidence(
            endpoint,
            target_id,
            process,
            expected_url=page_url,
        )

        assert heading_evidence.endpoint == endpoint
        assert heading_evidence.target_id == target_id
        assert heading_evidence.url == page_url
        assert heading_evidence.source == "document.querySelectorAll('h1,h2,h3,h4,h5,h6')"
        assert heading_evidence.heading_count == 3
        assert heading_evidence.heading_limit == 2
        assert heading_evidence.truncated is True
        assert heading_evidence.headings[0].ordinal == 1
        assert heading_evidence.headings[0].level == 1
        assert heading_evidence.headings[0].text_prefix == "Intro 😀"
        assert heading_evidence.headings[0].text_character_count == len("Intro 😀 section")
        assert heading_evidence.headings[0].text_limit == 7
        assert heading_evidence.headings[0].truncated is True
        assert heading_evidence.headings[1].ordinal == 2
        assert heading_evidence.headings[1].level == 3
        assert heading_evidence.headings[1].text_prefix == "Methods"
        assert heading_evidence.headings[1].truncated is False
    finally:
        _terminate_browser(process)
