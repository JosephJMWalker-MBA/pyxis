from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from pyxis.app.chromium_research_initial_session_reentry import (
    reenter_chromium_research_initial_session,
)


def add_research_reopen_parser(subparsers: Any) -> None:
    """Expose one explicit, read-only fresh initial-session reconstruction."""

    parser = subparsers.add_parser(
        "research-reopen",
        help=(
            "Freshly reconstruct and inspect one initial research-session root "
            "from four explicit durable files; no browser or writes."
        ),
    )
    for flag, help_text in (
        ("capture", "Exact durable research_capture.v1 source location."),
        ("selection", "Exact saved bare paragraph-text-selection source location."),
        ("working-set", "Exact research_working_set.v2 source location."),
        ("note", "Exact research_working_set_note.v2 source location."),
    ):
        parser.add_argument(
            f"--{flag}",
            required=True,
            type=Path,
            help=help_text + " The path is location context, not evidence authority.",
        )
    parser.add_argument(
        "--include-content",
        action="store_true",
        help=(
            "Opt in to emitting verified bounded source excerpts and the distinct "
            "human rationale in JSON. May expose private research text in logs."
        ),
    )


def run_research_reopen_command(
    parser: argparse.ArgumentParser,
    args: argparse.Namespace,
) -> int:
    """Inspect an already-saved root without inventing session/head authority."""

    try:
        reentry = reenter_chromium_research_initial_session(
            capture_source=args.capture,
            selection_source=args.selection,
            working_set_source=args.working_set,
            note_source=args.note,
        )
        presentation = reentry.controller.presentation
        loaded = reentry.loaded_root

        receipt: dict[str, object] = {
            "capture_input_context_only": str(reentry.loaded_capture.verification.path),
            "selection_input_context_only": str(reentry.loaded_selection.verification.path),
            "working_set_input_context_only": str(
                loaded.working_set.verification.path
            ),
            "note_input_context_only": str(loaded.verification.path),
            "working_set_format": presentation.working_set_format,
            "working_set_record_sha256": presentation.working_set_record_sha256,
            "note_format": presentation.note_format,
            "note_record_sha256": presentation.note_record_sha256,
            "initial_session_mode": presentation.presentation_mode,
            "member_count": len(presentation.members),
            "content_included": bool(args.include_content),
            "receipt_role": (
                "read_only_reentry_inspection_not_evidence_or_session_head_authority"
            ),
        }

        if args.include_content:
            # All content comes from the previously verified immutable 51C
            # presentation, never from untrusted raw file fields or browser state.
            # JSON encoding prevents raw terminal control sequences in source text
            # from being interpreted as terminal commands.
            receipt["human_rationale"] = {
                "role": "human_authored_rationale_not_source_evidence",
                "text": presentation.rationale_text,
            }
            receipt["source_members"] = [
                {
                    "member_position": member.member_position,
                    "member_kind": member.member_kind,
                    "human_note_text": member.human_note_text,
                    "excerpts": [
                        {
                            "role": "bounded_observed_source_not_verified_truth",
                            "excerpt_role": excerpt.excerpt_role,
                            "excerpt_kind": excerpt.excerpt_kind,
                            "text": excerpt.text,
                            "url_observed": excerpt.url,
                            "paragraph_ordinal": excerpt.paragraph_ordinal,
                            "start_offset": excerpt.start_offset,
                            "end_offset": excerpt.end_offset,
                            "offset_unit": excerpt.offset_unit,
                            "source_bundle_sha256": excerpt.source_bundle_sha256,
                            "paragraph_text_truncated": excerpt.paragraph_text_truncated,
                        }
                        for excerpt in member.excerpts
                    ],
                }
                for member in presentation.members
            ]

        print(
            json.dumps(
                receipt,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
        )
    except (OSError, TypeError, ValueError, RuntimeError) as exc:
        parser.error(f"research-reopen failed: {exc}")
    return 0
