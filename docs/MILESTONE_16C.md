# Milestone 16C — Verified Chromium Research Capture Rehydration

## Product question

Can Pyxis reopen a previously persisted, integrity-verified 16B Chromium research capture as the typed 16A application evidence model without reacquiring the browser and without strengthening the capture's authenticity, provenance, temporal, citation, quotation, or atomic-snapshot claims?

16C answers **yes**, but only after a second validation boundary beyond 16B file verification.

## Proven path

```text
persisted 16B capture
    ↓
16B canonical-byte + SHA-256 verification
    ↓
exact nested JSON type reconstruction
    ↓
full application evidence validation
    ↓
lossless payload round-trip proof
    ↓
ChromiumPageResearchLoadedCaptureEvidence
    ├── verification
    └── reconstructed ChromiumPageResearchEvidenceBundle
```

`pyxis.app.load_chromium_page_research_capture()` first delegates file integrity to `verify_chromium_page_research_capture()`. It does not duplicate the 16B canonical-file boundary and it does not contact Chromium.

Only after 16B verification succeeds does the loader decode the persisted bundle into the exact nested application dataclasses. JSON types are checked explicitly, including rejecting booleans where integer fields are required. Dataclass field sets must match exactly rather than accepting unknown or missing fields.

## Verification is necessary, not sufficient

16B and 16C answer different questions.

16B verification asks whether the file is a canonical supported Pyxis capture whose complete bundle payload matches the SHA-256 recorded beside it and whose top-level endpoint, target, URL, acquisition mode, and acquisition order remain coherent.

16C asks the stronger downstream question: is that verified payload valid enough to become typed Pyxis application evidence again?

A writer able to change both payload and digest can construct a new self-consistent 16B file. 16C therefore independently validates nested evidence invariants before it emits typed evidence. Tests prove a capture with a recomputed valid SHA-256 can pass 16B verification yet fail 16C because, for example, a collection count is negative or a JSON boolean occupies an integer field.

This does not turn 16C into producer authentication. It is application-contract validation, not proof of who created the file or whether the original page/source was genuine.

## Nested evidence validation

Rehydration validates the established evidence contracts rather than trusting arbitrary JSON that happens to have the right field names.

The loader checks:

- exact 16A acquisition mode and acquisition order;
- exact endpoint / target / URL coherence across all seven evidence families;
- literal evidence-source strings already established by 15A–15G;
- collection counts, limits, returned lengths, and truncation relationships;
- text counts, limits, prefixes, and truncation relationships;
- contiguous DOM-order ordinals;
- heading levels from 1 through 6;
- metadata declaration ordinals and text bounds;
- literal table `TH` / `TD` identity, non-negative spans, and nested row/cell contracts;
- literal list `OL` / `UL` identity, parent-list/item constraints, item ordinals, and direct-text contracts.

After reconstruction, `asdict()` over the new immutable bundle must serialize back to the exact persisted bundle payload. Rehydration is therefore lossless; it does not normalize, repair, enrich, or silently discard persisted evidence.

## Acquisition origin remains visible

16C deliberately does not return only a naked `ChromiumPageResearchEvidenceBundle`.

The public result is frozen `ChromiumPageResearchLoadedCaptureEvidence` containing:

```text
verification
    exact 16B ChromiumPageResearchCaptureVerificationEvidence

bundle
    newly reconstructed immutable ChromiumPageResearchEvidenceBundle
```

The reconstructed bundle has the same typed evidence shape as the original 16A bundle, but it is not a fresh browser observation. Retaining the exact file-verification evidence beside it preserves the fact that this evidence entered the current process through durable capture rehydration.

## Browser-independent acceptance proof

The established real-Chromium integration now proves the complete lifecycle:

```text
live caller-owned Chromium
    ↓
16A research bundle
    ↓
16B deterministic capture + verification
    ↓
terminate Chromium process
    ↓
16C typed rehydration from the durable file
```

The loader runs only after the disposable Chromium process has exited. The reconstructed bundle is value-equal to the original live evidence while remaining a distinct newly created object, and the load result retains the capture's exact digest and byte-count verification evidence.

No browser endpoint needs to remain reachable for durable evidence to re-enter the typed application layer.

## Failure proofs

Focused tests establish that:

- a valid persisted capture rehydrates into a new frozen bundle equal to the original bundle;
- the result retains frozen 16B verification evidence beside the reconstructed bundle;
- rehydration is lossless rather than normalized;
- checksum-valid semantic corruption is rejected before typed evidence is emitted;
- checksum-valid JSON type corruption is rejected before typed evidence is emitted;
- existing 16B stale-digest and noncanonical-byte failures remain owned by the verifier;
- the established no-overwrite persistence behavior is unchanged.

## Explicit non-goals

16C adds no:

- Chromium acquisition, discovery, target selection, navigation, or interaction;
- browser-state ownership or requirement that the original browser remain alive;
- mutation, repair, migration, or version conversion of a capture file;
- new capture format;
- automatic capture discovery, directory management, indexing, or search;
- cross-capture comparison;
- passage ranking, relevance scoring, selection, annotation, notes, claims, or questions;
- HMAC, signature, PKI, trusted timestamp, producer authentication, or chain-of-custody system;
- verified publisher or source identity;
- quotation or citation verification;
- locator-stability claims;
- atomic DOM snapshot or page-version identity;
- semantic cross-family joins;
- LLM interpretation, summarization, or autonomous research workflow;
- researcher UI.

## Validation

Implementation and nested-validation proof:

- Actions #545 on `0726adc315c04a8eab1c97b67cb3999db5c9cc32` passed on Python 3.11, 3.12, 3.13, and 3.14.

Browser-independent typed-rehydration proof:

- Actions #547 on `fd3c16682d6e0c88cf77a09c1aa429ae3049f78d` passed on Python 3.11, 3.12, 3.13, and 3.14.
- The inspected Python 3.11 log checked out that exact head, collected **268 tests**, passed all eight capture tests, passed the real Chromium research-bundle integration, and finished **268 passed in 40.32s**.
- The integration terminates Chromium before calling the 16C loader.

## Decision D130

**An integrity-verified durable Chromium research capture may be reopened as typed application evidence only when the complete persisted nested payload passes exact structural/domain validation and lossless reconstruction. Rehydration must retain the 16B file-verification evidence that authorized the load; the reconstructed bundle is not fresh browser observation and gains no stronger authenticity, source-provenance, temporal, citation, quotation, or atomic-snapshot authority.**

## Next-step guardrail

16C closes the basic `observe → compose → persist → verify → reopen` evidence lifecycle. Do not continue by adding capture indexing, cross-capture comparison, authentication infrastructure, semantic interpretation, or researcher UI merely because durable typed evidence now exists.

The next milestone should come from a concrete researcher action that needs this evidence. A likely pressure is explicit human selection of already-observed evidence, but that should be evaluated after 16C is merged rather than assumed here.
