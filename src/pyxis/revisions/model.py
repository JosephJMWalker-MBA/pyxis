from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json

from pyxis.authoring.workspace import WorkspaceSpec


REVISION_SCHEMA_VERSION = "0.1"


@dataclass(frozen=True, slots=True)
class RevisionEvent:
    """Immutable provenance for one proposed canonical architecture change.

    Revision events record human intent and canonical state identity only. They
    do not persist canonical state, compile artifacts, or claim compiler
    completion.
    """

    schema_version: str
    revision_id: str
    parent_revision_id: str | None
    operation: str
    rationale: str
    before_canonical_sha256: str
    after_canonical_sha256: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _normalized_json_bytes(payload: dict[str, object]) -> bytes:
    serialized = json.dumps(
        payload,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    return serialized.encode("utf-8")


def canonical_sha256(spec: WorkspaceSpec) -> str:
    """Return the deterministic identity of one canonical Workspace state."""

    return hashlib.sha256(
        _normalized_json_bytes(spec.to_canonical_dict())
    ).hexdigest()


def create_revision_event(
    current_spec: WorkspaceSpec,
    proposed_spec: WorkspaceSpec,
    operation: str,
    rationale: str,
    *,
    parent_revision_id: str | None = None,
) -> RevisionEvent:
    """Create immutable revision provenance without applying the change."""

    clean_operation = operation.strip()
    clean_rationale = rationale.strip()

    if not clean_operation:
        raise ValueError("Revision operation is required.")
    if not clean_rationale:
        raise ValueError("Revision rationale is required.")
    if current_spec.workspace_id != proposed_spec.workspace_id:
        raise ValueError("A revision cannot change Workspace identity.")

    before_sha256 = canonical_sha256(current_spec)
    after_sha256 = canonical_sha256(proposed_spec)
    if before_sha256 == after_sha256:
        raise ValueError("A revision must change canonical Workspace state.")

    identity_payload: dict[str, object] = {
        "schema_version": REVISION_SCHEMA_VERSION,
        "parent_revision_id": parent_revision_id,
        "operation": clean_operation,
        "rationale": clean_rationale,
        "before_canonical_sha256": before_sha256,
        "after_canonical_sha256": after_sha256,
    }
    revision_id = hashlib.sha256(
        _normalized_json_bytes(identity_payload)
    ).hexdigest()

    return RevisionEvent(
        schema_version=REVISION_SCHEMA_VERSION,
        revision_id=revision_id,
        parent_revision_id=parent_revision_id,
        operation=clean_operation,
        rationale=clean_rationale,
        before_canonical_sha256=before_sha256,
        after_canonical_sha256=after_sha256,
    )
