from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Input, Static, TextArea

from pyxis.app.chromium_research_second_changed_basis_revision_root import (
    ChromiumResearchSecondChangedBasisRevisionRootResult,
)
from pyxis.app.chromium_research_second_changed_basis_root_edge import (
    ChromiumResearchSecondChangedBasisRootEdgeResult,
)


SECOND_CHANGED_BASIS_ROOT_EDGE_AUTHORITY_NOTICE = (
    "This creates the one-time first ordinary revision edge after the exact persisted "
    "46B/34A second changed-basis root. Saving resumes local ordinary edge lineage "
    "only. It does not declare a sequence, create/adopt a second-epoch session, create "
    "re-entry authority, select current/latest/head state, or grant semantic-support "
    "authority."
)


def _root_summary(root_result: ChromiumResearchSecondChangedBasisRevisionRootResult) -> str:
    return (
        "PERSISTED SECOND CHANGED-BASIS ROOT — NO SECOND-EPOCH SESSION YET\n"
        f"Root SHA-256: {root_result.persistence.root_record_sha256}\n"
        f"Root output location receipt: {root_result.persistence.path}\n"
        "Root endpoint rationale:\n"
        f"{root_result.loaded_root.root.revision.revised_note.note_text}\n"
        "The location above is receipt context only. The current-root locator below "
        "remains blank and explicit so moved durable files are never inferred."
    )


def second_changed_basis_root_edge_success_receipt(
    result: ChromiumResearchSecondChangedBasisRootEdgeResult,
) -> str:
    return (
        "Success — first post-second-root ordinary edge persisted and freshly relinked. "
        "Mounted one-root continuation unchanged.\n"
        f"Edge SHA-256: {result.persistence.edge_record_sha256}\n"
        f"Edge destination: {result.persistence.path}\n"
        f"Retained second-root SHA-256: {result.persistence.root_verification.root_record_sha256}\n"
        "Revised rationale:\n"
        f"{result.loaded_edge.revision.revised_note.note_text}\n"
        "Ordinary edge lineage has resumed locally, but no sequence declaration, "
        "second-epoch session/re-entry/adoption, or current/latest/head state was created."
    )


class ResearchSecondChangedBasisRootEdgeControls(Vertical):
    """Explicit 46C controls for the one-time 46B-root → ordinary-edge bridge."""

    def __init__(
        self,
        root_result: ChromiumResearchSecondChangedBasisRevisionRootResult,
        prior_result: ChromiumResearchSecondChangedBasisRootEdgeResult | None = None,
    ) -> None:
        if type(root_result) is not ChromiumResearchSecondChangedBasisRevisionRootResult:
            raise TypeError(
                "root_result must be exactly "
                "ChromiumResearchSecondChangedBasisRevisionRootResult."
            )
        if prior_result is not None and prior_result.root_result is not root_result:
            raise ValueError(
                "Prior post-second-root edge does not belong to this exact 46B root."
            )
        super().__init__(id="research-second-changed-basis-root-edge-controls")
        self.root_result = root_result
        self.prior_result = prior_result

    def compose(self) -> ComposeResult:
        locked = self.prior_result is not None
        status_text = (
            second_changed_basis_root_edge_success_receipt(self.prior_result)
            if self.prior_result is not None
            else ""
        )

        yield Static(
            "Continue locally from the second changed-basis root",
            id="research-second-changed-basis-root-edge-title",
        )
        yield Static(
            SECOND_CHANGED_BASIS_ROOT_EDGE_AUTHORITY_NOTICE,
            id="research-second-changed-basis-root-edge-authority-notice",
            markup=False,
        )
        yield Static(
            _root_summary(self.root_result),
            id="research-second-changed-basis-root-edge-root-summary",
            markup=False,
        )
        yield Static(
            "New human rationale after the second root",
            id="research-second-changed-basis-root-edge-rationale-label",
        )
        yield TextArea(
            "",
            id="research-second-changed-basis-root-edge-rationale",
            disabled=locked,
        )
        yield Static(
            "Current durable file for the exact 46B/34A second root",
            id="research-second-changed-basis-root-edge-root-source-label",
        )
        yield Input(
            placeholder="Explicit current second-root path",
            id="research-second-changed-basis-root-edge-root-source",
            disabled=locked,
        )
        yield Static(
            "No-overwrite destination for the first post-second-root ordinary edge",
            id="research-second-changed-basis-root-edge-destination-label",
        )
        yield Input(
            placeholder="Explicit first post-second-root edge destination path",
            id="research-second-changed-basis-root-edge-destination",
            disabled=locked,
        )
        yield Button(
            "Persist first post-second-root ordinary edge — continuation will not advance",
            id="persist-research-second-changed-basis-root-edge",
            variant="warning",
            disabled=locked,
        )
        yield Static(
            status_text,
            id="research-second-changed-basis-root-edge-status",
            markup=False,
        )

    def lock_after_success(
        self,
        result: ChromiumResearchSecondChangedBasisRootEdgeResult,
    ) -> None:
        """Lock the exact 46B root after one successful 46C edge."""

        if result.root_result is not self.root_result:
            raise ValueError(
                "Post-second-root edge result does not retain this exact 46B root."
            )
        self.prior_result = result
        self.query_one(
            "#research-second-changed-basis-root-edge-rationale", TextArea
        ).disabled = True
        for widget_id in (
            "#research-second-changed-basis-root-edge-root-source",
            "#research-second-changed-basis-root-edge-destination",
        ):
            self.query_one(widget_id, Input).disabled = True
        self.query_one(
            "#persist-research-second-changed-basis-root-edge", Button
        ).disabled = True
        self.query_one(
            "#research-second-changed-basis-root-edge-status", Static
        ).update(second_changed_basis_root_edge_success_receipt(result))


__all__ = [
    "SECOND_CHANGED_BASIS_ROOT_EDGE_AUTHORITY_NOTICE",
    "ResearchSecondChangedBasisRootEdgeControls",
    "second_changed_basis_root_edge_success_receipt",
]
