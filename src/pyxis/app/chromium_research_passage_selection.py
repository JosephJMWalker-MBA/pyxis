from __future__ import annotations

from dataclasses import dataclass

from .chromium_paragraphs import ChromiumPageParagraphEvidence
from .chromium_research_capture_load import ChromiumPageResearchLoadedCaptureEvidence


_CAPTURE_FORMAT = "pyxis.chromium.research_capture.v1"
_ACQUISITION_MODE = "sequential_non_atomic_url_coherent"
_ACQUISITION_ORDER = (
    "page",
    "links",
    "headings",
    "metadata",
    "paragraphs",
    "tables",
    "lists",
)
_SELECTION_MODE = "caller_explicit_returned_paragraph_ordinal"


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchParagraphSelectionEvidence:
    """One explicit caller selection of already-loaded paragraph evidence.

    `source` is retained by exact object identity so the 16C verified-capture
    origin remains inspectable. `paragraph` is the exact paragraph object already
    present inside that source bundle; selection does not copy or upgrade its
    text into a quotation, citation, relevance, truth, or locator claim.
    """

    selection_mode: str
    source: ChromiumPageResearchLoadedCaptureEvidence
    paragraph: ChromiumPageParagraphEvidence


def select_chromium_research_capture_paragraph(
    source: ChromiumPageResearchLoadedCaptureEvidence,
    *,
    paragraph_ordinal: int,
) -> ChromiumPageResearchParagraphSelectionEvidence:
    """Select one already-returned paragraph from verified rehydrated evidence.

    The caller owns the choice by supplying an exact 1-based paragraph ordinal.
    This operation performs no browser acquisition, capture-file read, checksum
    verification, persistence, ranking, semantic interpretation, text expansion,
    quotation verification, citation resolution, or locator stabilization.

    If the persisted paragraph observation was collection-truncated, an ordinal
    that is known to exist but is outside the returned bounded prefix is rejected
    rather than silently reacquired or reconstructed.
    """

    if not isinstance(source, ChromiumPageResearchLoadedCaptureEvidence):
        raise TypeError("source must be ChromiumPageResearchLoadedCaptureEvidence.")
    if type(paragraph_ordinal) is not int:
        raise TypeError("paragraph_ordinal must be an integer.")
    if paragraph_ordinal < 1:
        raise ValueError("paragraph_ordinal must be >= 1.")

    _validate_selection_source(source)
    paragraphs = source.bundle.paragraphs

    if paragraph_ordinal > paragraphs.paragraph_count:
        raise ValueError(
            "paragraph_ordinal does not identify an observed paragraph in the source evidence."
        )
    if paragraph_ordinal > len(paragraphs.paragraphs):
        raise ValueError(
            "paragraph_ordinal identifies evidence outside the bounded returned paragraph prefix; "
            "selection does not reacquire or expand browser evidence."
        )

    paragraph = paragraphs.paragraphs[paragraph_ordinal - 1]
    if paragraph.ordinal != paragraph_ordinal:
        raise ValueError("returned paragraph ordinals are not contiguous DOM order.")

    return ChromiumPageResearchParagraphSelectionEvidence(
        selection_mode=_SELECTION_MODE,
        source=source,
        paragraph=paragraph,
    )


def _validate_selection_source(source: ChromiumPageResearchLoadedCaptureEvidence) -> None:
    verification = source.verification
    bundle = source.bundle

    if verification.capture_format != _CAPTURE_FORMAT:
        raise ValueError("source capture format is unsupported for paragraph selection.")
    if bundle.acquisition_mode != _ACQUISITION_MODE:
        raise ValueError("source bundle acquisition mode is unsupported for paragraph selection.")
    if bundle.acquisition_order != _ACQUISITION_ORDER:
        raise ValueError("source bundle acquisition order is unsupported for paragraph selection.")

    for label, verification_value, bundle_value in (
        ("endpoint", verification.endpoint, bundle.endpoint),
        ("target_id", verification.target_id, bundle.target_id),
        ("url", verification.url, bundle.url),
        ("acquisition_mode", verification.acquisition_mode, bundle.acquisition_mode),
        ("acquisition_order", verification.acquisition_order, bundle.acquisition_order),
    ):
        if verification_value != bundle_value:
            raise ValueError(f"source verification {label} is incoherent with the loaded bundle.")

    paragraphs = bundle.paragraphs
    for label, member_value, bundle_value in (
        ("endpoint", paragraphs.endpoint, bundle.endpoint),
        ("target_id", paragraphs.target_id, bundle.target_id),
        ("url", paragraphs.url, bundle.url),
    ):
        if member_value != bundle_value:
            raise ValueError(f"source paragraph evidence {label} is incoherent with the bundle.")

    if paragraphs.source != "document.querySelectorAll('p')":
        raise ValueError("source paragraph evidence selector is unsupported.")
    if paragraphs.paragraph_count < 0:
        raise ValueError("source paragraph count is negative.")
    if paragraphs.paragraph_limit < 0:
        raise ValueError("source paragraph limit is negative.")
    if len(paragraphs.paragraphs) > paragraphs.paragraph_limit:
        raise ValueError("source paragraph evidence exceeds its recorded collection limit.")
    if paragraphs.paragraph_count < len(paragraphs.paragraphs):
        raise ValueError("source paragraph count is smaller than returned evidence.")
    if paragraphs.truncated != (paragraphs.paragraph_count > len(paragraphs.paragraphs)):
        raise ValueError("source paragraph collection truncation is incoherent.")

    for expected_ordinal, paragraph in enumerate(paragraphs.paragraphs, start=1):
        if paragraph.ordinal != expected_ordinal:
            raise ValueError("returned paragraph ordinals are not contiguous DOM order.")
        if paragraph.text_character_count < 0:
            raise ValueError("source paragraph character count is negative.")
        if paragraph.text_limit < 0:
            raise ValueError("source paragraph text limit is negative.")
        if len(paragraph.text_prefix) > paragraph.text_limit:
            raise ValueError("source paragraph text exceeds its recorded text limit.")
        if paragraph.text_character_count < len(paragraph.text_prefix):
            raise ValueError("source paragraph character count is smaller than returned text.")
        if paragraph.truncated != (
            paragraph.text_character_count > len(paragraph.text_prefix)
        ):
            raise ValueError("source paragraph text truncation is incoherent.")
