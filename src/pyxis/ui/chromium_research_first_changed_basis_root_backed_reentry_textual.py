from __future__ import annotations

from collections.abc import Iterable

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Input, Static

from pyxis.app.chromium_research_first_changed_basis_root_backed_reentry import (
    ChromiumResearchFirstChangedBasisRootBackedReentryResult,
)
from pyxis.app.chromium_research_first_changed_basis_session_adoption import (
    ChromiumResearchFirstChangedBasisSessionAdoptionResult,
)
from pyxis.app.chromium_research_paragraph_text_selection_comparison_note_load import (
    ChromiumPageResearchLoadedParagraphTextSelectionComparisonNoteRecord,
)
from pyxis.app.chromium_research_paragraph_text_selection_note_load import (
    ChromiumPageResearchLoadedParagraphTextSelectionNoteRecord,
)
from pyxis.app.chromium_research_selection_note_load import (
    ChromiumPageResearchLoadedParagraphNoteRecord,
)
from pyxis.app.chromium_research_working_set import ChromiumPageResearchWorkingSetItem


FIRST_CHANGED_BASIS_ROOT_BACKED_REENTRY_AUTHORITY_NOTICE = (
    "Verify that the exact adopted 44E root-backed session can be reconstructed from "
    "explicit current durable locators. This reads and proves evidence but writes no "
    "35C overlay, does not replace the mounted governed session, and does not select "
    "a global current/latest/head branch."
)


def _member_kind(item: ChromiumPageResearchWorkingSetItem) -> str:
    if isinstance(item, ChromiumPageResearchLoadedParagraphNoteRecord):
        return "paragraph note"
    if isinstance(item, ChromiumPageResearchLoadedParagraphTextSelectionNoteRecord):
        return "exact-range note"
    if isinstance(item, ChromiumPageResearchLoadedParagraphTextSelectionComparisonNoteRecord):
        return "comparison note"
    raise TypeError("appended item must be a supported loaded working-set record.")


def _member_note_text(item: ChromiumPageResearchWorkingSetItem) -> str:
    return item.note.note_text


def _summary(
    adoption: ChromiumResearchFirstChangedBasisSessionAdoptionResult,
    items: tuple[ChromiumPageResearchWorkingSetItem, ...],
) -> str:
    return (
        "ADOPTED ROOT-BACKED SESSION — RESTARTABILITY NOT YET PERSISTED\n"
        f"Root SHA-256: {adoption.edge_result.root_result.persistence.root_record_sha256}\n"
        f"Declaration SHA-256: {adoption.declaration.sequence_record_sha256}\n"
        f"Endpoint edge SHA-256: {adoption.edge_result.persistence.edge_record_sha256}\n"
        f"Appended evidence members: {len(items)}\n"
        "The output locations from 44A–44E are historical receipt context only. "
        "Every locator below remains blank and explicit."
    )


def first_changed_basis_root_backed_reentry_success_receipt(
    result: ChromiumResearchFirstChangedBasisRootBackedReentryResult,
) -> str:
    fresh = result.fresh_reentry
    return (
        "Success — exact 44E root-backed session freshly reconstructed through 35B. "
        "Mounted governed session unchanged.\n"
        f"Root SHA-256: {fresh.loaded_root.verification.root_record_sha256}\n"
        f"Declaration SHA-256: {fresh.loaded_declaration.verification.sequence_record_sha256}\n"
        f"Endpoint edge SHA-256: {fresh.controller.declared_endpoint.verification.edge_record_sha256}\n"
        f"Appended evidence members freshly relinked: {len(fresh.loaded_appended_members)}\n"
        "Endpoint rationale:\n"
        f"{fresh.controller.declared_endpoint.revision.revised_note.note_text}\n"
        "Fresh-process reconstructability is proven for this exact session, but no "
        "durable 35C overlay/restart locator has been written and no global head/latest "
        "authority was created."
    )


