import importlib
from pathlib import Path
from types import SimpleNamespace

from pyxis.app import build_workspace, export_workspace
from pyxis.authoring import create_workspace_spec


app_export_module = importlib.import_module("pyxis.app.export")
compiler_repository_module = importlib.import_module("pyxis.compiler.repository")


def _file_snapshot(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in root.rglob("*")
        if path.is_file()
    }


def test_export_workspace_is_thin_composition_of_existing_export_boundaries(
    tmp_path: Path,
    monkeypatch,
) -> None:
    build = SimpleNamespace(
        repository=object(),
        artifacts=(object(),),
        manifest=object(),
    )
    source = tmp_path / "workspace"
    destination = tmp_path / "portable"
    text = "verification input"
    plan = object()
    materialization = object()
    verification = object()
    calls: list[tuple[object, ...]] = []

    def fake_build_export_plan(repository, artifacts, manifest):
        calls.append(("plan", repository, artifacts, manifest))
        return plan

    def fake_materialize_export_plan(actual_plan, source_root, destination_root):
        calls.append(("materialize", actual_plan, source_root, destination_root))
        return materialization

    def fake_verify_export(actual_plan, source_root, export_root, actual_text):
        calls.append(("verify", actual_plan, source_root, export_root, actual_text))
        return verification

    monkeypatch.setattr(app_export_module, "build_export_plan", fake_build_export_plan)
    monkeypatch.setattr(
        app_export_module,
        "materialize_export_plan",
        fake_materialize_export_plan,
    )
    monkeypatch.setattr(app_export_module, "verify_export", fake_verify_export)

    result = export_workspace(build, source, destination, text)

    assert calls == [
        ("plan", build.repository, build.artifacts, build.manifest),
        ("materialize", plan, source, destination),
        ("verify", plan, source, destination, text),
    ]
    assert result.materialization is materialization
    assert result.verification is verification
    assert not source.exists()
    assert not destination.exists()


def test_export_workspace_turns_existing_build_into_verified_ready_export(
    tmp_path: Path,
    monkeypatch,
) -> None:
    source = tmp_path / "workspace"
    destination = tmp_path / "portable"
    spec = create_workspace_spec(
        "Text Lab",
        "Application export orchestration proof.",
    )
    build = build_workspace(spec, source)
    source_before = _file_snapshot(source)

    def fail_if_compiled(*args, **kwargs):
        raise AssertionError("Application export orchestration must not compile.")

    monkeypatch.setattr(
        compiler_repository_module,
        "compile_repository",
        fail_if_compiled,
    )

    result = export_workspace(
        build,
        source,
        destination,
        "  hello   world  ",
    )

    assert result.materialization.destination_root == destination.resolve()
    assert result.verification.readiness == "READY"
    assert result.verification.identity.export_root == destination.resolve()
    assert result.verification.runtime.export_root == destination.resolve()
    assert result.verification.identity.repository_id == build.repository.repository_id
    assert result.verification.identity.workspace_id == build.repository.workspace.workspace_id
    assert result.verification.runtime.source_result == (
        result.verification.runtime.export_result
    )
    assert _file_snapshot(source) == source_before
