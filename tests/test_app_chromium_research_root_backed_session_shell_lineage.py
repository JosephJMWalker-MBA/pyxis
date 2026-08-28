from __future__ import annotations

from dataclasses import fields
from pathlib import Path

import pytest

from pyxis.app.chromium_research_root_backed_session_reentry import (
    create_chromium_research_root_backed_session_reentry_plan,
    reenter_chromium_research_root_backed_session,
)
from pyxis.app.chromium_research_root_backed_session_reentry_plan_document import (
    persist_chromium_research_root_backed_session_reentry_plan_document,
)
from pyxis.app.chromium_research_root_backed_session_shell_lineage import (
    ChromiumResearchRootBackedSessionContinuationShellLineage,
    ChromiumResearchRootBackedSessionShellLineage,
    ChromiumResearchRootBackedSessionShellLineageError,
    prove_chromium_research_root_backed_session_continuation_shell_lineage,
    prove_chromium_research_root_backed_session_shell_lineage,
)
from pyxis.app.chromium_research_session_working_set_transition_revision_root_edge_extension import (
    create_chromium_research_session_working_set_transition_revision_root_edge_extension,
)
from pyxis.app.chromium_research_session_working_set_transition_revision_root_edge_extension_persistence import (
    persist_chromium_research_session_working_set_transition_revision_root_edge_extension,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_sequence_load import (
    load_chromium_research_working_set_note_revision_edge_sequence,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_sequence_persistence import (
    persist_chromium_research_working_set_note_revision_edge_sequence,
)
from test_app_chromium_research_root_backed_session_continuation_reentry_plan_document import (
    _persist_valid_continuation,
)
from test_app_chromium_research_root_backed_session_reentry_plan_document import (
    _persist_valid_overlay,
)


def test_45a_proves_35c_path_and_retains_fresh_result_from_that_path(
    tmp_path: Path,
) -> None:
    _, _, earned, _, overlay, checkpoint = _persist_valid_overlay(
        tmp_path,
        stem="45a-root",
    )

    lineage = prove_chromium_research_root_backed_session_shell_lineage(
        earned,
        overlay_source=overlay,
    )

    assert isinstance(lineage, ChromiumResearchRootBackedSessionShellLineage)
    assert lineage.overlay_source == overlay.resolve()
    assert lineage.reentry is not earned
    assert lineage.reentry is not checkpoint.fresh_reentry
    assert lineage.reentry.controller.presentation == earned.controller.presentation
    assert (
        lineage.reentry.controller.declared_endpoint.verification.edge_record_sha256
        == earned.controller.declared_endpoint.verification.edge_record_sha256
    )
    assert lineage.reentry.loaded_root.verification.root_record_sha256 == (
        earned.loaded_root.verification.root_record_sha256
    )


def test_45a_proves_35d_path_and_retains_fresh_continuation(
    tmp_path: Path,
) -> None:
    values = _persist_valid_continuation(tmp_path, stem="45a-cont")
    overlay = values[8]
    earned = values[9].fresh_reentry

    lineage = prove_chromium_research_root_backed_session_continuation_shell_lineage(
        earned,
        overlay_source=overlay,
    )

    assert isinstance(lineage, ChromiumResearchRootBackedSessionContinuationShellLineage)
    assert lineage.overlay_source == overlay.resolve()
    assert lineage.reentry is not earned
    assert lineage.reentry.controller.presentation == earned.controller.presentation
    assert (
        lineage.reentry.controller.declared_endpoint.verification.edge_record_sha256
        == earned.controller.declared_endpoint.verification.edge_record_sha256
    )
    assert lineage.reentry.prior_root_backed_reentry.loaded_root.verification.root_record_sha256 == (
        earned.prior_root_backed_reentry.loaded_root.verification.root_record_sha256
    )


def test_45a_path_distinct_durably_equivalent_35c_overlay_is_valid_launch_context(
    tmp_path: Path,
) -> None:
    first = tmp_path / "first"
    second = tmp_path / "second"
    first.mkdir()
    second.mkdir()
    _, _, earned, _, first_overlay, _ = _persist_valid_overlay(first, stem="same")
    _, _, other_earned, _, other_overlay, _ = _persist_valid_overlay(second, stem="same")

    assert first_overlay.resolve() != other_overlay.resolve()
    assert earned.controller.presentation == other_earned.controller.presentation
    assert (
        earned.controller.declared_endpoint.verification.edge_record_sha256
        == other_earned.controller.declared_endpoint.verification.edge_record_sha256
    )
    assert (
        earned.loaded_root.verification.root_record_sha256
        == other_earned.loaded_root.verification.root_record_sha256
    )

    lineage = prove_chromium_research_root_backed_session_shell_lineage(
        earned,
        overlay_source=other_overlay,
    )

    assert lineage.overlay_source == other_overlay.resolve()
    assert lineage.reentry.controller.presentation == earned.controller.presentation


def test_45a_different_valid_35c_endpoint_rejects(
    tmp_path: Path,
) -> None:
    _, _, earned, prior_plan_source, _, _ = _persist_valid_overlay(
        tmp_path,
        stem="different-endpoint",
    )

    alternate_extension = (
        create_chromium_research_session_working_set_transition_revision_root_edge_extension(
            earned.loaded_root,
            revised_note_text="A genuinely different first post-root endpoint.",
        )
    )
    alternate_edge = (
        persist_chromium_research_session_working_set_transition_revision_root_edge_extension(
            alternate_extension,
            root_source=earned.plan.root_source,
            destination=tmp_path / "alternate-root-edge.json",
        )
    )
    alternate_sequence = load_chromium_research_working_set_note_revision_edge_sequence(
        earned.loaded_root,
        (alternate_edge.path,),
    )
    alternate_declaration = tmp_path / "alternate-root-backed-declaration.json"
    persist_chromium_research_working_set_note_revision_edge_sequence(
        alternate_sequence,
        alternate_declaration,
    )
    alternate_plan = create_chromium_research_root_backed_session_reentry_plan(
        earned.plan.prior_session_plan,
        earned.plan.appended_working_set_members,
        changed_working_set_source=earned.plan.changed_working_set_source,
        changed_note_source=earned.plan.changed_note_source,
        transition_source=earned.plan.transition_source,
        root_source=earned.plan.root_source,
        declared_edge_sources=(alternate_edge.path,),
        declaration_source=alternate_declaration,
    )
    alternate_earned = reenter_chromium_research_root_backed_session(alternate_plan)
    different_overlay = tmp_path / "alternate-root-backed.overlay.json"
    persist_chromium_research_root_backed_session_reentry_plan_document(
        alternate_earned,
        prior_session_plan_source=prior_plan_source,
        destination=different_overlay,
    )

    assert (
        alternate_earned.loaded_root.verification.root_record_sha256
        == earned.loaded_root.verification.root_record_sha256
    )
    assert (
        alternate_earned.controller.declared_endpoint.verification.edge_record_sha256
        != earned.controller.declared_endpoint.verification.edge_record_sha256
    )
    with pytest.raises(
        ChromiumResearchRootBackedSessionShellLineageError,
        match="does not match",
    ):
        prove_chromium_research_root_backed_session_shell_lineage(
            earned,
            overlay_source=different_overlay,
        )


def test_45a_tampered_35c_referenced_root_rejects_before_lineage_return(
    tmp_path: Path,
) -> None:
    _, _, earned, _, overlay, _ = _persist_valid_overlay(tmp_path, stem="tampered")
    earned.plan.root_source.write_bytes(earned.plan.root_source.read_bytes() + b"tampered")

    with pytest.raises(
        ChromiumResearchRootBackedSessionShellLineageError,
        match="could not freshly reconstruct",
    ):
        prove_chromium_research_root_backed_session_shell_lineage(
            earned,
            overlay_source=overlay,
        )


def test_45a_lineage_wrappers_carry_only_explicit_source_and_fresh_reentry(
    tmp_path: Path,
) -> None:
    _, _, earned, _, overlay, _ = _persist_valid_overlay(tmp_path, stem="shape")
    lineage = prove_chromium_research_root_backed_session_shell_lineage(
        earned,
        overlay_source=overlay,
    )

    assert tuple(field.name for field in fields(lineage)) == (
        "overlay_source",
        "reentry",
    )
    for forbidden in (
        "latest",
        "current_head",
        "canonical_head",
        "discovered_source",
        "checkpoint",
        "rollover",
        "semantic_support",
        "chronology",
    ):
        assert not hasattr(lineage, forbidden)


def test_45a_wrong_result_families_reject_before_path_work(tmp_path: Path) -> None:
    source = tmp_path / "does-not-need-to-exist.overlay.json"

    with pytest.raises(TypeError, match="ChromiumResearchRootBackedSessionReentryResult"):
        prove_chromium_research_root_backed_session_shell_lineage(
            object(),  # type: ignore[arg-type]
            overlay_source=source,
        )

    with pytest.raises(
        TypeError,
        match="ChromiumResearchRootBackedSessionContinuationReentryResult",
    ):
        prove_chromium_research_root_backed_session_continuation_shell_lineage(
            object(),  # type: ignore[arg-type]
            overlay_source=source,
        )
