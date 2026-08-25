import builtins
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

import pyxis.cli as cli
from test_app_chromium_research_root_backed_session_continuation_checkpoint_extension import (
    _persist_extension,
)
from test_app_chromium_research_root_backed_session_continuation_reentry_plan_document import (
    _persist_valid_continuation,
)
from test_app_chromium_research_root_backed_session_reentry_plan_document import (
    _persist_valid_overlay,
)
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

    def fake_run_research_session_shell(reentry) -> None:
        observed["reentry"] = reentry

    monkeypatch.setattr(cli, "build_and_run_workspace", fail_workspace_build)
    monkeypatch.setattr(
        cli,
        "_run_research_session_shell",
        fake_run_research_session_shell,
    )

    exit_code = cli.main(["research-shell", "--plan", str(plan_path)])

    assert exit_code == 0
    reentry = observed["reentry"]
    assert reentry.plan.declaration_source == fixture.plan.declaration_source
    assert reentry.controller.presentation.sequence.members[-1].note_text == (
        "v6 exact human wording\nStill tentative."
    )
    assert reentry.controller.loaded.verification.path == fixture.declaration_path.resolve()


def test_research_shell_command_launches_explicit_35c_root_backed_overlay_controller_only(
    tmp_path: Path,
    monkeypatch,
) -> None:
    _, _, earned, _, overlay_path, _ = _persist_valid_overlay(tmp_path, stem="36a-root")
    observed: dict[str, object] = {}

    def fail_workspace_build(*args, **kwargs):
        raise AssertionError("root-backed research-shell must not build Workspace state")

    def fail_ordinary_shell(*args, **kwargs):
        raise AssertionError("root-backed launch must not fabricate ordinary re-entry lineage")

    def fake_controller_shell(controller) -> None:
        observed["controller"] = controller

    monkeypatch.setattr(cli, "build_and_run_workspace", fail_workspace_build)
    monkeypatch.setattr(cli, "_run_research_session_shell", fail_ordinary_shell)
    monkeypatch.setattr(
        cli,
        "_run_controller_only_research_session_shell",
        fake_controller_shell,
    )

    exit_code = cli.main(
        ["research-shell", "--root-backed-overlay", str(overlay_path)]
    )

    assert exit_code == 0
    controller = observed["controller"]
    assert controller.presentation == earned.controller.presentation
    assert (
        controller.declared_endpoint.verification.edge_record_sha256
        == earned.controller.declared_endpoint.verification.edge_record_sha256
    )


def test_research_shell_command_launches_explicit_35d_continuation_overlay_controller_only(
    tmp_path: Path,
    monkeypatch,
) -> None:
    *_, rollover, overlay, _ = _persist_valid_continuation(tmp_path, stem="36a-cont")
    observed: dict[str, object] = {}

    def fake_controller_shell(controller) -> None:
        observed["controller"] = controller

    monkeypatch.setattr(
        cli,
        "_run_controller_only_research_session_shell",
        fake_controller_shell,
    )

    exit_code = cli.main(
        [
            "research-shell",
            "--root-backed-continuation-overlay",
            str(overlay),
        ]
    )

    assert exit_code == 0
    controller = observed["controller"]
    assert controller.presentation == rollover.continuation_controller.presentation
    assert (
        controller.declared_endpoint.verification.edge_record_sha256
        == rollover.continuation_controller.declared_endpoint.verification.edge_record_sha256
    )


def test_research_shell_command_launches_35e_overlay_through_unchanged_35d_family(
    tmp_path: Path,
    monkeypatch,
) -> None:
    *_, next_overlay, extension = _persist_extension(tmp_path, stem="36a-cumulative")
    observed: dict[str, object] = {}

    def fake_controller_shell(controller) -> None:
        observed["controller"] = controller

    monkeypatch.setattr(
        cli,
        "_run_controller_only_research_session_shell",
        fake_controller_shell,
    )

    exit_code = cli.main(
        [
            "research-shell",
            "--root-backed-continuation-overlay",
            str(next_overlay),
        ]
    )

    assert exit_code == 0
    controller = observed["controller"]
    assert (
        controller.declared_endpoint.verification.edge_record_sha256
        == extension.fresh_reentry.controller.declared_endpoint.verification.edge_record_sha256
    )
    assert len(controller.presentation.sequence.members) == len(
        extension.next_plan.declared_edge_sources
    )


