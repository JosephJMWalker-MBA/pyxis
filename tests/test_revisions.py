import json
from pathlib import Path

import pytest

from pyxis.app import preview_remove_normalize_text
from pyxis.authoring import create_workspace_spec
from pyxis.revisions import (
    append_revision_completion,
    append_revision_event,
    canonical_sha256,
    create_revision_completion,
    create_revision_event,
    revision_head_id,
)


def test_revision_event_records_deterministic_intent_without_applying(
    tmp_path: Path,
    monkeypatch,
) -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "Revision provenance model proof.",
    )
    preview = preview_remove_normalize_text(spec)
    monkeypatch.chdir(tmp_path)

    first = create_revision_event(
        spec,
        preview.proposed_spec,
        "remove_capability:normalize_text",
        "  Remove normalization to teach the architectural consequence.  ",
    )
    second = create_revision_event(
        spec,
        preview.proposed_spec,
        "remove_capability:normalize_text",
        "Remove normalization to teach the architectural consequence.",
    )

    assert first == second
    assert first.schema_version == "0.1"
    assert first.parent_revision_id is None
    assert first.rationale == (
        "Remove normalization to teach the architectural consequence."
    )
    assert first.before_canonical_sha256 == canonical_sha256(spec)
    assert first.after_canonical_sha256 == canonical_sha256(preview.proposed_spec)
    assert first.before_canonical_sha256 != first.after_canonical_sha256
    assert len(first.revision_id) == 64
    assert set(first.to_dict()) == {
        "schema_version",
        "revision_id",
        "parent_revision_id",
        "operation",
        "rationale",
        "before_canonical_sha256",
        "after_canonical_sha256",
    }
    assert not tuple(tmp_path.rglob("*"))


def test_revision_event_requires_human_rationale() -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "Required rationale proof.",
    )
    preview = preview_remove_normalize_text(spec)

    with pytest.raises(ValueError, match="rationale"):
        create_revision_event(
            spec,
            preview.proposed_spec,
            "remove_capability:normalize_text",
            "   ",
        )


def test_revision_log_appends_chain_without_rewriting_existing_history(
    tmp_path: Path,
) -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "Append-only revision chain proof.",
    )
    preview = preview_remove_normalize_text(spec)
    first = create_revision_event(
        spec,
        preview.proposed_spec,
        "remove_capability:normalize_text",
        "Remove normalization for the first architectural revision.",
    )

    log_path = append_revision_event(first, tmp_path)
    original_bytes = log_path.read_bytes()

    second = create_revision_event(
        preview.proposed_spec,
        spec,
        "restore_capability:normalize_text",
        "Restore normalization through a new forward revision.",
        parent_revision_id=first.revision_id,
    )
    append_revision_event(second, tmp_path)

    appended_bytes = log_path.read_bytes()
    assert log_path == tmp_path.resolve() / "revisions/events.jsonl"
    assert appended_bytes.startswith(original_bytes)
    assert appended_bytes != original_bytes

    entries = [
        json.loads(line)
        for line in log_path.read_text(encoding="utf-8").splitlines()
    ]
    assert entries == [first.to_dict(), second.to_dict()]
    assert entries[1]["parent_revision_id"] == entries[0]["revision_id"]


def test_revision_head_reader_is_non_mutating(tmp_path: Path) -> None:
    assert revision_head_id(tmp_path) is None
    assert not tuple(tmp_path.rglob("*"))

    spec = create_workspace_spec(
        "Text Lab",
        "Revision head read proof.",
    )
    preview = preview_remove_normalize_text(spec)
    event = create_revision_event(
        spec,
        preview.proposed_spec,
        "remove_capability:normalize_text",
        "Create one revision so the head can be read.",
    )
    log_path = append_revision_event(event, tmp_path)
    before = log_path.read_bytes()

    assert revision_head_id(tmp_path) == event.revision_id
    assert log_path.read_bytes() == before


def test_revision_log_rejects_stale_parent_without_mutation(tmp_path: Path) -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "Revision chain guard proof.",
    )
    preview = preview_remove_normalize_text(spec)
    first = create_revision_event(
        spec,
        preview.proposed_spec,
        "remove_capability:normalize_text",
        "Create the first revision event.",
    )
    log_path = append_revision_event(first, tmp_path)
    before = log_path.read_bytes()

    stale = create_revision_event(
        preview.proposed_spec,
        spec,
        "restore_capability:normalize_text",
        "This event deliberately has the wrong parent.",
    )

    with pytest.raises(ValueError, match="chain head"):
        append_revision_event(stale, tmp_path)

    assert log_path.read_bytes() == before


def test_revision_completion_is_separate_deterministic_evidence() -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "Revision completion model proof.",
    )
    preview = preview_remove_normalize_text(spec)
    revision = create_revision_event(
        spec,
        preview.proposed_spec,
        "remove_capability:normalize_text",
        "Record intent before compiler completion exists.",
    )

    completion = create_revision_completion(
        revision,
        after_canonical_sha256=revision.after_canonical_sha256,
        rir_sha256="rir-hash",
        generation_manifest_sha256="manifest-hash",
    )

    assert completion.revision_id == revision.revision_id
    assert completion.after_canonical_sha256 == revision.after_canonical_sha256
    assert completion.rir_sha256 == "rir-hash"
    assert completion.generation_manifest_sha256 == "manifest-hash"
    assert set(completion.to_dict()) == {
        "schema_version",
        "revision_id",
        "after_canonical_sha256",
        "rir_sha256",
        "generation_manifest_sha256",
    }


def test_revision_completion_log_requires_event_and_rejects_duplicate(
    tmp_path: Path,
) -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "Revision completion persistence proof.",
    )
    preview = preview_remove_normalize_text(spec)
    revision = create_revision_event(
        spec,
        preview.proposed_spec,
        "remove_capability:normalize_text",
        "Create intent before completion evidence.",
    )
    completion = create_revision_completion(
        revision,
        after_canonical_sha256=revision.after_canonical_sha256,
        rir_sha256="rir-hash",
        generation_manifest_sha256="manifest-hash",
    )

    with pytest.raises(ValueError, match="unknown revision"):
        append_revision_completion(completion, tmp_path)
    assert not (tmp_path / "revisions/completions.jsonl").exists()

    append_revision_event(revision, tmp_path)
    completion_path = append_revision_completion(completion, tmp_path)
    before = completion_path.read_bytes()

    assert completion_path == tmp_path.resolve() / "revisions/completions.jsonl"
    assert [
        json.loads(line)
        for line in completion_path.read_text(encoding="utf-8").splitlines()
    ] == [completion.to_dict()]

    with pytest.raises(ValueError, match="already has completion evidence"):
        append_revision_completion(completion, tmp_path)
    assert completion_path.read_bytes() == before
