# Milestone 16A — Read-Only Chromium Research Evidence Bundle

## Product question

Can Pyxis compose the seven proven browser evidence families into one convenient research-page evidence object without pretending that seven sequential browser reads form one atomic DOM snapshot?

Milestone 16A answers **yes**, but only by keeping the acquisition contract explicit.

## Why this milestone exists

Milestones 15A through 15G deliberately proved seven concrete read-only evidence families before Pyxis introduced any broader browser-research composition:

1. page URL/title/body text;
2. links;
3. headings;
4. page-declared metadata;
5. paragraphs;
6. tables;
7. ordered/unordered lists.

After seven independent proofs, the next concrete product problem is no longer “what additional HTML element can Pyxis expose?” A researcher needs a convenient way to acquire the already-proven evidence for one page without manually coordinating seven calls.

The obvious danger is epistemic: seven separate CDP reads can occur at seven different moments. Wrapping them in one object must not silently promote them into an atomic browser snapshot.

## 16A boundary

16A adds one **application-level composition** and no new browser transport:

```text
caller-supplied Chromium endpoint
        ↓
observe_chromium_page()
        ↓
existing 15A target-selection rules
        ↓
exact selected target id
        ↓
links
        ↓
headings
        ↓
metadata
        ↓
paragraphs
        ↓
tables
        ↓
lists
        ↓
exact endpoint / target / URL coherence gate
        ↓
frozen ChromiumPageResearchEvidenceBundle
```

The fixed acquisition order is:

```text
page → links → headings → metadata → paragraphs → tables → lists
```

The bundle records:

```text
acquisition_mode = "sequential_non_atomic_url_coherent"
```

That string is part of the evidence contract, not explanatory decoration.

## Target authority

The first page observation owns target selection exactly as 15A already proved:

- if exactly one page exists, it may be selected implicitly;
- if multiple pages exist, the caller must supply an exact `target_id`;
- Pyxis does not infer an active/current tab.

After the first observation succeeds, every later family receives the exact selected target ID explicitly. 16A does not add a second target-selection rule.

## Coherence rule

Every returned constituent evidence object must retain the same:

- normalized endpoint;
- exact target ID;
- exact page URL.

The check occurs after each read. If a member differs, Pyxis raises `ChromiumReadError`, stops acquisition immediately, and emits no bundle.

A URL change is therefore detectable and rejected.

A same-URL DOM mutation is **not** detectable by this contract. The bundle remains sequential and non-atomic even when all seven URLs match. 16A does not introduce a DOM hash, page-version token, mutation observer, freeze protocol, or browser-state ownership merely to create stronger snapshot language.

## Evidence ownership

`ChromiumPageResearchEvidenceBundle` contains the exact seven existing application evidence objects:

- `ChromiumPageObservationEvidence`;
- `ChromiumPageLinksEvidence`;
- `ChromiumPageHeadingsEvidence`;
- `ChromiumPageMetadataEvidence`;
- `ChromiumPageParagraphsEvidence`;
- `ChromiumPageTablesEvidence`;
- `ChromiumPageListsEvidence`.

Those constituent objects remain authoritative for their own facts. The bundle does not copy, reinterpret, summarize, merge, rank, deduplicate, or normalize their contents.

## Limit policy

16A deliberately adds **no new bundle-wide limit configuration**.

Each constituent observer uses its already-established bounded defaults. If a caller needs a differently bounded acquisition today, the existing individual observers remain available.

A future bundle-limit configuration object would require product pressure beyond the fact that such an abstraction is easy to build.

## Real Chromium proof

The 16A acceptance page contains all seven already-supported evidence shapes on one static local page:

- title and rendered body text;
- one link;
- one `h1`;
- authored `lang`;
- one canonical declaration;
- one meta description;
- one paragraph;
- one table;
- one ordered list with authored `start` / item `value`.

The production `observe_chromium_page_research_bundle()` path is called against a real disposable headless Chromium target.

The acceptance test proves:

- one exact caller-owned target is retained across the bundle;
- every member retains the same endpoint, target ID, and page URL;
- the acquisition order is exactly the documented seven-step order;
- the acquisition mode is explicitly sequential/non-atomic;
- each constituent family returns its expected literal evidence;
- no new browser transport or browser-control operation participates.

## Validation

Actions #527 on `b4e803ec725fb7bff34020ee94f894bb7cc759af` passed the full suite on:

- Python 3.11;
- Python 3.12;
- Python 3.13;
- Python 3.14.

The inspected Python 3.11 log collected **260 tests** and finished with **260 passed**. It shows the five focused 16A application tests and the real Chromium 16A integration passing before the established browser integration families continue successfully.

## Explicit non-goals

16A adds no:

- atomic DOM snapshot claim;
- DOM freeze or mutation lock;
- DOM hash or page-version identity;
- browser-state ownership;
- new CDP method;
- caller-supplied JavaScript;
- navigation or link following;
- scrolling or viewport ownership;
- target activation/creation/closure;
- click or form submission;
- persistence;
- evidence merging or normalization;
- cross-family semantic relationships;
- citation verification;
- source/provenance verification;
- ranking or recommendation;
- summarization or interpretation;
- LLM invocation;
- autonomous research workflow;
- browser UI;
- new bundle-wide limit abstraction.

## Decision D128

**Existing read-only Chromium evidence families may be composed into one research-page bundle only when composition preserves their independent evidence ownership and makes acquisition order, exact target reuse, URL coherence, and non-atomicity explicit. URL agreement across sequential reads is a coherence check, not proof of one frozen DOM state. A bundle is a convenience boundary, not a new browser snapshot authority or source of truth.**

## Next-step guardrail

Do not follow 16A by adding navigation, citation verification, semantic cross-family joins, a browser agent loop, or a generalized evidence-query language merely because the bundle makes those directions convenient.

The next browser milestone should be chosen from an actual research workflow pressure that cannot be satisfied by the seven existing evidence families plus this explicit composition layer.
