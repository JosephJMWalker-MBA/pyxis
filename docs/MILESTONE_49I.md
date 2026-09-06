# Milestone 49I — resume the general revision-edge lineage from continuation v2

Decision: **D254**  
Issue: **#233**

## Concrete researcher action

49H makes one further human revision valid in memory after an exact loaded continuation-v2 predecessor.

The next action is durable:

```text
loaded continuation v2
→ 24A human extension
→ preserve that extension
→ reopen it explicitly
→ continue ordinary later revisions
```

49I routes that action into the already-general 24B/24C revision-edge lineage instead of creating a parallel edge-v2 family.

## Prior-art decision

W3C PROV-O models revision as an explicit derivation relationship through `prov:wasRevisionOf`. Git commit objects and IPFS Merkle DAGs demonstrate immutable content-addressed objects linked to predecessor objects by durable identifiers.

Those systems do not supply Pyxis's exact human-action and authority boundaries. Git in particular also carries author/committer/time and commonly participates in branch/head semantics that Pyxis has not earned.

Internally, the decisive precedent is stronger:

- 24B / D156 deliberately introduced `research_working_set_note_revision_edge.v1` as a general content-addressed revision-edge representation so later human revisions would not require a new durable schema each time.
- 24C / D157 established explicit local relinking without predecessor discovery or whole-history traversal.
- 25A–25B proved the same edge-v1 representation is repeatable after one edge is loaded.
- 34B / D180 later added a changed-basis revision-root predecessor to the same edge-v1 schema rather than inventing edge v2.

Conclusion: **no end-to-end substitute demonstrated in this review; reuse the existing general edge-v1 representation and add continuation v2 only as an explicitly supported predecessor family.**

## No edge v2

49I does not add:

`pyxis.chromium.research_working_set_note_revision_edge.v2`

The durable edge format remains:

`pyxis.chromium.research_working_set_note_revision_edge.v1`

Its payload, edge mode, revised-note mode, canonical encoding, record digest semantics, and no-overwrite behavior are unchanged.

Only the set of explicitly supported predecessor formats expands.

## Supported edge-v1 predecessor formats

The edge-v1 verifier now recognizes:

```text
research_working_set_note_revision_continuation.v1
research_working_set_note_revision_continuation.v2
research_working_set_note_revision_edge.v1
research_session_working_set_transition_revision_root.v1
```

This does not make every predecessor type a generic 24C input.

The 34A root remains a distinct authority type and still uses the explicit 34B bridge.

Continuation v2 is different: it is already represented by the same public 23C loaded-continuation application record as continuation v1, with its durable version retained in verification evidence.

Therefore:

```text
different durable continuation version
!=
different predecessor authority type
```

## 24B persistence becomes continuation-version aware

`persist_chromium_research_working_set_note_revision_edge(...)` still accepts one 24A extension and explicit current durable predecessor paths.

It now permits the exact loaded predecessor continuation to be either supported continuation family.

Before writing, it still:

1. re-establishes the 24A extension through public 24A;
2. freshly relinks the explicit durable continuation through public 23C;
3. requires the loaded and retained continuation formats to match;
4. constant-time compares continuation-record SHA-256 identity;
5. preserves exact member object identity;
6. writes only predecessor format + predecessor record SHA plus the new human wording/modes.

No predecessor text, working-set payload, source/member payload, or filesystem path is copied into the edge.

## Generic 24C becomes continuation-version aware

The public:

`load_chromium_research_working_set_note_revision_edge(predecessor, edge_source)`

still accepts only an already-loaded 23C continuation or an already-loaded 24C edge.

For a loaded continuation predecessor, local validation now maps exactly:

```text
continuation v1 → revision v1
continuation v2 → revision v2
```

Cross-version or unsupported continuation/revision families reject.

The rest of 24C remains unchanged:

- fresh edge-v1 file verification;
- exact predecessor-format match;
- exact predecessor-record identity match;
- public 22A reconstruction over the exact predecessor endpoint note;
- exact textual no-op rejection;
- exact working-set retention.

