from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static

from pyxis.app.architecture_reconciliation import (
    ArchitectureConsequenceReconciliationPresentation,
)


def _comparison(value: bool) -> str:
    return "MATCH" if value else "DIFFERS"


def _format_reconciliation(
    presentation: ArchitectureConsequenceReconciliationPresentation,
) -> str:
    observed = presentation.observed
    lines = [
        "POST-APPLY RECONCILIATION — OBSERVED EVIDENCE",
        "Earlier preview remains separate proposed evidence.",
        "",
        "Revision transition",
        f"→ operation: {observed.operation}",
        f"→ revision id: {observed.revision_id}",
        (
            "→ preview canonical transition vs observed revision: "
            f"{_comparison(presentation.revision_transition_matches_preview)}"
        ),
        "",
        "Observed canonical state",
        f"→ sha256: {observed.canonical_sha256}",
        (
            "→ proposed canonical identity: "
            f"{_comparison(presentation.observed_canonical_matches_preview)}"
        ),
        "",
        "Observed RIR",
        "→ capabilities: " + ", ".join(observed.rir_capabilities),
        f"→ sha256: {observed.rir_sha256}",
        (
            "→ proposed RIR capabilities: "
            f"{_comparison(presentation.observed_rir_capabilities_match_preview)}"
        ),
        (
            "→ revision completion RIR identity: "
            f"{_comparison(presentation.revision_completion_rir_matches_observed_rir)}"
        ),
        "",
        "Observed compiler generation for predicted products",
    ]

    for consequence in presentation.artifact_consequences:
        observed_status = consequence.observed_generation_status or "not observed"
        lines.append(
            "→ "
            f"{consequence.path}: proposed {consequence.proposed_action}; "
            f"expected status {consequence.expected_generation_status}; "
            f"observed {observed_status}; {_comparison(consequence.matches)}"
        )

    lines.extend(
        (
            "",
            "Observed runtime keys",
            "→ " + ", ".join(observed.runtime_keys),
            (
                "→ proposed runtime keys: "
                f"{_comparison(presentation.observed_runtime_keys_match_preview)}"
            ),
        )
    )
    return "\n".join(lines)


class ArchitectureReconciliationDetail(Vertical):
    """Read-only renderer for distinct proposed-vs-observed Apply evidence."""

    def __init__(self) -> None:
        super().__init__(id="architecture-reconciliation")
        self.presentation: ArchitectureConsequenceReconciliationPresentation | None = None

    def compose(self) -> ComposeResult:
        yield Static(
            "Post-Apply architecture reconciliation",
            id="architecture-reconciliation-title",
            classes="section-title",
        )
        yield Static(
            "No post-Apply architecture reconciliation.",
            id="architecture-reconciliation-evidence",
            classes="evidence-body",
            markup=False,
        )

    def replace_presentation(
        self,
        presentation: ArchitectureConsequenceReconciliationPresentation,
    ) -> None:
        self.presentation = presentation
        self.query_one("#architecture-reconciliation-evidence", Static).update(
            _format_reconciliation(presentation)
        )

    def clear_presentation(self) -> None:
        self.presentation = None
        self.query_one("#architecture-reconciliation-evidence", Static).update(
            "No post-Apply architecture reconciliation."
        )
