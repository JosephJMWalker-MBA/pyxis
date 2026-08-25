from __future__ import annotations

import json
from pathlib import Path

import pytest

from pyxis.app.chromium_research_second_basis_epoch_continuation_checkpoint_extension import (
    ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionError,
    persist_chromium_research_second_basis_epoch_continuation_checkpoint_extension,
)
from pyxis.app.chromium_research_second_basis_epoch_continuation_reentry_plan_document import (
    load_chromium_research_second_basis_epoch_continuation_reentry_plan_document,
    reenter_chromium_research_second_basis_epoch_continuation,
)
from pyxis.app.chromium_research_session_rollover import (
    rollover_chromium_research_session_to_persisted_successor,
)
from test_app_chromium_research_second_basis_epoch_continuation_reentry_plan_document import (
    _persist_valid_continuation,
)


def _extension_fixture(tmp_path: Path, *, stem: str = "37d"):
    values = _persist_valid_continuation(tmp_path, stem=stem)
    current_overlay = values[6]
    current_checkpoint = values[8]
    current = current_checkpoint.fresh_reentry

    successor = tmp_path / f"{stem}-next-successor.json"
    revision = current.controller.persist_declared_endpoint_revision(
        "Second ordinary continuation after the second evidence-basis epoch.",
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
        current_overlay,
        successor,
        one_hop_declaration,
        rollover,
        cumulative_declaration,
        next_overlay,
        current_checkpoint,
    )


def _persist_extension(tmp_path: Path, *, stem: str = "37d"):
    values = _extension_fixture(tmp_path, stem=stem)
    (
        current,
        current_overlay,
        successor,
        _,
        rollover,
        cumulative_declaration,
        next_overlay,
        _,
    ) = values
    result = persist_chromium_research_second_basis_epoch_continuation_checkpoint_extension(
        current,
        rollover,
        current_overlay_source=current_overlay,
        successor_edge_source=successor,
        cumulative_declaration_destination=cumulative_declaration,
        next_overlay_destination=next_overlay,
    )
    return (*values, result)


def test_37d_extends_edge_tuple_without_recursive_continuation_overlay(
    tmp_path: Path,
) -> None:
    (
        current,
        current_overlay,
        successor,
        _,
        rollover,
        cumulative_declaration,
        next_overlay,
        _,
        result,
    ) = _persist_extension(tmp_path)

    assert result.current_reentry is current
    assert result.rollover is rollover
    assert result.next_plan.prior_second_basis_epoch_overlay_source == (
        current.plan.prior_second_basis_epoch_overlay_source
    )
    assert result.next_plan.prior_second_basis_epoch_overlay_source != current_overlay.resolve()
    assert result.next_plan.declared_edge_sources == (
        *result.current_plan.declared_edge_sources,
        successor.resolve(),
    )
    assert result.next_plan.declaration_source == cumulative_declaration.resolve()
    assert len(result.explicit_sequence.edges) == len(result.current_plan.declared_edge_sources) + 1
    assert (
        result.fresh_reentry.controller.declared_endpoint.verification.edge_record_sha256
        == rollover.continuation_controller.declared_endpoint.verification.edge_record_sha256
    )

    document = json.loads(next_overlay.read_text(encoding="utf-8"))
    assert document["prior_second_basis_epoch_overlay_source"] != current_overlay.name
    assert document["prior_second_basis_epoch_overlay_source"].endswith(
        Path(result.next_plan.prior_second_basis_epoch_overlay_source).name
    )
    assert len(document["declared_edge_sources"]) == len(result.next_plan.declared_edge_sources)


def test_37d_cumulative_presentation_is_longer_but_terminal_choice_matches_rollover(
    tmp_path: Path,
) -> None:
    *_, rollover, _, _, _, result = _persist_extension(tmp_path)

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


def test_37d_old_overlay_and_one_hop_declaration_remain_untouched(tmp_path: Path) -> None:
    (
        _,
        current_overlay,
        _,
        one_hop_declaration,
        _,
        _,
        next_overlay,
        _,
        _,
    ) = _persist_extension(tmp_path)

    old_overlay_bytes = current_overlay.read_bytes()
    one_hop_bytes = one_hop_declaration.read_bytes()
    assert next_overlay.exists()
    assert current_overlay.read_bytes() == old_overlay_bytes
    assert one_hop_declaration.read_bytes() == one_hop_bytes


