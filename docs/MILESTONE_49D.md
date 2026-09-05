# Milestone 49D — versioned durable working sets with bare selections

Decision: **D249**  
Issue: **#222**

## Concrete researcher action

49C lets already-relinked bare exact-range selections participate in the existing human-owned 20A working-set action in memory.

49D makes that expanded working set durable without redefining the established v1 file contract.

The researcher can now explicitly choose:

```text
established three-family working set
→ existing v1 writer

expanded working set, including bare 49B selections
→ explicit v2 writer
```

The choice of durable format is visible in the API.

## Why v1 stays frozen

`pyxis.chromium.research_working_set.v1` was established with exactly three member kinds:

- `paragraph_note`;
- `exact_range_note`;
- `comparison_note`.

Older v1 readers reject any other member vocabulary.

Adding `exact_range_selection` under the same format identifier would therefore create a file that claims to be v1 while violating the original v1 reader contract.

49D refuses that shortcut.

The established:

`persist_chromium_research_working_set(...)`

remains v1-only and continues to reject a 49C working set containing a bare selection.

## Explicit v2 writer

49D adds:

`persist_chromium_research_working_set_v2(...)`

which writes exactly:

`pyxis.chromium.research_working_set.v2`

The writer does not auto-select itself.

A caller who wants the expanded durable format must choose it explicitly.

Thus:

```text
member contents
!=
authority to silently upgrade format version
```

## v2 member vocabulary

v2 supports all four current 20A member families:

```text
paragraph_note
  → pyxis.chromium.research_paragraph_note.v1

exact_range_selection
  → pyxis.chromium.research_paragraph_text_selection.v1

exact_range_note
  → pyxis.chromium.research_paragraph_text_selection_note.v1

comparison_note
  → pyxis.chromium.research_paragraph_text_selection_comparison_note.v1
```

The new bare-selection member identity comes directly from the retained 49A verification inside the 49B loaded record:

- `selection_format`;
- `selection_record_sha256`.

No second identity scheme is introduced.

## Durable representation remains minimal

Like v1, v2 stores each member only as:

```text
member_kind
member_format
member_record_sha256
```

The working-set file still does not copy:

- selected text;
- paragraph coordinates;
- source capture format or digest;
- URL;
- source/member paths;
- human note text;
- comparison payloads.

Each member's own sidecar remains the authority for its durable content representation.

## Shared persistence mechanics

v1 and v2 reuse one private persistence procedure for:

- explicit destination resolution;
- existing-parent requirement;
- canonical working-set record projection;
- SHA-256 calculation;
- canonical UTF-8 JSON;
- one trailing newline;
- exclusive-create no-overwrite semantics;
- persistence evidence retaining the exact supplied working-set object.

The only format-specific inputs are:

- exact working-set format string;
- member-reference projector.

This shares mechanics without merging member semantics.

## v2 live validation

Before writing v2, Pyxis re-establishes the complete 49C in-memory working-set contract through public 20A.

Each member must then project to an allowed v2 durable reference.

For a bare selection, the retained 49A selection format and record digest must have the established shape.

No individual member sidecar is reread.

## One verifier for two explicit contracts

The existing:

`verify_chromium_research_working_set(source)`

now recognizes exactly:

- `pyxis.chromium.research_working_set.v1`;
- `pyxis.chromium.research_working_set.v2`.

The returned verification evidence preserves the exact verified format string.

Validation dispatches member vocabulary by format.

### v1

Allowed:

- paragraph note;
- exact-range note;
- comparison note.

### v2

Allowed:

- all v1 kinds;
- exact-range selection.

Therefore a canonical, self-consistent file labeled v1 that contains `exact_range_selection` still fails.

This is the primary old-reader compatibility proof.

## File integrity remains file-local

As in 20B, verification checks:

- top-level shape;
- exact supported format;
- working-set mode;
- non-empty ordered member list;
- member kind/format compatibility for that version;
- member record digest shape;
- working-set record digest;
- canonical bytes.

It still does not read any referenced member sidecar.

A self-consistent v2 file can therefore retain a wrong-but-well-shaped member digest and pass file-local verification.

Correct member identity is still earned during explicit 20C relinking.

## 20C becomes version-aware

The existing:

`load_chromium_research_working_set(...)`

now relinks either v1 or v2 after fresh generic verification.

It still requires the caller to supply the complete ordered loaded-member sequence.

For a bare-selection position, the observed durable reference is reconstructed from the supplied 49B record's retained:

- selection format;
- selection record SHA-256.

The expected and observed member references must match in:

