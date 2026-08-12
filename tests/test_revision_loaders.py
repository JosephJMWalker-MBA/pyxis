import json
from pathlib import Path

import pytest

from pyxis.app import preview_remove_normalize_text
from pyxis.authoring import create_workspace_spec
from pyxis.revisions import (
    append_revision_completion,
    append_revision_event,
    create_revision_completion,
    create_revision_event,
    load_revision_completions,
    load_revision_events,
)


def test_revision_history_loaders_round_trip_without_mutation(tmp_path: Path) -> None:
    assert load_revision_events(tmp_path) == ()
    assert load_revision_completions(tmp_path) == ()
    assert not tuple(tmp_path.rglob("*"))

    spec = create_workspace_spec("Text Lab", "Typed revision loader proof.")
    preview = preview_remove_normalize_text(spec)
    event = create_revision_event(
        spec,
        preview.proposed_spec,
        "remove_capability:normalize_text",
        "Persist one revision for typed loading.",
    )
    completion = create_revision_completion(
        event,
        after_canonical_sha256=event.after_canonical_sha256,
        rir_sha256="rir-hash",
        generation_manifest_sha256="manifest-hash",
    )

    event_path = append_revision_event(event, tmp_path)
    completion_path = append_revision_completion(completion, tmp_path)
    event_bytes = event_path.read_bytes()
    completion_bytes = completion_path.read_bytes()

    assert load_revision_events(tmp_path) == (event,)
    assert load_revision_completions(tmp_path) == (completion,)
    assert event_path.read_bytes() == event_bytes
    assert completion_path.read_bytes() == completion_bytes


def test_revision_completion_loader_rejects_unknown_persisted_revision(
    tmp_path: Path,
) -> None:
    completion_path = tmp_path / "revisions/completions.jsonl"
    completion_path.parent.mkdir(parents=True)
    completion_path.write_text(
        json.dumps(
            {
                "schema_version": "0.1",
                "revision_id": "unknown-revision",
                "after_canonical_sha256": "canonical-hash",
                "rir_sha256": "rir-hash",
                "generation_manifest_sha256": "manifest-hash",
            },
            separators=(",", ":"),
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    before = completion_path.read_bytes()
    with pytest.raises(ValueError, match="unknown revision"):
        load_revision_completions(tmp_path)
    assert completion_path.read_bytes() == before
