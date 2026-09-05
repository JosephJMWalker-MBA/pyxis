from __future__ import annotations

from dataclasses import replace
import hashlib
import json
from pathlib import Path

import pytest

from test_app_chromium_research_working_set import (
    _loaded_bare_selection,
    _loaded_records,
)
from pyxis.app.chromium_research_working_set import create_chromium_research_working_set
from pyxis.app.chromium_research_working_set_persistence import (
    ChromiumPageResearchWorkingSetPersistenceEvidence,
    ChromiumPageResearchWorkingSetVerificationEvidence,
    ChromiumResearchWorkingSetIntegrityError,
    persist_chromium_research_working_set,
    persist_chromium_research_working_set_v2,
    verify_chromium_research_working_set,
)


def _canonical_bytes(payload: object) -> bytes:
    return json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def _canonical_document_bytes(payload: object) -> bytes:
    return _canonical_bytes(payload) + b"\n"


def test_persist_working_set_records_only_ordered_member_identities(tmp_path: Path) -> None:
    paragraph_note, exact_note, comparison_note = _loaded_records(tmp_path)
    working_set = create_chromium_research_working_set(
        (exact_note, paragraph_note, comparison_note)
    )
    destination = tmp_path / "working-set.json"

    persisted = persist_chromium_research_working_set(working_set, destination)
    document = json.loads(destination.read_text(encoding="utf-8"))

    assert isinstance(persisted, ChromiumPageResearchWorkingSetPersistenceEvidence)
    assert persisted.working_set is working_set
    assert persisted.working_set_format == "pyxis.chromium.research_working_set.v1"
    assert document["working_set_record"]["working_set_mode"] == (
        "caller_explicit_ordered_relinked_research_working_set"
    )
    assert document["working_set_record"]["items"] == [
        {
            "member_kind": "exact_range_note",
            "member_format": "pyxis.chromium.research_paragraph_text_selection_note.v1",
            "member_record_sha256": exact_note.verification.note_record_sha256,
        },
        {
            "member_kind": "paragraph_note",
            "member_format": "pyxis.chromium.research_paragraph_note.v1",
            "member_record_sha256": paragraph_note.verification.note_record_sha256,
        },
        {
            "member_kind": "comparison_note",
            "member_format": (
                "pyxis.chromium.research_paragraph_text_selection_comparison_note.v1"
            ),
            "member_record_sha256": comparison_note.verification.note_record_sha256,
        },
    ]

    raw_text = destination.read_text(encoding="utf-8")
    assert paragraph_note.note.note_text not in raw_text
    assert exact_note.note.note_text not in raw_text
    assert comparison_note.note.note_text not in raw_text
    assert "source_bundle_sha256" not in raw_text
    assert "paragraph_ordinal" not in raw_text


def test_verify_working_set_preserves_order_and_duplicate_member_references(
    tmp_path: Path,
) -> None:
    _, _, comparison_note = _loaded_records(tmp_path)
    working_set = create_chromium_research_working_set(
        (comparison_note, comparison_note)
    )
    destination = tmp_path / "working-set.json"
    persist_chromium_research_working_set(working_set, destination)

    verified = verify_chromium_research_working_set(destination)

    assert isinstance(verified, ChromiumPageResearchWorkingSetVerificationEvidence)
    assert verified.working_set_mode == (
        "caller_explicit_ordered_relinked_research_working_set"
    )
    assert len(verified.items) == 2
    assert verified.items[0] == verified.items[1]
    assert verified.items[0].member_kind == "comparison_note"
    assert verified.items[0].member_record_sha256 == (
        comparison_note.verification.note_record_sha256
    )


def test_persist_working_set_does_not_reread_member_sidecars(tmp_path: Path) -> None:
    paragraph_note, exact_note, comparison_note = _loaded_records(tmp_path)
    working_set = create_chromium_research_working_set(
        (paragraph_note, exact_note, comparison_note)
    )

    paragraph_note.verification.path.unlink()
    exact_note.verification.path.unlink()
    comparison_note.verification.path.unlink()

    destination = tmp_path / "working-set.json"
    persisted = persist_chromium_research_working_set(working_set, destination)
    verified = verify_chromium_research_working_set(destination)

    assert persisted.path == destination.resolve()
    assert len(verified.items) == 3
    assert not paragraph_note.verification.path.exists()
    assert not exact_note.verification.path.exists()
    assert not comparison_note.verification.path.exists()


