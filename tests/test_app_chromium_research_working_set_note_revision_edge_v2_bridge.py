from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from test_app_chromium_research_working_set_note_revision_continuation_extension import (
    _loaded_continuation_v2,
)
from test_app_chromium_research_working_set_note_revision_continuation_persistence import (
    _canonical_bytes,
    _canonical_document_bytes,
)
from pyxis.app.chromium_research_working_set_note_revision_continuation_extension import (
    create_chromium_research_working_set_note_revision_continuation_extension,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_extension import (
    create_chromium_research_working_set_note_revision_edge_extension,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_extension_persistence import (
    persist_chromium_research_working_set_note_revision_edge_extension,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord,
    ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError,
    load_chromium_research_working_set_note_revision_edge,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_persistence import (
    ChromiumResearchWorkingSetNoteRevisionEdgeIntegrityError,
    persist_chromium_research_working_set_note_revision_edge,
    verify_chromium_research_working_set_note_revision_edge,
)


_EDGE_FORMAT = "pyxis.chromium.research_working_set_note_revision_edge.v1"
_CONTINUATION_FORMAT_V2 = (
    "pyxis.chromium.research_working_set_note_revision_continuation.v2"
)


def _v2_backed_edge(
    tmp_path: Path,
    *,
    extension_text: str = "v4 on the v2 durable rationale line.",
):
    (
        paragraph_note,
        bare,
        bare_path,
        working_set_path,
        prior_note_path,
        revision_path,
        continuation_path,
        loaded_continuation,
    ) = _loaded_continuation_v2(tmp_path)
    extension = create_chromium_research_working_set_note_revision_continuation_extension(
        loaded_continuation,
        revised_note_text=extension_text,
    )
    edge_path = tmp_path / "v2-backed-edge.json"
    persisted = persist_chromium_research_working_set_note_revision_edge(
        extension,
        working_set_path,
        prior_note_path,
        revision_path,
        continuation_path,
        edge_path,
    )
    return (
        paragraph_note,
        bare,
        bare_path,
        working_set_path,
        prior_note_path,
        revision_path,
        continuation_path,
        loaded_continuation,
        extension,
        edge_path,
        persisted,
    )


def test_49i_persists_continuation_v2_backed_action_in_existing_edge_v1_format(
    tmp_path: Path,
) -> None:
    (
        paragraph_note,
        bare,
        _,
        working_set_path,
        prior_note_path,
        revision_path,
        continuation_path,
        loaded_continuation,
        extension,
        edge_path,
        persisted,
    ) = _v2_backed_edge(
        tmp_path,
        extension_text="  v4 after another explicit check 😀\nStill human-owned.  ",
    )

    verified = verify_chromium_research_working_set_note_revision_edge(edge_path)
    document = json.loads(edge_path.read_text(encoding="utf-8"))

    assert persisted.edge_format == _EDGE_FORMAT
    assert persisted.extension is extension
    assert verified.edge_format == _EDGE_FORMAT
    assert verified.predecessor_format == _CONTINUATION_FORMAT_V2
    assert verified.predecessor_record_sha256 == (
        loaded_continuation.verification.continuation_record_sha256
    )
    assert document["edge_record"]["predecessor_reference"] == {
        "format": _CONTINUATION_FORMAT_V2,
        "record_sha256": loaded_continuation.verification.continuation_record_sha256,
    }
    assert document["edge_record"]["edge"]["revision"]["revised_note"]["text"] == (
        extension.revision.revised_note.note_text
    )

    raw = edge_path.read_text(encoding="utf-8")
    assert loaded_continuation.prior_revision.revision.prior_note.note_text not in raw
    assert loaded_continuation.prior_revision.revision.revised_note.note_text not in raw
    assert loaded_continuation.continuation.revision.revised_note.note_text not in raw
    assert bare.selection.selected_text not in raw
    assert paragraph_note.note.note_text not in raw
    assert "working_set_record_sha256" not in raw
    assert "note_record_sha256" not in raw
    assert "member_kind" not in raw
    assert str(working_set_path.resolve()) not in raw
    assert str(prior_note_path.resolve()) not in raw
    assert str(revision_path.resolve()) not in raw
    assert str(continuation_path.resolve()) not in raw


def test_49i_edge_v1_verifier_accepts_only_explicitly_supported_new_predecessor_family(
    tmp_path: Path,
) -> None:
    *_, edge_path, _ = _v2_backed_edge(tmp_path)
    document = json.loads(edge_path.read_text(encoding="utf-8"))
    document["edge_record"]["predecessor_reference"]["format"] = (
        "pyxis.chromium.research_working_set_note_revision_continuation.v3"
    )
    document["edge_record_sha256"] = hashlib.sha256(
        _canonical_bytes(document["edge_record"])
    ).hexdigest()
    edge_path.write_bytes(_canonical_document_bytes(document))

    with pytest.raises(
        ChromiumResearchWorkingSetNoteRevisionEdgeIntegrityError,
        match="predecessor format is unsupported",
    ):
        verify_chromium_research_working_set_note_revision_edge(edge_path)


def test_49i_generic_24c_relinks_exact_loaded_continuation_v2_predecessor(
    tmp_path: Path,
) -> None:
    *prefix, edge_path, persisted = _v2_backed_edge(
        tmp_path,
        extension_text="  v4 relinked through ordinary 24C.\nStill human-owned.  ",
    )
    loaded_continuation = prefix[7]

    loaded_edge = load_chromium_research_working_set_note_revision_edge(
        loaded_continuation,
        edge_path,
    )

    assert isinstance(loaded_edge, ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord)
    assert loaded_edge.verification.edge_format == _EDGE_FORMAT
    assert loaded_edge.verification.edge_record_sha256 == persisted.edge_record_sha256
    assert loaded_edge.predecessor is loaded_continuation
    assert (
        loaded_edge.revision.prior_note
        is loaded_continuation.continuation.revision.revised_note
    )
    assert (
        loaded_edge.revision.revised_note.working_set
        is loaded_continuation.continuation.revision.revised_note.working_set
    )


def test_49i_file_valid_wrong_continuation_v2_identity_fails_24c(
    tmp_path: Path,
) -> None:
    *prefix, edge_path, _ = _v2_backed_edge(tmp_path)
    loaded_continuation = prefix[7]
    document = json.loads(edge_path.read_text(encoding="utf-8"))
    wrong_digest = "f" * 64
    assert wrong_digest != loaded_continuation.verification.continuation_record_sha256
    document["edge_record"]["predecessor_reference"]["record_sha256"] = wrong_digest
    document["edge_record_sha256"] = hashlib.sha256(
        _canonical_bytes(document["edge_record"])
    ).hexdigest()
    edge_path.write_bytes(_canonical_document_bytes(document))

    verified = verify_chromium_research_working_set_note_revision_edge(edge_path)
    assert verified.predecessor_format == _CONTINUATION_FORMAT_V2
    assert verified.predecessor_record_sha256 == wrong_digest

    with pytest.raises(
        ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError,
        match="different predecessor record",
    ):
        load_chromium_research_working_set_note_revision_edge(
            loaded_continuation,
            edge_path,
        )


def test_49i_file_valid_exact_text_noop_fails_24c_reconstruction(
    tmp_path: Path,
) -> None:
    *prefix, edge_path, _ = _v2_backed_edge(
        tmp_path,
        extension_text="genuinely different v4 at creation",
    )
    loaded_continuation = prefix[7]
    predecessor_text = loaded_continuation.continuation.revision.revised_note.note_text

    document = json.loads(edge_path.read_text(encoding="utf-8"))
    document["edge_record"]["edge"]["revision"]["revised_note"]["text"] = predecessor_text
    document["edge_record_sha256"] = hashlib.sha256(
        _canonical_bytes(document["edge_record"])
    ).hexdigest()
    edge_path.write_bytes(_canonical_document_bytes(document))

    verified = verify_chromium_research_working_set_note_revision_edge(edge_path)
    assert verified.revised_note_text == predecessor_text

    with pytest.raises(
        ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError,
        match="cannot be re-established as an actual revision",
    ):
        load_chromium_research_working_set_note_revision_edge(
            loaded_continuation,
            edge_path,
        )


def test_49i_24b_v2_bridge_does_not_reread_individual_member_sidecars(
    tmp_path: Path,
) -> None:
    (
        paragraph_note,
        bare,
        bare_path,
        working_set_path,
        prior_note_path,
        revision_path,
        continuation_path,
        loaded_continuation,
    ) = _loaded_continuation_v2(tmp_path)
    extension = create_chromium_research_working_set_note_revision_continuation_extension(
        loaded_continuation,
        revised_note_text="v4 after individual member files disappear.",
    )

    paragraph_note.verification.path.unlink(missing_ok=True)
    bare_path.unlink(missing_ok=True)
    destination = tmp_path / "edge-without-member-sidecars.json"

    persisted = persist_chromium_research_working_set_note_revision_edge(
        extension,
        working_set_path,
        prior_note_path,
        revision_path,
        continuation_path,
        destination,
    )

    assert persisted.extension is extension
    assert destination.exists()
    assert not paragraph_note.verification.path.exists()
    assert not bare.verification.path.exists()


def test_49i_existing_25a_25b_loop_resumes_after_first_v2_backed_edge(
    tmp_path: Path,
) -> None:
    (
        paragraph_note,
        bare,
        bare_path,
        working_set_path,
        prior_note_path,
        revision_path,
        continuation_path,
        loaded_continuation,
        _,
        first_edge_path,
        _,
    ) = _v2_backed_edge(
        tmp_path,
        extension_text="v4 first ordinary edge after continuation v2.",
    )
    loaded_first = load_chromium_research_working_set_note_revision_edge(
        loaded_continuation,
        first_edge_path,
    )

    extension = create_chromium_research_working_set_note_revision_edge_extension(
        loaded_first,
        revised_note_text="v5 through unchanged 25A.",
    )

    paragraph_note.verification.path.unlink(missing_ok=True)
    bare_path.unlink(missing_ok=True)
    working_set_path.unlink()
    prior_note_path.unlink()
    revision_path.unlink()
    continuation_path.unlink()

    successor_path = tmp_path / "successor-edge-v1.json"
    persisted_successor = persist_chromium_research_working_set_note_revision_edge_extension(
        extension,
        first_edge_path,
        successor_path,
    )
    verified_successor = verify_chromium_research_working_set_note_revision_edge(
        successor_path
    )

    assert persisted_successor.edge_format == _EDGE_FORMAT
    assert verified_successor.edge_format == _EDGE_FORMAT
    assert verified_successor.predecessor_format == _EDGE_FORMAT
    assert verified_successor.predecessor_record_sha256 == (
        loaded_first.verification.edge_record_sha256
    )

    loaded_successor = load_chromium_research_working_set_note_revision_edge(
        loaded_first,
        successor_path,
    )
    assert loaded_successor.predecessor is loaded_first
    assert loaded_successor.revision.prior_note is loaded_first.revision.revised_note
    assert loaded_successor.revision.revised_note.note_text == "v5 through unchanged 25A."
    assert not bare.verification.path.exists()


def test_49i_edge_lineage_introduces_no_second_edge_format(tmp_path: Path) -> None:
    *prefix, edge_path, _ = _v2_backed_edge(tmp_path)
    loaded_continuation = prefix[7]
    first = load_chromium_research_working_set_note_revision_edge(
        loaded_continuation,
        edge_path,
    )
    extension = create_chromium_research_working_set_note_revision_edge_extension(
        first,
        revised_note_text="another ordinary edge",
    )
    successor_path = tmp_path / "another-edge.json"
    persist_chromium_research_working_set_note_revision_edge_extension(
        extension,
        edge_path,
        successor_path,
    )

    assert verify_chromium_research_working_set_note_revision_edge(edge_path).edge_format == (
        _EDGE_FORMAT
    )
    assert verify_chromium_research_working_set_note_revision_edge(
        successor_path
    ).edge_format == _EDGE_FORMAT
