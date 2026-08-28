from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Input, Static

from pyxis.app.chromium_research_first_changed_basis_root_edge import (
    ChromiumResearchFirstChangedBasisRootEdgeResult,
)
from pyxis.app.chromium_research_first_changed_basis_session_adoption import (
    ChromiumResearchFirstChangedBasisSessionAdoptionResult,
)


FIRST_CHANGED_BASIS_SESSION_ADOPTION_AUTHORITY_NOTICE = (
    "This explicitly adopts the displayed changed-basis lineage as this shell's governed "
    "research session by creating and freshly relinking an existing-format root-started "
    "declaration. The action changes this shell's active controller. It does not establish "
    "a global current/latest/head branch, infer chronology, or create fresh-process "
    "root-backed restart authority."
)


def _adoption_candidate_summary(
    edge_result: ChromiumResearchFirstChangedBasisRootEdgeResult,
) -> str:
    root_result = edge_result.root_result
    return (
        "CHANGED-BASIS LINEAGE READY FOR EXPLICIT SHELL ADOPTION\n"
        f"Root SHA-256: {root_result.persistence.root_record_sha256}\n"
        f"First edge SHA-256: {edge_result.persistence.edge_record_sha256}\n"
        f"First-edge output location receipt: {edge_result.persistence.path}\n"
        "Candidate governed endpoint rationale:\n"
        f"{edge_result.loaded_edge.revision.revised_note.note_text}\n"
        "The edge location above is receipt context only. The current edge locator below "
        "remains blank and explicit. The 34A root is already the exact loaded sequence-start "
        "record and is not rediscovered through a path."
    )


def first_changed_basis_session_adoption_success_receipt(
    result: ChromiumResearchFirstChangedBasisSessionAdoptionResult,
) -> str:
    return (
        "Success — changed-basis lineage explicitly adopted as this shell's governed session.\n"
        f"Declaration SHA-256: {result.declaration.sequence_record_sha256}\n"
        f"Declaration destination: {result.declaration.path}\n"
        f"Root SHA-256: {result.edge_result.root_result.persistence.root_record_sha256}\n"
        f"Governed endpoint edge SHA-256: {result.edge_result.persistence.edge_record_sha256}\n"
        "Governed endpoint rationale:\n"
        f"{result.controller.declared_endpoint.revision.revised_note.note_text}\n"
        "This is an explicit shell-local branch adoption only. No global current/latest/head "
        "authority and no 35B fresh-process root-backed restart authority were created."
    )


class ResearchFirstChangedBasisSessionAdoptionControls(Vertical):
    """Explicit 44E controls for one 35A root-backed governed-session adoption."""

    def __init__(
        self,
        edge_result: ChromiumResearchFirstChangedBasisRootEdgeResult,
        prior_result: ChromiumResearchFirstChangedBasisSessionAdoptionResult | None = None,
    ) -> None:
        if type(edge_result) is not ChromiumResearchFirstChangedBasisRootEdgeResult:
            raise TypeError(
                "edge_result must be exactly ChromiumResearchFirstChangedBasisRootEdgeResult."
            )
        if prior_result is not None and prior_result.edge_result is not edge_result:
            raise ValueError(
                "Prior changed-basis adoption does not belong to this exact 44D edge."
            )
        super().__init__(id="research-first-changed-basis-session-adoption-controls")
        self.edge_result = edge_result
        self.prior_result = prior_result

    def compose(self) -> ComposeResult:
        locked = self.prior_result is not None
        status_text = (
            first_changed_basis_session_adoption_success_receipt(self.prior_result)
            if self.prior_result is not None
            else ""
        )

        yield Static(
            "Adopt the changed-basis governed session",
            id="research-first-changed-basis-session-adoption-title",
        )
        yield Static(
            FIRST_CHANGED_BASIS_SESSION_ADOPTION_AUTHORITY_NOTICE,
            id="research-first-changed-basis-session-adoption-authority-notice",
            markup=False,
        )
        yield Static(
            _adoption_candidate_summary(self.edge_result),
            id="research-first-changed-basis-session-adoption-summary",
            markup=False,
        )
        yield Static(
            "Current durable file for the exact first post-root ordinary edge",
            id="research-first-changed-basis-session-adoption-edge-source-label",
        )
        yield Input(
            placeholder="Explicit current first-edge path",
            id="research-first-changed-basis-session-adoption-edge-source",
            disabled=locked,
        )
        yield Static(
            "No-overwrite destination for the root-backed session declaration",
            id="research-first-changed-basis-session-adoption-declaration-destination-label",
        )
        yield Input(
            placeholder="Explicit root-backed declaration destination path",
            id="research-first-changed-basis-session-adoption-declaration-destination",
            disabled=locked,
        )
        yield Button(
            "Adopt changed-basis session — active governed branch will change",
            id="adopt-research-first-changed-basis-session",
            variant="warning",
            disabled=locked,
        )
        yield Static(
            status_text,
            id="research-first-changed-basis-session-adoption-status",
            markup=False,
        )

    def lock_after_success(
        self,
        result: ChromiumResearchFirstChangedBasisSessionAdoptionResult,
    ) -> None:
        """Lock one exact 44D candidate after its successful 44E adoption."""

        if result.edge_result is not self.edge_result:
            raise ValueError(
                "Changed-basis adoption result does not retain this exact 44D edge."
            )
        self.prior_result = result
        for widget_id in (
            "#research-first-changed-basis-session-adoption-edge-source",
            "#research-first-changed-basis-session-adoption-declaration-destination",
        ):
            self.query_one(widget_id, Input).disabled = True
        self.query_one(
            "#adopt-research-first-changed-basis-session", Button
        ).disabled = True
        self.query_one(
            "#research-first-changed-basis-session-adoption-status", Static
        ).update(first_changed_basis_session_adoption_success_receipt(result))


__all__ = [
    "FIRST_CHANGED_BASIS_SESSION_ADOPTION_AUTHORITY_NOTICE",
    "ResearchFirstChangedBasisSessionAdoptionControls",
    "first_changed_basis_session_adoption_success_receipt",
]
