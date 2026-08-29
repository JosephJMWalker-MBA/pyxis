from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Input, Static

from pyxis.app.chromium_research_second_changed_basis_epoch_reentry import (
    ChromiumResearchSecondChangedBasisEpochReentryResult,
)
from pyxis.app.chromium_research_second_changed_basis_epoch_reentry_overlay import (
    ChromiumResearchSecondChangedBasisEpochReentryOverlayResult,
)


SECOND_CHANGED_BASIS_EPOCH_REENTRY_OVERLAY_AUTHORITY_NOTICE = (
    "Persist the exact verified 46E historical second-basis session as strict 37B "
    "restart configuration. Both paths below remain explicit current operational "
    "configuration. This does not relaunch the session, replace mounted governed "
    "state, backfill launch provenance, checkpoint a later continuation, or select "
    "a global current/latest/head branch."
)


def _summary(
    verification: ChromiumResearchSecondChangedBasisEpochReentryResult,
) -> str:
    fresh = verification.fresh_reentry
    return (
        "46E FRESH SECOND-BASIS RECONSTRUCTION PROVEN — 37B OVERLAY NOT YET PERSISTED\n"
        f"Retained first root SHA-256: {fresh.prior_continuation_reentry.prior_root_backed_reentry.loaded_root.verification.root_record_sha256}\n"
        f"Second root SHA-256: {fresh.loaded_root.verification.root_record_sha256}\n"
        f"Declaration SHA-256: {fresh.loaded_declaration.verification.sequence_record_sha256}\n"
        f"Endpoint edge SHA-256: {fresh.controller.declared_endpoint.verification.edge_record_sha256}\n"
        "Re-supply the current prior 35D/35E continuation-overlay path and choose one "
        "new no-overwrite 37B destination. No 46E plan or launch path is copied into either field."
    )


def second_changed_basis_epoch_reentry_overlay_success_receipt(
    result: ChromiumResearchSecondChangedBasisEpochReentryOverlayResult,
) -> str:
    checkpoint = result.checkpoint
    fresh = checkpoint.fresh_reentry
    return (
        "Success — durable 37B second-basis restart overlay persisted for the exact "
        "verified historical 46D/46E session. Mounted governed session unchanged.\n"
        "Overlay format: pyxis.chromium.research_second_basis_epoch_reentry_locator_overlay.v1\n"
        f"Overlay path: {checkpoint.persistence.path}\n"
        "Referenced prior continuation overlay: "
        f"{checkpoint.plan.prior_root_backed_continuation_overlay_source}\n"
        f"Retained first root SHA-256: {fresh.prior_continuation_reentry.prior_root_backed_reentry.loaded_root.verification.root_record_sha256}\n"
        f"Second root SHA-256: {fresh.loaded_root.verification.root_record_sha256}\n"
        f"Endpoint edge SHA-256: {fresh.controller.declared_endpoint.verification.edge_record_sha256}\n"
        "This overlay is durable operational restart configuration for that exact "
        "historical second-basis session. It does not claim global current/latest/head "
        "state, alter launch provenance, relaunch the session, or checkpoint a later continuation."
    )


class ResearchSecondChangedBasisEpochReentryOverlayControls(Vertical):
    """Explicit 46F controls for one proof-gated public-37B persistence step."""

    def __init__(
        self,
        verification_result: ChromiumResearchSecondChangedBasisEpochReentryResult,
        prior_result: ChromiumResearchSecondChangedBasisEpochReentryOverlayResult | None = None,
    ) -> None:
        if type(verification_result) is not ChromiumResearchSecondChangedBasisEpochReentryResult:
            raise TypeError(
                "verification_result must be exactly "
                "ChromiumResearchSecondChangedBasisEpochReentryResult."
            )
        if (
            prior_result is not None
            and prior_result.verification_result is not verification_result
        ):
            raise ValueError(
                "Prior 46F result does not belong to this exact 46E verification."
            )
        super().__init__(id="research-second-changed-basis-epoch-reentry-overlay-controls")
        self.verification_result = verification_result
        self.prior_result = prior_result

    def compose(self) -> ComposeResult:
        locked = self.prior_result is not None
        yield Static(
            "Persist verified second-basis restart overlay",
            id="research-second-changed-basis-epoch-reentry-overlay-title",
        )
        yield Static(
            SECOND_CHANGED_BASIS_EPOCH_REENTRY_OVERLAY_AUTHORITY_NOTICE,
            id="research-second-changed-basis-epoch-reentry-overlay-authority-notice",
            markup=False,
        )
        yield Static(
            _summary(self.verification_result),
            id="research-second-changed-basis-epoch-reentry-overlay-summary",
            markup=False,
        )
        yield Input(
            placeholder="Explicit current prior 35D/35E continuation-overlay path",
            id="research-second-changed-basis-epoch-reentry-overlay-prior-continuation-overlay-source",
            disabled=locked,
        )
        yield Input(
            placeholder="Explicit no-overwrite 37B second-basis overlay destination",
            id="research-second-changed-basis-epoch-reentry-overlay-destination",
            disabled=locked,
        )
        yield Button(
            "Persist verified 37B overlay — mounted session will not change",
            id="persist-research-second-changed-basis-epoch-reentry-overlay",
            variant="warning",
            disabled=locked,
        )
        yield Static(
            second_changed_basis_epoch_reentry_overlay_success_receipt(self.prior_result)
            if self.prior_result is not None
            else "",
            id="research-second-changed-basis-epoch-reentry-overlay-status",
            markup=False,
        )

    def lock_after_success(
        self,
        result: ChromiumResearchSecondChangedBasisEpochReentryOverlayResult,
    ) -> None:
        if result.verification_result is not self.verification_result:
            raise ValueError("46F result does not retain this exact 46E verification.")
        self.prior_result = result
        self.query_one(
            "#research-second-changed-basis-epoch-reentry-overlay-prior-continuation-overlay-source",
            Input,
        ).disabled = True
        self.query_one(
            "#research-second-changed-basis-epoch-reentry-overlay-destination",
            Input,
        ).disabled = True
        self.query_one(
            "#persist-research-second-changed-basis-epoch-reentry-overlay",
            Button,
        ).disabled = True
        self.query_one(
            "#research-second-changed-basis-epoch-reentry-overlay-status",
            Static,
        ).update(second_changed_basis_epoch_reentry_overlay_success_receipt(result))


__all__ = [
    "SECOND_CHANGED_BASIS_EPOCH_REENTRY_OVERLAY_AUTHORITY_NOTICE",
    "ResearchSecondChangedBasisEpochReentryOverlayControls",
    "second_changed_basis_epoch_reentry_overlay_success_receipt",
]
