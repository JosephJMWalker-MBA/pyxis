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


def test_workspace_spec_rejects_missing_human_intent() -> None:
    with pytest.raises(ValueError, match="Workspace name is required"):
        create_workspace_spec("   ", "Useful description")

    with pytest.raises(ValueError, match="Workspace description is required"):
        create_workspace_spec("Text Lab", "   ")
