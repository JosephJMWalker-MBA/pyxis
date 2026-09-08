from __future__ import annotations

import json
from pathlib import Path

import pytest

import pyxis.cli as cli
from pyxis.app.chromium_research_paragraph_text_selection_load import (
    ChromiumPageResearchLoadedParagraphTextSelectionRecord,
)
from pyxis.app.chromium_research_root_backed_session_authority_inspection import (
    inspect_chromium_research_root_backed_session_continuation_launch,
)
from pyxis.app.chromium_research_root_backed_session_authority_inspection_report import (
    serialize_chromium_research_root_backed_session_authority_inspection,
)
from pyxis.app.chromium_research_root_backed_session_continuation_reentry_plan_document import (
    ChromiumResearchRootBackedSessionContinuationReentryError,
    load_chromium_research_root_backed_session_continuation_reentry_plan_document,
    persist_chromium_research_root_backed_session_continuation_checkpoint,
    reenter_chromium_research_root_backed_session_continuation,
)
from pyxis.app.chromium_research_root_backed_session_reentry import (
    reenter_chromium_research_root_backed_session,
)
from pyxis.app.chromium_research_root_backed_session_reentry_plan_document import (
    load_chromium_research_root_backed_session_reentry_plan_document,
)
from pyxis.app.chromium_research_root_backed_session_shell_lineage import (
    ChromiumResearchRootBackedSessionContinuationShellLineage,
    prove_chromium_research_root_backed_session_continuation_shell_lineage,
)
from pyxis.app.chromium_research_session_rollover import (
    rollover_chromium_research_session_to_persisted_successor,
)
from test_app_chromium_research_root_backed_session_reentry_plan_document_v2 import (
    _persist_bare_overlay,
)


_ROOT_OVERLAY_V2 = (
    "pyxis.chromium.research_root_backed_session_reentry_locator_overlay.v2"
)
_CONTINUATION_OVERLAY_V1 = (
    "pyxis.chromium.research_root_backed_session_continuation_locator_overlay.v1"
)


def _persist_bare_root_continuation(tmp_path: Path, *, stem: str = "50j"):
    (
        fixture,
        locator,
        root,
        edge,
        verification,
        prior_plan,
        root_overlay,
        root_checkpoint,
    ) = _persist_bare_overlay(tmp_path, stem=f"{stem}-root")

    root_document = json.loads(root_overlay.read_text(encoding="utf-8"))
    assert root_document["format"] == _ROOT_OVERLAY_V2

    root_plan = load_chromium_research_root_backed_session_reentry_plan_document(
        root_overlay
    )
    prior = reenter_chromium_research_root_backed_session(root_plan)

    successor = tmp_path / f"{stem}-successor-edge.json"
    revision = prior.controller.persist_declared_endpoint_revision(
        "First ordinary continuation after fresh bare-selection overlay-v2 relaunch.",
        prior_edge_source=prior.controller.declared_endpoint.verification.path,
        destination=successor,
    )
    declaration = tmp_path / f"{stem}-continuation-declaration.json"
    rollover = rollover_chromium_research_session_to_persisted_successor(
        prior.controller,
        revision,
        successor_edge_source=successor,
        declaration_destination=declaration,
    )
    continuation_overlay = tmp_path / f"{stem}-continuation-overlay.json"
    checkpoint = persist_chromium_research_root_backed_session_continuation_checkpoint(
        prior,
        rollover,
        prior_root_backed_overlay_source=root_overlay,
        successor_edge_source=successor,
        continuation_declaration_source=declaration,
        destination=continuation_overlay,
    )
    return (
        fixture,
        locator,
        root,
        edge,
        verification,
        prior_plan,
        root_overlay,
        root_checkpoint,
        prior,
        successor,
        revision,
        declaration,
        rollover,
        continuation_overlay,
        checkpoint,
    )


def _assert_bare_member_survives(reentry) -> None:
    loaded_bare = reentry.prior_root_backed_reentry.loaded_appended_members[0]
    assert isinstance(
        loaded_bare,
        ChromiumPageResearchLoadedParagraphTextSelectionRecord,
    )
    assert loaded_bare.selection.selected_text == "Bare"
    assert not hasattr(loaded_bare, "note")
    assert (
        reentry.prior_root_backed_reentry.loaded_root.transition.successor_note.note.working_set.items[-1]
        is loaded_bare
    )
    assert (
        reentry.controller.declared_endpoint.revision.revised_note.working_set.items[-1]
        is loaded_bare
    )