def test_persist_working_set_rejects_invalid_retained_member_digest(tmp_path: Path) -> None:
    paragraph_note, _, _ = _loaded_records(tmp_path)
    forged_note = replace(
        paragraph_note,
        verification=replace(
            paragraph_note.verification,
            note_record_sha256="not-a-sha256",
        ),
    )
    working_set = create_chromium_research_working_set((forged_note,))

    with pytest.raises(ValueError, match="retained member record SHA-256"):
        persist_chromium_research_working_set(
            working_set,
            tmp_path / "working-set.json",
        )


def test_verify_working_set_rejects_member_change_without_matching_digest(
    tmp_path: Path,
) -> None:
    paragraph_note, exact_note, _ = _loaded_records(tmp_path)
    working_set = create_chromium_research_working_set((paragraph_note, exact_note))
    destination = tmp_path / "working-set.json"
    persist_chromium_research_working_set(working_set, destination)

    document = json.loads(destination.read_text(encoding="utf-8"))
    document["working_set_record"]["items"][0]["member_record_sha256"] = "f" * 64
    destination.write_bytes(_canonical_document_bytes(document))

    with pytest.raises(ChromiumResearchWorkingSetIntegrityError, match="SHA-256"):
        verify_chromium_research_working_set(destination)


def test_verify_working_set_accepts_recomputed_self_consistent_wrong_member_identity(
    tmp_path: Path,
) -> None:
    paragraph_note, exact_note, _ = _loaded_records(tmp_path)
    working_set = create_chromium_research_working_set((paragraph_note, exact_note))
    destination = tmp_path / "working-set.json"
    persist_chromium_research_working_set(working_set, destination)

    document = json.loads(destination.read_text(encoding="utf-8"))
    document["working_set_record"]["items"][1]["member_record_sha256"] = "f" * 64
    record_bytes = _canonical_bytes(document["working_set_record"])
    document["working_set_record_sha256"] = hashlib.sha256(record_bytes).hexdigest()
    destination.write_bytes(_canonical_document_bytes(document))

    verified = verify_chromium_research_working_set(destination)

    assert verified.items[1].member_record_sha256 == "f" * 64
    assert verified.items[1].member_record_sha256 != (
        exact_note.verification.note_record_sha256
    )


def test_persist_working_set_is_no_overwrite(tmp_path: Path) -> None:
    paragraph_note, _, _ = _loaded_records(tmp_path)
    working_set = create_chromium_research_working_set((paragraph_note,))
    destination = tmp_path / "working-set.json"

    first = persist_chromium_research_working_set(working_set, destination)
    original = destination.read_bytes()

    with pytest.raises(FileExistsError):
        persist_chromium_research_working_set(working_set, destination)

    assert destination.read_bytes() == original
    assert first.byte_count == len(original)


def test_working_set_persistence_module_is_publicly_importable(tmp_path: Path) -> None:
    paragraph_note, _, _ = _loaded_records(tmp_path)
    working_set = create_chromium_research_working_set((paragraph_note,))
    destination = tmp_path / "working-set.json"

    persisted = persist_chromium_research_working_set(working_set, destination)
    verified = verify_chromium_research_working_set(destination)

    assert persisted.working_set is working_set
    assert verified.items[0].member_format == "pyxis.chromium.research_paragraph_note.v1"


def test_49c_existing_v1_persistence_rejects_bare_selection_member_without_write(
    tmp_path: Path,
) -> None:
    bare, _ = _loaded_bare_selection(tmp_path)
    working_set = create_chromium_research_working_set((bare,))
    destination = tmp_path / "working-set-v1-must-not-widen.json"

    with pytest.raises(
        TypeError,
        match=r"working_set\.items\[0\] has an unsupported member family",
    ):
        persist_chromium_research_working_set(
            working_set,
            destination,
        )

    assert not destination.exists()


def test_49d_v2_persists_mixed_bare_and_note_members_without_copying_payloads(
    tmp_path: Path,
) -> None:
    paragraph_note, exact_note, comparison_note = _loaded_records(tmp_path)
    bare, _ = _loaded_bare_selection(tmp_path)
    working_set = create_chromium_research_working_set(
        (bare, paragraph_note, bare, exact_note, comparison_note)
    )
    destination = tmp_path / "working-set-v2.json"

    persisted = persist_chromium_research_working_set_v2(
        working_set,
        destination,
    )
    verified = verify_chromium_research_working_set(destination)
    document = json.loads(destination.read_text(encoding="utf-8"))

    assert persisted.working_set is working_set
    assert persisted.working_set_format == "pyxis.chromium.research_working_set.v2"
    assert verified.working_set_format == persisted.working_set_format
    assert [item.member_kind for item in verified.items] == [
        "exact_range_selection",
        "paragraph_note",
        "exact_range_selection",
        "exact_range_note",
        "comparison_note",
    ]
    assert verified.items[0].member_format == (
        "pyxis.chromium.research_paragraph_text_selection.v1"
    )
    assert verified.items[0].member_record_sha256 == (
        bare.verification.selection_record_sha256
    )
    assert verified.items[0] == verified.items[2]

    raw = destination.read_text(encoding="utf-8")
    assert bare.selection.selected_text not in raw
    assert paragraph_note.note.note_text not in raw
    assert exact_note.note.note_text not in raw
    assert comparison_note.note.note_text not in raw
    assert "source_bundle_sha256" not in raw
    assert "paragraph_ordinal" not in raw
    assert str(bare.verification.path) not in raw
    assert document["format"] == "pyxis.chromium.research_working_set.v2"


