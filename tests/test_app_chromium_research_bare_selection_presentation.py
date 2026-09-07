from __future__ import annotations

from pathlib import Path

from test_app_chromium_research_working_set_note_revision_edge_v2_bridge import (
    _v2_backed_edge,
)
from pyxis.app.chromium_research_revision_edge_working_set_presentation import (
    present_chromium_research_revision_edge_working_set_context,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_extension import (
    create_chromium_research_working_set_note_revision_edge_extension,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_extension_persistence import (
    persist_chromium_research_working_set_note_revision_edge_extension,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_load import (
    load_chromium_research_working_set_note_revision_edge,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_sequence_declaration_load import (
    load_chromium_research_working_set_note_revision_edge_sequence_declaration,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_sequence_load import (
    load_chromium_research_working_set_note_revision_edge_sequence,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_sequence_persistence import (
    persist_chromium_research_working_set_note_revision_edge_sequence,
)


def _declared_v2_bare_sequence(tmp_path: Path):
    (
        paragraph_note,
        bare,
        bare_path,
        working_set_path,
        prior_note_path,
        revision_path,
        continuation_path,
        loaded_continuation,
        _,
        first_edge_path,
        _,
    ) = _v2_backed_edge(
        tmp_path,
        extension_text="v4 first edge after continuation v2.",
    )
    loaded_first = load_chromium_research_working_set_note_revision_edge(
        loaded_continuation,
        first_edge_path,
    )
    successor = create_chromium_research_working_set_note_revision_edge_extension(
        loaded_first,
        revised_note_text="v5 ordinary edge retaining the v2 working set.",
    )
    successor_path = tmp_path / "50a-successor-edge.json"
    persist_chromium_research_working_set_note_revision_edge_extension(
        successor,
        first_edge_path,
        successor_path,
    )

    sequence = load_chromium_research_working_set_note_revision_edge_sequence(
        loaded_first,
        [successor_path],
    )
    declaration_path = tmp_path / "50a-declared-sequence.json"
    persist_chromium_research_working_set_note_revision_edge_sequence(
        sequence,
        declaration_path,
    )
    loaded = load_chromium_research_working_set_note_revision_edge_sequence_declaration(
        loaded_first,
        [successor_path],
        declaration_path,
    )
    return (
        paragraph_note,
        bare,
        bare_path,
        working_set_path,
        prior_note_path,
        revision_path,
        continuation_path,
        first_edge_path,
        successor_path,
        declaration_path,
        loaded_first,
        loaded,
    )


def test_50a_presents_bare_saved_passage_after_v2_line_rejoins_ordinary_edge_lineage(
    tmp_path: Path,
) -> None:
    paragraph_note, bare, *_, loaded = _declared_v2_bare_sequence(tmp_path)

    presentation = present_chromium_research_revision_edge_working_set_context(
        loaded,
        declared_position=1,
    )

    assert presentation.rationale_text == "v5 ordinary edge retaining the v2 working set."
    assert tuple(member.member_kind for member in presentation.members) == (
        "exact_range_selection",
        "paragraph_note",
        "exact_range_selection",
    )
    first_bare, presented_note, second_bare = presentation.members
    assert first_bare.human_note_text is None
    assert second_bare.human_note_text is None
    assert first_bare.excerpts[0].excerpt_role == "selection"
    assert first_bare.excerpts[0].excerpt_kind == "exact_returned_text_range"
    assert first_bare.excerpts[0].text == bare.selection.selected_text == "Gamma"
    assert first_bare.excerpts[0].url == "https://example.test/bare"
    assert first_bare.excerpts[0].offset_unit == "unicode_code_point"
    assert first_bare.excerpts[0].start_offset == 0
    assert first_bare.excerpts[0].end_offset == 5
    assert second_bare == first_bare.__class__(
        member_position=3,
        member_kind="exact_range_selection",
        human_note_text=None,
        excerpts=first_bare.excerpts,
    )
    assert presented_note.member_kind == "paragraph_note"
    assert presented_note.human_note_text == paragraph_note.note.note_text
    assert presented_note.human_note_text == "  Whole paragraph matters.  "


def test_50a_presentation_requires_no_member_or_lineage_files_after_explicit_load(
    tmp_path: Path,
) -> None:
    (
        paragraph_note,
        bare,
        bare_path,
        working_set_path,
        prior_note_path,
        revision_path,
        continuation_path,
        first_edge_path,
        successor_path,
        declaration_path,
        _,
        loaded,
    ) = _declared_v2_bare_sequence(tmp_path)

    for path in (
        paragraph_note.verification.path,
        bare_path,
        working_set_path,
        prior_note_path,
        revision_path,
        continuation_path,
        first_edge_path,
        successor_path,
        declaration_path,
    ):
        path.unlink(missing_ok=True)

    presentation = present_chromium_research_revision_edge_working_set_context(
        loaded,
        declared_position=1,
    )

    assert presentation.members[0].human_note_text is None
    assert presentation.members[0].excerpts[0].text == bare.selection.selected_text
    assert presentation.members[1].human_note_text == paragraph_note.note.note_text
    assert not bare.verification.path.exists()
    assert not declaration_path.exists()


def test_50a_does_not_require_direct_continuation_v2_sequence_start(tmp_path: Path) -> None:
    *_, loaded_first, loaded = _declared_v2_bare_sequence(tmp_path)

    assert loaded.sequence.starting_predecessor is loaded_first
    assert loaded_first.verification.edge_format == (
        "pyxis.chromium.research_working_set_note_revision_edge.v1"
    )
    assert loaded.sequence.edges[0].predecessor is loaded_first
