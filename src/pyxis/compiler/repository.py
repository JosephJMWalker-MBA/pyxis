from __future__ import annotations

from pyxis.rir.model import RepositoryIR

from .artifacts import (
    GeneratedArtifact,
    compile_inspect_text,
    compile_normalize_text,
    compile_split_lines,
    compile_workspace_entrypoint,
)


_CAPABILITY_COMPILERS = {
    "inspect_text": compile_inspect_text,
    "normalize_text": compile_normalize_text,
    "split_lines": compile_split_lines,
}


def compile_repository(
    repository: RepositoryIR,
) -> tuple[GeneratedArtifact, ...]:
    """Compile one RIR into the complete ordered repository artifact set.

    Capability artifacts are emitted in the order declared by the Workspace RIR.
    The composed Workspace entrypoint is always emitted last. This remains a pure
    compiler operation: no files are written and no generated code is executed.
    """

    artifacts: list[GeneratedArtifact] = []

    for capability_id in repository.workspace.capabilities:
        compiler = _CAPABILITY_COMPILERS.get(capability_id)
        if compiler is None:
            raise ValueError(
                f"No compiler is registered for capability {capability_id!r}."
            )
        artifacts.append(compiler(repository))

    artifacts.append(compile_workspace_entrypoint(repository))
    return tuple(artifacts)
