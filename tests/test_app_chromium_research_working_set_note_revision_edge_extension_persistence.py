from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path

import pytest

from test_app_chromium_research_working_set_note_revision_edge_extension import (
    _loaded_edge,
)
from test_app_chromium_research_working_set_note_revision_edge_load import (
    _write_edge,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_extension import (
    create_chromium_research_working_set_note_revision_edge_extension,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_extension_persistence import (
    ChromiumPageResearchWorkingSetNoteRevisionEdgeExtensionPersistenceEvidence,
    persist_chromium_research_working_set_note_revision_edge_extension,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_load import (
    ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError,
    load_chromium_research_working_set_note_revision_edge,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_persistence import (
    ChromiumResearchWorkingSetNoteRevisionEdgeIntegrityError,
    verify_chromium_research_working_set_note_revision_edge,
)


_EDGE_FORMAT = "pyxis.chromium.research_working_set_note_revision_edge.v1"
_EDGE_MODE = "caller_authored_research_working_set_note_revision_edge"
_REVISION_MODE = "caller_authored_revision_of_research_working_set_note"
_NOTE_MODE = "caller_authored_note_on_research_working_set"


def _durable_successor(
    tmp_path: Path,
    *,
    v4_text: str = "v4 exact wording",
    v5_text: str = "v5 exact wording",
):
    prefix, prior_edge_path, _, loaded_prior = _loaded_edge(
        tmp_path,
        v4_text=v4_text,
    )
    extension = create_chromium_research_working_set_note_revision_edge_extension(
        loaded_prior,
        revised_note_text=v5_text,
    )
    successor_path = tmp_path / "successor-edge.json"
    persisted = persist_chromium_research_working_set_note_revision_edge_extension(
        extension,
        prior_edge_path,
        successor_path,
    )
    return prefix, prior_edge_path, loaded_prior, extension, successor_path, persisted


def test_persist_loaded_edge_extension_reuses_24b_format_and_exact_edge_identity(
    tmp_path: Path,
) -> None:
    (
        _,
        prior_edge_path,
        loaded_prior,
        extension,
        successor_path,
        persisted,
    ) = _durable_successor(
        tmp_path,
        v4_text="v4 text that must not be copied",
        v5_text="  v5 after another check 😀\nStill human-owned.  ",
    )

    verified = verify_chromium_research_working_set_note_revision_edge(successor_path)
    document = json.loads(successor_path.read_text(encoding="utf-8"))

    assert isinstance(
        persisted,
        ChromiumPageResearchWorkingSetNoteRevisionEdgeExtensionPersistenceEvidence,
    )
    assert persisted.extension is extension
    assert persisted.edge_format == _EDGE_FORMAT
    assert verified.edge_format == _EDGE_FORMAT
    assert verified.predecessor_format == _EDGE_FORMAT
    assert verified.predecessor_record_sha256 == (
        loaded_prior.verification.edge_record_sha256
    )
    assert verified.edge_mode == _EDGE_MODE
    assert verified.revision_mode == _REVISION_MODE
    assert verified.revised_note_mode == _NOTE_MODE
    assert verified.revised_note_text == extension.revision.revised_note.note_text
    assert document["edge_record"] == {
        "predecessor_reference": {
            "format": _EDGE_FORMAT,
            "record_sha256": loaded_prior.verification.edge_record_sha256,
        },
        "edge": {
            "mode": _EDGE_MODE,
            "revision": {
                "mode": _REVISION_MODE,
                "revised_note": {
                    "mode": _NOTE_MODE,
                    "text": extension.revision.revised_note.note_text,
                },
            },
        },
    }

    raw_text = successor_path.read_text(encoding="utf-8")
    assert loaded_prior.revision.revised_note.note_text not in raw_text
    assert "extension_mode" not in raw_text
    assert str(prior_edge_path.resolve()) not in raw_text


def test_persist_loaded_edge_extension_uses_content_identity_not_path(tmp_path: Path) -> None:
    prefix, prior_edge_path, _, loaded_prior = _loaded_edge(tmp_path)
    extension = create_chromium_research_working_set_note_revision_edge_extension(
        loaded_prior,
        revised_note_text="v5 after moving the predecessor file",
    )
    moved = tmp_path / "moved-prior-edge.json"
    prior_edge_path.replace(moved)
    destination = tmp_path / "successor-after-move.json"

    persist_chromium_research_working_set_note_revision_edge_extension(
        extension,
        moved,
        destination,
    )
    verified = verify_chromium_research_working_set_note_revision_edge(destination)

    assert verified.predecessor_record_sha256 == loaded_prior.verification.edge_record_sha256
    assert str(moved.resolve()) not in verified.document_json
    assert prefix is not None


def test_persist_loaded_edge_extension_rejects_different_valid_prior_edge_before_write(
    tmp_path: Path,
) -> None:
    _, prior_edge_path, _, loaded_prior = _loaded_edge(
        tmp_path,
        v4_text="actual v4 predecessor",
    )
    extension = create_chromium_research_working_set_note_revision_edge_extension(
        loaded_prior,
        revised_note_text="v5 continuing actual v4",
    )
    other_prior = tmp_path / "other-valid-v4-edge.json"
    _write_edge(
        other_prior,
        predecessor_format=loaded_prior.verification.predecessor_format,
        predecessor_sha256=loaded_prior.verification.predecessor_record_sha256,
        revised_note_text="different but valid v4 predecessor",
    )
    assert other_prior.read_bytes() != prior_edge_path.read_bytes()
    destination = tmp_path / "should-not-write.json"

    with pytest.raises(
        ValueError,
        match="durable loaded-edge predecessor does not match the extension",
    ):
        persist_chromium_research_working_set_note_revision_edge_extension(
            extension,
            other_prior,
            destination,
        )

    assert not destination.exists()


def test_persist_loaded_edge_extension_requires_current_prior_edge_file(
    tmp_path: Path,
) -> None:
    _, prior_edge_path, _, loaded_prior = _loaded_edge(tmp_path)
    extension = create_chromium_research_working_set_note_revision_edge_extension(
        loaded_prior,
        revised_note_text="v5 still valid in memory",
    )
    prior_edge_path.unlink()
    destination = tmp_path / "cannot-write-without-prior-edge.json"

    with pytest.raises(FileNotFoundError):
        persist_chromium_research_working_set_note_revision_edge_extension(
            extension,
            prior_edge_path,
            destination,
        )

    assert not destination.exists()


def test_persist_loaded_edge_extension_does_not_require_older_sidecars(
    tmp_path: Path,
) -> None:
    prefix, prior_edge_path, _, loaded_prior = _loaded_edge(tmp_path)
    paragraph_note = prefix[0]
    exact_note = prefix[1]
    comparison_note = prefix[2]
    working_set_path = prefix[3]
    prior_note_path = prefix[4]
    revision_path = prefix[5]
    continuation_path = prefix[6]

    extension = create_chromium_research_working_set_note_revision_edge_extension(
        loaded_prior,
        revised_note_text="v5 with only the immediate predecessor edge still durable",
    )

    paragraph_note.verification.path.unlink(missing_ok=True)
    exact_note.verification.path.unlink(missing_ok=True)
    comparison_note.verification.path.unlink(missing_ok=True)
    working_set_path.unlink(missing_ok=True)
    prior_note_path.unlink(missing_ok=True)
    revision_path.unlink(missing_ok=True)
    continuation_path.unlink(missing_ok=True)

    destination = tmp_path / "successor-without-older-sidecars.json"
    persisted = persist_chromium_research_working_set_note_revision_edge_extension(
        extension,
        prior_edge_path,
        destination,
    )

    assert persisted.extension is extension
    assert destination.exists()
    assert prior_edge_path.exists()
    assert not continuation_path.exists()


def test_persist_loaded_edge_extension_reestablishes_live_25a_contract_before_write(
    tmp_path: Path,
) -> None:
    _, prior_edge_path, _, loaded_prior = _loaded_edge(tmp_path)
    extension = create_chromium_research_working_set_note_revision_edge_extension(
        loaded_prior,
        revised_note_text="v5 exact wording",
    )
    forged = replace(extension, extension_mode="forged-extension-mode")
    destination = tmp_path / "forged-extension.json"

    with pytest.raises(ValueError, match="extension mode is unsupported"):
        persist_chromium_research_working_set_note_revision_edge_extension(
            forged,
            prior_edge_path,
            destination,
        )

    assert not destination.exists()


def test_persist_loaded_edge_extension_fresh_24c_gate_is_stronger_than_25a(
    tmp_path: Path,
) -> None:
    _, first_edge_path, _, loaded_first = _loaded_edge(
        tmp_path,
        v4_text="v4 exact wording",
    )
    second_edge_path = tmp_path / "second-edge-v5.json"
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

    forged_first_verification = replace(
        loaded_first.verification,
        predecessor_record_sha256="f" * 64,
    )
    forged_first = replace(loaded_first, verification=forged_first_verification)
    locally_coherent_second = replace(loaded_second, predecessor=forged_first)

    extension = create_chromium_research_working_set_note_revision_edge_extension(
        locally_coherent_second,
        revised_note_text="v6 exact wording",
    )
    destination = tmp_path / "v6-must-not-persist.json"

    with pytest.raises(
        ChromiumResearchWorkingSetNoteRevisionEdgeRelinkError,
        match="incoherent predecessor identity",
    ):
        persist_chromium_research_working_set_note_revision_edge_extension(
            extension,
            second_edge_path,
            destination,
        )

    assert not destination.exists()
    assert first_edge_path.exists()


def test_persist_loaded_edge_extension_freshly_verifies_prior_edge_file(
    tmp_path: Path,
) -> None:
    _, prior_edge_path, _, loaded_prior = _loaded_edge(tmp_path)
    extension = create_chromium_research_working_set_note_revision_edge_extension(
        loaded_prior,
        revised_note_text="v5 after a valid v4",
    )
    document = json.loads(prior_edge_path.read_text(encoding="utf-8"))
    document["edge_record"]["edge"]["revision"]["revised_note"]["text"] = (
        "tampered v4 without recomputing the digest"
    )
    prior_edge_path.write_text(
        json.dumps(document, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    destination = tmp_path / "successor-after-tamper.json"

    with pytest.raises(ChromiumResearchWorkingSetNoteRevisionEdgeIntegrityError):
        persist_chromium_research_working_set_note_revision_edge_extension(
            extension,
            prior_edge_path,
            destination,
        )

    assert not destination.exists()


def test_persisted_loaded_edge_extension_reloads_through_existing_24c(
    tmp_path: Path,
) -> None:
    _, _, loaded_prior, extension, successor_path, _ = _durable_successor(
        tmp_path,
        v4_text="v4 exact wording",
        v5_text="v5 exact wording",
    )

    loaded_successor = load_chromium_research_working_set_note_revision_edge(
        loaded_prior,
        successor_path,
    )

    assert loaded_successor.predecessor is loaded_prior
    assert loaded_successor.revision.prior_note is loaded_prior.revision.revised_note
    assert loaded_successor.revision.revised_note.note_text == "v5 exact wording"
    assert loaded_successor.revision.revised_note.note_text == (
        extension.revision.revised_note.note_text
    )


def test_loaded_edge_extension_persistence_is_deterministic_no_overwrite_and_public(
    tmp_path: Path,
) -> None:
    _, prior_edge_path, _, loaded_prior = _loaded_edge(tmp_path)
    extension = create_chromium_research_working_set_note_revision_edge_extension(
        loaded_prior,
        revised_note_text="A repeatably durable successor edge.",
    )
    first_path = tmp_path / "first-successor.json"
    second_path = tmp_path / "second-successor.json"

    first = persist_chromium_research_working_set_note_revision_edge_extension(
        extension,
        prior_edge_path,
        first_path,
    )
    second = persist_chromium_research_working_set_note_revision_edge_extension(
        extension,
        prior_edge_path,
        second_path,
    )

    assert first.edge_record_sha256 == second.edge_record_sha256
    assert first_path.read_bytes() == second_path.read_bytes()

    original = first_path.read_bytes()
    with pytest.raises(FileExistsError):
        persist_chromium_research_working_set_note_revision_edge_extension(
            extension,
            prior_edge_path,
            first_path,
        )
    assert first_path.read_bytes() == original

    wrong_type_path = tmp_path / "wrong-type.json"
    with pytest.raises(TypeError, match="extension must be"):
        persist_chromium_research_working_set_note_revision_edge_extension(  # type: ignore[arg-type]
            object(),
            prior_edge_path,
            wrong_type_path,
        )
    assert not wrong_type_path.exists()
