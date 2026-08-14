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
    ChromiumPageLinksEvidence,
    ChromiumPageObservationEvidence,
    observe_chromium_page,
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
    page_urls: tuple[str, ...],
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
                *page_urls,
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

    links_page = tmp_path / "links.html"
    links_page.write_text(
        "<!doctype html><meta charset='utf-8'><title>Pyxis 15B</title><body>"
        "<a href='first.html'>First 😀 link</a>"
        "<a href='mailto:research@example.test'>Email</a>"
        "<a href='javascript:void(0)'>Action</a>"
        "</body>",
        encoding="utf-8",
    )
    links_page_url = links_page.as_uri()
    expected_first_href = (tmp_path / "first.html").as_uri()

    process, endpoint = _launch_browser_with_devtools(
        browsers,
        tmp_path,
        (page_url, links_page_url),
    )
    try:
        page_target_id = _wait_for_page_target(endpoint, page_url, process)
        page_evidence = _wait_for_page_evidence(
            endpoint,
            page_target_id,
            process,
            expected_url=page_url,
            expected_title=expected_title,
            expected_text=expected_text,
            text_limit=text_limit,
        )

        assert page_evidence.endpoint == endpoint
        assert page_evidence.target_id == page_target_id
        assert page_evidence.url == page_url
        assert page_evidence.title == expected_title
        assert page_evidence.content.source == "document.body.innerText"
        assert page_evidence.content.text_prefix == "alpha 😀"
        assert page_evidence.content.text_character_count == len(expected_text)
        assert page_evidence.content.text_limit == text_limit
        assert page_evidence.content.truncated is True

        links_target_id = _wait_for_page_target(endpoint, links_page_url, process)
        link_evidence = _wait_for_link_evidence(
            endpoint,
            links_target_id,
            process,
            expected_url=links_page_url,
            expected_first_href=expected_first_href,
        )

        assert link_evidence.endpoint == endpoint
        assert link_evidence.target_id == links_target_id
        assert link_evidence.url == links_page_url
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
    finally:
        _terminate_browser(process)
