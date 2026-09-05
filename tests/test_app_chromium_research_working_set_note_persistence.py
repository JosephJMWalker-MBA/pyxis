from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from test_app_chromium_research_working_set import (
    _loaded_bare_selection,
    _loaded_records,
)
from pyxis.app.chromium_research_working_set import create_chromium_research_working_set
from pyxis.app.chromium_research_working_set_load import (
    ChromiumResearchWorkingSetMemberMismatchError,
)
from pyxis.app.chromium_research_working_set_note import (
    create_chromium_research_working_set_note,
)
from pyxis.app.chromium_research_working_set_note_persistence import (
    ChromiumPageResearchWorkingSetNotePersistenceEvidence,
    ChromiumPageResearchWorkingSetNoteVerificationEvidence,
    ChromiumResearchWorkingSetNoteIntegrityError,
    persist_chromium_research_working_set_note,
    verify_chromium_research_working_set_note,
)
from pyxis.app.chromium_research_working_set_persistence import (
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


def test_persist_working_set_note_records_only_parent_identity_and_human_note(
    tmp_path: Path,
) -> None:
    paragraph_note, exact_note, comparison_note = _loaded_records(tmp_path)
    working_set = create_chromium_research_working_set(
        (paragraph_note, exact_note, comparison_note)
    )
    working_set_path = tmp_path / "working-set.json"
    working_set_persisted = persist_chromium_research_working_set(
        working_set,
        working_set_path,
    )
    note_text = "  Carry these together while I test the failure hypothesis 😀\nDo not resolve it yet.  "
    note = create_chromium_research_working_set_note(
        working_set,
        note_text=note_text,
    )
    destination = tmp_path / "working-set-note.json"

    persisted = persist_chromium_research_working_set_note(
        note,
        working_set_path,
        destination,
    )
    verified = verify_chromium_research_working_set_note(destination)
    document = json.loads(destination.read_text(encoding="utf-8"))

    assert isinstance(persisted, ChromiumPageResearchWorkingSetNotePersistenceEvidence)
    assert isinstance(verified, ChromiumPageResearchWorkingSetNoteVerificationEvidence)
    assert persisted.note is note
    assert persisted.note_format == "pyxis.chromium.research_working_set_note.v1"
    assert verified.note_text == note_text
    assert verified.note_mode == "caller_authored_note_on_research_working_set"
    assert verified.working_set_format == "pyxis.chromium.research_working_set.v1"
    assert verified.working_set_record_sha256 == (
        working_set_persisted.working_set_record_sha256
    )
    assert document["note_record"] == {
        "note": {
            "mode": "caller_authored_note_on_research_working_set",
            "text": note_text,
        },
        "working_set_reference": {
            "format": "pyxis.chromium.research_working_set.v1",
            "working_set_record_sha256": working_set_persisted.working_set_record_sha256,
        },
    }

    raw_text = destination.read_text(encoding="utf-8")
    assert "member_kind" not in raw_text
    assert "paragraph_ordinal" not in raw_text
    assert "source_bundle_sha256" not in raw_text
    assert str(working_set_path.resolve()) not in raw_text


def test_persist_working_set_note_uses_durable_parent_identity_not_parent_path(
    tmp_path: Path,
) -> None:
    paragraph_note, exact_note, _ = _loaded_records(tmp_path)
    working_set = create_chromium_research_working_set((paragraph_note, exact_note))
    original_path = tmp_path / "working-set.json"
    persist_chromium_research_working_set(working_set, original_path)
    moved_path = tmp_path / "moved-working-set.json"
    original_path.replace(moved_path)
    expected = verify_chromium_research_working_set(moved_path)
    note = create_chromium_research_working_set_note(
        working_set,
        note_text="The path moved; the durable parent content did not.",
    )
    destination = tmp_path / "working-set-note.json"

    persist_chromium_research_working_set_note(note, moved_path, destination)
    verified = verify_chromium_research_working_set_note(destination)

    assert verified.working_set_record_sha256 == expected.working_set_record_sha256
    assert str(original_path.resolve()) not in verified.document_json
    assert str(moved_path.resolve()) not in verified.document_json


def test_persist_working_set_note_rejects_different_durable_parent(
    tmp_path: Path,
) -> None:
    paragraph_note, exact_note, _ = _loaded_records(tmp_path)
    intended = create_chromium_research_working_set((paragraph_note,))
    different = create_chromium_research_working_set((exact_note,))
    different_path = tmp_path / "different-working-set.json"
    persist_chromium_research_working_set(different, different_path)
    note = create_chromium_research_working_set_note(
        intended,
        note_text="This rationale belongs to the paragraph-note set.",
    )
    destination = tmp_path / "working-set-note.json"

    with pytest.raises(
        ChromiumResearchWorkingSetMemberMismatchError,
        match="item 0 references a different member kind",
    ):
        persist_chromium_research_working_set_note(
            note,
            different_path,
            destination,
        )

    assert not destination.exists()


def test_persist_working_set_note_does_not_reread_individual_member_sidecars(
    tmp_path: Path,
) -> None:
    paragraph_note, exact_note, comparison_note = _loaded_records(tmp_path)
    working_set = create_chromium_research_working_set(
        (paragraph_note, exact_note, comparison_note)
    )
    working_set_path = tmp_path / "working-set.json"
    persist_chromium_research_working_set(working_set, working_set_path)
    note = create_chromium_research_working_set_note(
        working_set,
        note_text="The working-set parent remains durable even if member files move.",
    )

    paragraph_note.verification.path.unlink()
    exact_note.verification.path.unlink()
    comparison_note.verification.path.unlink()

    destination = tmp_path / "working-set-note.json"
    persisted = persist_chromium_research_working_set_note(
        note,
        working_set_path,
        destination,
    )

    assert persisted.note is note
    assert destination.exists()
    assert not paragraph_note.verification.path.exists()
    assert not exact_note.verification.path.exists()
    assert not comparison_note.verification.path.exists()


def test_verify_working_set_note_rejects_change_without_matching_digest(
    tmp_path: Path,
) -> None:
    paragraph_note, _, _ = _loaded_records(tmp_path)
    working_set = create_chromium_research_working_set((paragraph_note,))
    working_set_path = tmp_path / "working-set.json"
    persist_chromium_research_working_set(working_set, working_set_path)
    note = create_chromium_research_working_set_note(
        working_set,
        note_text="Original rationale.",
    )
    destination = tmp_path / "working-set-note.json"
    persist_chromium_research_working_set_note(note, working_set_path, destination)

    document = json.loads(destination.read_text(encoding="utf-8"))
    document["note_record"]["working_set_reference"]["working_set_record_sha256"] = (
        "f" * 64
    )
    destination.write_bytes(_canonical_document_bytes(document))

    with pytest.raises(ChromiumResearchWorkingSetNoteIntegrityError, match="SHA-256"):
        verify_chromium_research_working_set_note(destination)


def test_verify_working_set_note_accepts_recomputed_self_consistent_wrong_parent_identity(
    tmp_path: Path,
) -> None:
    paragraph_note, _, _ = _loaded_records(tmp_path)
    working_set = create_chromium_research_working_set((paragraph_note,))
    working_set_path = tmp_path / "working-set.json"
    working_set_persisted = persist_chromium_research_working_set(
        working_set,
        working_set_path,
    )
    note = create_chromium_research_working_set_note(
        working_set,
        note_text="Parent identity correctness is earned later.",
    )
    destination = tmp_path / "working-set-note.json"
    persist_chromium_research_working_set_note(note, working_set_path, destination)

    document = json.loads(destination.read_text(encoding="utf-8"))
    wrong_digest = "f" * 64
    assert wrong_digest != working_set_persisted.working_set_record_sha256
    document["note_record"]["working_set_reference"]["working_set_record_sha256"] = (
        wrong_digest
    )
    document["note_record_sha256"] = hashlib.sha256(
        _canonical_bytes(document["note_record"])
    ).hexdigest()
    destination.write_bytes(_canonical_document_bytes(document))

    verified = verify_chromium_research_working_set_note(destination)

    assert verified.working_set_record_sha256 == wrong_digest
    assert verified.working_set_record_sha256 != (
        working_set_persisted.working_set_record_sha256
    )


def test_persist_working_set_note_is_deterministic_and_no_overwrite(
    tmp_path: Path,
) -> None:
    paragraph_note, _, _ = _loaded_records(tmp_path)
    working_set = create_chromium_research_working_set((paragraph_note,))
    working_set_path = tmp_path / "working-set.json"
    persist_chromium_research_working_set(working_set, working_set_path)
    note = create_chromium_research_working_set_note(
        working_set,
        note_text="Exact same rationale.",
    )
    first_path = tmp_path / "working-set-note-a.json"
    second_path = tmp_path / "working-set-note-b.json"

    first = persist_chromium_research_working_set_note(
        note,
        working_set_path,
        first_path,
    )
    second = persist_chromium_research_working_set_note(
        note,
        working_set_path,
        second_path,
    )

    assert first.note_record_sha256 == second.note_record_sha256
    assert first_path.read_bytes() == second_path.read_bytes()

    original = first_path.read_bytes()
    with pytest.raises(FileExistsError):
        persist_chromium_research_working_set_note(
            note,
            working_set_path,
            first_path,
        )
    assert first_path.read_bytes() == original


def test_working_set_note_persistence_module_is_publicly_importable(
    tmp_path: Path,
) -> None:
    paragraph_note, _, _ = _loaded_records(tmp_path)
    working_set = create_chromium_research_working_set((paragraph_note,))
    working_set_path = tmp_path / "working-set.json"
    persist_chromium_research_working_set(working_set, working_set_path)
    note = create_chromium_research_working_set_note(
        working_set,
        note_text="Human rationale only.",
    )
    destination = tmp_path / "working-set-note.json"

    persisted = persist_chromium_research_working_set_note(
        note,
        working_set_path,
        destination,
    )
    verified = verify_chromium_research_working_set_note(destination)

    assert persisted.note is note
    assert verified.note_text == "Human rationale only."


def test_49d_working_set_note_v1_parent_contract_rejects_v2_working_set(
    tmp_path: Path,
) -> None:
    bare, _ = _loaded_bare_selection(tmp_path)
    working_set = create_chromium_research_working_set((bare,))
    working_set_path = tmp_path / "working-set-v2.json"
    persist_chromium_research_working_set_v2(
        working_set,
        working_set_path,
    )
    note = create_chromium_research_working_set_note(
        working_set,
        note_text="Overall rationale is a later durable boundary.",
    )
    destination = tmp_path / "working-set-note-must-not-write.json"

    with pytest.raises(
        ValueError,
        match="working-set format is unsupported for note persistence",
    ):
        persist_chromium_research_working_set_note(
            note,
            working_set_path,
            destination,
        )

    assert not destination.exists()
