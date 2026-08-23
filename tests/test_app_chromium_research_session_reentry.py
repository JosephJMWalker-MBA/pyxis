from __future__ import annotations

from dataclasses import fields, replace
import importlib
from pathlib import Path

import pytest

from pyxis.app.chromium_research_session_controller import ChromiumResearchSessionController
from pyxis.app.chromium_research_session_reentry import (
    ChromiumResearchComparisonNoteReentryLocator,
    ChromiumResearchExactRangeNoteReentryLocator,
    ChromiumResearchParagraphNoteReentryLocator,
    ChromiumResearchSessionReentryError,
    ChromiumResearchSessionReentryPlan,
    ChromiumResearchSessionReentryResult,
    create_chromium_research_session_reentry_plan,
    reenter_chromium_research_session,
)
from pyxis.app.chromium_research_working_set_note_revision_continuation_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_sequence_load import (
    load_chromium_research_working_set_note_revision_edge_sequence,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_sequence_persistence import (
    persist_chromium_research_working_set_note_revision_edge_sequence,
)
from test_app_chromium_research_session_presentation import _loaded
from test_app_chromium_research_working_set_note_revision_edge_persistence import (
    _durable_edge,
)


def _member_locators(paragraph_note, exact_note, comparison_note):
    return (
        ChromiumResearchParagraphNoteReentryLocator(
            capture_source=paragraph_note.note.selection.source.verification.path,
            note_source=paragraph_note.verification.path,
        ),
        ChromiumResearchExactRangeNoteReentryLocator(
            capture_source=exact_note.note.selection.source.source.verification.path,
            note_source=exact_note.verification.path,
        ),
        ChromiumResearchComparisonNoteReentryLocator(
            first_capture_source=(
                comparison_note.note.comparison.first_selection.source.source.verification.path
            ),
            second_capture_source=(
                comparison_note.note.comparison.second_selection.source.source.verification.path
            ),
            note_source=comparison_note.verification.path,
        ),
    )


def _fixture_plan(tmp_path: Path):
    prefix, v4_path, v5_path, v6_path, declaration_path, loaded = _loaded(tmp_path)
    paragraph_note, exact_note, comparison_note = prefix[:3]
    plan = create_chromium_research_session_reentry_plan(
        _member_locators(paragraph_note, exact_note, comparison_note),
        working_set_source=prefix[3],
        prior_note_source=prefix[4],
        prior_revision_source=prefix[5],
        continuation_source=prefix[6],
        starting_predecessor_edge_sources=(v4_path,),
        declared_edge_sources=(v5_path, v6_path),
        declaration_source=declaration_path,
    )
    return plan, loaded, prefix, v4_path, v5_path, v6_path, declaration_path


def _all_plan_paths(plan: ChromiumResearchSessionReentryPlan) -> tuple[Path, ...]:
    paths: list[Path] = []
    for locator in plan.working_set_members:
        if isinstance(locator, ChromiumResearchComparisonNoteReentryLocator):
            paths.extend(
                (
                    locator.first_capture_source,
                    locator.second_capture_source,
                    locator.note_source,
                )
            )
        else:
            paths.extend((locator.capture_source, locator.note_source))
    paths.extend(
        (
            plan.working_set_source,
            plan.prior_note_source,
            plan.prior_revision_source,
            plan.continuation_source,
            *plan.starting_predecessor_edge_sources,
            *plan.declared_edge_sources,
            plan.declaration_source,
        )
    )
    return tuple(dict.fromkeys(paths))


def _remap_plan(
    plan: ChromiumResearchSessionReentryPlan,
    mapping: dict[Path, Path],
) -> ChromiumResearchSessionReentryPlan:
    members = []
    for locator in plan.working_set_members:
        if isinstance(locator, ChromiumResearchParagraphNoteReentryLocator):
            members.append(
                ChromiumResearchParagraphNoteReentryLocator(
                    mapping[locator.capture_source],
                    mapping[locator.note_source],
                )
            )
        elif isinstance(locator, ChromiumResearchExactRangeNoteReentryLocator):
            members.append(
                ChromiumResearchExactRangeNoteReentryLocator(
                    mapping[locator.capture_source],
                    mapping[locator.note_source],
                )
            )
        else:
            assert isinstance(locator, ChromiumResearchComparisonNoteReentryLocator)
            members.append(
                ChromiumResearchComparisonNoteReentryLocator(
                    mapping[locator.first_capture_source],
                    mapping[locator.second_capture_source],
                    mapping[locator.note_source],
                )
            )
    return create_chromium_research_session_reentry_plan(
        members,
        working_set_source=mapping[plan.working_set_source],
        prior_note_source=mapping[plan.prior_note_source],
        prior_revision_source=mapping[plan.prior_revision_source],
        continuation_source=mapping[plan.continuation_source],
        starting_predecessor_edge_sources=tuple(
            mapping[path] for path in plan.starting_predecessor_edge_sources
        ),
        declared_edge_sources=tuple(mapping[path] for path in plan.declared_edge_sources),
        declaration_source=mapping[plan.declaration_source],
    )


def test_fresh_reentry_reconstructs_equivalent_governed_session(tmp_path: Path) -> None:
    plan, loaded, *_ = _fixture_plan(tmp_path)
    original = ChromiumResearchSessionController(loaded)

    result = reenter_chromium_research_session(plan)

    assert isinstance(result, ChromiumResearchSessionReentryResult)
    assert result.plan is plan
    assert result.loaded_declaration is not loaded
    assert result.controller is not original
    assert result.controller.loaded is result.loaded_declaration
    assert result.controller.presentation == original.presentation
    assert tuple(member.note.note_text for member in result.loaded_members) == (
        "  Whole paragraph matters.  ",
        "  Exact alpha matters.  ",
        "  Compare alpha and beta explicitly.  ",
    )
    assert result.controller.presentation.sequence.members[-1].note_text == (
        "v6 exact human wording\nStill tentative."
    )


def test_reentry_freshly_reverifies_files_instead_of_trusting_prior_loaded_state(
    tmp_path: Path,
) -> None:
    plan, loaded, *_ = _fixture_plan(tmp_path)
    original = ChromiumResearchSessionController(loaded)
    paragraph_locator = plan.working_set_members[0]
    assert isinstance(paragraph_locator, ChromiumResearchParagraphNoteReentryLocator)
    paragraph_locator.note_source.write_bytes(
        paragraph_locator.note_source.read_bytes() + b"tampered"
    )

    with pytest.raises(ChromiumResearchSessionReentryError, match="member 0"):
        reenter_chromium_research_session(plan)

    assert original.presentation.sequence.members[-1].note_text == (
        "v6 exact human wording\nStill tentative."
    )


def test_moved_identical_durable_artifacts_reenter_from_new_explicit_locations(
    tmp_path: Path,
) -> None:
    plan, loaded, *_ = _fixture_plan(tmp_path)
    original = ChromiumResearchSessionController(loaded)
    moved_root = tmp_path / "moved"
    moved_root.mkdir()
    mapping: dict[Path, Path] = {}
    for index, path in enumerate(_all_plan_paths(plan)):
        moved = moved_root / f"{index:02d}-{path.name}"
        path.replace(moved)
        mapping[path] = moved
    moved_plan = _remap_plan(plan, mapping)

    result = reenter_chromium_research_session(moved_plan)

    assert result.controller.presentation == original.presentation
    assert result.loaded_declaration.verification.path == mapping[plan.declaration_source].resolve()
    assert result.controller.declared_endpoint.verification.path == (
        mapping[plan.declared_edge_sources[-1]].resolve()
    )


def test_wrong_capture_for_one_member_rejects_before_base_session_relink(tmp_path: Path) -> None:
    plan, *_ = _fixture_plan(tmp_path)
    paragraph, exact, comparison = plan.working_set_members
    assert isinstance(paragraph, ChromiumResearchParagraphNoteReentryLocator)
    assert isinstance(comparison, ChromiumResearchComparisonNoteReentryLocator)
    wrong_paragraph = replace(
        paragraph,
        capture_source=comparison.second_capture_source,
    )
    wrong_plan = replace(
        plan,
        working_set_members=(wrong_paragraph, exact, comparison),
    )

    with pytest.raises(ChromiumResearchSessionReentryError, match="member 0"):
        reenter_chromium_research_session(wrong_plan)


def test_wrong_working_set_member_order_rejects_against_durable_working_set(
    tmp_path: Path,
) -> None:
    plan, *_ = _fixture_plan(tmp_path)
    wrong_plan = replace(
        plan,
        working_set_members=tuple(reversed(plan.working_set_members)),
    )

    with pytest.raises(ChromiumResearchSessionReentryError, match="20B/21B/22B/23B"):
        reenter_chromium_research_session(wrong_plan)


def test_omitted_predecessor_edge_is_not_discovered_even_when_decoy_file_exists(
    tmp_path: Path,
) -> None:
    plan, _, _, v4_path, *_ = _fixture_plan(tmp_path)
    decoy = tmp_path / "obvious-starting-predecessor-edge.json"
    decoy.write_bytes(v4_path.read_bytes())
    wrong_plan = replace(plan, starting_predecessor_edge_sources=())

    with pytest.raises(ChromiumResearchSessionReentryError, match="declared segment"):
        reenter_chromium_research_session(wrong_plan)

    assert decoy.exists()


def test_wrong_declared_edge_order_rejects_exact_caller_order(tmp_path: Path) -> None:
    plan, *_ = _fixture_plan(tmp_path)
    wrong_plan = replace(
        plan,
        declared_edge_sources=tuple(reversed(plan.declared_edge_sources)),
    )

    with pytest.raises(ChromiumResearchSessionReentryError, match="declared segment"):
        reenter_chromium_research_session(wrong_plan)


def test_declaration_may_start_directly_at_fresh_23c_continuation(tmp_path: Path) -> None:
    (
        paragraph_note,
        exact_note,
        comparison_note,
        working_set_path,
        prior_note_path,
        revision_path,
        continuation_path,
        _,
        _,
        loaded_continuation,
        _,
        v4_path,
        _,
    ) = _durable_edge(tmp_path, extension_text="v4 direct declaration member")
    sequence = load_chromium_research_working_set_note_revision_edge_sequence(
        loaded_continuation,
        (v4_path,),
    )
    declaration_path = tmp_path / "direct-from-continuation-declaration.json"
    persist_chromium_research_working_set_note_revision_edge_sequence(
        sequence,
        declaration_path,
    )
    plan = create_chromium_research_session_reentry_plan(
        _member_locators(paragraph_note, exact_note, comparison_note),
        working_set_source=working_set_path,
        prior_note_source=prior_note_path,
        prior_revision_source=revision_path,
        continuation_source=continuation_path,
        starting_predecessor_edge_sources=(),
        declared_edge_sources=(v4_path,),
        declaration_source=declaration_path,
    )

    result = reenter_chromium_research_session(plan)

    assert isinstance(
        result.starting_predecessor,
        ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord,
    )
    assert result.starting_predecessor is result.loaded_continuation
    assert result.controller.presentation.sequence.members[0].note_text == (
        "v4 direct declaration member"
    )


def test_loaded_session_remains_usable_after_every_reentry_source_disappears(
    tmp_path: Path,
) -> None:
    plan, *_ = _fixture_plan(tmp_path)
    result = reenter_chromium_research_session(plan)
    expected = result.controller.presentation

    for path in _all_plan_paths(plan):
        path.unlink(missing_ok=True)

    assert result.controller.presentation is expected
    assert expected.sequence.members[-1].note_text == (
        "v6 exact human wording\nStill tentative."
    )
    assert expected.working_set_contexts[0].members[0].excerpts[0].text == (
        "Alpha evidence paragraph"
    )


def test_plan_constructor_snapshots_generators_and_rejects_implicit_path_iterables(
    tmp_path: Path,
) -> None:
    plan, *_ = _fixture_plan(tmp_path)
    rebuilt = create_chromium_research_session_reentry_plan(
        (member for member in plan.working_set_members),
        working_set_source=plan.working_set_source,
        prior_note_source=plan.prior_note_source,
        prior_revision_source=plan.prior_revision_source,
        continuation_source=plan.continuation_source,
        starting_predecessor_edge_sources=(
            path for path in plan.starting_predecessor_edge_sources
        ),
        declared_edge_sources=(path for path in plan.declared_edge_sources),
        declaration_source=plan.declaration_source,
    )

    assert isinstance(rebuilt.working_set_members, tuple)
    assert isinstance(rebuilt.starting_predecessor_edge_sources, tuple)
    assert isinstance(rebuilt.declared_edge_sources, tuple)

    with pytest.raises(TypeError, match="not one path"):
        create_chromium_research_session_reentry_plan(
            plan.working_set_members,
            working_set_source=plan.working_set_source,
            prior_note_source=plan.prior_note_source,
            prior_revision_source=plan.prior_revision_source,
            continuation_source=plan.continuation_source,
            starting_predecessor_edge_sources=plan.starting_predecessor_edge_sources,
            declared_edge_sources=plan.declared_edge_sources[0],  # type: ignore[arg-type]
            declaration_source=plan.declaration_source,
        )


def test_reentry_surface_adds_locator_convenience_without_head_or_discovery_authority(
    tmp_path: Path,
) -> None:
    plan, *_ = _fixture_plan(tmp_path)
    result = reenter_chromium_research_session(plan)

    assert {field.name for field in fields(ChromiumResearchSessionReentryPlan)} == {
        "working_set_members",
        "working_set_source",
        "prior_note_source",
        "prior_revision_source",
        "continuation_source",
        "starting_predecessor_edge_sources",
        "declared_edge_sources",
        "declaration_source",
    }
    result_fields = {field.name for field in fields(ChromiumResearchSessionReentryResult)}
    assert result_fields == {
        "plan",
        "loaded_members",
        "loaded_continuation",
        "starting_predecessor",
        "loaded_declaration",
        "controller",
    }
    assert result_fields.isdisjoint(
        {
            "latest",
            "current",
            "head",
            "canonical_head",
            "complete_history",
            "discovered_paths",
            "chronology",
            "truth",
        }
    )
    assert result.controller.declared_endpoint is result.loaded_declaration.sequence.edges[-1]

    module = importlib.import_module("pyxis.app.chromium_research_session_reentry")
    assert hasattr(module, "create_chromium_research_session_reentry_plan")
    assert hasattr(module, "reenter_chromium_research_session")
