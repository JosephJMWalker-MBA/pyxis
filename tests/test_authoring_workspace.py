import pytest

from pyxis.authoring import WorkspaceSpec, create_workspace_spec


def test_create_workspace_spec_from_minimum_first_run_inputs() -> None:
    spec = create_workspace_spec(
        "Research Notes",
        "A small Workspace for testing the Pyxis compiler path.",
    )

    assert spec == WorkspaceSpec(
        workspace_id="research_notes",
        name="Research Notes",
        description="A small Workspace for testing the Pyxis compiler path.",
    )
    assert spec.to_canonical_dict() == {
        "workspace_id": "research_notes",
        "name": "Research Notes",
        "description": "A small Workspace for testing the Pyxis compiler path.",
        "capabilities": ("inspect_text", "normalize_text"),
    }


def test_workspace_spec_can_propose_capability_restoration_without_mutation() -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "Immutable capability restoration proof.",
    )
    inspect_only = spec.without_capability("normalize_text")
    before = inspect_only.to_canonical_dict()

    restored = inspect_only.with_capability("normalize_text")

    assert inspect_only.to_canonical_dict() == before
    assert restored is not inspect_only
    assert restored.capabilities == ("inspect_text", "normalize_text")
    assert restored == spec

    with pytest.raises(ValueError, match="already contains"):
        restored.with_capability("normalize_text")


def test_workspace_spec_rejects_missing_human_intent() -> None:
    with pytest.raises(ValueError, match="Workspace name is required"):
        create_workspace_spec("   ", "Useful description")

    with pytest.raises(ValueError, match="Workspace description is required"):
        create_workspace_spec("Text Lab", "   ")
