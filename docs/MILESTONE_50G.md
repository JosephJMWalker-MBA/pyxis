# Milestone 50G — expose bare-selection fresh re-entry in the 44F shell

Decision: **D261**  
Issue: **#250**

## Concrete researcher action

50F proves the application-layer 35B capability:

```text
explicit capture path
+
explicit bare-selection sidecar path
→ public 16C
→ public 49B
→ fresh root-backed governed session
```

The next concrete action is to perform that already-earned proof through the existing first changed-basis 44F Textual product.

Before 50G, the 44F form could express only note-bearing appended members.

## Demonstrated product gap

The 44F controls recognized only:

```text
paragraph note
exact-range note
comparison note
```

and unconditionally rendered:

```text
Note text:
...
```

Every appended member also received a note-sidecar path input.

The shell collector likewise queried a note-sidecar input before dispatch and could only construct the three historical note-bearing re-entry locators.

A valid bare `ChromiumPageResearchLoadedParagraphTextSelectionRecord` therefore could not be submitted through 44F even though 50F made public 35B capable of reconstructing it.

## Decision

50G adapts only the existing 44F presentation and locator collector.

No 35B application logic changes.

No persistence or durable format changes.

## Bare member presentation

The 44F member presenter now recognizes:

`ChromiumPageResearchLoadedParagraphTextSelectionRecord`

as:

`exact-range selection`

and renders:

```text
Appended member N — exact-range selection
Human note: none attached — saved source passage only
Selected text:
<exact selected text>
```

This preserves the semantic distinction established by 50A.

A bare passage is not displayed as though it had a note, and Python `None` is never presented as human-authored content.

Existing note-bearing summaries remain unchanged:

```text
Appended member N — <note family>
Note text:
<exact human note text>
```

## Bare member locator fields

For a bare exact-range selection the form now mounts exactly:

```text
capture_source
selection_source
```

It does not mount:

`note_source`

and does not mount comparison-only first/second capture fields.

The selection input is explicitly labeled as the current exact-range-selection sidecar path.

## Collector behavior

The 44F shell collector now dispatches on the bare loaded member before attempting to query a note input.

It requires:

1. one explicit capture path;
2. one explicit selection-sidecar path.

It constructs the 50F typed application locator:

`ChromiumResearchExactRangeSelectionReentryLocator`

and delegates verification to the unchanged public 44F/35B application boundary.

No source path is inferred from the retained member object.

No 44A–44E receipt path is promoted automatically.

## Retryable failures

The focused product test proves the form remains retryable when:

- capture path is blank;
- selection path is blank.

In both cases:

- no 44F proof result is retained;
- the verification button remains enabled;
- the mounted governed session remains available.

This is ordinary form validation, not durable evidence failure.

## Successful proof

The executable 50G test starts from one real persisted bare selection and drives the actual product lineage:

```text
ordinary governed session
+ bare selection candidate
→ inherited 44A preparation
→ inherited 44B transition
→ inherited 44C root
→ inherited 44D edge
→ inherited 44E adoption
→ 50G 44F locator form
→ public 50F / 35B fresh reconstruction
```

After successful 44F proof:

- the retained typed locator is exactly the new 50F locator family;
- the fresh appended member is still a loaded bare exact-range selection;
- selected text matches the original range;
- the fresh member retains the explicit supplied capture evidence;
- no note object is manufactured;
- the fresh declared endpoint retains the fresh bare member in its changed working set.

## Mounted session remains unchanged

44F remains a verification action.

The shell snapshots the mounted governed controller/session before public 35B proof and requires them to remain unchanged afterward.

50G does not promote the freshly reconstructed controller into active state.

The historical 44E session remains the explicit verification subject.

## Existing note-bearing behavior remains unchanged

The paragraph-note, exact-range-note, and comparison-note branches keep their existing:

- member labels;
- note text summaries;
- capture inputs;
- note-sidecar inputs;
- locator classes;
- validation wording.

50G does not refactor those paths into a new generic UI abstraction.

## Explicit stop boundary: 35C

Successful 44F verification still writes no durable restart configuration.

The success receipt continues to state that no 35C overlay/restart locator has been written.

No 35C overlay destination control appears in the 44F shell.

The strict overlay-v1 remains unable to serialize the new locator after 50F.

A separate review must decide the durable overlay representation.

## Focused falsification

50G mechanically proves:

1. a real bare appended member is accepted by the 44F controls;
2. it is labeled as an exact-range selection;
3. note absence is explicit and `None` is not rendered as human content;
4. exact selected text is visible;
5. one capture input exists;
6. one selection-sidecar input exists;
7. no note-sidecar input exists for the bare member;
8. no comparison-only capture inputs exist;
9. blank capture input fails retryably;
10. blank selection input fails retryably;
11. successful collection creates `ChromiumResearchExactRangeSelectionReentryLocator`;
12. public 44F/35B proof succeeds;
13. the fresh appended member remains a bare exact-range selection;
14. selected text and explicit capture attachment are preserved;
15. the fresh declared endpoint retains the fresh bare member;
16. mounted controller/session remain unchanged;
17. successful controls lock;
18. no 35C overlay controls are introduced;
19. historical note-bearing 44F tests remain unchanged.

Repository Zero full-suite CI on Python 3.11–3.14 is the executable gate.

## Non-goals

50G adds no:

- 35C overlay v2;
- 35C overlay-v1 widening;
- 31B plan v2;
- 31B plan-v1 widening;
- new 35B application semantics;
- automatic launch from fresh proof;
- browser interaction;
- source discovery;
- fuzzy anchoring;
- automatic adoption;
- chronology/current/latest/head authority;
- citation or semantic-support authority.

## Acceptance statement

50G permits only this statement:

> The existing first changed-basis 44F shell can explicitly collect a capture path plus bare-selection sidecar path for one appended exact-range selection, faithfully present that member without a manufactured note, and delegate to the already-proven 50F/35B fresh reconstruction boundary while leaving the mounted governed session and durable restart configuration unchanged.
