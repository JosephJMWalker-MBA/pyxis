from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import time
from urllib.request import urlopen

import pytest

from pyxis.app.chromium_research_bundle import (
    ChromiumPageResearchEvidenceBundle,
    observe_chromium_page_research_bundle,
)
from pyxis.app.chromium_research_capture import (
    persist_chromium_page_research_capture,
    verify_chromium_page_research_capture,
)
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
        profile = tmp_path / f"chromium-research-bundle-profile-{index}"
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


def _wait_for_bundle(
    endpoint: str,
    target_id: str,
    process: subprocess.Popen,
    *,
    expected_url: str,
    timeout_seconds: float = 15.0,
) -> ChromiumPageResearchEvidenceBundle:
    deadline = time.monotonic() + timeout_seconds
    last_evidence: ChromiumPageResearchEvidenceBundle | None = None
    last_error: ChromiumReadError | None = None

    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise AssertionError(
                f"Chromium exited before research-bundle evidence became ready: {process.returncode}"
            )
        try:
            evidence = observe_chromium_page_research_bundle(
                endpoint,
                target_id=target_id,
                timeout=3.0,
            )
            last_evidence = evidence
            if (
                evidence.url == expected_url
                and evidence.page.title == "Pyxis research bundle"
                and evidence.links.link_count == 1
                and evidence.headings.heading_count == 1
                and evidence.metadata.document_language == "en"
                and evidence.metadata.canonical_link_count == 1
                and evidence.metadata.description_count == 1
                and evidence.paragraphs.paragraph_count == 1
                and evidence.tables.table_count == 1
                and evidence.lists.list_count == 1
            ):
                return evidence
        except ChromiumReadError as exc:
            last_error = exc
        time.sleep(0.1)

    raise AssertionError(
        "Timed out waiting for loaded Chromium research-bundle evidence; "
        f"last evidence={last_evidence!r}; last error={last_error!r}"
    )


def test_research_bundle_composes_all_proven_readers_against_real_chromium(
    tmp_path: Path,
) -> None:
    browsers = _installed_browser_binaries()
    if not browsers:
        if os.environ.get("GITHUB_ACTIONS") == "true":
            pytest.fail("GitHub Actions browser integration requires Chrome or Chromium.")
        pytest.skip("Chrome/Chromium is not installed on this machine.")

    page = tmp_path / "research-bundle-page.html"
    page.write_text(
        "<!doctype html><html lang='en'><head><meta charset='utf-8'>"
        "<title>Pyxis research bundle</title>"
        "<link rel='canonical' href='canonical.html'>"
        "<meta name='description' content='Research bundle fixture'>"
        "</head><body>"
        "<h1>Evidence</h1>"
        "<p id='passage'>Passage <a href='source.html'>Source</a></p>"
        "<table><caption>Data</caption><tr><th>Metric</th><td>1</td></tr></table>"
        "<ol start='2'><li value='4'>First</li></ol>"
        "</body></html>",
        encoding="utf-8",
    )
    page_url = page.as_uri()

    process, endpoint = _launch_browser_with_devtools(browsers, tmp_path, page_url)
    try:
        target_id = _wait_for_page_target(endpoint, page_url, process)
        evidence = _wait_for_bundle(
            endpoint,
            target_id,
            process,
            expected_url=page_url,
        )

        assert evidence.endpoint == endpoint
        assert evidence.target_id == target_id
        assert evidence.url == page_url
        assert evidence.acquisition_mode == "sequential_non_atomic_url_coherent"
        assert evidence.acquisition_order == (
            "page",
            "links",
            "headings",
            "metadata",
            "paragraphs",
            "tables",
            "lists",
        )

        members = (
            evidence.page,
            evidence.links,
            evidence.headings,
            evidence.metadata,
            evidence.paragraphs,
            evidence.tables,
            evidence.lists,
        )
        assert all(member.endpoint == endpoint for member in members)
        assert all(member.target_id == target_id for member in members)
        assert all(member.url == page_url for member in members)

        assert evidence.page.content.text_prefix.startswith("Evidence")
        assert evidence.links.links[0].text_prefix == "Source"
        assert evidence.headings.headings[0].level == 1
        assert evidence.metadata.canonical_links[0].raw_href == "canonical.html"
        assert evidence.metadata.descriptions[0].content_prefix == "Research bundle fixture"
        assert evidence.paragraphs.paragraphs[0].element_id == "passage"
        assert evidence.tables.tables[0].rows[0].cells[0].tag_name == "TH"
        assert evidence.lists.lists[0].tag_name == "OL"
        assert evidence.lists.lists[0].start_attribute == "2"
        assert evidence.lists.lists[0].items[0].value_attribute == "4"

        capture_path = tmp_path / "research-capture.json"
        capture = persist_chromium_page_research_capture(evidence, capture_path)
        verification = verify_chromium_page_research_capture(capture_path)

        assert capture.bundle is evidence
        assert capture.capture_format == "pyxis.chromium.research_capture.v1"
        assert verification.bundle_sha256 == capture.bundle_sha256
        assert verification.byte_count == capture.byte_count
        assert verification.endpoint == endpoint
        assert verification.target_id == target_id
        assert verification.url == page_url
        assert verification.acquisition_mode == evidence.acquisition_mode
        assert verification.acquisition_order == evidence.acquisition_order
    finally:
        _terminate_browser(process)
