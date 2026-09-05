from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from test_app_chromium_research_working_set_note_revision_persistence import (
    _canonical_bytes,
    _canonical_document_bytes,
    _durable_prior,
    _durable_prior_v2,
)
from pyxis.app.chromium_research_working_set_note import (
    create_chromium_research_working_set_note,
)
from pyxis.app.chromium_research_working_set_note_persistence import (
    persist_chromium_research_working_set_note,
)
from pyxis.app.chromium_research_working_set_note_revision import (
    create_chromium_research_working_set_note_revision,
)
from pyxis.app.chromium_research_working_set_note_revision_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionRecord,
    ChromiumResearchWorkingSetNoteRevisionRelinkError,
    load_chromium_research_working_set_note_revision,
)
from pyxis.app.chromium_research_working_set_note_revision_persistence import (
    ChromiumResearchWorkingSetNoteRevisionIntegrityError,
    persist_chromium_research_working_set_note_revision,
    persist_chromium_research_working_set_note_revision_v2,
    verify_chromium_research_working_set_note_revision,
)


def _durable_revision(
    tmp_path: Path,
    *,
    prior_text: str = "Initial durable rationale.",
    revised_text: str = "Revised durable rationale.",
):
    (
        paragraph_note,
        exact_note,
        comparison_note,
        working_set,
        working_set_path,
        prior_note,
        prior_note_path,
        prior_persisted,
    ) = _durable_prior(tmp_path, note_text=prior_text)
    revision = create_chromium_research_working_set_note_revision(
        prior_note,
        revised_note_text=revised_text,
    )
    revision_path = tmp_path / "revision.json"
    revision_persisted = persist_chromium_research_working_set_note_revision(
        revision,
        working_set_path,
        prior_note_path,
        revision_path,
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
        revision,
        revision_path,
        revision_persisted,
    )


def _durable_revision_v2(
    tmp_path: Path,
    *,
    prior_text: str = "Initial durable v2 rationale.",
    revised_text: str = "Revised durable v2 rationale.",
):
    (
        paragraph_note,
        bare,
        bare_path,
        working_set,
        working_set_path,
        prior_note,
        prior_note_path,
        prior_persisted,
    ) = _durable_prior_v2(tmp_path, note_text=prior_text)
    revision = create_chromium_research_working_set_note_revision(
        prior_note,
        revised_note_text=revised_text,
    )
    revision_path = tmp_path / "revision-v2.json"
    revision_persisted = persist_chromium_research_working_set_note_revision_v2(
        revision,
        working_set_path,
        prior_note_path,
        revision_path,
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
        revision,
        revision_path,
        revision_persisted,
    )


def test_load_revision_relinks_moved_files_and_reconstructs_exact_revision(
    tmp_path: Path,
) -> None:
    revised_text = "  Revised interpretation after fresh reading 😀\nStill human-owned.  "
    (
        paragraph_note,
        exact_note,
        comparison_note,
        _,
        working_set_path,
        _,
        prior_note_path,
        _,
        _,
        revision_path,
        revision_persisted,
    ) = _durable_revision(tmp_path, revised_text=revised_text)

    moved_working_set = tmp_path / "moved-working-set.json"
    moved_prior_note = tmp_path / "moved-prior-note.json"
    moved_revision = tmp_path / "moved-revision.json"
    working_set_path.replace(moved_working_set)
    prior_note_path.replace(moved_prior_note)
    revision_path.replace(moved_revision)

    loaded = load_chromium_research_working_set_note_revision(
        (paragraph_note, exact_note, comparison_note),
        moved_working_set,
        moved_prior_note,
        moved_revision,
    )

    assert isinstance(loaded, ChromiumPageResearchLoadedWorkingSetNoteRevisionRecord)
    assert loaded.verification.revision_record_sha256 == (
        revision_persisted.revision_record_sha256
    )
    assert loaded.revision.prior_note is loaded.prior_note.note
    assert loaded.revision.revised_note.working_set is loaded.prior_note.note.working_set
    assert loaded.revision.revised_note.note_text == revised_text
    assert loaded.prior_note.note.working_set.items[0] is paragraph_note
    assert loaded.prior_note.note.working_set.items[1] is exact_note
    assert loaded.prior_note.note.working_set.items[2] is comparison_note


def test_load_revision_rejects_different_but_valid_predecessor(tmp_path: Path) -> None:
    (
        paragraph_note,
        exact_note,
        comparison_note,
        working_set,
        working_set_path,
        _,
        _,
        _,
        _,
        revision_path,
        _,
    ) = _durable_revision(tmp_path, prior_text="The actual predecessor.")
    other_prior = create_chromium_research_working_set_note(
        working_set,
        note_text="A different but independently valid predecessor.",
    )
    other_prior_path = tmp_path / "other-prior-note.json"
    persist_chromium_research_working_set_note(
        other_prior,
        working_set_path,
        other_prior_path,
    )

    with pytest.raises(
        ChromiumResearchWorkingSetNoteRevisionRelinkError,
        match="different predecessor note record",
    ):
        load_chromium_research_working_set_note_revision(
            (paragraph_note, exact_note, comparison_note),
            working_set_path,
            other_prior_path,
            revision_path,
        )


