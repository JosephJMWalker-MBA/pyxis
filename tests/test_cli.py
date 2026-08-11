import json
from pathlib import Path
from types import SimpleNamespace

import pyxis.cli as cli


def test_run_command_uses_permanent_workspace_path(
    tmp_path: Path,
    capsys,
) -> None:
    exit_code = cli.main(
        [
            "run",
            "--name",
            "Text Lab",
            "--description",
            "First real CLI path proof.",
            "--destination",
            str(tmp_path),
            "--text",
            "  hello   world  ",
        ]
    )

    output = json.loads(capsys.readouterr().out)

    assert exit_code == 0
    assert output["inspect_text"]["words"] == 2
    assert output["normalize_text"]["normalized_text"] == "hello world"
    assert (tmp_path / "authoring/canonical/workspace.json").is_file()
    assert (tmp_path / "generated/repository.rir.json").is_file()
    assert (tmp_path / "generated/generation.manifest.json").is_file()
    assert (tmp_path / "generated/workspaces/text_lab/main.py").is_file()


def test_run_command_delegates_to_application_orchestration(
    tmp_path: Path,
    capsys,
    monkeypatch,
) -> None:
    spec = object()
    observed: dict[str, object] = {}

    def fake_create_workspace_spec(name: str, description: str) -> object:
        observed["name"] = name
        observed["description"] = description
        return spec

    def fake_build_and_run_workspace(
        received_spec: object,
        destination: Path,
        text: str,
    ) -> SimpleNamespace:
        observed["spec"] = received_spec
        observed["destination"] = destination
        observed["text"] = text
        return SimpleNamespace(runtime_result={"delegated": True})

    monkeypatch.setattr(cli, "create_workspace_spec", fake_create_workspace_spec)
    monkeypatch.setattr(
        cli,
        "build_and_run_workspace",
        fake_build_and_run_workspace,
    )

    exit_code = cli.main(
        [
            "run",
            "--name",
            "Research Notes",
            "--description",
            "Thin CLI delegation proof.",
            "--destination",
            str(tmp_path),
            "--text",
            "sample text",
        ]
    )

    assert exit_code == 0
    assert observed == {
        "name": "Research Notes",
        "description": "Thin CLI delegation proof.",
        "spec": spec,
        "destination": tmp_path,
        "text": "sample text",
    }
    assert json.loads(capsys.readouterr().out) == {"delegated": True}
