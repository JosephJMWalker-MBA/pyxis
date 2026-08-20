from __future__ import annotations

from dataclasses import dataclass

from .chromium_research_paragraph_text_selection_note_load import (
    ChromiumPageResearchLoadedParagraphTextSelectionNoteRecord,
)
from .chromium_research_paragraph_text_selection_comparison_note_load import (
    ChromiumPageResearchLoadedParagraphTextSelectionComparisonNoteRecord,
)
from .chromium_research_selection_note_load import (
    ChromiumPageResearchLoadedParagraphNoteRecord,
)
from .chromium_research_working_set import create_chromium_research_working_set
from .chromium_research_working_set_note_revision_edge_sequence_declaration_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceDeclarationRecord,
)
from .chromium_research_working_set_note_revision_edge_sequence_presentation import (
    present_chromium_research_working_set_note_revision_edge_sequence_declaration,
)


_PRESENTATION_MODE = "read_only_declared_rationale_working_set_context"
_WORKING_SET_MODE = "caller_explicit_ordered_relinked_research_working_set"
_EDGE_FORMAT = "pyxis.chromium.research_working_set_note_revision_edge.v1"


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchSourceExcerptPresentation:
    """Bounded source text retained by one working-set member.

    `text` is either one already-returned paragraph prefix or one exact text range
    inside such a prefix. It is not promoted to a verified quotation, citation,
    complete paragraph, source-authenticity claim, or support claim.
    """

    excerpt_role: str
    source_capture_format: str
    source_bundle_sha256: str
    url: str
    paragraph_ordinal: int
    excerpt_kind: str
    text: str
    paragraph_text_truncated: bool
    offset_unit: str | None
    start_offset: int | None
    end_offset: int | None


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchWorkingSetMemberPresentation:
    """Read-only context for one exact human-owned working-set member."""

    member_position: int
    member_kind: str
    human_note_text: str
    excerpts: tuple[ChromiumPageResearchSourceExcerptPresentation, ...]


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchRationaleWorkingSetPresentation:
    """Read-only working-set context for one declared rationale revision.

    The record proves only that the selected rationale revision is attached to the
    exact retained human working set represented here. It does not claim that any
    source excerpt supports, proves, contradicts, or otherwise semantically bears
    on the rationale or on any member note.
    """

    presentation_mode: str
    declaration_record_sha256: str
    declared_position: int
    edge_format: str
    edge_record_sha256: str
    rationale_text: str
    working_set_mode: str
    members: tuple[ChromiumPageResearchWorkingSetMemberPresentation, ...]


def present_chromium_research_revision_edge_working_set_context(
    loaded: ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceDeclarationRecord,
    *,
    declared_position: int,
) -> ChromiumPageResearchRationaleWorkingSetPresentation:
    """Present bounded evidence context for one explicit declared rationale position.

    This function starts from already-loaded 26C evidence. It performs no file or
    browser reads. The existing 27A presentation boundary first re-establishes the
    declaration/sequence relationship. The chosen edge's working set is then
    revalidated through the existing public 20A constructor before source excerpts
    and human member notes are projected into small immutable presentation records.
    """

    if not isinstance(
        loaded,
        ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceDeclarationRecord,
    ):
        raise TypeError(
            "loaded must be "
            "ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceDeclarationRecord."
        )
    if type(declared_position) is not int:
        raise TypeError("declared_position must be an integer.")

    segment = present_chromium_research_working_set_note_revision_edge_sequence_declaration(
        loaded
    )
    if declared_position < 1 or declared_position > len(segment.members):
        raise ValueError("declared_position is outside the verified declared segment.")

    segment_member = segment.members[declared_position - 1]
    edge = loaded.sequence.edges[declared_position - 1]
    if edge.verification.edge_format != _EDGE_FORMAT:
        raise ValueError("selected loaded edge format is unsupported for working-set presentation.")
    if edge.verification.edge_record_sha256 != segment_member.edge_record_sha256:
        raise ValueError("selected loaded edge identity is incoherent with the declared segment.")
    if edge.revision.revised_note.note_text != segment_member.note_text:
        raise ValueError("selected loaded rationale text is incoherent with the declared segment.")

    working_set = edge.revision.revised_note.working_set
    if working_set.working_set_mode != _WORKING_SET_MODE:
        raise ValueError("selected rationale retains an unsupported working-set mode.")

    rebuilt = create_chromium_research_working_set(working_set.items)
    if rebuilt.working_set_mode != working_set.working_set_mode:
        raise ValueError("selected rationale working-set mode is incoherent.")
    if len(rebuilt.items) != len(working_set.items) or any(
        observed is not retained
        for observed, retained in zip(rebuilt.items, working_set.items)
    ):
        raise ValueError("selected rationale working-set membership is incoherent.")

    members = tuple(
        _present_working_set_member(item, position=index)
        for index, item in enumerate(working_set.items, start=1)
    )
    if not members:
        raise ValueError("selected rationale working set must contain at least one member.")

    return ChromiumPageResearchRationaleWorkingSetPresentation(
        presentation_mode=_PRESENTATION_MODE,
        declaration_record_sha256=segment.declaration_record_sha256,
        declared_position=declared_position,
        edge_format=segment_member.edge_format,
        edge_record_sha256=segment_member.edge_record_sha256,
        rationale_text=segment_member.note_text,
        working_set_mode=working_set.working_set_mode,
        members=members,
    )


