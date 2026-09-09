# Milestone 51A — CLI capture of one already-open Chromium page

Decision: **D281**  
Issue: **#293**  
Pull request: **#294**

## Concrete researcher action

50Y and 50Z establish the supported downstream path:

```text
durable research capture
→ research-save-selection
→ durable 49A bare-selection sidecar
→ research-shell --plan
   + explicit candidate capture
   + explicit candidate selection
→ existing first changed-basis product
```

The remaining concrete entry gap was one step earlier:

> Given a caller-owned Chromium DevTools endpoint with an already-open page,
> create one bounded durable Pyxis research capture without writing Python and
> without granting Pyxis navigation or browser-state ownership.

## Reuse review

No new browser reader, capture model, or durable format is required.

Public 16A already owns the complete bounded observation:

```text
caller-supplied DevTools endpoint
→ exact page-target selection under existing 15A rules
→ page
→ links
→ headings
→ metadata
→ paragraphs
→ tables
→ lists
→ ChromiumPageResearchEvidenceBundle
```

That bundle is explicitly sequential and non-atomic.

Public 16B already owns:

```text
exact 16A bundle
→ deterministic canonical JSON
→ SHA-256 self-integrity
→ no-overwrite research_capture.v1 persistence
→ strict fresh verification
```

Generic DevTools/CDP tooling exposes a much broader browser-control surface. That
is not the contract Pyxis needs here. 51A therefore reuses the narrower established
16A/16B path instead of exposing arbitrary CDP commands, navigation, screenshots,
JavaScript execution, or a second capture representation.

Conclusion:

> no end-to-end substitute demonstrated for this exact bounded Pyxis
> evidence/persistence contract; reuse the existing public boundaries.

## Decision

Add one thin CLI command:

```text
pyxis research-capture \
  --endpoint <caller-owned DevTools endpoint> \
  [--target-id <exact page target id>] \
  --destination <new research_capture.v1.json>
```

The command adds orchestration only.

It creates no application-layer type, browser-layer capability, or durable format.

## Exact target-selection semantics

`--endpoint` is mandatory.

`--target-id` is optional only because the pre-existing observation contract already
permits implicit selection when exactly one page target is available.

When multiple page targets are available and no target id is supplied, public
observation remains fail-closed.

51A does not infer:

- active tab;
- current tab;
- newest tab;
- first tab;
- browser focus; or
- URL preference.

An explicit target id is forwarded unchanged to public 16A.

An omitted target id is forwarded as `None`, preserving the established behavior.

## Exact execution sequence

The CLI performs:

```text
explicit endpoint
+ optional exact target id
→ observe_chromium_page_research_bundle()
→ exact returned bundle
→ persist_chromium_page_research_capture()
→ exact persisted path
→ verify_chromium_page_research_capture()
→ deterministic JSON operation receipt
```

The CLI does not duplicate the seven-reader acquisition sequence.

It does not rebuild canonical capture encoding or verification.

## Proof after write

A successful command does not trust the persistence return alone.

The just-written artifact is freshly verified.

The command requires persistence and verification to agree on:

- resolved output path;
- exact capture format;
- bundle SHA-256; and
- byte count.

Any disagreement fails before a success receipt is emitted.

## Receipt boundary

The deterministic receipt contains only operation and durable-artifact facts:

- `receipt_role = operation_receipt_not_source_authentication`;
- normalized endpoint;
- exact selected target id;
- observed URL;
- capture output path;
- `pyxis.chromium.research_capture.v1` format;
- bundle SHA-256;
- sequential/non-atomic acquisition mode;
- exact acquisition order; and
- byte count.

The receipt is not:

- source authentication;
- authorship proof;
- trusted time;
- chain-of-custody proof;
- quotation verification;
- citation authority;
- atomic DOM-snapshot proof; or
- semantic support.

## No-overwrite and failure ordering

Persistence remains the unchanged public 16B no-overwrite boundary.

An existing destination is not replaced.

A missing destination parent is not created implicitly.

If observation fails, persistence is never attempted.

Therefore target ambiguity, endpoint failure, or any other 16A failure creates no
capture artifact.

## No browser-control widening

51A adds no new browser-layer implementation.

The command has no option for:

- URL navigation;
- activation;
- click;
- form submission;
- page creation;
- page closure;
- arbitrary JavaScript;
- arbitrary CDP method execution;
- current/active-tab inference;
- repeated capture; or
- browser mutation.

The only live-browser action is the already-proven bounded read-only 16A observation.

## Executable proof

Executable head:

`b5f7c47be939037a570c02172575bfed650b64d0`

passed Repository Zero on:

```text
Python 3.11
Python 3.12
Python 3.13
Python 3.14
```

on both push and pull-request workflows.

The focused 51A proof demonstrates:

1. an explicit target id is forwarded unchanged to public 16A;
2. an omitted target id is forwarded as `None`;
3. the exact returned 16A bundle is passed to public 16B persistence;
4. the exact persisted path is freshly verified through public 16B verification;
5. the deterministic receipt is derived from verification facts;
6. persistence/verification path disagreement fails closed;
7. format disagreement fails closed;
8. bundle-digest disagreement fails closed;
9. byte-count disagreement fails closed;
10. target ambiguity/observation failure occurs before persistence;
11. existing-destination failure preserves existing bytes;
12. missing-parent failure creates neither directory nor file; and
13. command help exposes only the narrow endpoint/target/destination surface.

The first pre-proof CI attempt exposed only an incorrect test assumption that
`argparse` would preserve `Path` object identity. The CLI correctly creates an
equivalent `Path` value from command text. The proof was corrected to assert path
value equality; production behavior was unchanged.

The documentation-complete exact head must pass the same matrix before merge.

## Scope

51A changes only:

- thin CLI parsing and orchestration;
- focused CLI proof;
- this milestone record; and
- compact README continuity.

It changes no:

- public 15A target-selection semantics;
- public 16A evidence acquisition;
- public 16B persistence or verification;
- browser implementation;
- capture format;
- source-authentication model;
- research-session model;
- changed-basis UI; or
- durable lineage format.

## Explicit stop boundary

51A proves only:

```text
caller-owned Chromium endpoint
+ one already-open page
→ bounded public 16A observation
→ public 16B research_capture.v1
```

Do not infer:

- launching Chromium;
- navigating to a URL;
- choosing an active/current tab among multiple pages;
- autonomous page discovery;
- browser highlighting;
- periodic capture;
- capture indexing/search;
- change monitoring;
- source authentication;
- trusted time;
- quotation/citation authority;
- semantic interpretation; or
- automatic downstream selection/session actions.

## Compact result

After 51A the supported researcher product path is:

```text
already-open Chromium page
→ research-capture
→ durable research_capture.v1
→ research-save-selection
→ durable bare-selection sidecar
→ research-shell --plan
   + explicit saved candidate pair
→ fresh public 49B relink
→ existing first changed-basis product
```

The product now reaches from caller-owned live browser evidence to governed use of one
saved passage without requiring custom Python at the capture or saved-selection seams,
while the researcher continues to own navigation and every stronger interpretation.
