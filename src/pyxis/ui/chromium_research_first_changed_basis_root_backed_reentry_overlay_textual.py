from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Input, Static

from pyxis.app.chromium_research_first_changed_basis_root_backed_reentry import (
    ChromiumResearchFirstChangedBasisRootBackedReentryResult,
)
from pyxis.app.chromium_research_first_changed_basis_root_backed_reentry_overlay import (
    ChromiumResearchFirstChangedBasisRootBackedReentryOverlayResult,
)


FIRST_CHANGED_BASIS_ROOT_BACKED_REENTRY_OVERLAY_AUTHORITY_NOTICE = (
    "Persist the exact verified 44F historical root-backed session as strict 35C "
    "restart configuration. Both paths below remain explicit. This does not replace "
    "the mounted governed session, promote active restart controls, checkpoint a later "
    "continuation, or select a global current/latest/head branch."
)


def _summary(
    verification: ChromiumResearchFirstChangedBasisRootBackedReentryResult,
) -> str:
    fresh = verification.fresh_reentry
    return (
        "44F FRESH RECONSTRUCTION PROVEN — 35C OVERLAY NOT YET PERSISTED\n"
        f"Root SHA-256: {fresh.loaded_root.verification.root_record_sha256}\n"
        f"Declaration SHA-256: {fresh.loaded_declaration.verification.sequence_record_sha256}\n"
        f"Endpoint edge SHA-256: {fresh.controller.declared_endpoint.verification.edge_record_sha256}\n"
        "Supply the existing ordinary 31B plan document and a new overlay destination. "
        "No prior receipt path is copied into either field."
    )


def first_changed_basis_root_backed_reentry_overlay_success_receipt(
    result: ChromiumResearchFirstChangedBasisRootBackedReentryOverlayResult,
) -> str:
    checkpoint = result.checkpoint
    fresh = checkpoint.fresh_reentry
    return (
        "Success — durable 35C root-backed restart overlay persisted for the exact "
        "verified historical 44E/44F session. Mounted governed session unchanged.\n"
        "Overlay format: pyxis.chromium.research_root_backed_session_reentry_locator_overlay.v1\n"
        f"Overlay path: {checkpoint.persistence.path}\n"
        f"Referenced ordinary-plan path: {checkpoint.persistence.prior_session_plan_source}\n"
        f"Root SHA-256: {fresh.loaded_root.verification.root_record_sha256}\n"
        f"Endpoint edge SHA-256: {fresh.controller.declared_endpoint.verification.edge_record_sha256}\n"
        "Endpoint rationale:\n"
        f"{fresh.controller.declared_endpoint.revision.revised_note.note_text}\n"
        "This overlay is durable operational restart configuration for that verified "
        "historical session. It does not claim global current/latest/head state, does "
        "not replace the mounted controller, and does not checkpoint a later 35D continuation."
    )


class ResearchFirstChangedBasisRootBackedReentryOverlayControls(Vertical):
    """Explicit 44G controls for one proof-gated 35C overlay persistence step."""

    def __init__(
        self,
        verification_result: ChromiumResearchFirstChangedBasisRootBackedReentryResult,
        prior_result: ChromiumResearchFirstChangedBasisRootBackedReentryOverlayResult | None = None,
    ) -> None:
        if type(verification_result) is not ChromiumResearchFirstChangedBasisRootBackedReentryResult:
            raise TypeError(
                "verification_result must be exactly "
                "ChromiumResearchFirstChangedBasisRootBackedReentryResult."
            )
        if prior_result is not None and prior_result.verification_result is not verification_result:
            raise ValueError("Prior 44G result does not belong to this exact 44F verification.")
        super().__init__(id="research-first-changed-basis-root-backed-reentry-overlay-controls")
        self.verification_result = verification_result
        self.prior_result = prior_result

    def compose(self) -> ComposeResult:
        locked = self.prior_result is not None
        yield Static(
            "Persist verified root-backed restart overlay",
            id="research-first-changed-basis-root-backed-reentry-overlay-title",
        )
        yield Static(
            FIRST_CHANGED_BASIS_ROOT_BACKED_REENTRY_OVERLAY_AUTHORITY_NOTICE,
            id="research-first-changed-basis-root-backed-reentry-overlay-authority-notice",
            markup=False,
        )
        yield Static(
            _summary(self.verification_result),
            id="research-first-changed-basis-root-backed-reentry-overlay-summary",
            markup=False,
        )
        yield Input(
            placeholder="Explicit current ordinary 31B plan-document path",
            id="research-first-changed-basis-root-backed-reentry-overlay-prior-plan-source",
            disabled=locked,
        )
        yield Input(
            placeholder="Explicit no-overwrite 35C overlay destination",
            id="research-first-changed-basis-root-backed-reentry-overlay-destination",
            disabled=locked,
        )
        yield Button(
            "Persist verified restart overlay — mounted session will not change",
            id="persist-research-first-changed-basis-root-backed-reentry-overlay",
            variant="warning",
            disabled=locked,
        )
        yield Static(
            first_changed_basis_root_backed_reentry_overlay_success_receipt(self.prior_result)
            if self.prior_result is not None
            else "",
            id="research-first-changed-basis-root-backed-reentry-overlay-status",
            markup=False,
        )

    def lock_after_success(
        self,
        result: ChromiumResearchFirstChangedBasisRootBackedReentryOverlayResult,
    ) -> None:
        if result.verification_result is not self.verification_result:
            raise ValueError("44G result does not retain this exact 44F verification.")
        self.prior_result = result
        self.query_one(
            "#research-first-changed-basis-root-backed-reentry-overlay-prior-plan-source",
            Input,
        ).disabled = True
        self.query_one(
            "#research-first-changed-basis-root-backed-reentry-overlay-destination",
            Input,
        ).disabled = True
        self.query_one(
            "#persist-research-first-changed-basis-root-backed-reentry-overlay",
            Button,
        ).disabled = True
        self.query_one(
            "#research-first-changed-basis-root-backed-reentry-overlay-status",
            Static,
        ).update(first_changed_basis_root_backed_reentry_overlay_success_receipt(result))


__all__ = [
    "FIRST_CHANGED_BASIS_ROOT_BACKED_REENTRY_OVERLAY_AUTHORITY_NOTICE",
    "ResearchFirstChangedBasisRootBackedReentryOverlayControls",
    "first_changed_basis_root_backed_reentry_overlay_success_receipt",
]
