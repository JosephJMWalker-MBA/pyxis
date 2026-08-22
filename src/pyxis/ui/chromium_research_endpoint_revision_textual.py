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


def _success_receipt(
    result: ChromiumResearchSessionEndpointRevisionPersistenceResult,
) -> str:
    persistence = result.persistence
    return (
        "Success — durable successor written; declared session unchanged. "
        "Successor is not adopted/current/head.\n"
        f"Successor edge SHA-256: {persistence.edge_record_sha256}\n"
        f"Destination: {persistence.path}\n"
        "Reopen and explicitly redeclare before authoring another successor from the UI."
    )


class ResearchEndpointRevisionControls(Vertical):
    """Explicit UI inputs for one governed 29A declared-endpoint successor write."""

    def __init__(
        self,
        prior_result: ChromiumResearchSessionEndpointRevisionPersistenceResult | None = None,
    ) -> None:
        super().__init__(id="research-endpoint-revision-controls")
        self.prior_result = prior_result

    def compose(self) -> ComposeResult:
        locked = self.prior_result is not None
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
            _success_receipt(self.prior_result) if self.prior_result is not None else "",
            id="research-endpoint-revision-status",
            markup=False,
        )

    def lock_after_success(
        self,
        result: ChromiumResearchSessionEndpointRevisionPersistenceResult,
    ) -> None:
        """Lock this declared endpoint after one successful UI successor write."""

        self.prior_result = result
        self.query_one("#research-endpoint-revised-note", TextArea).disabled = True
        self.query_one("#research-endpoint-prior-edge-source", Input).disabled = True
        self.query_one("#research-endpoint-destination", Input).disabled = True
        self.query_one("#persist-research-endpoint-revision", Button).disabled = True
        self.query_one("#research-endpoint-revision-status", Static).update(
            _success_receipt(result)
        )
