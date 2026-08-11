from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path

from pyxis.rir.model import RepositoryIR

from .artifacts import GeneratedArtifact


_GENERATION_MANIFEST_PATH = Path("generated/generation.manifest.json")


@dataclass(frozen=True, slots=True)
class ManifestArtifact:
    """Integrity evidence for one deterministic compiler product."""

    path: str
    node_sha256: str
    artifact_sha256: str


@dataclass(frozen=True, slots=True)
class GenerationManifest:
    """Minimal evidence connecting one RIR to its compiler products."""

    rir_sha256: str
    artifacts: tuple[ManifestArtifact, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "rir_sha256": self.rir_sha256,
            "artifacts": [asdict(artifact) for artifact in self.artifacts],
        }


def _normalized_rir_bytes(repository: RepositoryIR) -> bytes:
    payload = json.dumps(
        repository.to_dict(),
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    return payload.encode("utf-8")


def build_generation_manifest(
    repository: RepositoryIR,
    artifacts: tuple[GeneratedArtifact, ...],
) -> GenerationManifest:
    """Build deterministic integrity evidence from compiler input and output.

    This function is pure. It does not read generated files, infer status from
    the filesystem, persist anything, or make reuse decisions.
    """

    rir_sha256 = hashlib.sha256(_normalized_rir_bytes(repository)).hexdigest()
    manifest_artifacts = tuple(
        ManifestArtifact(
            path=artifact.path,
            node_sha256=artifact.node_sha256,
            artifact_sha256=hashlib.sha256(artifact.source.encode("utf-8")).hexdigest(),
        )
        for artifact in artifacts
    )

    return GenerationManifest(
        rir_sha256=rir_sha256,
        artifacts=manifest_artifacts,
    )


def persist_generation_manifest(
    manifest: GenerationManifest,
    workspace_root: Path,
) -> Path:
    """Persist already-derived generation evidence as deterministic JSON.

    This filesystem boundary writes only the manifest. It does not compile,
    materialize implementation artifacts, or inspect existing generated files.
    """

    root = workspace_root.resolve()
    manifest_path = root / _GENERATION_MANIFEST_PATH
    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    payload = json.dumps(
        manifest.to_dict(),
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    )
    manifest_path.write_text(f"{payload}\n", encoding="utf-8")
    return manifest_path
