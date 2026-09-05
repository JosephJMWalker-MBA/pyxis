# Milestone 49E — durable human rationale over v2 working sets

Decision: **D250**  
Issue: **#224**

## Concrete researcher action

49D made the expanded 49C working set durable through an explicit `research_working_set.v2` format.

The human action over that set already existed in memory through 21A:

> Write one overall rationale, question, reminder, or interpretation about why this exact ordered working set is being carried forward.

49E makes that existing 21A action durable and explicitly relinkable when its durable parent is v2.

It does not change what the human text means.

## Product boundary

```text
exact 49C working set
→ explicit v2 working-set persistence
→ exact 21A human-authored working-set note
→ explicit v2 working-set-note persistence
→ file-local verification
→ explicit supplied v2 working set + members
→ 21C relinking
→ reconstructed 21A human note
```

while:

```text
durable rationale
!= source evidence
!= member interpretation
!= semantic support
!= citation
!= trusted provenance
```

## Existing in-memory action required no change

`create_chromium_research_working_set_note(...)` already validates its parent through public 20A.

Because 49C extended 20A membership, 21A already accepts working sets that contain bare 49B exact-range selections.

49E does not add another note constructor.

It versions only the durable parent-reference contract.

## Why note v1 remains frozen

The established note format:

`pyxis.chromium.research_working_set_note.v1`

requires parent:

`pyxis.chromium.research_working_set.v1`

The original v1 verifier rejects a v2 parent.

Allowing a v2 parent under a file still labeled note v1 would therefore produce bytes that old v1 readers reject while claiming to use the old contract.

49E keeps:

`persist_chromium_research_working_set_note(...)`

v1-only.

It does not inspect the supplied parent and silently upgrade.

## Explicit note v2 writer

49E adds:

`persist_chromium_research_working_set_note_v2(...)`

which writes:

`pyxis.chromium.research_working_set_note.v2`

and requires the explicitly supplied parent to freshly relink through 20C as:

`pyxis.chromium.research_working_set.v2`

The format choice is therefore caller-visible.

## v2 note record

The v2 record retains the same narrow shape as v1:

```text
format:
  pyxis.chromium.research_working_set_note.v2

note_record:
  working_set_reference:
    format:
      pyxis.chromium.research_working_set.v2
    working_set_record_sha256

  note:
    mode:
      caller_authored_note_on_research_working_set
    text:
      exact caller text

note_record_sha256
```

The note does not copy the working-set member list.

It does not copy:

- selected text;
- paragraph/range coordinates;
- member-sidecar identities;
- source capture identities;
- URLs;
- source/member paths;
- member-level note text;
- comparison payloads.

The durable working-set parent owns its own membership representation.

## Shared persistence mechanics

The v1 and v2 writers delegate to one private persistence procedure.

That procedure:

1. requires the established 21A note type;
2. reconstructs public 21A over the exact parent;
3. freshly relinks the caller-supplied durable working set through version-aware 20C;
4. requires the exact writer-specific parent format;
5. requires exact supplied member object identity at every position;
6. writes canonical no-overwrite JSON.

The only writer-specific inputs are:

- note format;
- required parent working-set format.

This shares mechanics without weakening version semantics.

## Exact parent membership is preserved

For a v2 note whose parent contains:

```text
bare selection A
paragraph note B
bare selection A
```

20C must reconstruct that exact ordered parent using those exact supplied loaded objects before note persistence is permitted.

The note therefore attaches to durable parent identity earned from the exact supplied working set.

It does not discover or substitute another set.

## Generic verifier, exact version pairing

The established:

`verify_chromium_research_working_set_note(source)`

now recognizes exactly:

- `research_working_set_note.v1`;
- `research_working_set_note.v2`.

The pairing rule is exact:

```text
note v1
→ working-set v1

note v2
→ working-set v2
```

A canonical self-consistent v1 note that claims a v2 parent rejects.

A canonical self-consistent v2 note that claims a v1 parent also rejects.

v2 is not a generic “newer reader accepts anything” mode. It exists specifically for the v2 parent contract.

## File verification remains file-local

As with 21B, generic note verification reads only the note sidecar.

It verifies:

- exact supported note version;
- exact matching parent-version family;
- parent record digest shape;
- note mode;
- non-whitespace exact human text;
- note-record SHA-256;
- canonical bytes.

It does not open the parent working set.

A self-consistent note may therefore contain a wrong but well-shaped parent digest and pass file-local verification.

Parent correctness is earned later through 21C.

## 21C becomes note-version aware

The existing:

`load_chromium_research_working_set_note(...)`

now accepts either exact note version.

It derives the required parent format from the verified note format, then:

1. freshly verifies the note sidecar;
2. freshly loads the explicit working-set parent through version-aware 20C;
3. requires parent format equality;
4. compares exact parent record SHA-256;
5. reconstructs public 21A over the exact 20C working-set object;
6. preserves the exact human text.

No second loader is introduced.

## Member sidecars remain unnecessary after earlier relinking

The v2 parent may contain a 49B bare selection whose 49A selection sidecar is no longer present.

That does not block note persistence or note relinking after the member has already crossed 49B and the working set has already crossed 49D.

The chain is:

```text
member sidecar
→ member relinking
→ loaded member application evidence
→ durable v2 working set
→ durable v2 working-set note
```

Later layers do not silently pretend to perform earlier fresh verification.

## Human text remains verbatim

49E preserves the established 21A/21B rule.

Leading and trailing whitespace, punctuation, Unicode, and line breaks remain exact.

The system does not normalize, summarize, classify, or infer a rationale.

## Wrong parent digest remains a relinking failure

A note v2 whose parent digest has been changed and whose note-record digest has been recomputed can pass file-local note verification.

21C then freshly loads the caller-supplied v2 working set and rejects the note because the durable parent identities differ.

Thus:

```text
note-file integrity
!=
parent attachment correctness
```

remains explicit.

## Revision v1 remains closed

49E deliberately does not widen:

`pyxis.chromium.research_working_set_note_revision.v1`

That format requires predecessor:

`pyxis.chromium.research_working_set_note.v1`

A v2 note can therefore:

- persist;
- verify;
- relink through 21C;

but cannot become the durable predecessor of revision v1.

The existing 22B persistence boundary rejects it before writing a revision file.

This preserves:

```text
durable rationale over v2 working set
!=
durable revision history over v2 rationale
```

## Prior art

The W3C Web Annotation Data Model distinguishes annotation Bodies—the descriptive material that is about a Target—from ordered Annotation Collections and their collection-level description. That supports the general separation between organized selected material and human description about it.

Zotero supports creating notes from multiple annotations and selectively adding multiple annotations to one note, demonstrating the common research workflow of organizing selected evidence and then writing one broader note across it.

Hypothesis distinguishes highlights from note-bearing annotations, further supporting the separation between selected evidence and human commentary.

These systems establish the product action but not Pyxis's exact durable identity or fail-closed supplied-parent relinking rules.

Conclusion: **no end-to-end substitute demonstrated in this review; reuse 21A–21C mechanics and version only the durable parent-reference contract.**

## Focused falsification

49E tests prove:

1. the existing v1 note writer remains unchanged;
2. the v1 writer still rejects a v2 parent;
3. the explicit v2 writer persists exact human rationale over a v2 parent containing bare selections;
4. v2 stores only durable parent identity plus note mode/text;
5. v2 does not copy selected/member/source payloads or paths;
6. exact whitespace, Unicode, punctuation, and line breaks survive;
7. generic verification accepts valid v1 and v2;
8. v1-note/v2-parent pairing rejects;
9. v2-note/v1-parent pairing rejects;
10. neither writer auto-upgrades or downgrades;
11. 21C relinks a v2 note to the exact supplied v2 parent and member objects;
12. a file-valid wrong parent digest fails during 21C relinking;
13. v2 note persistence and relinking do not reread individual member sidecars;
14. revision v1 persistence rejects a v2 note predecessor before writing.

Repository Zero full-suite CI on Python 3.11–3.14 remains the executable gate.

## Compatibility

49E adds one explicit durable note format and additive generic read/relink support.

It changes no:

- 21A in-memory note semantics;
- working-set v1/v2 file formats;
- 49A/49B exact selection semantics;
- existing v1 note bytes;
- source/member discovery rules;
- revision v1 semantics;
- browser behavior;
- UI;
- CLI;
- governed-session behavior.

## Next boundary

The next distinct researcher action is revision:

> I wrote an overall rationale over a durable v2 working set, then changed my interpretation. Can I preserve that change as an explicit durable revision without rewriting the predecessor?

That requires versioning the durable revision predecessor contract.

It is not part of 49E.

## Non-goals

49E adds no:

- automatic note version upgrade;
- mutation of old note files;
- revision v2;
- sequence/edge/history evolution;
- rationale presentation changes;
- UI;
- CLI;
- governed-session promotion;
- source discovery;
- quote copying;
- fuzzy anchoring;
- citation authority;
- semantic support;
- authorship/authenticity/trusted-time authority.

## Acceptance statement

49E permits only this statement:

> One existing human-authored 21A rationale can be explicitly persisted and relinked over one exact durable `research_working_set.v2` parent through a new `research_working_set_note.v2` contract. The original v1 note contract remains frozen, parent correctness is still earned by explicit relinking, and downstream durable revision/governed-session authority remains closed.
