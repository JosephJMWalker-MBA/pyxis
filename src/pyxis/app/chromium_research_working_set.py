from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
import hmac
from typing import TypeAlias

from .chromium_research_paragraph_text_selection import (
    select_chromium_research_paragraph_text,
)
from .chromium_research_paragraph_text_selection_load import (
    ChromiumPageResearchLoadedParagraphTextSelectionRecord,
)
from .chromium_research_paragraph_text_selection_persistence import (
    ChromiumPageResearchParagraphTextSelectionVerificationEvidence,
)
from .chromium_research_paragraph_text_selection_comparison_note import (
    create_chromium_research_paragraph_text_selection_comparison_note,
)
from .chromium_research_paragraph_text_selection_comparison_note_load import (
    ChromiumPageResearchLoadedParagraphTextSelectionComparisonNoteRecord,
)
from .chromium_research_paragraph_text_selection_comparison_note_persistence import (
    ChromiumPageResearchParagraphTextSelectionComparisonNoteVerificationEvidence,
)
from .chromium_research_paragraph_text_selection_note import (
    create_chromium_research_paragraph_text_selection_note,
)
from .chromium_research_paragraph_text_selection_note_load import (
    ChromiumPageResearchLoadedParagraphTextSelectionNoteRecord,
)
from .chromium_research_paragraph_text_selection_note_persistence import (
    ChromiumPageResearchParagraphTextSelectionNoteVerificationEvidence,
)
from .chromium_research_selection_note import create_chromium_research_paragraph_note
from .chromium_research_selection_note_load import (
    ChromiumPageResearchLoadedParagraphNoteRecord,
)
from .chromium_research_selection_note_persistence import (
    ChromiumPageResearchParagraphNoteVerificationEvidence,
)


_WORKING_SET_MODE = "caller_explicit_ordered_relinked_research_working_set"

ChromiumPageResearchWorkingSetItem: TypeAlias = (
    ChromiumPageResearchLoadedParagraphNoteRecord
    | ChromiumPageResearchLoadedParagraphTextSelectionRecord
    | ChromiumPageResearchLoadedParagraphTextSelectionNoteRecord
    | ChromiumPageResearchLoadedParagraphTextSelectionComparisonNoteRecord
)


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchWorkingSetRecord:
    """One explicit caller-owned ordered grouping of relinked research records.

    `items` is an immutable snapshot of the caller's requested order. Every tuple
    member is the exact supplied loaded record object; duplicates are preserved.

    Working-set membership records only that the caller chose to carry these
    already-relinked research records forward together. It does not claim that
    the records are related, mutually supportive, contradictory, equally useful,
    complete, representative, authentic, true, or otherwise semantically linked.
    """

    working_set_mode: str
    items: tuple[ChromiumPageResearchWorkingSetItem, ...]


def create_chromium_research_working_set(
    items: Iterable[ChromiumPageResearchWorkingSetItem],
) -> ChromiumPageResearchWorkingSetRecord:
    """Create one immutable human-owned working set from explicit loaded records.

    Membership is ordered and non-empty. The iterable is snapshotted to a tuple so
    later mutation of a caller-owned list cannot silently change the working set.
    Duplicate records are retained because Pyxis does not infer that repetition is
    accidental or semantically redundant.

    Each member must be one of the established relinked research record families:
    17D paragraph note, 49B bare exact-range selection, 18D exact-range note, or
    19D comparison note. The operation re-establishes each member's in-memory
    selection/note contract through existing public selectors/constructors and checks
    that the retained sidecar-verification facts still agree with the nested
    reconstructed source/selection/note objects. It deliberately does not reread
    any sidecar file.

    Therefore successful creation proves working-set membership over coherent
    already-loaded application evidence. It is not fresh file verification or
    fresh source relinking, and it adds no source authentication, semantic relation,
    ranking, deduplication, claim support, citation authority, or machine judgment.
    """

    try:
        frozen_items = tuple(items)
    except TypeError as exc:
        raise TypeError("items must be an iterable of relinked research records.") from exc

    if not frozen_items:
        raise ValueError("research working set must contain at least one item.")

    for index, item in enumerate(frozen_items):
        _validate_working_set_item(item, index=index)

    return ChromiumPageResearchWorkingSetRecord(
        working_set_mode=_WORKING_SET_MODE,
        items=frozen_items,
    )


