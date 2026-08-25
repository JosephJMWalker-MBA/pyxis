from __future__ import annotations

import json
from pathlib import Path

import pytest

from pyxis.app.chromium_research_root_backed_session_continuation_checkpoint_extension import (
    ChromiumResearchRootBackedSessionContinuationCheckpointExtensionError,
    persist_chromium_research_root_backed_session_continuation_checkpoint_extension,
)
from pyxis.app.chromium_research_root_backed_session_continuation_reentry_plan_document import (
    load_chromium_research_root_backed_session_continuation_reentry_plan_document,
    reenter_chromium_research_root_backed_session_continuation,
)
from pyxis.app.chromium_research_session_rollover import (
    rollover_chromium_research_session_to_persisted_successor,
)
from test_app_chromium_research_root_backed_session_continuation_reentry_plan_document import (
    _persist_valid_continuation,
)


def _extension_fixture(tmp_path: Path, *, stem: str = "35e"):
    *_, current_rollover, current_overlay, checkpoint = _persist_valid_continuation(
        tmp_path,
        stem=stem,
    )
    current = checkpoint.fresh_reentry
    successor = tmp_path / f"{stem}-next-successor.json"
    revision = current.controller.persist_declared_endpoint_revision(
        "Second ordinary continuation after the changed evidence basis.",
        prior_edge_source=current.controller.declared_endpoint.verification.path,
        destination=successor,
    )
    one_hop_declaration = tmp_path / f"{stem}-next-one-hop-declaration.json"
    rollover = rollover_chromium_research_session_to_persisted_successor(
        current.controller,
        revision,
        successor_edge_source=successor,
        declaration_destination=one_hop_declaration,
    )
    cumulative_declaration = tmp_path / f"{stem}-cumulative-declaration.json"
    next_overlay = tmp_path / f"{stem}-next-continuation.overlay.json"
    return (
        current,
        current_rollover,
        current_overlay,
        successor,
        one_hop_declaration,
        rollover,
        cumulative_declaration,
        next_overlay,
    )


def _persist_extension(tmp_path: Path, *, stem: str = "35e"):
    values = _extension_fixture(tmp_path, stem=stem)
    (
        current,
        _,
        current_overlay,
        successor,
        _,
        rollover,
        cumulative_declaration,
        next_overlay,
    ) = values
    result = persist_chromium_research_root_backed_session_continuation_checkpoint_extension(
        current,
        rollover,
        current_overlay_source=current_overlay,
        successor_edge_source=successor,
        cumulative_declaration_destination=cumulative_declaration,
        next_overlay_destination=next_overlay,
    )
    return (*values, result)


def test_35e_extends_post_root_edge_tuple_without_recursive_overlay(tmp_path: Path) -> None:
    (
        current,
        _,
        current_overlay,
        successor,
        _,
        rollover,
        cumulative_declaration,
        next_overlay,
        result,
    ) = _persist_extension(tmp_path)

    assert result.current_reentry is current
    assert result.rollover is rollover
    assert result.next_plan.prior_root_backed_overlay_source == (
        current.plan.prior_root_backed_overlay_source
    )
    assert result.next_plan.declared_edge_sources == (
        *current.plan.declared_edge_sources,
        successor.resolve(),
    )
    assert result.next_plan.declaration_source == cumulative_declaration.resolve()
    assert len(result.explicit_sequence.edges) == len(current.plan.declared_edge_sources) + 1
    assert result.fresh_reentry.controller.declared_endpoint.verification.edge_record_sha256 == (
        rollover.continuation_controller.declared_endpoint.verification.edge_record_sha256
    )

    document = json.loads(next_overlay.read_text(encoding="utf-8"))
    assert document["prior_root_backed_overlay_source"] != current_overlay.name
    assert document["prior_root_backed_overlay_source"].endswith(
        Path(current.plan.prior_root_backed_overlay_source).name
    )
    assert len(document["declared_edge_sources"]) == len(result.next_plan.declared_edge_sources)


def test_35e_cumulative_presentation_is_longer_but_terminal_edge_matches_rollover(
    tmp_path: Path,
) -> None:
    *_, rollover, _, _, result = _persist_extension(tmp_path)

    cumulative = result.fresh_reentry.controller.presentation.sequence
    one_hop = rollover.continuation_controller.presentation.sequence

    assert len(cumulative.members) > len(one_hop.members)
    assert (
        result.fresh_reentry.controller.declared_endpoint.verification.edge_record_sha256
        == rollover.continuation_controller.declared_endpoint.verification.edge_record_sha256
    )
    assert (
        result.fresh_reentry.controller.declared_endpoint.revision.revised_note.note_text
        == rollover.continuation_controller.declared_endpoint.revision.revised_note.note_text
    )


def test_35e_old_overlay_and_one_hop_declarations_remain_untouched(tmp_path: Path) -> None:
    (
        _,
        _,
        current_overlay,
        _,
        one_hop_declaration,
        _,
        _,
        next_overlay,
        _,
    ) = _persist_extension(tmp_path)

    old_overlay_bytes = current_overlay.read_bytes()
    one_hop_bytes = one_hop_declaration.read_bytes()
    assert next_overlay.exists()
    assert current_overlay.read_bytes() == old_overlay_bytes
    assert one_hop_declaration.read_bytes() == one_hop_bytes


def test_35e_next_overlay_roundtrips_through_existing_35d_loader(tmp_path: Path) -> None:
    *_, next_overlay, result = _persist_extension(tmp_path)

    decoded = load_chromium_research_root_backed_session_continuation_reentry_plan_document(
        next_overlay
    )
    fresh = reenter_chromium_research_root_backed_session_continuation(decoded)

    assert decoded == result.next_plan
    assert fresh.controller.declared_endpoint.verification.edge_record_sha256 == (
        result.fresh_reentry.controller.declared_endpoint.verification.edge_record_sha256
    )
    assert fresh.prior_root_backed_reentry.loaded_root.verification.root_record_sha256 == (
        result.fresh_reentry.prior_root_backed_reentry.loaded_root.verification.root_record_sha256
    )


def test_35e_can_extend_a_previous_cumulative_checkpoint_again(tmp_path: Path) -> None:
    *_, first_result = _persist_extension(tmp_path, stem="first")
    current = first_result.fresh_reentry
    successor = tmp_path / "third-successor.json"
    revision = current.controller.persist_declared_endpoint_revision(
        "Third ordinary continuation in the cumulative post-root region.",
        prior_edge_source=current.controller.declared_endpoint.verification.path,
        destination=successor,
    )
    one_hop = tmp_path / "third-one-hop-declaration.json"
    rollover = rollover_chromium_research_session_to_persisted_successor(
        current.controller,
        revision,
        successor_edge_source=successor,
        declaration_destination=one_hop,
    )

    second_result = persist_chromium_research_root_backed_session_continuation_checkpoint_extension(
        current,
        rollover,
        current_overlay_source=first_result.overlay.path,
        successor_edge_source=successor,
        cumulative_declaration_destination=tmp_path / "third-cumulative-declaration.json",
        next_overlay_destination=tmp_path / "third-continuation.overlay.json",
    )

    assert second_result.next_plan.prior_root_backed_overlay_source == (
        first_result.next_plan.prior_root_backed_overlay_source
    )
    assert second_result.next_plan.declared_edge_sources == (
        *first_result.next_plan.declared_edge_sources,
        successor.resolve(),
    )
    assert len(second_result.explicit_sequence.edges) == (
        len(first_result.explicit_sequence.edges) + 1
    )
    assert second_result.fresh_reentry.controller.declared_endpoint.verification.edge_record_sha256 == (
        rollover.continuation_controller.declared_endpoint.verification.edge_record_sha256
    )


def test_35e_wrong_current_overlay_rejects_before_new_writes(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    first.mkdir()
    second.mkdir()
    current, _, _, successor, _, rollover, cumulative, next_overlay = _extension_fixture(
        first,
        stem="first",
    )
    *_, other_overlay, _ = _persist_valid_continuation(second, stem="second")[-3:]

    with pytest.raises(
        ChromiumResearchRootBackedSessionContinuationCheckpointExtensionError,
        match="does not describe",
    ):
        persist_chromium_research_root_backed_session_continuation_checkpoint_extension(
            current,
            rollover,
            current_overlay_source=other_overlay,
            successor_edge_source=successor,
            cumulative_declaration_destination=cumulative,
            next_overlay_destination=next_overlay,
        )

    assert not cumulative.exists()
    assert not next_overlay.exists()


def test_35e_wrong_successor_is_not_discovered_or_replaced(tmp_path: Path) -> None:
    current, _, current_overlay, successor, _, rollover, cumulative, next_overlay = (
        _extension_fixture(tmp_path)
    )
    sibling = tmp_path / "wrong-sibling.json"
    current.controller.persist_declared_endpoint_revision(
        "Wrong explicit sibling.",
        prior_edge_source=current.controller.declared_endpoint.verification.path,
        destination=sibling,
    )
    decoy = tmp_path / "obvious-correct-successor.json"
    decoy.write_bytes(successor.read_bytes())

    with pytest.raises(
        ChromiumResearchRootBackedSessionContinuationCheckpointExtensionError,
        match="endpoint identity does not match",
    ):
        persist_chromium_research_root_backed_session_continuation_checkpoint_extension(
            current,
            rollover,
            current_overlay_source=current_overlay,
            successor_edge_source=sibling,
            cumulative_declaration_destination=cumulative,
            next_overlay_destination=next_overlay,
        )

    assert decoy.exists()
    assert not cumulative.exists()
    assert not next_overlay.exists()


def test_35e_existing_next_overlay_blocks_declaration_write(tmp_path: Path) -> None:
    current, _, current_overlay, successor, _, rollover, cumulative, next_overlay = (
        _extension_fixture(tmp_path)
    )
    next_overlay.write_text("keep exact\n", encoding="utf-8")

    with pytest.raises(FileExistsError, match="next_overlay_destination"):
        persist_chromium_research_root_backed_session_continuation_checkpoint_extension(
            current,
            rollover,
            current_overlay_source=current_overlay,
            successor_edge_source=successor,
            cumulative_declaration_destination=cumulative,
            next_overlay_destination=next_overlay,
        )

    assert not cumulative.exists()
    assert next_overlay.read_text(encoding="utf-8") == "keep exact\n"


def test_35e_existing_cumulative_declaration_blocks_overlay_write(tmp_path: Path) -> None:
    current, _, current_overlay, successor, _, rollover, cumulative, next_overlay = (
        _extension_fixture(tmp_path)
    )
    cumulative.write_text("keep declaration\n", encoding="utf-8")

    with pytest.raises(FileExistsError, match="cumulative_declaration_destination"):
        persist_chromium_research_root_backed_session_continuation_checkpoint_extension(
            current,
            rollover,
            current_overlay_source=current_overlay,
            successor_edge_source=successor,
            cumulative_declaration_destination=cumulative,
            next_overlay_destination=next_overlay,
        )

    assert cumulative.read_text(encoding="utf-8") == "keep declaration\n"
    assert not next_overlay.exists()


def test_35e_tampered_current_ancestry_rejects_before_new_writes(tmp_path: Path) -> None:
    current, _, current_overlay, successor, _, rollover, cumulative, next_overlay = (
        _extension_fixture(tmp_path)
    )
    current.prior_root_backed_reentry.plan.root_source.write_bytes(
        current.prior_root_backed_reentry.plan.root_source.read_bytes() + b"tampered"
    )

    with pytest.raises(
        ChromiumResearchRootBackedSessionContinuationCheckpointExtensionError,
        match="could not freshly reconstruct",
    ):
        persist_chromium_research_root_backed_session_continuation_checkpoint_extension(
            current,
            rollover,
            current_overlay_source=current_overlay,
            successor_edge_source=successor,
            cumulative_declaration_destination=cumulative,
            next_overlay_destination=next_overlay,
        )

    assert not cumulative.exists()
    assert not next_overlay.exists()
