from __future__ import annotations

from dataclasses import replace
import hashlib
import json
from pathlib import Path

import pytest

from test_app_chromium_research_working_set_note_revision_edge_sequence_load import (
    _two_successor_edges,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_sequence_load import (
    load_chromium_research_working_set_note_revision_edge_sequence,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_sequence_persistence import (
    ChromiumPageResearchWorkingSetNoteRevisionEdgeSequencePersistenceEvidence,
    ChromiumPageResearchWorkingSetNoteRevisionEdgeSequenceReference,
    ChromiumPageResearchWorkingSetNoteRevisionEdgeSequenceVerificationEvidence,
    ChromiumResearchWorkingSetNoteRevisionEdgeSequenceIntegrityError,
    persist_chromium_research_working_set_note_revision_edge_sequence,
    verify_chromium_research_working_set_note_revision_edge_sequence,
)


_SEQUENCE_FORMAT = (
    "pyxis.chromium.research_working_set_note_revision_edge_sequence.v1"
)
_CONTINUATION_FORMAT = (
    "pyxis.chromium.research_working_set_note_revision_continuation.v1"
)
_EDGE_FORMAT = "pyxis.chromium.research_working_set_note_revision_edge.v1"


def _sequence(tmp_path: Path):
    (
        prefix,
        v4_path,
        loaded_v4,
        _,
        v5_path,
        loaded_v5,
        _,
        _,
        v6_path,
        _,
    ) = _two_successor_edges(
        tmp_path,
        v4_text="v4 text that must not be copied",
        v5_text="  v5 exact human wording 😀  ",
        v6_text="v6 exact human wording\nStill tentative.",
    )
    sequence = load_chromium_research_working_set_note_revision_edge_sequence(
        loaded_v4,
        [v5_path, v6_path],
    )
    return prefix, v4_path, loaded_v4, loaded_v5, v5_path, v6_path, sequence


def _canonical_bytes(payload: object) -> bytes:
    return json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def _write_recomputed_document(path: Path, document: dict[str, object]) -> None:
    sequence_record = document["sequence_record"]
    document["sequence_record_sha256"] = hashlib.sha256(
        _canonical_bytes(sequence_record)
    ).hexdigest()
    path.write_bytes(_canonical_bytes(document) + b"\n")


def test_persist_sequence_stores_only_start_and_ordered_edge_identities(tmp_path: Path) -> None:
    _, _, loaded_v4, _, v5_path, v6_path, sequence = _sequence(tmp_path)
    destination = tmp_path / "declared-sequence.json"

    persisted = persist_chromium_research_working_set_note_revision_edge_sequence(
        sequence,
        destination,
    )
    verified = verify_chromium_research_working_set_note_revision_edge_sequence(
        destination
    )
    raw_text = destination.read_text(encoding="utf-8")

    assert isinstance(
        persisted,
        ChromiumPageResearchWorkingSetNoteRevisionEdgeSequencePersistenceEvidence,
    )
    assert isinstance(
        verified,
        ChromiumPageResearchWorkingSetNoteRevisionEdgeSequenceVerificationEvidence,
    )
    assert persisted.sequence is sequence
    assert persisted.sequence_format == _SEQUENCE_FORMAT
    assert verified.sequence_format == _SEQUENCE_FORMAT
    assert verified.starting_predecessor == (
        ChromiumPageResearchWorkingSetNoteRevisionEdgeSequenceReference(
            record_format=_EDGE_FORMAT,
            record_sha256=loaded_v4.verification.edge_record_sha256,
        )
    )
    assert tuple(reference.record_sha256 for reference in verified.edges) == tuple(
        edge.verification.edge_record_sha256 for edge in sequence.edges
    )
    assert all(reference.record_format == _EDGE_FORMAT for reference in verified.edges)

    assert "v4 text that must not be copied" not in raw_text
    assert "v5 exact human wording" not in raw_text
    assert "v6 exact human wording" not in raw_text
    assert str(v5_path.resolve()) not in raw_text
    assert str(v6_path.resolve()) not in raw_text


def test_persist_sequence_supports_explicit_loaded_continuation_start(tmp_path: Path) -> None:
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
    destination = tmp_path / "continuation-start-sequence.json"

    persist_chromium_research_working_set_note_revision_edge_sequence(
        sequence,
        destination,
    )
    verified = verify_chromium_research_working_set_note_revision_edge_sequence(
        destination
    )

    assert verified.starting_predecessor.record_format == _CONTINUATION_FORMAT
    assert verified.starting_predecessor.record_sha256 == (
        loaded_continuation.verification.continuation_record_sha256
    )
    assert len(verified.edges) == 3
    assert verified.edges[0].record_sha256 == loaded_v4.verification.edge_record_sha256


def test_persist_sequence_does_not_require_any_referenced_file_after_load(tmp_path: Path) -> None:
    prefix, v4_path, _, _, v5_path, v6_path, sequence = _sequence(tmp_path)
    paragraph_note = prefix[0]
    exact_note = prefix[1]
    comparison_note = prefix[2]
    working_set_path = prefix[3]
    prior_note_path = prefix[4]
    revision_path = prefix[5]
    continuation_path = prefix[6]

    paragraph_note.verification.path.unlink(missing_ok=True)
    exact_note.verification.path.unlink(missing_ok=True)
    comparison_note.verification.path.unlink(missing_ok=True)
    working_set_path.unlink(missing_ok=True)
    prior_note_path.unlink(missing_ok=True)
    revision_path.unlink(missing_ok=True)
    continuation_path.unlink(missing_ok=True)
    v4_path.unlink(missing_ok=True)
    v5_path.unlink(missing_ok=True)
    v6_path.unlink(missing_ok=True)

    destination = tmp_path / "sequence-after-files-removed.json"
    persisted = persist_chromium_research_working_set_note_revision_edge_sequence(
        sequence,
        destination,
    )

    assert persisted.sequence is sequence
    assert destination.exists()
    assert not v4_path.exists()
    assert not v5_path.exists()
    assert not v6_path.exists()
    assert not continuation_path.exists()


def test_persist_sequence_rejects_forged_loaded_edge_identity(tmp_path: Path) -> None:
    _, _, _, _, _, _, sequence = _sequence(tmp_path)
    first = sequence.edges[0]
    forged_verification = replace(
        first.verification,
        edge_record_sha256="f" * 64,
    )
    forged_first = replace(first, verification=forged_verification)
    forged_sequence = replace(
        sequence,
        edges=(forged_first, *sequence.edges[1:]),
    )
    destination = tmp_path / "forged-identity.json"

    with pytest.raises(ValueError, match="retained verification identity is incoherent"):
        persist_chromium_research_working_set_note_revision_edge_sequence(
            forged_sequence,
            destination,
        )

    assert not destination.exists()


def test_persist_sequence_rejects_forged_in_memory_order(tmp_path: Path) -> None:
    _, _, _, _, _, _, sequence = _sequence(tmp_path)
    forged_sequence = replace(
        sequence,
        edges=(sequence.edges[1], sequence.edges[0]),
    )
    destination = tmp_path / "forged-order.json"

    with pytest.raises(ValueError, match="does not retain the exact preceding"):
        persist_chromium_research_working_set_note_revision_edge_sequence(
            forged_sequence,
            destination,
        )

    assert not destination.exists()


def test_verify_sequence_rejects_raw_tamper_without_digest_update(tmp_path: Path) -> None:
    _, _, _, _, _, _, sequence = _sequence(tmp_path)
    destination = tmp_path / "raw-tamper.json"
    persist_chromium_research_working_set_note_revision_edge_sequence(
        sequence,
        destination,
    )
    document = json.loads(destination.read_text(encoding="utf-8"))
    document["sequence_record"]["edge_references"][0]["record_sha256"] = "a" * 64
    destination.write_bytes(_canonical_bytes(document) + b"\n")

    with pytest.raises(
        ChromiumResearchWorkingSetNoteRevisionEdgeSequenceIntegrityError,
        match="SHA-256 does not match",
    ):
        verify_chromium_research_working_set_note_revision_edge_sequence(destination)


def test_file_only_verification_accepts_recomputed_wrong_start_identity(tmp_path: Path) -> None:
    _, _, loaded_v4, _, _, _, sequence = _sequence(tmp_path)
    destination = tmp_path / "wrong-start-recomputed.json"
    persist_chromium_research_working_set_note_revision_edge_sequence(
        sequence,
        destination,
    )
    document = json.loads(destination.read_text(encoding="utf-8"))
    document["sequence_record"]["starting_predecessor_reference"]["record_sha256"] = (
        "f" * 64
    )
    _write_recomputed_document(destination, document)

    verified = verify_chromium_research_working_set_note_revision_edge_sequence(
        destination
    )

    assert verified.starting_predecessor.record_sha256 == "f" * 64
    assert verified.starting_predecessor.record_sha256 != (
        loaded_v4.verification.edge_record_sha256
    )


def test_file_only_verification_accepts_recomputed_different_declared_order(tmp_path: Path) -> None:
    _, _, _, _, _, _, sequence = _sequence(tmp_path)
    destination = tmp_path / "reordered-recomputed.json"
    persist_chromium_research_working_set_note_revision_edge_sequence(
        sequence,
        destination,
    )
    document = json.loads(destination.read_text(encoding="utf-8"))
    references = document["sequence_record"]["edge_references"]
    references.reverse()
    _write_recomputed_document(destination, document)

    verified = verify_chromium_research_working_set_note_revision_edge_sequence(
        destination
    )

    assert tuple(reference.record_sha256 for reference in verified.edges) == (
        sequence.edges[1].verification.edge_record_sha256,
        sequence.edges[0].verification.edge_record_sha256,
    )


def test_sequence_persistence_is_deterministic_no_overwrite_and_wrong_type_safe(
    tmp_path: Path,
) -> None:
    _, _, _, _, _, _, sequence = _sequence(tmp_path)
    first_path = tmp_path / "first-sequence.json"
    second_path = tmp_path / "second-sequence.json"

    first = persist_chromium_research_working_set_note_revision_edge_sequence(
        sequence,
        first_path,
    )
    second = persist_chromium_research_working_set_note_revision_edge_sequence(
        sequence,
        second_path,
    )

    assert first.sequence_record_sha256 == second.sequence_record_sha256
    assert first_path.read_bytes() == second_path.read_bytes()

    original = first_path.read_bytes()
    with pytest.raises(FileExistsError):
        persist_chromium_research_working_set_note_revision_edge_sequence(
            sequence,
            first_path,
        )
    assert first_path.read_bytes() == original

    wrong_type_path = tmp_path / "wrong-type.json"
    with pytest.raises(TypeError, match="sequence must be"):
        persist_chromium_research_working_set_note_revision_edge_sequence(  # type: ignore[arg-type]
            object(),
            wrong_type_path,
        )
    assert not wrong_type_path.exists()


def test_sequence_persistence_module_is_explicitly_importable_and_verifier_rejects_empty_edges(
    tmp_path: Path,
) -> None:
    _, _, _, _, _, _, sequence = _sequence(tmp_path)
    destination = tmp_path / "public-sequence.json"
    persisted = persist_chromium_research_working_set_note_revision_edge_sequence(
        sequence,
        destination,
    )
    assert isinstance(
        persisted,
        ChromiumPageResearchWorkingSetNoteRevisionEdgeSequencePersistenceEvidence,
    )

    document = json.loads(destination.read_text(encoding="utf-8"))
    document["sequence_record"]["edge_references"] = []
    _write_recomputed_document(destination, document)

    with pytest.raises(
        ChromiumResearchWorkingSetNoteRevisionEdgeSequenceIntegrityError,
        match="non-empty ordered list",
    ):
        verify_chromium_research_working_set_note_revision_edge_sequence(destination)