def _validate_working_set_item(
    item: ChromiumPageResearchWorkingSetItem,
    *,
    index: int,
) -> None:
    if isinstance(item, ChromiumPageResearchLoadedParagraphNoteRecord):
        _validate_loaded_paragraph_note(item, index=index)
        return
    if isinstance(item, ChromiumPageResearchLoadedParagraphTextSelectionRecord):
        _validate_loaded_exact_range_selection(item, index=index)
        return
    if isinstance(item, ChromiumPageResearchLoadedParagraphTextSelectionNoteRecord):
        _validate_loaded_exact_range_note(item, index=index)
        return
    if isinstance(
        item,
        ChromiumPageResearchLoadedParagraphTextSelectionComparisonNoteRecord,
    ):
        _validate_loaded_comparison_note(item, index=index)
        return
    raise TypeError(
        f"items[{index}] must be a supported relinked paragraph-note, bare "
        "exact-range-selection, exact-range-note, or comparison-note record."
    )


def _validate_loaded_paragraph_note(
    item: ChromiumPageResearchLoadedParagraphNoteRecord,
    *,
    index: int,
) -> None:
    verification = item.verification
    note = item.note
    if not isinstance(verification, ChromiumPageResearchParagraphNoteVerificationEvidence):
        raise TypeError(f"items[{index}] paragraph-note verification evidence is unsupported.")

    rebuilt = create_chromium_research_paragraph_note(
        note.selection,
        note_text=note.note_text,
    )
    source_verification = note.selection.source.verification
    if (
        rebuilt.note_mode != note.note_mode
        or verification.source_capture_format != source_verification.capture_format
        or not _same_digest(
            verification.source_bundle_sha256,
            source_verification.bundle_sha256,
        )
        or verification.selection_mode != note.selection.selection_mode
        or verification.paragraph_ordinal != note.selection.paragraph.ordinal
        or verification.note_mode != note.note_mode
        or verification.note_text != note.note_text
    ):
        raise ValueError(
            f"items[{index}] paragraph-note verification is incoherent with its loaded note."
        )


def _validate_loaded_exact_range_selection(
    item: ChromiumPageResearchLoadedParagraphTextSelectionRecord,
    *,
    index: int,
) -> None:
    verification = item.verification
    selection = item.selection
    if not isinstance(
        verification,
        ChromiumPageResearchParagraphTextSelectionVerificationEvidence,
    ):
        raise TypeError(
            f"items[{index}] bare exact-range-selection verification evidence is unsupported."
        )

    paragraph_selection = selection.source
    rebuilt = select_chromium_research_paragraph_text(
        paragraph_selection,
        start_offset=selection.start_offset,
        end_offset=selection.end_offset,
    )
    source_verification = paragraph_selection.source.verification
    if (
        rebuilt.source is not paragraph_selection
        or rebuilt.selection_mode != selection.selection_mode
        or rebuilt.offset_unit != selection.offset_unit
        or rebuilt.start_offset != selection.start_offset
        or rebuilt.end_offset != selection.end_offset
        or rebuilt.selected_text != selection.selected_text
        or verification.source_capture_format != source_verification.capture_format
        or not _same_digest(
            verification.source_bundle_sha256,
            source_verification.bundle_sha256,
        )
        or verification.paragraph_selection_mode != paragraph_selection.selection_mode
        or verification.paragraph_ordinal != paragraph_selection.paragraph.ordinal
        or verification.text_selection_mode != selection.selection_mode
        or verification.offset_unit != selection.offset_unit
        or verification.start_offset != selection.start_offset
        or verification.end_offset != selection.end_offset
    ):
        raise ValueError(
            f"items[{index}] bare exact-range-selection verification is incoherent "
            "with its loaded selection."
        )


