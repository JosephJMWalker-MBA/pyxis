from __future__ import annotations

from dataclasses import FrozenInstanceError, fields, replace
from pathlib import Path

import pytest

from test_app_chromium_research_working_set_note_revision_edge_sequence_declaration_load import (
    _declared_sequence,
)
from test_app_chromium_research_working_set_note_revision_edge_sequence_load import (
    _two_successor_edges,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_sequence_declaration_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceDeclarationRecord,
    load_chromium_research_working_set_note_revision_edge_sequence_declaration,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_sequence_persistence import (
    persist_chromium_research_working_set_note_revision_edge_sequence,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_sequence_load import (
    load_chromium_research_working_set_note_revision_edge_sequence,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_sequence_presentation import (
    ChromiumPageResearchRevisionEdgeSequenceMemberPresentation,
    ChromiumPageResearchRevisionEdgeSequencePresentation,
    present_chromium_research_working_set_note_revision_edge_sequence_declaration,
)


_PRESENTATION_MODE = (
    "read_only_verified_declared_research_working_set_note_revision_edge_sequence"
)
_SEQUENCE_FORMAT = (
    "pyxis.chromium.research_working_set_note_revision_edge_sequence.v1"
)
_EDGE_FORMAT = "pyxis.chromium.research_working_set_note_revision_edge.v1"


def _loaded_declared_sequence(tmp_path: Path):
    (
        prefix,
        v4_path,
        loaded_v4,
        _,
        v5_path,
        v6_path,
        _,
        declaration_path,
        _,
    ) = _declared_sequence(tmp_path)
    loaded = load_chromium_research_working_set_note_revision_edge_sequence_declaration(
        loaded_v4,
        [v5_path, v6_path],
        declaration_path,
    )
    return prefix, v4_path, v5_path, v6_path, declaration_path, loaded


def test_presentation_exposes_exact_declared_positions_identities_and_human_text(
    tmp_path: Path,
) -> None:
    _, _, _, _, _, loaded = _loaded_declared_sequence(tmp_path)

    presentation = (
        present_chromium_research_working_set_note_revision_edge_sequence_declaration(
            loaded
        )
    )

    assert isinstance(presentation, ChromiumPageResearchRevisionEdgeSequencePresentation)
    assert presentation.presentation_mode == _PRESENTATION_MODE
    assert presentation.declaration_format == _SEQUENCE_FORMAT
    assert presentation.declaration_record_sha256 == (
        loaded.verification.sequence_record_sha256
    )
    assert presentation.starting_record_format == _EDGE_FORMAT
    assert presentation.starting_record_sha256 == (
        loaded.sequence.starting_predecessor.verification.edge_record_sha256
    )
    assert tuple(member.declared_position for member in presentation.members) == (1, 2)
    assert tuple(member.note_text for member in presentation.members) == (
        "  v5 exact human wording 😀  ",
        "v6 exact human wording\nStill tentative.",
    )
    assert tuple(member.edge_record_sha256 for member in presentation.members) == tuple(
        edge.verification.edge_record_sha256 for edge in loaded.sequence.edges
    )


def test_presentation_requires_no_files_after_successful_26c_load(tmp_path: Path) -> None:
    prefix, v4_path, v5_path, v6_path, declaration_path, loaded = (
        _loaded_declared_sequence(tmp_path)
    )

    for item in prefix[:3]:
        item.verification.path.unlink(missing_ok=True)
    for path in (*prefix[3:7], v4_path, v5_path, v6_path, declaration_path):
        path.unlink(missing_ok=True)

    presentation = (
        present_chromium_research_working_set_note_revision_edge_sequence_declaration(
            loaded
        )
    )

    assert len(presentation.members) == 2
    assert presentation.members[-1].note_text == "v6 exact human wording\nStill tentative."
    assert not declaration_path.exists()
    assert not v5_path.exists()
    assert not v6_path.exists()


def test_presentation_supports_verified_declaration_starting_at_loaded_23c_continuation(
    tmp_path: Path,
) -> None:
    (
        _,
        v4_path,
        loaded_v4,
        _,
        v5_path,
        _,
        _,
        _,
        v6_path,
        _,
    ) = _two_successor_edges(tmp_path)
    loaded_continuation = loaded_v4.predecessor
    sequence = load_chromium_research_working_set_note_revision_edge_sequence(
        loaded_continuation,
        [v4_path, v5_path, v6_path],
    )
    declaration_path = tmp_path / "continuation-start-declaration.json"
    persist_chromium_research_working_set_note_revision_edge_sequence(
        sequence,
        declaration_path,
    )
    loaded = load_chromium_research_working_set_note_revision_edge_sequence_declaration(
        loaded_continuation,
        [v4_path, v5_path, v6_path],
        declaration_path,
    )

    presentation = (
        present_chromium_research_working_set_note_revision_edge_sequence_declaration(
            loaded
        )
    )

    assert presentation.starting_record_format == (
        "pyxis.chromium.research_working_set_note_revision_continuation.v1"
    )
    assert presentation.starting_record_sha256 == (
        loaded_continuation.verification.continuation_record_sha256
    )
    assert tuple(member.declared_position for member in presentation.members) == (1, 2, 3)


def test_presentation_rejects_wrong_input_type() -> None:
    with pytest.raises(TypeError, match="loaded must be"):
        present_chromium_research_working_set_note_revision_edge_sequence_declaration(  # type: ignore[arg-type]
            object()
        )


def test_presentation_rejects_forged_retained_starting_identity(tmp_path: Path) -> None:
    _, _, _, _, _, loaded = _loaded_declared_sequence(tmp_path)
    forged_start = replace(
        loaded.verification.starting_predecessor,
        record_sha256="f" * 64,
    )
    forged_verification = replace(
        loaded.verification,
        starting_predecessor=forged_start,
    )
    forged_loaded = replace(loaded, verification=forged_verification)

    with pytest.raises(ValueError, match="starting predecessor identity"):
        present_chromium_research_working_set_note_revision_edge_sequence_declaration(
            forged_loaded
        )


def test_presentation_rejects_forged_retained_declared_order(tmp_path: Path) -> None:
    _, _, _, _, _, loaded = _loaded_declared_sequence(tmp_path)
    forged_verification = replace(
        loaded.verification,
        edges=tuple(reversed(loaded.verification.edges)),
    )
    forged_loaded = replace(loaded, verification=forged_verification)

    with pytest.raises(ValueError, match="edge member 0 identity"):
        present_chromium_research_working_set_note_revision_edge_sequence_declaration(
            forged_loaded
        )


def test_presentation_rejects_forged_loaded_sequence_order(tmp_path: Path) -> None:
    _, _, _, _, _, loaded = _loaded_declared_sequence(tmp_path)
    forged_sequence = replace(
        loaded.sequence,
        edges=tuple(reversed(loaded.sequence.edges)),
    )
    forged_loaded = replace(loaded, sequence=forged_sequence)

    with pytest.raises(ValueError, match="does not retain the exact preceding"):
        present_chromium_research_working_set_note_revision_edge_sequence_declaration(
            forged_loaded
        )


def test_presentation_rejects_forged_loaded_edge_note_text(tmp_path: Path) -> None:
    _, _, _, _, _, loaded = _loaded_declared_sequence(tmp_path)
    first = loaded.sequence.edges[0]
    forged_note = replace(first.revision.revised_note, note_text="forged display text")
    forged_revision = replace(first.revision, revised_note=forged_note)
    forged_first = replace(first, revision=forged_revision)
    forged_sequence = replace(
        loaded.sequence,
        edges=(forged_first, loaded.sequence.edges[1]),
    )
    forged_loaded = replace(loaded, sequence=forged_sequence)

    with pytest.raises(ValueError):
        present_chromium_research_working_set_note_revision_edge_sequence_declaration(
            forged_loaded
        )


def test_presentation_records_are_frozen_and_have_no_path_or_head_fields(
    tmp_path: Path,
) -> None:
    _, _, _, _, _, loaded = _loaded_declared_sequence(tmp_path)
    presentation = (
        present_chromium_research_working_set_note_revision_edge_sequence_declaration(
            loaded
        )
    )

    presentation_fields = {field.name for field in fields(presentation)}
    member_fields = {field.name for field in fields(presentation.members[0])}

    assert presentation_fields == {
        "presentation_mode",
        "declaration_format",
        "declaration_record_sha256",
        "sequence_mode",
        "starting_record_format",
        "starting_record_sha256",
        "members",
    }
    assert member_fields == {
        "declared_position",
        "edge_format",
        "edge_record_sha256",
        "note_text",
    }
    assert not ({"path", "latest", "current_head", "timestamp"} & presentation_fields)
    assert not ({"path", "latest", "current_head", "timestamp"} & member_fields)

    with pytest.raises(FrozenInstanceError):
        presentation.presentation_mode = "mutated"  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        presentation.members[0].note_text = "mutated"  # type: ignore[misc]


def test_presentation_module_is_explicitly_importable_and_member_type_is_public(
    tmp_path: Path,
) -> None:
    _, _, _, _, _, loaded = _loaded_declared_sequence(tmp_path)
    presentation = (
        present_chromium_research_working_set_note_revision_edge_sequence_declaration(
            loaded
        )
    )

    assert all(
        isinstance(member, ChromiumPageResearchRevisionEdgeSequenceMemberPresentation)
        for member in presentation.members
    )
    assert all(member.edge_format == _EDGE_FORMAT for member in presentation.members)
    assert presentation.sequence_mode == loaded.verification.sequence_mode
    assert isinstance(
        loaded,
        ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceDeclarationRecord,
    )
