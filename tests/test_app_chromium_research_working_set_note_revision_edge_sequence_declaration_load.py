from __future__ import annotations

import json
from pathlib import Path

import pytest

from test_app_chromium_research_working_set_note_revision_edge_sequence_load import (
    _two_successor_edges,
)
from test_app_chromium_research_working_set_note_revision_edge_sequence_persistence import (
    _canonical_bytes,
    _sequence,
    _write_recomputed_document,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_persistence import (
    ChromiumResearchWorkingSetNoteRevisionEdgeIntegrityError,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_sequence_declaration_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceDeclarationRecord,
    ChromiumResearchWorkingSetNoteRevisionEdgeSequenceDeclarationRelinkError,
    load_chromium_research_working_set_note_revision_edge_sequence_declaration,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_sequence_load import (
    ChromiumResearchWorkingSetNoteRevisionEdgeSequenceRelinkError,
    load_chromium_research_working_set_note_revision_edge_sequence,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_sequence_persistence import (
    ChromiumResearchWorkingSetNoteRevisionEdgeSequenceIntegrityError,
    persist_chromium_research_working_set_note_revision_edge_sequence,
    verify_chromium_research_working_set_note_revision_edge_sequence,
)


def _declared_sequence(tmp_path: Path):
    prefix, v4_path, loaded_v4, loaded_v5, v5_path, v6_path, sequence = _sequence(
        tmp_path
    )
    declaration_path = tmp_path / "declared-sequence.json"
    persisted = persist_chromium_research_working_set_note_revision_edge_sequence(
        sequence,
        declaration_path,
    )
    return (
        prefix,
        v4_path,
        loaded_v4,
        loaded_v5,
        v5_path,
        v6_path,
        sequence,
        declaration_path,
        persisted,
    )


def test_declaration_load_relinks_exact_explicit_sequence_with_fresh_evidence(
    tmp_path: Path,
) -> None:
    (
        _,
        _,
        loaded_v4,
        _,
        v5_path,
        v6_path,
        original_sequence,
        declaration_path,
        _,
    ) = _declared_sequence(tmp_path)

    loaded = load_chromium_research_working_set_note_revision_edge_sequence_declaration(
        loaded_v4,
        [v5_path, v6_path],
        declaration_path,
    )

    assert isinstance(
        loaded,
        ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceDeclarationRecord,
    )
    assert loaded.verification.path == declaration_path.resolve()
    assert loaded.sequence is not original_sequence
    assert loaded.sequence.starting_predecessor is loaded_v4
    assert len(loaded.sequence.edges) == 2
    assert loaded.sequence.edges[0].predecessor is loaded_v4
    assert loaded.sequence.edges[1].predecessor is loaded.sequence.edges[0]
    assert loaded.sequence.edges[0].revision.revised_note.note_text == (
        "  v5 exact human wording 😀  "
    )
    assert loaded.sequence.edges[1].revision.revised_note.note_text == (
        "v6 exact human wording\nStill tentative."
    )


def test_declaration_load_uses_explicit_moved_paths_without_path_identity(
    tmp_path: Path,
) -> None:
    (
        _,
        _,
        loaded_v4,
        _,
        v5_path,
        v6_path,
        _,
        declaration_path,
        _,
    ) = _declared_sequence(tmp_path)
    moved_v5 = tmp_path / "moved-v5.json"
    moved_v6 = tmp_path / "moved-v6.json"
    moved_declaration = tmp_path / "moved-declaration.json"
    v5_path.replace(moved_v5)
    v6_path.replace(moved_v6)
    declaration_path.replace(moved_declaration)

    loaded = load_chromium_research_working_set_note_revision_edge_sequence_declaration(
        loaded_v4,
        [moved_v5, moved_v6],
        moved_declaration,
    )

    assert loaded.verification.path == moved_declaration.resolve()
    assert loaded.sequence.edges[0].verification.path == moved_v5.resolve()
    assert loaded.sequence.edges[1].verification.path == moved_v6.resolve()


def test_declaration_load_rejects_recomputed_wrong_start_that_file_verification_accepts(
    tmp_path: Path,
) -> None:
    (
        _,
        _,
        loaded_v4,
        _,
        v5_path,
        v6_path,
        _,
        declaration_path,
        _,
    ) = _declared_sequence(tmp_path)
    document = json.loads(declaration_path.read_text(encoding="utf-8"))
    document["sequence_record"]["starting_predecessor_reference"]["record_sha256"] = (
        "f" * 64
    )
    _write_recomputed_document(declaration_path, document)

    verified = verify_chromium_research_working_set_note_revision_edge_sequence(
        declaration_path
    )
    assert verified.starting_predecessor.record_sha256 == "f" * 64

    with pytest.raises(
        ChromiumResearchWorkingSetNoteRevisionEdgeSequenceDeclarationRelinkError,
        match="starting predecessor identity",
    ):
        load_chromium_research_working_set_note_revision_edge_sequence_declaration(
            loaded_v4,
            [v5_path, v6_path],
            declaration_path,
        )


def test_declaration_load_rejects_recomputed_reordered_declaration_that_verifies(
    tmp_path: Path,
) -> None:
    (
        _,
        _,
        loaded_v4,
        _,
        v5_path,
        v6_path,
        _,
        declaration_path,
        _,
    ) = _declared_sequence(tmp_path)
    document = json.loads(declaration_path.read_text(encoding="utf-8"))
    document["sequence_record"]["edge_references"].reverse()
    _write_recomputed_document(declaration_path, document)

    verified = verify_chromium_research_working_set_note_revision_edge_sequence(
        declaration_path
    )
    assert len(verified.edges) == 2

    with pytest.raises(
        ChromiumResearchWorkingSetNoteRevisionEdgeSequenceDeclarationRelinkError,
        match="edge member 0 identity",
    ):
        load_chromium_research_working_set_note_revision_edge_sequence_declaration(
            loaded_v4,
            [v5_path, v6_path],
            declaration_path,
        )


def test_declaration_load_does_not_discover_missing_declared_members(tmp_path: Path) -> None:
    (
        _,
        _,
        loaded_v4,
        _,
        v5_path,
        _,
        _,
        declaration_path,
        _,
    ) = _declared_sequence(tmp_path)

    with pytest.raises(
        ChromiumResearchWorkingSetNoteRevisionEdgeSequenceDeclarationRelinkError,
        match="member count",
    ):
        load_chromium_research_working_set_note_revision_edge_sequence_declaration(
            loaded_v4,
            [v5_path],
            declaration_path,
        )


def test_declaration_load_does_not_reorder_explicit_edge_paths(tmp_path: Path) -> None:
    (
        _,
        _,
        loaded_v4,
        _,
        v5_path,
        v6_path,
        _,
        declaration_path,
        _,
    ) = _declared_sequence(tmp_path)

    with pytest.raises(
        ChromiumResearchWorkingSetNoteRevisionEdgeSequenceDeclarationRelinkError,
        match="could not be freshly relinked",
    ) as exc_info:
        load_chromium_research_working_set_note_revision_edge_sequence_declaration(
            loaded_v4,
            [v6_path, v5_path],
            declaration_path,
        )

    assert isinstance(
        exc_info.value.__cause__,
        ChromiumResearchWorkingSetNoteRevisionEdgeSequenceRelinkError,
    )


def test_declaration_integrity_fails_before_explicit_edge_loading(tmp_path: Path) -> None:
    (
        _,
        _,
        loaded_v4,
        _,
        v5_path,
        v6_path,
        _,
        declaration_path,
        _,
    ) = _declared_sequence(tmp_path)
    document = json.loads(declaration_path.read_text(encoding="utf-8"))
    document["sequence_record"]["edge_references"][0]["record_sha256"] = "a" * 64
    declaration_path.write_bytes(_canonical_bytes(document) + b"\n")
    v5_path.unlink()
    v6_path.unlink()

    with pytest.raises(
        ChromiumResearchWorkingSetNoteRevisionEdgeSequenceIntegrityError,
        match="SHA-256 does not match",
    ):
        load_chromium_research_working_set_note_revision_edge_sequence_declaration(
            loaded_v4,
            [v5_path, v6_path],
            declaration_path,
        )


def test_declaration_load_rejects_explicit_edge_tamper_after_valid_declaration(
    tmp_path: Path,
) -> None:
    (
        _,
        _,
        loaded_v4,
        _,
        v5_path,
        v6_path,
        _,
        declaration_path,
        _,
    ) = _declared_sequence(tmp_path)
    document = json.loads(v5_path.read_text(encoding="utf-8"))
    document["edge_record"]["edge"]["revision"]["revised_note"]["text"] = (
        "tampered without edge digest update"
    )
    v5_path.write_bytes(_canonical_bytes(document) + b"\n")

    with pytest.raises(
        ChromiumResearchWorkingSetNoteRevisionEdgeSequenceDeclarationRelinkError,
        match="could not be freshly relinked",
    ) as exc_info:
        load_chromium_research_working_set_note_revision_edge_sequence_declaration(
            loaded_v4,
            [v5_path, v6_path],
            declaration_path,
        )

    sequence_error = exc_info.value.__cause__
    assert isinstance(
        sequence_error,
        ChromiumResearchWorkingSetNoteRevisionEdgeSequenceRelinkError,
    )
    assert isinstance(sequence_error.__cause__, ChromiumResearchWorkingSetNoteRevisionEdgeIntegrityError)


def test_declaration_load_supports_explicit_loaded_continuation_start(
    tmp_path: Path,
) -> None:
    (
        _,
        v4_path,
        loaded_v4,
        _,
        v5_path,
        _,
        _,
        _,
        v6_path,
        _,
    ) = _two_successor_edges(tmp_path)
    loaded_continuation = loaded_v4.predecessor
    sequence = load_chromium_research_working_set_note_revision_edge_sequence(
        loaded_continuation,
        [v4_path, v5_path, v6_path],
    )
    declaration_path = tmp_path / "continuation-start-declaration.json"
    persist_chromium_research_working_set_note_revision_edge_sequence(
        sequence,
        declaration_path,
    )

    loaded = load_chromium_research_working_set_note_revision_edge_sequence_declaration(
        loaded_continuation,
        [v4_path, v5_path, v6_path],
        declaration_path,
    )

    assert loaded.sequence.starting_predecessor is loaded_continuation
    assert len(loaded.sequence.edges) == 3
    assert loaded.sequence.edges[0].predecessor is loaded_continuation
    assert loaded.sequence.edges[1].predecessor is loaded.sequence.edges[0]
    assert loaded.sequence.edges[2].predecessor is loaded.sequence.edges[1]


def test_declaration_load_module_is_importable_and_invalid_caller_input_stays_explicit(
    tmp_path: Path,
) -> None:
    (
        _,
        _,
        loaded_v4,
        _,
        v5_path,
        v6_path,
        _,
        declaration_path,
        _,
    ) = _declared_sequence(tmp_path)

    loaded = load_chromium_research_working_set_note_revision_edge_sequence_declaration(
        loaded_v4,
        [v5_path, v6_path],
        declaration_path,
    )
    assert isinstance(
        loaded,
        ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceDeclarationRecord,
    )

    with pytest.raises(TypeError, match="starting_predecessor must be"):
        load_chromium_research_working_set_note_revision_edge_sequence_declaration(  # type: ignore[arg-type]
            object(),
            [v5_path, v6_path],
            declaration_path,
        )

    with pytest.raises(TypeError, match="ordered iterable"):
        load_chromium_research_working_set_note_revision_edge_sequence_declaration(
            loaded_v4,
            v5_path,  # type: ignore[arg-type]
            declaration_path,
        )
