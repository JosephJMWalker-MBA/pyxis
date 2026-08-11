from __future__ import annotations

from dataclasses import asdict, dataclass

from pyxis.authoring.workspace import WorkspaceSpec


RIR_SCHEMA_VERSION = "0.1"


@dataclass(frozen=True, slots=True)
class WorkspaceIR:
    """Compiler-facing representation of one authored Workspace."""

    workspace_id: str
    name: str
    description: str
    entrypoint: str
    capabilities: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class RepositoryIR:
    """Minimum deterministic Repository Intermediate Representation.

    The RIR is derived data. It contains the structure the compiler needs, but
    it does not contain generated source code or runtime behavior.
    """

    schema_version: str
    repository_id: str
    workspace: WorkspaceIR

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def build_repository_ir(spec: WorkspaceSpec) -> RepositoryIR:
    """Deterministically lower canonical Workspace intent into the RIR."""

    workspace = WorkspaceIR(
        workspace_id=spec.workspace_id,
        name=spec.name,
        description=spec.description,
        entrypoint="main.py",
        capabilities=spec.capabilities,
    )

    return RepositoryIR(
        schema_version=RIR_SCHEMA_VERSION,
        repository_id=spec.workspace_id.replace("_", "-"),
        workspace=workspace,
    )
