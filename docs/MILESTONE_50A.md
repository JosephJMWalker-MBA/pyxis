# Milestone 50A — present a bare saved passage without inventing a note

Decision: **D255**  
Issue: **#238**

## Concrete researcher action

Frontier 49 made one exact caller-selected passage durable independently from interpretation and carried that passage into the existing versioned working-set and ordinary edge lineage.

The remaining product discontinuity is presentation:

```text
loaded edge v1
→ retained working set containing exact_range_selection
→ normal governed working-set context
→ visible saved passage
→ explicit absence of human note
```

Before 50A, the working-set domain and v2 persistence path accepted a bare exact-range selection, but the established read-only rationale/working-set presenter still understood only paragraph-note, exact-range-note, and comparison-note members.

That mismatch made a valid durable state unpresentable in the normal governed-session context.

## Prior-art decision

The distinction between a saved highlight and an annotation-with-comment is mature.

- W3C Web Annotation permits an Annotation with zero Bodies and explicitly describes simple highlight/bookmark use without accompanying body text.
- Hypothesis exposes Highlight as a first-class action distinct from Annotate.
- Zotero creates highlights directly from selected text; adding an annotation to a note is a separate action.

Those systems also contain broader anchoring, mutation, social, search, and interaction capabilities that Pyxis has not earned and does not import here.

Conclusion: **no end-to-end substitute demonstrated in this review; reuse the mature highlight-without-note interaction distinction while preserving Pyxis's explicit supplied-evidence and fail-closed authority model.**

## Application presentation change

`ChromiumPageResearchWorkingSetMemberPresentation` now represents:

```python
human_note_text: str | None
```

with exact semantics:

```text
None
=
no human note exists for this working-set member

""
=
a human note exists and its exact authored text is the empty string
```

The presenter adds one explicit member projection:

```text
ChromiumPageResearchLoadedParagraphTextSelectionRecord
→ member_kind = "exact_range_selection"
→ human_note_text = None
→ one exact-range source excerpt
```

No durable object is changed.

## Textual rendering change

The governed read-only working-set detail validates member-kind/note-presence coherence before rendering.

For a bare exact-range selection:

- `human_note_text` must be `None`;
- exactly one `selection` excerpt must exist;
- that excerpt must remain `exact_returned_text_range`;
- the UI shows **No human note attached — saved source passage only**;
- no note-text widget is created for that member.

For note-bearing member kinds:

- `human_note_text` must remain a string;
- an authored empty string remains valid human note text;
- existing note labels and source-excerpt rendering remain unchanged.

Thus source text is never relabeled as a human note merely to satisfy an old presentation shape.

## Sequence authority remains unchanged

50A deliberately does not widen 26A–26C sequence declarations to start directly from continuation v2.

The executable proof follows the already-earned 49I seam:

```text
continuation v2
→ first edge v1
→ ordinary successor edge v1
→ existing edge-started sequence declaration
→ normal working-set presentation
```

The successor edge retains the same v2 working set containing the bare saved passage.

This proves presentation without adding the separately declined direct continuation-v2 sequence-start authority.

## Focused falsification

50A tests prove:

1. a real continuation-v2-backed working set rejoins edge v1 and survives into an ordinary successor edge;
2. the established working-set presenter emits bare members as `exact_range_selection`;
3. the exact selected source text, URL, paragraph ordinal, and range coordinates are projected through the existing bounded excerpt representation;
4. bare members carry `human_note_text is None`;
5. note-bearing members retain their exact human text unchanged;
6. deleting member sidecars and lineage files after explicit load does not prevent presentation;
7. the sequence used for the proof starts from an ordinary loaded edge rather than widening continuation-v2 sequence authority;
8. Textual renders an explicit no-note notice and creates no fake note-text widget for bare members;
9. a bare member with string note text rejects;
10. a note-bearing member with `None` note text rejects;
11. an authored empty-string note remains distinct from absence and is accepted.

Repository Zero full-suite CI on Python 3.11–3.14 is the executable gate.

## Compatibility

No persisted bytes or durable format versions change.

Existing note-bearing presentations continue to expose exact strings.

The only application presentation widening is the explicit ability to represent a member for which no note exists.

Consumers that validate the presentation must therefore distinguish `None` from a string rather than coercing absence to empty text.

## Non-goals

50A adds no:

- persistence format;
- working-set v3;
- edge v2;
- direct continuation-v2 sequence declaration;
- synthesized note text;
- empty-string absence sentinel;
- browser selection interaction;
- browser navigation or mutation;
- highlight color or tag semantics;
- source discovery;
- fuzzy anchoring;
- citation or quotation certification;
- authorship or trusted time;
- search or indexing;
- export;
- global current/latest/head authority.

## Acceptance statement

50A permits only this statement:

> A bare exact-range selection already retained by a valid loaded working set can be shown in the normal governed read-only working-set context as saved source evidence with an explicit absence of human note, while exact note-bearing members remain unchanged and no new persistence, browser, sequence-start, or semantic authority is introduced.
