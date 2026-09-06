# Milestone 49H — version-aware in-memory extension after continuation v2

Decision: **D253**  
Issue: **#231**

## Concrete researcher action

49G makes the second append-only human wording change on the v2 rationale line durable and explicitly relinkable through continuation v2.

The next established application action already exists as 24A:

```text
loaded continuation
+ exact different human wording
→ one further immutable human revision in memory
```

49H allows that action to consume either exact supported loaded continuation family without granting any new durable edge authority.

## Prior art and reuse decision

W3C PROV-O models `prov:wasRevisionOf` as an explicit derivation from an original entity to a revised entity. Repeated revision relationships therefore do not require mutation of prior entities.

The W3C Web Annotation Protocol demonstrates the contrasting mutable-resource model, where PUT replaces annotation state and `If-Match` may protect concurrent updates.

Internally, 49F already demonstrated the crucial separation: an in-memory human-action constructor may become version-aware while its downstream durable format remains frozen. 49G then versioned that downstream persistence separately.

Conclusion: **no end-to-end substitute demonstrated in this review; reuse 24A exactly and widen only its exact predecessor-family validation.**

## Exact supported predecessor families

24A now accepts exactly:

```text
continuation v1 → revision v1
continuation v2 → revision v2
```

Cross-version pairings reject.

No generic version inference is added.

## What remains unchanged

24A still:

- consumes one already-loaded 23C continuation;
- performs no file reads;
- retains the exact caller-supplied loaded continuation object;
- re-establishes the retained continuation through public 23A;
- preserves exact predecessor revision identity;
- creates the new human revision through public 22A over the exact predecessor revised-note object;
- preserves caller wording verbatim;
- rejects exact textual no-ops;
- adds no chronology, revision numbering, semantic diff, source discovery, or truth authority.

## Durable 24B remains closed

49H deliberately does not change:

`pyxis.chromium.research_working_set_note_revision_edge.v1`

or:

`persist_chromium_research_working_set_note_revision_edge(...)`

An extension created from a continuation-v2 predecessor is therefore valid in memory but still fails 24B before write because the durable predecessor continuation format is unsupported.

This preserves:

```text
valid next human action in memory
!=
durable revision-edge authority
```

## Focused falsification

49H tests prove:

1. established continuation-v1 extension behavior remains intact;
2. one freshly loaded continuation-v2 predecessor is accepted;
3. the exact loaded v2 predecessor object is retained;
4. the exact working-set object is retained;
5. exact human wording survives verbatim;
6. exact v2 no-op text is rejected through public 22A;
7. v1/v2 and v2/v1 predecessor-family mismatches reject;
8. deleting member, working-set, note, revision, and continuation files after successful loading does not prevent the in-memory extension;
9. existing 24B edge-v1 persistence rejects the v2-backed extension before creating a destination.

Repository Zero full-suite CI on Python 3.11–3.14 remains the executable gate.

## Compatibility

49H changes no durable format and no existing writer or verifier.

It adds no:

- edge v2;
- edge verifier/loader widening;
- automatic format migration;
- recursive history model;
- timestamps or revision numbers;
- semantic diff or reason-for-change inference;
- source discovery;
- UI or CLI;
- browser authority;
- governed-session behavior;
- authorship, authentication, or trusted-time authority.

## Next boundary

After 49H, the next distinct question is durable rather than in-memory:

> Should a valid 24A extension whose predecessor is continuation v2 be persistable as a versioned revision edge?

That decision may affect later edge/history/root products and therefore must be reviewed separately rather than inferred from 49H.

## Acceptance statement

49H permits only this statement:

> One further append-only human wording change can be represented in memory from either exact supported loaded continuation family, while durable revision-edge v1 remains frozen and closed to continuation v2.
