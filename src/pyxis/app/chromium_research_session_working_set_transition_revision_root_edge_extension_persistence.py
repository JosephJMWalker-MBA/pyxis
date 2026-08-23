from __future__ import annotations

from dataclasses import dataclass
import hashlib
import hmac
from pathlib import Path

from .chromium_research_session_working_set_transition_revision_root_edge_extension import (
    ChromiumResearchSessionWorkingSetTransitionRevisionRootEdgeExtensionRecord,
    create_chromium_research_session_working_set_transition_revision_root_edge_extension,
)
from .chromium_research_session_working_set_transition_revision_root_persistence import (
    ChromiumResearchSessionWorkingSetTransitionRevisionRootVerificationEvidence,
    verify_chromium_research_session_working_set_transition_revision_root,
)
from .chromium_research_working_set_note_revision_edge_load import (
    _validate_loaded_root_predecessor,
)
from .chromium_research_working_set_note_revision_edge_persistence import (
    _canonical_document_bytes,
    _canonical_json_bytes,
)


_EDGE_FORMAT = "pyxis.chromium.research_working_set_note_revision_edge.v1"
_ROOT_FORMAT = (
    "pyxis.chromium.research_session_working_set_transition_revision_root.v1"
)
_NOTE_MODE = "caller_authored_note_on_research_working_set"
_REVISION_MODE = "caller_authored_revision_of_research_working_set_note"
_EXTENSION_MODE = (
    "caller_authored_extension_of_verified_cross_working_set_revision_root"
)
_EDGE_MODE = "caller_authored_research_working_set_note_revision_edge"


@dataclass(frozen=True, slots=True)
class ChromiumResearchSessionWorkingSetTransitionRevisionRootEdgePersistenceEvidence:
    """Durable evidence for the first ordinary edge after one loaded 34A root.

    `extension` retains the exact caller-supplied 34B extension. `root_verification`
    is a fresh file-local verification of the caller-supplied current root file.
    The written bytes use the existing 24B edge format and name that exact root
    format + content identity as predecessor.
    """

    path: Path
    edge_format: str
    edge_record_sha256: str
    byte_count: int
    extension: ChromiumResearchSessionWorkingSetTransitionRevisionRootEdgeExtensionRecord
    root_verification: ChromiumResearchSessionWorkingSetTransitionRevisionRootVerificationEvidence


def persist_chromium_research_session_working_set_transition_revision_root_edge_extension(
    extension: ChromiumResearchSessionWorkingSetTransitionRevisionRootEdgeExtensionRecord,
    *,
    root_source: Path,
    destination: Path,
) -> ChromiumResearchSessionWorkingSetTransitionRevisionRootEdgePersistenceEvidence:
    """Persist the first existing-format 24B edge after one 34A root.

    The retained loaded root is re-established in memory. The current durable root
    file is then freshly verified and must match the exact loaded root format and
    SHA-256 before any edge bytes are written. This deliberately does not reopen the
    older 33B transition or old evidence-basis files; it is the same local-current-
    predecessor model already used by repeated ordinary edges.
    """

    if not isinstance(
        extension,
        ChromiumResearchSessionWorkingSetTransitionRevisionRootEdgeExtensionRecord,
    ):
        raise TypeError(
            "extension must be "
            "ChromiumResearchSessionWorkingSetTransitionRevisionRootEdgeExtensionRecord."
        )

    rebuilt = create_chromium_research_session_working_set_transition_revision_root_edge_extension(
        extension.prior_root,
        revised_note_text=extension.revision.revised_note.note_text,
    )
    if rebuilt.extension_mode != extension.extension_mode or extension.extension_mode != _EXTENSION_MODE:
        raise ValueError("Cross-working-set root edge-extension mode is unsupported.")
    if extension.revision.revision_mode != _REVISION_MODE:
        raise ValueError("Cross-working-set root edge revision mode is unsupported.")
    if extension.revision.revised_note.note_mode != _NOTE_MODE:
        raise ValueError("Cross-working-set root edge revised-note mode is unsupported.")

    root_format, root_sha256, endpoint_note = _validate_loaded_root_predecessor(
        extension.prior_root
    )
    if extension.revision.prior_note is not endpoint_note:
        raise ValueError("Root edge extension must retain the exact root endpoint note.")
    if extension.revision.revised_note.working_set is not endpoint_note.working_set:
        raise ValueError("Root edge extension must retain the exact changed working set.")

    if not isinstance(root_source, Path):
        raise TypeError("root_source must be pathlib.Path.")
    root_verification = verify_chromium_research_session_working_set_transition_revision_root(
        root_source
    )
    if root_verification.root_format != _ROOT_FORMAT or root_format != _ROOT_FORMAT:
        raise ValueError("Current durable root uses an unsupported format.")
    if root_verification.root_format != root_format:
        raise ValueError("Current durable root format does not match the loaded root.")
    if not hmac.compare_digest(root_verification.root_record_sha256, root_sha256):
        raise ValueError("Current durable root does not match the loaded root.")

    path = Path(destination).expanduser().resolve()
    if not path.parent.is_dir():
        raise FileNotFoundError(
            f"Research root-edge parent directory does not exist: {path.parent}"
        )

    edge_record = {
        "predecessor_reference": {
            "format": root_verification.root_format,
            "record_sha256": root_verification.root_record_sha256,
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

    return ChromiumResearchSessionWorkingSetTransitionRevisionRootEdgePersistenceEvidence(
        path=path,
        edge_format=_EDGE_FORMAT,
        edge_record_sha256=edge_record_sha256,
        byte_count=len(document_bytes),
        extension=extension,
        root_verification=root_verification,
    )


__all__ = [
    "ChromiumResearchSessionWorkingSetTransitionRevisionRootEdgePersistenceEvidence",
    "persist_chromium_research_session_working_set_transition_revision_root_edge_extension",
]
