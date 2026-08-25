# Milestone 35D — First Ordinary Continuation Above Persisted Root-Backed Ancestry

Decision: D184

## Product question

35C gives one root-backed governed session durable operational restart configuration:

```text
ordinary 31B v1 plan document
→ 35C root-backed overlay
→ 35B fresh re-entry
→ governed root-backed controller
```

The existing 29A/30A lifecycle can revise that controller and adopt one explicit
ordinary successor. The resulting 30A continuation declaration intentionally starts
at the old declared endpoint edge, not at the 34A root.

35D asks:

> How can that first ordinary continuation become restartable without rewriting the
> 35C overlay, pretending the new declaration starts at the root, or flattening the
> 33B→34A ancestry into ordinary edge history?

35D answers with a second compositional locator overlay.

## Continuation overlay format

The new operational format is:

```text
pyxis.chromium.research_root_backed_session_continuation_locator_overlay.v1
```

Its exact top-level fields are:

```text
format
prior_root_backed_overlay_source
declared_edge_sources
declaration_source
```

It contains no 33B, 34A, changed-working-set, appended-member, or ordinary 31B fields.
Those remain owned by the referenced 35C overlay and the ordinary plan it composes.

## Single representation of prior ancestry

An early design candidate carried both:

```text
prior_root_backed_overlay_source
+
decoded prior 35B plan
```

inside the 35D typed plan.

That would create two representations of the same prior configuration that could
disagree.

35D rejects that design.

The typed continuation plan owns only:

```text
prior_root_backed_overlay_source
declared_edge_sources
declaration_source
```

Fresh re-entry must decode the named 35C overlay again. Therefore the overlay path is
operationally meaningful rather than decorative.

## Fresh reconstruction chain

35D performs:

```text
35D continuation plan
→ explicit prior_root_backed_overlay_source
→ existing 35C overlay decoder
→ existing 35B typed root-backed plan
→ public 35B fresh root-backed re-entry
→ fresh prior governed endpoint

fresh prior endpoint
+ explicit declared_edge_sources
+ explicit declaration_source
→ existing 26C declaration relinking
→ existing governed controller
```

The new declaration remains exactly what 30A created: one ordinary continuation
segment above the previous endpoint.

The root-backed ancestry is preserved by composition, not copied into the new
declaration.

## Configuration decoding is not evidence proof

`load_chromium_research_root_backed_session_continuation_reentry_plan_document()`
reads only the 35D document itself.

It does not read the referenced 35C overlay and does not read research evidence.

Thus:

```text
35D document decoded successfully
!=
prior 35C ancestry exists or verifies
!=
continuation declaration verifies
```

Those proofs occur only in fresh re-entry/checkpoint execution.

## Proof-gated checkpoint

The public checkpoint operation accepts:

- one already-earned 35B root-backed re-entry result;
- one explicit successful 30A rollover;
- the explicit prior 35C overlay path;
- the explicit successor edge path;
- the explicit continuation declaration path; and
- a no-overwrite 35D destination.

Before writing, Pyxis performs:

```text
prior 35C overlay
→ decode
→ require typed prior-plan equality with earned 35B session
→ fresh 35B re-entry
→ require presentation + prior endpoint SHA-256 + root SHA-256 agreement

chosen 30A rollover
→ require prior presentation + endpoint SHA-256 agreement

candidate 35D continuation plan
→ fresh 35D re-entry
→ require continuation presentation + endpoint SHA-256 agreement
```

Only after all checks succeed is the continuation overlay written.

The persisted document is then round-trip decoded and must equal the exact candidate
plan.

## Why the 30A declaration is not consolidated back to the root

35D does not generate a replacement declaration spanning:

```text
34A root → every later edge
```

Doing so would create a new declaration solely to make persistence look flatter and
would erase the useful distinction between:

- the original root-backed declared segment; and
- the later caller-chosen ordinary continuation segment.

35D instead preserves both declarations through explicit configuration composition.

## First continuation only

D184 authorizes exactly one ordinary continuation whose prior configuration is a 35C
root-backed overlay.

It does **not** authorize a 35D document to reference another 35D document.

Therefore repeated continuation chaining is still a separate future authority
decision.

This keeps the milestone falsifiable and prevents recursive locator ancestry from
appearing before the one-hop boundary is established.

## Strict document behavior

The 35D overlay rejects:

- malformed JSON;
- duplicate JSON keys;
- missing fields;
- unknown fields;
- unsupported format values;
- empty declared-edge lists; and
- non-path locator values.

No filesystem search is performed for a missing prior overlay, edge, or declaration.

## No-overwrite behavior

The destination is opened exclusively.

Fresh proof occurs before the write. An existing destination remains byte-for-byte
untouched.

## Authority boundaries

35D does not infer or claim:

- global current/latest/canonical head;
- complete history;
- chronology;
- branch identity;
- unique successor;
- semantic improvement;
- evidence support for rationale text;
- source authenticity;
- authorship;
- citation authority;
- path identity;
- filesystem discovery;
- digest-based lookup;
- predecessor discovery;
- browser reacquisition;
- autonomous research; or
- recursive continuation-overlay ancestry.

SHA-256 comparisons remain local content-identity/coherence checks only.

## Falsifiability

Focused 35D coverage proves:

1. one chosen first 30A continuation can be persisted using only a reference to the
   prior 35C overlay plus continuation locators;
2. the 35D document does not copy root/change/ordinary-plan fields;
3. round-trip decoding reproduces the exact locator plan;
4. fresh 35D re-entry reconstructs the prior root-backed ancestry and then the chosen
   ordinary continuation;
5. loading a 35D document succeeds even while its referenced 35C overlay is
   temporarily unavailable, proving document decode is locator-only;
6. a different valid prior 35C overlay rejects before write;
7. a rollover from another root-backed session rejects before write;
8. a wrong explicit successor is not replaced by a decoy file;
9. tampered prior root-backed evidence rejects during mandatory fresh proof;
10. an existing 35D destination is not overwritten;
11. duplicate/missing/unknown JSON fields reject; and
12. the overlay stores no evidence digest or head/chronology/semantic authority.

## Scope

35D adds only:

- `src/pyxis/app/chromium_research_root_backed_session_continuation_reentry_plan_document.py`;
- `tests/test_app_chromium_research_root_backed_session_continuation_reentry_plan_document.py`; and
- this milestone document.

35D does not change:

- ordinary 31A/31B plans;
- ordinary 32A/32B checkpointing;
- 33A/33B basis-change semantics;
- 34A/34B root semantics;
- 35A root-backed declaration adoption;
- 35B root-backed typed re-entry;
- the 35C overlay format;
- generic 24C;
- evidence formats;
- CLI;
- Textual UI;
- Chromium acquisition;
- research-control-plane state; or
- Repository Zero.

## What successful 35D proves

Successful 35D establishes only:

> From one explicit continuation overlay referencing one explicit prior 35C
> root-backed overlay and one explicit ordinary continuation declaration, Pyxis can
> freshly reconstruct the prior 33B→34A ancestry and then the chosen first ordinary
> continuation session, with proof-gated no-overwrite checkpointing and without
> flattening ancestry or claiming global head/chronology/semantic authority.
