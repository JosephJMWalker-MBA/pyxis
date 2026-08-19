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
from pyxis.app.chromium_research_working_set_note_revision_continuation import (
    create_chromium_research_working_set_note_revision_continuation,
)
from pyxis.app.chromium_research_working_set_note_revision_continuation_extension import (
    create_chromium_research_working_set_note_revision_continuation_extension,
)
from pyxis.app.chromium_research_working_set_note_revision_continuation_persistence import (
    persist_chromium_research_working_set_note_revision_continuation,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_persistence import (
    ChromiumPageResearchWorkingSetNoteRevisionEdgePersistenceEvidence,
    ChromiumPageResearchWorkingSetNoteRevisionEdgeVerificationEvidence,
    ChromiumResearchWorkingSetNoteRevisionEdgeIntegrityError,
    persist_chromium_research_working_set_note_revision_edge,
    verify_chromium_research_working_set_note_revision_edge,
)


_EDGE_FORMAT = "pyxis.chromium.research_working_set_note_revision_edge.v1"
_CONTINUATION_FORMAT = (
    "pyxis.chromium.research_working_set_note_revision_continuation.v1"
)


def _durable_edge(
    tmp_path: Path,
    *,
    prior_text: str = "v1 rationale.",
    revised_text: str = "v2 rationale.",
    continued_text: str = "v3 rationale.",
    extension_text: str = "v4 rationale.",
):
    (
        paragraph_note,
        exact_note,
        comparison_note,
        working_set_path,
        prior_note_path,
        revision_path,
        continuation_path,
        loaded_revision,
        continuation,
        loaded_continuation,
    ) = _loaded_continuation(
        tmp_path,
        prior_text=prior_text,
        revised_text=revised_text,
        continued_text=continued_text,
    )
    extension = create_chromium_research_working_set_note_revision_continuation_extension(
        loaded_continuation,
        revised_note_text=extension_text,
    )
    edge_path = tmp_path / "revision-edge.json"
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
        exact_note,
        comparison_note,
        working_set_path,
        prior_note_path,
        revision_path,
        continuation_path,
        loaded_revision,
        continuation,
        loaded_continuation,
        extension,
        edge_path,
        persisted,
    )


def test_persist_revision_edge_records_only_predecessor_identity_and_v4_text(
    tmp_path: Path,
) -> None:
    (
        _,
        _,
        _,
        working_set_path,
        prior_note_path,
        revision_path,
        continuation_path,
        _,
        _,
        loaded_continuation,
        extension,
        edge_path,
        persisted,
    ) = _durable_edge(
        tmp_path,
        prior_text="v1 text that must not be copied.",
        revised_text="v2 text that must not be copied.",
        continued_text="v3 text that must not be copied.",
        extension_text="  v4 after another check 😀\nStill tentative.  ",
    )

    verified = verify_chromium_research_working_set_note_revision_edge(edge_path)
    document = json.loads(edge_path.read_text(encoding="utf-8"))

    assert isinstance(
        persisted,
        ChromiumPageResearchWorkingSetNoteRevisionEdgePersistenceEvidence,
    )
    assert isinstance(
        verified,
        ChromiumPageResearchWorkingSetNoteRevisionEdgeVerificationEvidence,
    )
    assert persisted.extension is extension
    assert persisted.edge_format == _EDGE_FORMAT
    assert verified.predecessor_format == _CONTINUATION_FORMAT
    assert verified.predecessor_record_sha256 == (
        loaded_continuation.verification.continuation_record_sha256
    )
    assert verified.edge_mode == "caller_authored_research_working_set_note_revision_edge"
    assert verified.revision_mode == (
        "caller_authored_revision_of_research_working_set_note"
    )
    assert verified.revised_note_mode == "caller_authored_note_on_research_working_set"
    assert verified.revised_note_text == extension.revision.revised_note.note_text
    assert document["edge_record"] == {
        "predecessor_reference": {
            "format": _CONTINUATION_FORMAT,
            "record_sha256": (
                loaded_continuation.verification.continuation_record_sha256
            ),
        },
        "edge": {
            "mode": "caller_authored_research_working_set_note_revision_edge",
            "revision": {
                "mode": "caller_authored_revision_of_research_working_set_note",
                "revised_note": {
                    "mode": "caller_authored_note_on_research_working_set",
                    "text": extension.revision.revised_note.note_text,
                },
            },
        },
    }

    raw_text = edge_path.read_text(encoding="utf-8")
    assert loaded_continuation.prior_revision.revision.prior_note.note_text not in raw_text
    assert loaded_continuation.prior_revision.revision.revised_note.note_text not in raw_text
    assert loaded_continuation.continuation.revision.revised_note.note_text not in raw_text
    assert "working_set_record_sha256" not in raw_text
    assert "note_record_sha256" not in raw_text
    assert "member_kind" not in raw_text
    assert "extension_mode" not in raw_text
    assert str(working_set_path.resolve()) not in raw_text
    assert str(prior_note_path.resolve()) not in raw_text
    assert str(revision_path.resolve()) not in raw_text
    assert str(continuation_path.resolve()) not in raw_text


