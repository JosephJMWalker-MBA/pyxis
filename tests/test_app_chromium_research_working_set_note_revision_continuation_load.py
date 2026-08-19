from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from test_app_chromium_research_working_set_note_revision_continuation_persistence import (
    _canonical_bytes,
    _canonical_document_bytes,
    _durable_continuation,
)
from pyxis.app.chromium_research_working_set_note_revision import (
    create_chromium_research_working_set_note_revision,
)
from pyxis.app.chromium_research_working_set_note_revision_continuation_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord,
    ChromiumResearchWorkingSetNoteRevisionContinuationRelinkError,
    load_chromium_research_working_set_note_revision_continuation,
)
from pyxis.app.chromium_research_working_set_note_revision_continuation_persistence import (
    ChromiumResearchWorkingSetNoteRevisionContinuationIntegrityError,
    persist_chromium_research_working_set_note_revision_continuation,
    verify_chromium_research_working_set_note_revision_continuation,
)
from pyxis.app.chromium_research_working_set_note_revision_persistence import (
    persist_chromium_research_working_set_note_revision,
)


def _loaded_continuation(
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
        loaded_revision,
        continuation,
    ) = _durable_continuation(
        tmp_path,
        prior_text=prior_text,
        revised_text=revised_text,
        continued_text=continued_text,
    )
    continuation_path = tmp_path / "continuation.json"
    persist_chromium_research_working_set_note_revision_continuation(
        continuation,
        working_set_path,
        prior_note_path,
        revision_path,
        continuation_path,
    )
    loaded = load_chromium_research_working_set_note_revision_continuation(
        (paragraph_note, exact_note, comparison_note),
        working_set_path,
        prior_note_path,
        revision_path,
        continuation_path,
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
        loaded,
    )


def test_load_continuation_relinks_exact_predecessor_and_reconstructs_v3(
    tmp_path: Path,
) -> None:
    *_, loaded = _loaded_continuation(
        tmp_path,
        prior_text="Earlier rationale.",
        revised_text="  Revised once 😀\nStill tentative.  ",
        continued_text="  Revised twice after another source.\nStill human-owned.  ",
    )

    assert isinstance(
        loaded,
        ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord,
    )
    assert loaded.verification.continuation_format == (
        "pyxis.chromium.research_working_set_note_revision_continuation.v1"
    )
    assert loaded.continuation.prior_revision is loaded.prior_revision
    assert (
        loaded.continuation.revision.prior_note
        is loaded.prior_revision.revision.revised_note
    )
    assert (
        loaded.continuation.revision.revised_note.working_set
        is loaded.prior_revision.revision.revised_note.working_set
    )
    assert loaded.continuation.revision.revised_note.note_text == (
        "  Revised twice after another source.\nStill human-owned.  "
    )


def test_load_continuation_uses_durable_identity_not_paths(tmp_path: Path) -> None:
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
    ) = _loaded_continuation(tmp_path)

    moved_working_set = tmp_path / "moved-working-set.json"
    moved_prior_note = tmp_path / "moved-prior-note.json"
    moved_revision = tmp_path / "moved-revision.json"
    moved_continuation = tmp_path / "moved-continuation.json"
    working_set_path.replace(moved_working_set)
    prior_note_path.replace(moved_prior_note)
    revision_path.replace(moved_revision)
    continuation_path.replace(moved_continuation)

    loaded = load_chromium_research_working_set_note_revision_continuation(
        (paragraph_note, exact_note, comparison_note),
        moved_working_set,
        moved_prior_note,
        moved_revision,
        moved_continuation,
    )

    assert loaded.verification.path == moved_continuation.resolve()
    assert loaded.prior_revision.verification.path == moved_revision.resolve()
    assert loaded.continuation.prior_revision is loaded.prior_revision


def test_load_continuation_rejects_different_but_valid_predecessor_after_22c_succeeds(
    tmp_path: Path,
) -> None:
    (
        paragraph_note,
        exact_note,
        comparison_note,
        working_set_path,
        prior_note_path,
        _,
        continuation_path,
        loaded_revision,
        _,
        _,
    ) = _loaded_continuation(
        tmp_path,
        revised_text="actual v2 predecessor",
        continued_text="v3 continuing actual v2",
    )

    other_revision = create_chromium_research_working_set_note_revision(
        loaded_revision.prior_note.note,
        revised_note_text="different but valid v2 predecessor",
    )
    other_revision_path = tmp_path / "other-revision.json"
    persist_chromium_research_working_set_note_revision(
        other_revision,
        working_set_path,
        prior_note_path,
        other_revision_path,
    )

    with pytest.raises(
        ChromiumResearchWorkingSetNoteRevisionContinuationRelinkError,
        match="different predecessor revision record",
    ):
        load_chromium_research_working_set_note_revision_continuation(
            (paragraph_note, exact_note, comparison_note),
            working_set_path,
            prior_note_path,
            other_revision_path,
            continuation_path,
        )


