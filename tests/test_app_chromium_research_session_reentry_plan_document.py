from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from pyxis.app.chromium_research_session_reentry import (
    ChromiumResearchComparisonNoteReentryLocator,
    ChromiumResearchExactRangeNoteReentryLocator,
    ChromiumResearchParagraphNoteReentryLocator,
    reenter_chromium_research_session,
)
from pyxis.app.chromium_research_session_reentry_plan_document import (
    ChromiumResearchSessionReentryPlanDocumentError,
    load_chromium_research_session_reentry_plan_document,
)
from test_app_chromium_research_session_reentry import _durable_fixture


PLAN_FORMAT = "pyxis.chromium.research_session_reentry_locator_plan.v1"


def _path_value(path: Path, base: Path, *, relative: bool) -> str:
    return os.path.relpath(path, base) if relative else str(path)


def _document_for(plan, base: Path, *, relative: bool = True) -> dict[str, object]:
    members: list[dict[str, str]] = []
    for member in plan.working_set_members:
        if isinstance(member, ChromiumResearchParagraphNoteReentryLocator):
            members.append(
                {
                    "kind": "paragraph_note",
                    "capture_source": _path_value(member.capture_source, base, relative=relative),
                    "note_source": _path_value(member.note_source, base, relative=relative),
                }
            )
        elif isinstance(member, ChromiumResearchExactRangeNoteReentryLocator):
            members.append(
                {
                    "kind": "exact_range_note",
                    "capture_source": _path_value(member.capture_source, base, relative=relative),
                    "note_source": _path_value(member.note_source, base, relative=relative),
                }
            )
        else:
            assert isinstance(member, ChromiumResearchComparisonNoteReentryLocator)
            members.append(
                {
                    "kind": "comparison_note",
                    "first_capture_source": _path_value(
                        member.first_capture_source, base, relative=relative
                    ),
                    "second_capture_source": _path_value(
                        member.second_capture_source, base, relative=relative
                    ),
                    "note_source": _path_value(member.note_source, base, relative=relative),
                }
            )

    return {
        "format": PLAN_FORMAT,
        "working_set_members": members,
        "working_set_source": _path_value(plan.working_set_source, base, relative=relative),
        "prior_note_source": _path_value(plan.prior_note_source, base, relative=relative),
        "prior_revision_source": _path_value(
            plan.prior_revision_source, base, relative=relative
        ),
        "continuation_source": _path_value(
            plan.continuation_source, base, relative=relative
        ),
        "starting_predecessor_edge_sources": [
            _path_value(path, base, relative=relative)
            for path in plan.starting_predecessor_edge_sources
        ],
        "declared_edge_sources": [
            _path_value(path, base, relative=relative)
            for path in plan.declared_edge_sources
        ],
        "declaration_source": _path_value(
            plan.declaration_source, base, relative=relative
        ),
    }


def _write_document(path: Path, document: dict[str, object]) -> None:
    path.write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def test_relative_locator_document_reconstructs_exact_31a_plan_and_session(
    tmp_path: Path,
) -> None:
    fixture = _durable_fixture(tmp_path)
    plan_path = tmp_path / "research-session.plan.json"
    _write_document(plan_path, _document_for(fixture.plan, tmp_path))

    loaded_plan = load_chromium_research_session_reentry_plan_document(plan_path)
    result = reenter_chromium_research_session(loaded_plan)

    assert loaded_plan == fixture.plan
    assert result.controller.presentation == (
        reenter_chromium_research_session(fixture.plan).controller.presentation
    )
    assert tuple(type(member) for member in loaded_plan.working_set_members) == (
        ChromiumResearchParagraphNoteReentryLocator,
        ChromiumResearchExactRangeNoteReentryLocator,
        ChromiumResearchComparisonNoteReentryLocator,
    )


def test_absolute_locator_document_is_location_only_and_needs_no_path_rewrite(
    tmp_path: Path,
) -> None:
    fixture = _durable_fixture(tmp_path)
    plan_path = tmp_path / "absolute.plan.json"
    _write_document(
        plan_path,
        _document_for(fixture.plan, tmp_path, relative=False),
    )

    loaded_plan = load_chromium_research_session_reentry_plan_document(plan_path)

    assert loaded_plan == fixture.plan
    assert all(path.is_absolute() for path in loaded_plan.declared_edge_sources)


def test_plan_document_loading_does_not_read_or_discover_referenced_artifacts(
    tmp_path: Path,
) -> None:
    plan_path = tmp_path / "missing-artifacts.plan.json"
    document = {
        "format": PLAN_FORMAT,
        "working_set_members": [
            {
                "kind": "paragraph_note",
                "capture_source": "does-not-exist/capture.json",
                "note_source": "does-not-exist/note.json",
            }
        ],
        "working_set_source": "does-not-exist/working-set.json",
        "prior_note_source": "does-not-exist/prior-note.json",
        "prior_revision_source": "does-not-exist/revision.json",
        "continuation_source": "does-not-exist/continuation.json",
        "starting_predecessor_edge_sources": [],
        "declared_edge_sources": ["does-not-exist/declared-edge.json"],
        "declaration_source": "does-not-exist/declaration.json",
    }
    _write_document(plan_path, document)

    loaded_plan = load_chromium_research_session_reentry_plan_document(plan_path)

    assert loaded_plan.working_set_source == tmp_path / "does-not-exist/working-set.json"
    assert not loaded_plan.working_set_source.exists()


def test_unknown_authority_like_root_or_member_fields_are_rejected(
    tmp_path: Path,
) -> None:
    fixture = _durable_fixture(tmp_path)
    base_document = _document_for(fixture.plan, tmp_path)

    root_document = dict(base_document)
    root_document["latest"] = True
    root_path = tmp_path / "root-authority.plan.json"
    _write_document(root_path, root_document)
    with pytest.raises(ChromiumResearchSessionReentryPlanDocumentError, match="unexpected"):
        load_chromium_research_session_reentry_plan_document(root_path)

    member_document = _document_for(fixture.plan, tmp_path)
    first_member = dict(member_document["working_set_members"][0])  # type: ignore[index]
    first_member["sha256"] = "a" * 64
    member_document["working_set_members"] = [
        first_member,
        *member_document["working_set_members"][1:],  # type: ignore[index]
    ]
    member_path = tmp_path / "member-authority.plan.json"
    _write_document(member_path, member_document)
    with pytest.raises(ChromiumResearchSessionReentryPlanDocumentError, match="unexpected"):
        load_chromium_research_session_reentry_plan_document(member_path)


def test_duplicate_keys_and_unsupported_member_kind_reject_before_31a(
    tmp_path: Path,
) -> None:
    duplicate_path = tmp_path / "duplicate.plan.json"
    duplicate_path.write_text(
        '{"format":"x","format":"y"}\n',
        encoding="utf-8",
    )
    with pytest.raises(ChromiumResearchSessionReentryPlanDocumentError, match="Duplicate"):
        load_chromium_research_session_reentry_plan_document(duplicate_path)

    fixture = _durable_fixture(tmp_path / "unsupported")
    unsupported_path = tmp_path / "unsupported-kind.plan.json"
    document = _document_for(fixture.plan, unsupported_path.parent, relative=False)
    member = dict(document["working_set_members"][0])  # type: ignore[index]
    member["kind"] = "machine_summary"
    document["working_set_members"] = [
        member,
        *document["working_set_members"][1:],  # type: ignore[index]
    ]
    _write_document(unsupported_path, document)

    with pytest.raises(ChromiumResearchSessionReentryPlanDocumentError, match="kind must be"):
        load_chromium_research_session_reentry_plan_document(unsupported_path)
