from __future__ import annotations

from dataclasses import dataclass
import hmac

from .chromium_research_working_set_note_revision_edge_sequence_declaration_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceDeclarationRecord,
)
from .chromium_research_working_set_note_revision_edge_sequence_persistence import (
    ChromiumPageResearchWorkingSetNoteRevisionEdgeSequenceReference,
    _validate_live_sequence,
)


_PRESENTATION_MODE = (
    "read_only_verified_declared_research_working_set_note_revision_edge_sequence"
)
_SEQUENCE_FORMAT = (
    "pyxis.chromium.research_working_set_note_revision_edge_sequence.v1"
)
_SEQUENCE_MODE = (
    "caller_explicit_ordered_relinked_research_working_set_note_revision_edge_sequence"
)
_EDGE_FORMAT = "pyxis.chromium.research_working_set_note_revision_edge.v1"


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchRevisionEdgeSequenceMemberPresentation:
    """Read-only presentation of one member in a verified declared edge segment.

    `declared_position` is the one-based position in the human-declared sequence.
    It is not a global revision number, timestamp ordering, rank, or current-head
    claim. `note_text` is the exact human-authored revised-note wording retained by
    the freshly relinked edge; presenting it does not make it source evidence or a
    machine semantic judgment.
    """

    declared_position: int
    edge_format: str
    edge_record_sha256: str
    note_text: str


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchRevisionEdgeSequencePresentation:
    """Small read-only presentation contract for one verified 26C declaration.

    This record exposes only the durable declaration identity, explicit starting
    content identity, and ordered edge member identities plus exact human-authored
    revised-note text already retained by the loaded application evidence.

    It performs no file reads, browser acquisition, mutation, persistence, path
    discovery, chronology inference, current-head selection, branch interpretation,
    source validation, semantic comparison, or LLM analysis.
    """

    presentation_mode: str
    declaration_format: str
    declaration_record_sha256: str
    sequence_mode: str
    starting_record_format: str
    starting_record_sha256: str
    members: tuple[ChromiumPageResearchRevisionEdgeSequenceMemberPresentation, ...]


def present_chromium_research_working_set_note_revision_edge_sequence_declaration(
    loaded: ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceDeclarationRecord,
) -> ChromiumPageResearchRevisionEdgeSequencePresentation:
    """Present one already-loaded verified declared edge segment without file I/O.

    The function does not trust the outer 26C dataclass by type alone. It
    re-establishes the retained in-memory 26A sequence through the same bounded
    local-coherence and retained-self-integrity checks used by 26B persistence,
    then requires those observed identities to match the retained 26B declaration
    verification position by position.

    This is presentation validation only. It does not freshly verify any file and
    deliberately does not audit ancestry beneath the loaded starting predecessor.
    """

    if not isinstance(
        loaded,
        ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceDeclarationRecord,
    ):
        raise TypeError(
            "loaded must be "
            "ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceDeclarationRecord."
        )

    verification = loaded.verification
    sequence = loaded.sequence

    if verification.sequence_format != _SEQUENCE_FORMAT:
        raise ValueError("loaded declaration format is unsupported for presentation.")
    if verification.sequence_mode != _SEQUENCE_MODE:
        raise ValueError("loaded declaration mode is unsupported for presentation.")
    if sequence.sequence_mode != verification.sequence_mode:
        raise ValueError("loaded sequence mode does not match its retained declaration.")

    observed_start, observed_edges = _validate_live_sequence(sequence)
    _require_reference_match(
        observed_start,
        verification.starting_predecessor,
        label="starting predecessor",
    )

    if len(observed_edges) != len(verification.edges):
        raise ValueError(
            "loaded sequence member count does not match its retained declaration."
        )

    members: list[ChromiumPageResearchRevisionEdgeSequenceMemberPresentation] = []
    for index, (edge, observed_reference, declared_reference) in enumerate(
        zip(sequence.edges, observed_edges, verification.edges),
        start=1,
    ):
        _require_reference_match(
            observed_reference,
            declared_reference,
            label=f"edge member {index - 1}",
        )
        if observed_reference.record_format != _EDGE_FORMAT:
            raise ValueError("loaded sequence edge format is unsupported for presentation.")

        note_text = edge.revision.revised_note.note_text
        if note_text != edge.verification.revised_note_text:
            raise ValueError(
                f"loaded sequence edge member {index - 1} retains incoherent note text."
            )

        members.append(
            ChromiumPageResearchRevisionEdgeSequenceMemberPresentation(
                declared_position=index,
                edge_format=observed_reference.record_format,
                edge_record_sha256=observed_reference.record_sha256,
                note_text=note_text,
            )
        )

    if not members:
        raise ValueError("loaded sequence must contain at least one member for presentation.")

    return ChromiumPageResearchRevisionEdgeSequencePresentation(
        presentation_mode=_PRESENTATION_MODE,
        declaration_format=verification.sequence_format,
        declaration_record_sha256=verification.sequence_record_sha256,
        sequence_mode=verification.sequence_mode,
        starting_record_format=observed_start.record_format,
        starting_record_sha256=observed_start.record_sha256,
        members=tuple(members),
    )


def _require_reference_match(
    observed: ChromiumPageResearchWorkingSetNoteRevisionEdgeSequenceReference,
    declared: ChromiumPageResearchWorkingSetNoteRevisionEdgeSequenceReference,
    *,
    label: str,
) -> None:
    if observed.record_format != declared.record_format:
        raise ValueError(f"loaded declaration {label} format is incoherent.")
    if not hmac.compare_digest(observed.record_sha256, declared.record_sha256):
        raise ValueError(f"loaded declaration {label} identity is incoherent.")
