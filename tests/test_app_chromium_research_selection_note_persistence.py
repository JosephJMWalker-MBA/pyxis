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
from pyxis.app.chromium_paragraphs import (
    ChromiumPageParagraphEvidence,
    ChromiumPageParagraphsEvidence,
)
from pyxis.app.chromium_research_bundle import ChromiumPageResearchEvidenceBundle
from pyxis.app.chromium_research_capture import ChromiumPageResearchCaptureVerificationEvidence
from pyxis.app.chromium_research_capture_load import ChromiumPageResearchLoadedCaptureEvidence
from pyxis.app.chromium_research_passage_selection import (
    select_chromium_research_capture_paragraph,
)
from pyxis.app.chromium_research_selection_note import (
    ChromiumPageResearchParagraphNoteRecord,
    create_chromium_research_paragraph_note,
)
from pyxis.app.chromium_research_selection_note_persistence import (
    ChromiumPageResearchParagraphNotePersistenceEvidence,
    ChromiumPageResearchParagraphNoteVerificationEvidence,
    ChromiumResearchParagraphNoteIntegrityError,
    persist_chromium_research_paragraph_note,
    verify_chromium_research_paragraph_note,
)
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
BUNDLE_SHA = "a" * 64


def _loaded_capture(*, path: Path) -> ChromiumPageResearchLoadedCaptureEvidence:
    page = ChromiumPageObservationEvidence(
        endpoint=ENDPOINT,
        target_id=TARGET_ID,
        url=URL,
        title="Research page",
        content=ChromiumPageContentEvidence(
            source="document.body.innerText",
            text_prefix="Alpha Beta",
            text_character_count=10,
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
        paragraphs=(
            ChromiumPageParagraphEvidence(
                ordinal=1,
                element_id="passage",
                text_prefix="Alpha",
                text_character_count=5,
                text_limit=1024,
                truncated=False,
            ),
            ChromiumPageParagraphEvidence(
                ordinal=2,
                element_id="passage",
                text_prefix="Beta",
                text_character_count=4,
                text_limit=1024,
                truncated=False,
            ),
        ),
        paragraph_count=2,
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
    bundle = ChromiumPageResearchEvidenceBundle(
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
    verification = ChromiumPageResearchCaptureVerificationEvidence(
        path=path,
        capture_format="pyxis.chromium.research_capture.v1",
        bundle_sha256=BUNDLE_SHA,
        byte_count=1,
        endpoint=ENDPOINT,
        target_id=TARGET_ID,
        url=URL,
        acquisition_mode="sequential_non_atomic_url_coherent",
        acquisition_order=ORDER,
        document_json="{}\n",
    )
    return ChromiumPageResearchLoadedCaptureEvidence(
        verification=verification,
        bundle=bundle,
    )


def _note(*, source_path: Path) -> ChromiumPageResearchParagraphNoteRecord:
    selection = select_chromium_research_capture_paragraph(
        _loaded_capture(path=source_path),
        paragraph_ordinal=2,
    )
    return create_chromium_research_paragraph_note(
        selection,
        note_text="  Human interpretation 😀\nKeep this exact.  ",
    )


def _canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def test_persist_note_writes_minimal_canonical_sidecar_and_retains_exact_note(
    tmp_path: Path,
) -> None:
    missing_source = tmp_path / "source-capture-does-not-need-to-exist.json"
    note = _note(source_path=missing_source)
    destination = tmp_path / "research-note.json"

    persisted = persist_chromium_research_paragraph_note(note, destination)

    assert isinstance(persisted, ChromiumPageResearchParagraphNotePersistenceEvidence)
    assert persisted.note is note
    assert persisted.path == destination.resolve()
    assert persisted.note_format == "pyxis.chromium.research_paragraph_note.v1"

    raw = destination.read_bytes()
    document = json.loads(raw)
    record = document["note_record"]
    assert record == {
        "note": {
            "mode": "caller_authored_exact_text_on_paragraph_selection",
            "text": "  Human interpretation 😀\nKeep this exact.  ",
        },
        "selection": {
            "mode": "caller_explicit_returned_paragraph_ordinal",
            "paragraph_ordinal": 2,
        },
        "source_capture": {
            "bundle_sha256": BUNDLE_SHA,
            "format": "pyxis.chromium.research_capture.v1",
        },
    }
    expected_sha = hashlib.sha256(_canonical_bytes(record)).hexdigest()
    assert document["note_record_sha256"] == expected_sha == persisted.note_record_sha256
    assert raw == _canonical_bytes(document) + b"\n"
    assert persisted.byte_count == len(raw)

    text = raw.decode("utf-8")
    assert URL not in text
    assert ENDPOINT not in text
    assert TARGET_ID not in text
    assert '"Beta"' not in text
    assert str(missing_source) not in text

    with pytest.raises(FrozenInstanceError):
        persisted.byte_count = 0  # type: ignore[misc]


def test_verify_note_reads_only_sidecar_and_preserves_exact_human_text(tmp_path: Path) -> None:
    missing_source = tmp_path / "missing-source-capture.json"
    assert not missing_source.exists()
    note = _note(source_path=missing_source)
    destination = tmp_path / "research-note.json"
    persisted = persist_chromium_research_paragraph_note(note, destination)

    verified = verify_chromium_research_paragraph_note(destination)

    assert isinstance(verified, ChromiumPageResearchParagraphNoteVerificationEvidence)
    assert verified.path == destination.resolve()
    assert verified.note_format == persisted.note_format
    assert verified.note_record_sha256 == persisted.note_record_sha256
    assert verified.byte_count == persisted.byte_count
    assert verified.source_capture_format == "pyxis.chromium.research_capture.v1"
    assert verified.source_bundle_sha256 == BUNDLE_SHA
    assert verified.selection_mode == "caller_explicit_returned_paragraph_ordinal"
    assert verified.paragraph_ordinal == 2
    assert verified.note_mode == "caller_authored_exact_text_on_paragraph_selection"
    assert verified.note_text == note.note_text
    assert verified.document_json == destination.read_text(encoding="utf-8")
    assert not missing_source.exists()


def test_persist_note_refuses_overwrite_and_missing_parent(tmp_path: Path) -> None:
    note = _note(source_path=tmp_path / "missing-source.json")
    destination = tmp_path / "research-note.json"

    persist_chromium_research_paragraph_note(note, destination)

    with pytest.raises(FileExistsError):
        persist_chromium_research_paragraph_note(note, destination)
    with pytest.raises(FileNotFoundError, match="parent directory does not exist"):
        persist_chromium_research_paragraph_note(
            note,
            tmp_path / "missing-parent" / "research-note.json",
        )


def test_persist_note_rejects_invalid_durable_source_reference(tmp_path: Path) -> None:
    note = _note(source_path=tmp_path / "missing-source.json")
    source = note.selection.source
    forged_verification = replace(source.verification, bundle_sha256="not-a-sha")
    forged_source = replace(source, verification=forged_verification)
    forged_selection = replace(note.selection, source=forged_source)
    forged_note = replace(note, selection=forged_selection)

    with pytest.raises(ValueError, match="bundle SHA-256 has an invalid shape"):
        persist_chromium_research_paragraph_note(
            forged_note,
            tmp_path / "research-note.json",
        )


def test_verify_note_rejects_digest_mismatch_and_noncanonical_bytes(tmp_path: Path) -> None:
    note = _note(source_path=tmp_path / "missing-source.json")
    destination = tmp_path / "research-note.json"
    persist_chromium_research_paragraph_note(note, destination)

    document = json.loads(destination.read_text(encoding="utf-8"))
    document["note_record"]["note"]["text"] = "Changed without updating digest"
    destination.write_bytes(_canonical_bytes(document) + b"\n")

    with pytest.raises(ChromiumResearchParagraphNoteIntegrityError, match="SHA-256"):
        verify_chromium_research_paragraph_note(destination)

    persist_again = tmp_path / "canonical-note.json"
    persist_chromium_research_paragraph_note(note, persist_again)
    canonical_document = json.loads(persist_again.read_text(encoding="utf-8"))
    persist_again.write_text(
        json.dumps(canonical_document, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    with pytest.raises(ChromiumResearchParagraphNoteIntegrityError, match="canonical"):
        verify_chromium_research_paragraph_note(persist_again)


def test_recomputed_digest_is_self_integrity_not_authentication(tmp_path: Path) -> None:
    note = _note(source_path=tmp_path / "missing-source.json")
    destination = tmp_path / "research-note.json"
    persist_chromium_research_paragraph_note(note, destination)

    document = json.loads(destination.read_text(encoding="utf-8"))
    record = document["note_record"]
    record["note"]["text"] = "Different human text with a recomputed digest."
    document["note_record_sha256"] = hashlib.sha256(_canonical_bytes(record)).hexdigest()
    destination.write_bytes(_canonical_bytes(document) + b"\n")

    verified = verify_chromium_research_paragraph_note(destination)

    assert verified.note_text == "Different human text with a recomputed digest."
    assert verified.note_record_sha256 == document["note_record_sha256"]
