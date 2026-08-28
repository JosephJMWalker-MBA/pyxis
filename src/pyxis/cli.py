from __future__ import annotations

import argparse
from collections.abc import Sequence
import json
from pathlib import Path

from pyxis.app import build_and_run_workspace
from pyxis.app.chromium_research_root_backed_session_authority_inspection import (
    inspect_chromium_research_root_backed_session_continuation_launch,
    inspect_chromium_research_root_backed_session_launch,
)
from pyxis.app.chromium_research_root_backed_session_authority_inspection_report import (
    serialize_chromium_research_root_backed_session_authority_inspection,
)
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
from pyxis.app.chromium_research_root_backed_session_shell_lineage import (
    ChromiumResearchRootBackedSessionContinuationShellLineage,
    ChromiumResearchRootBackedSessionShellLineage,
    prove_chromium_research_root_backed_session_continuation_shell_lineage,
    prove_chromium_research_root_backed_session_shell_lineage,
)
from pyxis.app.chromium_research_second_basis_epoch_authority_inspection import (
    inspect_chromium_research_second_basis_epoch_continuation_launch,
    inspect_chromium_research_second_basis_epoch_launch,
    serialize_chromium_research_second_basis_epoch_authority_inspection,
)
from pyxis.app.chromium_research_second_basis_epoch_continuation_reentry_plan_document import (
    ChromiumResearchSecondBasisEpochContinuationReentryResult,
    load_chromium_research_second_basis_epoch_continuation_reentry_plan_document,
    reenter_chromium_research_second_basis_epoch_continuation,
)
from pyxis.app.chromium_research_second_basis_epoch_reentry import (
    reenter_chromium_research_second_basis_epoch,
)
from pyxis.app.chromium_research_second_basis_epoch_reentry_plan_document import (
    load_chromium_research_second_basis_epoch_reentry_plan_document,
)
from pyxis.app.chromium_research_second_basis_epoch_shell_lineage import (
    ChromiumResearchSecondBasisEpochContinuationShellLineage,
    ChromiumResearchSecondBasisEpochShellLineage,
    prove_chromium_research_second_basis_epoch_continuation_shell_lineage,
    prove_chromium_research_second_basis_epoch_shell_lineage,
)
from pyxis.app.chromium_research_session_controller import ChromiumResearchSessionController
from pyxis.app.chromium_research_session_reentry import (
    ChromiumResearchSessionReentryResult,
    reenter_chromium_research_session,
)
from pyxis.app.chromium_research_session_reentry_plan_document import (
    load_chromium_research_session_reentry_plan_document,
)
from pyxis.app.chromium_research_third_basis_epoch_authority_inspection import (
    inspect_chromium_research_third_basis_epoch_continuation_launch,
    inspect_chromium_research_third_basis_epoch_launch,
)
from pyxis.app.chromium_research_third_basis_epoch_authority_inspection_report import (
    serialize_chromium_research_third_basis_epoch_authority_inspection,
)
from pyxis.app.chromium_research_third_basis_epoch_continuation_reentry_plan_document import (
    ChromiumResearchThirdBasisEpochContinuationReentryResult,
    load_chromium_research_third_basis_epoch_continuation_reentry_plan_document,
    reenter_chromium_research_third_basis_epoch_continuation,
)
from pyxis.app.chromium_research_third_basis_epoch_reentry import (
    reenter_chromium_research_third_basis_epoch,
)
from pyxis.app.chromium_research_third_basis_epoch_reentry_plan_document import (
    load_chromium_research_third_basis_epoch_reentry_plan_document,
)
from pyxis.app.chromium_research_third_basis_epoch_shell_lineage import (
    ChromiumResearchThirdBasisEpochContinuationShellLineage,
    ChromiumResearchThirdBasisEpochShellLineage,
    prove_chromium_research_third_basis_epoch_continuation_shell_lineage,
    prove_chromium_research_third_basis_epoch_shell_lineage,
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
    entry.add_argument(
        "--third-basis-epoch-overlay",
        type=Path,
        help=(
            "Explicit 40B third-basis-epoch locator overlay. The overlay is "
            "operational configuration, not evidence or a head pointer."
        ),
    )
    entry.add_argument(
        "--third-basis-epoch-continuation-overlay",
        type=Path,
        help=(
            "Explicit 40C/40D post-third-root continuation overlay. The overlay is "
            "operational configuration, not evidence or a head pointer."
        ),
    )

    research_inspect_parser = subparsers.add_parser(
        "research-inspect",
        help=(
            "Freshly prove one explicit persisted root-backed, second-, or third-epoch "
            "entry and emit a deterministic read-only authority inspection report."
        ),
    )
    inspect_entry = research_inspect_parser.add_mutually_exclusive_group(required=True)
    inspect_entry.add_argument(
        "--root-backed-overlay",
        type=Path,
        help=(
            "Explicit 35C root-backed locator overlay. The emitted path is launch "
            "location context only, never current/latest/head authority."
        ),
    )
    inspect_entry.add_argument(
        "--root-backed-continuation-overlay",
        type=Path,
        help=(
            "Explicit 35D/35E root-backed continuation overlay. The emitted path is "
            "launch location context only, never current/latest/head authority."
        ),
    )
    inspect_entry.add_argument(
        "--second-basis-epoch-overlay",
        type=Path,
        help=(
            "Explicit 37B second-basis-epoch locator overlay. The emitted path is "
            "launch location context only, never current/latest/head authority."
        ),
    )
    inspect_entry.add_argument(
        "--second-basis-epoch-continuation-overlay",
        type=Path,
        help=(
            "Explicit 37C/37D continuation overlay. The emitted path is launch "
            "location context only, never current/latest/head authority."
        ),
    )
    inspect_entry.add_argument(
        "--third-basis-epoch-overlay",
        type=Path,
        help=(
            "Explicit 40B third-basis-epoch locator overlay. The emitted path is "
            "launch location context only, never current/latest/head authority."
        ),
    )
    inspect_entry.add_argument(
        "--third-basis-epoch-continuation-overlay",
        type=Path,
        help=(
            "Explicit 40C/40D continuation overlay. The emitted path is launch "
            "location context only, never current/latest/head authority."
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
    """Lazily import the inspectable path-proofed 35C Textual shell factory."""

    try:
        from pyxis.ui.root_backed_authority_inspection_shell import (
            create_inspectable_root_backed_research_session_shell,
        )
    except ModuleNotFoundError as exc:
        if exc.name == "textual":
            raise RuntimeError(
                "research-shell requires the optional Pyxis UI dependency; "
                "install with: pip install 'pyxis[ui]'"
            ) from exc
        raise
    return create_inspectable_root_backed_research_session_shell


def _load_root_backed_continuation_research_shell_factory():
    """Lazily import the inspectable path-proofed 35D/35E Textual shell factory."""

    try:
        from pyxis.ui.root_backed_authority_inspection_shell import (
            create_inspectable_root_backed_continuation_research_session_shell,
        )
    except ModuleNotFoundError as exc:
        if exc.name == "textual":
            raise RuntimeError(
                "research-shell requires the optional Pyxis UI dependency; "
                "install with: pip install 'pyxis[ui]'"
            ) from exc
        raise
    return create_inspectable_root_backed_continuation_research_session_shell


def _load_root_backed_continuation_handoff_research_shell_factory():
    """Lazily import the inspectable raw-typed in-process 36D cumulative shell factory."""

    try:
        from pyxis.ui.root_backed_authority_inspection_shell import (
            create_inspectable_root_backed_continuation_handoff_research_session_shell,
        )
    except ModuleNotFoundError as exc:
        if exc.name == "textual":
            raise RuntimeError(
                "research-shell requires the optional Pyxis UI dependency; "
                "install with: pip install 'pyxis[ui]'"
            ) from exc
        raise
    return create_inspectable_root_backed_continuation_handoff_research_session_shell


def _load_second_basis_epoch_research_shell_factory():
    """Lazily import the inspectable explicit-handoff 37B Textual shell factory."""

    try:
        from pyxis.ui.second_basis_epoch_authority_inspection_shell import (
            create_inspectable_second_basis_epoch_cumulative_handoff_research_session_shell,
        )
    except ModuleNotFoundError as exc:
        if exc.name == "textual":
            raise RuntimeError(
                "research-shell requires the optional Pyxis UI dependency; "
                "install with: pip install 'pyxis[ui]'"
            ) from exc
        raise
    return create_inspectable_second_basis_epoch_cumulative_handoff_research_session_shell


def _load_second_basis_epoch_continuation_research_shell_factory():
    """Lazily import the inspectable path-proofed 37C/37D Textual shell factory."""

    try:
        from pyxis.ui.second_basis_epoch_authority_inspection_shell import (
            create_inspectable_second_basis_epoch_continuation_research_session_shell,
        )
    except ModuleNotFoundError as exc:
        if exc.name == "textual":
            raise RuntimeError(
                "research-shell requires the optional Pyxis UI dependency; "
                "install with: pip install 'pyxis[ui]'"
            ) from exc
        raise
    return create_inspectable_second_basis_epoch_continuation_research_session_shell


def _load_second_basis_epoch_continuation_handoff_research_shell_factory():
    """Lazily import the inspectable raw-typed in-process 38F cumulative shell factory."""

    try:
        from pyxis.ui.second_basis_epoch_authority_inspection_shell import (
            create_inspectable_second_basis_epoch_continuation_handoff_research_session_shell,
        )
    except ModuleNotFoundError as exc:
        if exc.name == "textual":
            raise RuntimeError(
                "research-shell requires the optional Pyxis UI dependency; "
                "install with: pip install 'pyxis[ui]'"
            ) from exc
        raise
    return create_inspectable_second_basis_epoch_continuation_handoff_research_session_shell


def _load_third_basis_epoch_research_shell_factory():
    """Lazily import the inspectable explicit-handoff 40B Textual shell factory."""

    try:
        from pyxis.ui.third_basis_epoch_authority_inspection_shell import (
            create_inspectable_third_basis_epoch_cumulative_handoff_research_session_shell,
        )
    except ModuleNotFoundError as exc:
        if exc.name == "textual":
            raise RuntimeError(
                "research-shell requires the optional Pyxis UI dependency; "
                "install with: pip install 'pyxis[ui]'"
            ) from exc
        raise
    return create_inspectable_third_basis_epoch_cumulative_handoff_research_session_shell


def _load_third_basis_epoch_continuation_research_shell_factory():
    """Lazily import the inspectable path-proofed 40C/40D Textual shell factory."""

    try:
        from pyxis.ui.third_basis_epoch_authority_inspection_shell import (
            create_inspectable_third_basis_epoch_continuation_research_session_shell,
        )
    except ModuleNotFoundError as exc:
        if exc.name == "textual":
            raise RuntimeError(
                "research-shell requires the optional Pyxis UI dependency; "
                "install with: pip install 'pyxis[ui]'"
            ) from exc
        raise
    return create_inspectable_third_basis_epoch_continuation_research_session_shell


def _load_third_basis_epoch_continuation_handoff_research_shell_factory():
    """Lazily import the inspectable raw-typed in-process 41E cumulative shell factory."""

    try:
        from pyxis.ui.third_basis_epoch_authority_inspection_shell import (
            create_inspectable_third_basis_epoch_continuation_handoff_research_session_shell,
        )
    except ModuleNotFoundError as exc:
        if exc.name == "textual":
            raise RuntimeError(
                "research-shell requires the optional Pyxis UI dependency; "
                "install with: pip install 'pyxis[ui]'"
            ) from exc
        raise
    return create_inspectable_third_basis_epoch_continuation_handoff_research_session_shell


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
    lineage: ChromiumResearchRootBackedSessionShellLineage,
) -> ChromiumResearchRootBackedSessionContinuationReentryResult | None:
    """Run one path-proofed persisted 35C launch and return only explicit 36D handoff."""

    create_shell = _load_root_backed_research_shell_factory()
    if not isinstance(lineage, ChromiumResearchRootBackedSessionShellLineage):
        raise TypeError(
            "lineage must be ChromiumResearchRootBackedSessionShellLineage."
        )
    handoff = create_shell(lineage).run()
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
    lineage: ChromiumResearchRootBackedSessionContinuationShellLineage,
) -> None:
    """Run one path-proofed persisted 35D/35E launch lineage."""

    create_shell = _load_root_backed_continuation_research_shell_factory()
    if not isinstance(lineage, ChromiumResearchRootBackedSessionContinuationShellLineage):
        raise TypeError(
            "lineage must be ChromiumResearchRootBackedSessionContinuationShellLineage."
        )
    create_shell(lineage).run()


def _run_root_backed_continuation_handoff_research_session_shell(
    reentry: ChromiumResearchRootBackedSessionContinuationReentryResult,
) -> None:
    """Run cumulative mode directly from one exact in-process 36D typed handoff."""

    create_shell = _load_root_backed_continuation_handoff_research_shell_factory()
    if not isinstance(
        reentry,
        ChromiumResearchRootBackedSessionContinuationReentryResult,
    ):
        raise TypeError(
            "reentry must be ChromiumResearchRootBackedSessionContinuationReentryResult."
        )
    create_shell(reentry).run()


def _run_second_basis_epoch_research_session_shell(
    lineage: ChromiumResearchSecondBasisEpochShellLineage,
) -> ChromiumResearchSecondBasisEpochContinuationReentryResult | None:
    """Run proven 37B first-checkpoint mode and return only an explicit 38F handoff."""

    create_shell = _load_second_basis_epoch_research_shell_factory()
    if not isinstance(lineage, ChromiumResearchSecondBasisEpochShellLineage):
        raise TypeError(
            "lineage must be ChromiumResearchSecondBasisEpochShellLineage."
        )
    handoff = create_shell(lineage).run()
    if handoff is None:
        return None
    if not isinstance(
        handoff,
        ChromiumResearchSecondBasisEpochContinuationReentryResult,
    ):
        raise TypeError(
            "second-basis-epoch research shell returned an invalid cumulative handoff result."
        )
    return handoff


def _run_second_basis_epoch_continuation_research_session_shell(
    lineage: ChromiumResearchSecondBasisEpochContinuationShellLineage,
) -> None:
    """Run one path-proofed persisted 37C/37D launch lineage."""

    create_shell = _load_second_basis_epoch_continuation_research_shell_factory()
    if not isinstance(
        lineage,
        ChromiumResearchSecondBasisEpochContinuationShellLineage,
    ):
        raise TypeError(
            "lineage must be ChromiumResearchSecondBasisEpochContinuationShellLineage."
        )
    create_shell(lineage).run()


def _run_second_basis_epoch_continuation_handoff_research_session_shell(
    reentry: ChromiumResearchSecondBasisEpochContinuationReentryResult,
) -> None:
    """Run cumulative mode directly from one exact in-process 38F typed handoff."""

    create_shell = _load_second_basis_epoch_continuation_handoff_research_shell_factory()
    if not isinstance(
        reentry,
        ChromiumResearchSecondBasisEpochContinuationReentryResult,
    ):
        raise TypeError(
            "reentry must be ChromiumResearchSecondBasisEpochContinuationReentryResult."
        )
    create_shell(reentry).run()


def _run_third_basis_epoch_research_session_shell(
    lineage: ChromiumResearchThirdBasisEpochShellLineage,
) -> ChromiumResearchThirdBasisEpochContinuationReentryResult | None:
    """Run proven 40B first-checkpoint mode and return only an explicit 41E handoff."""

    create_shell = _load_third_basis_epoch_research_shell_factory()
    if not isinstance(lineage, ChromiumResearchThirdBasisEpochShellLineage):
        raise TypeError(
            "lineage must be ChromiumResearchThirdBasisEpochShellLineage."
        )
    handoff = create_shell(lineage).run()
    if handoff is None:
        return None
    if not isinstance(
        handoff,
        ChromiumResearchThirdBasisEpochContinuationReentryResult,
    ):
        raise TypeError(
            "third-basis-epoch research shell returned an invalid cumulative handoff result."
        )
    return handoff


def _run_third_basis_epoch_continuation_research_session_shell(
    lineage: ChromiumResearchThirdBasisEpochContinuationShellLineage,
) -> None:
    """Run one path-proofed persisted 40C/40D launch lineage."""

    create_shell = _load_third_basis_epoch_continuation_research_shell_factory()
    if not isinstance(
        lineage,
        ChromiumResearchThirdBasisEpochContinuationShellLineage,
    ):
        raise TypeError(
            "lineage must be ChromiumResearchThirdBasisEpochContinuationShellLineage."
        )
    create_shell(lineage).run()


def _run_third_basis_epoch_continuation_handoff_research_session_shell(
    reentry: ChromiumResearchThirdBasisEpochContinuationReentryResult,
) -> None:
    """Run cumulative mode directly from one exact in-process 41E typed handoff."""

    create_shell = _load_third_basis_epoch_continuation_handoff_research_shell_factory()
    if not isinstance(
        reentry,
        ChromiumResearchThirdBasisEpochContinuationReentryResult,
    ):
        raise TypeError(
            "reentry must be ChromiumResearchThirdBasisEpochContinuationReentryResult."
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
            lineage = prove_chromium_research_root_backed_session_shell_lineage(
                result,
                overlay_source=args.root_backed_overlay,
            )
            handoff = _run_root_backed_research_session_shell(lineage)
            if handoff is not None:
                _run_root_backed_continuation_handoff_research_session_shell(handoff)
        elif args.root_backed_continuation_overlay is not None:
            plan = (
                load_chromium_research_root_backed_session_continuation_reentry_plan_document(
                    args.root_backed_continuation_overlay
                )
            )
            result = reenter_chromium_research_root_backed_session_continuation(plan)
            lineage = prove_chromium_research_root_backed_session_continuation_shell_lineage(
                result,
                overlay_source=args.root_backed_continuation_overlay,
            )
            _run_root_backed_continuation_research_session_shell(lineage)
        elif args.second_basis_epoch_overlay is not None:
            plan = load_chromium_research_second_basis_epoch_reentry_plan_document(
                args.second_basis_epoch_overlay
            )
            result = reenter_chromium_research_second_basis_epoch(plan)
            lineage = prove_chromium_research_second_basis_epoch_shell_lineage(
                result,
                overlay_source=args.second_basis_epoch_overlay,
            )
            handoff = _run_second_basis_epoch_research_session_shell(lineage)
            if handoff is not None:
                _run_second_basis_epoch_continuation_handoff_research_session_shell(
                    handoff
                )
        elif args.second_basis_epoch_continuation_overlay is not None:
            plan = (
                load_chromium_research_second_basis_epoch_continuation_reentry_plan_document(
                    args.second_basis_epoch_continuation_overlay
                )
            )
            result = reenter_chromium_research_second_basis_epoch_continuation(plan)
            lineage = (
                prove_chromium_research_second_basis_epoch_continuation_shell_lineage(
                    result,
                    overlay_source=args.second_basis_epoch_continuation_overlay,
                )
            )
            _run_second_basis_epoch_continuation_research_session_shell(lineage)
        elif args.third_basis_epoch_overlay is not None:
            plan = load_chromium_research_third_basis_epoch_reentry_plan_document(
                args.third_basis_epoch_overlay
            )
            result = reenter_chromium_research_third_basis_epoch(plan)
            lineage = prove_chromium_research_third_basis_epoch_shell_lineage(
                result,
                overlay_source=args.third_basis_epoch_overlay,
            )
            handoff = _run_third_basis_epoch_research_session_shell(lineage)
            if handoff is not None:
                _run_third_basis_epoch_continuation_handoff_research_session_shell(
                    handoff
                )
        elif args.third_basis_epoch_continuation_overlay is not None:
            plan = (
                load_chromium_research_third_basis_epoch_continuation_reentry_plan_document(
                    args.third_basis_epoch_continuation_overlay
                )
            )
            result = reenter_chromium_research_third_basis_epoch_continuation(plan)
            lineage = (
                prove_chromium_research_third_basis_epoch_continuation_shell_lineage(
                    result,
                    overlay_source=args.third_basis_epoch_continuation_overlay,
                )
            )
            _run_third_basis_epoch_continuation_research_session_shell(lineage)
        else:
            raise ValueError("research-shell requires one explicit entry configuration.")
    except (OSError, TypeError, ValueError, RuntimeError) as exc:
        parser.error(f"research-shell failed: {exc}")
    return 0


def _run_research_inspect_command(
    parser: argparse.ArgumentParser,
    args: argparse.Namespace,
) -> int:
    """Freshly prove one explicit persisted launch and emit deterministic JSON."""

    try:
        if args.root_backed_overlay is not None:
            plan = load_chromium_research_root_backed_session_reentry_plan_document(
                args.root_backed_overlay
            )
            result = reenter_chromium_research_root_backed_session(plan)
            lineage = prove_chromium_research_root_backed_session_shell_lineage(
                result,
                overlay_source=args.root_backed_overlay,
            )
            inspection = inspect_chromium_research_root_backed_session_launch(lineage)
            report = serialize_chromium_research_root_backed_session_authority_inspection(
                inspection
            )
        elif args.root_backed_continuation_overlay is not None:
            plan = (
                load_chromium_research_root_backed_session_continuation_reentry_plan_document(
                    args.root_backed_continuation_overlay
                )
            )
            result = reenter_chromium_research_root_backed_session_continuation(plan)
            lineage = prove_chromium_research_root_backed_session_continuation_shell_lineage(
                result,
                overlay_source=args.root_backed_continuation_overlay,
            )
            inspection = inspect_chromium_research_root_backed_session_continuation_launch(
                lineage
            )
            report = serialize_chromium_research_root_backed_session_authority_inspection(
                inspection
            )
        elif args.second_basis_epoch_overlay is not None:
            plan = load_chromium_research_second_basis_epoch_reentry_plan_document(
                args.second_basis_epoch_overlay
            )
            result = reenter_chromium_research_second_basis_epoch(plan)
            lineage = prove_chromium_research_second_basis_epoch_shell_lineage(
                result,
                overlay_source=args.second_basis_epoch_overlay,
            )
            inspection = inspect_chromium_research_second_basis_epoch_launch(lineage)
            report = serialize_chromium_research_second_basis_epoch_authority_inspection(
                inspection
            )
        elif args.second_basis_epoch_continuation_overlay is not None:
            plan = (
                load_chromium_research_second_basis_epoch_continuation_reentry_plan_document(
                    args.second_basis_epoch_continuation_overlay
                )
            )
            result = reenter_chromium_research_second_basis_epoch_continuation(plan)
            lineage = (
                prove_chromium_research_second_basis_epoch_continuation_shell_lineage(
                    result,
                    overlay_source=args.second_basis_epoch_continuation_overlay,
                )
            )
            inspection = (
                inspect_chromium_research_second_basis_epoch_continuation_launch(
                    lineage
                )
            )
            report = serialize_chromium_research_second_basis_epoch_authority_inspection(
                inspection
            )
        elif args.third_basis_epoch_overlay is not None:
            plan = load_chromium_research_third_basis_epoch_reentry_plan_document(
                args.third_basis_epoch_overlay
            )
            result = reenter_chromium_research_third_basis_epoch(plan)
            lineage = prove_chromium_research_third_basis_epoch_shell_lineage(
                result,
                overlay_source=args.third_basis_epoch_overlay,
            )
            inspection = inspect_chromium_research_third_basis_epoch_launch(lineage)
            report = serialize_chromium_research_third_basis_epoch_authority_inspection(
                inspection
            )
        elif args.third_basis_epoch_continuation_overlay is not None:
            plan = (
                load_chromium_research_third_basis_epoch_continuation_reentry_plan_document(
                    args.third_basis_epoch_continuation_overlay
                )
            )
            result = reenter_chromium_research_third_basis_epoch_continuation(plan)
            lineage = (
                prove_chromium_research_third_basis_epoch_continuation_shell_lineage(
                    result,
                    overlay_source=args.third_basis_epoch_continuation_overlay,
                )
            )
            inspection = inspect_chromium_research_third_basis_epoch_continuation_launch(
                lineage
            )
            report = serialize_chromium_research_third_basis_epoch_authority_inspection(
                inspection
            )
        else:
            raise ValueError(
                "research-inspect requires one explicit persisted entry configuration."
            )
        print(report, end="")
    except (OSError, TypeError, ValueError, RuntimeError) as exc:
        parser.error(f"research-inspect failed: {exc}")
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
    if args.command == "research-inspect":
        return _run_research_inspect_command(parser, args)

    parser.error(f"unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
