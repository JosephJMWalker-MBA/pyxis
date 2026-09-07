from __future__ import annotations

import json
from pathlib import Path

import pyxis.cli as cli
from pyxis.app.chromium_research_paragraph_text_selection_load import (
    ChromiumPageResearchLoadedParagraphTextSelectionRecord,
)
from pyxis.app.chromium_research_root_backed_session_authority_inspection import (
    inspect_chromium_research_root_backed_session_launch,
)
from pyxis.app.chromium_research_root_backed_session_authority_inspection_report import (
    serialize_chromium_research_root_backed_session_authority_inspection,
)
from pyxis.app.chromium_research_root_backed_session_reentry import (
    reenter_chromium_research_root_backed_session,
)
from pyxis.app.chromium_research_root_backed_session_reentry_plan_document import (
    load_chromium_research_root_backed_session_reentry_plan_document,
)
from pyxis.app.chromium_research_root_backed_session_shell_lineage import (
    ChromiumResearchRootBackedSessionShellLineage,
    prove_chromium_research_root_backed_session_shell_lineage,
)
from test_app_chromium_research_root_backed_session_reentry_plan_document_v2 import (
    _persist_bare_overlay,
)


_OVERLAY_V2 = "pyxis.chromium.research_root_backed_session_reentry_locator_overlay.v2"


def test_50i_research_shell_relaunches_bare_overlay_v2_into_existing_root_backed_product(
    tmp_path: Path,
    monkeypatch,
) -> None:
    (
        _,
        _,
        root,
        edge,
        verification,
        _,
        overlay,
        checkpoint_wrapper,
    ) = _persist_bare_overlay(tmp_path, stem="50i-shell")
    document = json.loads(overlay.read_text(encoding="utf-8"))
    assert document["format"] == _OVERLAY_V2

    observed: dict[str, object] = {}

    def fail_workspace_build(*args, **kwargs):
        raise AssertionError("50I root-backed relaunch must not build Workspace state")

    def fail_ordinary_shell(*args, **kwargs):
        raise AssertionError("50I root-backed relaunch must not use ordinary re-entry")

    def fail_controller_only_shell(*args, **kwargs):
        raise AssertionError("50I root-backed relaunch must retain typed 35B lineage")

    def fake_root_backed_shell(lineage):
        observed["lineage"] = lineage
        return None

    monkeypatch.setattr(cli, "build_and_run_workspace", fail_workspace_build)
    monkeypatch.setattr(cli, "_run_research_session_shell", fail_ordinary_shell)
    monkeypatch.setattr(
        cli,
        "_run_controller_only_research_session_shell",
        fail_controller_only_shell,
    )
    monkeypatch.setattr(
        cli,
        "_run_root_backed_research_session_shell",
        fake_root_backed_shell,
    )

    assert (
        cli.main(["research-shell", "--root-backed-overlay", str(overlay)])
        == 0
    )

    lineage = observed["lineage"]
    assert isinstance(lineage, ChromiumResearchRootBackedSessionShellLineage)
    assert lineage.overlay_source == overlay.resolve()

    fresh = lineage.reentry
    assert fresh is not verification.fresh_reentry
    assert fresh is not checkpoint_wrapper.checkpoint.fresh_reentry
    assert fresh.controller.presentation == verification.fresh_reentry.controller.presentation
    assert (
        fresh.loaded_root.verification.root_record_sha256
        == root.persistence.root_record_sha256
    )
    assert (
        fresh.controller.declared_endpoint.verification.edge_record_sha256
        == edge.persistence.edge_record_sha256
    )

    loaded_bare = fresh.loaded_appended_members[0]
    assert isinstance(
        loaded_bare,
        ChromiumPageResearchLoadedParagraphTextSelectionRecord,
    )
    assert loaded_bare.selection.selected_text == "Bare"
    assert not hasattr(loaded_bare, "note")
    assert (
        fresh.loaded_root.transition.successor_note.note.working_set.items[-1]
        is loaded_bare
    )
    assert (
        fresh.controller.declared_endpoint.revision.revised_note.working_set.items[-1]
        is loaded_bare
    )


def test_50i_research_inspect_is_deterministic_for_bare_overlay_v2_and_matches_shared_projection(
    tmp_path: Path,
    capsys,
) -> None:
    (
        _,
        _,
        root,
        edge,
        _,
        _,
        overlay,
        _,
    ) = _persist_bare_overlay(tmp_path, stem="50i-inspect")
    document = json.loads(overlay.read_text(encoding="utf-8"))
    assert document["format"] == _OVERLAY_V2

    assert (
        cli.main(["research-inspect", "--root-backed-overlay", str(overlay)])
        == 0
    )
    first = capsys.readouterr().out
    assert (
        cli.main(["research-inspect", "--root-backed-overlay", str(overlay)])
        == 0
    )
    second = capsys.readouterr().out

    assert first == second

    plan = load_chromium_research_root_backed_session_reentry_plan_document(
        overlay
    )
    reentry = reenter_chromium_research_root_backed_session(plan)
    lineage = prove_chromium_research_root_backed_session_shell_lineage(
        reentry,
        overlay_source=overlay,
    )
    expected = serialize_chromium_research_root_backed_session_authority_inspection(
        inspect_chromium_research_root_backed_session_launch(lineage)
    )
    assert first == expected

    report = json.loads(first)
    assert (
        report["format"]
        == "pyxis.chromium.research_root_backed_session_authority_inspection.v1"
    )
    assert report["report_role"] == "read_only_inspection_not_authority"
    assert report["launch_provenance"]["launch_family"] == (
        "persisted 35C root-backed launch"
    )
    assert report["launch_provenance"]["launch_location_context_only"] == str(
        overlay.resolve()
    )
    assert (
        report["launch_provenance"]["root_sha256"]
        == root.persistence.root_record_sha256
    )
    assert (
        report["launch_provenance"]["launch_endpoint_sha256"]
        == edge.persistence.edge_record_sha256
    )
    assert report["current_governed_state"]["endpoint_sha256"] == (
        edge.persistence.edge_record_sha256
    )
    assert report["current_governed_state"]["declared_continuation_edge_count"] is None

    loaded_bare = lineage.reentry.loaded_appended_members[0]
    assert isinstance(
        loaded_bare,
        ChromiumPageResearchLoadedParagraphTextSelectionRecord,
    )
    assert loaded_bare.selection.selected_text == "Bare"
    assert not hasattr(loaded_bare, "note")
