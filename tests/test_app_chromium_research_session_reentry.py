from __future__ import annotations

from dataclasses import dataclass, fields, replace
import importlib
from pathlib import Path

import pytest

from pyxis.app.chromium_research_capture import persist_chromium_page_research_capture
from pyxis.app.chromium_research_capture_load import load_chromium_page_research_capture
from pyxis.app.chromium_research_paragraph_text_selection import (
    select_chromium_research_paragraph_text,
)
from pyxis.app.chromium_research_paragraph_text_selection_comparison import (
    create_chromium_research_paragraph_text_selection_comparison,
)
from pyxis.app.chromium_research_paragraph_text_selection_comparison_note import (
    create_chromium_research_paragraph_text_selection_comparison_note,
)
from pyxis.app.chromium_research_paragraph_text_selection_comparison_note_load import (
    load_chromium_research_paragraph_text_selection_comparison_note,
)
from pyxis.app.chromium_research_paragraph_text_selection_comparison_note_persistence import (
    persist_chromium_research_paragraph_text_selection_comparison_note,
)
from pyxis.app.chromium_research_paragraph_text_selection_note import (
    create_chromium_research_paragraph_text_selection_note,
)
from pyxis.app.chromium_research_paragraph_text_selection_note_load import (
    load_chromium_research_paragraph_text_selection_note,
)
from pyxis.app.chromium_research_paragraph_text_selection_note_persistence import (
    persist_chromium_research_paragraph_text_selection_note,
)
from pyxis.app.chromium_research_passage_selection import (
    select_chromium_research_capture_paragraph,
)
from pyxis.app.chromium_research_selection_note import create_chromium_research_paragraph_note
from pyxis.app.chromium_research_selection_note_load import load_chromium_research_paragraph_note
from pyxis.app.chromium_research_selection_note_persistence import (
    persist_chromium_research_paragraph_note,
)
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
from pyxis.app.chromium_research_working_set import create_chromium_research_working_set
from pyxis.app.chromium_research_working_set_note import create_chromium_research_working_set_note
from pyxis.app.chromium_research_working_set_note_persistence import (
    persist_chromium_research_working_set_note,
)
from pyxis.app.chromium_research_working_set_note_revision import (
    create_chromium_research_working_set_note_revision,
)
from pyxis.app.chromium_research_working_set_note_revision_continuation import (
    create_chromium_research_working_set_note_revision_continuation,
)
from pyxis.app.chromium_research_working_set_note_revision_continuation_extension import (
    create_chromium_research_working_set_note_revision_continuation_extension,
)
from pyxis.app.chromium_research_working_set_note_revision_continuation_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord,
    load_chromium_research_working_set_note_revision_continuation,
)
from pyxis.app.chromium_research_working_set_note_revision_continuation_persistence import (
    persist_chromium_research_working_set_note_revision_continuation,
)
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
    persist_chromium_research_working_set_note_revision_edge,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_sequence_declaration_load import (
    load_chromium_research_working_set_note_revision_edge_sequence_declaration,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_sequence_load import (
    load_chromium_research_working_set_note_revision_edge_sequence,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_sequence_persistence import (
    persist_chromium_research_working_set_note_revision_edge_sequence,
)
from pyxis.app.chromium_research_working_set_note_revision_load import (
    load_chromium_research_working_set_note_revision,
)
from pyxis.app.chromium_research_working_set_note_revision_persistence import (
    persist_chromium_research_working_set_note_revision,
)
from pyxis.app.chromium_research_working_set_persistence import (
    persist_chromium_research_working_set,
)
from test_app_chromium_research_working_set import _loaded_capture


@dataclass(frozen=True, slots=True)
class _DurableFixture:
    plan: ChromiumResearchSessionReentryPlan
    loaded_declaration: object
    loaded_continuation: ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord
    v4_path: Path
    v5_path: Path
    v6_path: Path
    declaration_path: Path


def _persist_loaded_capture(
    tmp_path: Path,
    *,
    stem: str,
    target_id: str,
    url: str,
    paragraph_text: str,
):
    bundle = _loaded_capture(
        path=tmp_path / f"unused-{stem}.json",
        target_id=target_id,
        url=url,
        digest_character="a" if stem == "a" else "b",
        paragraph_text=paragraph_text,
    ).bundle
    capture_path = tmp_path / f"capture-{stem}.json"
    persist_chromium_page_research_capture(bundle, capture_path)
    return load_chromium_page_research_capture(capture_path)


def _durable_fixture(tmp_path: Path) -> _DurableFixture:
    first_source = _persist_loaded_capture(
        tmp_path,
        stem="a",
        target_id="page-a",
        url="https://example.test/a",
        paragraph_text="Alpha evidence paragraph",
    )
    second_source = _persist_loaded_capture(
        tmp_path,
        stem="b",
        target_id="page-b",
        url="https://example.test/b",
        paragraph_text="Beta evidence paragraph",
    )

    first_paragraph = select_chromium_research_capture_paragraph(
        first_source,
        paragraph_ordinal=1,
    )
    paragraph_note = create_chromium_research_paragraph_note(
        first_paragraph,
        note_text="  Whole paragraph matters.  ",
    )
    paragraph_note_path = tmp_path / "paragraph-note.json"
    persist_chromium_research_paragraph_note(paragraph_note, paragraph_note_path)
    loaded_paragraph_note = load_chromium_research_paragraph_note(
        first_source,
        paragraph_note_path,
    )

    first_range = select_chromium_research_paragraph_text(
        first_paragraph,
        start_offset=0,
        end_offset=5,
    )
    exact_note = create_chromium_research_paragraph_text_selection_note(
        first_range,
        note_text="Exact range note 😀",
    )
    exact_note_path = tmp_path / "exact-note.json"
    persist_chromium_research_paragraph_text_selection_note(exact_note, exact_note_path)
    loaded_exact_note = load_chromium_research_paragraph_text_selection_note(
        first_source,
        exact_note_path,
    )

    second_paragraph = select_chromium_research_capture_paragraph(
        second_source,
        paragraph_ordinal=1,
    )
    second_range = select_chromium_research_paragraph_text(
        second_paragraph,
        start_offset=0,
        end_offset=4,
    )
    comparison = create_chromium_research_paragraph_text_selection_comparison(
        first_range,
        second_range,
    )
    comparison_note = create_chromium_research_paragraph_text_selection_comparison_note(
        comparison,
        note_text="  Human comparison; no machine relation claim.\nKeep exact.  ",
    )
    comparison_note_path = tmp_path / "comparison-note.json"
    persist_chromium_research_paragraph_text_selection_comparison_note(
        comparison_note,
        comparison_note_path,
    )
    loaded_comparison_note = load_chromium_research_paragraph_text_selection_comparison_note(
        first_source,
        second_source,
        comparison_note_path,
    )

    members = (loaded_paragraph_note, loaded_exact_note, loaded_comparison_note)
    working_set = create_chromium_research_working_set(members)
    working_set_path = tmp_path / "working-set.json"
    persist_chromium_research_working_set(working_set, working_set_path)

    prior_note = create_chromium_research_working_set_note(
        working_set,
        note_text="v1 rationale.",
    )
    prior_note_path = tmp_path / "prior-note.json"
    persist_chromium_research_working_set_note(
        prior_note,
        working_set_path,
        prior_note_path,
    )

    revision = create_chromium_research_working_set_note_revision(
        prior_note,
        revised_note_text="v2 rationale.",
    )
    revision_path = tmp_path / "revision.json"
    persist_chromium_research_working_set_note_revision(
        revision,
        working_set_path,
        prior_note_path,
        revision_path,
    )
    loaded_revision = load_chromium_research_working_set_note_revision(
        members,
        working_set_path,
        prior_note_path,
        revision_path,
    )

    continuation = create_chromium_research_working_set_note_revision_continuation(
        loaded_revision,
        revised_note_text="v3 rationale.",
    )
    continuation_path = tmp_path / "continuation.json"
    persist_chromium_research_working_set_note_revision_continuation(
        continuation,
        working_set_path,
        prior_note_path,
        revision_path,
        continuation_path,
    )
    loaded_continuation = load_chromium_research_working_set_note_revision_continuation(
        members,
        working_set_path,
        prior_note_path,
        revision_path,
        continuation_path,
    )

    v4_extension = create_chromium_research_working_set_note_revision_continuation_extension(
        loaded_continuation,
        revised_note_text="v4 rationale.",
    )
    v4_path = tmp_path / "v4-edge.json"
    persist_chromium_research_working_set_note_revision_edge(
        v4_extension,
        working_set_path,
        prior_note_path,
        revision_path,
        continuation_path,
        v4_path,
    )
    loaded_v4 = load_chromium_research_working_set_note_revision_edge(
        loaded_continuation,
        v4_path,
    )

    v5_extension = create_chromium_research_working_set_note_revision_edge_extension(
        loaded_v4,
        revised_note_text="  v5 exact human wording 😀  ",
    )
    v5_path = tmp_path / "v5-edge.json"
    persist_chromium_research_working_set_note_revision_edge_extension(
        v5_extension,
        v4_path,
        v5_path,
    )
    loaded_v5 = load_chromium_research_working_set_note_revision_edge(
        loaded_v4,
        v5_path,
    )

    v6_extension = create_chromium_research_working_set_note_revision_edge_extension(
        loaded_v5,
        revised_note_text="v6 exact human wording\nStill tentative.",
    )
    v6_path = tmp_path / "v6-edge.json"
    persist_chromium_research_working_set_note_revision_edge_extension(
        v6_extension,
        v5_path,
        v6_path,
    )

    sequence = load_chromium_research_working_set_note_revision_edge_sequence(
        loaded_v4,
        (v5_path, v6_path),
    )
    declaration_path = tmp_path / "declared-sequence.json"
    persist_chromium_research_working_set_note_revision_edge_sequence(
        sequence,
        declaration_path,
    )
    loaded_declaration = (
        load_chromium_research_working_set_note_revision_edge_sequence_declaration(
            loaded_v4,
            (v5_path, v6_path),
            declaration_path,
        )
    )

    plan = create_chromium_research_session_reentry_plan(
        (
            ChromiumResearchParagraphNoteReentryLocator(
                first_source.verification.path,
                loaded_paragraph_note.verification.path,
            ),
            ChromiumResearchExactRangeNoteReentryLocator(
                first_source.verification.path,
                loaded_exact_note.verification.path,
            ),
            ChromiumResearchComparisonNoteReentryLocator(
                first_source.verification.path,
                second_source.verification.path,
                loaded_comparison_note.verification.path,
            ),
        ),
        working_set_source=working_set_path,
        prior_note_source=prior_note_path,
        prior_revision_source=revision_path,
        continuation_source=continuation_path,
        starting_predecessor_edge_sources=(v4_path,),
        declared_edge_sources=(v5_path, v6_path),
        declaration_source=declaration_path,
    )
    return _DurableFixture(
        plan=plan,
        loaded_declaration=loaded_declaration,
        loaded_continuation=loaded_continuation,
        v4_path=v4_path,
        v5_path=v5_path,
        v6_path=v6_path,
        declaration_path=declaration_path,
    )


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
    fixture = _durable_fixture(tmp_path)
    original = ChromiumResearchSessionController(fixture.loaded_declaration)

    result = reenter_chromium_research_session(fixture.plan)

    assert isinstance(result, ChromiumResearchSessionReentryResult)
    assert result.plan is fixture.plan
    assert result.loaded_declaration is not fixture.loaded_declaration
    assert result.controller is not original
    assert result.controller.loaded is result.loaded_declaration
    assert result.controller.presentation == original.presentation
    assert tuple(member.note.note_text for member in result.loaded_members) == (
        "  Whole paragraph matters.  ",
        "Exact range note 😀",
        "  Human comparison; no machine relation claim.\nKeep exact.  ",
    )
    assert result.controller.presentation.sequence.members[-1].note_text == (
        "v6 exact human wording\nStill tentative."
    )


def test_reentry_freshly_reverifies_files_instead_of_trusting_prior_loaded_state(
    tmp_path: Path,
) -> None:
    fixture = _durable_fixture(tmp_path)
    original = ChromiumResearchSessionController(fixture.loaded_declaration)
    paragraph_locator = fixture.plan.working_set_members[0]
    assert isinstance(paragraph_locator, ChromiumResearchParagraphNoteReentryLocator)
    paragraph_locator.note_source.write_bytes(
        paragraph_locator.note_source.read_bytes() + b"tampered"
    )

    with pytest.raises(ChromiumResearchSessionReentryError, match="member 0"):
        reenter_chromium_research_session(fixture.plan)

    assert original.presentation.sequence.members[-1].note_text == (
        "v6 exact human wording\nStill tentative."
    )


def test_moved_identical_durable_artifacts_reenter_from_new_explicit_locations(
    tmp_path: Path,
) -> None:
    fixture = _durable_fixture(tmp_path)
    original = ChromiumResearchSessionController(fixture.loaded_declaration)
    moved_root = tmp_path / "moved"
    moved_root.mkdir()
    mapping: dict[Path, Path] = {}
    for index, path in enumerate(_all_plan_paths(fixture.plan)):
        moved = moved_root / f"{index:02d}-{path.name}"
        path.replace(moved)
        mapping[path] = moved
    moved_plan = _remap_plan(fixture.plan, mapping)

    result = reenter_chromium_research_session(moved_plan)

    assert result.controller.presentation == original.presentation
    assert result.loaded_declaration.verification.path == (
        mapping[fixture.plan.declaration_source].resolve()
    )
    assert result.controller.declared_endpoint.verification.path == (
        mapping[fixture.plan.declared_edge_sources[-1]].resolve()
    )


def test_wrong_capture_for_one_member_rejects_before_base_session_relink(tmp_path: Path) -> None:
    fixture = _durable_fixture(tmp_path)
    paragraph, exact, comparison = fixture.plan.working_set_members
    assert isinstance(paragraph, ChromiumResearchParagraphNoteReentryLocator)
    assert isinstance(comparison, ChromiumResearchComparisonNoteReentryLocator)
    wrong_paragraph = replace(
        paragraph,
        capture_source=comparison.second_capture_source,
    )
    wrong_plan = replace(
        fixture.plan,
        working_set_members=(wrong_paragraph, exact, comparison),
    )

    with pytest.raises(ChromiumResearchSessionReentryError, match="member 0"):
        reenter_chromium_research_session(wrong_plan)


def test_wrong_working_set_member_order_rejects_against_durable_working_set(
    tmp_path: Path,
) -> None:
    fixture = _durable_fixture(tmp_path)
    wrong_plan = replace(
        fixture.plan,
        working_set_members=tuple(reversed(fixture.plan.working_set_members)),
    )

    with pytest.raises(ChromiumResearchSessionReentryError, match="20B/21B/22B/23B"):
        reenter_chromium_research_session(wrong_plan)


def test_omitted_predecessor_edge_is_not_discovered_even_when_decoy_file_exists(
    tmp_path: Path,
) -> None:
    fixture = _durable_fixture(tmp_path)
    decoy = tmp_path / "obvious-starting-predecessor-edge.json"
    decoy.write_bytes(fixture.v4_path.read_bytes())
    wrong_plan = replace(fixture.plan, starting_predecessor_edge_sources=())

    with pytest.raises(ChromiumResearchSessionReentryError, match="declared segment"):
        reenter_chromium_research_session(wrong_plan)

    assert decoy.exists()


def test_wrong_declared_edge_order_rejects_exact_caller_order(tmp_path: Path) -> None:
    fixture = _durable_fixture(tmp_path)
    wrong_plan = replace(
        fixture.plan,
        declared_edge_sources=tuple(reversed(fixture.plan.declared_edge_sources)),
    )

    with pytest.raises(ChromiumResearchSessionReentryError, match="declared segment"):
        reenter_chromium_research_session(wrong_plan)


def test_declaration_may_start_directly_at_fresh_23c_continuation(tmp_path: Path) -> None:
    fixture = _durable_fixture(tmp_path)
    direct_sequence = load_chromium_research_working_set_note_revision_edge_sequence(
        fixture.loaded_continuation,
        (fixture.v4_path,),
    )
    direct_declaration = tmp_path / "direct-from-continuation-declaration.json"
    persist_chromium_research_working_set_note_revision_edge_sequence(
        direct_sequence,
        direct_declaration,
    )
    direct_plan = replace(
        fixture.plan,
        starting_predecessor_edge_sources=(),
        declared_edge_sources=(fixture.v4_path,),
        declaration_source=direct_declaration,
    )

    result = reenter_chromium_research_session(direct_plan)

    assert isinstance(
        result.starting_predecessor,
        ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord,
    )
    assert result.starting_predecessor is result.loaded_continuation
    assert result.controller.presentation.sequence.members[0].note_text == "v4 rationale."


def test_loaded_session_remains_usable_after_every_reentry_source_disappears(
    tmp_path: Path,
) -> None:
    fixture = _durable_fixture(tmp_path)
    result = reenter_chromium_research_session(fixture.plan)
    expected = result.controller.presentation

    for path in _all_plan_paths(fixture.plan):
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
    fixture = _durable_fixture(tmp_path)
    plan = fixture.plan
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
    fixture = _durable_fixture(tmp_path)
    result = reenter_chromium_research_session(fixture.plan)

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
