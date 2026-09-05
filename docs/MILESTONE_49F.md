# Milestone 49F — durable revisions of v2 working-set rationale

Decision: **D251**  
Issue: **#226**

## Concrete researcher action

49E makes one overall human rationale durable over an exact v2 working set.

22A already lets the researcher change that rationale in memory without mutating the prior wording.

49F makes that append-only human change durable when the predecessor is a note-v2 artifact.

The product action is:

```text
durable note v2
→ human changes exact wording
→ prior wording remains immutable
→ explicit revision v2
→ file-local verification
→ explicit predecessor relinking
→ reconstructed 22A revision
```

## In-memory revision required no change

The 22A constructor is deliberately about application-level human revision rather than durable-format versions.

It takes one 21A note object, re-establishes that note through 21A/20A, requires non-whitespace revised text, rejects an exact textual no-op, and creates a new 21A note over the exact same working-set object.

A note reconstructed from note v2 by 49E/21C is therefore already a valid 22A predecessor.

49F does not create another revision constructor.

## Prior art

W3C PROV-O defines `prov:wasRevisionOf` as a derivation relationship in which one entity is a revised version of another. That model supports preserving an explicit predecessor rather than replacing it invisibly.

The W3C Web Annotation Protocol also demonstrates the more conventional mutable-server alternative, where updating an annotation replaces its state through PUT. Pyxis deliberately does not use that overwrite model for rationale history because 22A already established prior wording as retained human-action provenance.

Conclusion: **no end-to-end substitute demonstrated in this review; reuse 22A–22C append-only mechanics and version only the durable predecessor-note contract.**

## Why revision v1 remains frozen

The established format:

`pyxis.chromium.research_working_set_note_revision.v1`

requires predecessor:

`pyxis.chromium.research_working_set_note.v1`

Old revision-v1 readers reject a note-v2 predecessor.

Allowing note v2 inside a file still labeled revision v1 would therefore silently redefine the old contract.

49F keeps:

`persist_chromium_research_working_set_note_revision(...)`

exactly v1/note-v1.

It never auto-upgrades.

## Explicit revision v2 writer

49F adds:

`persist_chromium_research_working_set_note_revision_v2(...)`

which writes:

`pyxis.chromium.research_working_set_note_revision.v2`

and requires the supplied durable predecessor to freshly relink through 21C as:

`pyxis.chromium.research_working_set_note.v2`

The caller chooses the revision format explicitly.

## Durable revision v2 record

v2 preserves the established minimal shape:

```text
format:
  pyxis.chromium.research_working_set_note_revision.v2

revision_record:
  prior_note_reference:
    format:
      pyxis.chromium.research_working_set_note.v2
    note_record_sha256

  revision:
    mode:
      caller_authored_revision_of_research_working_set_note

    revised_note:
      mode:
        caller_authored_note_on_research_working_set
      text:
        exact revised human wording

revision_record_sha256
```

It does not copy:

- predecessor note text;
- working-set identity;
- working-set members;
- selected/source evidence;
- member/source paths;
- timestamps;
- revision numbers;
- inferred reason for change.

The predecessor note remains the durable owner of its earlier wording and working-set attachment.

## Shared writer mechanics

Revision v1 and v2 delegate to one private persistence procedure.

The shared procedure:

1. re-establishes the live 22A revision;
2. checks revision and note modes;
3. requires revised/prior notes to retain the exact same working-set object;
4. freshly relinks the explicit predecessor through version-aware 21C;
5. requires the writer-specific predecessor note format;
6. compares exact predecessor note mode/text;
7. preserves exact member object identity;
8. writes deterministic canonical no-overwrite JSON.

The format-specific values are only:

- revision format;
- required predecessor note format.

This shares procedure while retaining concrete version semantics.

## No auto-upgrade or downgrade

The pairings are exact:

```text
revision v1
→ note v1

revision v2
→ note v2
```

The v1 writer rejects a note-v2 predecessor.

The v2 writer rejects a note-v1 predecessor.

This keeps format selection visible rather than inferred from input.

## Generic revision verification

The established:

`verify_chromium_research_working_set_note_revision(source)`

now recognizes exactly:

- revision v1;
- revision v2.

Its returned verification evidence preserves the exact revision format found in the file.

The verifier derives the allowed predecessor note format from that revision format and rejects cross-version pairings.

## File-local integrity remains weaker than revision authority

Revision verification opens only the revision sidecar.

It can validate:

- exact supported revision version;
- exact predecessor-note version family;
- digest shapes;
- revision/note modes;
- non-whitespace revised text;
- revision-record SHA-256;
- canonical bytes.

It does not open the predecessor note.

Therefore it cannot prove:

- the predecessor digest names the real supplied predecessor;
- the revised wording differs from the real predecessor wording.

Both relationships are re-earned by 22C.

## 22C becomes revision-version aware

The existing:

`load_chromium_research_working_set_note_revision(...)`

now accepts revision v1 or v2.

It maps:

```text
revision v1 → required note v1
revision v2 → required note v2
```

and then:

1. freshly verifies the revision sidecar;
2. freshly relinks the explicit predecessor note through version-aware 21C;
3. compares predecessor note format;
4. constant-time compares predecessor note-record SHA-256;
5. reconstructs public 22A over the exact fresh predecessor note;
6. re-establishes exact textual inequality;
7. preserves the exact revised wording.

No second loader is added.

## Exact textual no-op remains rejected only where authority exists

