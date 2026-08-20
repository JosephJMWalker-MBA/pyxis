from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .chromium_research_working_set_note_revision_continuation_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord,
)
from .chromium_research_working_set_note_revision_edge_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord,
    load_chromium_research_working_set_note_revision_edge,
)


_SEQUENCE_MODE = (
    "caller_explicit_ordered_relinked_research_working_set_note_revision_edge_sequence"
)


class ChromiumResearchWorkingSetNoteRevisionEdgeSequenceRelinkError(ValueError):
    """Raised when one explicit member of an ordered edge sequence cannot relink."""


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceRecord:
    """One caller-explicit ordered sequence of freshly relinked revision edges.

    `starting_predecessor` retains the exact already-loaded 23C continuation or 24C
    edge supplied by the caller. `edges` contains the freshly loaded 24C records in
    exactly the order supplied through `edge_sources`.

    Successful creation proves only the explicit local adjacency sequence from the
    supplied starting predecessor through these files. It does not discover files,
    infer a current head, establish chronology, prove uniqueness or global
    linearity, validate ancestry below the starting predecessor, or make semantic
    claims about the human revisions.
    """

    sequence_mode: str
    starting_predecessor: (
        ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord
        | ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord
    )
    edges: tuple[ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord, ...]


def load_chromium_research_working_set_note_revision_edge_sequence(
    starting_predecessor: (
        ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord
        | ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord
    ),
    edge_sources: Iterable[Path],
) -> ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceRecord:
    """Freshly relink one explicit ordered sequence of durable 24B edge files.

    The caller owns both the starting predecessor and file order. Pyxis snapshots
    the supplied iterable, requires at least one edge, then repeatedly delegates to
    public 24C. The first edge is loaded against `starting_predecessor`; every later
    edge is loaded against the exact 24C object produced for the preceding member.

    No directory scan, digest search, predecessor discovery, path inference,
    reordering, skipping, branch selection, automatic history traversal, current-
    head selection, revision numbering, timestamp inference, or semantic comparison
    occurs. Failure is reported at the exact zero-based sequence position where the
    delegated 24C boundary fails.
    """

    if not isinstance(
        starting_predecessor,
        (
            ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord,
            ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord,
        ),
    ):
        raise TypeError(
            "starting_predecessor must be an already-loaded 23C continuation or "
            "24C revision edge."
        )

    if isinstance(edge_sources, (str, bytes, Path)):
        raise TypeError(
            "edge_sources must be an ordered iterable of edge paths, not one path."
        )
    try:
        sources = tuple(edge_sources)
    except TypeError as exc:
        raise TypeError("edge_sources must be an ordered iterable of edge paths.") from exc

    if not sources:
        raise ValueError("edge_sources must contain at least one explicit edge path.")

    current = starting_predecessor
    loaded_edges: list[ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord] = []
    for index, source in enumerate(sources):
        try:
            loaded = load_chromium_research_working_set_note_revision_edge(
                current,
                source,
            )
        except (OSError, TypeError, ValueError) as exc:
            raise ChromiumResearchWorkingSetNoteRevisionEdgeSequenceRelinkError(
                f"Revision-edge sequence member {index} could not be relinked to "
                "the explicit preceding application record."
            ) from exc
        loaded_edges.append(loaded)
        current = loaded

    return ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceRecord(
        sequence_mode=_SEQUENCE_MODE,
        starting_predecessor=starting_predecessor,
        edges=tuple(loaded_edges),
    )