def test_persist_revision_edge_uses_durable_identity_not_paths(tmp_path: Path) -> None:
    (
        _,
        _,
        _,
        working_set_path,
        prior_note_path,
        revision_path,
        continuation_path,
        _,
        _,
        loaded_continuation,
        extension,
        edge_path,
        _,
    ) = _durable_edge(tmp_path)
    edge_path.unlink()

    moved_working_set = tmp_path / "moved-working-set.json"
    moved_prior_note = tmp_path / "moved-prior-note.json"
    moved_revision = tmp_path / "moved-revision.json"
    moved_continuation = tmp_path / "moved-continuation.json"
    working_set_path.replace(moved_working_set)
    prior_note_path.replace(moved_prior_note)
    revision_path.replace(moved_revision)
    continuation_path.replace(moved_continuation)
    destination = tmp_path / "moved-edge.json"

    persist_chromium_research_working_set_note_revision_edge(
        extension,
        moved_working_set,
        moved_prior_note,
        moved_revision,
        moved_continuation,
        destination,
    )
    verified = verify_chromium_research_working_set_note_revision_edge(destination)

    assert verified.predecessor_record_sha256 == (
        loaded_continuation.verification.continuation_record_sha256
    )
    assert str(moved_working_set.resolve()) not in verified.document_json
    assert str(moved_prior_note.resolve()) not in verified.document_json
    assert str(moved_revision.resolve()) not in verified.document_json
    assert str(moved_continuation.resolve()) not in verified.document_json


def test_persist_revision_edge_rejects_different_valid_23b_predecessor_before_write(
    tmp_path: Path,
) -> None:
    (
        paragraph_note,
        exact_note,
        comparison_note,
        working_set_path,
        prior_note_path,
        revision_path,
        _,
        loaded_revision,
        _,
        _,
        extension,
        edge_path,
        _,
    ) = _durable_edge(
        tmp_path,
        continued_text="actual v3 predecessor",
        extension_text="v4 continuing the actual v3",
    )
    edge_path.unlink()

    other_continuation = create_chromium_research_working_set_note_revision_continuation(
        loaded_revision,
        revised_note_text="different but valid v3 predecessor",
    )
    other_continuation_path = tmp_path / "other-continuation.json"
    persist_chromium_research_working_set_note_revision_continuation(
        other_continuation,
        working_set_path,
        prior_note_path,
        revision_path,
        other_continuation_path,
    )
    destination = tmp_path / "edge-with-wrong-predecessor.json"

    with pytest.raises(
        ValueError,
        match="durable revision-edge predecessor does not match extension",
    ):
        persist_chromium_research_working_set_note_revision_edge(
            extension,
            working_set_path,
            prior_note_path,
            revision_path,
            other_continuation_path,
            destination,
        )

    assert not destination.exists()
    assert paragraph_note is not None
    assert exact_note is not None
    assert comparison_note is not None


def test_persist_revision_edge_does_not_reread_individual_member_sidecars(
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
        _,
        extension,
        edge_path,
        _,
    ) = _durable_edge(tmp_path)
    edge_path.unlink()

    paragraph_note.verification.path.unlink(missing_ok=True)
    exact_note.verification.path.unlink(missing_ok=True)
    comparison_note.verification.path.unlink(missing_ok=True)

    destination = tmp_path / "edge-after-member-sidecars-disappear.json"
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
    assert not exact_note.verification.path.exists()
    assert not comparison_note.verification.path.exists()


def test_persist_revision_edge_reestablishes_live_24a_contract_before_write(
    tmp_path: Path,
) -> None:
    (
        _,
        _,
        _,
        working_set_path,
        prior_note_path,
        revision_path,
        continuation_path,
        _,
        _,
        _,
        extension,
        edge_path,
        _,
    ) = _durable_edge(tmp_path)
    edge_path.unlink()
    forged = replace(extension, extension_mode="forged-extension-mode")
    destination = tmp_path / "forged-extension-edge.json"

    with pytest.raises(ValueError, match="extension mode is unsupported"):
        persist_chromium_research_working_set_note_revision_edge(
            forged,
            working_set_path,
            prior_note_path,
            revision_path,
            continuation_path,
            destination,
        )

    assert not destination.exists()


