from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Input, Static, TextArea

from pyxis.app.chromium_research_first_changed_basis_revision_root import (
    ChromiumResearchFirstChangedBasisRevisionRootResult,
)
from pyxis.app.chromium_research_first_changed_basis_root_edge import (
    ChromiumResearchFirstChangedBasisRootEdgeResult,
)


FIRST_CHANGED_BASIS_ROOT_EDGE_AUTHORITY_NOTICE = (
    "This creates the one-time first ordinary revision edge after the persisted 34A "
    "changed-basis root. Saving resumes local ordinary edge lineage only. It does not "
    "declare a sequence, create/adopt a root-backed governed session, create an epoch, "
    "select current/latest/head state, or grant semantic-support authority."
)


def _root_summary(root_result: ChromiumResearchFirstChangedBasisRevisionRootResult) -> str:
    return (
        "PERSISTED FIRST CHANGED-BASIS ROOT — NO ROOT-BACKED SESSION YET\n"
        f"Root SHA-256: {root_result.persistence.root_record_sha256}\n"
        f"Root output location receipt: {root_result.persistence.path}\n"
        "Root endpoint rationale:\n"
        f"{root_result.loaded_root.root.revision.revised_note.note_text}\n"
        "The location above is receipt context only. The current-root locator below "
        "remains blank and explicit so moved durable files are never inferred."
    )


def first_changed_basis_root_edge_success_receipt(
    result: ChromiumResearchFirstChangedBasisRootEdgeResult,
) -> str:
    return (
        "Success — first post-root ordinary edge persisted and freshly relinked. "
        "Mounted governed session unchanged.\n"
        f"Edge SHA-256: {result.persistence.edge_record_sha256}\n"
        f"Edge destination: {result.persistence.path}\n"
        f"Retained root SHA-256: {result.persistence.root_verification.root_record_sha256}\n"
        "Revised rationale:\n"
        f"{result.loaded_edge.revision.revised_note.note_text}\n"
        "Ordinary edge lineage has resumed locally, but no sequence declaration, 35A "
        "root-backed governed session/adoption, epoch, or current/latest/head state was created."
    )


class ResearchFirstChangedBasisRootEdgeControls(Vertical):
    """Explicit 44D controls for the one-time 34A-root → ordinary-edge bridge."""

    def __init__(
        self,
        root_result: ChromiumResearchFirstChangedBasisRevisionRootResult,
        prior_result: ChromiumResearchFirstChangedBasisRootEdgeResult | None = None,
    ) -> None:
        if type(root_result) is not ChromiumResearchFirstChangedBasisRevisionRootResult:
            raise TypeError(
                "root_result must be exactly ChromiumResearchFirstChangedBasisRevisionRootResult."
            )
        if prior_result is not None and prior_result.root_result is not root_result:
            raise ValueError(
                "Prior first post-root edge does not belong to this exact 44C root."
            )
        super().__init__(id="research-first-changed-basis-root-edge-controls")
        self.root_result = root_result
        self.prior_result = prior_result

    def compose(self) -> ComposeResult:
        locked = self.prior_result is not None
        status_text = (
            first_changed_basis_root_edge_success_receipt(self.prior_result)
            if self.prior_result is not None
            else ""
        )

        yield Static(
            "Continue from the changed-basis root",
            id="research-first-changed-basis-root-edge-title",
        )
        yield Static(
            FIRST_CHANGED_BASIS_ROOT_EDGE_AUTHORITY_NOTICE,
            id="research-first-changed-basis-root-edge-authority-notice",
            markup=False,
        )
        yield Static(
            _root_summary(self.root_result),
            id="research-first-changed-basis-root-edge-root-summary",
            markup=False,
        )
        yield Static(
            "New human rationale after the root",
            id="research-first-changed-basis-root-edge-rationale-label",
        )
        yield TextArea(
            "",
            id="research-first-changed-basis-root-edge-rationale",
            disabled=locked,
        )
        yield Static(
            "Current durable file for the exact 34A root",
            id="research-first-changed-basis-root-edge-root-source-label",
        )
        yield Input(
            placeholder="Explicit current root path",
            id="research-first-changed-basis-root-edge-root-source",
            disabled=locked,
        )
        yield Static(
            "No-overwrite destination for the first post-root ordinary edge",
            id="research-first-changed-basis-root-edge-destination-label",
        )
        yield Input(
            placeholder="Explicit first post-root edge destination path",
            id="research-first-changed-basis-root-edge-destination",
            disabled=locked,
        )
        yield Button(
            "Persist first post-root ordinary edge — session will not advance",
            id="persist-research-first-changed-basis-root-edge",
            variant="warning",
            disabled=locked,
        )
        yield Static(
            status_text,
            id="research-first-changed-basis-root-edge-status",
            markup=False,
        )

    def lock_after_success(
        self,
        result: ChromiumResearchFirstChangedBasisRootEdgeResult,
    ) -> None:
        """Lock the exact 44C root after one successful 44D edge."""

        if result.root_result is not self.root_result:
            raise ValueError(
                "First post-root edge result does not retain this exact 44C root."
            )
        self.prior_result = result
        self.query_one(
            "#research-first-changed-basis-root-edge-rationale", TextArea
        ).disabled = True
        for widget_id in (
            "#research-first-changed-basis-root-edge-root-source",
            "#research-first-changed-basis-root-edge-destination",
        ):
            self.query_one(widget_id, Input).disabled = True
        self.query_one(
            "#persist-research-first-changed-basis-root-edge", Button
        ).disabled = True
        self.query_one(
            "#research-first-changed-basis-root-edge-status", Static
        ).update(first_changed_basis_root_edge_success_receipt(result))


__all__ = [
    "FIRST_CHANGED_BASIS_ROOT_EDGE_AUTHORITY_NOTICE",
    "ResearchFirstChangedBasisRootEdgeControls",
    "first_changed_basis_root_edge_success_receipt",
]
