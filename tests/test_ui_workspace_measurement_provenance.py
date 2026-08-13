from dataclasses import replace
import importlib
from pathlib import Path

import pytest

from pyxis.app import build_and_run_workspace, create_workspace_presentation
from pyxis.authoring import create_workspace_spec
from pyxis.ui import create_workspace_shell
from test_ui_workspace_measurement_mount import _measurement_presentation


workspace_shell_module = importlib.import_module("pyxis.ui.workspace_shell")


def _matching_presentations(tmp_path: Path):
    measurement = _measurement_presentation(tmp_path)
    spec = create_workspace_spec("Text Lab", "Mean stays attached to median evidence.")
    run = build_and_run_workspace(spec, tmp_path / "workspace", "same workload")
    workspace = create_workspace_presentation(spec, run)
    return workspace, measurement


@pytest.mark.parametrize(
    ("field", "replacement", "message"),
    (
        ("repository_id", "other-repository", "Repository ID"),
        ("workspace_id", "other-workspace", "Workspace ID"),
        ("rir_sha256", "f" * 64, "RIR SHA-256"),
    ),
)
def test_workspace_shell_rejects_measurement_provenance_before_textual_init(
    tmp_path: Path,
    monkeypatch,
    field: str,
    replacement: str,
    message: str,
) -> None:
    workspace, measurement = _matching_presentations(tmp_path)
    subject = measurement.source.envelope.partition.condition.subject
    assert subject.repository_id == workspace.rir.repository_id
    assert subject.workspace_id == workspace.rir.workspace_id
    assert subject.rir_sha256 == workspace.rir.rir_sha256

    mismatched = replace(
        workspace,
        rir=replace(workspace.rir, **{field: replacement}),
    )

    def fail_if_textual_initializes(*args, **kwargs):
        raise AssertionError("Provenance mismatch must fail before Textual initialization.")

    monkeypatch.setattr(
        workspace_shell_module._WorkspaceShell,
        "__init__",
        fail_if_textual_initializes,
    )

    with pytest.raises(ValueError, match=message):
        create_workspace_shell(
            mismatched,
            measurement_presentation=measurement,
        )
