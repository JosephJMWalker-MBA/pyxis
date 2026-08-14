from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import time
from urllib.request import urlopen

import pytest

from pyxis.app import observe_chromium_page


def _free_loopback_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


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


def test_observe_chromium_page_against_real_headless_browser(tmp_path: Path) -> None:
    browser = shutil.which("google-chrome") or shutil.which("chromium")
    if browser is None:
        if os.environ.get("GITHUB_ACTIONS") == "true":
            pytest.fail("GitHub Actions browser integration requires Chrome or Chromium.")
        pytest.skip("Chrome/Chromium is not installed on this machine.")

    page = tmp_path / "page.html"
    page.write_text(
        "<!doctype html><meta charset='utf-8'><title>Pyxis 15A</title>"
        "<body>alpha 😀 beta</body>",
        encoding="utf-8",
    )
    page_url = page.as_uri()
    port = _free_loopback_port()
    endpoint = f"http://127.0.0.1:{port}"
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
            f"--remote-debugging-port={port}",
            f"--user-data-dir={profile}",
            page_url,
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    try:
        target_id = _wait_for_page_target(endpoint, page_url, process)
        evidence = observe_chromium_page(
            endpoint,
            target_id=target_id,
            text_limit=7,
            timeout=3.0,
        )

        assert evidence.endpoint == endpoint
        assert evidence.target_id == target_id
        assert evidence.url == page_url
        assert evidence.title == "Pyxis 15A"
        assert evidence.content.source == "document.body.innerText"
        assert evidence.content.text_prefix == "alpha 😀"
        assert evidence.content.text_character_count == len("alpha 😀 beta")
        assert evidence.content.text_limit == 7
        assert evidence.content.truncated is True
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)
