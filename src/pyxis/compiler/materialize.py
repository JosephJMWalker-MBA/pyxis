from __future__ import annotations

from pathlib import Path

from .artifacts import GeneratedArtifact


def materialize_artifacts(
    artifacts: tuple[GeneratedArtifact, ...],
    destination_root: Path,
) -> tuple[Path, ...]:
    """Write an already-compiled artifact set beneath one destination root.

    This function does not compile, interpret, or execute generated code. It
    materializes the artifact paths and source exactly as provided by the
    compiler result.
    """

    root = destination_root.resolve()
    written: list[Path] = []

    for artifact in artifacts:
        relative = Path(artifact.path)
        if relative.is_absolute() or ".." in relative.parts:
            raise ValueError(
                f"Artifact path must remain relative to the destination: {artifact.path!r}."
            )

        target = (root / relative).resolve()
        if target != root and root not in target.parents:
            raise ValueError(
                f"Artifact path escapes the destination: {artifact.path!r}."
            )

        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(artifact.source, encoding="utf-8")
        written.append(target)

    return tuple(written)
