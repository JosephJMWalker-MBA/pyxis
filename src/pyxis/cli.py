from __future__ import annotations

import argparse
from collections.abc import Sequence
import json
from pathlib import Path

from pyxis.app import build_and_run_workspace
from pyxis.app.chromium_research_session_reentry import (
    ChromiumResearchSessionReentryResult,
    reenter_chromium_research_session,
)
from pyxis.app.chromium_research_session_reentry_plan_document import (
    load_chromium_research_session_reentry_plan_document,
)
from pyxis.authoring import create_workspace_spec


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pyxis",
        description=(
            "Transparent architecture-to-code compiler, Workspace runtime, and "
            "explicit governed research-session launcher."
        ),
    )
    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser(
        "run",
        help="Create, build, and run one Workspace through the permanent Pyxis path.",
    )
    run_parser.add_argument("--name", required=True, help="Workspace name.")
    run_parser.add_argument(
        "--description",
        required=True,
        help="Workspace description.",
    )
    run_parser.add_argument(
        "--destination",
        required=True,
        type=Path,
        help="Directory where Workspace state and generated output are written.",
    )
    run_parser.add_argument(
        "--text",
        required=True,
        help="Sample text passed to the generated Workspace runtime.",
    )

    research_shell_parser = subparsers.add_parser(
        "research-shell",
        help=(
            "Freshly reopen one explicitly located durable research session and "
            "launch the standalone governed Textual shell."
        ),
    )
    research_shell_parser.add_argument(
        "--plan",
        required=True,
        type=Path,
        help=(
            "Locator-only JSON plan. Relative artifact paths are interpreted "
            "relative to the plan file; the plan is not evidence or a head pointer."
        ),
    )
    return parser


def _run_workspace_command(args: argparse.Namespace) -> int:
    spec = create_workspace_spec(args.name, args.description)
    result = build_and_run_workspace(spec, args.destination, args.text)
    print(
        json.dumps(
            result.runtime_result,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


def _run_research_session_shell(reentry: ChromiumResearchSessionReentryResult) -> None:
    """Lazily import the optional UI and run one exact re-entry-aware research shell."""

    if not isinstance(reentry, ChromiumResearchSessionReentryResult):
        raise TypeError("reentry must be ChromiumResearchSessionReentryResult.")

    try:
        from pyxis.ui.research_session_shell import create_research_session_shell
    except ModuleNotFoundError as exc:
        if exc.name == "textual":
            raise RuntimeError(
                "research-shell requires the optional Pyxis UI dependency; "
                "install with: pip install 'pyxis[ui]'"
            ) from exc
        raise

    create_research_session_shell(
        reentry.controller,
        reentry=reentry,
    ).run()


def _run_research_shell_command(
    parser: argparse.ArgumentParser,
    args: argparse.Namespace,
) -> int:
    try:
        plan = load_chromium_research_session_reentry_plan_document(args.plan)
        result = reenter_chromium_research_session(plan)
        _run_research_session_shell(result)
    except (OSError, TypeError, ValueError, RuntimeError) as exc:
        parser.error(f"research-shell failed: {exc}")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    """Run the thin command-line interface over established application boundaries."""

    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 0
    if args.command == "run":
        return _run_workspace_command(args)
    if args.command == "research-shell":
        return _run_research_shell_command(parser, args)

    parser.error(f"unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
