# Milestone 35C — Persisted Root-Backed Re-entry Overlay

Decision: D183

## Product question

35B established a typed fresh-process plan for one governed session whose declared
segment starts at a 34A cross-working-set revision root.

That plan is intentionally in-memory only.

The ordinary persisted restart configuration already has a stable format:

```text
pyxis.chromium.research_session_reentry_locator_plan.v1
```

35C asks:

> How can the 35B root-backed plan become durable operational configuration without
> silently widening the ordinary v1 document, copying its locator schema into a
> second format, or turning configuration paths into evidence/head authority?

35C answers with a separate **overlay** document.

## Overlay format

The new operational format is:

```text
pyxis.chromium.research_root_backed_session_reentry_locator_overlay.v1
```

Its top-level shape is exactly:

```text
format
prior_session_plan_source
appended_working_set_members
changed_working_set_source
changed_note_source
transition_source
root_source
declared_edge_sources
declaration_source
```

The overlay does **not** embed the ordinary 31B plan fields.

Instead:

```text
prior_session_plan_source
→ existing ordinary v1 plan document
→ existing 31B decoder
→ existing 31A typed plan
```

The overlay then contributes only the additional locator layer needed by 35B after
the evidence basis changed.

## Why composition beats schema copying

A root-backed session still depends on the complete pre-change ordinary session.

Copying all ordinary plan fields into the new format would create two independent
serializers for the same 31A contract and invite drift between them.

35C therefore preserves one owner for the ordinary plan format:

```text
31B ordinary plan document owns ordinary locator serialization
35C overlay owns changed-basis/root/declaration locator serialization
```

The 35C loader composes those two configuration layers into the existing 35B typed
plan.

## Loading is configuration decoding, not evidence proof

`load_chromium_research_root_backed_session_reentry_plan_document()` reads:

1. the explicitly supplied overlay document; and
2. the explicitly referenced ordinary 31B plan document.

It does **not** read the research evidence artifacts named by those configuration
documents.

The loader performs:

```text
strict overlay JSON decode
→ explicit prior plan path decode
→ existing strict 31B plan decode
→ strict appended-member/path decode
→ existing 35B typed plan construction
```

Therefore:

```text
overlay loaded successfully
!=
research session freshly proven
```

The proof boundary remains public 35B re-entry.

## Strict document behavior

The overlay rejects:

- malformed JSON;
- duplicate JSON object keys;
- missing top-level fields;
- unknown top-level fields;
- unsupported format values;
- empty appended-member arrays;
- unsupported member locator shapes;
- empty declared-edge sequences;
- non-path locator values; and
- an unreadable or invalid explicitly referenced ordinary plan document.

No sibling or decoy configuration file is searched for.

## Relative path behavior

Paths are encoded with the same operational rule used by the ordinary 31B document:

- a path beneath the overlay document's directory tree may be written relative to
  that directory;
- a path outside that tree remains absolute;
- Pyxis does not synthesize `..` traversal.

On load, relative paths are interpreted only relative to the overlay document's
parent directory.

This remains a location rule, not an identity rule.

## Proof-gated persistence

35C does not expose an unchecked public overlay writer.

The public persistence operation accepts one already-earned
`ChromiumResearchRootBackedSessionReentryResult` plus:

- the explicit ordinary v1 plan-document path; and
- the overlay destination.

Before writing, Pyxis performs:

```text
explicit prior plan document
→ existing 31B decode
→ require exact typed-plan equality with earned 35B prior plan

that decoded prior plan
+ earned overlay locator layer
→ candidate 35B typed plan
→ fresh public 35B re-entry
```

The fresh reconstruction must match the already-earned root-backed session by:

- governed presentation;
- declared endpoint record SHA-256; and
- 34A root record SHA-256.

These are content/coherence comparisons, not Python object-identity requirements.

Only after those checks succeed is the overlay written with no-overwrite semantics.

## Round-trip requirement

After persistence, 35C immediately decodes the new overlay through the public 35C
loader.

The decoded typed plan must equal the exact candidate plan that was freshly proven
before the write.

Thus the durable configuration is checked against the same composition contract that
a later fresh process will use.

## No-overwrite behavior

The overlay destination is opened exclusively.

An existing destination is never replaced or normalized.

Failure during fresh proof occurs before any overlay write.

## Authority boundaries

35C does not infer or claim:

- a global current/latest/canonical head;
- complete history;
- chronology;
- branch identity;
- unique successor;
- evidence relevance or completeness;
- semantic improvement;
- semantic support for rationale text;
- source authenticity;
- authorship;
- citation authority;
- path identity;
- filesystem discovery;
- digest-based lookup;
- predecessor discovery;
- browser reacquisition;
- autonomous research;
- automatic creation of a prior ordinary plan document; or
- Textual/CLI authority for the overlay.

The SHA-256 comparisons used before persistence are the already-established local
content-identity/coherence checks. They do not authenticate artifacts or authors.

## Relationship to the ordinary restart-plan flow

35C does not alter:

```text
pyxis.chromium.research_session_reentry_locator_plan.v1
```

and does not modify ordinary 32A continuation-plan construction or the 32B Textual
checkpoint behavior.

A root-backed session now has a durable configuration path, but exposing that path in
the shell or automatically carrying it through later rollovers remains a separate
product/authority decision.

## Falsifiability

Focused 35C coverage proves:

1. an earned 35B session can be freshly re-proven and persisted as one overlay;
2. the overlay contains only the overlay keys and an explicit prior ordinary-plan
   document path rather than copied ordinary-plan fields;
3. the overlay round-trips to the exact 35B typed plan;
4. a plan decoded from the overlay can freshly reconstruct the same governed
   root-backed session;
5. overlay loading still succeeds after referenced research evidence is removed,
   because loading is configuration decoding rather than evidence proof;
6. a different valid ordinary v1 plan document rejects before overlay write;
7. changed/root artifact tampering after the earned 35B result rejects during the
   mandatory fresh proof before overlay write;
8. an existing overlay destination is not overwritten;
9. duplicate JSON keys reject;
10. missing or unknown top-level fields reject;
11. an explicitly missing prior-plan path is not replaced by a decoy file; and
12. the overlay stores locator configuration rather than evidence digests or
    head/chronology/semantic authority.

## Scope

35C adds only:

- `src/pyxis/app/chromium_research_root_backed_session_reentry_plan_document.py`;
- `tests/test_app_chromium_research_root_backed_session_reentry_plan_document.py`; and
- this milestone document.

35C does not change:

- 31A typed ordinary re-entry plans;
- the 31B ordinary v1 plan document;
- 32A ordinary continuation-plan persistence;
- 32B restart-plan checkpoint UI;
- 33A/33B basis-change behavior;
- 34A/34B root behavior;
- 35A root-backed declaration adoption;
- 35B typed root-backed re-entry;
- generic 24C;
- research evidence formats;
- Chromium acquisition;
- CLI;
- Textual UI;
- research-control-plane state; or
- Repository Zero.

## What successful 35C proves

Successful 35C establishes only:

> From one explicit overlay document that references one explicit ordinary v1
> re-entry-plan document and stores only the additional changed-basis/root/declaration
> locators, Pyxis can reconstruct the 35B typed plan and freshly re-enter the same
> governed root-backed session without duplicating the ordinary plan schema,
> discovering files, erasing changed-basis ancestry, or claiming global
> head/chronology/semantic authority.
