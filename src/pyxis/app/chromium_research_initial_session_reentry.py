from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .chromium_research_capture_load import (
    ChromiumPageResearchLoadedCaptureEvidence,
    load_chromium_page_research_capture,
)
from .chromium_research_initial_session_controller import (
    ChromiumResearchInitialSessionController,
)
from .chromium_research_paragraph_text_selection_load import (
    ChromiumPageResearchLoadedParagraphTextSelectionRecord,
    load_chromium_research_paragraph_text_selection,
)
from .chromium_research_working_set_note_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRecord,
    load_chromium_research_working_set_note,
)


@dataclass(frozen=True, slots=True)
class ChromiumResearchInitialSessionReentryResult:
    """Freshly reconstructed initial-session application state from explicit paths.

    Every retained object was re-earned in this call from caller-explicit durable
    locations. The result is application reconstruction state only; it is not a
    durable locator registry, evidence artifact, chronology record, source-truth
    claim, or current/latest/head authority.
    """

    loaded_capture: ChromiumPageResearchLoadedCaptureEvidence
    loaded_selection: ChromiumPageResearchLoadedParagraphTextSelectionRecord
    loaded_root: ChromiumPageResearchLoadedWorkingSetNoteRecord
    controller: ChromiumResearchInitialSessionController


def reenter_chromium_research_initial_session(
    *,
    capture_source: Path,
    selection_source: Path,
    working_set_source: Path,
    note_source: Path,
) -> ChromiumResearchInitialSessionReentryResult:
    """Freshly mount one initial governed session from four explicit locations.

    The operation is deliberately read-only and performs no path discovery, digest
    search, browser acquisition, latest/current/head inference, or persistence.
    Location only tells Pyxis where the caller wants it to look. Existing public
    16C, 49B, and 21C boundaries independently re-establish content and attachment
    coherence before the existing 51C controller is constructed.
    """

    _require_path(capture_source, "capture_source")
    _require_path(selection_source, "selection_source")
    _require_path(working_set_source, "working_set_source")
    _require_path(note_source, "note_source")

    loaded_capture = load_chromium_page_research_capture(capture_source)
    loaded_selection = load_chromium_research_paragraph_text_selection(
        loaded_capture,
        selection_source,
    )
    loaded_root = load_chromium_research_working_set_note(
        (loaded_selection,),
        working_set_source,
        note_source,
    )
    controller = ChromiumResearchInitialSessionController(loaded_root)

    return ChromiumResearchInitialSessionReentryResult(
        loaded_capture=loaded_capture,
        loaded_selection=loaded_selection,
        loaded_root=loaded_root,
        controller=controller,
    )


def _require_path(value: Path, label: str) -> Path:
    if not isinstance(value, Path):
        raise TypeError(f"{label} must be pathlib.Path.")
    return value


__all__ = [
    "ChromiumResearchInitialSessionReentryResult",
    "reenter_chromium_research_initial_session",
]
