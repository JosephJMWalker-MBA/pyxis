from __future__ import annotations

import argparse
from collections.abc import Sequence
import json
from pathlib import Path

from pyxis.app import build_and_run_workspace
from pyxis.app.chromium_research_root_backed_session_continuation_reentry_plan_document import (
    ChromiumResearchRootBackedSessionContinuationReentryResult,
    load_chromium_research_root_backed_session_continuation_reentry_plan_document,
    reenter_chromium_research_root_backed_session_continuation,
)
from pyxis.app.chromium_research_root_backed_session_reentry import (
    ChromiumResearchRootBackedSessionReentryResult,
    reenter_chromium_research_root_backed_session,
)
from pyxis.app.chromium_research_root_backed_session_reentry_plan_document import (
    load_chromium_research_root_backed_session_reentry_plan_document,
)
from pyxis.app.chromium_research_second_basis_epoch_continuation_reentry_plan_document import (
    load_chromium_research_second_basis_epoch_continuation_reentry_plan_document,
    reenter_chromium_research_second_basis_epoch_continuation,
)
from pyxis.app.chromium_research_second_basis_epoch_reentry import (
    reenter_chromium_research_second_basis_epoch,
)
from pyxis.app.chromium_research_second_basis_epoch_reentry_plan_document import (
    load_chromium_research_second_basis_epoch_reentry_plan_document,
)
from pyxis.app.chromium_research_session_controller import ChromiumResearchSessionController
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
    entry = research_shell_parser.add_mutually_exclusive_group(required=True)
    entry.add_argument(
        "--plan",
        type=Path,
        help=(
            "Ordinary locator-only JSON plan. Relative artifact paths are interpreted "
            "relative to the plan file; the plan is not evidence or a head pointer."
        ),
    )
    entry.add_argument(
        "--root-backed-overlay",
        type=Path,
        help=(
            "Explicit 35C root-backed locator overlay. The overlay is operational "
            "configuration, not evidence or a head pointer."
        ),
    )
    entry.add_argument(
        "--root-backed-continuation-overlay",
        type=Path,
        help=(
            "Explicit 35D/35E post-root continuation overlay. The overlay is "
            "operational configuration, not evidence or a head pointer."
        ),
    )
    entry.add_argument(
        "--second-basis-epoch-overlay",
        type=Path,
        help=(
            "Explicit 37B second-basis-epoch locator overlay. The overlay is "
            "operational configuration, not evidence or a head pointer."
        ),
    )
    entry.add_argument(
        "--second-basis-epoch-continuation-overlay",
        type=Path,
        help=(
            "Explicit 37C/37D post-second-root continuation overlay. The overlay is "
            "operational configuration, not evidence or a head pointer."
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


def _load_research_shell_factory():
    """Lazily import the optional ordinary/controller-only Textual shell factory."""

    try:
        from pyxis.ui.research_session_shell import create_research_session_shell
    except ModuleNotFoundError as exc:
        if exc.name == "textual":
            raise RuntimeError(
                "research-shell requires the optional Pyxis UI dependency; "
                "install with: pip install 'pyxis[ui]'"
            ) from exc
        raise
    return create_research_session_shell


def _load_root_backed_research_shell_factory():
    """Lazily import the optional first-checkpoint-aware 35B Textual shell factory."""

    try:
        from pyxis.ui.root_backed_research_session_shell import (
            create_root_backed_research_session_shell,
        )
    except ModuleNotFoundError as exc:
        if exc.name == "textual":
            raise RuntimeError(
                "research-shell requires the optional Pyxis UI dependency; "
                "install with: pip install 'pyxis[ui]'"
            ) from exc
        raise
    return create_root_backed_research_session_shell


def _load_root_backed_continuation_research_shell_factory():
    """Lazily import the optional repeatable 35D/35E Textual shell factory."""

    try:
        from pyxis.ui.root_backed_continuation_research_session_shell import (
            create_root_backed_continuation_research_session_shell,
        )
    except ModuleNotFoundError as exc:
        if exc.name == "textual":
            raise RuntimeError(
                "research-shell requires the optional Pyxis UI dependency; "
                "install with: pip install 'pyxis[ui]'"
            ) from exc
        raise
    return create_root_backed_continuation_research_session_shell


def _run_research_session_shell(reentry: ChromiumResearchSessionReentryResult) -> None:
    """Run one exact ordinary re-entry-aware research shell."""

    create_research_session_shell = _load_research_shell_factory()
    if not isinstance(reentry, ChromiumResearchSessionReentryResult):
        raise TypeError("reentry must be ChromiumResearchSessionReentryResult.")

    create_research_session_shell(
        reentry.controller,
        reentry=reentry,
    ).run()


def _run_root_backed_research_session_shell(
    reentry: ChromiumResearchRootBackedSessionReentryResult,
) -> ChromiumResearchRootBackedSessionContinuationReentryResult | None:
    """Run first-checkpoint shell and return only an explicit typed 36D handoff."""

    create_root_backed_research_session_shell = _load_root_backed_research_shell_factory()
    if not isinstance(reentry, ChromiumResearchRootBackedSessionReentryResult):
        raise TypeError(
            "reentry must be ChromiumResearchRootBackedSessionReentryResult."
        )
    handoff = create_root_backed_research_session_shell(reentry).run()
    if handoff is None:
        return None
    if not isinstance(
        handoff,
        ChromiumResearchRootBackedSessionContinuationReentryResult,
    ):
        raise TypeError(
            "root-backed research shell returned an invalid cumulative handoff result."
        )
    return handoff


def _run_root_backed_continuation_research_session_shell(
    reentry: ChromiumResearchRootBackedSessionContinuationReentryResult,
) -> None:
    """Run one exact 35D/35E lineage through the cumulative-checkpoint shell."""

    create_shell = _load_root_backed_continuation_research_shell_factory()
    if not isinstance(
        reentry,
        ChromiumResearchRootBackedSessionContinuationReentryResult,
    ):
        raise TypeError(
            "reentry must be ChromiumResearchRootBackedSessionContinuationReentryResult."
        )
    create_shell(reentry).run()


def _run_controller_only_research_session_shell(
    controller: ChromiumResearchSessionController,
) -> None:
    """Run one governed controller without inventing restart lineage."""

    create_research_session_shell = _load_research_shell_factory()
    if not isinstance(controller, ChromiumResearchSessionController):
        raise TypeError("controller must be ChromiumResearchSessionController.")
    create_research_session_shell(controller).run()


def _run_research_shell_command(
    parser: argparse.ArgumentParser,
    args: argparse.Namespace,
) -> int:
    try:
        if args.plan is not None:
            plan = load_chromium_research_session_reentry_plan_document(args.plan)
            result = reenter_chromium_research_session(plan)
            _run_research_session_shell(result)
        elif args.root_backed_overlay is not None:
            plan = load_chromium_research_root_backed_session_reentry_plan_document(
                args.root_backed_overlay
            )
            result = reenter_chromium_research_root_backed_session(plan)
            handoff = _run_root_backed_research_session_shell(result)
            if handoff is not None:
                _run_root_backed_continuation_research_session_shell(handoff)
        elif args.root_backed_continuation_overlay is not None:
            plan = (
                load_chromium_research_root_backed_session_continuation_reentry_plan_document(
                    args.root_backed_continuation_overlay
                )
            )
            result = reenter_chromium_research_root_backed_session_continuation(plan)
            _run_root_backed_continuation_research_session_shell(result)
        elif args.second_basis_epoch_overlay is not None:
            plan = load_chromium_research_second_basis_epoch_reentry_plan_document(
                args.second_basis_epoch_overlay
            )
            result = reenter_chromium_research_second_basis_epoch(plan)
            _run_controller_only_research_session_shell(result.controller)
        elif args.second_basis_epoch_continuation_overlay is not None:
            plan = (
                load_chromium_research_second_basis_epoch_continuation_reentry_plan_document(
                    args.second_basis_epoch_continuation_overlay
                )
            )
            result = reenter_chromium_research_second_basis_epoch_continuation(plan)
            _run_controller_only_research_session_shell(result.controller)
        else:
            raise ValueError("research-shell requires one explicit entry configuration.")
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
