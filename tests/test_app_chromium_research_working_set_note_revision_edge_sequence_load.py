from __future__ import annotations

from dataclasses import FrozenInstanceError, replace
import json
from pathlib import Path

import pytest

from test_app_chromium_research_working_set_note_revision_edge_extension_persistence import (
    _durable_successor,
)
from test_app_chromium_research_working_set_note_revision_edge_load import _write_edge
from pyxis.app.chromium_research_working_set_note_revision_edge_extension import (
    create_chromium_research_working_set_note_revision_edge_extension,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_extension_persistence import (
    persist_chromium_research_working_set_note_revision_edge_extension,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_load import (
    load_chromium_research_working_set_note_revision_edge,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_persistence import (
    ChromiumResearchWorkingSetNoteRevisionEdgeIntegrityError,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_sequence_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceRecord,
    ChromiumResearchWorkingSetNoteRevisionEdgeSequenceRelinkError,
    load_chromium_research_working_set_note_revision_edge_sequence,
)


_SEQUENCE_MODE = (
    "caller_explicit_ordered_relinked_research_working_set_note_revision_edge_sequence"
)


def _two_successor_edges(
    tmp_path: Path,
    *,
    v4_text: str = "v4 exact wording",
    v5_text: str = "v5 exact wording",
    v6_text: str = "v6 exact wording",
):
    (
        prefix,
        v4_path,
        loaded_v4,
        extension_v5,
        v5_path,
        persisted_v5,
    ) = _durable_successor(
        tmp_path,
        v4_text=v4_text,
        v5_text=v5_text,
    )
    loaded_v5 = load_chromium_research_working_set_note_revision_edge(
        loaded_v4,
        v5_path,
    )
    extension_v6 = create_chromium_research_working_set_note_revision_edge_extension(
        loaded_v5,
        revised_note_text=v6_text,
    )
    v6_path = tmp_path / "second-successor-edge.json"
    persisted_v6 = persist_chromium_research_working_set_note_revision_edge_extension(
        extension_v6,
        v5_path,
        v6_path,
    )
    return (
        prefix,
        v4_path,
        loaded_v4,
        extension_v5,
        v5_path,
        loaded_v5,
        persisted_v5,
        extension_v6,
        v6_path,
        persisted_v6,
    )


def test_sequence_loads_explicit_edges_in_order_with_exact_identity(tmp_path: Path) -> None:
    (
        _,
        _,
        loaded_v4,
        _,
        v5_path,
        _,
        _,
        _,
        v6_path,
        _,
    ) = _two_successor_edges(
        tmp_path,
        v4_text="v4 exact wording",
        v5_text="  v5 wording 😀\nStill tentative.  ",
        v6_text="  v6 after another check.\nStill human-owned.  ",
    )

    sequence = load_chromium_research_working_set_note_revision_edge_sequence(
        loaded_v4,
        (path for path in (v5_path, v6_path)),
    )

    assert isinstance(sequence, ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceRecord)
    assert sequence.sequence_mode == _SEQUENCE_MODE
    assert sequence.starting_predecessor is loaded_v4
    assert len(sequence.edges) == 2
    assert sequence.edges[0].predecessor is loaded_v4
    assert sequence.edges[0].revision.prior_note is loaded_v4.revision.revised_note
    assert sequence.edges[0].revision.revised_note.note_text == (
        "  v5 wording 😀\nStill tentative.  "
    )
    assert sequence.edges[1].predecessor is sequence.edges[0]
    assert sequence.edges[1].revision.prior_note is sequence.edges[0].revision.revised_note
    assert sequence.edges[1].revision.revised_note.note_text == (
        "  v6 after another check.\nStill human-owned.  "
    )

    with pytest.raises(FrozenInstanceError):
        sequence.sequence_mode = "changed"  # type: ignore[misc]


def test_sequence_can_resume_from_an_already_loaded_edge(tmp_path: Path) -> None:
    (
        _,
        _,
        _,
        _,
        _,
        loaded_v5,
        _,
        _,
        v6_path,
        _,
    ) = _two_successor_edges(tmp_path)

    sequence = load_chromium_research_working_set_note_revision_edge_sequence(
        loaded_v5,
        [v6_path],
    )

    assert sequence.starting_predecessor is loaded_v5
    assert len(sequence.edges) == 1
    assert sequence.edges[0].predecessor is loaded_v5
    assert sequence.edges[0].revision.revised_note.note_text == "v6 exact wording"


def test_sequence_uses_explicit_moved_paths_without_path_identity(tmp_path: Path) -> None:
    (
        _,
        _,
        loaded_v4,
        _,
        v5_path,
        _,
        _,
        _,
        v6_path,
        _,
    ) = _two_successor_edges(tmp_path)
    moved_v5 = tmp_path / "moved-v5-edge.json"
    moved_v6 = tmp_path / "moved-v6-edge.json"
    v5_path.replace(moved_v5)
    v6_path.replace(moved_v6)

    sequence = load_chromium_research_working_set_note_revision_edge_sequence(
        loaded_v4,
        [moved_v5, moved_v6],
    )

    assert sequence.edges[0].verification.path == moved_v5.resolve()
    assert sequence.edges[1].verification.path == moved_v6.resolve()
    assert sequence.edges[1].predecessor is sequence.edges[0]


def test_sequence_rejects_skipped_predecessor_at_exact_position_zero(tmp_path: Path) -> None:
    (
        _,
        _,
        loaded_v4,
        _,
        _,
        _,
        _,
        _,
        v6_path,
        _,
    ) = _two_successor_edges(tmp_path)

    with pytest.raises(
        ChromiumResearchWorkingSetNoteRevisionEdgeSequenceRelinkError,
        match="member 0",
    ):
        load_chromium_research_working_set_note_revision_edge_sequence(
            loaded_v4,
            [v6_path],
        )


def test_sequence_does_not_reorder_or_treat_siblings_as_a_chain(tmp_path: Path) -> None:
    _, _, _, loaded_v4, _, _ = _durable_successor(
        tmp_path,
        v4_text="v4 shared predecessor",
        v5_text="unused first successor",
    )
    first = tmp_path / "sibling-a.json"
    second = tmp_path / "sibling-b.json"
    for path, text in ((first, "sibling A"), (second, "sibling B")):
        _write_edge(
            path,
            predecessor_format=loaded_v4.verification.edge_format,
            predecessor_sha256=loaded_v4.verification.edge_record_sha256,
            revised_note_text=text,
        )

    with pytest.raises(
        ChromiumResearchWorkingSetNoteRevisionEdgeSequenceRelinkError,
        match="member 1",
    ):
        load_chromium_research_working_set_note_revision_edge_sequence(
            loaded_v4,
            [first, second],
        )


def test_sequence_stops_at_first_invalid_member_without_skipping(tmp_path: Path) -> None:
    (
        _,
        _,
        loaded_v4,
        _,
        v5_path,
        _,
        _,
        _,
        v6_path,
        _,
    ) = _two_successor_edges(tmp_path)
    document = json.loads(v5_path.read_text(encoding="utf-8"))
    document["edge_record"]["edge"]["revision"]["revised_note"]["text"] = (
        "tampered without recomputing digest"
    )
    v5_path.write_text(
        json.dumps(document, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    v6_path.unlink()

    with pytest.raises(
        ChromiumResearchWorkingSetNoteRevisionEdgeSequenceRelinkError,
        match="member 0",
    ) as exc_info:
        load_chromium_research_working_set_note_revision_edge_sequence(
            loaded_v4,
            [v5_path, v6_path],
        )

    assert isinstance(
        exc_info.value.__cause__,
        ChromiumResearchWorkingSetNoteRevisionEdgeIntegrityError,
    )


def test_sequence_needs_only_loaded_start_and_explicit_sequence_files(tmp_path: Path) -> None:
    (
        prefix,
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
    v4_path.unlink(missing_ok=True)

    sequence = load_chromium_research_working_set_note_revision_edge_sequence(
        loaded_v4,
        [v5_path, v6_path],
    )

    assert len(sequence.edges) == 2
    assert sequence.edges[0].predecessor is loaded_v4
    assert not v4_path.exists()
    assert not continuation_path.exists()


def test_sequence_does_not_recursively_audit_ancestry_below_start(tmp_path: Path) -> None:
    (
        _,
        _,
        loaded_v4,
        _,
        _,
        loaded_v5,
        _,
        _,
        v6_path,
        _,
    ) = _two_successor_edges(tmp_path)

    forged_v4_verification = replace(
        loaded_v4.verification,
        predecessor_record_sha256="f" * 64,
    )
    forged_v4 = replace(loaded_v4, verification=forged_v4_verification)
    locally_coherent_v5 = replace(loaded_v5, predecessor=forged_v4)

    sequence = load_chromium_research_working_set_note_revision_edge_sequence(
        locally_coherent_v5,
        [v6_path],
    )

    assert sequence.starting_predecessor is locally_coherent_v5
    assert sequence.edges[0].predecessor is locally_coherent_v5
    assert sequence.edges[0].revision.revised_note.note_text == "v6 exact wording"


def test_sequence_rejects_invalid_start_empty_sequence_and_single_path(tmp_path: Path) -> None:
    _, _, _, loaded_v4, _, _ = _durable_successor(tmp_path)
    path = tmp_path / "one-edge.json"

    with pytest.raises(TypeError, match="starting_predecessor must be"):
        load_chromium_research_working_set_note_revision_edge_sequence(  # type: ignore[arg-type]
            object(),
            [path],
        )

    with pytest.raises(ValueError, match="at least one"):
        load_chromium_research_working_set_note_revision_edge_sequence(
            loaded_v4,
            [],
        )

    with pytest.raises(TypeError, match="ordered iterable"):
        load_chromium_research_working_set_note_revision_edge_sequence(
            loaded_v4,
            path,  # type: ignore[arg-type]
        )


def test_sequence_module_is_publicly_importable(tmp_path: Path) -> None:
    _, _, loaded_v4, _, v5_path, _ = _durable_successor(tmp_path)

    sequence = load_chromium_research_working_set_note_revision_edge_sequence(
        loaded_v4,
        [v5_path],
    )

    assert isinstance(sequence, ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceRecord)
    assert sequence.sequence_mode == _SEQUENCE_MODE