def _validate_loaded_exact_range_note(
    item: ChromiumPageResearchLoadedParagraphTextSelectionNoteRecord,
    *,
    index: int,
) -> None:
    verification = item.verification
    note = item.note
    if not isinstance(
        verification,
        ChromiumPageResearchParagraphTextSelectionNoteVerificationEvidence,
    ):
        raise TypeError(f"items[{index}] exact-range-note verification evidence is unsupported.")

    rebuilt = create_chromium_research_paragraph_text_selection_note(
        note.selection,
        note_text=note.note_text,
    )
    selection = note.selection
    paragraph_selection = selection.source
    source_verification = paragraph_selection.source.verification
    if (
        rebuilt.note_mode != note.note_mode
        or verification.source_capture_format != source_verification.capture_format
        or not _same_digest(
            verification.source_bundle_sha256,
            source_verification.bundle_sha256,
        )
        or verification.paragraph_selection_mode != paragraph_selection.selection_mode
        or verification.paragraph_ordinal != paragraph_selection.paragraph.ordinal
        or verification.text_selection_mode != selection.selection_mode
        or verification.offset_unit != selection.offset_unit
        or verification.start_offset != selection.start_offset
        or verification.end_offset != selection.end_offset
        or verification.note_mode != note.note_mode
        or verification.note_text != note.note_text
    ):
        raise ValueError(
            f"items[{index}] exact-range-note verification is incoherent with its loaded note."
        )


def _validate_loaded_comparison_note(
    item: ChromiumPageResearchLoadedParagraphTextSelectionComparisonNoteRecord,
    *,
    index: int,
) -> None:
    verification = item.verification
    note = item.note
    if not isinstance(
        verification,
        ChromiumPageResearchParagraphTextSelectionComparisonNoteVerificationEvidence,
    ):
        raise TypeError(f"items[{index}] comparison-note verification evidence is unsupported.")

    rebuilt = create_chromium_research_paragraph_text_selection_comparison_note(
        note.comparison,
        note_text=note.note_text,
    )
    first = note.comparison.first_selection
    second = note.comparison.second_selection
    first_paragraph = first.source
    second_paragraph = second.source
    first_source_verification = first_paragraph.source.verification
    second_source_verification = second_paragraph.source.verification

    if (
        rebuilt.note_mode != note.note_mode
        or verification.comparison_mode != note.comparison.comparison_mode
        or verification.first_source_capture_format
        != first_source_verification.capture_format
        or not _same_digest(
            verification.first_source_bundle_sha256,
            first_source_verification.bundle_sha256,
        )
        or verification.first_paragraph_selection_mode
        != first_paragraph.selection_mode
        or verification.first_paragraph_ordinal != first_paragraph.paragraph.ordinal
        or verification.first_text_selection_mode != first.selection_mode
        or verification.first_offset_unit != first.offset_unit
        or verification.first_start_offset != first.start_offset
        or verification.first_end_offset != first.end_offset
        or verification.second_source_capture_format
        != second_source_verification.capture_format
        or not _same_digest(
            verification.second_source_bundle_sha256,
            second_source_verification.bundle_sha256,
        )
        or verification.second_paragraph_selection_mode
        != second_paragraph.selection_mode
        or verification.second_paragraph_ordinal != second_paragraph.paragraph.ordinal
        or verification.second_text_selection_mode != second.selection_mode
        or verification.second_offset_unit != second.offset_unit
        or verification.second_start_offset != second.start_offset
        or verification.second_end_offset != second.end_offset
        or verification.note_mode != note.note_mode
        or verification.note_text != note.note_text
    ):
        raise ValueError(
            f"items[{index}] comparison-note verification is incoherent with its loaded note."
        )


def _same_digest(first: object, second: object) -> bool:
    return (
        type(first) is str
        and type(second) is str
        and hmac.compare_digest(first, second)
    )