class ResearchFirstChangedBasisRootBackedReentryControls(Vertical):
    """Explicit 44F locators for one fresh 35B reconstruction proof."""

    def __init__(
        self,
        adoption_result: ChromiumResearchFirstChangedBasisSessionAdoptionResult,
        appended_items: Iterable[ChromiumPageResearchWorkingSetItem],
        prior_result: ChromiumResearchFirstChangedBasisRootBackedReentryResult | None = None,
    ) -> None:
        if type(adoption_result) is not ChromiumResearchFirstChangedBasisSessionAdoptionResult:
            raise TypeError(
                "adoption_result must be exactly ChromiumResearchFirstChangedBasisSessionAdoptionResult."
            )
        items = tuple(appended_items)
        if not items:
            raise ValueError("appended_items must contain at least one exact changed-basis member.")
        for item in items:
            _member_kind(item)
        if prior_result is not None and prior_result.adoption_result is not adoption_result:
            raise ValueError("Prior 44F proof does not belong to this exact 44E adoption.")
        super().__init__(id="research-first-changed-basis-root-backed-reentry-controls")
        self.adoption_result = adoption_result
        self.appended_items = items
        self.prior_result = prior_result

    def compose(self) -> ComposeResult:
        locked = self.prior_result is not None
        yield Static(
            "Verify fresh-process root-backed re-entry",
            id="research-first-changed-basis-root-backed-reentry-title",
        )
        yield Static(
            FIRST_CHANGED_BASIS_ROOT_BACKED_REENTRY_AUTHORITY_NOTICE,
            id="research-first-changed-basis-root-backed-reentry-authority-notice",
            markup=False,
        )
        yield Static(
            _summary(self.adoption_result, self.appended_items),
            id="research-first-changed-basis-root-backed-reentry-summary",
            markup=False,
        )

        for index, item in enumerate(self.appended_items):
            kind = _member_kind(item)
            yield Static(
                f"Appended member {index} — {kind}\nNote text:\n{_member_note_text(item)}",
                classes="research-first-changed-basis-reentry-member-summary",
                id=f"research-first-changed-basis-reentry-member-{index}-summary",
                markup=False,
            )
            if kind == "comparison note":
                yield Input(
                    placeholder="Explicit current first capture path",
                    id=f"research-first-changed-basis-reentry-member-{index}-first-capture-source",
                    classes="research-first-changed-basis-reentry-input",
                    disabled=locked,
                )
                yield Input(
                    placeholder="Explicit current second capture path",
                    id=f"research-first-changed-basis-reentry-member-{index}-second-capture-source",
                    classes="research-first-changed-basis-reentry-input",
                    disabled=locked,
                )
            else:
                yield Input(
                    placeholder="Explicit current capture path",
                    id=f"research-first-changed-basis-reentry-member-{index}-capture-source",
                    classes="research-first-changed-basis-reentry-input",
                    disabled=locked,
                )
            yield Input(
                placeholder="Explicit current note sidecar path",
                id=f"research-first-changed-basis-reentry-member-{index}-note-source",
                classes="research-first-changed-basis-reentry-input",
                disabled=locked,
            )

        fields = (
            ("changed-working-set-source", "Explicit current changed working-set path"),
            ("changed-note-source", "Explicit current changed working-set-note path"),
            ("transition-source", "Explicit current 33B transition path"),
            ("root-source", "Explicit current 34A root path"),
            ("first-edge-source", "Explicit current first post-root edge path"),
            ("declaration-source", "Explicit current root-backed declaration path"),
        )
        for suffix, placeholder in fields:
            yield Input(
                placeholder=placeholder,
                id=f"research-first-changed-basis-reentry-{suffix}",
                classes="research-first-changed-basis-reentry-input",
                disabled=locked,
            )

        yield Button(
            "Verify fresh-process reconstruction — mounted session will not change",
            id="verify-research-first-changed-basis-root-backed-reentry",
            variant="warning",
            disabled=locked,
        )
        yield Static(
            first_changed_basis_root_backed_reentry_success_receipt(self.prior_result)
            if self.prior_result is not None
            else "",
            id="research-first-changed-basis-root-backed-reentry-status",
            markup=False,
        )

    def lock_after_success(
        self,
        result: ChromiumResearchFirstChangedBasisRootBackedReentryResult,
    ) -> None:
        if result.adoption_result is not self.adoption_result:
            raise ValueError("44F result does not retain this exact 44E adoption.")
        self.prior_result = result
        for widget in self.query(".research-first-changed-basis-reentry-input"):
            if isinstance(widget, Input):
                widget.disabled = True
        self.query_one(
            "#verify-research-first-changed-basis-root-backed-reentry", Button
        ).disabled = True
        self.query_one(
            "#research-first-changed-basis-root-backed-reentry-status", Static
        ).update(first_changed_basis_root_backed_reentry_success_receipt(result))


__all__ = [
    "FIRST_CHANGED_BASIS_ROOT_BACKED_REENTRY_AUTHORITY_NOTICE",
    "ResearchFirstChangedBasisRootBackedReentryControls",
    "first_changed_basis_root_backed_reentry_success_receipt",
]
