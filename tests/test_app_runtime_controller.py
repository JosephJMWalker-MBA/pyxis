import importlib
from pathlib import Path

from pyxis.app import (
    WorkspaceRuntimeController,
    build_and_run_workspace,
)
from pyxis.authoring import create_workspace_spec


controller_module = importlib.import_module("pyxis.app.controller")
compiler_repository_module = importlib.import_module("pyxis.compiler.repository")


def test_workspace_runtime_controller_retains_fresh_run_evidence(
    tmp_path: Path,
    monkeypatch,
) -> None:
    root = tmp_path / "workspace"
    spec = create_workspace_spec(
        "Text Lab",
        "Application controller retains transient runtime evidence.",
    )
    first = build_and_run_workspace(spec, root, "one")
    controller = WorkspaceRuntimeController(root, first)

    def fail_if_compiled(*args, **kwargs):
        raise AssertionError("Runtime controller must not compile.")

    monkeypatch.setattr(
        compiler_repository_module,
        "compile_repository",
        fail_if_compiled,
    )

    real_rerun = controller_module.rerun_workspace
    rerun_calls = 0

    def counted_rerun(*args, **kwargs):
        nonlocal rerun_calls
        rerun_calls += 1
        return real_rerun(*args, **kwargs)

    monkeypatch.setattr(controller_module, "rerun_workspace", counted_rerun)

    presentation = controller.rerun("two words")

    assert rerun_calls == 1
    assert controller.current_run is not first
    assert controller.current_run.build is first.build
    assert controller.current_run.runtime_result != first.runtime_result
    assert presentation.runtime_result == controller.current_run.runtime_result