- kind;
- format;
- record digest.

No member is discovered by path, URL, digest search, source identity, note text, or browser state.

## Exact supplied member identity remains preserved

After successful relinking, the reconstructed 20A working set retains the exact supplied member objects.

Intentional duplicates remain duplicates.

For example:

```text
bare A
paragraph note B
bare A
```

round-trips as the same three supplied objects in the same positions.

## Individual member files remain unnecessary after loading

49D preserves the established 20C rule.

Once members have already been successfully relinked into application evidence, their individual sidecar files may be absent and the durable working-set sidecar can still be relinked against those loaded objects.

For a bare selection:

```text
49A sidecar available
→ 49B relink succeeds
→ 49A sidecar later absent
→ v2 working-set relinking can still use retained 49B evidence
```

This does not claim the missing member file can itself be freshly reopened.

## Wrong member identity remains a later failure

A v2 file with a recomputed working-set digest but a wrong well-shaped bare-selection record SHA-256 may pass file-local verification.

When the caller supplies the actual 49B loaded selection, 20C rejects because the expected and observed member record digests differ.

Thus:

```text
v2 file integrity
!=
v2 member identity correctness
```

## 21B remains v1-only

49D deliberately does not widen durable working-set-note persistence.

`persist_chromium_research_working_set_note(...)` still requires its durable working-set parent to be:

`pyxis.chromium.research_working_set.v1`

A v2 working set may be loaded successfully by 20C, but 21B then rejects the parent format before writing a working-set-note sidecar.

This keeps:

```text
durable expanded working set
!=
durable human rationale over expanded working set
```

visible as a separate authority boundary.

## Prior art and reuse

The W3C Web Annotation model establishes ordered collections of annotation identities, including annotations that need not carry textual commentary.

Hypothesis and Zotero demonstrate durable highlight-first workflows where note-free selections can remain first-class research objects and later participate in broader organization or notes.

Those systems support the product action but do not replace Pyxis's exact canonical JSON, durable identity, or explicit supplied-member relinking contract.

Internally, 20B and 20C already own nearly all required mechanics.

Conclusion: **no end-to-end substitute demonstrated in this review; reuse 20B/20C mechanics while adding an explicit new format version rather than silently changing v1.**

## Focused falsification

49D tests prove:

1. existing v1 persistence behavior remains intact;
2. the v1 writer still rejects a bare selection;
3. explicit v2 persistence accepts mixed bare and note-bearing members;
4. v2 preserves caller order and duplicates;
5. v2 copies no selected text, human note text, source identity, or paths;
6. generic verification preserves exact v1/v2 format identity;
7. v1 rejects a self-consistent v2-only member kind;
8. v2 rejects a bare member with the wrong member format;
9. v2 persistence remains deterministic and no-overwrite;
10. v2 20C relinking preserves exact supplied member objects;
11. v2 relinking does not reread individual member sidecars;
12. a file-valid wrong bare-member digest fails during member relinking;
13. changed caller order fails closed;
14. 21B still rejects a v2 parent before writing a note sidecar.

Repository Zero full-suite CI on Python 3.11–3.14 remains the executable gate.

## Compatibility

49D adds one new explicit durable format while preserving the existing v1 writer and v1 files.

It changes no:

- 49A selection format;
- 49B source relinking;
- 49C in-memory working-set behavior;
- original v1 member vocabulary;
- note/comparison member formats;
- source/member discovery policy;
- browser behavior;
- governed-session behavior;
- UI;
- CLI.

## Expected next boundary

The next concrete question is now:

> Can a researcher persist one overall human rationale over a durable v2 working set containing bare selections?

That requires explicit evolution of the working-set-note parent-format contract.

49D does not pre-authorize how that note format should version or how later rationale-revision/presentation products should consume it.

## Non-goals

49D adds no:

- automatic v1→v2 upgrade;
- mutation of existing v1 files;
- selection-collection parallel format;
- 21B note-format evolution;
- rationale-revision format evolution;
- presentation/UI change;
- governed-session promotion;
- CLI;
- source discovery;
- quote copying;
- fuzzy re-anchoring;
- citation authority;
- semantic-support authority;
- authorship/authenticity/trusted-time authority.

## Acceptance statement

49D permits only this statement:

> Pyxis can explicitly persist and relink expanded 49C working sets through a new `research_working_set.v2` contract while preserving the original v1 writer and member vocabulary, keeping format choice caller-visible, reusing established file-integrity and member-relinking mechanics, and leaving durable rationale/governed-session authority closed.
