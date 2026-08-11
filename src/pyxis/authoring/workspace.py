from __future__ import annotations

from dataclasses import asdict, dataclass, replace
import re


_DEFAULT_CAPABILITIES = ("inspect_text", "normalize_text")


@dataclass(frozen=True, slots=True)
class WorkspaceSpec:
    """Canonical user-authored Workspace intent.

    This object is deliberately small. It records what the user asked Pyxis to
    create without containing compiler or runtime behavior.
    """

    workspace_id: str
    name: str
    description: str
    capabilities: tuple[str, ...] = _DEFAULT_CAPABILITIES

    def to_canonical_dict(self) -> dict[str, object]:
        return asdict(self)

    def without_capability(self, capability_id: str) -> WorkspaceSpec:
        """Return a proposed canonical state with one capability removed.

        The current canonical object is immutable and remains unchanged. This
        method performs no persistence, lowering, compilation, or runtime work.
        """

        if capability_id not in self.capabilities:
            raise ValueError(
                f"Workspace does not contain capability {capability_id!r}."
            )

        return replace(
            self,
            capabilities=tuple(
                capability
                for capability in self.capabilities
                if capability != capability_id
            ),
        )


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", value.strip().lower()).strip("_")
    return slug or "workspace"


def create_workspace_spec(name: str, description: str) -> WorkspaceSpec:
    """Create canonical Workspace intent from the minimum first-run inputs."""

    clean_name = name.strip()
    clean_description = description.strip()

    if not clean_name:
        raise ValueError("Workspace name is required.")
    if not clean_description:
        raise ValueError("Workspace description is required.")

    return WorkspaceSpec(
        workspace_id=_slugify(clean_name),
        name=clean_name,
        description=clean_description,
    )
