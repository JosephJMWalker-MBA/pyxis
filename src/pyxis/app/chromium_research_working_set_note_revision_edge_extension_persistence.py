from __future__ import annotations

from dataclasses import dataclass
import hashlib
import hmac
from pathlib import Path

from .chromium_research_working_set_note_revision_edge_extension import (
    ChromiumPageResearchWorkingSetNoteRevisionEdgeExtensionRecord,
    create_chromium_research_working_set_note_revision_edge_extension,
)
from .chromium_research_working_set_note_revision_edge_load import (
    load_chromium_research_working_set_note_revision_edge,
)
from .chromium_research_working_set_note_revision_edge_persistence import (
    _canonical_document_bytes,
    _canonical_json_bytes,
)


_EDGE_FORMAT = "pyxis.chromium.research_working_set_note_revision_edge.v1"
_NOTE_MODE = "caller_authored_note_on_research_working_set"
_REVISION_MODE = "caller_authored_revision_of_research_working_set_note"
_EXTENSION_MODE = (
    "caller_authored_extension_of_verified_research_working_set_note_revision_edge"
)
_EDGE_MODE = "caller_authored_research_working_set_note_revision_edge"


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchWorkingSetNoteRevisionEdgeExtensionPersistenceEvidence:
    """Durable evidence for one 25A extension written in the existing 24B format.

    `extension` retains the exact caller-supplied 25A object. The persisted record
    contains only the freshly re-established content identity of the immediate 24B
    predecessor edge, the generic edge/revision/note modes, and the new verbatim
    human wording.

    This evidence does not establish chronology, a current head, uniqueness of the
    successor, whole-history validity, authorship identity, trusted time, semantic
    improvement, or source/claim authority.
    """

    path: Path
    edge_format: str
    edge_record_sha256: str
    byte_count: int
    extension: ChromiumPageResearchWorkingSetNoteRevisionEdgeExtensionRecord


