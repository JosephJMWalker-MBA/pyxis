from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Input, Static

from pyxis.app.chromium_research_first_changed_basis_transition import (
    ChromiumResearchFirstChangedBasisTransitionResult,
)
from pyxis.app.chromium_research_session_working_set_extension import (
    ChromiumResearchSessionWorkingSetExtensionPersistenceResult,
)


FIRST_CHANGED_BASIS_TRANSITION_AUTHORITY_NOTICE = (
    "This is the first explicit cross-working-set transition from ordinary pre-root "
    "lineage. Saving persists and freshly relinks a 33B transition only. The mounted "
    "governed session does not advance, and no revision root, root-backed session, "
    "epoch, current/latest/head state, or semantic-support authority is created."
)
_STALE_NOTICE = (
    "Transition preparation is stale because the shell adopted a different declared "
    "session before this transition was saved. Reprepare/reconfigure against the new "
    "eligible lineage; this form will not silently retarget."
)


def _prepared_summary(
    prepared: ChromiumResearchSessionWorkingSetExtensionPersistenceResult,
) -> str:
    return (
        "PREPARED CHANGED BASIS — NOT YET TRANSITIONED / NOT ROOTED\n"
        f"Working-set SHA-256: {prepared.working_set_persistence.working_set_record_sha256}\n"
        f"Prepared working-set output location: {prepared.working_set_persistence.path}\n"
        f"Working-set-note SHA-256: {prepared.note_persistence.note_record_sha256}\n"
        f"Prepared note output location: {prepared.note_persistence.path}\n"
        "The locations above are receipts only. Transition locator inputs below remain blank "
        "and explicit so moved durable files are never inferred."
    )


def first_changed_basis_transition_success_receipt(
    result: ChromiumResearchFirstChangedBasisTransitionResult,
) -> str:
    loaded = result.loaded_transition
    return (
        "Success — first changed-basis transition persisted and freshly relinked. "
        "Mounted governed session unchanged; no root/epoch was created.\n"
        f"Transition SHA-256: {result.persistence.transition_record_sha256}\n"
        f"Transition destination: {result.persistence.path}\n"
        "Successor working-set SHA-256: "
        f"{loaded.successor_note.working_set.verification.working_set_record_sha256}\n"
        f"Successor note SHA-256: {loaded.successor_note.verification.note_record_sha256}\n"
        "This transition is not itself a root-backed declared session and does not select "
        "current/latest/head state."
    )


class ResearchFirstChangedBasisTransitionControls(Vertical):
    """Explicit 44B controls for one first pre-root 33B basis transition."""

    def __init__(
        self,
        prepared: ChromiumResearchSessionWorkingSetExtensionPersistenceResult,
        prior_result: ChromiumResearchFirstChangedBasisTransitionResult | None = None,
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
                "Prior first changed-basis transition does not belong to this exact prepared basis."
            )
        super().__init__(id="research-first-changed-basis-transition-controls")
        self.prepared = prepared
        self.prior_result = prior_result
        self.stale = False

    def compose(self) -> ComposeResult:
        locked = self.prior_result is not None or self.stale
        if self.prior_result is not None:
            status_text = first_changed_basis_transition_success_receipt(
                self.prior_result
            )
        elif self.stale:
            status_text = _STALE_NOTICE
        else:
            status_text = ""

        yield Static(
            "Transition to prepared changed evidence basis",
            id="research-first-changed-basis-transition-title",
        )
        yield Static(
            FIRST_CHANGED_BASIS_TRANSITION_AUTHORITY_NOTICE,
            id="research-first-changed-basis-transition-authority-notice",
            markup=False,
        )
        yield Static(
            _prepared_summary(self.prepared),
            id="research-first-changed-basis-transition-prepared-summary",
            markup=False,
        )
        yield Static(
            "Current durable file for the exact declared endpoint",
            id="research-first-changed-basis-transition-prior-edge-source-label",
        )
        yield Input(
            placeholder="Explicit prior endpoint edge path",
            id="research-first-changed-basis-transition-prior-edge-source",
            disabled=locked,
        )
        yield Static(
            "Durable source for the exact prepared working set",
            id="research-first-changed-basis-transition-working-set-source-label",
        )
        yield Input(
            placeholder="Explicit prepared working-set path",
            id="research-first-changed-basis-transition-working-set-source",
            disabled=locked,
        )
        yield Static(
            "Durable source for the exact prepared working-set note",
            id="research-first-changed-basis-transition-note-source-label",
        )
        yield Input(
            placeholder="Explicit prepared working-set-note path",
            id="research-first-changed-basis-transition-note-source",
            disabled=locked,
        )
        yield Static(
            "No-overwrite destination for the first changed-basis transition",
            id="research-first-changed-basis-transition-destination-label",
        )
        yield Input(
            placeholder="Explicit transition destination path",
            id="research-first-changed-basis-transition-destination",
            disabled=locked,
        )
        yield Button(
            "Persist first changed-basis transition — session will not advance",
            id="persist-research-first-changed-basis-transition",
            variant="warning",
            disabled=locked,
        )
        yield Static(
            status_text,
            id="research-first-changed-basis-transition-status",
            markup=False,
        )

    def lock_after_success(
        self,
        result: ChromiumResearchFirstChangedBasisTransitionResult,
    ) -> None:
        """Lock the exact prepared basis after one successful 44B transition."""

        if result.prepared is not self.prepared:
            raise ValueError(
                "First changed-basis transition result does not retain this exact prepared basis."
            )
        self.prior_result = result
        self.stale = False
        self._set_inputs_disabled(True)
        self.query_one(
            "#persist-research-first-changed-basis-transition", Button
        ).disabled = True
        self.query_one(
            "#research-first-changed-basis-transition-status", Static
        ).update(first_changed_basis_transition_success_receipt(result))

    def mark_stale(self) -> None:
        """Disable an unsaved transition after its mounted session was replaced."""

        if self.prior_result is not None:
            return
        self.stale = True
        self._set_inputs_disabled(True)
        self.query_one(
            "#persist-research-first-changed-basis-transition", Button
        ).disabled = True
        self.query_one(
            "#research-first-changed-basis-transition-status", Static
        ).update(_STALE_NOTICE)

    def _set_inputs_disabled(self, disabled: bool) -> None:
        for widget_id in (
            "#research-first-changed-basis-transition-prior-edge-source",
            "#research-first-changed-basis-transition-working-set-source",
            "#research-first-changed-basis-transition-note-source",
            "#research-first-changed-basis-transition-destination",
        ):
            self.query_one(widget_id, Input).disabled = disabled


__all__ = [
    "FIRST_CHANGED_BASIS_TRANSITION_AUTHORITY_NOTICE",
    "ResearchFirstChangedBasisTransitionControls",
    "first_changed_basis_transition_success_receipt",
]