def test_49d_v1_file_cannot_smuggle_v2_bare_selection_kind(
    tmp_path: Path,
) -> None:
    paragraph_note, _, _ = _loaded_records(tmp_path)
    working_set = create_chromium_research_working_set((paragraph_note,))
    destination = tmp_path / "working-set-v1.json"
    persist_chromium_research_working_set(working_set, destination)

    document = json.loads(destination.read_text(encoding="utf-8"))
    record = document["working_set_record"]
    record["items"][0] = {
        "member_kind": "exact_range_selection",
        "member_format": "pyxis.chromium.research_paragraph_text_selection.v1",
        "member_record_sha256": "a" * 64,
    }
    document["working_set_record_sha256"] = hashlib.sha256(
        _canonical_bytes(record)
    ).hexdigest()
    destination.write_bytes(_canonical_document_bytes(document))

    with pytest.raises(
        ChromiumResearchWorkingSetIntegrityError,
        match="unsupported member kind",
    ):
        verify_chromium_research_working_set(destination)


def test_49d_v2_rejects_wrong_bare_member_format_even_with_matching_file_digest(
    tmp_path: Path,
) -> None:
    bare, _ = _loaded_bare_selection(tmp_path)
    working_set = create_chromium_research_working_set((bare,))
    destination = tmp_path / "working-set-v2.json"
    persist_chromium_research_working_set_v2(working_set, destination)

    document = json.loads(destination.read_text(encoding="utf-8"))
    record = document["working_set_record"]
    record["items"][0]["member_format"] = (
        "pyxis.chromium.research_paragraph_text_selection_note.v1"
    )
    document["working_set_record_sha256"] = hashlib.sha256(
        _canonical_bytes(record)
    ).hexdigest()
    destination.write_bytes(_canonical_document_bytes(document))

    with pytest.raises(
        ChromiumResearchWorkingSetIntegrityError,
        match="unsupported member format",
    ):
        verify_chromium_research_working_set(destination)


def test_49d_v2_is_deterministic_and_no_overwrite(
    tmp_path: Path,
) -> None:
    bare, _ = _loaded_bare_selection(tmp_path)
    working_set = create_chromium_research_working_set((bare, bare))
    first_path = tmp_path / "working-set-v2-a.json"
    second_path = tmp_path / "working-set-v2-b.json"

    first = persist_chromium_research_working_set_v2(
        working_set,
        first_path,
    )
    second = persist_chromium_research_working_set_v2(
        working_set,
        second_path,
    )

    assert first.working_set_record_sha256 == second.working_set_record_sha256
    assert first_path.read_bytes() == second_path.read_bytes()

    original = first_path.read_bytes()
    with pytest.raises(FileExistsError):
        persist_chromium_research_working_set_v2(
            working_set,
            first_path,
        )
    assert first_path.read_bytes() == original


def test_49d_generic_verifier_preserves_v1_and_v2_format_identity(
    tmp_path: Path,
) -> None:
    paragraph_note, _, _ = _loaded_records(tmp_path)
    bare, _ = _loaded_bare_selection(tmp_path)

    v1_set = create_chromium_research_working_set((paragraph_note,))
    v1_path = tmp_path / "working-set-v1.json"
    persist_chromium_research_working_set(v1_set, v1_path)

    v2_set = create_chromium_research_working_set((bare,))
    v2_path = tmp_path / "working-set-v2.json"
    persist_chromium_research_working_set_v2(v2_set, v2_path)

    assert (
        verify_chromium_research_working_set(v1_path).working_set_format
        == "pyxis.chromium.research_working_set.v1"
    )
    assert (
        verify_chromium_research_working_set(v2_path).working_set_format
        == "pyxis.chromium.research_working_set.v2"
    )
