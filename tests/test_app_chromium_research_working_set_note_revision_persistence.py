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
from pyxis.app.chromium_research_working_set_note import (
    create_chromium_research_working_set_note,
)
from pyxis.app.chromium_research_working_set_note_persistence import (
    persist_chromium_research_working_set_note,
    persist_chromium_research_working_set_note_v2,
)
from pyxis.app.chromium_research_working_set_note_revision import (
    create_chromium_research_working_set_note_revision,
)
from pyxis.app.chromium_research_working_set_note_revision_persistence import (
    ChromiumPageResearchWorkingSetNoteRevisionPersistenceEvidence,
    ChromiumPageResearchWorkingSetNoteRevisionVerificationEvidence,
    ChromiumResearchWorkingSetNoteRevisionIntegrityError,
    persist_chromium_research_working_set_note_revision,
    persist_chromium_research_working_set_note_revision_v2,
    verify_chromium_research_working_set_note_revision,
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


def _durable_prior(tmp_path: Path, *, note_text: str = "Initial rationale."):
    paragraph_note, exact_note, comparison_note = _loaded_records(tmp_path)
    working_set = create_chromium_research_working_set(
        (paragraph_note, exact_note, comparison_note)
    )
    working_set_path = tmp_path / "working-set.json"
    persist_chromium_research_working_set(working_set, working_set_path)
    prior_note = create_chromium_research_working_set_note(
        working_set,
        note_text=note_text,
    )
    prior_note_path = tmp_path / "prior-note.json"
    prior_persisted = persist_chromium_research_working_set_note(
        prior_note,
        working_set_path,
        prior_note_path,
    )
    return (
        paragraph_note,
        exact_note,
        comparison_note,
        working_set,
        working_set_path,
        prior_note,
        prior_note_path,
        prior_persisted,
    )


def _durable_prior_v2(
    tmp_path: Path,
    *,
    note_text: str = "Initial v2 rationale.",
):
    paragraph_note, _, _ = _loaded_records(tmp_path)
    bare, bare_path = _loaded_bare_selection(tmp_path)
    working_set = create_chromium_research_working_set(
        (bare, paragraph_note, bare)
    )
    working_set_path = tmp_path / "working-set-v2.json"
    persist_chromium_research_working_set_v2(
        working_set,
        working_set_path,
    )
    prior_note = create_chromium_research_working_set_note(
        working_set,
        note_text=note_text,
    )
    prior_note_path = tmp_path / "prior-note-v2.json"
    prior_persisted = persist_chromium_research_working_set_note_v2(
        prior_note,
        working_set_path,
        prior_note_path,
    )
    return (
        paragraph_note,
        bare,
        bare_path,
        working_set,
        working_set_path,
        prior_note,
        prior_note_path,
        prior_persisted,
    )


def test_persist_revision_records_only_predecessor_identity_and_revised_human_wording(
    tmp_path: Path,
) -> None:
    (
        _,
        _,
        _,
        _,
        working_set_path,
        prior_note,
        prior_note_path,
        prior_persisted,
    ) = _durable_prior(tmp_path, note_text="Earlier interpretation that should not be copied.")
    revised_text = "  Revised interpretation after more reading 😀\nStill tentative.  "
    revision = create_chromium_research_working_set_note_revision(
        prior_note,
        revised_note_text=revised_text,
    )
    destination = tmp_path / "revision.json"

    persisted = persist_chromium_research_working_set_note_revision(
        revision,
        working_set_path,
        prior_note_path,
        destination,
    )
    verified = verify_chromium_research_working_set_note_revision(destination)
    document = json.loads(destination.read_text(encoding="utf-8"))

    assert isinstance(
        persisted,
        ChromiumPageResearchWorkingSetNoteRevisionPersistenceEvidence,
    )
    assert isinstance(
        verified,
        ChromiumPageResearchWorkingSetNoteRevisionVerificationEvidence,
    )
    assert persisted.revision is revision
    assert persisted.revision_format == (
        "pyxis.chromium.research_working_set_note_revision.v1"
    )
    assert verified.prior_note_record_sha256 == prior_persisted.note_record_sha256
    assert verified.revision_mode == (
        "caller_authored_revision_of_research_working_set_note"
    )
    assert verified.revised_note_mode == "caller_authored_note_on_research_working_set"
    assert verified.revised_note_text == revised_text
    assert document["revision_record"] == {
        "prior_note_reference": {
            "format": "pyxis.chromium.research_working_set_note.v1",
            "note_record_sha256": prior_persisted.note_record_sha256,
        },
        "revision": {
            "mode": "caller_authored_revision_of_research_working_set_note",
            "revised_note": {
                "mode": "caller_authored_note_on_research_working_set",
                "text": revised_text,
            },
        },
    }

    raw_text = destination.read_text(encoding="utf-8")
    assert prior_note.note_text not in raw_text
    assert "member_kind" not in raw_text
    assert "working_set_record_sha256" not in raw_text
    assert str(working_set_path.resolve()) not in raw_text
    assert str(prior_note_path.resolve()) not in raw_text


def test_persist_revision_uses_durable_identity_not_parent_paths(tmp_path: Path) -> None:
    (
        _,
        _,
        _,
        _,
        working_set_path,
        prior_note,
        prior_note_path,
        prior_persisted,
    ) = _durable_prior(tmp_path)
    moved_working_set = tmp_path / "moved-working-set.json"
    moved_prior_note = tmp_path / "moved-prior-note.json"
    working_set_path.replace(moved_working_set)
    prior_note_path.replace(moved_prior_note)
    revision = create_chromium_research_working_set_note_revision(
        prior_note,
        revised_note_text="The files moved; the human revision did not change.",
    )
    destination = tmp_path / "revision.json"

    persist_chromium_research_working_set_note_revision(
        revision,
        moved_working_set,
        moved_prior_note,
        destination,
    )
    verified = verify_chromium_research_working_set_note_revision(destination)

    assert verified.prior_note_record_sha256 == prior_persisted.note_record_sha256
    assert str(working_set_path.resolve()) not in verified.document_json
    assert str(prior_note_path.resolve()) not in verified.document_json
    assert str(moved_working_set.resolve()) not in verified.document_json
    assert str(moved_prior_note.resolve()) not in verified.document_json


def test_persist_revision_rejects_different_valid_predecessor_before_write(
    tmp_path: Path,
) -> None:
    (
        _,
        _,
        _,
        working_set,
        working_set_path,
        prior_note,
        _,
        _,
    ) = _durable_prior(tmp_path, note_text="The actual predecessor.")
    other_prior = create_chromium_research_working_set_note(
        working_set,
        note_text="A different but valid predecessor note.",
    )
    other_path = tmp_path / "other-prior-note.json"
    persist_chromium_research_working_set_note(
        other_prior,
        working_set_path,
        other_path,
    )
    revision = create_chromium_research_working_set_note_revision(
        prior_note,
        revised_note_text="Revision of the actual predecessor.",
    )
    destination = tmp_path / "revision.json"

    with pytest.raises(
        ValueError,
        match="durable predecessor note text does not match revision.prior_note",
    ):
        persist_chromium_research_working_set_note_revision(
            revision,
            working_set_path,
            other_path,
            destination,
        )

    assert not destination.exists()


def test_persist_revision_does_not_reread_individual_member_sidecars(
    tmp_path: Path,
) -> None:
    (
        paragraph_note,
        exact_note,
        comparison_note,
        _,
        working_set_path,
        prior_note,
        prior_note_path,
        _,
    ) = _durable_prior(tmp_path)
    revision = create_chromium_research_working_set_note_revision(
        prior_note,
        revised_note_text="Revision survives member-sidecar disappearance.",
    )

    paragraph_note.verification.path.unlink()
    exact_note.verification.path.unlink()
    comparison_note.verification.path.unlink()

    destination = tmp_path / "revision.json"
    persisted = persist_chromium_research_working_set_note_revision(
        revision,
        working_set_path,
        prior_note_path,
        destination,
    )

    assert persisted.revision is revision
    assert destination.exists()
    assert not paragraph_note.verification.path.exists()
    assert not exact_note.verification.path.exists()
    assert not comparison_note.verification.path.exists()


def test_verify_revision_rejects_change_without_matching_digest(tmp_path: Path) -> None:
    (
        _,
        _,
        _,
        _,
        working_set_path,
        prior_note,
        prior_note_path,
        _,
    ) = _durable_prior(tmp_path)
    revision = create_chromium_research_working_set_note_revision(
        prior_note,
        revised_note_text="Original revised wording.",
    )
    destination = tmp_path / "revision.json"
    persist_chromium_research_working_set_note_revision(
        revision,
        working_set_path,
        prior_note_path,
        destination,
    )

    document = json.loads(destination.read_text(encoding="utf-8"))
    document["revision_record"]["prior_note_reference"]["note_record_sha256"] = (
        "f" * 64
    )
    destination.write_bytes(_canonical_document_bytes(document))

    with pytest.raises(
        ChromiumResearchWorkingSetNoteRevisionIntegrityError,
        match="SHA-256",
    ):
        verify_chromium_research_working_set_note_revision(destination)


def test_verify_revision_accepts_recomputed_self_consistent_wrong_predecessor_identity(
    tmp_path: Path,
) -> None:
    (
        _,
        _,
        _,
        _,
        working_set_path,
        prior_note,
        prior_note_path,
        prior_persisted,
    ) = _durable_prior(tmp_path)
    revision = create_chromium_research_working_set_note_revision(
        prior_note,
        revised_note_text="Predecessor identity correctness is earned later.",
    )
    destination = tmp_path / "revision.json"
    persist_chromium_research_working_set_note_revision(
        revision,
        working_set_path,
        prior_note_path,
        destination,
    )

    document = json.loads(destination.read_text(encoding="utf-8"))
    wrong_digest = "f" * 64
    assert wrong_digest != prior_persisted.note_record_sha256
    document["revision_record"]["prior_note_reference"]["note_record_sha256"] = (
        wrong_digest
    )
    document["revision_record_sha256"] = hashlib.sha256(
        _canonical_bytes(document["revision_record"])
    ).hexdigest()
    destination.write_bytes(_canonical_document_bytes(document))

    verified = verify_chromium_research_working_set_note_revision(destination)

    assert verified.prior_note_record_sha256 == wrong_digest
    assert verified.prior_note_record_sha256 != prior_persisted.note_record_sha256


def test_verify_revision_accepts_recomputed_text_equal_to_real_predecessor(
    tmp_path: Path,
) -> None:
    prior_text = "The real predecessor wording."
    (
        _,
        _,
        _,
        _,
        working_set_path,
        prior_note,
        prior_note_path,
        _,
    ) = _durable_prior(tmp_path, note_text=prior_text)
    revision = create_chromium_research_working_set_note_revision(
        prior_note,
        revised_note_text="A genuinely different revision at creation time.",
    )
    destination = tmp_path / "revision.json"
    persist_chromium_research_working_set_note_revision(
        revision,
        working_set_path,
        prior_note_path,
        destination,
    )

    document = json.loads(destination.read_text(encoding="utf-8"))
    document["revision_record"]["revision"]["revised_note"]["text"] = prior_text
    document["revision_record_sha256"] = hashlib.sha256(
        _canonical_bytes(document["revision_record"])
    ).hexdigest()
    destination.write_bytes(_canonical_document_bytes(document))

    verified = verify_chromium_research_working_set_note_revision(destination)

    assert verified.revised_note_text == prior_text
    assert verified.revised_note_text == prior_note.note_text


def test_persist_revision_is_deterministic_and_no_overwrite(tmp_path: Path) -> None:
    (
        _,
        _,
        _,
        _,
        working_set_path,
        prior_note,
        prior_note_path,
        _,
    ) = _durable_prior(tmp_path)
    revision = create_chromium_research_working_set_note_revision(
        prior_note,
        revised_note_text="Exact same durable revision action.",
    )
    first_path = tmp_path / "revision-a.json"
    second_path = tmp_path / "revision-b.json"

    first = persist_chromium_research_working_set_note_revision(
        revision,
        working_set_path,
        prior_note_path,
        first_path,
    )
    second = persist_chromium_research_working_set_note_revision(
        revision,
        working_set_path,
        prior_note_path,
        second_path,
    )

    assert first.revision_record_sha256 == second.revision_record_sha256
    assert first_path.read_bytes() == second_path.read_bytes()

    original = first_path.read_bytes()
    with pytest.raises(FileExistsError):
        persist_chromium_research_working_set_note_revision(
            revision,
            working_set_path,
            prior_note_path,
            first_path,
        )
    assert first_path.read_bytes() == original


def test_working_set_note_revision_persistence_module_is_publicly_importable(
    tmp_path: Path,
) -> None:
    (
        _,
        _,
        _,
        _,
        working_set_path,
        prior_note,
        prior_note_path,
        _,
    ) = _durable_prior(tmp_path)
    revision = create_chromium_research_working_set_note_revision(
        prior_note,
        revised_note_text="Durable human revision only.",
    )
    destination = tmp_path / "revision.json"

    persisted = persist_chromium_research_working_set_note_revision(
        revision,
        working_set_path,
        prior_note_path,
        destination,
    )
    verified = verify_chromium_research_working_set_note_revision(destination)

    assert persisted.revision is revision
    assert verified.revised_note_text == "Durable human revision only."


def test_49e_revision_v1_persistence_rejects_v2_note_predecessor(
    tmp_path: Path,
) -> None:
    bare, _ = _loaded_bare_selection(tmp_path)
    working_set = create_chromium_research_working_set((bare,))
    working_set_path = tmp_path / "working-set-v2.json"
    persist_chromium_research_working_set_v2(
        working_set,
        working_set_path,
    )
    prior_note = create_chromium_research_working_set_note(
        working_set,
        note_text="Durable v2 rationale predecessor.",
    )
    prior_note_path = tmp_path / "working-set-note-v2.json"
    persist_chromium_research_working_set_note_v2(
        prior_note,
        working_set_path,
        prior_note_path,
    )
    revision = create_chromium_research_working_set_note_revision(
        prior_note,
        revised_note_text="A later interpretation that needs its own versioned boundary.",
    )
    destination = tmp_path / "revision-v1-must-not-write.json"

    with pytest.raises(
        ValueError,
        match="durable predecessor note format is unsupported",
    ):
        persist_chromium_research_working_set_note_revision(
            revision,
            working_set_path,
            prior_note_path,
            destination,
        )

    assert not destination.exists()


def test_49f_v2_revision_persists_only_predecessor_identity_and_new_wording(
    tmp_path: Path,
) -> None:
    (
        paragraph_note,
        bare,
        _,
        _,
        working_set_path,
        prior_note,
        prior_note_path,
        prior_persisted,
    ) = _durable_prior_v2(
        tmp_path,
        note_text="Earlier v2 rationale that must not be copied.",
    )
    revised_text = "  Revised v2 interpretation after more reading 😀\nStill uncertain.  "
    revision = create_chromium_research_working_set_note_revision(
        prior_note,
        revised_note_text=revised_text,
    )
    destination = tmp_path / "revision-v2.json"

    persisted = persist_chromium_research_working_set_note_revision_v2(
        revision,
        working_set_path,
        prior_note_path,
        destination,
    )
    verified = verify_chromium_research_working_set_note_revision(destination)
    document = json.loads(destination.read_text(encoding="utf-8"))

    assert persisted.revision is revision
    assert persisted.revision_format == (
        "pyxis.chromium.research_working_set_note_revision.v2"
    )
    assert verified.revision_format == persisted.revision_format
    assert verified.prior_note_format == (
        "pyxis.chromium.research_working_set_note.v2"
    )
    assert verified.prior_note_record_sha256 == prior_persisted.note_record_sha256
    assert verified.revised_note_text == revised_text
    assert document["revision_record"] == {
        "prior_note_reference": {
            "format": "pyxis.chromium.research_working_set_note.v2",
            "note_record_sha256": prior_persisted.note_record_sha256,
        },
        "revision": {
            "mode": "caller_authored_revision_of_research_working_set_note",
            "revised_note": {
                "mode": "caller_authored_note_on_research_working_set",
                "text": revised_text,
            },
        },
    }

    raw = destination.read_text(encoding="utf-8")
    assert prior_note.note_text not in raw
    assert bare.selection.selected_text not in raw
    assert paragraph_note.note.note_text not in raw
    assert "working_set_record_sha256" not in raw
    assert "member_kind" not in raw
    assert str(working_set_path.resolve()) not in raw
    assert str(prior_note_path.resolve()) not in raw


def test_49f_revision_writers_do_not_auto_upgrade_or_downgrade(
    tmp_path: Path,
) -> None:
    (
        _,
        _,
        _,
        _,
        v1_working_set_path,
        v1_prior_note,
        v1_prior_note_path,
        _,
    ) = _durable_prior(tmp_path)
    v1_revision = create_chromium_research_working_set_note_revision(
        v1_prior_note,
        revised_note_text="new v1 revision",
    )

    (
        _,
        _,
        _,
        _,
        v2_working_set_path,
        v2_prior_note,
        v2_prior_note_path,
        _,
    ) = _durable_prior_v2(tmp_path)
    v2_revision = create_chromium_research_working_set_note_revision(
        v2_prior_note,
        revised_note_text="new v2 revision",
    )

    v1_destination = tmp_path / "revision-v1-must-not-upgrade.json"
    with pytest.raises(ValueError, match="durable predecessor note format is unsupported"):
        persist_chromium_research_working_set_note_revision(
            v2_revision,
            v2_working_set_path,
            v2_prior_note_path,
            v1_destination,
        )
    assert not v1_destination.exists()

    v2_destination = tmp_path / "revision-v2-must-not-downgrade.json"
    with pytest.raises(ValueError, match="durable predecessor note format is unsupported"):
        persist_chromium_research_working_set_note_revision_v2(
            v1_revision,
            v1_working_set_path,
            v1_prior_note_path,
            v2_destination,
        )
    assert not v2_destination.exists()


@pytest.mark.parametrize(
    ("revision_format", "prior_note_format"),
    [
        (
            "pyxis.chromium.research_working_set_note_revision.v1",
            "pyxis.chromium.research_working_set_note.v2",
        ),
        (
            "pyxis.chromium.research_working_set_note_revision.v2",
            "pyxis.chromium.research_working_set_note.v1",
        ),
    ],
)
def test_49f_verifier_rejects_cross_version_predecessor_pairing(
    tmp_path: Path,
    revision_format: str,
    prior_note_format: str,
) -> None:
    (
        _,
        _,
        _,
        _,
        working_set_path,
        prior_note,
        prior_note_path,
        _,
    ) = _durable_prior(tmp_path)
    revision = create_chromium_research_working_set_note_revision(
        prior_note,
        revised_note_text="A real revision.",
    )
    destination = tmp_path / "revision.json"
    persist_chromium_research_working_set_note_revision(
        revision,
        working_set_path,
        prior_note_path,
        destination,
    )

    document = json.loads(destination.read_text(encoding="utf-8"))
    document["format"] = revision_format
    document["revision_record"]["prior_note_reference"]["format"] = prior_note_format
    document["revision_record_sha256"] = hashlib.sha256(
        _canonical_bytes(document["revision_record"])
    ).hexdigest()
    destination.write_bytes(_canonical_document_bytes(document))

    with pytest.raises(
        ChromiumResearchWorkingSetNoteRevisionIntegrityError,
        match="predecessor format is unsupported",
    ):
        verify_chromium_research_working_set_note_revision(destination)


def test_49f_v2_revision_persistence_does_not_reread_member_sidecars(
    tmp_path: Path,
) -> None:
    (
        paragraph_note,
        bare,
        bare_path,
        _,
        working_set_path,
        prior_note,
        prior_note_path,
        _,
    ) = _durable_prior_v2(tmp_path)
    revision = create_chromium_research_working_set_note_revision(
        prior_note,
        revised_note_text="Revision can use retained loaded member evidence.",
    )

    paragraph_note.verification.path.unlink()
    bare_path.unlink()

    destination = tmp_path / "revision-v2.json"
    persisted = persist_chromium_research_working_set_note_revision_v2(
        revision,
        working_set_path,
        prior_note_path,
        destination,
    )

    assert persisted.revision is revision
    assert destination.exists()
    assert not paragraph_note.verification.path.exists()
    assert not bare.verification.path.exists()
