from __future__ import annotations

import json

from .chromium_research_root_backed_session_authority_inspection import (
    RootBackedAuthorityInspection,
    root_backed_authority_notice,
)


_INSPECTION_FORMAT = (
    "pyxis.chromium.research_root_backed_session_authority_inspection.v1"
)


def serialize_chromium_research_root_backed_session_authority_inspection(
    inspection: RootBackedAuthorityInspection,
) -> str:
    """Serialize one already-derived one-root authority inspection deterministically.

    Serialization is presentation only. It performs no file reads, path proof,
    re-entry, discovery, mutation, checkpointing, restart, or authority promotion.
    """

    if not isinstance(inspection, RootBackedAuthorityInspection):
        raise TypeError("inspection must be RootBackedAuthorityInspection.")

    launch = inspection.launch_provenance
    current = inspection.current_state
    document = {
        "authority_notice": root_backed_authority_notice(),
        "current_governed_state": {
            "declared_continuation_edge_count": current.declared_continuation_edge_count,
            "endpoint_sha256": current.endpoint_sha256,
            "state_kind": current.state_kind,
            "state_source": current.state_source,
        },
        "format": _INSPECTION_FORMAT,
        "launch_provenance": {
            "launch_endpoint_sha256": launch.launch_endpoint_sha256,
            "launch_family": launch.launch_family,
            "launch_location_context_only": (
                None
                if launch.launch_location_context is None
                else str(launch.launch_location_context)
            ),
            "root_sha256": launch.root_sha256,
        },
        "report_role": "read_only_inspection_not_authority",
    }
    return json.dumps(
        document,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    ) + "\n"


__all__ = [
    "serialize_chromium_research_root_backed_session_authority_inspection",
]
