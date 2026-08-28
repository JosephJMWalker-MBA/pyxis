from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Input, Static

from pyxis.app.chromium_research_second_changed_basis_transition import (
    ChromiumResearchSecondChangedBasisTransitionResult,
)
from pyxis.app.chromium_research_session_working_set_extension import (
    ChromiumResearchSessionWorkingSetExtensionPersistenceResult,
)


SECOND_CHANGED_BASIS_TRANSITION_AUTHORITY_NOTICE = (
    "This is one explicit second cross-working-set transition from exact one-root "
    "continuation authority. Saving persists and freshly relinks a public 33B transition "
    "only. The mounted governed session does not advance, and no second revision root, "
    "second-epoch session, current/latest/head state, or semantic-support authority is created."
)
_STALE_NOTICE = (
    "Second-transition preparation is stale because the shell adopted a different "
    "declared session before this transition was saved. Reprepare/reconfigure against "
    "the new eligible continuation; this form will not silently retarget."
)


def _prepared_summary(
    prepared: ChromiumResearchSessionWorkingSetExtensionPersistenceResult,
) -> str:
    return (
        "PREPARED SECOND CHANGED BASIS — NOT YET TRANSITIONED / NOT ROOTED\n"
        f"Working-set SHA-256: {prepared.working_set_persistence.working_set_record_sha256}\n"
        f"Prepared working-set output location: {prepared.working_set_persistence.path}\n"
        f"Working-set-note SHA-256: {prepared.note_persistence.note_record_sha256}\n"
        f"Prepared note output location: {prepared.note_persistence.path}\n"
        "The locations above are receipts only. Transition locator inputs below remain blank "
        "and explicit so moved durable files are never inferred."
    )


def second_changed_basis_transition_success_receipt(
    result: ChromiumResearchSecondChangedBasisTransitionResult,
) -> str:
    loaded = result.loaded_transition
    return (
        "Success — second changed-basis transition persisted and freshly relinked. "
        "Mounted governed session unchanged; no second root/epoch was created.\n"
        f"Transition SHA-256: {result.persistence.transition_record_sha256}\n"
        f"Transition destination: {result.persistence.path}\n"
        "Successor working-set SHA-256: "
        f"{loaded.successor_note.working_set.verification.working_set_record_sha256}\n"
        f"Successor note SHA-256: {loaded.successor_note.verification.note_record_sha256}\n"
        "This transition is not itself a second-epoch declared session and does not select "
        "current/latest/head state."
    )


class ResearchSecondChangedBasisTransitionControls(Vertical):
    """Explicit 46A controls for one second 33B basis transition."""

    def __init__(
        self,
        prepared: ChromiumResearchSessionWorkingSetExtensionPersistenceResult,
        prior_result: ChromiumResearchSecondChangedBasisTransitionResult | None = None,
    ) -> None:
        if not isinstance(
            prepared,
            ChromiumResearchSessionWorkingSetExtensionPersistenceResult,
        ):
            raise TypeError(
                "prepared must be ChromiumResearchSessionWorkingSetExtensionPersistenceResult."
            )
        if prior_result is not None and prior_result.prepared is not prepared:
            raise ValueError(
                "Prior second changed-basis transition does not belong to this exact prepared basis."
            )
        super().__init__(id="research-second-changed-basis-transition-controls")
        self.prepared = prepared
        self.prior_result = prior_result
        self.stale = False

    def compose(self) -> ComposeResult:
        locked = self.prior_result is not None or self.stale
        if self.prior_result is not None:
            status_text = second_changed_basis_transition_success_receipt(self.prior_result)
        elif self.stale:
            status_text = _STALE_NOTICE
        else:
            status_text = ""

        yield Static(
            "Transition to prepared second changed evidence basis",
            id="research-second-changed-basis-transition-title",
        )
        yield Static(
            SECOND_CHANGED_BASIS_TRANSITION_AUTHORITY_NOTICE,
            id="research-second-changed-basis-transition-authority-notice",
            markup=False,
        )
        yield Static(
            _prepared_summary(self.prepared),
            id="research-second-changed-basis-transition-prepared-summary",
            markup=False,
        )
        yield Static(
            "Current durable file for the exact one-root continuation endpoint",
            id="research-second-changed-basis-transition-prior-edge-source-label",
        )
        yield Input(
            placeholder="Explicit current prior endpoint edge path",
            id="research-second-changed-basis-transition-prior-edge-source",
            disabled=locked,
        )
        yield Static(
            "Durable source for the exact prepared working set",
            id="research-second-changed-basis-transition-working-set-source-label",
        )
        yield Input(
            placeholder="Explicit prepared working-set path",
            id="research-second-changed-basis-transition-working-set-source",
            disabled=locked,
        )
        yield Static(
            "Durable source for the exact prepared working-set note",
            id="research-second-changed-basis-transition-note-source-label",
        )
        yield Input(
            placeholder="Explicit prepared working-set-note path",
            id="research-second-changed-basis-transition-note-source",
            disabled=locked,
        )
        yield Static(
            "No-overwrite destination for the second changed-basis transition",
            id="research-second-changed-basis-transition-destination-label",
        )
        yield Input(
            placeholder="Explicit second transition destination path",
            id="research-second-changed-basis-transition-destination",
            disabled=locked,
        )
        yield Button(
            "Persist second changed-basis transition — session will not advance",
            id="persist-research-second-changed-basis-transition",
            variant="warning",
            disabled=locked,
        )
        yield Static(
            status_text,
            id="research-second-changed-basis-transition-status",
            markup=False,
        )

    def lock_after_success(
        self,
        result: ChromiumResearchSecondChangedBasisTransitionResult,
    ) -> None:
        if result.prepared is not self.prepared:
            raise ValueError(
                "Second changed-basis transition result does not retain this exact prepared basis."
            )
        self.prior_result = result
        self.stale = False
        self._set_inputs_disabled(True)
        self.query_one(
            "#persist-research-second-changed-basis-transition", Button
        ).disabled = True
        self.query_one(
            "#research-second-changed-basis-transition-status", Static
        ).update(second_changed_basis_transition_success_receipt(result))

    def mark_stale(self) -> None:
        if self.prior_result is not None:
            return
        self.stale = True
        self._set_inputs_disabled(True)
        self.query_one(
            "#persist-research-second-changed-basis-transition", Button
        ).disabled = True
        self.query_one(
            "#research-second-changed-basis-transition-status", Static
        ).update(_STALE_NOTICE)

    def _set_inputs_disabled(self, disabled: bool) -> None:
        for widget_id in (
            "#research-second-changed-basis-transition-prior-edge-source",
            "#research-second-changed-basis-transition-working-set-source",
            "#research-second-changed-basis-transition-note-source",
            "#research-second-changed-basis-transition-destination",
        ):
            self.query_one(widget_id, Input).disabled = disabled


__all__ = [
    "SECOND_CHANGED_BASIS_TRANSITION_AUTHORITY_NOTICE",
    "ResearchSecondChangedBasisTransitionControls",
    "second_changed_basis_transition_success_receipt",
]
