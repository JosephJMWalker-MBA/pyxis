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
from pyxis.app.chromium_research_working_set_note_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRecord,
    ChromiumResearchWorkingSetNoteParentMismatchError,
    load_chromium_research_working_set_note,
)
from pyxis.app.chromium_research_working_set_note_persistence import (
    ChromiumResearchWorkingSetNoteIntegrityError,
    persist_chromium_research_working_set_note,
    persist_chromium_research_working_set_note_v2,
    verify_chromium_research_working_set_note,
)
from pyxis.app.chromium_research_working_set_persistence import (
    persist_chromium_research_working_set,
    persist_chromium_research_working_set_v2,
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


def _persist_note(
    tmp_path: Path,
    items: tuple[object, ...],
    *,
    note_text: str = "  Keep these together while I test the failure hypothesis 😀\nDo not resolve it yet.  ",
) -> tuple[Path, Path]:
    working_set = create_chromium_research_working_set(items)  # type: ignore[arg-type]
    working_set_path = tmp_path / "working-set.json"
    persist_chromium_research_working_set(working_set, working_set_path)
    note = create_chromium_research_working_set_note(
        working_set,
        note_text=note_text,
    )
    note_path = tmp_path / "working-set-note.json"
    persist_chromium_research_working_set_note(
        note,
        working_set_path,
        note_path,
    )
    return working_set_path, note_path


def _persist_note_v2(
    tmp_path: Path,
    items: tuple[object, ...],
    *,
    note_text: str = "  Human rationale over the v2 working set 😀\nKeep exact.  ",
) -> tuple[Path, Path]:
    working_set = create_chromium_research_working_set(items)  # type: ignore[arg-type]
    working_set_path = tmp_path / "working-set-v2.json"
    persist_chromium_research_working_set_v2(
        working_set,
        working_set_path,
    )
    note = create_chromium_research_working_set_note(
        working_set,
        note_text=note_text,
    )
    note_path = tmp_path / "working-set-note-v2.json"
    persist_chromium_research_working_set_note_v2(
        note,
        working_set_path,
        note_path,
    )
    return working_set_path, note_path


def test_load_working_set_note_relinks_moved_files_and_retains_exact_members(
    tmp_path: Path,
) -> None:
    paragraph_note, exact_note, comparison_note = _loaded_records(tmp_path)
    items = (paragraph_note, exact_note, comparison_note)
    note_text = "  Why these three travel together 😀\nLeave the question open.  "
    working_set_path, note_path = _persist_note(
        tmp_path,
        items,
        note_text=note_text,
    )
    moved_working_set = tmp_path / "moved-working-set.json"
    moved_note = tmp_path / "moved-working-set-note.json"
    working_set_path.replace(moved_working_set)
    note_path.replace(moved_note)

    loaded = load_chromium_research_working_set_note(
        items,
        moved_working_set,
        moved_note,
    )

    assert isinstance(loaded, ChromiumPageResearchLoadedWorkingSetNoteRecord)
    assert loaded.verification.path == moved_note.resolve()
    assert loaded.working_set.verification.path == moved_working_set.resolve()
    assert loaded.note.working_set is loaded.working_set.working_set
    assert loaded.note.note_text == note_text
    assert loaded.note.working_set.items[0] is paragraph_note
    assert loaded.note.working_set.items[1] is exact_note
    assert loaded.note.working_set.items[2] is comparison_note
    assert loaded.verification.working_set_record_sha256 == (
        loaded.working_set.verification.working_set_record_sha256
    )


def test_load_working_set_note_rejects_different_valid_durable_parent(
    tmp_path: Path,
) -> None:
    paragraph_note, exact_note, _ = _loaded_records(tmp_path)
    intended = create_chromium_research_working_set((paragraph_note,))
    intended_path = tmp_path / "intended-working-set.json"
    persist_chromium_research_working_set(intended, intended_path)
    note = create_chromium_research_working_set_note(
        intended,
        note_text="This belongs only to the paragraph-note working set.",
    )
    note_path = tmp_path / "working-set-note.json"
    persist_chromium_research_working_set_note(note, intended_path, note_path)

    different = create_chromium_research_working_set((exact_note,))
    different_path = tmp_path / "different-working-set.json"
    persist_chromium_research_working_set(different, different_path)

    with pytest.raises(
        ChromiumResearchWorkingSetNoteParentMismatchError,
        match="different working-set record",
    ):
        load_chromium_research_working_set_note(
            (exact_note,),
            different_path,
            note_path,
        )


def test_load_working_set_note_rejects_recomputed_21b_valid_wrong_parent_digest(
    tmp_path: Path,
) -> None:
    paragraph_note, _, _ = _loaded_records(tmp_path)
    working_set_path, note_path = _persist_note(tmp_path, (paragraph_note,))

    document = json.loads(note_path.read_text(encoding="utf-8"))
    wrong_digest = "f" * 64
    document["note_record"]["working_set_reference"]["working_set_record_sha256"] = (
        wrong_digest
    )
    document["note_record_sha256"] = hashlib.sha256(
        _canonical_bytes(document["note_record"])
    ).hexdigest()
    note_path.write_bytes(_canonical_document_bytes(document))

    verified = verify_chromium_research_working_set_note(note_path)
    assert verified.working_set_record_sha256 == wrong_digest

    with pytest.raises(
        ChromiumResearchWorkingSetNoteParentMismatchError,
        match="different working-set record",
    ):
        load_chromium_research_working_set_note(
            (paragraph_note,),
            working_set_path,
            note_path,
        )


def test_load_working_set_note_freshly_verifies_note_sidecar(tmp_path: Path) -> None:
    paragraph_note, _, _ = _loaded_records(tmp_path)
    working_set_path, note_path = _persist_note(tmp_path, (paragraph_note,))

    document = json.loads(note_path.read_text(encoding="utf-8"))
    document["note_record"]["note"]["text"] = "Tampered rationale."
    note_path.write_bytes(_canonical_document_bytes(document))

    with pytest.raises(ChromiumResearchWorkingSetNoteIntegrityError, match="SHA-256"):
        load_chromium_research_working_set_note(
            (paragraph_note,),
            working_set_path,
            note_path,
        )


def test_load_working_set_note_does_not_reread_individual_member_sidecars(
    tmp_path: Path,
) -> None:
    paragraph_note, exact_note, comparison_note = _loaded_records(tmp_path)
    items = (paragraph_note, exact_note, comparison_note)
    working_set_path, note_path = _persist_note(tmp_path, items)

    paragraph_note.verification.path.unlink()
    exact_note.verification.path.unlink()
    comparison_note.verification.path.unlink()

    loaded = load_chromium_research_working_set_note(
        items,
        working_set_path,
        note_path,
    )

    assert loaded.note.working_set is loaded.working_set.working_set
    assert not paragraph_note.verification.path.exists()
    assert not exact_note.verification.path.exists()
    assert not comparison_note.verification.path.exists()


def test_load_working_set_note_preserves_20c_order_authority(tmp_path: Path) -> None:
    paragraph_note, exact_note, _ = _loaded_records(tmp_path)
    working_set_path, note_path = _persist_note(
        tmp_path,
        (paragraph_note, exact_note),
    )

    with pytest.raises(
        ChromiumResearchWorkingSetMemberMismatchError,
        match="item 0 references a different member kind",
    ):
        load_chromium_research_working_set_note(
            (exact_note, paragraph_note),
            working_set_path,
            note_path,
        )


def test_load_working_set_note_requires_complete_member_sequence(tmp_path: Path) -> None:
    paragraph_note, exact_note, comparison_note = _loaded_records(tmp_path)
    working_set_path, note_path = _persist_note(
        tmp_path,
        (paragraph_note, exact_note),
    )

    with pytest.raises(
        ChromiumResearchWorkingSetMemberMismatchError,
        match="member count does not match",
    ):
        load_chromium_research_working_set_note(
            (paragraph_note,),
            working_set_path,
            note_path,
        )

    with pytest.raises(
        ChromiumResearchWorkingSetMemberMismatchError,
        match="member count does not match",
    ):
        load_chromium_research_working_set_note(
            (paragraph_note, exact_note, comparison_note),
            working_set_path,
            note_path,
        )


def test_working_set_note_load_module_is_publicly_importable(tmp_path: Path) -> None:
    paragraph_note, _, _ = _loaded_records(tmp_path)
    working_set_path, note_path = _persist_note(
        tmp_path,
        (paragraph_note,),
        note_text="Human rationale restored only after explicit parent relinking.",
    )

    loaded = load_chromium_research_working_set_note(
        (paragraph_note,),
        working_set_path,
        note_path,
    )

    assert loaded.note.note_text == (
        "Human rationale restored only after explicit parent relinking."
    )
    assert loaded.note.working_set is loaded.working_set.working_set


def test_49e_load_v2_note_relinks_exact_v2_parent_and_bare_members(
    tmp_path: Path,
) -> None:
    paragraph_note, _, _ = _loaded_records(tmp_path)
    bare, _ = _loaded_bare_selection(tmp_path)
    items = (bare, paragraph_note, bare)
    note_text = "  Overall human rationale for these exact passages 😀\nStill tentative.  "
    working_set_path, note_path = _persist_note_v2(
        tmp_path,
        items,
        note_text=note_text,
    )

    loaded = load_chromium_research_working_set_note(
        items,
        working_set_path,
        note_path,
    )

    assert loaded.verification.note_format == (
        "pyxis.chromium.research_working_set_note.v2"
    )
    assert loaded.verification.working_set_format == (
        "pyxis.chromium.research_working_set.v2"
    )
    assert loaded.working_set.verification.working_set_format == (
        "pyxis.chromium.research_working_set.v2"
    )
    assert loaded.note.note_text == note_text
    assert loaded.note.working_set is loaded.working_set.working_set
    assert loaded.note.working_set.items[0] is bare
    assert loaded.note.working_set.items[1] is paragraph_note
    assert loaded.note.working_set.items[2] is bare


def test_49e_load_v2_note_rejects_file_valid_wrong_parent_digest(
    tmp_path: Path,
) -> None:
    bare, _ = _loaded_bare_selection(tmp_path)
    working_set_path, note_path = _persist_note_v2(
        tmp_path,
        (bare,),
    )

    document = json.loads(note_path.read_text(encoding="utf-8"))
    wrong_digest = "f" * 64
    document["note_record"]["working_set_reference"]["working_set_record_sha256"] = (
        wrong_digest
    )
    document["note_record_sha256"] = hashlib.sha256(
        _canonical_bytes(document["note_record"])
    ).hexdigest()
    note_path.write_bytes(_canonical_document_bytes(document))

    verified = verify_chromium_research_working_set_note(note_path)
    assert verified.note_format == "pyxis.chromium.research_working_set_note.v2"
    assert verified.working_set_record_sha256 == wrong_digest

    with pytest.raises(
        ChromiumResearchWorkingSetNoteParentMismatchError,
        match="different working-set record",
    ):
        load_chromium_research_working_set_note(
            (bare,),
            working_set_path,
            note_path,
        )


def test_49e_load_v2_note_does_not_reread_member_sidecars(
    tmp_path: Path,
) -> None:
    paragraph_note, _, _ = _loaded_records(tmp_path)
    bare, bare_path = _loaded_bare_selection(tmp_path)
    items = (paragraph_note, bare)
    working_set_path, note_path = _persist_note_v2(tmp_path, items)

    paragraph_note.verification.path.unlink()
    bare_path.unlink()

    loaded = load_chromium_research_working_set_note(
        items,
        working_set_path,
        note_path,
    )

    assert loaded.note.working_set.items[0] is paragraph_note
    assert loaded.note.working_set.items[1] is bare
    assert not paragraph_note.verification.path.exists()
    assert not bare.verification.path.exists()


def test_49e_load_note_rejects_cross_version_parent_file(
    tmp_path: Path,
) -> None:
    paragraph_note, _, _ = _loaded_records(tmp_path)
    bare, _ = _loaded_bare_selection(tmp_path)

    v1_working_set_path, v1_note_path = _persist_note(
        tmp_path,
        (paragraph_note,),
    )
    v2_set = create_chromium_research_working_set((bare,))
    v2_working_set_path = tmp_path / "other-working-set-v2.json"
    persist_chromium_research_working_set_v2(
        v2_set,
        v2_working_set_path,
    )

    with pytest.raises(
        ChromiumResearchWorkingSetNoteParentMismatchError,
        match="different parent format",
    ):
        load_chromium_research_working_set_note(
            (bare,),
            v2_working_set_path,
            v1_note_path,
        )

    assert v1_working_set_path.exists()
