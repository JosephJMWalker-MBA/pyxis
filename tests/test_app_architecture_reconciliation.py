from dataclasses import FrozenInstanceError, replace
from pathlib import Path

import pytest

from pyxis.app import (
    WorkspaceController,
    apply_workspace_add_split_lines,
    build_and_run_workspace,
    preview_add_split_lines,
)
from pyxis.app.architecture_reconciliation import (
    create_architecture_consequence_reconciliation,
)
from pyxis.app.preview_presentation import create_architecture_preview_presentation
from pyxis.authoring import create_workspace_spec


def test_split_lines_apply_reconciles_proposed_and_observed_evidence(
    tmp_path: Path,
) -> None:
    source = tmp_path / "workspace"
    text = "first line\nsecond line"
    spec = create_workspace_spec(
        "Text Lab",
        "Observed architecture consequence reconciliation proof.",
    )
    run = build_and_run_workspace(spec, source, text)
    controller = WorkspaceController(source, run)

    proposed = controller.preview_add_split_lines()
    assert controller.last_architecture_reconciliation is None

    presentation = controller.apply_pending_add_split_lines(
        "Observe whether the proposed split_lines consequences actually occur.",
        text,
    )
    reconciliation = controller.last_architecture_reconciliation

    assert reconciliation is not None
    assert reconciliation.proposed == proposed
    assert reconciliation.observed.operation == "add_capability:split_lines"
    assert (
        reconciliation.observed.before_canonical_sha256
        == proposed.current.canonical_sha256
    )
    assert (
        reconciliation.observed.after_canonical_sha256
        == proposed.proposed.canonical_sha256
    )
    assert reconciliation.observed.canonical_sha256 == presentation.canonical.canonical_sha256
    assert reconciliation.observed.rir_sha256 == presentation.rir.rir_sha256
    assert reconciliation.observed.rir_capabilities == presentation.rir.capabilities
    assert reconciliation.observed.runtime_keys == tuple(presentation.runtime_result)

    assert reconciliation.revision_transition_matches_preview is True
    assert reconciliation.observed_canonical_matches_preview is True
    assert reconciliation.observed_rir_capabilities_match_preview is True
    assert reconciliation.observed_runtime_keys_match_preview is True
    assert reconciliation.revision_completion_rir_matches_observed_rir is True

    by_path = {
        consequence.path: consequence
        for consequence in reconciliation.artifact_consequences
    }
    assert by_path["generated/capabilities/split_lines.py"].proposed_action == "add"
    assert (
        by_path["generated/capabilities/split_lines.py"].expected_generation_status
        == "new"
    )
    assert (
        by_path["generated/capabilities/split_lines.py"].observed_generation_status
        == "new"
    )
    assert by_path["generated/capabilities/split_lines.py"].matches is True
    assert (
        by_path["generated/workspaces/text_lab/main.py"].proposed_action
        == "change"
    )
    assert (
        by_path["generated/workspaces/text_lab/main.py"].expected_generation_status
        == "regenerated"
    )
    assert (
        by_path["generated/workspaces/text_lab/main.py"].observed_generation_status
        == "regenerated"
    )
    assert by_path["generated/workspaces/text_lab/main.py"].matches is True

    observed_statuses = {
        artifact.path: artifact.status
        for artifact in reconciliation.observed.artifact_generation
    }
    assert observed_statuses["generated/capabilities/inspect_text.py"] == "reused"
    assert observed_statuses["generated/capabilities/normalize_text.py"] == "reused"
    assert observed_statuses["generated/capabilities/split_lines.py"] == "new"
    assert observed_statuses["generated/workspaces/text_lab/main.py"] == "regenerated"

    with pytest.raises(FrozenInstanceError):
        reconciliation.observed.operation = "changed"  # type: ignore[misc]


def test_remove_normalize_reconciliation_observes_removed_compiler_product(
    tmp_path: Path,
) -> None:
    source = tmp_path / "workspace"
    spec = create_workspace_spec(
        "Text Lab",
        "Removal reconciliation remains a concrete architecture operation.",
    )
    run = build_and_run_workspace(spec, source, "hello world")
    controller = WorkspaceController(source, run)

    proposed = controller.preview_remove_normalize_text()
    controller.apply_pending_remove_normalize_text(
        "Observe the concrete normalize_text removal consequences.",
        "hello world",
    )
    reconciliation = controller.last_architecture_reconciliation

    assert reconciliation is not None
    assert reconciliation.proposed == proposed
    by_path = {
        consequence.path: consequence
        for consequence in reconciliation.artifact_consequences
    }
    removed = by_path["generated/capabilities/normalize_text.py"]
    assert removed.proposed_action == "remove"
    assert removed.expected_generation_status == "removed"
    assert removed.observed_generation_status == "removed"
    assert removed.matches is True
    assert reconciliation.observed_runtime_keys == ("inspect_text",)
    assert reconciliation.observed_runtime_keys_match_preview is True


def test_reconciliation_surfaces_observed_artifact_mismatch_without_rewriting_preview(
    tmp_path: Path,
) -> None:
    source = tmp_path / "workspace"
    spec = create_workspace_spec(
        "Text Lab",
        "Mismatch presentation must remain distinguishable from the preview.",
    )
    run = build_and_run_workspace(spec, source, "first\nsecond")
    pending = preview_add_split_lines(spec)
    proposed = create_architecture_preview_presentation(pending)
    applied = apply_workspace_add_split_lines(
        source,
        pending,
        run,
        "Produce genuine Apply evidence before altering only the test presentation.",
        "first\nsecond",
    )

    altered_artifacts = tuple(
        replace(artifact, status="reused")
        if artifact.path == "generated/capabilities/split_lines.py"
        else artifact
        for artifact in applied.presentation.artifacts
    )
    altered_presentation = replace(
        applied.presentation,
        artifacts=altered_artifacts,
    )

    reconciliation = create_architecture_consequence_reconciliation(
        proposed,
        applied.apply,
        altered_presentation,
    )

    split_lines = next(
        consequence
        for consequence in reconciliation.artifact_consequences
        if consequence.path == "generated/capabilities/split_lines.py"
    )
    assert split_lines.expected_generation_status == "new"
    assert split_lines.observed_generation_status == "reused"
    assert split_lines.matches is False
    assert reconciliation.proposed == proposed
    assert proposed.added_artifact_paths == (
        "generated/capabilities/split_lines.py",
    )


def test_successful_new_preview_clears_prior_reconciliation(
    tmp_path: Path,
) -> None:
    source = tmp_path / "workspace"
    spec = create_workspace_spec(
        "Text Lab",
        "A reconciliation must not be mistaken for evidence about a later preview.",
    )
    run = build_and_run_workspace(spec, source, "first\nsecond")
    controller = WorkspaceController(source, run)
    controller.preview_add_split_lines()
    controller.apply_pending_add_split_lines(
        "First architecture change.",
        "first\nsecond",
    )
    prior = controller.last_architecture_reconciliation
    assert prior is not None

    controller.preview_remove_normalize_text()

    assert controller.pending_preview is not None
    assert controller.last_architecture_reconciliation is None
