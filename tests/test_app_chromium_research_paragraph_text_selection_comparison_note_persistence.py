from __future__ import annotations

from dataclasses import FrozenInstanceError, fields, replace
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
from pyxis.app.chromium_research_paragraph_text_selection import (
    select_chromium_research_paragraph_text,
)
from pyxis.app.chromium_research_paragraph_text_selection_comparison import (
    create_chromium_research_paragraph_text_selection_comparison,
)
from pyxis.app.chromium_research_paragraph_text_selection_comparison_note import (
    ChromiumPageResearchParagraphTextSelectionComparisonNoteRecord,
    create_chromium_research_paragraph_text_selection_comparison_note,
)
from pyxis.app.chromium_research_paragraph_text_selection_comparison_note_persistence import (
    ChromiumPageResearchParagraphTextSelectionComparisonNotePersistenceEvidence,
    ChromiumPageResearchParagraphTextSelectionComparisonNoteVerificationEvidence,
    ChromiumResearchParagraphTextSelectionComparisonNoteIntegrityError,
    persist_chromium_research_paragraph_text_selection_comparison_note,
    verify_chromium_research_paragraph_text_selection_comparison_note,
)
from pyxis.app.chromium_research_passage_selection import (
    select_chromium_research_capture_paragraph,
)
from pyxis.app.chromium_tables import ChromiumPageTablesEvidence


ENDPOINT = "http://127.0.0.1:9222"
ORDER = ("page", "links", "headings", "metadata", "paragraphs", "tables", "lists")


