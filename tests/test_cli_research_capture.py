from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from pyxis import cli


def _bundle() -> object:
    return object()


def _persisted(path: Path, *, digest: str = "a" * 64):
    return SimpleNamespace(
        path=path.resolve(),
        capture_format="pyxis.chromium.research_capture.v1",
        bundle_sha256=digest,
        byte_count=321,
    )


def _verified(path: Path, *, digest: str = "a" * 64):
    return SimpleNamespace(
        path=path.resolve(),
        capture_format="pyxis.chromium.research_capture.v1",
        bundle_sha256=digest,
        byte_count=321,
        endpoint="http://127.0.0.1:9222",
        target_id="PAGE-EXACT",
        url="https://example.test/research",
        acquisition_mode="sequential_non_atomic_url_coherent",
        acquisition_order=(
            "page",
            "links",
            "headings",
            "metadata",
            "paragraphs",
            "tables",
            "lists",
        ),
    )


def test_51a_cli_research_capture_delegates_exact_target_and_emits_verification_receipt(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    destination = tmp_path / "capture.json"
    bundle = _bundle()
    persisted = _persisted(destination)
    verified = _verified(destination)
    calls: list[tuple] = []

    def observe(endpoint: str, *, target_id: str | None = None):
        calls.append(("observe", endpoint, target_id))
        return bundle

    def persist(observed, output: Path):
        calls.append(("persist", observed, output))
        assert observed is bundle
        assert output == destination
        return persisted

    def verify(source: Path):
        calls.append(("verify", source))
        assert source == persisted.path
        return verified

    monkeypatch.setattr(cli, "observe_chromium_page_research_bundle", observe)
    monkeypatch.setattr(cli, "persist_chromium_page_research_capture", persist)
    monkeypatch.setattr(cli, "verify_chromium_page_research_capture", verify)

    assert (
        cli.main(
            [
                "research-capture",
                "--endpoint",
                "http://127.0.0.1:9222",
                "--target-id",
                "PAGE-EXACT",
                "--destination",
                str(destination),
            ]
        )
        == 0
    )

    assert calls == [
        ("observe", "http://127.0.0.1:9222", "PAGE-EXACT"),
        ("persist", bundle, destination),
        ("verify", persisted.path),
    ]
    assert json.loads(capsys.readouterr().out) == {
        "acquisition_mode": "sequential_non_atomic_url_coherent",
        "acquisition_order": [
            "page",
            "links",
            "headings",
            "metadata",
            "paragraphs",
            "tables",
            "lists",
        ],
        "bundle_sha256": "a" * 64,
        "byte_count": 321,
        "capture_format": "pyxis.chromium.research_capture.v1",
        "capture_output_path": str(destination.resolve()),
        "endpoint": "http://127.0.0.1:9222",
        "receipt_role": "operation_receipt_not_source_authentication",
        "target_id": "PAGE-EXACT",
        "url": "https://example.test/research",
    }


def test_51a_cli_research_capture_forwards_omitted_target_as_none(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    destination = tmp_path / "capture.json"
    bundle = _bundle()

    def observe(endpoint: str, *, target_id: str | None = None):
        assert endpoint == "http://127.0.0.1:9222"
        assert target_id is None
        return bundle

    monkeypatch.setattr(cli, "observe_chromium_page_research_bundle", observe)
    monkeypatch.setattr(
        cli,
        "persist_chromium_page_research_capture",
        lambda observed, output: _persisted(destination),
    )
    monkeypatch.setattr(
        cli,
        "verify_chromium_page_research_capture",
        lambda source: _verified(destination),
    )

    assert (
        cli.main(
            [
                "research-capture",
                "--endpoint",
                "http://127.0.0.1:9222",
                "--destination",
                str(destination),
            ]
        )
        == 0
    )
    assert json.loads(capsys.readouterr().out)["target_id"] == "PAGE-EXACT"


@pytest.mark.parametrize(
    ("field", "replacement", "message"),
    [
        ("path", Path("/tmp/other-capture.json"), "path does not match"),
        ("capture_format", "pyxis.chromium.research_capture.v2", "format does not match"),
        ("bundle_sha256", "b" * 64, "SHA-256 does not match"),
        ("byte_count", 999, "byte count does not match"),
    ],
)
def test_51a_cli_research_capture_rejects_persistence_verification_disagreement(
    tmp_path: Path,
    monkeypatch,
    capsys,
    field: str,
    replacement,
    message: str,
) -> None:
    destination = tmp_path / "capture.json"
    bundle = _bundle()
    persisted = _persisted(destination)
    values = vars(_verified(destination)).copy()
    values[field] = replacement
    verified = SimpleNamespace(**values)

    monkeypatch.setattr(
        cli,
        "observe_chromium_page_research_bundle",
        lambda endpoint, *, target_id=None: bundle,
    )
    monkeypatch.setattr(
        cli,
        "persist_chromium_page_research_capture",
        lambda observed, output: persisted,
    )
    monkeypatch.setattr(
        cli,
        "verify_chromium_page_research_capture",
        lambda source: verified,
    )

    with pytest.raises(SystemExit) as exc_info:
        cli.main(
            [
                "research-capture",
                "--endpoint",
                "http://127.0.0.1:9222",
                "--destination",
                str(destination),
            ]
        )

    assert exc_info.value.code == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert message in captured.err


def test_51a_cli_research_capture_observation_failure_writes_nothing(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    destination = tmp_path / "capture.json"
    persist_called = False

    def fail_observe(endpoint: str, *, target_id: str | None = None):
        assert target_id is None
        raise ValueError(
            "Multiple Chromium page targets are available; supply target_id explicitly."
        )

    def persist(*args, **kwargs):
        nonlocal persist_called
        persist_called = True
        raise AssertionError("persistence must not run after observation failure")

    monkeypatch.setattr(cli, "observe_chromium_page_research_bundle", fail_observe)
    monkeypatch.setattr(cli, "persist_chromium_page_research_capture", persist)

    with pytest.raises(SystemExit) as exc_info:
        cli.main(
            [
                "research-capture",
                "--endpoint",
                "http://127.0.0.1:9222",
                "--destination",
                str(destination),
            ]
        )

    assert exc_info.value.code == 2
    assert persist_called is False
    assert not destination.exists()
    assert "supply target_id explicitly" in capsys.readouterr().err


def test_51a_cli_research_capture_existing_destination_failure_preserves_bytes(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    destination = tmp_path / "capture.json"
    destination.write_bytes(b"preexisting")
    bundle = _bundle()

    monkeypatch.setattr(
        cli,
        "observe_chromium_page_research_bundle",
        lambda endpoint, *, target_id=None: bundle,
    )

    def fail_persist(observed, output: Path):
        assert observed is bundle
        assert output == destination
        assert destination.read_bytes() == b"preexisting"
        raise FileExistsError("destination already exists")

    monkeypatch.setattr(cli, "persist_chromium_page_research_capture", fail_persist)

    with pytest.raises(SystemExit) as exc_info:
        cli.main(
            [
                "research-capture",
                "--endpoint",
                "http://127.0.0.1:9222",
                "--destination",
                str(destination),
            ]
        )

    assert exc_info.value.code == 2
    assert destination.read_bytes() == b"preexisting"
    assert "destination already exists" in capsys.readouterr().err


def test_51a_cli_research_capture_missing_parent_creates_nothing(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    destination = tmp_path / "missing" / "capture.json"
    bundle = _bundle()

    monkeypatch.setattr(
        cli,
        "observe_chromium_page_research_bundle",
        lambda endpoint, *, target_id=None: bundle,
    )

    def fail_persist(observed, output: Path):
        assert output == destination
        raise FileNotFoundError("Research capture parent directory does not exist")

    monkeypatch.setattr(cli, "persist_chromium_page_research_capture", fail_persist)

    with pytest.raises(SystemExit) as exc_info:
        cli.main(
            [
                "research-capture",
                "--endpoint",
                "http://127.0.0.1:9222",
                "--destination",
                str(destination),
            ]
        )

    assert exc_info.value.code == 2
    assert not destination.exists()
    assert not destination.parent.exists()
    assert "parent directory does not exist" in capsys.readouterr().err


def test_51a_cli_research_capture_help_exposes_only_narrow_capture_inputs(capsys) -> None:
    with pytest.raises(SystemExit) as exc_info:
        cli.main(["research-capture", "--help"])

    output = capsys.readouterr().out
    assert exc_info.value.code == 0
    for option in ("--endpoint", "--target-id", "--destination"):
        assert option in output
    for forbidden in (
        "--url",
        "--navigate",
        "--active",
        "--current",
        "--latest",
        "--head",
        "--click",
        "--script",
        "--javascript",
        "--interval",
    ):
        assert forbidden not in output
