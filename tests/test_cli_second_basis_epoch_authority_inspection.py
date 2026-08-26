from __future__ import annotations

from pathlib import Path

import pyxis.cli as cli
from pyxis.app.chromium_research_second_basis_epoch_shell_lineage import (
    prove_chromium_research_second_basis_epoch_continuation_shell_lineage,
)
from test_app_chromium_research_second_basis_epoch_continuation_reentry_plan_document import (
    _persist_valid_continuation,
)


def test_persisted_second_epoch_continuation_runner_uses_inspection_adapter(
    tmp_path: Path,
    monkeypatch,
) -> None:
    import pyxis.ui.second_basis_epoch_authority_inspection_shell as shell_module

    values = _persist_valid_continuation(tmp_path, stem="39a-cli-persisted")
    overlay = values[6]
    earned = values[8].fresh_reentry
    lineage = prove_chromium_research_second_basis_epoch_continuation_shell_lineage(
        earned,
        overlay_source=overlay,
    )
    observed: dict[str, object] = {}

    class FakeShell:
        def run(self):
            observed["ran"] = True
            return None

    def fake_factory(supplied):
        observed["lineage"] = supplied
        return FakeShell()

    monkeypatch.setattr(
        shell_module,
        "create_inspectable_second_basis_epoch_continuation_research_session_shell",
        fake_factory,
    )

    cli._run_second_basis_epoch_continuation_research_session_shell(lineage)

    assert observed["lineage"] is lineage
    assert observed["ran"] is True
