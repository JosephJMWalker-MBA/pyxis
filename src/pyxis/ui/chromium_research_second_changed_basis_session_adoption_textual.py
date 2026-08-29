from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Input, Static

from pyxis.app.chromium_research_second_changed_basis_root_edge import (
    ChromiumResearchSecondChangedBasisRootEdgeResult,
)
from pyxis.app.chromium_research_second_changed_basis_session_adoption import (
    ChromiumResearchSecondChangedBasisSessionAdoptionResult,
)


SECOND_CHANGED_BASIS_SESSION_ADOPTION_AUTHORITY_NOTICE = (
    "This explicitly adopts the displayed second changed-basis lineage as this shell's "
    "governed research session by creating and freshly relinking an existing-format "
    "root-started declaration. The action changes this shell's active controller. It "
    "does not establish global current/latest/head authority, infer chronology, create "
    "second-epoch fresh-process re-entry, or persist a second-epoch overlay."
)


def _adoption_candidate_summary(
    edge_result: ChromiumResearchSecondChangedBasisRootEdgeResult,
) -> str:
    root_result = edge_result.root_result
    return (
        "SECOND CHANGED-BASIS LINEAGE READY FOR EXPLICIT SHELL ADOPTION\n"
        f"Second root SHA-256: {root_result.persistence.root_record_sha256}\n"
        f"First post-second-root edge SHA-256: {edge_result.persistence.edge_record_sha256}\n"
        f"Edge output location receipt: {edge_result.persistence.path}\n"
        "Candidate governed endpoint rationale:\n"
        f"{edge_result.loaded_edge.revision.revised_note.note_text}\n"
        "The edge location above is receipt context only. The current edge locator below "
        "remains blank and explicit. The second 34A root is already the exact loaded "
        "sequence-start record and is not rediscovered through a path."
    )


def second_changed_basis_session_adoption_success_receipt(
    result: ChromiumResearchSecondChangedBasisSessionAdoptionResult,
) -> str:
    return (
        "Success — second changed-basis lineage explicitly adopted as this shell's governed session.\n"
        f"Declaration SHA-256: {result.declaration.sequence_record_sha256}\n"
        f"Declaration destination: {result.declaration.path}\n"
        f"Second root SHA-256: {result.edge_result.root_result.persistence.root_record_sha256}\n"
        f"Governed endpoint edge SHA-256: {result.edge_result.persistence.edge_record_sha256}\n"
        "Governed endpoint rationale:\n"
        f"{result.controller.declared_endpoint.revision.revised_note.note_text}\n"
        "This is an explicit shell-local branch adoption only. No second-epoch fresh-process "
        "re-entry/overlay and no global current/latest/head authority were created."
    )


class ResearchSecondChangedBasisSessionAdoptionControls(Vertical):
    """Explicit 46D controls for one second-root-backed governed-session adoption."""

    def __init__(
        self,
        edge_result: ChromiumResearchSecondChangedBasisRootEdgeResult,
        prior_result: ChromiumResearchSecondChangedBasisSessionAdoptionResult | None = None,
    ) -> None:
        if type(edge_result) is not ChromiumResearchSecondChangedBasisRootEdgeResult:
            raise TypeError(
                "edge_result must be exactly ChromiumResearchSecondChangedBasisRootEdgeResult."
            )
        if prior_result is not None and prior_result.edge_result is not edge_result:
            raise ValueError(
                "Prior second changed-basis adoption does not belong to this exact 46C edge."
            )
        super().__init__(id="research-second-changed-basis-session-adoption-controls")
        self.edge_result = edge_result
        self.prior_result = prior_result

    def compose(self) -> ComposeResult:
        locked = self.prior_result is not None
        status_text = (
            second_changed_basis_session_adoption_success_receipt(self.prior_result)
            if self.prior_result is not None
            else ""
        )

        yield Static(
            "Adopt the second changed-basis governed session",
            id="research-second-changed-basis-session-adoption-title",
        )
        yield Static(
            SECOND_CHANGED_BASIS_SESSION_ADOPTION_AUTHORITY_NOTICE,
            id="research-second-changed-basis-session-adoption-authority-notice",
            markup=False,
        )
        yield Static(
            _adoption_candidate_summary(self.edge_result),
            id="research-second-changed-basis-session-adoption-summary",
            markup=False,
        )
        yield Static(
            "Current durable file for the exact first post-second-root ordinary edge",
            id="research-second-changed-basis-session-adoption-edge-source-label",
        )
        yield Input(
            placeholder="Explicit current first post-second-root edge path",
            id="research-second-changed-basis-session-adoption-edge-source",
            disabled=locked,
        )
        yield Static(
            "No-overwrite destination for the second-root-backed session declaration",
            id="research-second-changed-basis-session-adoption-declaration-destination-label",
        )
        yield Input(
            placeholder="Explicit second-root-backed declaration destination path",
            id="research-second-changed-basis-session-adoption-declaration-destination",
            disabled=locked,
        )
        yield Button(
            "Adopt second changed-basis session — active governed branch will change",
            id="adopt-research-second-changed-basis-session",
            variant="warning",
            disabled=locked,
        )
        yield Static(
            status_text,
            id="research-second-changed-basis-session-adoption-status",
            markup=False,
        )

    def lock_after_success(
        self,
        result: ChromiumResearchSecondChangedBasisSessionAdoptionResult,
    ) -> None:
        """Lock one exact 46C candidate after its successful 46D adoption."""

        if result.edge_result is not self.edge_result:
            raise ValueError(
                "Second changed-basis adoption result does not retain this exact 46C edge."
            )
        self.prior_result = result
        for widget_id in (
            "#research-second-changed-basis-session-adoption-edge-source",
            "#research-second-changed-basis-session-adoption-declaration-destination",
        ):
            self.query_one(widget_id, Input).disabled = True
        self.query_one(
            "#adopt-research-second-changed-basis-session", Button
        ).disabled = True
        self.query_one(
            "#research-second-changed-basis-session-adoption-status", Static
        ).update(second_changed_basis_session_adoption_success_receipt(result))


__all__ = [
    "SECOND_CHANGED_BASIS_SESSION_ADOPTION_AUTHORITY_NOTICE",
    "ResearchSecondChangedBasisSessionAdoptionControls",
    "second_changed_basis_session_adoption_success_receipt",
]
