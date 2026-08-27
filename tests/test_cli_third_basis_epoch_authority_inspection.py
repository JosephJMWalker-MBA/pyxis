from __future__ import annotations

import pytest

import pyxis.cli as cli


def test_current_third_epoch_cli_factories_route_through_inspection_adapters() -> None:
    factories = (
        cli._load_third_basis_epoch_research_shell_factory(),
        cli._load_third_basis_epoch_continuation_research_shell_factory(),
        cli._load_third_basis_epoch_continuation_handoff_research_shell_factory(),
    )

    assert [factory.__module__ for factory in factories] == [
        "pyxis.ui.third_basis_epoch_authority_inspection_shell",
        "pyxis.ui.third_basis_epoch_authority_inspection_shell",
        "pyxis.ui.third_basis_epoch_authority_inspection_shell",
    ]
    assert [factory.__name__ for factory in factories] == [
        "create_inspectable_third_basis_epoch_cumulative_handoff_research_session_shell",
        "create_inspectable_third_basis_epoch_continuation_research_session_shell",
        "create_inspectable_third_basis_epoch_continuation_handoff_research_session_shell",
    ]


def test_42a_does_not_expand_research_inspect_to_third_epoch(capsys) -> None:
    with pytest.raises(SystemExit) as exc_info:
        cli.main(["research-inspect", "--help"])

    assert exc_info.value.code == 0
    output = capsys.readouterr().out
    assert "--second-basis-epoch-overlay" in output
    assert "--second-basis-epoch-continuation-overlay" in output
    assert "--third-basis-epoch-overlay" not in output
    assert "--third-basis-epoch-continuation-overlay" not in output