## Ordinary edge lineage resumes unchanged

Once the first continuation-v2-backed edge is loaded, the result is the ordinary existing:

`ChromiumPageResearchLoadedWorkingSetNoteRevisionEdgeRecord`

with edge format v1.

Existing 25A and 25B then operate unchanged:

```text
loaded continuation v2
→ 24A extension
→ 24B edge v1
→ 24C loaded edge v1
→ 25A extension
→ 25B edge v1
→ 24C loaded edge v1
→ repeat
```

No version dispatch is added to 25A or 25B.

That is the architectural point of 49I: once the explicit v2 continuation enters the already-general edge seam, ordinary repeated revision behavior is shared again.

## File integrity remains weaker than relink authority

An edge-v1 file can name:

```text
continuation-v2 format
+ a well-shaped but wrong continuation-record SHA
```

and remain file-valid after its own edge digest is recomputed.

24C rejects it when the exact supplied loaded continuation has a different durable content identity.

Likewise an edge file can be rewritten so its new wording exactly equals the real continuation-v2 endpoint and remain file-valid after digest recomputation.

24C then invokes public 22A over the exact real endpoint and rejects the textual no-op.

Thus:

```text
edge file integrity
!=
correct predecessor attachment
!=
actual revision relationship
```

## Member sidecars remain unnecessary

The first v2-backed edge persistence freshly relinks through the established durable working-set/note/revision/continuation chain.

Individual earlier member sidecars are not silently reread.

After the first edge has been loaded, 25B needs only the immediate predecessor edge file plus already-loaded application evidence; older working-set/note/revision/continuation files may be absent.

This preserves the local-current-predecessor principle.

## Focused falsification

49I tests prove:

1. the new bridge writes the existing edge-v1 format;
2. the persisted predecessor is exact continuation-v2 format + continuation-record SHA-256;
3. no earlier human wording, selected text, member/source payload, or durable path is copied into the edge;
4. the edge verifier accepts continuation v2 as a supported predecessor family;
5. an unsupported hypothetical continuation-v3 predecessor rejects even after digest recomputation;
6. generic 24C relinks the edge to the exact supplied loaded continuation-v2 object;
7. a file-valid wrong continuation-v2 digest fails 24C;
8. a file-valid exact-text no-op fails 24C/public 22A reconstruction;
9. individual member sidecars remain unnecessary for first-edge persistence;
10. existing 25A extends the loaded v2-backed edge without semantic changes;
11. existing 25B persists the successor in edge-v1 format after older pre-edge durable files disappear;
12. existing 24C reopens that successor through the ordinary edge→edge path;
13. both first and successor edges remain edge v1.

Repository Zero full-suite CI on Python 3.11–3.14 is the executable gate.

## Downstream authority remains closed

49I does not automatically widen durable sequence declarations, checkpoint products, changed-basis products, or any later record that explicitly enumerates starting predecessor formats.

A caller may begin ordinary edge processing from the loaded edge-v1 produced here.

Allowing a sequence declaration itself to start directly at continuation v2 is a separate durable product decision.

## Compatibility

Existing edge-v1 files remain valid.

49I adds one predecessor family to an already-general predecessor-reference schema; it does not reinterpret existing bytes.

This is intentionally different from earlier working-set/note/revision/continuation v1 contracts, whose durable schemas paired directly with one exact predecessor version and therefore required explicit v2 formats.

## Non-goals

49I adds no:

- edge v2;
- parallel loaded-edge type;
- automatic history discovery;
- recursive ancestry audit;
- global current/latest/head model;
- sequence-format widening;
- timestamps or revision numbers;
- semantic diff;
- author/committer identity;
- signatures or authentication;
- source discovery;
- UI or CLI;
- browser authority;
- governed-session behavior.

## Acceptance statement

49I permits only this statement:

> One valid continuation-v2-backed 24A human extension can enter the existing general edge-v1 lineage through explicit durable predecessor identity, reopen through ordinary 24C, and continue through unchanged 25A/25B edge behavior without introducing a new edge format or stronger history authority.
