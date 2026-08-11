from pyxis.authoring.workspace import create_workspace_spec
from pyxis.rir import build_repository_ir


def test_workspace_spec_lowers_to_minimum_repository_ir() -> None:
    spec = create_workspace_spec(
        "Research Notes",
        "A small Workspace for proving the compiler path.",
    )

    rir = build_repository_ir(spec)

    assert rir.schema_version == "0.1"
    assert rir.repository_id == "research-notes"
    assert rir.workspace.workspace_id == "research_notes"
    assert rir.workspace.entrypoint == "main.py"
    assert rir.workspace.capabilities == (
        "inspect_text",
        "normalize_text",
    )


def test_rir_build_is_deterministic_and_does_not_mutate_authoring_state() -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "Deterministic lowering proof.",
    )
    before = spec.to_canonical_dict()

    first = build_repository_ir(spec)
    second = build_repository_ir(spec)

    assert first == second
    assert first.to_dict() == second.to_dict()
    assert spec.to_canonical_dict() == before


def test_rir_contains_structure_not_generated_implementation() -> None:
    spec = create_workspace_spec(
        "Text Lab",
        "Keep the RIR compiler-facing and implementation-free.",
    )

    payload = build_repository_ir(spec).to_dict()
    serialized = repr(payload)

    assert "def execute" not in serialized
    assert "def run_text" not in serialized
    assert "generated/" not in serialized
