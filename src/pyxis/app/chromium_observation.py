from __future__ import annotations

from dataclasses import dataclass

from pyxis.browser import (
    ChromiumPageSnapshot,
    ChromiumPageTarget,
    ChromiumReadError,
    list_chromium_page_targets,
    normalize_chromium_endpoint,
    read_chromium_page_snapshot,
)


@dataclass(frozen=True, slots=True)
class ChromiumPageContentEvidence:
    """Bounded exact rendered-text evidence from one observed page."""

    source: str
    text_prefix: str
    text_character_count: int
    text_limit: int
    truncated: bool


@dataclass(frozen=True, slots=True)
class ChromiumPageObservationEvidence:
    """Read-only evidence acquired from one explicit Chromium page target."""

    endpoint: str
    target_id: str
    url: str
    title: str
    content: ChromiumPageContentEvidence


def observe_chromium_page(
    endpoint: str,
    *,
    target_id: str | None = None,
    text_limit: int = 2048,
    timeout: float = 5.0,
) -> ChromiumPageObservationEvidence:
    """Observe one existing Chromium page without taking browser-state ownership.

    Pyxis discovers only page targets exposed by the caller-supplied DevTools
    endpoint. When exactly one page exists it may be selected implicitly. When
    multiple pages exist, the caller must provide an exact target id; Pyxis does
    not infer an active/current tab from ordering or browser heuristics.

    Acquisition is read-only: target discovery plus one fixed page snapshot.
    This operation does not navigate, activate targets, click, submit forms,
    create or close pages, persist evidence, invoke an LLM, or mutate Pyxis
    Workspace state.
    """

    normalized_endpoint = normalize_chromium_endpoint(endpoint)
    targets = list_chromium_page_targets(normalized_endpoint, timeout=timeout)
    target = _select_page_target(targets, target_id=target_id)
    snapshot = read_chromium_page_snapshot(
        target,
        text_limit=text_limit,
        timeout=timeout,
    )
    return _create_observation(
        endpoint=normalized_endpoint,
        target=target,
        snapshot=snapshot,
        text_limit=text_limit,
    )


def _select_page_target(
    targets: tuple[ChromiumPageTarget, ...],
    *,
    target_id: str | None,
) -> ChromiumPageTarget:
    if target_id is not None:
        requested = target_id.strip()
        if not requested:
            raise ValueError("target_id must be non-empty when supplied.")
        matches = tuple(target for target in targets if target.target_id == requested)
        if len(matches) != 1:
            raise ChromiumReadError(
                f"Chromium page target {requested!r} was not found at the supplied endpoint."
            )
        return matches[0]

    if not targets:
        raise ChromiumReadError("No Chromium page targets are available.")
    if len(targets) > 1:
        available = ", ".join(target.target_id for target in targets)
        raise ChromiumReadError(
            "Multiple Chromium page targets are available; supply target_id explicitly. "
            f"Available target ids: {available}"
        )
    return targets[0]


def _create_observation(
    *,
    endpoint: str,
    target: ChromiumPageTarget,
    snapshot: ChromiumPageSnapshot,
    text_limit: int,
) -> ChromiumPageObservationEvidence:
    if text_limit < 0:
        raise ValueError("text_limit must be >= 0.")
    if snapshot.text_character_count < len(snapshot.text_prefix):
        raise ChromiumReadError(
            "Chromium snapshot text count is smaller than the returned prefix."
        )
    if len(snapshot.text_prefix) > text_limit:
        raise ChromiumReadError("Chromium snapshot exceeded the requested text limit.")

    return ChromiumPageObservationEvidence(
        endpoint=endpoint,
        target_id=target.target_id,
        url=snapshot.url,
        title=snapshot.title,
        content=ChromiumPageContentEvidence(
            source="document.body.innerText",
            text_prefix=snapshot.text_prefix,
            text_character_count=snapshot.text_character_count,
            text_limit=text_limit,
            truncated=snapshot.text_truncated,
        ),
    )