def test_load_revision_rejects_recomputed_22b_valid_wrong_predecessor_digest(
    tmp_path: Path,
) -> None:
    (
        paragraph_note,
        exact_note,
        comparison_note,
        _,
        working_set_path,
        _,
        prior_note_path,
        prior_persisted,
        _,
        revision_path,
        _,
    ) = _durable_revision(tmp_path)

    document = json.loads(revision_path.read_text(encoding="utf-8"))
    wrong_digest = "f" * 64
    assert wrong_digest != prior_persisted.note_record_sha256
    document["revision_record"]["prior_note_reference"]["note_record_sha256"] = (
        wrong_digest
    )
    document["revision_record_sha256"] = hashlib.sha256(
        _canonical_bytes(document["revision_record"])
    ).hexdigest()
    revision_path.write_bytes(_canonical_document_bytes(document))

    verified = verify_chromium_research_working_set_note_revision(revision_path)
    assert verified.prior_note_record_sha256 == wrong_digest

    with pytest.raises(
        ChromiumResearchWorkingSetNoteRevisionRelinkError,
        match="different predecessor note record",
    ):
        load_chromium_research_working_set_note_revision(
            (paragraph_note, exact_note, comparison_note),
            working_set_path,
            prior_note_path,
            revision_path,
        )


def test_load_revision_rejects_recomputed_22b_valid_exact_noop_against_predecessor(
    tmp_path: Path,
) -> None:
    prior_text = "The real predecessor wording."
    (
        paragraph_note,
        exact_note,
        comparison_note,
        _,
        working_set_path,
        _,
        prior_note_path,
        _,
        _,
        revision_path,
        _,
    ) = _durable_revision(
        tmp_path,
        prior_text=prior_text,
        revised_text="A real revision before tampering.",
    )

    document = json.loads(revision_path.read_text(encoding="utf-8"))
    document["revision_record"]["revision"]["revised_note"]["text"] = prior_text
    document["revision_record_sha256"] = hashlib.sha256(
        _canonical_bytes(document["revision_record"])
    ).hexdigest()
    revision_path.write_bytes(_canonical_document_bytes(document))

    verified = verify_chromium_research_working_set_note_revision(revision_path)
    assert verified.revised_note_text == prior_text

    with pytest.raises(
        ChromiumResearchWorkingSetNoteRevisionRelinkError,
        match="actual revision",
    ):
        load_chromium_research_working_set_note_revision(
            (paragraph_note, exact_note, comparison_note),
            working_set_path,
            prior_note_path,
            revision_path,
        )


def test_load_revision_freshly_verifies_revision_sidecar(tmp_path: Path) -> None:
    (
        paragraph_note,
        exact_note,
        comparison_note,
        _,
        working_set_path,
        _,
        prior_note_path,
        _,
        _,
        revision_path,
        _,
    ) = _durable_revision(tmp_path)

    document = json.loads(revision_path.read_text(encoding="utf-8"))
    document["revision_record"]["revision"]["revised_note"]["text"] = "Tampered."
    revision_path.write_bytes(_canonical_document_bytes(document))

    with pytest.raises(ChromiumResearchWorkingSetNoteRevisionIntegrityError):
        load_chromium_research_working_set_note_revision(
            (paragraph_note, exact_note, comparison_note),
            working_set_path,
            prior_note_path,
            revision_path,
        )


def test_load_revision_does_not_reread_individual_member_sidecars(
    tmp_path: Path,
) -> None:
    (
        paragraph_note,
        exact_note,
        comparison_note,
        _,
        working_set_path,
        _,
        prior_note_path,
        _,
        _,
        revision_path,
        _,
    ) = _durable_revision(tmp_path)

    paragraph_note.verification.path.unlink()
    exact_note.verification.path.unlink()
    comparison_note.verification.path.unlink()

    loaded = load_chromium_research_working_set_note_revision(
        (paragraph_note, exact_note, comparison_note),
        working_set_path,
        prior_note_path,
        revision_path,
    )

    assert loaded.revision.prior_note is loaded.prior_note.note
    assert not paragraph_note.verification.path.exists()
    assert not exact_note.verification.path.exists()
    assert not comparison_note.verification.path.exists()


def test_load_revision_preserves_21c_order_and_count_authority(tmp_path: Path) -> None:
    (
        paragraph_note,
        exact_note,
        comparison_note,
        _,
        working_set_path,
        _,
        prior_note_path,
        _,
        _,
        revision_path,
        _,
    ) = _durable_revision(tmp_path)

    with pytest.raises(ValueError):
        load_chromium_research_working_set_note_revision(
            (exact_note, paragraph_note, comparison_note),
            working_set_path,
            prior_note_path,
            revision_path,
        )

    with pytest.raises(ValueError):
        load_chromium_research_working_set_note_revision(
            (paragraph_note, exact_note),
            working_set_path,
            prior_note_path,
            revision_path,
        )


