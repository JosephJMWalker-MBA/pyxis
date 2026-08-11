import json
from pathlib import Path

from pyxis.app import build_and_run_workspace
from pyxis.authoring import create_workspace_spec
from pyxis.runtime import run_materialized_workspace


_REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
_EXAMPLE_ROOT = _REPOSITORY_ROOT / "examples/text_lab"
_DESCRIPTION = "Permanent executable architectural specification for Repository Zero."


def test_text_lab_is_current_executable_architectural_specification(
    tmp_path: Path,
) -> None:
    sample = json.loads(
        (_EXAMPLE_ROOT / "runtime/sample.json").read_text(encoding="utf-8")
    )
    expected = json.loads(
        (_EXAMPLE_ROOT / "runtime/expected.json").read_text(encoding="utf-8")
    )
    spec = create_workspace_spec("Text Lab", _DESCRIPTION)

    rebuilt = build_and_run_workspace(spec, tmp_path, sample["text"])

    produced_paths = (
        rebuilt.build.canonical_path,
        rebuilt.build.rir_path,
        rebuilt.build.manifest_path,
        *rebuilt.build.written_paths,
    )
    assert tuple(path.relative_to(tmp_path).as_posix() for path in produced_paths) == (
        "authoring/canonical/workspace.json",
        "generated/repository.rir.json",
        "generated/generation.manifest.json",
        "generated/capabilities/inspect_text.py",
        "generated/capabilities/normalize_text.py",
        "generated/workspaces/text_lab/main.py",
    )

    for produced_path in produced_paths:
        relative_path = produced_path.relative_to(tmp_path)
        committed_path = _EXAMPLE_ROOT / relative_path
        assert committed_path.is_file()
        assert produced_path.read_bytes() == committed_path.read_bytes()

    assert rebuilt.runtime_result == expected

    committed_runtime_result = run_materialized_workspace(
        rebuilt.build.repository,
        _EXAMPLE_ROOT,
        sample["text"],
    )
    assert committed_runtime_result == expected
