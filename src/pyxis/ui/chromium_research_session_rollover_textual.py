from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Input, Static

from pyxis.app.chromium_research_session_controller import (
    ChromiumResearchSessionEndpointRevisionPersistenceResult,
)
from pyxis.app.chromium_research_session_rollover import (
    ChromiumResearchSessionRolloverResult,
)


ROLLOVER_AUTHORITY_NOTICE = (
    "Continue only from the displayed persisted successor by explicit choice. "
    "A successful rollover creates and mounts a new declared continuation session; "
    "it does not make that successor a global latest, current, or canonical head."
)


def _candidate_receipt(
    result: ChromiumResearchSessionEndpointRevisionPersistenceResult,
) -> str:
    return (
        "Displayed successor available for explicit continuation choice.\n"
        f"Successor edge SHA-256: {result.persistence.edge_record_sha256}\n"
        "Other sibling successors, if any, are not discovered or enumerated here."
    )


def rollover_success_receipt(result: ChromiumResearchSessionRolloverResult) -> str:
    """Format one transient UI receipt for a successful explicit rollover."""

    return (
        "Continued from the explicitly selected successor into a new declared "
        "continuation session.\n"
        f"Selected successor SHA-256: {result.prior_revision.persistence.edge_record_sha256}\n"
        f"New declaration SHA-256: {result.declaration.sequence_record_sha256}\n"
        f"New declaration: {result.declaration.path}\n"
        "The mounted research session now represents this explicit continuation only. "
        "It is not a global latest/current/head claim."
    )


class ResearchSessionRolloverControls(Vertical):
    """Explicit UI choice and paths for one governed 30A continuation rollover."""

    def __init__(
        self,
        candidate_revision: ChromiumResearchSessionEndpointRevisionPersistenceResult | None = None,
    ) -> None:
        super().__init__(id="research-session-rollover-controls")
        self.candidate_revision = candidate_revision

    def compose(self) -> ComposeResult:
        enabled = self.candidate_revision is not None
        yield Static(
            "Continue from persisted successor",
            id="research-session-rollover-title",
        )
        yield Static(
            ROLLOVER_AUTHORITY_NOTICE,
            id="research-session-rollover-authority-notice",
            markup=False,
        )
        yield Static(
            _candidate_receipt(self.candidate_revision)
            if self.candidate_revision is not None
            else "Persist one successor before choosing a continuation session.",
            id="research-session-rollover-candidate",
            markup=False,
        )
        yield Static(
            "Durable file for this exact displayed successor",
            id="research-session-rollover-successor-source-label",
        )
        yield Input(
            placeholder="Explicit successor edge path",
            id="research-session-rollover-successor-source",
            disabled=not enabled,
        )
        yield Static(
            "No-overwrite destination for the new continuation declaration",
            id="research-session-rollover-declaration-destination-label",
        )
        yield Input(
            placeholder="Explicit continuation declaration path",
            id="research-session-rollover-declaration-destination",
            disabled=not enabled,
        )
        yield Button(
            "Continue from this successor — create new declared session",
            id="rollover-research-session",
            variant="warning",
            disabled=not enabled,
        )
        yield Static(
            "",
            id="research-session-rollover-status",
            markup=False,
        )

    def enable_for_revision(
        self,
        result: ChromiumResearchSessionEndpointRevisionPersistenceResult,
    ) -> None:
        """Expose an exact successful 29A result as the displayed rollover candidate."""

        if not isinstance(result, ChromiumResearchSessionEndpointRevisionPersistenceResult):
            raise TypeError(
                "result must be ChromiumResearchSessionEndpointRevisionPersistenceResult."
            )
        self.candidate_revision = result
        self.query_one("#research-session-rollover-candidate", Static).update(
            _candidate_receipt(result)
        )
        self.query_one("#research-session-rollover-successor-source", Input).disabled = False
        self.query_one(
            "#research-session-rollover-declaration-destination", Input
        ).disabled = False
        self.query_one("#rollover-research-session", Button).disabled = False
        self.query_one("#research-session-rollover-status", Static).update(
            "Ready for explicit continuation choice. Both paths remain caller-supplied."
        )
