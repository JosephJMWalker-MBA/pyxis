from __future__ import annotations

from pathlib import Path

import pytest

from pyxis.app.chromium_research_first_changed_basis_root_edge import (
    persist_chromium_research_first_changed_basis_root_edge,
)
from pyxis.app.chromium_research_first_changed_basis_session_adoption import (
    ChromiumResearchFirstChangedBasisSessionAdoptionResult,
    adopt_chromium_research_first_changed_basis_governed_session,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_sequence_persistence import (
    verify_chromium_research_working_set_note_revision_edge_sequence,
)
from test_ui_research_first_changed_basis_root_edge import _direct_root


_ROOT_FORMAT = (
    "pyxis.chromium.research_session_working_set_transition_revision_root.v1"
)
_EDGE_FORMAT = "pyxis.chromium.research_working_set_note_revision_edge.v1"
_SEQUENCE_FORMAT = "pyxis.chromium.research_working_set_note_revision_edge_sequence.v1"


def _edge(tmp_path: Path, *, stem: str):
    _, _, _, _, root = _direct_root(tmp_path, stem=stem)
    edge = persist_chromium_research_first_changed_basis_root_edge(
        root,
        revised_note_text=f"First post-root rationale for {stem}.",
        root_source=root.persistence.path,
        destination=tmp_path / f"{stem}-edge.json",
    )
    return root, edge


def test_44e_application_declares_and_freshly_relinks_exact_root_backed_session(
    tmp_path: Path,
) -> None:
    root, edge = _edge(tmp_path, stem="44e-app")
    destination = tmp_path / "44e-app-declaration.json"

    result = adopt_chromium_research_first_changed_basis_governed_session(
        edge,
        edge_source=edge.persistence.path,
        declaration_destination=destination,
    )

    assert isinstance(result, ChromiumResearchFirstChangedBasisSessionAdoptionResult)
    assert result.edge_result is edge
    assert result.sequence.starting_predecessor is root.loaded_root
    assert len(result.sequence.edges) == 1
    assert result.sequence.edges[0].verification.edge_record_sha256 == edge.persistence.edge_record_sha256
    assert result.declaration.path == destination.resolve()
    assert result.declaration.sequence_format == _SEQUENCE_FORMAT
    assert result.loaded_declaration.verification.sequence_record_sha256 == result.declaration.sequence_record_sha256
    assert result.loaded_declaration.sequence.starting_predecessor is root.loaded_root
    assert result.controller.loaded is result.loaded_declaration
    assert result.controller.declared_endpoint.verification.edge_record_sha256 == edge.persistence.edge_record_sha256
    assert result.controller.presentation.sequence.starting_record_format == _ROOT_FORMAT

    verification = verify_chromium_research_working_set_note_revision_edge_sequence(destination)
    assert verification.starting_predecessor.record_format == _ROOT_FORMAT
    assert verification.starting_predecessor.record_sha256 == root.persistence.root_record_sha256
    assert len(verification.edges) == 1
    assert verification.edges[0].record_format == _EDGE_FORMAT
    assert verification.edges[0].record_sha256 == edge.persistence.edge_record_sha256


def test_44e_application_accepts_moved_edge_only_through_explicit_new_path(
    tmp_path: Path,
) -> None:
    _, edge = _edge(tmp_path, stem="44e-moved")
    moved_edge = tmp_path / "44e-explicit-moved-edge.json"
    edge.persistence.path.rename(moved_edge)

    result = adopt_chromium_research_first_changed_basis_governed_session(
        edge,
        edge_source=moved_edge,
        declaration_destination=tmp_path / "44e-moved-declaration.json",
    )

    assert result.sequence.edges[0].verification.path == moved_edge.resolve()
    assert result.loaded_declaration.sequence.edges[0].verification.path == moved_edge.resolve()
    assert result.controller.declared_endpoint.verification.edge_record_sha256 == edge.persistence.edge_record_sha256


def test_44e_wrong_edge_source_rejects_without_declaration_write(tmp_path: Path) -> None:
    root, edge = _edge(tmp_path, stem="44e-wrong-edge")
    destination = tmp_path / "44e-wrong-edge-declaration.json"

    with pytest.raises(Exception):
        adopt_chromium_research_first_changed_basis_governed_session(
            edge,
            edge_source=root.persistence.path,
            declaration_destination=destination,
        )
    assert not destination.exists()
