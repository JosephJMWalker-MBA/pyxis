from __future__ import annotations

from dataclasses import replace
import hashlib
import json
from pathlib import Path

import pytest

from test_app_chromium_research_working_set_note_revision_continuation import (
    _loaded_revision,
)
from test_app_chromium_research_working_set_note_revision_load import (
    _durable_revision_v2,
)
from pyxis.app.chromium_research_working_set_note_revision import (
    create_chromium_research_working_set_note_revision,
)
from pyxis.app.chromium_research_working_set_note_revision_load import (
    load_chromium_research_working_set_note_revision,
)
from pyxis.app.chromium_research_working_set_note_revision_continuation import (
    create_chromium_research_working_set_note_revision_continuation,
)
from pyxis.app.chromium_research_working_set_note_revision_continuation_persistence import (
    ChromiumPageResearchWorkingSetNoteRevisionContinuationPersistenceEvidence,
    ChromiumPageResearchWorkingSetNoteRevisionContinuationVerificationEvidence,
    ChromiumResearchWorkingSetNoteRevisionContinuationIntegrityError,
    persist_chromium_research_working_set_note_revision_continuation,
    verify_chromium_research_working_set_note_revision_continuation,
)
from pyxis.app.chromium_research_working_set_note_revision_persistence import (
    persist_chromium_research_working_set_note_revision,
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


def _durable_continuation(
    tmp_path: Path,
    *,
    prior_text: str = "v1 rationale.",
    revised_text: str = "v2 rationale.",
    continued_text: str = "v3 rationale.",
):
    (
        paragraph_note,
        exact_note,
        comparison_note,
        working_set_path,
        prior_note_path,
        revision_path,
        loaded,
    ) = _loaded_revision(
        tmp_path,
        prior_text=prior_text,
        revised_text=revised_text,
    )
    continuation = create_chromium_research_working_set_note_revision_continuation(
        loaded,
        revised_note_text=continued_text,
    )
    return (
        paragraph_note,
        exact_note,
        comparison_note,
        working_set_path,
        prior_note_path,
        revision_path,
        loaded,
        continuation,
    )


def test_persist_continuation_records_only_predecessor_revision_identity_and_v3_text(
    tmp_path: Path,
) -> None:
    (
        _,
        _,
        _,
        working_set_path,
        prior_note_path,
        revision_path,
        loaded,
        continuation,
    ) = _durable_continuation(
        tmp_path,
        prior_text="Earlier v1 text that must not be copied.",
        revised_text="Earlier v2 text that must not be copied.",
        continued_text="  v3 after more reading 😀\nStill tentative.  ",
    )
    destination = tmp_path / "continuation.json"

    persisted = persist_chromium_research_working_set_note_revision_continuation(
        continuation,
        working_set_path,
        prior_note_path,
        revision_path,
        destination,
    )
    verified = verify_chromium_research_working_set_note_revision_continuation(
        destination
    )
    document = json.loads(destination.read_text(encoding="utf-8"))

    assert isinstance(
        persisted,
        ChromiumPageResearchWorkingSetNoteRevisionContinuationPersistenceEvidence,
    )
    assert isinstance(
        verified,
        ChromiumPageResearchWorkingSetNoteRevisionContinuationVerificationEvidence,
    )
    assert persisted.continuation is continuation
    assert persisted.continuation_format == (
        "pyxis.chromium.research_working_set_note_revision_continuation.v1"
    )
    assert verified.prior_revision_record_sha256 == (
        loaded.verification.revision_record_sha256
    )
    assert verified.continuation_mode == (
        "caller_authored_continuation_of_verified_research_working_set_note_revision"
    )
    assert verified.revision_mode == (
        "caller_authored_revision_of_research_working_set_note"
    )
    assert verified.revised_note_mode == "caller_authored_note_on_research_working_set"
    assert verified.revised_note_text == continuation.revision.revised_note.note_text
    assert document["continuation_record"] == {
        "prior_revision_reference": {
            "format": "pyxis.chromium.research_working_set_note_revision.v1",
            "revision_record_sha256": loaded.verification.revision_record_sha256,
        },
        "continuation": {
            "mode": (
                "caller_authored_continuation_of_verified_research_working_set_note_revision"
            ),
            "revision": {
                "mode": "caller_authored_revision_of_research_working_set_note",
                "revised_note": {
                    "mode": "caller_authored_note_on_research_working_set",
                    "text": continuation.revision.revised_note.note_text,
                },
            },
        },
    }

    raw_text = destination.read_text(encoding="utf-8")
    assert loaded.revision.prior_note.note_text not in raw_text
    assert loaded.revision.revised_note.note_text not in raw_text
    assert "working_set_record_sha256" not in raw_text
    assert "note_record_sha256" not in raw_text
    assert "member_kind" not in raw_text
    assert str(working_set_path.resolve()) not in raw_text
    assert str(prior_note_path.resolve()) not in raw_text
    assert str(revision_path.resolve()) not in raw_text


def test_persist_continuation_uses_durable_identity_not_paths(tmp_path: Path) -> None:
    (
        _,
        _,
        _,
        working_set_path,
        prior_note_path,
        revision_path,
        loaded,
        continuation,
    ) = _durable_continuation(tmp_path)
    moved_working_set = tmp_path / "moved-working-set.json"
    moved_prior_note = tmp_path / "moved-prior-note.json"
    moved_revision = tmp_path / "moved-revision.json"
    working_set_path.replace(moved_working_set)
    prior_note_path.replace(moved_prior_note)
    revision_path.replace(moved_revision)
    destination = tmp_path / "continuation.json"

    persist_chromium_research_working_set_note_revision_continuation(
        continuation,
        moved_working_set,
        moved_prior_note,
        moved_revision,
        destination,
    )
    verified = verify_chromium_research_working_set_note_revision_continuation(
        destination
    )

    assert verified.prior_revision_record_sha256 == (
        loaded.verification.revision_record_sha256
    )
    assert str(moved_working_set.resolve()) not in verified.document_json
    assert str(moved_prior_note.resolve()) not in verified.document_json
    assert str(moved_revision.resolve()) not in verified.document_json


def test_persist_continuation_rejects_different_valid_predecessor_before_write(
    tmp_path: Path,
) -> None:
    (
        _,
        _,
        _,
        working_set_path,
        prior_note_path,
        _,
        loaded,
        continuation,
    ) = _durable_continuation(
        tmp_path,
        revised_text="the actual v2 predecessor",
        continued_text="v3 continuing the actual v2",
    )
    other_revision = create_chromium_research_working_set_note_revision(
        loaded.prior_note.note,
        revised_note_text="a different but valid v2 predecessor",
    )
    other_revision_path = tmp_path / "other-revision.json"
    persist_chromium_research_working_set_note_revision(
        other_revision,
        working_set_path,
        prior_note_path,
        other_revision_path,
    )
    destination = tmp_path / "continuation.json"

    with pytest.raises(
        ValueError,
        match="durable predecessor revision does not match continuation",
    ):
        persist_chromium_research_working_set_note_revision_continuation(
            continuation,
            working_set_path,
            prior_note_path,
            other_revision_path,
            destination,
        )

    assert not destination.exists()


def test_persist_continuation_does_not_reread_individual_member_sidecars(
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
        continuation,
    ) = _durable_continuation(tmp_path)

    paragraph_note.verification.path.unlink(missing_ok=True)
    exact_note.verification.path.unlink(missing_ok=True)
    comparison_note.verification.path.unlink(missing_ok=True)

    destination = tmp_path / "continuation.json"
    persisted = persist_chromium_research_working_set_note_revision_continuation(
        continuation,
        working_set_path,
        prior_note_path,
        revision_path,
        destination,
    )

    assert persisted.continuation is continuation
    assert destination.exists()
    assert not paragraph_note.verification.path.exists()
    assert not exact_note.verification.path.exists()
    assert not comparison_note.verification.path.exists()


def test_persist_continuation_reestablishes_live_23a_contract_before_write(
    tmp_path: Path,
) -> None:
    (
        _,
        _,
        _,
        working_set_path,
        prior_note_path,
        revision_path,
        _,
        continuation,
    ) = _durable_continuation(tmp_path)
    forged = replace(continuation, continuation_mode="forged-continuation-mode")
    destination = tmp_path / "continuation.json"

    with pytest.raises(ValueError, match="mode is unsupported for persistence"):
        persist_chromium_research_working_set_note_revision_continuation(
            forged,
            working_set_path,
            prior_note_path,
            revision_path,
            destination,
        )

    assert not destination.exists()


def test_verify_continuation_rejects_change_without_matching_digest(
    tmp_path: Path,
) -> None:
    (
        _,
        _,
        _,
        working_set_path,
        prior_note_path,
        revision_path,
        _,
        continuation,
    ) = _durable_continuation(tmp_path)
    destination = tmp_path / "continuation.json"
    persist_chromium_research_working_set_note_revision_continuation(
        continuation,
        working_set_path,
        prior_note_path,
        revision_path,
        destination,
    )

    document = json.loads(destination.read_text(encoding="utf-8"))
    document["continuation_record"]["prior_revision_reference"][
        "revision_record_sha256"
    ] = "f" * 64
    destination.write_bytes(_canonical_document_bytes(document))

    with pytest.raises(
        ChromiumResearchWorkingSetNoteRevisionContinuationIntegrityError,
        match="SHA-256",
    ):
        verify_chromium_research_working_set_note_revision_continuation(destination)


def test_verify_continuation_accepts_recomputed_self_consistent_wrong_predecessor_identity(
    tmp_path: Path,
) -> None:
    (
        _,
        _,
        _,
        working_set_path,
        prior_note_path,
        revision_path,
        loaded,
        continuation,
    ) = _durable_continuation(tmp_path)
    destination = tmp_path / "continuation.json"
    persist_chromium_research_working_set_note_revision_continuation(
        continuation,
        working_set_path,
        prior_note_path,
        revision_path,
        destination,
    )

    document = json.loads(destination.read_text(encoding="utf-8"))
    wrong_digest = "f" * 64
    assert wrong_digest != loaded.verification.revision_record_sha256
    document["continuation_record"]["prior_revision_reference"][
        "revision_record_sha256"
    ] = wrong_digest
    document["continuation_record_sha256"] = hashlib.sha256(
        _canonical_bytes(document["continuation_record"])
    ).hexdigest()
    destination.write_bytes(_canonical_document_bytes(document))

    verified = verify_chromium_research_working_set_note_revision_continuation(
        destination
    )

    assert verified.prior_revision_record_sha256 == wrong_digest
    assert verified.prior_revision_record_sha256 != (
        loaded.verification.revision_record_sha256
    )


def test_verify_continuation_accepts_recomputed_v3_text_equal_to_real_v2(
    tmp_path: Path,
) -> None:
    v2_text = "the real v2 predecessor wording"
    (
        _,
        _,
        _,
        working_set_path,
        prior_note_path,
        revision_path,
        loaded,
        continuation,
    ) = _durable_continuation(
        tmp_path,
        revised_text=v2_text,
        continued_text="a genuinely different v3 at creation time",
    )
    destination = tmp_path / "continuation.json"
    persist_chromium_research_working_set_note_revision_continuation(
        continuation,
        working_set_path,
        prior_note_path,
        revision_path,
        destination,
    )

    document = json.loads(destination.read_text(encoding="utf-8"))
    document["continuation_record"]["continuation"]["revision"]["revised_note"][
        "text"
    ] = v2_text
    document["continuation_record_sha256"] = hashlib.sha256(
        _canonical_bytes(document["continuation_record"])
    ).hexdigest()
    destination.write_bytes(_canonical_document_bytes(document))

    verified = verify_chromium_research_working_set_note_revision_continuation(
        destination
    )

    assert verified.revised_note_text == v2_text
    assert verified.revised_note_text == loaded.revision.revised_note.note_text


def test_persist_continuation_is_deterministic_and_no_overwrite(tmp_path: Path) -> None:
    (
        _,
        _,
        _,
        working_set_path,
        prior_note_path,
        revision_path,
        _,
        continuation,
    ) = _durable_continuation(tmp_path)
    first_path = tmp_path / "continuation-a.json"
    second_path = tmp_path / "continuation-b.json"

    first = persist_chromium_research_working_set_note_revision_continuation(
        continuation,
        working_set_path,
        prior_note_path,
        revision_path,
        first_path,
    )
    second = persist_chromium_research_working_set_note_revision_continuation(
        continuation,
        working_set_path,
        prior_note_path,
        revision_path,
        second_path,
    )

    assert first.continuation_record_sha256 == second.continuation_record_sha256
    assert first_path.read_bytes() == second_path.read_bytes()

    original = first_path.read_bytes()
    with pytest.raises(FileExistsError):
        persist_chromium_research_working_set_note_revision_continuation(
            continuation,
            working_set_path,
            prior_note_path,
            revision_path,
            first_path,
        )
    assert first_path.read_bytes() == original


def test_revision_continuation_persistence_module_is_publicly_importable(
    tmp_path: Path,
) -> None:
    (
        _,
        _,
        _,
        working_set_path,
        prior_note_path,
        revision_path,
        _,
        continuation,
    ) = _durable_continuation(
        tmp_path,
        continued_text="A durable explicit second human change of wording.",
    )
    destination = tmp_path / "continuation.json"

    persisted = persist_chromium_research_working_set_note_revision_continuation(
        continuation,
        working_set_path,
        prior_note_path,
        revision_path,
        destination,
    )
    verified = verify_chromium_research_working_set_note_revision_continuation(
        destination
    )

    assert persisted.continuation is continuation
    assert verified.revised_note_text == (
        "A durable explicit second human change of wording."
    )


def test_49f_continuation_v1_persistence_rejects_revision_v2_predecessor(
    tmp_path: Path,
) -> None:
    (
        paragraph_note,
        bare,
        _,
        _,
        working_set_path,
        _,
        prior_note_path,
        _,
        _,
        revision_path,
        _,
    ) = _durable_revision_v2(tmp_path)
    loaded = load_chromium_research_working_set_note_revision(
        (bare, paragraph_note, bare),
        working_set_path,
        prior_note_path,
        revision_path,
    )
    continuation = create_chromium_research_working_set_note_revision_continuation(
        loaded,
        revised_note_text="A second v2-line human revision needs its own continuation version.",
    )
    destination = tmp_path / "continuation-v1-must-not-write.json"

    with pytest.raises(
        ValueError,
        match="durable predecessor revision format is unsupported",
    ):
        persist_chromium_research_working_set_note_revision_continuation(
            continuation,
            working_set_path,
            prior_note_path,
            revision_path,
            destination,
        )

    assert not destination.exists()