def test_controller_only_shell_does_not_supply_ordinary_reentry_lineage(
    tmp_path: Path,
    monkeypatch,
) -> None:
    import pyxis.ui.research_session_shell as shell_module

    _, _, earned, _, _, _ = _persist_valid_overlay(tmp_path, stem="36a-ui")
    observed: dict[str, object] = {}

    class FakeShell:
        def run(self) -> None:
            observed["ran"] = True

    def fake_create(controller, **kwargs):
        observed["controller"] = controller
        observed["kwargs"] = kwargs
        return FakeShell()

    monkeypatch.setattr(shell_module, "create_research_session_shell", fake_create)

    cli._run_controller_only_research_session_shell(earned.controller)

    assert observed["controller"] is earned.controller
    assert observed["kwargs"] == {}
    assert observed["ran"] is True


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


def test_research_shell_command_reports_invalid_root_backed_overlay_before_ui(
    tmp_path: Path,
    capsys,
    monkeypatch,
) -> None:
    overlay = tmp_path / "invalid-root.overlay.json"
    overlay.write_text("{}\n", encoding="utf-8")

    def fail_if_launched(*args, **kwargs):
        raise AssertionError("invalid root-backed overlay must fail before Textual launch")

    monkeypatch.setattr(
        cli,
        "_run_controller_only_research_session_shell",
        fail_if_launched,
    )

    with pytest.raises(SystemExit) as exc_info:
        cli.main(["research-shell", "--root-backed-overlay", str(overlay)])

    assert exc_info.value.code == 2
    assert "research-shell failed" in capsys.readouterr().err


def test_research_shell_requires_exactly_one_explicit_entry_family(
    tmp_path: Path,
    capsys,
) -> None:
    plan = tmp_path / "ordinary.json"
    overlay = tmp_path / "root.json"

    with pytest.raises(SystemExit) as missing:
        cli.main(["research-shell"])
    assert missing.value.code == 2

    with pytest.raises(SystemExit) as mixed:
        cli.main(
            [
                "research-shell",
                "--plan",
                str(plan),
                "--root-backed-overlay",
                str(overlay),
            ]
        )
    assert mixed.value.code == 2
    error = capsys.readouterr().err
    assert "not allowed with argument" in error or "one of the arguments" in error


def test_research_shell_help_exposes_only_explicit_entry_families(capsys) -> None:
    with pytest.raises(SystemExit) as exc_info:
        cli.main(["research-shell", "--help"])

    output = capsys.readouterr().out
    assert exc_info.value.code == 0
    assert "--plan" in output
    assert "--root-backed-overlay" in output
    assert "--root-backed-continuation-overlay" in output
    assert "--latest" not in output
    assert "--head" not in output
    assert "--directory" not in output
    assert "--auto" not in output


def test_research_shell_ui_dependency_is_lazy_and_reports_install_hint(monkeypatch) -> None:
    original_import = builtins.__import__

    def fake_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name == "pyxis.ui.research_session_shell":
            raise ModuleNotFoundError("No module named 'textual'", name="textual")
        return original_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(builtins, "__import__", fake_import)

    with pytest.raises(RuntimeError, match=r"pyxis\[ui\]"):
        cli._run_research_session_shell(object())  # type: ignore[arg-type]
    with pytest.raises(RuntimeError, match=r"pyxis\[ui\]"):
        cli._run_controller_only_research_session_shell(object())  # type: ignore[arg-type]
