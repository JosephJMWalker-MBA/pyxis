from __future__ import annotations

import json

from .chromium_research_third_basis_epoch_authority_inspection import (
    ThirdBasisEpochAuthorityInspection,
    third_basis_epoch_authority_notice,
)


_INSPECTION_FORMAT = (
    "pyxis.chromium.research_third_basis_epoch_authority_inspection.v1"
)


def serialize_chromium_research_third_basis_epoch_authority_inspection(
    inspection: ThirdBasisEpochAuthorityInspection,
) -> str:
    """Serialize one already-derived third-epoch inspection deterministically.

    Serialization is presentation only. It performs no file reads, path proof,
    re-entry, discovery, mutation, checkpointing, or authority promotion.
    """

    if not isinstance(inspection, ThirdBasisEpochAuthorityInspection):
        raise TypeError("inspection must be ThirdBasisEpochAuthorityInspection.")

    launch = inspection.launch_provenance
    current = inspection.current_state
    document = {
        "authority_notice": third_basis_epoch_authority_notice(),
        "current_governed_state": {
            "declared_continuation_edge_count": current.declared_continuation_edge_count,
            "endpoint_sha256": current.endpoint_sha256,
            "state_kind": current.state_kind,
            "state_source": current.state_source,
        },
        "format": _INSPECTION_FORMAT,
        "launch_provenance": {
            "first_root_sha256": launch.first_root_sha256,
            "launch_endpoint_sha256": launch.launch_endpoint_sha256,
            "launch_family": launch.launch_family,
            "launch_location_context_only": (
                None
                if launch.launch_location_context is None
                else str(launch.launch_location_context)
            ),
            "second_root_sha256": launch.second_root_sha256,
            "third_root_sha256": launch.third_root_sha256,
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
    "serialize_chromium_research_third_basis_epoch_authority_inspection",
]
