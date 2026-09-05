from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
import hmac
from pathlib import Path
from typing import Any

from .chromium_research_paragraph_text_selection_load import (
    ChromiumPageResearchLoadedParagraphTextSelectionRecord,
)
from .chromium_research_paragraph_text_selection_comparison_note_load import (
    ChromiumPageResearchLoadedParagraphTextSelectionComparisonNoteRecord,
)
from .chromium_research_paragraph_text_selection_note_load import (
    ChromiumPageResearchLoadedParagraphTextSelectionNoteRecord,
)
from .chromium_research_selection_note_load import (
    ChromiumPageResearchLoadedParagraphNoteRecord,
)
from .chromium_research_working_set import (
    ChromiumPageResearchWorkingSetItem,
    ChromiumPageResearchWorkingSetRecord,
    create_chromium_research_working_set,
)
from .chromium_research_working_set_persistence import (
    ChromiumPageResearchWorkingSetMemberReference,
    ChromiumPageResearchWorkingSetVerificationEvidence,
    verify_chromium_research_working_set,
)


_WORKING_SET_MODE = "caller_explicit_ordered_relinked_research_working_set"

_PARAGRAPH_NOTE_KIND = "paragraph_note"
_PARAGRAPH_NOTE_FORMAT = "pyxis.chromium.research_paragraph_note.v1"
_EXACT_RANGE_SELECTION_KIND = "exact_range_selection"
_EXACT_RANGE_SELECTION_FORMAT = "pyxis.chromium.research_paragraph_text_selection.v1"
_EXACT_RANGE_NOTE_KIND = "exact_range_note"
_EXACT_RANGE_NOTE_FORMAT = "pyxis.chromium.research_paragraph_text_selection_note.v1"
_COMPARISON_NOTE_KIND = "comparison_note"
_COMPARISON_NOTE_FORMAT = (
    "pyxis.chromium.research_paragraph_text_selection_comparison_note.v1"
)


class ChromiumResearchWorkingSetMemberMismatchError(ValueError):
    """Raised when a verified working-set sidecar does not match supplied members."""


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchLoadedWorkingSetRecord:
    """One verified durable working set relinked to explicit loaded members.

    `verification` is fresh 20B file-local verification evidence. `working_set` is
    a newly reconstructed 20A record that retains the exact caller-supplied loaded
    member objects in their supplied order, including intentional duplicates.

    Relinking proves only ordered member-identity coherence. It does not prove that
    member files still exist, authenticate any member or source, establish semantic
    relationship or importance, or grant quotation/citation or claim authority.
    """

    verification: ChromiumPageResearchWorkingSetVerificationEvidence
    working_set: ChromiumPageResearchWorkingSetRecord


def load_chromium_research_working_set(
    items: Iterable[ChromiumPageResearchWorkingSetItem],
    working_set_source: Path,
) -> ChromiumPageResearchLoadedWorkingSetRecord:
    """Verify one 20B sidecar and relink it to explicit ordered loaded members.

    The caller supplies the complete member sequence. Pyxis does not search for
    members by digest, sidecar path, source identity, note text, URL, or semantic
    similarity, and it does not reorder or deduplicate the supplied sequence.

    The working-set sidecar is freshly verified from `working_set_source`. The
    supplied members are then re-established through the existing 20A in-memory
    coherence boundary, and each position must exactly match the persisted member
    kind, sidecar format, and member-record SHA-256 for that same position.

    Individual member sidecars are not reread. Therefore already-loaded members may
    be relinked into the working set even if those member files have moved or become
    unavailable after their earlier successful 17D/18D/19D/49B relinking.
    """

    try:
        supplied_items = tuple(items)
    except TypeError as exc:
        raise TypeError("items must be an iterable of relinked research records.") from exc

    verification = verify_chromium_research_working_set(working_set_source)
    if verification.working_set_mode != _WORKING_SET_MODE:
        raise ChromiumResearchWorkingSetMemberMismatchError(
            "Verified working-set sidecar uses an unsupported working-set mode."
        )

    if len(supplied_items) != len(verification.items):
        raise ChromiumResearchWorkingSetMemberMismatchError(
            "Supplied working-set member count does not match the verified sidecar."
        )

    working_set = create_chromium_research_working_set(supplied_items)
    if working_set.working_set_mode != verification.working_set_mode:
        raise ChromiumResearchWorkingSetMemberMismatchError(
            "Reconstructed working-set mode does not match the verified sidecar."
        )

    for index, (item, expected) in enumerate(zip(working_set.items, verification.items)):
        observed = _loaded_member_reference(item, index=index)
        _validate_member_reference(expected, observed, index=index)

    return ChromiumPageResearchLoadedWorkingSetRecord(
        verification=verification,
        working_set=working_set,
    )


