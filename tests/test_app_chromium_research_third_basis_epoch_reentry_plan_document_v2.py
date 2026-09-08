from __future__ import annotations

import json
from pathlib import Path

import pytest

from pyxis.app.chromium_research_paragraph_text_selection_load import (
    ChromiumPageResearchLoadedParagraphTextSelectionRecord,
)
from pyxis.app.chromium_research_third_basis_epoch_reentry_plan_document import (
    ChromiumResearchThirdBasisEpochReentryPlanCheckpointError,
    ChromiumResearchThirdBasisEpochReentryPlanDocumentError,
    load_chromium_research_third_basis_epoch_reentry_plan_document,
)
from pyxis.app.chromium_research_third_changed_basis_epoch_reentry import (
    verify_chromium_research_third_changed_basis_epoch_reentry,
)
from pyxis.app.chromium_research_third_changed_basis_epoch_reentry_overlay import (
    persist_chromium_research_third_changed_basis_epoch_reentry_overlay,
)
from pyxis.app.chromium_research_third_changed_basis_revision_root import (
    persist_chromium_research_third_changed_basis_revision_root,
)
from pyxis.app.chromium_research_third_changed_basis_root_edge import (
    persist_chromium_research_third_changed_basis_root_edge,
)
from pyxis.app.chromium_research_third_changed_basis_session_adoption import (
    adopt_chromium_research_third_changed_basis_governed_session,
)
from pyxis.app.chromium_research_third_changed_basis_transition import (
    persist_chromium_research_third_changed_basis_transition,
)
from pyxis.ui.chromium_research_third_changed_basis_epoch_reentry_overlay_textual import (
    third_changed_basis_epoch_reentry_overlay_success_receipt,
)
from test_app_chromium_research_bare_selection_fresh_reentry import _bare_selection
from test_app_chromium_research_third_basis_epoch_reentry_plan_document import (
    _persist_valid_overlay,
)
from test_second_basis_bare_continuation_v1 import (
    _assert_bare_passages_survive_continuation,
)
from test_second_basis_bare_cumulative_v1 import (
    _persist_bare_second_basis_cumulative,
)
from test_ui_research_third_changed_basis_epoch_reentry_overlay import (
    _direct_47e_verification,
)
from test_ui_research_third_changed_basis_transition import _prepare_direct


_OVERLAY_V1 = "pyxis.chromium.research_third_basis_epoch_reentry_locator_overlay.v1"
_OVERLAY_V2 = "pyxis.chromium.research_third_basis_epoch_reentry_locator_overlay.v2"


def _bare_third_basis_verification(tmp_path: Path, *, stem: str = "50r"):
    prior_values = _persist_bare_second_basis_cumulative(
        tmp_path,
        stem=f"{stem}-prior",
    )
    prior_overlay = prior_values[31]
    prior = prior_values[34].fresh_reentry
    _assert_bare_passages_survive_continuation(prior)

    member_dir = tmp_path / f"{stem}-bare-member"
    member_dir.mkdir()
    _, bare, locator = _bare_selection(member_dir)
    assert bare.selection.selected_text == "Bare"

    prepared = _prepare_direct(tmp_path, prior, bare, stem=stem)
    transition = persist_chromium_research_third_changed_basis_transition(
        prior.controller,
        prior,
        prepared,
        prior_edge_source=prior.controller.declared_endpoint.verification.path,
        working_set_source=prepared.working_set_persistence.path,
        note_source=prepared.note_persistence.path,
        destination=tmp_path / f"{stem}-transition.json",
    )
    root = persist_chromium_research_third_changed_basis_revision_root(
        transition,
        revised_note_text=f"{stem} explicit third-root rationale.",
        prior_edge_source=prior.controller.declared_endpoint.verification.path,
        working_set_source=prepared.working_set_persistence.path,
        note_source=prepared.note_persistence.path,
        transition_source=transition.persistence.path,
        destination=tmp_path / f"{stem}-root.json",
    )
    edge = persist_chromium_research_third_changed_basis_root_edge(
        root,
        revised_note_text=f"{stem} first post-third-root rationale.",
        root_source=root.persistence.path,
        destination=tmp_path / f"{stem}-edge.json",
    )
    adoption = adopt_chromium_research_third_changed_basis_governed_session(
        edge,
        edge_source=edge.persistence.path,
        declaration_destination=tmp_path / f"{stem}-declaration.json",
    )
    verification = verify_chromium_research_third_changed_basis_epoch_reentry(
        adoption,
        prior_overlay,
        (locator,),
        changed_working_set_source=prepared.working_set_persistence.path,
        changed_note_source=prepared.note_persistence.path,
        transition_source=transition.persistence.path,
        root_source=root.persistence.path,
        first_edge_source=edge.persistence.path,
        declaration_source=adoption.declaration.path,
    )
    return (
        prior_overlay,
        prior,
        bare,
        locator,
        prepared,
        transition,
        root,
        edge,
        adoption,
        verification,
    )


