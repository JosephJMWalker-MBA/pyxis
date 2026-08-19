from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
from pathlib import Path

import pytest

from test_app_chromium_research_working_set_note_revision_persistence import _durable_prior
from pyxis.app.chromium_research_working_set_note_revision import (
    create_chromium_research_working_set_note_revision,
)
from pyxis.app.chromium_research_working_set_note_revision_continuation import (
    ChromiumPageResearchWorkingSetNoteRevisionContinuationRecord,
    create_chromium_research_working_set_note_revision_continuation,
)
from pyxis.app.chromium_research_working_set_note_revision_load import (
    load_chromium_research_working_set_note_revision,
)
from pyxis.app.chromium_research_working_set_note_revision_persistence import (
    persist_chromium_research_working_set_note_revision,
)


def _loaded_revision(
    tmp_path: Path,
    *,
    prior_text: str = "v1 rationale.",
    revised_text: str = "v2 rationale.",
):
    (
        paragraph_note,
        exact_note,
        comparison_note,
        _,
        working_set_path,
        prior_note,
        prior_note_path,
        _,
    ) = _durable_prior(tmp_path, note_text=prior_text)
    revision = create_chromium_research_working_set_note_revision(
        prior_note,
        revised_note_text=revised_text,
    )
    revision_path = tmp_path / "revision.json"
    persist_chromium_research_working_set_note_revision(
        revision,
        working_set_path,
        prior_note_path,
        revision_path,
    )
    loaded = load_chromium_research_working_set_note_revision(
        (paragraph_note, exact_note, comparison_note),
        working_set_path,
        prior_note_path,
        revision_path,
    )
    return (
        paragraph_note,
        exact_note,
        comparison_note,
        working_set_path,
        prior_note_path,
        revision_path,
        loaded,
    )


def test_revision_continuation_retains_exact_loaded_predecessor_and_exact_v2_note(
    tmp_path: Path,
) -> None:
    *_, loaded = _loaded_revision(
        tmp_path,
        prior_text="Earlier rationale.",
        revised_text="  Revised once 😀\nStill tentative.  ",
    )
    v3_text = "  Revised twice after another source.\nStill human-owned.  "

    continuation = create_chromium_research_working_set_note_revision_continuation(
        loaded,
        revised_note_text=v3_text,
    )

    assert isinstance(
        continuation,
        ChromiumPageResearchWorkingSetNoteRevisionContinuationRecord,
    )
    assert continuation.continuation_mode == (
        "caller_authored_continuation_of_verified_research_working_set_note_revision"
    )
    assert continuation.prior_revision is loaded
    assert continuation.revision.prior_note is loaded.revision.revised_note
    assert (
        continuation.revision.revised_note.working_set
        is loaded.revision.revised_note.working_set
    )
    assert continuation.revision.revised_note.note_text == v3_text

    with pytest.raises(FrozenInstanceError):
        continuation.continuation_mode = "changed"  # type: ignore[misc]


def test_revision_continuation_represents_v1_v2_v3_without_mutating_earlier_records(
    tmp_path: Path,
) -> None:
    *_, loaded = _loaded_revision(
        tmp_path,
        prior_text="v1 exact wording.",
        revised_text="v2 exact wording.",
    )
    v1 = loaded.revision.prior_note
    v2 = loaded.revision.revised_note

    continuation = create_chromium_research_working_set_note_revision_continuation(
        loaded,
        revised_note_text="v3 exact wording.",
    )

    assert v1.note_text == "v1 exact wording."
    assert v2.note_text == "v2 exact wording."
    assert continuation.revision.prior_note is v2
    assert continuation.revision.revised_note.note_text == "v3 exact wording."
    assert loaded.revision.prior_note is v1
    assert loaded.revision.revised_note is v2


