from __future__ import annotations

from dataclasses import fields, replace
from pathlib import Path

import pytest

from pyxis.app.chromium_research_passage_selection import (
    select_chromium_research_capture_paragraph,
)
from pyxis.app.chromium_research_second_basis_epoch_reentry import (
    ChromiumResearchSecondBasisEpochReentryError,
    ChromiumResearchSecondBasisEpochReentryPlan,
    ChromiumResearchSecondBasisEpochReentryResult,
    create_chromium_research_second_basis_epoch_reentry_plan,
    reenter_chromium_research_second_basis_epoch,
)
from pyxis.app.chromium_research_selection_note import (
    create_chromium_research_paragraph_note,
)
from pyxis.app.chromium_research_selection_note_load import (
    load_chromium_research_paragraph_note,
)
from pyxis.app.chromium_research_selection_note_persistence import (
    persist_chromium_research_paragraph_note,
)
from pyxis.app.chromium_research_session_reentry import (
    ChromiumResearchParagraphNoteReentryLocator,
)
from pyxis.app.chromium_research_session_working_set_extension import (
    persist_chromium_research_session_working_set_extension,
)
from pyxis.app.chromium_research_session_working_set_transition import (
    create_chromium_research_session_working_set_transition,
)
from pyxis.app.chromium_research_session_working_set_transition_load import (
    load_chromium_research_session_working_set_transition,
)
from pyxis.app.chromium_research_session_working_set_transition_persistence import (
    persist_chromium_research_session_working_set_transition,
)
from pyxis.app.chromium_research_session_working_set_transition_revision_root import (
    create_chromium_research_session_working_set_transition_revision_root,
)
from pyxis.app.chromium_research_session_working_set_transition_revision_root_edge_extension import (
    create_chromium_research_session_working_set_transition_revision_root_edge_extension,
)
from pyxis.app.chromium_research_session_working_set_transition_revision_root_edge_extension_persistence import (
    persist_chromium_research_session_working_set_transition_revision_root_edge_extension,
)
from pyxis.app.chromium_research_session_working_set_transition_revision_root_load import (
    load_chromium_research_session_working_set_transition_revision_root,
)
from pyxis.app.chromium_research_session_working_set_transition_revision_root_persistence import (
    persist_chromium_research_session_working_set_transition_revision_root,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_sequence_load import (
    load_chromium_research_working_set_note_revision_edge_sequence,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_sequence_persistence import (
    persist_chromium_research_working_set_note_revision_edge_sequence,
)
from test_app_chromium_research_root_backed_session_continuation_checkpoint_extension import (
    _persist_extension as _persist_cumulative_continuation,
)
from test_app_chromium_research_root_backed_session_continuation_reentry_plan_document import (
    _persist_valid_continuation,
)
from test_app_chromium_research_session_reentry import _persist_loaded_capture


def _prior_continuation(tmp_path: Path, *, cumulative: bool, stem: str):
    tmp_path.mkdir(parents=True, exist_ok=True)
    if cumulative:
        *_, overlay, extension = _persist_cumulative_continuation(tmp_path, stem=stem)
        return overlay, extension.fresh_reentry
    *_, overlay, checkpoint = _persist_valid_continuation(tmp_path, stem=stem)
    return overlay, checkpoint.fresh_reentry


def _new_paragraph_member_with_locator(tmp_path: Path, *, stem: str):
    source = _persist_loaded_capture(
        tmp_path,
        stem=stem,
        target_id=f"page-{stem}",
        url=f"https://example.test/{stem}",
        paragraph_text=f"Second-epoch evidence paragraph for {stem}.",
    )
    paragraph = select_chromium_research_capture_paragraph(
        source,
        paragraph_ordinal=1,
    )
    note = create_chromium_research_paragraph_note(
        paragraph,
        note_text=f"Second-epoch explicit source note for {stem}.",
    )
    note_path = tmp_path / f"{stem}-paragraph-note.json"
    persist_chromium_research_paragraph_note(note, note_path)
    loaded = load_chromium_research_paragraph_note(source, note_path)
    locator = ChromiumResearchParagraphNoteReentryLocator(
        source.verification.path,
        note_path,
    )
    return loaded, locator


def _second_epoch_fixture(
    tmp_path: Path,
    *,
    cumulative_prior: bool = False,
    stem: str = "37a",
):
    prior_dir = tmp_path / "prior"
    second_dir = tmp_path / "second"
    second_dir.mkdir(parents=True, exist_ok=True)
    prior_overlay, prior = _prior_continuation(
        prior_dir,
        cumulative=cumulative_prior,
        stem=f"{stem}-prior",
    )

    member, locator = _new_paragraph_member_with_locator(
        second_dir,
        stem=f"{stem}-member",
    )
    prepared = persist_chromium_research_session_working_set_extension(
        prior.controller,
        (member,),
        rationale_text="Second evidence-basis rationale before its first revision.",
        working_set_destination=second_dir / f"{stem}-working-set.json",
        note_destination=second_dir / f"{stem}-working-set-note.json",
    )

    transition = create_chromium_research_session_working_set_transition(
        prior.controller,
        prepared,
    )
    transition_persistence = persist_chromium_research_session_working_set_transition(
        transition,
        prior_edge_source=prior.controller.declared_endpoint.verification.path,
        working_set_source=prepared.working_set_persistence.path,
        note_source=prepared.note_persistence.path,
        destination=second_dir / f"{stem}-transition.json",
    )
    loaded_transition = load_chromium_research_session_working_set_transition(
        prior.controller.declared_endpoint,
        prepared.working_set.items,
        prior_edge_source=prior.controller.declared_endpoint.verification.path,
        working_set_source=prepared.working_set_persistence.path,
        note_source=prepared.note_persistence.path,
        transition_source=transition_persistence.path,
    )

    root = create_chromium_research_session_working_set_transition_revision_root(
        loaded_transition,
        revised_note_text="First rationale revision in the second evidence-basis epoch.",
    )
    root_persistence = persist_chromium_research_session_working_set_transition_revision_root(
        root,
        prior_edge_source=prior.controller.declared_endpoint.verification.path,
        working_set_source=prepared.working_set_persistence.path,
        note_source=prepared.note_persistence.path,
        transition_source=transition_persistence.path,
        destination=second_dir / f"{stem}-root.json",
    )
    loaded_root = load_chromium_research_session_working_set_transition_revision_root(
        prior.controller.declared_endpoint,
        prepared.working_set.items,
        prior_edge_source=prior.controller.declared_endpoint.verification.path,
        working_set_source=prepared.working_set_persistence.path,
        note_source=prepared.note_persistence.path,
        transition_source=transition_persistence.path,
        root_source=root_persistence.path,
    )

    first_edge = create_chromium_research_session_working_set_transition_revision_root_edge_extension(
        loaded_root,
        revised_note_text="Second-epoch first ordinary edge after the second root.",
    )
    first_edge_persistence = (
        persist_chromium_research_session_working_set_transition_revision_root_edge_extension(
            first_edge,
            root_source=root_persistence.path,
            destination=second_dir / f"{stem}-root-edge.json",
        )
    )
    sequence = load_chromium_research_working_set_note_revision_edge_sequence(
        loaded_root,
        (first_edge_persistence.path,),
    )
    declaration_path = second_dir / f"{stem}-declaration.json"
    persist_chromium_research_working_set_note_revision_edge_sequence(
        sequence,
        declaration_path,
    )

    plan = create_chromium_research_second_basis_epoch_reentry_plan(
        prior_overlay,
        (locator,),
        changed_working_set_source=prepared.working_set_persistence.path,
        changed_note_source=prepared.note_persistence.path,
        transition_source=transition_persistence.path,
        root_source=root_persistence.path,
        declared_edge_sources=(first_edge_persistence.path,),
        declaration_source=declaration_path,
    )
    return {
        "prior_overlay": prior_overlay,
        "prior": prior,
        "member": member,
        "locator": locator,
        "prepared": prepared,
        "transition": transition_persistence,
        "root": root_persistence,
        "loaded_root": loaded_root,
        "edge": first_edge_persistence,
        "declaration": declaration_path,
        "plan": plan,
    }


def test_second_epoch_fresh_reentry_above_persisted_35d_continuation(tmp_path: Path) -> None:
    fixture = _second_epoch_fixture(tmp_path, cumulative_prior=False)

    result = reenter_chromium_research_second_basis_epoch(fixture["plan"])

    assert isinstance(result, ChromiumResearchSecondBasisEpochReentryResult)
    assert result.plan is fixture["plan"]
    assert result.prior_continuation_reentry is not fixture["prior"]
    assert result.prior_continuation_reentry.controller.presentation == (
        fixture["prior"].controller.presentation
    )
    assert result.loaded_root.verification.root_record_sha256 == (
        fixture["root"].root_record_sha256
    )
    assert result.controller.declared_endpoint.verification.edge_record_sha256 == (
        fixture["edge"].edge_record_sha256
    )
    assert result.controller.presentation.sequence.starting_record_format == (
        "pyxis.chromium.research_session_working_set_transition_revision_root.v1"
    )


def test_second_epoch_fresh_reentry_above_cumulative_35e_continuation(tmp_path: Path) -> None:
    fixture = _second_epoch_fixture(tmp_path, cumulative_prior=True, stem="cumulative")

    result = reenter_chromium_research_second_basis_epoch(fixture["plan"])

    assert len(result.prior_continuation_reentry.plan.declared_edge_sources) >= 2
    assert result.controller.declared_endpoint.verification.edge_record_sha256 == (
        fixture["edge"].edge_record_sha256
    )
    assert result.successor_items[:-1] == (
        result.prior_continuation_reentry.controller.declared_endpoint.revision.revised_note.working_set.items
    )
    assert result.loaded_appended_members[-1].note.note_text.startswith(
        "Second-epoch explicit source note"
    )


def test_second_epoch_retains_first_and_second_roots_as_distinct_ancestry_layers(
    tmp_path: Path,
) -> None:
    fixture = _second_epoch_fixture(tmp_path, cumulative_prior=True, stem="layers")

    result = reenter_chromium_research_second_basis_epoch(fixture["plan"])
    first_root = (
        result.prior_continuation_reentry.prior_root_backed_reentry.loaded_root
    )

    assert first_root is not result.loaded_root
    assert first_root.verification.root_record_sha256 != (
        result.loaded_root.verification.root_record_sha256
    )
    assert result.loaded_root.transition.prior_endpoint.verification.edge_record_sha256 == (
        result.prior_continuation_reentry.controller.declared_endpoint.verification.edge_record_sha256
    )


def test_second_epoch_plan_shape_does_not_embed_first_epoch_plan_or_head_state(
    tmp_path: Path,
) -> None:
    fixture = _second_epoch_fixture(tmp_path, stem="shape")
    plan = fixture["plan"]

    assert isinstance(plan, ChromiumResearchSecondBasisEpochReentryPlan)
    assert tuple(field.name for field in fields(plan)) == (
        "prior_root_backed_continuation_overlay_source",
        "appended_working_set_members",
        "changed_working_set_source",
        "changed_note_source",
        "transition_source",
        "root_source",
        "declared_edge_sources",
        "declaration_source",
    )
    for forbidden in (
        "prior_session_plan",
        "prior_root_backed_plan",
        "latest",
        "current_head",
        "canonical_head",
        "chronology",
        "semantic_support",
    ):
        assert not hasattr(plan, forbidden)


def test_missing_prior_continuation_overlay_rejects_without_discovery(tmp_path: Path) -> None:
    fixture = _second_epoch_fixture(tmp_path, stem="missing-prior")
    plan = replace(
        fixture["plan"],
        prior_root_backed_continuation_overlay_source=tmp_path / "does-not-exist.overlay.json",
    )

    with pytest.raises(
        ChromiumResearchSecondBasisEpochReentryError,
        match="prior 35D/35E continuation overlay could not be decoded",
    ):
        reenter_chromium_research_second_basis_epoch(plan)


def test_tampered_second_root_rejects_fresh_reentry(tmp_path: Path) -> None:
    fixture = _second_epoch_fixture(tmp_path, stem="tampered-root")
    fixture["root"].path.write_bytes(fixture["root"].path.read_bytes() + b"tampered")

    with pytest.raises(
        ChromiumResearchSecondBasisEpochReentryError,
        match="second changed working set, 33B transition, and 34A root",
    ):
        reenter_chromium_research_second_basis_epoch(fixture["plan"])


def test_wrong_second_declared_edge_rejects_without_decoy_discovery(tmp_path: Path) -> None:
    fixture = _second_epoch_fixture(tmp_path, stem="wrong-edge")
    wrong = tmp_path / "wrong-edge.json"
    wrong.write_text("{}\n", encoding="utf-8")
    decoy = tmp_path / "obvious-correct-edge.json"
    decoy.write_bytes(fixture["edge"].path.read_bytes())
    plan = replace(fixture["plan"], declared_edge_sources=(wrong,))

    with pytest.raises(
        ChromiumResearchSecondBasisEpochReentryError,
        match="second root-backed declared segment",
    ):
        reenter_chromium_research_second_basis_epoch(plan)

    assert decoy.exists()


def test_moved_second_epoch_locations_work_only_when_explicitly_resupplied(tmp_path: Path) -> None:
    fixture = _second_epoch_fixture(tmp_path, stem="moved")
    plan = fixture["plan"]

    moved_overlay = fixture["prior_overlay"].rename(
        fixture["prior_overlay"].with_name("moved-prior.overlay.json")
    )
    moved_working_set = plan.changed_working_set_source.rename(
        plan.changed_working_set_source.with_name("moved-working-set.json")
    )
    moved_note = plan.changed_note_source.rename(
        plan.changed_note_source.with_name("moved-note.json")
    )
    moved_transition = plan.transition_source.rename(
        plan.transition_source.with_name("moved-transition.json")
    )
    moved_root = plan.root_source.rename(plan.root_source.with_name("moved-root.json"))
    moved_edge = plan.declared_edge_sources[0].rename(
        plan.declared_edge_sources[0].with_name("moved-edge.json")
    )
    moved_declaration = plan.declaration_source.rename(
        plan.declaration_source.with_name("moved-declaration.json")
    )

    moved_plan = create_chromium_research_second_basis_epoch_reentry_plan(
        moved_overlay,
        plan.appended_working_set_members,
        changed_working_set_source=moved_working_set,
        changed_note_source=moved_note,
        transition_source=moved_transition,
        root_source=moved_root,
        declared_edge_sources=(moved_edge,),
        declaration_source=moved_declaration,
    )
    result = reenter_chromium_research_second_basis_epoch(moved_plan)

    assert result.loaded_root.verification.path == moved_root.resolve()
    assert result.controller.declared_endpoint.verification.path == moved_edge.resolve()


def test_path_distinct_content_identical_prior_continuation_is_valid_authority(
    tmp_path: Path,
) -> None:
    fixture = _second_epoch_fixture(tmp_path / "earned", stem="same")
    other_overlay, other_prior = _prior_continuation(
        tmp_path / "other-prior",
        cumulative=False,
        stem="same",
    )

    assert other_prior.controller is not fixture["prior"].controller
    assert other_prior.controller.presentation == fixture["prior"].controller.presentation
    assert other_prior.controller.declared_endpoint.verification.path != (
        fixture["prior"].controller.declared_endpoint.verification.path
    )
    assert other_prior.controller.declared_endpoint.verification.edge_record_sha256 == (
        fixture["prior"].controller.declared_endpoint.verification.edge_record_sha256
    )

    alternate_plan = replace(
        fixture["plan"],
        prior_root_backed_continuation_overlay_source=other_overlay,
    )
    result = reenter_chromium_research_second_basis_epoch(alternate_plan)

    assert result.prior_continuation_reentry.controller.presentation == (
        other_prior.controller.presentation
    )
    assert result.controller.declared_endpoint.verification.edge_record_sha256 == (
        fixture["edge"].edge_record_sha256
    )


def test_plan_creation_rejects_empty_members_and_declared_edges_without_reads(
    tmp_path: Path,
) -> None:
    fake = tmp_path / "unread.overlay.json"

    with pytest.raises(ValueError, match="at least one explicit member"):
        create_chromium_research_second_basis_epoch_reentry_plan(
            fake,
            (),
            changed_working_set_source=tmp_path / "working.json",
            changed_note_source=tmp_path / "note.json",
            transition_source=tmp_path / "transition.json",
            root_source=tmp_path / "root.json",
            declared_edge_sources=(tmp_path / "edge.json",),
            declaration_source=tmp_path / "declaration.json",
        )

    assert not fake.exists()


def test_wrong_plan_type_rejects_before_any_file_read() -> None:
    with pytest.raises(TypeError, match="ChromiumResearchSecondBasisEpochReentryPlan"):
        reenter_chromium_research_second_basis_epoch(object())  # type: ignore[arg-type]
