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
from pyxis.app.chromium_research_selection_note_load import (
    ChromiumPageResearchLoadedParagraphNoteRecord,
)
from pyxis.app.chromium_research_third_changed_basis_epoch_reentry import (
    ChromiumResearchThirdChangedBasisEpochReentryResult,
)
from pyxis.app.chromium_research_third_changed_basis_session_adoption import (
    ChromiumResearchThirdChangedBasisSessionAdoptionResult,
)
from pyxis.app.chromium_research_working_set import ChromiumPageResearchWorkingSetItem


THIRD_CHANGED_BASIS_EPOCH_REENTRY_AUTHORITY_NOTICE = (
    "Verify that the exact historical 47D third-basis session can be freshly "
    "reconstructed through existing 40A from explicit current durable locators. "
    "This writes no 40B overlay, does not replace the mounted governed session, "
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
    adoption: ChromiumResearchThirdChangedBasisSessionAdoptionResult,
    items: tuple[ChromiumPageResearchWorkingSetItem, ...],
) -> str:
    retained_prior = adoption.edge_result.root_result.transition_result.continuation_reentry
    retained_second_epoch = retained_prior.prior_second_basis_epoch_reentry
    return (
        "ADOPTED THIRD-BASIS SESSION — 40A RESTARTABILITY NOT YET PROVEN\n"
        f"Retained first root SHA-256: "
        f"{retained_second_epoch.prior_continuation_reentry.prior_root_backed_reentry.loaded_root.verification.root_record_sha256}\n"
        f"Retained second root SHA-256: "
        f"{retained_second_epoch.loaded_root.verification.root_record_sha256}\n"
        f"Third root SHA-256: {adoption.edge_result.root_result.persistence.root_record_sha256}\n"
        f"Declaration SHA-256: {adoption.declaration.sequence_record_sha256}\n"
        f"Endpoint edge SHA-256: {adoption.edge_result.persistence.edge_record_sha256}\n"
        f"Appended evidence members: {len(items)}\n"
        "All locator fields below are blank and explicit; historical receipts and launch paths are not locator authority."
    )


def third_changed_basis_epoch_reentry_success_receipt(
    result: ChromiumResearchThirdChangedBasisEpochReentryResult,
) -> str:
    fresh = result.fresh_reentry
    prior = fresh.prior_second_basis_epoch_continuation_reentry
    second_epoch = prior.prior_second_basis_epoch_reentry
    return (
        "Success — exact historical 47D third-basis session freshly reconstructed through 40A. Mounted governed session unchanged.\n"
        f"Retained first root SHA-256: "
        f"{second_epoch.prior_continuation_reentry.prior_root_backed_reentry.loaded_root.verification.root_record_sha256}\n"
        f"Retained second root SHA-256: {second_epoch.loaded_root.verification.root_record_sha256}\n"
        f"Third root SHA-256: {fresh.loaded_root.verification.root_record_sha256}\n"
        f"Declaration SHA-256: {fresh.loaded_declaration.verification.sequence_record_sha256}\n"
        f"Endpoint edge SHA-256: {fresh.controller.declared_endpoint.verification.edge_record_sha256}\n"
        f"Appended evidence members freshly relinked: {len(fresh.loaded_appended_members)}\n"
        "Fresh-process reconstructability is proven for this exact third-basis session, but no durable 40B overlay was written and no launch provenance or global head authority changed."
    )


