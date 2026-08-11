import hashlib
import json
from pathlib import Path

from pyxis.authoring.workspace import create_workspace_spec
from pyxis.compiler import (
    build_generation_manifest,
    compile_repository,
    persist_generation_manifest,
)
from pyxis.rir.model import build_repository_ir


def test_generation_manifest_records_only_current_integrity_evidence() -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "Minimal generation manifest proof.",
    )
    repository = build_repository_ir(spec)
    artifacts = compile_repository(repository)

    manifest = build_generation_manifest(repository, artifacts)

    normalized_rir = json.dumps(
        repository.to_dict(),
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    assert manifest.rir_sha256 == hashlib.sha256(normalized_rir).hexdigest()
    assert tuple(entry.path for entry in manifest.artifacts) == tuple(
        artifact.path for artifact in artifacts
    )
    assert tuple(entry.node_sha256 for entry in manifest.artifacts) == tuple(
        artifact.node_sha256 for artifact in artifacts
    )
    assert tuple(entry.artifact_sha256 for entry in manifest.artifacts) == tuple(
        hashlib.sha256(artifact.source.encode("utf-8")).hexdigest()
        for artifact in artifacts
    )

    payload = manifest.to_dict()
    assert set(payload) == {"rir_sha256", "artifacts"}
    assert all(
        set(entry) == {"path", "node_sha256", "artifact_sha256"}
        for entry in payload["artifacts"]
    )


def test_generation_manifest_is_deterministic_and_non_mutating() -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "Manifest determinism proof.",
    )
    repository = build_repository_ir(spec)
    artifacts = compile_repository(repository)
    repository_before = repository.to_dict()
    artifacts_before = artifacts

    first = build_generation_manifest(repository, artifacts)
    second = build_generation_manifest(repository, artifacts)

    assert first == second
    assert repository.to_dict() == repository_before
    assert artifacts == artifacts_before


def test_persist_generation_manifest_writes_only_manifest_evidence(
    tmp_path: Path,
) -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "Manifest persistence boundary proof.",
    )
    repository = build_repository_ir(spec)
    artifacts = compile_repository(repository)
    manifest = build_generation_manifest(repository, artifacts)

    first_root = tmp_path / "first"
    second_root = tmp_path / "second"
    first_path = persist_generation_manifest(manifest, first_root)
    second_path = persist_generation_manifest(manifest, second_root)

    assert first_path == first_root.resolve() / "generated/generation.manifest.json"
    assert second_path == second_root.resolve() / "generated/generation.manifest.json"
    assert first_path.read_text(encoding="utf-8") == second_path.read_text(
        encoding="utf-8"
    )
    assert json.loads(first_path.read_text(encoding="utf-8")) == manifest.to_dict()
    assert tuple(path for path in first_root.rglob("*") if path.is_file()) == (
        first_path,
    )
    assert not tuple(first_root.rglob("*.py"))
