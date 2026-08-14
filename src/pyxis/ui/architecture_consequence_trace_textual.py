from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static

from pyxis.app.preview_presentation import ArchitecturePreviewPresentation


_STAGE_LABELS = {
    "requested_architecture_change": "Requested architecture change",
    "proposed_canonical": "Proposed canonical state",
    "proposed_rir": "Proposed RIR",
    "compiler_product": "Compiler products",
    "runtime_contract": "Runtime contract",
}
_SUBJECT_LABELS = {
    "capability": "capability",
    "artifact_path": "artifact",
    "runtime_key": "runtime key",
}


def _format_consequence_trace(
    presentation: ArchitecturePreviewPresentation,
) -> str:
    lines = ["PROPOSED CONSEQUENCE TRACE — NOT APPLIED"]
    current_stage: str | None = None

    for step in presentation.consequence_trace:
        if step.stage != current_stage:
            current_stage = step.stage
            lines.extend(("", _STAGE_LABELS.get(step.stage, step.stage)))

        subject_label = _SUBJECT_LABELS.get(step.subject_kind, step.subject_kind)
        lines.append(f"→ {step.action} {subject_label}: {step.subject}")

    return "\n".join(lines)


class ArchitectureConsequenceTraceDetail(Vertical):
    """Read-only renderer for preview-owned architecture consequence evidence."""

    def __init__(self) -> None:
        super().__init__(id="architecture-consequence-trace")
        self.presentation: ArchitecturePreviewPresentation | None = None

    def compose(self) -> ComposeResult:
        yield Static(
            "Architecture consequence trace",
            id="architecture-consequence-trace-title",
            classes="section-title",
        )
        yield Static(
            "No pending architecture consequence trace.",
            id="architecture-consequence-trace-evidence",
            classes="evidence-body",
            markup=False,
        )

    def replace_presentation(
        self,
        presentation: ArchitecturePreviewPresentation,
    ) -> None:
        self.presentation = presentation
        self.query_one("#architecture-consequence-trace-evidence", Static).update(
            _format_consequence_trace(presentation)
        )

    def clear_presentation(self) -> None:
        self.presentation = None
        self.query_one("#architecture-consequence-trace-evidence", Static).update(
            "No pending architecture consequence trace."
        )
