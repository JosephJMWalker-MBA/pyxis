# Milestone 16B — Durable Chromium Research Capture

## Product question

Can Pyxis preserve one already-observed Chromium research bundle as durable, inspectable evidence without re-reading the browser, reinterpreting the evidence, or promoting a file checksum into verified provenance?

16B answers **yes**, through one narrow application-level persistence boundary.

## Boundary

The established browser path remains unchanged:

```text
caller-owned Chromium
    ↓
15A–15G read-only evidence families
    ↓
16A sequential non-atomic research bundle
    ↓
16B deterministic capture persistence
    ↓
caller-chosen JSON file
```

Persistence begins only after a `ChromiumPageResearchEvidenceBundle` already exists. Saving a capture never triggers a second page observation or any new Chromium/CDP command.

## Capture format

The persisted document has exactly three top-level fields:

```json
{
  "bundle": { "...": "complete 16A bundle payload" },
  "bundle_sha256": "...",
  "format": "pyxis.chromium.research_capture.v1"
}
```

The bundle payload is the complete dataclass projection of the seven-family 16A bundle. No evidence family is selected, summarized, ranked, omitted, or normalized into a second semantic representation.

Serialization is deterministic:

- UTF-8
- Unicode retained directly (`ensure_ascii=False`)
- keys sorted
- compact JSON separators
- non-finite numeric values rejected
- one final newline

The SHA-256 is computed over the canonical JSON bytes of the complete `bundle` payload, excluding the outer format/checksum wrapper.

## Persistence operation

`pyxis.app.persist_chromium_page_research_capture()` accepts:

- one existing `ChromiumPageResearchEvidenceBundle`;
- one exact caller-supplied destination file path.

Before writing, it rechecks the narrow 16A bundle invariants required for capture:

- acquisition mode is exactly `sequential_non_atomic_url_coherent`;
- acquisition order is exactly `page → links → headings → metadata → paragraphs → tables → lists`;
- bundle endpoint, target ID, and URL are non-empty;
- all seven constituent members retain that exact endpoint, target ID, and URL.

The destination parent directory must already exist. The file is opened in exclusive-create mode; an existing destination is never overwritten.

Successful persistence returns frozen `ChromiumPageResearchCaptureEvidence` containing:

- exact resolved path;
- capture-format identity;
- bundle SHA-256;
- complete file byte count;
- the exact original 16A bundle object.

Persistence does not alter the original bundle.

## Verification operation

`pyxis.app.verify_chromium_page_research_capture()` reads one existing capture file and verifies only the durable-file contract.

It requires:

1. valid UTF-8;
2. valid JSON;
3. exact three-field outer document shape;
4. exact supported capture-format identity;
5. a lowercase 64-character SHA-256 field;
6. exact expected 16A bundle top-level fields;
7. the established acquisition mode/order;
8. endpoint/target/URL coherence across all seven persisted members;
9. recomputed canonical bundle SHA-256 equal to the recorded digest;
10. complete file bytes equal to Pyxis's canonical JSON encoding of that same document.

A successful verification returns frozen `ChromiumPageResearchCaptureVerificationEvidence` with path, format, digest, byte count, endpoint, target ID, URL, acquisition mode/order, and the exact canonical document JSON string.

Verification does **not** reconnect to Chromium and does not reconstruct a new typed `ChromiumPageResearchEvidenceBundle`.

## Integrity is not authentication

The embedded SHA-256 is intentionally described as file-integrity evidence, not authentication.

It can prove that the persisted bundle payload still matches the digest recorded beside it. It cannot prove who created the capture if an actor can rewrite both payload and checksum. It therefore does not establish:

- source authenticity;
- publisher identity;
- verified provenance;
- cryptographic authorship;
- trusted timestamping;
- quotation truth;
- page immutability;
- evidence chain-of-custody against an adversary with file-write authority.

Any future HMAC, signature, external timestamp, or trust-anchor design requires a separate product question and authority model.

## No timestamp in 16B

16B deliberately does not add a capture timestamp.

A timestamp acquired when the file is written would describe persistence time, not the seven distinct browser-read moments that produced the 16A bundle. Labeling that value as page-capture time would overstate the evidence.

If temporal provenance becomes necessary, it should be acquired explicitly at the observation boundary with semantics that preserve sequential acquisition rather than inferred later from filesystem metadata or save time.

## Real Chromium proof

The existing 16A real-browser acceptance path now continues through 16B without launching a second browser.

One caller-owned local Chromium page produces the complete seven-family `ChromiumPageResearchEvidenceBundle`. That exact bundle object is then passed to `persist_chromium_page_research_capture()`, producing one new capture file. `verify_chromium_page_research_capture()` verifies that file without reconnecting to the page.

The acceptance path proves:

- persistence consumes the exact already-observed bundle object;
- no second acquisition path is introduced;
- capture format is `pyxis.chromium.research_capture.v1`;
- persisted and verified SHA-256 values match;
- persisted and verified byte counts match;
- endpoint, exact target ID, URL, acquisition mode, and acquisition order survive persistence unchanged;
- the browser remains caller-owned and no control authority is added.

## Failure proofs

Focused application tests prove:

- the same bundle written to two distinct new files produces byte-identical deterministic captures and the same digest;
- Unicode remains direct UTF-8 content;
- capture/verification evidence dataclasses are frozen;
- an existing destination is not overwritten;
- a missing parent directory is rejected without creating a capture;
- an incoherent manually constructed bundle is rejected before write;
- changing the persisted payload while retaining the old digest fails SHA-256 verification;
- reformatting otherwise self-consistent JSON fails the canonical-byte contract.

## Validation

Actions #537 on exact implementation head `60fdb77ae1a56dd2654311fac70b743f4c99e797` passed on:

- Python 3.11
- Python 3.12
- Python 3.13
- Python 3.14

The inspected Python 3.11 log collected **265 tests**. It shows:

- `tests/test_app_chromium_research_bundle_integration.py` passing with the real Chromium → bundle → persist → verify path;
- all five `tests/test_app_chromium_research_capture.py` tests passing;
- all established Repository Zero and browser tests passing;
- **265 passed**.

## Explicit non-goals

16B adds no:

- browser navigation or interaction;
- new CDP method;
- second page acquisition during save;
- automatic browser discovery;
- capture timestamp;
- filesystem-mtime provenance;
- overwrite/update semantics;
- automatic file naming or capture directory;
- capture database or ledger;
- typed bundle rehydration;
- capture search/indexing;
- capture comparison;
- HMAC, signature, PKI, or authentication;
- verified source identity or publisher provenance;
- quotation/citation verification;
- atomic DOM snapshot claim;
- DOM hash or page-version identity;
- cross-family semantic joins;
- ranking, summarization, or LLM interpretation;
- autonomous research workflow;
- browser UI.

## Decision D129

**A completed read-only Chromium research bundle may be persisted as a deterministic, no-overwrite capture artifact whose complete bundle payload is protected by explicit SHA-256 integrity evidence. Persistence and later file verification preserve already-acquired evidence; they do not reacquire page state, authenticate the producer or source, verify provenance, add a trusted timestamp, rehydrate new semantic authority, or strengthen the bundle's sequential/non-atomic browser claim.**

## Next-step guardrail

Do not turn one capture file into a generalized research database merely because persistence now exists.

The next browser/research capability should answer a concrete researcher workflow need. Likely candidates include read-only capture presentation/reopening, explicitly modeled temporal provenance, or another operation justified by actual use. Typed rehydration, capture indexing/search, cross-capture comparison, authenticity/signature systems, citation verification, semantic interpretation, browser control, and autonomous workflows remain separate decisions.