def test_37d_next_overlay_roundtrips_through_unchanged_37c_loader(tmp_path: Path) -> None:
    *_, next_overlay, _, result = _persist_extension(tmp_path)

    decoded = load_chromium_research_second_basis_epoch_continuation_reentry_plan_document(
        next_overlay
    )
    fresh = reenter_chromium_research_second_basis_epoch_continuation(decoded)

    assert decoded == result.next_plan
    assert (
        fresh.controller.declared_endpoint.verification.edge_record_sha256
        == result.fresh_reentry.controller.declared_endpoint.verification.edge_record_sha256
    )
    assert fresh.prior_second_basis_epoch_reentry.loaded_root.verification.root_record_sha256 == (
        result.fresh_reentry.prior_second_basis_epoch_reentry.loaded_root.verification.root_record_sha256
    )
    assert (
        fresh.prior_second_basis_epoch_reentry.prior_continuation_reentry.prior_root_backed_reentry.loaded_root.verification.root_record_sha256
        == result.fresh_reentry.prior_second_basis_epoch_reentry.prior_continuation_reentry.prior_root_backed_reentry.loaded_root.verification.root_record_sha256
    )


def test_37d_can_extend_a_previous_cumulative_checkpoint_again(tmp_path: Path) -> None:
    *_, first_result = _persist_extension(tmp_path, stem="first")
    current = first_result.fresh_reentry
    successor = tmp_path / "third-successor.json"
    revision = current.controller.persist_declared_endpoint_revision(
        "Third ordinary continuation after the second evidence-basis epoch.",
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

    second_result = persist_chromium_research_second_basis_epoch_continuation_checkpoint_extension(
        current,
        rollover,
        current_overlay_source=first_result.overlay.path,
        successor_edge_source=successor,
        cumulative_declaration_destination=tmp_path / "third-cumulative-declaration.json",
        next_overlay_destination=tmp_path / "third-continuation.overlay.json",
    )

    assert second_result.next_plan.prior_second_basis_epoch_overlay_source == (
        first_result.next_plan.prior_second_basis_epoch_overlay_source
    )
    assert second_result.next_plan.declared_edge_sources == (
        *first_result.next_plan.declared_edge_sources,
        successor.resolve(),
    )
    assert len(second_result.explicit_sequence.edges) == len(first_result.explicit_sequence.edges) + 1
    assert (
        second_result.fresh_reentry.controller.declared_endpoint.verification.edge_record_sha256
        == rollover.continuation_controller.declared_endpoint.verification.edge_record_sha256
    )


def test_37d_path_distinct_durably_equivalent_current_overlay_is_valid_authority(
    tmp_path: Path,
) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    first.mkdir()
    second.mkdir()
    current, _, successor, _, rollover, cumulative, next_overlay, _ = _extension_fixture(
        first,
        stem="same",
    )
    other_values = _persist_valid_continuation(second, stem="same")
    other_overlay = other_values[6]
    other_current = other_values[8].fresh_reentry

    assert other_current.controller.declared_endpoint.verification.path != (
        current.controller.declared_endpoint.verification.path
    )
    assert (
        other_current.controller.declared_endpoint.verification.edge_record_sha256
        == current.controller.declared_endpoint.verification.edge_record_sha256
    )
    assert other_current.prior_second_basis_epoch_reentry.loaded_root.verification.root_record_sha256 == (
        current.prior_second_basis_epoch_reentry.loaded_root.verification.root_record_sha256
    )

    result = persist_chromium_research_second_basis_epoch_continuation_checkpoint_extension(
        current,
        rollover,
        current_overlay_source=other_overlay,
        successor_edge_source=successor,
        cumulative_declaration_destination=cumulative,
        next_overlay_destination=next_overlay,
    )

    assert result.current_plan.prior_second_basis_epoch_overlay_source == (
        other_current.plan.prior_second_basis_epoch_overlay_source
    )
    assert result.fresh_reentry.controller.declared_endpoint.verification.edge_record_sha256 == (
        rollover.continuation_controller.declared_endpoint.verification.edge_record_sha256
    )


def test_37d_wrong_current_overlay_rejects_before_new_writes(tmp_path: Path) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    first.mkdir()
    second.mkdir()
    current, _, successor, _, rollover, cumulative, next_overlay, _ = _extension_fixture(
        first,
        stem="first",
    )
    other_values = _persist_valid_continuation(second, stem="genuinely-different")
    other_overlay = other_values[6]

    with pytest.raises(
        ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionError,
        match="does not match",
    ):
        persist_chromium_research_second_basis_epoch_continuation_checkpoint_extension(
            current,
            rollover,
            current_overlay_source=other_overlay,
            successor_edge_source=successor,
            cumulative_declaration_destination=cumulative,
            next_overlay_destination=next_overlay,
        )

    assert not cumulative.exists()
    assert not next_overlay.exists()


def test_37d_wrong_successor_is_not_discovered_or_replaced(tmp_path: Path) -> None:
    current, current_overlay, successor, _, rollover, cumulative, next_overlay, _ = (
        _extension_fixture(tmp_path, stem="wrong-successor")
    )
    sibling = tmp_path / "wrong-sibling.json"
    current.controller.persist_declared_endpoint_revision(
        "Wrong explicit sibling for cumulative second-epoch continuation.",
        prior_edge_source=current.controller.declared_endpoint.verification.path,
        destination=sibling,
    )
    decoy = tmp_path / "obvious-correct-successor.json"
    decoy.write_bytes(successor.read_bytes())

    with pytest.raises(
        ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionError,
        match="endpoint identity does not match",
    ):
        persist_chromium_research_second_basis_epoch_continuation_checkpoint_extension(
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


def test_37d_tampered_second_root_rejects_before_new_writes(tmp_path: Path) -> None:
    current, current_overlay, successor, _, rollover, cumulative, next_overlay, _ = (
        _extension_fixture(tmp_path, stem="tampered-second")
    )
    second_root = current.prior_second_basis_epoch_reentry.plan.root_source
    second_root.write_bytes(second_root.read_bytes() + b"tampered")

    with pytest.raises(
        ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionError,
        match="could not freshly reconstruct",
    ):
        persist_chromium_research_second_basis_epoch_continuation_checkpoint_extension(
            current,
            rollover,
            current_overlay_source=current_overlay,
            successor_edge_source=successor,
            cumulative_declaration_destination=cumulative,
            next_overlay_destination=next_overlay,
        )

    assert not cumulative.exists()
    assert not next_overlay.exists()


def test_37d_tampered_retained_first_root_rejects_before_new_writes(tmp_path: Path) -> None:
    current, current_overlay, successor, _, rollover, cumulative, next_overlay, _ = (
        _extension_fixture(tmp_path, stem="tampered-first")
    )
    first_root = (
        current.prior_second_basis_epoch_reentry.prior_continuation_reentry.prior_root_backed_reentry.plan.root_source
    )
    first_root.write_bytes(first_root.read_bytes() + b"tampered")

    with pytest.raises(
        ChromiumResearchSecondBasisEpochContinuationCheckpointExtensionError,
        match="could not freshly reconstruct",
    ):
        persist_chromium_research_second_basis_epoch_continuation_checkpoint_extension(
            current,
            rollover,
            current_overlay_source=current_overlay,
            successor_edge_source=successor,
            cumulative_declaration_destination=cumulative,
            next_overlay_destination=next_overlay,
        )

    assert not cumulative.exists()
    assert not next_overlay.exists()


def test_37d_existing_next_overlay_blocks_declaration_write(tmp_path: Path) -> None:
    current, current_overlay, successor, _, rollover, cumulative, next_overlay, _ = (
        _extension_fixture(tmp_path, stem="existing-overlay")
    )
    next_overlay.write_text("keep exact\n", encoding="utf-8")

    with pytest.raises(FileExistsError, match="next_overlay_destination"):
        persist_chromium_research_second_basis_epoch_continuation_checkpoint_extension(
            current,
            rollover,
            current_overlay_source=current_overlay,
            successor_edge_source=successor,
            cumulative_declaration_destination=cumulative,
            next_overlay_destination=next_overlay,
        )

    assert not cumulative.exists()
    assert next_overlay.read_text(encoding="utf-8") == "keep exact\n"


def test_37d_existing_cumulative_declaration_blocks_overlay_write(tmp_path: Path) -> None:
    current, current_overlay, successor, _, rollover, cumulative, next_overlay, _ = (
        _extension_fixture(tmp_path, stem="existing-declaration")
    )
    cumulative.write_text("keep declaration\n", encoding="utf-8")

    with pytest.raises(FileExistsError, match="cumulative_declaration_destination"):
        persist_chromium_research_second_basis_epoch_continuation_checkpoint_extension(
            current,
            rollover,
            current_overlay_source=current_overlay,
            successor_edge_source=successor,
            cumulative_declaration_destination=cumulative,
            next_overlay_destination=next_overlay,
        )

    assert cumulative.read_text(encoding="utf-8") == "keep declaration\n"
    assert not next_overlay.exists()


def test_37d_same_destination_rejects_before_write(tmp_path: Path) -> None:
    current, current_overlay, successor, _, rollover, _, _, _ = _extension_fixture(
        tmp_path,
        stem="same-destination",
    )
    destination = tmp_path / "same-output.json"

    with pytest.raises(ValueError, match="must be distinct"):
        persist_chromium_research_second_basis_epoch_continuation_checkpoint_extension(
            current,
            rollover,
            current_overlay_source=current_overlay,
            successor_edge_source=successor,
            cumulative_declaration_destination=destination,
            next_overlay_destination=destination,
        )

    assert not destination.exists()
