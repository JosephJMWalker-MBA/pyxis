# Milestone 50B — version-aware changed-basis preparation with bare selections

Decision: **D256**  
Issue: **#240**

## Concrete researcher action

50A makes a bare saved passage faithfully visible in the normal governed working-set context.

That state exposed the next continuity boundary:

```text
declared session whose working set contains a bare saved passage
→ append explicit additional research evidence
→ author a rationale over the changed basis
→ prepare that changed basis durably
```

Established 33A already owns this preparation action, but its persistence dispatch was frozen to working-set/note v1.

A valid in-memory changed working set containing a bare exact-range selection therefore could not be prepared durably.

50B widens only the preparation dispatch needed to use the already-established v2 persistence pair.

## Prior-art and reuse decision

W3C Web Annotation permits annotations with no Body for simple highlights/bookmarks. Hypothesis treats a highlight without a note as a first-class retained state. Zotero likewise permits highlight creation independently from later note composition.

Those systems support the researcher-level distinction already adopted by 49 and 50A. They do not provide Pyxis's content-addressed changed-basis authority model.

Internally, the decisive prior art is already implemented:

- 49D / D249 introduced explicit `research_working_set.v2` for the expanded member vocabulary containing `exact_range_selection`;
- 49E / D250 introduced the matching `research_working_set_note.v2` parent contract;
- the original v1 writers deliberately remain frozen and do not auto-upgrade.

Conclusion: **reuse the existing explicit v2 pair only when the newly prepared combined member vocabulary requires it. Preserve v1 behavior otherwise. No new durable format is introduced.**

## Version selection belongs to the newly prepared basis

33A still reconstructs one ordinary in-memory 20A working set from:

```text
exact prior members
+ exact caller-supplied appended members
```

The new dispatch rule is:

```text
combined working set contains no exact_range_selection
→ persist research_working_set.v1
→ persist research_working_set_note.v1

combined working set contains >= 1 exact_range_selection
→ persist research_working_set.v2
→ persist research_working_set_note.v2
```

This rule is based only on the member vocabulary of the newly prepared working set.

It does not migrate, rewrite, infer, or preserve the version of an earlier durable working-set file.

## Two supported crossings

50B therefore covers both ordinary ways the expanded vocabulary can enter 33A.

### Retained bare passage

```text
prior session working set already contains exact_range_selection
+ append note-bearing member
→ preserve all prior members exactly
→ v2 working set + v2 rationale
```

### Newly appended bare passage

```text
prior session is v1-compatible
+ append exact_range_selection
→ preserve prior members exactly
→ append bare member exactly
→ v2 working set + v2 rationale
```

No deduplication or semantic interpretation is added.

## Existing v1 behavior remains frozen

If the combined working set contains only the original note-bearing member families, 33A still delegates to the original v1 writers.

Thus:

```text
50B compatibility
!=
always write v2
```

A caller does not receive v2 merely because v2 exists.

## Member sidecars remain unnecessary

33A still operates only over already-loaded application evidence.

The focused 50B proof removes sidecars for:

- a retained bare exact-range selection;
- a retained paragraph-note member;
- an explicitly appended paragraph-note member;
- an explicitly appended bare selection.

Preparation still succeeds because working-set persistence uses retained verified member identity rather than silently reopening member files.

No browser reacquisition is added.

## Candidate presentation remains semantically honest

50A widened the shared working-set member projection used by the changed-basis candidate presenter.

That means a candidate may now legitimately have:

```text
member_kind = exact_range_selection
human_note_text = None
```

50B updates only the existing Textual candidate summary so it renders that state as:

```text
Human note: none attached — saved source passage only
```

It does not render Python `None` as if it were human-authored content.

Existing note-bearing candidate text remains unchanged.

## Explicit stop boundary: 33B remains v1-only

The next durable changed-basis boundary still expects:

```text
research_session_working_set_transition.v1
→ successor research_working_set.v1
→ successor research_working_set_note.v1
```

50B does not change that.

A focused falsification constructs a valid v2 33A preparation, then proves existing 33B persistence rejects it before writing a transition file.

Therefore:

```text
v2-capable 33A preparation
!=
v2-capable 33B transition
```

The next review must separately determine whether transition v1 is a general content-addressed successor-reference representation that should authorize an exact v2/v2 successor pair, or whether a transition-v2 format is required.

## Focused falsification

50B tests prove:

1. a declared session whose prior working set contains bare selections can prepare a changed basis;
2. prior members remain first and retain exact object identity;
3. appended members retain exact order and object identity;
4. retained bare membership selects working-set v2 + note v2;
5. a newly appended bare selection also selects the v2/v2 pair;
6. existing note-only preparation remains exactly v1/v1;
7. generic working-set/note relinking reopens the new v2 pair;
8. retained and appended member sidecars need not remain on disk after loading;
9. the changed-basis candidate summary represents bare-note absence explicitly rather than displaying `None`;
10. existing note-bearing candidate summary text remains unchanged;
11. current 33B rejects the v2 successor pair and writes no transition artifact.

Repository Zero full-suite CI on Python 3.11–3.14 is the executable gate.

## Non-goals

50B adds no:

- new working-set format;
- new working-set-note format;
- transition-format widening;
- transition v2;
- revision-root change;
- automatic transition or adoption;
- browser selection interaction;
- browser navigation or mutation;
- source discovery;
- fuzzy anchoring;
- tags or colors;
- citation or quotation certification;
- semantic support;
- global current/latest/head authority.

## Acceptance statement

50B permits only this statement:

> A researcher can prepare a new durable changed evidence basis whose retained or newly appended members include bare exact-range selections by selecting the already-established working-set/note v2 pair, while v1-only bases continue using the frozen v1 pair, member sidecars remain unnecessary after load, and the existing 33B transition boundary remains explicitly closed to that v2 successor basis.
