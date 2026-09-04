from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Input, Static, TextArea

from pyxis.app.chromium_research_third_changed_basis_revision_root import (
    ChromiumResearchThirdChangedBasisRevisionRootResult,
)
from pyxis.app.chromium_research_third_changed_basis_transition import (
    ChromiumResearchThirdChangedBasisTransitionResult,
)


THIRD_CHANGED_BASIS_REVISION_ROOT_AUTHORITY_NOTICE = (
    "This creates one human-authored public-34A third revision root over the exact "
    "persisted 47A/33B changed-basis transition. Saving does not create the first "
    "ordinary post-root edge, a third-epoch declaration/session, 40A re-entry, 40B "
    "restart overlay, current/latest/head state, or semantic-support authority. The "
    "mounted second-epoch continuation does not advance."
)


def _transition_summary(
    transition_result: ChromiumResearchThirdChangedBasisTransitionResult,
) -> str:
    loaded = transition_result.loaded_transition
    return (
        "PERSISTED THIRD CHANGED-BASIS TRANSITION — NOT YET ROOTED / NOT ADOPTED\n"
        f"Transition SHA-256: {transition_result.persistence.transition_record_sha256}\n"
        f"Transition output location: {transition_result.persistence.path}\n"
        "Successor working-set SHA-256: "
        f"{loaded.successor_note.working_set.verification.working_set_record_sha256}\n"
        f"Successor note SHA-256: {loaded.successor_note.verification.note_record_sha256}\n"
        f"Successor note text:\n{loaded.successor_note.note.note_text}\n"
        "The locations above are receipts only. Root locator inputs below remain blank "
        "and explicit; no location is inferred or treated as identity authority."
    )


def third_changed_basis_revision_root_success_receipt(
    result: ChromiumResearchThirdChangedBasisRevisionRootResult,
) -> str:
    return (
        "Success — third changed-basis public-34A revision root persisted and freshly "
        "relinked. Mounted second-epoch continuation unchanged.\n"
        f"Root SHA-256: {result.persistence.root_record_sha256}\n"
        f"Root destination: {result.persistence.path}\n"
        "Retained third-transition SHA-256: "
        f"{result.loaded_root.transition.verification.transition_record_sha256}\n"
        f"Human revised rationale:\n{result.loaded_root.root.revision.revised_note.note_text}\n"
        "No first post-root edge, third-epoch declaration/session, 40A/40B re-entry or "
        "restart, adoption, or current/latest/head state was created."
    )


class ResearchThirdChangedBasisRevisionRootControls(Vertical):
    """Explicit 47B controls for one human public-34A root after exact 47A success."""

    def __init__(
        self,
        transition_result: ChromiumResearchThirdChangedBasisTransitionResult,
        prior_result: ChromiumResearchThirdChangedBasisRevisionRootResult | None = None,
    ) -> None:
        if type(transition_result) is not ChromiumResearchThirdChangedBasisTransitionResult:
            raise TypeError(
                "transition_result must be exactly ChromiumResearchThirdChangedBasisTransitionResult."
            )
        if prior_result is not None and prior_result.transition_result is not transition_result:
            raise ValueError(
                "Prior third changed-basis root does not belong to this exact transition result."
            )
        super().__init__(id="research-third-changed-basis-revision-root-controls")
        self.transition_result = transition_result
        self.prior_result = prior_result

    def compose(self) -> ComposeResult:
        locked = self.prior_result is not None
        status_text = (
            third_changed_basis_revision_root_success_receipt(self.prior_result)
            if self.prior_result is not None
            else ""
        )

        yield Static(
            "Author first rationale revision after the third evidence-basis change",
            id="research-third-changed-basis-revision-root-title",
        )
        yield Static(
            THIRD_CHANGED_BASIS_REVISION_ROOT_AUTHORITY_NOTICE,
            id="research-third-changed-basis-revision-root-authority-notice",
            markup=False,
        )
        yield Static(
            _transition_summary(self.transition_result),
            id="research-third-changed-basis-revision-root-transition-summary",
            markup=False,
        )
        yield Static(
            "New human rationale — must differ exactly from the third-transition successor note",
            id="research-third-changed-basis-revision-root-rationale-label",
        )
        yield TextArea(
            "",
            id="research-third-changed-basis-revision-root-rationale",
            disabled=locked,
        )
        yield Static(
            "Durable prior endpoint edge source",
            id="research-third-changed-basis-revision-root-prior-edge-source-label",
        )
        yield Input(
            placeholder="Explicit prior endpoint edge path",
            id="research-third-changed-basis-revision-root-prior-edge-source",
            disabled=locked,
        )
        yield Static(
            "Durable changed working-set source",
            id="research-third-changed-basis-revision-root-working-set-source-label",
        )
        yield Input(
            placeholder="Explicit changed working-set path",
            id="research-third-changed-basis-revision-root-working-set-source",
            disabled=locked,
        )
        yield Static(
            "Durable changed working-set-note source",
            id="research-third-changed-basis-revision-root-note-source-label",
        )
        yield Input(
            placeholder="Explicit changed working-set-note path",
            id="research-third-changed-basis-revision-root-note-source",
            disabled=locked,
        )
        yield Static(
            "Durable third changed-basis transition source",
            id="research-third-changed-basis-revision-root-transition-source-label",
        )
        yield Input(
            placeholder="Explicit 47A/33B third-transition path",
            id="research-third-changed-basis-revision-root-transition-source",
            disabled=locked,
        )
        yield Static(
            "No-overwrite destination for the third changed-basis revision root",
            id="research-third-changed-basis-revision-root-destination-label",
        )
        yield Input(
            placeholder="Explicit third public-34A root destination path",
            id="research-third-changed-basis-revision-root-destination",
            disabled=locked,
        )
        yield Button(
            "Persist third changed-basis revision root — continuation will not advance",
            id="persist-research-third-changed-basis-revision-root",
            variant="warning",
            disabled=locked,
        )
        yield Static(
            status_text,
            id="research-third-changed-basis-revision-root-status",
            markup=False,
        )

    def lock_after_success(
        self,
        result: ChromiumResearchThirdChangedBasisRevisionRootResult,
    ) -> None:
        """Lock this exact 47A transition after one successful 47B public-34A root."""

        if result.transition_result is not self.transition_result:
            raise ValueError(
                "Third changed-basis root result does not retain this exact 47A transition."
            )
        self.prior_result = result
        self.query_one(
            "#research-third-changed-basis-revision-root-rationale", TextArea
        ).disabled = True
        for widget_id in (
            "#research-third-changed-basis-revision-root-prior-edge-source",
            "#research-third-changed-basis-revision-root-working-set-source",
            "#research-third-changed-basis-revision-root-note-source",
            "#research-third-changed-basis-revision-root-transition-source",
            "#research-third-changed-basis-revision-root-destination",
        ):
            self.query_one(widget_id, Input).disabled = True
        self.query_one(
            "#persist-research-third-changed-basis-revision-root", Button
        ).disabled = True
        self.query_one(
            "#research-third-changed-basis-revision-root-status", Static
        ).update(third_changed_basis_revision_root_success_receipt(result))


__all__ = [
    "ResearchThirdChangedBasisRevisionRootControls",
    "THIRD_CHANGED_BASIS_REVISION_ROOT_AUTHORITY_NOTICE",
    "third_changed_basis_revision_root_success_receipt",
]
