from pyxis.authoring import create_workspace_spec
from pyxis.compiler import (
    ExistingArtifactIntegrity,
    build_generation_manifest,
    classify_generation_statuses,
    compile_repository,
)
from pyxis.compiler.artifacts import GeneratedArtifact
from pyxis.rir import build_repository_ir


def _integrity_from_manifest(manifest):
    return tuple(
        ExistingArtifactIntegrity(
            path=entry.path,
            artifact_sha256=entry.artifact_sha256,
        )
        for entry in manifest.artifacts
    )


def _pairs(statuses):
    return tuple((entry.path, entry.status) for entry in statuses)


def test_first_generation_classifies_all_current_artifacts_as_new() -> None:
    spec = create_workspace_spec("Text Lab", "First generation status proof.")
    artifacts = compile_repository(build_repository_ir(spec))

    statuses = classify_generation_statuses(artifacts, None, ())

    assert _pairs(statuses) == (
        ("generated/capabilities/inspect_text.py", "new"),
        ("generated/capabilities/normalize_text.py", "new"),
        ("generated/workspaces/text_lab/main.py", "new"),
    )


def test_reuse_requires_semantic_and_artifact_integrity_agreement() -> None:
    spec = create_workspace_spec("Text Lab", "Reuse evidence proof.")
    repository = build_repository_ir(spec)
    artifacts = compile_repository(repository)
    manifest = build_generation_manifest(repository, artifacts)

    reused = classify_generation_statuses(
        artifacts,
        manifest,
        _integrity_from_manifest(manifest),
    )
    assert tuple(entry.status for entry in reused) == ("reused", "reused", "reused")

    tampered_integrity = list(_integrity_from_manifest(manifest))
    tampered_integrity[0] = ExistingArtifactIntegrity(
        path=tampered_integrity[0].path,
        artifact_sha256="tampered",
    )
    tampered = classify_generation_statuses(
        artifacts,
        manifest,
        tuple(tampered_integrity),
    )
    assert tuple(entry.status for entry in tampered) == (
        "regenerated",
        "reused",
        "reused",
    )

    changed_source = (
        GeneratedArtifact(
            path=artifacts[0].path,
            source=f"{artifacts[0].source}# compiler output changed\n",
            node_sha256=artifacts[0].node_sha256,
        ),
        *artifacts[1:],
    )
    compiler_changed = classify_generation_statuses(
        changed_source,
        manifest,
        _integrity_from_manifest(manifest),
    )
    assert tuple(entry.status for entry in compiler_changed) == (
        "regenerated",
        "reused",
        "reused",
    )


def test_generation_statuses_capture_semantic_regeneration_and_removal() -> None:
    spec = create_workspace_spec("Text Lab", "Semantic delta status proof.")
    current_repository = build_repository_ir(spec)
    current_artifacts = compile_repository(current_repository)
    previous_manifest = build_generation_manifest(
        current_repository,
        current_artifacts,
    )

    proposed_spec = spec.without_capability("normalize_text")
    proposed_artifacts = compile_repository(build_repository_ir(proposed_spec))

    statuses = classify_generation_statuses(
        proposed_artifacts,
        previous_manifest,
        _integrity_from_manifest(previous_manifest),
    )

    assert _pairs(statuses) == (
        ("generated/capabilities/inspect_text.py", "reused"),
        ("generated/workspaces/text_lab/main.py", "regenerated"),
        ("generated/capabilities/normalize_text.py", "removed"),
    )