def test_load_continuation_rejects_recomputed_wrong_predecessor_identity(
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
        loaded_revision,
        _,
        _,
    ) = _loaded_continuation(tmp_path)

    document = json.loads(continuation_path.read_text(encoding="utf-8"))
    wrong_digest = "f" * 64
    assert wrong_digest != loaded_revision.verification.revision_record_sha256
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
            (paragraph_note, exact_note, comparison_note),
            working_set_path,
            prior_note_path,
            revision_path,
            continuation_path,
        )


def test_load_continuation_rejects_recomputed_v3_equal_to_real_v2(
    tmp_path: Path,
) -> None:
    v2_text = "the exact real v2 wording"
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
    ) = _loaded_continuation(
        tmp_path,
        revised_text=v2_text,
        continued_text="genuinely different v3 at creation",
    )

    document = json.loads(continuation_path.read_text(encoding="utf-8"))
    document["continuation_record"]["continuation"]["revision"]["revised_note"][
        "text"
    ] = v2_text
    document["continuation_record_sha256"] = hashlib.sha256(
        _canonical_bytes(document["continuation_record"])
    ).hexdigest()
    continuation_path.write_bytes(_canonical_document_bytes(document))

    verified = verify_chromium_research_working_set_note_revision_continuation(
        continuation_path
    )
    assert verified.revised_note_text == v2_text

    with pytest.raises(
        ChromiumResearchWorkingSetNoteRevisionContinuationRelinkError,
        match="cannot be re-established as an actual continuation",
    ):
        load_chromium_research_working_set_note_revision_continuation(
            (paragraph_note, exact_note, comparison_note),
            working_set_path,
            prior_note_path,
            revision_path,
            continuation_path,
        )


def test_load_continuation_freshly_verifies_23b_before_relinking(tmp_path: Path) -> None:
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
    ) = _loaded_continuation(tmp_path)

    document = json.loads(continuation_path.read_text(encoding="utf-8"))
    document["continuation_record"]["continuation"]["revision"]["revised_note"][
        "text"
    ] = "tampered without matching digest"
    continuation_path.write_bytes(_canonical_document_bytes(document))

    with pytest.raises(ChromiumResearchWorkingSetNoteRevisionContinuationIntegrityError):
        load_chromium_research_working_set_note_revision_continuation(
            (paragraph_note, exact_note, comparison_note),
            working_set_path,
            prior_note_path,
            revision_path,
            continuation_path,
        )


def test_load_continuation_does_not_reread_individual_member_sidecars(
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
    ) = _loaded_continuation(tmp_path)

    paragraph_note.verification.path.unlink(missing_ok=True)
    exact_note.verification.path.unlink(missing_ok=True)
    comparison_note.verification.path.unlink(missing_ok=True)

    loaded = load_chromium_research_working_set_note_revision_continuation(
        (paragraph_note, exact_note, comparison_note),
        working_set_path,
        prior_note_path,
        revision_path,
        continuation_path,
    )

    assert loaded.continuation.prior_revision is loaded.prior_revision
    assert not paragraph_note.verification.path.exists()
    assert not exact_note.verification.path.exists()
    assert not comparison_note.verification.path.exists()


def test_load_continuation_preserves_caller_member_order_authority(tmp_path: Path) -> None:
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
    ) = _loaded_continuation(tmp_path)

    with pytest.raises(ValueError):
        load_chromium_research_working_set_note_revision_continuation(
            (comparison_note, exact_note, paragraph_note),
            working_set_path,
            prior_note_path,
            revision_path,
            continuation_path,
        )


def test_revision_continuation_load_rejects_noniterable_and_is_publicly_importable(
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
    ) = _loaded_continuation(tmp_path)

    with pytest.raises(TypeError, match="items must be an iterable"):
        load_chromium_research_working_set_note_revision_continuation(  # type: ignore[arg-type]
            object(),
            working_set_path,
            prior_note_path,
            revision_path,
            continuation_path,
        )

    loaded = load_chromium_research_working_set_note_revision_continuation(
        (paragraph_note, exact_note, comparison_note),
        working_set_path,
        prior_note_path,
        revision_path,
        continuation_path,
    )
    assert loaded.continuation.prior_revision is loaded.prior_revision
