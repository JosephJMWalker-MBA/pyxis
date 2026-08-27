from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Button, Input, Static

from pyxis.app.chromium_research_session_rollover import ChromiumResearchSessionRolloverResult


ReentryT = TypeVar("ReentryT")
ResultT = TypeVar("ResultT")


@dataclass(frozen=True, slots=True)
class _CumulativeCheckpointTextualSpec:
    """Concrete wording and DOM IDs for one cumulative checkpoint form family."""

    controls_id: str
    title: str
    title_id: str
    authority_notice: str
    authority_notice_id: str
    candidate_id: str
    current_overlay_label: str
    current_overlay_label_id: str
    current_overlay_placeholder: str
    current_overlay_input_id: str
    successor_label: str
    successor_label_id: str
    successor_placeholder: str
    successor_input_id: str
    declaration_label: str
    declaration_label_id: str
    declaration_placeholder: str
    declaration_input_id: str
    overlay_label: str
    overlay_label_id: str
    overlay_placeholder: str
    overlay_input_id: str
    save_label: str
    save_button_id: str
    pending_status: str
    status_id: str

    @property
    def input_ids(self) -> tuple[str, str, str, str]:
        return (
            self.current_overlay_input_id,
            self.successor_input_id,
            self.declaration_input_id,
            self.overlay_input_id,
        )


class _CumulativeCheckpointTextualControls(Vertical, Generic[ReentryT, ResultT]):
    """Private mechanics shared by the independently proven cumulative forms.

    The base knows no root count, epoch, milestone, persistence format, or ancestry
    semantics. Concrete public controls retain their exact type checks, wording,
    selectors, and receipt functions. This base owns only composition of four blank
    explicit path inputs and post-success locking of the old form.
    """

    def __init__(
        self,
        current_reentry: ReentryT,
        rollover: ChromiumResearchSessionRolloverResult,
        *,
        spec: _CumulativeCheckpointTextualSpec,
        candidate_receipt: str,
        success_receipt: Callable[[ResultT], str],
    ) -> None:
        super().__init__(id=spec.controls_id)
        self.current_reentry = current_reentry
        self.rollover = rollover
        self.persistence_result: ResultT | None = None
        self._cumulative_checkpoint_spec = spec
        self._cumulative_checkpoint_candidate_receipt = candidate_receipt
        self._cumulative_checkpoint_success_receipt = success_receipt

    def compose(self) -> ComposeResult:
        spec = self._cumulative_checkpoint_spec
        yield Static(spec.title, id=spec.title_id)
        yield Static(
            spec.authority_notice,
            id=spec.authority_notice_id,
            markup=False,
        )
        yield Static(
            self._cumulative_checkpoint_candidate_receipt,
            id=spec.candidate_id,
            markup=False,
        )
        yield Static(spec.current_overlay_label, id=spec.current_overlay_label_id)
        yield Input(
            placeholder=spec.current_overlay_placeholder,
            id=spec.current_overlay_input_id,
        )
        yield Static(spec.successor_label, id=spec.successor_label_id)
        yield Input(
            placeholder=spec.successor_placeholder,
            id=spec.successor_input_id,
        )
        yield Static(spec.declaration_label, id=spec.declaration_label_id)
        yield Input(
            placeholder=spec.declaration_placeholder,
            id=spec.declaration_input_id,
        )
        yield Static(spec.overlay_label, id=spec.overlay_label_id)
        yield Input(
            placeholder=spec.overlay_placeholder,
            id=spec.overlay_input_id,
        )
        yield Button(
            spec.save_label,
            id=spec.save_button_id,
            variant="warning",
        )
        yield Static(
            spec.pending_status,
            id=spec.status_id,
            markup=False,
        )

    def _lock_cumulative_checkpoint_after_success(
        self,
        result: ResultT,
        *,
        result_type: type[Any],
        result_type_error: str,
        current_identity_error: str,
        rollover_identity_error: str,
    ) -> None:
        """Apply only the shared old-form locking mechanics after concrete proof."""

        if not isinstance(result, result_type):
            raise TypeError(result_type_error)
        if result.current_reentry is not self.current_reentry:
            raise ValueError(current_identity_error)
        if result.rollover is not self.rollover:
            raise ValueError(rollover_identity_error)

        self.persistence_result = result
        spec = self._cumulative_checkpoint_spec
        for input_id in spec.input_ids:
            self.query_one(f"#{input_id}", Input).disabled = True
        self.query_one(f"#{spec.save_button_id}", Button).disabled = True
        self.query_one(f"#{spec.status_id}", Static).update(
            self._cumulative_checkpoint_success_receipt(result)
        )


__all__: list[str] = []
