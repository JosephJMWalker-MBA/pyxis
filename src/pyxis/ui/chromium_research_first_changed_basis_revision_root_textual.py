from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Input, Static, TextArea

from pyxis.app.chromium_research_first_changed_basis_revision_root import (
    ChromiumResearchFirstChangedBasisRevisionRootResult,
)
from pyxis.app.chromium_research_first_changed_basis_transition import (
    ChromiumResearchFirstChangedBasisTransitionResult,
)


FIRST_CHANGED_BASIS_REVISION_ROOT_AUTHORITY_NOTICE = (
    "This creates the first human-authored 34A revision root over the exact persisted "
    "33B changed-basis transition. Saving does not create the 34B first ordinary edge, "
    "a root-backed declared session, an epoch, current/latest/head state, or semantic-"
    "support authority. The mounted governed session does not advance."
)


def _transition_summary(
    transition_result: ChromiumResearchFirstChangedBasisTransitionResult,
) -> str:
    loaded = transition_result.loaded_transition
    return (
        "PERSISTED FIRST CHANGED-BASIS TRANSITION — NOT YET ROOTED / NOT ADOPTED\n"
        f"Transition SHA-256: {transition_result.persistence.transition_record_sha256}\n"
        f"Transition output location: {transition_result.persistence.path}\n"
        "Successor working-set SHA-256: "
        f"{loaded.successor_note.working_set.verification.working_set_record_sha256}\n"
        f"Successor note SHA-256: {loaded.successor_note.verification.note_record_sha256}\n"
        f"Successor note text:\n{loaded.successor_note.note.note_text}\n"
        "The locations above are receipts only. Root locator inputs below remain blank "
        "and explicit; no location is inferred or treated as identity authority."
    )


def first_changed_basis_revision_root_success_receipt(
    result: ChromiumResearchFirstChangedBasisRevisionRootResult,
) -> str:
    return (
        "Success — first changed-basis 34A revision root persisted and freshly relinked. "
        "Mounted governed session unchanged.\n"
        f"Root SHA-256: {result.persistence.root_record_sha256}\n"
        f"Root destination: {result.persistence.path}\n"
        "Retained transition SHA-256: "
        f"{result.loaded_root.transition.verification.transition_record_sha256}\n"
        f"Human revised rationale:\n{result.loaded_root.root.revision.revised_note.note_text}\n"
        "No 34B first edge, 35A declared root-backed session, root-backed adoption, "
        "epoch, or current/latest/head state was created."
    )


class ResearchFirstChangedBasisRevisionRootControls(Vertical):
    """Explicit 44C controls for the first human 34A root after exact 44B success."""

    def __init__(
        self,
        transition_result: ChromiumResearchFirstChangedBasisTransitionResult,
        prior_result: ChromiumResearchFirstChangedBasisRevisionRootResult | None = None,
    ) -> None:
        if type(transition_result) is not ChromiumResearchFirstChangedBasisTransitionResult:
            raise TypeError(
                "transition_result must be exactly ChromiumResearchFirstChangedBasisTransitionResult."
            )
        if prior_result is not None and prior_result.transition_result is not transition_result:
            raise ValueError(
                "Prior first changed-basis root does not belong to this exact transition result."
            )
        super().__init__(id="research-first-changed-basis-revision-root-controls")
        self.transition_result = transition_result
        self.prior_result = prior_result

    def compose(self) -> ComposeResult:
        locked = self.prior_result is not None
        status_text = (
            first_changed_basis_revision_root_success_receipt(self.prior_result)
            if self.prior_result is not None
            else ""
        )

        yield Static(
            "Author first rationale revision after the evidence-basis change",
            id="research-first-changed-basis-revision-root-title",
        )
        yield Static(
            FIRST_CHANGED_BASIS_REVISION_ROOT_AUTHORITY_NOTICE,
            id="research-first-changed-basis-revision-root-authority-notice",
            markup=False,
        )
        yield Static(
            _transition_summary(self.transition_result),
            id="research-first-changed-basis-revision-root-transition-summary",
            markup=False,
        )
        yield Static(
            "New human rationale — must differ exactly from the transition successor note",
            id="research-first-changed-basis-revision-root-rationale-label",
        )
        yield TextArea(
            "",
            id="research-first-changed-basis-revision-root-rationale",
            disabled=locked,
        )
        yield Static(
            "Durable prior endpoint edge source",
            id="research-first-changed-basis-revision-root-prior-edge-source-label",
        )
        yield Input(
            placeholder="Explicit prior endpoint edge path",
            id="research-first-changed-basis-revision-root-prior-edge-source",
            disabled=locked,
        )
        yield Static(
            "Durable changed working-set source",
            id="research-first-changed-basis-revision-root-working-set-source-label",
        )
        yield Input(
            placeholder="Explicit changed working-set path",
            id="research-first-changed-basis-revision-root-working-set-source",
            disabled=locked,
        )
        yield Static(
            "Durable changed working-set-note source",
            id="research-first-changed-basis-revision-root-note-source-label",
        )
        yield Input(
            placeholder="Explicit changed working-set-note path",
            id="research-first-changed-basis-revision-root-note-source",
            disabled=locked,
        )
        yield Static(
            "Durable first changed-basis transition source",
            id="research-first-changed-basis-revision-root-transition-source-label",
        )
        yield Input(
            placeholder="Explicit 33B transition path",
            id="research-first-changed-basis-revision-root-transition-source",
            disabled=locked,
        )
        yield Static(
            "No-overwrite destination for the first changed-basis revision root",
            id="research-first-changed-basis-revision-root-destination-label",
        )
        yield Input(
            placeholder="Explicit 34A root destination path",
            id="research-first-changed-basis-revision-root-destination",
            disabled=locked,
        )
        yield Button(
            "Persist first changed-basis revision root — session will not advance",
            id="persist-research-first-changed-basis-revision-root",
            variant="warning",
            disabled=locked,
        )
        yield Static(
            status_text,
            id="research-first-changed-basis-revision-root-status",
            markup=False,
        )

    def lock_after_success(
        self,
        result: ChromiumResearchFirstChangedBasisRevisionRootResult,
    ) -> None:
        """Lock this exact transition after one successful 44C 34A root."""

        if result.transition_result is not self.transition_result:
            raise ValueError(
                "First changed-basis root result does not retain this exact 44B transition."
            )
        self.prior_result = result
        self.query_one(
            "#research-first-changed-basis-revision-root-rationale", TextArea
        ).disabled = True
        for widget_id in (
            "#research-first-changed-basis-revision-root-prior-edge-source",
            "#research-first-changed-basis-revision-root-working-set-source",
            "#research-first-changed-basis-revision-root-note-source",
            "#research-first-changed-basis-revision-root-transition-source",
            "#research-first-changed-basis-revision-root-destination",
        ):
            self.query_one(widget_id, Input).disabled = True
        self.query_one(
            "#persist-research-first-changed-basis-revision-root", Button
        ).disabled = True
        self.query_one(
            "#research-first-changed-basis-revision-root-status", Static
        ).update(first_changed_basis_revision_root_success_receipt(result))


__all__ = [
    "FIRST_CHANGED_BASIS_REVISION_ROOT_AUTHORITY_NOTICE",
    "ResearchFirstChangedBasisRevisionRootControls",
    "first_changed_basis_revision_root_success_receipt",
]
