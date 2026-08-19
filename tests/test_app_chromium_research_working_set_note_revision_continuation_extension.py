from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
from pathlib import Path

import pytest

from test_app_chromium_research_working_set_note_revision_continuation_load import (
    _loaded_continuation,
)
from pyxis.app.chromium_research_working_set_note_revision_continuation_extension import (
    ChromiumPageResearchWorkingSetNoteRevisionContinuationExtensionRecord,
    create_chromium_research_working_set_note_revision_continuation_extension,
)


def test_continuation_extension_retains_exact_loaded_predecessor_and_exact_v3_note(
    tmp_path: Path,
) -> None:
    *_, loaded = _loaded_continuation(
        tmp_path,
        prior_text="Earlier rationale.",
        revised_text="  Revised once 😀\nStill tentative.  ",
        continued_text="  Revised twice after another source.\nStill human-owned.  ",
    )
    v4_text = "  Revised three times after another check.\nStill human-owned.  "

    extension = create_chromium_research_working_set_note_revision_continuation_extension(
        loaded,
        revised_note_text=v4_text,
    )

    assert isinstance(
        extension,
        ChromiumPageResearchWorkingSetNoteRevisionContinuationExtensionRecord,
    )
    assert extension.extension_mode == (
        "caller_authored_extension_of_verified_research_working_set_note_revision_continuation"
    )
    assert extension.prior_continuation is loaded
    assert extension.revision.prior_note is loaded.continuation.revision.revised_note
    assert (
        extension.revision.revised_note.working_set
        is loaded.continuation.revision.revised_note.working_set
    )
    assert extension.revision.revised_note.note_text == v4_text

    with pytest.raises(FrozenInstanceError):
        extension.extension_mode = "changed"  # type: ignore[misc]


def test_continuation_extension_represents_v1_v2_v3_v4_without_mutation(
    tmp_path: Path,
) -> None:
    *_, loaded = _loaded_continuation(
        tmp_path,
        prior_text="v1 exact wording.",
        revised_text="v2 exact wording.",
        continued_text="v3 exact wording.",
    )
    v1 = loaded.prior_revision.revision.prior_note
    v2 = loaded.prior_revision.revision.revised_note
    v3 = loaded.continuation.revision.revised_note

    extension = create_chromium_research_working_set_note_revision_continuation_extension(
        loaded,
        revised_note_text="v4 exact wording.",
    )

    assert v1.note_text == "v1 exact wording."
    assert v2.note_text == "v2 exact wording."
    assert v3.note_text == "v3 exact wording."
    assert loaded.continuation.revision.prior_note is v2
    assert extension.revision.prior_note is v3
    assert extension.revision.revised_note.note_text == "v4 exact wording."
    assert loaded.prior_revision.revision.prior_note is v1
    assert loaded.prior_revision.revision.revised_note is v2
    assert loaded.continuation.revision.revised_note is v3


def test_continuation_extension_performs_no_hidden_file_reread(tmp_path: Path) -> None:
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
        loaded,
    ) = _loaded_continuation(tmp_path)

    paragraph_note.verification.path.unlink(missing_ok=True)
    exact_note.verification.path.unlink(missing_ok=True)
    comparison_note.verification.path.unlink(missing_ok=True)
    working_set_path.unlink()
    prior_note_path.unlink()
    revision_path.unlink()
    continuation_path.unlink()

    extension = create_chromium_research_working_set_note_revision_continuation_extension(
        loaded,
        revised_note_text="v4 after every durable input disappeared from this filesystem.",
    )

    assert extension.prior_continuation is loaded
    assert extension.revision.prior_note is loaded.continuation.revision.revised_note
    assert not working_set_path.exists()
    assert not prior_note_path.exists()
    assert not revision_path.exists()
    assert not continuation_path.exists()


def test_continuation_extension_rejects_wrong_type_and_invalid_revised_text(
    tmp_path: Path,
) -> None:
    *_, loaded = _loaded_continuation(tmp_path)

    with pytest.raises(TypeError, match="prior_continuation must be"):
        create_chromium_research_working_set_note_revision_continuation_extension(  # type: ignore[arg-type]
            object(),
            revised_note_text="new wording",
        )

    with pytest.raises(TypeError, match="revised_note_text must be a string"):
        create_chromium_research_working_set_note_revision_continuation_extension(  # type: ignore[arg-type]
            loaded,
            revised_note_text=4,
        )

    with pytest.raises(ValueError, match="non-whitespace"):
        create_chromium_research_working_set_note_revision_continuation_extension(
            loaded,
            revised_note_text="  \n\t ",
        )


def test_continuation_extension_rejects_exact_v3_noop(tmp_path: Path) -> None:
    *_, loaded = _loaded_continuation(tmp_path, continued_text="v3 exact wording.")

    with pytest.raises(ValueError, match="must differ exactly"):
        create_chromium_research_working_set_note_revision_continuation_extension(
            loaded,
            revised_note_text="v3 exact wording.",
        )


def test_continuation_extension_accepts_exact_whitespace_change_without_semantic_claim(
    tmp_path: Path,
) -> None:
    *_, loaded = _loaded_continuation(tmp_path, continued_text="v3 exact wording.")

    extension = create_chromium_research_working_set_note_revision_continuation_extension(
        loaded,
        revised_note_text=" v3 exact wording. ",
    )

    assert extension.revision.revised_note.note_text == " v3 exact wording. "


def test_continuation_extension_rejects_forged_loaded_predecessor_identity(
    tmp_path: Path,
) -> None:
    *_, loaded = _loaded_continuation(tmp_path)
    forged_verification = replace(
        loaded.verification,
        prior_revision_record_sha256="f" * 64,
    )
    forged_loaded = replace(loaded, verification=forged_verification)

    with pytest.raises(ValueError, match="incoherent prior-revision identity"):
        create_chromium_research_working_set_note_revision_continuation_extension(
            forged_loaded,
            revised_note_text="v4 should not be accepted.",
        )


def test_continuation_extension_rejects_forged_loaded_v3_text(tmp_path: Path) -> None:
    *_, loaded = _loaded_continuation(
        tmp_path,
        continued_text="verified v3 wording.",
    )
    forged_v3 = replace(
        loaded.continuation.revision.revised_note,
        note_text="forged v3 wording.",
    )
    forged_revision = replace(loaded.continuation.revision, revised_note=forged_v3)
    forged_continuation = replace(loaded.continuation, revision=forged_revision)
    forged_loaded = replace(loaded, continuation=forged_continuation)

    with pytest.raises(ValueError, match="incoherent v3 note text"):
        create_chromium_research_working_set_note_revision_continuation_extension(
            forged_loaded,
            revised_note_text="v4 should not be accepted.",
        )


def test_continuation_extension_module_is_publicly_importable(tmp_path: Path) -> None:
    *_, loaded = _loaded_continuation(tmp_path)

    extension = create_chromium_research_working_set_note_revision_continuation_extension(
        loaded,
        revised_note_text="A third explicit human change of wording.",
    )

    assert extension.prior_continuation is loaded
    assert extension.revision.revised_note.note_text == (
        "A third explicit human change of wording."
    )