def test_revision_continuation_performs_no_hidden_file_reread(tmp_path: Path) -> None:
    (
        paragraph_note,
        exact_note,
        comparison_note,
        working_set_path,
        prior_note_path,
        revision_path,
        loaded,
    ) = _loaded_revision(tmp_path)

    paragraph_note.verification.path.unlink(missing_ok=True)
    exact_note.verification.path.unlink(missing_ok=True)
    comparison_note.verification.path.unlink(missing_ok=True)
    working_set_path.unlink()
    prior_note_path.unlink()
    revision_path.unlink()

    continuation = create_chromium_research_working_set_note_revision_continuation(
        loaded,
        revised_note_text="v3 after all durable inputs disappeared from this filesystem.",
    )

    assert continuation.prior_revision is loaded
    assert continuation.revision.prior_note is loaded.revision.revised_note
    assert not working_set_path.exists()
    assert not prior_note_path.exists()
    assert not revision_path.exists()


def test_revision_continuation_rejects_wrong_type_and_invalid_revised_text(
    tmp_path: Path,
) -> None:
    *_, loaded = _loaded_revision(tmp_path)

    with pytest.raises(TypeError, match="prior_revision must be"):
        create_chromium_research_working_set_note_revision_continuation(  # type: ignore[arg-type]
            object(),
            revised_note_text="new wording",
        )

    with pytest.raises(TypeError, match="revised_note_text must be a string"):
        create_chromium_research_working_set_note_revision_continuation(  # type: ignore[arg-type]
            loaded,
            revised_note_text=3,
        )

    with pytest.raises(ValueError, match="non-whitespace"):
        create_chromium_research_working_set_note_revision_continuation(
            loaded,
            revised_note_text="  \n\t ",
        )


def test_revision_continuation_rejects_exact_v2_noop(tmp_path: Path) -> None:
    *_, loaded = _loaded_revision(tmp_path, revised_text="v2 exact wording.")

    with pytest.raises(ValueError, match="must differ exactly"):
        create_chromium_research_working_set_note_revision_continuation(
            loaded,
            revised_note_text="v2 exact wording.",
        )


def test_revision_continuation_accepts_exact_whitespace_change_without_semantic_claim(
    tmp_path: Path,
) -> None:
    *_, loaded = _loaded_revision(tmp_path, revised_text="v2 exact wording.")

    continuation = create_chromium_research_working_set_note_revision_continuation(
        loaded,
        revised_note_text=" v2 exact wording. ",
    )

    assert continuation.revision.revised_note.note_text == " v2 exact wording. "


def test_revision_continuation_rejects_forged_loaded_predecessor_identity(
    tmp_path: Path,
) -> None:
    *_, loaded = _loaded_revision(tmp_path)
    forged_verification = replace(
        loaded.verification,
        prior_note_record_sha256="f" * 64,
    )
    forged_loaded = replace(loaded, verification=forged_verification)

    with pytest.raises(ValueError, match="incoherent prior-note identity"):
        create_chromium_research_working_set_note_revision_continuation(
            forged_loaded,
            revised_note_text="v3 should not be accepted.",
        )


def test_revision_continuation_rejects_forged_loaded_v2_text(tmp_path: Path) -> None:
    *_, loaded = _loaded_revision(tmp_path, revised_text="verified v2 wording.")
    forged_v2 = replace(
        loaded.revision.revised_note,
        note_text="forged v2 wording.",
    )
    forged_revision = replace(loaded.revision, revised_note=forged_v2)
    forged_loaded = replace(loaded, revision=forged_revision)

    with pytest.raises(ValueError, match="incoherent revised-note text"):
        create_chromium_research_working_set_note_revision_continuation(
            forged_loaded,
            revised_note_text="v3 should not be accepted.",
        )


def test_revision_continuation_module_is_publicly_importable(tmp_path: Path) -> None:
    *_, loaded = _loaded_revision(tmp_path)

    continuation = create_chromium_research_working_set_note_revision_continuation(
        loaded,
        revised_note_text="A second explicit human change of wording.",
    )

    assert continuation.prior_revision is loaded
    assert continuation.revision.revised_note.note_text == (
        "A second explicit human change of wording."
    )
