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
from pyxis.app.chromium_research_working_set_load import (
    ChromiumPageResearchLoadedWorkingSetRecord,
    ChromiumResearchWorkingSetMemberMismatchError,
    load_chromium_research_working_set,
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


def test_load_working_set_relinks_exact_ordered_supplied_members(tmp_path: Path) -> None:
    paragraph_note, exact_note, comparison_note = _loaded_records(tmp_path)
    original = create_chromium_research_working_set(
        (exact_note, paragraph_note, comparison_note)
    )
    original_path = tmp_path / "working-set.json"
    persist_chromium_research_working_set(original, original_path)
    moved_path = tmp_path / "moved-working-set.json"
    original_path.replace(moved_path)

    loaded = load_chromium_research_working_set(
        (exact_note, paragraph_note, comparison_note),
        moved_path,
    )

    assert isinstance(loaded, ChromiumPageResearchLoadedWorkingSetRecord)
    assert loaded.verification.path == moved_path.resolve()
    assert loaded.working_set is not original
    assert loaded.working_set.items[0] is exact_note
    assert loaded.working_set.items[1] is paragraph_note
    assert loaded.working_set.items[2] is comparison_note
    assert loaded.working_set.working_set_mode == loaded.verification.working_set_mode


def test_load_working_set_preserves_intentional_duplicate_positions(tmp_path: Path) -> None:
    _, _, comparison_note = _loaded_records(tmp_path)
    original = create_chromium_research_working_set(
        (comparison_note, comparison_note)
    )
    path = tmp_path / "working-set.json"
    persist_chromium_research_working_set(original, path)

    loaded = load_chromium_research_working_set(
        (comparison_note, comparison_note),
        path,
    )

    assert len(loaded.working_set.items) == 2
    assert loaded.working_set.items[0] is comparison_note
    assert loaded.working_set.items[1] is comparison_note


def test_load_working_set_does_not_reread_individual_member_sidecars(tmp_path: Path) -> None:
    paragraph_note, exact_note, comparison_note = _loaded_records(tmp_path)
    original = create_chromium_research_working_set(
        (paragraph_note, exact_note, comparison_note)
    )
    path = tmp_path / "working-set.json"
    persist_chromium_research_working_set(original, path)

    paragraph_note.verification.path.unlink()
    exact_note.verification.path.unlink()
    comparison_note.verification.path.unlink()

    loaded = load_chromium_research_working_set(
        (paragraph_note, exact_note, comparison_note),
        path,
    )

    assert loaded.working_set.items == (paragraph_note, exact_note, comparison_note)
    assert not paragraph_note.verification.path.exists()
    assert not exact_note.verification.path.exists()
    assert not comparison_note.verification.path.exists()


def test_load_working_set_rejects_same_members_in_different_order(tmp_path: Path) -> None:
    paragraph_note, exact_note, comparison_note = _loaded_records(tmp_path)
    original = create_chromium_research_working_set(
        (paragraph_note, exact_note, comparison_note)
    )
    path = tmp_path / "working-set.json"
    persist_chromium_research_working_set(original, path)

    with pytest.raises(
        ChromiumResearchWorkingSetMemberMismatchError,
        match="item 0 references a different member kind",
    ):
        load_chromium_research_working_set(
            (exact_note, paragraph_note, comparison_note),
            path,
        )


def test_load_working_set_rejects_recomputed_file_valid_wrong_member_digest(
    tmp_path: Path,
) -> None:
    paragraph_note, exact_note, _ = _loaded_records(tmp_path)
    original = create_chromium_research_working_set((paragraph_note, exact_note))
    path = tmp_path / "working-set.json"
    persist_chromium_research_working_set(original, path)

    document = json.loads(path.read_text(encoding="utf-8"))
    wrong_digest = "f" * 64
    assert wrong_digest != exact_note.verification.note_record_sha256
    document["working_set_record"]["items"][1]["member_record_sha256"] = wrong_digest
    document["working_set_record_sha256"] = hashlib.sha256(
        _canonical_bytes(document["working_set_record"])
    ).hexdigest()
    path.write_bytes(_canonical_document_bytes(document))

    verified = verify_chromium_research_working_set(path)
    assert verified.items[1].member_record_sha256 == wrong_digest

    with pytest.raises(
        ChromiumResearchWorkingSetMemberMismatchError,
        match="item 1 references a different member record",
    ):
        load_chromium_research_working_set((paragraph_note, exact_note), path)


def test_load_working_set_rejects_missing_or_extra_supplied_members(tmp_path: Path) -> None:
    paragraph_note, exact_note, comparison_note = _loaded_records(tmp_path)
    original = create_chromium_research_working_set((paragraph_note, exact_note))
    path = tmp_path / "working-set.json"
    persist_chromium_research_working_set(original, path)

    with pytest.raises(
        ChromiumResearchWorkingSetMemberMismatchError,
        match="member count does not match",
    ):
        load_chromium_research_working_set((paragraph_note,), path)

    with pytest.raises(
        ChromiumResearchWorkingSetMemberMismatchError,
        match="member count does not match",
    ):
        load_chromium_research_working_set(
            (paragraph_note, exact_note, comparison_note),
            path,
        )


def test_load_working_set_reestablishes_20a_in_memory_coherence(tmp_path: Path) -> None:
    paragraph_note, _, _ = _loaded_records(tmp_path)
    original = create_chromium_research_working_set((paragraph_note,))
    path = tmp_path / "working-set.json"
    persist_chromium_research_working_set(original, path)

    forged = replace(
        paragraph_note,
        verification=replace(
            paragraph_note.verification,
            note_text="Different retained verification text",
        ),
    )

    with pytest.raises(
        ValueError,
        match=r"items\[0\] paragraph-note verification is incoherent",
    ):
        load_chromium_research_working_set((forged,), path)


def test_working_set_load_module_is_publicly_importable(tmp_path: Path) -> None:
    paragraph_note, _, _ = _loaded_records(tmp_path)
    original = create_chromium_research_working_set((paragraph_note,))
    path = tmp_path / "working-set.json"
    persist_chromium_research_working_set(original, path)

    loaded = load_chromium_research_working_set((paragraph_note,), path)

    assert loaded.verification.working_set_record_sha256
    assert loaded.working_set.items[0] is paragraph_note


def test_49d_load_v2_relinks_mixed_members_and_preserves_exact_identity(
    tmp_path: Path,
) -> None:
    paragraph_note, exact_note, comparison_note = _loaded_records(tmp_path)
    bare, _ = _loaded_bare_selection(tmp_path)
    original = create_chromium_research_working_set(
        (bare, paragraph_note, bare, exact_note, comparison_note)
    )
    path = tmp_path / "working-set-v2.json"
    persist_chromium_research_working_set_v2(original, path)

    loaded = load_chromium_research_working_set(
        (bare, paragraph_note, bare, exact_note, comparison_note),
        path,
    )

    assert loaded.verification.working_set_format == (
        "pyxis.chromium.research_working_set.v2"
    )
    assert loaded.working_set.items[0] is bare
    assert loaded.working_set.items[1] is paragraph_note
    assert loaded.working_set.items[2] is bare
    assert loaded.working_set.items[3] is exact_note
    assert loaded.working_set.items[4] is comparison_note


def test_49d_load_v2_does_not_reread_individual_member_sidecars(
    tmp_path: Path,
) -> None:
    paragraph_note, exact_note, comparison_note = _loaded_records(tmp_path)
    bare, bare_path = _loaded_bare_selection(tmp_path)
    original = create_chromium_research_working_set(
        (paragraph_note, bare, exact_note, comparison_note)
    )
    path = tmp_path / "working-set-v2.json"
    persist_chromium_research_working_set_v2(original, path)

    paragraph_note.verification.path.unlink()
    bare_path.unlink()
    exact_note.verification.path.unlink()
    comparison_note.verification.path.unlink()

    loaded = load_chromium_research_working_set(
        (paragraph_note, bare, exact_note, comparison_note),
        path,
    )

    assert loaded.working_set.items == (
        paragraph_note,
        bare,
        exact_note,
        comparison_note,
    )
    assert not paragraph_note.verification.path.exists()
    assert not bare.verification.path.exists()
    assert not exact_note.verification.path.exists()
    assert not comparison_note.verification.path.exists()


def test_49d_v2_file_valid_wrong_bare_digest_fails_member_relink(
    tmp_path: Path,
) -> None:
    bare, _ = _loaded_bare_selection(tmp_path)
    original = create_chromium_research_working_set((bare,))
    path = tmp_path / "working-set-v2.json"
    persist_chromium_research_working_set_v2(original, path)

    document = json.loads(path.read_text(encoding="utf-8"))
    wrong_digest = "f" * 64
    assert wrong_digest != bare.verification.selection_record_sha256
    document["working_set_record"]["items"][0]["member_record_sha256"] = wrong_digest
    document["working_set_record_sha256"] = hashlib.sha256(
        _canonical_bytes(document["working_set_record"])
    ).hexdigest()
    path.write_bytes(_canonical_document_bytes(document))

    verified = verify_chromium_research_working_set(path)
    assert verified.working_set_format == "pyxis.chromium.research_working_set.v2"
    assert verified.items[0].member_record_sha256 == wrong_digest

    with pytest.raises(
        ChromiumResearchWorkingSetMemberMismatchError,
        match="item 0 references a different member record",
    ):
        load_chromium_research_working_set((bare,), path)


def test_49d_v2_rejects_same_members_in_different_order(
    tmp_path: Path,
) -> None:
    paragraph_note, _, _ = _loaded_records(tmp_path)
    bare, _ = _loaded_bare_selection(tmp_path)
    original = create_chromium_research_working_set((bare, paragraph_note))
    path = tmp_path / "working-set-v2.json"
    persist_chromium_research_working_set_v2(original, path)

    with pytest.raises(
        ChromiumResearchWorkingSetMemberMismatchError,
        match="item 0 references a different member kind",
    ):
        load_chromium_research_working_set(
            (paragraph_note, bare),
            path,
        )
