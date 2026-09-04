from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Input, Static

from pyxis.app.chromium_research_third_changed_basis_epoch_reentry import (
    ChromiumResearchThirdChangedBasisEpochReentryResult,
)
from pyxis.app.chromium_research_third_changed_basis_epoch_reentry_overlay import (
    ChromiumResearchThirdChangedBasisEpochReentryOverlayResult,
)


THIRD_CHANGED_BASIS_EPOCH_REENTRY_OVERLAY_AUTHORITY_NOTICE = (
    "Persist the exact verified 47E historical third-basis session as strict 40B "
    "restart configuration. Both paths below remain explicit current operational "
    "configuration. This does not relaunch the session, replace mounted governed "
    "state, backfill launch provenance, checkpoint a later continuation, or select "
    "a global current/latest/head branch."
)


def _summary(
    verification: ChromiumResearchThirdChangedBasisEpochReentryResult,
) -> str:
    fresh = verification.fresh_reentry
    prior = fresh.prior_second_basis_epoch_continuation_reentry
    second_epoch = prior.prior_second_basis_epoch_reentry
    return (
        "47E FRESH THIRD-BASIS RECONSTRUCTION PROVEN — 40B OVERLAY NOT YET PERSISTED\n"
        f"Retained first root SHA-256: "
        f"{second_epoch.prior_continuation_reentry.prior_root_backed_reentry.loaded_root.verification.root_record_sha256}\n"
        f"Retained second root SHA-256: {second_epoch.loaded_root.verification.root_record_sha256}\n"
        f"Third root SHA-256: {fresh.loaded_root.verification.root_record_sha256}\n"
        f"Declaration SHA-256: {fresh.loaded_declaration.verification.sequence_record_sha256}\n"
        f"Endpoint edge SHA-256: {fresh.controller.declared_endpoint.verification.edge_record_sha256}\n"
        "Re-supply the current prior 37C/37D second-epoch continuation-overlay path "
        "and choose one new no-overwrite 40B destination. No 47E plan or launch path "
        "is copied into either field."
    )


def third_changed_basis_epoch_reentry_overlay_success_receipt(
    result: ChromiumResearchThirdChangedBasisEpochReentryOverlayResult,
) -> str:
    checkpoint = result.checkpoint
    fresh = checkpoint.fresh_reentry
    prior = fresh.prior_second_basis_epoch_continuation_reentry
    second_epoch = prior.prior_second_basis_epoch_reentry
    return (
        "Success — durable 40B third-basis restart overlay persisted for the exact "
        "verified historical 47D/47E session. Mounted governed session unchanged.\n"
        "Overlay format: pyxis.chromium.research_third_basis_epoch_reentry_locator_overlay.v1\n"
        f"Overlay path: {checkpoint.persistence.path}\n"
        "Referenced prior second-epoch continuation overlay: "
        f"{checkpoint.plan.prior_second_basis_epoch_continuation_overlay_source}\n"
        f"Retained first root SHA-256: "
        f"{second_epoch.prior_continuation_reentry.prior_root_backed_reentry.loaded_root.verification.root_record_sha256}\n"
        f"Retained second root SHA-256: {second_epoch.loaded_root.verification.root_record_sha256}\n"
        f"Third root SHA-256: {fresh.loaded_root.verification.root_record_sha256}\n"
        f"Endpoint edge SHA-256: {fresh.controller.declared_endpoint.verification.edge_record_sha256}\n"
        "This overlay is durable operational restart configuration for that exact "
        "historical third-basis session. It does not claim global current/latest/head "
        "state, alter launch provenance, relaunch the session, or checkpoint a later continuation."
    )


class ResearchThirdChangedBasisEpochReentryOverlayControls(Vertical):
    """Explicit 47F controls for one proof-gated public-40B persistence step."""

    def __init__(
        self,
        verification_result: ChromiumResearchThirdChangedBasisEpochReentryResult,
        prior_result: ChromiumResearchThirdChangedBasisEpochReentryOverlayResult | None = None,
    ) -> None:
        if type(verification_result) is not ChromiumResearchThirdChangedBasisEpochReentryResult:
            raise TypeError(
                "verification_result must be exactly "
                "ChromiumResearchThirdChangedBasisEpochReentryResult."
            )
        if (
            prior_result is not None
            and prior_result.verification_result is not verification_result
        ):
            raise ValueError(
                "Prior 47F result does not belong to this exact 47E verification."
            )
        super().__init__(id="research-third-changed-basis-epoch-reentry-overlay-controls")
        self.verification_result = verification_result
        self.prior_result = prior_result

    def compose(self) -> ComposeResult:
        locked = self.prior_result is not None
        yield Static(
            "Persist verified third-basis restart overlay",
            id="research-third-changed-basis-epoch-reentry-overlay-title",
        )
        yield Static(
            THIRD_CHANGED_BASIS_EPOCH_REENTRY_OVERLAY_AUTHORITY_NOTICE,
            id="research-third-changed-basis-epoch-reentry-overlay-authority-notice",
            markup=False,
        )
        yield Static(
            _summary(self.verification_result),
            id="research-third-changed-basis-epoch-reentry-overlay-summary",
            markup=False,
        )
        yield Input(
            placeholder="Explicit current prior 37C/37D second-epoch continuation-overlay path",
            id="research-third-changed-basis-epoch-reentry-overlay-prior-continuation-overlay-source",
            disabled=locked,
        )
        yield Input(
            placeholder="Explicit no-overwrite 40B third-basis overlay destination",
            id="research-third-changed-basis-epoch-reentry-overlay-destination",
            disabled=locked,
        )
        yield Button(
            "Persist verified 40B overlay — mounted session will not change",
            id="persist-research-third-changed-basis-epoch-reentry-overlay",
            variant="warning",
            disabled=locked,
        )
        yield Static(
            third_changed_basis_epoch_reentry_overlay_success_receipt(self.prior_result)
            if self.prior_result is not None
            else "",
            id="research-third-changed-basis-epoch-reentry-overlay-status",
            markup=False,
        )

    def lock_after_success(
        self,
        result: ChromiumResearchThirdChangedBasisEpochReentryOverlayResult,
    ) -> None:
        if result.verification_result is not self.verification_result:
            raise ValueError("47F result does not retain this exact 47E verification.")
        self.prior_result = result
        self.query_one(
            "#research-third-changed-basis-epoch-reentry-overlay-prior-continuation-overlay-source",
            Input,
        ).disabled = True
        self.query_one(
            "#research-third-changed-basis-epoch-reentry-overlay-destination",
            Input,
        ).disabled = True
        self.query_one(
            "#persist-research-third-changed-basis-epoch-reentry-overlay",
            Button,
        ).disabled = True
        self.query_one(
            "#research-third-changed-basis-epoch-reentry-overlay-status",
            Static,
        ).update(third_changed_basis_epoch_reentry_overlay_success_receipt(result))


__all__ = [
    "THIRD_CHANGED_BASIS_EPOCH_REENTRY_OVERLAY_AUTHORITY_NOTICE",
    "ResearchThirdChangedBasisEpochReentryOverlayControls",
    "third_changed_basis_epoch_reentry_overlay_success_receipt",
]
