from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Input, Static, TextArea

from pyxis.app.chromium_research_session_controller import (
    ChromiumResearchSessionEndpointRevisionPersistenceResult,
)


REVISION_AUTHORITY_NOTICE = (
    "Revise only the declared segment endpoint. A successful write creates one durable "
    "successor but does not adopt it as current, latest, head, or part of this displayed session."
)
_RESTART_CHECKPOINT_NOTICE = (
    "Further revision is locked until a proven restart locator plan is saved for this "
    "mounted continuation. Restartability is an operational checkpoint, not a latest/head claim."
)


def _success_receipt(
    result: ChromiumResearchSessionEndpointRevisionPersistenceResult,
) -> str:
    persistence = result.persistence
    return (
        "Success — durable successor written; declared session unchanged. "
        "Successor is not adopted/current/head.\n"
        f"Successor edge SHA-256: {persistence.edge_record_sha256}\n"
        f"Destination: {persistence.path}\n"
        "Explicitly continue from this displayed successor before authoring another "
        "successor from the UI."
    )


class ResearchEndpointRevisionControls(Vertical):
    """Explicit UI inputs for one governed 29A declared-endpoint successor write."""

    def __init__(
        self,
        prior_result: ChromiumResearchSessionEndpointRevisionPersistenceResult | None = None,
        *,
        restart_checkpoint_required: bool = False,
    ) -> None:
        if not isinstance(restart_checkpoint_required, bool):
            raise TypeError("restart_checkpoint_required must be bool.")
        if prior_result is not None and restart_checkpoint_required:
            raise ValueError(
                "A prior successful endpoint revision and a restart checkpoint cannot both own the controls."
            )
        super().__init__(id="research-endpoint-revision-controls")
        self.prior_result = prior_result
        self.restart_checkpoint_required = restart_checkpoint_required

    def compose(self) -> ComposeResult:
        locked = self.prior_result is not None or self.restart_checkpoint_required
        if self.prior_result is not None:
            status_text = _success_receipt(self.prior_result)
        elif self.restart_checkpoint_required:
            status_text = _RESTART_CHECKPOINT_NOTICE
        else:
            status_text = ""

        yield Static(
            "Revise declared endpoint rationale",
            id="research-endpoint-revision-title",
        )
        yield Static(
            REVISION_AUTHORITY_NOTICE,
            id="research-endpoint-revision-authority-notice",
            markup=False,
        )
        yield Static(
            "New human-authored rationale — exact multiline text is preserved",
            id="research-endpoint-revised-note-label",
        )
        yield TextArea(
            id="research-endpoint-revised-note",
            disabled=locked,
        )
        yield Static(
            "Current durable file for the exact declared endpoint",
            id="research-endpoint-prior-edge-source-label",
        )
        yield Input(
            placeholder="Explicit predecessor edge path",
            id="research-endpoint-prior-edge-source",
            disabled=locked,
        )
        yield Static(
            "No-overwrite destination for the new successor edge",
            id="research-endpoint-destination-label",
        )
        yield Input(
            placeholder="Explicit successor destination path",
            id="research-endpoint-destination",
            disabled=locked,
        )
        yield Button(
            "Persist durable successor — displayed session will not advance",
            id="persist-research-endpoint-revision",
            variant="warning",
            disabled=locked,
        )
        yield Static(
            status_text,
            id="research-endpoint-revision-status",
            markup=False,
        )

    def lock_after_success(
        self,
        result: ChromiumResearchSessionEndpointRevisionPersistenceResult,
    ) -> None:
        """Lock this declared endpoint after one successful UI successor write."""

        self.prior_result = result
        self.restart_checkpoint_required = False
        self.query_one("#research-endpoint-revised-note", TextArea).disabled = True
        self.query_one("#research-endpoint-prior-edge-source", Input).disabled = True
        self.query_one("#research-endpoint-destination", Input).disabled = True
        self.query_one("#persist-research-endpoint-revision", Button).disabled = True
        self.query_one("#research-endpoint-revision-status", Static).update(
            _success_receipt(result)
        )

    def unlock_after_restart_plan(self) -> None:
        """Unlock a continuation endpoint after its explicit restart checkpoint succeeds."""

        if self.prior_result is not None:
            raise ValueError(
                "Cannot unlock restart checkpoint after this endpoint already wrote a successor."
            )
        if not self.restart_checkpoint_required:
            raise ValueError("No restart checkpoint is currently locking these controls.")

        self.restart_checkpoint_required = False
        self.query_one("#research-endpoint-revised-note", TextArea).disabled = False
        self.query_one("#research-endpoint-prior-edge-source", Input).disabled = False
        self.query_one("#research-endpoint-destination", Input).disabled = False
        self.query_one("#persist-research-endpoint-revision", Button).disabled = False
        self.query_one("#research-endpoint-revision-status", Static).update(
            "Restart checkpoint satisfied. This mounted continuation may now author one explicit successor."
        )
