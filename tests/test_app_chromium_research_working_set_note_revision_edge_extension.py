from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
from pathlib import Path

import pytest

from test_app_chromium_research_working_set_note_revision_edge_load import _write_edge
from test_app_chromium_research_working_set_note_revision_edge_persistence import (
    _durable_edge,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_extension import (
    ChromiumPageResearchWorkingSetNoteRevisionEdgeExtensionRecord,
    create_chromium_research_working_set_note_revision_edge_extension,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_load import (
    ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError,
    load_chromium_research_working_set_note_revision_edge,
)


_EXTENSION_MODE = "caller_authored_extension_of_verified_research_working_set_note_revision_edge"


def _loaded_edge(tmp_path: Path, *, v4_text: str = "v4 exact wording"):
    *prefix, edge_path, persisted = _durable_edge(
        tmp_path,
        extension_text=v4_text,
    )
    loaded_continuation = prefix[9]
    loaded = load_chromium_research_working_set_note_revision_edge(
        loaded_continuation,
        edge_path,
    )
    return prefix, edge_path, persisted, loaded


def test_loaded_edge_extension_retains_exact_edge_and_endpoint_identity(tmp_path: Path) -> None:
    _, _, _, loaded = _loaded_edge(tmp_path, v4_text="  v4 wording 😀\nStill tentative.  ")

    extension = create_chromium_research_working_set_note_revision_edge_extension(
        loaded,
        revised_note_text="  v5 after another check.\nStill human-owned.  ",
    )

    assert isinstance(extension, ChromiumPageResearchWorkingSetNoteRevisionEdgeExtensionRecord)
    assert extension.extension_mode == _EXTENSION_MODE
    assert extension.prior_edge is loaded
    assert extension.revision.prior_note is loaded.revision.revised_note
    assert (
        extension.revision.revised_note.working_set
        is loaded.revision.revised_note.working_set
    )
    assert extension.revision.revised_note.note_text == (
        "  v5 after another check.\nStill human-owned.  "
    )

    with pytest.raises(FrozenInstanceError):
        extension.extension_mode = "changed"  # type: ignore[misc]


def test_loaded_edge_extension_represents_v4_to_v5_without_mutation(tmp_path: Path) -> None:
    _, _, _, loaded = _loaded_edge(tmp_path, v4_text="v4 exact wording")
    v4 = loaded.revision.revised_note

    extension = create_chromium_research_working_set_note_revision_edge_extension(
        loaded,
        revised_note_text="v5 exact wording",
    )

    assert v4.note_text == "v4 exact wording"
    assert loaded.revision.revised_note is v4
    assert extension.revision.prior_note is v4
    assert extension.revision.revised_note.note_text == "v5 exact wording"
    assert extension.revision.revised_note is not v4


def test_loaded_edge_extension_performs_no_file_reads(tmp_path: Path) -> None:
    prefix, edge_path, _, loaded = _loaded_edge(tmp_path)
    paragraph_note = prefix[0]
    exact_note = prefix[1]
    comparison_note = prefix[2]
    working_set_path = prefix[3]
    prior_note_path = prefix[4]
    revision_path = prefix[5]
    continuation_path = prefix[6]

    paragraph_note.verification.path.unlink(missing_ok=True)
    exact_note.verification.path.unlink(missing_ok=True)
    comparison_note.verification.path.unlink(missing_ok=True)
    working_set_path.unlink(missing_ok=True)
    prior_note_path.unlink(missing_ok=True)
    revision_path.unlink(missing_ok=True)
    continuation_path.unlink(missing_ok=True)
    edge_path.unlink()

    extension = create_chromium_research_working_set_note_revision_edge_extension(
        loaded,
        revised_note_text="v5 after every durable input disappeared",
    )

    assert extension.prior_edge is loaded
    assert extension.revision.prior_note is loaded.revision.revised_note
    assert not edge_path.exists()
    assert not continuation_path.exists()


def test_loaded_edge_extension_rejects_wrong_type_and_invalid_text(tmp_path: Path) -> None:
    _, _, _, loaded = _loaded_edge(tmp_path)

    with pytest.raises(TypeError, match="prior_edge must be"):
        create_chromium_research_working_set_note_revision_edge_extension(  # type: ignore[arg-type]
            object(),
            revised_note_text="new wording",
        )

    with pytest.raises(TypeError, match="revised_note_text must be a string"):
        create_chromium_research_working_set_note_revision_edge_extension(  # type: ignore[arg-type]
            loaded,
            revised_note_text=5,
        )

    with pytest.raises(ValueError, match="non-whitespace"):
        create_chromium_research_working_set_note_revision_edge_extension(
            loaded,
            revised_note_text="  \n\t ",
        )


def test_loaded_edge_extension_rejects_exact_endpoint_noop(tmp_path: Path) -> None:
    _, _, _, loaded = _loaded_edge(tmp_path, v4_text="v4 exact wording")

    with pytest.raises(ValueError, match="must differ exactly"):
        create_chromium_research_working_set_note_revision_edge_extension(
            loaded,
            revised_note_text="v4 exact wording",
        )


def test_loaded_edge_extension_accepts_exact_whitespace_change(tmp_path: Path) -> None:
    _, _, _, loaded = _loaded_edge(tmp_path, v4_text="v4 exact wording")

    extension = create_chromium_research_working_set_note_revision_edge_extension(
        loaded,
        revised_note_text=" v4 exact wording ",
    )

    assert extension.revision.revised_note.note_text == " v4 exact wording "


def test_loaded_edge_extension_rejects_forged_immediate_predecessor_identity(
    tmp_path: Path,
) -> None:
    _, _, _, loaded = _loaded_edge(tmp_path)
    forged_verification = replace(
        loaded.verification,
        predecessor_record_sha256="f" * 64,
    )
    forged_loaded = replace(loaded, verification=forged_verification)

    with pytest.raises(
        ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError,
        match="incoherent predecessor identity",
    ):
        create_chromium_research_working_set_note_revision_edge_extension(
            forged_loaded,
            revised_note_text="v5 should not be accepted",
        )


def test_loaded_edge_extension_rejects_forged_endpoint_text(tmp_path: Path) -> None:
    _, _, _, loaded = _loaded_edge(tmp_path, v4_text="verified v4 wording")
    forged_endpoint = replace(
        loaded.revision.revised_note,
        note_text="forged v4 wording",
    )
    forged_revision = replace(loaded.revision, revised_note=forged_endpoint)
    forged_loaded = replace(loaded, revision=forged_revision)

    with pytest.raises(
        ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError,
        match="incoherent endpoint text",
    ):
        create_chromium_research_working_set_note_revision_edge_extension(
            forged_loaded,
            revised_note_text="v5 should not be accepted",
        )


def test_loaded_edge_extension_does_not_recursively_revalidate_deeper_ancestry(
    tmp_path: Path,
) -> None:
    _, first_edge_path, _, loaded_first = _loaded_edge(
        tmp_path,
        v4_text="v4 exact wording",
    )
    second_edge_path = tmp_path / "second-edge.json"
    _write_edge(
        second_edge_path,
        predecessor_format=loaded_first.verification.edge_format,
        predecessor_sha256=loaded_first.verification.edge_record_sha256,
        revised_note_text="v5 exact wording",
    )
    loaded_second = load_chromium_research_working_set_note_revision_edge(
        loaded_first,
        second_edge_path,
    )

    # Corrupt only the deeper edge-A -> continuation relationship while retaining
    # edge A's own content identity and endpoint note. Edge B's immediate local
    # relationship to A therefore remains coherent. 25A must not turn extension of
    # B into a recursive ancestry audit.
    forged_first_verification = replace(
        loaded_first.verification,
        predecessor_record_sha256="f" * 64,
    )
    forged_first = replace(loaded_first, verification=forged_first_verification)
    locally_coherent_second = replace(loaded_second, predecessor=forged_first)

    first_edge_path.unlink(missing_ok=True)
    second_edge_path.unlink(missing_ok=True)

    extension = create_chromium_research_working_set_note_revision_edge_extension(
        locally_coherent_second,
        revised_note_text="v6 exact wording",
    )

    assert extension.prior_edge is locally_coherent_second
    assert extension.revision.prior_note is loaded_second.revision.revised_note
    assert extension.revision.revised_note.note_text == "v6 exact wording"


def test_loaded_edge_extension_module_is_publicly_importable(tmp_path: Path) -> None:
    _, _, _, loaded = _loaded_edge(tmp_path)

    extension = create_chromium_research_working_set_note_revision_edge_extension(
        loaded,
        revised_note_text="A further explicit human change.",
    )

    assert extension.prior_edge is loaded
    assert extension.revision.revised_note.note_text == "A further explicit human change."
