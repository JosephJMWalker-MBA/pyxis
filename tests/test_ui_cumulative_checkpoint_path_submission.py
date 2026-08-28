from __future__ import annotations

import asyncio
from pathlib import Path
from types import SimpleNamespace

import pyxis.ui.chromium_research_cumulative_checkpoint_textual as form_module
import pyxis.ui.root_backed_continuation_research_session_shell as root_module
import pyxis.ui.second_basis_epoch_research_session_shell as second_module
import pyxis.ui.third_basis_epoch_research_session_shell as third_module


def _spec() -> form_module._CumulativeCheckpointTextualSpec:
    return form_module._CumulativeCheckpointTextualSpec(
        controls_id="controls",
        title="title",
        title_id="title-id",
        authority_notice="notice",
        authority_notice_id="notice-id",
        candidate_id="candidate-id",
        current_overlay_label="current",
        current_overlay_label_id="current-label",
        current_overlay_placeholder="current",
        current_overlay_input_id="current-input",
        successor_label="successor",
        successor_label_id="successor-label",
        successor_placeholder="successor",
        successor_input_id="successor-input",
        declaration_label="declaration",
        declaration_label_id="declaration-label",
        declaration_placeholder="declaration",
        declaration_input_id="declaration-input",
        overlay_label="next overlay",
        overlay_label_id="overlay-label",
        overlay_placeholder="next overlay",
        overlay_input_id="overlay-input",
        save_label="save",
        save_button_id="save-button",
        pending_status="pending",
        status_id="status",
    )


def _fake_form(values: dict[str, str]):
    spec = _spec()
    updates: list[str] = []
    widgets = {
        "#status": SimpleNamespace(update=updates.append),
        "#current-input": SimpleNamespace(value=values["current"]),
        "#successor-input": SimpleNamespace(value=values["successor"]),
        "#declaration-input": SimpleNamespace(value=values["declaration"]),
        "#overlay-input": SimpleNamespace(value=values["overlay"]),
    }

    def query_one(selector, _widget_type):
        return widgets[selector]

    controls = SimpleNamespace(
        _cumulative_checkpoint_spec=spec,
        query_one=query_one,
    )
    return controls, widgets, updates


def _collect(controls):
    return form_module._CumulativeCheckpointTextualControls._collect_cumulative_checkpoint_path_submission(
        controls,
        current_overlay_required="current required",
        successor_required="successor required",
        declaration_required="declaration required",
        next_overlay_required="next overlay required",
    )


def test_private_path_submission_preserves_blank_validation_order() -> None:
    cases = (
        ({"current": "", "successor": "", "declaration": "", "overlay": ""}, "current required"),
        ({"current": "current", "successor": "", "declaration": "", "overlay": ""}, "successor required"),
        ({"current": "current", "successor": "successor", "declaration": "", "overlay": ""}, "declaration required"),
        ({"current": "current", "successor": "successor", "declaration": "declaration", "overlay": ""}, "next overlay required"),
    )

    for values, expected in cases:
        controls, _widgets, updates = _fake_form(values)
        assert _collect(controls) is None
        assert updates == [expected]


def test_private_path_submission_returns_exact_unstripped_path_values() -> None:
    values = {
        "current": "  current.json  ",
        "successor": " successor.json ",
        "declaration": " declaration.json ",
        "overlay": " next-overlay.json ",
    }
    controls, _widgets, updates = _fake_form(values)

    submission = _collect(controls)

    assert submission == form_module._CumulativeCheckpointPathSubmission(
        current_overlay_source=Path(values["current"]),
        successor_edge_source=Path(values["successor"]),
        cumulative_declaration_destination=Path(values["declaration"]),
        next_overlay_destination=Path(values["overlay"]),
    )
    assert updates == []


