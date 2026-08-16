from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
import hashlib
import json
from pathlib import Path

import pytest

from pyxis.app.chromium_headings import ChromiumPageHeadingsEvidence
from pyxis.app.chromium_lists import ChromiumPageListsEvidence
from pyxis.app.chromium_metadata import ChromiumPageMetadataEvidence
from pyxis.app.chromium_observation import (
    ChromiumPageContentEvidence,
    ChromiumPageLinksEvidence,
    ChromiumPageObservationEvidence,
)
from pyxis.app.chromium_paragraphs import ChromiumPageParagraphsEvidence
from pyxis.app.chromium_research_bundle import ChromiumPageResearchEvidenceBundle
from pyxis.app.chromium_research_capture import (
    ChromiumResearchCaptureIntegrityError,
    persist_chromium_page_research_capture,
    verify_chromium_page_research_capture,
)
from pyxis.app.chromium_research_capture_load import load_chromium_page_research_capture
from pyxis.app.chromium_tables import ChromiumPageTablesEvidence


ENDPOINT = "http://127.0.0.1:9222"
TARGET_ID = "page-1"
URL = "https://example.test/research"
ORDER = (
    "page",
    "links",
    "headings",
    "metadata",
    "paragraphs",
    "tables",
    "lists",
)


def _bundle() -> ChromiumPageResearchEvidenceBundle:
    page = ChromiumPageObservationEvidence(
        endpoint=ENDPOINT,
        target_id=TARGET_ID,
        url=URL,
        title="Research 😀 page",
        content=ChromiumPageContentEvidence(
            source="document.body.innerText",
            text_prefix="Body 😀",
            text_character_count=6,
            text_limit=2048,
            truncated=False,
        ),
    )
    links = ChromiumPageLinksEvidence(
        endpoint=ENDPOINT,
        target_id=TARGET_ID,
        url=URL,
        source="document.querySelectorAll('a[href]')",
        links=(),
        link_count=0,
        link_limit=64,
        truncated=False,
    )
    headings = ChromiumPageHeadingsEvidence(
        endpoint=ENDPOINT,
        target_id=TARGET_ID,
        url=URL,
        source="document.querySelectorAll('h1,h2,h3,h4,h5,h6')",
        headings=(),
        heading_count=0,
        heading_limit=64,
        truncated=False,
    )
    metadata = ChromiumPageMetadataEvidence(
        endpoint=ENDPOINT,
        target_id=TARGET_ID,
        url=URL,
        document_language="en",
        language_source="document.documentElement.getAttribute('lang')",
        canonical_source='document.querySelectorAll("link[rel~=\'canonical\' i][href]")',
        canonical_links=(),
        canonical_link_count=0,
        canonical_link_limit=8,
        canonical_links_truncated=False,
        description_source='document.querySelectorAll("meta[name=\'description\' i]")',
        descriptions=(),
        description_count=0,
        description_limit=8,
        descriptions_truncated=False,
    )
    paragraphs = ChromiumPageParagraphsEvidence(
        endpoint=ENDPOINT,
        target_id=TARGET_ID,
        url=URL,
        source="document.querySelectorAll('p')",
        paragraphs=(),
        paragraph_count=0,
        paragraph_limit=128,
        truncated=False,
    )
    tables = ChromiumPageTablesEvidence(
        endpoint=ENDPOINT,
        target_id=TARGET_ID,
        url=URL,
        source="document.querySelectorAll('table')",
        tables=(),
        table_count=0,
        table_limit=32,
        truncated=False,
    )
    lists = ChromiumPageListsEvidence(
        endpoint=ENDPOINT,
        target_id=TARGET_ID,
        url=URL,
        source="document.querySelectorAll('ol,ul')",
        lists=(),
        list_count=0,
        list_limit=64,
        truncated=False,
    )
    return ChromiumPageResearchEvidenceBundle(
        endpoint=ENDPOINT,
        target_id=TARGET_ID,
        url=URL,
        acquisition_mode="sequential_non_atomic_url_coherent",
        acquisition_order=ORDER,
        page=page,
        links=links,
        headings=headings,
        metadata=metadata,
        paragraphs=paragraphs,
        tables=tables,
        lists=lists,
    )


