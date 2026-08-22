from __future__ import annotations

from dataclasses import FrozenInstanceError, fields, replace
import importlib
from pathlib import Path

import pytest

from pyxis.app.chromium_research_revision_edge_working_set_presentation import (
    present_chromium_research_revision_edge_working_set_context,
)
from pyxis.app.chromium_research_session_presentation import (
    ChromiumPageResearchSessionPresentation,
    present_chromium_research_session,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_sequence_presentation import (
    present_chromium_research_working_set_note_revision_edge_sequence_declaration,
)
from test_app_chromium_research_working_set_note_revision_edge_sequence_presentation import (
    _loaded_declared_sequence,
)


_PRESENTATION_MODE = "read_only_complete_declared_research_session"


def _loaded(tmp_path: Path):
    return _loaded_declared_sequence(tmp_path)


def test_one_call_presents_complete_segment_and_every_working_set_context(
    tmp_path: Path,
) -> None:
    _, _, _, _, _, loaded = _loaded(tmp_path)

    session = present_chromium_research_session(loaded)

    assert isinstance(session, ChromiumPageResearchSessionPresentation)
    assert session.presentation_mode == _PRESENTATION_MODE
    assert tuple(member.declared_position for member in session.sequence.members) == (1, 2)
    assert tuple(
        context.declared_position for context in session.working_set_contexts
    ) == (1, 2)
    assert len(session.working_set_contexts) == len(session.sequence.members)


def test_bundle_reuses_exact_27a_and_27c_presentation_contracts(tmp_path: Path) -> None:
    _, _, _, _, _, loaded = _loaded(tmp_path)

    session = present_chromium_research_session(loaded)
    sequence = present_chromium_research_working_set_note_revision_edge_sequence_declaration(
        loaded
    )
    first = present_chromium_research_revision_edge_working_set_context(
        loaded,
        declared_position=1,
    )
    second = present_chromium_research_revision_edge_working_set_context(
        loaded,
        declared_position=2,
    )

    assert session.sequence == sequence
    assert session.working_set_contexts == (first, second)


def test_every_context_reconciles_to_exact_sequence_member(tmp_path: Path) -> None:
    _, _, _, _, _, loaded = _loaded(tmp_path)
    session = present_chromium_research_session(loaded)

    for member, context in zip(
        session.sequence.members,
        session.working_set_contexts,
    ):
        assert context.declaration_record_sha256 == session.sequence.declaration_record_sha256
        assert context.declared_position == member.declared_position
        assert context.edge_format == member.edge_format
        assert context.edge_record_sha256 == member.edge_record_sha256
        assert context.rationale_text == member.note_text


def test_exact_human_text_and_mixed_working_set_context_survive_bundle(tmp_path: Path) -> None:
    _, _, _, _, _, loaded = _loaded(tmp_path)
    session = present_chromium_research_session(loaded)

    first, second = session.working_set_contexts
    assert first.rationale_text == "  v5 exact human wording 😀  "
    assert second.rationale_text == "v6 exact human wording\nStill tentative."
    assert tuple(member.member_kind for member in first.members) == (
        "paragraph_note",
        "exact_range_note",
        "comparison_note",
    )
    assert first.members[0].human_note_text == "  Whole paragraph matters.  "
    assert first.members[0].excerpts[0].text == "Alpha evidence paragraph"
    assert first.members[1].excerpts[0].text == "Alpha"
    assert tuple(excerpt.text for excerpt in first.members[2].excerpts) == (
        "Alpha",
        "Beta",
    )


def test_rejects_wrong_loaded_type() -> None:
    with pytest.raises(TypeError, match="loaded must be"):
        present_chromium_research_session(object())  # type: ignore[arg-type]


def test_reuses_27a_declaration_coherence_before_building_session(tmp_path: Path) -> None:
    _, _, _, _, _, loaded = _loaded(tmp_path)
    forged = replace(
        loaded,
        verification=replace(
            loaded.verification,
            edges=tuple(reversed(loaded.verification.edges)),
        ),
    )

    with pytest.raises(ValueError, match="edge member 0 identity is incoherent"):
        present_chromium_research_session(forged)


def test_later_forged_working_set_rejects_whole_session(tmp_path: Path) -> None:
    _, _, _, _, _, loaded = _loaded(tmp_path)
    first_edge, second_edge = loaded.sequence.edges
    forged_working_set = replace(
        second_edge.revision.revised_note.working_set,
        working_set_mode="forged-working-set-mode",
    )
    forged_note = replace(
        second_edge.revision.revised_note,
        working_set=forged_working_set,
    )
    forged_revision = replace(second_edge.revision, revised_note=forged_note)
    forged_second = replace(second_edge, revision=forged_revision)
    forged = replace(
        loaded,
        sequence=replace(loaded.sequence, edges=(first_edge, forged_second)),
    )

    with pytest.raises(ValueError):
        present_chromium_research_session(forged)


def test_session_requires_no_files_after_successful_26c_load(tmp_path: Path) -> None:
    prefix, v4_path, v5_path, v6_path, declaration_path, loaded = _loaded(tmp_path)

    for item in prefix[:3]:
        item.verification.path.unlink(missing_ok=True)
    for path in (*prefix[3:7], v4_path, v5_path, v6_path, declaration_path):
        path.unlink(missing_ok=True)

    session = present_chromium_research_session(loaded)

    assert len(session.sequence.members) == 2
    assert len(session.working_set_contexts) == 2
    assert session.working_set_contexts[1].members[0].excerpts[0].text == (
        "Alpha evidence paragraph"
    )
    assert not declaration_path.exists()
    assert not v6_path.exists()


def test_session_record_is_immutable_and_adds_no_authority_upgrade_fields(
    tmp_path: Path,
) -> None:
    _, _, _, _, _, loaded = _loaded(tmp_path)
    session = present_chromium_research_session(loaded)

    with pytest.raises(FrozenInstanceError):
        session.presentation_mode = "changed"  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        session.working_set_contexts = ()  # type: ignore[misc]

    field_names = {
        field.name for field in fields(ChromiumPageResearchSessionPresentation)
    }
    assert field_names == {
        "presentation_mode",
        "sequence",
        "working_set_contexts",
    }
    forbidden = {
        "path",
        "timestamp",
        "latest",
        "current_head",
        "truth",
        "support",
        "citation",
        "source_authenticity",
        "workspace_id",
    }
    assert field_names.isdisjoint(forbidden)


def test_explicit_session_module_is_importable_without_package_root_broadening() -> None:
    module = importlib.import_module("pyxis.app.chromium_research_session_presentation")
    assert hasattr(module, "ChromiumPageResearchSessionPresentation")
    assert hasattr(module, "present_chromium_research_session")