def _exercise_concrete_save(
    monkeypatch,
    *,
    module,
    method,
    current_attr: str,
    persist_name: str,
    proof_name: str,
    promote_name: str,
    expected_messages: dict[str, str],
) -> None:
    current_reentry = object()
    rollover = object()
    controller = object()
    checkpoint = object()
    submission = form_module._CumulativeCheckpointPathSubmission(
        current_overlay_source=Path("current-overlay.json"),
        successor_edge_source=Path("successor.json"),
        cumulative_declaration_destination=Path("cumulative-declaration.json"),
        next_overlay_destination=Path("next-overlay.json"),
    )
    events: dict[str, object] = {}

    def collect_submission(**kwargs):
        events["messages"] = kwargs
        return submission

    def lock_after_success(received):
        events["locked"] = received

    controls = SimpleNamespace(
        rollover=rollover,
        current_reentry=current_reentry,
        _collect_cumulative_checkpoint_path_submission=collect_submission,
        lock_after_success=lock_after_success,
    )
    status_updates: list[str] = []
    status = SimpleNamespace(update=status_updates.append)

    def query_one(selector, _widget_type):
        if selector.endswith("-controls"):
            return controls
        return status

    shell = SimpleNamespace(
        last_research_rollover=rollover,
        research_controller=controller,
        query_one=query_one,
    )
    setattr(shell, current_attr, current_reentry)

    def persist(received_current, received_rollover, **kwargs):
        assert received_current is current_reentry
        assert received_rollover is rollover
        events["persistence_kwargs"] = kwargs
        return checkpoint

    def proof(received_checkpoint, **kwargs):
        assert received_checkpoint is checkpoint
        assert kwargs["current_reentry"] is current_reentry
        assert kwargs["rollover"] is rollover
        assert kwargs["one_hop_controller"] is controller
        events["proved"] = True

    async def promote(received_checkpoint):
        assert received_checkpoint is checkpoint
        events["promoted"] = True

    setattr(shell, promote_name, promote)
    monkeypatch.setattr(module, persist_name, persist)
    monkeypatch.setattr(module, proof_name, proof)

    asyncio.run(method(shell))

    assert events["messages"] == expected_messages
    assert events["persistence_kwargs"] == {
        "current_overlay_source": submission.current_overlay_source,
        "successor_edge_source": submission.successor_edge_source,
        "cumulative_declaration_destination": submission.cumulative_declaration_destination,
        "next_overlay_destination": submission.next_overlay_destination,
    }
    assert events["proved"] is True
    assert events["locked"] is checkpoint
    assert events["promoted"] is True
    assert status_updates == []


def test_root_backed_save_maps_private_submission_into_concrete_persistence(monkeypatch) -> None:
    _exercise_concrete_save(
        monkeypatch,
        module=root_module,
        method=root_module.RootBackedContinuationResearchSessionShell._save_root_backed_cumulative_checkpoint,
        current_attr="root_backed_continuation_reentry",
        persist_name="persist_chromium_research_root_backed_session_continuation_checkpoint_extension",
        proof_name="_require_checkpoint_result_matches_shell",
        promote_name="_promote_cumulative_checkpoint",
        expected_messages={
            "current_overlay_required": "Cumulative checkpoint failed: explicit current 35D/35E overlay path is required.",
            "successor_required": "Cumulative checkpoint failed: explicit current successor edge path is required.",
            "declaration_required": "Cumulative checkpoint failed: explicit no-overwrite cumulative declaration destination is required.",
            "next_overlay_required": "Cumulative checkpoint failed: explicit no-overwrite next overlay destination is required.",
        },
    )


def test_second_epoch_save_maps_private_submission_into_concrete_persistence(monkeypatch) -> None:
    _exercise_concrete_save(
        monkeypatch,
        module=second_module,
        method=second_module.SecondBasisEpochContinuationResearchSessionShell._save_second_basis_epoch_cumulative_checkpoint,
        current_attr="second_basis_epoch_continuation_reentry",
        persist_name="persist_chromium_research_second_basis_epoch_continuation_checkpoint_extension",
        proof_name="_require_second_basis_epoch_cumulative_checkpoint_matches_shell",
        promote_name="_promote_second_basis_epoch_cumulative_checkpoint",
        expected_messages={
            "current_overlay_required": "Cumulative second-epoch checkpoint failed: explicit current 37C/37D overlay path is required.",
            "successor_required": "Cumulative second-epoch checkpoint failed: explicit current successor edge path is required.",
            "declaration_required": "Cumulative second-epoch checkpoint failed: explicit no-overwrite cumulative declaration destination is required.",
            "next_overlay_required": "Cumulative second-epoch checkpoint failed: explicit no-overwrite next overlay destination is required.",
        },
    )


def test_third_epoch_save_maps_private_submission_into_concrete_persistence(monkeypatch) -> None:
    _exercise_concrete_save(
        monkeypatch,
        module=third_module,
        method=third_module.ThirdBasisEpochContinuationResearchSessionShell._save_third_basis_epoch_cumulative_checkpoint,
        current_attr="third_basis_epoch_continuation_reentry",
        persist_name="persist_chromium_research_third_basis_epoch_continuation_checkpoint_extension",
        proof_name="_require_third_basis_epoch_cumulative_checkpoint_matches_shell",
        promote_name="_promote_third_basis_epoch_cumulative_checkpoint",
        expected_messages={
            "current_overlay_required": "Cumulative third-epoch checkpoint failed: explicit current 40C/40D overlay path is required.",
            "successor_required": "Cumulative third-epoch checkpoint failed: explicit current successor edge path is required.",
            "declaration_required": "Cumulative third-epoch checkpoint failed: explicit no-overwrite cumulative declaration destination is required.",
            "next_overlay_required": "Cumulative third-epoch checkpoint failed: explicit no-overwrite next overlay destination is required.",
        },
    )


def test_private_form_kernel_still_exports_no_public_authority_surface() -> None:
    assert form_module.__all__ == []
