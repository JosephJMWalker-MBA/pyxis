from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from pyxis.app.chromium_research_session_working_set_extension import (
    persist_chromium_research_session_working_set_extension,
)
from pyxis.app.chromium_research_third_changed_basis_transition import (
    ChromiumResearchThirdChangedBasisTransitionError,
    persist_chromium_research_third_changed_basis_transition,
)
from test_app_chromium_research_second_basis_epoch_continuation_reentry_plan_document import (
    _persist_valid_continuation,
)
from test_app_chromium_research_session_working_set_extension import (
    _new_paragraph_member,
)


def _continuation(tmp_path: Path, *, stem: str):
    values = _persist_valid_continuation(tmp_path, stem=stem)
    return values[8].fresh_reentry


def _prepare(tmp_path: Path, reentry, *, stem: str):
    member, _ = _new_paragraph_member(tmp_path, stem=f"{stem}-member")
    return persist_chromium_research_session_working_set_extension(
        reentry.controller,
        (member,),
        rationale_text="Exact third-basis preparation ownership test.",
        working_set_destination=tmp_path / f"{stem}-working-set.json",
        note_destination=tmp_path / f"{stem}-working-set-note.json",
    )


def test_47a_rejects_preparation_from_different_second_epoch_session_before_write(
    tmp_path: Path,
) -> None:
    first_dir = tmp_path / "first"
    second_dir = tmp_path / "second"
    first_dir.mkdir()
    second_dir.mkdir()
    first = _continuation(first_dir, stem="first")
    second = _continuation(second_dir, stem="second")
    prepared = _prepare(first_dir, first, stem="foreign-prepared")
    destination = tmp_path / "must-not-write-foreign-prepared.json"

    with pytest.raises(
        ChromiumResearchThirdChangedBasisTransitionError,
        match="does not belong to the exact second-epoch continuation session",
    ):
        persist_chromium_research_third_changed_basis_transition(
            second.controller,
            second,
            prepared,
            prior_edge_source=second.controller.declared_endpoint.verification.path,
            working_set_source=prepared.working_set_persistence.path,
            note_source=prepared.note_persistence.path,
            destination=destination,
        )

    assert not destination.exists()


def test_47a_rejects_preparation_that_does_not_retain_exact_controller_endpoint(
    tmp_path: Path,
) -> None:
    first_dir = tmp_path / "first"
    other_dir = tmp_path / "other"
    first_dir.mkdir()
    other_dir.mkdir()
    reentry = _continuation(first_dir, stem="first")
    other = _continuation(other_dir, stem="other")
    prepared = _prepare(first_dir, reentry, stem="wrong-endpoint")
    forged = replace(prepared, prior_endpoint=other.controller.declared_endpoint)
    destination = tmp_path / "must-not-write-wrong-endpoint.json"

    assert forged.prior_session == reentry.controller.presentation
    assert forged.prior_endpoint is not reentry.controller.declared_endpoint

    with pytest.raises(
        ChromiumResearchThirdChangedBasisTransitionError,
        match="does not retain the supplied controller's exact declared endpoint",
    ):
        persist_chromium_research_third_changed_basis_transition(
            reentry.controller,
            reentry,
            forged,
            prior_edge_source=reentry.controller.declared_endpoint.verification.path,
            working_set_source=prepared.working_set_persistence.path,
            note_source=prepared.note_persistence.path,
            destination=destination,
        )

    assert not destination.exists()