def test_working_set_note_revision_load_module_is_publicly_importable(
    tmp_path: Path,
) -> None:
    (
        paragraph_note,
        exact_note,
        comparison_note,
        _,
        working_set_path,
        _,
        prior_note_path,
        _,
        _,
        revision_path,
        _,
    ) = _durable_revision(tmp_path, revised_text="Loaded durable revision.")

    loaded = load_chromium_research_working_set_note_revision(
        (paragraph_note, exact_note, comparison_note),
        working_set_path,
        prior_note_path,
        revision_path,
    )

    assert loaded.revision.revised_note.note_text == "Loaded durable revision."


def test_49f_load_v2_revision_relinks_exact_note_v2_predecessor(
    tmp_path: Path,
) -> None:
    revised_text = "  Revised interpretation over v2 rationale 😀\nStill human-owned.  "
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
        revision_persisted,
    ) = _durable_revision_v2(
        tmp_path,
        revised_text=revised_text,
    )

    loaded = load_chromium_research_working_set_note_revision(
        (bare, paragraph_note, bare),
        working_set_path,
        prior_note_path,
        revision_path,
    )

    assert loaded.verification.revision_format == (
        "pyxis.chromium.research_working_set_note_revision.v2"
    )
    assert loaded.verification.prior_note_format == (
        "pyxis.chromium.research_working_set_note.v2"
    )
    assert loaded.verification.revision_record_sha256 == (
        revision_persisted.revision_record_sha256
    )
    assert loaded.prior_note.verification.note_format == (
        "pyxis.chromium.research_working_set_note.v2"
    )
    assert loaded.revision.prior_note is loaded.prior_note.note
    assert loaded.revision.revised_note.working_set is loaded.prior_note.note.working_set
    assert loaded.revision.revised_note.note_text == revised_text
    assert loaded.prior_note.note.working_set.items[0] is bare
    assert loaded.prior_note.note.working_set.items[1] is paragraph_note
    assert loaded.prior_note.note.working_set.items[2] is bare


def test_49f_load_v2_revision_rejects_file_valid_wrong_predecessor_digest(
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

    document = json.loads(revision_path.read_text(encoding="utf-8"))
    wrong_digest = "f" * 64
    document["revision_record"]["prior_note_reference"]["note_record_sha256"] = (
        wrong_digest
    )
    document["revision_record_sha256"] = hashlib.sha256(
        _canonical_bytes(document["revision_record"])
    ).hexdigest()
    revision_path.write_bytes(_canonical_document_bytes(document))

    verified = verify_chromium_research_working_set_note_revision(revision_path)
    assert verified.revision_format == (
        "pyxis.chromium.research_working_set_note_revision.v2"
    )
    assert verified.prior_note_record_sha256 == wrong_digest

    with pytest.raises(
        ChromiumResearchWorkingSetNoteRevisionRelinkError,
        match="different predecessor note record",
    ):
        load_chromium_research_working_set_note_revision(
            (bare, paragraph_note, bare),
            working_set_path,
            prior_note_path,
            revision_path,
        )


def test_49f_load_v2_revision_rejects_file_valid_exact_text_noop(
    tmp_path: Path,
) -> None:
    prior_text = "The real v2 predecessor wording."
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
    ) = _durable_revision_v2(
        tmp_path,
        prior_text=prior_text,
        revised_text="A real revision before tampering.",
    )

    document = json.loads(revision_path.read_text(encoding="utf-8"))
    document["revision_record"]["revision"]["revised_note"]["text"] = prior_text
    document["revision_record_sha256"] = hashlib.sha256(
        _canonical_bytes(document["revision_record"])
    ).hexdigest()
    revision_path.write_bytes(_canonical_document_bytes(document))

    verified = verify_chromium_research_working_set_note_revision(revision_path)
    assert verified.revised_note_text == prior_text

    with pytest.raises(
        ChromiumResearchWorkingSetNoteRevisionRelinkError,
        match="actual revision",
    ):
        load_chromium_research_working_set_note_revision(
            (bare, paragraph_note, bare),
            working_set_path,
            prior_note_path,
            revision_path,
        )


def test_49f_load_v2_revision_does_not_reread_member_sidecars(
    tmp_path: Path,
) -> None:
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
        _,
    ) = _durable_revision_v2(tmp_path)

    paragraph_note.verification.path.unlink()
    bare_path.unlink()

    loaded = load_chromium_research_working_set_note_revision(
        (bare, paragraph_note, bare),
        working_set_path,
        prior_note_path,
        revision_path,
    )

    assert loaded.revision.prior_note is loaded.prior_note.note
    assert not paragraph_note.verification.path.exists()
    assert not bare.verification.path.exists()