def _write_self_consistent_document(path: Path, document: dict) -> None:
    bundle_bytes = json.dumps(
        document["bundle"],
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    document["bundle_sha256"] = hashlib.sha256(bundle_bytes).hexdigest()
    path.write_text(
        json.dumps(
            document,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
        + "\n",
        encoding="utf-8",
    )


def test_persist_and_verify_research_capture_is_deterministic_and_frozen(tmp_path: Path) -> None:
    bundle = _bundle()
    first_path = tmp_path / "capture-one.json"
    second_path = tmp_path / "capture-two.json"

    first = persist_chromium_page_research_capture(bundle, first_path)
    second = persist_chromium_page_research_capture(bundle, second_path)

    assert first.bundle is bundle
    assert first.capture_format == "pyxis.chromium.research_capture.v1"
    assert first.path == first_path.resolve()
    assert first.bundle_sha256 == second.bundle_sha256
    assert first.byte_count == second.byte_count
    assert first_path.read_bytes() == second_path.read_bytes()
    assert "😀".encode("utf-8") in first_path.read_bytes()

    verification = verify_chromium_page_research_capture(first_path)
    assert verification.path == first_path.resolve()
    assert verification.capture_format == first.capture_format
    assert verification.bundle_sha256 == first.bundle_sha256
    assert verification.byte_count == first.byte_count
    assert verification.endpoint == ENDPOINT
    assert verification.target_id == TARGET_ID
    assert verification.url == URL
    assert verification.acquisition_mode == "sequential_non_atomic_url_coherent"
    assert verification.acquisition_order == ORDER
    assert verification.document_json.encode("utf-8") == first_path.read_bytes()

    with pytest.raises(FrozenInstanceError):
        verification.url = "changed"  # type: ignore[misc]


def test_load_research_capture_retains_verification_and_losslessly_rehydrates_bundle(
    tmp_path: Path,
) -> None:
    bundle = _bundle()
    path = tmp_path / "capture.json"
    capture = persist_chromium_page_research_capture(bundle, path)

    loaded = load_chromium_page_research_capture(path)

    assert loaded.verification.path == path.resolve()
    assert loaded.verification.bundle_sha256 == capture.bundle_sha256
    assert loaded.verification.byte_count == capture.byte_count
    assert loaded.bundle == bundle
    assert loaded.bundle is not bundle
    assert loaded.bundle.page is not bundle.page
    assert loaded.bundle.metadata is not bundle.metadata
    assert loaded.bundle.acquisition_mode == bundle.acquisition_mode
    assert loaded.bundle.acquisition_order == bundle.acquisition_order

    with pytest.raises(FrozenInstanceError):
        loaded.bundle.url = "changed"  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        loaded.verification.url = "changed"  # type: ignore[misc]


def test_persist_research_capture_refuses_overwrite_and_missing_parent(tmp_path: Path) -> None:
    bundle = _bundle()
    existing = tmp_path / "capture.json"
    existing.write_text("keep me", encoding="utf-8")

    with pytest.raises(FileExistsError):
        persist_chromium_page_research_capture(bundle, existing)
    assert existing.read_text(encoding="utf-8") == "keep me"

    missing_parent = tmp_path / "missing" / "capture.json"
    with pytest.raises(FileNotFoundError, match="parent directory"):
        persist_chromium_page_research_capture(bundle, missing_parent)
    assert not missing_parent.exists()


def test_persist_research_capture_rejects_incoherent_live_bundle_before_write(tmp_path: Path) -> None:
    bundle = _bundle()
    incoherent_links = replace(bundle.links, url="https://example.test/changed")
    incoherent = replace(bundle, links=incoherent_links)
    destination = tmp_path / "capture.json"

    with pytest.raises(ValueError, match="links url is incoherent"):
        persist_chromium_page_research_capture(incoherent, destination)

    assert not destination.exists()


def test_verify_research_capture_rejects_payload_change_with_stale_digest(tmp_path: Path) -> None:
    path = tmp_path / "capture.json"
    persist_chromium_page_research_capture(_bundle(), path)
    document = json.loads(path.read_text(encoding="utf-8"))
    document["bundle"]["url"] = "https://example.test/tampered"
    for name in ORDER:
        document["bundle"][name]["url"] = "https://example.test/tampered"
    path.write_text(
        json.dumps(
            document,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n",
        encoding="utf-8",
    )

    with pytest.raises(ChromiumResearchCaptureIntegrityError, match="SHA-256"):
        verify_chromium_page_research_capture(path)


def test_verify_research_capture_rejects_noncanonical_bytes_even_when_digest_matches(
    tmp_path: Path,
) -> None:
    path = tmp_path / "capture.json"
    capture = persist_chromium_page_research_capture(_bundle(), path)
    document = json.loads(path.read_text(encoding="utf-8"))
    bundle_bytes = json.dumps(
        document["bundle"],
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    assert hashlib.sha256(bundle_bytes).hexdigest() == capture.bundle_sha256

    path.write_text(json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    with pytest.raises(ChromiumResearchCaptureIntegrityError, match="canonical Pyxis JSON"):
        verify_chromium_page_research_capture(path)


def test_load_research_capture_rejects_checksum_valid_semantic_corruption(tmp_path: Path) -> None:
    path = tmp_path / "capture.json"
    persist_chromium_page_research_capture(_bundle(), path)
    document = json.loads(path.read_text(encoding="utf-8"))
    document["bundle"]["links"]["link_count"] = -1
    _write_self_consistent_document(path, document)

    assert verify_chromium_page_research_capture(path).bundle_sha256 == document["bundle_sha256"]
    with pytest.raises(ChromiumResearchCaptureIntegrityError, match="links count is negative"):
        load_chromium_page_research_capture(path)


def test_load_research_capture_rejects_checksum_valid_json_type_corruption(tmp_path: Path) -> None:
    path = tmp_path / "capture.json"
    persist_chromium_page_research_capture(_bundle(), path)
    document = json.loads(path.read_text(encoding="utf-8"))
    document["bundle"]["headings"]["heading_limit"] = True
    _write_self_consistent_document(path, document)

    assert verify_chromium_page_research_capture(path).bundle_sha256 == document["bundle_sha256"]
    with pytest.raises(
        ChromiumResearchCaptureIntegrityError,
        match=r"bundle\.headings\.heading_limit must be a JSON integer",
    ):
        load_chromium_page_research_capture(path)
