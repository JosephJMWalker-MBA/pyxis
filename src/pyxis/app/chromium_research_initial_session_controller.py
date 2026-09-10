from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .chromium_research_initial_session_presentation import (
    ChromiumPageResearchInitialSessionPresentation,
    present_chromium_research_initial_session,
)
from .chromium_research_working_set_note_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRecord,
)
from .chromium_research_working_set_note_revision import (
    ChromiumPageResearchWorkingSetNoteRevisionRecord,
    create_chromium_research_working_set_note_revision,
)
from .chromium_research_working_set_note_revision_persistence import (
    ChromiumPageResearchWorkingSetNoteRevisionPersistenceEvidence,
    persist_chromium_research_working_set_note_revision,
    persist_chromium_research_working_set_note_revision_v2,
)


_NOTE_FORMAT_V1 = "pyxis.chromium.research_working_set_note.v1"
_NOTE_FORMAT_V2 = "pyxis.chromium.research_working_set_note.v2"


@dataclass(frozen=True, slots=True)
class ChromiumResearchInitialSessionFirstRevisionPersistenceResult:
    """One explicit successor write from an immutable initial-session rationale root."""

    prior_session: ChromiumPageResearchInitialSessionPresentation
    revision: ChromiumPageResearchWorkingSetNoteRevisionRecord
    persistence: ChromiumPageResearchWorkingSetNoteRevisionPersistenceEvidence


class ChromiumResearchInitialSessionController:
    """Application-owned state for one loaded working-set-note session root.

    The mounted root remains unchanged after a successor write. Persisting a first
    revision does not adopt it as current/head, create a continuation or edge,
    declare a sequence, or transition into the ordinary declared-session controller.
    """

    def __init__(
        self,
        loaded: ChromiumPageResearchLoadedWorkingSetNoteRecord,
    ) -> None:
        if not isinstance(loaded, ChromiumPageResearchLoadedWorkingSetNoteRecord):
            raise TypeError(
                "loaded must be ChromiumPageResearchLoadedWorkingSetNoteRecord."
            )
        presentation = present_chromium_research_initial_session(loaded)
        self._loaded = loaded
        self._presentation = presentation
        self._last_revision: (
            ChromiumResearchInitialSessionFirstRevisionPersistenceResult | None
        ) = None

    @property
    def loaded(self) -> ChromiumPageResearchLoadedWorkingSetNoteRecord:
        """Return the exact public-21C record mounted as this session root."""

        return self._loaded

    @property
    def presentation(self) -> ChromiumPageResearchInitialSessionPresentation:
        """Return the immutable read-only initial-session presentation."""

        return self._presentation

    @property
    def last_revision(
        self,
    ) -> ChromiumResearchInitialSessionFirstRevisionPersistenceResult | None:
        """Return the last successful first-root successor write, if any."""

        return self._last_revision

    def persist_first_revision(
        self,
        revised_note_text: str,
        *,
        working_set_source: Path,
        prior_note_source: Path,
        destination: Path,
    ) -> ChromiumResearchInitialSessionFirstRevisionPersistenceResult:
        """Persist one genuine human wording change from the exact mounted root.

        The operation delegates revision semantics to public 22A and durable
        predecessor reopening/write semantics to the matching existing 22B writer.
        All durable locations remain caller-explicit.
        """

        revision = create_chromium_research_working_set_note_revision(
            self._loaded.note,
            revised_note_text=revised_note_text,
        )

        note_format = self._loaded.verification.note_format
        if note_format == _NOTE_FORMAT_V1:
            persistence = persist_chromium_research_working_set_note_revision(
                revision,
                working_set_source,
                prior_note_source,
                destination,
            )
        elif note_format == _NOTE_FORMAT_V2:
            persistence = persist_chromium_research_working_set_note_revision_v2(
                revision,
                working_set_source,
                prior_note_source,
                destination,
            )
        else:
            raise ValueError(
                "loaded initial-session note format is unsupported for first revision."
            )

        result = ChromiumResearchInitialSessionFirstRevisionPersistenceResult(
            prior_session=self._presentation,
            revision=revision,
            persistence=persistence,
        )
        self._last_revision = result
        return result