def _persist_bare_third_basis_overlay(tmp_path: Path, *, stem: str = "50r"):
    values = _bare_third_basis_verification(tmp_path, stem=stem)
    prior_overlay = values[0]
    verification = values[-1]
    destination = tmp_path / f"{stem}-third-basis.overlay.json"
    result = persist_chromium_research_third_changed_basis_epoch_reentry_overlay(
        verification,
        prior_second_basis_epoch_continuation_overlay_source=prior_overlay,
        destination=destination,
    )
    return (*values, destination, result)


def test_50r_public_40b_persists_bare_selection_as_strict_overlay_v2(
    tmp_path: Path,
) -> None:
    (
        prior_overlay,
        prior,
        _,
        locator,
        prepared,
        transition,
        root,
        edge,
        adoption,
        verification,
        destination,
        result,
    ) = _persist_bare_third_basis_overlay(tmp_path)

    assert result.verification_result is verification
    assert result.checkpoint.reentry is verification.fresh_reentry
    assert result.checkpoint.persistence.path == destination.resolve()
    assert result.checkpoint.persistence.overlay_format == _OVERLAY_V2

    document = json.loads(destination.read_text(encoding="utf-8"))
    assert document["format"] == _OVERLAY_V2
    assert set(document) == {
        "format",
        "prior_second_basis_epoch_continuation_overlay_source",
        "appended_working_set_members",
        "changed_working_set_source",
        "changed_note_source",
        "transition_source",
        "root_source",
        "declared_edge_sources",
        "declaration_source",
    }
    member = document["appended_working_set_members"][0]
    assert set(member) == {"kind", "capture_source", "selection_source"}
    assert member["kind"] == "exact_range_selection"
    assert "note_source" not in member
    base = destination.parent
    assert (base / member["capture_source"]).resolve() == locator.capture_source.resolve()
    assert (base / member["selection_source"]).resolve() == locator.selection_source.resolve()
    assert (
        base / document["prior_second_basis_epoch_continuation_overlay_source"]
    ).resolve() == prior_overlay.resolve()

    decoded = load_chromium_research_third_basis_epoch_reentry_plan_document(destination)
    assert decoded == result.checkpoint.plan

    fresh = result.checkpoint.fresh_reentry
    assert fresh.controller.presentation == verification.fresh_reentry.controller.presentation
    assert (
        fresh.loaded_root.verification.root_record_sha256
        == root.persistence.root_record_sha256
    )
    assert (
        fresh.loaded_declaration.verification.sequence_record_sha256
        == adoption.declaration.sequence_record_sha256
    )
    assert (
        fresh.controller.declared_endpoint.verification.edge_record_sha256
        == edge.persistence.edge_record_sha256
    )
    assert (
        fresh.prior_second_basis_epoch_continuation_reentry.controller.presentation
        == prior.controller.presentation
    )
    assert (
        fresh.prior_second_basis_epoch_continuation_reentry.controller
        .declared_endpoint.verification.edge_record_sha256
        == prior.controller.declared_endpoint.verification.edge_record_sha256
    )
    assert result.checkpoint.plan.changed_working_set_source == (
        prepared.working_set_persistence.path
    )
    assert result.checkpoint.plan.transition_source == transition.persistence.path

    third_bare = fresh.loaded_appended_members[0]
    assert isinstance(
        third_bare,
        ChromiumPageResearchLoadedParagraphTextSelectionRecord,
    )
    assert third_bare.selection.selected_text == "Bare"
    assert not hasattr(third_bare, "note")
    assert (
        fresh.loaded_root.transition.successor_note.note.working_set.items[-1]
        is third_bare
    )
    assert (
        fresh.controller.declared_endpoint.revision.revised_note.working_set.items[-1]
        is third_bare
    )
    _assert_bare_passages_survive_continuation(
        fresh.prior_second_basis_epoch_continuation_reentry
    )


