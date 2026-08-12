import json
from pathlib import Path

import pytest
from textual.widgets import Button, Static

from pyxis.app import (
    BuildAndRunResult,
    apply_remove_normalize_text,
    build_and_run_workspace,
    create_workspace_presentation,
    export_workspace,
    preview_remove_normalize_text,
)
from pyxis.authoring import create_workspace_spec
from pyxis.runtime import run_materialized_workspace
from pyxis.ui import WorkspaceDetail, create_workspace_shell


@pytest.mark.asyncio
async def test_workspace_detail_renders_complete_presentation_contract(
    tmp_path: Path,
) -> None:
    source = tmp_path / "workspace"
    portable = tmp_path / "portable"
    text = "  hello   world  "
    spec = create_workspace_spec(
        "Text Lab",
        "Complete read-only Workspace detail proof.",
    )
    build_and_run_workspace(spec, source, text)
    preview = preview_remove_normalize_text(spec)
    applied = apply_remove_normalize_text(
        preview,
        source,
        "Remove normalization so the detail screen shows governed change evidence.",
    )
    runtime_result = run_materialized_workspace(
        applied.build.repository,
        source,
        text,
    )
    run = BuildAndRunResult(
        build=applied.build,
        runtime_result=runtime_result,
    )
    export = export_workspace(applied.build, source, portable, text)
    presentation = create_workspace_presentation(
        preview.proposed_spec,
        run,
        revision_events=(applied.revision,),
        revision_completions=(applied.completion,),
        export=export,
    )
    shell = create_workspace_shell(presentation)

    async with shell.run_test(size=(120, 40)) as pilot:
        await pilot.pause()

        detail = shell.query_one(WorkspaceDetail)
        assert detail.presentation is presentation
        assert len(shell.query(Button)) == 0

        canonical_text = shell.query_one("#canonical-evidence", Static).content
        assert canonical_text == "\n".join(
            (
                f"Workspace ID: {presentation.canonical.workspace_id}",
                f"Name: {presentation.canonical.name}",
                f"Description: {presentation.canonical.description}",
                "Capabilities:",
                *(
                    f"- {capability}"
                    for capability in presentation.canonical.capabilities
                ),
                f"Canonical SHA-256: {presentation.canonical.canonical_sha256}",
            )
        )

        rir_text = shell.query_one("#rir-evidence", Static).content
        assert rir_text == "\n".join(
            (
                f"Schema version: {presentation.rir.schema_version}",
                f"Repository ID: {presentation.rir.repository_id}",
                f"Workspace ID: {presentation.rir.workspace_id}",
                f"Entrypoint: {presentation.rir.entrypoint}",
                "Capabilities:",
                *(
                    f"- {capability}"
                    for capability in presentation.rir.capabilities
                ),
                f"RIR SHA-256: {presentation.rir.rir_sha256}",
            )
        )

        artifact_blocks = []
        for artifact in presentation.artifacts:
            artifact_blocks.append(
                "\n".join(
                    (
                        f"Path: {artifact.path}",
                        f"Status: {artifact.status}",
                        f"Node SHA-256: {artifact.node_sha256 or '—'}",
                        f"Artifact SHA-256: {artifact.artifact_sha256 or '—'}",
                    )
                )
            )
        compiler_text = shell.query_one("#compiler-artifacts", Static).content
        assert compiler_text == "\n\n".join(artifact_blocks)
        assert "Status: removed" in str(compiler_text)
        assert (
            "Path: generated/capabilities/normalize_text.py\n"
            "Status: removed\n"
            "Node SHA-256: —\n"
            "Artifact SHA-256: —"
        ) in str(compiler_text)

        runtime_text = shell.query_one("#runtime-result", Static).content
        assert runtime_text == json.dumps(
            runtime_result,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        assert "normalize_text" not in str(runtime_text)

        revision = presentation.revisions[0]
        revision_text = shell.query_one("#revision-timeline", Static).content
        assert revision_text == "\n".join(
            (
                "Revision 1",
                f"Revision ID: {revision.revision_id}",
                f"Parent revision ID: {revision.parent_revision_id or '—'}",
                f"Operation: {revision.operation}",
                f"Rationale: {revision.rationale}",
                f"Before canonical SHA-256: {revision.before_canonical_sha256}",
                f"After canonical SHA-256: {revision.after_canonical_sha256}",
                "Completed: yes",
                f"Completion RIR SHA-256: {revision.completion_rir_sha256}",
                "Completion generation manifest SHA-256: "
                f"{revision.completion_generation_manifest_sha256}",
            )
        )

        assert presentation.export is not None
        export_text = shell.query_one("#export-verification", Static).content
        assert export_text == "\n".join(
            (
                "Readiness: READY",
                f"Export root: {presentation.export.export_root}",
                f"RIR SHA-256: {presentation.export.rir_sha256}",
                "Generation manifest SHA-256: "
                f"{presentation.export.generation_manifest_sha256}",
                "Verification input SHA-256: "
                f"{presentation.export.input_sha256}",
                f"Compiler product count: {presentation.export.compiler_product_count}",
            )
        )


@pytest.mark.asyncio
async def test_workspace_detail_keeps_missing_optional_evidence_explicit(
    tmp_path: Path,
) -> None:
    root = tmp_path / "workspace"
    spec = create_workspace_spec(
        "Text Lab",
        "Optional evidence remains explicitly absent.",
    )
    run = build_and_run_workspace(spec, root, "hello world")
    presentation = create_workspace_presentation(spec, run)
    shell = create_workspace_shell(presentation)

    async with shell.run_test(size=(100, 30)) as pilot:
        await pilot.pause()
        assert shell.query_one("#revision-timeline", Static).content == (
            "No revision evidence."
        )
        assert shell.query_one("#export-verification", Static).content == (
            "No READY evidence."
        )
        assert "NOT READY" not in str(
            shell.query_one("#export-verification", Static).content
        )
        assert len(shell.query(Button)) == 0
