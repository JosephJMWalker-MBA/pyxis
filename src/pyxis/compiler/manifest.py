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


def repository_ir_sha256(repository: RepositoryIR) -> str:
    """Return the deterministic identity of one compiler-input RIR."""

    return hashlib.sha256(_normalized_rir_bytes(repository)).hexdigest()


def _normalized_manifest_bytes(manifest: GenerationManifest) -> bytes:
    payload = json.dumps(
        manifest.to_dict(),
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    return payload.encode("utf-8")


def generation_manifest_sha256(manifest: GenerationManifest) -> str:
    """Return the deterministic identity of one generation evidence object."""

    return hashlib.sha256(_normalized_manifest_bytes(manifest)).hexdigest()


def build_generation_manifest(
    repository: RepositoryIR,
    artifacts: tuple[GeneratedArtifact, ...],
) -> GenerationManifest:
    """Build deterministic integrity evidence from compiler input and output.

    This function is pure. It does not read generated files, infer status from
    the filesystem, persist anything, or make reuse decisions.
    """

    rir_sha256 = repository_ir_sha256(repository)
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


def load_generation_manifest(
    workspace_root: Path,
) -> GenerationManifest | None:
    """Load prior compiler evidence without inferring ownership from files.

    A missing manifest means there is no prior artifact ownership evidence.
    Malformed evidence fails explicitly rather than being silently repaired or
    reconstructed from filesystem shape.
    """

    manifest_path = workspace_root.resolve() / _GENERATION_MANIFEST_PATH
    if not manifest_path.exists():
        return None

    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or set(payload) != {"rir_sha256", "artifacts"}:
        raise ValueError("Generation manifest has an invalid top-level shape.")

    rir_sha256 = payload["rir_sha256"]
    raw_artifacts = payload["artifacts"]
    if not isinstance(rir_sha256, str) or not rir_sha256:
        raise ValueError("Generation manifest has no valid rir_sha256.")
    if not isinstance(raw_artifacts, list):
        raise ValueError("Generation manifest artifacts must be a list.")

    artifacts: list[ManifestArtifact] = []
    seen_paths: set[str] = set()
    for index, raw_artifact in enumerate(raw_artifacts, start=1):
        if not isinstance(raw_artifact, dict) or set(raw_artifact) != {
            "path",
            "node_sha256",
            "artifact_sha256",
        }:
            raise ValueError(
                f"Generation manifest artifact {index} has an invalid shape."
            )

        path = raw_artifact["path"]
        node_sha256 = raw_artifact["node_sha256"]
        artifact_sha256 = raw_artifact["artifact_sha256"]
        if not all(
            isinstance(value, str) and value
            for value in (path, node_sha256, artifact_sha256)
        ):
            raise ValueError(
                f"Generation manifest artifact {index} contains invalid values."
            )
        if path in seen_paths:
            raise ValueError(f"Generation manifest repeats artifact path {path!r}.")

        seen_paths.add(path)
        artifacts.append(
            ManifestArtifact(
                path=path,
                node_sha256=node_sha256,
                artifact_sha256=artifact_sha256,
            )
        )

    return GenerationManifest(
        rir_sha256=rir_sha256,
        artifacts=tuple(artifacts),
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
