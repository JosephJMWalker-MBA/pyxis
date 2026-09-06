# Milestone 49G — durable continuation of v2 rationale revisions

Decision: **D252**  
Issue: **#228**

## Concrete researcher action

49F makes one append-only revision durable over a note-v2 predecessor.

Its executable-evidence correction also established that the existing 23A in-memory continuation action can consume either exact supported loaded revision family.

49G closes the next narrow gap:

> I revised the v2 rationale once, then changed that revised wording again. Preserve this second human change against the exact durable revision-v2 predecessor without mutating prior wording.

The v2 line now reaches:

```text
durable working set v2
→ durable note v2
→ durable revision v2
→ in-memory 23A continuation
→ durable continuation v2
→ file-local verification
→ explicit predecessor relinking through 23C
```

## Internal prior art

23A already owns the human action.

It retains the exact loaded predecessor revision, creates a new public 22A revision over that predecessor's revised note, rejects an exact textual no-op, and performs no file reads.

23B already owns durable continuation-v1 mechanics.

23C already owns fail-closed relinking of one continuation-v1 sidecar against one explicit durable revision-v1 predecessor.

49G therefore introduces no new continuation model.

It versions only the durable predecessor-revision contract.

## External prior art

W3C PROV-O defines `prov:wasRevisionOf` as a derivation relationship in which the resulting entity is a revised version of an original. Repeated explicit revision relations support provenance chains without requiring earlier entities to be overwritten.

The W3C Web Annotation Protocol demonstrates a contrasting mutable-server model: an annotation update replaces the annotation state through PUT, with `If-Match` available to avoid conflicting replacement.

Pyxis keeps its established append-only human-action model rather than replacing earlier rationale wording.

Conclusion: **no end-to-end substitute demonstrated in this review; reuse 23A–23C append-only mechanics and version only the durable predecessor-revision contract.**

## Continuation v1 remains frozen

The existing writer:

`persist_chromium_research_working_set_note_revision_continuation(...)`

continues to produce only:

`pyxis.chromium.research_working_set_note_revision_continuation.v1`

with predecessor:

`pyxis.chromium.research_working_set_note_revision.v1`

It does not auto-upgrade when supplied a revision-v2 predecessor.

Existing continuation-v1 bytes and reader expectations remain unchanged.

## Explicit continuation v2 writer

49G adds:

`persist_chromium_research_working_set_note_revision_continuation_v2(...)`

which writes:

`pyxis.chromium.research_working_set_note_revision_continuation.v2`

and requires its explicit predecessor to freshly relink through version-aware 22C as:

`pyxis.chromium.research_working_set_note_revision.v2`

The caller therefore chooses the durable continuation family explicitly.

## Exact version pairing

The pairings are:

```text
continuation v1 → revision v1
continuation v2 → revision v2
```

The v1 writer rejects revision v2.

The v2 writer rejects revision v1.

No format is inferred from the supplied object graph.

## Durable continuation-v2 record

v2 preserves the established minimal shape:

```text
format:
  pyxis.chromium.research_working_set_note_revision_continuation.v2

continuation_record:
  prior_revision_reference:
    format:
      pyxis.chromium.research_working_set_note_revision.v2
    revision_record_sha256

  continuation:
    mode:
      caller_authored_continuation_of_verified_research_working_set_note_revision

    revision:
      mode:
        caller_authored_revision_of_research_working_set_note

      revised_note:
        mode:
          caller_authored_note_on_research_working_set
        text:
          exact new human wording

continuation_record_sha256
```

It does not copy:

- predecessor revision wording;
- predecessor note wording;
- working-set identity;
- working-set members;
- selected/source evidence;
- member/source paths;
- timestamps;
- revision numbers;
- inferred reasons for change.

The predecessor revision remains the durable owner of the previous revision state.

## Shared persistence mechanics

Continuation-v1 and continuation-v2 writers delegate to one private procedure.

The shared procedure:

1. requires one exact 23A continuation record;
2. re-establishes public 23A over the retained predecessor;
3. checks continuation/revision/note modes;
4. requires exact predecessor revised-note and working-set object relationships;
5. freshly relinks the explicit predecessor through version-aware 22C;
6. requires the writer-specific predecessor revision format;
7. constant-time compares predecessor revision identity with the retained loaded predecessor;
8. preserves exact supplied member objects;
9. writes deterministic canonical no-overwrite JSON.

Only continuation format and required predecessor revision format vary.

## Generic continuation verification

The established:

`verify_chromium_research_working_set_note_revision_continuation(source)`

now recognizes exactly:

- continuation v1;
- continuation v2.

Its verification evidence preserves the exact file format.

The verifier derives the permitted predecessor revision family from the continuation format.

A self-consistent continuation-v1 file that names revision v2 therefore rejects, as does the reverse pairing.

## File-local integrity remains weaker than continuation authority

The verifier opens only the continuation sidecar.

It can prove canonical structure, version pairing, modes, digest shapes, non-whitespace new wording, outer record SHA-256, and canonical bytes.

It cannot prove:

- that the predecessor digest identifies the caller's actual predecessor revision;
- that the new wording actually differs from the predecessor's revised wording.

Those relationships require explicit 23C relinking.

## 23C becomes continuation-version aware

The existing:

`load_chromium_research_working_set_note_revision_continuation(...)`

now accepts either continuation family.

It:

1. freshly verifies the continuation sidecar;
2. derives the exact required predecessor revision family;
3. freshly relinks the explicit predecessor through version-aware 22C;
4. compares predecessor revision format;
5. constant-time compares predecessor revision-record SHA-256;
6. reconstructs public 23A over that exact loaded predecessor;
7. public 22A re-establishes exact textual inequality;
8. preserves exact new human wording and exact supplied working-set member objects.

No second loader is introduced.

## Wrong predecessor identity remains visible

A continuation-v2 file may be changed to contain a different well-shaped predecessor digest and then have its outer digest recomputed.

File-local verification can still succeed.

23C then freshly loads the explicit predecessor revision-v2 sidecar and rejects the mismatch.

Thus:

```text
continuation file integrity
!=
predecessor identity correctness
```

## Exact textual no-op remains a relinking failure

Likewise, the continuation-v2 file can be changed so its new wording exactly equals the real predecessor revision wording, with a recomputed outer digest.

File-local verification still has no predecessor text and therefore succeeds.

23C reconstructs public 23A, which reconstructs public 22A, and the exact textual no-op is rejected.

Thus:

```text
structurally valid new wording
!=
actual human revision step
```

## Individual member sidecars remain unnecessary

A revision-v2 predecessor may ultimately depend on a v2 working set containing bare 49B selections.

After those members have already been successfully relinked, their individual sidecars can be absent.

Continuation-v2 persistence and 23C relinking operate through retained loaded evidence plus the explicit durable working-set/note/revision chain; they do not discover or reread the missing member sidecars.

## Exact human wording remains verbatim

Whitespace, Unicode, line breaks, punctuation, tentative language, and uncertainty are retained exactly.

Pyxis adds no semantic diff, confidence score, correction classification, or reason-for-change inference.

## Downstream revision-edge/history stays closed

49G does not widen 24B or later revision-edge/history products.

The existing revision-edge persistence boundary names continuation v1 as its continuation predecessor family.

A continuation-v2 artifact can now persist, verify, and relink through 23C, but that does not grant authority to enter v1-only downstream history products.

A later milestone must justify and version that boundary separately if the researcher needs it.

## Focused falsification

49G tests demonstrate:

1. explicit continuation-v2 persistence over an actual revision-v2 predecessor;
2. minimal predecessor-revision identity plus exact new wording only;
3. no copied predecessor note/revision wording, working-set/member/source payload, or paths;
4. exact continuation-v2/revision-v2 pairing;
5. v1 writer rejects revision-v2 predecessor;
6. v2 writer rejects revision-v1 predecessor;
7. generic verification rejects both cross-version pairings even with recomputed digest;
8. 23C relinks v2 to the exact explicit revision-v2 predecessor;
9. exact supplied member identity and deliberate duplicate bare-selection positions survive;
10. file-valid wrong predecessor digest fails 23C;
11. file-valid exact textual no-op fails 23C/23A/22A reconstruction;
12. member sidecars are not reread after earlier relinking;
13. v2 persistence is deterministic and no-overwrite;
14. the mature continuation-v1 suite remains unchanged.

Repository Zero full-suite CI on Python 3.11–3.14 remains the executable gate.

## Compatibility

49G adds one explicit durable continuation version and additive generic verification/relinking support.

It changes no:

- 23A in-memory semantics established by the 49F correction;
- revision v1/v2 formats;
- note v1/v2 formats;
- working-set v1/v2 formats;
- exact no-op rule;
- existing continuation-v1 bytes;
- source/member discovery policy;
- browser behavior;
- UI;
- CLI;
- governed-session behavior.

## Next boundary

The v2 rationale line now has two durable human wording transitions:

```text
note v2
→ revision v2
→ continuation v2
```

The next old-line product is the general revision-edge/history layer beginning at 24A–24B.

That boundary remains deliberately v1-only where it names a continuation predecessor.

Before extending it, development should ask whether the researcher actually needs the durable v2 rationale chain to enter general revision-edge/history machinery, rather than inferring that requirement from numerical symmetry.

## Non-goals

49G adds no:

- automatic continuation migration;
- mutation of v1 continuation files;
- revision-edge/history/sequence versioning;
- timestamps;
- revision numbers;
- semantic diff;
- machine reason-for-change inference;
- presentation/UI change;
- governed-session promotion;
- CLI;
- source discovery;
- citation authority;
- semantic-support authority;
- authorship/authenticity/trusted-time authority.

## Acceptance statement

49G permits only this statement:

> One existing 23A human continuation can be explicitly persisted and relinked against one exact durable revision-v2 predecessor through a new `research_working_set_note_revision_continuation.v2` contract. Continuation v1 remains frozen, predecessor correctness and exact-text continuation validity are still earned by explicit relinking, and downstream revision-edge/history authority remains closed.
