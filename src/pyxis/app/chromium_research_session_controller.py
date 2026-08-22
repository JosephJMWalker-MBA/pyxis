from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .chromium_research_session_presentation import (
    ChromiumPageResearchSessionPresentation,
    present_chromium_research_session,
)
from .chromium_research_working_set_note_revision_edge_extension import (
    ChromiumPageResearchWorkingSetNoteRevisionEdgeExtensionRecord,
    create_chromium_research_working_set_note_revision_edge_extension,
)
from .chromium_research_working_set_note_revision_edge_extension_persistence import (
    ChromiumPageResearchWorkingSetNoteRevisionEdgeExtensionPersistenceEvidence,
    persist_chromium_research_working_set_note_revision_edge_extension,
)
from .chromium_research_working_set_note_revision_edge_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord,
)
from .chromium_research_working_set_note_revision_edge_sequence_declaration_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceDeclarationRecord,
)


@dataclass(frozen=True, slots=True)
class ChromiumResearchSessionEndpointRevisionPersistenceResult:
    """One explicit durable successor written from one declared session endpoint.

    `prior_session` is the exact complete read-only presentation retained by the
    controller before and after this operation. `extension` is the exact 25A human
    extension from the declared endpoint, and `persistence` is the exact 25B durable
    write evidence for that extension.

    The result does not assert that the newly persisted edge is latest, current,
    adopted by the durable declaration, part of a complete history, or semantically
    better than its predecessor.
    """

    prior_session: ChromiumPageResearchSessionPresentation
    extension: ChromiumPageResearchWorkingSetNoteRevisionEdgeExtensionRecord
    persistence: ChromiumPageResearchWorkingSetNoteRevisionEdgeExtensionPersistenceEvidence


class ChromiumResearchSessionController:
    """Application-owned interaction state for one loaded declared research session.

    The controller retains one already-loaded coherent 26C declaration/sequence
    record and its exact 28A complete presentation. Its first mutation operation is
    intentionally narrow: persist one explicit human revision from the *declared
    sequence endpoint* using the already-proven 25A -> 25B path.

    Persisting a successor does not mutate or replace the loaded declaration, does
    not extend its declared sequence, and does not promote the new edge to current or
    head status. A later explicit relinking/adoption boundary would be required for
    any such state transition.
    """

    def __init__(
        self,
        loaded: ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceDeclarationRecord,
    ) -> None:
        if not isinstance(
            loaded,
            ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceDeclarationRecord,
        ):
            raise TypeError(
                "loaded must be "
                "ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceDeclarationRecord."
            )

        presentation = present_chromium_research_session(loaded)
        if not loaded.sequence.edges:
            raise ValueError(
                "Declared research session must contain at least one revision edge."
            )

        self._loaded = loaded
        self._presentation = presentation
        self._last_endpoint_revision: (
            ChromiumResearchSessionEndpointRevisionPersistenceResult | None
        ) = None

    @property
    def loaded(
        self,
    ) -> ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceDeclarationRecord:
        """Return the exact loaded 26C evidence retained for this session."""

        return self._loaded

    @property
    def presentation(self) -> ChromiumPageResearchSessionPresentation:
        """Return the exact complete 28A presentation retained for this session."""

        return self._presentation

    @property
    def declared_endpoint(self) -> ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord:
        """Return the exact final edge in the caller-declared, verified segment.

        "Endpoint" here means only the final member of this explicit declared
        sequence. It does not mean latest revision, global head, canonical current
        state, or unique successor position.
        """

        return self._loaded.sequence.edges[-1]

    @property
    def last_endpoint_revision(
        self,
    ) -> ChromiumResearchSessionEndpointRevisionPersistenceResult | None:
        """Return the last successful durable endpoint-revision write, if any."""

        return self._last_endpoint_revision

    def persist_declared_endpoint_revision(
        self,
        revised_note_text: str,
        *,
        prior_edge_source: Path,
        destination: Path,
    ) -> ChromiumResearchSessionEndpointRevisionPersistenceResult:
        """Persist one explicit human successor from the declared session endpoint.

        The caller explicitly supplies both the durable file for the exact declared
        endpoint and a no-overwrite destination for the new successor. The operation
        delegates human exact-text revision semantics to public 25A and durable
        predecessor reopening/write semantics to public 25B.

        On success the controller records the write result but deliberately retains
        the same loaded declaration and the same 28A presentation. No declaration
        rewrite, automatic relinking, digest search, directory scan, head selection,
        chronology inference, branch interpretation, or semantic judgment occurs.
        """

        extension = create_chromium_research_working_set_note_revision_edge_extension(
            self.declared_endpoint,
            revised_note_text=revised_note_text,
        )
        persistence = persist_chromium_research_working_set_note_revision_edge_extension(
            extension,
            prior_edge_source,
            destination,
        )
        result = ChromiumResearchSessionEndpointRevisionPersistenceResult(
            prior_session=self._presentation,
            extension=extension,
            persistence=persistence,
        )
        self._last_endpoint_revision = result
        return result
