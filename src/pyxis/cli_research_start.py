from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from pyxis.app import (
    create_chromium_research_working_set,
    load_chromium_page_research_capture,
    load_chromium_research_paragraph_text_selection,
)
from pyxis.app.chromium_research_initial_session_controller import (
    ChromiumResearchInitialSessionController,
)
from pyxis.app.chromium_research_working_set_note import (
    create_chromium_research_working_set_note,
)
from pyxis.app.chromium_research_working_set_note_load import (
    load_chromium_research_working_set_note,
)
from pyxis.app.chromium_research_working_set_note_persistence import (
    persist_chromium_research_working_set_note_v2,
)
from pyxis.app.chromium_research_working_set_persistence import (
    persist_chromium_research_working_set_v2,
)


def add_research_start_parser(subparsers: Any) -> None:
    """Register the narrow initial-root creation command on the main CLI parser."""

    parser = subparsers.add_parser(
        "research-start",
        help=(
            "Create one initial governed research-session root from one explicit "
            "saved bare selection and one human-authored rationale."
        ),
    )
    parser.add_argument(
        "--capture",
        required=True,
        type=Path,
        help=(
            "Explicit durable research capture used only to freshly relink the saved "
            "selection."
        ),
    )
    parser.add_argument(
        "--selection",
        required=True,
        type=Path,
        help="Explicit 49A saved bare exact-range-selection sidecar.",
    )
    parser.add_argument(
        "--rationale",
        required=True,
        help="Exact first human-authored rationale over this one-member working set.",
    )
    parser.add_argument(
        "--working-set-destination",
        required=True,
        type=Path,
        help="Explicit no-overwrite research_working_set.v2 destination.",
    )
    parser.add_argument(
        "--note-destination",
        required=True,
        type=Path,
        help="Explicit no-overwrite research_working_set_note.v2 destination.",
    )


def run_research_start_command(
    parser: argparse.ArgumentParser,
    args: argparse.Namespace,
) -> int:
    """Create one initial v2 root entirely through already-public evidence boundaries."""

    try:
        working_set_destination, note_destination = _preflight_destinations(
            args.working_set_destination,
            args.note_destination,
        )

        capture = load_chromium_page_research_capture(args.capture)
        member = load_chromium_research_paragraph_text_selection(
            capture,
            args.selection,
        )
        working_set = create_chromium_research_working_set((member,))

        # 21A is deliberately created before the first durable write. This lets the
        # existing application boundary reject a non-note without leaving a partial
        # root and avoids duplicating its rationale validation in this CLI adapter.
        note = create_chromium_research_working_set_note(
            working_set,
            note_text=args.rationale,
        )

        persisted_working_set = persist_chromium_research_working_set_v2(
            working_set,
            working_set_destination,
        )
        persisted_note = persist_chromium_research_working_set_note_v2(
            note,
            persisted_working_set.path,
            note_destination,
        )

        loaded = load_chromium_research_working_set_note(
            (member,),
            persisted_working_set.path,
            persisted_note.path,
        )
        controller = ChromiumResearchInitialSessionController(loaded)

        if loaded.working_set.verification.path != persisted_working_set.path:
            raise ValueError(
                "Fresh initial-root working-set path does not match persistence."
            )
        if loaded.verification.path != persisted_note.path:
            raise ValueError(
                "Fresh initial-root note path does not match persistence."
            )
        if loaded.note.working_set.items != (member,):
            raise ValueError(
                "Fresh initial-root working set does not retain the exact one-member basis."
            )

        presentation = controller.presentation
        receipt = {
            "capture_input_context_only": str(capture.verification.path),
            "initial_session_mode": presentation.presentation_mode,
            "note_format": loaded.verification.note_format,
            "note_output_path": str(loaded.verification.path),
            "note_record_sha256": loaded.verification.note_record_sha256,
            "receipt_role": "operation_receipt_not_evidence_or_session_head_authority",
            "selection_input_context_only": str(member.verification.path),
            "working_set_format": loaded.working_set.verification.working_set_format,
            "working_set_output_path": str(loaded.working_set.verification.path),
            "working_set_record_sha256": (
                loaded.working_set.verification.working_set_record_sha256
            ),
        }
        print(
            json.dumps(
                receipt,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
        )
    except (OSError, TypeError, ValueError, RuntimeError) as exc:
        parser.error(f"research-start failed: {exc}")
    return 0


def _preflight_destinations(
    working_set_destination: Path,
    note_destination: Path,
) -> tuple[Path, Path]:
    """Reject predictable output conflicts before the first durable mutation."""

    if not isinstance(working_set_destination, Path):
        raise TypeError("working_set_destination must be pathlib.Path.")
    if not isinstance(note_destination, Path):
        raise TypeError("note_destination must be pathlib.Path.")

    working_set_path = working_set_destination.expanduser().resolve()
    note_path = note_destination.expanduser().resolve()
    if working_set_path == note_path:
        raise ValueError(
            "working-set and note destinations must resolve to distinct paths."
        )

    for label, path in (
        ("Research working-set", working_set_path),
        ("Research working-set-note", note_path),
    ):
        if not path.parent.is_dir():
            raise FileNotFoundError(
                f"{label} parent directory does not exist: {path.parent}"
            )

    for label, path in (
        ("Research working-set", working_set_path),
        ("Research working-set-note", note_path),
    ):
        if path.exists():
            raise FileExistsError(f"{label} destination already exists: {path}")

    return working_set_path, note_path
