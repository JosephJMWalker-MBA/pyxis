from __future__ import annotations

import argparse
import json
from pathlib import Path
from collections.abc import Sequence

from pyxis.app import build_and_run_workspace
from pyxis.authoring import create_workspace_spec


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pyxis",
        description="Transparent architecture-to-code compiler and Workspace runtime.",
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
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the thin command-line interface over application orchestration."""

    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        return 0

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


if __name__ == "__main__":
    raise SystemExit(main())
