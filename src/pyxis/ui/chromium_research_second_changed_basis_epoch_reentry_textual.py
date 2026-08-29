from __future__ import annotations

from collections.abc import Iterable

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Input, Static

from pyxis.app.chromium_research_paragraph_text_selection_comparison_note_load import (
    ChromiumPageResearchLoadedParagraphTextSelectionComparisonNoteRecord,
)
from pyxis.app.chromium_research_paragraph_text_selection_note_load import (
    ChromiumPageResearchLoadedParagraphTextSelectionNoteRecord,
)
from pyxis.app.chromium_research_second_changed_basis_epoch_reentry import (
    ChromiumResearchSecondChangedBasisEpochReentryResult,
)
from pyxis.app.chromium_research_second_changed_basis_session_adoption import (
    ChromiumResearchSecondChangedBasisSessionAdoptionResult,
)
from pyxis.app.chromium_research_selection_note_load import (
    ChromiumPageResearchLoadedParagraphNoteRecord,
)
from pyxis.app.chromium_research_working_set import ChromiumPageResearchWorkingSetItem


SECOND_CHANGED_BASIS_EPOCH_REENTRY_AUTHORITY_NOTICE = (
    "Verify that the exact historical 46D second-basis session can be freshly "
    "reconstructed through existing 37A from explicit current durable locators. "
    "This writes no 37B overlay, does not replace the mounted governed session, "
    "does not backfill launch provenance, and does not select a global current/latest/head."
)


def _member_kind(item: ChromiumPageResearchWorkingSetItem) -> str:
    if isinstance(item, ChromiumPageResearchLoadedParagraphNoteRecord):
        return "paragraph note"
    if isinstance(item, ChromiumPageResearchLoadedParagraphTextSelectionNoteRecord):
        return "exact-range note"
    if isinstance(item, ChromiumPageResearchLoadedParagraphTextSelectionComparisonNoteRecord):
        return "comparison note"
    raise TypeError("appended item must be a supported loaded working-set record.")


def _summary(
    adoption: ChromiumResearchSecondChangedBasisSessionAdoptionResult,
    items: tuple[ChromiumPageResearchWorkingSetItem, ...],
) -> str:
    retained_prior = adoption.edge_result.root_result.transition_result.continuation_reentry
    return (
        "ADOPTED SECOND-BASIS SESSION — 37A RESTARTABILITY NOT YET PROVEN\n"
        f"Retained first root SHA-256: {retained_prior.prior_root_backed_reentry.loaded_root.verification.root_record_sha256}\n"
        f"Second root SHA-256: {adoption.edge_result.root_result.persistence.root_record_sha256}\n"
        f"Declaration SHA-256: {adoption.declaration.sequence_record_sha256}\n"
        f"Endpoint edge SHA-256: {adoption.edge_result.persistence.edge_record_sha256}\n"
        f"Appended evidence members: {len(items)}\n"
        "All locator fields below are blank and explicit; historical receipts and launch paths are not locator authority."
    )


def second_changed_basis_epoch_reentry_success_receipt(
    result: ChromiumResearchSecondChangedBasisEpochReentryResult,
) -> str:
    fresh = result.fresh_reentry
    return (
        "Success — exact historical 46D second-basis session freshly reconstructed through 37A. Mounted governed session unchanged.\n"
        f"Retained first root SHA-256: {fresh.prior_continuation_reentry.prior_root_backed_reentry.loaded_root.verification.root_record_sha256}\n"
        f"Second root SHA-256: {fresh.loaded_root.verification.root_record_sha256}\n"
        f"Declaration SHA-256: {fresh.loaded_declaration.verification.sequence_record_sha256}\n"
        f"Endpoint edge SHA-256: {fresh.controller.declared_endpoint.verification.edge_record_sha256}\n"
        f"Appended evidence members freshly relinked: {len(fresh.loaded_appended_members)}\n"
        "Fresh-process reconstructability is proven for this exact second-basis session, but no durable 37B overlay was written and no launch provenance or global head authority changed."
    )


