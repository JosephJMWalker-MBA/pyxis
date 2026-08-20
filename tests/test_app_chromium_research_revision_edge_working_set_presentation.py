from __future__ import annotations

from dataclasses import FrozenInstanceError, fields, replace
import importlib
from pathlib import Path

import pytest

from pyxis.app.chromium_research_revision_edge_working_set_presentation import (
    ChromiumPageResearchRationaleWorkingSetPresentation,
    ChromiumPageResearchSourceExcerptPresentation,
    ChromiumPageResearchWorkingSetMemberPresentation,
    present_chromium_research_revision_edge_working_set_context,
)
from test_app_chromium_research_working_set_note_revision_edge_sequence_presentation import (
    _loaded_declared_sequence,
)


_PRESENTATION_MODE = "read_only_declared_rationale_working_set_context"
_WORKING_SET_MODE = "caller_explicit_ordered_relinked_research_working_set"


def _loaded(tmp_path: Path):
    return _loaded_declared_sequence(tmp_path)


def test_presents_exact_mixed_working_set_for_one_declared_rationale_position(
    tmp_path: Path,
) -> None:
    _, _, _, _, _, loaded = _loaded(tmp_path)

    presentation = present_chromium_research_revision_edge_working_set_context(
        loaded,
        declared_position=2,
    )

    assert isinstance(presentation, ChromiumPageResearchRationaleWorkingSetPresentation)
    assert presentation.presentation_mode == _PRESENTATION_MODE
    assert presentation.declared_position == 2
    assert presentation.rationale_text == "v6 exact human wording\nStill tentative."
    assert presentation.working_set_mode == _WORKING_SET_MODE
    assert tuple(member.member_kind for member in presentation.members) == (
        "paragraph_note",
        "exact_range_note",
        "comparison_note",
    )
    assert tuple(member.member_position for member in presentation.members) == (1, 2, 3)

    paragraph, exact, comparison = presentation.members
    assert paragraph.human_note_text == "  Whole paragraph matters.  "
    assert paragraph.excerpts[0].excerpt_kind == "returned_paragraph_prefix"
    assert paragraph.excerpts[0].text == "Alpha evidence paragraph"
    assert paragraph.excerpts[0].url == "https://example.test/a"
    assert paragraph.excerpts[0].offset_unit is None
    assert paragraph.excerpts[0].start_offset is None
    assert paragraph.excerpts[0].end_offset is None

    assert exact.human_note_text == "Exact range note 😀"
    assert exact.excerpts[0].excerpt_kind == "exact_returned_text_range"
    assert exact.excerpts[0].text == "Alpha"
    assert exact.excerpts[0].offset_unit == "unicode_code_point"
    assert exact.excerpts[0].start_offset == 0
    assert exact.excerpts[0].end_offset == 5

    assert comparison.human_note_text == (
        "  Human comparison; no machine relation claim.\nKeep exact.  "
    )
    assert tuple(excerpt.excerpt_role for excerpt in comparison.excerpts) == (
        "first_selection",
        "second_selection",
    )
    assert tuple(excerpt.text for excerpt in comparison.excerpts) == ("Alpha", "Beta")
    assert tuple(excerpt.url for excerpt in comparison.excerpts) == (
        "https://example.test/a",
        "https://example.test/b",
    )


def test_declared_position_selects_rationale_edge_without_changing_working_set(
    tmp_path: Path,
) -> None:
    _, _, _, _, _, loaded = _loaded(tmp_path)

    first = present_chromium_research_revision_edge_working_set_context(
        loaded,
        declared_position=1,
    )
    second = present_chromium_research_revision_edge_working_set_context(
        loaded,
        declared_position=2,
    )

    assert first.rationale_text == "  v5 exact human wording 😀  "
    assert second.rationale_text == "v6 exact human wording\nStill tentative."
    assert first.edge_record_sha256 != second.edge_record_sha256
    assert first.members == second.members


def test_rejects_wrong_loaded_type_and_invalid_declared_position(tmp_path: Path) -> None:
    _, _, _, _, _, loaded = _loaded(tmp_path)

    with pytest.raises(TypeError, match="loaded must be"):
        present_chromium_research_revision_edge_working_set_context(  # type: ignore[arg-type]
            object(),
            declared_position=1,
        )
    with pytest.raises(TypeError, match="declared_position must be an integer"):
        present_chromium_research_revision_edge_working_set_context(  # type: ignore[arg-type]
            loaded,
            declared_position="1",
        )
    for invalid in (0, 3):
        with pytest.raises(ValueError, match="outside the verified declared segment"):
            present_chromium_research_revision_edge_working_set_context(
                loaded,
                declared_position=invalid,
            )


def test_reuses_27a_declaration_coherence_before_exposing_working_set(tmp_path: Path) -> None:
    _, _, _, _, _, loaded = _loaded(tmp_path)
    forged_verification = replace(
        loaded.verification,
        edges=tuple(reversed(loaded.verification.edges)),
    )
    forged = replace(loaded, verification=forged_verification)

    with pytest.raises(ValueError, match="edge member 0 identity is incoherent"):
        present_chromium_research_revision_edge_working_set_context(
            forged,
            declared_position=1,
        )


