# Milestone 50C — bridge v2 changed bases through the existing transition-v1 format

Decision: **D257**  
Issue: **#242**

## Concrete researcher action

50B permits established 33A preparation to produce a changed evidence basis containing bare exact-range selections:

```text
research_working_set.v2
+
research_working_set_note.v2
```

50C answers the next already-established researcher action:

```text
declared prior endpoint
→ exact prepared changed basis
→ explicit durable cross-working-set transition
→ fresh explicit relinking
```

Before 50C, public 33B represented successor records through general `format + record_sha256` references but validation permitted only the original v1/v1 successor pair.

## Prior-art and internal design decision

The durable transition format remains:

`pyxis.chromium.research_session_working_set_transition.v1`

Its record already contains exactly three content-addressed references:

```text
prior endpoint: format + record_sha256
successor working set: format + record_sha256
successor working-set note: format + record_sha256
```

It does not embed member payloads, selected text, rationale text, filesystem paths, or a working-set schema.

49D/49E established the v2/v2 successor products, and 50B established that ordinary 33A preparation can legitimately produce them.

Therefore the successor product version does not change the transition relationship itself.

This follows the same bounded general-reference reasoning proven by 49I: explicitly authorize another supported referenced product family without inventing a parallel relationship format.

Conclusion: **no transition v2.**

## Exact supported successor pairs

Transition-v1 now supports exactly:

```text
research_working_set.v1
+ research_working_set_note.v1
```

and:

```text
research_working_set.v2
+ research_working_set_note.v2
```

These are pairs, not independent format unions.

Thus the following remain invalid:

```text
working_set.v1 + note.v2
working_set.v2 + note.v1
```

even when the transition record and outer digest are otherwise canonical.

## Persistence

Public 33B persistence still:

1. validates one exact in-memory cross-working-set transition;
2. freshly reopens the explicit prior endpoint through public 24C;
3. freshly reopens the explicit successor working-set/note basis through public 21C;
4. requires that successor formats form one exact supported pair;
5. requires exact successor human text, note mode, member count, member order, and member object identity;
6. writes only the prior endpoint, successor working-set, and successor-note content identities plus the unchanged transition mode.

The persisted format stays transition-v1.

## File-local verification

The verifier still proves only canonical transition bytes and self-integrity.

It validates reference shapes first, then requires the successor working-set/note formats to form one exact supported pair.

This makes a recomputed cross-version pair file-invalid before any referenced durable file is opened.

A same-version but wrong record SHA can remain file-valid; fresh relinking must reject that incorrect attachment.

Thus:

```text
transition file integrity
!=
correct successor attachment
```

## Fresh relinking

Public 33B loading still receives all locators and the complete ordered successor member sequence explicitly.

Generic public 20C/21C reopen the supplied successor basis. 33B then requires:

- supported successor format pairing;
- exact transition reference formats;
- exact transition reference record SHA-256 identities;
- exact prior endpoint identity.

No directory scan, digest search, filename inference, member discovery, chronology, or current/head selection is introduced.

## Member sidecars remain unnecessary

50C uses a real 50B v2 prepared basis and removes already-loaded member sidecars before transition persistence.

Fresh successor reopening still succeeds because public working-set/note relinking consumes caller-supplied loaded member application evidence plus the explicit durable working-set/note files.

The transition record copies no selected source text or member note text.

## Existing v1 path remains unchanged

Original note-only 33A preparations still create v1/v1 successor bases.

Existing 33B tests continue to exercise those bases through the same transition-v1 format and public persistence/load boundaries.

50C does not reinterpret old transition-v1 bytes.

## Explicit stop boundary: 34A remains closed

The existing 34A in-memory revision-root validator independently requires a transition successor whose working set and note are both v1.

50C does not change that validator.

A focused test proves:

```text
valid loaded transition-v1
+ exact v2/v2 successor
→ existing 34A root creation rejects
```

Therefore:

```text
v2-capable 33B
!=
v2-capable 34A
```

Whether the existing root-v1 representation can safely bridge a v2-backed transition remains a separate researcher-action review.

## Focused falsification

50C tests prove:

1. a real 50B v2/v2 preparation can create the existing in-memory 33B transition;
2. persistence writes transition-v1;
3. transition-v1 records exact v2 working-set/note formats and record identities;
4. file-local verification accepts that exact pair;
5. public 33B loading freshly relinks the exact v2/v2 basis;
6. successor member object identity/order survives fresh relinking;
7. member sidecars are unnecessary after preparation;
8. selected source text, rationale text, and durable paths are not copied into transition bytes;
9. both recomputed cross-version pairs fail file-local verification;
10. a file-valid wrong v2 successor-note digest fails fresh relinking;
11. untouched 34A rejects the valid v2-backed loaded transition;
12. the established v1/v1 transition suite remains unchanged.

Repository Zero full-suite CI on Python 3.11–3.14 is the executable gate.

## Non-goals

50C adds no:

- transition v2;
- new working-set or note format;
- 34A widening;
- revision-root v2;
- ordinary revision-edge changes;
- automatic adoption;
- browser interaction;
- source discovery;
- tags, search, or export;
- chronology, current/latest/head authority;
- citation or semantic-support authority.

## Acceptance statement

50C permits only this statement:

> One explicitly prepared v2 working-set/note basis can be durably related to one exact declared edge endpoint through the existing content-addressed transition-v1 representation and freshly reopened from explicit locators, while cross-version successor pairs fail closed and the downstream 34A root boundary remains unchanged.