def test_verify_revision_edge_rejects_change_without_matching_digest(
    tmp_path: Path,
) -> None:
    *_, edge_path, _ = _durable_edge(tmp_path)
    document = json.loads(edge_path.read_text(encoding="utf-8"))
    document["edge_record"]["predecessor_reference"]["record_sha256"] = "f" * 64
    edge_path.write_bytes(_canonical_document_bytes(document))

    with pytest.raises(
        ChromiumResearchWorkingSetNoteRevisionEdgeIntegrityError,
        match="SHA-256",
    ):
        verify_chromium_research_working_set_note_revision_edge(edge_path)


def test_verify_revision_edge_accepts_recomputed_wrong_predecessor_identity(
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
    assert verified.predecessor_record_sha256 != (
        loaded_continuation.verification.continuation_record_sha256
    )


def test_verify_revision_edge_accepts_recomputed_v4_equal_to_real_v3(
    tmp_path: Path,
) -> None:
    v3_text = "the real v3 predecessor wording"
    *prefix, edge_path, _ = _durable_edge(
        tmp_path,
        continued_text=v3_text,
        extension_text="a genuinely different v4 at creation time",
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
    assert verified.revised_note_text == (
        loaded_continuation.continuation.revision.revised_note.note_text
    )


def test_verify_revision_edge_accepts_same_format_predecessor_shape_without_traversal(
    tmp_path: Path,
) -> None:
    *_, edge_path, _ = _durable_edge(tmp_path)
    document = json.loads(edge_path.read_text(encoding="utf-8"))
    hypothetical_prior_edge_digest = "a" * 64
    document["edge_record"]["predecessor_reference"] = {
        "format": _EDGE_FORMAT,
        "record_sha256": hypothetical_prior_edge_digest,
    }
    document["edge_record_sha256"] = hashlib.sha256(
        _canonical_bytes(document["edge_record"])
    ).hexdigest()
    edge_path.write_bytes(_canonical_document_bytes(document))

    verified = verify_chromium_research_working_set_note_revision_edge(edge_path)

    assert verified.predecessor_format == _EDGE_FORMAT
    assert verified.predecessor_record_sha256 == hypothetical_prior_edge_digest


def test_persist_revision_edge_is_deterministic_and_no_overwrite(tmp_path: Path) -> None:
    (
        _,
        _,
        _,
        working_set_path,
        prior_note_path,
        revision_path,
        continuation_path,
        _,
        _,
        _,
        extension,
        edge_path,
        first,
    ) = _durable_edge(tmp_path)
    second_path = tmp_path / "revision-edge-second.json"

    second = persist_chromium_research_working_set_note_revision_edge(
        extension,
        working_set_path,
        prior_note_path,
        revision_path,
        continuation_path,
        second_path,
    )

    assert first.edge_record_sha256 == second.edge_record_sha256
    assert edge_path.read_bytes() == second_path.read_bytes()

    original = edge_path.read_bytes()
    with pytest.raises(FileExistsError):
        persist_chromium_research_working_set_note_revision_edge(
            extension,
            working_set_path,
            prior_note_path,
            revision_path,
            continuation_path,
            edge_path,
        )
    assert edge_path.read_bytes() == original


def test_revision_edge_persistence_module_is_publicly_importable(tmp_path: Path) -> None:
    (
        _,
        _,
        _,
        working_set_path,
        prior_note_path,
        revision_path,
        continuation_path,
        _,
        _,
        _,
        extension,
        edge_path,
        persisted,
    ) = _durable_edge(
        tmp_path,
        extension_text="A durable general edge for another human wording.",
    )

    verified = verify_chromium_research_working_set_note_revision_edge(edge_path)
    assert persisted.extension is extension
    assert verified.revised_note_text == (
        "A durable general edge for another human wording."
    )

    other_path = tmp_path / "wrong-type-edge.json"
    with pytest.raises(TypeError, match="extension must be"):
        persist_chromium_research_working_set_note_revision_edge(  # type: ignore[arg-type]
            object(),
            working_set_path,
            prior_note_path,
            revision_path,
            continuation_path,
            other_path,
        )