class ResearchThirdChangedBasisEpochReentryControls(Vertical):
    """Explicit 47E locator form for one public 40A reconstruction proof."""

    def __init__(
        self,
        adoption_result: ChromiumResearchThirdChangedBasisSessionAdoptionResult,
        appended_items: Iterable[ChromiumPageResearchWorkingSetItem],
        prior_result: ChromiumResearchThirdChangedBasisEpochReentryResult | None = None,
    ) -> None:
        if type(adoption_result) is not ChromiumResearchThirdChangedBasisSessionAdoptionResult:
            raise TypeError(
                "adoption_result must be exactly ChromiumResearchThirdChangedBasisSessionAdoptionResult."
            )
        items = tuple(appended_items)
        if not items:
            raise ValueError("appended_items must contain at least one exact changed-basis member.")
        for item in items:
            _member_kind(item)
        if prior_result is not None and prior_result.adoption_result is not adoption_result:
            raise ValueError("Prior 47E proof does not belong to this exact 47D adoption.")
        super().__init__(id="research-third-changed-basis-epoch-reentry-controls")
        self.adoption_result = adoption_result
        self.appended_items = items
        self.prior_result = prior_result

    def compose(self) -> ComposeResult:
        locked = self.prior_result is not None
        yield Static(
            "Verify third-basis fresh-process re-entry",
            id="research-third-changed-basis-epoch-reentry-title",
        )
        yield Static(
            THIRD_CHANGED_BASIS_EPOCH_REENTRY_AUTHORITY_NOTICE,
            id="research-third-changed-basis-epoch-reentry-authority-notice",
            markup=False,
        )
        yield Static(
            _summary(self.adoption_result, self.appended_items),
            id="research-third-changed-basis-epoch-reentry-summary",
            markup=False,
        )

        yield Input(
            placeholder="Explicit current prior 37C/37D second-epoch continuation overlay path",
            id="research-third-changed-basis-epoch-reentry-prior-continuation-overlay-source",
            classes="research-third-changed-basis-epoch-reentry-input",
            disabled=locked,
        )

        for index, item in enumerate(self.appended_items):
            kind = _member_kind(item)
            yield Static(
                f"Appended member {index} — {kind}\nNote text:\n{item.note.note_text}",
                classes="research-third-changed-basis-epoch-reentry-member-summary",
                id=f"research-third-changed-basis-epoch-reentry-member-{index}-summary",
                markup=False,
            )
            if kind == "comparison note":
                yield Input(
                    placeholder="Explicit current first capture path",
                    id=f"research-third-changed-basis-epoch-reentry-member-{index}-first-capture-source",
                    classes="research-third-changed-basis-epoch-reentry-input",
                    disabled=locked,
                )
                yield Input(
                    placeholder="Explicit current second capture path",
                    id=f"research-third-changed-basis-epoch-reentry-member-{index}-second-capture-source",
                    classes="research-third-changed-basis-epoch-reentry-input",
                    disabled=locked,
                )
            else:
                yield Input(
                    placeholder="Explicit current capture path",
                    id=f"research-third-changed-basis-epoch-reentry-member-{index}-capture-source",
                    classes="research-third-changed-basis-epoch-reentry-input",
                    disabled=locked,
                )
            yield Input(
                placeholder="Explicit current note sidecar path",
                id=f"research-third-changed-basis-epoch-reentry-member-{index}-note-source",
                classes="research-third-changed-basis-epoch-reentry-input",
                disabled=locked,
            )

        fields = (
            ("changed-working-set-source", "Explicit current changed working-set path"),
            ("changed-note-source", "Explicit current changed working-set-note path"),
            ("transition-source", "Explicit current third 33B transition path"),
            ("root-source", "Explicit current third 34A root path"),
            ("first-edge-source", "Explicit current first post-third-root edge path"),
            ("declaration-source", "Explicit current third-root-backed declaration path"),
        )
        for suffix, placeholder in fields:
            yield Input(
                placeholder=placeholder,
                id=f"research-third-changed-basis-epoch-reentry-{suffix}",
                classes="research-third-changed-basis-epoch-reentry-input",
                disabled=locked,
            )

        yield Button(
            "Verify 40A fresh reconstruction — mounted session will not change",
            id="verify-research-third-changed-basis-epoch-reentry",
            variant="warning",
            disabled=locked,
        )
        yield Static(
            third_changed_basis_epoch_reentry_success_receipt(self.prior_result)
            if self.prior_result is not None
            else "",
            id="research-third-changed-basis-epoch-reentry-status",
            markup=False,
        )

    def lock_after_success(
        self,
        result: ChromiumResearchThirdChangedBasisEpochReentryResult,
    ) -> None:
        if result.adoption_result is not self.adoption_result:
            raise ValueError("47E result does not retain this exact 47D adoption.")
        self.prior_result = result
        for widget in self.query(".research-third-changed-basis-epoch-reentry-input"):
            if isinstance(widget, Input):
                widget.disabled = True
        self.query_one("#verify-research-third-changed-basis-epoch-reentry", Button).disabled = True
        self.query_one("#research-third-changed-basis-epoch-reentry-status", Static).update(
            third_changed_basis_epoch_reentry_success_receipt(result)
        )


__all__ = [
    "THIRD_CHANGED_BASIS_EPOCH_REENTRY_AUTHORITY_NOTICE",
    "ResearchThirdChangedBasisEpochReentryControls",
    "third_changed_basis_epoch_reentry_success_receipt",
]
