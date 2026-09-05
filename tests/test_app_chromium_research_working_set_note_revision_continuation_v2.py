from __future__ import annotations

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
from pyxis.app.chromium_research_working_set_note_revision_load import (
    load_chromium_research_working_set_note_revision,
)
from pyxis.app.chromium_research_working_set_note_revision_continuation import (
    create_chromium_research_working_set_note_revision_continuation,
)
from pyxis.app.chromium_research_working_set_note_revision_continuation_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord,
    ChromiumResearchWorkingSetNoteRevisionContinuationRelinkError,
    load_chromium_research_working_set_note_revision_continuation,
)
from pyxis.app.chromium_research_working_set_note_revision_continuation_persistence import (
    ChromiumResearchWorkingSetNoteRevisionContinuationIntegrityError,
    persist_chromium_research_working_set_note_revision_continuation,
    persist_chromium_research_working_set_note_revision_continuation_v2,
    verify_chromium_research_working_set_note_revision_continuation,
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


def _v2_continuation(
    tmp_path: Path,
    *,
    prior_text: str = "Initial durable v2 rationale.",
    revised_text: str = "First durable v2 revision.",
    continued_text: str = "Second durable v2 revision.",
):
    (
        paragraph_note,
        bare,
        bare_path,
        _,
        working_set_path,
        _,
        prior_note_path,
        _,
        _,
        revision_path,
        revision_persisted,
    ) = _durable_revision_v2(
        tmp_path,
        prior_text=prior_text,
        revised_text=revised_text,
    )
    loaded_revision = load_chromium_research_working_set_note_revision(
        (bare, paragraph_note, bare),
        working_set_path,
        prior_note_path,
        revision_path,
    )
    continuation = create_chromium_research_working_set_note_revision_continuation(
        loaded_revision,
        revised_note_text=continued_text,
    )
    return (
        paragraph_note,
        bare,
        bare_path,
        working_set_path,
        prior_note_path,
        revision_path,
        revision_persisted,
        loaded_revision,
        continuation,
    )


def test_49g_v2_continuation_persists_minimal_predecessor_identity_and_new_wording(
    tmp_path: Path,
) -> None:
    (
        paragraph_note,
        bare,
        _,
        working_set_path,
        prior_note_path,
        revision_path,
        revision_persisted,
        loaded_revision,
        continuation,
    ) = _v2_continuation(
        tmp_path,
        prior_text="Earlier note-v2 wording that must not be copied.",
        revised_text="Earlier revision-v2 wording that must not be copied.",
        continued_text="  Second v2-line revision 😀\nStill tentative.  ",
    )
    destination = tmp_path / "continuation-v2.json"

    persisted = persist_chromium_research_working_set_note_revision_continuation_v2(
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

    assert persisted.continuation is continuation
    assert persisted.continuation_format == (
        "pyxis.chromium.research_working_set_note_revision_continuation.v2"
    )
    assert verified.continuation_format == persisted.continuation_format
    assert verified.prior_revision_format == (
        "pyxis.chromium.research_working_set_note_revision.v2"
    )
    assert verified.prior_revision_record_sha256 == (
        revision_persisted.revision_record_sha256
    )
    assert document["continuation_record"] == {
        "prior_revision_reference": {
            "format": "pyxis.chromium.research_working_set_note_revision.v2",
            "revision_record_sha256": revision_persisted.revision_record_sha256,
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

    raw = destination.read_text(encoding="utf-8")
    assert loaded_revision.prior_note.note.note_text not in raw
    assert loaded_revision.revision.revised_note.note_text not in raw
    assert bare.selection.selected_text not in raw
    assert paragraph_note.note.note_text not in raw
    assert "working_set_record_sha256" not in raw
    assert "note_record_sha256" not in raw
    assert "member_kind" not in raw
    assert str(working_set_path.resolve()) not in raw
    assert str(prior_note_path.resolve()) not in raw
    assert str(revision_path.resolve()) not in raw


def test_49g_continuation_writers_do_not_auto_upgrade_or_downgrade(
    tmp_path: Path,
) -> None:
    (
        _,
        bare,
        _,
        working_set_path_v2,
        prior_note_path_v2,
        revision_path_v2,
        _,
        _,
        continuation_v2,
    ) = _v2_continuation(tmp_path)

    v1_destination = tmp_path / "continuation-v1-must-not-upgrade.json"
    with pytest.raises(
        ValueError,
        match="durable predecessor revision format is unsupported",
    ):
        persist_chromium_research_working_set_note_revision_continuation(
            continuation_v2,
            working_set_path_v2,
            prior_note_path_v2,
            revision_path_v2,
            v1_destination,
        )
    assert not v1_destination.exists()

    v1_fixture = tmp_path / "v1-line"
    v1_fixture.mkdir()
    (
        _,
        _,
        _,
        working_set_path_v1,
        prior_note_path_v1,
        revision_path_v1,
        loaded_v1,
    ) = _loaded_revision(v1_fixture)
    continuation_v1 = create_chromium_research_working_set_note_revision_continuation(
        loaded_v1,
        revised_note_text="A second v1-line human change.",
    )

    v2_destination = tmp_path / "continuation-v2-must-not-downgrade.json"
    with pytest.raises(
        ValueError,
        match="durable predecessor revision format is unsupported",
    ):
        persist_chromium_research_working_set_note_revision_continuation_v2(
            continuation_v1,
            working_set_path_v1,
            prior_note_path_v1,
            revision_path_v1,
            v2_destination,
        )
    assert not v2_destination.exists()
    assert bare.verification.selection_record_sha256


@pytest.mark.parametrize(
    ("continuation_format", "prior_revision_format"),
    [
        (
            "pyxis.chromium.research_working_set_note_revision_continuation.v1",
            "pyxis.chromium.research_working_set_note_revision.v2",
        ),
        (
            "pyxis.chromium.research_working_set_note_revision_continuation.v2",
            "pyxis.chromium.research_working_set_note_revision.v1",
        ),
    ],
)
def test_49g_verifier_rejects_cross_version_predecessor_pairing(
    tmp_path: Path,
    continuation_format: str,
    prior_revision_format: str,
) -> None:
    (
        _,
        _,
        _,
        working_set_path,
        prior_note_path,
        revision_path,
        _,
        _,
        continuation,
    ) = _v2_continuation(tmp_path)
    destination = tmp_path / "continuation-v2.json"
    persist_chromium_research_working_set_note_revision_continuation_v2(
        continuation,
        working_set_path,
        prior_note_path,
        revision_path,
        destination,
    )

    document = json.loads(destination.read_text(encoding="utf-8"))
    document["format"] = continuation_format
    document["continuation_record"]["prior_revision_reference"]["format"] = (
        prior_revision_format
    )
    document["continuation_record_sha256"] = hashlib.sha256(
        _canonical_bytes(document["continuation_record"])
    ).hexdigest()
    destination.write_bytes(_canonical_document_bytes(document))

    with pytest.raises(
        ChromiumResearchWorkingSetNoteRevisionContinuationIntegrityError,
        match="predecessor format is unsupported",
    ):
        verify_chromium_research_working_set_note_revision_continuation(destination)


def test_49g_23c_relinks_v2_continuation_to_exact_revision_v2_predecessor(
    tmp_path: Path,
) -> None:
    (
        paragraph_note,
        bare,
        _,
        working_set_path,
        prior_note_path,
        revision_path,
        _,
        _,
        continuation,
    ) = _v2_continuation(
        tmp_path,
        continued_text="Exact relinked second v2-line wording.",
    )
    continuation_path = tmp_path / "continuation-v2.json"
    persisted = persist_chromium_research_working_set_note_revision_continuation_v2(
        continuation,
        working_set_path,
        prior_note_path,
        revision_path,
        continuation_path,
    )

    loaded = load_chromium_research_working_set_note_revision_continuation(
        (bare, paragraph_note, bare),
        working_set_path,
        prior_note_path,
        revision_path,
        continuation_path,
    )

    assert isinstance(
        loaded,
        ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord,
    )
    assert loaded.verification.continuation_format == (
        "pyxis.chromium.research_working_set_note_revision_continuation.v2"
    )
    assert loaded.verification.continuation_record_sha256 == (
        persisted.continuation_record_sha256
    )
    assert loaded.prior_revision.verification.revision_format == (
        "pyxis.chromium.research_working_set_note_revision.v2"
    )
    assert loaded.continuation.prior_revision is loaded.prior_revision
    assert loaded.continuation.revision.prior_note is (
        loaded.prior_revision.revision.revised_note
    )
    assert loaded.continuation.revision.revised_note.note_text == (
        "Exact relinked second v2-line wording."
    )
    assert loaded.continuation.revision.revised_note.working_set.items[0] is bare
    assert loaded.continuation.revision.revised_note.working_set.items[1] is paragraph_note
    assert loaded.continuation.revision.revised_note.working_set.items[2] is bare


def test_49g_file_valid_wrong_predecessor_digest_fails_23c_relink(
    tmp_path: Path,
) -> None:
    (
        paragraph_note,
        bare,
        _,
        working_set_path,
        prior_note_path,
        revision_path,
        revision_persisted,
        _,
        continuation,
    ) = _v2_continuation(tmp_path)
    continuation_path = tmp_path / "continuation-v2.json"
    persist_chromium_research_working_set_note_revision_continuation_v2(
        continuation,
        working_set_path,
        prior_note_path,
        revision_path,
        continuation_path,
    )

    document = json.loads(continuation_path.read_text(encoding="utf-8"))
    wrong_digest = "f" * 64
    assert wrong_digest != revision_persisted.revision_record_sha256
    document["continuation_record"]["prior_revision_reference"][
        "revision_record_sha256"
    ] = wrong_digest
    document["continuation_record_sha256"] = hashlib.sha256(
        _canonical_bytes(document["continuation_record"])
    ).hexdigest()
    continuation_path.write_bytes(_canonical_document_bytes(document))

    verified = verify_chromium_research_working_set_note_revision_continuation(
        continuation_path
    )
    assert verified.prior_revision_record_sha256 == wrong_digest

    with pytest.raises(
        ChromiumResearchWorkingSetNoteRevisionContinuationRelinkError,
        match="different predecessor revision record",
    ):
        load_chromium_research_working_set_note_revision_continuation(
            (bare, paragraph_note, bare),
            working_set_path,
            prior_note_path,
            revision_path,
            continuation_path,
        )


def test_49g_file_valid_text_equal_to_real_predecessor_fails_23c_reconstruction(
    tmp_path: Path,
) -> None:
    predecessor_text = "The actual revision-v2 predecessor wording."
    (
        paragraph_note,
        bare,
        _,
        working_set_path,
        prior_note_path,
        revision_path,
        _,
        _,
        continuation,
    ) = _v2_continuation(
        tmp_path,
        revised_text=predecessor_text,
        continued_text="A genuinely different continuation at creation time.",
    )
    continuation_path = tmp_path / "continuation-v2.json"
    persist_chromium_research_working_set_note_revision_continuation_v2(
        continuation,
        working_set_path,
        prior_note_path,
        revision_path,
        continuation_path,
    )

    document = json.loads(continuation_path.read_text(encoding="utf-8"))
    document["continuation_record"]["continuation"]["revision"]["revised_note"][
        "text"
    ] = predecessor_text
    document["continuation_record_sha256"] = hashlib.sha256(
        _canonical_bytes(document["continuation_record"])
    ).hexdigest()
    continuation_path.write_bytes(_canonical_document_bytes(document))

    verified = verify_chromium_research_working_set_note_revision_continuation(
        continuation_path
    )
    assert verified.revised_note_text == predecessor_text

    with pytest.raises(
        ChromiumResearchWorkingSetNoteRevisionContinuationRelinkError,
        match="cannot be re-established as an actual continuation",
    ):
        load_chromium_research_working_set_note_revision_continuation(
            (bare, paragraph_note, bare),
            working_set_path,
            prior_note_path,
            revision_path,
            continuation_path,
        )


def test_49g_v2_persistence_and_relink_do_not_reread_member_sidecars(
    tmp_path: Path,
) -> None:
    (
        paragraph_note,
        bare,
        bare_path,
        working_set_path,
        prior_note_path,
        revision_path,
        _,
        _,
        continuation,
    ) = _v2_continuation(tmp_path)

    paragraph_note.verification.path.unlink(missing_ok=True)
    bare_path.unlink(missing_ok=True)

    continuation_path = tmp_path / "continuation-v2.json"
    persist_chromium_research_working_set_note_revision_continuation_v2(
        continuation,
        working_set_path,
        prior_note_path,
        revision_path,
        continuation_path,
    )
    loaded = load_chromium_research_working_set_note_revision_continuation(
        (bare, paragraph_note, bare),
        working_set_path,
        prior_note_path,
        revision_path,
        continuation_path,
    )

    assert loaded.continuation.revision.revised_note.working_set.items[0] is bare
    assert not paragraph_note.verification.path.exists()
    assert not bare.verification.path.exists()


def test_49g_v2_persistence_is_deterministic_and_no_overwrite(
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
        _,
        continuation,
    ) = _v2_continuation(tmp_path)
    first_path = tmp_path / "continuation-v2-a.json"
    second_path = tmp_path / "continuation-v2-b.json"

    first = persist_chromium_research_working_set_note_revision_continuation_v2(
        continuation,
        working_set_path,
        prior_note_path,
        revision_path,
        first_path,
    )
    second = persist_chromium_research_working_set_note_revision_continuation_v2(
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
        persist_chromium_research_working_set_note_revision_continuation_v2(
            continuation,
            working_set_path,
            prior_note_path,
            revision_path,
            first_path,
        )
    assert first_path.read_bytes() == original
