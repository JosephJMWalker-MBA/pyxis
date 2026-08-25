from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Iterable

from .chromium_research_working_set_note_revision_continuation_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord,
)
from .chromium_research_working_set_note_revision_edge_load import (
    ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord,
    load_chromium_research_working_set_note_revision_edge,
)

if TYPE_CHECKING:
    from .chromium_research_session_working_set_transition_revision_root_load import (
        ChromiumPageResearchLoadedWorkingSetTransitionRevisionRootRecord,
    )


_SEQUENCE_MODE = (
    "caller_explicit_ordered_relinked_research_working_set_note_revision_edge_sequence"
)


class ChromiumResearchWorkingSetNoteRevisionEdgeSequenceRelinkError(ValueError):
    """Raised when one explicit member of an ordered edge sequence cannot relink."""


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceRecord:
    """One caller-explicit ordered sequence of freshly relinked revision edges.

    `starting_predecessor` retains the exact already-loaded 23C continuation, 24C
    edge, or 34A cross-working-set revision root supplied by the caller. `edges`
    contains the freshly loaded standard 24B edge records in exactly the order
    supplied through `edge_sources`.

    If the caller explicitly starts at a 34A root, only the first edge is reopened
    through the root-specific 34B bridge. Every later edge resumes ordinary public
    24C relinking. Root support therefore adds one explicit sequence-start authority
    without making roots generic 24C predecessors.

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
        | ChromiumPageResearchLoadedWorkingSetTransitionRevisionRootRecord
    )
    edges: tuple[ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord, ...]


def load_chromium_research_working_set_note_revision_edge_sequence(
    starting_predecessor: (
        ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord
        | ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord
        | ChromiumPageResearchLoadedWorkingSetTransitionRevisionRootRecord
    ),
    edge_sources: Iterable[Path],
) -> ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeSequenceRecord:
    """Freshly relink one explicit ordered sequence of durable 24B edge files.

    The caller owns both the starting predecessor and file order. Pyxis snapshots
    the supplied iterable and requires at least one edge. An ordinary 23C/24C start
    delegates every member to public 24C. A 34A root start delegates exactly the
    first member to the explicit 34B root-edge loader, then resumes public 24C for
    every later edge.

    Root imports are deliberately resolved only inside this application boundary.
    That preserves the existing controller/presentation import graph while keeping
    root authority explicit at runtime.

    No directory scan, digest search, predecessor discovery, path inference,
    reordering, skipping, branch selection, automatic history traversal, current-
    head selection, revision numbering, timestamp inference, or semantic comparison
    occurs. Failure is reported at the exact zero-based sequence position where the
    delegated relinking boundary fails.
    """

    root_type = _loaded_root_type()
    if not isinstance(
        starting_predecessor,
        (
            ChromiumPageResearchLoadedWorkingSetNoteRevisionContinuationRecord,
            ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord,
            root_type,
        ),
    ):
        raise TypeError(
            "starting_predecessor must be an already-loaded 23C continuation, "
            "24C revision edge, or 34A cross-working-set revision root."
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
            if index == 0 and isinstance(current, root_type):
                from .chromium_research_session_working_set_transition_revision_root_edge_load import (
                    load_chromium_research_session_working_set_transition_revision_root_edge,
                )

                loaded = (
                    load_chromium_research_session_working_set_transition_revision_root_edge(
                        current,
                        source,
                    )
                )
            else:
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


def _loaded_root_type():
    from .chromium_research_session_working_set_transition_revision_root_load import (
        ChromiumPageResearchLoadedWorkingSetTransitionRevisionRootRecord,
    )

    return ChromiumPageResearchLoadedWorkingSetTransitionRevisionRootRecord
