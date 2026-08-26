from __future__ import annotations

from dataclasses import fields, replace
from pathlib import Path

import pytest

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
from pyxis.app.chromium_research_third_basis_epoch_reentry import (
    ChromiumResearchThirdBasisEpochReentryError,
    ChromiumResearchThirdBasisEpochReentryPlan,
    ChromiumResearchThirdBasisEpochReentryResult,
    create_chromium_research_third_basis_epoch_reentry_plan,
    reenter_chromium_research_third_basis_epoch,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_sequence_load import (
    load_chromium_research_working_set_note_revision_edge_sequence,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_sequence_persistence import (
    persist_chromium_research_working_set_note_revision_edge_sequence,
)
from test_app_chromium_research_second_basis_epoch_continuation_reentry_plan_document import (
    _persist_valid_continuation,
)
from test_app_chromium_research_second_basis_epoch_reentry import (
    _new_paragraph_member_with_locator,
)


def _prior_second_epoch_continuation(tmp_path: Path, *, stem: str):
    tmp_path.mkdir(parents=True, exist_ok=True)
    values = _persist_valid_continuation(tmp_path, stem=stem)
    overlay = values[6]
    checkpoint = values[8]
    return overlay, checkpoint.fresh_reentry


def _third_epoch_fixture(tmp_path: Path, *, stem: str = "40a"):
    prior_dir = tmp_path / "prior"
    third_dir = tmp_path / "third"
    third_dir.mkdir(parents=True, exist_ok=True)

    prior_overlay, prior = _prior_second_epoch_continuation(
        prior_dir,
        stem=f"{stem}-prior",
    )
    member, locator = _new_paragraph_member_with_locator(
        third_dir,
        stem=f"{stem}-member",
    )

    prepared = persist_chromium_research_session_working_set_extension(
        prior.controller,
        (member,),
        rationale_text="Third evidence-basis rationale before its first revision.",
        working_set_destination=third_dir / f"{stem}-working-set.json",
        note_destination=third_dir / f"{stem}-working-set-note.json",
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
        destination=third_dir / f"{stem}-transition.json",
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
        revised_note_text="First rationale revision in the third evidence-basis epoch.",
    )
    root_persistence = persist_chromium_research_session_working_set_transition_revision_root(
        root,
        prior_edge_source=prior.controller.declared_endpoint.verification.path,
        working_set_source=prepared.working_set_persistence.path,
        note_source=prepared.note_persistence.path,
        transition_source=transition_persistence.path,
        destination=third_dir / f"{stem}-root.json",
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
        revised_note_text="Third-epoch first ordinary edge after the third root.",
    )
    first_edge_persistence = (
        persist_chromium_research_session_working_set_transition_revision_root_edge_extension(
            first_edge,
            root_source=root_persistence.path,
            destination=third_dir / f"{stem}-root-edge.json",
        )
    )
    sequence = load_chromium_research_working_set_note_revision_edge_sequence(
        loaded_root,
        (first_edge_persistence.path,),
    )
    declaration_path = third_dir / f"{stem}-declaration.json"
    persist_chromium_research_working_set_note_revision_edge_sequence(
        sequence,
        declaration_path,
    )

    plan = create_chromium_research_third_basis_epoch_reentry_plan(
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


def _root_shas(prior):
    second_epoch = prior.prior_second_basis_epoch_reentry
    first_root = (
        second_epoch.prior_continuation_reentry.prior_root_backed_reentry.loaded_root
        .verification.root_record_sha256
    )
    second_root = second_epoch.loaded_root.verification.root_record_sha256
    return first_root, second_root


def test_third_epoch_fresh_reentry_above_persisted_second_epoch_continuation(
    tmp_path: Path,
) -> None:
    fixture = _third_epoch_fixture(tmp_path)

    result = reenter_chromium_research_third_basis_epoch(fixture["plan"])

    assert isinstance(result, ChromiumResearchThirdBasisEpochReentryResult)
    assert result.plan is fixture["plan"]
    assert result.prior_second_basis_epoch_continuation_reentry is not fixture["prior"]
    assert result.prior_second_basis_epoch_continuation_reentry.controller.presentation == (
        fixture["prior"].controller.presentation
    )
    assert result.loaded_root.verification.root_record_sha256 == (
        fixture["root"].root_record_sha256
    )
    assert result.controller.declared_endpoint.verification.edge_record_sha256 == (
        fixture["edge"].edge_record_sha256
    )
    assert result.successor_items[:-1] == (
        result.prior_second_basis_epoch_continuation_reentry.controller.declared_endpoint
        .revision.revised_note.working_set.items
    )


def test_third_epoch_retains_three_distinct_root_layers(tmp_path: Path) -> None:
    fixture = _third_epoch_fixture(tmp_path, stem="layers")

    result = reenter_chromium_research_third_basis_epoch(fixture["plan"])
    prior = result.prior_second_basis_epoch_continuation_reentry
    first_root_sha, second_root_sha = _root_shas(prior)
    third_root_sha = result.loaded_root.verification.root_record_sha256

    assert len({first_root_sha, second_root_sha, third_root_sha}) == 3
    assert result.loaded_root.transition.prior_endpoint.verification.edge_record_sha256 == (
        prior.controller.declared_endpoint.verification.edge_record_sha256
    )
    assert (
        prior.prior_second_basis_epoch_reentry.loaded_root.verification.root_record_sha256
        == second_root_sha
    )


def test_third_epoch_plan_is_one_explicit_composition_step_not_recursive_schema(
    tmp_path: Path,
) -> None:
    fixture = _third_epoch_fixture(tmp_path, stem="shape")
    plan = fixture["plan"]

    assert isinstance(plan, ChromiumResearchThirdBasisEpochReentryPlan)
    assert tuple(field.name for field in fields(plan)) == (
        "prior_second_basis_epoch_continuation_overlay_source",
        "appended_working_set_members",
        "changed_working_set_source",
        "changed_note_source",
        "transition_source",
        "root_source",
        "declared_edge_sources",
        "declaration_source",
    )
    for forbidden in (
        "prior_second_basis_epoch_plan",
        "epochs",
        "epoch_chain",
        "latest",
        "current_head",
        "canonical_head",
        "chronology",
        "semantic_support",
    ):
        assert not hasattr(plan, forbidden)


def test_missing_prior_second_epoch_continuation_overlay_rejects_without_discovery(
    tmp_path: Path,
) -> None:
    fixture = _third_epoch_fixture(tmp_path, stem="missing-prior")
    plan = replace(
        fixture["plan"],
        prior_second_basis_epoch_continuation_overlay_source=(
            tmp_path / "does-not-exist.overlay.json"
        ),
    )

    with pytest.raises(
        ChromiumResearchThirdBasisEpochReentryError,
        match="prior 37C/37D second-basis-epoch continuation overlay could not be decoded",
    ):
        reenter_chromium_research_third_basis_epoch(plan)


def test_tampered_prior_second_epoch_continuation_rejects_before_third_root(
    tmp_path: Path,
) -> None:
    fixture = _third_epoch_fixture(tmp_path, stem="tampered-prior")
    prior_declaration = fixture["prior"].plan.declaration_source
    prior_declaration.write_bytes(prior_declaration.read_bytes() + b"tampered")

    with pytest.raises(
        ChromiumResearchThirdBasisEpochReentryError,
        match="Prior second-basis-epoch continuation could not be freshly re-entered",
    ):
        reenter_chromium_research_third_basis_epoch(fixture["plan"])


def test_tampered_third_root_rejects_fresh_reentry(tmp_path: Path) -> None:
    fixture = _third_epoch_fixture(tmp_path, stem="tampered-root")
    fixture["root"].path.write_bytes(fixture["root"].path.read_bytes() + b"tampered")

    with pytest.raises(
        ChromiumResearchThirdBasisEpochReentryError,
        match="third changed working set, 33B transition, and 34A root",
    ):
        reenter_chromium_research_third_basis_epoch(fixture["plan"])


def test_wrong_third_declared_edge_is_not_discovered_or_replaced(tmp_path: Path) -> None:
    fixture = _third_epoch_fixture(tmp_path, stem="wrong-edge")
    wrong = tmp_path / "wrong-edge.json"
    wrong.write_text("{}\n", encoding="utf-8")
    decoy = tmp_path / "obvious-correct-edge.json"
    decoy.write_bytes(fixture["edge"].path.read_bytes())
    plan = replace(fixture["plan"], declared_edge_sources=(wrong,))

    with pytest.raises(
        ChromiumResearchThirdBasisEpochReentryError,
        match="third root-backed declared segment",
    ):
        reenter_chromium_research_third_basis_epoch(plan)

    assert decoy.exists()


def test_moved_third_epoch_locations_work_only_when_explicitly_resupplied(
    tmp_path: Path,
) -> None:
    fixture = _third_epoch_fixture(tmp_path, stem="moved")
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

    moved_plan = create_chromium_research_third_basis_epoch_reentry_plan(
        moved_overlay,
        plan.appended_working_set_members,
        changed_working_set_source=moved_working_set,
        changed_note_source=moved_note,
        transition_source=moved_transition,
        root_source=moved_root,
        declared_edge_sources=(moved_edge,),
        declaration_source=moved_declaration,
    )
    result = reenter_chromium_research_third_basis_epoch(moved_plan)

    assert result.loaded_root.verification.path == moved_root.resolve()
    assert result.controller.declared_endpoint.verification.path == moved_edge.resolve()


def test_path_distinct_equivalent_prior_second_epoch_continuation_is_valid_authority(
    tmp_path: Path,
) -> None:
    fixture = _third_epoch_fixture(tmp_path / "earned", stem="same")
    other_overlay, other_prior = _prior_second_epoch_continuation(
        tmp_path / "other-prior",
        stem="same-prior",
    )
    earned_prior = fixture["prior"]

    assert other_prior.controller is not earned_prior.controller
    assert other_prior.controller.presentation == earned_prior.controller.presentation
    assert _root_shas(other_prior) == _root_shas(earned_prior)
    assert (
        other_prior.controller.declared_endpoint.verification.edge_record_sha256
        == earned_prior.controller.declared_endpoint.verification.edge_record_sha256
    )

    alternate_plan = replace(
        fixture["plan"],
        prior_second_basis_epoch_continuation_overlay_source=other_overlay,
    )
    result = reenter_chromium_research_third_basis_epoch(alternate_plan)

    assert result.prior_second_basis_epoch_continuation_reentry.controller.presentation == (
        earned_prior.controller.presentation
    )
    assert result.loaded_root.verification.root_record_sha256 == (
        fixture["root"].root_record_sha256
    )


def test_third_epoch_reentry_rejects_wrong_plan_type() -> None:
    with pytest.raises(TypeError, match="ChromiumResearchThirdBasisEpochReentryPlan"):
        reenter_chromium_research_third_basis_epoch(object())  # type: ignore[arg-type]