def _loaded_member_reference(
    item: ChromiumPageResearchWorkingSetItem,
    *,
    index: int,
) -> ChromiumPageResearchWorkingSetMemberReference:
    if isinstance(item, ChromiumPageResearchLoadedParagraphNoteRecord):
        return _reference_from_verification(
            member_kind=_PARAGRAPH_NOTE_KIND,
            expected_format=_PARAGRAPH_NOTE_FORMAT,
            member_format=item.verification.note_format,
            member_record_sha256=item.verification.note_record_sha256,
            index=index,
        )
    if isinstance(item, ChromiumPageResearchLoadedParagraphTextSelectionRecord):
        return _reference_from_verification(
            member_kind=_EXACT_RANGE_SELECTION_KIND,
            expected_format=_EXACT_RANGE_SELECTION_FORMAT,
            member_format=item.verification.selection_format,
            member_record_sha256=item.verification.selection_record_sha256,
            index=index,
        )
    if isinstance(item, ChromiumPageResearchLoadedParagraphTextSelectionNoteRecord):
        return _reference_from_verification(
            member_kind=_EXACT_RANGE_NOTE_KIND,
            expected_format=_EXACT_RANGE_NOTE_FORMAT,
            member_format=item.verification.note_format,
            member_record_sha256=item.verification.note_record_sha256,
            index=index,
        )
    if isinstance(
        item,
        ChromiumPageResearchLoadedParagraphTextSelectionComparisonNoteRecord,
    ):
        return _reference_from_verification(
            member_kind=_COMPARISON_NOTE_KIND,
            expected_format=_COMPARISON_NOTE_FORMAT,
            member_format=item.verification.note_format,
            member_record_sha256=item.verification.note_record_sha256,
            index=index,
        )
    raise TypeError(f"items[{index}] has an unsupported relinked member family.")


def _reference_from_verification(
    *,
    member_kind: str,
    expected_format: str,
    member_format: object,
    member_record_sha256: object,
    index: int,
) -> ChromiumPageResearchWorkingSetMemberReference:
    if member_format != expected_format:
        raise ChromiumResearchWorkingSetMemberMismatchError(
            f"Supplied working-set member {index} retains an unsupported sidecar format."
        )
    if not _is_sha256(member_record_sha256):
        raise ChromiumResearchWorkingSetMemberMismatchError(
            f"Supplied working-set member {index} retains an invalid record SHA-256."
        )
    return ChromiumPageResearchWorkingSetMemberReference(
        member_kind=member_kind,
        member_format=expected_format,
        member_record_sha256=member_record_sha256,
    )


def _validate_member_reference(
    expected: ChromiumPageResearchWorkingSetMemberReference,
    observed: ChromiumPageResearchWorkingSetMemberReference,
    *,
    index: int,
) -> None:
    if expected.member_kind != observed.member_kind:
        raise ChromiumResearchWorkingSetMemberMismatchError(
            f"Verified working-set item {index} references a different member kind."
        )
    if expected.member_format != observed.member_format:
        raise ChromiumResearchWorkingSetMemberMismatchError(
            f"Verified working-set item {index} references a different member format."
        )
    if not hmac.compare_digest(
        expected.member_record_sha256,
        observed.member_record_sha256,
    ):
        raise ChromiumResearchWorkingSetMemberMismatchError(
            f"Verified working-set item {index} references a different member record."
        )


def _is_sha256(value: Any) -> bool:
    return (
        type(value) is str
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )
