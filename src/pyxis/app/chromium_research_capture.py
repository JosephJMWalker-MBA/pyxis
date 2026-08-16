from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import hmac
import json
from pathlib import Path
from typing import Any

from .chromium_research_bundle import ChromiumPageResearchEvidenceBundle


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
_BUNDLE_KEYS = {
    "endpoint",
    "target_id",
    "url",
    "acquisition_mode",
    "acquisition_order",
    "page",
    "links",
    "headings",
    "metadata",
    "paragraphs",
    "tables",
    "lists",
}
_MEMBER_NAMES = (
    "page",
    "links",
    "headings",
    "metadata",
    "paragraphs",
    "tables",
    "lists",
)


class ChromiumResearchCaptureIntegrityError(ValueError):
    """Raised when persisted research-capture bytes fail their narrow integrity contract."""


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchCaptureEvidence:
    """Durable-file evidence produced from one already-observed research bundle."""

    path: Path
    capture_format: str
    bundle_sha256: str
    byte_count: int
    bundle: ChromiumPageResearchEvidenceBundle


@dataclass(frozen=True, slots=True)
class ChromiumPageResearchCaptureVerificationEvidence:
    """Verified file-level integrity facts for one persisted research capture."""

    path: Path
    capture_format: str
    bundle_sha256: str
    byte_count: int
    endpoint: str
    target_id: str
    url: str
    acquisition_mode: str
    acquisition_order: tuple[str, ...]
    document_json: str


def persist_chromium_page_research_capture(
    bundle: ChromiumPageResearchEvidenceBundle,
    destination: Path,
) -> ChromiumPageResearchCaptureEvidence:
    """Persist one research bundle as deterministic JSON without overwriting.

    The bundle must already satisfy the 16A endpoint/target/URL coherence and
    sequential non-atomic acquisition contract. The caller supplies the exact
    destination file; its parent directory must already exist and the destination
    itself must not exist.

    The embedded SHA-256 is an integrity checksum over the canonical bundle JSON.
    It is not an authentication mechanism: an actor able to rewrite both payload
    and checksum can create a different self-consistent file. Persistence does not
    verify source identity, provenance, quotation truth, or atomic DOM state.
    """

    _validate_live_bundle(bundle)
    path = Path(destination).expanduser().resolve()
    if not path.parent.is_dir():
        raise FileNotFoundError(
            f"Research capture parent directory does not exist: {path.parent}"
        )

    bundle_payload = asdict(bundle)
    bundle_bytes = _canonical_json_bytes(bundle_payload)
    bundle_sha256 = hashlib.sha256(bundle_bytes).hexdigest()
    document = {
        "bundle": bundle_payload,
        "bundle_sha256": bundle_sha256,
        "format": _CAPTURE_FORMAT,
    }
    document_bytes = _canonical_document_bytes(document)

    with path.open("xb") as handle:
        handle.write(document_bytes)

    return ChromiumPageResearchCaptureEvidence(
        path=path,
        capture_format=_CAPTURE_FORMAT,
        bundle_sha256=bundle_sha256,
        byte_count=len(document_bytes),
        bundle=bundle,
    )


def verify_chromium_page_research_capture(
    source: Path,
) -> ChromiumPageResearchCaptureVerificationEvidence:
    """Verify canonical bytes and the recorded bundle digest for one capture file.

    Successful return means the file is canonical Pyxis capture JSON, its bundle
    payload matches the SHA-256 recorded beside it, and the persisted top-level
    endpoint/target/URL identities remain coherent across all seven members.

    This verifies file integrity only. It does not authenticate the producer,
    compare the file with a live page, rehydrate a new typed bundle, or strengthen
    the original sequential/non-atomic browser evidence claim.
    """

    path = Path(source).expanduser().resolve()
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ChromiumResearchCaptureIntegrityError(
            "Research capture is not valid UTF-8."
        ) from exc

    try:
        document = json.loads(text)
    except json.JSONDecodeError as exc:
        raise ChromiumResearchCaptureIntegrityError(
            "Research capture is not valid JSON."
        ) from exc

    bundle_payload, recorded_sha256 = _validate_persisted_document(document)
    canonical_bundle_bytes = _canonical_json_bytes(bundle_payload)
    observed_sha256 = hashlib.sha256(canonical_bundle_bytes).hexdigest()
    if not hmac.compare_digest(recorded_sha256, observed_sha256):
        raise ChromiumResearchCaptureIntegrityError(
            "Research capture bundle SHA-256 does not match the persisted payload."
        )

    canonical_document_bytes = _canonical_document_bytes(document)
    if raw != canonical_document_bytes:
        raise ChromiumResearchCaptureIntegrityError(
            "Research capture bytes are not in the canonical Pyxis JSON encoding."
        )

    endpoint = bundle_payload["endpoint"]
    target_id = bundle_payload["target_id"]
    url = bundle_payload["url"]
    acquisition_mode = bundle_payload["acquisition_mode"]
    acquisition_order = tuple(bundle_payload["acquisition_order"])

    return ChromiumPageResearchCaptureVerificationEvidence(
        path=path,
        capture_format=_CAPTURE_FORMAT,
        bundle_sha256=recorded_sha256,
        byte_count=len(raw),
        endpoint=endpoint,
        target_id=target_id,
        url=url,
        acquisition_mode=acquisition_mode,
        acquisition_order=acquisition_order,
        document_json=text,
    )


def _validate_live_bundle(bundle: ChromiumPageResearchEvidenceBundle) -> None:
    if not isinstance(bundle, ChromiumPageResearchEvidenceBundle):
        raise TypeError("bundle must be ChromiumPageResearchEvidenceBundle.")
    if bundle.acquisition_mode != _ACQUISITION_MODE:
        raise ValueError("Research bundle acquisition mode is not the proven 16A mode.")
    if bundle.acquisition_order != _ACQUISITION_ORDER:
        raise ValueError("Research bundle acquisition order is not the proven 16A order.")
    if not all(
        isinstance(value, str) and value
        for value in (bundle.endpoint, bundle.target_id, bundle.url)
    ):
        raise ValueError("Research bundle endpoint, target_id, and url must be non-empty strings.")

    for name in _MEMBER_NAMES:
        member = getattr(bundle, name)
        if getattr(member, "endpoint", None) != bundle.endpoint:
            raise ValueError(f"Research bundle {name} endpoint is incoherent.")
        if getattr(member, "target_id", None) != bundle.target_id:
            raise ValueError(f"Research bundle {name} target_id is incoherent.")
        if getattr(member, "url", None) != bundle.url:
            raise ValueError(f"Research bundle {name} url is incoherent.")


def _validate_persisted_document(document: Any) -> tuple[dict[str, Any], str]:
    if not isinstance(document, dict) or set(document) != {
        "bundle",
        "bundle_sha256",
        "format",
    }:
        raise ChromiumResearchCaptureIntegrityError(
            "Research capture document has an invalid top-level shape."
        )
    if document["format"] != _CAPTURE_FORMAT:
        raise ChromiumResearchCaptureIntegrityError(
            "Research capture format is unsupported."
        )

    recorded_sha256 = document["bundle_sha256"]
    if (
        not isinstance(recorded_sha256, str)
        or len(recorded_sha256) != 64
        or any(character not in "0123456789abcdef" for character in recorded_sha256)
    ):
        raise ChromiumResearchCaptureIntegrityError(
            "Research capture bundle SHA-256 has an invalid shape."
        )

    bundle = document["bundle"]
    if not isinstance(bundle, dict) or set(bundle) != _BUNDLE_KEYS:
        raise ChromiumResearchCaptureIntegrityError(
            "Research capture bundle has an invalid top-level shape."
        )

    endpoint = bundle["endpoint"]
    target_id = bundle["target_id"]
    url = bundle["url"]
    if not all(isinstance(value, str) and value for value in (endpoint, target_id, url)):
        raise ChromiumResearchCaptureIntegrityError(
            "Research capture bundle identity fields must be non-empty strings."
        )
    if bundle["acquisition_mode"] != _ACQUISITION_MODE:
        raise ChromiumResearchCaptureIntegrityError(
            "Research capture acquisition mode is unsupported."
        )
    if bundle["acquisition_order"] != list(_ACQUISITION_ORDER):
        raise ChromiumResearchCaptureIntegrityError(
            "Research capture acquisition order is unsupported."
        )

    for name in _MEMBER_NAMES:
        member = bundle[name]
        if not isinstance(member, dict):
            raise ChromiumResearchCaptureIntegrityError(
                f"Research capture {name} evidence has an invalid shape."
            )
        if member.get("endpoint") != endpoint:
            raise ChromiumResearchCaptureIntegrityError(
                f"Research capture {name} endpoint is incoherent."
            )
        if member.get("target_id") != target_id:
            raise ChromiumResearchCaptureIntegrityError(
                f"Research capture {name} target_id is incoherent."
            )
        if member.get("url") != url:
            raise ChromiumResearchCaptureIntegrityError(
                f"Research capture {name} url is incoherent."
            )

    return bundle, recorded_sha256


def _canonical_json_bytes(payload: Any) -> bytes:
    try:
        encoded = json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise ValueError("Research capture evidence is not canonical-JSON serializable.") from exc
    return encoded.encode("utf-8")


def _canonical_document_bytes(document: Any) -> bytes:
    return _canonical_json_bytes(document) + b"\n"
