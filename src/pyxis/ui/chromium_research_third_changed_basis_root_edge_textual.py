from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Input, Static, TextArea

from pyxis.app.chromium_research_third_changed_basis_revision_root import (
    ChromiumResearchThirdChangedBasisRevisionRootResult,
)
from pyxis.app.chromium_research_third_changed_basis_root_edge import (
    ChromiumResearchThirdChangedBasisRootEdgeResult,
)


THIRD_CHANGED_BASIS_ROOT_EDGE_AUTHORITY_NOTICE = (
    "This creates the one-time first ordinary revision edge after the exact persisted "
    "47B/public-34A third changed-basis root. Saving resumes local ordinary edge "
    "lineage only. It does not declare a root-started sequence, create/adopt a "
    "third-epoch governed session, create re-entry/restart authority, select "
    "current/latest/head state, or grant semantic-support authority."
)


def _root_summary(root_result: ChromiumResearchThirdChangedBasisRevisionRootResult) -> str:
    return (
        "PERSISTED THIRD CHANGED-BASIS ROOT — NO THIRD-EPOCH SESSION YET\n"
        f"Root SHA-256: {root_result.persistence.root_record_sha256}\n"
        f"Root output location receipt: {root_result.persistence.path}\n"
        "Root endpoint rationale:\n"
        f"{root_result.loaded_root.root.revision.revised_note.note_text}\n"
        "The location above is receipt context only. The current-root locator below "
        "remains blank and explicit so moved durable files are never inferred."
    )


def third_changed_basis_root_edge_success_receipt(
    result: ChromiumResearchThirdChangedBasisRootEdgeResult,
) -> str:
    return (
        "Success — first post-third-root ordinary edge persisted and freshly relinked. "
        "Mounted second-epoch continuation unchanged.\n"
        f"Edge SHA-256: {result.persistence.edge_record_sha256}\n"
        f"Edge destination: {result.persistence.path}\n"
        f"Retained third-root SHA-256: "
        f"{result.persistence.root_verification.root_record_sha256}\n"
        "Revised rationale:\n"
        f"{result.loaded_edge.revision.revised_note.note_text}\n"
        "Ordinary edge lineage has resumed locally, but no root-started sequence "
        "declaration, third-epoch session/re-entry/restart/adoption, or "
        "current/latest/head state was created."
    )


class ResearchThirdChangedBasisRootEdgeControls(Vertical):
    """Explicit 47C controls for the one-time 47B-root → ordinary-edge bridge."""

    def __init__(
        self,
        root_result: ChromiumResearchThirdChangedBasisRevisionRootResult,
        prior_result: ChromiumResearchThirdChangedBasisRootEdgeResult | None = None,
    ) -> None:
        if type(root_result) is not ChromiumResearchThirdChangedBasisRevisionRootResult:
            raise TypeError(
                "root_result must be exactly "
                "ChromiumResearchThirdChangedBasisRevisionRootResult."
            )
        if prior_result is not None and prior_result.root_result is not root_result:
            raise ValueError(
                "Prior post-third-root edge does not belong to this exact 47B root."
            )
        super().__init__(id="research-third-changed-basis-root-edge-controls")
        self.root_result = root_result
        self.prior_result = prior_result

    def compose(self) -> ComposeResult:
        locked = self.prior_result is not None
        status_text = (
            third_changed_basis_root_edge_success_receipt(self.prior_result)
            if self.prior_result is not None
            else ""
        )

        yield Static(
            "Continue locally from the third changed-basis root",
            id="research-third-changed-basis-root-edge-title",
        )
        yield Static(
            THIRD_CHANGED_BASIS_ROOT_EDGE_AUTHORITY_NOTICE,
            id="research-third-changed-basis-root-edge-authority-notice",
            markup=False,
        )
        yield Static(
            _root_summary(self.root_result),
            id="research-third-changed-basis-root-edge-root-summary",
            markup=False,
        )
        yield Static(
            "New human rationale after the third root",
            id="research-third-changed-basis-root-edge-rationale-label",
        )
        yield TextArea(
            "",
            id="research-third-changed-basis-root-edge-rationale",
            disabled=locked,
        )
        yield Static(
            "Current durable file for the exact 47B/public-34A third root",
            id="research-third-changed-basis-root-edge-root-source-label",
        )
        yield Input(
            placeholder="Explicit current third-root path",
            id="research-third-changed-basis-root-edge-root-source",
            disabled=locked,
        )
        yield Static(
            "No-overwrite destination for the first post-third-root ordinary edge",
            id="research-third-changed-basis-root-edge-destination-label",
        )
        yield Input(
            placeholder="Explicit first post-third-root edge destination path",
            id="research-third-changed-basis-root-edge-destination",
            disabled=locked,
        )
        yield Button(
            "Persist first post-third-root ordinary edge — continuation will not advance",
            id="persist-research-third-changed-basis-root-edge",
            variant="warning",
            disabled=locked,
        )
        yield Static(
            status_text,
            id="research-third-changed-basis-root-edge-status",
            markup=False,
        )

    def lock_after_success(
        self,
        result: ChromiumResearchThirdChangedBasisRootEdgeResult,
    ) -> None:
        """Lock the exact 47B root after one successful 47C edge."""

        if result.root_result is not self.root_result:
            raise ValueError(
                "Post-third-root edge result does not retain this exact 47B root."
            )
        self.prior_result = result
        self.query_one(
            "#research-third-changed-basis-root-edge-rationale", TextArea
        ).disabled = True
        for widget_id in (
            "#research-third-changed-basis-root-edge-root-source",
            "#research-third-changed-basis-root-edge-destination",
        ):
            self.query_one(widget_id, Input).disabled = True
        self.query_one(
            "#persist-research-third-changed-basis-root-edge", Button
        ).disabled = True
        self.query_one(
            "#research-third-changed-basis-root-edge-status", Static
        ).update(third_changed_basis_root_edge_success_receipt(result))


__all__ = [
    "THIRD_CHANGED_BASIS_ROOT_EDGE_AUTHORITY_NOTICE",
    "ResearchThirdChangedBasisRootEdgeControls",
    "third_changed_basis_root_edge_success_receipt",
]