def test_50r_note_only_third_basis_persistence_remains_overlay_v1(
    tmp_path: Path,
) -> None:
    lineage, verification = _direct_47e_verification(tmp_path, stem="50r-v1")
    destination = tmp_path / "50r-note-only.overlay.json"

    result = persist_chromium_research_third_changed_basis_epoch_reentry_overlay(
        verification,
        prior_second_basis_epoch_continuation_overlay_source=lineage.overlay_source,
        destination=destination,
    )

    document = json.loads(destination.read_text(encoding="utf-8"))
    assert document["format"] == _OVERLAY_V1
    assert result.checkpoint.persistence.overlay_format == _OVERLAY_V1
    assert load_chromium_research_third_basis_epoch_reentry_plan_document(
        destination
    ) == result.checkpoint.plan


def test_50r_v2_loader_delegates_historical_note_member_shapes_unchanged(
    tmp_path: Path,
) -> None:
    _, _, overlay, checkpoint = _persist_valid_overlay(tmp_path, stem="50r-delegate")
    document = json.loads(overlay.read_text(encoding="utf-8"))
    assert document["format"] == _OVERLAY_V1
    document["format"] = _OVERLAY_V2
    v2 = tmp_path / "50r-delegate-v2.overlay.json"
    v2.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    assert load_chromium_research_third_basis_epoch_reentry_plan_document(v2) == (
        checkpoint.plan
    )


def test_50r_v1_remains_closed_to_bare_member_shape(tmp_path: Path) -> None:
    *_, destination, _ = _persist_bare_third_basis_overlay(
        tmp_path,
        stem="50r-v1-closed",
    )
    document = json.loads(destination.read_text(encoding="utf-8"))
    document["format"] = _OVERLAY_V1
    invalid = tmp_path / "50r-bare-as-v1.overlay.json"
    invalid.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ChromiumResearchThirdBasisEpochReentryPlanDocumentError,
        match="cannot form a valid explicit 40A locator plan",
    ):
        load_chromium_research_third_basis_epoch_reentry_plan_document(invalid)


@pytest.mark.parametrize("mutation", ["missing_selection", "extra_note", "wrong_kind"])
def test_50r_overlay_v2_rejects_cross_shaped_bare_members(
    tmp_path: Path,
    mutation: str,
) -> None:
    *_, destination, _ = _persist_bare_third_basis_overlay(
        tmp_path,
        stem=f"50r-{mutation}",
    )
    document = json.loads(destination.read_text(encoding="utf-8"))
    member = document["appended_working_set_members"][0]

    if mutation == "missing_selection":
        member.pop("selection_source")
    elif mutation == "extra_note":
        member["note_source"] = "fake-note.json"
    else:
        member["kind"] = "exact_range_note"

    invalid = tmp_path / f"50r-{mutation}-invalid.overlay.json"
    invalid.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ChromiumResearchThirdBasisEpochReentryPlanDocumentError,
        match="cannot form a valid explicit 40A locator plan",
    ):
        load_chromium_research_third_basis_epoch_reentry_plan_document(invalid)


