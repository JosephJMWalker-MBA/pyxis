from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Input, Static

from pyxis.app.chromium_research_third_changed_basis_root_edge import (
    ChromiumResearchThirdChangedBasisRootEdgeResult,
)
from pyxis.app.chromium_research_third_changed_basis_session_adoption import (
    ChromiumResearchThirdChangedBasisSessionAdoptionResult,
)


THIRD_CHANGED_BASIS_SESSION_ADOPTION_AUTHORITY_NOTICE = (
    "This explicitly adopts the displayed third changed-basis lineage as this shell's "
    "governed research session by creating and freshly relinking an existing-format "
    "root-started declaration. The action changes this shell's active controller. It "
    "does not establish global current/latest/head authority, infer chronology, perform "
    "40A third-epoch fresh-process re-entry, persist a 40B overlay, or create third-epoch "
    "launch provenance."
)


def _adoption_candidate_summary(
    edge_result: ChromiumResearchThirdChangedBasisRootEdgeResult,
) -> str:
    root_result = edge_result.root_result
    return (
        "THIRD CHANGED-BASIS LINEAGE READY FOR EXPLICIT SHELL ADOPTION\n"
        f"Third root SHA-256: {root_result.persistence.root_record_sha256}\n"
        f"First post-third-root edge SHA-256: {edge_result.persistence.edge_record_sha256}\n"
        f"Edge output location receipt: {edge_result.persistence.path}\n"
        "Candidate governed endpoint rationale:\n"
        f"{edge_result.loaded_edge.revision.revised_note.note_text}\n"
        "The edge location above is receipt context only. The current edge locator below "
        "remains blank and explicit. The third public-34A root is already the exact loaded "
        "sequence-start record and is not rediscovered through a path."
    )


def third_changed_basis_session_adoption_success_receipt(
    result: ChromiumResearchThirdChangedBasisSessionAdoptionResult,
) -> str:
    return (
        "Success — third changed-basis lineage explicitly adopted as this shell's governed session.\n"
        f"Declaration SHA-256: {result.declaration.sequence_record_sha256}\n"
        f"Declaration destination: {result.declaration.path}\n"
        f"Third root SHA-256: {result.edge_result.root_result.persistence.root_record_sha256}\n"
        f"Governed endpoint edge SHA-256: {result.edge_result.persistence.edge_record_sha256}\n"
        "Governed endpoint rationale:\n"
        f"{result.controller.declared_endpoint.revision.revised_note.note_text}\n"
        "This is an explicit shell-local adoption only. No 40A third-epoch fresh-process "
        "re-entry, 40B overlay, third-epoch launch provenance, or global current/latest/head "
        "authority was created."
    )


class ResearchThirdChangedBasisSessionAdoptionControls(Vertical):
    """Explicit 47D controls for one third-root-backed governed-session adoption."""

    def __init__(
        self,
        edge_result: ChromiumResearchThirdChangedBasisRootEdgeResult,
        prior_result: ChromiumResearchThirdChangedBasisSessionAdoptionResult | None = None,
    ) -> None:
        if type(edge_result) is not ChromiumResearchThirdChangedBasisRootEdgeResult:
            raise TypeError(
                "edge_result must be exactly ChromiumResearchThirdChangedBasisRootEdgeResult."
            )
        if prior_result is not None and prior_result.edge_result is not edge_result:
            raise ValueError(
                "Prior third changed-basis adoption does not belong to this exact 47C edge."
            )
        super().__init__(id="research-third-changed-basis-session-adoption-controls")
        self.edge_result = edge_result
        self.prior_result = prior_result

    def compose(self) -> ComposeResult:
        locked = self.prior_result is not None
        status_text = (
            third_changed_basis_session_adoption_success_receipt(self.prior_result)
            if self.prior_result is not None
            else ""
        )

        yield Static(
            "Adopt the third changed-basis governed session",
            id="research-third-changed-basis-session-adoption-title",
        )
        yield Static(
            THIRD_CHANGED_BASIS_SESSION_ADOPTION_AUTHORITY_NOTICE,
            id="research-third-changed-basis-session-adoption-authority-notice",
            markup=False,
        )
        yield Static(
            _adoption_candidate_summary(self.edge_result),
            id="research-third-changed-basis-session-adoption-summary",
            markup=False,
        )
        yield Static(
            "Current durable file for the exact first post-third-root ordinary edge",
            id="research-third-changed-basis-session-adoption-edge-source-label",
        )
        yield Input(
            placeholder="Explicit current first post-third-root edge path",
            id="research-third-changed-basis-session-adoption-edge-source",
            disabled=locked,
        )
        yield Static(
            "No-overwrite destination for the third-root-backed session declaration",
            id="research-third-changed-basis-session-adoption-declaration-destination-label",
        )
        yield Input(
            placeholder="Explicit third-root-backed declaration destination path",
            id="research-third-changed-basis-session-adoption-declaration-destination",
            disabled=locked,
        )
        yield Button(
            "Adopt third changed-basis session — active governed branch will change",
            id="adopt-research-third-changed-basis-session",
            variant="warning",
            disabled=locked,
        )
        yield Static(
            status_text,
            id="research-third-changed-basis-session-adoption-status",
            markup=False,
        )

    def lock_after_success(
        self,
        result: ChromiumResearchThirdChangedBasisSessionAdoptionResult,
    ) -> None:
        """Lock one exact 47C candidate after its successful 47D adoption."""

        if result.edge_result is not self.edge_result:
            raise ValueError(
                "Third changed-basis adoption result does not retain this exact 47C edge."
            )
        self.prior_result = result
        for widget_id in (
            "#research-third-changed-basis-session-adoption-edge-source",
            "#research-third-changed-basis-session-adoption-declaration-destination",
        ):
            self.query_one(widget_id, Input).disabled = True
        self.query_one(
            "#adopt-research-third-changed-basis-session", Button
        ).disabled = True
        self.query_one(
            "#research-third-changed-basis-session-adoption-status", Static
        ).update(third_changed_basis_session_adoption_success_receipt(result))


__all__ = [
    "THIRD_CHANGED_BASIS_SESSION_ADOPTION_AUTHORITY_NOTICE",
    "ResearchThirdChangedBasisSessionAdoptionControls",
    "third_changed_basis_session_adoption_success_receipt",
]