def _present_working_set_member(item: object, *, position: int) -> ChromiumPageResearchWorkingSetMemberPresentation:
    if isinstance(item, ChromiumPageResearchLoadedParagraphNoteRecord):
        selection = item.note.selection
        return ChromiumPageResearchWorkingSetMemberPresentation(
            member_position=position,
            member_kind="paragraph_note",
            human_note_text=item.note.note_text,
            excerpts=(
                _paragraph_excerpt(selection, role="paragraph"),
            ),
        )

    if isinstance(item, ChromiumPageResearchLoadedParagraphTextSelectionNoteRecord):
        selection = item.note.selection
        return ChromiumPageResearchWorkingSetMemberPresentation(
            member_position=position,
            member_kind="exact_range_note",
            human_note_text=item.note.note_text,
            excerpts=(
                _range_excerpt(selection, role="selection"),
            ),
        )

    if isinstance(
        item,
        ChromiumPageResearchLoadedParagraphTextSelectionComparisonNoteRecord,
    ):
        comparison = item.note.comparison
        return ChromiumPageResearchWorkingSetMemberPresentation(
            member_position=position,
            member_kind="comparison_note",
            human_note_text=item.note.note_text,
            excerpts=(
                _range_excerpt(comparison.first_selection, role="first_selection"),
                _range_excerpt(comparison.second_selection, role="second_selection"),
            ),
        )

    raise TypeError(f"working-set member {position} has an unsupported loaded record type.")


def _paragraph_excerpt(selection: object, *, role: str) -> ChromiumPageResearchSourceExcerptPresentation:
    paragraph = selection.paragraph
    source = selection.source
    return ChromiumPageResearchSourceExcerptPresentation(
        excerpt_role=role,
        source_capture_format=source.verification.capture_format,
        source_bundle_sha256=source.verification.bundle_sha256,
        url=source.bundle.url,
        paragraph_ordinal=paragraph.ordinal,
        excerpt_kind="returned_paragraph_prefix",
        text=paragraph.text_prefix,
        paragraph_text_truncated=paragraph.truncated,
        offset_unit=None,
        start_offset=None,
        end_offset=None,
    )


def _range_excerpt(selection: object, *, role: str) -> ChromiumPageResearchSourceExcerptPresentation:
    paragraph_selection = selection.source
    paragraph = paragraph_selection.paragraph
    source = paragraph_selection.source
    return ChromiumPageResearchSourceExcerptPresentation(
        excerpt_role=role,
        source_capture_format=source.verification.capture_format,
        source_bundle_sha256=source.verification.bundle_sha256,
        url=source.bundle.url,
        paragraph_ordinal=paragraph.ordinal,
        excerpt_kind="exact_returned_text_range",
        text=selection.selected_text,
        paragraph_text_truncated=paragraph.truncated,
        offset_unit=selection.offset_unit,
        start_offset=selection.start_offset,
        end_offset=selection.end_offset,
    )