class ResearchSecondChangedBasisEpochReentryControls(Vertical):
    """Explicit 46E locator form for one public 37A reconstruction proof."""

    def __init__(
        self,
        adoption_result: ChromiumResearchSecondChangedBasisSessionAdoptionResult,
        appended_items: Iterable[ChromiumPageResearchWorkingSetItem],
        prior_result: ChromiumResearchSecondChangedBasisEpochReentryResult | None = None,
    ) -> None:
        if type(adoption_result) is not ChromiumResearchSecondChangedBasisSessionAdoptionResult:
            raise TypeError(
                "adoption_result must be exactly ChromiumResearchSecondChangedBasisSessionAdoptionResult."
            )
        items = tuple(appended_items)
        if not items:
            raise ValueError("appended_items must contain at least one exact changed-basis member.")
        for item in items:
            _member_kind(item)
        if prior_result is not None and prior_result.adoption_result is not adoption_result:
            raise ValueError("Prior 46E proof does not belong to this exact 46D adoption.")
        super().__init__(id="research-second-changed-basis-epoch-reentry-controls")
        self.adoption_result = adoption_result
        self.appended_items = items
        self.prior_result = prior_result

    def compose(self) -> ComposeResult:
        locked = self.prior_result is not None
        yield Static(
            "Verify second-basis fresh-process re-entry",
            id="research-second-changed-basis-epoch-reentry-title",
        )
        yield Static(
            SECOND_CHANGED_BASIS_EPOCH_REENTRY_AUTHORITY_NOTICE,
            id="research-second-changed-basis-epoch-reentry-authority-notice",
            markup=False,
        )
        yield Static(
            _summary(self.adoption_result, self.appended_items),
            id="research-second-changed-basis-epoch-reentry-summary",
            markup=False,
        )

        yield Input(
            placeholder="Explicit current prior 35D/35E continuation overlay path",
            id="research-second-changed-basis-epoch-reentry-prior-continuation-overlay-source",
            classes="research-second-changed-basis-epoch-reentry-input",
            disabled=locked,
        )

        for index, item in enumerate(self.appended_items):
            kind = _member_kind(item)
            yield Static(
                f"Appended member {index} — {kind}\nNote text:\n{item.note.note_text}",
                classes="research-second-changed-basis-epoch-reentry-member-summary",
                id=f"research-second-changed-basis-epoch-reentry-member-{index}-summary",
                markup=False,
            )
            if kind == "comparison note":
                yield Input(
                    placeholder="Explicit current first capture path",
                    id=f"research-second-changed-basis-epoch-reentry-member-{index}-first-capture-source",
                    classes="research-second-changed-basis-epoch-reentry-input",
                    disabled=locked,
                )
                yield Input(
                    placeholder="Explicit current second capture path",
                    id=f"research-second-changed-basis-epoch-reentry-member-{index}-second-capture-source",
                    classes="research-second-changed-basis-epoch-reentry-input",
                    disabled=locked,
                )
            else:
                yield Input(
                    placeholder="Explicit current capture path",
                    id=f"research-second-changed-basis-epoch-reentry-member-{index}-capture-source",
                    classes="research-second-changed-basis-epoch-reentry-input",
                    disabled=locked,
                )
            yield Input(
                placeholder="Explicit current note sidecar path",
                id=f"research-second-changed-basis-epoch-reentry-member-{index}-note-source",
                classes="research-second-changed-basis-epoch-reentry-input",
                disabled=locked,
            )

        fields = (
            ("changed-working-set-source", "Explicit current changed working-set path"),
            ("changed-note-source", "Explicit current changed working-set-note path"),
            ("transition-source", "Explicit current second 33B transition path"),
            ("root-source", "Explicit current second 34A root path"),
            ("first-edge-source", "Explicit current first post-second-root edge path"),
            ("declaration-source", "Explicit current second-root-backed declaration path"),
        )
        for suffix, placeholder in fields:
            yield Input(
                placeholder=placeholder,
                id=f"research-second-changed-basis-epoch-reentry-{suffix}",
                classes="research-second-changed-basis-epoch-reentry-input",
                disabled=locked,
            )

        yield Button(
            "Verify 37A fresh reconstruction — mounted session will not change",
            id="verify-research-second-changed-basis-epoch-reentry",
            variant="warning",
            disabled=locked,
        )
        yield Static(
            second_changed_basis_epoch_reentry_success_receipt(self.prior_result)
            if self.prior_result is not None
            else "",
            id="research-second-changed-basis-epoch-reentry-status",
            markup=False,
        )

    def lock_after_success(
        self,
        result: ChromiumResearchSecondChangedBasisEpochReentryResult,
    ) -> None:
        if result.adoption_result is not self.adoption_result:
            raise ValueError("46E result does not retain this exact 46D adoption.")
        self.prior_result = result
        for widget in self.query(".research-second-changed-basis-epoch-reentry-input"):
            if isinstance(widget, Input):
                widget.disabled = True
        self.query_one("#verify-research-second-changed-basis-epoch-reentry", Button).disabled = True
        self.query_one("#research-second-changed-basis-epoch-reentry-status", Static).update(
            second_changed_basis_epoch_reentry_success_receipt(result)
        )


__all__ = [
    "SECOND_CHANGED_BASIS_EPOCH_REENTRY_AUTHORITY_NOTICE",
    "ResearchSecondChangedBasisEpochReentryControls",
    "second_changed_basis_epoch_reentry_success_receipt",
]
