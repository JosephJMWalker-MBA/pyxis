from __future__ import annotations

import json
import os
from pathlib import Path
import re
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
from pyxis.app.chromium_research_capture_load import load_chromium_page_research_capture
from pyxis.browser import ChromiumReadError


_DEVTOOLS_LISTENING_PATTERN = re.compile(
    r"DevTools listening on ws://127\\.0\\.0\\.1:(\\d+)/"
)
_BROWSER_LAUNCH_ROUNDS = 2
_BROWSER_LOG_TAIL_LIMIT = 2000


def _browser_log_tail(source: Path) -> str:
    try:
        text = source.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return "<browser log unavailable>"
    if not text:
        return "<browser log empty>"
    return text[-_BROWSER_LOG_TAIL_LIMIT:]


def _devtools_endpoint_from_browser_log(source: Path) -> str | None:
    """Recover Chrome's own ephemeral DevTools endpoint announcement."""

    try:
        text = source.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    matches = _DEVTOOLS_LISTENING_PATTERN.findall(text)
    if not matches:
        return None
    port = int(matches[-1])
    if not 1 <= port <= 65535:
        return None
    return f"http://127.0.0.1:{port}"


def _wait_for_devtools_endpoint(
    profile: Path,
    process: subprocess.Popen,
    *,
    browser_log: Path,
    timeout_seconds: float = 30.0,
) -> str:
    """Wait for either documented ephemeral-port bootstrap signal from Chrome."""

    active_port = profile / "DevToolsActivePort"
    deadline = time.monotonic() + timeout_seconds
    last_error: Exception | None = None

    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise AssertionError(
                "Chromium exited before publishing a usable DevTools endpoint: "
                f"{process.returncode}; browser log tail={_browser_log_tail(browser_log)!r}"
            )
        try:
            lines = active_port.read_text(encoding="utf-8").splitlines()
            if lines and int(lines[0]) > 0:
                return f"http://127.0.0.1:{int(lines[0])}"
        except (OSError, ValueError) as exc:
            last_error = exc

        announced = _devtools_endpoint_from_browser_log(browser_log)
        if announced is not None:
            return announced
        time.sleep(0.1)

    raise AssertionError(
        "Timed out waiting for Chromium DevTools endpoint bootstrap; "
        f"DevToolsActivePort last error={last_error!r}; "
        f"browser log tail={_browser_log_tail(browser_log)!r}"
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
) -> tuple[subprocess.Popen, str, str]:
    """Launch a browser only after its exact fixture page target is reachable."""

    startup_failures: list[str] = []
    for round_index in range(_BROWSER_LAUNCH_ROUNDS):
        for browser_index, browser in enumerate(binaries):
            profile = tmp_path / (
                "chromium-research-bundle-profile-"
                f"{round_index}-{browser_index}"
            )
            browser_log = tmp_path / (
                "chromium-research-bundle-browser-"
                f"{round_index}-{browser_index}.log"
            )
            log_handle = browser_log.open("wb")
            try:
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
                    stdout=log_handle,
                    stderr=subprocess.STDOUT,
                )
            finally:
                log_handle.close()

            try:
                endpoint = _wait_for_devtools_endpoint(
                    profile,
                    process,
                    browser_log=browser_log,
                )
                target_id = _wait_for_page_target(
                    endpoint,
                    page_url,
                    process,
                )
            except AssertionError as exc:
                _terminate_browser(process)
                startup_failures.append(
                    f"{browser} attempt {round_index + 1}: {exc}; "
                    f"browser log tail={_browser_log_tail(browser_log)!r}"
                )
                continue
            return process, endpoint, target_id

    details = "; ".join(startup_failures) or "no launch attempts were made"
    raise AssertionError(
        "No installed Chromium-family browser published a reachable exact page target; "
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
                and evidence.page.content.text_prefix.startswith("Evidence")
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





class _RunningProcess:
    returncode = None

    def poll(self):
        return None


def test_devtools_endpoint_bootstrap_accepts_browser_announcement_when_port_file_absent(
    tmp_path: Path,
) -> None:
    profile = tmp_path / "profile-without-active-port"
    profile.mkdir()
    browser_log = tmp_path / "browser.log"
    browser_log.write_text(
        "noise before startup\n"
        "DevTools listening on ws://127.0.0.1:45678/devtools/browser/example-id\n",
        encoding="utf-8",
    )

    endpoint = _wait_for_devtools_endpoint(
        profile,
        _RunningProcess(),
        browser_log=browser_log,
        timeout_seconds=0.1,
    )

    assert endpoint == "http://127.0.0.1:45678"
    assert not (profile / "DevToolsActivePort").exists()


def test_devtools_endpoint_log_parser_uses_latest_valid_announcement(
    tmp_path: Path,
) -> None:
    browser_log = tmp_path / "browser.log"
    browser_log.write_text(
        "DevTools listening on ws://127.0.0.1:12345/devtools/browser/old\n"
        "other output\n"
        "DevTools listening on ws://127.0.0.1:54321/devtools/browser/new\n",
        encoding="utf-8",
    )

    assert _devtools_endpoint_from_browser_log(browser_log) == (
        "http://127.0.0.1:54321"
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

    process, endpoint, target_id = _launch_browser_with_devtools(
        browsers,
        tmp_path,
        page_url,
    )
    try:
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

    assert process.poll() is not None
    loaded = load_chromium_page_research_capture(capture_path)
    assert loaded.verification.bundle_sha256 == capture.bundle_sha256
    assert loaded.verification.byte_count == capture.byte_count
    assert loaded.bundle == evidence
    assert loaded.bundle is not evidence
    assert loaded.bundle.page is not evidence.page
    assert loaded.bundle.endpoint == endpoint
    assert loaded.bundle.target_id == target_id
    assert loaded.bundle.url == page_url
    assert loaded.bundle.acquisition_mode == evidence.acquisition_mode
    assert loaded.bundle.acquisition_order == evidence.acquisition_order
