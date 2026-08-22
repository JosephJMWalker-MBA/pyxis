from __future__ import annotations

from dataclasses import dataclass

from .chromium_research_revision_edge_working_set_presentation import (
    ChromiumPageResearchRationaleWorkingSetPresentation,
    present_chromium_research_revision_edge_working_set_context,
)
from .chromium_research_working_set_note_revision_edge_sequence_declaration_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceDeclarationRecord,
)
from .chromium_research_working_set_note_revision_edge_sequence_presentation import (
    ChromiumPageResearchRevisionEdgeSequencePresentation,
    present_chromium_research_working_set_note_revision_edge_sequence_declaration,
)


_PRESENTATION_MODE = "read_only_complete_declared_research_session"


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchSessionPresentation:
    """Complete read-only presentation surface for one loaded declared segment.

    The record only groups already-earned presentation evidence: the exact 27A
    declared rationale segment plus one exact 27C working-set context for every
    declared position in that segment. Grouping these presentations does not add
    chronology, current-head, semantic-support, source-authenticity, citation, file
    discovery, browser acquisition, persistence, mutation, or Workspace provenance
    authority.
    """

    presentation_mode: str
    sequence: ChromiumPageResearchRevisionEdgeSequencePresentation
    working_set_contexts: tuple[
        ChromiumPageResearchRationaleWorkingSetPresentation, ...
    ]


def present_chromium_research_session(
    loaded: ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceDeclarationRecord,
) -> ChromiumPageResearchSessionPresentation:
    """Build one complete presentation bundle from already-loaded 26C evidence.

    This function performs no file or browser reads. It first reuses the complete
    27A sequence-presentation boundary, then reuses the complete 27C selected-context
    boundary once for every declared position. The result is returned only after all
    positions successfully present and reconcile back to the same 27A segment.
    """

    if not isinstance(
        loaded,
        ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceDeclarationRecord,
    ):
        raise TypeError(
            "loaded must be "
            "ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceDeclarationRecord."
        )

    sequence = (
        present_chromium_research_working_set_note_revision_edge_sequence_declaration(
            loaded
        )
    )

    contexts: list[ChromiumPageResearchRationaleWorkingSetPresentation] = []
    for member in sequence.members:
        context = present_chromium_research_revision_edge_working_set_context(
            loaded,
            declared_position=member.declared_position,
        )
        _require_context_matches_sequence_member(
            sequence,
            member_position=member.declared_position,
            context=context,
        )
        contexts.append(context)

    if len(contexts) != len(sequence.members):
        raise ValueError(
            "complete research session context count does not match the declared segment."
        )
    if not contexts:
        raise ValueError("complete research session must contain at least one context.")

    return ChromiumPageResearchSessionPresentation(
        presentation_mode=_PRESENTATION_MODE,
        sequence=sequence,
        working_set_contexts=tuple(contexts),
    )


def _require_context_matches_sequence_member(
    sequence: ChromiumPageResearchRevisionEdgeSequencePresentation,
    *,
    member_position: int,
    context: ChromiumPageResearchRationaleWorkingSetPresentation,
) -> None:
    member = sequence.members[member_position - 1]

    if context.declaration_record_sha256 != sequence.declaration_record_sha256:
        raise ValueError(
            f"research session context {member_position} references a different declaration."
        )
    if context.declared_position != member.declared_position:
        raise ValueError(
            f"research session context {member_position} declared position is incoherent."
        )
    if context.edge_format != member.edge_format:
        raise ValueError(
            f"research session context {member_position} edge format is incoherent."
        )
    if context.edge_record_sha256 != member.edge_record_sha256:
        raise ValueError(
            f"research session context {member_position} edge identity is incoherent."
        )
    if context.rationale_text != member.note_text:
        raise ValueError(
            f"research session context {member_position} rationale text is incoherent."
        )
