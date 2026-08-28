from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Input, Static, TextArea

from pyxis.app.chromium_research_changed_basis_candidate_presentation import (
    ChromiumResearchChangedBasisCandidatePresentation,
)
from pyxis.app.chromium_research_session_working_set_extension import (
    ChromiumResearchSessionWorkingSetExtensionPersistenceResult,
)


CHANGED_BASIS_AUTHORITY_NOTICE = (
    "Candidate appended evidence is not yet part of the declared working set. Saving "
    "prepares a new durable working set and human rationale only; it does not transition, "
    "adopt, create a root/epoch, or select current/latest/head research state."
)
_STALE_NOTICE = (
    "Candidate preparation is stale because the shell adopted a different declared "
    "session before this candidate was saved. Reconfigure candidate evidence against "
    "the new declared endpoint; this form will not silently retarget."
)


def _candidate_summary(
    presentation: ChromiumResearchChangedBasisCandidatePresentation,
) -> str:
    lines = [
        "CANDIDATE APPENDED MEMBERS — NOT YET WORKING SET / NOT ADOPTED",
        f"Declared endpoint anchor SHA-256: {presentation.declared_endpoint_sha256}",
        f"Candidate member count: {presentation.candidate_member_count}",
    ]
    for member in presentation.members:
        lines.append("")
        lines.append(
            f"Candidate member {member.member_position}: {member.member_kind}"
        )
        lines.append(f"Human note: {member.human_note_text}")
        for excerpt in member.excerpts:
            coordinate = f"paragraph {excerpt.paragraph_ordinal}"
            if excerpt.start_offset is not None and excerpt.end_offset is not None:
                coordinate += f", offsets {excerpt.start_offset}:{excerpt.end_offset}"
            lines.append(
                f"{excerpt.excerpt_role}: {excerpt.url} — {coordinate}"
            )
            lines.append(f"Excerpt: {excerpt.text}")
    return "\n".join(lines)


def _success_receipt(
    result: ChromiumResearchSessionWorkingSetExtensionPersistenceResult,
) -> str:
    return (
        "Success — changed evidence basis prepared; displayed governed session unchanged.\n"
        f"Working-set SHA-256: {result.working_set_persistence.working_set_record_sha256}\n"
        f"Working-set destination: {result.working_set_persistence.path}\n"
        f"Working-set-note SHA-256: {result.note_persistence.note_record_sha256}\n"
        f"Working-set-note destination: {result.note_persistence.path}\n"
        "Prepared basis is not transitioned/adopted/current/latest/head."
    )


class ResearchChangedBasisPreparationControls(Vertical):
    """Explicit 44A UI for preparing, but never adopting, one changed evidence basis."""

    DEFAULT_CSS = """
    ResearchChangedBasisPreparationControls {
        width: 94%;
        height: auto;
        padding: 1 2;
        margin-top: 1;
        border: round $secondary;
    }

    #research-changed-basis-authority-notice,
    #research-changed-basis-candidate,
    #research-changed-basis-rationale-label,
    #research-changed-basis-working-set-destination-label,
    #research-changed-basis-note-destination-label,
    #research-changed-basis-status,
    #persist-research-changed-basis-preparation {
        margin-top: 1;
    }

    #research-changed-basis-title,
    #research-changed-basis-rationale-label,
    #research-changed-basis-working-set-destination-label,
    #research-changed-basis-note-destination-label {
        text-style: bold;
    }

    #research-changed-basis-rationale {
        width: 100%;
        height: 8;
        margin-top: 1;
    }
    """

    def __init__(
        self,
        presentation: ChromiumResearchChangedBasisCandidatePresentation,
    ) -> None:
        if not isinstance(
            presentation,
            ChromiumResearchChangedBasisCandidatePresentation,
        ):
            raise TypeError(
                "presentation must be ChromiumResearchChangedBasisCandidatePresentation."
            )
        super().__init__(id="research-changed-basis-preparation-controls")
        self.presentation = presentation
        self.result: ChromiumResearchSessionWorkingSetExtensionPersistenceResult | None = None
        self.stale = False

    def compose(self) -> ComposeResult:
        yield Static(
            "Prepare changed evidence basis — candidate only",
            id="research-changed-basis-title",
        )
        yield Static(
            CHANGED_BASIS_AUTHORITY_NOTICE,
            id="research-changed-basis-authority-notice",
            markup=False,
        )
        yield Static(
            _candidate_summary(self.presentation),
            id="research-changed-basis-candidate",
            markup=False,
        )
        yield Static(
            "New human-authored rationale over the changed evidence basis",
            id="research-changed-basis-rationale-label",
        )
        yield TextArea(id="research-changed-basis-rationale")
        yield Static(
            "No-overwrite destination for the prepared working set",
            id="research-changed-basis-working-set-destination-label",
        )
        yield Input(
            placeholder="Explicit prepared working-set destination path",
            id="research-changed-basis-working-set-destination",
        )
        yield Static(
            "No-overwrite destination for the prepared working-set note",
            id="research-changed-basis-note-destination-label",
        )
        yield Input(
            placeholder="Explicit prepared working-set-note destination path",
            id="research-changed-basis-note-destination",
        )
        yield Button(
            "Persist prepared basis — do not adopt",
            id="persist-research-changed-basis-preparation",
            variant="warning",
        )
        yield Static("", id="research-changed-basis-status", markup=False)

    def lock_after_success(
        self,
        result: ChromiumResearchSessionWorkingSetExtensionPersistenceResult,
    ) -> None:
        if not isinstance(
            result,
            ChromiumResearchSessionWorkingSetExtensionPersistenceResult,
        ):
            raise TypeError(
                "result must be ChromiumResearchSessionWorkingSetExtensionPersistenceResult."
            )
        self.result = result
        self.stale = False
        self._set_locked(True)
        self.query_one("#research-changed-basis-status", Static).update(
            _success_receipt(result)
        )

    def mark_stale(self) -> None:
        """Lock an unsaved candidate instead of silently retargeting after adoption."""

        if self.result is not None:
            return
        self.stale = True
        self._set_locked(True)
        self.query_one("#research-changed-basis-status", Static).update(_STALE_NOTICE)

    def _set_locked(self, locked: bool) -> None:
        self.query_one("#research-changed-basis-rationale", TextArea).disabled = locked
        self.query_one(
            "#research-changed-basis-working-set-destination", Input
        ).disabled = locked
        self.query_one("#research-changed-basis-note-destination", Input).disabled = locked
        self.query_one(
            "#persist-research-changed-basis-preparation", Button
        ).disabled = locked


__all__ = [
    "CHANGED_BASIS_AUTHORITY_NOTICE",
    "ResearchChangedBasisPreparationControls",
]