def test_50j_35d_checkpoint_remains_v1_above_bare_root_overlay_v2(
    tmp_path: Path,
) -> None:
    (
        _,
        _,
        root,
        _,
        _,
        _,
        root_overlay,
        _,
        prior,
        successor,
        _,
        declaration,
        rollover,
        continuation_overlay,
        checkpoint,
    ) = _persist_bare_root_continuation(tmp_path)

    assert checkpoint.prior_reentry is prior
    assert checkpoint.rollover is rollover
    assert checkpoint.persistence.path == continuation_overlay.resolve()
    assert checkpoint.plan.prior_root_backed_overlay_source == root_overlay.resolve()

    document = json.loads(continuation_overlay.read_text(encoding="utf-8"))
    assert document["format"] == _CONTINUATION_OVERLAY_V1
    assert set(document) == {
        "format",
        "prior_root_backed_overlay_source",
        "declared_edge_sources",
        "declaration_source",
    }
    base = continuation_overlay.parent
    assert (
        base / document["prior_root_backed_overlay_source"]
    ).resolve() == root_overlay.resolve()
    assert [(base / value).resolve() for value in document["declared_edge_sources"]] == [
        successor.resolve()
    ]
    assert (base / document["declaration_source"]).resolve() == declaration.resolve()

    serialized = json.dumps(document, sort_keys=True)
    for forbidden in (
        "appended_working_set_members",
        "exact_range_selection",
        "capture_source",
        "selection_source",
        "changed_working_set_source",
        "changed_note_source",
        "root_source",
        "prior_session_plan_source",
    ):
        assert forbidden not in serialized

    fresh = checkpoint.fresh_reentry
    assert fresh.prior_root_backed_reentry is not prior
    assert (
        fresh.prior_root_backed_reentry.loaded_root.verification.root_record_sha256
        == root.persistence.root_record_sha256
    )
    assert fresh.controller.presentation == rollover.continuation_controller.presentation
    assert (
        fresh.controller.declared_endpoint.verification.edge_record_sha256
        == rollover.continuation_controller.declared_endpoint.verification.edge_record_sha256
    )
    _assert_bare_member_survives(fresh)

    decoded = load_chromium_research_root_backed_session_continuation_reentry_plan_document(
        continuation_overlay
    )
    roundtrip = reenter_chromium_research_root_backed_session_continuation(decoded)
    assert decoded == checkpoint.plan
    assert roundtrip is not fresh
    assert roundtrip.controller.presentation == fresh.controller.presentation
    _assert_bare_member_survives(roundtrip)


def test_50j_research_shell_relaunches_35d_above_bare_v2_ancestry(
    tmp_path: Path,
    monkeypatch,
) -> None:
    *_, continuation_overlay, checkpoint = _persist_bare_root_continuation(
        tmp_path,
        stem="50j-shell",
    )
    observed: dict[str, object] = {}

    def fail_controller_only_shell(*args, **kwargs):
        raise AssertionError("50J continuation launch must retain typed 35D lineage")

    def fail_root_only_shell(*args, **kwargs):
        raise AssertionError("50J continuation launch must use continuation product")

    def fake_continuation_shell(lineage) -> None:
        observed["lineage"] = lineage

    monkeypatch.setattr(
        cli,
        "_run_controller_only_research_session_shell",
        fail_controller_only_shell,
    )
    monkeypatch.setattr(
        cli,
        "_run_root_backed_research_session_shell",
        fail_root_only_shell,
    )
    monkeypatch.setattr(
        cli,
        "_run_root_backed_continuation_research_session_shell",
        fake_continuation_shell,
    )

    assert (
        cli.main(
            [
                "research-shell",
                "--root-backed-continuation-overlay",
                str(continuation_overlay),
            ]
        )
        == 0
    )

    lineage = observed["lineage"]
    assert isinstance(
        lineage,
        ChromiumResearchRootBackedSessionContinuationShellLineage,
    )
    assert lineage.overlay_source == continuation_overlay.resolve()
    assert lineage.reentry is not checkpoint.fresh_reentry
    assert (
        lineage.reentry.controller.presentation
        == checkpoint.fresh_reentry.controller.presentation
    )
    _assert_bare_member_survives(lineage.reentry)


def test_50j_research_inspect_is_deterministic_for_35d_above_bare_v2_ancestry(
    tmp_path: Path,
    capsys,
) -> None:
    *_, continuation_overlay, checkpoint = _persist_bare_root_continuation(
        tmp_path,
        stem="50j-inspect",
    )

    args = [
        "research-inspect",
        "--root-backed-continuation-overlay",
        str(continuation_overlay),
    ]
    assert cli.main(args) == 0
    first = capsys.readouterr().out
    assert cli.main(args) == 0
    second = capsys.readouterr().out
    assert first == second

    plan = load_chromium_research_root_backed_session_continuation_reentry_plan_document(
        continuation_overlay
    )
    reentry = reenter_chromium_research_root_backed_session_continuation(plan)
    lineage = prove_chromium_research_root_backed_session_continuation_shell_lineage(
        reentry,
        overlay_source=continuation_overlay,
    )
    expected = serialize_chromium_research_root_backed_session_authority_inspection(
        inspect_chromium_research_root_backed_session_continuation_launch(lineage)
    )
    assert first == expected

    report = json.loads(first)
    assert report["report_role"] == "read_only_inspection_not_authority"
    assert report["launch_provenance"]["launch_family"] == (
        "persisted 35D/35E root-backed continuation launch"
    )
    assert report["launch_provenance"]["launch_location_context_only"] == str(
        continuation_overlay.resolve()
    )
    assert report["current_governed_state"]["declared_continuation_edge_count"] == 1
    assert report["current_governed_state"]["endpoint_sha256"] == (
        checkpoint.fresh_reentry.controller.declared_endpoint.verification.edge_record_sha256
    )
    _assert_bare_member_survives(lineage.reentry)


def test_50j_tampered_prior_bare_overlay_v2_breaks_fresh_35d_reentry(
    tmp_path: Path,
) -> None:
    values = _persist_bare_root_continuation(tmp_path, stem="50j-tamper")
    root_overlay = values[6]
    continuation_overlay = values[13]

    root_overlay.write_bytes(root_overlay.read_bytes() + b"tampered")

    plan = load_chromium_research_root_backed_session_continuation_reentry_plan_document(
        continuation_overlay
    )
    with pytest.raises(
        ChromiumResearchRootBackedSessionContinuationReentryError,
        match="prior 35C overlay",
    ):
        reenter_chromium_research_root_backed_session_continuation(plan)