def persist_chromium_research_working_set_note_revision_edge_extension(
    extension: ChromiumPageResearchWorkingSetNoteRevisionEdgeExtensionRecord,
    prior_edge_source: Path,
    destination: Path,
) -> ChromiumPageResearchWorkingSetNoteRevisionEdgeExtensionPersistenceEvidence:
    """Persist one 25A extension as another existing-format 24B revision edge.

    The caller explicitly supplies the current durable file for the exact loaded
    edge retained by `extension`. Before writing, Pyxis re-establishes the live 25A
    application contract and freshly reopens that predecessor edge.

    Ordinary edge-backed predecessors use public 24C exactly as before. If the prior
    edge is the first edge after a 34A basis-change root, 34B dispatches through the
    explicit root-edge loader once so that the root-backed predecessor identity can
    be re-established without widening generic 24C itself.

    No digest search, directory scan, automatic ancestry traversal, current-head
    selection, revision numbering, timestamp inference, or semantic comparison occurs.
    """

    if not isinstance(
        extension,
        ChromiumPageResearchWorkingSetNoteRevisionEdgeExtensionRecord,
    ):
        raise TypeError(
            "extension must be "
            "ChromiumPageResearchWorkingSetNoteRevisionEdgeExtensionRecord."
        )

    rebuilt = create_chromium_research_working_set_note_revision_edge_extension(
        extension.prior_edge,
        revised_note_text=extension.revision.revised_note.note_text,
    )
    if rebuilt.extension_mode != extension.extension_mode:
        raise ValueError(
            "loaded-edge extension mode is unsupported for durable edge persistence."
        )
    if extension.extension_mode != _EXTENSION_MODE:
        raise ValueError(
            "loaded-edge extension mode is unsupported for durable edge persistence."
        )
    if rebuilt.revision.revision_mode != extension.revision.revision_mode:
        raise ValueError(
            "loaded-edge extension revision mode is unsupported for persistence."
        )
    if extension.revision.revision_mode != _REVISION_MODE:
        raise ValueError(
            "loaded-edge extension revision mode is unsupported for persistence."
        )
    if rebuilt.revision.revised_note.note_mode != extension.revision.revised_note.note_mode:
        raise ValueError(
            "loaded-edge extension revised-note mode is unsupported for persistence."
        )
    if extension.revision.revised_note.note_mode != _NOTE_MODE:
        raise ValueError(
            "loaded-edge extension revised-note mode is unsupported for persistence."
        )
    if extension.revision.prior_note is not extension.prior_edge.revision.revised_note:
        raise ValueError(
            "loaded-edge extension must retain the exact predecessor edge endpoint note."
        )
    if (
        extension.revision.revised_note.working_set
        is not extension.prior_edge.revision.revised_note.working_set
    ):
        raise ValueError(
            "loaded-edge extension revised note must retain the exact predecessor working set."
        )

    prior_predecessor = extension.prior_edge.predecessor
    from .chromium_research_session_working_set_transition_revision_root_load import (
        ChromiumPageResearchLoadedWorkingSetTransitionRevisionRootRecord,
    )

    if isinstance(
        prior_predecessor,
        ChromiumPageResearchLoadedWorkingSetTransitionRevisionRootRecord,
    ):
        from .chromium_research_session_working_set_transition_revision_root_edge_load import (
            load_chromium_research_session_working_set_transition_revision_root_edge,
        )

        loaded_prior = load_chromium_research_session_working_set_transition_revision_root_edge(
            prior_predecessor,
            prior_edge_source,
        )
    else:
        loaded_prior = load_chromium_research_working_set_note_revision_edge(
            prior_predecessor,
            prior_edge_source,
        )

    if loaded_prior.verification.edge_format != _EDGE_FORMAT:
        raise ValueError("durable loaded-edge predecessor format is unsupported.")
    if extension.prior_edge.verification.edge_format != _EDGE_FORMAT:
        raise ValueError("retained loaded-edge predecessor format is unsupported.")
    if loaded_prior.verification.edge_format != extension.prior_edge.verification.edge_format:
        raise ValueError(
            "durable loaded-edge predecessor format does not match the extension."
        )
    if not hmac.compare_digest(
        loaded_prior.verification.edge_record_sha256,
        extension.prior_edge.verification.edge_record_sha256,
    ):
        raise ValueError(
            "durable loaded-edge predecessor does not match the extension."
        )
    if loaded_prior.predecessor is not extension.prior_edge.predecessor:
        raise ValueError(
            "freshly relinked loaded-edge predecessor does not retain the exact supplied predecessor object."
        )
    if (
        loaded_prior.revision.revised_note.working_set
        is not extension.prior_edge.revision.revised_note.working_set
    ):
        raise ValueError(
            "freshly relinked loaded-edge predecessor does not retain the exact working set."
        )
    if (
        loaded_prior.revision.revised_note.note_text
        != extension.prior_edge.revision.revised_note.note_text
    ):
        raise ValueError(
            "freshly relinked loaded-edge predecessor endpoint does not match the extension."
        )

    path = Path(destination).expanduser().resolve()
    if not path.parent.is_dir():
        raise FileNotFoundError(
            "Research working-set-note revision-edge parent directory does not exist: "
            f"{path.parent}"
        )

    edge_record = {
        "predecessor_reference": {
            "format": loaded_prior.verification.edge_format,
            "record_sha256": loaded_prior.verification.edge_record_sha256,
        },
        "edge": {
            "mode": _EDGE_MODE,
            "revision": {
                "mode": extension.revision.revision_mode,
                "revised_note": {
                    "mode": extension.revision.revised_note.note_mode,
                    "text": extension.revision.revised_note.note_text,
                },
            },
        },
    }
    edge_record_sha256 = hashlib.sha256(_canonical_json_bytes(edge_record)).hexdigest()
    document = {
        "format": _EDGE_FORMAT,
        "edge_record": edge_record,
        "edge_record_sha256": edge_record_sha256,
    }
    document_bytes = _canonical_document_bytes(document)

    with path.open("xb") as handle:
        handle.write(document_bytes)

    return ChromiumPageResearchWorkingSetNoteRevisionEdgeExtensionPersistenceEvidence(
        path=path,
        edge_format=_EDGE_FORMAT,
        edge_record_sha256=edge_record_sha256,
        byte_count=len(document_bytes),
        extension=extension,
    )