def test_50r_third_basis_overlay_loader_rejects_unknown_version(tmp_path: Path) -> None:
    *_, destination, _ = _persist_bare_third_basis_overlay(
        tmp_path,
        stem="50r-unknown",
    )
    document = json.loads(destination.read_text(encoding="utf-8"))
    document["format"] = (
        "pyxis.chromium.research_third_basis_epoch_reentry_locator_overlay.v3"
    )
    invalid = tmp_path / "50r-unknown-version.overlay.json"
    invalid.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    with pytest.raises(
        ChromiumResearchThirdBasisEpochReentryPlanDocumentError,
        match="unsupported format",
    ):
        load_chromium_research_third_basis_epoch_reentry_plan_document(invalid)


def test_50r_bare_third_basis_checkpoint_reverifies_before_write(
    tmp_path: Path,
) -> None:
    *_, root, _, _, verification = _bare_third_basis_verification(
        tmp_path,
        stem="50r-tamper",
    )
    destination = tmp_path / "50r-tamper.overlay.json"
    root.persistence.path.write_bytes(root.persistence.path.read_bytes() + b"tampered")

    with pytest.raises(
        ChromiumResearchThirdBasisEpochReentryPlanCheckpointError,
        match="could not freshly reconstruct",
    ):
        persist_chromium_research_third_changed_basis_epoch_reentry_overlay(
            verification,
            prior_second_basis_epoch_continuation_overlay_source=(
                verification.fresh_reentry.plan
                .prior_second_basis_epoch_continuation_overlay_source
            ),
            destination=destination,
        )

    assert not destination.exists()


def test_50r_bare_third_basis_overlay_remains_no_overwrite(tmp_path: Path) -> None:
    *_, verification = _bare_third_basis_verification(
        tmp_path,
        stem="50r-no-overwrite",
    )
    destination = tmp_path / "50r-existing.overlay.json"
    destination.write_text("preserve exactly\n", encoding="utf-8")

    with pytest.raises(
        ChromiumResearchThirdBasisEpochReentryPlanDocumentError,
        match="already exists",
    ):
        persist_chromium_research_third_changed_basis_epoch_reentry_overlay(
            verification,
            prior_second_basis_epoch_continuation_overlay_source=(
                verification.fresh_reentry.plan
                .prior_second_basis_epoch_continuation_overlay_source
            ),
            destination=destination,
        )

    assert destination.read_text(encoding="utf-8") == "preserve exactly\n"


def test_50r_bare_third_basis_overlay_stores_locator_configuration_only(
    tmp_path: Path,
) -> None:
    *_, destination, _ = _persist_bare_third_basis_overlay(
        tmp_path,
        stem="50r-semantics",
    )
    document = json.loads(destination.read_text(encoding="utf-8"))
    serialized = json.dumps(document, sort_keys=True)

    for forbidden in (
        "selected_text",
        "note_text",
        "evidence_digest",
        "timestamp",
        "current_head",
        "latest",
        "semantic_support",
        "authorship",
        "citation",
    ):
        assert forbidden not in serialized


def test_50r_success_receipt_reports_actual_v2_format(tmp_path: Path) -> None:
    *_, result = _persist_bare_third_basis_overlay(
        tmp_path,
        stem="50r-receipt",
    )
    receipt = third_changed_basis_epoch_reentry_overlay_success_receipt(result)

    assert f"Overlay format: {_OVERLAY_V2}" in receipt
    assert (
        "Overlay format: "
        "pyxis.chromium.research_third_basis_epoch_reentry_locator_overlay.v1"
        not in receipt
    )