A revision-v2 file can be tampered so that its revised text equals the real predecessor text, with the outer digest recomputed.

File-local verification still succeeds because the predecessor text is not duplicated in the revision file.

22C then opens/relinks the real predecessor and calls public 22A.

22A sees:

```text
revised text == prior text
```

and rejects the reconstruction.

Thus:

```text
revision file integrity
!=
actual revision relationship
```

remains falsifiable.

## Wrong predecessor identity remains a 22C failure

Likewise, a revision-v2 file may contain a wrong but well-shaped predecessor digest and remain self-consistent after recomputation.

22C freshly relinks the caller-supplied note-v2 predecessor and rejects because its actual durable identity differs.

Thus:

```text
valid predecessor-shaped digest
!=
correct predecessor
```

## Individual member files remain unnecessary after prior relinking

A v2 predecessor note may sit over a v2 working set containing bare 49B selections.

The earlier individual member sidecars can be absent after their successful relinking.

Revision-v2 persistence and 22C relinking operate through the established layered chain:

```text
loaded members
→ durable v2 working set
→ durable note v2
→ durable revision v2
```

They do not silently reread member files.

## Exact human wording remains verbatim

The revised text remains caller-owned.

Whitespace, Unicode, line breaks, punctuation, uncertainty, and tentative phrasing are preserved exactly.

No semantic diff, correction, confidence score, or reason-for-change field is inferred.

## 23A remains an in-memory action across explicit revision versions

Repository Zero exposed one important boundary during 49F CI: the existing 23A constructor rejected a freshly loaded revision-v2 predecessor before the intended 23B persistence gate could be exercised.

That was stricter than the already-established separation between in-memory human action and durable format choice.

49F therefore makes **only the in-memory 23A predecessor validation** version-aware across the two explicit 22C families:

```text
revision v1 → note v1
revision v2 → note v2
```

23A still performs no persistence and introduces no continuation-v2 file format. It simply permits the same human action — “revise this already-loaded revision again” — over either supported loaded revision family while re-establishing the exact revision/note pairing and retained object graph.

This mirrors the earlier 22A result: application-level human revision mechanics need not inherit durable file-version restrictions.

## Continuation v1 remains closed

49F deliberately does not widen:

`pyxis.chromium.research_working_set_note_revision_continuation.v1`

That format requires predecessor:

`pyxis.chromium.research_working_set_note_revision.v1`

A revision-v2 artifact can therefore:

- persist;
- verify;
- relink through 22C;
- participate in the in-memory 23A continuation action;

but cannot become a continuation-v1 durable predecessor.

The existing 23B persistence boundary rejects it before writing.

This preserves:

```text
in-memory second human change
!=
durable versioned multi-step revision history
```

## Focused falsification

49F tests prove:

1. existing revision-v1 behavior remains intact;
2. revision v1 still rejects note-v2 predecessors;
3. explicit revision v2 persists a real 22A change over note v2;
4. revision v2 stores only predecessor identity plus revised wording/modes;
5. predecessor text, working-set/member/source payloads, and paths are absent;
6. exact revised whitespace/Unicode/line breaks survive;
7. generic verification accepts revision v1 and v2;
8. revision-v1/note-v2 pairing rejects;
9. revision-v2/note-v1 pairing rejects;
10. neither writer auto-upgrades/downgrades;
11. 22C relinks revision v2 to the exact supplied note-v2 predecessor;
12. a file-valid wrong predecessor digest fails 22C;
13. a file-valid exact-text no-op fails public 22A reconstruction through 22C;
14. member sidecars are not reread;
15. 23A can express a second in-memory human change over a revision-v2 predecessor while continuation-v1 persistence still rejects that predecessor before write.

Repository Zero full-suite CI on Python 3.11–3.14 remains the executable gate.

## Compatibility

49F adds one explicit durable revision version and additive generic verification/relinking support.

It also broadens only the in-memory 23A predecessor validator from revision-v1-only to the two exact supported 22C revision families.

It changes no:

- 22A in-memory revision semantics;
- note v1/v2 formats;
- working-set v1/v2 formats;
- exact no-op rule;
- old revision-v1 bytes;
- source/member discovery policy;
- continuation-v1 durable format semantics;
- browser behavior;
- UI;
- CLI;
- governed-session behavior.

## Next boundary

The next distinct human action is durable continuation:

> I revised the v2 rationale once, then changed it again. Preserve another append-only step against the exact durable revision-v2 predecessor.

The v1 product already owns that durable action through 23B–23C, while 23A now already owns the in-memory action for either explicit revision family.

Supporting durable continuation on the v2 line requires a separate continuation format version.

That is not part of 49F.

## Non-goals

49F adds no:

- automatic revision version migration;
- mutation of old revision files;
- continuation-v2 durable format;
- revision-edge/history/sequence versioning;
- timestamps;
- revision numbers;
- semantic diff;
- machine reason-for-change inference;
- presentation/UI changes;
- governed-session promotion;
- CLI;
- source discovery;
- citation authority;
- semantic-support authority;
- authorship/authenticity/trusted-time authority.

## Acceptance statement

49F permits only this statement:

> One existing append-only 22A human revision can be explicitly persisted and relinked against one exact durable note-v2 predecessor through a new `research_working_set_note_revision.v2` contract. The in-memory 23A continuation action can consume either exact supported loaded revision family, but durable continuation v1 remains frozen to revision-v1 predecessors. Predecessor correctness and exact-text revision validity are still earned by explicit relinking, and versioned multi-step durable history authority remains closed.
