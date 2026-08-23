import builtins
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

import pyxis.cli as cli
from test_app_chromium_research_session_reentry import _durable_fixture
from test_app_chromium_research_session_reentry_plan_document import (
    _document_for,
    _write_document,
)


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


def test_research_shell_command_freshly_reenters_plan_and_never_builds_workspace(
    tmp_path: Path,
    monkeypatch,
) -> None:
    fixture = _durable_fixture(tmp_path)
    plan_path = tmp_path / "launch.plan.json"
    _write_document(plan_path, _document_for(fixture.plan, tmp_path))
    observed: dict[str, object] = {}

    def fail_workspace_build(*args, **kwargs):
        raise AssertionError("research-shell must not fabricate Repository Zero state")

    def fake_run_research_session_shell(controller) -> None:
        observed["controller"] = controller

    monkeypatch.setattr(cli, "build_and_run_workspace", fail_workspace_build)
    monkeypatch.setattr(
        cli,
        "_run_research_session_shell",
        fake_run_research_session_shell,
    )

    exit_code = cli.main(["research-shell", "--plan", str(plan_path)])

    assert exit_code == 0
    controller = observed["controller"]
    assert controller.presentation.sequence.members[-1].note_text == (
        "v6 exact human wording\nStill tentative."
    )
    assert controller.loaded.verification.path == fixture.declaration_path.resolve()


def test_research_shell_command_reports_invalid_plan_as_cli_usage_error(
    tmp_path: Path,
    capsys,
    monkeypatch,
) -> None:
    plan_path = tmp_path / "invalid.plan.json"
    plan_path.write_text("{}\n", encoding="utf-8")

    def fail_if_launched(*args, **kwargs):
        raise AssertionError("invalid plan must fail before Textual launch")

    monkeypatch.setattr(cli, "_run_research_session_shell", fail_if_launched)

    with pytest.raises(SystemExit) as exc_info:
        cli.main(["research-shell", "--plan", str(plan_path)])

    assert exc_info.value.code == 2
    assert "research-shell failed" in capsys.readouterr().err


def test_research_shell_help_exposes_only_explicit_plan_entry(capsys) -> None:
    with pytest.raises(SystemExit) as exc_info:
        cli.main(["research-shell", "--help"])

    output = capsys.readouterr().out
    assert exc_info.value.code == 0
    assert "--plan" in output
    assert "--latest" not in output
    assert "--head" not in output
    assert "--directory" not in output


def test_research_shell_ui_dependency_is_lazy_and_reports_install_hint(monkeypatch) -> None:
    original_import = builtins.__import__

    def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name == "pyxis.ui.research_session_shell":
            raise ModuleNotFoundError("No module named 'textual'", name="textual")
        return original_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    with pytest.raises(RuntimeError, match=r"pyxis\[ui\]"):
        cli._run_research_session_shell(object())  # type: ignore[arg-type]
