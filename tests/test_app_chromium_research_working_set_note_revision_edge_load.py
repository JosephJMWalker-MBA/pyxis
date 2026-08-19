from __future__ import annotations

from dataclasses import replace
import hashlib
import json
from pathlib import Path

import pytest

from test_app_chromium_research_working_set_note_revision_continuation_load import (
    _loaded_continuation,
)
from test_app_chromium_research_working_set_note_revision_continuation_persistence import (
    _canonical_bytes,
    _canonical_document_bytes,
)
from test_app_chromium_research_working_set_note_revision_edge_persistence import (
    _durable_edge,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord,
    ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError,
    load_chromium_research_working_set_note_revision_edge,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_persistence import (
    ChromiumResearchWorkingSetNoteRevisionEdgeIntegrityError,
    verify_chromium_research_working_set_note_revision_edge,
)


_EDGE_FORMAT = "pyxis.chromium.research_working_set_note_revision_edge.v1"
_EDGE_MODE = "caller_authored_research_working_set_note_revision_edge"
_REVISION_MODE = "caller_authored_revision_of_research_working_set_note"
_NOTE_MODE = "caller_authored_note_on_research_working_set"


def _write_edge(
    path: Path,
    *,
    predecessor_format: str,
    predecessor_sha256: str,
    revised_note_text: str,
) -> None:
    edge_record = {
        "predecessor_reference": {
            "format": predecessor_format,
            "record_sha256": predecessor_sha256,
        },
        "edge": {
            "mode": _EDGE_MODE,
            "revision": {
                "mode": _REVISION_MODE,
                "revised_note": {
                    "mode": _NOTE_MODE,
                    "text": revised_note_text,
                },
            },
        },
    }
    document = {
        "format": _EDGE_FORMAT,
        "edge_record": edge_record,
        "edge_record_sha256": hashlib.sha256(_canonical_bytes(edge_record)).hexdigest(),
    }
    path.write_bytes(_canonical_document_bytes(document))


def test_load_revision_edge_relinks_exact_loaded_continuation_and_reconstructs_v4(
    tmp_path: Path,
) -> None:
    *prefix, edge_path, _ = _durable_edge(
        tmp_path,
        continued_text="  v3 after another source 😀\nStill tentative.  ",
        extension_text="  v4 after checking again.\nStill human-owned.  ",
    )
    loaded_continuation = prefix[9]

    loaded = load_chromium_research_working_set_note_revision_edge(
        loaded_continuation,
        edge_path,
    )

    assert isinstance(loaded, ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord)
    assert loaded.verification.edge_format == _EDGE_FORMAT
    assert loaded.predecessor is loaded_continuation
    assert (
        loaded.revision.prior_note
        is loaded_continuation.continuation.revision.revised_note
    )
    assert (
        loaded.revision.revised_note.working_set
        is loaded_continuation.continuation.revision.revised_note.working_set
    )
    assert loaded.revision.revised_note.note_text == (
        "  v4 after checking again.\nStill human-owned.  "
    )


def test_load_revision_edge_uses_content_identity_not_path(tmp_path: Path) -> None:
    *prefix, edge_path, _ = _durable_edge(tmp_path)
    loaded_continuation = prefix[9]
    moved = tmp_path / "moved-revision-edge.json"
    edge_path.replace(moved)

    loaded = load_chromium_research_working_set_note_revision_edge(
        loaded_continuation,
        moved,
    )

    assert loaded.verification.path == moved.resolve()
    assert loaded.predecessor is loaded_continuation


def test_load_revision_edge_rejects_different_valid_loaded_continuation(
    tmp_path: Path,
) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    first.mkdir()
    second.mkdir()

    *prefix, edge_path, _ = _durable_edge(
        first,
        continued_text="actual v3 predecessor",
        extension_text="v4 continuing actual v3",
    )
    actual_predecessor = prefix[9]
    *_, other_predecessor = _loaded_continuation(
        second,
        continued_text="different but valid v3 predecessor",
    )
    assert other_predecessor.verification.continuation_record_sha256 != (
        actual_predecessor.verification.continuation_record_sha256
    )

    with pytest.raises(
        ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError,
        match="different predecessor record",
    ):
        load_chromium_research_working_set_note_revision_edge(
            other_predecessor,
            edge_path,
        )


def test_load_revision_edge_rejects_recomputed_wrong_predecessor_identity(
    tmp_path: Path,
) -> None:
    *prefix, edge_path, _ = _durable_edge(tmp_path)
    loaded_continuation = prefix[9]
    document = json.loads(edge_path.read_text(encoding="utf-8"))
    wrong_digest = "f" * 64
    assert wrong_digest != loaded_continuation.verification.continuation_record_sha256
    document["edge_record"]["predecessor_reference"]["record_sha256"] = wrong_digest
    document["edge_record_sha256"] = hashlib.sha256(
        _canonical_bytes(document["edge_record"])
    ).hexdigest()
    edge_path.write_bytes(_canonical_document_bytes(document))

    verified = verify_chromium_research_working_set_note_revision_edge(edge_path)
    assert verified.predecessor_record_sha256 == wrong_digest

    with pytest.raises(
        ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError,
        match="different predecessor record",
    ):
        load_chromium_research_working_set_note_revision_edge(
            loaded_continuation,
            edge_path,
        )


def test_load_revision_edge_rejects_recomputed_v4_equal_to_real_v3(
    tmp_path: Path,
) -> None:
    v3_text = "the exact real v3 wording"
    *prefix, edge_path, _ = _durable_edge(
        tmp_path,
        continued_text=v3_text,
        extension_text="genuinely different v4 at creation",
    )
    loaded_continuation = prefix[9]
    document = json.loads(edge_path.read_text(encoding="utf-8"))
    document["edge_record"]["edge"]["revision"]["revised_note"]["text"] = v3_text
    document["edge_record_sha256"] = hashlib.sha256(
        _canonical_bytes(document["edge_record"])
    ).hexdigest()
    edge_path.write_bytes(_canonical_document_bytes(document))

    verified = verify_chromium_research_working_set_note_revision_edge(edge_path)
    assert verified.revised_note_text == v3_text

    with pytest.raises(
        ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError,
        match="cannot be re-established as an actual revision",
    ):
        load_chromium_research_working_set_note_revision_edge(
            loaded_continuation,
            edge_path,
        )


def test_load_revision_edge_accepts_explicit_loaded_edge_predecessor_without_traversal(
    tmp_path: Path,
) -> None:
    (
        paragraph_note,
        exact_note,
        comparison_note,
        working_set_path,
        prior_note_path,
        revision_path,
        continuation_path,
        _,
        _,
        loaded_continuation,
        _,
        first_edge_path,
        _,
    ) = _durable_edge(
        tmp_path,
        extension_text="v4 exact wording",
    )
    loaded_first = load_chromium_research_working_set_note_revision_edge(
        loaded_continuation,
        first_edge_path,
    )
    second_edge_path = tmp_path / "second-edge.json"
    _write_edge(
        second_edge_path,
        predecessor_format=loaded_first.verification.edge_format,
        predecessor_sha256=loaded_first.verification.edge_record_sha256,
        revised_note_text="v5 exact wording",
    )

    paragraph_note.verification.path.unlink(missing_ok=True)
    exact_note.verification.path.unlink(missing_ok=True)
    comparison_note.verification.path.unlink(missing_ok=True)
    working_set_path.unlink(missing_ok=True)
    prior_note_path.unlink(missing_ok=True)
    revision_path.unlink(missing_ok=True)
    continuation_path.unlink(missing_ok=True)
    first_edge_path.unlink()

    loaded_second = load_chromium_research_working_set_note_revision_edge(
        loaded_first,
        second_edge_path,
    )

    assert loaded_second.predecessor is loaded_first
    assert loaded_second.revision.prior_note is loaded_first.revision.revised_note
    assert loaded_second.revision.revised_note.note_text == "v5 exact wording"
    assert not first_edge_path.exists()
    assert not continuation_path.exists()


def test_load_revision_edge_rejects_wrong_explicit_loaded_edge_predecessor(
    tmp_path: Path,
) -> None:
    first_dir = tmp_path / "first"
    other_dir = tmp_path / "other"
    first_dir.mkdir()
    other_dir.mkdir()

    *first_prefix, first_edge_path, _ = _durable_edge(
        first_dir,
        extension_text="first v4 wording",
    )
    first_loaded_continuation = first_prefix[9]
    loaded_first = load_chromium_research_working_set_note_revision_edge(
        first_loaded_continuation,
        first_edge_path,
    )

    *other_prefix, other_edge_path, _ = _durable_edge(
        other_dir,
        extension_text="other v4 wording",
    )
    other_loaded_continuation = other_prefix[9]
    loaded_other = load_chromium_research_working_set_note_revision_edge(
        other_loaded_continuation,
        other_edge_path,
    )
    assert loaded_other.verification.edge_record_sha256 != (
        loaded_first.verification.edge_record_sha256
    )

    second_edge_path = tmp_path / "edge-referencing-first.json"
    _write_edge(
        second_edge_path,
        predecessor_format=loaded_first.verification.edge_format,
        predecessor_sha256=loaded_first.verification.edge_record_sha256,
        revised_note_text="v5 after first",
    )

    with pytest.raises(
        ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError,
        match="different predecessor record",
    ):
        load_chromium_research_working_set_note_revision_edge(
            loaded_other,
            second_edge_path,
        )


def test_load_revision_edge_rejects_forged_loaded_edge_local_predecessor_identity(
    tmp_path: Path,
) -> None:
    *prefix, first_edge_path, _ = _durable_edge(tmp_path, extension_text="v4 wording")
    loaded_continuation = prefix[9]
    loaded_first = load_chromium_research_working_set_note_revision_edge(
        loaded_continuation,
        first_edge_path,
    )
    forged_verification = replace(
        loaded_first.verification,
        predecessor_record_sha256="f" * 64,
    )
    forged_loaded = replace(loaded_first, verification=forged_verification)
    second_edge_path = tmp_path / "second-edge.json"
    _write_edge(
        second_edge_path,
        predecessor_format=forged_loaded.verification.edge_format,
        predecessor_sha256=forged_loaded.verification.edge_record_sha256,
        revised_note_text="v5 should not load from forged predecessor state",
    )

    with pytest.raises(
        ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError,
        match="incoherent predecessor identity",
    ):
        load_chromium_research_working_set_note_revision_edge(
            forged_loaded,
            second_edge_path,
        )


def test_load_revision_edge_freshly_verifies_current_edge_before_relinking(
    tmp_path: Path,
) -> None:
    *prefix, edge_path, _ = _durable_edge(tmp_path)
    loaded_continuation = prefix[9]
    document = json.loads(edge_path.read_text(encoding="utf-8"))
    document["edge_record"]["edge"]["revision"]["revised_note"]["text"] = (
        "tampered without matching digest"
    )
    edge_path.write_bytes(_canonical_document_bytes(document))

    with pytest.raises(ChromiumResearchWorkingSetNoteRevisionEdgeIntegrityError):
        load_chromium_research_working_set_note_revision_edge(
            loaded_continuation,
            edge_path,
        )


def test_revision_edge_load_rejects_wrong_type_and_is_publicly_importable(
    tmp_path: Path,
) -> None:
    *prefix, edge_path, _ = _durable_edge(tmp_path)
    loaded_continuation = prefix[9]

    with pytest.raises(TypeError, match="already-loaded 23C continuation or 24C revision edge"):
        load_chromium_research_working_set_note_revision_edge(  # type: ignore[arg-type]
            object(),
            edge_path,
        )

    loaded = load_chromium_research_working_set_note_revision_edge(
        loaded_continuation,
        edge_path,
    )
    assert loaded.predecessor is loaded_continuation
    assert loaded.revision.revised_note.note_text == (
        loaded.verification.revised_note_text
    )
