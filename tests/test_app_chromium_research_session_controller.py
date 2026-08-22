from __future__ import annotations

from dataclasses import fields, replace
import importlib
from pathlib import Path

import pytest

from pyxis.app.chromium_research_session_controller import (
    ChromiumResearchSessionController,
    ChromiumResearchSessionEndpointRevisionPersistenceResult,
)
from pyxis.app.chromium_research_session_presentation import (
    present_chromium_research_session,
)
from pyxis.app.chromium_research_working_set_note_revision_edge_load import (
    load_chromium_research_working_set_note_revision_edge,
)
from test_app_chromium_research_session_presentation import _loaded


def _session(tmp_path: Path):
    return _loaded(tmp_path)


def test_controller_retains_exact_loaded_evidence_and_complete_presentation(
    tmp_path: Path,
) -> None:
    _, _, _, _, _, loaded = _session(tmp_path)

    controller = ChromiumResearchSessionController(loaded)

    assert controller.loaded is loaded
    assert controller.presentation == present_chromium_research_session(loaded)
    assert controller.last_endpoint_revision is None


def test_declared_endpoint_is_exact_final_edge_not_global_head(tmp_path: Path) -> None:
    _, _, _, _, _, loaded = _session(tmp_path)
    controller = ChromiumResearchSessionController(loaded)

    assert controller.declared_endpoint is loaded.sequence.edges[-1]
    assert controller.declared_endpoint is not loaded.sequence.edges[0]


def test_persist_declared_endpoint_revision_reuses_25a_25b_and_preserves_exact_text(
    tmp_path: Path,
) -> None:
    _, _, _, _, v6_path, loaded = (*_session(tmp_path)[:3], *_session(tmp_path)[3:])
