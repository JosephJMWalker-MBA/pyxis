from __future__ import annotations

from dataclasses import dataclass
import hmac
from pathlib import Path
from typing import Iterable

from .chromium_research_working_set_note_revision_continuation_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord,
)
from .chromium_research_working_set_note_revision_edge_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord,
)
from .chromium_research_working_set_note_revision_edge_sequence_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceRecord,
    ChromiumResearchWorkingSetNoteRevisionEdgeSequenceRelinkError,
    load_chromium_research_working_set_note_revision_edge_sequence,
)
from .chromium_research_working_set_note_revision_edge_sequence_persistence import (
    ChromiumPageResearchWorkingSetNoteRevisionEdgeSequenceReference,
    ChromiumPageResearchWorkingSetNoteRevisionEdgeSequenceVerificationEvidence,
    _loaded_record_reference,
    _retained_edge_reference,
    verify_chromium_research_working_set_note_revision_edge_sequence,
)


_SEQUENCE_FORMAT = (
    "pyxis.chromium.research_working_set_note_revision_edge_sequence.v1"
)
_SEQUENCE_MODE = (
    "caller_explicit_ordered_relinked_research_working_set_note_revision_edge_sequence"
)


class ChromiumResearchWorkingSetNoteRevisionEdgeSequenceDeclarationRelinkError(
    ValueError
):
    """Raised when a durable 26B declaration does not match explicit relinked evidence."""


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceDeclarationRecord:
    """One freshly verified 26B declaration reconciled to one explicit 26A sequence.

    `verification` is fresh file-local 26B evidence for the declaration file.
    `sequence` is a fresh 26A relinking from the exact caller-supplied starting
    predecessor and exact caller-supplied ordered edge paths.

    Successful creation establishes only that the durable declaration names the
    same starting content identity and the same ordered edge content identities as
    that freshly relinked explicit sequence. It does not discover files, select a
    current head, establish completeness or chronology, infer branches, validate
    ancestry below the supplied start, or make semantic claims about revisions.
    """

    verification: ChromiumPageResearchWorkingSetNoteRevisionEdgeSequenceVerificationEvidence
    sequence: ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceRecord


def load_chromium_research_working_set_note_revision_edge_sequence_declaration(
    starting_predecessor: (
        ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord
        | ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord
    ),
    edge_sources: Iterable[Path],
    declaration_source: Path,
) -> ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceDeclarationRecord:
    """Relink one durable 26B declaration against explicit caller-supplied evidence.

    The declaration never locates its referenced records. The caller supplies the
    already-loaded starting predecessor and the ordered edge paths independently.
    Pyxis first freshly verifies only the declaration file, then freshly composes
    public 26A across those explicit edge paths, and finally compares the declared
    content identities to the freshly relinked application evidence position by
    position.

    Thus 26C re-establishes declaration attachment without adding directory scans,
    digest search, path inference, automatic traversal, head selection, chronology,
    branch semantics, completeness claims, or semantic interpretation.
    """

    verification = verify_chromium_research_working_set_note_revision_edge_sequence(
        declaration_source
    )
    if verification.sequence_format != _SEQUENCE_FORMAT:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeSequenceDeclarationRelinkError(
            "Verified revision-edge-sequence declaration format is unsupported."
        )
    if verification.sequence_mode != _SEQUENCE_MODE:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeSequenceDeclarationRelinkError(
            "Verified revision-edge-sequence declaration mode is unsupported."
        )

    try:
        sequence = load_chromium_research_working_set_note_revision_edge_sequence(
            starting_predecessor,
            edge_sources,
        )
    except ChromiumResearchWorkingSetNoteRevisionEdgeSequenceRelinkError as exc:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeSequenceDeclarationRelinkError(
            "Explicit revision-edge sequence could not be freshly relinked."
        ) from exc

    if sequence.sequence_mode != verification.sequence_mode:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeSequenceDeclarationRelinkError(
            "Fresh explicit sequence mode does not match the durable declaration."
        )

    observed_start = _loaded_record_reference(sequence.starting_predecessor)
    _require_reference_match(
        observed_start,
        verification.starting_predecessor,
        label="starting predecessor",
    )

    if len(sequence.edges) != len(verification.edges):
        raise ChromiumResearchWorkingSetNoteRevisionEdgeSequenceDeclarationRelinkError(
            "Fresh explicit sequence member count does not match the durable declaration."
        )

    for index, (edge, declared_reference) in enumerate(
        zip(sequence.edges, verification.edges)
    ):
        observed_reference = _retained_edge_reference(edge)
        _require_reference_match(
            observed_reference,
            declared_reference,
            label=f"edge member {index}",
        )

    return ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceDeclarationRecord(
        verification=verification,
        sequence=sequence,
    )


def _require_reference_match(
    observed: ChromiumPageResearchWorkingSetNoteRevisionEdgeSequenceReference,
    declared: ChromiumPageResearchWorkingSetNoteRevisionEdgeSequenceReference,
    *,
    label: str,
) -> None:
    if observed.record_format != declared.record_format:
        raise ChromiumResearchWorkingSetNoteRevisionEdgeSequenceDeclarationRelinkError(
            f"Durable declaration {label} format does not match explicit relinked evidence."
        )
    if not hmac.compare_digest(observed.record_sha256, declared.record_sha256):
        raise ChromiumResearchWorkingSetNoteRevisionEdgeSequenceDeclarationRelinkError(
            f"Durable declaration {label} identity does not match explicit relinked evidence."
        )