def _loaded_capture(
    *,
    target_id: str,
    url: str,
    digest_character: str,
    paragraph_text: str,
) -> ChromiumPageResearchLoadedCaptureEvidence:
    page = ChromiumPageObservationEvidence(
        endpoint=ENDPOINT,
        target_id=target_id,
        url=url,
        title="Research page",
        content=ChromiumPageContentEvidence(
            source="document.body.innerText",
            text_prefix=paragraph_text,
            text_character_count=len(paragraph_text),
            text_limit=2048,
            truncated=False,
        ),
    )
    links = ChromiumPageLinksEvidence(
        endpoint=ENDPOINT,
        target_id=target_id,
        url=url,
        source="document.querySelectorAll('a[href]')",
        links=(),
        link_count=0,
        link_limit=64,
        truncated=False,
    )
    headings = ChromiumPageHeadingsEvidence(
        endpoint=ENDPOINT,
        target_id=target_id,
        url=url,
        source="document.querySelectorAll('h1,h2,h3,h4,h5,h6')",
        headings=(),
        heading_count=0,
        heading_limit=64,
        truncated=False,
    )
    metadata = ChromiumPageMetadataEvidence(
        endpoint=ENDPOINT,
        target_id=target_id,
        url=url,
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
    paragraph = ChromiumPageParagraphEvidence(
        ordinal=1,
        element_id="passage",
        text_prefix=paragraph_text,
        text_character_count=len(paragraph_text),
        text_limit=1024,
        truncated=False,
    )
    paragraphs = ChromiumPageParagraphsEvidence(
        endpoint=ENDPOINT,
        target_id=target_id,
        url=url,
        source="document.querySelectorAll('p')",
        paragraphs=(paragraph,),
        paragraph_count=1,
        paragraph_limit=128,
        truncated=False,
    )
    tables = ChromiumPageTablesEvidence(
        endpoint=ENDPOINT,
        target_id=target_id,
        url=url,
        source="document.querySelectorAll('table')",
        tables=(),
        table_count=0,
        table_limit=32,
        truncated=False,
    )
    lists = ChromiumPageListsEvidence(
        endpoint=ENDPOINT,
        target_id=target_id,
        url=url,
        source="document.querySelectorAll('ol,ul')",
        lists=(),
        list_count=0,
        list_limit=64,
        truncated=False,
    )
    bundle = ChromiumPageResearchEvidenceBundle(
        endpoint=ENDPOINT,
        target_id=target_id,
        url=url,
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
        path=Path(f"/tmp/{target_id}.json"),
        capture_format="pyxis.chromium.research_capture.v1",
        bundle_sha256=digest_character * 64,
        byte_count=1,
        endpoint=ENDPOINT,
        target_id=target_id,
        url=url,
        acquisition_mode="sequential_non_atomic_url_coherent",
        acquisition_order=ORDER,
        document_json="{}\n",
    )
    return ChromiumPageResearchLoadedCaptureEvidence(
        verification=verification,
        bundle=bundle,
    )


def _range(
    *,
    target_id: str,
    url: str,
    digest_character: str,
    paragraph_text: str,
    start: int,
    end: int,
):
    capture = _loaded_capture(
        target_id=target_id,
        url=url,
        digest_character=digest_character,
        paragraph_text=paragraph_text,
    )
    paragraph = select_chromium_research_capture_paragraph(capture, paragraph_ordinal=1)
    return select_chromium_research_paragraph_text(
        paragraph,
        start_offset=start,
        end_offset=end,
    )


def _note() -> ChromiumPageResearchParagraphTextSelectionComparisonNoteRecord:
    first = _range(
        target_id="page-a",
        url="https://example.test/a",
        digest_character="a",
        paragraph_text="SECRET-ALPHA evidence",
        start=0,
        end=6,
    )
    second = _range(
        target_id="page-b",
        url="https://example.test/b",
        digest_character="b",
        paragraph_text="SECRET-BETA evidence",
        start=0,
        end=6,
    )
    comparison = create_chromium_research_paragraph_text_selection_comparison(first, second)
    return create_chromium_research_paragraph_text_selection_comparison_note(
        comparison,
        note_text="  Human view: Δ differs?\nSecond line.  ",
    )


def _canonical_bytes(payload: object) -> bytes:
    return (
        json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
        + b"\n"
    )


def test_persist_and_verify_two_source_comparison_note_without_copying_source(
    tmp_path: Path,
) -> None:
    note = _note()
    destination = tmp_path / "comparison-note.json"

    persisted = persist_chromium_research_paragraph_text_selection_comparison_note(
        note,
        destination,
    )
    verified = verify_chromium_research_paragraph_text_selection_comparison_note(
        destination
    )

    assert isinstance(
        persisted,
        ChromiumPageResearchParagraphTextSelectionComparisonNotePersistenceEvidence,
    )
    assert persisted.note is note
    assert persisted.path == destination.resolve()
    assert persisted.note_format == (
        "pyxis.chromium.research_paragraph_text_selection_comparison_note.v1"
    )
    assert len(persisted.note_record_sha256) == 64
    assert persisted.byte_count == len(destination.read_bytes())

    assert isinstance(
        verified,
        ChromiumPageResearchParagraphTextSelectionComparisonNoteVerificationEvidence,
    )
    assert verified.note_record_sha256 == persisted.note_record_sha256
    assert verified.comparison_mode == "caller_explicit_exact_text_range_comparison"
    assert verified.first_source_bundle_sha256 == "a" * 64
    assert verified.second_source_bundle_sha256 == "b" * 64
    assert verified.first_paragraph_ordinal == 1
    assert verified.second_paragraph_ordinal == 1
    assert (verified.first_start_offset, verified.first_end_offset) == (0, 6)
    assert (verified.second_start_offset, verified.second_end_offset) == (0, 6)
    assert verified.first_offset_unit == "unicode_code_point"
    assert verified.second_offset_unit == "unicode_code_point"
    assert verified.note_text == note.note_text

    assert "SECRET-ALPHA" not in verified.document_json
    assert "SECRET-BETA" not in verified.document_json
    assert "https://example.test/a" not in verified.document_json
    assert "https://example.test/b" not in verified.document_json
    assert "/tmp/page-a.json" not in verified.document_json
    assert "/tmp/page-b.json" not in verified.document_json
    assert [field.name for field in fields(persisted)] == [
        "path",
        "note_format",
        "note_record_sha256",
        "byte_count",
        "note",
    ]

    with pytest.raises(FrozenInstanceError):
        persisted.byte_count = 0  # type: ignore[misc]


def test_persistence_is_deterministic_and_no_overwrite(tmp_path: Path) -> None:
    note = _note()
    first_path = tmp_path / "first.json"
    second_path = tmp_path / "second.json"

    first = persist_chromium_research_paragraph_text_selection_comparison_note(
        note, first_path
    )
    second = persist_chromium_research_paragraph_text_selection_comparison_note(
        note, second_path
    )

    assert first.note_record_sha256 == second.note_record_sha256
    assert first_path.read_bytes() == second_path.read_bytes()

    with pytest.raises(FileExistsError):
        persist_chromium_research_paragraph_text_selection_comparison_note(
            note, first_path
        )


def test_persistence_requires_existing_parent_and_live_19b_contract(
    tmp_path: Path,
) -> None:
    note = _note()

    with pytest.raises(FileNotFoundError, match="parent directory does not exist"):
        persist_chromium_research_paragraph_text_selection_comparison_note(
            note, tmp_path / "missing" / "note.json"
        )

    forged_second = replace(note.comparison.second_selection, end_offset=999)
    forged_comparison = replace(note.comparison, second_selection=forged_second)
    forged_note = replace(note, comparison=forged_comparison)

    with pytest.raises(ValueError, match="outside returned paragraph text evidence"):
        persist_chromium_research_paragraph_text_selection_comparison_note(
            forged_note, tmp_path / "forged.json"
        )

    with pytest.raises(TypeError, match="note must be"):
        persist_chromium_research_paragraph_text_selection_comparison_note(
            None,  # type: ignore[arg-type]
            tmp_path / "wrong.json",
        )


def test_verification_rejects_digest_tampering_and_noncanonical_bytes(
    tmp_path: Path,
) -> None:
    destination = tmp_path / "note.json"
    persist_chromium_research_paragraph_text_selection_comparison_note(
        _note(), destination
    )

    document = json.loads(destination.read_text(encoding="utf-8"))
    document["note_record"]["note"]["text"] = "changed"
    destination.write_bytes(_canonical_bytes(document))

    with pytest.raises(
        ChromiumResearchParagraphTextSelectionComparisonNoteIntegrityError,
        match="SHA-256 does not match",
    ):
        verify_chromium_research_paragraph_text_selection_comparison_note(destination)

    record = document["note_record"]
    document["note_record_sha256"] = hashlib.sha256(
        json.dumps(
            record,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    ).hexdigest()
    destination.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ChromiumResearchParagraphTextSelectionComparisonNoteIntegrityError,
        match="not in canonical Pyxis JSON encoding",
    ):
        verify_chromium_research_paragraph_text_selection_comparison_note(destination)


def test_file_valid_end_offset_999_remains_possible_until_explicit_relink(
    tmp_path: Path,
) -> None:
    destination = tmp_path / "note.json"
    persist_chromium_research_paragraph_text_selection_comparison_note(
        _note(), destination
    )

    document = json.loads(destination.read_text(encoding="utf-8"))
    record = document["note_record"]
    record["comparison"]["second"]["selection"]["text_range"]["end_offset"] = 999
    record_bytes = json.dumps(
        record,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    document["note_record_sha256"] = hashlib.sha256(record_bytes).hexdigest()
    destination.write_bytes(_canonical_bytes(document))

    verified = verify_chromium_research_paragraph_text_selection_comparison_note(
        destination
    )

    assert verified.second_end_offset == 999
    assert verified.note_record_sha256 == document["note_record_sha256"]


def test_verification_rejects_invalid_reference_domain_shapes(tmp_path: Path) -> None:
    destination = tmp_path / "note.json"
    persist_chromium_research_paragraph_text_selection_comparison_note(
        _note(), destination
    )
    original = json.loads(destination.read_text(encoding="utf-8"))

    cases = [
        (("comparison", "mode"), "other", "comparison mode is unsupported"),
        (
            ("comparison", "first", "source_capture", "bundle_sha256"),
            "not-a-digest",
            "first source bundle SHA-256",
        ),
        (
            ("comparison", "second", "selection", "text_range", "offset_unit"),
            "utf16_code_unit",
            "second offset unit is unsupported",
        ),
        (("note", "text"), "   ", "must contain non-whitespace"),
    ]

    for index, (path, value, message) in enumerate(cases):
        document = json.loads(json.dumps(original))
        cursor = document["note_record"]
        for key in path[:-1]:
            cursor = cursor[key]
        cursor[path[-1]] = value
        record = document["note_record"]
        record_bytes = json.dumps(
            record,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
        document["note_record_sha256"] = hashlib.sha256(record_bytes).hexdigest()
        candidate = tmp_path / f"invalid-{index}.json"
        candidate.write_bytes(_canonical_bytes(document))

        with pytest.raises(
            ChromiumResearchParagraphTextSelectionComparisonNoteIntegrityError,
            match=message,
        ):
            verify_chromium_research_paragraph_text_selection_comparison_note(candidate)


def test_same_selection_comparison_persists_without_significance_judgment(
    tmp_path: Path,
) -> None:
    selection = _range(
        target_id="same",
        url="https://example.test/same",
        digest_character="c",
        paragraph_text="Same source",
        start=0,
        end=4,
    )
    comparison = create_chromium_research_paragraph_text_selection_comparison(
        selection, selection
    )
    note = create_chromium_research_paragraph_text_selection_comparison_note(
        comparison,
        note_text="I intentionally compared this range with itself.",
    )
    destination = tmp_path / "same.json"

    persist_chromium_research_paragraph_text_selection_comparison_note(
        note, destination
    )
    verified = verify_chromium_research_paragraph_text_selection_comparison_note(
        destination
    )

    assert verified.first_source_bundle_sha256 == "c" * 64
    assert verified.second_source_bundle_sha256 == "c" * 64
    assert verified.first_start_offset == verified.second_start_offset == 0
    assert verified.first_end_offset == verified.second_end_offset == 4


def test_comparison_note_persistence_is_available_through_public_app_surface() -> None:
    from pyxis.app import (
        ChromiumPageResearchParagraphTextSelectionComparisonNotePersistenceEvidence as PublicPersistence,
    )
    from pyxis.app import (
        ChromiumPageResearchParagraphTextSelectionComparisonNoteVerificationEvidence as PublicVerification,
    )
    from pyxis.app import (
        ChromiumResearchParagraphTextSelectionComparisonNoteIntegrityError as PublicError,
    )
    from pyxis.app import (
        persist_chromium_research_paragraph_text_selection_comparison_note as public_persist,
    )
    from pyxis.app import (
        verify_chromium_research_paragraph_text_selection_comparison_note as public_verify,
    )

    assert PublicPersistence is (
        ChromiumPageResearchParagraphTextSelectionComparisonNotePersistenceEvidence
    )
    assert PublicVerification is (
        ChromiumPageResearchParagraphTextSelectionComparisonNoteVerificationEvidence
    )
    assert PublicError is ChromiumResearchParagraphTextSelectionComparisonNoteIntegrityError
    assert public_persist is persist_chromium_research_paragraph_text_selection_comparison_note
    assert public_verify is verify_chromium_research_paragraph_text_selection_comparison_note