def test_rejects_forged_selected_working_set_mode(tmp_path: Path) -> None:
    _, _, _, _, _, loaded = _loaded(tmp_path)
    edge = loaded.sequence.edges[0]
    forged_working_set = replace(
        edge.revision.revised_note.working_set,
        working_set_mode="forged-working-set-mode",
    )
    forged_note = replace(edge.revision.revised_note, working_set=forged_working_set)
    forged_revision = replace(edge.revision, revised_note=forged_note)
    forged_edge = replace(edge, revision=forged_revision)
    forged_sequence = replace(
        loaded.sequence,
        edges=(forged_edge, *loaded.sequence.edges[1:]),
    )
    forged = replace(loaded, sequence=forged_sequence)

    with pytest.raises(ValueError):
        present_chromium_research_revision_edge_working_set_context(
            forged,
            declared_position=1,
        )


def test_source_excerpt_keeps_capture_identity_and_boundedness_facts(tmp_path: Path) -> None:
    _, _, _, _, _, loaded = _loaded(tmp_path)

    presentation = present_chromium_research_revision_edge_working_set_context(
        loaded,
        declared_position=1,
    )
    paragraph_excerpt = presentation.members[0].excerpts[0]
    first_comparison = presentation.members[2].excerpts[0]
    second_comparison = presentation.members[2].excerpts[1]

    assert paragraph_excerpt.source_capture_format == "pyxis.chromium.research_capture.v1"
    assert paragraph_excerpt.source_bundle_sha256 == "a" * 64
    assert paragraph_excerpt.paragraph_ordinal == 1
    assert paragraph_excerpt.paragraph_text_truncated is False
    assert first_comparison.source_bundle_sha256 == "a" * 64
    assert second_comparison.source_bundle_sha256 == "b" * 64
    assert first_comparison.paragraph_text_truncated is False
    assert second_comparison.paragraph_text_truncated is False


def test_presentation_requires_no_files_after_successful_26c_load(tmp_path: Path) -> None:
    prefix, v4_path, v5_path, v6_path, declaration_path, loaded = _loaded(tmp_path)

    for item in prefix[:3]:
        item.verification.path.unlink(missing_ok=True)
    for path in (*prefix[3:7], v4_path, v5_path, v6_path, declaration_path):
        path.unlink(missing_ok=True)

    presentation = present_chromium_research_revision_edge_working_set_context(
        loaded,
        declared_position=2,
    )

    assert presentation.members[0].excerpts[0].text == "Alpha evidence paragraph"
    assert presentation.members[1].excerpts[0].text == "Alpha"
    assert tuple(excerpt.text for excerpt in presentation.members[2].excerpts) == (
        "Alpha",
        "Beta",
    )
    assert not declaration_path.exists()
    assert not v6_path.exists()


def test_presentation_records_are_immutable_and_have_no_authority_upgrade_fields(
    tmp_path: Path,
) -> None:
    _, _, _, _, _, loaded = _loaded(tmp_path)
    presentation = present_chromium_research_revision_edge_working_set_context(
        loaded,
        declared_position=1,
    )

    with pytest.raises(FrozenInstanceError):
        presentation.declared_position = 2  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        presentation.members[0].human_note_text = "changed"  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        presentation.members[0].excerpts[0].text = "changed"  # type: ignore[misc]

    top_fields = {field.name for field in fields(ChromiumPageResearchRationaleWorkingSetPresentation)}
    member_fields = {field.name for field in fields(ChromiumPageResearchWorkingSetMemberPresentation)}
    excerpt_fields = {field.name for field in fields(ChromiumPageResearchSourceExcerptPresentation)}
    forbidden = {
        "path",
        "timestamp",
        "latest",
        "current_head",
        "truth",
        "support",
        "citation",
        "source_authenticity",
    }
    assert top_fields.isdisjoint(forbidden)
    assert member_fields.isdisjoint(forbidden)
    assert excerpt_fields.isdisjoint(forbidden)


def test_human_notes_and_rationale_remain_distinct_from_source_text(tmp_path: Path) -> None:
    _, _, _, _, _, loaded = _loaded(tmp_path)

    presentation = present_chromium_research_revision_edge_working_set_context(
        loaded,
        declared_position=2,
    )

    assert presentation.rationale_text == "v6 exact human wording\nStill tentative."
    assert presentation.rationale_text not in {
        excerpt.text
        for member in presentation.members
        for excerpt in member.excerpts
    }
    assert presentation.members[0].human_note_text == "  Whole paragraph matters.  "
    assert presentation.members[0].human_note_text != presentation.members[0].excerpts[0].text


def test_explicit_module_is_importable() -> None:
    module = importlib.import_module(
        "pyxis.app.chromium_research_revision_edge_working_set_presentation"
    )
    assert hasattr(module, "present_chromium_research_revision_edge_working_set_context")
